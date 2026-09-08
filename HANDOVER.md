# Handover – Weiterarbeit an einem anderen PC

Stand: 2026-09-08 · Branch `master`

Dieses Dokument fasst den aktuellen Zustand zusammen, damit die Arbeit an
einem anderen Rechner nahtlos weitergeht. Verbindliche Workflows stehen in
`CLAUDE.md`, dieses Handover ergänzt nur den *aktuellen* Kontext.

## 1. Setup auf dem neuen PC

```bash
git clone <repo-url> agrar && cd agrar

# Wiki-Werkzeuge laufen ad-hoc via uv (kein festes venv nötig):
#   uv run --with pdfplumber python3 scripts/extract_raw.py
#   uv run --with pyyaml    python3 scripts/lint_wiki.py

# Service (FastAPI + PydanticAI):
cd service
uv venv && source .venv/bin/activate
uv pip install -e . --group dev        # nutzt service/uv.lock
cp .env.example .env                    # .env ist git-ignored → neu befüllen
```

Voraussetzungen: `uv`, Python 3, `poppler` (`brew install poppler`, für
PDF-Health-Checks), optional Docker+Redis für den lokalen Service-Smoke-Test.

## 2. Geheimnisse / lokale Dateien, die NICHT im Repo sind

Diese liegen nur lokal (git-ignored) und müssen auf dem neuen PC neu gesetzt
werden:

- `service/.env` – `GEMINI_API_KEY`, `SESSION_SECRET`, `ACCESS_CODES`,
  `TOKEN_CAP_PER_LABEL`, optional `LOGFIRE_TOKEN`. Vorlage: `service/.env.example`.
- `.claude/` – lokale Claude-Code-Config.
- `downloads/` – Original-Archiv vom MLR-Portal (nicht zitierbar, reproduzierbar
  durch erneuten Download).
- Reproduzierbare Artefakte: `wiki_snapshot.json`,
  `raw/konditionalitaet/kond_extracted.json` (via `scripts/`).

Der `GEMINI_API_KEY` und die übrigen ENV-Variablen sind auf **Railway**
separat gesetzt (Push deployt die lokale `.env` nicht).

## 3. Aktueller Stand

### Wiki (`wiki/`)
- Vollständiges FAKT-II-Wiki, Lint zuletzt clean (0 kritisch). Letzte Arbeit:
  Quellenangaben in Antragstellung-/Konzept-Seiten um Kapitel+Seitenzahl
  angereichert (siehe `wiki/log.md`).
- Health-Check / Verifizierungs-Workflows: siehe `CLAUDE.md`.

### Service (`service/`) – Deployment auf Railway
- Stack: PydanticAI (Agent) + FastAPI + Redis (Token-Budget) + Railway (Docker).
- **Default-Modell:** `google-gla:gemini-flash-latest` (in `app/agent.py`).
  Der `-latest`-Alias vermeidet 404s durch abgekündigte Preview-Modelle.
  Preview-Modelle **nicht** hart pinnen – Google schaltet sie regelmäßig ab
  (führte zuletzt zu hängendem Lade-Spinner). Override via `MODEL_ID` (ENV).
- **Hinweis:** `service/.env.example` nennt im Kommentar noch das alte Default
  `gemini-3-pro-preview` – veraltet, tatsächlicher Default ist `gemini-flash-latest`.
- Deploy-Anleitung: `service/DEPLOY.md` · Nach-Deploy-Checks: `service/POST_DEPLOY.md`.
- Token-Budget pro Access-Label (Lifetime, Input+Output). Reset:
  `redis-cli DEL tokens:<label>`.

## 4. Offene Punkte / TODO

- **HTML-Report-Toggle** (`service/HTML_REPORT_TODO.md`): geparkt, ~1 h Aufwand,
  drei Dateien, keine neuen Dependencies. Antworten optional als HTML rendern.
- **`service/.env.example`**: Modell-Kommentar auf `gemini-flash-latest`
  aktualisieren (Detail).
- GA-Erläuterungen: einzelne Kapitel niedriger Priorität noch offen
  (siehe Memory / `wiki/log.md`).

## 5. Nicht versionierte Render-Artefakte

`service/DEPLOY.html` und `service/POST_DEPLOY.html` sind gerenderte Fassungen
der gleichnamigen `.md`-Dateien (je ~600 KB). Sie bleiben lokal und werden
bei Bedarf neu erzeugt – die `.md`-Quellen sind im Repo maßgeblich.
