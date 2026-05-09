# Wiki Schema

Konstitution des FAKT II Agrar-Wikis. Diese Datei definiert *was* das Wiki abdeckt
und nach welchen Konventionen Seiten gebaut werden. Die operativen Anleitungen
(Ingest-Workflow, Update, Archiv, Lint, Werkzeuge) stehen in `CLAUDE.md`.

## Domain

FAKT II-Förderprogramm Baden-Württemberg, Konditionalität (GLÖZ/GAB), 1.-Säule-
Öko-Regelungen, sowie angrenzende Antrags- und Beratungsthemen für Landwirte.
Fokus: **Beratung** ("soll ich beantragen?") und **Antragstellung**
("wie beantrage ich korrekt?"). Formularfeld-Details und Bestandsverzeichnis-
Pflichten sind ausgeschlossen (Verweis auf `GA - Erlaeuterungen und Ausfuellhinweise 2026.pdf`).

## Seitentypen

| `type:` | Verzeichnis | Zweck |
|---|---|---|
| `massnahme` | `massnahmen/` | Eine Maßnahme (B1.2, E7, …) mit Fördersatz, Auflagen, Kombinationen |
| `kategorie` | `Kategorien/` | Übersicht einer FAKT-Kategorie A–G |
| `konzept` | `Konzepte/` | Schlüsselbegriff (RGV, GLÖZ 8, Konditionalität, …) |
| `antragstellung` | `Antragstellung/` | Checklisten, FAKT-Codes, Fristen, gruppiert nach Antragskontext |
| `beispielfrage` | `Beispielfragen/` | Gefilterte Synthese-Antwort zu einem Praxisszenario |
| `strategie` | `strategie/` | Beratungs-Use-Case (z.B. Erosionsfläche umbauen) |
| `uebersicht` | (Wurzel) | Programm-/Listen-Übersicht (FAKT_II_Uebersicht, Nutzcodeliste, Kombinationstabelle) |

Drei bis sechs Typen reichen — keine Proliferation. Neue Typen brauchen einen
Eintrag hier *vor* der ersten Verwendung.

## Konventionen

- **Dateinamen:** Maßnahmen-Codes wie `B1.2_Extensive_Gruenland.md` sind erlaubt
  (Punkt im Namen ist Obsidian-tauglich). Sonst Unterstriche, keine Leerzeichen.
- **Wikilinks:** `[[Dateiname_ohne_Extension|Anzeigename]]`. Mindestens
  **2 ausgehende Links pro Seite** — isolierte Seiten sind im Graph unsichtbar.
- **Backlinks:** Wenn A auf B verlinkt, sollte B auf A zurückverlinken
  (Obsidian zeigt das automatisch, explizite Links sind aber robuster).
- **Quellen:** Inline `(Quelle: dateiname.pdf, S. X)` für einzelne Behauptungen,
  Footer `*Quelle: ...*` als Default-Quelle der Seite. Zusätzlich strukturierte
  `sources:` im Frontmatter (siehe unten).
- **`updated:` bumpen** bei jeder inhaltlichen Änderung.
- **Index-Pflicht:** Jede neue Seite kommt in `index.md`.
- **Log-Pflicht:** Jede Aktion (ingest, update, lint, archive) wird in
  `log.md` notiert.

## Frontmatter

Pflicht für **alle** Seiten:

```yaml
---
type: massnahme | kategorie | konzept | antragstellung | beispielfrage | strategie
titel: "Anzeigetitel"
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: ["Dateiname.pdf", "Andere_Quelle.xlsx"]
tags: [tag1, tag2]   # nur aus Taxonomie unten
---
```

Maßnahmen-Seiten ergänzen domänenspezifische Felder:

```yaml
code: "B1.2"
kategorie: "B – Erhaltung und Pflege der Kulturlandschaft"
foerdersatz: "150 €/ha"
einheit: "ha"
verpflichtung: "mehrjährig"
fakt_code: "21"
```

Antragstellungs-Seiten dokumentieren ihren Geltungsbereich:

```yaml
betrifft: ["B1.2", "B3.2", ...]
```

### Optionale Qualitäts-Signale

```yaml
confidence: high | medium | low
contested: true
contradictions: [seitenname_ohne_md]
```

- `confidence` Default ist `high` (Broschüre + Kombinationstabelle stimmen
  überein, kein Konflikt). `medium` bei rekonstruierten Werten oder
  Einzelquelle. `low` bei indirekten Ableitungen.
- `contested: true` flaggt ungelöste Widersprüche auf der Seite.
- Beim Archivieren: `archived: YYYY-MM-DD` und `archived_reason: "..."`.

### `sources:`-Konvention

- **Nur Dateinamen**, kein `raw/`-Prefix, keine Unterordner.
  Beispiel: `Kond_Infobroschuere_2026.pdf` (nicht `raw/konditionalitaet/Kond_Infobroschuere_2026.pdf`).
- **Nur Dateien aus `raw/`**, nie Wiki-Slugs, nie `downloads/`.
- **Reihenfolge:** Hauptquelle zuerst, ergänzende danach.

## Tag-Taxonomie

Jede `tags:`-Eintrag muss in dieser Liste stehen. Neuer Tag → erst hier
hinzufügen, dann verwenden. Verhindert Tag-Wildwuchs („gruenland",
„grünland", „GL" als drei Tags für dieselbe Sache).

**Flächentypen / Bewirtschaftung**
- `ackerbau`
- `gruenland`
- `dauerkultur` — Streuobst, Wein, Obst
- `tierhaltung` — Rind/Schwein/Geflügel/Schaf

**Schutzgüter**
- `biodiversitaet` — Blühflächen, Artenschutz, Niederwild
- `wasserschutz` — Gewässerrandstreifen, Düngung an Gewässern, GLÖZ 4
- `bodenschutz` — Erosion, Humuserhalt, Bodenbedeckung
- `klimaschutz` — Moor, Dauergrünland, Treibhausgas

**Bewirtschaftungsthemen**
- `pflanzenschutz` — PSM-Verzicht, Reduktion
- `duengung` — N-Düngung, Wirtschaftsdünger
- `tierwohl` — Haltungsformen, Auslauf, Weide
- `oekolandbau` — D2 und ÖR-Anrechnung

**Regulatorisch**
- `konditionalitaet` — GLÖZ, GAB, Soziale Konditionalität
- `oekoregelung` — 1.-Säule-Maßnahmen ÖR 1–7
- `landschaftselement` — Hecken, Feldgehölze, Steinmauern

**Antrags-/Förderlogik**
- `kombination` — Kombinationsregeln zwischen Maßnahmen
- `foerderhoehe` — Fördersätze, Abzüge, Staffelungen
- `nachweis` — Belegpflichten, Dokumentation, Fristen
- `antragstellung` — FIONA, FAKT-Codes, Antragspraxis

## Seiten-Schwellwerte

- **Neue Seite anlegen**, wenn ein Begriff in 2+ Quellen vorkommt
  ODER zentral für eine Quelle ist.
- **Bestehende Seite erweitern**, wenn das Thema schon abgedeckt ist.
- **Keine Seite** für Randerwähnungen (ein Name in einer Fußnote ≠ Seite).
- **Splitten**, wenn eine Seite ~200 Zeilen überschreitet.
- **Archivieren** statt löschen — Ablauf siehe `CLAUDE.md`.

## Update-Politik bei Konflikten

1. Datum prüfen — neuere Quelle gewinnt im Default
2. Bei echtem inhaltlichem Widerspruch: beide Positionen mit Datum + Quelle behalten
3. `contradictions: [seite]` und ggf. `contested: true` setzen
4. Im Lint-Bericht zur User-Review markieren
5. Nie still überschreiben

---
*Diese Datei ist die Wiki-Verfassung — ändert sich selten. Operative Workflows: `CLAUDE.md`.*
