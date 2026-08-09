"""Backwards-compatible facade over the section-wise modules.

The project is now split by assignment task and by who owns each part:

    config.py       settings                        Member 1
    data_prep.py    Task 2 - cleaning and splits    Member 1
    attention.py    Task 3.1 - Bahdanau attention   Member 2
    model_lstm.py   Task 3.1 - Seq2Seq LSTM         Member 2
    model_t5.py     Task 3.2 - the Transformer      Member 3
    aggregate.py    Task 3.2 - map-reduce           Member 3
    aspects.py      Task 3.3 - aspect mining        Member 3
    app.py          Task 4 - Streamlit              Member 4
    evaluate_rouge.py Task 5 - ROUGE                Member 5

This module simply re-exports the pieces, so `from summarizer import ...`
still works in the already-executed notebook and in older scripts. New
code should import from the module that owns the function instead.
"""

from __future__ import annotations

from aggregate import build_overall_summary, map_summaries, reduce_summaries
from aspects import AspectReport, analyse_aspects
from config import (BASE_MODEL, HERE, MAX_INPUT_TOKENS, MAX_TARGET_TOKENS,
                    MAX_TRAIN_INPUT_TOKENS, MODEL_DIR, TASK_PREFIX)
from data_prep import (clean_text, is_usable, split_reviews, split_sentences,
                       write_sample_reviews)
from model_t5 import ReviewSummarizer

__all__ = [
    "AspectReport", "BASE_MODEL", "HERE", "MAX_INPUT_TOKENS",
    "MAX_TARGET_TOKENS", "MAX_TRAIN_INPUT_TOKENS", "MODEL_DIR",
    "ReviewSummarizer", "TASK_PREFIX", "analyse_aspects",
    "build_overall_summary", "clean_text", "is_usable", "map_summaries",
    "reduce_summaries", "split_reviews", "split_sentences",
    "write_sample_reviews",
]
