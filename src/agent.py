"""Agentic orchestrator. Routes a user question:

  1. Detect intent (specific question vs topic summary vs help).
  2. Run BM25 search.
  3. Find sentence-level evidence in AI summaries.
  4. Synthesize an answer with exact session references + timestamps + links.
  5. Gracefully say so when nothing relevant is found.

Optional: if OPENAI_API_KEY or AZURE_OPENAI_API_KEY is set, runs the structured
context through the LLM for a more natural rewrite. Defaults to a clean
template response that matches the formatting style we use.
"""
import os
import re
from typing import Dict, List, Optional

from .search import SessionIndex
from .topics import TOPICS, detect_topic_in_query, filter_sessions_by_topic, list_topics

SESSION_URL = "https://build.microsoft.com/en-US/sessions/{code}"


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


class BuildAgent:
    def __init__(self, index: SessionIndex):
        self.index = index

    # --- Public API ---

    def answer(self, query: str) -> Dict:
        query = (query or "").strip()
        if not query:
            return self._reply(
                "Ask me anything about Microsoft Build 2026 — a feature, a "
                "product, a session code, or a whole topic like 'AI Foundry' "
                "or 'Windows'.",
                kind="hint",
            )

        if HELP_INTENT.search(query):
            return self._help()
        if LIST_TOPICS_INTENT.match(query):
            return self._reply(self._render_topics(), kind="topics",
                               extras={"topics": list_topics()})

        # Direct session-code lookup ("BRK230", "tell me about KEY01")
        m = re.search(r"\b([A-Z]{2,4}\d{2,4}(?:-[A-Z0-9]+)?)\b", query.upper())
        if m:
            code = m.group(1)
            s = self.index.by_code(code)
            if s:
                return self._render_session_card(s, query)

        # Topic detection (explicit or via patterns in query)
        topics = detect_topic_in_query(query)
        is_summary = bool(SUMMARY_INTENT.search(query)) or any(
            t.lower() in query.lower() for t in TOPICS.keys()
        ) and len(query.split()) <= 6

        if topics and is_summary:
            return self._render_topic_summary(topics[0], query)

        # Fall through to BM25 search + sentence extraction
        return self._render_search_answer(query, topics_hint=topics)

    # --- Renderers ---

    def _help(self) -> Dict:
        body = (
            "**I'm a Microsoft Build 2026 chatbot.** I have AI summaries for "
            "**170+ sessions** and structured metadata for **460 sessions** total. "
            "I can answer in three ways:\n\n"
            "1. **Specific question** — e.g. *“What did Naomi Moneypenny say "
            "about prompt caching?”* — I'll quote the AI summary with timestamps "
            "and links.\n"
            "2. **Topic summary** — e.g. *“Summarize all AI Foundry sessions”* "
            "— I'll list every matching session with its AI summary excerpt.\n"
            "3. **Session lookup** — type any session code (e.g. *BRK230*, "
            "*KEY01*) for a full card.\n\n"
            "Topics I know: " + ", ".join(f"*{t}*" for t in TOPICS.keys())
        )
        return self._reply(body, kind="help")

    def _render_topics(self) -> str:
        out = ["**Topics I cover at Microsoft Build 2026:**", ""]
        for t in list_topics():
            out.append(f"- **{t['name']}** — {t['description']}")
        out.append("")
        out.append("Try: *“summarize Windows sessions”* or *“what's new in AI Foundry?”*")
        return "\n".join(out)

    def _render_session_card(self, s: Dict, query: str) -> Dict:
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
            # If query has specific keywords, surface those sentences
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
            lines.append("_AI summary not yet available for this session — full "
                         "metadata still public on the session page._")
        return self._reply("\n".join(lines), kind="session", extras={"session": s})

    def _render_topic_summary(self, topic_name: str, query: str) -> Dict:
        matches = filter_sessions_by_topic(self.index.sessions, topic_name)
        # Prefer sessions with AI summaries, then non-AI
        with_ai = [s for s in matches if s.get("hasAI")]
        without = [s for s in matches if not s.get("hasAI")]
        ordered = with_ai + without

        if not ordered:
            return self._not_found(topic_name)

        cfg = TOPICS[topic_name]
        lines = [f"## {topic_name} at Microsoft Build 2026", "", cfg["description"], ""]
        lines.append(f"**{len(ordered)} sessions** match this topic "
                     f"({len(with_ai)} have AI summaries).")
        lines.append("")

        for s in ordered[:25]:
            code = s["code"]
            title = s["title"]
            url = SESSION_URL.format(code=code)
            speakers = _format_speakers(s)
            lines.append(f"### [{code}] {title}")
            lines.append(f"*{speakers}* · [Session page]({url})"
                         + (f" · [Transcript]({s['transcript']})" if s.get("transcript") else ""))
            lines.append("")
            if s.get("aiSummary"):
                # Take first 2 sentences of summary as a quick excerpt
                sents = re.split(r"(?<=[.!?])\s+(?=[A-Z])", s["aiSummary"])
                excerpt = " ".join(sents[:2])[:600]
                lines.append(f"> {excerpt}")
                lines.append("")
        if len(ordered) > 25:
            lines.append(f"_…and {len(ordered) - 25} more sessions in this topic._")
        return self._reply("\n".join(lines), kind="topic-summary",
                           extras={"topic": topic_name, "count": len(ordered),
                                   "session_codes": [s["code"] for s in ordered]})

    def _render_search_answer(self, query: str,
                              topics_hint: Optional[List[str]] = None) -> Dict:
        # Search top sessions
        ai_results = self.index.search(query, k=8, require_ai=True)
        # If too few with AI, also pull from non-AI
        if len(ai_results) < 3:
            extra = self.index.search(query, k=5)
            seen = {s["code"] for s in ai_results}
            for r in extra:
                if r["code"] not in seen:
                    ai_results.append(r)

        if not ai_results:
            return self._not_found(query)

        # Sentence-level extraction over the top-N AI sessions
        ai_sessions = [s for s in ai_results if s.get("hasAI")][:5]
        sent_results = self.index.find_sentences(query, ai_sessions,
                                                 max_sentences_per_session=2)

        # If we found NO sentence-level evidence, the topical match is weak.
        if not sent_results or all(not r["hits"] for r in sent_results):
            # Provide closest-match list with graceful message
            return self._weak_match(query, ai_results[:5])

        lines = []
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

        # Also list runner-up sessions without sentence hits
        scored_codes = {r["session"]["code"] for r in sent_results}
        runners = [s for s in ai_results if s["code"] not in scored_codes][:3]
        if runners:
            lines.append("**Also worth checking:**")
            for s in runners:
                url = SESSION_URL.format(code=s["code"])
                lines.append(f"- [{s['code']}] *{s['title']}* — [{url}]({url})")
            lines.append("")
        return self._reply("\n".join(lines), kind="answer",
                           extras={"session_codes": [r["session"]["code"]
                                                     for r in sent_results]})

    def _not_found(self, query: str) -> Dict:
        body = (
            f"I couldn't find anything in Microsoft Build 2026 specifically "
            f"about **“{query}”**. A few things to try:\n\n"
            f"- Check the spelling, or use a session code (e.g. *BRK230*).\n"
            f"- Try a broader topic like " +
            ", ".join(f"*{t}*" for t in list(TOPICS.keys())[:6]) + ".\n"
            "- Type **`topics`** to see everything I cover."
        )
        return self._reply(body, kind="not-found")

    def _weak_match(self, query: str, candidates: List[Dict]) -> Dict:
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
        return self._reply("\n".join(lines), kind="weak")

    def _reply(self, body: str, kind: str = "answer",
               extras: Optional[Dict] = None) -> Dict:
        out = {"answer": body, "kind": kind}
        if extras:
            out.update(extras)
        return out
