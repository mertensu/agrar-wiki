---
type: konzept
titel: Flächenangaben, Schlagdefinition und Landschaftselemente
created: '2026-04-16'
updated: '2026-04-16'
sources:
- GA - Erlaeuterungen und Ausfuellhinweise 2026.pdf
tags:
- wasserschutz
- biodiversitaet
- landschaftselement
- konditionalitaet
- oekoregelung
---

# Flächenangaben, Schlagdefinition und Landschaftselemente

## Schlag und Teilschlag

Ein **Schlag** ist eine zusammenhängende landwirtschaftliche Fläche mit einem einheitlichen Nutzcode, digitalisiert in FIONA-GIS. Jeder Schlag erhält eine Schlagnummer.

Ein **Teilschlag** entsteht, wenn für Teile eines Schlags abweichende Angaben gemacht werden (z.B. andere Maßnahmen). Teilschläge werden im FIONA-GIS separat digitalisiert. (Quelle: GA - Erlaeuterungen und Ausfuellhinweise 2026.pdf, S. 18)

Teilschlagbildung ist **zwingend erforderlich** bei:
- ÖR 1b und ÖR 1c (Blühstreifen/-flächen)
- ÖR 1d (Altgrasstreifen/-flächen)
- ÖR 6 auf Flächen mit Gewässerrandstreifen nach § 38a WHG
- Streifenförmige Agroforstsysteme (Gehölzstreifen)
- K-LE auf Flächen mit ÖR 1a, ÖR 1d oder Agri-PV (als NC 040)

(Quelle: GA - Erlaeuterungen und Ausfuellhinweise 2026.pdf, S. 18)

## Bruttofläche Landwirtschaft

Die **Bruttofläche Landwirtschaft** ist die maximal förderfähige landwirtschaftliche Fläche einschließlich förderfähiger Landschaftselemente. Sie ist in FIONA-GIS über den Reiter "Karten" einblendbar. (Quelle: GA - Erlaeuterungen und Ausfuellhinweise 2026.pdf, S. 18)

Zur landwirtschaftlichen Fläche gehören: Ackerland, Dauerkulturen und Dauergrünland.

**Wegflurstücke** (Flurstücke, die im Wesentlichen aus Wegeflächen bestehen) sind als Ganzes nicht förderfähig – auch nicht die unbefestigten Teilflächen, es sei denn, diese sind bereits als Bruttofläche Landwirtschaft ausgewiesen (Bestandsschutz). (Quelle: GA - Erlaeuterungen und Ausfuellhinweise 2026.pdf, S. 19)

## Landschaftselemente (LE) und förderfähige Fläche

### K-LE (Konditionalitäts-Landschaftselemente)

K-LE sind die unter [[GLOEZ_8_Landschaftselemente|GLÖZ 8]] geschützten Landschaftselemente (Hecken ≥10 m, Feldgehölze 50–2.000 m², Baumreihen ≥5 Bäume/≥50 m etc.).

**Grundregel:** K-LE können für alle landwirtschaftlichen Fördermaßnahmen (außer AZL) in die förderfähige Fläche einbezogen werden – auch wenn der Anteil auf der beantragten Fläche die Mindestgröße des K-LE unterschreitet. (Quelle: GA - Erlaeuterungen und Ausfuellhinweise 2026.pdf, S. 21)

**Ausnahme ÖR 1a und ÖR 1d:** Hier müssen K-LE als eigene Teilschläge digitalisiert werden und zählen **nicht** zur begünstigungsfähigen Fläche. (Quelle: GA - Erlaeuterungen und Ausfuellhinweise 2026.pdf, S. 18)

### Andere LE (unterhalb der K-LE-Schwellenwerte)

Folgende kleinere Landschaftselemente können ebenfalls als Teil der Schlagfläche beantragt werden, ohne separat im FIONA-GIS gezeichnet werden zu müssen:

| Element | Schwellenwert |
|---------|--------------|
| Hecken/Knicks | unter 10 m Länge |
| Feldgehölze | unter 50 m² |
| Trocken-/Natursteinmauern, Lesesteinwälle | unter 5 m Länge |
| Feldraine | bis 2 m Durchschnittsbreite |
| Gräben | (kein Schwellenwert) |
| Einzelbäume inkl. Baumreihen | (kein Schwellenwert) |
| Sträucher/Strauchgruppen | bis 500 m² |
| Hochstaudenfluren | bis 500 m² |

(Quelle: GA - Erlaeuterungen und Ausfuellhinweise 2026.pdf, S. 21)

**25%-Regel:** Andere LE zählen nur dann zur förderfähigen Fläche, wenn sie **in Summe höchstens 25 %** der Fläche des landwirtschaftlichen Schlages einnehmen. Wird die 25%-Grenze überschritten, sind die betroffenen Flächenanteile nicht mehr Teil der Bruttofläche und die Schlagabgrenzung muss angepasst werden. (Quelle: GA - Erlaeuterungen und Ausfuellhinweise 2026.pdf, S. 22)

**Bäume:** Je Baum werden 10 m² angerechnet. Bei Flächen ohne weitere LE ergibt das eine maximale Standdichte von **250 Bäumen/ha** (bei Überschreitung → nicht mehr förderfähig als landwirtschaftliche Fläche). (Quelle: GA - Erlaeuterungen und Ausfuellhinweise 2026.pdf, S. 22)

### Voraussetzungen für LE-Einbeziehung

Für beide LE-Typen (K-LE und andere LE) gilt:
- **Unmittelbarer räumlicher Zusammenhang** zur landwirtschaftlich genutzten Fläche (auf oder direkt angrenzend)
- Teil der Betriebsfläche der antragstellenden Person
- Der **landwirtschaftliche Charakter** der Fläche muss im Vordergrund stehen (überwiegend landwirtschaftliche Nutzung)
- Flächenhafte Feldgehölze/Baumgruppen nur als LE einbeziehbar, wenn sie **isoliert** stehen und nicht unmittelbar an Waldflächen angrenzen

(Quelle: GA - Erlaeuterungen und Ausfuellhinweise 2026.pdf, S. 22)

### Bedeutung für die Schlaggröße

Die Schlaggröße (= Antragsfläche) umfasst die im FIONA-GIS digitalisierte Fläche einschließlich einbezogener LE. Das heißt: **Landschaftselemente am Rand eines Schlags, die die Voraussetzungen erfüllen, zählen zur Schlaggröße dazu** – sie werden nicht abgezogen. Dies ist relevant für größenabhängige Maßnahmen wie [[A3_Kleine_Strukturen|A3 Kleine Strukturen]] (Schläge ≤0,5 ha).

## Agri-Photovoltaik (Agri-PV)

Landwirtschaftliche Flächen mit Agri-PV-Anlagen können förderfähig sein, wenn folgende Bedingungen erfüllt sind:

- **DIN SPEC 91434:2021-05** muss eingehalten werden
- Die Agri-PV-Anlage darf die landwirtschaftliche Fläche um **max. 15 %** reduzieren
- Die restliche Fläche muss mit üblichen Methoden, Maschinen und Geräten bewirtschaftbar bleiben
- Nur die **tatsächlich landwirtschaftlich nutzbare Fläche** ist förderfähig
- K-LE auf Agri-PV-Flächen zählen **nicht** zur landwirtschaftlich nutzbaren Fläche und müssen als eigener Teilschlag (NC 040) abgegrenzt werden
- Nicht nutzbare Fläche im Sinne der DIN SPEC muss per "Loch zeichnen" aus der Schlaggeometrie herausgenommen werden

(Quelle: GA - Erlaeuterungen und Ausfuellhinweise 2026.pdf, S. 21)

**Formen von Agroforstsystemen** (keine Agri-PV, aber verwandt):
- **Streifenförmig:** mind. 2 Gehölzstreifen, max. 40 % der Schlagfläche
- **Verstreut:** 50–200 Gehölzpflanzen je ha

LE und KUP (Niederwald mit Kurzumtrieb) gelten **nicht** als Agroforstsystem. Streuobstwiesen benötigen keine Agroforst-Kennzeichnung. (Quelle: GA - Erlaeuterungen und Ausfuellhinweise 2026.pdf, S. 19)

## Obstbäume – Abgrenzung Streuobst vs. Dauerkultur

Siehe auch [[C1_Streuobst|C1 Streuobst]].

| Kriterium | Streuobstwiese (Grünland) | Intensivobstanlage (Dauerkultur) |
|-----------|--------------------------|--------------------------------|
| **Baumbestand** | ≤330 Bäume/ha | >330 Bäume/ha |
| **Nutzcode** | NC 451 (Wiese), NC 481 (Streuobst ohne Wiesennutzung) | NC 821 (Kern-/Steinobst), NC 825 (Kernobst), NC 826 (Steinobst) |
| **Primärnutzung** | Futtererzeugung (HFF), Obst als Nebennutzung | Obsterzeugung |

**Ausnahme:** Bis zu 330 Bäume/ha können als Intensivobstanlage eingestuft werden, wenn:
- Intensiv genutzte Steinobst-/Schalenobst-Anlage (NC 826), oder
- Intensiv genutzte Wirtschaftsobstanlage Kernobst (200–330 Bäume/ha)
- Anlagentypischer Baumschnitt, gepflegtes Erscheinungsbild, kein Zweinutzungssystem

(Quelle: GA - Erlaeuterungen und Ausfuellhinweise 2026.pdf, S. 22)

## Relevante FAKT II-Maßnahmen

- [[A3_Kleine_Strukturen|A3 Kleine Strukturen]] – Schlaggrößen-Obergrenze 0,5 ha; LE-Einbeziehung beeinflusst, ob ein Schlag förderfähig ist
- [[C1_Streuobst|C1 Streuobst]] – Abgrenzung Streuobst vs. Dauerkultur
- [[E7_Bluehflaechen|E7 Blühflächen]] – Teilschlagbildung bei Kombination mit ÖR 1b

---
*Quelle: GA - Erlaeuterungen und Ausfuellhinweise 2026.pdf, S. 17–22 (Stand Februar 2026)*
