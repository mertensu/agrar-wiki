#!/bin/bash
# Split "GA - Erlaeuterungen und Ausfuellhinweise 2026.pdf" (102 S.)
# nach Hauptkapiteln mit +1-Seiten-Überlappung.
#
# Voraussetzung: qpdf (brew install qpdf)

set -euo pipefail

INPUT="raw/GA - Erlaeuterungen und Ausfuellhinweise 2026.pdf"
OUTDIR="raw/ga_erlaeuterungen"

mkdir -p "$OUTDIR"

# Kapitel-Splits (Start-Ende inkl. +1 Überlappung)
# Kap 1-3: Allgemeines, Antragstellung, Stammdaten (S. 9-16)
qpdf --warning-exit-0 "$INPUT" --pages . 9-17 -- "$OUTDIR/ga_01-03_allgemeines.pdf"

# Kap 4: Flächenangaben (S. 17-34)
qpdf --warning-exit-0 "$INPUT" --pages . 17-35 -- "$OUTDIR/ga_04_flaechenangaben.pdf"

# Kap 5: Direktzahlungen + Öko-Regelungen (S. 34-47)
qpdf --warning-exit-0 "$INPUT" --pages . 34-48 -- "$OUTDIR/ga_05_direktzahlungen_oer.pdf"

# Kap 6-7.1: Hopfen + FAKT II (S. 48-78) - Kernkapitel!
qpdf --warning-exit-0 "$INPUT" --pages . 48-79 -- "$OUTDIR/ga_07_fakt2.pdf"

# Kap 7.2-7.4: AZL, LPR-A, UZW (S. 79-83)
qpdf --warning-exit-0 "$INPUT" --pages . 79-84 -- "$OUTDIR/ga_07b_azl_lpr_uzw.pdf"

# Kap 8-11: UuU, Cross Compliance, PHW, HWB (S. 84-87)
qpdf --warning-exit-0 "$INPUT" --pages . 84-88 -- "$OUTDIR/ga_08-11_uuu_phw_hwb.pdf"

# Kap 12-16: SchALVO, Steillagen, De-minimis, EAPS, MGV (S. 87-95)
qpdf --warning-exit-0 "$INPUT" --pages . 87-96 -- "$OUTDIR/ga_12-16_schalvo_slg_deminimis_mgv.pdf"

# Kap 17-19: Fristen/Sanktionen, Konditionalität (S. 95-102)
qpdf --warning-exit-0 "$INPUT" --pages . 95-102 -- "$OUTDIR/ga_17-19_fristen_konditionalitaet.pdf"

echo "Split fertig. Dateien in $OUTDIR/:"
ls -la "$OUTDIR/"
