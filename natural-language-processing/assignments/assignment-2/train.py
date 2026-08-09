"""Fine-tune t5-small to summarise Amazon food reviews (Task 2 + Task 3).

Dataset : jhan21/amazon-food-reviews-dataset  (Amazon Fine Food Reviews, 568k rows)
          `Text` is the review, `Summary` is the human-written headline.

Run:
    python train.py                     # default: 4k reviews, 1 epoch, ~30 min CPU
    python train.py --train-size 20000  # better quality, several hours on CPU
"""

from __future__ import annotations

import sys

# Windows consoles default to cp1252 and raise UnicodeEncodeError on any
# character they cannot represent. Training prints model output, so force
# UTF-8 and degrade gracefully rather than losing a long run to a print.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

import argparse
import os
import time

from summarizer import (BASE_MODEL, HERE, MAX_TARGET_TOKENS,
                        MAX_TRAIN_INPUT_TOKENS, MODEL_DIR, TASK_PREFIX,
                        clean_text)

DATASET = "jhan21/amazon-food-reviews-dataset"
DATA_DIR = os.path.join(HERE, "data")


# ---------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------

def is_usable(row) -> bool:
    """Keep only rows that can actually teach the model something."""
    text, summary = row.get("Text") or "", row.get("Summary") or ""
    if not (50 <= len(text) <= 2000):
        return False
    if not (10 <= len(summary) <= 80):
        return False
    # A headline that just repeats the review teaches copying, not summarising.
    return summary.lower().strip() not in text.lower()[:120]


def load_splits(train_size: int, val_size: int, test_size: int, seed: int = 42):
    """Download, filter, clean and split the reviews."""
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

    Picks a product that has both happy and unhappy reviews, so the
    positive/negative aspect lists both have something to show.
    """
    from datasets import load_dataset

    df = load_dataset(DATASET, split="train").to_pandas()
    df = df[["ProductId", "Score", "Summary", "Text"]].dropna()

    stats = df.groupby("ProductId")["Score"].agg(["count", "mean"])
    # A genuinely divided product gives both aspect lists something to say.
    mixed = stats[(stats["count"].between(min_reviews, 120)) &
                  (stats["mean"].between(2.8, 3.8))]
    if mixed.empty:
        mixed = stats[stats["count"] >= min_reviews]

    product = mixed.sort_values("count", ascending=False).index[0]
    sample = df[df["ProductId"] == product].head(60)

    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, "sample_reviews.csv")
    sample.to_csv(path, index=False)
    print(f"[data] wrote {path} ({len(sample)} reviews for product {product}, "
          f"mean score {sample['Score'].mean():.1f})")
    return path


# ---------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--train-size", type=int, default=4000)
    ap.add_argument("--val-size", type=int, default=300)
    ap.add_argument("--test-size", type=int, default=500)
    ap.add_argument("--epochs", type=float, default=1.0)
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--out", default=MODEL_DIR)
    args = ap.parse_args()

    from transformers import (AutoModelForSeq2SeqLM, AutoTokenizer,
                              DataCollatorForSeq2Seq, Seq2SeqTrainer,
                              Seq2SeqTrainingArguments)

    splits = load_splits(args.train_size, args.val_size, args.test_size)

    # Keep the test split on disk - the notebook scores ROUGE on it.
    os.makedirs(DATA_DIR, exist_ok=True)
    test_csv = os.path.join(DATA_DIR, "test_reviews.csv")
    splits["test"].to_csv(test_csv, index=False)
    print(f"[data] wrote {test_csv}")
    write_sample_reviews()

    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    model = AutoModelForSeq2SeqLM.from_pretrained(BASE_MODEL)

    def tokenize(batch):
        enc = tokenizer([TASK_PREFIX + d for d in batch["document"]],
                        max_length=MAX_TRAIN_INPUT_TOKENS, truncation=True)
        # text_target tells the tokenizer this is the decoder side.
        enc["labels"] = tokenizer(text_target=batch["summary"],
                                  max_length=MAX_TARGET_TOKENS,
                                  truncation=True)["input_ids"]
        return enc

    tokenized = {
        k: v.map(tokenize, batched=True, remove_columns=v.column_names,
                 desc=f"tokenizing {k}")
        for k, v in splits.items() if k != "test"
    }

    targs = Seq2SeqTrainingArguments(
        output_dir=os.path.join(HERE, "models", "_checkpoints"),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        learning_rate=args.lr,
        weight_decay=0.01,
        warmup_steps=100,
        eval_strategy="epoch",
        save_strategy="no",          # we save once at the end ourselves
        logging_steps=50,
        # Generating with beam search over the whole eval set costs more
        # than the training itself on CPU. Eval loss is enough here; real
        # ROUGE is computed once at the end, in the notebook.
        predict_with_generate=False,
        # Batch similar-length reviews together so dynamic padding has
        # far less filler to process - the single biggest CPU speed-up.
        # (v5 name; this was called `group_by_length` in transformers v4.)
        sortish_sampler=True,
        report_to="none",
        use_cpu=True,                # no CUDA on this machine
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=targs,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["validation"],
        processing_class=tokenizer,  # v5 name for the old `tokenizer=` arg
        data_collator=DataCollatorForSeq2Seq(tokenizer, model=model),
    )

    print(f"[train] {len(tokenized['train']):,} examples, "
          f"{args.epochs} epoch(s), batch {args.batch_size}")
    start = time.time()
    trainer.train()
    print(f"[train] done in {(time.time() - start) / 60:.1f} min")

    os.makedirs(args.out, exist_ok=True)
    model.save_pretrained(args.out)
    tokenizer.save_pretrained(args.out)
    print(f"[train] saved model -> {args.out}")

    # Eyeball a few outputs so a failed run is obvious immediately.
    from summarizer import ReviewSummarizer
    s = ReviewSummarizer(args.out)
    sample = splits["test"].select(range(min(3, len(splits["test"]))))
    for row, pred in zip(sample, s.summarize(sample["document"])):
        print("\n  review :", row["document"][:110], "...")
        print("  human  :", row["summary"])
        print("  model  :", pred)


if __name__ == "__main__":
    main()
