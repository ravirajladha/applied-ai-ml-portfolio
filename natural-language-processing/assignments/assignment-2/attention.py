"""Task 3.1 - Bahdanau (additive) attention.

Owner: Member 2 (Deep Learning Engineer - Baseline).

Without attention, an encoder must squeeze a whole review into one fixed
vector and the decoder sees only that - everything else is forgotten. This
is the bottleneck attention was invented to remove.

At every output step the decoder asks "which input words matter now?",
scores each encoder state, and reads a weighted blend of them.

Bahdanau scoring adds the two states and passes them through a small
network:

    score(h_dec, h_enc) = v^T * tanh(W1 * h_dec + W2 * h_enc)

Luong attention instead multiplies them. Additive is used here because it
copes with the encoder and decoder having different hidden sizes.
"""

from __future__ import annotations

import torch
import torch.nn as nn


class BahdanauAttention(nn.Module):
    """Additive attention over the encoder outputs."""

    def __init__(self, enc_dim: int, dec_dim: int, attn_dim: int = 128):
        super().__init__()
        self.W1 = nn.Linear(dec_dim, attn_dim, bias=False)   # decoder side
        self.W2 = nn.Linear(enc_dim, attn_dim, bias=False)   # encoder side
        self.v = nn.Linear(attn_dim, 1, bias=False)          # to one score

    def forward(self, dec_hidden, enc_outputs, mask=None):
        """
        dec_hidden  : (batch, dec_dim)        where the decoder is now
        enc_outputs : (batch, src_len, enc_dim)  one vector per input word
        mask        : (batch, src_len) True for real words, False for padding

        Returns the context vector (batch, enc_dim) and the attention
        weights (batch, src_len), which are what an attention heat-map plots.
        """
        # Broadcast the decoder state across every input position.
        dec = self.W1(dec_hidden).unsqueeze(1)      # (b, 1, attn)
        enc = self.W2(enc_outputs)                  # (b, src_len, attn)
        scores = self.v(torch.tanh(dec + enc)).squeeze(-1)   # (b, src_len)

        # Padding must never win attention.
        if mask is not None:
            scores = scores.masked_fill(~mask, float("-inf"))

        weights = torch.softmax(scores, dim=1)
        context = torch.bmm(weights.unsqueeze(1), enc_outputs).squeeze(1)
        return context, weights
