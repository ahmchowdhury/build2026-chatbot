"""Azure-grounded RAG pipeline: hybrid search (BM25 + vector) on Azure AI
Search, with grounded answer synthesis via Azure OpenAI chat completions.

Hard speaker filter happens BEFORE search (we set $filter on the search query),
so "What did Naomi say about prompt caching?" can only ever return sentences
from sessions where Naomi is a listed speaker.

Falls back to local BM25 if the Azure clients can't be initialised.
"""
from __future__ import annotations

import json
import os
import re
import threading
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import httpx

INDEX_NAME = os.environ.get("AZURE_SEARCH_INDEX", "build2026-chunks")


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    v = os.environ.get(name)
    if v is None or v.strip() == "":
        return default
    return v.strip()


class AzureRAG:
    """Thin wrapper around Azure AI Search + Azure OpenAI for our use case.

    Uses the REST API directly to keep the deps minimal — no `openai` or
    `azure-search-documents` SDK install needed.
    """

    def __init__(self):
        self.search_endpoint = _env("AZURE_SEARCH_ENDPOINT")
        self.search_key = _env("AZURE_SEARCH_KEY")
        self.search_index = _env("AZURE_SEARCH_INDEX", INDEX_NAME)

        self.aoai_endpoint = _env("AZURE_OPENAI_ENDPOINT")
        self.aoai_key = _env("AZURE_OPENAI_KEY")
        self.aoai_chat_deployment = _env(
            "AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-4.1-mini"
        )
        self.aoai_embed_deployment = _env(
            "AZURE_OPENAI_EMBED_DEPLOYMENT", "text-embedding-ada-002"
        )
        self.aoai_api_version = _env(
            "AZURE_OPENAI_API_VERSION", "2024-10-21"
        )
        self.search_api_version = _env(
            "AZURE_SEARCH_API_VERSION", "2024-07-01"
        )

        # Quick budget controls
        self.top_k = int(_env("RAG_TOP_K", "8") or "8")
        self.embed_dim = int(_env("RAG_EMBED_DIM", "1536") or "1536")

        self._client = httpx.Client(timeout=60.0)
        self._embed_lock = threading.Lock()

    # ---------- availability ----------

    def is_configured(self) -> bool:
        return all([
            self.search_endpoint, self.search_key,
            self.aoai_endpoint, self.aoai_key,
        ])

    # ---------- AOAI helpers ----------

    def embed(self, texts: List[str]) -> List[List[float]]:
        """Compute embeddings for a batch of texts via Azure OpenAI.
        Honors 429 + Retry-After with exponential backoff."""
        if not self.aoai_endpoint or not self.aoai_key:
            raise RuntimeError("Azure OpenAI not configured.")
        url = (
            f"{self.aoai_endpoint.rstrip('/')}/openai/deployments/"
            f"{self.aoai_embed_deployment}/embeddings"
            f"?api-version={self.aoai_api_version}"
        )
        import time as _t
        delay = 1.0
        for attempt in range(8):
            with self._embed_lock:
                r = self._client.post(
                    url,
                    headers={"api-key": self.aoai_key,
                             "Content-Type": "application/json"},
                    json={"input": texts},
                )
            if r.status_code == 200:
                return [d["embedding"] for d in r.json()["data"]]
            if r.status_code == 429:
                ra = r.headers.get("retry-after") or r.headers.get("retry-after-ms")
                wait = float(ra) if ra and ra.replace(".", "").isdigit() else delay
                # cap at a sensible max
                wait = min(max(wait, 1.0), 60.0)
                _t.sleep(wait)
                delay = min(delay * 2, 60.0)
                continue
            raise RuntimeError(f"embed failed {r.status_code}: {r.text[:300]}")
        raise RuntimeError("embed failed: rate limit exhausted retries")

    def chat(self, messages: List[Dict], temperature: float = 0.1,
             max_tokens: int = 900) -> str:
        url = (
            f"{self.aoai_endpoint.rstrip('/')}/openai/deployments/"
            f"{self.aoai_chat_deployment}/chat/completions"
            f"?api-version={self.aoai_api_version}"
        )
        r = self._client.post(
            url,
            headers={"api-key": self.aoai_key,
                     "Content-Type": "application/json"},
            json={
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": 0.9,
            },
        )
        if r.status_code == 400:
            # Most commonly: content filter blocked either prompt or response.
            # Surface a structured refusal so downstream classification still
            # works (this answer trips _answer_is_refusal → kind=not-found).
            try:
                err = r.json().get("error", {})
                msg = str(err).lower()
            except Exception:
                msg = r.text.lower()
            if "content management policy" in msg or "content_filter" in msg:
                return (
                    "I can't respond to that request. It appears to contain "
                    "content that the safety filter blocked. There is no "
                    "Microsoft Build 2026 information I can share for this "
                    "query — try rephrasing or asking about a specific "
                    "session or topic."
                )
        if r.status_code != 200:
            raise RuntimeError(f"chat failed {r.status_code}: {r.text[:300]}")
        return r.json()["choices"][0]["message"]["content"]

    # ---------- Search helpers ----------

    def hybrid_search(
        self,
        query: str,
        speaker_codes: Optional[List[str]] = None,
        topic_filter: Optional[str] = None,
        k: Optional[int] = None,
    ) -> List[Dict]:
        """Hybrid BM25 + vector search with optional speaker hard-filter.

        Returns ranked passages with metadata. Each passage is one paragraph
        from a session AI summary.
        """
        if not (self.search_endpoint and self.search_key):
            return []
        k = k or self.top_k

        # 1. Embed the query
        try:
            q_vec = self.embed([query])[0]
        except Exception as e:
            print(f"embed failed (falling back to keyword-only): {e}")
            q_vec = None

        # 2. Build filter expression
        filters: List[str] = []
        if speaker_codes:
            quoted = ", ".join(f"'{c}'" for c in speaker_codes)
            filters.append(f"search.in(sessionCode, '{','.join(speaker_codes)}', ',')")
        if topic_filter:
            filters.append(f"topic eq '{topic_filter}'")
        filter_str = " and ".join(filters) if filters else None

        # 3. Construct search request
        body: Dict = {
            "search": query,
            "queryType": "simple",
            "select": ("id,sessionCode,sessionTitle,speakers,topic,"
                       "level,sessionType,passage,timestamps,"
                       "sessionPage,transcriptUrl,videoUrl"),
            "top": k,
        }
        if filter_str:
            body["filter"] = filter_str
        if q_vec is not None:
            body["vectorQueries"] = [{
                "kind": "vector",
                "vector": q_vec,
                "fields": "passageVector",
                "k": k * 2,
            }]
        url = (
            f"{self.search_endpoint.rstrip('/')}/indexes/"
            f"{self.search_index}/docs/search"
            f"?api-version={self.search_api_version}"
        )
        r = self._client.post(
            url,
            headers={"api-key": self.search_key,
                     "Content-Type": "application/json"},
            json=body,
        )
        if r.status_code != 200:
            print(f"search failed {r.status_code}: {r.text[:300]}")
            return []
        return r.json().get("value", [])

    # ---------- Grounded answer ----------

    def grounded_answer(
        self,
        query: str,
        passages: List[Dict],
        speaker_filter: Optional[str] = None,
    ) -> str:
        """Use the chat model to synthesize an answer strictly grounded in the
        provided passages. Refuses to answer if passages are insufficient."""
        if not passages:
            if speaker_filter:
                return (f"I couldn't find any Microsoft Build 2026 session "
                        f"where **{speaker_filter}** discusses *“{query}”*. "
                        f"Try removing the speaker name to broaden the search, "
                        f"or check if the name was spelled differently.")
            return (f"I couldn't find any Microsoft Build 2026 content for "
                    f"*“{query}”*. Try different keywords, a session code, "
                    f"or type **`topics`** to see what I cover.")

        # Compose grounding context
        ctx_blocks = []
        for i, p in enumerate(passages, 1):
            ctx_blocks.append(
                f"[{i}] Session **[{p['sessionCode']}] {p['sessionTitle']}**\n"
                f"Speakers: {p.get('speakers', '—')}\n"
                f"Page: {p.get('sessionPage', '')}\n"
                f"Transcript: {p.get('transcriptUrl', 'n/a')}\n"
                f"Excerpt: {p['passage']}\n"
            )
        context = "\n---\n".join(ctx_blocks)

        speaker_clause = (
            f"\n\nIMPORTANT: The user named **{speaker_filter}** as a speaker. "
            f"Only quote sentences in the passages that explicitly involve "
            f"{speaker_filter} (look for that name in the excerpt). If no "
            f"passage mentions {speaker_filter}, say so honestly."
        ) if speaker_filter else ""

        system = (
            "You are an expert Microsoft Build 2026 analyst. Answer the user's "
            "question STRICTLY using the provided session excerpts. \n\n"
            "Rules:\n"
            "1. Quote excerpts verbatim using > markdown blockquotes.\n"
            "2. Always cite by session code in square brackets (e.g. [BRK230]) "
            "and link the session page when first referenced.\n"
            "3. Preserve any timestamps in the excerpts (e.g. 00:32:00).\n"
            "4. If the excerpts don't actually answer the question, say so "
            "explicitly — do not invent details.\n"
            "5. Use second-level markdown headers and concise prose. Add a "
            "short '— *Source:* [code] *Speakers:* …' footer line for the "
            "primary session you're quoting.\n"
            "6. Keep the answer under 350 words unless the user asked for a "
            "summary." + speaker_clause
        )

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content":
                f"Question: {query}\n\nSession excerpts:\n{context}"},
        ]
        return self.chat(messages)
