"""BM25 + sentence-extraction search over Build 2026 session AI summaries."""
import json
import re
from pathlib import Path
from typing import List, Dict, Optional

from rank_bm25 import BM25Okapi

DATA_PATH = Path(__file__).parent.parent / "data" / "sessions.json"
ANNOUNCEMENT_PATH = Path(__file__).parent.parent / "Announcement.md"

_TOKEN_RE = re.compile(r"[A-Za-z0-9_+]+")
_SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")


def _tokenize(text: str) -> List[str]:
    return [t.lower() for t in _TOKEN_RE.findall(text or "")]


class SessionIndex:
    """Loads sessions.json, builds BM25 over searchable text, supports
    keyword + sentence retrieval."""

    def __init__(self, data_path: Path = DATA_PATH):
        self.data_path = data_path
        self._load()

    def _load(self):
        with open(self.data_path) as f:
            data = json.load(f)
        self.sessions: List[Dict] = data["sessions"]
        # Build searchable corpus
        self.corpus_tokens: List[List[str]] = []
        for s in self.sessions:
            def _s(v):
                if v is None: return ""
                if isinstance(v, list): return " ".join(str(x) for x in v)
                return str(v)
            title = _s(s.get("title"))
            blob = " ".join([
                title * 3,
                _s(s.get("description")),
                _s(s.get("aiSummary")),
                _s(s.get("speakers")),
                _s(s.get("topic")),
            ])
            self.corpus_tokens.append(_tokenize(blob))
        self.bm25 = BM25Okapi(self.corpus_tokens)

    def reload(self):
        self._load()

    def search(self, query: str, k: int = 5,
               require_ai: bool = False,
               restrict_codes: Optional[List[str]] = None) -> List[Dict]:
        toks = _tokenize(query)
        if not toks:
            return []
        scores = self.bm25.get_scores(toks)
        ranked = sorted(
            range(len(self.sessions)),
            key=lambda i: -scores[i],
        )
        out = []
        for i in ranked:
            if scores[i] <= 0:
                break
            s = self.sessions[i]
            if require_ai and not s.get("hasAI"):
                continue
            if restrict_codes and s["code"] not in restrict_codes:
                continue
            out.append({**s, "_score": float(scores[i])})
            if len(out) >= k:
                break
        return out

    def find_sentences(self, query: str, sessions: List[Dict],
                       max_sentences_per_session: int = 3,
                       window: int = 1) -> List[Dict]:
        """For each session, find sentences in aiSummary that contain query
        keywords; return them with a one-sentence-before/after context window."""
        q_keywords = [t for t in _tokenize(query) if len(t) >= 3]
        if not q_keywords:
            return []
        # Treat each token as required to score, but only require at least one
        results = []
        for s in sessions:
            summ = s.get("aiSummary", "") or ""
            if not summ:
                continue
            sents = _SENT_SPLIT_RE.split(summ)
            scored = []
            for idx, sent in enumerate(sents):
                low = sent.lower()
                hits = sum(1 for kw in q_keywords if kw in low)
                if hits == 0:
                    continue
                length_penalty = 0 if 60 <= len(sent) <= 500 else 1
                # Prefer sentences with announcement signal words
                signal_bonus = 0
                for sig in ("announc", "introduc", "preview", "available",
                            "launch", "new", "today"):
                    if sig in low:
                        signal_bonus += 1
                score = hits * 3 + signal_bonus - length_penalty
                scored.append((score, idx, sent))
            scored.sort(reverse=True)
            picks = scored[:max_sentences_per_session]
            picks.sort(key=lambda x: x[1])  # restore textual order
            session_hits = []
            for score, idx, sent in picks:
                ctx_start = max(0, idx - window)
                ctx_end = min(len(sents), idx + window + 1)
                session_hits.append({
                    "sentence": sent,
                    "context_before": sents[ctx_start:idx],
                    "context_after": sents[idx + 1:ctx_end],
                    "score": score,
                })
            if session_hits:
                results.append({"session": s, "hits": session_hits})
        return results

    def by_code(self, code: str) -> Optional[Dict]:
        for s in self.sessions:
            if s.get("code", "").upper() == code.upper():
                return s
        return None
