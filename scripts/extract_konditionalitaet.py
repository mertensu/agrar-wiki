#!/usr/bin/env python3
"""
Extrahiert Text aus den gesplitteten Konditionalitaets-PDFs.
Gibt JSON auf stdout aus (ein Eintrag pro PDF, darin Seiten mit Text).

Verwendung:
    uv run --with pdfplumber python3 scripts/extract_konditionalitaet.py \
        > raw/konditionalitaet/kond_extracted.json

Voraussetzung: scripts/split_kond_info.sh wurde ausgefuehrt.
"""

import json
import os
import sys

import pdfplumber

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KOND = os.path.join(BASE, "raw", "konditionalitaet")

PDFS = [
    "kond_I_einleitung.pdf",
    "kond_II_gloez.pdf",
    "kond_III_gab.pdf",
    "kond_IV_kontrolle.pdf",
    "kond_V_anlagen.pdf",
    "kond_VI_weitere_info.pdf",
]


def extract_pdf(path):
    pages = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            pages.append({"seite": i + 1, "text": text})
    return pages


def main():
    result = {}
    for name in PDFS:
        path = os.path.join(KOND, name)
        if not os.path.exists(path):
            print(f"WARNUNG: {path} nicht gefunden", file=sys.stderr)
            continue
        result[name] = extract_pdf(path)
        print(f"  {name}: {len(result[name])} Seiten extrahiert", file=sys.stderr)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
