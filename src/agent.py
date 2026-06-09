"""Agentic orchestrator. Routes a user question through entity extraction,
hybrid retrieval, and grounded synthesis.

Flow:
  1. Detect intent (specific question / topic summary / session lookup / help).
  2. Extract entities — speakers, session codes, topics — from the query.
  3. If a speaker is mentioned, HARD-FILTER retrieval to that speaker's
     sessions only (this is what makes "What did Naomi say about prompt
     caching?" never return a session that lacks Naomi as a speaker).
  4. Run hybrid Azure AI Search (BM25 + vector) when configured; fall back to
     local BM25 + sentence extraction otherwise.
  5. Synthesize a grounded answer via Azure OpenAI when configured; otherwise
     render a clean template answer.

Both modes preserve exact citations: session code, speakers, timestamps, link
to the official session page and transcript.
"""
import os
import re
import time
from typing import Dict, List, Optional, Set

from .entities import (build_speaker_index, detect_speakers,
                       detect_session_code, expand_query_for_speaker)
from .rag import AzureRAG
from .agentic_rag import AgenticRAG
from .search import SessionIndex
from .topics import TOPICS, detect_topic_in_query, filter_sessions_by_topic, list_topics

SESSION_URL = "https://build.microsoft.com/en-US/sessions/{code}"

# Heuristic patterns that mean "the model's answer is a refusal, even though
# it came from the grounded-synthesis path". When we detect this we demote
# `kind` from "answer-rag" to "not-found" so eval / downstream consumers can
# trust the structural signal. This is intentionally conservative — only
# matches at the start of the answer (first ~400 chars).
_REFUSAL_PATTERNS = re.compile(
    r"(?ix)\b(?:"
    r"there \s+ is \s+ no \s+ (?:mention|information|reference|indication|record) \s+ of"
    r"| is \s+ not \s+ mentioned \s+ in \s+ (?:the|any|provided)"
    r"| (?:do|does|did) \s+ not \s+ (?:mention|reference|discuss|include|cover|appear|contain)"
    r"| (?:are|is) \s+ not \s+ (?:covered|included|present|listed|available)"
    r"| (?:i|the \s+ provided \s+ session \s+ excerpts) \s+ (?:could \s+ not|couldn'?t|cannot|can'?t) \s+ find"
    r"| (?:i|we) \s+ (?:do|don'?t|do \s+ not) \s+ (?:see|find) \s+ (?:any|a|the)?"
    r"| no \s+ (?:session|excerpt|reference|mention) \s+ (?:in|of|for|about)"
    r"| no \s+ information \s+ (?:is)? \s* provided"
    r"| not \s+ specifically \s+ (?:mentioned|discussed|covered)"
    r"| there \s+ is \s+ no \s+ information"
    r"| the \s+ excerpts \s+ provided \s+ do \s+ not"
    r"| (?:the \s+ provided \s+ session \s+ excerpts|the \s+ retrieved \s+ context) \s+ do \s+ not \s+ contain"
    r"| i \s+ can'?t \s+ (?:respond|answer|help|provide|confirm)"
    r"| i \s+ cannot \s+ (?:respond|answer|help|provide|confirm)"
    r"| the \s+ prompt \s+ was \s+ filtered"
    r"| this \s+ claim \s+ is \s+ (?:false|incorrect|not \s+ supported)"
    r"| that \s+ (?:statement|claim) \s+ is \s+ (?:false|incorrect)"
    r")\b"
)


def _answer_is_refusal(answer: str) -> bool:
    """True when the synthesised answer is materially a refusal — i.e. the
    model is saying "no such thing in this corpus". Used to reclassify the
    `kind` field after a grounded-synthesis call.
    """
    if not answer:
        return True
    # Look at the first 400 chars (the lead is where refusals live) plus any
    # detect anywhere in the first 1200.
    head = answer[:400]
    body = answer[:1200]
    return bool(_REFUSAL_PATTERNS.search(head)
                or _REFUSAL_PATTERNS.search(body))

# When True, every reply includes an `eval_trace` field with retrieval
# diagnostics (detected speakers, filter applied, retrieved passages with
# scores, latency). Used by the eval harness; **disabled by default** in prod.
EVAL_TRACE_ENABLED = os.environ.get("EVAL_TRACE_ENABLED", "").lower() in ("1", "true", "yes")


def _format_session_link(session: Dict) -> str:
    code = session.get("code", "")
    title = session.get("title", "")
    return f"**[{code}]** *{title}* — {SESSION_URL.format(code=code)}"


def _format_speakers(session: Dict) -> str:
    speakers = session.get("speakers")
    if not speakers:
        return "—"
    if isinstance(speakers, list):
        return ", ".join(str(s) for s in speakers if s)
    return str(speakers)


SUMMARY_INTENT = re.compile(
    r"(?i)\b(summari[sz]e|list|all|give me|show me|what(?:\'s| is) covered|sessions? (?:on|about|for))\b"
)
LIST_TOPICS_INTENT = re.compile(r"(?i)\b(?:what )?topics?(?: do you know| are available)?\??$")
HELP_INTENT = re.compile(r"(?i)^\s*(help|how do i|what can you do|examples?)\b")
GREETING_INTENT = re.compile(
    r"(?ix) ^ \s* (?: hi | hey | hello | yo | hiya | sup | greetings | "
    r"good \s+ (?:morning|afternoon|evening) ) [\s!.,]* $"
)


class BuildAgent:
    def __init__(self, index: SessionIndex):
        self.index = index
        self.speaker_idx = build_speaker_index(self.index.sessions)
        self.rag = AzureRAG()
        self.rag_enabled = self.rag.is_configured()
        self.agentic = AgenticRAG()
        # USE_AGENTIC_RETRIEVAL=1 makes the agent prefer the
        # /knowledgebases/.../retrieve pipeline. The legacy hybrid path is
        # kept as the automatic fallback (and as a comparison baseline for
        # eval).
        self.agentic_enabled = (
            self.agentic.is_configured()
            and os.environ.get("USE_AGENTIC_RETRIEVAL", "").lower()
            in ("1", "true", "yes")
        )
        if self.agentic_enabled:
            print(f"BuildAgent: Agentic Retrieval enabled "
                  f"(KB={self.agentic.kb_name}, KS={self.agentic.ks_name})")
        elif self.rag_enabled:
            print("BuildAgent: Azure RAG enabled (hybrid search + grounded synthesis)")
        else:
            print("BuildAgent: Azure RAG not configured — using local BM25 fallback")

    # --- Public API ---

    def answer(self, query: str, include_trace: bool = False) -> Dict:
        """Answer a user query. When `include_trace` is True (or
        EVAL_TRACE_ENABLED env var is set), the reply will include an
        `eval_trace` field with retrieval diagnostics. Used by the eval
        harness; safe to leave off in production.
        """
        t0 = time.perf_counter()
        trace_on = include_trace or EVAL_TRACE_ENABLED
        trace: Dict = {
            "query": query,
            "detected_speakers": [],
            "speaker_label": None,
            "speaker_filter_codes": None,
            "detected_topics": [],
            "detected_session_code": None,
            "intent": None,
            "search_query": None,
            "retrieved": [],
            "rag_path": False,
            "latency_ms": None,
        } if trace_on else None

        query = (query or "").strip()
        if not query:
            return self._reply(
                "Ask me anything about Microsoft Build 2026 — a feature, a "
                "product, a session code, or a whole topic like 'AI Foundry' "
                "or 'Windows'.",
                kind="hint", trace=trace, t0=t0,
            )

        if HELP_INTENT.search(query):
            if trace is not None:
                trace["intent"] = "help"
            return self._help(trace=trace, t0=t0)
        if GREETING_INTENT.match(query):
            if trace is not None:
                trace["intent"] = "greeting"
            return self._reply(
                "Hi! I'm a Microsoft Build 2026 chatbot. Try asking a "
                "specific question (*“what did Naomi say about prompt "
                "caching?”*), a topic summary (*“summarize Foundry sessions”*), "
                "or a session code (*BRK230*). Type **`help`** for examples "
                "or **`topics`** for what I cover.",
                kind="hint", trace=trace, t0=t0,
            )
        if LIST_TOPICS_INTENT.match(query):
            if trace is not None:
                trace["intent"] = "topics"
            return self._reply(self._render_topics(), kind="topics",
                               extras={"topics": list_topics()},
                               trace=trace, t0=t0)

        # Direct session-code lookup
        code = detect_session_code(query)
        if code:
            if trace is not None:
                trace["detected_session_code"] = code
                trace["intent"] = "session-lookup"
            s = self.index.by_code(code)
            if s:
                return self._render_session_card(s, query, trace=trace, t0=t0)
            # Code was detected but doesn't exist in the catalog — refuse
            # cleanly. Without this, the agent falls through to RAG and the
            # model invariably hallucinates plausible-but-wrong details
            # about the non-existent session.
            return self._reply(
                f"There's no Microsoft Build 2026 session with code "
                f"**{code}**. Session codes look like *BRK230*, *KEY01*, "
                f"*OD823* — double-check the code or type **`topics`** to "
                f"browse what's in the catalog.",
                kind="not-found",
                extras={"detected_code": code},
                trace=trace, t0=t0,
            )

        # Topic detection
        topics = detect_topic_in_query(query)
        is_summary = bool(SUMMARY_INTENT.search(query))
        if trace is not None:
            trace["detected_topics"] = topics
        if topics and is_summary:
            if trace is not None:
                trace["intent"] = "topic-summary"
            return self._render_topic_summary(topics[0], query,
                                              trace=trace, t0=t0)

        # Entity extraction — does the user name a speaker?
        speakers = detect_speakers(query, self.speaker_idx)
        speaker_codes: Optional[Set[str]] = None
        speaker_label: Optional[str] = None
        speaker_tokens: List[str] = []
        if speakers:
            # Union of session codes from all matched speakers
            speaker_codes = set()
            for name, codes in speakers:
                speaker_codes |= codes
                for tok in re.split(r"\s+", name):
                    if len(tok) >= 3:
                        speaker_tokens.append(tok)
            speaker_label = max((name for name, _ in speakers), key=len).title()

        if trace is not None:
            trace["detected_speakers"] = [n for n, _ in speakers]
            trace["speaker_label"] = speaker_label
            trace["speaker_filter_codes"] = sorted(speaker_codes) if speaker_codes else None
            if self.agentic_enabled:
                trace["intent"] = "agentic"
            elif self.rag_enabled:
                trace["intent"] = "rag"
            else:
                trace["intent"] = "local"

        # Preferred path: agentic retrieval (KB-driven query planning +
        # answer synthesis). Falls back to legacy hybrid on failure.
        if self.agentic_enabled:
            try:
                return self._render_agentic_answer(
                    query, speaker_codes, speaker_label, speaker_tokens,
                    topics, trace=trace, t0=t0,
                )
            except Exception as e:
                print(f"agentic retrieve failed, falling back to hybrid: {e}")
                if trace is not None:
                    trace["agentic_error"] = str(e)[:300]

        # Hybrid retrieval via Azure RAG when available
        if self.rag_enabled:
            return self._render_rag_answer(
                query, speaker_codes, speaker_label, speaker_tokens, topics,
                trace=trace, t0=t0,
            )
        return self._render_local_answer(
            query, speaker_codes, speaker_label, speaker_tokens, topics,
            trace=trace, t0=t0,
        )

    # --- Renderers ---

    def _help(self, trace: Optional[Dict] = None, t0: float = 0.0) -> Dict:
        body = (
            "**I'm a Microsoft Build 2026 chatbot.** I have AI summaries for "
            "**170+ sessions** and structured metadata for **460 sessions** total. "
            "I can answer in three ways:\n\n"
            "1. **Specific question** — e.g. *“What did Naomi Moneypenny say "
            "about prompt caching?”* — I'll only use sessions where Naomi "
            "actually appears, and quote the AI summary with timestamps and "
            "links.\n"
            "2. **Topic summary** — e.g. *“Summarize all AI Foundry sessions”* "
            "— I'll list every matching session with its AI summary excerpt.\n"
            "3. **Session lookup** — type any session code (e.g. *BRK230*, "
            "*KEY01*) for a full card.\n\n"
            "Topics I know: " + ", ".join(f"*{t}*" for t in TOPICS.keys())
        )
        return self._reply(body, kind="help", trace=trace, t0=t0)

    def _render_topics(self) -> str:
        out = ["**Topics I cover at Microsoft Build 2026:**", ""]
        for t in list_topics():
            out.append(f"- **{t['name']}** — {t['description']}")
        out.append("")
        out.append("Try: *“summarize Windows sessions”* or *“what's new in AI Foundry?”*")
        return "\n".join(out)

    def _render_session_card(self, s: Dict, query: str,
                             trace: Optional[Dict] = None,
                             t0: float = 0.0) -> Dict:
        def _flat(v):
            if v is None: return ""
            if isinstance(v, list): return ", ".join(str(x) for x in v if x)
            return str(v)
        lines = []
        lines.append(f"## [{s['code']}] {s['title']}")
        lines.append("")
        lines.append(f"**Speakers:** {_format_speakers(s)}  ")
        if s.get("level"):
            lines.append(f"**Level:** {_flat(s['level'])}  ")
        if s.get("type"):
            lines.append(f"**Type:** {_flat(s['type'])}  ")
        if s.get("duration"):
            lines.append(f"**Duration:** {s['duration']} min  ")
        lines.append(f"**Page:** {SESSION_URL.format(code=s['code'])}")
        if s.get("video"):
            lines.append(f"**Video:** {s['video']}")
        if s.get("transcript"):
            lines.append(f"**Transcript:** {s['transcript']}")
        if s.get("deck"):
            lines.append(f"**Slides:** {s['deck']}")
        lines.append("")

        if s.get("aiSummary"):
            specific = [t for t in re.findall(r"[A-Za-z]+", query.lower())
                        if len(t) >= 4 and t not in {"about", "tell", "what", "session"}]
            if specific:
                hits = self.index.find_sentences(query, [s], max_sentences_per_session=4)
                if hits and hits[0]["hits"]:
                    lines.append("**Most relevant excerpts:**")
                    lines.append("")
                    for h in hits[0]["hits"]:
                        lines.append(f"> {h['sentence']}")
                        lines.append("")
            lines.append("**AI Summary (excerpt):**")
            lines.append("")
            excerpt = s["aiSummary"][:1200]
            if len(s["aiSummary"]) > 1200:
                excerpt += "…"
            lines.append(excerpt)
        else:
            lines.append("_AI summary not yet available for this session._")
        # Populate trace.retrieved with the session's AI summary PLUS the
        # canonical metadata (so the eval judge can ground claims like
        # "Duration: 45 min", "Video: https://..." which are factual fields
        # rendered into the card but live in the JSON, not the summary
        # text).
        if trace is not None:
            meta_lines: List[str] = []
            if s.get("speakers"):
                meta_lines.append(f"Speakers: {_format_speakers(s)}")
            if s.get("level"):
                meta_lines.append(f"Level: {s['level']}")
            if s.get("type"):
                meta_lines.append(f"Type: {s['type']}")
            if s.get("duration"):
                meta_lines.append(f"Duration: {s['duration']} min")
            meta_lines.append(f"Page: {SESSION_URL.format(code=s['code'])}")
            if s.get("video"):
                meta_lines.append(f"Video: {s['video']}")
            if s.get("transcript"):
                meta_lines.append(f"Transcript: {s['transcript']}")
            if s.get("deck"):
                meta_lines.append(f"Slides: {s['deck']}")
            meta_blob = "\n".join(meta_lines)
            passage = (meta_blob + "\n\nAI Summary:\n"
                       + (s.get("aiSummary") or "_(no AI summary)_"))[:6000]
            trace["retrieved"] = [{
                "rank": 1,
                "sessionCode": s.get("code"),
                "sessionTitle": s.get("title"),
                "speakers": s.get("speakers"),
                "score": None,
                "passage": passage,
            }]
        return self._reply("\n".join(lines), kind="session",
                           extras={"session": s,
                                   "session_codes": [s["code"]]},
                           trace=trace, t0=t0)

    def _render_topic_summary(self, topic_name: str, query: str,
                              trace: Optional[Dict] = None,
                              t0: float = 0.0) -> Dict:
        matches = filter_sessions_by_topic(self.index.sessions, topic_name)
        with_ai = [s for s in matches if s.get("hasAI")]
        without = [s for s in matches if not s.get("hasAI")]
        ordered = with_ai + without

        if not ordered:
            return self._not_found(topic_name, trace=trace, t0=t0)

        cfg = TOPICS[topic_name]
        lines = [f"## {topic_name} at Microsoft Build 2026", "", cfg["description"], ""]
        lines.append(f"**{len(ordered)} sessions** match this topic "
                     f"({len(with_ai)} have AI summaries).")
        lines.append("")

        for s in ordered[:25]:
            code = s["code"]
            title = s["title"]
            url = SESSION_URL.format(code=code)
            lines.append(f"### [{code}] {title}")
            lines.append(f"*{_format_speakers(s)}* · [Session page]({url})"
                         + (f" · [Transcript]({s['transcript']})" if s.get("transcript") else ""))
            lines.append("")
            if s.get("aiSummary"):
                sents = re.split(r"(?<=[.!?])\s+(?=[A-Z])", s["aiSummary"])
                excerpt = " ".join(sents[:2])[:600]
                lines.append(f"> {excerpt}")
                lines.append("")
        if len(ordered) > 25:
            lines.append(f"_…and {len(ordered) - 25} more sessions in this topic._")
        # Populate trace.retrieved with each session's AI summary excerpt so
        # the eval judge can ground the topic-summary text against real
        # passages.
        if trace is not None:
            trace["retrieved"] = [
                {
                    "rank": i + 1,
                    "sessionCode": s.get("code"),
                    "sessionTitle": s.get("title"),
                    "speakers": s.get("speakers"),
                    "score": None,
                    "passage": (s.get("aiSummary") or "")[:1500],
                }
                for i, s in enumerate(ordered[:25]) if s.get("aiSummary")
            ]
        return self._reply("\n".join(lines), kind="topic-summary",
                           extras={"topic": topic_name, "count": len(ordered),
                                   "session_codes": [s["code"] for s in ordered]},
                           trace=trace, t0=t0)

    # --- Agentic Retrieval path (preferred) ---

    @staticmethod
    def _strip_unauthorized_citations(answer: str,
                                      allowed_codes: Set[str]) -> str:
        """Remove `[CODE]` citations from `answer` whose code is NOT in
        `allowed_codes`. Defends against the synthesizer hallucinating
        session codes from training memory (we've seen e.g. [BRK230]
        appearing in answers about KEY01 because Naomi/Foundry topics
        co-occur in pretraining). Citations like [Transcript], [Session
        page], or any non-session text in brackets are left intact.
        """
        if not allowed_codes:
            return answer
        # Same regex shape as the eval harness's bracketed-code matcher
        cite_re = re.compile(r"\[([A-Z]{2,4}\d{2,4}(?:-[A-Z0-9]+)?)\]")

        def _sub(m):
            code = m.group(1)
            if code in allowed_codes:
                return m.group(0)
            return ""  # drop hallucinated cite entirely

        cleaned = cite_re.sub(_sub, answer)
        # Also strip numeric/internal-only citation formats that the
        # synthesizer sometimes emits despite our instructions:
        # [ref_id:16], [ref_id: 7], [Source 3], [1], (ref 3), etc.
        # These leak the model's internal reference indexing — they're
        # never meaningful to the end user and the eval judge can't
        # resolve them. Replace with a generic source marker.
        cleaned = re.sub(r"\[ref_id\s*:\s*\d+\]", "", cleaned, flags=re.I)
        cleaned = re.sub(r"\[Source\s+\d+\]", "", cleaned, flags=re.I)
        cleaned = re.sub(r"\(\s*ref\s+\d+\s*\)", "", cleaned, flags=re.I)
        # Tidy up double spaces / orphan punctuation we may have left
        cleaned = re.sub(r" {2,}", " ", cleaned)
        cleaned = re.sub(r" ([,.;:])", r"\1", cleaned)
        return cleaned

    @staticmethod
    def _audit_title_citation_match(answer: str,
                                    refs: List[Dict]) -> str:
        """Fix the 'right session named, wrong code cited' bug. When the
        synthesizer writes a bullet/sentence that explicitly names a
        session by its title (e.g. *"Foundry IQ: Fuel agents with
        enterprise knowledge"*) but cites a DIFFERENT session's code at
        the end (e.g. [BRK230] when BRK246 is the actual Foundry IQ
        session), swap the citation to the correct code.

        Heuristic: for each line of the answer, find any reference title
        that appears in the line (case-insensitive, normalized
        whitespace), then ensure the trailing [CODE] cite on that line
        matches that reference's sessionCode. If it doesn't, replace
        the wrong code with the correct one (preserving any other valid
        cites on the line).
        """
        if not refs:
            return answer

        # Build (normalized_title, code) pairs. Drop very short titles
        # (<20 chars) to avoid false matches on generic phrases.
        def _norm(s: str) -> str:
            return re.sub(r"\s+", " ", (s or "").lower()).strip()

        title_to_code: List[tuple] = []
        for r in refs:
            code = r.get("sessionCode") or ""
            title = _norm(r.get("sessionTitle") or "")
            if code and title and len(title) >= 20:
                title_to_code.append((title, code))
        if not title_to_code:
            return answer

        cite_re = re.compile(r"\[([A-Z]{2,4}\d{2,4}(?:-[A-Z0-9]+)?)\]")
        lines = answer.split("\n")
        fixed_lines: List[str] = []
        for line in lines:
            line_norm = _norm(line)
            matched_codes: List[str] = []
            for t, c in title_to_code:
                if t in line_norm and c not in matched_codes:
                    matched_codes.append(c)
            if matched_codes:
                # The line explicitly names one or more sessions. The cite(s)
                # at the end MUST include those codes. If we find a cite
                # whose code is NOT in matched_codes AND the matched_codes
                # set is non-empty, swap the first wrong cite to the
                # first matched code.
                wrong_cites: List[int] = []
                cites = list(cite_re.finditer(line))
                if cites:
                    have_codes = {m.group(1) for m in cites}
                    missing_codes = [c for c in matched_codes if c not in have_codes]
                    wrong_cites = [i for i, m in enumerate(cites)
                                   if m.group(1) not in matched_codes]
                    if missing_codes and wrong_cites:
                        # Swap the first wrong cite to the first missing
                        # correct code. Build new line by replacing in-place.
                        new_code = missing_codes[0]
                        m = cites[wrong_cites[0]]
                        line = (line[:m.start()] + f"[{new_code}]" +
                                line[m.end():])
                    elif missing_codes and not cites:
                        # No cite at all but a title is named — append.
                        line = line.rstrip() + f" [{missing_codes[0]}]"
            fixed_lines.append(line)
        return "\n".join(fixed_lines)

    def _render_agentic_answer(self, query: str,
                               speaker_codes: Optional[Set[str]],
                               speaker_label: Optional[str],
                               speaker_tokens: List[str],
                               topics_hint: List[str],
                               trace: Optional[Dict] = None,
                               t0: float = 0.0) -> Dict:
        """Single round-trip to /knowledgebases/.../retrieve. The KB does
        query planning, hybrid + semantic-ranked retrieval, AND answer
        synthesis. We just shape the result, append references, and
        run the same refusal-demotion + speaker-purity logic as the
        legacy path."""
        codes_list = sorted(speaker_codes) if speaker_codes else None
        result = self.agentic.retrieve(
            query=query,
            speaker_codes=codes_list,
            speaker_label=speaker_label,
        )
        refs = result["references"]
        answer_md = (result.get("answer") or "").strip()

        if trace is not None:
            trace["rag_path"] = True
            trace["agentic"] = True
            trace["search_query"] = query
            trace["agentic_filter"] = result.get("filter_used")
            trace["agentic_latency_ms"] = result.get("latency_ms")
            trace["agentic_activity"] = [
                {k: a.get(k) for k in ("type", "elapsedMs", "count",
                                       "queryTime", "query", "inputTokens",
                                       "outputTokens")
                 if k in a}
                for a in result.get("activity", [])
            ]
            trace["retrieved"] = [
                {
                    "rank": i + 1,
                    "sessionCode": r.get("sessionCode"),
                    "sessionTitle": r.get("sessionTitle"),
                    "speakers": r.get("speakers"),
                    "score": r.get("score"),
                    # Full passage (not truncated) so the judge can ground
                    # against the same text the synthesizer saw.
                    "passage": (r.get("passage") or "")[:4000],
                }
                for i, r in enumerate(refs)
            ]

        # When the speaker hard-filter wiped out the retrieval, honour our
        # honest-refusal contract (same wording as the hybrid path so the
        # gold cases match either way).
        if speaker_codes is not None and not refs:
            body = (
                f"I searched Microsoft Build 2026 for sessions where "
                f"**{speaker_label}** speaks AND that mention *“{query}”* "
                f"— and got zero matches. \n\n"
                f"It's possible {speaker_label} doesn't discuss this topic in "
                f"any indexed session. Try removing the speaker name to see "
                f"every Build 2026 session that covers this topic.")
            return self._reply(body, kind="not-found",
                               extras={"speaker": speaker_label,
                                       "speaker_codes": codes_list,
                                       "engine": "agentic"},
                               trace=trace, t0=t0)

        if not refs and not answer_md:
            return self._not_found(query, trace=trace, t0=t0)

        # Append a "References" footer with all unique sessions cited.
        seen_codes: Set[str] = set()
        ref_lines: List[str] = []
        for r in refs:
            code = r.get("sessionCode")
            if not code or code in seen_codes:
                continue
            seen_codes.add(code)
            url = SESSION_URL.format(code=code)
            line = f"- **[{code}]** *{r.get('sessionTitle','')}* — [{url}]({url})"
            if r.get("transcriptUrl"):
                line += f" · [Transcript]({r['transcriptUrl']})"
            ref_lines.append(line)

        # Strip any citation whose code wasn't actually retrieved — defends
        # against the synthesizer hallucinating session codes from training
        # memory. Must run BEFORE refusal-detection so the cleaned text is
        # what the user sees AND what citation_support checks.
        answer_md = self._strip_unauthorized_citations(answer_md, seen_codes)
        # Then audit title↔code matching: when a bullet explicitly names
        # session "Foundry IQ: Fuel agents..." but cites [BRK230] instead
        # of [BRK246], swap. This catches gpt-4o's habit of defaulting to
        # the most-cited code in its working set.
        answer_md = self._audit_title_citation_match(answer_md, refs)

        # If the KB produced no answer text but did return references, fall
        # back to a structured listing (rare path — happens when synthesis
        # is gated by content filters).
        if not answer_md:
            answer_md = (f"Here are the Microsoft Build 2026 session "
                         f"excerpts that match *“{query}”*:")

        full = answer_md.strip()
        if ref_lines:
            full += "\n\n---\n**References:**\n" + "\n".join(ref_lines)

        final_kind = "not-found" if _answer_is_refusal(answer_md) else "answer-rag"
        return self._reply(full, kind=final_kind,
                           extras={"speaker": speaker_label,
                                   "session_codes": list(seen_codes),
                                   "engine": "agentic"},
                           trace=trace, t0=t0)

    # --- Hybrid (Azure) path ---

    def _render_rag_answer(self, query: str,
                           speaker_codes: Optional[Set[str]],
                           speaker_label: Optional[str],
                           speaker_tokens: List[str],
                           topics_hint: List[str],
                           trace: Optional[Dict] = None,
                           t0: float = 0.0) -> Dict:
        # When a speaker is named, drop the speaker tokens from the search
        # query so search focuses on the actual topic.
        search_query = query
        if speaker_label:
            search_query = expand_query_for_speaker(query, [(speaker_label.lower(), set())])
            if not search_query.strip():
                search_query = query  # fallback

        codes_list = sorted(speaker_codes) if speaker_codes else None
        passages = self.rag.hybrid_search(
            search_query,
            speaker_codes=codes_list,
            k=8,
        )

        if trace is not None:
            trace["rag_path"] = True
            trace["search_query"] = search_query
            trace["retrieved"] = [
                {
                    "rank": i + 1,
                    "sessionCode": p.get("sessionCode"),
                    "sessionTitle": p.get("sessionTitle"),
                    "speakers": p.get("speakers"),
                    "score": p.get("@search.score"),
                    "passage": (p.get("passage") or "")[:4000],
                }
                for i, p in enumerate(passages)
            ]

        # If a speaker filter was applied AND wiped out everything, tell the
        # user explicitly.
        if speaker_codes is not None and not passages:
            body = (
                f"I searched Microsoft Build 2026 for sessions where "
                f"**{speaker_label}** speaks AND that mention *“{search_query}”* "
                f"— and got zero matches. \n\n"
                f"It's possible {speaker_label} doesn't discuss this topic in "
                f"any indexed session. Try removing the speaker name to see "
                f"every Build 2026 session that covers this topic.")
            return self._reply(body, kind="not-found",
                               extras={"speaker": speaker_label,
                                       "speaker_codes": codes_list},
                               trace=trace, t0=t0)

        if not passages:
            return self._not_found(query, trace=trace, t0=t0)

        # Synthesize grounded answer
        try:
            answer_md = self.rag.grounded_answer(
                query, passages, speaker_filter=speaker_label,
            )
        except Exception as e:
            print(f"grounded_answer failed: {e}")
            return self._render_local_answer(
                query, speaker_codes, speaker_label, speaker_tokens, topics_hint,
                trace=trace, t0=t0,
            )

        # Append a "References" footer with all unique sessions used
        seen_codes: Set[str] = set()
        refs: List[str] = []
        for p in passages:
            code = p.get("sessionCode")
            if not code or code in seen_codes:
                continue
            seen_codes.add(code)
            url = SESSION_URL.format(code=code)
            ref = f"- **[{code}]** *{p.get('sessionTitle','')}* — [{url}]({url})"
            if p.get("transcriptUrl"):
                ref += f" · [Transcript]({p['transcriptUrl']})"
            refs.append(ref)
        full = answer_md.strip() + "\n\n---\n**References:**\n" + "\n".join(refs)
        # If the synthesised answer is materially a refusal ("no mention of
        # ColdFusion in the excerpts") demote `kind` to "not-found" so the
        # structural signal matches the textual one. This is what makes the
        # eval harness's `refusal_correct` check reliable.
        final_kind = "not-found" if _answer_is_refusal(answer_md) else "answer-rag"
        return self._reply(full, kind=final_kind,
                           extras={"speaker": speaker_label,
                                   "session_codes": list(seen_codes)},
                           trace=trace, t0=t0)

    # --- Local-BM25 path (fallback) ---

    def _render_local_answer(self, query: str,
                             speaker_codes: Optional[Set[str]],
                             speaker_label: Optional[str],
                             speaker_tokens: List[str],
                             topics_hint: List[str],
                             trace: Optional[Dict] = None,
                             t0: float = 0.0) -> Dict:
        # Strip the speaker name from the BM25 query so search focuses on
        # the topic itself.
        if speaker_label:
            search_query = expand_query_for_speaker(query, [(speaker_label.lower(), set())])
            if not search_query.strip():
                search_query = query
        else:
            search_query = query

        ai_results = self.index.search(
            search_query, k=12, require_ai=True,
            restrict_codes=speaker_codes,
        )
        if len(ai_results) < 3 and speaker_codes is None:
            extra = self.index.search(search_query, k=5)
            seen = {s["code"] for s in ai_results}
            for r in extra:
                if r["code"] not in seen:
                    ai_results.append(r)

        if trace is not None:
            trace["search_query"] = search_query
            trace["retrieved"] = [
                {
                    "rank": i + 1,
                    "sessionCode": s.get("code"),
                    "sessionTitle": s.get("title"),
                    "speakers": s.get("speakers"),
                    "score": s.get("_score"),
                    "passage": (s.get("aiSummary") or "")[:600],
                }
                for i, s in enumerate(ai_results)
            ]

        if not ai_results:
            if speaker_label:
                body = (
                    f"I couldn't find any Microsoft Build 2026 session where "
                    f"**{speaker_label}** discusses *“{search_query}”*. \n\n"
                    f"This usually means the topic is not covered in any of "
                    f"{speaker_label}'s indexed sessions. Try removing the "
                    f"name to broaden the search."
                )
                return self._reply(body, kind="not-found",
                                   extras={"speaker": speaker_label},
                                   trace=trace, t0=t0)
            return self._not_found(query, trace=trace, t0=t0)

        # Sentence-level extraction with optional speaker bias
        ai_sessions = [s for s in ai_results if s.get("hasAI")][:6]
        sent_results = self.index.find_sentences(
            search_query, ai_sessions,
            max_sentences_per_session=2,
            speaker_tokens=speaker_tokens or None,
        )

        if not sent_results:
            if speaker_label:
                body = (
                    f"I found sessions where **{speaker_label}** speaks, but "
                    f"none of their AI summaries reference *“{search_query}”* "
                    f"directly. Closest matches:"
                )
                for s in ai_results[:5]:
                    body += f"\n- **[{s['code']}]** *{s['title']}* — " \
                            f"{SESSION_URL.format(code=s['code'])}"
                return self._reply(body, kind="weak",
                                   extras={"speaker": speaker_label,
                                           "session_codes": [s["code"] for s in ai_results[:5]]},
                                   trace=trace, t0=t0)
            return self._weak_match(query, ai_results[:5], trace=trace, t0=t0)

        lines = []
        if speaker_label:
            lines.append(f"## What **{speaker_label}** said about "
                         f"*“{search_query}”* at Microsoft Build 2026")
        else:
            lines.append(f"## On *“{query}”* across Microsoft Build 2026")
        lines.append("")
        if topics_hint:
            lines.append(f"_Topic match: {', '.join(topics_hint)}_")
            lines.append("")

        for r in sent_results:
            s = r["session"]
            url = SESSION_URL.format(code=s["code"])
            lines.append(f"### [{s['code']}] {s['title']}")
            lines.append(
                f"*Speakers:* {_format_speakers(s)} · "
                f"[Session page]({url})"
                + (f" · [Transcript]({s['transcript']})" if s.get("transcript") else "")
            )
            lines.append("")
            for h in r["hits"]:
                lines.append(f"> {h['sentence']}")
                lines.append("")

        return self._reply("\n".join(lines), kind="answer-local",
                           extras={"speaker": speaker_label,
                                   "session_codes": [r["session"]["code"]
                                                     for r in sent_results]},
                           trace=trace, t0=t0)

    def _not_found(self, query: str, trace: Optional[Dict] = None,
                   t0: float = 0.0) -> Dict:
        body = (
            f"I couldn't find anything in Microsoft Build 2026 specifically "
            f"about **“{query}”**. A few things to try:\n\n"
            f"- Check the spelling, or use a session code (e.g. *BRK230*).\n"
            f"- Try a broader topic like " +
            ", ".join(f"*{t}*" for t in list(TOPICS.keys())[:6]) + ".\n"
            "- Type **`topics`** to see everything I cover."
        )
        return self._reply(body, kind="not-found", trace=trace, t0=t0)

    def _weak_match(self, query: str, candidates: List[Dict],
                    trace: Optional[Dict] = None, t0: float = 0.0) -> Dict:
        lines = [
            f"I don't see Microsoft Build 2026 content that *directly* "
            f"addresses **“{query}”**. The closest sessions in the catalog:",
            "",
        ]
        for s in candidates:
            url = SESSION_URL.format(code=s["code"])
            lines.append(f"- **[{s['code']}]** *{s['title']}* — [{url}]({url})")
        lines.append("")
        lines.append("If one of these looks right, ask about it by session code "
                     "(e.g. *“tell me about BRK230”*) and I'll surface the AI summary.")
        return self._reply("\n".join(lines), kind="weak",
                           extras={"session_codes": [s["code"] for s in candidates]},
                           trace=trace, t0=t0)

    def _reply(self, body: str, kind: str = "answer",
               extras: Optional[Dict] = None,
               trace: Optional[Dict] = None,
               t0: float = 0.0) -> Dict:
        out = {"answer": body, "kind": kind}
        if extras:
            out.update(extras)
        if trace is not None:
            trace["latency_ms"] = int((time.perf_counter() - t0) * 1000)
            out["eval_trace"] = trace
        return out
