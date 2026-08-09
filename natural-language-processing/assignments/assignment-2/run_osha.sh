#!/usr/bin/env bash
# Task 4 - one-command setup and launch for the BITS OSHA Virtual Lab.
#
# Owner: Member 4 (Application & DevOps Engineer).
#
#   ./run_osha.sh              set up, verify, launch Streamlit
#   ./run_osha.sh flask        launch the Flask app instead
#   ./run_osha.sh verify       only run the self-check
#   ./run_osha.sh train        fine-tune the model first
#
# The lab may be offline. If so, copy `models/t5-review-summarizer/` and the
# NLTK `vader_lexicon` across by hand; this script checks for both and says
# what is missing rather than failing halfway through.

set -euo pipefail
cd "$(dirname "$0")"

PY="${PYTHON:-python3}"
command -v "$PY" >/dev/null 2>&1 || PY=python

echo "==> using $($PY --version 2>&1)"

# ---- virtual environment ------------------------------------------------
if [ ! -d ".venv" ]; then
  echo "==> creating .venv"
  "$PY" -m venv .venv
fi
# shellcheck disable=SC1091
if [ -f ".venv/bin/activate" ]; then
  . .venv/bin/activate                 # Linux / macOS
else
  . .venv/Scripts/activate             # Git Bash on Windows
fi

# ---- dependencies -------------------------------------------------------
echo "==> installing dependencies"
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt

# ---- offline assets -----------------------------------------------------
if [ ! -d "models/t5-review-summarizer" ]; then
  echo "!!  no fine-tuned model found."
  echo "    Online : run './run_osha.sh train' (about 2 hours on CPU)"
  echo "    Offline: copy models/t5-review-summarizer/ into this folder"
  echo "    The app still runs meanwhile, using plain t5-small."
fi

python - <<'EOF' || true
import nltk
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
    print("==> VADER lexicon present")
except LookupError:
    print("==> downloading VADER lexicon")
    try:
        nltk.download("vader_lexicon", quiet=True)
    except Exception:
        print("!!  download failed (offline?). A built-in word list will be "
              "used instead, so the app still runs.")
EOF

# ---- go -----------------------------------------------------------------
case "${1:-streamlit}" in
  verify) python verify.py --trace ;;
  train)  python train_t5.py ;;
  flask)  echo "==> Flask on http://localhost:5000"; python flask_app.py ;;
  *)      echo "==> self-check"; python verify.py
          echo "==> Streamlit on http://localhost:8501"
          python -m streamlit run app.py \
            --server.port 8501 --server.headless true ;;
esac
