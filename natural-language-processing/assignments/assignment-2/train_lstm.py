"""Task 3.1 - train the Seq2Seq LSTM baseline.

Owner: Member 2 (Deep Learning Engineer - Baseline).

Run:
    python train_lstm.py                    # small default, ~20 min on CPU
    python train_lstm.py --train-size 20000 --epochs 5
"""

from __future__ import annotations

import argparse
import os
import time

import torch
import torch.nn as nn

from config import (LSTM_BATCH_SIZE, LSTM_EPOCHS, LSTM_LEARNING_RATE,
                    LSTM_MAX_INPUT, LSTM_MAX_TARGET, LSTM_MODEL_DIR,
                    LSTM_TRAIN_SIZE, LSTM_VOCAB_SIZE, PAD_ID, SOS_ID,
                    T5_TEST_SIZE, T5_VAL_SIZE, use_utf8_console)
from data_prep import load_splits
from model_lstm import Seq2Seq, Vocab, pad_batch


def make_batches(docs, sums, vocab, batch_size, shuffle=True):
    """Yield (src, tgt) tensor pairs."""
    idx = torch.randperm(len(docs)) if shuffle else torch.arange(len(docs))
    for i in range(0, len(idx), batch_size):
        chunk = idx[i:i + batch_size]
        src = pad_batch([vocab.encode(docs[j], LSTM_MAX_INPUT) for j in chunk],
                        LSTM_MAX_INPUT)
        # Targets start with <sos> so the decoder has something to begin from.
        tgt = pad_batch([[SOS_ID] + vocab.encode(sums[j], LSTM_MAX_TARGET)
                         for j in chunk], LSTM_MAX_TARGET + 1)
        yield src, tgt


def main() -> None:
    use_utf8_console()
    ap = argparse.ArgumentParser()
    ap.add_argument("--train-size", type=int, default=LSTM_TRAIN_SIZE)
    ap.add_argument("--val-size", type=int, default=T5_VAL_SIZE)
    ap.add_argument("--test-size", type=int, default=T5_TEST_SIZE)
    ap.add_argument("--epochs", type=int, default=LSTM_EPOCHS)
    ap.add_argument("--batch-size", type=int, default=LSTM_BATCH_SIZE)
    ap.add_argument("--lr", type=float, default=LSTM_LEARNING_RATE)
    ap.add_argument("--out", default=LSTM_MODEL_DIR)
    args = ap.parse_args()

    splits = load_splits(args.train_size, args.val_size, args.test_size)
    train_docs = list(splits["train"]["document"])
    train_sums = list(splits["train"]["summary"])
    val_docs = list(splits["validation"]["document"])
    val_sums = list(splits["validation"]["summary"])

    # The vocabulary is built from the TRAINING text only - building it from
    # everything would leak the test set into the model.
    vocab = Vocab.build(train_docs + train_sums, max_size=LSTM_VOCAB_SIZE)
    print(f"[lstm] vocabulary: {len(vocab):,} words")

    model = Seq2Seq(len(vocab))
    params = sum(p.numel() for p in model.parameters())
    print(f"[lstm] parameters: {params:,}")

    opt = torch.optim.Adam(model.parameters(), lr=args.lr)
    # Padding must not contribute to the loss.
    loss_fn = nn.CrossEntropyLoss(ignore_index=PAD_ID)

    start = time.time()
    for epoch in range(1, args.epochs + 1):
        model.train()
        total, seen = 0.0, 0
        for step, (src, tgt) in enumerate(
                make_batches(train_docs, train_sums, vocab, args.batch_size)):
            opt.zero_grad()
            out = model(src, tgt)
            # Skip position 0 - it is the <sos> we fed in, not a prediction.
            loss = loss_fn(out[:, 1:].reshape(-1, out.size(-1)),
                           tgt[:, 1:].reshape(-1))
            loss.backward()
            # LSTMs blow up without this.
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()

            total += loss.item(); seen += 1
            if step % 50 == 0:
                print(f"  epoch {epoch} step {step:4d}  loss {loss.item():.3f}")

        model.eval()
        with torch.no_grad():
            v_total, v_seen = 0.0, 0
            for src, tgt in make_batches(val_docs, val_sums, vocab,
                                         args.batch_size, shuffle=False):
                out = model(src, tgt, teacher_forcing=0.0)
                v_total += loss_fn(out[:, 1:].reshape(-1, out.size(-1)),
                                   tgt[:, 1:].reshape(-1)).item()
                v_seen += 1
        print(f"[lstm] epoch {epoch}: train {total/max(seen,1):.3f} | "
              f"val {v_total/max(v_seen,1):.3f}")

    print(f"[lstm] trained in {(time.time()-start)/60:.1f} min")

    os.makedirs(args.out, exist_ok=True)
    torch.save(model.state_dict(), os.path.join(args.out, "model.pt"))
    vocab.save(os.path.join(args.out, "vocab.json"))
    print(f"[lstm] saved -> {args.out}")

    # Eyeball a few outputs so a failed run is obvious immediately.
    from infer_lstm import LSTMSummarizer
    s = LSTMSummarizer(args.out)
    for doc, ref, pred in zip(val_docs[:3], val_sums[:3],
                              s.summarize(val_docs[:3])):
        print(f"\n  review : {doc[:100]}...")
        print(f"  human  : {ref}")
        print(f"  model  : {pred}")


if __name__ == "__main__":
    main()
