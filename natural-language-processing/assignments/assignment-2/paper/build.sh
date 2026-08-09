#!/usr/bin/env bash
# Build the paper. Run from the paper/ directory:  ./build.sh
#
# Four passes are needed, and that is not a mistake:
#   1. pdflatex  writes out which citations and cross-references were used
#   2. bibtex    turns the citations into a formatted bibliography
#   3. pdflatex  pulls the bibliography in
#   4. pdflatex  fixes the numbers that step 3 just shifted
#
# Everything intermediate goes into .build/ and only the finished PDF is copied
# out. That keeps the source folder clean, and it stops a stale main.aux in
# this directory from shadowing a fresh one (which silently breaks every
# \ref and \cite in the document).
set -e

# MiKTeX installs per-user and is not always on PATH in a fresh shell.
MIKTEX="$LOCALAPPDATA/Programs/MiKTeX/miktex/bin/x64"
[ -d "$MIKTEX" ] && export PATH="$MIKTEX:$PATH"

command -v pdflatex >/dev/null || { echo "pdflatex not found. See README.md"; exit 1; }

OUT=.build
mkdir -p "$OUT"

run() { pdflatex -interaction=nonstopmode -file-line-error -output-directory="$OUT" main.tex >/dev/null; }

echo "[1/4] pdflatex"; run
echo "[2/4] bibtex  "; bibtex "$OUT/main" >/dev/null || echo "  (bibtex warnings, continuing)"
echo "[3/4] pdflatex"; run
echo "[4/4] pdflatex"; run

# Adobe Acrobat holds an exclusive write lock on any PDF it has open, so
# copying the result out can fail through no fault of the document.
if ! cp "$OUT/main.pdf" main.pdf 2>/dev/null; then
  echo
  echo "  Built OK, but could not write main.pdf - it is open in a PDF viewer."
  echo "  The fresh copy is at $OUT/main.pdf"
  echo
  echo "  Fix this for good: close Adobe Reader and preview the PDF inside"
  echo "  VS Code instead (Ctrl+Alt+V). The built-in viewer does not lock the"
  echo "  file, so you can keep it open while you write."
  exit 1
fi

# pdfinfo ships with poppler and is not always present, so fall back to
# counting page objects in the PDF itself.
PAGES=$(pdfinfo main.pdf 2>/dev/null | awk '/^Pages/{print $2}')
[ -z "$PAGES" ] && PAGES=$(grep -c "/Type[[:space:]]*/Page[^s]" main.pdf 2>/dev/null || true)
echo
echo "Built main.pdf ($(du -h main.pdf | cut -f1)${PAGES:+, $PAGES pages})"

if grep -qi "undefined" "$OUT/main.log"; then
  echo
  echo "Undefined references or citations:"
  grep -i "undefined" "$OUT/main.log" | sort -u | sed 's/^/  /'
else
  echo "No undefined references or citations."
fi
