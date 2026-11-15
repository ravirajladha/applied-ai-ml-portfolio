# The Transformer: from attention to next token — build guide

**Topic 02 · Large Language Models for Generative AI · practice**

| File | What it is |
|------|------------|
| `explainer.html` | **Open this first.** Interactive lesson: the 4-station assembly line, "it → animal / street" attention, a live Q·K·V slider, the causal-mask grid, heads, a block stepper, a click-to-generate LM head, the real `print(model)` of your assignment model, a skip list and a 6-question quiz. |
| `practice.ipynb` | Template notebook. Part A (numpy only, runs on this laptop) has short `# TODO` lines. Part B (optional) opens real GPT-2 / Qwen2.5 on the lab server. |
| `guide.md` | This file: schedule, recap, build plan, checklist. |

Sources: Session 1 note §6 & §11 (`../../materials/notes/Session-01-Intro-to-LLMs.md`), CS-1 slide 13, Alammar *Hands-On LLMs* ch. 3 (optional).

---

## ⏱️ When and how long

**Total: about 6–7 hours, spread over 5 days, about 1–1.5 h a day.** Fit it **between the Session 1 note and the Session 2 note**:

- The Session 1 note ends at "Transformer blocks → Module 3". This topic fills that gap.
- The professor asked everyone to revise attention and the Transformer before the architecture module. That module starts right after QLoRA, so in the next class or the one after.
- Your Assignment 1A `target_modules=['q_proj','v_proj']` only makes sense once you know what Wq and Wv are.

| Day | Do | Time | Done when |
|-----|----|------|-----------|
| **Sun 15-Nov** (today) | Finish `Session-01-Intro-to-LLMs.md`. Stop after §11. Read §12–13 quickly; they weren't taught. | ~1–1.5 h | You can do the BPE self-check on paper |
| **Mon 16** | `explainer.html` §1–4 (assembly line, attention, Q/K/V, mask). Click every demo. | 1 h | You can say "Q = search, K = label, V = content" and why the mask exists |
| **Tue 17** | Notebook cells 0–6 (attention by hand) | 1–1.5 h | ✅ on cell 6 |
| **Wed 18** | Explainer §5–7, then notebook cells 7–10 (heads, block, LM head, 124M) | 1.5 h | ✅ on cell 10 |
| **Thu 19** | ⚠️ **Submit the 1A/1B preference form today (deadline).** Then explainer §8 and quiz §10 (aim for 5/6). Part B on the lab server if it's set up; otherwise skip it. | 1 h | Quiz ≥ 5/6, and you can point at `q_proj` in the printout |
| **Fri 20** | Cell 15: write the 4 answers in your own words. Then start the Session 2 note §1–4 (it reuses causal mask and teacher forcing). | 1 h | 4 answers written |
| **Sat 21** | Class. You'll be ahead on architecture. | — | — |

Breaks are part of the plan: stop at the "Done when" line even if you feel like pushing on.

**Order after this:** Session 2 note → Session 3 note (around Webinar 1 next week) → Assignment 1A.

---

## The problem statement

Build, with plain numpy, the middle of an LLM for `"The cat sat down"`:

`embeddings + position → Q, K, V → scores → causal mask → softmax → blend values → multi-head → block (attention + FFN + residual + norm) × 3 → LM head → next-token probabilities`

Then (optional) find every one of those parts by name inside real GPT-2 and Qwen2.5-0.5B.

---

## Plain-English recap

| Term | In one line |
|------|-------------|
| **Transformer** | The neural network inside every modern LLM: a stack of identical blocks. |
| **Self-attention** | Each token pulls in information from other tokens; makes embeddings contextual. |
| **Query / Key / Value** | What I'm looking for / my label / what I hand over. Three learned matrices `Wq, Wk, Wv` (`q_proj, k_proj, v_proj`). |
| **Score** | `Q·K / √d`: how well a query matches a key. |
| **Attention weights** | Softmax of the scores; each row adds up to 1. |
| **Causal mask** | Blocks the future (`−∞` before softmax) so a decoder can't cheat. |
| **Multi-head** | Several small attentions in parallel, concatenated, mixed by `Wo` (`o_proj`). |
| **Feed-forward (FFN / MLP)** | Small network applied to each token separately: "think per token". |
| **Residual** | `x = x + sublayer(x)`. Add, never replace. |
| **Norm** | LayerNorm / RMSNorm keeps numbers in range. |
| **Block / layer** | Attention + FFN + 2 residuals + 2 norms. Same input and output shape, so blocks stack. |
| **LM head** | Last vector × `Eᵀ` → logits → softmax → next token. |
| **Formula** | `Attention(Q,K,V) = softmax(QKᵀ/√d)·V` |

---

## The build plan, cell by cell

| Cell | You write | Explainer § |
|------|-----------|-------------|
| 0 | *nothing*: setup, `X = E[ids] + P` | 1 |
| 1 | `softmax`: 2 lines | 3 |
| 2 | `Q, K, V_`: 3 lines | 3 |
| 3 | `scores`: 1 line | 3 |
| 4 | `masked` with `np.where`: 1 line | 4 |
| 5 | `weights`, `out`: 2 lines | 3 |
| 6 | `self_attention()`: 3 lines (reuse 3–5) | 3, 4 |
| 7 | `concat`: 1 line | 5 |
| 8 | the two residual lines | 6 |
| 9 | `logits`, `probs`, `next_id`: 3 lines | 7 |
| 10 | parameter count for GPT-2 small: 3 lines | 6 |
| 11–14 | *optional, lab server*: 4 name lookups on real models | 8 |
| 15 | 4 answers in your own words | all |

### Where people get stuck

- **Cell 1:** `e.sum(axis=axis, keepdims=True)`. Without `keepdims` the division breaks for 2-D input in cell 5.
- **Cell 3:** transpose is `.T` → `K.T`. `np.sqrt(d_k)` is 2 here.
- **Cell 4:** `np.where(mask, -np.inf, scores)` reads "where mask is True put −∞, else keep the score".
- **Cell 5:** `axis=-1` means "softmax each row". Rows are listeners.
- **Cell 6:** it's cells 3–5 again with new names (`s`, `m`, `Vv`).
- **Cell 8:** the shape of `x` must not change. If an assert says shape, you probably replaced `x` instead of adding to it.
- **Cell 12:** if `"Ġit"` isn't found, print `pieces` and look at the spelling.

---

## What to skip (deliberately)

RoPE and sinusoidal maths (taught in Module 3) · cross-attention internals · LayerNorm vs RMSNorm formulas · KV cache, FlashAttention, grouped-query maths (Modules 4–5) · backprop through attention · writing a full PyTorch Transformer from scratch.

---

## Progress checklist

- [ ] Session 1 note finished (§1–11 read, §12–13 skimmed)
- [ ] Explainer §1–4 + demos
- [ ] Cells 0–6 ✅
- [ ] Explainer §5–7
- [ ] Cells 7–10 ✅
- [ ] Explainer §8 + quiz ≥ 5/6
- [ ] (optional) Part B on the lab server
- [ ] Cell 15: 4 answers in my own words
- [ ] 1A/1B preference form submitted (19-Nov)
