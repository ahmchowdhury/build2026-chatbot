"""LLM-as-judge for groundedness, attribution, and answer-relevance.

Design:
  * Uses Azure OpenAI gpt-4o (configurable). temperature=0, response_format
    forced to JSON, structured schema with bounded fields.
  * Cached on disk by sha256(case_id + query + answer + context + rubric +
    model + judge_version). Re-running an unchanged answer is free.
  * Operates over the *retrieved passages* from eval_trace, not the final
    answer alone — judging groundedness without context is meaningless.
  * Returns 0..1 scores with a short rationale and a list of unsupported
    claims. Falls back to a graceful "judge unavailable" if AOAI is not
    configured.

Calling pattern:
    judge = Judge.from_env()
    if judge.available:
        result = judge.judge(case, variant_outcome, passages)
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional

import httpx

from .schema import GoldCase, JudgeResult

JUDGE_VERSION = "v1.0"

JUDGE_RUBRIC = """You are an evaluator for a Retrieval-Augmented Generation (RAG) chatbot.
You will be given a USER_QUESTION, the RETRIEVED_CONTEXT the chatbot was given, the
chatbot's ANSWER, and the EXPECTED_BEHAVIOR.

Score the answer on three independent 0.0–1.0 axes:

1. groundedness — every factual claim in ANSWER is supported by RETRIEVED_CONTEXT.
   - 1.0 = every claim is directly traceable to a passage
   - 0.7 = mostly supported, one minor unsupported detail
   - 0.4 = at least one significant unsupported claim
   - 0.0 = answer is mostly fabricated or contradicts context

2. attribution_fidelity — quotes and statements are attributed to the correct speaker.
   - 1.0 = all attributions verified or none present
   - 0.5 = one or more speaker mix-ups (Mark vs Marcus, etc.)
   - 0.0 = answer fabricates attributions

3. answer_relevance — answer actually addresses USER_QUESTION (not off-topic).
   - 1.0 = directly answers the question
   - 0.5 = partial or tangential
   - 0.0 = ignores the question

Special rules:
- If EXPECTED_BEHAVIOR is "honest_refusal" or "out_of_scope_refusal", a polite
  refusal that explains why no answer is possible is grounded (1.0) and relevant
  (1.0), as long as it does NOT fabricate facts.
- If the answer says "I don't know" or refuses, that is *grounded* and *relevant*
  iff the context truly doesn't support an answer.
- Quoting verbatim from RETRIEVED_CONTEXT is always grounded.
- A correct refusal beats a confident wrong answer.

Output STRICT JSON with exactly these fields:
{
  "groundedness": <0..1>,
  "attribution_fidelity": <0..1>,
  "answer_relevance": <0..1>,
  "unsupported_claims": [<string>, ...],
  "rationale": "<one or two sentences>"
}
Do not include anything else. Do not wrap in markdown.
"""


def _cache_key(case_id: str, query: str, answer: str, context: str,
               model: str) -> str:
    h = hashlib.sha256()
    for piece in (JUDGE_VERSION, case_id, query, answer, context, model,
                  JUDGE_RUBRIC):
        h.update(piece.encode("utf-8", errors="replace"))
        h.update(b"\x00")
    return h.hexdigest()


def _context_from_passages(passages: List[Dict], max_chars: int = 24000) -> str:
    # 24k chars ≈ 6k tokens — comfortable inside gpt-4o's 128k window and
    # large enough to fit ~10-15 typical RAG passages (the most relevant
    # ones the synthesizer actually grounded on). Without enough breadth
    # here the judge marks legitimately-supported claims as "unsupported"
    # because the supporting passage was clipped.
    chunks = []
    used = 0
    for i, p in enumerate(passages, 1):
        block = (
            f"[{i}] [{p.get('sessionCode','?')}] {p.get('sessionTitle','?')}\n"
            f"Speakers: {p.get('speakers','—')}\n"
            f"Excerpt: {(p.get('passage') or '').strip()}\n"
        )
        if used + len(block) > max_chars:
            chunks.append("…(truncated)")
            break
        chunks.append(block)
        used += len(block)
    return "\n---\n".join(chunks) or "(no context retrieved)"


def _safe_float(x, default: float = 0.0) -> float:
    try:
        f = float(x)
        if f < 0:
            return 0.0
        if f > 1:
            return 1.0
        return f
    except Exception:
        return default


class Judge:
    """LLM judge over Azure OpenAI. File-cached, deterministic-temperature."""

    def __init__(self, endpoint: str, key: str, deployment: str,
                 api_version: str = "2024-10-21",
                 cache_dir: Optional[Path] = None):
        self.endpoint = endpoint.rstrip("/")
        self.key = key
        self.deployment = deployment
        self.api_version = api_version
        self.cache_dir = cache_dir or Path(__file__).parent / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._client = httpx.Client(timeout=60.0)

    @classmethod
    def from_env(cls, cache_dir: Optional[Path] = None) -> Optional["Judge"]:
        endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        key = os.environ.get("AZURE_OPENAI_KEY")
        deployment = (os.environ.get("AZURE_OPENAI_JUDGE_DEPLOYMENT")
                      or os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT")
                      or "gpt-4o")
        if not (endpoint and key):
            return None
        return cls(endpoint=endpoint.strip(), key=key.strip(),
                   deployment=deployment.strip(),
                   cache_dir=cache_dir)

    @property
    def available(self) -> bool:
        return bool(self.endpoint and self.key)

    @property
    def model_id(self) -> str:
        return self.deployment

    def _cache_path(self, key: str) -> Path:
        return self.cache_dir / f"{key}.json"

    def judge(self, case: GoldCase, answer: str,
              passages: List[Dict]) -> JudgeResult:
        context = _context_from_passages(passages)
        key = _cache_key(case.case_id, case.query, answer, context, self.deployment)
        cache_path = self._cache_path(key)
        if cache_path.exists():
            try:
                data = json.loads(cache_path.read_text())
                return JudgeResult(**data, cached=True)
            except Exception:
                # fall through to recompute on corrupted cache
                pass

        prompt_user = (
            f"USER_QUESTION: {case.query}\n\n"
            f"EXPECTED_BEHAVIOR: {case.expected_behavior.value}\n\n"
            f"RETRIEVED_CONTEXT:\n{context}\n\n"
            f"ANSWER:\n{answer}\n\n"
            f"{ ('NOTE: ' + case.judge_context_note) if case.judge_context_note else '' }"
        )
        url = (f"{self.endpoint}/openai/deployments/{self.deployment}/"
               f"chat/completions?api-version={self.api_version}")
        body = {
            "messages": [
                {"role": "system", "content": JUDGE_RUBRIC},
                {"role": "user", "content": prompt_user},
            ],
            "temperature": 0,
            "top_p": 1,
            "max_tokens": 500,
            "response_format": {"type": "json_object"},
        }
        try:
            r = self._client.post(
                url,
                headers={"api-key": self.key, "Content-Type": "application/json"},
                json=body,
            )
            r.raise_for_status()
            raw = r.json()["choices"][0]["message"]["content"]
            data = json.loads(raw)
        except Exception as e:
            # Conservative: report low groundedness so a transient judge
            # failure surfaces in the report rather than silently passing.
            return JudgeResult(
                groundedness=0.0,
                attribution_fidelity=0.0,
                answer_relevance=0.0,
                rationale=f"judge_error: {e}",
                unsupported_claims=[],
                cached=False,
            )

        result = JudgeResult(
            groundedness=_safe_float(data.get("groundedness")),
            attribution_fidelity=_safe_float(data.get("attribution_fidelity")),
            answer_relevance=_safe_float(data.get("answer_relevance")),
            unsupported_claims=list(data.get("unsupported_claims") or []),
            rationale=str(data.get("rationale", ""))[:1000],
            cached=False,
        )
        try:
            cache_path.write_text(result.model_dump_json())
        except Exception:
            pass
        return result
