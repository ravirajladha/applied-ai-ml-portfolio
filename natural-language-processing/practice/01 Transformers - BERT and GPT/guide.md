# Transformers, BERT and GPT — build guide

**Topic 01 · Natural Language Processing · practice**

| File | What it is |
|------|------------|
| `explainer.html` | **Open this first.** The interactive lesson — attention computed step by step, an attention explorer, the BERT/GPT mask toggle, and a self-check quiz. |
| `practice.ipynb` | The template notebook. Boilerplate is filled in; the core lines are left as `# TODO` for you. |
| `guide.md` | This file — the plan, the recap, and the checklist. |

---

## The problem statement

Build the attention mechanism from scratch in NumPy, then use it to demonstrate — in code, not prose — the one
difference between BERT and GPT.

By the end you will have written:

1. A numerically stable `softmax`.
2. `scaled_dot_product_attention(Q, K, V, mask)` — about six lines that sit at the heart of every modern language model.
3. A causal mask, and a side-by-side comparison of what a token can see under each mode.
4. Sinusoidal positional encoding.
5. Multi-head attention.
6. One complete transformer block, with residual connections and layer normalisation.

No downloads, no GPU, no `pip install`. Everything runs on the NumPy you already have.

---

## On dependencies — why this is NumPy only

You asked whether importing `transformers` would eat memory. It would, and more importantly it would hide the
thing you are trying to learn.

| Package | Disk | RAM in use | Needed here? |
|---|---|---|---|
| `numpy` | already installed | a few KB for our arrays | **yes** |
| `transformers` | ~50 MB | negligible on its own | no |
| `torch` (its dependency) | ~200 MB CPU-only, ~2.5 GB with CUDA | ~300 MB | no |
| `bert-base-uncased` weights | ~440 MB download, cached | ~1.5 GB peak | no |
| `distilbert-base` (lighter) | ~265 MB | ~900 MB | no |
| `gpt2` (smallest) | ~550 MB | ~1.8 GB | no |

A working HuggingFace setup is roughly **0.7–3 GB on disk** and **~2 GB of RAM** while a model is loaded. That is
survivable on a normal laptop, but `BertModel.from_pretrained()` is one line that hides the entire mechanism
behind it. Write the mechanism first; the library will make far more sense afterwards.

If you do want it later, the light path is:

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu   # CPU-only, ~200 MB not 2.5 GB
pip install transformers
```

and then use `distilbert-base-uncased` rather than `bert-base-uncased`.

---

## Plain-English recap

Everything in the notebook, in one table.

| Term | In one line |
|------|-------------|
| **Token** | A piece of a word. Text becomes integers before a model ever sees it. |
| **Embedding** | The vector a token ID looks up. Similar meanings → similar vectors. |
| **Positional encoding** | A per-slot vector added to the embedding, because attention has no sense of order on its own. |
| **Query (Q)** | What this token is looking for. |
| **Key (K)** | What this token advertises about itself. |
| **Value (V)** | What this token actually contributes if attended to. |
| **Attention score** | `q · k` — how relevant one token is to another. |
| **√d_k scaling** | Divides the scores so softmax does not saturate and kill the gradients. |
| **Attention weights** | The scores after softmax: positive, summing to 1. |
| **Mask** | Adding `−∞` to forbidden scores so their weight becomes exactly 0 after softmax. |
| **Causal mask** | A lower triangle — each token may only see itself and what came before. This *is* GPT. |
| **Bidirectional** | No mask — every token sees everything. This *is* BERT. |
| **Multi-head** | Several attentions in parallel on slices of the dimensions, each free to specialise. |
| **Residual connection** | `y = F(x) + x`. Gives the gradient an unobstructed path backwards. |
| **LayerNorm** | Normalises across the features of one sample. Used instead of BatchNorm because sequences vary in length. |
| **Feed-forward network** | Two linear layers per position; where most parameters live. |
| **Transformer block** | attention → add & norm → feed-forward → add & norm. Stack it 12× for BERT-base. |

---

## The build plan, cell by cell

The notebook follows this order. Each `# TODO` is one idea — do them in sequence.

| Cell | What you build | The one line that matters |
|---|---|---|
| 1–2 | Setup, toy sentence | — |
| **3** | `softmax(x)` | Subtract the max before `exp` — otherwise large scores overflow to `inf` |
| **4** | `attention(Q, K, V)` | `scores = Q @ K.T / np.sqrt(d_k)` |
| 5 | Run it on the toy sentence | Read the weight matrix — each row sums to 1 |
| **6** | `causal_mask(n)` | `np.tril(np.ones((n, n)))` |
| 7 | BERT mode vs GPT mode, side by side | The upper triangle becomes exactly 0 |
| **8** | `positional_encoding(seq_len, d)` | Even dims get `sin`, odd dims get `cos` |
| 9 | Prove attention is permutation-invariant without it | Shuffle the input, get the same output |
| **10** | `multi_head_attention(...)` | Split `d_model` into `h` heads of `d_model // h` |
| **11** | `layer_norm(x)` | Normalise over the **last** axis, not the batch |
| **12** | `transformer_block(x)` | `x = layer_norm(x + attn(x))` then `x = layer_norm(x + ffn(x))` |
| 13 | Stack blocks, watch representations change | — |
| 14 | Stretch exercises | — |

### The five checkpoints

If these five outputs are right, everything is right:

1. **Softmax rows sum to 1.** `np.allclose(weights.sum(axis=-1), 1.0)` → `True`.
2. **Causal weights are lower-triangular.** Every entry above the diagonal is exactly `0.0`.
3. **Row 0 of a causal attention is `[1, 0, 0, …]`.** The first token can only attend to itself, so its weight
   must be 1 — a good sanity check that your mask is applied *before* the softmax, not after.
4. **Without positional encoding, shuffling the input shuffles the output identically** — proving permutation
   invariance. With it, the outputs genuinely differ.
5. **Multi-head output has the same shape as single-head output.** Heads split the dimensions, they do not add to them.

---

## The traps, in advance

These are the mistakes that will actually cost you time.

- **Masking after the softmax instead of before.** If you zero the weights afterwards, the rows no longer sum to
  1 and the maths is wrong. Add `−1e9` to the *scores*, then softmax.
- **Forgetting `keepdims=True`** in softmax. `x.max(axis=-1)` drops a dimension and broadcasting silently does
  the wrong thing. This bug does not raise an error — it just gives wrong numbers.
- **Transposing the wrong axes.** `K.T` is fine for a 2-D array but wrong once you add a head dimension; you
  need `K.transpose(0, 2, 1)` or `np.swapaxes(K, -1, -2)`.
- **Normalising over the wrong axis in LayerNorm.** It is the *feature* axis (`axis=-1`), one sample at a time.
  Averaging across the batch is BatchNorm, which is a different thing entirely.
- **Expecting meaningful attention patterns from random weights.** Our matrices are random, so the patterns are
  noise. You are verifying the *mechanism*, not the linguistics. Real patterns need training.

---

## Progress checklist

Tick as you go.

- [ ] Read `explainer.html` end to end, including the step-by-step attention walkthrough
- [ ] Scored at least 6/7 on the self-check quiz
- [ ] `softmax` written and verified numerically stable on `[1000, 1001, 1002]`
- [ ] `scaled_dot_product_attention` written; weight rows sum to 1
- [ ] Explained out loud why we divide by √d_k
- [ ] `causal_mask` written; upper triangle is exactly zero
- [ ] Printed the BERT-vs-GPT weight matrices side by side and can point at the difference
- [ ] `positional_encoding` written; permutation-invariance demonstrated and then fixed
- [ ] `multi_head_attention` written; output shape unchanged
- [ ] `layer_norm` written over the correct axis
- [ ] `transformer_block` assembled with both residual connections
- [ ] Can state the six memorised sentences from the explainer without looking

---

## How this connects to the interview prep

The material in `interview-preparation/` covers these at answer level; this topic is where you actually
understand them.

| Question | Where |
|---|---|
| What is a Transformer and why did it replace RNNs? | `top-100-questions.md` Q84 |
| Explain self-attention, Q/K/V, multi-head | Q85 |
| Why positional encoding? | Q86 |
| **BERT vs GPT** | Q87 |
| Tokens, context window, temperature | Q88 |
| Implement scaled dot-product attention | `coding-questions.md` Q60 |
| Attention and why Transformers replaced RNNs | `deep-learning.md` Q71–Q72 |

Having built it, you can answer Q85 with "let me walk you through it with three tokens" instead of reciting the
formula. That is a noticeably different interview.

---

## Where to go next

- **Add a decoder cross-attention layer** — queries from the decoder, keys and values from the encoder. That is
  the encoder–decoder architecture (T5, BART, the original translation model).
- **Implement greedy decoding** — run the causal model, take the argmax, append it, run again. That loop is text
  generation.
- **Then** install `transformers` and load `distilbert-base-uncased`. Print
  `model.config.num_attention_heads` and `model.config.num_hidden_layers` and recognise every field. The library
  will feel obvious rather than magical.
