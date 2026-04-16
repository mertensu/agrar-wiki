# Wiki-Log

## [2026-04-16] ingest | Flächenangaben & Schlagdefinition aus GA-Erläuterungen Kap. 4

**Quelle:** `GA - Erlaeuterungen und Ausfuellhinweise 2026.pdf`, Kap. 4.1–4.3 (S. 17–24)

**Was & Warum:**
Kap. 4 der GA-Erläuterungen war beim initialen Ingest (2026-04-14) als "prozedural" übersprungen worden. Ausgelöst durch eine Beispielfrage zu A3 und Landschaftselementen zeigte sich, dass die Kapitel beratungsrelevante Grundbegriffe definieren: Was ist ein Schlag, wie zählen LE zur förderfähigen Fläche, wann ist ein Schlag >0,5 ha? Diese fehlenden Definitionen konnten aus dem Wiki heraus nicht beantwortet werden.

**Änderungen mit Quellennachweis:**

*Flaechenangaben_Schlagdefinition.md (neu):*
- Schlag vs. Teilschlag: Definitionen und wann Teilschlagbildung Pflicht ist (S. 18)
- Bruttofläche Landwirtschaft: maximal förderfähige Fläche inkl. LE (S. 18)
- K-LE: grundsätzlich einbeziehbar in förderfähige Fläche, Ausnahme ÖR 1a/1d (S. 18, 21)
- Andere LE: 8 Elementtypen mit Schwellenwerten, 25%-Regel (S. 21–22)
- Bäume: je 10 m² Anrechnung, max. 250 Bäume/ha (S. 22)
- Voraussetzungen: unmittelbarer räumlicher Zusammenhang, ldw. Charakter, isoliert von Wald (S. 22)
- Agri-PV: DIN SPEC 91434, max. 15% Flächenreduktion, K-LE als NC 040 (S. 21)
- Obstbaum-Abgrenzung: ≤330 Bäume/ha = Streuobst, >330 = Dauerkultur, Ausnahmeregel (S. 22)

*A3_Kleine_Strukturen.md:*
- Verbot der künstlichen Schlagaufteilung ergänzt (S. 52)
- Klarstellung: A3 ist gesamtbetrieblich, keine Auswahl einzelner Schläge
- Hinweis auf LE-Einbeziehung und Auswirkung auf Schlaggröße mit Link auf Konzeptseite

*C1_Streuobst.md:*
- Abgrenzung Streuobst vs. Intensivobst ergänzt (≤330 Bäume/ha) mit Link auf Konzeptseite (S. 22)

**Strukturelle Änderungen:**
- `wiki/Konzepte/Flaechenangaben_Schlagdefinition.md` neu
- `wiki/index.md` – Konzeptseite aufgenommen

## [2026-04-15] ingest | ÖR-Details aus GA-Erläuterungen + LPR-Hinweise

**Quelle:** `GA - Erlaeuterungen und Ausfuellhinweise 2026.pdf`, Kap. 5.5 (S. 38–46, Split: `ga_05_direktzahlungen_oer.pdf`)

**Was & Warum:**
Öko-Regelungen-Seite war unvollständig – ÖR 1a, ÖR 1d, ÖR 3, ÖR 6 und ÖR 7 fehlten als Detailabschnitte, ÖR 4 hatte nur Kombinations-Hinweise ohne eigene Voraussetzungen. Alle ÖR sind jetzt vollständig mit Voraussetzungen, Einheitsbeträgen und FAKT-II-Kombinierbarkeit dokumentiert. Zusätzlich LPR-Hinweise auf B4, B5, C1 ergänzt.

**Änderungen mit Quellennachweis:**
- ÖR-Übersichtstabelle: Prämien von "variabel" auf konkrete geplante Einheitsbeträge aktualisiert (GA-Erläuterungen S. 39–46)
- ÖR 1a: Stufensystem 1.300/500/300 €/ha, Voraussetzungen, Ausnahmen ab 1.9./15.8. (S. 39)
- ÖR 1b/1c: Korrektur Einheitsbetrag 150→200 €/ha (S. 40)
- ÖR 1d: Stufensystem 1.000/450/200 €/ha, FFH-Mähwiesen-Ausschluss, 1–6% DGL (S. 41)
- ÖR 3: 600 €/ha, Gehölzstreifen-Vorgaben, ULB-Bestätigung (S. 43)
- ÖR 4: 100 €/ha, 0,3–1,4 RGV/ha, Pflugverbot, Düngeobergrenze 140 kg N/ha, Nicht kombinierbar mit B1.2/B7 (S. 43–44)
- ÖR 5: Nicht kombinierbar mit B3.2/B4 ergänzt (S. 44–45)
- ÖR 6: 150/50 €/ha, kulturspezifische PSM-Verbotszeiträume, Nicht kombinierbar mit D2/E3/E4/E5/E6/E10/E11/E12 (S. 45)
- ÖR 7: 40 €/ha, Natura-2000-Kulisse, kombinierbar mit allen ÖR und FAKT (S. 45–46)
- B4, B5, C1: LPR-Alternativhinweis ergänzt (Quelle: Broschüre_LPR-Grünlandmaßnahmen_in_Kombination_mit_Öko-Regelungen.pdf aus downloads/)

**Korrekturen:**
- ÖR 1b/1c Einheitsbetrag war mit 150 €/ha angegeben, korrekt ist 200 €/ha (GA-Erläuterungen S. 40)

**Strukturelle Änderungen:**
- Keine neuen Dateien, nur Erweiterung von `wiki/Konzepte/Oeko-Regelungen.md` und Ergänzung in `wiki/massnahmen/B4_Biotope.md`, `B5_FFH_Maehwiesen.md`, `C1_Streuobst.md`

## [2026-04-15] refactor | Quellenverweise vereinheitlichen

**Was & Warum:**
Alle Quellenverweise im Wiki auf einen einheitlichen Stil konsolidiert: Dateiname ohne Pfad-Prefix, keine beschreibenden Titel. Ziel: konsistente, maschinenlesbare Quellenangaben.

**Konventionen (neu):**
- Immer Dateiname, nie beschreibender Titel (`Kond_Infobroschuere_2026.pdf` statt `Informationsbroschüre Konditionalität 2026`)
- Kein `raw/`-Prefix (`FAKT_G_Haeufige_Fragen.pdf` statt `raw/FAKT_G_Haeufige_Fragen.pdf`)
- Auf Originale verweisen, nicht auf Splits (`FAKT_II_Broschuere.pdf` statt `fakt_broschuere_3.pdf`)
- `downloads/` wird nie referenziert – nur `raw/` enthält zitierbare Quellen

**Neue Dateien in raw/:**
- `FAKT_II_Broschuere.pdf` – Original-Broschüre (47 S.), bisher nur als 3 manuelle Splits vorhanden
- `Empfehlungen_ackerbauliche_FAKT_II-Massnahmen.pdf` – kopiert aus downloads/, normalisierter Name
- `Ergaenzende_Informationen_OeR1b_OeR1c_OeR2_OeR5.pdf` – kopiert aus downloads/, normalisierter Name
- `Merkblatt_Pflege_Bluehmischungen_E8.pdf` – kopiert aus downloads/, normalisierter Name

**Neues Skript:**
- `scripts/split_fakt_broschuere.sh` – reproduzierbarer Split der Original-Broschüre in die 3 Teile

**Geänderte Dateien (~60):**
- Alle ~35 Maßnahmen-Seiten: Fußzeile `FAKT II-Broschüre Baden-Württemberg` → `FAKT_II_Broschuere.pdf`
- 16 Konditionalitäts-Seiten: Fußzeile `Informationsbroschüre Konditionalität 2026` → `Kond_Infobroschuere_2026.pdf`
- Soziale_Konditionalitaet.md, Gewaesserrandstreifen_BW.md, GLOEZ_5_Erosionsschutz.md: beschreibende Titel → Dateinamen
- Oeko-Regelungen.md: `Ergänzende Informationen zu ÖR…` → `Ergaenzende_Informationen_OeR1b_OeR1c_OeR2_OeR5.pdf`
- Antragstellung_Ackerbau.md, Antragstellung_Bluehflaechen.md: `LTZ-Empfehlungen 2026` → `Empfehlungen_ackerbauliche_FAKT_II-Massnahmen.pdf`
- Antragstellung_Tierwohl.md, FAKT_Codes.md, Kombinationstabelle.md: `raw/`-Prefix entfernt
- log.md: `Empfehlungen Kap. X` → `Empfehlungen_ackerbauliche_FAKT_II-Massnahmen.pdf`; `raw/`-Prefixe entfernt
- CLAUDE.md: Quellenreferenz-Konvention dokumentiert, Verzeichnisstruktur aktualisiert

**Verifizierung:**
- `grep -r 'raw/' wiki/` → 1 Treffer (Verzeichnispfad in "noch offen"-Notiz, kein Quellenverweis)
- `grep -r 'Informationsbroschüre Konditionalität' wiki/` → 0 Treffer
- `grep -r 'FAKT II-Broschüre Baden' wiki/` → 0 Treffer
- `grep -r 'LTZ-Empfehlungen\|LTZ-Merkblatt\|Empfehlungen Kap\.' wiki/` → 0 Treffer
- Alle referenzierten Dateinamen existieren in `raw/`

## [2026-04-14] erstellt | Restliche Antragstellung-Seiten (Plan B, Schritt 7)

**Quelle:** Bestehende Wiki-Seiten (keine neuen Quellen)

**Was & Warum:**
4 neue Antragstellung-Seiten aus vorhandenem Wiki-Material erstellt. Damit hat jede Maßnahme eine Antragstellung-Seite mit Checkliste und häufigen Fehlern.

**Neue Dateien:**
- `wiki/Antragstellung/Antragstellung_Gruenland.md` – betrifft B1.2, B3.2, B4, B5, B6, B7
- `wiki/Antragstellung/Antragstellung_Oekolandbau.md` – betrifft D2 (Einführung, Beibehaltung, Transaktionskosten)
- `wiki/Antragstellung/Antragstellung_Betriebsbezogen.md` – betrifft A2, A3, C1, C2, C3
- `wiki/Antragstellung/Antragstellung_Sonderkulturen.md` – betrifft E4, E5, E6, E11

**Verlinkte Maßnahmen-Seiten (18 Stück):**
B1.2, B3.2, B4, B5, B6, B7 → Antragstellung_Gruenland
A2, A3, C1, C2, C3 → Antragstellung_Betriebsbezogen
D2 Beibehaltung, D2 Einführung, D2 Transaktionskosten → Antragstellung_Oekolandbau
E4, E5, E6, E11 → Antragstellung_Sonderkulturen

**index.md** um 4 Einträge erweitert.

## [2026-04-14] scope-check | LPR-Broschüre (Plan B, Schritt 6)

**Quelle:** `downloads/formulare_2026/Broschüre_LPR-Grünlandmaßnahmen_in_Kombination_mit_Öko-Regelungen.pdf` (7 S., Umweltministerium BW, Stand 12/2025)

**Entscheidung: Nicht in Scope.** LPR ist ein eigenständiges Förderprogramm (Vertragsnaturschutz). Einzige FAKT-II-relevante Info: LPR Teil A und FAKT II sind auf derselben Fläche nicht kombinierbar (Ausnahme G1). Dieser Hinweis wurde in `wiki/Konzepte/Oeko-Regelungen.md` ergänzt. Die LPR-spezifischen Leistungssätze und Beispielrechnungen gehören nicht ins FAKT-II-Wiki.

## [2026-04-14] ingest | ÖR-Ergänzungen (Plan B, Schritt 5)

**Quelle:** `downloads/formulare_2026/Ergänzende_Informationen_zu_ÖR1b_ÖR1c_ÖR2_und_ÖR5.pdf` (15 S., MLR BW, Stand 12.03.2026)

**Was & Warum:**
Oeko-Regelungen.md von reiner Übersichtstabelle zu detaillierter Konzeptseite erweitert. Die Quelle enthält konkrete Umsetzungsregeln, die für FAKT-II-Antragsteller relevant sind (Hauptfruchtarten-Gruppierung bei ÖR 2, Kennartenliste bei ÖR 5, Artenlisten für Blühmischungen bei ÖR 1b/1c).

**Änderungen mit Quellennachweis:**

*Oeko-Regelungen.md – erweitert:*
- ÖR 1b/1c: Artenlisten-Zusammenfassung Gruppe A (einjährig, mind. 10 Arten) und Gruppe B (mehrjährig, mind. 5+5 Arten), Hinweis auf Streichungen ab 2026 (Quelle: Kap. 3, S. 10–15)
- ÖR 2: Hauptfruchtarten-Zusammenfassungen (Weizen, Mais, Kartoffeln etc.), 40%-beetweiser-Anbau-Variante seit 2025, Leguminosen-/Getreideanteil-Regeln, Bracheflächen-Ausschluss (Quelle: Kap. 1, S. 1–6)
- ÖR 4: Kombinations-Abzüge mit D2 ergänzt
- ÖR 5: Vollständige Kennartenliste (33 Einträge), Dokumentationspflicht via profil(bw)-App mit Flora Incognita, Querverweis zu B3.2 (Quelle: Kap. 2, S. 7–9)

## [2026-04-14] ingest | Ackerbau-Empfehlungen + E8 Merkblatt (Plan B, Schritt 4)

**Quellen:**
- `downloads/formulare_2026/Empfehlungen_für_ackerbauliche_FAKT_II-Maßnahmen_E1.2_E7-E9_E13_E14_E15_F3_F4.pdf` (48 S., LTZ Augustenberg 03/2026) – Praxishandreichung mit Umsetzungstipps
- `downloads/formulare_2026/Merkblatt_Pflege_mehrjähriger_Blühmischungen_E8.pdf` (3 S., LTZ Augustenberg) – Pflegehinweise bei Problemvegetation

**Was & Warum:**
Zwei neue Antragstellung-Seiten erstellt, die thematisch verwandte Ackerbau- bzw. Blühflächen-Maßnahmen bündeln. Praxishinweise aus LTZ-Quelle eingearbeitet, da sie für Antragssteller beratungsrelevant sind (Mischungswahl, Fristen, häufige Fehler). Detaillierte Mischungstabellen (Anhang) bewusst nicht 1:1 übernommen – Verweis auf Originalquelle.

**Änderungen mit Quellennachweis:**

*Antragstellung_Ackerbau.md (neu):*
- Checklisten + Praxistipps für E1.2, E3, E9, E10, E12, E13.1, E13.2, F3, F4
- E1.2: Neue Nachweispflicht ab Verschlussdatum 1.1.2027 (Quelle: Empfehlungen_ackerbauliche_FAKT_II-Massnahmen.pdf, S. 6–8)
- E9: Mischungsverhältnis 60–67 % Mais / 33–40 % Bohne; PSM nur Vorauflauf (Quelle: Empfehlungen_ackerbauliche_FAKT_II-Massnahmen.pdf, S. 16–17)
- E13.2: Seit 2025 einheitliche Untersaat-Mischung (Quelle: Empfehlungen_ackerbauliche_FAKT_II-Massnahmen.pdf, S. 19)
- F3: Förderfähige Verfahren (Satellit, Drohne, Sensor, Ertragskarten); mind. 60 % N teilflächenspezifisch (Quelle: Empfehlungen_ackerbauliche_FAKT_II-Massnahmen.pdf, S. 24–27)

*Antragstellung_Bluehflaechen.md (neu):*
- Checklisten + Praxistipps für E7, E8, E14, E15
- E7: Mischung M3+ Detailinfos (30+ Arten), Öko-Betriebe dürfen 5 Arten weglassen (Quelle: Empfehlungen_ackerbauliche_FAKT_II-Massnahmen.pdf, S. 11–12)
- E8: 7 zugelassene Mischungen mit regionaler Zertifizierung (VWW/RegioZert); Öko-Sonderregel 40/60-Mischung (Quelle: Empfehlungen_ackerbauliche_FAKT_II-Massnahmen.pdf, S. 13–15)
- E8 Pflege: Konkrete Maßnahmen bei Verunkrautung/Vergrasung/Disteln; max. 50 % gleichzeitig; Mulchen nie geeignet (Quelle: Merkblatt_Pflege_Bluehmischungen_E8.pdf, S. 1–3)
- E14/E15: 7+ zugelassene Biomasse-Mischungen; Hanf-BLE-Regelung (Quelle: Empfehlungen_ackerbauliche_FAKT_II-Massnahmen.pdf, S. 21–23)

*13 Maßnahmen-Seiten – `## Antragstellung`-Links:*
- E1.2, E3, E9, E10, E12, E13.1, E13.2, F3, F4 → [[Antragstellung_Ackerbau]]
- E7, E8, E14, E15 → [[Antragstellung_Bluehflaechen]]

**Strukturelle Änderungen:**
- `wiki/Antragstellung/Antragstellung_Ackerbau.md` neu
- `wiki/Antragstellung/Antragstellung_Bluehflaechen.md` neu
- `scripts/split_empfehlungen_ackerbau.sh` neu – Split-Skript für 48-S.-PDF (8 Teile in `downloads/formulare_2026/splits/`)
- `wiki/index.md` – Antragstellung-Sektion um 2 Einträge ergänzt

## [2026-04-14] scope-update + ingest | Antragstellung: FAKT-Codes + G-FAQ

**Quellen:**
- `FAKT_Codes_2026.pdf` (2 S.) – Übersicht aller Maßnahmen mit FAKT-Codes
- `FAKT_G_Haeufige_Fragen.pdf` (2 S.) – FAQ zu G-Maßnahmen (MLR, Stand 21.12.2023)

**Was & Warum:**
Wiki-Scope um Antragstellungsebene erweitert (Entscheidung 2026-04-14). Bisher nur Beratung ("Soll ich?"), jetzt auch "Wie beantrage ich korrekt?". Zwei kleinste Quellen als erste Antragstellung-Seiten verarbeitet: FAKT-Code-Zuordnung (für Schlag-Codierung in FIONA) und Tierwohl-FAQ (Praxisfragen zu Auflagen).

**Änderungen mit Quellennachweis:**

*CLAUDE.md – Scope-Update:*
- Überschrift: "Beratungs- und Antragstellungsebene" (vorher: "Beratungsebene, nicht Formularebene")
- Ausschlussliste dreigeteilt: "Jetzt aufgenommen" (FAKT-Codes, Nachweisfristen), "Teilweise aufgenommen" (Platzangebote G), "Weiterhin ausgeschlossen" (Formular-Details, FIONA, Rückgabe)
- Faustregel erweitert um "ODER dabei, den Antrag korrekt und vollständig einzureichen"
- Verzeichnisstruktur: `Antragstellung/` ergänzt
- Neuer Abschnitt: Antragstellung-Seiten (Format, YAML, Verlinkungskonvention)
- YAML-Template: `fakt_code` als optionales Feld ergänzt
- Maßnahmen-Seitenformat: `## Antragstellung`-Abschnitt dokumentiert

*FAKT_Codes.md (neu):*
- Mapping-Tabelle aller 42 Maßnahmen → FAKT-Codes (FAKT_Codes_2026.pdf, S. 1–2)
- 23 Maßnahmen haben FAKT-Codes (B1.2=21, B3.2=23, B4=24, B5=25, B6=62, C2=30, E1.2=41, E3=44, E4=45, E5=46, E6=47, E7=48, E8=49, E9=70, E10=71, E11=72, E12=73, E13.1=74, E13.2=75, E14=76, E15=77, F3=52, F4=53)
- 19 Maßnahmen ohne FAKT-Code (A2, A3, B7, C1, C3, D2, G1–G7) – betriebsbezogen/tierbezogen beantragt

*23 Maßnahmen-Seiten – `fakt_code` in YAML-Frontmatter:*
- Alle 23 Maßnahmen mit FAKT-Code über `scripts/add_fakt_codes.py` aktualisiert

*Antragstellung_Tierwohl.md (neu):*
- FAQ zu Tränke, Ausläufe, Raufutter, Einstreu, Beschäftigungsmaterial (FAKT_G_Haeufige_Fragen.pdf, S. 1–2)
- Fallstricke-Abschnitt: Einstreu Premiumstufe >5cm, Raufutter≠Stroh, Auslauf-Definition, Beschäftigungsautomat G2.1

*11 G-Maßnahmen-Seiten:*
- `## Antragstellung` → Link auf [[Antragstellung_Tierwohl]] in G1–G7 ergänzt

**Strukturelle Änderungen:**
- `wiki/Antragstellung/` Verzeichnis erstellt
- `wiki/Antragstellung/FAKT_Codes.md` neu
- `wiki/Antragstellung/Antragstellung_Tierwohl.md` neu
- `scripts/add_fakt_codes.py` neu – trägt fakt_code in Maßnahmen-YAMLs ein
- `wiki/index.md` – Antragstellung-Sektion ergänzt

## [2026-04-14] ingest | GA-Wichtige Hinweise + GA-Erläuterungen 2026 (FAKT-II-Kapitel)

**Quellen:**
- `GA - Wichtige Hinweise zum GA 2026.pdf` (2 S.) – Neuerungen-Überblick
- `GA - Erlaeuterungen und Ausfuellhinweise 2026.pdf` (102 S.) – Kapitel 7.1 FAKT II (S. 49–78) ausgewertet

**Was & Warum:**
Zwei neue GA-Dokumente aufbereitet. Die "Wichtigen Hinweise" sind das kompakte Neuerungen-Blatt für 2026, die "Erläuterungen" das ausführliche Ausfüllhandbuch. Fokus auf beratungsrelevante Inhalte – FIONA-Codes, Nachweisfristen und Formulardetails bewusst nicht ins Wiki aufgenommen (siehe Scope-Entscheidung in CLAUDE.md).

**Strukturelle Änderungen:**
- `wiki/Konzepte/Neuerungen_2026.md` neu erstellt – zentrale Übersichtsseite für alle Änderungen 2026
- `scripts/split_ga_erlaeuterungen.sh` erstellt – splittet 102-S.-PDF in 8 Kapitel-PDFs (qpdf)
- `ga_erlaeuterungen/` – 8 Teil-PDFs für kapitelweisen Zugriff
- `CLAUDE.md` – Abschnitt "Scope-Entscheidungen" ergänzt

**Änderungen mit Quellennachweis:**

*A3_Kleine_Strukturen.md:*
- Hinweis "Neu ab Antragsjahr 2026" ergänzt (GA - Wichtige Hinweise, S. 2)
- ÖR-3-Ausschluss explizit dokumentiert (GA - Erlaeuterungen, S. 52)

*C2_Weinbausteillagen.md:*
- Hinweis "Neu ab Antragsjahr 2026" ergänzt (GA - Wichtige Hinweise, S. 2)

*C3_Nutztierrassen.md – komplett überarbeitet:*
- Alle Rassen-Varianten mit Einzelpreisen statt Spanne "90–600 €/Tier" (GA - Erlaeuterungen, S. 55–60):
  - Vorderwälder: Milchkuh 380 €, Mutterkuh 200 €, Bulle 300 €
  - Hinterwälder: Milchkuh 600 €, Mutterkuh 160 €, Bulle 200 €
  - Limpurger: Milchkuh 580 €, Mutterkuh 160 €, Bulle 360 €
  - Braunvieh a.Z.: Milchkuh 550 €, Mutterkuh 160 €, Bulle 360 €
  - Altwürttemberger Pferd: Stute 120 €, Hengst 250 €
  - Schwarzwälder Fuchs: Stute 120 €, Hengst 250 €
  - Schwäb. Hällisches: Sau 180 €, Eber 160 €
  - Dt. Edelschwein: Sau 100 €, Eber 100 €
  - Dt. Landrasse: Sau 100 €, Eber 100 €

*Verpflichtungszeitraum.md – erweitert:*
- Neuverpflichtungen ab 2026: 3 Jahre Verpflichtungsdauer (GA - Wichtige Hinweise, S. 2)
- Beginn des Verpflichtungszeitraums je Maßnahmentyp (GA - Erlaeuterungen, S. 50)
- Konsequenzen bei vorzeitiger Kündigung (GA - Erlaeuterungen, S. 50–51)

*Gemeinsamer_Antrag.md – aktualisiert:*
- Fristen 2026: FIONA ab 9. März, Antrag bis 15. Mai (GA - Wichtige Hinweise, S. 1)
- Vorgelagerter Förderantrag entfällt ab 2026 (GA - Wichtige Hinweise, S. 2)
- Kontrollen über App "profil (bw)" (GA - Wichtige Hinweise, S. 1)

*index.md:*
- Neuerungen_2026 als Konzeptseite aufgenommen

**Noch offen:**
- Kapitel 5.5 Öko-Regelungen (S. 38–47) – Detailinfos zu ÖR1–ÖR7
- Kapitel 7.2–7.4 AZL, LPR-A, UZW – aktuell nicht im Wiki-Scope
- Kapitel 17–19 Fristen/Sanktionen/Konditionalität – teilweise Überschneidung mit bestehenden Konditionalitäts-Seiten
- GLÖZ-2 und GLÖZ-6 Änderungen 2026 in die bestehenden Konzeptseiten eintragen

## [2026-04-14] ingest | 4 weitere Konditionalitäts-PDFs

**Quellen:**
- `Soz_Kond_Infobroschuere_2026.pdf` (16 S.) – Soziale Konditionalität
- `Merkblatt_Pflanzenschutzdokumentation.pdf` (4 S.) – PSM-Dokumentation ab 01.01.2026
- `Info_Mindestpraktiken_Bodenbewirtschaftung_zur_Begrenzung_von_Erosion_(GLÖZ_5).pdf` (8 S.) – Erosionsschutz BW-Detail
- `Merkblatt 36_Gewässerrandstreifen in Baden-Württemberg_2024.pdf` (10 S.) – Gewässerrandstreifen BW

**Was & Warum:**
Vier ergänzende Konditionalitäts-Dokumente integriert. Die soziale Konditionalität ist ein komplett neues Thema (seit 2025), das viele Landwirte mit Angestellten nicht kennen. PSM-Dokumentation konkretisiert die ab 2026 geltenden erweiterten Aufzeichnungspflichten. GLÖZ-5-Detail liefert die BW-spezifische Einstufungs-Methodik und gleichwertigen Maßnahmen. Gewässerrandstreifen-Merkblatt enthält die Praxisdetails für die häufigste Frage: "Was darf ich am Bach noch machen?"

**Änderungen mit Quellennachweis:**

*GAB_7_8_Pflanzenschutz.md – Abschnitt Aufzeichnungspflicht erweitert:*
- Pflichtangaben-Tabelle mit EPPO-Codes, BBCH, Zulassungsnummer etc. (Merkblatt_Pflanzenschutzdokumentation.pdf, S. 1–3)
- Lage-Angaben differenziert: GA-Fläche (UD-Nr./Schlagnr./FLIK) vs. Nicht-GA (GPS) (Merkblatt_Pflanzenschutzdokumentation.pdf, S. 2)
- Uhrzeit-Pflicht nur bei zeitbeschränkter Zulassung, nur Freiland (Merkblatt_Pflanzenschutzdokumentation.pdf, S. 2)
- PSM-DOK (www.psmdok.de) als kostenfreies BW-Dokumentationstool (Merkblatt_Pflanzenschutzdokumentation.pdf, S. 3–4)

*GLOEZ_5_Erosionsschutz.md – grundlegend erweitert:*
- K/S/R-Faktor-Berechnung und Datengrundlagen (Info_GLÖZ_5.pdf, S. 1–2)
- Flächenanteil-Berechnung mit Formel und Schwellenwerten (Info_GLÖZ_5.pdf, S. 2–3)
- FIONA-GIS-Layer für Wasser- und Winderosion (Info_GLÖZ_5.pdf, S. 2, 4)
- Gleichwertige Maßnahmen detailliert mit Definitionen (Info_GLÖZ_5.pdf, S. 5–8)
- Frühe-Sommerkulturen-Liste nach Anlage 5 GAPKondV (Info_GLÖZ_5.pdf, S. 8)
- Begriffserläuterungen: Reihenkultur, raue Winterfurche (Info_GLÖZ_5.pdf, S. 8)

**Korrekturen:**
- GLOEZ_5: KWasser2 gleichwertige Maßnahmen – "1. Dezember bis 15. Januar" war falsch, korrigiert zu "1. Dezember bis 15. Februar" (belegt durch Info_GLÖZ_5.pdf, S. 5 und Kond_Infobroschuere_2026.pdf, S. 12)

**Strukturelle Änderungen:**
- `wiki/Konzepte/Soziale_Konditionalitaet.md` neu erstellt
- `wiki/Konzepte/Gewaesserrandstreifen_BW.md` neu erstellt
- `wiki/Konzepte/Konditionalitaet.md` um Abschnitt "Soziale Konditionalität" ergänzt
- `wiki/Konzepte/GLOEZ_4_Pufferstreifen.md` um Querverweis auf Gewässerrandstreifen erweitert
- `wiki/index.md` um neue Konzeptseiten ergänzt

## [2026-04-14] health-check | Visueller PDF-Abgleich (Stichprobe)

**Geprüfte Maßnahmen:** B1.2, C1, E6 (zufällige Auswahl aus verschiedenen Kategorien)

**Methodik:** PDF-Seiten aus `FAKT_II_Broschuere.pdf` als Bilder gerendert (pdftoppm, 200 dpi) und visuell gegen Wiki-Seiten abgeglichen.

**Ergebnis:**
- **B1.2 Extensive Grünland** (PDF S. 1–2): Alle Angaben korrekt – Fördersatz (150 €/ha), Voraussetzungen (0,3 RGV/ha), alle 6 Auflagen vollständig
- **C1 Streuobst** (PDF S. 5): Alle Angaben korrekt – Fördersatz (5,00 €/Baum), Grenzen (100/200/250 Bäume), Stammhöhe, Ersatzpflicht, abgestorbene Bäume
- **E6 Pheromoneinsatz** (PDF S. 12): Alle Angaben korrekt – Fördersatz (100 €/ha), Erwerbsobstanlagen, Wicklerart, Kaufbelege, Teilzeitraum-Regelung

**Befunde:** Keine Abweichungen festgestellt. Wiki gibt die PDF-Inhalte korrekt wieder.

**Nicht geprüft:** Kombinations-Links (Quelle: Excel), Öko-Regelungen (Quelle: Broschüre 1/2), Konditionalitäts-Verknüpfungen.

## [2026-04-14] ingest | Konditionalität – Kond_Infobroschuere_2026.pdf

**Quelle:** `Kond_Infobroschuere_2026.pdf` (76 S.), gesplittet in 6 Kapitel-PDFs via `scripts/split_kond_info.sh`

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

**Quelle:** `Nutzcodeliste für FAKT II-Förderantrag_2026.pdf` (1 S.)

**Erstellt:**
- `wiki/Nutzcodeliste.md` – Zuordnung Nutzcode → zulässige FAKT-Maßnahmen (B1.2, B3.2, B4, B5, E7, E8, E14)

**Aktualisiert:**
- 7 Maßnahmen-Seiten: Link auf [[Nutzcodeliste]] ergänzt
- `wiki/index.md`: Nutzcodeliste aufgenommen

## [2026-04-13] refactor | Kombinations-Links angereichert + Schema erstellt

**Quelle:** `Kombinationstabelle FAKT II.xlsx` (Stand 24.10.2025), Fußnoten Zeilen 48–51

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
- `FAKT_II_Broschuere.pdf` (8 S.) – Gesamtbroschüre mit Einführung, Antragstellung
- `FAKT_II_Broschuere.pdf` (2 S.) – Maßnahmenübersicht mit Fördersätzen
- `FAKT_II_Broschuere.pdf` (37 S.) – Detaillierte Kurzbeschreibungen aller Maßnahmen
- `Kombinationstabelle FAKT II.xlsx` – Kombinierbarkeitsmatrix

**Erstellt:**
- 34 Maßnahmen-Seiten (A2–G7)
- 7 Kategorie-Seiten (A–G)
- 5 Konzept-Seiten (RGV, Konditionalität, Öko-Regelungen, Verpflichtungszeitraum, Gemeinsamer Antrag)
- 1 Überblicksseite (FAKT II Gesamtübersicht)
- 1 Kombinationstabelle (Zusammenfassung)
- 1 Index
- Vernetzung über Wikilinks zwischen Maßnahmen, Kategorien und Konzepten
