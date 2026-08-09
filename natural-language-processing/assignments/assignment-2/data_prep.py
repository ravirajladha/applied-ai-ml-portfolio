"""Task 2 - data collection, cleaning and splitting.

Owner: Member 1 (Problem Analyst & Data Engineer).

Everything that turns raw Amazon review rows into clean train/val/test
splits lives here. Both models (LSTM and T5) consume the same output, so
the comparison in Task 5 is fair.
"""

from __future__ import annotations

import html
import os
import re

from config import (DATA_DIR, DATASET, MAX_REVIEW_CHARS, MAX_SUMMARY_CHARS,
                    MIN_REVIEW_CHARS, MIN_SUMMARY_CHARS, SAMPLE_CSV, SEED)

# ---------------------------------------------------------------------
# 1. Cleaning
# ---------------------------------------------------------------------

# Reviews scraped from the web carry HTML tags and entities.
_TAG_RE = re.compile(r"<[^>]+>")
_URL_RE = re.compile(r"https?://\S+|www\.\S+")
_SPACE_RE = re.compile(r"\s+")

# "don't" -> "do not" etc. Keeps the vocabulary smaller and more regular.
_CONTRACTIONS = {
    "won't": "will not", "can't": "cannot", "n't": " not",
    "'re": " are", "'d": " would",
    "'ll": " will", "'ve": " have", "'m": " am",
}

# "'s" is the one ambiguous case: "it's" is a contraction, but "cow's milk"
# is possessive. Expanding it blindly produced "baby cow is milk". Only
# expand after words that cannot take a possessive.
_ITS_RE = re.compile(r"\b(it|he|she|that|there|here|what|who|this)'s\b")


def clean_text(text: str) -> str:
    """Normalise one piece of review text.

    Lowercases, strips HTML/URLs, expands contractions and squeezes
    whitespace. Sentence-ending punctuation is deliberately kept, because
    the aspect step needs to split on it later.
    """
    if not isinstance(text, str):
        return ""

    text = html.unescape(text)
    text = _TAG_RE.sub(" ", text)
    text = _URL_RE.sub(" ", text)
    text = text.lower()

    text = _ITS_RE.sub(r"\1 is", text)
    for short, long in _CONTRACTIONS.items():
        text = text.replace(short, long)

    # Drop anything that is not a letter, digit, space or sentence mark.
    text = re.sub(r"[^a-z0-9\s.!?,'-]", " ", text)
    return _SPACE_RE.sub(" ", text).strip()


def split_reviews(raw: str) -> list[str]:
    """Split pasted text into individual reviews.

    A blank line separates reviews; if there are none, one review per line.
    """
    if not raw or not raw.strip():
        return []

    blocks = [b.strip() for b in re.split(r"\n\s*\n", raw) if b.strip()]
    if len(blocks) == 1:
        blocks = [ln.strip() for ln in raw.splitlines() if ln.strip()]

    # A "review" shorter than this is almost always a stray heading.
    return [b for b in blocks if len(b) >= 15]


def split_sentences(text: str) -> list[str]:
    """Rough sentence splitter - good enough for aspect counting."""
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if len(p.strip()) >= 10]


# ---------------------------------------------------------------------
# 2. Filtering
# ---------------------------------------------------------------------

def is_usable(row) -> bool:
    """Keep only rows that can actually teach a model something."""
    text, summary = row.get("Text") or "", row.get("Summary") or ""
    if not (MIN_REVIEW_CHARS <= len(text) <= MAX_REVIEW_CHARS):
        return False
    if not (MIN_SUMMARY_CHARS <= len(summary) <= MAX_SUMMARY_CHARS):
        return False
    # A headline that just repeats the review teaches copying, not summarising.
    return summary.lower().strip() not in text.lower()[:120]


# ---------------------------------------------------------------------
# 3. Splits
# ---------------------------------------------------------------------

def load_splits(train_size: int, val_size: int, test_size: int,
                seed: int = SEED):
    """Download, filter, clean and split the reviews.

    Returns a dict with "train", "validation" and "test" datasets, each
    having a `document` (the review) and a `summary` (the headline).
    """
    from datasets import load_dataset

    print(f"[data] loading {DATASET} ...")
    ds = load_dataset(DATASET, split="train")
    print(f"[data] raw rows: {len(ds):,}")

    # Sample first so filtering is fast; take extra to survive the filter.
    need = (train_size + val_size + test_size) * 4
    ds = ds.shuffle(seed=seed).select(range(min(need, len(ds))))

    ds = ds.filter(is_usable)
    print(f"[data] usable rows after filtering: {len(ds):,}")

    def prep(row):
        return {"document": clean_text(row["Text"]),
                "summary": clean_text(row["Summary"])}

    keep = ["Score", "ProductId"]
    drop = [c for c in ds.column_names if c not in keep]
    ds = ds.map(prep, remove_columns=drop, desc="cleaning")

    total = train_size + val_size + test_size
    ds = ds.select(range(min(total, len(ds))))
    n = len(ds)
    train_n = int(n * train_size / total)
    val_n = int(n * val_size / total)

    splits = {
        "train": ds.select(range(train_n)),
        "validation": ds.select(range(train_n, train_n + val_n)),
        "test": ds.select(range(train_n + val_n, n)),
    }
    for k, v in splits.items():
        print(f"[data] {k}: {len(v):,}")
    return splits


def write_sample_reviews(min_reviews: int = 40) -> str:
    """Save all reviews for one real product, for the app's demo tab.

    Picks a product with both happy and unhappy reviews, so the positive
    and negative aspect lists both have something to show.
    """
    from datasets import load_dataset

    df = load_dataset(DATASET, split="train").to_pandas()
    df = df[["ProductId", "Score", "Summary", "Text"]].dropna()

    stats = df.groupby("ProductId")["Score"].agg(["count", "mean"])
    mixed = stats[(stats["count"].between(min_reviews, 120)) &
                  (stats["mean"].between(2.8, 3.8))]
    if mixed.empty:
        mixed = stats[stats["count"] >= min_reviews]

    product = mixed.sort_values("count", ascending=False).index[0]
    sample = df[df["ProductId"] == product].head(60)

    os.makedirs(DATA_DIR, exist_ok=True)
    sample.to_csv(SAMPLE_CSV, index=False)
    print(f"[data] wrote {SAMPLE_CSV} ({len(sample)} reviews for product "
          f"{product}, mean score {sample['Score'].mean():.1f})")
    return SAMPLE_CSV
