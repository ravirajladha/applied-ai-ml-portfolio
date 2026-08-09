"""Task 5 - demonstration cases.

Owner: Member 5 (Evaluation Lead & Report Editor).

Runs the fixed scenarios we show in the report, so the numbers quoted
there can always be reproduced with one command.

Run:
    python demo_cases.py            # all cases
    python demo_cases.py --case 2   # just one
"""

from __future__ import annotations

import argparse
import textwrap

from config import use_utf8_console
from summarizer_service import analyse, load_sample_reviews

# A clearly positive product, a clearly negative one, and a divided one -
# so the aggregate verdict is exercised in all three of its branches.
CASES = {
    1: ("Mostly positive - a well-liked coffee", [
        "The coffee flavor is rich and smooth, absolutely delicious every morning.",
        "Great taste and the price is very reasonable for the quantity.",
        "Delicious blend with a rich aroma, I will definitely order more.",
        "Wonderful taste and great value, much better than the supermarket.",
        "The aroma and flavor are both excellent, worth every penny.",
        "Strong rich flavor, brews perfectly every time, my new favourite.",
    ]),
    2: ("Mixed - good product, bad delivery", [
        "The coffee flavor is rich and smooth, absolutely delicious.",
        "Great taste and the price is very reasonable for the quantity.",
        "Shipping was incredibly slow, it took nearly three weeks to arrive.",
        "The box arrived completely crushed and damaged, packaging is terrible.",
        "I love the flavor but the packaging was damaged again, disappointing.",
        "The packaging is awful, the seal was already broken on arrival.",
        "Wonderful taste and great value for the price.",
        "Shipping took forever and customer service never replied.",
    ]),
    3: ("Mostly negative - a product with real problems", [
        "Tastes stale and old, this box sat in a warehouse for months.",
        "The packaging is awful and the seal was broken when it arrived.",
        "Shipping took forever and customer service never replied to me.",
        "Terrible flavor, bitter and burnt, I poured the whole batch away.",
        "The box arrived crushed and damaged, a complete waste of money.",
        "Overpriced for the quality, I will not be buying this again.",
    ]),
    4: ("Real product from the dataset (60 reviews)", None),   # loaded lazily
    5: ("Edge case - a single very short review", [
        "It was fine, nothing special about the taste really.",
    ]),
}


def run_case(num: int) -> None:
    title, reviews = CASES[num]
    if reviews is None:
        reviews = load_sample_reviews()
        if not reviews:
            print(f"\nCASE {num}: {title}\n  skipped - run `python train_t5.py` "
                  f"to build data/sample_reviews.csv")
            return

    print(f"\n{'='*74}\nCASE {num}: {title}\n{'='*74}")
    print(f"  input: {len(reviews)} reviews")

    result = analyse(reviews)
    if "error" in result:
        print(f"  {result['error']}")
        return

    rep = result["report"]
    print(f"\n  OVERALL:\n{textwrap.indent(textwrap.fill(result['overall'], 68), '    ')}")
    print(f"\n  sentiment : {rep.n_positive} positive / {rep.n_negative} "
          f"negative / {rep.n_neutral} neutral")
    print(f"  praised   : {[a for a, _ in rep.positive_aspects] or '-'}")
    print(f"  criticised: {[a for a, _ in rep.negative_aspects] or '-'}")
    if result["model_verdict"]:
        print(f"  model's reduce-step verdict: {result['model_verdict']!r}")

    print("\n  per-review summaries:")
    for r, s in list(zip(result["reviews"], result["summaries"]))[:6]:
        print(f"    {r[:58]:60s} -> {s}")


def main() -> None:
    use_utf8_console()
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", type=int, choices=sorted(CASES), default=0,
                    help="run a single case instead of all of them")
    args = ap.parse_args()

    for num in ([args.case] if args.case else sorted(CASES)):
        run_case(num)
    print()


if __name__ == "__main__":
    main()
