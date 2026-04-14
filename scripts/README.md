# Scripts

Skripte zur Erzeugung und Aktualisierung des FAKT II-Wikis aus den Rohdaten.

## Ablauf bei Aktualisierung

Wenn ein neuer Maßnahmenkatalog oder aktualisierte Fördersätze erscheinen:

1. Neue PDFs/Excel in `raw/` ablegen (alte Dateien behalten als Archiv)
2. Rohdaten extrahieren:
   ```bash
   uv run --with pdfplumber --with openpyxl python3 scripts/extract_raw.py > /tmp/fakt_extracted.json
   ```
3. Wiki-Seiten aktualisieren – am besten im Dialog mit dem LLM:
   - Neue/geänderte Maßnahmen identifizieren
   - Fördersätze in YAML-Frontmatter und Text aktualisieren
   - Kombinationstabelle neu einlesen und Links aktualisieren:
     ```bash
     python3 scripts/update_kombinationen.py
     ```
4. `wiki/log.md` ergänzen mit Datum und Änderungen

## Dateien

| Script | Zweck | Abhängigkeiten |
|--------|-------|----------------|
| `extract_raw.py` | Extrahiert Text aus PDFs + Excel → JSON auf stdout | pdfplumber, openpyxl |
| `update_kombinationen.py` | Schreibt Kombinations-Links (Symbole, Abzüge, ÖR) in alle Maßnahmen-Seiten | – (liest JSON inline) |

## Hinweise

- `update_kombinationen.py` enthält die Maßnahmen-Daten inline (Mapping Code → Dateiname, Titel, Fördersätze, Abzugsbeträge). Bei einem neuen Katalog müssen diese Dicts aktualisiert werden.
- Die Scripts sind idempotent – sie können beliebig oft ausgeführt werden und überschreiben die relevanten Abschnitte in den Wiki-Dateien.
- G-Maßnahmen (Tierhaltung) sind nicht in der Kombinationstabelle enthalten, da sie nicht flächenbezogen kombiniert werden.
