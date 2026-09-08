# HTML-Report-Modus (Toggle) – Umsetzungsplan

Status: **noch nicht umgesetzt** (geparkt am 2026-05-11).

## Idee

Inspiriert von Thariqs Artikel "Using Claude Code: The Unreasonable Effectiveness of HTML". Wiki-Content bleibt Markdown (Obsidian, Wikilinks, Lint, Diffs), aber **Agent-Antworten** können optional als HTML gerendert werden – nützlich für:

- Kombinations-Vergleiche als Tabelle mit Farbcode
- Antrags-Checklisten zum Ausdrucken
- Mehrquellige Reports mit Quellen-Footer

User entscheidet pro Anfrage per **Checkbox unter dem Chat-Input**.

## Drei Änderungen (minimal-invasiv)

### 1. Frontend: `service/app/templates/chat.html`

- Checkbox unter der Textarea:
  ```html
  <label><input type="checkbox" name="html_mode"> Als HTML-Report</label>
  ```
- Submit-Handler ergänzen:
  ```js
  body.append('format', form.html_mode.checked ? 'html' : 'markdown');
  ```
- Finales Rendern: wenn HTML-Modus → `out.innerHTML = acc` (kein `marked.parse`), und `out.classList.add('report')` setzen.
- Während Streaming weiterhin `textContent` (verhindert kaputte Tags).

### 2. Backend: `service/app/main.py` + `service/app/prompts.py`

- `chat()` nimmt zusätzlichen Form-Parameter: `format: str = Form("markdown")`.
- Bei `format == "html"`: Prompt-Suffix anhängen, der dem Agent vorgibt:
  > Antworte als HTML-Fragment (keine `<html>`/`<head>`/`<script>`-Tags).
  > Nutze `<h2>`, `<h3>`, `<table>`, `<ul>`, `<strong>`, `<footer>` für Quellen.
  > Für Kombinations-Symbole feste Klassen: `<span class="badge-x">`, `badge-xa`, `badge-no`, `badge-kr`.
- Streaming bleibt identisch.

### 3. CSS: `service/app/static/style.css` (~30-40 Zeilen ergänzen)

- `.report h2, .report h3` – Typografie an Inter/Lora angleichen
- `.report table` – Border, Padding, zebra rows
- `.report footer` – Quellen abgesetzt (kleinere Schrift, grauer Strich darüber)
- `.report .badge-x`, `.badge-xa`, `.badge-no`, `.badge-kr` – Farbcodes (grün/gelb/rot/grau)
- `@media print` – Header und Form ausblenden, Report füllt die Seite

## Bewusst NICHT in V1

- Kein separates Artifact-Panel (Output bleibt im `#answer`-Bereich)
- Kein Download als `.html`-Datei
- Kein HTML-Sanitizer (LLM-Prompt vermeidet `<script>`; bei Bedarf später `bleach`)
- Kein eigenes `report.css` – erstmal an bestehendes `style.css` anhängen

## Risiken / Tradeoffs

- Token-Verbrauch 2-4× höher → daher Toggle, nicht Default
- Unvollständige Tags während Streaming → durch `textContent` bis Stream-Ende abgefangen
- LLM könnte CSS-Klassen halluzinieren → im Prompt explizit die erlaubten Klassen aufzählen

## Aufwand-Schätzung

~1 Stunde inkl. lokalem Testen. Drei Dateien, keine neuen Dependencies.
