#!/usr/bin/env python3
"""
Einmalige Migration: ergänzt jede Wiki-Seite um die Felder

  - created:   Datum des ersten Git-Commits der Datei (Fallback: heute)
  - updated:   Datum des letzten Git-Commits der Datei (Fallback: heute)
  - sources:   Liste der raw/-Dateien, die in der Seite zitiert werden
               (extrahiert aus Inline (Quelle: …) und Footer *Quelle: …*)
  - tags:      Liste aus der SCHEMA.md-Taxonomie, heuristisch ermittelt

Bestehende Werte werden NICHT überschrieben — die Migration ist idempotent.
Mit --dry-run wird nur gemeldet, was passieren würde.

Usage:
    uv run --with pyyaml python3 scripts/migrate_frontmatter.py [--dry-run]
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import unicodedata
from datetime import date
from pathlib import Path

import yaml


def nfc(s: str) -> str:
    """macOS speichert Dateinamen in NFD; Wiki-Texte in NFC. Vor Vergleich normalisieren."""
    return unicodedata.normalize("NFC", s)


WIKI_ROOT = Path(__file__).resolve().parent.parent / "wiki"
RAW_ROOT = Path(__file__).resolve().parent.parent / "raw"
TODAY = date.today().isoformat()

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)
QUELLE_INLINE_RE = re.compile(r"\(Quellen?:\s*([^)]+)\)")
QUELLE_FOOTER_RE = re.compile(r"^\*Quelle:\s*([^*]+)\*", re.MULTILINE)
PROVENANCE_RE = re.compile(r"\^\[([^\]]+\.(?:pdf|xlsx))\]")
FILE_RE = re.compile(r"([\w\-\.\s\(\)ÄÖÜäöüß]+\.(?:pdf|xlsx))")


def load_known_raw_files() -> set[str]:
    """Sammelt alle .pdf/.xlsx-Dateinamen aus raw/ (auch in Unterordnern)."""
    files = set()
    for p in RAW_ROOT.rglob("*"):
        if p.is_file() and p.suffix.lower() in (".pdf", ".xlsx"):
            files.add(nfc(p.name))
    return files


KNOWN_RAW = load_known_raw_files()


def git_date(path: Path, first: bool) -> str | None:
    """Datum des ersten (first=True) bzw. letzten Commits, der die Datei berührt."""
    try:
        flag = "--diff-filter=A" if first else ""
        cmd = ["git", "log", "--follow", "--format=%ad", "--date=short"]
        if flag:
            cmd.insert(2, flag)
        cmd.append(str(path))
        out = subprocess.check_output(cmd, cwd=path.parent, stderr=subprocess.DEVNULL).decode().strip()
        if not out:
            return None
        lines = out.splitlines()
        return lines[-1] if first else lines[0]
    except subprocess.CalledProcessError:
        return None


def extract_sources(body: str) -> list[str]:
    """Findet alle in raw/ existierenden Dateien, die in der Seite zitiert werden."""
    found: list[str] = []
    seen: set[str] = set()

    for chunk in QUELLE_INLINE_RE.findall(body):
        for fname in FILE_RE.findall(chunk):
            fname = nfc(fname.strip())
            if fname in KNOWN_RAW and fname not in seen:
                found.append(fname)
                seen.add(fname)

    for chunk in QUELLE_FOOTER_RE.findall(body):
        for fname in FILE_RE.findall(chunk):
            fname = nfc(fname.strip())
            if fname in KNOWN_RAW and fname not in seen:
                found.append(fname)
                seen.add(fname)

    for fname in PROVENANCE_RE.findall(body):
        fname = nfc(fname.strip())
        if fname in KNOWN_RAW and fname not in seen:
            found.append(fname)
            seen.add(fname)

    return found


# ---- Tag-Heuristik -----------------------------------------------------------
#
# Tags werden aus drei Signalen abgeleitet: Pfad, Dateiname, Inhalt.
# Pro Seite ergeben sich i.d.R. 2–4 Tags. Mehr als 5 wird gekappt.

CONTENT_KEYWORDS = {
    "wasserschutz": [r"\bgewäss", r"\bbach\b", r"\bpufferstreifen", r"\bGLÖZ\s*4\b", r"§\s*29\s*WG"],
    "bodenschutz": [r"\berosion", r"\bhumus", r"\bbodenbedeckung", r"\bGLÖZ\s*[567]\b"],
    "klimaschutz": [r"\bmoor\b", r"\btreibhausgas", r"\bdauergrünland\b.*\bschutz"],
    "biodiversitaet": [r"\bblühflächen", r"\bniederwild", r"\bartenreich", r"\binsekten"],
    "landschaftselement": [r"\blandschaftselement", r"\bhecke", r"\bfeldgehölz", r"\bsteinmauer", r"\bGLÖZ\s*8\b"],
    "pflanzenschutz": [r"\bPSM\b", r"\bpflanzenschutzmittel", r"\bchem.-synth"],
    "duengung": [r"\bdüngung\b", r"\bN-Düngung", r"\bnitrat", r"\bphosphat"],
    "tierwohl": [r"\btierwohl", r"\bauslauf", r"\bweide\b", r"\bhaltungs"],
    "oekolandbau": [r"\bökolandbau", r"\böko-betrieb", r"\bD2\b"],
    "konditionalitaet": [r"\bkonditionalität", r"\bGLÖZ\b", r"\bGAB\b"],
    "oekoregelung": [r"\böko-regelung", r"\bÖR\s*\d", r"\b1\.?\s*säule"],
    "kombination": [r"\bkombinier", r"\bkombination"],
    "foerderhoehe": [r"\bfördersatz", r"\b€/ha\b", r"\bauszahlung"],
    "nachweis": [r"\bnachweis", r"\bbelegpflicht", r"\bdokumentation"],
    "antragstellung": [r"\bFIONA\b", r"\bFAKT-Code", r"\bgemeinsamer antrag"],
}

CATEGORY_DEFAULTS = {
    "A": ["ackerbau"],
    "B": ["gruenland"],
    "C": ["dauerkultur"],
    "D": ["oekolandbau"],
    "E": ["ackerbau", "biodiversitaet"],
    "F": ["bodenschutz"],
    "G": ["tierhaltung", "tierwohl"],
}

PATH_DEFAULTS = {
    "Antragstellung": ["antragstellung"],
    "Beispielfragen": [],  # tags ergeben sich aus Inhalt
    "Kategorien": [],      # ergibt sich aus Code
    "Konzepte": [],        # ergibt sich aus Inhalt
    "massnahmen": [],      # ergibt sich aus Code
    "strategie": [],       # ergibt sich aus Inhalt
}


def derive_tags(path: Path, fm: dict, body: str) -> list[str]:
    tags: list[str] = []

    # Pfad-basierter Default
    rel = path.relative_to(WIKI_ROOT)
    top = rel.parts[0] if len(rel.parts) > 1 else ""
    tags.extend(PATH_DEFAULTS.get(top, []))

    # Maßnahmen-Code → Kategorie-Default
    code = fm.get("code", "")
    if code and code[0] in CATEGORY_DEFAULTS:
        tags.extend(CATEGORY_DEFAULTS[code[0]])

    # Kategorie-Seite (z.B. Kategorie_B.md)
    fname = path.stem
    m = re.match(r"Kategorie_([A-G])", fname)
    if m and m.group(1) in CATEGORY_DEFAULTS:
        tags.extend(CATEGORY_DEFAULTS[m.group(1)])

    # Inhalts-basiert
    body_lower = body.lower()
    for tag, patterns in CONTENT_KEYWORDS.items():
        for pat in patterns:
            if re.search(pat, body_lower, re.IGNORECASE):
                tags.append(tag)
                break

    # Dedupe, max 5
    seen = set()
    unique = []
    for t in tags:
        if t not in seen:
            seen.add(t)
            unique.append(t)
    return unique[:5]


def process_file(path: Path, dry_run: bool) -> dict:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {"path": str(path), "skipped": "no frontmatter"}

    fm_text, body = m.group(1), m.group(2)
    fm = yaml.safe_load(fm_text) or {}
    if not isinstance(fm, dict):
        return {"path": str(path), "skipped": "frontmatter not a mapping"}

    changes = {}

    if "created" not in fm:
        fm["created"] = git_date(path, first=True) or TODAY
        changes["created"] = fm["created"]
    if "updated" not in fm:
        fm["updated"] = git_date(path, first=False) or TODAY
        changes["updated"] = fm["updated"]
    if "sources" not in fm:
        srcs = extract_sources(body)
        if srcs:
            fm["sources"] = srcs
            changes["sources"] = srcs
    if "tags" not in fm:
        tags = derive_tags(path, fm, body)
        if tags:
            fm["tags"] = tags
            changes["tags"] = tags

    if not changes:
        return {"path": str(path), "skipped": "already has all fields"}

    if not dry_run:
        new_fm = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False).rstrip()
        new_text = f"---\n{new_fm}\n---\n{body}"
        path.write_text(new_text, encoding="utf-8")

    return {"path": str(path.relative_to(WIKI_ROOT)), "changes": changes}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    files = sorted(WIKI_ROOT.rglob("*.md"))
    files = [f for f in files if "_archive" not in f.parts]

    summary = {"updated": 0, "skipped": 0, "missing_sources": []}
    for f in files:
        result = process_file(f, dry_run=args.dry_run)
        rel = str(f.relative_to(WIKI_ROOT))
        if "skipped" in result:
            summary["skipped"] += 1
        else:
            summary["updated"] += 1
            ch = result["changes"]
            marker = "DRY" if args.dry_run else "OK "
            print(f"[{marker}] {result['path']}")
            for k, v in ch.items():
                v_str = v if not isinstance(v, list) else ", ".join(v)
                print(f"       {k}: {v_str}")

        # Frontmatter erneut lesen (nach Schreibvorgang) ODER aus changes ableiten
        text = f.read_text(encoding="utf-8")
        m = FRONTMATTER_RE.match(text)
        if m:
            fm_after = yaml.safe_load(m.group(1)) or {}
        else:
            fm_after = {}
        sources_after = fm_after.get("sources") or (result.get("changes", {}).get("sources") if not args.dry_run else None)
        if not sources_after:
            # Bei dry-run aus changes prüfen
            if "changes" in result and "sources" in result["changes"]:
                continue
            summary["missing_sources"].append(rel)

    print(f"\n{'DRY-RUN: ' if args.dry_run else ''}Updated: {summary['updated']}, Skipped: {summary['skipped']}")
    if summary["missing_sources"]:
        print(f"\nSeiten ohne sources (manuelle Prüfung nötig, {len(summary['missing_sources'])} Stk.):")
        for p in summary["missing_sources"]:
            print(f"  - {p}")


if __name__ == "__main__":
    main()
