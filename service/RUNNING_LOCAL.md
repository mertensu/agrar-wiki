# Lokal laufen lassen – Schritt für Schritt

Anleitung, um den FAKT-II Wiki-Agent auf deinem Mac zu starten und im Browser
zu testen, bevor du auf Railway deployst.

## 0. Voraussetzungen prüfen

Du brauchst drei Dinge:

- **Python 3.12** – haben wir schon, das venv liegt unter `service/.venv`.
- **Docker Desktop** – für Redis lokal. Wenn nicht installiert:
  <https://www.docker.com/products/docker-desktop/> oder
  `brew install --cask docker`. Nach Installation Docker Desktop einmal
  starten, sonst antwortet das Daemon nicht.
- **Gemini API Key** – kostenlos aus Google AI Studio:
  <https://aistudio.google.com/apikey>. Beim ersten Mal Google-Login,
  dann "Create API key" → in ein bestehendes Google-Cloud-Projekt legen
  oder "Create API key in new project". Der Key sieht aus wie `AIza...`.

Schnellcheck:

```bash
docker --version          # zeigt z.B. "Docker version 27.x"
docker info >/dev/null    # darf nicht "Cannot connect" sagen
```

## 1. `.env` aus dem Beispiel kopieren und füllen

```bash
cd /Users/ulfmertens/Documents/agrar/service
cp .env.example .env
```

Jetzt `service/.env` öffnen und vier Werte echt setzen, den Rest kannst du
erstmal lassen:

| Variable | Was reinkommt |
|---|---|
| `GEMINI_API_KEY` | Dein Key aus Google AI Studio (`AIza...`). |
| `SESSION_SECRET` | Random-Bytes für Cookie-Signing. Erzeugen mit: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"` – Output reinkopieren. |
| `ACCESS_CODES` | Komma-Liste `code:label`. Für dich allein z.B. `ACCESS_CODES=test123:ulf`. Code = was du im Login eingibst, Label = wie du im Log auftauchst. |
| `COOKIE_SECURE` | Lokal auf `false` setzen, sonst akzeptiert der Browser das Cookie nicht (weil ohne HTTPS). In Railway später auf `true`. |

`MODEL_ID`, `RL_PER_HOUR`, `RL_PER_DAY`, `REDIS_URL`, `WIKI_ROOT` lässt du
zunächst auf den Defaults.

> Nicht versehentlich committen – check mit `git status`. Wenn `service/.env`
> dort auftaucht, in `.gitignore` `service/.env` ergänzen.

## 2. Redis lokal starten

Redis braucht der Rate-Limiter. Statt es nativ zu installieren, ziehst du es
als Docker-Container:

```bash
docker run -d --name fakt-redis -p 6379:6379 redis:7
```

Was der Befehl macht:

- `-d` – detached, läuft im Hintergrund.
- `--name fakt-redis` – Container kriegt einen Namen, damit du ihn später
  per `docker stop fakt-redis` / `docker start fakt-redis` ansprechen kannst.
- `-p 6379:6379` – Port 6379 (Redis-Default) vom Container ans Host-System
  durchreichen, damit deine App ihn unter `localhost:6379` erreicht.
- `redis:7` – offizielles Redis-Image, Version 7.

Schnellcheck:

```bash
docker ps                                  # zeigt fakt-redis "Up X seconds"
docker exec fakt-redis redis-cli ping      # Antwort: PONG
```

Wenn der Port belegt ist (`bind: address already in use`): irgendwas anderes
hört auf 6379. Entweder das stoppen oder einen anderen Port nehmen
(`-p 6380:6379` und in `.env` dann `REDIS_URL=redis://localhost:6380/0`).

Beim nächsten Mal nach Reboot reicht `docker start fakt-redis` – `docker run`
musst du nur einmal absetzen.

## 3. Server starten

`uvicorn` selbst lädt keine `.env`-Datei. Drei Wege, das zu lösen – wähle
einen:

**Variante A – `set -a` + `source` (am einfachsten, bash/zsh):**

```bash
cd /Users/ulfmertens/Documents/agrar/service
set -a; source .env; set +a
WIKI_ROOT=$(pwd)/../wiki .venv/bin/uvicorn app.main:app --reload --port 8000
```

`set -a` heißt "alle ab jetzt gesetzten Variablen automatisch exportieren".
`source .env` führt die Datei wie ein Shell-Skript aus (deshalb keine
Anführungszeichen um Werte mit Leerzeichen!). `set +a` schaltet das wieder
aus.

**Variante B – manuell:**

```bash
export GEMINI_API_KEY="AIza..."
export SESSION_SECRET="..."
export ACCESS_CODES="test123:ulf"
export COOKIE_SECURE=false
export REDIS_URL=redis://localhost:6379/0
WIKI_ROOT=$(pwd)/../wiki .venv/bin/uvicorn app.main:app --reload --port 8000
```

**Variante C – Inline:**

```bash
env $(cat .env | grep -v '^#' | xargs) WIKI_ROOT=$(pwd)/../wiki \
  .venv/bin/uvicorn app.main:app --reload --port 8000
```

Was die Flags an uvicorn heißen:

- `app.main:app` – "in Modul `app.main` das Objekt namens `app`".
  Funktioniert, weil unser Working-Dir `service/` ist und Python von dort
  aus `app/` als Package sieht.
- `--reload` – Code-Änderungen sofort übernehmen, ohne Server-Neustart. Nur
  lokal benutzen, in Production aus.
- `--port 8000` – Default; explizit damit du es weißt.

Wenn alles startet, siehst du Logs ungefähr so:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
INFO:fakt-agent:Agent bereit. Wiki: /Users/.../agrar/wiki
```

Wenn nicht: in 95 % der Fälle ist `GEMINI_API_KEY` nicht gesetzt oder
`WIKI_ROOT` zeigt ins Leere. Die Fehlermeldung sagt es ziemlich direkt.

## 4. Im Browser testen

Öffne <http://localhost:8000>. Du siehst die Login-Seite, dort den Code aus
`ACCESS_CODES` eintippen (in unserem Beispiel `test123`). Nach dem Submit
landest du auf der Chat-Seite, eine Frage stellen, Antwort sollte tokenweise
aufploppen.

Smoketests, die du direkt machen kannst:

- "Was ist der Fördersatz von B1.2?" → 150 €/ha mit Quellenangabe
- "Kombinierbar B4 mit B7?" → x/a mit Euro-Betrag
- "Welche Felder muss ich in FIONA für B1.2 ausfüllen?" → sollte sagen
  "siehe `raw/GA - Erlaeuterungen…`"

## 5. Stoppen / wieder anfahren

```bash
# uvicorn: Ctrl-C im Terminal
# Redis-Container am Tagesende:
docker stop fakt-redis
# Beim nächsten Mal:
docker start fakt-redis    # behält Daten – Rate-Limit-Counter überleben
# Wenn du frisch starten willst:
docker rm -f fakt-redis    # weg, danach wieder mit docker run von oben
```

## Häufige Stolperer

| Symptom | Ursache | Fix |
|---|---|---|
| `Cannot connect to redis` beim Chat | Redis-Container läuft nicht | `docker ps`, ggf. `docker start fakt-redis` |
| Beim Start `UserError: Set the GEMINI_API_KEY ...` | ENV nicht geladen | Variante A oben – `set -a; source .env; set +a` |
| Login-Cookie wird nicht gesetzt, immer wieder Login-Seite | `COOKIE_SECURE=true` ohne HTTPS | in `.env` auf `false` |
| 401 bei `/chat` direkt nach Login | Cookie-Problem oder `SESSION_SECRET` zwischen Requests geändert | `SESSION_SECRET` einmal fix setzen, danach nicht ändern |
| `WikiPathError` oder `index.md not found` beim Start | `WIKI_ROOT` zeigt falsch | `ls $WIKI_ROOT/index.md` muss klappen |
| `address already in use` Port 8000 | Anderer Prozess auf 8000 | `--port 8001` oder `lsof -ti:8000 \| xargs kill` |
