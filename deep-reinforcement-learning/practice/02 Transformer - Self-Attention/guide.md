# Transformer Practice — Self-Attention (Build Guide)

**Date:** 2026-07-04
**Files in this topic folder:**
- `explainer.html` — interactive, click-to-learn visual explanation (open this first!)
- `practice.ipynb` — the template notebook you fill in (this is the `.py`-style solution notebook)
- `guide.md` — this cell-by-cell build guide
**Goal:** Learn the **self-attention** mechanism — the single idea the whole Transformer is built on — by coding it from scratch with plain NumPy, **cell by cell.**

This is the *basic version*: the problem statement and an empty scaffold. We fill in the code together, one cell at a time.

---

## How we'll work (cell by cell)

For each cell below we follow the same loop:

1. **Read the concept** for that cell in plain English.
2. **You write** the code (the notebook has `# TODO` blanks for the important lines).
3. **You run it** and check the output (or any error).
4. **Verify** it and move to the next cell.

> Rule for today: don't jump to the finished answer up front. Try each `# TODO` first, then check. That's how it sticks.

---

## The problem

We have a tiny sentence of **4 words**. Each word is already turned into a small vector (its "embedding"). We want each word to **look at every other word and mix in the information that matters to it** — that is exactly what self-attention does.

```
Sentence:   "the  cat  sat  down"
Word index:   0     1    2    3
Embedding:  each word -> a vector of length d (e.g. d = 8)
```

Real-world analogy: you're in a group chat of 4 people. Before you speak, you skim what **everyone** said, decide **whose message is most relevant to you** (that's the *attention weight*), and write your reply as a **blend** of the messages you cared about most. Self-attention does this for every word at once.

## Self-attention in one table — **(Q, K, V, scores, weights, output)**

| Symbol | Name | Plain meaning |
|--------|------|---------------|
| **Q** | Query | "What am I looking for?" — one query vector per word |
| **K** | Key | "What do I offer?" — one key vector per word |
| **V** | Value | "The actual info I'll hand over if you pick me" |
| **scores** | Q · Kᵀ | How well each word's query matches every word's key |
| **weights** | softmax(scores / √dₖ) | Scores turned into % that add up to 1 per word |
| **output** | weights · V | Each word's new vector = weighted blend of all values |

---

## Build plan — the cells

- [ ] **Cell 0 — Setup.** Import `numpy`, set a random seed, build a fake `X` of shape `(4, d)` (4 words, d features). *(done for you)*
- [ ] **Cell 1 — Weight matrices.** Create random `W_q`, `W_k`, `W_v` of shape `(d, d_k)`. *(done for you)*
- [ ] **Cell 2 — Project into Q, K, V.** ✏️ Fill in:
  `Q = X · W_q`, `K = X · W_k`, `V = X · W_v`
- [ ] **Cell 3 — Scores + scaling.** ✏️ `scores = Q · Kᵀ`, then divide by `√d_k` so the numbers don't blow up.
- [ ] **Cell 4 — Softmax → weights.** ✏️ Turn each row of scores into probabilities that sum to 1.
- [ ] **Cell 5 — Weighted sum → output.** ✏️ `output = weights · V`. Check the shape is back to `(4, d_k)`.
- [ ] **Cell 6 — Check + stretch goals.** Verify each weight row sums to 1; try a longer sentence; wrap it all in one `self_attention(X)` function.

---

## Key idea to hold onto

The **scaled dot-product attention** formula is the whole game:

```
Attention(Q, K, V) = softmax( (Q · Kᵀ) / sqrt(d_k) ) · V
```

Every cell from 2 to 5 is just one piece of this single line. Once this clicks, "multi-head attention" is only this same block run a few times in parallel and stitched together.

## Progress log

Use this to track what we finished together:

- [ ] Understood what Q, K, V mean
- [ ] Q, K, V projections run without error
- [ ] Scores are scaled by √d_k
- [ ] Each softmax weight row sums to 1
- [ ] `output` has the right shape
- [ ] Tried a stretch goal
