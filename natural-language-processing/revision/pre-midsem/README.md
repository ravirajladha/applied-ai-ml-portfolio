# NLP Pre-Midsem — Endsem Exam Pack

**AIMLCLZG525 · End-Semester Test · Q1 + Q2 = 10 of 40 marks**

## ⚠️ Read this first — it saves you hours

In the **End-Semester** exam, pre-midsem material is **only Q1 and Q2**. Across
**all four** past papers, those two questions have been the **same two topics
every single time**:

| Q | Marks | Always asks | Chapters needed |
|---|---|---|---|
| **Q1** | 5 | **(A)** bigram probability with **Laplace smoothing** · **(B)** a **neural LM forward pass** ending in **softmax** | 4, 5 |
| **Q2** | 5 | **HMM** — the **Viterbi** algorithm or the **Forward** algorithm | 6 |

**Chapters 1, 7 and 8** — intro/ambiguity, Bi-LSTM/BERT, prompting — **have
never appeared in Q1 or Q2** of an endsem. They were tested in the
*mid-semester* test. Skip them unless you have spare time.

> ### 🛑 Correction — chapters 2 and 3 are back in scope
> This file used to tell you to skip **vector semantics / TF-IDF / word2vec**
> too, on the evidence of four past papers. **The official question-paper
> structure overrides that**: it lists *Module 2: Vector Semantics — Problem*
> inside the 5-mark Q1, alongside the language-model problems.
>
> TF-IDF, cosine similarity and PPMI are live. They are short sums —
> do them in [`../scheme-drill/SIMPLE-NUMERICALS.md`](../scheme-drill/SIMPLE-NUMERICALS.md) §1,
> about fifteen minutes for all three.

## Three files

| # | File | What it is | What you do |
|---|---|---|---|
| **1** | 🧠 **`CHEATSHEET`** (10 pp) | The theory for exactly those three things — Laplace, forward pass, HMM. Plain English, every term defined | **READ** — ~20 min total |
| **2** | 📘 **`SOLVED-NUMERICALS`** (22 pp) | **Every real Q1 and Q2 from all four past papers**, question as printed + full solution, then 5 practice questions | **WORK** through it |
| **3** | ✏️ **`MARGIN-NOTES`** (16 pp) | **What to pencil into the printed handout, page by page.** Keyed to `notes/NLP_Handout_Part1_Sessions_1-8 (1).pdf` — five pages carry all 10 marks | **COPY** into the margins before the exam |

Each exists as `.pdf` (print) and `.html` (dark, on screen, answers hidden until
you click) plus the `.md` source.

## The whole 10 marks

| | Formula |
|---|---|
| **Laplace** | `P = (count(w1 w2) + 1) / (count(w1) + V)` — **add V, not 1** |
| **Forward pass** | `z = Σ wᵢxᵢ + b` → `h = ReLU/Sigmoid(z)` → scores → softmax |
| **Softmax** | `e^(z_A) / (e^(z_A) + e^(z_B))` |
| **Viterbi cell** | `MAX(prev × transition) × emission` + backpointer |
| **Forward cell** | `SUM(prev × transition) × emission` |

**Viterbi = MAX** (best sequence). **Forward = SUM** (total probability).
Otherwise the two are identical — learn one, you have both.

## Timing

10 marks of 40 ≈ **35 minutes**. Do these **after** the easy post-midsem
questions (Q4 attention, Q7 MMR), not before.

## ⚠️ One official answer key is wrong

The **Oct 2024 Q2** printed solution swaps two transition probabilities — it uses
`a(S2→S2)` where it needs `a(S2→S1)` and vice versa, and its stated totals don't
match its own arithmetic. The correct working and a one-sentence defence are in
`SOLVED-NUMERICALS`. Don't copy that key.

## Rebuilding

```bash
python build_html.py          # HTML only
python build_html.py --pdf    # HTML + PDF  (needs Chrome or Edge)
```
Edit the `.md` files — they are the source of truth. Close any open PDF first,
or Windows locks it and the rebuild silently keeps the old copy.

## Sources

Question papers in `../../notes/question papers/` and slide decks in
`../../slides/`. **Every number was recomputed independently** and agrees with
the official keys — except the Oct 2024 Q2 case noted above, which is flagged
in place.

## Related

- **Post-midsem pack** — [`../post-midsem/`](../post-midsem/README.md) — **30 of
  40 marks. Spend most of your time there.**
- **Full chapter notes + interactive explainers** for all of chapters 1–8 (for
  the *mid-semester* test rather than the endsem) — [`../`](../README.md)
