# Build 2026 Chatbot

> **Agentic chatbot grounded in 460 Microsoft Build 2026 sessions.** Ask a focused question, get session‑level answers with timestamps, speaker names, and direct links to the official session page, transcript, and video. Or ask for a whole‑topic summary.

![status](https://img.shields.io/badge/sessions-460-7c5cff) ![ai-summaries](https://img.shields.io/badge/AI%20summaries-170-7c5cff) ![transcripts](https://img.shields.io/badge/transcripts-185-7c5cff) ![python](https://img.shields.io/badge/python-3.10+-blue)

---

## What it does

- **Specific Q&A** — *“What did Naomi Moneypenny say about prompt caching?”* → quotes the AI summary with the BRK code, timestamp, and link to the session and transcript.
- **Topic summary** — *“Summarize all AI Foundry sessions”* → returns every Foundry session with a 2-sentence excerpt and link.
- **Session lookup** — type any session code (e.g. `BRK230`, `KEY01`, `DEMSP383`) for a full card.
- **Graceful fallback** — if a topic isn't in Build 2026, the bot says so and offers closest matches.
- **`Announcement.md`** — a local, searchable, regeneratable index of every announcement-signal sentence across all 170 AI summaries, cross-referenced against the public [`microsoft/Build26-news`](https://github.com/microsoft/Build26-news) repo.

## Topics covered

`AI Foundry` · `AI Infrastructure` · `Models` · `Agents` · `Windows` · `Developer Tools` · `Data + AI` · `Microsoft IQ` · `Security + Governance` · `Discovery + Frontier Science` · `M365 Copilot`

## Quick start

```bash
cd ~/build2026-chatbot
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 1. Generate the announcement index (runs in ~5s)
python scripts/build_announcements.py

# 2. Start the chatbot (FastAPI + static UI on one port)
uvicorn src.server:app --host 0.0.0.0 --port 8000

# Then open http://localhost:8000
```

That's it. **No login, no API key required** — the data is bundled in `data/sessions.json` and the search is fully local (BM25 over session AI summaries).

## How it works

```
┌─────────────────────────────────────────────────────────────┐
│  web/index.html   (Tailwind via CDN, marked.js, vanilla JS) │
└──────────────────────┬──────────────────────────────────────┘
                       │ POST /api/chat
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  src/server.py    (FastAPI)                                 │
│      └── src/agent.py    intent routing                     │
│             ├── help / topics / session-code lookup         │
│             ├── topic summary  (filter by keyword pattern)  │
│             └── BM25 search + sentence-level extraction     │
│                  └── src/search.py                          │
│                         data/sessions.json (460 sessions)   │
└─────────────────────────────────────────────────────────────┘
```

### Intent routing

| User input | Branch | Example |
|---|---|---|
| Session code (`BRK230`, `KEY01`, …) | **Session card** | "tell me about BRK230" |
| `topics` / `help` / `what topics` | **Topic list** | "topics" |
| Topic name + summary verb | **Topic summary** | "summarize AI Foundry sessions" |
| Anything else | **BM25 + sentence extraction** | "what is explicit prompt caching?" |
| No match | **Graceful "not found"** with closest sessions | "tell me about ColdFusion" |

### Why BM25 + sentence extraction (not RAG/embeddings)

For an event catalog of 460 sessions × ~3000 chars, BM25 is *faster, deterministic, and zero-dep* — and the answers we surface are direct quotes from the AI summary anyway. Adding embeddings would obscure attribution. If you want LLM rewording, set `OPENAI_API_KEY` (planned passthrough hook in `agent.py`).

## Updating data

The bundled `data/sessions.json` was scraped from public session pages on `build.microsoft.com` (no login). To refresh:

```bash
# Re-scrape (uses public sitemap + SSR HTML; 460 sessions, ~5 min)
python scripts/scrape_sessions.py    # TODO if you ever need fresh data
python scripts/build_announcements.py
```

## File layout

```
build2026-chatbot/
├── README.md
├── Announcement.md            # auto-generated; mirror of news + AI-summary mining
├── requirements.txt
├── data/
│   └── sessions.json          # 460 sessions w/ AI summaries, transcripts, video URLs
├── scripts/
│   └── build_announcements.py
├── src/
│   ├── __init__.py
│   ├── topics.py              # topic taxonomy + keyword patterns
│   ├── search.py              # BM25 index + sentence extraction
│   ├── agent.py               # intent routing + answer rendering
│   └── server.py              # FastAPI app
└── web/
    ├── index.html             # Tailwind, no build step
    ├── style.css              # custom polish on top of Tailwind
    └── app.js                 # chat UI logic
```

## Notes

- **Data freshness:** sessions snapshot taken at scrape time. Microsoft adds AI summaries asynchronously; re-run the scraper to refresh.
- **Public data only:** every link points to `build.microsoft.com` or `medius.microsoft.com` (the public CDN for transcripts and video). Nothing internal is bundled.
- **High availability:** for production, drop this behind a reverse proxy (Caddy, Cloudflare Tunnel) — the FastAPI server is stateless and the data is static.

## License

This tool's code is yours to use. The session content (titles, AI summaries, transcripts, slides, video) is © Microsoft and is **referenced via public URLs only** — nothing is rehosted.
