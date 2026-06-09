"""Event-agnostic RAG evaluation harness for chatbots over event-session
corpora (Build, Ignite, Decoded, etc.).

Three layers of measurement per case:

  1. Deterministic retrieval metrics  (recall@k, speaker purity, citation
     support) — fast, no LLM, suitable for CI gates.
  2. Deterministic answer constraints (must_contain, must_not_contain,
     refusal_correct, contract checks) — fast, deterministic.
  3. LLM-as-judge                     (groundedness, attribution fidelity,
     answer relevance) — opt-in, structured JSON, file-cached.

Run from the repo root:

    python -m evals                          # local agent, deterministic only
    python -m evals --judge                  # adds LLM judge
    python -m evals --url https://prod.url   # against deployed app
    python -m evals --event build2026        # explicit event (default)
"""

__version__ = "1.0.0"
