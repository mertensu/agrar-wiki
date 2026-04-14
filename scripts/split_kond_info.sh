#!/usr/bin/env bash
# Splittet Kond_Infobroschuere_2026.pdf nach Hauptkapiteln.
# Seitenranges mit +1-Überlappung an Kapitelgrenzen.

set -uo pipefail

SRC="raw/konditionalitaet/Kond_Infobroschuere_2026.pdf"

# qpdf gibt Exit-Code 3 bei harmlosen Warnungen (z.B. fehlender xref-Eintrag).
# Wrapper: nur bei echten Fehlern (exit > 3) abbrechen.
run_qpdf() {
  qpdf "$@"
  local rc=$?
  if [ $rc -gt 3 ]; then
    echo "qpdf Fehler (exit $rc)" >&2
    exit $rc
  fi
}
OUT="raw/konditionalitaet"

if [ ! -f "$SRC" ]; then
  echo "Fehler: $SRC nicht gefunden. Bitte aus dem Projektroot ausführen."
  exit 1
fi

# I.   Einleitung                                    S. 1–3   (+1 = 4)
run_qpdf "$SRC" --pages . 1-4 -- "$OUT/kond_I_einleitung.pdf"

# II.  GLÖZ (Erhaltung ldw. Flächen)                 S. 4–19  (+1 = 20)
run_qpdf "$SRC" --pages . 4-21 -- "$OUT/kond_II_gloez.pdf"

# III. Grundanforderungen Betriebsführung (GAB)       S. 20–56 (+1 = 57)
run_qpdf "$SRC" --pages . 20-57 -- "$OUT/kond_III_gab.pdf"

# IV.  Kontroll- und Sanktionssystem                  S. 57–60 (+1 = 61)
run_qpdf "$SRC" --pages . 57-62 -- "$OUT/kond_IV_kontrolle.pdf"

# V.   Anlagen                                        S. 61–75 (+1 = 76)
run_qpdf "$SRC" --pages . 61-76 -- "$OUT/kond_V_anlagen.pdf"

# VI.  Weitere Informationen                          S. 76–Ende
run_qpdf "$SRC" --pages . 76 -- "$OUT/kond_VI_weitere_info.pdf"

echo "Fertig. Gesplittete PDFs in $OUT/"
ls -lh "$OUT"/kond_*.pdf
