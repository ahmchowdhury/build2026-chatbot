"""Generate Announcement.md by mining session AI summaries.

For each session with an AI summary, extract sentences that have announcement
signals (announc/introduc/launch/preview/now available/GA/new feature/unveil/
debut), then cluster by topic. Cross-reference the public microsoft/Build26-news
repo (news.md) and append it as a separate section.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import httpx

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data" / "sessions.json"
OUT = ROOT / "Announcement.md"

sys.path.insert(0, str(ROOT))
from src.topics import TOPICS, topic_for_session  # noqa: E402

SESSION_URL = "https://build.microsoft.com/en-US/sessions/{code}"
NEWS_URL = "https://raw.githubusercontent.com/microsoft/Build26-news/main/news.md"

SIGNAL = re.compile(
    r"(?i)(?:we (?:are |just )?announc|today (?:we|i) |announc(?:ed|ing|es)?|"
    r"now (?:in (?:public )?preview|generally available|available)|"
    r"generally available|launched? (?:today|this )|just released|"
    r"new (?:feature|capability|tool|product|service|api|sdk|model|"
    r"integration|version|capability|generation|class|framework)|"
    r"introduc(?:e|ing|ed) [^.]{0,40}\b(?:new|the|a )|"
    r"debut|unveil|reveal(?:ed|s)? |upcoming|coming (?:in |to |on |this )"
    r"|public preview|private preview)"
)
NOISE = re.compile(
    r"(?i)\b(?:welcom|opens?|introduces? (?:himself|herself|themselves|"
    r"the (?:audience|agenda|session|speakers?|topic))|outlin\w+ the agenda|"
    r"greeting|apolog|open(?:s|ed|ing) the (?:session|video|talk|presentation))"
)


def split_sentences(text: str):
    return re.split(r"(?<=[.!?])\s+(?=[A-Z])", text)


def _speaker_str(spk):
    if not spk:
        return ""
    if isinstance(spk, list):
        return ", ".join(str(x) for x in spk if x)
    return str(spk)


def mine_announcements(sessions):
    """Return dict[topic] -> list[(code, title, sentence, speakers)]."""
    bucket = defaultdict(list)
    seen = set()
    for s in sessions:
        if not s.get("hasAI"):
            continue
        topics = topic_for_session(s) or ["Other"]
        for sent in split_sentences(s["aiSummary"]):
            sent = sent.strip()
            if NOISE.search(sent):
                continue
            if not SIGNAL.search(sent):
                continue
            if not (70 < len(sent) < 500):
                continue
            # dedupe by (code, prefix)
            prefix = re.sub(r"\W+", " ", sent[:80]).lower()
            key = (s["code"], prefix)
            if key in seen:
                continue
            seen.add(key)
            primary_topic = topics[0]
            bucket[primary_topic].append({
                "code": s["code"],
                "title": s["title"],
                "speakers": _speaker_str(s.get("speakers")),
                "sentence": sent,
                "transcript": s.get("transcript"),
                "video": s.get("video"),
            })
    return bucket


def fetch_public_news():
    try:
        r = httpx.get(NEWS_URL, timeout=10.0,
                      headers={"User-Agent": "build2026-chatbot/1.0"})
        if r.status_code == 200:
            return r.text
    except Exception as e:
        print(f"  (warning) failed to fetch microsoft/Build26-news: {e}",
              file=sys.stderr)
    return None


def render(bucket: dict, public_news: str | None) -> str:
    lines = []
    lines.append("# Microsoft Build 2026 — AI Announcement Index\n")
    lines.append(
        "_Auto-generated from public Microsoft Build 2026 session AI summaries "
        "(`build.microsoft.com/sessions`) and the public "
        "[`microsoft/Build26-news`](https://github.com/microsoft/Build26-news) "
        "repo. Re-run `python scripts/build_announcements.py` to refresh._\n"
    )
    total = sum(len(v) for v in bucket.values())
    lines.append(f"**{total} announcement-signal items** mined across "
                 f"**{len(bucket)} topics**.\n")
    lines.append("---\n")

    # Table of contents
    lines.append("## Table of contents\n")
    for topic in TOPICS.keys():
        if topic in bucket:
            lines.append(f"- [{topic}](#{slug(topic)}) "
                         f"({len(bucket[topic])} items)")
    if "Other" in bucket:
        lines.append(f"- [Other / Cross-cutting](#other--cross-cutting) "
                     f"({len(bucket['Other'])} items)")
    lines.append("- [Public Microsoft Build 2026 News (mirror)]"
                 "(#public-microsoft-build-2026-news-mirror)")
    lines.append("\n---\n")

    # Per-topic sections in defined order
    ordering = list(TOPICS.keys()) + ["Other"]
    for topic in ordering:
        items = bucket.get(topic)
        if not items:
            continue
        if topic == "Other":
            lines.append("## Other / Cross-cutting\n")
        else:
            lines.append(f"## {topic}\n")
            cfg = TOPICS.get(topic)
            if cfg:
                lines.append(f"_{cfg['description']}_\n")
        # sort by code for consistency
        items.sort(key=lambda x: x["code"])
        # group by session code
        by_code = defaultdict(list)
        for it in items:
            by_code[it["code"]].append(it)
        for code in sorted(by_code.keys()):
            entries = by_code[code]
            title = entries[0]["title"]
            speakers = entries[0]["speakers"] or "—"
            url = SESSION_URL.format(code=code)
            lines.append(f"### [{code}] {title}")
            lines.append(f"*Speakers:* {speakers}  ")
            extra = [f"[Session page]({url})"]
            if entries[0].get("transcript"):
                extra.append(f"[Transcript]({entries[0]['transcript']})")
            if entries[0].get("video"):
                extra.append(f"[Video]({entries[0]['video']})")
            lines.append(" · ".join(extra) + "\n")
            for it in entries:
                lines.append(f"- {it['sentence']}")
            lines.append("")
        lines.append("---\n")

    # Public news mirror
    lines.append("## Public Microsoft Build 2026 News (mirror)\n")
    lines.append("_The following is mirrored verbatim from the public "
                 "[`microsoft/Build26-news`](https://github.com/microsoft/Build26-news/blob/main/news.md) "
                 "repository, Microsoft's canonical announcement index._\n")
    if public_news:
        lines.append(public_news.strip())
    else:
        lines.append("> _Could not fetch news.md at build time. Visit the repo "
                     "directly: https://github.com/microsoft/Build26-news_")
    return "\n".join(lines)


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def main():
    print(f"Loading sessions from {DATA}…")
    with open(DATA) as f:
        sessions = json.load(f)["sessions"]
    with_ai = [s for s in sessions if s.get("hasAI")]
    print(f"  {len(sessions)} sessions ({len(with_ai)} with AI summaries)")

    print("Mining announcements from AI summaries…")
    bucket = mine_announcements(sessions)
    for topic, items in sorted(bucket.items(), key=lambda x: -len(x[1])):
        print(f"  {topic}: {len(items)} items")

    print(f"Fetching public microsoft/Build26-news…")
    public_news = fetch_public_news()
    if public_news:
        print(f"  fetched {len(public_news)} chars")

    md = render(bucket, public_news)
    OUT.write_text(md)
    print(f"\nWrote {OUT} ({len(md)} chars)")

    # Also emit a structured JSON view that the web UI consumes for
    # the topic-dropdown announcements page. Keeping this alongside
    # the markdown so both formats stay in sync (regenerate together).
    json_out = ROOT / "data" / "announcements.json"
    flat_items: list = []
    for topic in list(TOPICS.keys()) + ["Other"]:
        for it in bucket.get(topic, []):
            flat_items.append({
                "topic": topic,
                "code": it["code"],
                "title": it["title"],
                "speakers": it["speakers"],
                "sentence": it["sentence"],
                "transcript": it.get("transcript"),
                "video": it.get("video"),
                "session_url": SESSION_URL.format(code=it["code"]),
            })
    payload = {
        "generated_at": __import__("datetime").datetime.utcnow()
            .replace(microsecond=0).isoformat() + "Z",
        "total": len(flat_items),
        "topics": [
            {
                "name": t,
                "description": TOPICS[t]["description"]
                    if t in TOPICS else "Cross-cutting / uncategorized",
                "count": sum(1 for x in flat_items if x["topic"] == t),
            }
            for t in list(TOPICS.keys()) + ["Other"]
            if any(x["topic"] == t for x in flat_items)
        ],
        "items": flat_items,
    }
    json_out.write_text(json.dumps(payload, indent=2))
    print(f"Wrote {json_out} ({len(flat_items)} items, "
          f"{len(payload['topics'])} topics)")


if __name__ == "__main__":
    main()
