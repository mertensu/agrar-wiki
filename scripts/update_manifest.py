#!/usr/bin/env python3
"""
Pflegt raw/manifest.json – ein SHA256-Manifest aller Rohdateien in raw/.

Zweck: Änderungen an Quelldateien erkennen, die sonst unbemerkt bleiben
(z.B. MLR veröffentlicht aktualisierte Broschüre unter gleichem Namen).

Verwendung:
    python3 scripts/update_manifest.py              # Drift prüfen, neue Dateien eintragen
    python3 scripts/update_manifest.py --check      # Nur prüfen, nichts schreiben (exit 1 bei Drift)

Was drift bedeutet:
- Hash-Mismatch → Datei wurde geändert → Wiki-Seiten prüfen
- Neue Datei → wird ins Manifest aufgenommen
- Fehlende Datei → im Manifest markiert, aber nicht automatisch entfernt
"""

import argparse
import datetime as dt
import hashlib
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, "raw")
MANIFEST = os.path.join(RAW, "manifest.json")

# Dateien/Verzeichnisse, die nicht ins Manifest gehören (Cache, Hilfs-Ordner)
SKIP_NAMES = {"manifest.json", ".DS_Store"}
SKIP_SUFFIXES = {".json"}  # extraktions-Caches wie kond_extracted.json
SKIP_DIRS = {"help"}


def sha256_of(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def iter_raw_files():
    for root, dirs, files in os.walk(RAW):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if name in SKIP_NAMES:
                continue
            if any(name.endswith(s) for s in SKIP_SUFFIXES):
                continue
            full = os.path.join(root, name)
            rel = os.path.relpath(full, RAW)
            yield rel, full


def load_manifest() -> dict:
    if not os.path.exists(MANIFEST):
        return {}
    with open(MANIFEST) as f:
        return json.load(f)


def save_manifest(data: dict) -> None:
    with open(MANIFEST, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true",
                        help="Nur prüfen, nichts schreiben. Exit 1 bei Drift.")
    args = parser.parse_args()

    manifest = load_manifest()
    today = dt.date.today().isoformat()

    drift, new, missing = [], [], []
    seen = set()

    for rel, full in iter_raw_files():
        seen.add(rel)
        actual = sha256_of(full)
        entry = manifest.get(rel)
        if entry is None:
            new.append(rel)
            if not args.check:
                manifest[rel] = {"sha256": actual, "ingested": today}
        elif entry.get("sha256") != actual:
            drift.append((rel, entry.get("sha256", "?")[:12], actual[:12]))
            if not args.check:
                manifest[rel] = {
                    **entry,
                    "sha256": actual,
                    "previous_sha256": entry.get("sha256"),
                    "updated": today,
                }

    for rel in manifest.keys():
        if rel not in seen:
            missing.append(rel)

    if new:
        print(f"Neu ({len(new)}):")
        for r in new:
            print(f"  + {r}")
    if drift:
        print(f"\nDRIFT ({len(drift)}) – Inhalt hat sich geändert:")
        for r, old, new_h in drift:
            print(f"  ! {r}  {old}… → {new_h}…")
    if missing:
        print(f"\nFehlt ({len(missing)}) – im Manifest, aber nicht mehr auf Platte:")
        for r in missing:
            print(f"  - {r}")

    if not (new or drift or missing):
        print("Manifest konsistent – keine Änderungen.")

    if args.check:
        sys.exit(1 if drift else 0)

    save_manifest(manifest)
    print(f"\nManifest geschrieben: {MANIFEST}")


if __name__ == "__main__":
    main()
