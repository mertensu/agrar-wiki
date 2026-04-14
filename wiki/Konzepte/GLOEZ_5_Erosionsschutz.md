---
type: konzept
titel: "GLÖZ 5 – Mindestpraktiken Erosionsschutz"
---

# GLÖZ 5: Mindestpraktiken der Bodenbewirtschaftung zur Begrenzung von Erosion

Die Anforderungen richten sich nach dem Grad der Erosionsgefährdung der Flächen. Die Einteilung wird im Gemeinsamen Antrag / FIONA mitgeteilt.

**Ausnahme:** Betriebe ≤10 ha sind von Kontrollen und Sanktionen befreit (Verpflichtungen gelten weiterhin). (Quelle: Info_Mindestpraktiken_Bodenbewirtschaftung_zur_Begrenzung_von_Erosion_(GLÖZ_5).pdf, S. 1)

## Erosionsgefährdungsklassen

### Wassererosion

| Klasse | Bedeutung |
|--------|-----------|
| KWasser1 | Erosionsgefährdung |
| KWasser2 | Hohe Erosionsgefährdung |

### Winderosion

| Klasse | Bedeutung |
|--------|-----------|
| KWind | Erosionsgefährdung |

(Quelle: Info_Mindestpraktiken_Bodenbewirtschaftung_zur_Begrenzung_von_Erosion_(GLÖZ_5).pdf, S. 1)

## Einstufung der Flächen (BW-spezifisch)

### Wassererosion – Berechnung

Die Einstufung erfolgt anhand von drei Faktoren (Anlehnung an DIN 19708):

| Faktor | Beschreibung | Datengrundlage |
|--------|-------------|----------------|
| **K-Faktor** (Bodenerodierbarkeit) | Erosionsanfälligkeit des Bodens | Bodenschätzung / ALKIS |
| **S-Faktor** (Hangneigung) | Neigung des Geländes | Digitales Geländemodell (DGM), 5×5 m Raster |
| **R-Faktor** (Regenerosivität) | Intensität/Menge erosionswirksamer Niederschläge | RADKLIM (DWD), 1×1 km Raster, Messdaten 2001–2017, je Gemarkung gemittelt |

**Änderung ab GAP 2023:** Der R-Faktor ist nun verpflichtend, was zu einer **deutlichen Zunahme** erosionsgefährdeter Flächen führt.

(Quelle: Info_Mindestpraktiken_Bodenbewirtschaftung_zur_Begrenzung_von_Erosion_(GLÖZ_5).pdf, S. 1–2)

### Zuordnung zum Schlag

Die Erosionsgefährdung wird je 5×5 m Rasterzelle berechnet (unabhängig von Flurstücksgrenzen). Die Zuordnung zum Schlag erfolgt automatisch in FIONA-GIS über den **flächengewichteten Mittelwert**:

**Formel:**
Flächenanteil ohne Gefährdung × 0 + Flächenanteil KWasser1 × 1 + Flächenanteil KWasser2 × 2

| Ergebnis | Zuordnung |
|----------|-----------|
| < 0,5 | Keine Wassererosionsgefährdung |
| ≥ 0,5 und < 1,5 | **KWasser1** |
| ≥ 1,5 | **KWasser2** |

**Wichtig:** Die Bewertung bezieht sich immer auf den **gesamten Schlag** – alle Teilschläge mit derselben Schlagnummer werden einheitlich bewertet.

**FIONA-GIS-Layer:**
- Karten > Umweltdaten > „GLÖZ 5 Erosionsgefährdung Wasser" → Einzelne 5×5 m Rasterflächen
- Karten > Umweltdaten > „GLÖZ 5 Wassererosionsgefährdungsklasse Schlag" → Gelb = KWasser1, Rot = KWasser2, keine Schraffierung = keine Gefährdung

(Quelle: Info_Mindestpraktiken_Bodenbewirtschaftung_zur_Begrenzung_von_Erosion_(GLÖZ_5).pdf, S. 2–4)

### Winderosion – Einstufung

Flurstücksbezogen nach DIN 19706. Faktoren: Bodenerodierbarkeit, Windgeschwindigkeit, Schutzwirkung von Windhindernissen. In BW spielt Winderosion eine vergleichsweise untergeordnete Rolle.

**FIONA-GIS:** Karten > Gebietskulissen > „GLÖZ 5 Erosionskulisse KWind"

(Quelle: Info_Mindestpraktiken_Bodenbewirtschaftung_zur_Begrenzung_von_Erosion_(GLÖZ_5).pdf, S. 4)

## Grundregeln

### KWasser1

- **Pflugverbot:** 1. Dezember bis 15. Februar
- Pflügen nach Ernte der Vorfrucht nur bei Aussaat vor 1. Dezember

### KWasser2 (strenger)

- **Pflugverbot:** 1. Dezember bis 15. Februar
- Pflügen 16. Februar bis 30. November nur bei **unmittelbar folgender Aussaat** (spätester Zeitpunkt: 30. November)
- **Reihenkulturen ≥45 cm Reihenabstand:** Pflügen grundsätzlich verboten

### KWind

- Pflügen nur bei Aussaat vor 1. März
- Ab 1. März nur bei unmittelbar folgender Aussaat (nicht bei Reihenkulturen ≥45 cm, außer: Grünstreifen ≥2,5 m alle 100 m quer zur Hauptwindrichtung, Agroforstsystem quer zur Hauptwindrichtung, Dämme quer zur Hauptwindrichtung, oder unmittelbares Setzen von Jungpflanzen)

**Andere Bodenbearbeitungsformen** (Grubber, Scheibenegge, Kreiselegge, Fräse, Hacke, Striegel) sind auf erosionsgefährdeten Flächen **nicht eingeschränkt**.

(Quelle: Info_Mindestpraktiken_Bodenbewirtschaftung_zur_Begrenzung_von_Erosion_(GLÖZ_5).pdf, S. 5; Kond_Infobroschuere_2026.pdf, S. 12–13)

## Gleichwertige Erosionsschutzmaßnahmen (BW)

In BW wird der Pflugeinsatz auf KWasser1- und KWasser2-Flächen ermöglicht, sofern gleichwertige Erosionsschutzmaßnahmen erbracht werden.

### KWasser1: Pflügen im Verbotszeitraum erlaubt bei

Bewirtschaftung quer zum Hang **oder** eine der folgenden Maßnahmen:

1. Anlage von Erosionsschutzstreifen
2. Raue Winterfurche mit nachfolgender früher Sommerkultur
3. Rasenbildende Kultur als Vorfrucht
4. Abdecken der Fläche
5. Pflugfurche auf schweren Böden (≥17% Ton)

### KWasser2: Pflügen im Verbotszeitraum erlaubt bei

Bewirtschaftung quer zum Hang **und** zusätzlich eine der folgenden Maßnahmen:

1. Anlage von Erosionsschutzstreifen **(sollte priorisiert werden)**
2. Raue Winterfurche mit nachfolgender früher Sommerkultur
3. Rasenbildende Kultur als Vorfrucht
4. Abdecken der Fläche
5. Pflugfurche auf schweren Böden (≥17% Ton)

**Reihenkulturen ≥45 cm auf KWasser2:** Pflügen zulässig bei quer zum Hang **und** zusätzlich Maßnahme 1, 3, 4 oder 5 (nicht raue Winterfurche).

(Quelle: Info_Mindestpraktiken_Bodenbewirtschaftung_zur_Begrenzung_von_Erosion_(GLÖZ_5).pdf, S. 5–6)

### Definitionen der Maßnahmen

**Erosionsschutzstreifen** (bei Schlägen >0,6 ha):
- ≥6 m breit, überwiegend quer zur Haupthangrichtung
- Einsaat mit winterharter Kultur, Reihenabstand <45 cm, spätestens bis 30. November
- Mindestens 10% der Schlagfläche
- Lage: Nicht in den oberen oder unteren 20% des Schlags (dort keine gute Schutzwirkung)
- Bodenbearbeitung im Streifen frühestens ab Reihenschluss der Hauptkultur
- Gewässerrandstreifen nach § 29 WG BW nicht als Erosionsschutzstreifen anrechenbar
- Direktsaat der Hauptkultur in den Streifen zulässig (keine flächige Bodenbearbeitung)
- Schläge ≤0,6 ha: Anlage möglich aber nicht zwingend (kleine Flächen erfüllen Zielvorgabe eigenständig)

**Raue Winterfurche + frühe Sommerkultur:**
- Pflugfurche darf nicht vor 16. Februar bearbeitet werden
- Danach Anbau einer frühen Sommerkultur (Reihenabstand <45 cm)

**Rasenbildende Kultur als Vorfrucht:**
- Klee, Luzerne, Ackergras, Esparsette, Serradella (Rein-/Mischsaat), neues Grünland, Grünlandeinsaaten
- Muss mindestens **6 Monate** vor Pflugeinsatz ausgesät sein

**Abdecken der Fläche:**
- Folie, Vlies, engmaschiges Netz oder gleichwertig
- Unmittelbar nach Aussaat/Pflanzung
- Muss bis Reihenschluss auf der Fläche verbleiben

**Pflugfurche auf schweren Böden:**
- Schwere Böden nach Anlage 6 GAPKondV und ≥17% Tongehalt (Kartenebene „schwere Böden GLÖZ 6" in FIONA)
- Feldoberfläche wird bis 15. Februar grob gehalten, gefolgt vom Anbau einer Sommerkultur
- Fördert Frostgare (Gefrieren/Auftauen)

(Quelle: Info_Mindestpraktiken_Bodenbewirtschaftung_zur_Begrenzung_von_Erosion_(GLÖZ_5).pdf, S. 6–8)

### Frühe Sommerkulturen (Anlage 5 GAPKondV)

Aussaat/Pflanzung zum frühestmöglichen Zeitpunkt nach guter fachlicher Praxis:

- Sommergetreide (ohne Mais und Hirse)
- Leguminosen (ohne Sojabohnen)
- Sonnenblumen, Sommerraps, Sommerrüben, Körnersenf, Körnerhanf, Leindotter, Lein, Mohn
- Heil-/Duft-/Gewürzpflanzen, Küchenkräuter, Faserhanf, Buchweizen, Amaranth, Quinoa
- Kleegras, Klee-/Luzernegras-Gemisch, Ackergras, Grünlandeinsaat
- Kartoffeln, Rüben, Gemüsekulturen

(Quelle: Info_Mindestpraktiken_Bodenbewirtschaftung_zur_Begrenzung_von_Erosion_(GLÖZ_5).pdf, S. 8)

## Ausnahmen für Öko-Betriebe

Für nach VO (EU) 2018/848 zertifizierte Betriebe (ab 2025):

- **Frühe Sommerkulturen (keine Reihenkulturen)** auf KWasser1 und KWasser2: Raue Winterfurche zulässig
- **Sommer-Reihenkulturen** auf KWasser2: Pflügen nur mit vorhergehender Winterzwischenfrucht (auch als Untersaat) und Pflügen unmittelbar vor Einsaat

(Quelle: Info_Mindestpraktiken_Bodenbewirtschaftung_zur_Begrenzung_von_Erosion_(GLÖZ_5).pdf, S. 5; Kond_Infobroschuere_2026.pdf, S. 12–13)

## Begriffserläuterungen

- **Reihenkultur** (§ 16 GAPKondV): Kultur mit Reihenabstand ≥45 cm
- **Raue Winterfurche** (§ 16 GAPKondV): Durch Pflügen im Spätherbst/Winter hergestellte, grob strukturierte Feldoberfläche, die ohne jede weitere Bearbeitung mindestens bis zum Ablauf des 15. Februar vorhanden sein muss

(Quelle: Info_Mindestpraktiken_Bodenbewirtschaftung_zur_Begrenzung_von_Erosion_(GLÖZ_5).pdf, S. 8)

## Praxishinweis

Auf Böden mit hohem Schluffanteil (Lössgebiete) mindern die gleichwertigen Maßnahmen die Erosion, verhindern sie aber nicht vollständig. Verfahren der **Mulch- und Direktsaat** werden weiterhin dringend empfohlen, soweit betrieblich möglich. (Quelle: Info_Mindestpraktiken_Bodenbewirtschaftung_zur_Begrenzung_von_Erosion_(GLÖZ_5).pdf, S. 6)

## Relevante FAKT II-Maßnahmen

- [[F4_Strip_Till|F4 Strip Till]] – Reduzierte Bodenbearbeitung (geht über GLÖZ 5 hinaus)
- [[E1.2_Begruenungsmischungen|E1.2]] – Begrünungsmischungen (Erosionsschutz als Nebeneffekt)
- [[D2_Oekolandbau_Beibehaltung|D2]] – Ökolandbau (besondere Ausnahmen bei GLÖZ 5)

*Siehe auch: [[Konditionalitaet]], [[GLOEZ_6_Bodenbedeckung]], [[Gewaesserrandstreifen_BW]]*

---
*Quellen: Info Mindestpraktiken Bodenbewirtschaftung zur Begrenzung von Erosion (GLÖZ 5), MLR BW, Stand 23.04.2025; Informationsbroschüre Konditionalität 2026, S. 12–13*
