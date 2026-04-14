# Plan A: Scope-Update + Erste Antragstellung-Seiten (Schritte 1–3)

## Context

Das Wiki deckt bisher nur die Beratungsebene ab. Wir erweitern den Scope um Antragstellungs-Checklisten und Fallstricke. Dieser Plan deckt die Grundlagen ab: CLAUDE.md-Update, Struktur anlegen, und die zwei kleinsten Quellen verarbeiten (FAKT-Codes + G-FAQ).

**FAKT-Codes vollwertig:** FAKT II wird ab 2027 weitergeführt und angepasst (kein FAKT III – laut Pressemitteilung BW stehen Änderungen "unter Vorbehalt", aber das Programm bleibt). Die bestehenden Codes bleiben stabil. Daher: zentrale Mapping-Tabelle UND `fakt_code`-Feld in allen Maßnahmen-YAML-Frontmattern. Skript `scripts/add_fakt_codes.py` übernimmt das Eintragen.

---

## Schritt 1: CLAUDE.md Scope-Update

**Datei:** `CLAUDE.md`

### 1a. Überschrift (Z. 283)
"Beratungsebene, nicht Formularebene" → "Beratungs- und Antragstellungsebene (Entscheidung 2026-04-14)"

### 1b. Einleitungstext (Z. 285)
Erweitern: Wiki hilft bei "Soll ich?" UND "Wie beantrage ich korrekt?"

### 1c. Ausschlussliste (Z. 287–293) dreiteilen

**Jetzt aufgenommen:**
- FAKT-Codes → zentrale Mapping-Tabelle in `wiki/Antragstellung/FAKT_Codes.md` + `fakt_code` in jedem Maßnahmen-YAML
- Nachweisfristen → als Checklisten in Antragstellung-Seiten

**Teilweise aufgenommen:**
- Platzangebote G-Maßnahmen → nur im FAQ-Kontext ("Schaffe ich die Auflagen?")

**Weiterhin ausgeschlossen:**
- Bestandsverzeichnis-Pflichten und Formular-Details
- FIONA-Formularfeld-Hinweise
- Rückgabe-/Übertragungsregeln

### 1d. Faustregel (Z. 297)
→ "Hilft diese Info bei der Entscheidung ODER dabei, den Antrag korrekt und vollständig einzureichen?"

### 1e. Verzeichnisstruktur (Z. 7–27)
`Antragstellung/` ergänzen

### 1f. Neuer Abschnitt nach Z. 120 (nach Konzept-Seiten)

```markdown
### Antragstellung-Seiten (`wiki/Antragstellung/`)

Dateiname: `Antragstellung_{Thema}.md` oder `FAKT_Codes.md`

YAML: `type: antragstellung`, `betrifft: ["B1.2", "B3.2", ...]`

Inhalt: Checkliste (Nachweise, Fristen), FAKT-Code-Zuordnung, häufige Fehler.
Antragstellung-Seiten bündeln thematisch verwandte Maßnahmen –
nicht 1:1 pro Maßnahme, sondern nach Antragskontext gruppiert.

Jede Maßnahmen-Seite verlinkt auf ihre Antragstellung-Seite:
`## Antragstellung` → `[[Antragstellung_Tierwohl|Checkliste & Fallstricke]]`
```

### 1g. Maßnahmen-YAML-Template
`fakt_code: "48"` als optionales Feld im YAML-Frontmatter ergänzen (im Template-Beispiel in CLAUDE.md)

### 1h. Maßnahmen-Seitenformat
`## Antragstellung`-Abschnitt als neues optionales Element dokumentieren (vor dem `---`-Footer, nach Öko-Regelungen)

---

## Schritt 2: FAKT-Codes Mapping

**Quelle:** `downloads/formulare_2026/FAKT_II_-_Maßnahmen_und_FAKT-Codes_2026.pdf` (152 KB, ~2 Seiten)

1. PDF extrahieren (`uv run --with pdfplumber`)
2. `wiki/Antragstellung/FAKT_Codes.md` erstellen – Mapping-Tabelle aller Maßnahmen → FAKT-Codes
3. `fakt_code` in YAML-Frontmatter jeder Maßnahmen-Seite ergänzen (Skript: `scripts/add_fakt_codes.py`)
4. `wiki/index.md` um Antragstellung-Sektion erweitern
5. `wiki/log.md` ergänzen

---

## Schritt 3: G-Maßnahmen FAQ

**Quelle:** `downloads/formulare_2026/FAKT_II_G-Maßnahmen_-_Häufige_Fragen.pdf` (432 KB)

1. PDF extrahieren
2. `wiki/Antragstellung/Antragstellung_Tierwohl.md` erstellen (Checkliste, Platzangebote im FAQ-Kontext, Fallstricke)
3. `## Antragstellung`-Link in G1–G7-Maßnahmen-Seiten ergänzen
4. Log

---

## Memory-Update

`project_wiki_scope.md` aktualisieren: Neuer Scope umfasst Beratung + Antragstellung.

---

## Verifikation Plan A

- [ ] CLAUDE.md: Scope, Verzeichnisstruktur, Seitenformat, Faustregel konsistent
- [ ] `wiki/Antragstellung/FAKT_Codes.md` existiert mit vollständiger Tabelle
- [ ] Alle Maßnahmen-Seiten haben `fakt_code` in YAML-Frontmatter
- [ ] `wiki/Antragstellung/Antragstellung_Tierwohl.md` existiert
- [ ] G-Maßnahmen-Seiten haben `## Antragstellung`-Link
- [ ] `wiki/index.md` listet Antragstellung-Seiten
- [ ] `wiki/log.md` dokumentiert beide Ingests
