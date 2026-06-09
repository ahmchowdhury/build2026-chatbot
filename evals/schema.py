"""Schemas for gold cases, eval results, and event configs."""
from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ExpectedBehavior(str, Enum):
    """What the user *should* see for this query.

    Determines which checks apply. For example, `out_of_scope_refusal`
    requires `kind in {"not-found", "weak"}` AND the answer must NOT cite a
    session, while `answerable` requires at least one cited session.
    """
    answerable = "answerable"                       # full answer expected
    partially_answerable = "partially_answerable"   # some claims OK, some refused
    honest_refusal = "honest_refusal"               # context retrieved but doesn't support claim
    out_of_scope_refusal = "out_of_scope_refusal"   # not in corpus at all
    weak_match = "weak_match"                       # nothing direct, candidates only
    session_lookup = "session_lookup"               # direct session code
    topic_summary = "topic_summary"                 # listing many sessions
    no_ai_summary_available = "no_ai_summary_available"  # metadata-only answer
    clarification_needed = "clarification_needed"   # query too vague

    @property
    def requires_citation(self) -> bool:
        return self in (
            ExpectedBehavior.answerable,
            ExpectedBehavior.partially_answerable,
            ExpectedBehavior.session_lookup,
            ExpectedBehavior.topic_summary,
            ExpectedBehavior.weak_match,
            ExpectedBehavior.no_ai_summary_available,
        )

    @property
    def expects_refusal(self) -> bool:
        return self in (
            ExpectedBehavior.honest_refusal,
            ExpectedBehavior.out_of_scope_refusal,
        )


class GoldCase(BaseModel):
    """A single test case. Designed to be reusable across events — the
    only event-specific bits are `gold_session_codes` and `expected_speaker`.
    """
    case_id: str
    description: Optional[str] = None
    query: str
    query_variants: List[str] = Field(default_factory=list)
    """Paraphrases of `query` that should produce equivalent retrieval and
    behavior. The runner asserts every variant satisfies the same constraints
    (with `must_contain_all` enforced only on the canonical query to avoid
    over-fitting wording).
    """

    expected_behavior: ExpectedBehavior

    # Retrieval expectations
    gold_session_codes: List[str] = Field(default_factory=list)
    """Sessions that should be retrieved. Empty for out-of-scope cases."""
    forbidden_session_codes: List[str] = Field(default_factory=list)
    """Sessions that, if cited, are highly misleading (e.g. wrong speaker)."""
    recall_at_k: int = 5

    # Speaker expectations
    expected_speaker: Optional[str] = None
    allowed_speaker_aliases: List[str] = Field(default_factory=list)
    disallowed_speakers: List[str] = Field(default_factory=list)
    speaker_session_purity_required: bool = False
    """All retrieved sessions must list `expected_speaker`."""
    speaker_evidence_purity_required: bool = False
    """At least one retrieved passage must mention `expected_speaker`."""

    # Topic expectations
    expected_topic: Optional[str] = None
    min_sessions_returned: Optional[int] = None
    """For topic_summary, minimum number of sessions that must appear."""

    # Answer-text constraints (deterministic substring checks, case-insensitive)
    must_contain_all: List[str] = Field(default_factory=list)
    must_not_contain_any: List[str] = Field(default_factory=list)

    # Required / forbidden citations in the answer body
    required_citations: List[str] = Field(default_factory=list)
    forbidden_citations: List[str] = Field(default_factory=list)

    # LLM judge instructions
    judge_context_note: Optional[str] = None
    """Optional hint to the judge about what the *correct* answer looks like.
    Use sparingly — over-specifying biases the judge.
    """
    skip_judge: bool = False

    # Latency / cost budgets
    max_latency_ms: Optional[int] = None  # default from event config

    tags: List[str] = Field(default_factory=list)


class EventConfig(BaseModel):
    """Event-scoped knobs the eval framework needs. Keep this small."""
    event_id: str
    event_name: str
    session_code_regex: str = r"\b([A-Z]{2,4}\d{2,4}(?:-[A-Z0-9]+)?)\b"
    data_path: str = "data/sessions.json"
    session_code_field: str = "code"
    session_title_field: str = "title"
    speaker_field: str = "speakers"
    summary_field: str = "aiSummary"

    # Refusal markers used for `refusal_correct` (case-insensitive substrings).
    refusal_markers: List[str] = Field(default_factory=lambda: [
        "couldn't find", "could not find", "not in", "not covered",
        "not specifically discuss", "did not explicitly discuss",
        "did not discuss", "no session", "i don't see",
        "no microsoft build", "cannot confirm",
    ])
    # Refusal kind classifications produced by the agent.
    refusal_kinds: List[str] = Field(default_factory=lambda: [
        "not-found", "weak", "hint",
    ])

    default_max_latency_ms: int = 12000  # p95-ish budget for synthesis calls

    # Gating thresholds for CI (defaults — overridden per-event in YAML).
    # Defaults are calibrated for the inevitable judge non-determinism at
    # the per-claim level; gross hallucinations score < 0.5.
    min_pass_rate: float = 0.85
    min_groundedness: float = 0.75
    min_attribution_fidelity: float = 0.80


# ----- Results -----

class CheckResult(BaseModel):
    name: str
    passed: bool
    score: Optional[float] = None  # 0..1 when graded; None for boolean checks
    detail: Optional[str] = None


class JudgeResult(BaseModel):
    groundedness: float          # 0..1
    attribution_fidelity: float  # 0..1
    answer_relevance: float      # 0..1
    rationale: str
    unsupported_claims: List[str] = Field(default_factory=list)
    cached: bool = False


class VariantOutcome(BaseModel):
    query: str
    answer: str
    kind: str
    session_codes: List[str] = Field(default_factory=list)
    latency_ms: Optional[int] = None
    checks: List[CheckResult] = Field(default_factory=list)
    judge: Optional[JudgeResult] = None

    @property
    def passed(self) -> bool:
        return all(c.passed for c in self.checks)


class CaseResult(BaseModel):
    case_id: str
    description: Optional[str]
    expected_behavior: str
    variants: List[VariantOutcome]
    error: Optional[str] = None  # set if the case failed to execute

    @property
    def passed(self) -> bool:
        return self.error is None and all(v.passed for v in self.variants)

    @property
    def latency_ms_p95(self) -> int:
        lats = sorted(v.latency_ms for v in self.variants if v.latency_ms is not None)
        if not lats:
            return 0
        # tiny set, just take the last
        return lats[-1]


class RunMetadata(BaseModel):
    started_at: str
    finished_at: str
    duration_s: float
    event_id: str
    dataset_id: str
    dataset_version: str
    target: str  # "local" or URL
    git_sha: Optional[str] = None
    search_index: Optional[str] = None
    chat_model: Optional[str] = None
    embed_model: Optional[str] = None
    judge_model: Optional[str] = None
    judged: bool = False
    case_count: int = 0


class RunReport(BaseModel):
    metadata: RunMetadata
    case_results: List[CaseResult]

    @property
    def pass_rate(self) -> float:
        if not self.case_results:
            return 0.0
        return sum(1 for c in self.case_results if c.passed) / len(self.case_results)

    @property
    def avg_groundedness(self) -> Optional[float]:
        scores = [v.judge.groundedness for c in self.case_results
                  for v in c.variants if v.judge]
        return sum(scores) / len(scores) if scores else None

    @property
    def avg_attribution_fidelity(self) -> Optional[float]:
        scores = [v.judge.attribution_fidelity for c in self.case_results
                  for v in c.variants if v.judge]
        return sum(scores) / len(scores) if scores else None
