#!/usr/bin/env bash
# Lokaler Dev-Start. Lädt .env, setzt WIKI_ROOT auf den lokalen Pfad
# (überschreibt den Docker-Default /app/wiki aus .env) und startet uvicorn.
#
# Aufruf:  ./run.sh           # Port 8000, --reload
#          ./run.sh 8001      # eigener Port
set -euo pipefail

cd "$(dirname "$0")"

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

export WIKI_ROOT="$(cd .. && pwd)/wiki"

# Lokal: Beispielfragen + Archiv aus Agentenblick ausblenden, damit Antworten
# aus den Primitiven (Maßnahmen-/Konzept-Seiten) rekonstruiert werden statt
# aus vorgekochten Beispielfragen paraphrasiert. Override per Env möglich.
export WIKI_EXCLUDE_PREFIXES="${WIKI_EXCLUDE_PREFIXES:-Beispielfragen,_archive}"

PORT="${1:-8000}"
exec .venv/bin/uvicorn app.main:app --reload --port "$PORT"
