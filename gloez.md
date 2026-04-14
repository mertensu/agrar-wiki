# Konditionalitäts-Integration: Arbeitsnotizen

## Status: Extraktion abgeschlossen, Wiki-Schreiben noch nicht begonnen

## Neue Quellen (5 PDFs in raw/)

1. **Kond_Infobroschuere_2026.pdf** (76 Seiten) – Hauptquelle für alle GLÖZ + GAB
2. **Soz_Kond_Infobroschuere_2026.pdf** (16 Seiten) – Soziale Konditionalität (Arbeitsrecht, Arbeitssicherheit)
3. **Info_Mindestpraktiken_Bodenbewirtschaftung_zur_Begrenzung_von_Erosion_(GLÖZ_5).pdf** (8 Seiten) – Detail zu GLÖZ 5, BW-spezifisch
4. **Merkblatt 36_Gewässerrandstreifen in Baden-Württemberg_2024.pdf** (10 Seiten) – Detail zu GLÖZ 4 / Gewässerrandstreifen
5. **Merkblatt_Pflanzenschutzdokumentation.pdf** (4 Seiten) – Detail zu GAB 7/8 Pflanzenschutz-Dokumentation ab 2026

## Extraktionsskript

`scripts/extract_konditionalitaet.py` – fertig, getestet, JSON nach `/tmp/kond_extracted.json`

## Bereits gelesene Inhalte

### GLÖZ-Standards (aus Kond_Infobroschuere_2026.pdf)

| GLÖZ | Thema | FAKT-II-Relevanz (erste Einschätzung) |
|------|-------|---------------------------------------|
| GLÖZ 1 | Erhaltung Dauergrünland | B-Maßnahmen (Grünland), D2 Ökolandbau |
| GLÖZ 2 | Schutz Feuchtgebiete/Moore | B4 Biotope, B5 FFH-Mähwiesen |
| GLÖZ 3 | Verbot Stoppelbrand | Allgemein alle Ackerbau-Maßnahmen |
| GLÖZ 4 | Pufferstreifen Gewässer (3m) | F3/F4 Erosionsschutz, E7/E8 Blühflächen, E14/E15 |
| GLÖZ 5 | Erosionsschutz (Pflugverbote) | F3 Precision Farming, F4 Strip-Till, E1.2 Begrünung |
| GLÖZ 6 | Mindestbodenbedeckung (80% AL) | E1.2 Begrünungsmischungen, E8 Brachebegrünung, E10 Ackerfutterbau |
| GLÖZ 7 | Fruchtwechsel (3J/2 Kulturen) | E9 Mais-Stangenbohnen, E13 Drillreihenabstand, allgemein Ackerbau |
| GLÖZ 8 | Landschaftselemente | A3 Kleine Strukturen, C1 Streuobst |
| GLÖZ 9 | Umweltsensibles DGL in Natura 2000 | B4 Biotope, B5 FFH-Mähwiesen |

### GAB-Standards (Inhaltsverzeichnis gelesen, Detail noch nicht)

| GAB | Thema | FAKT-II-Relevanz |
|-----|-------|------------------|
| GAB 1 | Wasserrahmenrichtlinie (Phosphat) | F-Maßnahmen, D2 |
| GAB 2 | Nitratrichtlinie (Stickstoff) | F-Maßnahmen, D2 |
| GAB 3 | Vogelschutzrichtlinie | B4, B5, C1 |
| GAB 4 | FFH-Richtlinie | B4, B5 |
| GAB 5 | Lebensmittel-/Futtermittelsicherheit | G-Maßnahmen (Tierhaltung) |
| GAB 6 | Verbot bestimmter Stoffe (Tiererzeugung) | G-Maßnahmen |
| GAB 7+8 | Pflanzenschutz | E3 Herbizidverzicht, E11 Herbizidfreie DK, E4 Trichogramma, E5/E6, B7 |
| GAB 9 | Kälberschutz | G7 Kälber |
| GAB 10 | Schweineschutz | G2 Mastschweine, G5/G6 Ferkel |
| GAB 11 | Nutztiere allgemein | Alle G-Maßnahmen |

### Soziale Konditionalität (Soz_Kond_Infobroschuere_2026.pdf)
- Betrifft Arbeitsrecht (transparente Arbeitsbedingungen, Arbeitssicherheit, Gesundheitsschutz)
- Gilt für alle Empfänger von Direktzahlungen + FAKT II
- Weniger relevant für einzelne Maßnahmen, eher betriebsübergreifend

### GLÖZ 5 Detail (BW-spezifisches Merkblatt)
- **Vollständig gelesen**
- Erosionsgefährdungsklassen: KWasser1, KWasser2, KWind
- Pflugverbote mit Zeitfenstern und gleichwertigen Erosionsschutzmaßnahmen
- BW erlaubt Pflug auf K1/K2 mit gleichwertigen Maßnahmen (Erosionsschutzstreifen, raue Winterfurche, etc.)
- Öko-Betriebe: Erleichterungen (raue Winterfurche auf K1+K2)
- Einstufung über FIONA-GIS, rasterbasiert 5x5m

### Gewässerrandstreifen (Merkblatt 36)
- **Seiten 1-6 gelesen**
- 10m Außenbereich / 5m Innenbereich
- 5m-Zone: kein Ackerbau (Ausnahmen: mehrjährige Blühstreifen, KUP), kein Dünger/PSM
- Tabelle mit möglichen Nutzungen im Gewässerrandstreifen inkl. FAKT-II-Codes (E8, E10, E14, E15)
- GLÖZ 4: 3m Pufferstreifen (Konditionalität)

### Pflanzenschutzdokumentation (Merkblatt)
- **Vollständig gelesen**
- Neue Pflichten ab 01.01.2026 (DVO 2023/564)
- Erweiterte Dokumentation: EPPO-Code, BBCH-Stadium, Zulassungsnummer, GPS, unverzügliche Dokumentation
- PSM-DOK Plattform für BW
- Ab 2027 voraussichtlich elektronisch + maschinenlesbar Pflicht

## Geplante Wiki-Struktur

### Neue Konzept-Seiten
- `wiki/Konzepte/Konditionalitaet.md` – **existiert bereits**, muss massiv erweitert werden
- `wiki/Konzepte/GLOEZ_Standards.md` – Übersichtsseite alle 9 GLÖZ
- `wiki/Konzepte/GAB_Standards.md` – Übersichtsseite alle 11 GAB
- `wiki/Konzepte/Soziale_Konditionalitaet.md` – eigene Seite
- `wiki/Konzepte/Gewaesserrandstreifen.md` – Detail GLÖZ 4 + Wasserrecht BW
- `wiki/Konzepte/Erosionsschutz.md` – Detail GLÖZ 5 + BW-Regelung
- `wiki/Konzepte/Pflanzenschutzdokumentation.md` – GAB 7/8 Detail

### Änderungen an Maßnahmen-Seiten
Jede Maßnahme bekommt einen neuen Abschnitt:

```markdown
## Konditionalitäts-Bezug
- **GLÖZ 5** (Erosionsschutz): F4 Strip-Till geht über GLÖZ-5-Pflugverbote hinaus …
- **GAB 7/8** (Pflanzenschutz): Dokumentationspflichten gelten zusätzlich …
```

### Noch zu tun (nächste Session)
1. GAB-Abschnitte (S. 20-56) der Hauptbroschüre lesen (bisher nur Inhaltsverzeichnis)
2. Restliche Seiten Gewässerrandstreifen-Merkblatt (S. 7-10)
3. Soziale Konditionalität Detail lesen
4. Mapping GLÖZ/GAB → Maßnahmen finalisieren
5. Wiki-Seiten schreiben
6. Konditionalitäts-Bezug in alle ~42 Maßnahmen-Seiten einfügen
7. index.md und log.md aktualisieren
