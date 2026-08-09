# Team update — NLP Assignment 2 (PS-11, Customer Review Summarization)

Repo: https://github.com/sumanthtps/customer-review-text-summarization

---

## Short version (paste this into the group chat)

> Hi team — I've pushed a working end-to-end version of PS-11 to the repo.
>
> **Model choice: I went with the Transformer route — a fine-tuned `t5-small`
> encoder–decoder — rather than building an LSTM Seq2Seq from scratch.** The
> problem statement allows either ("Seq2Seq/LSTM **or** Transformer"). I chose
> the Transformer because with the compute we have (CPU only, no GPU) an LSTM
> trained from scratch produces generic, often ungrammatical summaries, while
> fine-tuning a pretrained model gives summaries a human would actually accept.
>
> **What's working:** the full pipeline runs — data prep, training, summary
> generation, aspect analysis, and a Streamlit web app. ROUGE is measured
> against two baselines and our model beats both. The notebook is executed with
> all outputs and exported to PDF and HTML.
>
> **What I need from you:**
> 1. Everyone's name + BITS ID + contribution % (group number is confirmed: **140**)
> 2. Does anyone have the **OSHA Virtual Lab** working, and does it have
>    internet? That's worth 1 mark and may need a code change if it's offline.
> 3. Please sanity-check the **analysis/evaluation section** (see below) — I'd
>    like a second pair of eyes on the numbers before we submit.
>
> Everything is explained in `JOURNEY.md`, open questions are in `one.md`.

---

## Code is now split by task and by owner

The repo follows the 5-way work split, so nobody edits the same file:

| # | Role | Modules owned |
|---|---|---|
| 1 | Problem Analyst & Data Engineer | `config.py`, `data_prep.py` (Tasks 1–2) |
| 2 | DL Engineer – Baseline | `attention.py`, `model_lstm.py`, `train_lstm.py`, `infer_lstm.py` (Task 3.1) |
| 3 | DL Engineer – Transformer | `model_t5.py`, `train_t5.py`, `aggregate.py`, `aspects.py` (Tasks 3.2–3.3) |
| 4 | Application & DevOps | `summarizer_service.py`, `app.py`, `flask_app.py`, `run_osha.sh` (Task 4) |
| 5 | Evaluation Lead & Report Editor | `evaluate_rouge.py`, `demo_cases.py`, report (Tasks 5–6) |

**Before you change anything, run `python verify.py`.** It checks the whole
project in about a minute and prints PASS/FAIL per stage, so you never have to
guess whether a problem is yours or already there. `python verify.py --trace`
walks the pipeline stage by stage.

### The LSTM baseline is written but not trained

`model_lstm.py` and `attention.py` are complete — bidirectional LSTM encoder,
Bahdanau attention, teacher forcing, gradient clipping, ~2.1M parameters — and
verified to learn (loss 3.3 → 0.003 on a toy set). **Nobody has run the real
training yet**, so it does not appear in the ROUGE table. Member 2: run
`python train_lstm.py` when you have a few hours, and `evaluate_rouge.py` will
pick it up automatically.

---

## What is accomplished

| Task | Marks | Status | Where |
|---|---|---|---|
| 1. Problem analysis | 2 | Done | `assignment2.ipynb` §1 |
| 2. Data + preprocessing | 2 | Done | `data_prep.py`, `config.py` |
| 3.1 LSTM baseline | — | Written, **not trained** | `model_lstm.py`, `attention.py` |
| 3.2 Transformer + map–reduce | 3 | Done, trained | `model_t5.py`, `train_t5.py`, `aggregate.py` |
| 3.3 Aspect mining | — | Done | `aspects.py` |
| 4. Web application | 3 | Done, both run | `app.py`, `flask_app.py` |
| 5. Evaluation + demo | 2 | Done | `assignment2.ipynb` §5 |
| 6. Project report | 1 | Done (23 pages) | `Group140.pdf` |
| BITS OSHA Virtual Lab | 1 | **Not done** | needs lab access |

### The model

- **`t5-small` encoder–decoder, fine-tuned** on the Amazon Fine Food Reviews
  dataset (568,454 reviews; each row has the review text *and* the short
  headline the customer wrote, which serves as the reference summary).
- Trained on 4,000 reviews for 1 epoch, CPU only — about 112 minutes.
- Inputs capped at 128 tokens for training / 256 for inference; summaries at
  32 tokens.

### Results (300 held-out reviews the model never saw)

| Model | ROUGE-1 | ROUGE-2 | ROUGE-L |
|---|---|---|---|
| Lead-1 (just take the first sentence) | 0.1255 | 0.0341 | 0.1145 |
| `t5-small` **without** fine-tuning | 0.1086 | 0.0266 | 0.0974 |
| **Ours — fine-tuned `t5-small`** | **0.1751** | **0.0448** | **0.1723** |

> These are the numbers from the executed notebook, i.e. the ones printed in
> `Group140.pdf`. An earlier draft of this file quoted a slightly different run
> (0.1744 / 0.1245); if you have that version, discard it. Quote the notebook.

Two things worth noting for the viva:
- The un-tuned model scores **below** the trivial baseline. It writes fluent
  full sentences when the task wants a terse headline — the right words in the
  wrong shape.
- Fine-tuning lifted ROUGE-1 by **61%** over the un-tuned model, and also beat Lead-1, which is a
  deceptively strong baseline because customers often reuse their opening words
  in their headline.

### Beyond the model — the aspect analysis

The problem statement asks for "the most frequently discussed positive and
negative aspects", which a per-review summarizer alone cannot answer. We split
reviews into sentences, score each with VADER sentiment, then rank phrases by
how **distinctive** they are to the positive vs negative side.

For the demo product this surfaced something the summaries alone missed —
per-review summaries read broadly positive, but the aggregate complaint list
showed *constipation*, *health*, *levels* and *risks* (customers discussing
arsenic levels in baby formula). That's the signal a star rating hides.

---

## What is pending

**Blocking — we cannot submit without these:**

1. **Member details.** The group number (140) is now in the report and the
   export is named `Group140.pdf`, but page 1 still has placeholder names and
   BITS IDs for all five members. Send me yours and I'll fill them in.
2. **BITS OSHA Virtual Lab run** (1 mark, compulsory per the instructions).
   Key question: **does the lab have internet access?** The app currently
   downloads the `t5-small` checkpoint and the NLTK VADER lexicon on first run.
   If the lab is offline, we must bundle those locally — that is a code change,
   so please answer this early.

**Optional, our call as a group:**

3. **Longer training run.** We used 4,000 of 568,454 available reviews for one
   epoch because of CPU-only hardware. A longer overnight run would likely
   improve the scores. Worth doing if anyone has a GPU machine.
4. **Train the LSTM baseline.** The code is written and verified to learn, but
   nobody has run the real training. Doing so adds a from-scratch model to the
   ROUGE table, which is worth having if an evaluator wants to see one.
   `evaluate_rouge.py` picks it up automatically once trained.
5. **Code appendix in the report.** The `.py` sources are referenced but not
   pasted into the PDF. Evaluators often mark only what is in the submitted
   file, so we may want to paste them in.

---

## Please check the analysis section

I would like a second opinion on these specific points before we submit:

1. **Are the ROUGE numbers reasonable to quote?** They look low in absolute
   terms (ROUGE-2 of 0.044). I've argued in §5.3 that this is expected because
   the reference summaries are only 3–5 words, so there are very few bigrams to
   match, and these values should not be compared to paragraph-length
   summarization benchmarks. Does that argument hold up?

2. **Is comparing against Lead-1 and the un-tuned model enough?** Those are the
   two baselines I chose. Should we add anything else?

3. **Is the evaluation set big enough?** I used 300 held-out reviews. An early
   check on 24 reviews gave ROUGE-1 of 0.234 versus 0.174 on the full 300 — the
   small sample was optimistic by a third, which is why I moved to 300.

4. **The aspect analysis is frequency-based, not a trained ABSA model.** It
   finds *what* is discussed but cannot resolve a negated aspect inside an
   otherwise positive sentence. Is that an acceptable limitation to declare, or
   should we do more?

5. **One known rough edge:** singular and plural are collapsed only *within* a
   list, so "formula" can head the praised list while "formulas" heads the
   criticised one. A lemmatiser would fix it properly. Worth doing?

---

## How to run it yourself

```bash
git clone https://github.com/sumanthtps/customer-review-text-summarization.git
cd customer-review-text-summarization
python -m venv .venv
.venv/Scripts/activate            # Windows;  source .venv/bin/activate on Mac/Linux
pip install -r requirements.txt

python train.py                   # trains the model (~112 min on CPU)
streamlit run app.py              # opens the web app
```

The trained weights are **not** in the repo (234 MB) — `train.py` rebuilds them.
The app still runs before training, falling back to the plain `t5-small` and
saying so in the sidebar.

Read `JOURNEY.md` first if you want the reasoning behind every decision; it is
written to be readable without prior background.
