# FAKT II Agrar-Wiki – Schema

Dieses Projekt ist ein **LLM-Wiki** für das FAKT II-Förderprogramm (Baden-Württemberg). Die Wissensbasis wird vom LLM geschrieben und gepflegt, der Mensch kuratiert Quellen und stellt Fragen.

## Verzeichnisstruktur

```
raw/                          # Rohdaten – NIEMALS verändern
  fakt_broschuere_1.pdf       # Allgemeine Infos, Antragstellung
  fakt_broschuere_2.pdf       # Übersichtstabelle Maßnahmen
  fakt_broschuere_3.pdf       # Detailbeschreibungen A2–G7
  Kombinationstabelle FAKT II.xlsx  # Kombinationsmatrix

wiki/                         # LLM-generiertes Wiki – Obsidian-Vault
  index.md                    # Inhaltsverzeichnis (nach Kategorien)
  log.md                      # Chronologisches Arbeitsprotokoll
  FAKT_II_Uebersicht.md      # Programmübersicht
  Kombinationstabelle.md      # Kombinationsregeln (Zusammenfassung)
  massnahmen/                 # Eine Seite pro Maßnahme (~42 Dateien)
  Kategorien/                 # Eine Seite pro Kategorie (A–G)
  Konzepte/                   # Schlüsselbegriffe (RGV, Konditionalität, …)

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

## Quellenangaben und Widersprüche

### Quellenangaben

Jede faktische Behauptung im Wiki muss ihre Quelle referenzieren. Format: `(Quelle: Dateiname)` nach der Behauptung.

```markdown
- Betriebe ab 0,3 RGV/ha Grünland (Quelle: fakt_broschuere_3.pdf, S. 8)
```

- Bei mehreren Quellen: `(Quellen: datei1.pdf, datei2.xlsx)`
- Wenn eine Behauptung **keine Quelle** hat: mit `<!-- TODO: Quelle prüfen -->` markieren
- Die Fußzeile `*Quelle: FAKT II-Broschüre Baden-Württemberg, Stand Oktober 2025*` gilt als Default-Quelle für die ganze Seite. Inline-Quellenangaben nur nötig, wenn die Info aus einer **anderen** Quelle stammt oder besonders kritisch ist (z.B. Abzugsbeträge).

### Widersprüche

Wenn zwei Quellen sich widersprechen, **nie stillschweigend eine Version wählen**. Stattdessen explizit markieren:

```markdown
> **Widerspruch:** Laut fakt_broschuere_2.pdf beträgt der Fördersatz 150 €/ha,
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

## Wikilinks

- Format: `[[Dateiname_ohne_Extension|Anzeigename]]`
- Links sind **bidirektional**: wenn A auf B verlinkt, muss B auch auf A verlinken (Obsidian zeigt Backlinks, aber explizite Links sind besser)
- Dateinamen verwenden Unterstriche, keine Leerzeichen

## Operationen

### Ingest (neue Quelle verarbeiten)

1. Neue Datei in `raw/` ablegen
2. Text extrahieren: `uv run --with pdfplumber python3 scripts/extract_raw.py`
3. **Erst besprechen, dann schreiben:** Schlüsselinformationen mit dem User diskutieren – was ist neu, was hat sich geändert, was widerspricht bestehenden Daten? Nicht blind losschreiben.
4. Bestehende Wiki-Seiten aktualisieren oder neue erstellen
5. Quellenangaben setzen: `(Quelle: dateiname.pdf)` bei neuen/geänderten Fakten
6. Widersprüche zu bestehenden Daten explizit markieren (siehe Quellenangaben)
7. Kombinations-Links prüfen und aktualisieren
8. `wiki/index.md` aktualisieren
9. `wiki/log.md` ergänzen (siehe Log-Format unten)

### Query (Frage beantworten)

1. `wiki/index.md` lesen um relevante Seiten zu finden
2. Relevante Seiten lesen (Grep/Glob statt alles laden)
3. Antwort synthetisieren mit Quellenverweisen
4. **Wenn die Antwort wiederverwendbar ist** → als neue Wiki-Seite ablegen

### Lint (Gesundheitscheck)

Periodisch prüfen:
- Widersprüche zwischen Seiten
- Veraltete Informationen
- Orphan-Seiten (keine eingehenden Links)
- Fehlende Konzeptseiten für häufig erwähnte Begriffe
- Kombinations-Links ohne Euro-Betrag bei x/a
- Fehlende Quellenangaben bei kritischen Zahlen (Fördersätze, Abzüge)
- `<!-- TODO: Quelle prüfen -->`-Markierungen auflösen
- Inkonsistente Kombinations-Angaben (A sagt kombinierbar mit B, aber B erwähnt A nicht)

### Update (bei neuem Maßnahmenkatalog, z.B. FAKT II → FAKT III)

1. **Vorher-Snapshot erstellen:** `python3 scripts/snapshot_wiki.py > wiki_snapshot_vor_update.json`
2. Neue PDFs/Excel in `raw/` ablegen (alte behalten, nie löschen)
3. `scripts/extract_raw.py` ausführen (ggf. anpassen für neue Dateinamen)
4. **Diff identifizieren:** Neuen Snapshot gegen alten vergleichen – was ist neu, was hat sich geändert, was entfällt?
5. Wiki-Seiten aktualisieren (Fördersätze, Auflagen, neue/entfallene Maßnahmen)
6. `scripts/update_kombinationen.py` Dicts anpassen und ausführen
7. `scripts/update_konditionalitaet.py` Mapping anpassen und ausführen
8. `wiki/log.md` ergänzen
9. **Nachher-Snapshot erstellen** und als `wiki_snapshot.json` committen
10. Commit mit aussagekräftiger Message, die die Quelle und Hauptänderungen benennt

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

## Prinzipien

- **Single Source of Truth:** Jede Information lebt an genau einer Stelle. Kombinations-Infos stehen in den Maßnahmen-Seiten, nicht in einer separaten Datendatei.
- **Raw ist immutable:** Die Dateien in `raw/` werden nie verändert.
- **Wiki gehört dem LLM:** Der Mensch liest, das LLM schreibt und pflegt.
- **Jedes Detail zählt:** Fördersätze, Abzüge, Symbole – alles explizit und mit Euro-Beträgen. Landwirte brauchen exakte Zahlen.
- **Links sind Wissen:** Die Vernetzung zwischen Seiten ist genauso wertvoll wie der Seiteninhalt selbst.
