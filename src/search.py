"""BM25 + sentence-extraction search over Build 2026 session AI summaries."""
import json
import re
from pathlib import Path
from typing import List, Dict, Optional, Set

from rank_bm25 import BM25Okapi

from .entities import STOPWORDS

DATA_PATH = Path(__file__).parent.parent / "data" / "sessions.json"
ANNOUNCEMENT_PATH = Path(__file__).parent.parent / "Announcement.md"

_TOKEN_RE = re.compile(r"[A-Za-z0-9_+]+")
_SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")


def _tokenize(text: str, drop_stopwords: bool = False) -> List[str]:
    toks = [t.lower() for t in _TOKEN_RE.findall(text or "")]
    if drop_stopwords:
        toks = [t for t in toks if t not in STOPWORDS and len(t) > 1]
    return toks


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
               restrict_codes: Optional[Set[str]] = None,
               drop_stopwords: bool = True) -> List[Dict]:
        """BM25 search.

        - If `restrict_codes` is provided, only those sessions are eligible
          (the speaker hard-filter goes here).
        - If `drop_stopwords` is True (default), strip English stopwords from
          the query so "what did Naomi say about prompt caching" reduces to
          "naomi prompt caching" — much cleaner BM25.
        """
        toks = _tokenize(query, drop_stopwords=drop_stopwords)
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
            if restrict_codes is not None and s["code"] not in restrict_codes:
                continue
            out.append({**s, "_score": float(scores[i])})
            if len(out) >= k:
                break
        return out

    def find_sentences(self, query: str, sessions: List[Dict],
                       max_sentences_per_session: int = 3,
                       window: int = 1,
                       speaker_tokens: Optional[List[str]] = None) -> List[Dict]:
        """For each session, find sentences in aiSummary that contain query
        keywords; return them with a one-sentence-before/after context window.

        If `speaker_tokens` is provided (e.g. ["naomi", "moneypenny"] for
        "Naomi Moneypenny"), sentences mentioning the speaker get a large
        score bonus, and we *require* at least one such sentence per session
        before returning anything for that session.
        """
        q_keywords = [t for t in _tokenize(query, drop_stopwords=True)
                      if len(t) >= 3]
        if not q_keywords and not speaker_tokens:
            return []
        speaker_tokens_low = [t.lower() for t in (speaker_tokens or [])]
        results = []
        for s in sessions:
            summ = s.get("aiSummary", "") or ""
            if not summ:
                continue
            sents = _SENT_SPLIT_RE.split(summ)
            scored = []
            for idx, sent in enumerate(sents):
                low = sent.lower()
                topic_hits = sum(1 for kw in q_keywords if kw in low)
                speaker_hit = any(tok in low for tok in speaker_tokens_low) \
                    if speaker_tokens_low else False
                if not topic_hits and not speaker_hit:
                    continue
                length_penalty = 0 if 60 <= len(sent) <= 500 else 1
                signal_bonus = 0
                for sig in ("announc", "introduc", "preview", "available",
                            "launch", "new", "today"):
                    if sig in low:
                        signal_bonus += 1
                # Big bonus when the sentence mentions both the speaker and a
                # topic keyword — that's exactly what the user asked for.
                speaker_bonus = 0
                if speaker_hit:
                    speaker_bonus += 6
                if speaker_hit and topic_hits:
                    speaker_bonus += 6
                score = topic_hits * 3 + signal_bonus + speaker_bonus - length_penalty
                scored.append((score, idx, sent, speaker_hit, topic_hits))
            if not scored:
                continue
            # If a speaker filter was requested, require at least ONE sentence
            # in this session to mention the speaker (otherwise the AI summary
            # never references them — they may be a co-speaker but didn't
            # discuss this topic).
            if speaker_tokens_low and not any(sp for _, _, _, sp, _ in scored):
                continue
            scored.sort(reverse=True)
            picks = scored[:max_sentences_per_session]
            picks.sort(key=lambda x: x[1])  # restore textual order
            session_hits = []
            for score, idx, sent, sp, th in picks:
                ctx_start = max(0, idx - window)
                ctx_end = min(len(sents), idx + window + 1)
                session_hits.append({
                    "sentence": sent,
                    "context_before": sents[ctx_start:idx],
                    "context_after": sents[idx + 1:ctx_end],
                    "score": score,
                    "speaker_hit": sp,
                    "topic_hits": th,
                })
            if session_hits:
                results.append({"session": s, "hits": session_hits})
        # Order results: sessions with at least one speaker+topic sentence
        # first, then by best individual score.
        def _sort_key(r):
            best = max(r["hits"], key=lambda h: h["score"])
            return (-int(best.get("speaker_hit") and best.get("topic_hits") > 0),
                    -best["score"])
        results.sort(key=_sort_key)
        return results

    def by_code(self, code: str) -> Optional[Dict]:
        for s in self.sessions:
            if s.get("code", "").upper() == code.upper():
                return s
        return None
