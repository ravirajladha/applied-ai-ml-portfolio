"""Task 3.1 - run the trained LSTM baseline.

Owner: Member 2 (Deep Learning Engineer - Baseline).

Gives the LSTM the same `.summarize(list_of_reviews)` interface as the T5
model, so `evaluate_rouge.py` can score them side by side without caring
which is which.
"""

from __future__ import annotations

import os

import torch

from config import LSTM_MAX_INPUT, LSTM_MAX_TARGET, LSTM_MODEL_DIR
from data_prep import clean_text
from model_lstm import Seq2Seq, Vocab, pad_batch


class LSTMSummarizer:
    """Same interface as ReviewSummarizer, backed by the LSTM."""

    def __init__(self, model_dir: str | None = None):
        self.source = model_dir or LSTM_MODEL_DIR
        weights = os.path.join(self.source, "model.pt")
        vocab_path = os.path.join(self.source, "vocab.json")

        if not (os.path.exists(weights) and os.path.exists(vocab_path)):
            raise FileNotFoundError(
                f"no trained LSTM in {self.source} - run `python train_lstm.py`")

        self.vocab = Vocab.load(vocab_path)
        self.model = Seq2Seq(len(self.vocab))
        self.model.load_state_dict(torch.load(weights, map_location="cpu"))
        self.model.eval()
        self.is_finetuned = True

    def summarize(self, reviews, batch_size: int = 32, **_) -> list[str]:
        """Summarise a list of reviews. Extra kwargs are ignored, so this
        can be swapped for the T5 model without changing the caller."""
        if isinstance(reviews, str):
            reviews = [reviews]

        cleaned = [clean_text(r) for r in reviews]
        out: list[str] = []

        for i in range(0, len(cleaned), batch_size):
            chunk = cleaned[i:i + batch_size]
            src = pad_batch([self.vocab.encode(t, LSTM_MAX_INPUT)
                             for t in chunk], LSTM_MAX_INPUT)
            ids = self.model.generate(src, max_len=LSTM_MAX_TARGET)
            out += [self.vocab.decode(row) for row in ids]

        return [s.strip() for s in out]

    def describe(self) -> dict:
        return {
            "source": self.source,
            "architecture": "Seq2Seq bi-LSTM + Bahdanau attention",
            "vocab_size": len(self.vocab),
            "parameters": sum(p.numel() for p in self.model.parameters()),
        }


def available(model_dir: str | None = None) -> bool:
    """True when a trained LSTM exists, so callers can skip it politely."""
    d = model_dir or LSTM_MODEL_DIR
    return (os.path.exists(os.path.join(d, "model.pt")) and
            os.path.exists(os.path.join(d, "vocab.json")))


if __name__ == "__main__":
    from config import use_utf8_console
    use_utf8_console()
    s = LSTMSummarizer()
    print(s.describe())
    print(s.summarize(["The coffee tastes wonderful and arrived quickly, "
                       "great value and I will order it again."]))
