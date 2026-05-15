"""
FastAPI-Eintrittspunkt: Login, Chat-Streaming, Healthcheck.

Streaming-Mechanik (kurz, für die Lerner-Notizen in agent.py):
  - PydanticAI bietet `agent.run_stream(user_prompt, deps=...)`
  - das gibt einen Async-Stream-Manager zurück; `result.stream_text(delta=True)`
    liefert die Text-Deltas tokenweise.
  - wir konvertieren die Deltas in eine SSE-ähnliche Plain-Text-Antwort, die
    der Browser per ReadableStream Stück für Stück liest.
"""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

import redis.asyncio as redis
from fastapi import FastAPI, Form, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic_ai.messages import ModelMessagesTypeAdapter

from app.agent import WikiDeps, build_agent
from app.auth import COOKIE_MAX_AGE, COOKIE_NAME, AuthService, auth_from_env
from app.observability import setup as setup_observability
from app.ratelimit import BudgetTracker, tracker_from_env
from app.traces import write_trace


log = logging.getLogger("fakt-agent")

WIKI_ROOT = Path(os.environ.get("WIKI_ROOT", "/app/wiki")).resolve()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Build-once-Setup für Agent + Redis + Auth."""
    setup_observability(app)
    if not WIKI_ROOT.is_dir():
        raise RuntimeError(f"WIKI_ROOT nicht gefunden: {WIKI_ROOT}")
    redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    redis_client = redis.from_url(redis_url, decode_responses=True)

    app.state.agent = build_agent(WIKI_ROOT)
    app.state.auth = auth_from_env()
    app.state.budget = tracker_from_env(redis_client)
    app.state.redis = redis_client

    log.info("Agent bereit. Wiki: %s", WIKI_ROOT)
    try:
        yield
    finally:
        await redis_client.aclose()


app = FastAPI(lifespan=lifespan, title="FAKT-II Wiki-Agent")

_TEMPLATES_DIR = Path(__file__).parent / "templates"
_STATIC_DIR = Path(__file__).parent / "static"
templates = Jinja2Templates(directory=_TEMPLATES_DIR)
app.mount("/static", StaticFiles(directory=_STATIC_DIR), name="static")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _auth(request: Request) -> AuthService:
    return request.app.state.auth


def _budget(request: Request) -> BudgetTracker:
    return request.app.state.budget


def _current_session(request: Request):
    auth = _auth(request)
    return auth.read_cookie(request.cookies.get(COOKIE_NAME))


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/budget")
async def budget_status(request: Request):
    session = _current_session(request)
    if session is None:
        raise HTTPException(status_code=401, detail="Nicht angemeldet")
    b = _budget(request)
    used = await b.used(session.label)
    return {"used": used, "cap": b._budget.cap}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    session = _current_session(request)
    if session is None:
        return templates.TemplateResponse(request, "login.html", {"error": None})
    used = await _budget(request).used(session.label)
    cap = _budget(request)._budget.cap
    return templates.TemplateResponse(
        request,
        "chat.html",
        {"label": session.label, "tokens_used": used, "tokens_cap": cap},
    )


@app.post("/login")
async def login(request: Request, code: str = Form(...)):
    auth = _auth(request)
    session = auth.verify_code(code)
    if session is None:
        return templates.TemplateResponse(
            request, "login.html", {"error": "Ungültiger Zugangscode."}, status_code=401
        )
    response = RedirectResponse("/", status_code=303)
    response.set_cookie(
        COOKIE_NAME,
        auth.issue_cookie(session),
        max_age=COOKIE_MAX_AGE,
        httponly=True,
        samesite="lax",
        secure=os.environ.get("COOKIE_SECURE", "true").lower() == "true",
    )
    return response


@app.post("/logout")
async def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie(COOKIE_NAME)
    return response


@app.post("/chat")
async def chat(request: Request, question: str = Form(...)):
    session = _current_session(request)
    if session is None:
        raise HTTPException(status_code=401, detail="Nicht angemeldet")

    question = (question or "").strip()
    if not question:
        raise HTTPException(status_code=400, detail="Frage ist leer")
    if len(question) > 2000:
        raise HTTPException(status_code=400, detail="Frage zu lang (max 2000 Zeichen)")

    budget = _budget(request)
    allowed, reason, _used, _cap = await budget.check(session.label)
    if not allowed:
        return Response(content=reason or "Token-Budget aufgebraucht", status_code=429)

    agent = request.app.state.agent
    deps = WikiDeps(wiki_root=WIKI_ROOT)

    log.info("chat label=%s len=%d", session.label, len(question))

    async def token_stream():
        async with agent.run_stream(question, deps=deps) as result:
            async for delta in result.stream_text(delta=True):
                yield delta.encode("utf-8")
            try:
                msgs = result.all_messages()
                msgs_json = ModelMessagesTypeAdapter.dump_json(msgs)
                usage = {}
                total_tokens = 0
                try:
                    u = result.usage
                    req_t = getattr(u, "request_tokens", None)
                    resp_t = getattr(u, "response_tokens", None)
                    tot_t = getattr(u, "total_tokens", None)
                    usage = {
                        "request_tokens": req_t,
                        "response_tokens": resp_t,
                        "total_tokens": tot_t,
                    }
                    if tot_t:
                        total_tokens = int(tot_t)
                    elif req_t or resp_t:
                        total_tokens = int(req_t or 0) + int(resp_t or 0)
                except Exception:
                    log.exception("usage() lesen fehlgeschlagen")

                if total_tokens > 0:
                    new_total = await budget.add(session.label, total_tokens)
                    log.info(
                        "tokens label=%s call=%d total=%d",
                        session.label,
                        total_tokens,
                        new_total,
                    )

                model_name = getattr(agent.model, "model_name", str(agent.model))
                write_trace(
                    label=session.label,
                    question=question,
                    model_name=model_name,
                    messages_json=msgs_json,
                    usage=usage,
                )
            except Exception:
                log.exception("trace persisting failed")

    return StreamingResponse(token_stream(), media_type="text/plain; charset=utf-8")
