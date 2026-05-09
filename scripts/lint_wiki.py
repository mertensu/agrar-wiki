#!/usr/bin/env python3
"""
Wiki-Gesundheitscheck.

Prüft:
  - Broken Wikilinks       — [[Ziel]] zeigt auf nicht-existente Seite
  - Orphan-Pages           — keine eingehenden Wikilinks von anderen Seiten
  - Frontmatter            — Pflichtfelder vorhanden? Tags in der Taxonomie?
  - Quellen                — Datei in `sources:` existiert in raw/?
  - Page-Size              — > 200 Zeilen → Split-Kandidat
  - TODO-Marker            — `<!-- TODO: ... -->` im Body
  - Konfidenz / contested  — Seiten mit `confidence: low` oder `contested: true`

Manifest-Drift ist separat: `python3 scripts/update_manifest.py --check`.

Exit-Code 0 wenn nichts kritisch (broken links, frontmatter-Fehler, fehlende
Quellen). Sonst 1 — eignet sich für CI.

Usage:
    uv run --with pyyaml python3 scripts/lint_wiki.py [--strict]
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

import yaml


WIKI_ROOT = Path(__file__).resolve().parent.parent / "wiki"
RAW_ROOT = Path(__file__).resolve().parent.parent / "raw"
SCHEMA_PATH = WIKI_ROOT / "SCHEMA.md"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)
# Wikilink: [[Ziel]] oder [[Ziel|Anzeige]]. In Tabellen wird `|` als `\|` escaped,
# also `[[Ziel\|Anzeige]]` — wir akzeptieren beide.
WIKILINK_RE = re.compile(r"\[\[([^\]\|\\]+)(?:\\?\|[^\]]+)?\]\]")
TODO_RE = re.compile(r"<!--\s*TODO.*?-->", re.IGNORECASE | re.DOTALL)

REQUIRED_FRONTMATTER = {"type", "titel", "created", "updated"}
ALLOWED_TYPES = {"massnahme", "kategorie", "konzept", "antragstellung",
                 "beispielfrage", "strategie", "uebersicht"}
# Meta-Seiten haben kein reguläres Frontmatter
META_PAGES = {"index", "log", "SCHEMA"}


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def load_taxonomy() -> set[str]:
    """Liest die Tag-Liste aus SCHEMA.md unter dem Abschnitt # Tag-Taxonomie."""
    if not SCHEMA_PATH.exists():
        return set()
    text = SCHEMA_PATH.read_text(encoding="utf-8")
    after = text.split("## Tag-Taxonomie", 1)
    if len(after) < 2:
        return set()
    section = after[1].split("\n## ", 1)[0]
    tags = set(re.findall(r"^-\s+`([\w-]+)`", section, re.MULTILINE))
    return tags


def load_known_raw() -> set[str]:
    return {nfc(p.name) for p in RAW_ROOT.rglob("*") if p.is_file() and p.suffix.lower() in (".pdf", ".xlsx")}


def load_pages() -> dict[str, dict]:
    """Liest alle Wiki-Seiten, gibt {slug: {path, fm, body, lines, links}}."""
    pages = {}
    for p in WIKI_ROOT.rglob("*.md"):
        if "_archive" in p.parts:
            continue
        text = p.read_text(encoding="utf-8")
        fm, body = {}, text
        m = FRONTMATTER_RE.match(text)
        if m:
            fm = yaml.safe_load(m.group(1)) or {}
            body = m.group(2)
        slug = p.stem
        rel = str(p.relative_to(WIKI_ROOT))
        links = [nfc(l.strip()) for l in WIKILINK_RE.findall(body)]
        pages[slug] = {
            "path": rel,
            "fm": fm if isinstance(fm, dict) else {},
            "body": body,
            "lines": len(text.splitlines()),
            "links": links,
        }
    return pages


def lint(pages: dict, taxonomy: set[str], known_raw: set[str]) -> dict:
    issues = defaultdict(list)
    valid_slugs = set(pages.keys())

    incoming = defaultdict(set)
    for slug, p in pages.items():
        for link in p["links"]:
            target = link.split("/")[-1]
            incoming[target].add(slug)

    for slug, p in pages.items():
        rel = p["path"]
        fm = p["fm"]

        # Broken links — `#anchor` ist Heading-Verweis innerhalb der Zielseite,
        # nicht Teil des Slugs. SCHEMA.md ist Schema-Doku mit Platzhaltern.
        if slug != "SCHEMA":
            for link in p["links"]:
                target = link.rstrip("\\").split("#")[0].split("/")[-1]
                if target and target not in valid_slugs:
                    issues["broken_links"].append(f"{rel} → [[{link}]]")

        # Meta-Seiten von Frontmatter-/Orphan-Checks ausnehmen
        if slug in META_PAGES:
            continue

        # Orphans (keine eingehenden Links). Übersichts-Seiten sind absichtlich nur
        # vom Index aus erreichbar.
        if slug not in incoming or len(incoming[slug]) == 0:
            if slug not in {"FAKT_II_Uebersicht", "Kombinationstabelle", "Nutzcodeliste"}:
                issues["orphans"].append(rel)

        # Frontmatter-Pflichtfelder
        missing = REQUIRED_FRONTMATTER - set(fm.keys())
        if missing:
            issues["frontmatter_missing"].append(f"{rel}: fehlt {sorted(missing)}")

        # Type-Wert
        if fm.get("type") and fm["type"] not in ALLOWED_TYPES:
            issues["frontmatter_invalid"].append(f"{rel}: type='{fm['type']}' nicht in {sorted(ALLOWED_TYPES)}")

        # Tags in Taxonomie?
        for t in fm.get("tags") or []:
            if t not in taxonomy:
                issues["tag_unknown"].append(f"{rel}: '{t}' nicht in SCHEMA.md")

        # Sources existieren in raw/?
        for s in fm.get("sources") or []:
            if nfc(s) not in known_raw:
                issues["source_missing"].append(f"{rel}: '{s}' nicht in raw/")

        # Page-Size
        if p["lines"] > 200:
            issues["page_too_large"].append(f"{rel}: {p['lines']} Zeilen")

        # TODO-Marker
        for todo in TODO_RE.findall(p["body"]):
            issues["todo"].append(f"{rel}: {todo[:80]}")

        # Confidence/contested
        if fm.get("confidence") == "low":
            issues["confidence_low"].append(rel)
        if fm.get("contested"):
            issues["contested"].append(rel)

    return issues


SEVERITY = [
    ("broken_links", "BROKEN WIKILINKS"),
    ("frontmatter_missing", "FRONTMATTER unvollständig"),
    ("frontmatter_invalid", "FRONTMATTER ungültiger Wert"),
    ("source_missing", "QUELLE nicht in raw/"),
    ("tag_unknown", "TAG nicht in Taxonomie"),
    ("orphans", "ORPHAN-Pages (kein Backlink)"),
    ("page_too_large", "SEITE > 200 Zeilen (Split-Kandidat)"),
    ("contested", "CONTESTED — ungelöster Widerspruch"),
    ("confidence_low", "CONFIDENCE: low"),
    ("todo", "TODO-Marker"),
]

CRITICAL = {"broken_links", "frontmatter_missing", "frontmatter_invalid", "source_missing", "tag_unknown"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true",
                    help="Exit-Code 1 schon bei Warnings (orphans, todo, large)")
    args = ap.parse_args()

    taxonomy = load_taxonomy()
    known_raw = load_known_raw()
    pages = load_pages()

    print(f"Geprüfte Seiten: {len(pages)}, Tag-Taxonomie: {len(taxonomy)}, raw-Dateien: {len(known_raw)}\n")

    issues = lint(pages, taxonomy, known_raw)

    has_critical = False
    for key, label in SEVERITY:
        items = issues.get(key, [])
        if not items:
            continue
        marker = "❌" if key in CRITICAL else "⚠ "
        print(f"{marker} {label} ({len(items)})")
        for it in items[:30]:
            print(f"    {it}")
        if len(items) > 30:
            print(f"    ... und {len(items)-30} weitere")
        print()
        if key in CRITICAL:
            has_critical = True

    if not any(issues.values()):
        print("✅ Keine Auffälligkeiten.")

    if has_critical or (args.strict and any(issues.values())):
        sys.exit(1)


if __name__ == "__main__":
    main()
