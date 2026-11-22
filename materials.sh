#!/usr/bin/env bash
# Third-party course material (handouts, slides, past papers, transcripts, labware)
# is NOT in this public repo. It lives in the private repo ravirajladha/ai-ml-materials,
# checked out on top of this folder (same paths) through a separate git dir next to it.
#
#   bash materials.sh init     # first time on a machine: clone + write files into this tree
#   bash materials.sh pull     # get material added on the other machine
#   bash materials.sh push     # commit + push new/changed material from this machine
#   bash materials.sh status   # what would be pushed
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
GD="$ROOT/../ai-ml-materials.git"
URL="git@github.com:ravirajladha/ai-ml-materials.git"
PATTERN='(^|/)(materials|transcript|books|handouts|labware|lecture-slides|past-question-papers|old-batch-slides)/'
g() { git --git-dir="$GD" --work-tree="$ROOT" "$@"; }

candidates() {  # ignored-by-public-repo files that belong to the material set
  git -C "$ROOT" -c core.quotepath=off ls-files --others --ignored --exclude-standard \
    | grep -E "$PATTERN" | grep -v -E '\.md$|/\.gitkeep$' \
    | while IFS= read -r f; do  # GitHub rejects files over 100 MB: copy those by hand
        if [ "$(wc -c < "$ROOT/$f")" -gt 95000000 ]; then echo "skip (>95 MB): $f" >&2; else echo "$f"; fi
      done || true
}

case "${1:-}" in
  init)
    [ -d "$GD" ] || git clone --bare "$URL" "$GD"
    g config core.bare false
    g config status.showUntrackedFiles no
    g config core.autocrlf false
    g config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*'
    printf '* -filter -diff -merge -text\n' > "$GD/info/attributes"   # real bytes, no LFS
    g fetch -q origin
    g reset -q origin/main
    g checkout -- .
    echo "materials: $(g ls-files | wc -l) files in place" ;;
  pull)
    g pull --ff-only origin main ;;
  status)
    candidates | while IFS= read -r f; do g ls-files --error-unmatch -- "$f" >/dev/null 2>&1 || echo "new: $f"; done
    g status --short ;;
  push)
    candidates | tr '\n' '\0' | g add -f --pathspec-from-file=- --pathspec-file-nul
    g add -u
    if g diff --cached --quiet; then echo "materials: nothing to push"; exit 0; fi
    g commit -q -m "${2:-Materials sync $(date +%F)}"
    g push -q origin main
    echo "materials: pushed" ;;
  *) sed -n '2,10p' "$0"; exit 1 ;;
esac
