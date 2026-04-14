#!/usr/bin/env python3
"""Trägt fakt_code in das YAML-Frontmatter aller Maßnahmen-Seiten ein.

Quelle: raw/FAKT_Codes_2026.pdf (Stand 17.10.2025)

Usage:
    uv run python3 scripts/add_fakt_codes.py
"""

import pathlib
import re

# Mapping: Maßnahmencode → FAKT-Code (aus PDF extrahiert)
# Nur Maßnahmen mit explizitem FAKT-Code; Maßnahmen ohne Code werden übersprungen.
FAKT_CODES = {
    "B1.2": "21",
    "B3.2": "23",
    "B4": "24",
    "B5": "25",
    "B6": "62",
    "C2": "30",
    "E1.2": "41",
    "E3": "44",
    "E4": "45",
    "E5": "46",
    "E6": "47",
    "E7": "48",
    "E8": "49",
    "E9": "70",
    "E10": "71",
    "E11": "72",
    "E12": "73",
    "E13.1": "74",
    "E13.2": "75",
    "E14": "76",
    "E15": "77",
    "F3": "52",
    "F4": "53",
}

MASSNAHMEN_DIR = pathlib.Path("wiki/massnahmen")


def add_fakt_code(filepath: pathlib.Path, fakt_code: str) -> bool:
    """Fügt fakt_code ins YAML-Frontmatter ein. Gibt True zurück wenn geändert."""
    text = filepath.read_text(encoding="utf-8")

    # Bereits vorhanden?
    if re.search(r"^fakt_code:", text, re.MULTILINE):
        # Update falls abweichend
        new_text = re.sub(
            r'^fakt_code:.*$',
            f'fakt_code: "{fakt_code}"',
            text,
            count=1,
            flags=re.MULTILINE,
        )
        if new_text != text:
            filepath.write_text(new_text, encoding="utf-8")
            return True
        return False

    # Einfügen vor "type: massnahme"
    new_text = text.replace(
        'type: massnahme',
        f'fakt_code: "{fakt_code}"\ntype: massnahme',
        1,
    )
    if new_text == text:
        print(f"  WARNUNG: Konnte fakt_code nicht einfügen in {filepath}")
        return False

    filepath.write_text(new_text, encoding="utf-8")
    return True


def main():
    updated = []
    skipped = []

    for filepath in sorted(MASSNAHMEN_DIR.glob("*.md")):
        # Code aus YAML extrahieren
        text = filepath.read_text(encoding="utf-8")
        match = re.search(r'^code:\s*"([^"]+)"', text, re.MULTILINE)
        if not match:
            continue

        code = match.group(1)
        # G1.1/G1.2 → einzelne Codes prüfen
        codes_to_check = [c.strip() for c in code.split("/")]

        fakt_code = None
        for c in codes_to_check:
            if c in FAKT_CODES:
                fakt_code = FAKT_CODES[c]
                break

        if fakt_code is None:
            skipped.append(f"{code} ({filepath.name})")
            continue

        if add_fakt_code(filepath, fakt_code):
            updated.append(f"{code} → FC {fakt_code} ({filepath.name})")
        else:
            skipped.append(f"{code} → FC {fakt_code} (bereits korrekt)")

    print(f"\n=== FAKT-Codes eingetragen ===")
    print(f"Aktualisiert: {len(updated)}")
    for u in updated:
        print(f"  + {u}")
    print(f"\nÜbersprungen: {len(skipped)}")
    for s in skipped:
        print(f"  - {s}")


if __name__ == "__main__":
    main()
