"""Task 5 - ROUGE evaluation.

Owner: Member 5 (Evaluation Lead & Report Editor).

Scores every model we have against the same held-out reviews, so the
comparison is fair:

  Lead-1                   take the review's first sentence (trivial baseline)
  t5-small, not fine-tuned  shows what the fine-tuning actually bought
  Seq2Seq LSTM              Task 3.1 baseline, if it has been trained
  t5-small, fine-tuned      our model

Run:
    python evaluate_rouge.py                 # 300 held-out reviews
    python evaluate_rouge.py --n 100 --csv results.csv
"""

from __future__ import annotations

import argparse
import os

from config import BASE_MODEL, TEST_CSV, use_utf8_console
from data_prep import split_sentences


def load_test_set(n: int, path: str = TEST_CSV):
    import pandas as pd
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} missing - run `python train_t5.py`")
    df = pd.read_csv(path).head(n)
    return list(df["document"]), list(df["summary"])


def score(rouge, preds, refs, name: str) -> dict:
    r = rouge.compute(predictions=preds, references=refs, use_stemmer=True)
    print(f"  {name:<30} R1 {r['rouge1']:.4f} | R2 {r['rouge2']:.4f} "
          f"| RL {r['rougeL']:.4f}")
    return {"Model": name, "ROUGE-1": round(r["rouge1"], 4),
            "ROUGE-2": round(r["rouge2"], 4), "ROUGE-L": round(r["rougeL"], 4)}


def main() -> None:
    use_utf8_console()
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=300,
                    help="how many held-out reviews to score")
    ap.add_argument("--csv", default="", help="optional path to save results")
    ap.add_argument("--skip-baselines", action="store_true")
    args = ap.parse_args()

    import evaluate
    rouge = evaluate.load("rouge")

    docs, refs = load_test_set(args.n)
    print(f"Scoring {len(docs)} held-out reviews\n")
    results = []

    if not args.skip_baselines:
        # Trivial extractive baseline - the "did we beat doing nothing?" check.
        lead1 = [(split_sentences(d) or [d])[0] for d in docs]
        results.append(score(rouge, lead1, refs, "Lead-1 (extractive)"))

        from model_t5 import ReviewSummarizer
        base = ReviewSummarizer(BASE_MODEL)
        results.append(score(rouge, base.summarize(docs), refs,
                             "t5-small (not fine-tuned)"))

    # Task 3.1 baseline, only if someone has trained it.
    try:
        import infer_lstm
        if infer_lstm.available():
            lstm = infer_lstm.LSTMSummarizer()
            results.append(score(rouge, lstm.summarize(docs), refs,
                                 "Seq2Seq LSTM + attention"))
        else:
            print("  (Seq2Seq LSTM skipped - not trained yet)")
    except Exception as exc:
        print(f"  (Seq2Seq LSTM skipped - {type(exc).__name__}: {exc})")

    from model_t5 import ReviewSummarizer
    ours = ReviewSummarizer()
    label = ("t5-small (fine-tuned)" if ours.is_finetuned
             else "t5-small (NOT fine-tuned - train it first!)")
    results.append(score(rouge, ours.summarize(docs), refs, label))

    if args.csv:
        import pandas as pd
        pd.DataFrame(results).to_csv(args.csv, index=False)
        print(f"\nwrote {args.csv}")

    best = max(results, key=lambda r: r["ROUGE-1"])
    print(f"\nBest ROUGE-1: {best['Model']} at {best['ROUGE-1']}")
    return results


if __name__ == "__main__":
    main()
