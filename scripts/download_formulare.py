#!/usr/bin/env python3
"""
Download alle PDFs/Excel-Dateien von der GA-Formularseite BW.
Erstellt eine Übersichts-Markdown-Datei mit Links zu den lokalen Dateien.

Quelle: https://foerderung.landwirtschaft-bw.de/,Lde/Startseite/Gemeinsamer+Antrag/Formulare+_+Merkblaetter+_+Informationen+zum+Gemeinsamen+Antrag
"""

import os
import urllib.request
import urllib.parse
import time
import sys

BASE = "https://foerderung.landwirtschaft-bw.de/site"
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "downloads", "formulare_2026")

# (section, title, relative_url, filetype)
# relative_url starts with /pbs-bw-rebrush2024/... or is a full URL
DOCUMENTS = [
    # === Allgemein 2026 ===
    ("Allgemein 2026", "Gemeinsamer Antrag 2026: Start in Antragssaison – 20 Jahre FIONA",
     "/pbs-bw-rebrush2024/get/documents_E-623649228/MLR.LEL/PB5Documents/fiona/2026/Pressemitteilungen/Pressemitteilung_FIONA_Start_2026.pdf", "pdf"),

    # === Allgemeines zum Gemeinsamen Antrag 2026 ===
    ("Gemeinsamer Antrag 2026 > Allgemeines", "GA - Erläuterungen und Ausfüllhinweise zum Gemeinsamen Antrag 2026",
     "/pbs-bw-rebrush2024/get/documents_E1610400717/MLR.LEL/PB5Documents/fiona/2026/Merkblaetter/GA%20-%20Erlaeuterungen%20und%20Ausfuellhinweise%202026.pdf", "pdf"),
    ("Gemeinsamer Antrag 2026 > Allgemeines", "GA - Wichtige Informationen zum Gemeinsamen Antrag 2026",
     "/pbs-bw-rebrush2024/get/documents_E73965132/MLR.LEL/PB5Documents/fiona/2026/Merkblaetter/GA%20-%20Wichtige%20Hinweise%20zum%20GA%202026.pdf", "pdf"),
    ("Gemeinsamer Antrag 2026 > Allgemeines", "GA - Nutzcodeliste 2026",
     "/pbs-bw-rebrush2024/get/documents_E1299865769/MLR.LEL/PB5Documents/fiona/2026/Merkblaetter/GA%20-%20Nutzcodeliste%202026.pdf", "pdf"),
    ("Gemeinsamer Antrag 2026 > Allgemeines", "GA – Nutzcodeliste für die Beantragung Erschwernisausgleich Pflanzenschutz 2026",
     "/pbs-bw-rebrush2024/get/documents_E-1266267685/MLR.LEL/PB5Documents/fiona/2026/Merkblaetter/NC-Liste_fuer_Beantragung_Erschwernisausgleich_Pflanzenschutz.pdf", "pdf"),
    ("Gemeinsamer Antrag 2026 > Allgemeines", "GA - Infoblatt FFH-Mähwiesen",
     "/pbs-bw-rebrush2024/get/documents_E814910130/MLR.LEL/PB5Documents/fiona/2026/Merkblaetter/GA%20-%20Infoblatt%20Maehwiesen%20fuer%202026.pdf", "pdf"),
    ("Gemeinsamer Antrag 2026 > Allgemeines", "GA - Informationen zum Datenschutz",
     "/pbs-bw-rebrush2024/get/documents_E1436408410/MLR.LEL/PB5Documents/fiona/2026/Merkblaetter/GA%20-%20Informationen%20zum%20Datenschutz%202026.pdf", "pdf"),

    # === Beratung ===
    ("Gemeinsamer Antrag 2026 > Beratung", "Infoblatt: Beratung.Zukunft.Land.- Beratungsmodule für Landwirtschaft, Gartenbau und Weinbau in BW",
     "/pbs-bw-rebrush2024/get/documents_E-273824787/MLR.LEL/PB5Documents/mlr/GA/GA_026_extern/Beratung/Flyer_BZL_Modulberatung.pdf", "pdf"),
    ("Gemeinsamer Antrag 2026 > Beratung", "Infoblatt: Der Betriebs-Check für Landwirtschaft, Gartenbau und Weinbau in BW",
     "/pbs-bw-rebrush2024/get/documents_E-1770350688/MLR.LEL/PB5Documents/mlr/GA/GA_026_extern/Beratung/Flyer_BC_BetriebsCheck.pdf", "pdf"),

    # === UZW ===
    ("Gemeinsamer Antrag 2026 > Umweltzulage Wald", "UZW Auerhuhn - Handlungsempfehlungen für die Forstwirtschaft und Jagd ab 2023",
     "/pbs-bw-rebrush2024/get/documents_E-578997485/MLR.LEL/PB5Documents/fiona/2026/Merkblaetter/UZW-Auerhuhn_Handlungsempfehlung_Waldarbeit.pdf", "pdf"),

    # === Konditionalität ===
    ("Gemeinsamer Antrag 2026 > Konditionalität", "Informationsbroschüre Konditionalität 2026",
     "/pbs-bw-rebrush2024/get/documents_E808563796/MLR.LEL/PB5Documents/fiona/2026/Merkblaetter/Kond_Infobroschuere_2026.pdf", "pdf"),
    ("Gemeinsamer Antrag 2026 > Konditionalität", "Informationsbroschüre soziale Konditionalität 2026",
     "/pbs-bw-rebrush2024/get/documents_E-420409930/MLR.LEL/PB5Documents/fiona/2026/Merkblaetter/Soz_Kond_Infobroschuere_2026.pdf", "pdf"),
    ("Gemeinsamer Antrag 2026 > Konditionalität", "Information zu Mindestpraktiken der Bodenbewirtschaftung (GLÖZ 5)",
     "/pbs-bw-rebrush2024/get/documents_E2085734829/MLR.LEL/PB5Documents/fiona/2026/Merkblaetter/Info_Mindestpraktiken_Bodenbewirtschaftung_zur_Begrenzung_von_Erosion_%28GL%C3%96Z_5%29.pdf", "pdf"),
    ("Gemeinsamer Antrag 2026 > Konditionalität", "Merkblatt 36: Gewässerrandstreifen (LTZ Augustenberg)",
     "/pbs-bw-rebrush2024/get/documents_E1637300481/MLR.LEL/PB5Documents/ltz_ka/Service/Schriftenreihen/Merkblatt%20f%C3%BCr%20die%20Umweltgerechte%20Landbewirtschaftung/Merkblatt-Gew%C3%A4sserrandstreifen_DL/Merkblatt%2036_Gew%C3%A4sserrandstreifen%20in%20Baden-W%C3%BCrttemberg_2024.pdf", "pdf"),
    ("Gemeinsamer Antrag 2026 > Konditionalität", "Merkblatt Dokumentation Pflanzenschutzanwendungen ab 01.01.2026 (LTZ)",
     "https://ltz.landwirtschaft-bw.de/site/pbs-bw-mlr-root/get/documents_E-805393053/MLR.LEL/PB5Documents/ltz_ka/Arbeitsfelder/Pflanzenschutz/Rechtliche%20Vorgaben/Merkblatt_Pflanzenschutzdokumentation.pdf", "pdf"),

    # === Direktzahlungen ===
    ("Gemeinsamer Antrag 2026 > Direktzahlungen", "Nachweis und Merkblatt Agri-Photovoltaik",
     "/pbs-bw-rebrush2024/get/documents_E-1418936225/MLR.LEL/PB5Documents/fiona/2026/Merkblaetter/Nachweis_und_Merkblatt_Agri-Photovoltaik.pdf", "pdf"),
    ("Gemeinsamer Antrag 2026 > Direktzahlungen", "Nachweis der Gehölzarten im Agroforstsystem",
     "/pbs-bw-rebrush2024/get/documents_E-967632648/MLR.LEL/PB5Documents/fiona/2026/Merkblaetter/Nachweis_der_Gehoelzarten_im_Agroforstsystem.pdf", "pdf"),

    # === Öko-Regelungen ===
    ("Gemeinsamer Antrag 2026 > Öko-Regelungen", "Ergänzende Informationen zu ÖR1b, ÖR1c, ÖR2 und ÖR5",
     "/pbs-bw-rebrush2024/get/documents_E485303700/MLR.LEL/PB5Documents/mlr/GA/GA_026_extern/OER/Ergaenzende_Informationen_zu_den_Oeko-Regelungen.pdf", "pdf"),
    ("Gemeinsamer Antrag 2026 > Öko-Regelungen", "Nachweis der Kennarten ÖR5 und FAKT II B3.2",
     "/pbs-bw-rebrush2024/get/documents_E1754315346/MLR.LEL/PB5Documents/mlr/GA/GA_026_extern/OER/Nachweis_Kennarten%20_OER%205_FAKT_II_B3.2.pdf", "pdf"),
    ("Gemeinsamer Antrag 2026 > Öko-Regelungen", "ÖR1a - Neuerungen 2026 für Weinbaubetriebe",
     "/pbs-bw-rebrush2024/get/documents_E-1163093124/MLR.LEL/PB5Documents/mlr/GA/GA_026_extern/OER/OER1a_Neuerungen_2026_f%C3%BCr_Weinbaubetriebe.pdf", "pdf"),
    ("Gemeinsamer Antrag 2026 > Öko-Regelungen", "Nachweis Wiederbepflanzungsgenehmigung ÖR1a Weinbau 2026",
     "/pbs-bw-rebrush2024/get/documents_E-1581347744/MLR.LEL/PB5Documents/mlr/GA/GA_026_extern/OER/Nachweis_Wiederbepflanzungsgenehmigung.pdf", "pdf"),
    ("Gemeinsamer Antrag 2026 > Öko-Regelungen", "Merkblatt 40: ÖR1a-Brachflächen gestalten / Hinweise ÖR1b (LTZ Augustenberg)",
     "/pbs-bw-rebrush2024/get/documents_E-1540869266/MLR.LEL/PB5Documents/ltz_ka/Service/Schriftenreihen/Merkblatt%20f%C3%BCr%20die%20Umweltgerechte%20Landbewirtschaftung/Merkblatt%2040%20GL%C3%96Z%208_DL/Merkblatt%2040_%E2%80%9E%C3%96R%201a%E2%80%9C-%20und%20%E2%80%9EGL%C3%96Z%208%E2%80%9C-Brachfl%C3%A4chen.pdf", "pdf"),
    ("Gemeinsamer Antrag 2026 > Öko-Regelungen", "Broschüre LPR-Grünlandmaßnahmen in Kombination mit Öko-Regelungen",
     "/pbs-bw-rebrush2024/get/documents_E-2142117225/MLR.LEL/PB5Documents/mlr/Foerderwegweiser/LPR/2026/Broschuere_LPR-OER-Gruenland_Kombinationsmoeglichkeiten.pdf", "pdf"),
    ("Gemeinsamer Antrag 2026 > Öko-Regelungen", "Saatgutmischungen und Qualitätsvorgaben FAKT II / ÖR1b (LTZ)",
     "/pbs-bw-rebrush2024/get/documents_E1455819265/MLR.LEL/PB5Documents/ltz_ka/Arbeitsfelder/Landwirtschaft_und_Umwelt/Greening%20und%20FAKT/FAKT_DL/Saatgutmischungen%20und%20Qualit%C3%A4tsvorgaben.pdf", "pdf"),

    # === Kennarten ===
    ("Gemeinsamer Antrag 2026 > Kennarten", "Kennarten des artenreichen Grünland - ÖR5 und FAKT II (Broschüre)",
     "/pbs-bw-rebrush2024/get/documents_E-2044795642/MLR.LEL/PB5Documents/lazbw_2024/lazbw_gl/Gr%C3%BCnlandwirtschaft_und_Futterbau/01_Gr%C3%BCnlandbewirtschaftung/01_Artenreiches_Gr%C3%BCnland/05_F%C3%B6rderung/2025_FAKTII_Kennarten_onlineVersion.pdf", "pdf"),
    ("Gemeinsamer Antrag 2026 > Kennarten", "Anleitung Einstufung Flächen ÖR5 und FAKT II",
     "/pbs-bw-rebrush2024/get/documents_E-1815617299/MLR.LEL/PB5Documents/lazbw_2024/lazbw_gl/Gr%C3%BCnlandwirtschaft_und_Futterbau/01_Gr%C3%BCnlandbewirtschaftung/01_Artenreiches_Gr%C3%BCnland/05_F%C3%B6rderung/2025_FAKTII_Artenreiches_Gruenland_Kennarten_8_Seiten.pdf", "pdf"),

    # === GA-Formulare ===
    ("Gemeinsamer Antrag 2026 > GA-Formulare", "GA - Widerruf Einwilligungserklärung",
     "/pbs-bw-rebrush2024/get/documents_E-1852281645/MLR.LEL/PB5Documents/fiona/2026/Formulare/GA%20-%20Widerruf%20Einwilligungserklaerung%202026.pdf", "pdf"),

    # === FAKT II-Informationen 2026 > Merkblätter ===
    ("FAKT II 2026 > Merkblätter", "FAKT II - Broschüre",
     "/pbs-bw-rebrush2024/get/documents_E-2011444163/MLR.LEL/PB5Documents/fiona/2023/Merkblaetter/FAKT%20II-Broschuere.pdf", "pdf"),
    ("FAKT II 2026 > Merkblätter", "FAKT II - Kombinationstabelle (Excel)",
     "/pbs-bw-rebrush2024/get/documents_E1177616672/MLR.LEL/PB5Documents/fiona/2026/Merkblaetter/Kombinationstabelle%20FAKT%20II.xlsx", "xlsx"),
    ("FAKT II 2026 > Merkblätter", "FAKT II - Kombinationstabelle (PDF)",
     "/pbs-bw-rebrush2024/get/documents_E-892471267/MLR.LEL/PB5Documents/fiona/2026/Merkblaetter/Kombinationstabelle%20FAKT%20II.pdf", "pdf"),
    ("FAKT II 2026 > Merkblätter", "FAKT II - Maßnahmen und FAKT-Codes 2026",
     "/pbs-bw-rebrush2024/get/documents_E1564151305/MLR.LEL/PB5Documents/fiona/2026/Merkblaetter/FAKT%20II-Ma%C3%9Fnahmen%20und%20Fakt-Codes%202026.pdf", "pdf"),
    ("FAKT II 2026 > Merkblätter", "FAKT II - Nutzcodeliste für FAKT II-Förderantrag",
     "/pbs-bw-rebrush2024/get/documents_E869622301/MLR.LEL/PB5Documents/fiona/2026/Merkblaetter/Nutzcodeliste%20f%C3%BCr%20FAKT%20II-F%C3%B6rderantrag_2026.pdf", "pdf"),

    # === FAKT II > Übertragung ===
    ("FAKT II 2026 > Übertragung Verpflichtungen", "Formular zur Übertragung von FAKT II-Verpflichtungen",
     "/pbs-bw-rebrush2024/get/documents_E-1635694469/MLR.LEL/PB5Documents/fiona/2026/Formulare/FAKT%20II%20-%20Uebertragung%20von%20FAKT-Verpflichtungen.pdf", "pdf"),

    # === FAKT II B Formulare ===
    ("FAKT II 2026 > B-Formulare", "FAKT II B1.2 - Aufzeichnung Grünlandmaßnahme (Excel)",
     "/pbs-bw-rebrush2024/get/documents_E1798575063/MLR.LEL/PB5Documents/fiona/2026/Formulare/FAKT%20B1.2%20%20-%20Aufzeichnungen%20zu%20den%20Gr%C3%BCnlandma%C3%9Fnahmen%202026.xlsx", "xlsx"),
    ("FAKT II 2026 > B-Formulare", "FAKT II B1.2 - Aufzeichnung Grünlandmaßnahme (PDF)",
     "/pbs-bw-rebrush2024/get/documents_E-1646019713/MLR.LEL/PB5Documents/fiona/2026/Formulare/FAKT%20B1.2%20%20-%20Aufzeichnungen%20zu%20den%20Gr%C3%BCnlandma%C3%9Fnahmen%202026.pdf", "pdf"),
    ("FAKT II 2026 > B-Formulare", "FAKT II B3.2 - Aufzeichnungen Grünlandmaßnahmen (Excel)",
     "/pbs-bw-rebrush2024/get/documents_E543676351/MLR.LEL/PB5Documents/fiona/2026/Formulare/FAKT%20B3.2%20-%20Aufzeichnungen%20zu%20den%20Gr%C3%BCnlandma%C3%9Fnahmen%202026.xlsx", "xlsx"),
    ("FAKT II 2026 > B-Formulare", "FAKT II B3.2 - Aufzeichnungen Grünlandmaßnahmen (PDF)",
     "/pbs-bw-rebrush2024/get/documents_E-1297204800/MLR.LEL/PB5Documents/fiona/2026/Formulare/FAKT%20B3.2%20-%20Aufzeichnungen%20zu%20den%20Gr%C3%BCnlandma%C3%9Fnahmen%202026.pdf", "pdf"),

    # === FAKT II D Formulare ===
    ("FAKT II 2026 > D-Formulare", "FAKT II D2 - Bericht Kontrolle Ökolandbaubetriebe",
     "/pbs-bw-rebrush2024/get/documents_E-1668214323/MLR.LEL/PB5Documents/fiona/2026/Formulare/FAKT%20D2%20-%20Bericht%20%C3%BCber%20die%20Kontrolle%20der%20Oekolandbaubetriebe.pdf", "pdf"),

    # === FAKT II E Informationen ===
    ("FAKT II 2026 > E-Informationen", "Empfehlungen für ackerbauliche FAKT II-Maßnahmen (E1.2, E7-E9, E13, E14, E15, F3, F4)",
     "/pbs-bw-rebrush2024/get/documents_E-140461577/MLR.LEL/PB5Documents/ltz_ka/Arbeitsfelder/Landwirtschaft_und_Umwelt/Greening%20und%20FAKT/FAKT_DL/Empfehlungen%20f%C3%BCr%20ausgew%C3%A4hlte%20ackerbauliche%20FAKT%20II-Ma%C3%9Fnahmen.pdf", "pdf"),
    ("FAKT II 2026 > E-Informationen", "Merkblatt Pflege mehrjähriger Blühmischungen (E8)",
     "/pbs-bw-rebrush2024/get/documents_E-2121432110/MLR.LEL/PB5Documents/fiona/2026/Merkblaetter/FAKT_Merkblatt_Pflege_mehrjaehrige_Bluehflaechen.pdf", "pdf"),
    ("FAKT II 2026 > E-Informationen", "FAKT II E13.1 und E13.2 - Erweiterter Drillreihenabstand - FAQ",
     "/pbs-bw-rebrush2024/get/documents_E-2007284674/MLR.LEL/PB5Documents/fiona/2026/Merkblaetter/FAKT%20II%20E13.1%20und%20E13.2%20-%20Erweiterter%20Drillreihenabstand%20in%20Getreide%20-%20H%C3%A4ufig%20gestellte%20Fragen.pdf", "pdf"),

    # === FAKT II G Formulare ===
    ("FAKT II 2026 > G-Formulare", "FAKT II G1 - Weidetagebuch (Excel)",
     "/pbs-bw-rebrush2024/get/documents_E-946132854/MLR.LEL/PB5Documents/fiona/2026/Formulare/FAKT%20II%20G1%20-%20Weidetagebuch.xlsx", "xlsx"),
    ("FAKT II 2026 > G-Formulare", "FAKT II G2 - Bestandsverzeichnis Mastschweine (Excel)",
     "/pbs-bw-rebrush2024/get/documents_E-741747257/MLR.LEL/PB5Documents/fiona/2026/Formulare/FAKT%20II%20G2%20-%20Bestandsverzeichnis%20Mastschweine.xlsx", "xlsx"),
    ("FAKT II 2026 > G-Formulare", "FAKT II G2 - Anlage Antrag Tierwohl Mastschweine (Excel)",
     "/pbs-bw-rebrush2024/get/documents_E1636714171/MLR.LEL/PB5Documents/fiona/2026/Formulare/FAKT%20II%20G2%20-%20Anlage%20zum%20Antrag%20Tierwohl%20Mastschwein.xlsx", "xlsx"),
    ("FAKT II 2026 > G-Formulare", "FAKT II G3 - Bestandsverzeichnis Masthühner (Excel)",
     "/pbs-bw-rebrush2024/get/documents_E-1761987262/MLR.LEL/PB5Documents/fiona/2026/Formulare/FAKT%20II%20G3%20-%20Bestandsverzeichnis%20Masthuehner.xlsx", "xlsx"),
    ("FAKT II 2026 > G-Formulare", "FAKT II G3 - Anlage Antrag Tierwohl Masthühner (Excel)",
     "/pbs-bw-rebrush2024/get/documents_E931727168/MLR.LEL/PB5Documents/fiona/2026/Formulare/FAKT%20II%20G3%20-%20Anlage%20zum%20Antrag%20Tierwohl%20Masthuehner.xlsx", "xlsx"),
    ("FAKT II 2026 > G-Formulare", "FAKT II G4.1 - Bestandsverzeichnis Junghühneraufzucht Zweinutzungsrassen (Excel)",
     "/pbs-bw-rebrush2024/get/documents_E681182499/MLR.LEL/PB5Documents/fiona/2026/Formulare/FAKT%20II%20G4.1%20-%20Bestandsverzeichnis%20Junghuehneraufzucht%20Zweinutzungsrassen.xlsx", "xlsx"),
    ("FAKT II 2026 > G-Formulare", "FAKT II G4.1 - Anlage Antrag Tierwohl Zweinutzungshuhnaufzucht (Excel)",
     "/pbs-bw-rebrush2024/get/documents_E-594443708/MLR.LEL/PB5Documents/fiona/2026/Formulare/FAKT%20II%20G4.1%20-%20Anlage%20zum%20Antrag%20Tierwohl%20Zweinutzungshuhnaufzucht.xlsx", "xlsx"),
    ("FAKT II 2026 > G-Formulare", "FAKT II G4.2 - Bestandsverzeichnis Legehennen Zweinutzungsrassen (Excel)",
     "/pbs-bw-rebrush2024/get/documents_E-1925713538/MLR.LEL/PB5Documents/fiona/2026/Formulare/FAKT%20II%20G4.2%20-%20Bestandsverzeichnis%20Legehennen%20Zweinutzungshuhnrassen.xlsx", "xlsx"),
    ("FAKT II 2026 > G-Formulare", "FAKT II G4.2 - Anlage Tierwohl Zweinutzungshühner Legehennen (Excel)",
     "/pbs-bw-rebrush2024/get/documents_E1636453780/MLR.LEL/PB5Documents/fiona/2026/Formulare/FAKT%20II%20G4.2%20-%20Anlage%20zum%20Antrag%20Tierwohl%20Zweinutzungshuehner%20Legehennen.xlsx", "xlsx"),
    ("FAKT II 2026 > G-Formulare", "FAKT II G5 - Bestandsverzeichnis Ferkelerzeugung (Excel)",
     "/pbs-bw-rebrush2024/get/documents_E-450650687/MLR.LEL/PB5Documents/fiona/2026/Formulare/FAKT%20II%20G5%20-%20Bestandsverzeichnis%20Ferkelerzeugung.xlsx", "xlsx"),
    ("FAKT II 2026 > G-Formulare", "FAKT II G5 - Anlage Antrag Tierwohl Ferkelerzeugung (Excel)",
     "/pbs-bw-rebrush2024/get/documents_E-1812915599/MLR.LEL/PB5Documents/fiona/2026/Formulare/FAKT%20II%20G5%20-%20Anlage%20zum%20Antrag%20Tierwohl%20Ferkelerzeugung.xlsx", "xlsx"),
    ("FAKT II 2026 > G-Formulare", "FAKT II G6 - Bestandsverzeichnis Ferkelaufzucht (Excel)",
     "/pbs-bw-rebrush2024/get/documents_E-860488160/MLR.LEL/PB5Documents/fiona/2026/Formulare/FAKT%20II%20G6%20-%20Bestandsverzeichnis%20Ferkelaufzucht.xlsx", "xlsx"),
    ("FAKT II 2026 > G-Formulare", "FAKT II G6 - Anlage Antrag Tierwohl Ferkelaufzucht (Excel)",
     "/pbs-bw-rebrush2024/get/documents_E-100757618/MLR.LEL/PB5Documents/fiona/2026/Formulare/FAKT%20II%20G6%20-%20Anlage%20zum%20Antrag%20Tierwohl%20Ferkelaufzucht.xlsx", "xlsx"),
    ("FAKT II 2026 > G-Formulare", "FAKT II G7 - Anlage Antrag Tierwohl Kälberhaltung (Excel)",
     "/pbs-bw-rebrush2024/get/documents_E1051231025/MLR.LEL/PB5Documents/fiona/2026/Formulare/FAKT%20II%20G7%20-%20Anlage%20zum%20Antrag%20Tierwohl%20Kaelberhaltung%20Formblatt%20und%20Bestandsverzeichnis.xlsx", "xlsx"),

    # === FAKT II G Informationen ===
    ("FAKT II 2026 > G-Informationen", "FAKT II G4 - Zweinutzungshuhnrassen - Liste",
     "/pbs-bw-rebrush2024/get/documents_E-1125344490/MLR.LEL/PB5Documents/fiona/2026/Merkblaetter/FAKT%20II%20G4%20-%20Zweinutzungsh%C3%BChner%20-%20Liste%20Rassen.pdf", "pdf"),
    ("FAKT II 2026 > G-Informationen", "FAKT II G-Maßnahmen - Häufige Fragen",
     "/pbs-bw-rebrush2024/get/documents_E-232475855/MLR.LEL/PB5Documents/fiona/2026/Merkblaetter/FAKT%20II%20G-Ma%C3%9Fnahmen%20-%20H%C3%A4ufige%20Fragen.pdf", "pdf"),

    # === UuU ===
    ("UuU-Förderantrag 2026", "Merkblatt Antrag Umstrukturierung/Umstellung Rebflächen 2026",
     "/pbs-bw-rebrush2024/get/documents_E-1939576586/MLR.LEL/PB5Documents/mlr/GA/GA_026_extern/UuU_Unterlagen/UuU%202026%20-%2001%20Merkblatt%20zur%20Antragstellung%20Stand%20Dezember%202025.pdf", "pdf"),
]


def make_filename(title, filetype):
    """Create a clean filename from the title."""
    # Remove special chars, keep umlauts
    name = title.replace("/", "_").replace(":", "_").replace("–", "-")
    name = name.replace("(", "").replace(")", "").replace(",", "")
    name = name.replace("  ", " ").strip()
    name = name.replace(" ", "_")
    # Truncate if too long
    if len(name) > 80:
        name = name[:80]
    return f"{name}.{filetype}"


def download_file(url, filepath):
    """Download a file via httpx (SSL-tolerant), return True on success."""
    import httpx
    try:
        with httpx.Client(verify=False, follow_redirects=True, timeout=30) as client:
            resp = client.get(url)
            resp.raise_for_status()
            with open(filepath, "wb") as f:
                f.write(resp.content)
        if os.path.getsize(filepath) == 0:
            print(f"  FEHLER: Datei leer", file=sys.stderr)
            os.remove(filepath)
            return False
        return True
    except Exception as e:
        print(f"  FEHLER: {e}", file=sys.stderr)
        if os.path.exists(filepath):
            os.remove(filepath)
        return False


def main():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    results = []  # (section, title, filename, success, filetype)

    for i, (section, title, url_path, filetype) in enumerate(DOCUMENTS):
        filename = make_filename(title, filetype)
        filepath = os.path.join(DOWNLOAD_DIR, filename)

        # Build full URL
        if url_path.startswith("https://"):
            full_url = url_path
        else:
            full_url = f"{BASE}{url_path}"

        print(f"[{i+1}/{len(DOCUMENTS)}] {title}...")

        if os.path.exists(filepath):
            print(f"  Bereits vorhanden: {filename}")
            results.append((section, title, filename, True, filetype))
            continue

        success = download_file(full_url, filepath)
        if success:
            size = os.path.getsize(filepath)
            print(f"  OK ({size:,} bytes) -> {filename}")
        results.append((section, title, filename, success, filetype))
        time.sleep(0.3)

    # Generate markdown overview
    md_path = os.path.join(os.path.dirname(__file__), "..", "formulare_uebersicht.md")
    with open(md_path, "w") as f:
        f.write("# Formulare / Merkblätter / Informationen zum Gemeinsamen Antrag 2026\n\n")
        f.write("Quelle: [foerderung.landwirtschaft-bw.de](https://foerderung.landwirtschaft-bw.de/,Lde/Startseite/Gemeinsamer+Antrag/Formulare+_+Merkblaetter+_+Informationen+zum+Gemeinsamen+Antrag)\n\n")
        f.write(f"Stand: 2026-04-14 | {sum(1 for r in results if r[3])} von {len(results)} Dateien heruntergeladen\n\n")
        f.write("---\n\n")

        current_section = None
        for section, title, filename, success, filetype in results:
            if section != current_section:
                current_section = section
                # Determine heading level from section depth
                parts = section.split(" > ")
                if len(parts) == 1:
                    f.write(f"\n## {section}\n\n")
                else:
                    f.write(f"\n### {' / '.join(parts)}\n\n")

            icon = {"pdf": "PDF", "xlsx": "Excel"}.get(filetype, filetype.upper())
            status = "" if success else " **(FEHLER)**"
            f.write(f"- [{title}](downloads/formulare_2026/{filename}) ({icon}){status}\n")

        # Summary section for wiki relevance
        f.write("\n---\n\n")
        f.write("## Einordnung: Was davon ist wiki-relevant?\n\n")
        f.write("### Bereits im Wiki verarbeitet\n\n")
        f.write("- FAKT II - Broschüre (→ `raw/fakt_broschuere_*.pdf`)\n")
        f.write("- FAKT II - Kombinationstabelle Excel (→ `raw/Kombinationstabelle FAKT II.xlsx`)\n")
        f.write("- GA - Erläuterungen und Ausfüllhinweise 2026 (→ `raw/GA - Erlaeuterungen und Ausfuellhinweise 2026.pdf`, teilweise)\n")
        f.write("- Informationsbroschüre Konditionalität 2026 (→ `raw/Kond_Infobroschuere_2026.pdf`)\n")
        f.write("\n### Potenziell wiki-relevant (Beratungsebene)\n\n")
        f.write("- **GA - Wichtige Informationen zum GA 2026** – Neuerungen, Änderungen gegenüber Vorjahr\n")
        f.write("- **Ergänzende Informationen ÖR1b, ÖR1c, ÖR2, ÖR5** – Details zu Öko-Regelungen\n")
        f.write("- **Empfehlungen ackerbauliche FAKT II-Maßnahmen** – Praxishinweise E1.2, E7-E9, E13, E14, E15, F3, F4\n")
        f.write("- **FAKT II - Maßnahmen und FAKT-Codes 2026** – Mapping Codes ↔ Maßnahmen\n")
        f.write("- **LPR-Grünlandmaßnahmen + Öko-Regelungen Kombinationen** – Ergänzung zu bestehender Kombinationstabelle\n")
        f.write("- **Kennarten-Broschüre ÖR5/FAKT II** – Für B3.2 relevant\n")
        f.write("- **Merkblatt Pflege mehrjähriger Blühmischungen (E8)** – Praxisrelevant\n")
        f.write("- **FAKT II G-Maßnahmen FAQ** – Häufige Fragen Tierhaltung\n")
        f.write("- **GLÖZ 5 Mindestpraktiken Bodenbewirtschaftung** – Konditionalität-Ergänzung\n")
        f.write("- **Informationsbroschüre soziale Konditionalität 2026** – Neues Thema\n")
        f.write("\n### Eher nicht wiki-relevant (Formularebene / Scope-Ausschluss)\n\n")
        f.write("- Nutzcodelisten (FIONA-Codes → Scope-Ausschluss)\n")
        f.write("- Aufzeichnungsformulare B1.2, B3.2 (Formularebene)\n")
        f.write("- G-Bestandsverzeichnisse und Antragsanlagen (Formularebene)\n")
        f.write("- D2 Kontrollbericht (Formularebene)\n")
        f.write("- Übertragungsformular Verpflichtungen (Formularebene)\n")
        f.write("- Widerruf Einwilligung (Formularebene)\n")
        f.write("- Datenschutz-Infos (Formularebene)\n")
        f.write("- FFH-Mähwiesen Infoblatt (Spezialthema)\n")
        f.write("- Beratungsflyer (Werbung)\n")
        f.write("- UZW Auerhuhn (Forstwirtschaft, nicht FAKT II)\n")
        f.write("- Weinbau-spezifische ÖR1a-Dokumente (Nische)\n")
        f.write("- Agri-Photovoltaik / Agroforstsystem (Nische)\n")
        f.write("- UuU Rebflächen (Weinbau)\n")

    print(f"\nÜbersicht geschrieben: {md_path}")
    print(f"Ergebnis: {sum(1 for r in results if r[3])}/{len(results)} erfolgreich")


if __name__ == "__main__":
    main()
