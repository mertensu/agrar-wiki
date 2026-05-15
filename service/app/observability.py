"""
Logfire-Setup (optional).

Wenn `LOGFIRE_TOKEN` als Env-Variable gesetzt ist, schicken wir Traces an
Pydantics Logfire-Cloud (https://logfire.pydantic.dev). Lokale Entwicklung
ohne Token läuft komplett ohne Trace-Versand.

Was wir instrumentieren:
  - PydanticAI: Agent-Runs, Tool-Calls, Model-Calls inkl. Token-Nutzung
  - FastAPI: HTTP-Requests + Antwortzeiten

Was wir bewusst NICHT instrumentieren:
  - HTTPX: das Gemini-SDK nutzt eigene Clients; PydanticAI deckt das ab.
  - Redis: Rate-Limit-Pings spammen das Trace-Volumen, ohne Erkenntnisgewinn.
"""

from __future__ import annotations

import logging
import os


log = logging.getLogger("fakt-agent.observability")


def setup(app=None) -> bool:
    """Initialisiert Logfire, falls Token gesetzt ist.

    Returns True wenn aktiviert, False wenn übersprungen.
    Idempotent: mehrfacher Aufruf ist okay.
    """
    token = os.environ.get("LOGFIRE_TOKEN")
    if not token:
        log.info("LOGFIRE_TOKEN nicht gesetzt – Tracing deaktiviert.")
        return False

    try:
        import logfire

        # service_name landet als Tag in der Logfire-UI.
        logfire.configure(
            token=token,
            service_name=os.environ.get("LOGFIRE_SERVICE_NAME", "fakt-wiki-agent"),
            service_version=os.environ.get("RAILWAY_GIT_COMMIT_SHA", "dev"),
            # Sende auch beim SIGTERM noch gepufferte Spans raus.
            send_to_logfire=True,
        )
        logfire.instrument_pydantic_ai()
        if app is not None:
            logfire.instrument_fastapi(app, capture_headers=False)
        log.info("Logfire aktiv (service=fakt-wiki-agent).")
        return True
    except Exception:
        log.exception("Logfire-Setup fehlgeschlagen – läuft ohne Tracing weiter.")
        return False
