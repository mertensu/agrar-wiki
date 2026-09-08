# Deployment-Plan – FAKT-II Wiki-Agent

Schritt-für-Schritt-Anleitung, um den Service aus `service/` produktiv auf Railway zu bringen.

---

## 1. Accounts & externe Dienste

| Dienst | Wofür | Link |
| --- | --- | --- |
| **Google AI Studio** | API-Key für Gemini (`GEMINI_API_KEY`) | <https://aistudio.google.com/apikey> |
| **Railway** | Hosting (Docker-Build + Redis-Plugin) | <https://railway.app> |
| **GitHub** | Quelle, aus der Railway baut | <https://github.com> |

> Redis braucht keinen separaten Account – läuft als Railway-Plugin im selben Projekt.

---

## 2. Kosten (Stand 2026-05)

- **Railway Free Trial:** 30 Tage, $5 Guthaben – reicht zum Ausprobieren.
- **Railway Hobby:** $1/Monat Grundgebühr + Usage.
  Realistisch landest du mit FastAPI-App + Redis-Plugin im niedrigen einstelligen Dollar-Bereich pro Monat.
- **Gemini API:** Kostenloser Tier im AI Studio reicht für Demo-Last; bei höherem Volumen Pay-as-you-go.

---

## 3. Vorbereitung – lokaler Smoke-Test

Bevor du deployst, einmal lokal hochfahren, damit Konfigurationsfehler nicht erst in der Cloud auftauchen:

```bash
cd service
uv venv && source .venv/bin/activate
uv pip install -e . --group dev

cp .env.example .env
# In .env eintragen:
#   GEMINI_API_KEY=...
#   SESSION_SECRET=<python -c "import secrets; print(secrets.token_urlsafe(32))">
#   ACCESS_CODES=demo123:gast
#   COOKIE_SECURE=false   # lokal ohne HTTPS

docker run -d -p 6379:6379 redis
WIKI_ROOT=$(pwd)/../wiki uvicorn app.main:app --reload
```

Browser auf <http://localhost:8000>, mit `demo123` einloggen, eine Wiki-Frage stellen. Wenn das durchläuft, ist die Code-Seite okay.

---

## 4. Railway-Deploy

### 4.1 Repo bei GitHub

Falls das Repo nur lokal liegt: `gh repo create` (privat reicht) und pushen. Railway zieht direkt aus GitHub.

### 4.2 Projekt anlegen

1. **Railway → New Project → Deploy from GitHub repo** – Repo auswählen.
2. **Service-Settings:**
   - **Build:** Dockerfile
   - **Dockerfile Path:** `service/Dockerfile`
   - **Build Context:** `.` (Repo-Root – nötig, damit `wiki/` ins Image kommt)
   - Start-Command + Healthcheck kommen aus `service/railway.toml`.

### 4.3 Redis hinzufügen

Im Projekt **+ New → Database → Redis** anlegen.
Railway injiziert `REDIS_URL` automatisch als Variable in den App-Service.

### 4.4 Environment Variables setzen

Im App-Service unter **Variables** eintragen:

| Variable | Wert | Pflicht |
| --- | --- | --- |
| `GEMINI_API_KEY` | Aus AI Studio | ✅ |
| `SESSION_SECRET` | `python -c "import secrets; print(secrets.token_urlsafe(32))"` | ✅ |
| `ACCESS_CODES` | `code1:label1,code2:label2` | ✅ |
| `COOKIE_SECURE` | `true` (Railway = HTTPS) | ✅ |
| `WIKI_ROOT` | `/app/wiki` | ✅ |
| `RL_PER_HOUR` | z.B. `20` | optional |
| `RL_PER_DAY` | z.B. `100` | optional |
| `MODEL_ID` | z.B. `google-gla:gemini-2.5-flash` | optional |
| `REDIS_URL` | wird vom Plugin gesetzt | – |

### 4.5 Domain

Service-Settings → **Networking → Generate Domain**.
Ergebnis: `https://<projekt>.up.railway.app`. Custom-Domain optional.

### 4.6 Deployen

`git push` auf den verbundenen Branch – Railway baut neu, kopiert `wiki/` ins Image, startet den Container.
Status sichtbar im **Deployments**-Tab; Healthcheck-Pfad ist `/healthz`.

---

## 5. Nach dem Deploy verifizieren

- [ ] `https://<domain>/healthz` antwortet mit `200 OK`.
- [ ] Login-Seite öffnet sich, einer der `ACCESS_CODES` funktioniert.
- [ ] Eine Frage an den Agent liefert eine streamende Antwort.
- [ ] Rate-Limit greift nach `RL_PER_HOUR` Requests (Test mit kleinem Wert).
- [ ] Railway-Logs zeigen keine Fehler beim Tool-Call ins Wiki.

---

## 6. Updates

| Was sich ändert | Was du tun musst |
| --- | --- |
| Wiki-Inhalt (`wiki/*.md`) | `git push` → Rebuild (Wiki ist Build-Time ins Image gebacken) |
| Code in `service/app/` | `git push` → Rebuild |
| Env-Variable (z.B. neuer `ACCESS_CODE`) | Variable in Railway anpassen → Redeploy |
| `GEMINI_API_KEY` rotieren | Neuer Key in AI Studio, Variable ersetzen, Redeploy |

---

## 7. Stolperfallen

- **Build Context falsch:** Wenn Build-Context auf `service/` statt `.` steht, fehlt `wiki/` im Image und der Agent findet keine Inhalte.
- **`ACCESS_CODES` schwach:** Das ist die einzige Authentifizierung. Wer einen Code hat, kann dein Gemini-Kontingent bis zum Rate-Limit verbrauchen. Lange, zufällige Codes verwenden.
- **`COOKIE_SECURE=false` in Prod:** Session-Cookies wären unverschlüsselt im Klartext übertragbar – nur lokal so setzen.
- **Wiki-Drift:** Nach jedem Wiki-Update redeployen, sonst antwortet der Service mit dem Stand vom letzten Build.
- **Free-Trial-Ende:** Nach 30 Tagen ohne Bezahlmethode wird der Service pausiert. Rechtzeitig Hobby-Plan aktivieren, wenn er live bleiben soll.
