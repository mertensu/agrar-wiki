#!/usr/bin/env bash
# Split: Empfehlungen für ackerbauliche FAKT II-Maßnahmen (48 Seiten)
# Quelle: downloads/formulare_2026/Empfehlungen_für_ackerbauliche_FAKT_II-Maßnahmen_E1.2_E7-E9_E13_E14_E15_F3_F4.pdf
#
# Kapitelstruktur laut Inhaltsverzeichnis (S. 2):
#   Kap 1: Einleitung (S. 3–4)
#   Kap 2: E1.2 Begrünungsmischungen (S. 5–9)
#   Kap 3: E7/E8 Blühmischungen + Brachebegrünung (S. 10–15)
#   Kap 4: E9 Mais/Stangenbohnen (S. 16–17)
#   Kap 5: E13.1/E13.2 Drillreihenabstand (S. 18–20)
#   Kap 6: E14/E15 Biomassepflanzen (S. 21–23)
#   Kap 7: F3 Precision Farming (S. 24–27)
#   Kap 8: F4 Strip Till (S. 28–29)
#   Anhang: Abbildungen + Tabellen (S. 30–47)
#   Impressum (S. 48 – ignoriert)
#
# +1-Seite-Regel: Jeder Split nimmt eine Seite über die Kapitelgrenze hinaus mit.

set -uo pipefail
# qpdf gibt Exit-Code 3 bei Warnungen zurück – das ist OK

SRC="downloads/formulare_2026/Empfehlungen_für_ackerbauliche_FAKT_II-Maßnahmen_E1.2_E7-E9_E13_E14_E15_F3_F4.pdf"
OUT="downloads/formulare_2026/splits"

mkdir -p "$OUT"

# Kap 1+2: Einleitung + E1.2 (S. 1–10, +1 über S.9)
qpdf "$SRC" --pages . 1-10 -- "$OUT/empf_1_einleitung_E1.2.pdf"

# Kap 3: E7/E8 Blühmischungen (S. 10–16, +1 über S.15)
qpdf "$SRC" --pages . 10-16 -- "$OUT/empf_2_E7_E8_blueh.pdf"

# Kap 4: E9 Mais/Stangenbohnen (S. 16–18, +1 über S.17)
qpdf "$SRC" --pages . 16-18 -- "$OUT/empf_3_E9_mais.pdf"

# Kap 5: E13.1/E13.2 Drillreihenabstand (S. 18–21, +1 über S.20)
qpdf "$SRC" --pages . 18-21 -- "$OUT/empf_4_E13_drillreihen.pdf"

# Kap 6: E14/E15 Biomassepflanzen (S. 21–24, +1 über S.23)
qpdf "$SRC" --pages . 21-24 -- "$OUT/empf_5_E14_E15_biomasse.pdf"

# Kap 7: F3 Precision Farming (S. 24–28, +1 über S.27)
qpdf "$SRC" --pages . 24-28 -- "$OUT/empf_6_F3_precision.pdf"

# Kap 8: F4 Strip Till (S. 28–30, +1 über S.29)
qpdf "$SRC" --pages . 28-30 -- "$OUT/empf_7_F4_strip_till.pdf"

# Anhang: Tabellen + Abbildungen (S. 30–47)
qpdf "$SRC" --pages . 30-47 -- "$OUT/empf_8_anhang.pdf"

echo "Split fertig. Dateien in $OUT:"
ls -lh "$OUT"
