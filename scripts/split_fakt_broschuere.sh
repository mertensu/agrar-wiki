#!/usr/bin/env bash
# Split: FAKT II Broschüre (47 Seiten)
# Quelle: downloads/formulare_2026/FAKT_II_-_Broschüre.pdf
# → raw/FAKT_II_Broschuere.pdf (Original)
#
# Struktur:
#   Teil 1: Allgemeine Infos + Antragstellung (S. 1–8)
#   Teil 2: Übersichtstabelle Maßnahmen (S. 9–10)
#   Teil 3: Kurzbeschreibungen A2–G7 (S. 11–47)
#
# Diese Splits reproduzieren die manuell erstellten fakt_broschuere_1/2/3.pdf.
# +1-Seite-Regel angewendet.

set -uo pipefail

SRC="raw/FAKT_II_Broschuere.pdf"

# Teil 1: Allgemeine Infos + Antragstellung (S. 1–9, +1 über S.8)
qpdf "$SRC" --pages . 1-9 -- "raw/fakt_broschuere_1.pdf"

# Teil 2: Übersichtstabelle (S. 9–11, +1 über S.10)
qpdf "$SRC" --pages . 9-11 -- "raw/fakt_broschuere_2.pdf"

# Teil 3: Kurzbeschreibungen (S. 11–47)
qpdf "$SRC" --pages . 11-47 -- "raw/fakt_broschuere_3.pdf"

echo "Split fertig. Dateien:"
ls -lh raw/fakt_broschuere_*.pdf
