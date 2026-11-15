"""Check one deep subject bank: structure + run every code snippet.

Usage (use the Anaconda Python, it has numpy/pandas/sklearn/torch):
    C:/ProgramData/anaconda3/python.exe check_subject.py np-arrays [more slugs...]
    C:/ProgramData/anaconda3/python.exe check_subject.py --all

Code rules checked:
  * code_output: stdout of the snippet (trailing newline stripped) must equal the answer.
    If the snippet raises, the expected answer is the exception class name, e.g. "KeyError"
    (any printed lines before it come first, one per line).
  * every other snippet (code shown with an mcq/tf/fill) must at least run without error,
    unless the question sets lang="text" / "bash" / "sql" (then it isn't executed).
  * snippets run twice under different PYTHONHASHSEED values; the output must be identical
    (catches set-ordering and unseeded randomness).
"""
import contextlib
import io
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "content"))

import build_seed  # noqa: E402

TARGETS = {1: 15, 2: 15, 3: 12, 4: 8}   # minimum questions per level for a deep subject


def run_snippet(code):
    import matplotlib
    matplotlib.use("Agg")
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(code, "<snippet>", "exec"), {"__name__": "__snippet__"})
    except BaseException as e:  # noqa: BLE001
        out = buf.getvalue().rstrip("\n")
        return (out + "\n" if out else "") + type(e).__name__, True
    finally:
        try:
            import matplotlib.pyplot as plt
            plt.close("all")
        except Exception:
            pass
    return buf.getvalue().rstrip("\n"), False


def worker(slugs):
    """Run all snippets for the slugs, print JSON {key: [output, raised]}."""
    import warnings
    warnings.filterwarnings("ignore")
    results = {}
    for slug in slugs:
        mod = build_seed.load_subject_file(build_seed.SUBJECT_DIR / f"{slug}.py")
        for i, q in enumerate(mod.QUESTIONS):
            if q["code"] and (q["lang"] or "python") == "python":
                results[f"{slug}#{i}"] = run_snippet(q["code"])
    sys.stdout = sys.__stdout__
    print("@@RESULT@@" + json.dumps(results))


def run_workers(slugs):
    outs = []
    for seed in ("0", "12345"):
        env = dict(os.environ, PYTHONHASHSEED=seed, PYTHONIOENCODING="utf-8")
        p = subprocess.run([sys.executable, __file__, "--worker", *slugs], capture_output=True,
                           text=True, encoding="utf-8", env=env, cwd=str(HERE))
        marker = p.stdout.rfind("@@RESULT@@")
        if marker < 0:
            raise SystemExit(f"worker crashed:\n{p.stdout[-2000:]}\n{p.stderr[-4000:]}")
        outs.append(json.loads(p.stdout[marker + len("@@RESULT@@"):]))
    return outs


def check(slugs):
    names = {s[0]: s for s in build_seed.SUBJECTS}
    ok = True
    for slug in slugs:
        if slug not in names:
            print(f"[{slug}] not in content/structure.py SUBJECTS"); ok = False; continue
        path = build_seed.SUBJECT_DIR / f"{slug}.py"
        if not path.exists():
            print(f"[{slug}] missing {path}"); ok = False; continue
        if not (build_seed.SPEC_DIR / f"{slug}.md").exists():
            print(f"[{slug}] missing specs/{slug}.md"); ok = False
        mod = build_seed.load_subject_file(path)
        tslugs = {t[0] for t in mod.TOPICS}
        errs = build_seed.validate_questions(slug, mod.QUESTIONS, tslugs)
        for e in errs:
            print("  " + e)
        ok &= not errs
        levels = Counter(q["level"] for q in mod.QUESTIONS)
        per_topic = Counter(q["topic"] for q in mod.QUESTIONS)
        empty = [t for t in tslugs if not per_topic[t]]
        short = {lv: n for lv, n in TARGETS.items() if levels[lv] < n}
        print(f"[{slug}] {len(mod.QUESTIONS)} questions | levels "
              + " ".join(f"L{lv}={levels[lv]}" for lv in (1, 2, 3, 4))
              + f" | topics {len(tslugs)}" + (f" | EMPTY topics: {empty}" if empty else "")
              + (f" | BELOW TARGET: {short}" if short else ""))
        if empty or short:
            ok = False

    run_a, run_b = run_workers([s for s in slugs if (build_seed.SUBJECT_DIR / f"{s}.py").exists()])
    bad = 0
    for slug in slugs:
        path = build_seed.SUBJECT_DIR / f"{slug}.py"
        if not path.exists():
            continue
        mod = build_seed.load_subject_file(path)
        for i, q in enumerate(mod.QUESTIONS):
            key = f"{slug}#{i}"
            if key not in run_a:
                continue
            got, raised = run_a[key]
            label = f"  [{slug} q{i}] {q['question'][:60]!r}"
            if run_b[key] != run_a[key]:
                print(f"{label}\n      NON-DETERMINISTIC output: {got!r} vs {run_b[key][0]!r}"); bad += 1
            elif q["qtype"] == "code_output" and got != q["answer"]:
                print(f"{label}\n      expected {q['answer']!r}\n      actual   {got!r}"); bad += 1
            elif q["qtype"] != "code_output" and raised:
                print(f"{label}\n      snippet raised {got.splitlines()[-1]}"); bad += 1
    print(f"snippets checked: {len(run_a)}, problems: {bad}")
    return ok and bad == 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--worker":
        worker(args[1:])
        sys.exit(0)
    if args == ["--all"]:
        args = sorted(p.stem for p in build_seed.SUBJECT_DIR.glob("*.py"))
    if not args:
        print(__doc__); sys.exit(2)
    sys.exit(0 if check(args) else 1)
