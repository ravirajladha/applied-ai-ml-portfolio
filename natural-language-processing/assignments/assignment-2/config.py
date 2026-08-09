"""Shared settings for the whole project.

Owner: Member 1 (Problem Analyst & Data Engineer).

Every other module imports its constants from here, so there is exactly one
place to change a path or a hyper-parameter.
"""

from __future__ import annotations

import os
import sys

# ---------------------------------------------------------------------
# Console
# ---------------------------------------------------------------------

def use_utf8_console() -> None:
    """Stop Windows consoles crashing on non-ASCII output.

    Windows defaults to cp1252, which raises UnicodeEncodeError on the
    sub-word marker T5's tokenizer prints. Every script that prints model
    output calls this first.
    """
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
MODELS_DIR = os.path.join(HERE, "models")
SCREENSHOT_DIR = os.path.join(HERE, "screenshots")

T5_MODEL_DIR = os.path.join(MODELS_DIR, "t5-review-summarizer")
LSTM_MODEL_DIR = os.path.join(MODELS_DIR, "lstm-review-summarizer")

SAMPLE_CSV = os.path.join(DATA_DIR, "sample_reviews.csv")
TEST_CSV = os.path.join(DATA_DIR, "test_reviews.csv")

# Kept for backwards compatibility with earlier code and the notebook.
MODEL_DIR = T5_MODEL_DIR


# ---------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------

DATASET = "jhan21/amazon-food-reviews-dataset"

# A row only teaches the model something if it sits inside these bounds.
MIN_REVIEW_CHARS, MAX_REVIEW_CHARS = 50, 2000
MIN_SUMMARY_CHARS, MAX_SUMMARY_CHARS = 10, 80

SEED = 42


# ---------------------------------------------------------------------
# Transformer (T5) - Task 3.2
# ---------------------------------------------------------------------

BASE_MODEL = "t5-small"

# T5 is multi-task, so every input must state which task it is.
TASK_PREFIX = "summarize: "

MAX_INPUT_TOKENS = 256      # inference
MAX_TARGET_TOKENS = 32

# Training truncates harder than inference. Attention cost grows with the
# square of the sequence and this project trains on an emulated CPU, so
# 128 tokens roughly halves the time per example. The median review is 74
# tokens and reviews state their point early, so little is lost.
MAX_TRAIN_INPUT_TOKENS = 128

T5_TRAIN_SIZE = 4000
T5_VAL_SIZE = 300
T5_TEST_SIZE = 500
T5_EPOCHS = 1.0
T5_BATCH_SIZE = 8
T5_LEARNING_RATE = 3e-4

# Decoding
NUM_BEAMS = 4
NO_REPEAT_NGRAM = 2         # stops "good good good"


# ---------------------------------------------------------------------
# Seq2Seq LSTM baseline - Task 3.1
# ---------------------------------------------------------------------

LSTM_VOCAB_SIZE = 12000
LSTM_EMBED_DIM = 128
LSTM_HIDDEN_DIM = 256
LSTM_MAX_INPUT = 80         # words, not sub-words
LSTM_MAX_TARGET = 12
LSTM_BATCH_SIZE = 32
LSTM_EPOCHS = 3
LSTM_LEARNING_RATE = 1e-3
LSTM_TRAIN_SIZE = 8000

PAD, SOS, EOS, UNK = "<pad>", "<sos>", "<eos>", "<unk>"
PAD_ID, SOS_ID, EOS_ID, UNK_ID = 0, 1, 2, 3


# ---------------------------------------------------------------------
# Aspect mining - Task 3.3
# ---------------------------------------------------------------------

TOP_K_ASPECTS = 8
MIN_ASPECT_MENTIONS = 2     # a one-off mention is noise, not an aspect
ASPECT_SKEW = 0.6           # share of use that must fall on one side
POS_SENTENCE_THRESHOLD = 0.2
NEG_SENTENCE_THRESHOLD = -0.2
POS_REVIEW_THRESHOLD = 0.05
NEG_REVIEW_THRESHOLD = -0.05


# ---------------------------------------------------------------------
# Web app - Task 4
# ---------------------------------------------------------------------

STREAMLIT_PORT = 8501
FLASK_PORT = 5000
MAX_REVIEWS_DEFAULT = 50
