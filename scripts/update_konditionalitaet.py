#!/usr/bin/env python3
"""
Fügt jeder Maßnahmen-Seite einen '## Konditionalität'-Abschnitt hinzu,
der die relevanten GLÖZ/GAB-Standards verlinkt und beschreibt, wie die
Maßnahme über die jeweilige Baseline hinausgeht.

Verwendung:
    python3 scripts/update_konditionalitaet.py [--dry-run]

Idempotent: überspringt Dateien, die bereits '## Konditionalität' enthalten.
"""

import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASSNAHMEN_DIR = os.path.join(BASE, "wiki", "massnahmen")

# Zuordnung: Dateiname → Liste von (Wiki-Link, Beschreibung)
# Jede Beschreibung erklärt knapp, wie die Maßnahme sich zur Baseline verhält.
MAPPING = {
    # === A – Betriebsmanagement ===
    "A2_Silageverzicht.md": [
        ("[[GLOEZ_1_Dauergruenland|GLÖZ 1 Dauergrünland]]",
         "Silageverzicht setzt Grünlandbewirtschaftung voraus – GLÖZ 1 sichert Erhalt des DGL"),
        ("[[GAB_5_Lebensmittelsicherheit|GAB 5 Lebensmittelsicherheit]]",
         "Heumilch-Erzeugung unterliegt denselben Hygieneanforderungen"),
    ],
    "A3_Kleine_Strukturen.md": [
        ("[[GLOEZ_8_Landschaftselemente|GLÖZ 8 Landschaftselemente]]",
         "Fördert Strukturen, die teils unter GLÖZ-8-Schutz stehen – geht über Beseitigungsverbot hinaus"),
    ],

    # === B – Grünland ===
    "B1.2_Extensive_Gruenland.md": [
        ("[[GLOEZ_1_Dauergruenland|GLÖZ 1 Dauergrünland]]",
         "Extensive Bewirtschaftung erhält DGL – GLÖZ 1 sichert den Flächenstatus"),
        ("[[GAB_2_Nitratrichtlinie|GAB 2 Nitratrichtlinie]]",
         "Verzicht auf N-Düngung geht deutlich über GAB-2-Obergrenzen hinaus"),
        ("[[GAB_7_8_Pflanzenschutz|GAB 7/8 Pflanzenschutz]]",
         "Baseline: zugelassene PSM regelkonform anwenden"),
    ],
    "B3.2_Artenreiches_Gruenland.md": [
        ("[[GLOEZ_1_Dauergruenland|GLÖZ 1 Dauergrünland]]",
         "Artenreiches DGL erhält den Grünlandstatus"),
        ("[[GLOEZ_8_Landschaftselemente|GLÖZ 8 Landschaftselemente]]",
         "Artenreiches Grünland fördert Biodiversität über GLÖZ-8-Mindestschutz hinaus"),
    ],
    "B4_Biotope.md": [
        ("[[GLOEZ_1_Dauergruenland|GLÖZ 1 Dauergrünland]]",
         "§ 30-Biotope sind häufig Dauergrünland"),
        ("[[GAB_3_4_Naturschutz|GAB 3/4 Naturschutz]]",
         "Extensive Nutzung geschützter Biotope geht über das Verschlechterungsverbot hinaus"),
    ],
    "B5_FFH_Maehwiesen.md": [
        ("[[GLOEZ_1_Dauergruenland|GLÖZ 1 Dauergrünland]]",
         "FFH-Mähwiesen sind Dauergrünland"),
        ("[[GLOEZ_9_Natura2000_Dauergruenland|GLÖZ 9 Natura 2000 DGL]]",
         "FFH-Mähwiesen in Natura-2000-Gebieten unterliegen GLÖZ 9"),
        ("[[GAB_3_4_Naturschutz|GAB 3/4 Naturschutz]]",
         "Extensive Nutzung geht über das FFH-Verschlechterungsverbot hinaus"),
    ],
    "B6_Messerbalkenschnitt.md": [
        ("[[GLOEZ_1_Dauergruenland|GLÖZ 1 Dauergrünland]]",
         "Begleitmaßnahme zu GL-Maßnahmen auf Dauergrünland"),
    ],
    "B7_Verzicht_Chemie_Gruenland.md": [
        ("[[GLOEZ_1_Dauergruenland|GLÖZ 1 Dauergrünland]]",
         "Grünland-Maßnahme – GLÖZ 1 sichert DGL-Status"),
        ("[[GAB_2_Nitratrichtlinie|GAB 2 Nitratrichtlinie]]",
         "Verzicht auf mineralischen N-Dünger geht über GAB-2-Obergrenzen hinaus"),
        ("[[GAB_7_8_Pflanzenschutz|GAB 7/8 Pflanzenschutz]]",
         "Vollständiger PSM-Verzicht geht deutlich über GAB 7/8 hinaus"),
    ],

    # === C – Landschaftspflege & Tierrassen ===
    "C1_Streuobst.md": [
        ("[[GLOEZ_8_Landschaftselemente|GLÖZ 8 Landschaftselemente]]",
         "Streuobstbäume können als Landschaftselemente unter GLÖZ-8-Schutz stehen"),
        ("[[GAB_3_4_Naturschutz|GAB 3/4 Naturschutz]]",
         "Streuobstwiesen als Vogelhabitat – Bewirtschaftung geht über Erhaltungspflicht hinaus"),
    ],
    "C2_Weinbausteillagen.md": [
        ("[[GLOEZ_5_Erosionsschutz|GLÖZ 5 Erosionsschutz]]",
         "Steillagen sind erosionsgefährdet – Bewirtschaftung sichert Erosionsschutz"),
        ("[[GAB_7_8_Pflanzenschutz|GAB 7/8 Pflanzenschutz]]",
         "Baseline: zugelassene PSM regelkonform anwenden"),
    ],
    "C3_Nutztierrassen.md": [
        ("[[GAB_9_10_11_Tierschutz|GAB 11 Tierschutz]]",
         "Haltung gefährdeter Nutztierrassen unterliegt allgemeinen Tierschutzanforderungen"),
    ],

    # === D – Ökolandbau ===
    "D2_Oekolandbau_Einfuehrung.md": [
        ("[[GLOEZ_1_Dauergruenland|GLÖZ 1 Dauergrünland]]",
         "Öko-DGL unterliegt GLÖZ 1; Omnibus III könnte Öko-Betriebe von GLÖZ 1 befreien"),
        ("[[GLOEZ_7_Fruchtwechsel|GLÖZ 7 Fruchtwechsel]]",
         "Öko-Fruchtfolge erfüllt GLÖZ 7 automatisch; Omnibus-III-Befreiung möglich"),
        ("[[GAB_2_Nitratrichtlinie|GAB 2 Nitratrichtlinie]]",
         "Öko-Düngungsbeschränkungen gehen über GAB 2 hinaus"),
        ("[[GAB_7_8_Pflanzenschutz|GAB 7/8 Pflanzenschutz]]",
         "Grundsätzlicher Verzicht auf chem.-synth. PSM geht weit über GAB 7/8 hinaus"),
    ],
    "D2_Oekolandbau_Beibehaltung.md": [
        ("[[GLOEZ_1_Dauergruenland|GLÖZ 1 Dauergrünland]]",
         "Öko-DGL unterliegt GLÖZ 1; Omnibus III könnte Öko-Betriebe von GLÖZ 1 befreien"),
        ("[[GLOEZ_7_Fruchtwechsel|GLÖZ 7 Fruchtwechsel]]",
         "Öko-Fruchtfolge erfüllt GLÖZ 7 automatisch; Omnibus-III-Befreiung möglich"),
        ("[[GAB_2_Nitratrichtlinie|GAB 2 Nitratrichtlinie]]",
         "Öko-Düngungsbeschränkungen gehen über GAB 2 hinaus"),
        ("[[GAB_7_8_Pflanzenschutz|GAB 7/8 Pflanzenschutz]]",
         "Grundsätzlicher Verzicht auf chem.-synth. PSM geht weit über GAB 7/8 hinaus"),
    ],
    "D2_Oekolandbau_Transaktionskosten.md": [
        ("[[Konditionalitaet|Konditionalität]]",
         "Administrativer Ausgleich – keine direkten GLÖZ/GAB-Bezüge; allgemeine Konditionalität gilt"),
    ],

    # === E – Pflanzenerzeugung (Acker) ===
    "E1.2_Begruenungsmischungen.md": [
        ("[[GLOEZ_6_Bodenbedeckung|GLÖZ 6 Bodenbedeckung]]",
         "Begrünungsmischungen gehen über 80%-Mindestbodenbedeckung hinaus"),
        ("[[GLOEZ_7_Fruchtwechsel|GLÖZ 7 Fruchtwechsel]]",
         "Zwischenfrüchte zählen nicht als Hauptkultur, unterstützen aber Fruchtfolge"),
        ("[[GAB_2_Nitratrichtlinie|GAB 2 Nitratrichtlinie]]",
         "Begrünung bindet Reststickstoff und reduziert Auswaschung"),
    ],
    "E3_Herbizidverzicht.md": [
        ("[[GAB_7_8_Pflanzenschutz|GAB 7/8 Pflanzenschutz]]",
         "Herbizidverzicht geht über GAB-7/8-Grundregeln hinaus"),
        ("[[GLOEZ_6_Bodenbedeckung|GLÖZ 6 Bodenbedeckung]]",
         "Mechanische Unkrautbekämpfung statt Herbizid beeinflusst Bodenbedeckung"),
    ],
    "E4_Trichogramma.md": [
        ("[[GAB_7_8_Pflanzenschutz|GAB 7/8 Pflanzenschutz]]",
         "Biologischer Pflanzenschutz ersetzt Insektizideinsatz – geht über GAB 7/8 hinaus"),
    ],
    "E5_Nuetzlingseinsatz.md": [
        ("[[GAB_7_8_Pflanzenschutz|GAB 7/8 Pflanzenschutz]]",
         "Nützlingseinsatz statt chem. PSM im Gewächshaus – geht über GAB 7/8 hinaus"),
    ],
    "E6_Pheromoneinsatz.md": [
        ("[[GAB_7_8_Pflanzenschutz|GAB 7/8 Pflanzenschutz]]",
         "Pheromonfallen statt Insektizide im Obstbau – geht über GAB 7/8 hinaus"),
    ],
    "E7_Bluehflaechen.md": [
        ("[[GLOEZ_6_Bodenbedeckung|GLÖZ 6 Bodenbedeckung]]",
         "Blühflächen erfüllen und übertreffen GLÖZ-6-Mindestbodenbedeckung"),
        ("[[GLOEZ_8_Landschaftselemente|GLÖZ 8 Landschaftselemente]]",
         "Blühflächen schaffen zusätzliche Habitatstrukturen über GLÖZ 8 hinaus"),
        ("[[GAB_3_4_Naturschutz|GAB 3/4 Naturschutz]]",
         "Brut- und Rückzugsflächen für Vogelarten"),
    ],
    "E8_Brachebegruenung.md": [
        ("[[GLOEZ_6_Bodenbedeckung|GLÖZ 6 Bodenbedeckung]]",
         "Mehrjährige Blühmischungen übertreffen GLÖZ-6-Mindestbodenbedeckung"),
        ("[[GLOEZ_8_Landschaftselemente|GLÖZ 8 Landschaftselemente]]",
         "Brachebegrünung als Strukturelement"),
    ],
    "E9_Mais_Stangenbohnen.md": [
        ("[[GLOEZ_7_Fruchtwechsel|GLÖZ 7 Fruchtwechsel]]",
         "Mais-Mischkultur zählt als Hauptkultur Mais (Änderung 2026)"),
        ("[[GAB_7_8_Pflanzenschutz|GAB 7/8 Pflanzenschutz]]",
         "Gemengepartner können PSM-Bedarf reduzieren"),
    ],
    "E10_Ackerfutterbau.md": [
        ("[[GLOEZ_7_Fruchtwechsel|GLÖZ 7 Fruchtwechsel]]",
         "Mehrjähriger Ackerfutterbau beeinflusst Fruchtfolgegestaltung"),
        ("[[GAB_2_Nitratrichtlinie|GAB 2 Nitratrichtlinie]]",
         "Leguminosenbetont – reduziert mineralische N-Düngung über GAB-2-Anforderungen hinaus"),
    ],
    "E11_Herbizidfreie_Dauerkulturen.md": [
        ("[[GAB_7_8_Pflanzenschutz|GAB 7/8 Pflanzenschutz]]",
         "Herbizidfreie Bewirtschaftung in Dauerkulturen geht über GAB 7/8 hinaus"),
        ("[[GLOEZ_5_Erosionsschutz|GLÖZ 5 Erosionsschutz]]",
         "Mechanische Beikrautregulierung statt Herbizid beeinflusst Erosionsschutz in Dauerkulturen"),
    ],
    "E12_Fungizidverzicht.md": [
        ("[[GAB_7_8_Pflanzenschutz|GAB 7/8 Pflanzenschutz]]",
         "Fungizidverzicht im Getreide geht über GAB-7/8-Grundregeln hinaus"),
    ],
    "E13.1_Drillreihenabstand.md": [
        ("[[GLOEZ_7_Fruchtwechsel|GLÖZ 7 Fruchtwechsel]]",
         "Erweiterter Reihenabstand in Getreide – Fruchtfolge bleibt Baseline"),
    ],
    "E13.2_Drillreihenabstand_Untersaat.md": [
        ("[[GLOEZ_6_Bodenbedeckung|GLÖZ 6 Bodenbedeckung]]",
         "Blühende Untersaat verbessert Bodenbedeckung über GLÖZ 6 hinaus"),
        ("[[GLOEZ_7_Fruchtwechsel|GLÖZ 7 Fruchtwechsel]]",
         "Erweiterter Reihenabstand in Getreide – Fruchtfolge bleibt Baseline"),
    ],
    "E14_Wildpflanzenmischungen.md": [
        ("[[GLOEZ_6_Bodenbedeckung|GLÖZ 6 Bodenbedeckung]]",
         "Mehrjährige Wildpflanzenmischungen übertreffen GLÖZ-6-Mindestbodenbedeckung"),
        ("[[GLOEZ_8_Landschaftselemente|GLÖZ 8 Landschaftselemente]]",
         "Dauerhafte Strukturen über GLÖZ-8-Mindestschutz hinaus"),
    ],
    "E15_Streifenanbau_Biomasse.md": [
        ("[[GLOEZ_6_Bodenbedeckung|GLÖZ 6 Bodenbedeckung]]",
         "Streifenanbau mit Dauerkulturen übertrifft GLÖZ-6-Bodenbedeckung"),
        ("[[GLOEZ_8_Landschaftselemente|GLÖZ 8 Landschaftselemente]]",
         "Streifen als Strukturelemente in der Landschaft"),
    ],

    # === F – Gewässer & Erosion ===
    "F3_Precision_Farming.md": [
        ("[[GAB_1_Wasserrahmenrichtlinie|GAB 1 Wasserrahmenrichtlinie]]",
         "Teilflächenspezifische Düngung reduziert P-Überschüsse über GAB-1-Vorgaben hinaus"),
        ("[[GAB_2_Nitratrichtlinie|GAB 2 Nitratrichtlinie]]",
         "Teilflächenspezifische N-Düngung reduziert Auswaschung über GAB-2-Vorgaben hinaus"),
    ],
    "F4_Strip_Till.md": [
        ("[[GLOEZ_5_Erosionsschutz|GLÖZ 5 Erosionsschutz]]",
         "Strip Till als erosionsminderndes Verfahren über GLÖZ-5-Mindestpraktiken hinaus"),
        ("[[GLOEZ_6_Bodenbedeckung|GLÖZ 6 Bodenbedeckung]]",
         "Reduzierte Bodenbearbeitung erhält Bodenbedeckung"),
    ],

    # === G – Tierwohl ===
    "G1_Sommerweide.md": [
        ("[[GAB_9_10_11_Tierschutz|GAB 11 Tierschutz]]",
         "Weidegang geht über allgemeine Haltungsanforderungen hinaus"),
    ],
    "G2.1_Mastschweine_Einstieg.md": [
        ("[[GAB_9_10_11_Tierschutz|GAB 10 Schweine]]",
         "Mehr Platz und Beschäftigung über GAB-10-Mindestflächen hinaus"),
    ],
    "G2.2_Mastschweine_Premium.md": [
        ("[[GAB_9_10_11_Tierschutz|GAB 10 Schweine]]",
         "Auslauf/Außenklima geht deutlich über GAB-10-Mindestanforderungen hinaus"),
    ],
    "G3.1_Masthuehner_Einstieg.md": [
        ("[[GAB_9_10_11_Tierschutz|GAB 11 Tierschutz]]",
         "Reduzierte Besatzdichte über allgemeine Tierschutzanforderungen hinaus"),
    ],
    "G3.2_Masthuehner_Premium.md": [
        ("[[GAB_9_10_11_Tierschutz|GAB 11 Tierschutz]]",
         "Deutlich reduzierte Besatzdichte und Außenklima über GAB 11 hinaus"),
    ],
    "G3.3_Bruderhahn.md": [
        ("[[GAB_9_10_11_Tierschutz|GAB 11 Tierschutz]]",
         "Bruderhahn-Aufzucht statt Kükentöten – über GAB 11 hinaus"),
    ],
    "G4.1_Junghuhner_Zweinutzung.md": [
        ("[[GAB_9_10_11_Tierschutz|GAB 11 Tierschutz]]",
         "Zweinutzungshuhn-Aufzucht über allgemeine Tierschutzanforderungen hinaus"),
    ],
    "G4.2_Legehennen_Zweinutzung.md": [
        ("[[GAB_9_10_11_Tierschutz|GAB 11 Tierschutz]]",
         "Zweinutzungshuhn-Haltung über allgemeine Tierschutzanforderungen hinaus"),
    ],
    "G5_Ferkelerzeugung.md": [
        ("[[GAB_9_10_11_Tierschutz|GAB 10 Schweine]]",
         "Freie Abferkelung, Deckzentrum, Wartestall – geht über GAB-10-Kastenstandregelungen hinaus"),
    ],
    "G6_Ferkelaufzucht.md": [
        ("[[GAB_9_10_11_Tierschutz|GAB 10 Schweine]]",
         "Mehr Platz und Beschäftigung in der Aufzucht über GAB-10-Mindestflächen hinaus"),
    ],
    "G7_Kaelber.md": [
        ("[[GAB_9_10_11_Tierschutz|GAB 9 Kälber]]",
         "Mehr Platz, früherer Weidegang, Gruppenhaltung ab Geburt – über GAB-9-Mindestanforderungen hinaus"),
    ],
}


def insert_section(filepath, entries):
    """Fügt den Konditionalitäts-Abschnitt vor der letzten ---/Quelle-Zeile ein."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if "## Konditionalität" in content:
        return False  # bereits vorhanden

    lines = []
    lines.append("\n## Konditionalität\n")
    lines.append("Die Maßnahme baut auf folgenden Konditionalitäts-Anforderungen auf "
                  "(siehe [[Konditionalitaet|Konditionalität]]):\n")
    for link, desc in entries:
        lines.append(f"- {link}: {desc}")
    section = "\n".join(lines) + "\n"

    # Einfügen vor dem letzten "---" gefolgt von "*Quelle:"
    pattern = r"\n---\n\*Quelle:"
    match = re.search(pattern, content)
    if match:
        pos = match.start()
        content = content[:pos] + "\n" + section + content[pos:]
    else:
        # Fallback: am Ende anhängen
        content = content.rstrip() + "\n\n" + section

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return True


def main():
    dry_run = "--dry-run" in sys.argv
    updated = 0
    skipped = 0
    missing = 0

    for filename, entries in sorted(MAPPING.items()):
        filepath = os.path.join(MASSNAHMEN_DIR, filename)
        if not os.path.exists(filepath):
            print(f"WARNUNG: {filepath} nicht gefunden", file=sys.stderr)
            missing += 1
            continue

        if dry_run:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            if "## Konditionalität" in content:
                print(f"  SKIP  {filename} (bereits vorhanden)")
                skipped += 1
            else:
                print(f"  WÜRDE {filename} aktualisieren ({len(entries)} Einträge)")
                updated += 1
        else:
            if insert_section(filepath, entries):
                print(f"  OK    {filename} ({len(entries)} Einträge)")
                updated += 1
            else:
                print(f"  SKIP  {filename} (bereits vorhanden)")
                skipped += 1

    action = "Würde aktualisieren" if dry_run else "Aktualisiert"
    print(f"\n{action}: {updated}, Übersprungen: {skipped}, Nicht gefunden: {missing}")


if __name__ == "__main__":
    main()
