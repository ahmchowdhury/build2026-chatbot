"""Azure AI Search Agentic Retrieval client.

Talks to the `/knowledgebases/{name}/retrieve` endpoint (api-version
2026-05-01-preview) which:

  * runs LLM-based query planning + sub-query fan-out,
  * does parallel hybrid + semantic ranked retrieval on the knowledge
    source's index,
  * synthesises a single grounded answer string with bracketed
    citations,
  * returns an `activity` trace of every internal step (sub-queries,
    timings, doc counts).

We use it as a drop-in replacement for the manual hybrid_search +
grounded_answer pair in `rag.py`. Speaker hard-filtering is preserved by
passing `filterAddOn` per knowledge-source in the retrieve request.

If the KB call fails, the caller is expected to fall back to the
legacy `AzureRAG` path.
"""
from __future__ import annotations

import os
import time
from typing import Dict, List, Optional

import httpx


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    v = os.environ.get(name)
    if v is None or v.strip() == "":
        return default
    return v.strip()


class AgenticRAG:
    """Thin wrapper around the agentic-retrieval `retrieve` action."""

    def __init__(self):
        self.endpoint = _env("AZURE_SEARCH_ENDPOINT")
        self.key = _env("AZURE_SEARCH_KEY")
        self.kb_name = _env("AZURE_SEARCH_KB_NAME", "build2026-kb")
        self.ks_name = _env("AZURE_SEARCH_KS_NAME", "build2026-ks")
        self.api_version = _env(
            "AZURE_SEARCH_AGENTIC_API_VERSION", "2026-05-01-preview"
        )
        self._client = httpx.Client(timeout=90.0)

    def is_configured(self) -> bool:
        return bool(self.endpoint and self.key and self.kb_name and self.ks_name)

    @staticmethod
    def _speaker_filter(codes: Optional[List[str]],
                        speaker_label: Optional[str]) -> Optional[str]:
        """Build an OData filterAddOn that hard-narrows retrieval to the
        speaker's sessions.

        We rely on the sessionCode `search.in` clause alone — `speakers/any`
        with a literal name is brittle because:
          1. The catalog stores full names ("Naomi Moneypenny") but the user
             often supplies an alias ("Naomi"), and `s eq 'Naomi'` would
             never match the full-name string.
          2. Every chunk from a session carries the SAME speakers list
             (it's a session-level attribute), so once we pin sessionCode
             the speakers filter adds nothing — it would only ever
             over-restrict due to alias mismatches.

        Attribution inside a session (e.g. did Naomi say X or did her
        co-speaker say X?) is handled in two places:
          a) the user's literal query text still mentions the speaker, so
             the semantic ranker biases toward passages that name them,
          b) the KB's answerInstructions tell the LLM to honestly refuse
             when no retrieved passage attributes the claim to the named
             speaker.
        """
        if not codes:
            return None
        quoted = ",".join(c for c in codes if c)
        if not quoted:
            return None
        return f"search.in(sessionCode, '{quoted}', ',')"

    def retrieve(
        self,
        query: str,
        speaker_codes: Optional[List[str]] = None,
        speaker_label: Optional[str] = None,
        history: Optional[List[Dict]] = None,
        reasoning_effort: Optional[str] = None,
        max_output_documents: int = 50,
        reranker_threshold: float = 1.5,
    ) -> Dict:
        """Run a retrieve action against the configured knowledge base.

        Returns a dict with keys:
          answer        - synthesised grounded answer string (may be "" on
                          refusal)
          references    - list of normalised reference dicts (one per
                          retrieved passage); each has sessionCode,
                          sessionTitle, speakers, passage, sessionPage,
                          transcriptUrl, videoUrl, score
          activity      - raw activity trace from the KB pipeline
          raw           - the full response JSON (for debugging)
          latency_ms    - wall-clock latency of the retrieve call
          filter_used   - the filterAddOn string we sent (may be None)
        """
        if not self.is_configured():
            raise RuntimeError("AgenticRAG not configured")

        url = (f"{self.endpoint.rstrip('/')}/knowledgebases/{self.kb_name}"
               f"/retrieve?api-version={self.api_version}")

        messages: List[Dict] = list(history or [])
        # When the user names a specific speaker, prepend the literal
        # constraint to the user message. The KB's global
        # answerInstructions are general; this per-query hint tells the
        # query planner + synthesizer that strict speaker-name attribution
        # is required for THIS turn. Catches the Mark/Marcus case where
        # the passage attributes a claim to a name that the LLM might
        # "resolve" back to the canonical speaker.
        if speaker_label:
            query = (f"{query}\n\n"
                     f"STRICT: Only attribute claims to **{speaker_label}** "
                     f"if the passage text explicitly contains that exact "
                     f"name. If the passage attributes the claim to a "
                     f"different name (even a similar one or a typo), "
                     f"refuse honestly and call out the discrepancy.")
        messages.append({
            "role": "user",
            "content": [{"type": "text", "text": query}],
        })

        ks_params: Dict = {
            "knowledgeSourceName": self.ks_name,
            "kind": "searchIndex",
            "includeReferences": True,
            "includeReferenceSourceData": True,
            "rerankerThreshold": reranker_threshold,
            "maxOutputDocuments": max_output_documents,
            "alwaysQuerySource": True,
        }
        filter_str = self._speaker_filter(speaker_codes, speaker_label)
        if filter_str:
            ks_params["filterAddOn"] = filter_str

        body: Dict = {
            "messages": messages,
            "knowledgeSourceParams": [ks_params],
            "includeActivity": True,
        }
        if reasoning_effort:
            body["retrievalReasoningEffort"] = {"kind": reasoning_effort}

        t0 = time.perf_counter()
        r = self._client.post(
            url,
            headers={"api-key": self.key, "Content-Type": "application/json"},
            json=body,
        )
        elapsed_ms = int((time.perf_counter() - t0) * 1000)
        if r.status_code != 200:
            # Azure OpenAI content filter trips show up as 400 with a
            # "content management policy" message inside the JSON. Return
            # a structured refusal so the agent can render an honest "I
            # can't answer that" rather than crashing.
            body_text = r.text or ""
            if ("content management policy" in body_text
                    or "content filter" in body_text.lower()):
                return {
                    "answer": ("I can't respond to that request. The "
                               "prompt was filtered for safety. Please "
                               "rephrase your question about Microsoft "
                               "Build 2026."),
                    "references": [],
                    "activity": [],
                    "raw": {"error": "content_filter"},
                    "latency_ms": elapsed_ms,
                    "filter_used": filter_str,
                    "content_filtered": True,
                }
            raise RuntimeError(
                f"agentic retrieve failed {r.status_code}: {r.text[:400]}"
            )
        j = r.json()

        # Synthesised answer string — for outputMode=answerSynthesis the KB
        # returns one assistant message with a `text` content block.
        answer = ""
        for msg in (j.get("response") or []):
            for c in (msg.get("content") or []):
                if c.get("type") == "text":
                    answer += c.get("text", "")

        refs_norm: List[Dict] = []
        for ref in (j.get("references") or []):
            sd = ref.get("sourceData") or {}
            refs_norm.append({
                "id": sd.get("id"),
                "sessionCode": sd.get("sessionCode"),
                "sessionTitle": sd.get("sessionTitle"),
                "speakers": sd.get("speakers"),
                "topic": sd.get("topic"),
                "passage": sd.get("passage"),
                "sessionPage": sd.get("sessionPage"),
                "transcriptUrl": sd.get("transcriptUrl"),
                "videoUrl": sd.get("videoUrl"),
                "timestamps": sd.get("timestamps"),
                "score": (ref.get("rerankerScore")
                          or ref.get("score")),
                "activitySource": ref.get("activitySource"),
            })

        return {
            "answer": answer,
            "references": refs_norm,
            "activity": j.get("activity") or [],
            "raw": j,
            "latency_ms": elapsed_ms,
            "filter_used": filter_str,
        }
