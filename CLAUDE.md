# FAKT II Agrar-Wiki – Schema

Dieses Projekt ist ein **LLM-Wiki** für das FAKT II-Förderprogramm (Baden-Württemberg). Die Wissensbasis wird vom LLM geschrieben und gepflegt, der Mensch kuratiert Quellen und stellt Fragen.

## Verzeichnisstruktur

```
raw/                          # Rohdaten – NIEMALS verändern
  FAKT_II_Broschuere.pdf      # Original-Broschüre (47 S.)
  Kombinationstabelle FAKT II.xlsx  # Kombinationsmatrix

downloads/                    # Archiv – Originaldateien vom MLR-Portal
                              # Wird nie in Quellenverweisen referenziert

wiki/                         # LLM-generiertes Wiki – Obsidian-Vault
  index.md                    # Inhaltsverzeichnis (nach Kategorien)
  log.md                      # Chronologisches Arbeitsprotokoll
  FAKT_II_Uebersicht.md      # Programmübersicht
  Kombinationstabelle.md      # Kombinationsregeln (Zusammenfassung)
  massnahmen/                 # Eine Seite pro Maßnahme (~42 Dateien)
  Kategorien/                 # Eine Seite pro Kategorie (A–G)
  Konzepte/                   # Schlüsselbegriffe (RGV, Konditionalität, …)
  Antragstellung/             # Checklisten, FAKT-Codes, Fallstricke

scripts/                      # Reproduzierbare Skripte
  extract_raw.py              # PDFs + Excel → JSON
  update_kombinationen.py     # Kombinations-Links in alle Seiten schreiben
  README.md                   # Anleitung
```

## Seitenformat

### Maßnahmen-Seiten (`wiki/massnahmen/`)

Dateiname: `{Code}_{Kurzname}.md` (z.B. `B1.2_Extensive_Gruenland.md`)

```markdown
---
code: "B1.2"
titel: "Extensive Bewirtschaftung bestimmter Grünlandflächen ohne Stickstoffdüngung"
kategorie: "B – Erhaltung und Pflege der Kulturlandschaft"
foerdersatz: "150 €/ha"
einheit: "ha"
verpflichtung: "mehrjährig"
fakt_code: "21"
type: massnahme
---

# B1.2: Extensive Bewirtschaftung bestimmter Grünlandflächen ohne Stickstoffdüngung

**Kategorie:** B – Erhaltung und Pflege der Kulturlandschaft
**Fördersatz:** 150 €/ha
**Verpflichtungszeitraum:** mehrjährig

## Ziele
- …

## Fördervoraussetzungen
- …

## Auflagen/Verpflichtungen
- …

## Sonstiges
…

## Kombinierbar mit
- [[A2_Silageverzicht|A2 Silageverzicht]]
- [[B7_Verzicht_Chemie_Gruenland|B7 Verzicht chem.-synth. Produktionsmittel]] (x/a – 220 €/ha statt 300 €/ha)
- [[B6_Messerbalkenschnitt|B6 Messerbalkenschnitt]] (o – nur mit GL-Maßnahme)

## Nicht kombinierbar mit
- [[B3.2_Artenreiches_Gruenland|B3.2 Artenreiches Grünland]] (–)
- [[E7_Bluehflaechen|E7 Blühflächen]] (kR – keine zusätzliche D2-Förderung)

## Öko-Regelungen (1. Säule)
Siehe auch [[Oeko-Regelungen]].
- ÖR 4 Extensivierung Dauergrünland (x/a – 190 €/ha statt 240 €/ha)
- ÖR 7 Natura 2000

## Antragstellung
→ [[Antragstellung_Tierwohl|Checkliste & Fallstricke]]

---
*Quelle: FAKT II-Broschüre Baden-Württemberg, Stand Oktober 2025*
```

### Kombinations-Annotationen

Die Kombinations-Links tragen Symbole direkt am Link:

| Symbol | Bedeutung | Beispiel |
|--------|-----------|---------|
| *(kein)* | Volle Kombinierbarkeit (X) | `[[A2_Silageverzicht\|A2 Silageverzicht]]` |
| `(x/a – …)` | Kombinierbar mit Abzug, inkl. Euro-Betrag | `(x/a – B1.2 wird auf 100 €/ha gekürzt)` |
| `(o – …)` | Nur mit GL-Maßnahme | `(o – nur mit GL-Maßnahme)` |
| `((o) – …)` | Nur wenn zusätzlich GL-Maßnahme beantragt | |
| `(–)` | Nicht kombinierbar | |
| `(kR – …)` | Keine Zusatzförderung (Rechtsgrundlage) | `(kR – keine zusätzliche D2-Förderung)` |

**Alle reduzierten Beträge müssen explizit in Euro angegeben werden.** Nie nur "x/a" ohne Betrag.

### Bekannte reduzierte Fördersätze (Stand 10/2025)

**Bei Kombination mit D2 Ökolandbau:**
- B1.2: 100 €/ha (statt 150)
- E5: 2.500 €/ha (statt 2.700)
- E10: 40 €/ha (statt 100)
- E14: 420 €/ha (statt 500)
- E15: 180 €/ha (statt 260)

**Bei Kombination mit ÖR 4:**
- D2 Beibehaltung GL: 190 €/ha (statt 240)
- D2 Einführung GL: 380 €/ha (statt 430)

**Bei Kombination mit B7:**
- B4: 220 €/ha (statt 300)
- B5: 220 €/ha (statt 300)

### Kategorie-Seiten (`wiki/Kategorien/`)

YAML: `type: kategorie`. Kurzbeschreibung der Kategorie + Links zu allen zugehörigen Maßnahmen.

### Konzept-Seiten (`wiki/Konzepte/`)

YAML: `type: konzept`. Erklärung eines Schlüsselbegriffs mit Rücklinks zu relevanten Maßnahmen.

### Antragstellung-Seiten (`wiki/Antragstellung/`)

Dateiname: `Antragstellung_{Thema}.md` oder `FAKT_Codes.md`

YAML: `type: antragstellung`, `betrifft: ["B1.2", "B3.2", ...]`

Inhalt: Checkliste (Nachweise, Fristen), FAKT-Code-Zuordnung, häufige Fehler.
Antragstellung-Seiten bündeln thematisch verwandte Maßnahmen –
nicht 1:1 pro Maßnahme, sondern nach Antragskontext gruppiert.

Jede Maßnahmen-Seite verlinkt auf ihre Antragstellung-Seite:
`## Antragstellung` → `[[Antragstellung_Tierwohl|Checkliste & Fallstricke]]`

## Quellenangaben und Widersprüche

### Quellenangaben

Jede faktische Behauptung im Wiki muss ihre Quelle referenzieren. Format: `(Quelle: Dateiname)` nach der Behauptung.

**Quellenreferenz-Konvention:**
- **Immer Dateiname** verwenden, nie beschreibende Titel. Beispiel: `Kond_Infobroschuere_2026.pdf` statt `Informationsbroschüre Konditionalität 2026`.
- **Kein `raw/`-Prefix.** Beispiel: `(Quelle: FAKT_G_Haeufige_Fragen.pdf, S. 1)` statt `(Quelle: raw/FAKT_G_Haeufige_Fragen.pdf, S. 1)`.
- **`downloads/` nie referenzieren.** Alle zitierbaren Quellen liegen in `raw/`. `downloads/` ist ein Archiv der Originaldateien vom MLR-Portal.

```markdown
- Betriebe ab 0,3 RGV/ha Grünland (Quelle: FAKT_II_Broschuere.pdf, S. 18)
```

- Bei mehreren Quellen: `(Quellen: datei1.pdf, datei2.xlsx)`
- Wenn eine Behauptung **keine Quelle** hat: mit `<!-- TODO: Quelle prüfen -->` markieren
- Die Fußzeile `*Quelle: FAKT_II_Broschuere.pdf, Stand Oktober 2025*` gilt als Default-Quelle für die ganze Seite. Inline-Quellenangaben nur nötig, wenn die Info aus einer **anderen** Quelle stammt oder besonders kritisch ist (z.B. Abzugsbeträge).

### Widersprüche

Wenn zwei Quellen sich widersprechen, **nie stillschweigend eine Version wählen**. Stattdessen explizit markieren:

```markdown
> **Widerspruch:** Laut FAKT_II_Broschuere.pdf (S. 9) beträgt der Fördersatz 150 €/ha,
> laut der aktualisierten Tabelle (Stand 03/2026) jedoch 160 €/ha.
> → Neuere Quelle übernommen, alte Angabe hier dokumentiert.
```

Bei einem Update-Ingest (neue Version einer bestehenden Quelle):
1. Geänderte Werte identifizieren und aktualisieren
2. Im `wiki/log.md` die konkreten Änderungen auflisten
3. Wenn unklar ist welche Quelle aktueller ist → User fragen, nicht raten

### Verifizierung

Bevor eine Zahl aus dem Wiki an den User kommuniziert wird:
- Prüfen ob die Quelle im Wiki angegeben ist
- Bei Abzugsbeträgen (x/a): Gegenchecken ob die Angabe auf beiden Seiten der Kombination konsistent ist (z.B. steht auf B1.2 dasselbe wie auf D2?)
- Wenn unsicher: `Kombinationstabelle FAKT II.xlsx` direkt auslesen statt sich auf Wiki-Text zu verlassen

### Konfidenz-Signale (optional im Frontmatter)

Für Seiten mit schwacher Belegkette oder ungelösten Widersprüchen:

```yaml
confidence: high | medium | low   # wie gut belegt die Aussagen sind
contested: true                    # ungelöster Widerspruch auf der Seite
contradictions: [D2_Oekolandbau]   # verweist auf Seiten mit Konfliktbezug
```

- `high` ist der Default und muss nicht gesetzt werden – Broschüre + Kombinationstabelle konsistent.
- `medium` bei rekonstruierten Zahlen (z.B. x/a-Beträge aus Fußnoten abgeleitet) oder Einzelquelle.
- `low` bei unsicheren Ableitungen oder indirekten Hinweisen.
- Lint zieht gezielt `contested: true` und `confidence: low` Seiten für Review raus.

### Provenance-Marker (für mehrquellige Seiten)

Auf Seiten, die aus **3+ Quellen** synthetisieren (z.B. Konzept-Seiten zu Konditionalität, GLÖZ), kann pro Absatz ein Marker am Absatzende gesetzt werden, damit einzelne Aussagen rückverfolgbar sind ohne die `sources:`-Liste der ganzen Seite durchzugehen:

```markdown
Betriebe ab 10 ha Ackerland müssen 4% nicht-produktive Flächen ausweisen
(GLÖZ 8). ^[Kond_Infobroschuere_2026.pdf]

FAKT E7 Blühflächen können darauf angerechnet werden, sofern sie die GLÖZ-
Anforderungen erfüllen. ^[FAKT_II_Broschuere.pdf]
```

Auf Maßnahmen-Seiten (typisch eine Hauptquelle) **nicht nötig** – die Default-Fußzeile reicht.

## Wikilinks

- Format: `[[Dateiname_ohne_Extension|Anzeigename]]`
- Links sind **bidirektional**: wenn A auf B verlinkt, muss B auch auf A verlinken (Obsidian zeigt Backlinks, aber explizite Links sind besser)
- Dateinamen verwenden Unterstriche, keine Leerzeichen

## Operationen

### Session-Orientierung (vor jeder Operation)

Bevor irgendetwas geschrieben, geändert oder beantwortet wird, muss der Zustand des Wikis bekannt sein. Sonst entstehen Duplikate, verpasste Rücklinks oder Widersprüche zu bereits dokumentierten Entscheidungen.

Pflicht-Reihenfolge beim Session-Start:
1. `CLAUDE.md` (dieses Dokument) – operative Workflows
2. `wiki/SCHEMA.md` – Wiki-Verfassung (Seitentypen, Frontmatter, Tag-Taxonomie)
3. `wiki/index.md` – welche Seiten existieren
4. `wiki/log.md` – letzte 20–30 Einträge scannen, um jüngste Aktivität zu kennen

Erst danach folgt Ingest, Query oder Lint. Bei gezielten Suchen nach Begriffen zusätzlich `Grep` über `wiki/` laufen lassen, bevor eine neue Seite angelegt wird – ein ähnlicher Begriff kann schon unter anderem Namen existieren.

### Ingest (neue Quelle verarbeiten)

1. Neue Datei in `raw/` ablegen (ggf. vorher splitten, siehe "Große PDFs aufbereiten")
2. **Manifest aktualisieren:** `python3 scripts/update_manifest.py` – erfasst neue Datei mit SHA256. Bei Re-Ingest derselben Datei wird Drift gemeldet (Hash-Mismatch).
3. Text extrahieren: `uv run --with pdfplumber python3 scripts/extract_raw.py`
4. **Erst besprechen, dann schreiben:** Schlüsselinformationen mit dem User diskutieren – was ist neu, was hat sich geändert, was widerspricht bestehenden Daten? Nicht blind losschreiben.
5. Bestehende Wiki-Seiten aktualisieren oder neue erstellen
6. Quellenangaben setzen: `(Quelle: dateiname.pdf)` bei neuen/geänderten Fakten
7. Widersprüche zu bestehenden Daten explizit markieren (siehe Quellenangaben)
8. Kombinations-Links prüfen und aktualisieren
9. `wiki/index.md` aktualisieren
10. `wiki/log.md` ergänzen (siehe Log-Format unten)

### Query (Frage beantworten)

1. `wiki/index.md` lesen um relevante Seiten zu finden
2. Relevante Seiten lesen (Grep/Glob statt alles laden)
3. Antwort synthetisieren mit Quellenverweisen
4. **Wenn die Antwort wiederverwendbar ist** → als neue Wiki-Seite ablegen

### Lint (Gesundheitscheck)

**Vor jedem Commit verpflichtend:**
```
uv run --with pyyaml python3 scripts/lint_wiki.py
```
Prüft Broken Wikilinks, Frontmatter-Pflichtfelder, Tag-Taxonomie, `sources:`-
Existenz in `raw/`, Page-Size > 200 Zeilen, TODO-Marker, `confidence: low` /
`contested: true`. Exit-Code 1 bei kritischen Problemen (Broken Links,
Frontmatter-Fehler, fehlende Quellen, unbekannte Tags) – diese **müssen** vor
dem Commit behoben werden. Warnungen (Orphans, Größe, TODOs) sind tolerierbar,
sollten aber begründet sein.

**Periodisch zusätzlich prüfen:**
- **Quellen-Drift:** `python3 scripts/update_manifest.py --check` – meldet, wenn eine `raw/`-Datei geändert wurde (Hash-Mismatch). Nicht im Lint enthalten, da es Hash-Berechnung über alle PDFs erfordert.
- Widersprüche zwischen Seiten
- Veraltete Informationen (`updated:` älter als jüngste Quelle)
- Fehlende Konzeptseiten für häufig erwähnte Begriffe
- Kombinations-Links ohne Euro-Betrag bei x/a
- Fehlende Quellenangaben bei kritischen Zahlen (Fördersätze, Abzüge)
- `<!-- TODO: Quelle prüfen -->`-Markierungen auflösen
- Inkonsistente Kombinations-Angaben (A sagt kombinierbar mit B, aber B erwähnt A nicht)

### Health Check (visueller PDF-Abgleich)

Stichprobenartige Prüfung, ob Wiki-Inhalte mit den Original-PDFs übereinstimmen:

1. 3–5 zufällige Maßnahmen auswählen (verschiedene Kategorien)
2. Zugehörige PDF-Seiten finden: `uv run --with pdfplumber python3 -c "..."` mit Stichwortsuche nach Maßnahmencode
3. PDF-Seiten als Bild rendern: `pdftoppm -png -f {seite} -l {seite} -r 200 raw/{datei}.pdf /tmp/pdf_check/{prefix}`
4. Bilder mit Read-Tool visuell lesen und gegen Wiki-Seite abgleichen
5. Prüfpunkte pro Maßnahme:
   - Fördersatz (€-Betrag und Einheit)
   - Fördervoraussetzungen
   - Auflagen/Verpflichtungen (vollständig?)
   - Sonstiges (korrekt wiedergegeben?)
6. Ergebnis in `wiki/log.md` dokumentieren (Datum, geprüfte Maßnahmen, Befunde)

**Voraussetzung:** `poppler` muss installiert sein (`brew install poppler`).

### Update (bei neuem Maßnahmenkatalog, z.B. FAKT II → FAKT III)

1. **Vorher-Snapshot erstellen:** `python3 scripts/snapshot_wiki.py > wiki_snapshot_vor_update.json`
2. Neue PDFs/Excel in `raw/` ablegen (alte behalten, nie löschen)
3. `python3 scripts/update_manifest.py` – neue Dateien erfassen, Drift an bestehenden Dateien flaggen
4. `scripts/extract_raw.py` ausführen (ggf. anpassen für neue Dateinamen)
5. **Diff identifizieren:** Neuen Snapshot gegen alten vergleichen – was ist neu, was hat sich geändert, was entfällt?
6. Wiki-Seiten aktualisieren (Fördersätze, Auflagen, neue/entfallene Maßnahmen)
7. `scripts/update_kombinationen.py` Dicts anpassen und ausführen
8. `scripts/update_konditionalitaet.py` Mapping anpassen und ausführen
9. `wiki/log.md` ergänzen
10. **Nachher-Snapshot erstellen** und als `wiki_snapshot.json` committen
11. Commit mit aussagekräftiger Message, die die Quelle und Hauptänderungen benennt

### Archivieren (statt löschen)

Wenn eine Wiki-Seite vollständig überholt ist (z.B. entfallene Maßnahme beim FAKT II → FAKT III Wechsel) oder aus dem Scope fällt, wird sie **nicht gelöscht**, sondern verschoben. Grund: Querverweise aus Log-Einträgen oder alten Commits bleiben dadurch auflösbar, und die Nachvollziehbarkeit der Wiki-Historie bleibt erhalten.

Ablauf:
1. Ordner `wiki/_archive/` anlegen, falls noch nicht vorhanden
2. Seite unter Beibehaltung der Unterordner-Struktur verschieben (z.B. `wiki/massnahmen/X1_Alt.md` → `wiki/_archive/massnahmen/X1_Alt.md`)
3. Im Frontmatter der archivierten Seite ergänzen: `archived: YYYY-MM-DD` und `archived_reason: "..."` (z.B. `"entfallen mit FAKT III"`)
4. Eintrag aus `wiki/index.md` entfernen
5. Alle Seiten, die auf die archivierte Seite verlinkt haben, finden (`Grep` auf Dateinamen) und die Wikilinks durch Plaintext + `(archiviert)` ersetzen – z.B. aus `[[X1_Alt|X1 Alte Maßnahme]]` wird `X1 Alte Maßnahme (archiviert)`
6. `wiki/log.md` ergänzen: `## [YYYY-MM-DD] archive | X1_Alt` mit Grund

`raw/`-Dateien werden nie archiviert – sie bleiben immutable am Ursprungsort, auch wenn die zugehörige Maßnahme entfallen ist. Das Archiv betrifft nur die `wiki/`-Seiten.

## Log-Format (`wiki/log.md`)

Jeder Log-Eintrag muss **revisionssicher** sein – ein Prüfer muss nachvollziehen können, woher jede Zahl stammt.

```markdown
## [YYYY-MM-DD] ingest | Quellentitel

**Quelle:** `raw/dateiname.pdf` (Seitenanzahl), ggf. Fußnoten/Zeilennummern

**Was & Warum:**
Kurzbeschreibung was geändert wurde und warum (z.B. "Fördersatz fehlte", "Widerspruch zu neuer Quelle aufgelöst").

**Änderungen mit Quellennachweis:**
- Konkrete Änderung mit Verweis auf Quelle (z.B. "B1.2 auf 100 €/ha gemäß Kombinationstabelle FAKT II.xlsx, Fußnote Zeile 50")
- Jede Zahl, die geändert wird, braucht eine Quellenangabe

**Korrekturen:** (falls zutreffend)
- Was war vorher falsch und warum (z.B. "B4 × B7 war als 'nicht kombinierbar' eingetragen – Excel-Zelle K21 zeigt 'x/a'")

**Strukturelle Änderungen:** (falls zutreffend)
- Neue/gelöschte/umbenannte Dateien
```

**Regeln:**
- Keine Änderung an Fördersätzen oder Abzugsbeträgen ohne Quellenangabe im Log
- Bei Korrekturen: dokumentieren was falsch war und wie die richtige Angabe belegt ist
- Relative Angaben ("laut Fußnote") reichen nicht – immer Dateiname + Position (Zeile, Seite, Zellkoordinate)

## Werkzeuge

- **PDF-Extraktion:** `uv run --with pdfplumber python3 …`
- **Excel-Extraktion:** `uv run --with openpyxl python3 …`
- **Suche im Wiki:** Grep (nach Inhalten) und Glob (nach Dateinamen) – kein RAG nötig bei aktueller Größe
- **Skripte immer in `scripts/` ablegen**, nie nur in `/tmp`

### Große PDFs aufbereiten (>20 Seiten)

Bei PDFs mit mehr als 20 Seiten **vor der Extraktion splitten**, damit pdfplumber mit kleineren Dateien arbeitet:

1. **Inhaltsverzeichnis lesen** – falls vorhanden (als Bild oder direkt im PDF). Wenn kein Inhaltsverzeichnis vorhanden ist → User darauf hinweisen und gemeinsam eine sinnvolle Aufteilung festlegen.
2. **Nach Hauptkapiteln splitten** – pro Hauptüberschrift (z.B. römische Nummerierung I, II, III…) ein eigenes PDF.
3. **"+1 Seite"-Regel** – beim Splitting immer eine Seite über die Kapitelgrenze hinaus mitnehmen, da neue Kapitel oft mitten auf einer Seite beginnen und der Anfang noch zum vorherigen Kapitel gehört. Seitenranges überlappen sich also leicht.
4. **Benennung:** `{quellenprefix}_{kapitel}_{kurzname}.pdf` (z.B. `kond_II_gloez.pdf`)
5. **Werkzeug:** `qpdf input.pdf --pages . {start}-{end} -- output.pdf`
6. **Skript in `scripts/` ablegen** – damit der Split reproduzierbar ist.

## Quellen-Manifest (`raw/manifest.json`)

Damit Änderungen an Quelldateien nicht unbemerkt ins Wiki einsickern, wird für jede Datei in `raw/` ein SHA256-Hash in einem zentralen Manifest geführt. Grund: Das MLR veröffentlicht aktualisierte Versionen unter **gleichem Dateinamen** (z.B. `FAKT_II_Broschuere.pdf`) – ohne Hash-Check bleibt das unentdeckt und das Wiki zitiert dann veraltete Zahlen als aktuelle.

**Format:**

```json
{
  "FAKT_II_Broschuere.pdf": {
    "sha256": "a3f...",
    "ingested": "2026-04-14",
    "source_url": "https://…/fakt_broschuere.pdf"
  },
  "Kond_Infobroschuere_2026.pdf": { "sha256": "…", "ingested": "…" }
}
```

**Warum Manifest statt Frontmatter:** PDFs und Excel-Dateien können kein Frontmatter tragen. Ein zentrales JSON ist einfacher zu pflegen als Sidecar-Files.

**Workflow:**
- Bei jedem Ingest: Hash der neuen Datei berechnen und im Manifest ablegen.
- Bei Re-Ingest derselben Datei: Hash vergleichen – bei Mismatch als Drift behandeln (Widerspruchs-Workflow, Log-Eintrag, betroffene Wiki-Seiten prüfen).
- Lint prüft periodisch: stimmen die Hashes aller `raw/`-Dateien noch mit dem Manifest überein? Mismatches flaggen.

**Skript:** `scripts/update_manifest.py` – aktualisiert Einträge und meldet Drift.

## Prinzipien

- **Single Source of Truth:** Jede Information lebt an genau einer Stelle. Kombinations-Infos stehen in den Maßnahmen-Seiten, nicht in einer separaten Datendatei.
- **Raw ist immutable:** Die Dateien in `raw/` werden nie verändert.
- **Wiki gehört dem LLM:** Der Mensch liest, das LLM schreibt und pflegt.
- **Jedes Detail zählt:** Fördersätze, Abzüge, Symbole – alles explizit und mit Euro-Beträgen. Landwirte brauchen exakte Zahlen.
- **Links sind Wissen:** Die Vernetzung zwischen Seiten ist genauso wertvoll wie der Seiteninhalt selbst.

## Scope-Entscheidungen

### Beratungs- und Antragstellungsebene (Entscheidung 2026-04-14)

Das Wiki hilft bei zwei Fragen: **"Soll ich diese Maßnahme beantragen?"** (Beratung) und **"Wie beantrage ich korrekt?"** (Antragstellung). Zielgruppe ist ein Landwirt, der Maßnahmen bewerten und den Antrag vollständig einreichen will.

**Jetzt aufgenommen:**
- FAKT-Codes → zentrale Mapping-Tabelle in `wiki/Antragstellung/FAKT_Codes.md` + `fakt_code` in jedem Maßnahmen-YAML
- Nachweisfristen → als Checklisten in Antragstellung-Seiten

**Teilweise aufgenommen:**
- Platzangebote G-Maßnahmen → nur im FAQ-Kontext ("Schaffe ich die Auflagen?")

**Weiterhin ausgeschlossen:**
- Bestandsverzeichnis-Pflichten und Formular-Details
- FIONA-Formularfeld-Hinweise
- Rückgabe-/Übertragungsregeln für Verpflichtungen

**Begründung Ausschlüsse:** Diese Infos sind rein prozedural – man braucht sie erst, wenn man vor FIONA sitzt. Für diese Details verweist das Wiki auf die Originalquelle: `raw/GA - Erlaeuterungen und Ausfuellhinweise 2026.pdf`.

**Faustregel bei Ingest:** "Hilft diese Info bei der Entscheidung ODER dabei, den Antrag korrekt und vollständig einzureichen?" – wenn nein, gehört sie nicht ins Wiki.
