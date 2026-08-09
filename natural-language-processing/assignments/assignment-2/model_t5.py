"""Task 3.2 - the T5 encoder-decoder wrapper.

Owner: Member 3 (Deep Learning Engineer - Transformer).

Loads the fine-tuned t5-small and turns reviews into short summaries.
Falls back to the plain pretrained checkpoint when nothing has been
trained yet, so the app and notebook always run.
"""

from __future__ import annotations

import os

from config import (BASE_MODEL, MAX_INPUT_TOKENS, MAX_TARGET_TOKENS,
                    NO_REPEAT_NGRAM, NUM_BEAMS, T5_MODEL_DIR, TASK_PREFIX)
from data_prep import clean_text


class ReviewSummarizer:
    """The encoder-decoder that summarises one review at a time.

    The encoder reads the whole review and turns it into hidden vectors.
    The decoder writes the summary token by token, attending to those
    vectors through cross-attention - that is what keeps the summary
    faithful to the review while still using new words.
    """

    def __init__(self, model_dir: str | None = None):
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

        wanted = model_dir or T5_MODEL_DIR
        if os.path.isdir(wanted):
            self.source, self.is_finetuned = wanted, True
        else:
            self.source, self.is_finetuned = BASE_MODEL, False

        self.tokenizer = AutoTokenizer.from_pretrained(self.source)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.source)
        self.model.eval()

    def summarize(self, reviews, num_beams: int = NUM_BEAMS,
                  max_new_tokens: int = MAX_TARGET_TOKENS,
                  batch_size: int = 8) -> list[str]:
        """Summarise a list of reviews. Returns one short summary each."""
        import torch

        if isinstance(reviews, str):
            reviews = [reviews]

        cleaned = [clean_text(r) for r in reviews]
        out: list[str] = []

        for i in range(0, len(cleaned), batch_size):
            batch = [TASK_PREFIX + t for t in cleaned[i:i + batch_size]]
            enc = self.tokenizer(batch, max_length=MAX_INPUT_TOKENS,
                                 truncation=True, padding=True,
                                 return_tensors="pt")
            with torch.no_grad():
                ids = self.model.generate(
                    **enc,
                    num_beams=num_beams,
                    max_new_tokens=max_new_tokens,
                    no_repeat_ngram_size=NO_REPEAT_NGRAM,
                    early_stopping=True,
                )
            out += self.tokenizer.batch_decode(ids, skip_special_tokens=True)

        return [s.strip() for s in out]

    def describe(self) -> dict:
        """Architecture facts, used by the notebook in Task 3."""
        cfg = self.model.config
        total = sum(p.numel() for p in self.model.parameters())
        return {
            "source": self.source,
            "fine_tuned": self.is_finetuned,
            "encoder_blocks": cfg.num_layers,
            "decoder_blocks": cfg.num_decoder_layers,
            "attention_heads": cfg.num_heads,
            "d_model": cfg.d_model,
            "vocab_size": cfg.vocab_size,
            "parameters": total,
        }
