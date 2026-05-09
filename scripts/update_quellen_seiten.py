#!/usr/bin/env python3
"""
Reichert die Footer-Quelle der Maßnahmen-Seiten um Kapitel + Seitenzahl an.

Aus:    *Quelle: FAKT_II_Broschuere.pdf, Stand Oktober 2025*
Wird:   *Quelle: FAKT_II_Broschuere.pdf, Kap. B / S. 11, Stand Oktober 2025*

Das Mapping {wiki-dateiname → (kapitel, seitenbereich)} kommt aus dem
Inhaltsverzeichnis der Broschüre (Seiten 3–4, geprüft 2026-05-07).
Bei einem späteren Broschüren-Update muss das Mapping neu erzeugt werden —
dann TOC erneut lesen und die Konstante unten aktualisieren.

Idempotent: Seiten, die bereits eine Seitenzahl in der Footer-Quelle tragen,
werden übersprungen.

Usage:
    python3 scripts/update_quellen_seiten.py [--dry-run]
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


WIKI = Path(__file__).resolve().parent.parent / "wiki" / "massnahmen"

# Stand: Inhaltsverzeichnis FAKT_II_Broschuere.pdf, Stand 20.10.2025, S. 3–4.
# Seitenbereich = Anfang bis vor der nächsten Maßnahme (oder Kapitelwechsel).
# Format: wiki-Dateiname-stem → (kapitel-buchstabe, seitenbereich-string)
MAPPING: dict[str, tuple[str, str]] = {
    "A2_Silageverzicht":               ("A", "11"),
    "A3_Kleine_Strukturen":            ("A", "11"),
    "B1.2_Extensive_Gruenland":        ("B", "11–12"),
    "B3.2_Artenreiches_Gruenland":     ("B", "12–13"),
    "B4_Biotope":                      ("B", "13"),
    "B5_FFH_Maehwiesen":               ("B", "13–14"),
    "B6_Messerbalkenschnitt":          ("B", "14"),
    "B7_Verzicht_Chemie_Gruenland":    ("B", "14–15"),
    "C1_Streuobst":                    ("C", "15"),
    "C2_Weinbausteillagen":            ("C", "15"),
    "C3_Nutztierrassen":               ("C", "15–16"),
    "D2_Oekolandbau_Einfuehrung":      ("D", "17–18"),
    "D2_Oekolandbau_Beibehaltung":     ("D", "18–19"),
    "D2_Oekolandbau_Transaktionskosten": ("D", "19"),
    "E1.2_Begruenungsmischungen":      ("E", "19–20"),
    "E3_Herbizidverzicht":             ("E", "20–21"),
    "E4_Trichogramma":                 ("E", "21"),
    "E5_Nuetzlingseinsatz":            ("E", "21–22"),
    "E6_Pheromoneinsatz":              ("E", "22"),
    "E7_Bluehflaechen":                ("E", "22–23"),
    "E8_Brachebegruenung":             ("E", "23–24"),
    "E9_Mais_Stangenbohnen":           ("E", "24–25"),
    "E10_Ackerfutterbau":              ("E", "25"),
    "E11_Herbizidfreie_Dauerkulturen": ("E", "25–26"),
    "E12_Fungizidverzicht":            ("E", "26"),
    "E13.1_Drillreihenabstand":        ("E", "26–27"),
    "E13.2_Drillreihenabstand_Untersaat": ("E", "27–28"),
    "E14_Wildpflanzenmischungen":      ("E", "28–29"),
    "E15_Streifenanbau_Biomasse":      ("E", "29"),
    "F3_Precision_Farming":            ("F", "30–31"),
    "F4_Strip_Till":                   ("F", "31"),
    "G1_Sommerweide":                  ("G", "32"),
    "G2.1_Mastschweine_Einstieg":      ("G", "32–33"),
    "G2.2_Mastschweine_Premium":       ("G", "33–34"),
    "G3.1_Masthuehner_Einstieg":       ("G", "35–36"),
    "G3.2_Masthuehner_Premium":        ("G", "36–37"),
    "G3.3_Bruderhahn":                 ("G", "37–38"),
    "G4.1_Junghuhner_Zweinutzung":     ("G", "38–39"),
    "G4.2_Legehennen_Zweinutzung":     ("G", "40–41"),
    "G5_Ferkelerzeugung":              ("G", "41–43"),
    "G6_Ferkelaufzucht":               ("G", "43–44"),
    "G7_Kaelber":                      ("G", "44–45"),
}

OLD_FOOTER_RE = re.compile(
    r"\*Quelle:\s*FAKT_II_Broschuere\.pdf,\s*Stand\s*Oktober\s*2025\*"
)
# Variante: Mehrquellen-Footer wie *Quellen: FAKT_II_Broschuere.pdf (Stand Oktober 2025), ...*
MULTI_FOOTER_RE = re.compile(
    r"FAKT_II_Broschuere\.pdf\s*\(Stand\s*Oktober\s*2025\)"
)
NEW_FOOTER_HAS_PAGE_RE = re.compile(
    r"FAKT_II_Broschuere\.pdf,\s*Kap\."
)


def patch(path: Path, kapitel: str, seiten: str, dry_run: bool) -> str:
    text = path.read_text(encoding="utf-8")
    if NEW_FOOTER_HAS_PAGE_RE.search(text):
        return "skip (bereits gepatcht)"

    if OLD_FOOTER_RE.search(text):
        new_footer = f"*Quelle: FAKT_II_Broschuere.pdf, Kap. {kapitel} / S. {seiten}, Stand Oktober 2025*"
        new_text = OLD_FOOTER_RE.sub(new_footer, text, count=1)
    elif MULTI_FOOTER_RE.search(text):
        replacement = f"FAKT_II_Broschuere.pdf, Kap. {kapitel} / S. {seiten} (Stand Oktober 2025)"
        new_text = MULTI_FOOTER_RE.sub(replacement, text, count=1)
    else:
        return "skip (Footer-Format unbekannt)"

    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return f"-> Kap. {kapitel} / S. {seiten}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    matched = 0
    unmatched = []
    for slug, (kap, seiten) in MAPPING.items():
        path = WIKI / f"{slug}.md"
        if not path.exists():
            unmatched.append(slug)
            continue
        result = patch(path, kap, seiten, args.dry_run)
        marker = "DRY" if args.dry_run else "OK "
        print(f"[{marker}] {slug}.md  {result}")
        if result.startswith("->"):
            matched += 1

    print(f"\n{'DRY-RUN: ' if args.dry_run else ''}Patched: {matched}, Mapping-Einträge: {len(MAPPING)}")
    if unmatched:
        print(f"\nMapping ohne Wiki-Datei (zu prüfen):")
        for s in unmatched:
            print(f"  - {s}")

    # Wiki-Dateien ohne Mapping melden
    extra = [p.stem for p in WIKI.glob("*.md") if p.stem not in MAPPING]
    if extra:
        print(f"\nWiki-Dateien ohne Mapping (manuell ergänzen):")
        for s in extra:
            print(f"  - {s}")


if __name__ == "__main__":
    main()
