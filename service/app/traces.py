"""
Persistente Traces der Agent-Runs.

Jeder Chat-Request wird als JSON-Datei abgelegt:
  service/logs/traces/YYYY-MM-DD/HHMMSS_<n>_<label>.json

Inhalt:
  - Zeitstempel, Label, Frage, Modell
  - Komplette Message-Historie (PydanticAI `result.all_messages()`):
    Systemprompt, User-Frage, Assistant-Tool-Calls, Tool-Results,
    finale Text-Antwort.
  - Falls verfügbar: Token-Verbrauch.

Damit lassen sich Halluzinationen im Nachhinein debuggen ("hat das Modell
die richtige Seite überhaupt gelesen, oder den Index nur überflogen?").

Format ist Pydantic-AI-spezifisch (ModelMessage-Liste); zum Lesen einfach
mit `pydantic_ai.messages.ModelMessagesTypeAdapter` deserialisieren oder
roh als JSON anschauen.
"""

from __future__ import annotations

import datetime as dt
import json
import logging
import re
from itertools import count
from pathlib import Path
from typing import Any


log = logging.getLogger("fakt-agent.trace")

_TRACES_ROOT = Path(__file__).resolve().parents[1] / "logs" / "traces"
_safe_label = re.compile(r"[^A-Za-z0-9_-]+")
_counter = count()


def _slugify(value: str) -> str:
    return _safe_label.sub("_", value)[:32] or "anon"


def write_trace(
    label: str,
    question: str,
    model_name: str,
    messages_json: bytes | str,
    usage: dict[str, Any] | None = None,
) -> Path | None:
    """Speichert einen Run-Trace als JSON. Returnt den Pfad oder None bei Fehler.

    `messages_json` ist die Ausgabe von
    `pydantic_ai.messages.ModelMessagesTypeAdapter.dump_json(result.all_messages())`
    – also bereits serialisiertes JSON, das wir in unser Wrapper-Objekt
    einbetten ohne nochmal zu parsen.
    """
    try:
        now = dt.datetime.now()
        day_dir = _TRACES_ROOT / now.strftime("%Y-%m-%d")
        day_dir.mkdir(parents=True, exist_ok=True)
        n = next(_counter)
        filename = f"{now.strftime('%H%M%S')}_{n:04d}_{_slugify(label)}.json"
        path = day_dir / filename

        if isinstance(messages_json, bytes):
            messages_json = messages_json.decode("utf-8")

        payload = {
            "timestamp": now.isoformat(timespec="seconds"),
            "label": label,
            "question": question,
            "model": model_name,
            "usage": usage or {},
            # raw → wir parsen nicht, aber serialisieren als nested JSON
            # damit es im File-Viewer lesbar bleibt.
            "messages": json.loads(messages_json),
        }
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return path
    except Exception:  # nie den Request killen, nur loggen
        log.exception("trace-write failed")
        return None
