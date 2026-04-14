import json, os, re, glob

WIKI = "/Users/ulfmertens/Documents/agrar/wiki"
DATA = os.path.join(WIKI, "data/kombinationstabelle.json")

with open(DATA) as f:
    data = json.load(f)

matrix = data["matrix"]["fakt_vs_fakt"]
oer_matrix = data["matrix"]["oeko_regelungen_vs_fakt"]
reduced = data["reduzierte_foerdersaetze"]

# Map JSON keys to filenames
key_to_file = {
    "A2": "A2_Silageverzicht",
    "A3": "A3_Kleine_Strukturen",
    "B1.2": "B1.2_Extensive_Gruenland",
    "B3.2": "B3.2_Artenreiches_Gruenland",
    "B4": "B4_Biotope",
    "B5": "B5_FFH_Maehwiesen",
    "B6": "B6_Messerbalkenschnitt",
    "B7": "B7_Verzicht_Chemie_Gruenland",
    "C1": "C1_Streuobst",
    "C2": "C2_Weinbausteillagen",
    "D2_Einfuehrung": "D2_Oekolandbau_Einfuehrung",
    "D2_Beibehaltung": "D2_Oekolandbau_Beibehaltung",
    "D2_Transaktionskosten": "D2_Oekolandbau_Transaktionskosten",
    "E1.2": "E1.2_Begruenungsmischungen",
    "E3": "E3_Herbizidverzicht",
    "E4": "E4_Trichogramma",
    "E5": "E5_Nuetzlingseinsatz",
    "E6": "E6_Pheromoneinsatz",
    "E7": "E7_Bluehflaechen",
    "E8": "E8_Brachebegruenung",
    "E9": "E9_Mais_Stangenbohnen",
    "E10": "E10_Ackerfutterbau",
    "E11": "E11_Herbizidfreie_Dauerkulturen",
    "E12": "E12_Fungizidverzicht",
    "E13.1": "E13.1_Drillreihenabstand",
    "E13.2": "E13.2_Drillreihenabstand_Untersaat",
    "E14": "E14_Wildpflanzenmischungen",
    "E15": "E15_Streifenanbau_Biomasse",
    "F3": "F3_Precision_Farming",
    "F4": "F4_Strip_Till",
}

# Short titles for display
key_to_title = {
    "A2": "A2 Silageverzicht",
    "A3": "A3 Kleine Strukturen",
    "B1.2": "B1.2 Extensive Grünlandbewirtschaftung",
    "B3.2": "B3.2 Artenreiches Grünland",
    "B4": "B4 §30/§33 Biotope",
    "B5": "B5 FFH-Mähwiesen",
    "B6": "B6 Messerbalkenschnitt",
    "B7": "B7 Verzicht chem.-synth. Produktionsmittel",
    "C1": "C1 Streuobst",
    "C2": "C2 Weinbausteillagen",
    "D2_Einfuehrung": "D2 Ökolandbau – Einführung",
    "D2_Beibehaltung": "D2 Ökolandbau – Beibehaltung",
    "D2_Transaktionskosten": "D2 Transaktionskosten",
    "E1.2": "E1.2 Begrünungsmischungen",
    "E3": "E3 Herbizidverzicht Ackerbau",
    "E4": "E4 Trichogramma",
    "E5": "E5 Nützlingseinsatz",
    "E6": "E6 Pheromoneinsatz",
    "E7": "E7 Blühflächen",
    "E8": "E8 Brachebegrünung",
    "E9": "E9 Mais mit Stangenbohnen",
    "E10": "E10 Ackerfutterbau",
    "E11": "E11 Herbizidfreie Dauerkulturen",
    "E12": "E12 Fungizidverzicht",
    "E13.1": "E13.1 Drillreihenabstand",
    "E13.2": "E13.2 Drillreihenabstand mit Untersaat",
    "E14": "E14 Wildpflanzenmischungen",
    "E15": "E15 Streifenanbau Biomasse",
    "F3": "F3 Precision Farming",
    "F4": "F4 Strip Till",
}

# ÖR titles
oer_titles = {
    "OeR1a": "ÖR 1a Nichtproduktive Flächen Ackerland",
    "OeR1b": "ÖR 1b Blühstreifen Ackerland",
    "OeR1c": "ÖR 1c Blühstreifen Dauerkulturen",
    "OeR1d": "ÖR 1d Altgrasstreifen Dauergrünland",
    "OeR2": "ÖR 2 Vielfältige Kulturen",
    "OeR3": "ÖR 3 Agroforst",
    "OeR4": "ÖR 4 Extensivierung Dauergrünland",
    "OeR5": "ÖR 5 Kennarten Dauergrünland",
    "OeR6": "ÖR 6 Verzicht chem.-synth. PSM",
    "OeR7": "ÖR 7 Natura 2000",
}

# Build reduced rate lookup: (measure_key, context) -> annotation string
def get_reduction_note(measure_key, partner_key):
    """Return annotation for x/a combinations with exact euro amounts."""
    # D2 mit FAKT
    d2_reductions = reduced["D2_mit_FAKT"]
    # Extract the base code from measure_key (e.g. "B1.2" from "B1.2")
    base = measure_key.replace("_Einfuehrung","").replace("_Beibehaltung","").replace("_Transaktionskosten","")
    partner_base = partner_key.replace("_Einfuehrung","").replace("_Beibehaltung","").replace("_Transaktionskosten","")
    
    # If this measure is combined with D2, check if THIS measure gets reduced
    if partner_key in ("D2_Einfuehrung", "D2_Beibehaltung") and base in d2_reductions:
        return d2_reductions[base]
    
    # If this IS D2 and partner is one that reduces D2
    # (doesn't apply - D2 itself isn't reduced by FAKT, the FAKT measure is reduced)
    
    # D2 with ÖR4
    oer4_reductions = reduced["D2_mit_OeR4"]
    
    # B7 mit FAKT
    b7_reductions = reduced["B7_mit_FAKT"]
    if partner_key == "B7" and base in b7_reductions:
        return b7_reductions[base]
    if base == "B7" and partner_base in b7_reductions:
        return f"{partner_base}: {b7_reductions[partner_base]}"
    
    return None

# Symbol explanations
symbol_explain = {
    "X": "",
    "x/a": "Abzug",
    "o": "nur mit GL-Maßnahme",
    "(o)": "nur wenn zusätzlich GL-Maßnahme beantragt",
    "kR": "keine zusätzliche D2-Förderung auf dieser Fläche",
    "-": "",
}

def build_combination_sections(measure_key):
    """Build the new combination sections for a measure."""
    if measure_key not in matrix:
        return None
    
    combos = matrix[measure_key]
    
    kombinierbar = []
    nicht_kombinierbar = []
    
    # Collect all known partner keys to find explicit non-combinable ones
    all_partners = set()
    for k in matrix:
        if k != measure_key:
            all_partners.add(k)
    
    for partner, symbol in sorted(combos.items(), key=lambda x: x[0]):
        if partner not in key_to_file:
            continue
        
        filename = key_to_file[partner]
        title = key_to_title[partner]
        
        if symbol == "-":
            nicht_kombinierbar.append(f"- [[{filename}|{title}]] (–)")
        elif symbol == "X":
            kombinierbar.append(f"- [[{filename}|{title}]]")
        elif symbol == "x/a":
            reduction = get_reduction_note(measure_key, partner)
            if reduction:
                kombinierbar.append(f"- [[{filename}|{title}]] (x/a – {reduction})")
            else:
                kombinierbar.append(f"- [[{filename}|{title}]] (x/a)")
        elif symbol == "o":
            kombinierbar.append(f"- [[{filename}|{title}]] (o – nur mit GL-Maßnahme)")
        elif symbol == "(o)":
            kombinierbar.append(f"- [[{filename}|{title}]] ((o) – nur wenn zusätzlich GL-Maßnahme beantragt)")
        elif symbol == "kR":
            nicht_kombinierbar.append(f"- [[{filename}|{title}]] (kR – keine zusätzliche D2-Förderung)")
    
    # Build ÖR section
    oer_entries = []
    for oer_key, oer_combos in oer_matrix.items():
        # Find this measure in ÖR combinations
        # Need to match: measure_key might be "A2" and in oer_combos it's also "A2"
        if measure_key in oer_combos:
            symbol = oer_combos[measure_key]
            title = oer_titles[oer_key]
            if symbol == "X":
                oer_entries.append(f"- {title}")
            elif symbol == "x/a":
                # Check ÖR4 + D2 reductions
                if oer_key == "OeR4" and measure_key in ("D2_Einfuehrung", "D2_Beibehaltung"):
                    oer4 = reduced["D2_mit_OeR4"]
                    if measure_key == "D2_Einfuehrung":
                        oer_entries.append(f"- {title} (x/a – {oer4['D2_Einfuehrung_Gruenland']})")
                    else:
                        oer_entries.append(f"- {title} (x/a – {oer4['D2_Beibehaltung_Gruenland']})")
                else:
                    oer_entries.append(f"- {title} (x/a)")
            elif symbol == "-":
                oer_entries.append(f"- {title} (–)")
            elif symbol == "(o)":
                oer_entries.append(f"- {title} ((o))")
            elif symbol == "kR":
                oer_entries.append(f"- {title} (kR – keine zusätzliche D2-Förderung)")
    
    sections = []
    
    if kombinierbar:
        sections.append("## Kombinierbar mit\n")
        sections.append("\n".join(kombinierbar))
    
    if nicht_kombinierbar:
        sections.append("\n\n## Nicht kombinierbar mit\n")
        sections.append("\n".join(nicht_kombinierbar))
    
    if oer_entries:
        sections.append("\n\n## Öko-Regelungen (1. Säule)\n")
        sections.append("Siehe auch [[Oeko-Regelungen]].\n")
        sections.append("\n".join(oer_entries))
    
    return "\n".join(sections)

# Process each measure file
updated = 0
skipped = 0

for measure_key, filename in key_to_file.items():
    filepath = os.path.join(WIKI, "massnahmen", filename + ".md")
    if not os.path.exists(filepath):
        print(f"SKIP (not found): {filepath}")
        skipped += 1
        continue
    
    new_sections = build_combination_sections(measure_key)
    if new_sections is None:
        print(f"SKIP (no matrix data): {measure_key}")
        skipped += 1
        continue
    
    with open(filepath, "r") as f:
        content = f.read()
    
    # Remove old combination sections (everything from "## Kombinierbar" or "## Nicht kombinierbar" to the next "---" or end)
    # Strategy: find the FIRST occurrence of "## Kombinierbar" or "## Nicht kombinierbar" and replace everything from there to the final "---\n*Quelle" line
    
    # Find where combination sections start
    patterns = [
        r'\n## Kombinierbar mit\n',
        r'\n## Nicht kombinierbar mit\n',
    ]
    
    earliest_pos = len(content)
    for pat in patterns:
        m = re.search(pat, content)
        if m and m.start() < earliest_pos:
            earliest_pos = m.start()
    
    if earliest_pos == len(content):
        # No existing combination section, append before the final ---
        footer_match = re.search(r'\n---\n\*Quelle:', content)
        if footer_match:
            earliest_pos = footer_match.start()
        else:
            earliest_pos = len(content)
    
    # Find the footer
    footer = "\n\n---\n*Quelle: FAKT II-Broschüre Baden-Württemberg, Stand Oktober 2025*\n"
    
    # Rebuild: everything before combination sections + new sections + footer
    new_content = content[:earliest_pos].rstrip() + "\n\n" + new_sections + footer
    
    with open(filepath, "w") as f:
        f.write(new_content)
    
    updated += 1
    print(f"OK: {filename}")

print(f"\nDone: {updated} updated, {skipped} skipped")
