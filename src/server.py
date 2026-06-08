"""FastAPI server. Single process, serves API + static UI."""
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .agent import BuildAgent
from .search import SessionIndex
from .topics import list_topics

ROOT = Path(__file__).parent.parent
WEB = ROOT / "web"

app = FastAPI(title="Build 2026 Chatbot",
              description="Agentic chatbot over Microsoft Build 2026 sessions",
              version="1.0.0")

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


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "sessions": len(index.sessions),
        "with_ai_summary": sum(1 for s in index.sessions if s.get("hasAI")),
    }


@app.get("/api/topics")
def topics():
    return {"topics": list_topics()}


@app.post("/api/chat")
def chat(req: ChatRequest):
    if not req.message or len(req.message) > 1000:
        raise HTTPException(400, "Message must be 1-1000 chars")
    return agent.answer(req.message)


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
    def announcements():
        ann = ROOT / "Announcement.md"
        if ann.exists():
            return FileResponse(str(ann), media_type="text/markdown")
        raise HTTPException(404, "Announcement.md not generated yet — "
                                  "run scripts/build_announcements.py")
