# Plan B: Weitere Quellen + Antragstellung-Seiten (Schritte 4–7)

*Standalone – setzt Plan A voraus, braucht aber keine Kenntnis der Details.*

## Context

Die Antragstellung-Struktur steht (Plan A). Jetzt werden die größeren Quellen verarbeitet und die restlichen Antragstellung-Seiten angelegt.

---

## Schritt 4: Ackerbau-Empfehlungen + E8 Merkblatt

**Quellen:**
- `downloads/formulare_2026/Empfehlungen_für_ackerbauliche_FAKT_II-Maßnahmen_E1.2_E7-E9_E13_E14_E15_F3_F4.pdf` (5 MB, ~48 Seiten → **splitten**)
- `downloads/formulare_2026/Merkblatt_Pflege_mehrjähriger_Blühmischungen_E8.pdf` (119 KB)

1. Split-Skript `scripts/split_empfehlungen_ackerbau.sh` (qpdf, +1-Seite-Regel)
2. Kapitelweise extrahieren, mit User besprechen
3. Erstellen:
   - `wiki/Antragstellung/Antragstellung_Ackerbau.md` (E1.2, E9, E10, E12, E13.1, E13.2, F3, F4)
   - `wiki/Antragstellung/Antragstellung_Bluehflaechen.md` (E7, E8, E14, E15)
4. Praxishinweise in bestehende Maßnahmen-Seiten einarbeiten (wo beratungsrelevant)
5. `## Antragstellung`-Links in betroffene Seiten
6. Log

---

## Schritt 5: ÖR-Ergänzungen

**Quelle:** `downloads/formulare_2026/Ergänzende_Informationen_zu_ÖR1b_ÖR1c_ÖR2_und_ÖR5.pdf` (274 KB)

1. Extrahieren
2. `wiki/Konzepte/Oeko-Regelungen.md` anreichern (aktuell nur Übersichtstabelle)
3. Querverweise in Maßnahmen-Seiten, die mit diesen ÖR interagieren
4. Log

---

## Schritt 6: LPR-Broschüre – Scope-Prüfung

**Quelle:** `downloads/formulare_2026/Broschüre_LPR-Grünlandmaßnahmen_in_Kombination_mit_Öko-Regelungen.pdf` (2,9 MB)

1. Lesen und mit User besprechen, ob LPR-Inhalt in Scope
2. Falls ja: in Oeko-Regelungen.md / Kombinationstabelle einarbeiten
3. Falls nein: Entscheidung in log.md dokumentieren

---

## Schritt 7: Restliche Antragstellung-Seiten

Aus bereits vorhandenem Wiki-Material (keine neuen Quellen nötig):

- `wiki/Antragstellung/Antragstellung_Gruenland.md` (B1.2, B3.2, B4, B5, B6, B7)
- `wiki/Antragstellung/Antragstellung_Oekolandbau.md` (D2)
- `wiki/Antragstellung/Antragstellung_Betriebsbezogen.md` (A2, A3, C1, C2, C3)
- `wiki/Antragstellung/Antragstellung_Sonderkulturen.md` (E4, E5, E6, E11)
- `## Antragstellung`-Links in alle noch fehlenden Maßnahmen-Seiten

---

## Verifikation Plan B

- [ ] Alle Antragstellung-Seiten existieren (~8 Stück)
- [ ] Alle Maßnahmen-Seiten haben `## Antragstellung`-Link
- [ ] Bidirektionale Links: Antragstellung → Maßnahme und zurück
- [ ] `wiki/Konzepte/Oeko-Regelungen.md` angereichert
- [ ] `wiki/log.md` dokumentiert jeden Ingest
- [ ] Grep nach `type: antragstellung` findet alle neuen Seiten
