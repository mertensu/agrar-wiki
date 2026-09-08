# Letzte Schritte nach erfolgreichem Deploy

1. **Domain generieren:** Service → Settings → Networking → Generate Domain.
   Du bekommst eine URL wie `https://radiant-laughter-production.up.railway.app`.

2. **Verifizieren:**
   - `https://<domain>/healthz` → sollte `200 OK` oder `{"status":"ok"}` zeigen.
   - `https://<domain>/` → Login-Seite, einloggen mit einem deiner `ACCESS_CODES` (z.B. `demo123`).
   - Eine Wiki-Frage stellen — Streaming-Antwort sollte kommen.

3. **Falls Login funktioniert, aber die Frage hängt:**
   Vermutlich fehlt `GEMINI_API_KEY` oder `REDIS_URL`. Logs prüfen.
