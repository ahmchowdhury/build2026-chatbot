"""Adapters: uniform interface for invoking the chatbot, whether locally
(import the agent) or via a deployed HTTP endpoint.

Every adapter returns the same shape: a dict with keys
  answer, kind, session_codes, eval_trace, latency_ms_observed
"""
from __future__ import annotations

import time
from typing import Dict, Optional

import httpx


class Adapter:
    """Abstract base. Sub-classes implement `ask(query) -> Dict`."""
    name: str = "abstract"

    def ask(self, query: str) -> Dict:
        raise NotImplementedError


class LocalAdapter(Adapter):
    """Direct in-process invocation of `BuildAgent`. Fastest path. Used by
    CI and local iteration. Requires the agent module to be importable.
    """

    name = "local"

    def __init__(self):
        from src.search import SessionIndex
        from src.agent import BuildAgent
        self._agent = BuildAgent(SessionIndex())
        self.rag_enabled = self._agent.rag_enabled

    def ask(self, query: str) -> Dict:
        t0 = time.perf_counter()
        out = self._agent.answer(query, include_trace=True)
        observed_ms = int((time.perf_counter() - t0) * 1000)
        out["_latency_ms_observed"] = observed_ms
        return out


class HTTPAdapter(Adapter):
    """Invoke the deployed `/api/chat`. Requires the server to have
    `EVAL_TRACE_ENABLED=1` set for `eval_trace` to be populated.
    """

    name = "http"

    def __init__(self, base_url: str, timeout: float = 90.0):
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(timeout=timeout)

    def ask(self, query: str) -> Dict:
        t0 = time.perf_counter()
        r = self._client.post(
            f"{self.base_url}/api/chat",
            json={"message": query},
            headers={"X-Eval-Trace": "1", "Content-Type": "application/json"},
        )
        observed_ms = int((time.perf_counter() - t0) * 1000)
        if r.status_code != 200:
            return {
                "answer": "",
                "kind": "http_error",
                "session_codes": [],
                "eval_trace": None,
                "_latency_ms_observed": observed_ms,
                "_http_status": r.status_code,
                "_http_body": r.text[:500],
            }
        out = r.json()
        out["_latency_ms_observed"] = observed_ms
        return out


def make_adapter(url: Optional[str] = None) -> Adapter:
    if url:
        return HTTPAdapter(url)
    return LocalAdapter()
