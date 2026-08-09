"""Task 3.1 - Seq2Seq LSTM encoder-decoder built from scratch.

Owner: Member 2 (Deep Learning Engineer - Baseline).

This is the classical encoder-decoder, written layer by layer, as the
baseline the Transformer is compared against in Task 5.

    Encoder : bidirectional LSTM reads the review, one vector per word
    Attention : picks which of those vectors matter at each output step
    Decoder : LSTM writes the summary one word at a time

Unlike T5 this model starts from random weights and learns English only
from our training reviews, which is exactly why it is the weaker baseline.
"""

from __future__ import annotations

import json
import os
import re
from collections import Counter

import torch
import torch.nn as nn

from attention import BahdanauAttention
from config import (EOS, EOS_ID, LSTM_EMBED_DIM, LSTM_HIDDEN_DIM,
                    LSTM_MAX_INPUT, LSTM_MAX_TARGET, LSTM_VOCAB_SIZE, PAD,
                    PAD_ID, SOS, SOS_ID, UNK, UNK_ID)

_WORD_RE = re.compile(r"[a-z0-9']+")


# ---------------------------------------------------------------------
# Vocabulary
# ---------------------------------------------------------------------

class Vocab:
    """Maps words to integer ids. Rare words become <unk>."""

    def __init__(self, itos: list[str] | None = None):
        self.itos = itos or [PAD, SOS, EOS, UNK]
        self.stoi = {w: i for i, w in enumerate(self.itos)}

    @classmethod
    def build(cls, texts, max_size: int = LSTM_VOCAB_SIZE, min_freq: int = 2):
        counter = Counter(w for t in texts for w in tokenize(t))
        itos = [PAD, SOS, EOS, UNK]
        for word, freq in counter.most_common():
            if freq < min_freq or len(itos) >= max_size:
                break
            itos.append(word)
        return cls(itos)

    def __len__(self):
        return len(self.itos)

    def encode(self, text: str, max_len: int, add_eos: bool = True):
        ids = [self.stoi.get(w, UNK_ID) for w in tokenize(text)][:max_len - 1]
        if add_eos:
            ids.append(EOS_ID)
        return ids

    def decode(self, ids) -> str:
        words = []
        for i in ids:
            i = int(i)
            if i in (PAD_ID, SOS_ID):
                continue
            if i == EOS_ID:
                break
            words.append(self.itos[i] if i < len(self.itos) else UNK)
        return " ".join(words)

    def save(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self.itos, fh)

    @classmethod
    def load(cls, path: str):
        with open(path, encoding="utf-8") as fh:
            return cls(json.load(fh))


def tokenize(text: str) -> list[str]:
    """Plain word tokenizer - the LSTM has no sub-word model."""
    return _WORD_RE.findall((text or "").lower())


# ---------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------

class Encoder(nn.Module):
    """Bidirectional LSTM over the review."""

    def __init__(self, vocab_size, embed_dim=LSTM_EMBED_DIM,
                 hidden_dim=LSTM_HIDDEN_DIM):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim,
                                      padding_idx=PAD_ID)
        self.rnn = nn.LSTM(embed_dim, hidden_dim, batch_first=True,
                           bidirectional=True)
        # Two directions are concatenated, so squeeze them back down.
        self.fc_h = nn.Linear(hidden_dim * 2, hidden_dim)
        self.fc_c = nn.Linear(hidden_dim * 2, hidden_dim)

    def forward(self, src):
        emb = self.embedding(src)
        outputs, (h, c) = self.rnn(emb)
        h = torch.tanh(self.fc_h(torch.cat([h[0], h[1]], dim=1)))
        c = torch.tanh(self.fc_c(torch.cat([c[0], c[1]], dim=1)))
        return outputs, (h, c)


class Decoder(nn.Module):
    """LSTM that writes the summary, one word per step, using attention."""

    def __init__(self, vocab_size, embed_dim=LSTM_EMBED_DIM,
                 hidden_dim=LSTM_HIDDEN_DIM):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim,
                                      padding_idx=PAD_ID)
        self.attention = BahdanauAttention(hidden_dim * 2, hidden_dim)
        # Input is the previous word plus the attention context.
        self.rnn = nn.LSTMCell(embed_dim + hidden_dim * 2, hidden_dim)
        self.out = nn.Linear(hidden_dim * 2 + hidden_dim + embed_dim,
                             vocab_size)

    def forward(self, token, state, enc_outputs, mask):
        h, c = state
        emb = self.embedding(token)                       # (b, embed)
        context, weights = self.attention(h, enc_outputs, mask)
        h, c = self.rnn(torch.cat([emb, context], dim=1), (h, c))
        logits = self.out(torch.cat([h, context, emb], dim=1))
        return logits, (h, c), weights


class Seq2Seq(nn.Module):
    """Encoder + attention + decoder, trained end to end."""

    def __init__(self, vocab_size, embed_dim=LSTM_EMBED_DIM,
                 hidden_dim=LSTM_HIDDEN_DIM):
        super().__init__()
        self.encoder = Encoder(vocab_size, embed_dim, hidden_dim)
        self.decoder = Decoder(vocab_size, embed_dim, hidden_dim)
        self.vocab_size = vocab_size

    def forward(self, src, tgt, teacher_forcing: float = 0.5):
        """Training pass. Teacher forcing feeds the true previous word
        some of the time, which makes early training far more stable."""
        batch, tgt_len = tgt.shape
        mask = src != PAD_ID
        enc_outputs, state = self.encoder(src)

        outputs = torch.zeros(batch, tgt_len, self.vocab_size,
                              device=src.device)
        token = tgt[:, 0]                                  # <sos>
        for t in range(1, tgt_len):
            logits, state, _ = self.decoder(token, state, enc_outputs, mask)
            outputs[:, t] = logits
            use_truth = torch.rand(1).item() < teacher_forcing
            token = tgt[:, t] if use_truth else logits.argmax(1)
        return outputs

    @torch.no_grad()
    def generate(self, src, max_len: int = LSTM_MAX_TARGET):
        """Greedy decoding, used at inference time."""
        mask = src != PAD_ID
        enc_outputs, state = self.encoder(src)
        token = torch.full((src.size(0),), SOS_ID, dtype=torch.long,
                           device=src.device)

        result = []
        for _ in range(max_len):
            logits, state, _ = self.decoder(token, state, enc_outputs, mask)
            token = logits.argmax(1)
            result.append(token)
        return torch.stack(result, dim=1)


def pad_batch(sequences, max_len: int) -> torch.Tensor:
    """Pad a list of id-lists into one rectangular tensor."""
    out = torch.full((len(sequences), max_len), PAD_ID, dtype=torch.long)
    for i, seq in enumerate(sequences):
        seq = seq[:max_len]
        out[i, :len(seq)] = torch.tensor(seq, dtype=torch.long)
    return out
