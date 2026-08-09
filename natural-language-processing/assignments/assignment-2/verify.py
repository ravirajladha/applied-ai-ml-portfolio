"""Self-check for the Customer Review Summarization project.

Run this first, on any machine, before trusting anything else:

    python verify.py            # check everything works, print PASS/FAIL
    python verify.py --trace    # also walk the pipeline stage by stage

Exits 0 if everything passed, 1 if anything failed, so it can be used in CI.
"""

from __future__ import annotations

import sys

# Windows consoles default to cp1252, which cannot print the sub-word marker
# T5's tokenizer uses. Force UTF-8 and never crash on an unprintable
# character - a diagnostic tool must not fail for a cosmetic reason.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

import argparse
import os
import platform
import textwrap
import warnings

warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)          # so this runs from any working directory

PASS, FAIL, WARN = [], [], []


def check(name, fn, required=True):
    """Run one check and record the result."""
    try:
        detail = fn()
        print(f"  [ OK ]  {name}" + (f"  -  {detail}" if detail else ""))
        PASS.append(name)
    except Exception as exc:
        tag = "FAIL" if required else "WARN"
        (FAIL if required else WARN).append(name)
        print(f"  [{tag}]  {name}\n          {type(exc).__name__}: {exc}")


# ---------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------

def c_python():
    if sys.version_info < (3, 10):
        raise RuntimeError(f"need Python 3.10+, found {sys.version.split()[0]}")
    return f"{sys.version.split()[0]} on {platform.machine()}"


def c_packages():
    import importlib.metadata as md
    missing, versions = [], []
    for pkg, mod in [("torch", "torch"), ("transformers", "transformers"),
                     ("scikit-learn", "sklearn"), ("nltk", "nltk"),
                     ("pandas", "pandas"), ("streamlit", "streamlit")]:
        try:
            __import__(mod)
            versions.append(f"{pkg} {md.version(pkg)}")
        except Exception:
            missing.append(pkg)
    if missing:
        raise RuntimeError(f"missing: {', '.join(missing)} - run "
                           f"`pip install -r requirements.txt`")
    return " | ".join(versions[:3]) + " ..."


def c_import():
    import summarizer                                    # noqa: F401
    return "summarizer.py imports cleanly"


def c_clean():
    """Cleaning must normalise text WITHOUT destroying possessives.

    Regression test: "'s" used to be expanded blindly, turning
    "a baby cow's milk" into "a baby cow is milk" before the model saw it.
    """
    from summarizer import clean_text
    cases = [
        ("a baby cow's milk", "cow's", "possessive must survive"),
        ("it's great", "it is", "'it's' must expand"),
        ("don't buy this", "do not", "'n't' must expand"),
        ("<br />Great &amp; fast", "great", "html must be stripped"),
        ("see https://x.co now", "see now", "urls must be stripped"),
    ]
    for text, expected, why in cases:
        got = clean_text(text)
        if expected not in got:
            raise AssertionError(f"{why}: {text!r} -> {got!r}")
    if clean_text(None) != "" or clean_text("") != "":
        raise AssertionError("clean_text must tolerate empty/None input")
    return f"{len(cases)} text rules hold"


def c_split():
    from summarizer import split_reviews, split_sentences
    two = split_reviews("First review, long enough to count here.\n\n"
                        "Second review, also long enough to count.")
    one_each = split_reviews("First review, long enough to count here.\n"
                             "Second review, also long enough to count.")
    if len(two) != 2 or len(one_each) != 2:
        raise AssertionError(f"expected 2 reviews, got {len(two)}/{len(one_each)}")
    if split_reviews("") != [] or split_reviews("   ") != []:
        raise AssertionError("empty input must give an empty list")
    if len(split_sentences("One sentence here. And a second one here.")) != 2:
        raise AssertionError("sentence splitting failed")
    return "blank-line, per-line and empty inputs all handled"


def c_data():
    need = ["data/sample_reviews.csv", "data/test_reviews.csv"]
    missing = [f for f in need if not os.path.exists(os.path.join(HERE, f))]
    if missing:
        raise FileNotFoundError(f"{', '.join(missing)} - run `python train.py`")
    import pandas as pd
    n = len(pd.read_csv(os.path.join(HERE, "data/sample_reviews.csv")))
    return f"sample product has {n} reviews"


def c_model_files():
    from summarizer import MODEL_DIR
    if not os.path.isdir(MODEL_DIR):
        raise FileNotFoundError(
            "no fine-tuned model - run `python train.py`. "
            "(The app still works, falling back to plain t5-small.)")
    mb = sum(os.path.getsize(os.path.join(MODEL_DIR, f))
             for f in os.listdir(MODEL_DIR)) / 1e6
    return f"{mb:.0f} MB in models/t5-review-summarizer"


def c_generate():
    from summarizer import ReviewSummarizer
    s = ReviewSummarizer()
    out = s.summarize(["The coffee tastes wonderful and arrived very quickly, "
                       "great value for the price and I will order it again."])
    if not out or not out[0].strip():
        raise AssertionError("model produced an empty summary")
    globals()["_SUMMARIZER"] = s
    kind = "fine-tuned" if s.is_finetuned else "base t5-small (not fine-tuned)"
    return f"{kind} -> {out[0]!r}"


def c_aspects():
    """Praise and criticism must not collapse into the same word list."""
    from summarizer import analyse_aspects
    reviews = [
        "The flavor is rich and the aroma is lovely, delicious every morning.",
        "Wonderful flavor and a great price, much better than the shop.",
        "The aroma and flavor are excellent, worth every penny.",
        "Packaging was crushed and damaged when the box arrived.",
        "Terrible packaging, the box arrived crushed and broken again.",
        "The packaging is awful and the seal was damaged on arrival.",
    ]
    r = analyse_aspects(reviews, top_k=5)
    pos = {a for a, _ in r.positive_aspects}
    neg = {a for a, _ in r.negative_aspects}
    if not pos or not neg:
        raise AssertionError(f"empty aspect list (pos={pos}, neg={neg})")
    if pos & neg:
        raise AssertionError(f"same word on both sides: {pos & neg}")
    if r.n_positive == 0 or r.n_negative == 0:
        raise AssertionError("sentiment split found only one polarity")
    return f"praised {sorted(pos)} vs criticised {sorted(neg)}"


def c_app():
    import py_compile
    py_compile.compile(os.path.join(HERE, "app.py"), doraise=True)
    py_compile.compile(os.path.join(HERE, "train.py"), doraise=True)
    return "app.py and train.py compile"


def c_notebook():
    import nbformat
    nb = nbformat.read(os.path.join(HERE, "assignment2.ipynb"), as_version=4)
    errs = [o for c in nb.cells if c.cell_type == "code"
            for o in c.get("outputs", []) if o.output_type == "error"]
    if errs:
        raise AssertionError(f"{len(errs)} cell(s) have error output")
    figs = sum(1 for c in nb.cells for o in c.get("outputs", [])
               if "image/png" in o.get("data", {}))
    return f"{len(nb.cells)} cells, no errors, {figs} figures embedded"


# ---------------------------------------------------------------------
# Optional stage-by-stage trace
# ---------------------------------------------------------------------

def trace():
    import pandas as pd
    from summarizer import (MAX_INPUT_TOKENS, MAX_TARGET_TOKENS, TASK_PREFIX,
                            ReviewSummarizer, analyse_aspects,
                            build_overall_summary, clean_text, split_sentences)

    raw = pd.read_csv(os.path.join(HERE, "data/sample_reviews.csv"))["Text"]
    raw = raw.dropna().tolist()
    s = globals().get("_SUMMARIZER") or ReviewSummarizer()

    def head(n, t):
        print(f"\n{'='*72}\nSTAGE {n}: {t}\n{'='*72}")

    head(1, "INPUT - many reviews of one product")
    print(f"  {len(raw)} reviews loaded")
    print(textwrap.indent(textwrap.fill(raw[3][:240], 66), "    "))

    head(2, "CLEAN - clean_text()")
    print("  before:", repr(raw[3][:95]))
    print("  after :", repr(clean_text(raw[3])[:95]))
    print(f"  sentences: {len(split_sentences(clean_text(raw[3])))}")

    head(3, "TOKENIZE - text becomes numbers the encoder can read")
    ids = s.tokenizer(TASK_PREFIX + clean_text(raw[3]),
                      max_length=MAX_INPUT_TOKENS, truncation=True)["input_ids"]
    print(f"  prefix     : {TASK_PREFIX!r}   (tells T5 which task)")
    print(f"  tokens     : {len(ids)} (cap {MAX_INPUT_TOKENS})")
    print(f"  first few  : {s.tokenizer.convert_ids_to_tokens(ids[:10])}")

    head(4, f"GENERATE - encoder reads all, decoder writes <={MAX_TARGET_TOKENS}")
    for r, p in zip(raw[:5], s.summarize(raw[:5])):
        print(f"    review : {r[:70].replace(chr(10), ' ')}...")
        print(f"    SUMMARY: {p}\n")

    head(5, "AGGREGATE - analyse_aspects() across ALL reviews")
    rep = analyse_aspects(raw, top_k=6)
    print(f"  sentiment : {rep.n_positive} pos / {rep.n_negative} neg / "
          f"{rep.n_neutral} neutral")
    print(f"  praised   : {[a for a, _ in rep.positive_aspects]}")
    print(f"  criticised: {[a for a, _ in rep.negative_aspects]}")

    head(6, "REPORT - build_overall_summary(), what the app displays")
    print(textwrap.indent(
        textwrap.fill(build_overall_summary(s.summarize(raw), rep), 66), "  "))


# ---------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--trace", action="store_true",
                    help="walk the pipeline stage by stage after checking")
    args = ap.parse_args()

    print("Customer Review Summarization - self check")
    print("=" * 72)

    check("Python version", c_python)
    check("Required packages", c_packages)
    check("summarizer.py imports", c_import)
    check("Text cleaning rules", c_clean)
    check("Review/sentence splitting", c_split)
    check("Data files", c_data)
    check("Trained model present", c_model_files, required=False)
    check("Model loads and generates", c_generate)
    check("Aspect mining separates praise from criticism", c_aspects)
    check("app.py / train.py compile", c_app)
    check("Notebook executed cleanly", c_notebook, required=False)

    print("=" * 72)
    print(f"  {len(PASS)} passed, {len(FAIL)} failed, {len(WARN)} warnings")
    if WARN:
        print(f"  warnings (not fatal): {', '.join(WARN)}")
    if FAIL:
        print(f"  FAILED: {', '.join(FAIL)}")
        print("\n  Everything above that failed needs fixing before submitting.")
        return 1

    print("\n  All good - the project runs correctly on this machine.")
    if args.trace:
        trace()
    else:
        print("  Run `python verify.py --trace` to see the pipeline stage by stage.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
