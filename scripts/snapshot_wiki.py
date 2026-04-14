#!/usr/bin/env python3
"""
Extrahiert den Ist-Zustand aller Maßnahmen-Seiten als maschinenlesbares JSON.
Dient als Basis für Diff-Vergleiche bei FAKT-Updates (z.B. FAKT II → FAKT III).

Verwendung:
    python3 scripts/snapshot_wiki.py > wiki_snapshot.json

Extrahiert pro Maßnahme:
    - YAML-Frontmatter (code, titel, foerdersatz, einheit, kategorie)
    - Kombinierbar mit (Liste von Codes + Annotationen)
    - Nicht kombinierbar mit (Liste von Codes)
    - Konditionalität (Liste von GLÖZ/GAB-Bezügen)
"""

import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASSNAHMEN_DIR = os.path.join(BASE, "wiki", "massnahmen")


def parse_frontmatter(content):
    """Extrahiert YAML-Frontmatter als Dict."""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).splitlines():
        m = re.match(r'^(\w+):\s*"?([^"]*)"?\s*$', line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm


def parse_section_links(content, header):
    """Extrahiert Wikilinks aus einem bestimmten Abschnitt (## header)."""
    pattern = rf"## {re.escape(header)}\n(.*?)(?=\n## |\n---|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return []
    section = match.group(1)
    links = []
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("- [["):
            continue
        # Extrahiere Code aus dem Link-Text
        link_match = re.match(r"- \[\[([^|]+)\|([^\]]+)\]\](.*)", line)
        if link_match:
            target = link_match.group(1)
            label = link_match.group(2)
            annotation = link_match.group(3).strip()
            links.append({
                "target": target,
                "label": label,
                "annotation": annotation if annotation else None,
            })
    return links


def parse_konditionalitaet(content):
    """Extrahiert Konditionalitäts-Bezüge."""
    pattern = r"## Konditionalität\n(.*?)(?=\n## |\n---|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return []
    section = match.group(1)
    refs = []
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("- [["):
            continue
        link_match = re.match(r"- \[\[([^|]+)\|([^\]]+)\]\]:\s*(.*)", line)
        if link_match:
            refs.append({
                "target": link_match.group(1),
                "label": link_match.group(2),
                "beschreibung": link_match.group(3),
            })
    return refs


def snapshot_massnahme(filepath):
    """Erstellt einen Snapshot einer einzelnen Maßnahmen-Seite."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    fm = parse_frontmatter(content)
    return {
        "datei": os.path.basename(filepath),
        "code": fm.get("code", ""),
        "titel": fm.get("titel", ""),
        "foerdersatz": fm.get("foerdersatz", ""),
        "einheit": fm.get("einheit", ""),
        "kategorie": fm.get("kategorie", ""),
        "verpflichtung": fm.get("verpflichtung", ""),
        "kombinierbar_mit": parse_section_links(content, "Kombinierbar mit"),
        "nicht_kombinierbar_mit": parse_section_links(content, "Nicht kombinierbar mit"),
        "konditionalitaet": parse_konditionalitaet(content),
    }


def main():
    massnahmen = []
    for filename in sorted(os.listdir(MASSNAHMEN_DIR)):
        if not filename.endswith(".md"):
            continue
        filepath = os.path.join(MASSNAHMEN_DIR, filename)
        massnahmen.append(snapshot_massnahme(filepath))

    snapshot = {
        "version": "FAKT II",
        "stand": "2025-10",
        "massnahmen_count": len(massnahmen),
        "massnahmen": massnahmen,
    }
    json.dump(snapshot, sys.stdout, ensure_ascii=False, indent=2)
    print(file=sys.stderr)
    print(f"Snapshot: {len(massnahmen)} Maßnahmen extrahiert", file=sys.stderr)


if __name__ == "__main__":
    main()
