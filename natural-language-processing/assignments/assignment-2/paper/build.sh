#!/usr/bin/env bash
# Build the paper. Run from the paper/ directory:  ./build.sh
#
# Four passes are needed, and that is not a mistake:
#   1. pdflatex  writes out which citations were used
#   2. bibtex    turns those into a formatted bibliography
#   3. pdflatex  pulls the bibliography in
#   4. pdflatex  fixes the page numbers the bibliography just shifted
set -e

# MiKTeX installs per-user and is not always on PATH in a fresh shell.
MIKTEX="$LOCALAPPDATA/Programs/MiKTeX/miktex/bin/x64"
[ -d "$MIKTEX" ] && export PATH="$MIKTEX:$PATH"

command -v pdflatex >/dev/null || { echo "pdflatex not found. See README.md"; exit 1; }

echo "[1/4] pdflatex"; pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
echo "[2/4] bibtex  "; bibtex main >/dev/null || echo "  (bibtex warnings, continuing)"
echo "[3/4] pdflatex"; pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
echo "[4/4] pdflatex"; pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null

echo
echo "Built main.pdf ($(du -h main.pdf | cut -f1), $(pdfinfo main.pdf 2>/dev/null | awk '/^Pages/{print $2}' || echo '?') pages)"
echo "Undefined references / citations:"
grep -c "undefined" main.log || echo "  none"
