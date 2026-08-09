# Experiment facts — the single source of truth for the paper

**Read this file instead of the notebook.** Every number the paper needs is
here. `assignment2.ipynb` is ~200 KB and re-reading it in each writing session
is the single biggest waste of context in this project.

All values below were extracted from the *executed* notebook on 2026-08-09 —
the same run that produced `Group140.pdf`. If a number appears differently in
`TEAM_UPDATE.md` or `JOURNEY.md`, **this file wins** (see "Known discrepancy").

---

## 1. Task

Abstractive summarization of individual customer product reviews, plus an
aggregate "what do customers praise / criticise" verdict over many reviews of
one product. BITS Pilani WILP, NLP course, Problem Statement 11.

## 2. Dataset

| Property | Value |
|---|---|
| Source | Amazon Fine Food Reviews (`jhan21/amazon-food-reviews-dataset`) |
| Total rows available | 568,454 |
| Reference summary | the customer's own review headline (`Summary` column) |
| Mean review length | 80.3 words |
| Median review length | 56 words |
| 90th percentile | 161 words |
| Longest review | 3,432 words |
| Mean summary length | 4.1 words |
| Median summary length | 4 words |
| 90th percentile summary | 8 words |
| Longest summary | 42 words |
| Share of 4–5 star reviews | 78.1% |

**This is the paper's central design fact:** references are 4-word headlines,
not paragraph abstracts. Everything about the ROUGE discussion follows from it.

### Filtering

Keep a row only if `50 ≤ review chars ≤ 2000` and `10 ≤ summary chars ≤ 80`.
Filter retains **84.6%** of rows (3,383 of a 4,000 sample).

### Splits (seed 42)

| Split | Size |
|---|---|
| Train | 4,000 |
| Validation | 300 |
| Test (written to disk) | 500 |
| **Test actually scored** | **300** |

## 3. Model and training

| Setting | Value |
|---|---|
| Base model | `t5-small` (60M params) |
| Task prefix | `"summarize: "` |
| Max input tokens (training) | 128 |
| Max input tokens (inference) | 256 |
| Max target tokens | 32 |
| Epochs | 1.0 |
| Batch size | 8 |
| Learning rate | 3e-4 |
| Beams | 4 |
| `no_repeat_ngram_size` | 2 |
| Hardware | CPU only (x64 Anaconda under emulation on Windows ARM64) |
| Training wall-clock | **Unrecoverable — do not cite a number.** See below. |

Training truncates to 128 tokens while inference allows 256: attention cost is
quadratic in sequence length, and the median review is 74 tokens, so little is
lost. This asymmetry is a legitimate methods detail for the paper.

### Training time — resolved 2026-08-09: it cannot be recovered

`README.md` said ~50 min; `TEAM_UPDATE.md` said ~112 min. Checked for evidence:
`models/_checkpoints/` is **empty**, there is no `trainer_state.json` beside the
saved model, and no timing is logged anywhere in `train_t5.py` or `train.py`.
Both figures are unsourced recollections.

**Decision: the paper reports no wall-clock figure.** It states CPU-only, one
epoch, 4,000 examples, and says explicitly that the run was not instrumented.
That is honest and costs the argument nothing. If we ever want the number, it
requires re-running training with timing instrumentation — a new experiment,
which is out of scope for this paper.

## 4. Main result — ROUGE on 300 held-out reviews

| Model | ROUGE-1 | ROUGE-2 | ROUGE-L |
|---|---|---|---|
| Lead-1 (first sentence, extractive) | 0.1255 | 0.0341 | 0.1145 |
| `t5-small`, **not** fine-tuned | 0.1086 | 0.0266 | 0.0974 |
| `t5-small`, **fine-tuned** (ours) | **0.1751** | **0.0448** | **0.1723** |

Derived numbers:
- Fine-tuning over the un-tuned model: **+61.2%** ROUGE-1
- Fine-tuned over Lead-1: **+39.5%** ROUGE-1
- The un-tuned model scores **13.5% below** the trivial Lead-1 baseline

### Known discrepancy

`TEAM_UPDATE.md` quotes 0.1744 / 0.1245 for the fine-tuned and Lead-1 ROUGE-1.
Those come from an **earlier run**. The executed notebook and `Group140.pdf`
say 0.1751 / 0.1255. **Use the notebook values.** Fix the docs, or state the
run explicitly, before the paper quotes anything.

### Evaluation-set size effect (anecdotal, not a controlled sweep)

An early check on **24** reviews gave ROUGE-1 **0.234**; the full **300** gave
**0.174**. The small sample was optimistic by roughly a third. This is a real
observation but was not run as a proper sweep — the paper must either present
it as an anecdote or we run the sweep properly.

## 5. Qualitative examples (test set, model vs human headline)

| Human headline | Model output |
|---|---|
| totally worth the money!!! | he loves it! |
| i like this stuff! | i love this cereal! |
| best i have found | good taste, good quality |
| offensive gas producer!!! | a great treat! |

The fourth row is the informative failure: the review praises the treat then
complains about flatulence; the model keeps the praise and drops the complaint.
Good material for an error-analysis section.

## 6. Aggregate demo — product B002FJM9SU (baby formula)

| Property | Value |
|---|---|
| Reviews | 60 |
| Average stars | 3.13 |
| VADER sentiment split | 46 positive, 13 negative, 1 neutral |

Generated verdict:

> Most customers are happy with this product (46 positive, 13 negative, 1
> neutral out of 60 reviews). Most praised: formula, milk, earth, breast,
> months. Most criticised: formulas, hard, health, levels, constipation.
> Typical review headline: "i love this formula!".

| Praised | n | Criticised | n |
|---|---|---|---|
| formula | 82 | formulas | 11 |
| milk | 22 | hard | 10 |
| earth | 15 | health | 9 |
| breast | 13 | levels | 9 |
| months | 13 | constipation | 8 |
| breast milk | 12 | pain | 8 |
| babies | 11 | baby formula | 7 |
| brand | 11 | child | 7 |

**The paper's second finding.** Per-review summaries read broadly positive, but
the aggregate criticism list surfaces *arsenic levels*, *constipation* and
*health* — customers discussing arsenic contamination in baby formula. Some
individual generated summaries state it outright:

> "baby's only, both dairy and soy formulas, contain arsenic levels 20-30x more
> than the …"
> "inorganic arsenic levels equal or higher than fda standard for drinking water"

A 3.13 star average hides this entirely. This is the strongest argument in the
paper for aggregation over per-item summarization.

**Known weakness:** `formula` heads the praised list while `formulas` heads the
criticised one. Singular/plural are collapsed only *within* a list, not across.
A lemmatiser fixes it. Must be declared as a limitation.

## 7. Aspect mining method

Not a trained ABSA model. Sentence-split → VADER sentiment per sentence → rank
phrases by how *distinctive* they are to the positive vs negative side.

| Parameter | Value |
|---|---|
| Top-k aspects | 8 |
| Min mentions to count | 2 |
| Aspect skew (share on one side) | 0.6 |
| Positive/negative sentence threshold | ±0.2 |
| Positive/negative review threshold | ±0.05 |

Limitation to declare: cannot resolve a negated aspect inside an otherwise
positive sentence.

Details confirmed by reading `aspects.py` (2026-08-09), not previously written
down anywhere:

- Candidates are **unigrams and bigrams**.
- Stop words are sklearn's English list **plus a hand-built opinion-word list**
  (`good`, `love`, `disappointed`, and transaction filler like `product`,
  `amazon`, `bought`). Without it the "aspects" would be verdicts.
- Selection is **contrastive by rate, not raw frequency**: a term is listed on
  a side only if its share of usage there is $\geq 0.6$ (~1.5x more often).
  Rates rather than counts because the two sentence pools differ in size.
- A unigram is dropped when a bigram containing it has an equal or higher
  count, so "battery life" beats "battery".
- **Two different thresholds:** sentences use $\pm0.2$ (strict — only clearly
  polar sentences contribute aspects), whole reviews use $\pm0.05$ (loose) for
  the positive/negative/neutral counts.
- `polarity_share` **excludes neutral reviews** on purpose. With 3 pos / 3 neg
  / 2 neutral, including them gives 0.375 and reads as "mostly unhappy"; the
  correct reading is "mixed".
- There is a **non-NLTK fallback lexicon** so the app never hard-fails offline
  — relevant to the OSHA-lab question.

## 7b. Two facts found by reading the code — both belong in the paper

**The map--reduce ceiling is not removed, only raised.** The reduce step joins
the per-review summaries into one pseudo-document and passes it back through
the *same* encoder, which still accepts only 256 tokens. At four to six tokens
per summary, one reduce pass saturates around **40--50 reviews**; past that,
later summaries are truncated exactly as raw reviews would have been. The demo
uses **60 reviews**, so it sits just inside the regime where mild truncation is
possible. A hierarchical reduce (reduce in batches, then reduce the results)
would fix it. Not implemented. Declare this honestly — a reviewer would find it.

**The reported verdict is a template, not end-to-end generation.** The
paragraph the app displays is assembled from (a) a mood phrase chosen by
threshold from `polarity_share`, (b) the top five praised and criticised
aspects, and (c) the reduce step's generated sentence quoted verbatim. The
neural model contributes the summaries and the quoted sentence; the sentence
around them is a fixed template. The paper must not imply the whole paragraph
was generated.

## 8. The LSTM baseline — written, never trained

`model_lstm.py` + `attention.py`: bidirectional LSTM encoder, Bahdanau additive
attention, teacher forcing, gradient clipping, ~2.1M parameters. Verified to
learn (loss 3.3 → 0.003 on a toy set) but **never trained on the real data**,
so it does not appear in the ROUGE table.

Config if we ever train it: vocab 12,000 · embed 128 · hidden 256 · input 80
words · target 12 · batch 32 · 3 epochs · lr 1e-3 · train size 8,000.

**Decision for this paper (2026-08-09): we write up existing results only, so
the LSTM stays out of the results table.** It is discussed as an unrun
comparison and named as the primary limitation.

---

## What this paper can honestly claim

1. Fine-tuning a small pretrained encoder–decoder on in-domain data beats both
   a trivial extractive baseline and the same model un-tuned.
2. **An un-tuned pretrained model can score below a trivial baseline** because
   it produces the right content in the wrong *form* — fluent sentences where
   the task wants a terse headline. Fluency is not task fit.
3. Aggregate aspect mining surfaces safety-relevant complaints that both the
   star average and the per-review summaries conceal.
4. ROUGE against ~4-word references is compressed and near-floor for ROUGE-2;
   absolute values must not be compared to paragraph-summarization benchmarks.

## What it cannot claim

- No from-scratch vs pretrained comparison (LSTM untrained).
- No statistical significance testing on the ROUGE differences.
- One dataset, one domain, one model size, one seed, one epoch.
- The eval-size observation is anecdotal, not a sweep.
- No human evaluation; no faithfulness metric.
