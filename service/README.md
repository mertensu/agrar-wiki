# FAKT-II Wiki-Agent (Service)

Webdienst, der das `wiki/`-Verzeichnis dieses Repos als Frage-Antwort-Agent
verfügbar macht. Stack: **PydanticAI** (Agent), **FastAPI** (HTTP),
**Redis** (Rate-Limit), **Railway** (Hosting).

Dieses Verzeichnis ist absichtlich vom Wiki-Code getrennt: das Wiki bleibt
ein vom LLM gepflegter Markdown-Vault, hier liegt nur die Deployment-Schicht.

## Lese-Reihenfolge zum Lernen

Wenn du die App von innen nach außen verstehen willst, lies in dieser
Reihenfolge – die Lehrkommentare bauen aufeinander auf:

1.  **`app/wiki_tools.py`** – die reinen Funktionen, die der Agent aufruft.
    Erklärt, wie aus einer Python-Funktion ein "Tool" wird, das das LLM
    sieht. Path-Traversal-Schutz live demonstriert.
2.  **`app/agent.py`** – das Herzstück. Erklärt Agent / Deps / RunContext /
    Tool-Schleife / Streaming / Prompt-Caching. Wer PydanticAI lernen will,
    fängt hier an.
3.  **`app/prompts.py`** – Systemprompt-Builder. Zeigt, warum wir den
    Prompt einmal beim Start bauen (Cache) und wie der Wiki-Index drin
    landet.
4.  **`app/main.py`** – FastAPI-Glue: Login, Streaming-Endpoint,
    Lifespan. Hier nur Standardware, keine Lerninhalte über PydanticAI.
5.  **`app/auth.py`** + **`app/ratelimit.py`** – kleine Bausteine, in sich
    geschlossen.

## Glossar PydanticAI

| Begriff | Was es ist | Wo im Code |
| --- | --- | --- |
| `Agent` | Bündelt Modell, Systemprompt, Tools. Alle Runs laufen über ihn. | `agent.py: build_agent` |
| `Deps` | Beliebiges Datenobjekt, das pro Run mitgegeben wird – z.B. ein DB-Handle oder Pfad. **Sieht das LLM nicht.** | `agent.py: WikiDeps` |
| `RunContext[Deps]` | Erstes Argument eines Tools, wenn es Zugriff auf Deps braucht. PydanticAI füllt das automatisch. | `agent.py: search_wiki(ctx, ...)` |
| `Tool` | Python-Funktion, die der Agent aufrufen darf. Docstring + Type-Hints werden zum Schema, das ans LLM geht. | `wiki_tools.py` + Registrierung in `agent.py` |
| `run_stream` | Async-Stream-Manager. Liefert Tokens während sie kommen. | `main.py: chat()` |
| Tool-Schleife | LLM → Tool-Call → Result → LLM → Result → ... bis zur finalen Text-Antwort. Läuft im Hintergrund. | konzeptionell, siehe Kommentar oben in `agent.py` |
| Prompt-Caching | Anthropic cached den Systemprompt, wenn er bytegleich bleibt. ~90% Input-Token-Ersparnis ab dem 2. Request. | `prompts.py` baut ihn einmal beim Start |

## Lokal entwickeln

```bash
cd service
uv venv && source .venv/bin/activate
uv pip install -e . --group dev
cp .env.example .env  # GEMINI_API_KEY und SESSION_SECRET eintragen
# Lokal Redis via Docker:
docker run -d -p 6379:6379 redis
# COOKIE_SECURE=false in .env, damit ohne HTTPS Cookies kommen
WIKI_ROOT=$(pwd)/../wiki uvicorn app.main:app --reload
```

## Tests

```bash
cd service && pytest
```

Die Tests laufen ohne Anthropic-Key – sie testen nur die reinen
Wiki-Tools (Path-Traversal, Suche, Pfadauflösung).

## Deploy auf Railway

1.  Repo bei Railway als Service verbinden.
2.  In den Service-Settings:
    - Build = "Dockerfile"
    - Dockerfile Path: `service/Dockerfile`
    - Build Context: `.` (Repo-Root – nötig, damit das Dockerfile auf
      `wiki/` zugreifen kann)
3.  Redis-Plugin hinzufügen → liefert `REDIS_URL` automatisch.
4.  Environment Variables aus `.env.example` übernehmen, mindestens:
    `GEMINI_API_KEY`, `SESSION_SECRET`, `ACCESS_CODES`.
5.  `git push` – Railway baut neu, auch das Wiki landet so im Image.
