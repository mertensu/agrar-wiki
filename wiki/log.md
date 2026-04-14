# Wiki-Log

## [2026-04-14] ingest | Konditionalität – Kond_Infobroschuere_2026.pdf

**Quelle:** `raw/konditionalitaet/Kond_Infobroschuere_2026.pdf` (76 S.), gesplittet in 6 Kapitel-PDFs via `scripts/split_kond_info.sh`

**Was & Warum:**
Die Konditionalität ist das regulatorische Fundament aller GAP-Zahlungen (inkl. FAKT II). Jede FAKT-Maßnahme baut auf diesen Baseline-Anforderungen auf. Integration als Konzeptseiten, damit jede Maßnahme zeigt, welche Basisregeln sie berührt.

**Strukturelle Änderungen:**
- `scripts/split_kond_info.sh` erstellt – splittet 76-S.-PDF in 6 Kapitel-PDFs (qpdf, +1-Seiten-Überlappung)
- `scripts/extract_konditionalitaet.py` erstellt – pdfplumber-Extraktion aller 6 Teil-PDFs → JSON
- `CLAUDE.md` ergänzt um "Große PDFs aufbereiten (>20 Seiten)"-Workflow

**Erstellt (17 Seiten):**
- `wiki/Konzepte/Konditionalitaet.md` – Übersichtsseite (Rewrite, vorher Platzhalter)
- 9 GLÖZ-Einzelseiten: `GLOEZ_1_Dauergruenland.md` bis `GLOEZ_9_Natura2000_Dauergruenland.md`
- 7 GAB-Einzelseiten: `GAB_1_Wasserrahmenrichtlinie.md`, `GAB_2_Nitratrichtlinie.md`, `GAB_3_4_Naturschutz.md`, `GAB_5_Lebensmittelsicherheit.md`, `GAB_6_Hormonverbot.md`, `GAB_7_8_Pflanzenschutz.md`, `GAB_9_10_11_Tierschutz.md`

**Aktualisiert:**
- `wiki/index.md` – GLÖZ- und GAB-Unterabschnitte unter Konzepte ergänzt

**Änderungen mit Quellennachweis:**
- Alle Inhalte aus Kond_Infobroschuere_2026.pdf, S. 1–57 (Kapitel I–IV)
- Änderungen 2026: GLÖZ 1 Ersatzflächen-Einschränkung (S. 5), GLÖZ 2 Narbenerneuerung (S. 5), GLÖZ 6 Zikaden-Ausnahme (S. 5–6), GLÖZ 7 Mais-Mischkultur (S. 6), GAB 1/2 BVerwG-Urteil (S. 6), GAB 7/8 neue Aufzeichnungspflichten (S. 6, 46), Omnibus III Öko-Befreiung (S. 2)
- Sanktionssystem: 3% fahrlässig (1–10%), 5% Kappung, 20% Wiederholung, 15–100% Vorsatz (S. 59–60)
- Kontrollquote 1%, ≤10 ha befreit seit 2024 (S. 57–58)
- Tierschutz-Mindestflächen: Kälber 1,5–1,8 m² (S. 52), Mastschweine 0,20–1,00 m² (S. 56), Sauen 1,48–2,48 m² (S. 56)

**Noch offen:**
- Integration der Konditionalitäts-Links in alle ~42 Maßnahmen-Seiten (Abschnitt "## Konditionalität")
- Verarbeitung der 4 weiteren PDFs in `raw/konditionalitaet/`

## [2026-04-13] query → strategie | Erosions-Gewinner

**Anlass:** Analyse welche Maßnahmen für erosionsgefährdetes Ackerland am Hang den höchsten Ertrag bringen.

**Erstellt:** `wiki/strategie/Erosions_Gewinner.md`

**Methodik:**
- Grep nach Erosion/Boden/Gewässer/Wasser in allen Maßnahmen-Seiten → 8 relevante Maßnahmen identifiziert
- Kombinierbarkeit geprüft anhand der Kombinations-Links auf den jeweiligen Seiten
- Drei Strategien durchgerechnet mit FAKT-Fördersätzen + geschätztem Mais-Deckungsbeitrag
- x/a-Abzüge berücksichtigt (E14+D2: 420€ gemäß Kombinationstabelle Fußnote Zeile 50)

**Hinweis:** Mais-Deckungsbeiträge (600–800 €/ha) sind Schätzwerte, keine FAKT-Quelle. Betriebliche Kalkulation erforderlich.

## [2026-04-13] ingest | Nutzcodeliste für FAKT II-Förderantrag 2026

**Quelle:** `raw/Nutzcodeliste für FAKT II-Förderantrag_2026.pdf` (1 S.)

**Erstellt:**
- `wiki/Nutzcodeliste.md` – Zuordnung Nutzcode → zulässige FAKT-Maßnahmen (B1.2, B3.2, B4, B5, E7, E8, E14)

**Aktualisiert:**
- 7 Maßnahmen-Seiten: Link auf [[Nutzcodeliste]] ergänzt
- `wiki/index.md`: Nutzcodeliste aufgenommen

## [2026-04-13] refactor | Kombinations-Links angereichert + Schema erstellt

**Quelle:** `raw/Kombinationstabelle FAKT II.xlsx` (Stand 24.10.2025), Fußnoten Zeilen 48–51

**Was & Warum:**

Alle 30 Maßnahmen-Seiten hatten bisher nur "kombinierbar / nicht kombinierbar" ohne Symbole oder Beträge. Beim Beantworten der Frage "Kann D2 mit B1.2 kombiniert werden?" fiel auf, dass die Abzugsbeträge (x/a) fehlten – ein Landwirt hätte mit 580 €/ha statt 530 €/ha gerechnet.

**Änderungen mit Quellennachweis:**

Reduzierte Fördersätze aus `Kombinationstabelle FAKT II.xlsx`, Fußnoten:
- B1.2 auf 100 €/ha bei Kombination mit D2 (Fußnote Zeile 50: "Reduzierte Förderprämie in Kombination mit D2 Ökolandbau: B1.2: 100€")
- E5 auf 2.500 €/ha bei Kombination mit D2 (Fußnote Zeile 50: "E5: 2500€")
- E10 auf 40 €/ha bei Kombination mit D2 (Fußnote Zeile 50: "E10: 40€")
- E14 auf 420 €/ha bei Kombination mit D2 (Fußnote Zeile 50: "E14: 420€")
- E15 auf 180 €/ha bei Kombination mit D2 (Fußnote Zeile 50: "E15: 180€")
- D2 Beibehaltung GL auf 190 €/ha bei Kombination mit ÖR 4 (Fußnote Zeile 48: "D2 Ökolandbau - Beibehaltung - Grünland: 190€")
- D2 Einführung GL auf 380 €/ha bei Kombination mit ÖR 4 (Fußnote Zeile 48: "D2 Ökolandbau - Einführung - Grünland: 380€")
- B4 auf 220 €/ha bei Kombination mit B7 (Fußnote Zeile 51: "B4: 220€")
- B5 auf 220 €/ha bei Kombination mit B7 (Fußnote Zeile 51: "B5: 220€")

Symbole (X, x/a, o, (o), kR, –) aus den Matrix-Zellen der Excel-Datei, Zeilen 5–46.
ÖR-Kombinationen aus den Zeilen 5–14 (Öko-Regelungen × FAKT II).

**Korrekturen:**
- B4 × B7 war fälschlich als "nicht kombinierbar" eingetragen – Excel-Zellen K21 und H24 zeigen beide "x/a". Korrigiert zu "kombinierbar mit Abzug (220 €/ha)".

**Strukturelle Änderungen:**
- JSON-Kombinationstabelle (`wiki/data/kombinationstabelle.json`) entfernt – Wiki-Links sind jetzt Single Source of Truth
- `scripts/extract_raw.py` und `scripts/update_kombinationen.py` gesichert
- `CLAUDE.md` erstellt – vollständiges Schema für alle Agenten

## [2026-04-12] ingest | FAKT II Broschüren (3 PDFs) + Kombinationstabelle (Excel)

**Quellen:**
- `raw/fakt_broschuere_1.pdf` (8 S.) – Gesamtbroschüre mit Einführung, Antragstellung
- `raw/fakt_broschuere_2.pdf` (2 S.) – Maßnahmenübersicht mit Fördersätzen
- `raw/fakt_broschuere_3.pdf` (37 S.) – Detaillierte Kurzbeschreibungen aller Maßnahmen
- `raw/Kombinationstabelle FAKT II.xlsx` – Kombinierbarkeitsmatrix

**Erstellt:**
- 34 Maßnahmen-Seiten (A2–G7)
- 7 Kategorie-Seiten (A–G)
- 5 Konzept-Seiten (RGV, Konditionalität, Öko-Regelungen, Verpflichtungszeitraum, Gemeinsamer Antrag)
- 1 Überblicksseite (FAKT II Gesamtübersicht)
- 1 Kombinationstabelle (Zusammenfassung)
- 1 Index
- Vernetzung über Wikilinks zwischen Maßnahmen, Kategorien und Konzepten
