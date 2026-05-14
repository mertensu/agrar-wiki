# FAKT II Agrar-Wiki

Ein **LLM-Wiki** zum FAKT II-Förderprogramm Baden-Württemberg
(Förderung für Agrarumwelt, Klima- und Tierwohlmaßnahmen).

Das Wiki bündelt die offiziellen Quellen (Broschüre, Kombinationstabelle,
Konditionalität, GA-Erläuterungen, Merkblätter) zu einer durchsuchbaren,
verlinkten Wissensbasis – nach dem Pattern eines persistenten, vom LLM
gepflegten Knowledge Vaults (Karpathy-Style LLM-Wiki) statt RAG.

**Zielgruppe:** Landwirte, Berater:innen und Sachbearbeitung, die zwei
Fragen beantworten müssen:

1. **Soll ich diese Maßnahme beantragen?** (Beratung)
2. **Wie beantrage ich korrekt?** (Antragstellung)

## Aufbau

```
raw/          Originalquellen (PDF, Excel) – immutable
              + manifest.json mit SHA256-Hashes zur Drift-Erkennung
downloads/    Archiv der Originaldateien vom MLR-Portal
wiki/         Das eigentliche Wiki (Obsidian-Vault, Markdown + Wikilinks)
  index.md             Inhaltsverzeichnis
  log.md               Chronologisches Arbeitsprotokoll
  SCHEMA.md            Wiki-Verfassung (Seitentypen, Frontmatter, Tags)
  massnahmen/          Eine Seite pro FAKT-Maßnahme (~42)
  Kategorien/          A–G nach FAKT-Kategorie
  Konzepte/            Schlüsselbegriffe (RGV, GLÖZ, Konditionalität …)
  Antragstellung/      Checklisten, FAKT-Codes, Fristen
scripts/      Reproduzierbare Skripte (Extraktion, Lint, Manifest, Snapshots)
service/      FastAPI/PydanticAI-Service, der einen Wiki-Agent als API bereitstellt
CLAUDE.md     Operative Workflows (Ingest, Query, Update, Lint)
```

## Nutzung

### Wiki lesen

Das Wiki ist als **Obsidian-Vault** angelegt – `wiki/` als Vault-Wurzel
öffnen, Backlinks und Graph funktionieren nativ. Es funktioniert
aber auch als reines Markdown-Verzeichnis (z.B. auf GitHub).

Einstieg: [`wiki/index.md`](wiki/index.md).

### Wiki abfragen (per Service)

Unter `service/` läuft ein FastAPI-basierter Wiki-Agent mit Redis-
Rate-Limit. Setup & Deploy: siehe [`service/README.md`](service/README.md)
und [`service/DEPLOY.md`](service/DEPLOY.md).

### Wiki pflegen

Alle wiederkehrenden Operationen (Ingest neuer Quellen, Updates,
Snapshots, Lint, Health-Check) sind in [`CLAUDE.md`](CLAUDE.md)
und [`scripts/README.md`](scripts/README.md) beschrieben.

Wichtige Skripte:

| Skript | Zweck |
|--------|-------|
| `scripts/update_manifest.py` | SHA256-Manifest pflegen / Drift in `raw/` melden |
| `scripts/extract_raw.py` | PDFs + Excel nach JSON extrahieren |
| `scripts/lint_wiki.py` | Pflicht-Lint (Frontmatter, Links, Quellen, Tags) |
| `scripts/snapshot_wiki.py` | Snapshot der Wiki-Inhalte für Diff bei Updates |
| `scripts/update_kombinationen.py` | Kombinations-Links über alle Seiten setzen |
| `scripts/update_konditionalitaet.py` | Konditionalitäts-Verweise pflegen |

**Lint vor jedem Commit verpflichtend:**

```bash
uv run --with pyyaml python3 scripts/lint_wiki.py
```

## Prinzipien

- **Single Source of Truth** – jede Information lebt an genau einer Stelle.
- **Raw ist immutable** – Dateien in `raw/` werden nie verändert.
- **Wiki gehört dem LLM** – der Mensch kuratiert Quellen und stellt Fragen,
  das LLM schreibt und pflegt die Seiten.
- **Quellenpflicht** – jede faktische Aussage ist mit Dateiname + Position
  (Seite, Zeile, Zelle) belegt. Widersprüche werden explizit markiert,
  nie stillschweigend aufgelöst.
- **Links sind Wissen** – die bidirektionale Vernetzung zwischen Seiten
  ist genauso wertvoll wie die Seiteninhalte selbst.

Details und Workflows: [`CLAUDE.md`](CLAUDE.md), [`wiki/SCHEMA.md`](wiki/SCHEMA.md).

## Stand

Aktueller Förderkatalog: **FAKT II**, Stand Oktober 2025
(BW-Broschüre + Kombinationstabelle + Konditionalität 2026).
Quellenstand und Änderungen siehe [`wiki/log.md`](wiki/log.md) und
[`raw/manifest.json`](raw/manifest.json).
