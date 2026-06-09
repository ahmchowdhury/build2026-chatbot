"""FastAPI server. Single process, serves API + static UI."""
import json
import os
import threading
import time
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .agent import BuildAgent
from .search import SessionIndex
from .topics import list_topics

ROOT = Path(__file__).parent.parent
WEB = ROOT / "web"
DATA = ROOT / "data"

EVAL_TRACE_ENABLED = os.environ.get("EVAL_TRACE_ENABLED", "").lower() in ("1", "true", "yes")

app = FastAPI(title="Build 2026 Chatbot",
              description="Agentic chatbot over Microsoft Build 2026 sessions",
              version="1.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

index = SessionIndex()
agent = BuildAgent(index)


class ChatRequest(BaseModel):
    message: str


@app.on_event("startup")
def warmup():
    """Pre-warm DNS, TLS, and the agentic search pipeline so the first
    real user request doesn't pay the cold-start tax. Runs in a daemon
    thread so it never blocks the server from accepting connections.

    On Azure App Service with Always On + WEBSITES_WARMUP_PATH=/api/health,
    the platform also pings us during deploy slot swaps — but that's a
    health probe only and doesn't exercise the search/synthesis path.
    """
    def _go():
        try:
            time.sleep(1.0)  # let uvicorn finish bringing up workers
            t0 = time.perf_counter()
            agent.answer("warmup", include_trace=False)
            print(f"[warmup] agentic round-trip primed in "
                  f"{(time.perf_counter() - t0) * 1000:.0f}ms")
        except Exception as e:
            print(f"[warmup] non-fatal: {e}")

    threading.Thread(target=_go, daemon=True, name="warmup").start()


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "sessions": len(index.sessions),
        "with_ai_summary": sum(1 for s in index.sessions if s.get("hasAI")),
        "rag_enabled": agent.rag_enabled,
        "agentic_enabled": agent.agentic_enabled,
        "eval_trace_enabled": EVAL_TRACE_ENABLED,
        "version": "1.3.0",
    }


@app.get("/api/topics")
def topics():
    return {"topics": list_topics()}


@app.get("/api/announcements")
def announcements_json():
    """Structured JSON powering the /announcements page UI. Refreshed
    by `scripts/build_announcements.py` (writes data/announcements.json).
    """
    p = DATA / "announcements.json"
    if not p.exists():
        raise HTTPException(
            404,
            "data/announcements.json not generated yet — "
            "run `python scripts/build_announcements.py`",
        )
    return json.loads(p.read_text())


@app.post("/api/chat")
def chat(req: ChatRequest, request: Request):
    if not req.message or len(req.message) > 1000:
        raise HTTPException(400, "Message must be 1-1000 chars")
    # Per-request trace flag: env-level toggle OR opt-in header. The header
    # path lets the eval harness exercise prod without enabling traces
    # globally — but only when EVAL_TRACE_ENABLED is set (security).
    include_trace = False
    if EVAL_TRACE_ENABLED and request.headers.get("x-eval-trace", "").lower() in ("1", "true", "yes"):
        include_trace = True
    elif EVAL_TRACE_ENABLED:
        include_trace = True
    return agent.answer(req.message, include_trace=include_trace)


@app.get("/api/session/{code}")
def session(code: str):
    s = index.by_code(code)
    if not s:
        raise HTTPException(404, f"Session {code} not found")
    return s


# Static frontend
if WEB.exists():
    app.mount("/static", StaticFiles(directory=str(WEB)), name="static")

    @app.get("/")
    def root():
        return FileResponse(str(WEB / "index.html"))

    @app.get("/announcements")
    def announcements_page():
        """Modern HTML view of the announcement index with a topic
        dropdown filter (matches the build.microsoft.com filter UX).
        Falls back to the markdown if the HTML isn't bundled."""
        html = WEB / "announcements.html"
        if html.exists():
            return FileResponse(str(html))
        ann = ROOT / "Announcement.md"
        if ann.exists():
            return FileResponse(str(ann), media_type="text/markdown")
        raise HTTPException(404, "Announcement.md not generated yet — "
                                  "run scripts/build_announcements.py")

    @app.get("/announcements.md")
    def announcements_md():
        """Raw markdown export — kept for users who want a flat file."""
        ann = ROOT / "Announcement.md"
        if ann.exists():
            return FileResponse(str(ann), media_type="text/markdown")
        raise HTTPException(404, "Announcement.md not generated yet — "
                                  "run scripts/build_announcements.py")
