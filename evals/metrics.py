"""Deterministic metric scorers. Every function returns a CheckResult.

Design rules:
  * Pure functions, no side effects, no network.
  * Boolean checks set `passed`; graded checks set both `passed` and `score`.
  * `detail` always carries enough context to triage a failure without
    re-running the case.

What we explicitly avoid:
  * String matching for refusal detection. Refusal classification reads the
    agent's `kind` field, which is structured. Substring markers are an
    *additional* signal, not the primary one.
  * Citation-substring counting without checking that the cited session is
    in the retrieved set. Citation laundering must not pass.
"""
from __future__ import annotations

import re
from typing import Dict, List, Optional, Sequence, Set

from .schema import CheckResult, EventConfig, ExpectedBehavior, GoldCase

# ---------- helpers ----------


def _ci_contains(haystack: str, needle: str) -> bool:
    return needle.lower() in (haystack or "").lower()


def _extract_session_codes(text: str, regex: str) -> List[str]:
    """Pull every session code referenced in the answer body."""
    if not text:
        return []
    out = []
    seen = set()
    for m in re.finditer(regex, text):
        code = m.group(1) if m.groups() else m.group(0)
        if code not in seen:
            seen.add(code)
            out.append(code)
    return out


# A citation, specifically — only matches `[CODE]` in square brackets. This
# is much stricter than the general session-code regex (which would also
# match product mentions like "MI300" in prose). Used by citation_support
# and required/forbidden_citations.
_CITED_CODE_RE = re.compile(r"\[([A-Z]{2,4}\d{2,4}(?:-[A-Z0-9]+)?)\]")


def _extract_citations(text: str) -> List[str]:
    if not text:
        return []
    out, seen = [], set()
    for m in _CITED_CODE_RE.finditer(text):
        c = m.group(1)
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


# Kinds for which citation checks don't apply (capability descriptions,
# help, topic lists — they may mention session codes as examples).
_NON_CITING_KINDS = {"help", "topics", "hint"}


def _passage_text(p: Dict) -> str:
    return (p.get("passage") or "")


def _retrieved_codes(trace: Optional[Dict]) -> List[str]:
    if not trace:
        return []
    out, seen = [], set()
    for r in trace.get("retrieved") or []:
        code = r.get("sessionCode")
        if code and code not in seen:
            seen.add(code)
            out.append(code)
    return out


def _passage_mentions_speaker(text: str, speaker: str,
                              aliases: Sequence[str] = ()) -> bool:
    if not text or not speaker:
        return False
    low = text.lower()
    candidates = {speaker.lower()}
    for tok in re.split(r"\W+", speaker):
        if len(tok) >= 3:
            candidates.add(tok.lower())
    for a in aliases:
        if a:
            candidates.add(a.lower())
    for c in candidates:
        if " " in c:
            if c in low:
                return True
        else:
            if re.search(r"\b" + re.escape(c) + r"\b", low):
                return True
    return False


# ---------- contract checks ----------


def check_response_shape(out: Dict) -> CheckResult:
    """The /api/chat response must always carry answer + kind."""
    has_answer = bool(out.get("answer"))
    has_kind = bool(out.get("kind"))
    no_traceback = "Traceback (most recent call last)" not in (out.get("answer") or "")
    passed = has_answer and has_kind and no_traceback
    return CheckResult(
        name="response_shape",
        passed=passed,
        detail=("ok" if passed else
                f"answer={has_answer} kind={has_kind} no_traceback={no_traceback}"),
    )


def check_http_ok(out: Dict) -> CheckResult:
    status = out.get("_http_status", 200)
    passed = status == 200
    return CheckResult(
        name="http_ok",
        passed=passed,
        detail=f"status={status}" + (f" body={out.get('_http_body','')[:200]}" if not passed else ""),
    )


def check_latency(out: Dict, budget_ms: int) -> CheckResult:
    observed = out.get("_latency_ms_observed", 0)
    passed = observed <= budget_ms
    return CheckResult(
        name="latency_ok",
        passed=passed,
        score=min(1.0, budget_ms / max(observed, 1)),
        detail=f"observed={observed}ms budget={budget_ms}ms",
    )


# ---------- behavior / kind checks ----------


def check_expected_behavior(out: Dict, case: GoldCase,
                            cfg: EventConfig) -> CheckResult:
    """The agent's `kind` must match the expected behavior class."""
    kind = (out.get("kind") or "").lower()
    expected = case.expected_behavior

    if expected == ExpectedBehavior.answerable:
        ok = kind in ("answer-rag", "answer-local", "answer")
    elif expected == ExpectedBehavior.partially_answerable:
        # Either a successful answer OR an honest refusal counts as
        # "partial" — what matters is that the substring constraints encode
        # the actual desired behavior.
        ok = kind in ("answer-rag", "answer-local", "answer", "weak")
    elif expected == ExpectedBehavior.honest_refusal:
        # Honest refusal can still be tagged "answer-rag" because the model
        # refused inside a successful synthesis call. We check substring
        # constraints separately. Here we accept either.  "session" counts
        # too: a session-card response that returns the truthful speakers
        # implicitly refutes a false claim about the session.
        ok = kind in ("answer-rag", "answer-local", "not-found", "weak", "answer", "session")
    elif expected == ExpectedBehavior.out_of_scope_refusal:
        ok = kind in tuple(cfg.refusal_kinds)
    elif expected == ExpectedBehavior.weak_match:
        ok = kind in ("weak", "answer-rag", "answer-local")
    elif expected == ExpectedBehavior.session_lookup:
        ok = kind == "session"
    elif expected == ExpectedBehavior.topic_summary:
        ok = kind == "topic-summary"
    elif expected == ExpectedBehavior.no_ai_summary_available:
        ok = kind == "session"
    elif expected == ExpectedBehavior.clarification_needed:
        ok = kind in ("hint", "help", "not-found", "weak", "topics")
    else:
        ok = True

    return CheckResult(
        name="expected_behavior",
        passed=ok,
        detail=f"expected={expected.value} got_kind={kind}",
    )


# ---------- retrieval metrics ----------


def check_recall_at_k(out: Dict, case: GoldCase) -> CheckResult:
    """At least one gold session must appear in top-K retrieved."""
    if not case.gold_session_codes:
        return CheckResult(name=f"recall@{case.recall_at_k}", passed=True,
                           score=1.0, detail="no gold session — skipped")
    retrieved = _retrieved_codes(out.get("eval_trace"))[:case.recall_at_k]
    if not retrieved:
        # Fallback to cited sessions if trace is missing.
        retrieved = (out.get("session_codes") or [])[:case.recall_at_k]
    gold = set(case.gold_session_codes)
    hits = [c for c in retrieved if c in gold]
    passed = len(hits) > 0
    score = len(hits) / max(len(case.gold_session_codes), 1)
    return CheckResult(
        name=f"recall@{case.recall_at_k}",
        passed=passed,
        score=score,
        detail=f"gold={sorted(gold)} retrieved_topk={retrieved} hits={hits}",
    )


def check_speaker_session_purity(out: Dict, case: GoldCase) -> CheckResult:
    """When speaker_session_purity_required, every retrieved session must
    list the expected speaker (we check via the agent's speaker_filter_codes
    in the trace — that field already reflects the speaker-index lookup).
    """
    if not case.speaker_session_purity_required:
        return CheckResult(name="speaker_session_purity", passed=True,
                           detail="not required — skipped")
    trace = out.get("eval_trace") or {}
    filter_codes = set(trace.get("speaker_filter_codes") or [])
    retrieved = _retrieved_codes(trace)
    if not filter_codes:
        return CheckResult(name="speaker_session_purity", passed=False,
                           detail=f"speaker_filter_codes empty (speaker_label="
                                  f"{trace.get('speaker_label')!r}); the agent "
                                  f"did not apply the speaker filter")
    violators = [c for c in retrieved if c not in filter_codes]
    passed = not violators
    return CheckResult(
        name="speaker_session_purity",
        passed=passed,
        score=1.0 - (len(violators) / max(len(retrieved), 1)),
        detail=(f"speaker={case.expected_speaker} "
                f"filter_codes={sorted(filter_codes)[:5]}... "
                f"violators={violators}"),
    )


def check_speaker_evidence_purity(out: Dict, case: GoldCase) -> CheckResult:
    """When speaker_evidence_purity_required, at least one retrieved passage
    must mention the expected speaker name (or alias). This catches the
    Mark/Marcus class of bug: session lists Mark but excerpt attributes the
    quote to someone else."""
    if not case.speaker_evidence_purity_required or not case.expected_speaker:
        return CheckResult(name="speaker_evidence_purity", passed=True,
                           detail="not required — skipped")
    trace = out.get("eval_trace") or {}
    passages = trace.get("retrieved") or []
    if not passages:
        return CheckResult(name="speaker_evidence_purity", passed=False,
                           detail="no passages retrieved")
    aliases = case.allowed_speaker_aliases
    mentioning = [
        p.get("sessionCode")
        for p in passages
        if _passage_mentions_speaker(_passage_text(p),
                                     case.expected_speaker, aliases)
    ]
    passed = len(mentioning) >= 1
    return CheckResult(
        name="speaker_evidence_purity",
        passed=passed,
        score=len(mentioning) / max(len(passages), 1),
        detail=f"speaker={case.expected_speaker} mentioning_passages={mentioning}",
    )


# ---------- answer constraints ----------


def check_must_contain(out: Dict, case: GoldCase) -> CheckResult:
    """All `must_contain_all` substrings present in answer."""
    if not case.must_contain_all:
        return CheckResult(name="must_contain_all", passed=True,
                           detail="empty — skipped")
    answer = out.get("answer") or ""
    missing = [s for s in case.must_contain_all if not _ci_contains(answer, s)]
    passed = not missing
    return CheckResult(
        name="must_contain_all",
        passed=passed,
        score=1.0 - len(missing) / len(case.must_contain_all),
        detail=f"missing={missing}" if missing else "all present",
    )


def check_must_not_contain(out: Dict, case: GoldCase) -> CheckResult:
    if not case.must_not_contain_any:
        return CheckResult(name="must_not_contain_any", passed=True,
                           detail="empty — skipped")
    answer = out.get("answer") or ""
    hits = [s for s in case.must_not_contain_any if _ci_contains(answer, s)]
    passed = not hits
    return CheckResult(
        name="must_not_contain_any",
        passed=passed,
        score=1.0 if passed else 0.0,
        detail=f"unwanted_hits={hits}" if hits else "clean",
    )


def check_required_citations(out: Dict, case: GoldCase,
                             cfg: EventConfig) -> CheckResult:
    if not case.required_citations:
        return CheckResult(name="required_citations", passed=True,
                           detail="empty — skipped")
    answer = out.get("answer") or ""
    cited = set(_extract_citations(answer))
    missing = [c for c in case.required_citations if c not in cited]
    passed = not missing
    return CheckResult(
        name="required_citations",
        passed=passed,
        score=1.0 - len(missing) / len(case.required_citations),
        detail=f"missing={missing} cited={sorted(cited)}",
    )


def check_forbidden_citations(out: Dict, case: GoldCase,
                              cfg: EventConfig) -> CheckResult:
    if not case.forbidden_citations and not case.forbidden_session_codes:
        return CheckResult(name="forbidden_citations", passed=True,
                           detail="empty — skipped")
    answer = out.get("answer") or ""
    cited = set(_extract_citations(answer))
    forbidden = set(case.forbidden_citations) | set(case.forbidden_session_codes)
    hits = [c for c in forbidden if c in cited]
    passed = not hits
    return CheckResult(
        name="forbidden_citations",
        passed=passed,
        score=1.0 if passed else 0.0,
        detail=f"unwanted_citations={hits}" if hits else "clean",
    )


def check_citation_support(out: Dict, cfg: EventConfig) -> CheckResult:
    """Every session cited in the answer body must also appear in the
    retrieved set (anti citation-laundering). Defends against the model
    hallucinating session codes that look real.

    Skipped for capability-description kinds (help/topics/hint) — those
    may legitimately mention session codes as examples.
    """
    kind = (out.get("kind") or "").lower()
    if kind in _NON_CITING_KINDS:
        return CheckResult(name="citation_support", passed=True,
                           detail=f"kind={kind} — skipped (non-citing)")
    answer = out.get("answer") or ""
    cited = _extract_citations(answer)
    if not cited:
        return CheckResult(name="citation_support", passed=True,
                           detail="no citations — skipped")
    trace = out.get("eval_trace") or {}
    retrieved = set(_retrieved_codes(trace))
    if not retrieved:
        retrieved = set(out.get("session_codes") or [])
    unsupported = [c for c in cited if c not in retrieved]
    passed = not unsupported
    return CheckResult(
        name="citation_support",
        passed=passed,
        score=1.0 - len(unsupported) / len(cited),
        detail=f"cited={cited} unsupported={unsupported}",
    )


def check_refusal_correct(out: Dict, case: GoldCase,
                          cfg: EventConfig) -> CheckResult:
    """When `expected_behavior` is a refusal flavor, the answer must
    actually refuse. Primary signal: `kind`. Secondary: refusal markers.

    We *also* assert that the answer does NOT contain confident-claim
    phrases ("said", "announced", "explained that") attributed to the
    forbidden subject — that's why honest-refusal cases pair this check
    with `must_not_contain_any`.
    """
    if not case.expected_behavior.expects_refusal:
        return CheckResult(name="refusal_correct", passed=True,
                           detail="not a refusal case — skipped")
    kind = (out.get("kind") or "").lower()
    answer = (out.get("answer") or "").lower()
    has_refusal_marker = any(m.lower() in answer for m in cfg.refusal_markers)
    kind_is_refusal = kind in tuple(cfg.refusal_kinds)

    if case.expected_behavior == ExpectedBehavior.out_of_scope_refusal:
        passed = kind_is_refusal or has_refusal_marker
    else:  # honest_refusal — can come from inside a successful synthesis
        # `session` counts as honest refusal when the user planted a false
        # claim about the session and the card returns the truthful
        # speakers/details (which implicitly refutes the claim). The
        # must_not_contain_any constraint on the gold case still guards
        # against actually agreeing with the lie.
        passed = has_refusal_marker or kind_is_refusal or kind == "session"

    return CheckResult(
        name="refusal_correct",
        passed=passed,
        detail=f"kind={kind} kind_is_refusal={kind_is_refusal} "
               f"has_refusal_marker={has_refusal_marker}",
    )


def check_min_sessions_returned(out: Dict, case: GoldCase) -> CheckResult:
    if case.min_sessions_returned is None:
        return CheckResult(name="min_sessions_returned", passed=True,
                           detail="not required — skipped")
    n = len(out.get("session_codes") or [])
    passed = n >= case.min_sessions_returned
    return CheckResult(
        name="min_sessions_returned",
        passed=passed,
        score=min(1.0, n / max(case.min_sessions_returned, 1)),
        detail=f"got={n} required>={case.min_sessions_returned}",
    )


def check_forbidden_session_in_retrieval(out: Dict, case: GoldCase) -> CheckResult:
    """Defense against retrieval leaking sessions known to be irrelevant or
    misleading (e.g. wrong-speaker session for honest-refusal cases)."""
    if not case.forbidden_session_codes:
        return CheckResult(name="forbidden_retrieval", passed=True,
                           detail="empty — skipped")
    retrieved = set(_retrieved_codes(out.get("eval_trace")))
    if not retrieved:
        retrieved = set(out.get("session_codes") or [])
    hits = [c for c in case.forbidden_session_codes if c in retrieved]
    passed = not hits
    return CheckResult(
        name="forbidden_retrieval",
        passed=passed,
        detail=f"unwanted_retrieved={hits}" if hits else "clean",
    )


# ---------- runner facade ----------


def run_all_checks(out: Dict, case: GoldCase, cfg: EventConfig,
                   target: str = "local") -> List[CheckResult]:
    """Run every deterministic check appropriate for this case. The order
    matters for readability of failure reports but not correctness.
    """
    checks: List[CheckResult] = [check_response_shape(out)]
    if target == "http":
        checks.append(check_http_ok(out))
    checks.extend([
        check_expected_behavior(out, case, cfg),
        check_recall_at_k(out, case),
        check_speaker_session_purity(out, case),
        check_speaker_evidence_purity(out, case),
        check_must_contain(out, case),
        check_must_not_contain(out, case),
        check_required_citations(out, case, cfg),
        check_forbidden_citations(out, case, cfg),
        check_citation_support(out, cfg),
        check_refusal_correct(out, case, cfg),
        check_min_sessions_returned(out, case),
        check_forbidden_session_in_retrieval(out, case),
        check_latency(out, case.max_latency_ms or cfg.default_max_latency_ms),
    ])
    return checks
