# RAG Eval Harness

> **Concrete, regression-proof quality gates for the chatbot.** Three layers of measurement per case: deterministic retrieval, deterministic answer constraints, and an LLM judge. Designed to be reusable across events (Build, Ignite, Decoded, …) — just swap the gold dataset.

## TL;DR

```bash
# From the repo root
pip install -r requirements.txt

# 1. Deterministic run (no LLM) — ~5s, free, CI-friendly
python -m evals

# 2. Add the LLM judge (uses Azure OpenAI gpt-4o) — adds groundedness +
#    attribution-fidelity scoring. Cached to disk so re-runs are free.
export AZURE_OPENAI_ENDPOINT=...
export AZURE_OPENAI_KEY=...
export AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4o
python -m evals --judge

# 3. Run against the deployed app
python -m evals --url https://build2026-chatbot-50261.azurewebsites.net

# 4. Run a single case (TDD-style)
python -m evals --case naomi-prompt-caching --judge

# 5. CI gate: exit 1 on any regression
python -m evals --strict
```

Reports land under `evals/reports/<event>-<target>-<ts>.{md,json}`.

---

## Why this design

For an enterprise rollout you need to catch **four** classes of failure that a simple "did it return the right session?" check misses:

| Failure class | Example | Caught by |
|---|---|---|
| **Wrong-speaker retrieval** | "What did Naomi say about prompt caching?" returns BRK226 (Mark) | `speaker_session_purity` |
| **Wrong-speaker attribution** | Session lists Mark; AI summary says "Marcus did X"; answer says "Mark did X" | `speaker_evidence_purity` + `must_not_contain_any` + judge `attribution_fidelity` |
| **Citation laundering** | Answer cites BRK999 (doesn't exist) or BRK226 when only BRK230 was retrieved | `citation_support`, `forbidden_citations` |
| **Confident hallucination on out-of-scope queries** | "Tell me about ColdFusion at Build" → "ColdFusion was announced as…" | `refusal_correct` driven by `kind`, not substrings |

Each gold case codifies one such expectation. The harness is what stops these regressions from reaching prod.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│  python -m evals                                                 │
│      │                                                           │
│      ├─ loads evals/configs/<event>.yaml  (event-specific knobs) │
│      ├─ loads evals/gold/<event>.yaml     (test cases)           │
│      │                                                           │
│      ├─ Adapter: Local (in-process) or HTTP (deployed URL)       │
│      │     ↓ /api/chat or BuildAgent.answer()                    │
│      │     ↓ response includes eval_trace ← gated by env/header  │
│      │                                                           │
│      ├─ Deterministic checks (metrics.py)                        │
│      │     - response_shape                                      │
│      │     - expected_behavior (matches `kind` field)            │
│      │     - recall@k (gold session in top-K retrieved)          │
│      │     - speaker_session_purity                              │
│      │     - speaker_evidence_purity                             │
│      │     - must_contain_all / must_not_contain_any             │
│      │     - required_citations / forbidden_citations            │
│      │     - citation_support (cited ⊆ retrieved)                │
│      │     - refusal_correct                                     │
│      │     - latency_ok                                          │
│      │                                                           │
│      ├─ LLM judge (judge.py, opt-in)                             │
│      │     - groundedness (0..1) — claim → context traceability  │
│      │     - attribution_fidelity (0..1) — speaker assignments   │
│      │     - answer_relevance (0..1) — answers the question      │
│      │     - structured JSON, temp=0, file-cached by hash        │
│      │                                                           │
│      └─ Renderer (report.py) — Markdown + JSON, optional diff    │
└──────────────────────────────────────────────────────────────────┘
```

---

## Gold dataset format

Every test case is a YAML entry in `evals/gold/<event>.yaml`:

```yaml
- case_id: naomi-prompt-caching            # required, kebab-case, unique
  description: "..."
  query: "What did Naomi say about prompt caching?"
  query_variants:                          # paraphrases — same retrieval expected
    - "Did Naomi talk about prompt cache?"

  expected_behavior: answerable            # enum, see schema.py

  # Retrieval expectations
  gold_session_codes: ["BRK230"]
  forbidden_session_codes: ["BRK226"]      # would be a wrong-speaker leak
  recall_at_k: 5

  # Speaker expectations
  expected_speaker: "Naomi Moneypenny"
  speaker_session_purity_required: true    # all retrieved sessions list speaker
  speaker_evidence_purity_required: true   # passage text mentions speaker

  # Answer-text constraints
  must_contain_all: ["BRK230", "00:32"]
  must_not_contain_any: ["BRK226"]

  # Citation contract
  required_citations: ["BRK230"]
  forbidden_citations: ["BRK226"]

  # LLM judge guidance
  judge_context_note: "...optional hint..."
  skip_judge: false

  tags: [speaker-precision, p0]            # filter with --tag
```

### `expected_behavior` taxonomy

| Value | When to use |
|---|---|
| `answerable` | Question has a clear answer in the corpus |
| `partially_answerable` | Some sub-claims OK, others must refuse |
| `honest_refusal` | Context retrieved but doesn't actually support the asked claim (the Mark/Marcus case) |
| `out_of_scope_refusal` | Topic/speaker truly not in corpus |
| `weak_match` | Nothing direct, only adjacent candidates |
| `session_lookup` | Direct session-code query |
| `topic_summary` | Listing many sessions for a topic |
| `no_ai_summary_available` | Metadata-only answer (no AI summary indexed) |
| `clarification_needed` | Vague / greeting / help intent |

---

## Adding a new event

1. **Drop in your data** under `data/<event>.json` (or reuse `data/sessions.json`).
2. **Create `evals/configs/<event>.yaml`** — copy `build2026.yaml`, change `event_id`, `session_code_regex`, and refusal markers if needed.
3. **Create `evals/gold/<event>.yaml`** — start with 5–10 high-value cases (your p0 speaker-precision cases first).
4. Run: `python -m evals --event <event> --judge`

The eval framework itself is event-agnostic.

---

## Running against the deployed app

The HTTP adapter posts to `/api/chat` with header `X-Eval-Trace: 1`. The server only returns the trace if `EVAL_TRACE_ENABLED=1` is set in app config (security: traces leak retrieval scores + filter logic).

For Build 2026:

```bash
az webapp config appsettings set -g rg-build2026-chatbot -n build2026-chatbot-50261 \
  --settings EVAL_TRACE_ENABLED=1

python -m evals --url https://build2026-chatbot-50261.azurewebsites.net --judge --strict

# Turn off when done if you don't want traces in prod
az webapp config appsettings delete -g rg-build2026-chatbot -n build2026-chatbot-50261 \
  --setting-names EVAL_TRACE_ENABLED
```

---

## CI integration

`.github/workflows/eval.yml` runs `python -m evals --strict` on every PR. Deterministic checks only; the LLM judge is opt-in (requires AOAI secrets you may or may not want in CI).

Failure modes:
- `pass_rate < min_pass_rate` (default 90%) → CI fails
- With `--judge`: `avg_groundedness < min_groundedness` → CI fails

Tune thresholds in `evals/configs/<event>.yaml`.

---

## Cost & determinism

| Mode | Cost / run | Wall time | Deterministic |
|---|---|---|---|
| `python -m evals` (deterministic only) | $0 | ~5s | Yes |
| `python -m evals --judge` (with cache) | $0 after first run | ~5s | Yes |
| `python -m evals --judge` (cold cache, 25 cases) | ~$0.15 | ~60s | Yes (temp=0, cached) |
| `python -m evals --url ... --judge` | ~$0.15 + latency | 1–3 min | Yes (cached) |

The judge cache lives in `evals/cache/`. Hash key is `sha256(case_id + query + answer + context + rubric + model + version)` — if any of those change, the case is re-judged.

---

## When to add a case

Add a gold case whenever you:
1. **See a user query produce a wrong answer in prod or staging.** Bug → reproduction → gold case → fix.
2. **Ship a new retrieval/prompt change.** Add cases that lock in the new behavior.
3. **Add a new event corpus** that introduces new speakers / topics.

Goal: every released regression has a gold case behind it. The gold dataset is your spec.

---

## File layout

```
evals/
├── __init__.py
├── __main__.py          # CLI entrypoint
├── README.md
├── schema.py            # pydantic models (GoldCase, RunReport, JudgeResult)
├── adapters.py          # LocalAdapter, HTTPAdapter
├── metrics.py           # all deterministic checks
├── judge.py             # LLM-as-judge (cached, structured JSON)
├── runner.py            # orchestrator
├── report.py            # markdown + JSON renderers
├── configs/
│   └── build2026.yaml   # event-specific knobs
├── gold/
│   └── build2026.yaml   # 25+ gold cases (the spec)
├── reports/             # generated, gitignored
└── cache/               # judge cache, gitignored
```
