"""Task 3.2 - fine-tune t5-small on Amazon food reviews.

Owner: Member 3 (Deep Learning Engineer - Transformer).

Dataset : jhan21/amazon-food-reviews-dataset  (Amazon Fine Food Reviews, 568k rows)
          `Text` is the review, `Summary` is the human-written headline.

Run:
    python train.py                     # default: 4k reviews, 1 epoch, ~30 min CPU
    python train.py --train-size 20000  # better quality, several hours on CPU
"""

from __future__ import annotations

import argparse
import os
import time

from config import (BASE_MODEL, DATA_DIR, HERE, MAX_TARGET_TOKENS,
                    MAX_TRAIN_INPUT_TOKENS, T5_BATCH_SIZE, T5_EPOCHS,
                    T5_LEARNING_RATE, T5_MODEL_DIR, T5_TEST_SIZE,
                    T5_TRAIN_SIZE, T5_VAL_SIZE, TASK_PREFIX, TEST_CSV,
                    use_utf8_console)
from data_prep import is_usable, load_splits, write_sample_reviews


# ---------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------

def main() -> None:
    use_utf8_console()
    ap = argparse.ArgumentParser()
    ap.add_argument("--train-size", type=int, default=T5_TRAIN_SIZE)
    ap.add_argument("--val-size", type=int, default=T5_VAL_SIZE)
    ap.add_argument("--test-size", type=int, default=T5_TEST_SIZE)
    ap.add_argument("--epochs", type=float, default=T5_EPOCHS)
    ap.add_argument("--batch-size", type=int, default=T5_BATCH_SIZE)
    ap.add_argument("--lr", type=float, default=T5_LEARNING_RATE)
    ap.add_argument("--out", default=T5_MODEL_DIR)
    args = ap.parse_args()

    from transformers import (AutoModelForSeq2SeqLM, AutoTokenizer,
                              DataCollatorForSeq2Seq, Seq2SeqTrainer,
                              Seq2SeqTrainingArguments)

    splits = load_splits(args.train_size, args.val_size, args.test_size)

    # Keep the test split on disk - the notebook scores ROUGE on it.
    os.makedirs(DATA_DIR, exist_ok=True)
    test_csv = TEST_CSV
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
    from model_t5 import ReviewSummarizer
    s = ReviewSummarizer(args.out)
    sample = splits["test"].select(range(min(3, len(splits["test"]))))
    for row, pred in zip(sample, s.summarize(sample["document"])):
        print("\n  review :", row["document"][:110], "...")
        print("  human  :", row["summary"])
        print("  model  :", pred)


if __name__ == "__main__":
    main()
