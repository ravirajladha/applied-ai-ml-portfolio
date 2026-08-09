# The Journey — how this assignment was built

This file is the story of the project, written for someone who has **not** done
this before. Read it top to bottom and you should understand what was built,
why each choice was made, and what to do if you have to rebuild it.

---

## 1. What the assignment actually asks for

**Problem Statement 11 — Customer Review Text Summarization.**

An online shop has thousands of reviews per product. Nobody reads them all.
Build an app that reads many reviews and produces a short, honest summary —
including *what people liked* and *what people complained about*.

The marks break down like this (13 total):

| # | Task | Marks | Where it lives |
|---|------|-------|----------------|
| 1 | Problem analysis | 2 | `assignment2.ipynb` §1 (markdown) |
| 2 | Data collection + preprocessing | 2 | `config.py`, `data_prep.py` |
| 3 | Encoder–Decoder model | 3 | `model_t5.py`, `train_t5.py`, `aggregate.py`, `aspects.py` (and the `model_lstm.py` baseline) |
| 4 | Web application | 3 | `app.py`, `flask_app.py`, `summarizer_service.py` |
| 5 | Evaluation (ROUGE) + demo | 2 | `evaluate_rouge.py`, `demo_cases.py`, `assignment2.ipynb` §5 |
| 6 | Project report | 1 | exported PDF |

> These are the module names **after** the by-owner split described in §11b.
> Early in the build everything lived in `train.py` and `summarizer.py`; the
> rest of this log follows that history as it happened.

Plus 1 mark for running it on the BITS OSHA Virtual Lab.

---

## 2. A false start worth recording

The first PDF sitting in this folder was **PS-05, a Prolog decision tree for
diagnosing COVID/flu/dengue** — a completely different subject's assignment. A
working Prolog solution was actually built against it before the mistake was
caught.

That work was not thrown away; it was moved to
`artificial-and-computational-intelligence/assignments/assignment-2/`, where it
belongs.

**Lesson:** confirm the PDF matches the subject before writing a line of code.

---

## 3. Choosing the tools (and hitting a wall)

Before writing anything, the machine was inspected. Two surprises:

**Surprise 1 — this is an ARM64 laptop** (Snapdragon X, Windows on ARM). Most
deep-learning libraries are built for Intel/AMD x64 chips.

**Surprise 2 — there is no PyTorch for ARM64 Python on Windows.** The check
came back `No matching distribution found for torch`.

So the plan changed:

- **TensorFlow / Keras** — ruled out, no Windows-ARM64 build at all.
- **Native ARM64 Python 3.12** — ruled out, no PyTorch.
- **Anaconda x64 Python 3.13** — ✅ works. It runs under *emulation* (the ARM
  chip pretends to be an Intel chip), which is slower, but it already had
  `torch 2.6.0` and `streamlit` installed.

A **virtual environment** (`.venv`) was created on top of Anaconda. A virtual
environment is just a private folder of Python packages, so installing things
for this project cannot break anything else on the laptop. It was created with
`--system-site-packages` so it reuses the big `torch` install instead of
downloading it again.

> **Jargon:** *wheel* = a pre-built package file. If no wheel exists for your
> chip, the library simply cannot be installed the easy way.

---

## 4. Picking the model

The assignment says: build an **Encoder–Decoder (Seq2Seq/LSTM or Transformer)**.

### What "encoder–decoder" means, in plain English

Think of a translator who does not speak by echoing words. They:

1. **Listen** to the whole sentence and form a mental idea of it — this is the
   **encoder**. It squeezes the input text into a set of numbers ("meaning").
2. **Speak** a new sentence from that idea, one word at a time — this is the
   **decoder**.

This is exactly what summarization needs: read a long review (encode), then
write a short new sentence (decode). Because the decoder invents its own words
rather than copying, this is called **abstractive** summarization. Copying the
best existing sentence instead would be **extractive**.

### The two options considered

| Option | Pros | Cons |
|--------|------|------|
| Build an LSTM Seq2Seq from scratch | Clearly "I built it" | Summaries come out generic; low scores |
| Fine-tune **t5-small** (a Transformer) | Genuinely readable summaries | Starts from someone else's weights |

**t5-small was chosen.** The PDF explicitly permits "Transformer", and a model
that produces summaries a human would accept is worth more than one that
technically exists but writes nonsense.

> **Jargon:** *fine-tuning* = taking a model that already understands English
> and giving it extra practice on your specific job. Far cheaper than teaching
> language from zero.
>
> **Why t5-small?** T5 treats every task as text-in/text-out. You tell it the
> job with a prefix — here, `"summarize: "`. The `small` version has ~60 million
> parameters, which trains on a CPU in under an hour. The bigger versions would
> take days without a GPU.

---

## 5. Finding a dataset

The assignment allows any suitable summarization dataset. The natural fit is
**Amazon Fine Food Reviews**: every row has a long review *and* a short headline
the customer wrote themselves. That headline is a ready-made "correct answer".

Four candidate datasets were tried on the Hugging Face Hub. Three failed —
modern `datasets` refuses to run the old script-based loaders. The one that
worked:

```
jhan21/amazon-food-reviews-dataset   →  568,454 reviews
```

Its columns matter:

| Column | Used for |
|--------|----------|
| `Text` | the review — the model's **input** |
| `Summary` | the customer's headline — the **target** to learn |
| `Score` | 1–5 stars — a sanity check on sentiment |
| `ProductId` | groups reviews by product — powers the app's demo |

`ProductId` is the quiet hero: the problem statement asks for summaries of
*multiple* reviews of *one product*, and this column makes that possible.

---

## 6. Cleaning the text (Task 2)

Raw reviews are messy. `clean_text()` in `summarizer.py` does the tidying:

| Step | Why it matters |
|------|----------------|
| Unescape HTML, strip `<br/>` tags | Scraped text is full of markup |
| Remove URLs | Links carry no opinion |
| Lowercase | So `Great` and `great` are the same word |
| Expand contractions (`don't` → `do not`) | Fewer odd tokens to learn |
| Drop odd symbols, squeeze spaces | Removes noise |
| **Keep `. ! ?`** | Needed later to split into sentences |

That last row is deliberate. Most tutorials strip all punctuation; here the
aspect-mining step must break reviews into sentences, so sentence-enders stay.

Rows are then filtered — a review must be 50–2000 characters and its headline
10–80 characters. Headlines that merely repeat the review's opening are dropped,
because they would teach the model to copy rather than summarise.

> **Jargon:** *tokenization* = chopping text into the small pieces the model
> actually reads (roughly word fragments). `"summarize: great coffee"` becomes a
> list of numbers. Summaries are capped at 32 tokens. Inputs are capped at
> **128 tokens while training** (for speed — see section 7) but **256 when
> actually summarising**, where the extra length costs almost nothing.

---

## 7. Training (Task 3)

`train.py` does the work. The data is split three ways:

- **train** — the model learns from these
- **validation** — checked during training, to spot overfitting
- **test** — locked away until the very end, for honest scoring

Splitting matters: scoring a model on data it studied is like marking an exam
with the answer sheet visible.

The submitted run was:

```bash
python train.py --train-size 4000 --val-size 300 --test-size 500 --epochs 1
```

### A version trap worth knowing

The installed `transformers` was **v5**, a new major release that renamed things:

| Old (v4, most tutorials) | New (v5, used here) |
|---|---|
| `evaluation_strategy=` | `eval_strategy=` |
| `Seq2SeqTrainer(tokenizer=…)` | `Seq2SeqTrainer(processing_class=…)` |
| `warmup_ratio=` | `warmup_steps=` |
| `group_by_length=` | `sortish_sampler=` |

Copy-pasting a 2023 tutorial would have failed. The first three were caught by
probing the API with `inspect.signature` before writing the script. The fourth
was **not** — it was added later from memory, and the run crashed instantly with
`unexpected keyword argument 'group_by_length'`.

**Lesson:** when a library has just jumped a major version, check *every*
argument against the actual signature, not just the ones you happen to doubt.

### Getting the training size right — three wrong guesses

This is worth recording in full, because the first estimate was wrong by 4x.

**Guess 1 — "1 step per second".** A smoke test on 40 examples suggested a
20,000-review run would take ~45 minutes. It was left running.

**Reality check.** After 41 minutes it had completed **840 of 2,500 steps** and
was *slowing down* (3 s/step → 7 s/step). Projected time: about 4 hours. The
smoke test had lied because its tiny batches padded to a fraction of the real
sequence length.

**Guess 2 — bigger batches.** A benchmark suggested most of the per-step cost
was fixed overhead, so batch 16 should be nearly free. Wrong again: the
benchmark reused *one hot batch*, avoiding all the data-loading and
varying-shape costs of real training. Batch 16 measured **18 s/step** — worse
per example than batch 8.

**What actually worked.** Attention cost grows with the *square* of sequence
length, so the lever was length, not batch size:

| Change | Effect |
|---|---|
| Train at 128 tokens instead of 256 | median review is 74 tokens, so little is lost |
| Keep inference at 256 tokens | generation is dominated by decoding, so length is cheap there |
| `sortish_sampler=True` | groups similar-length reviews so padding wastes less |
| Skip beam-search eval during training | generating over the val set cost more than training itself |

Final measured rate: **~6 s/step at batch 8**, so 4,000 reviews ≈ 500 steps ≈
**50 minutes**.

> **The real lesson:** never size a long job from a micro-benchmark. Start the
> real thing, measure it for two minutes, *then* decide. An emulated x64 CPU on
> an ARM laptop is roughly two orders of magnitude slower than a GPU, and no
> amount of tuning changes that — only honest expectations do.

---

## 8. Finding what people praise and complain about

The model summarises *one* review at a time. The problem statement also wants
the **most frequently discussed positive and negative aspects** across all of
them. `analyse_aspects()` handles this without a second neural network:

1. Split every review into sentences.
2. Score each sentence's mood with **VADER**, a rule-based sentiment tool. It
   returns a number from −1 (angry) to +1 (delighted).
3. Put clearly positive sentences in one pile, clearly negative in another.
4. In each pile, count the most common 1- and 2-word phrases, ignoring
   stop-words (`the`, `and`) *and* opinion words (`good`, `love`, `terrible`).

Step 4's second filter is the important one. Without it every product's "top
positive aspect" is just the word *good*, which tells a buyer nothing. Removing
opinion words leaves the **thing being discussed** — `flavor`, `packaging`,
`shipping`, `price`.

Two-word phrases beat their own single words, so `battery life` is reported
instead of `battery` and `life` separately.

If VADER's word list cannot be downloaded, a small built-in list takes over, so
the app never crashes offline.

---

## 9. The web app (Task 4)

`app.py` uses **Streamlit**, chosen over Flask because it needs no HTML, CSS or
JavaScript — a text box is one line of Python.

The app offers three ways in: **paste text**, **upload** a `.txt`/`.csv`, or
**try the sample product**. It then shows the overall verdict, positive/negative
counts, two bar charts of praised and criticised aspects, and a table of
per-review summaries you can download as CSV.

Two details that make it robust:

- `@st.cache_resource` loads the model **once** instead of on every click.
- If no trained model exists, it falls back to plain `t5-small` and says so in
  the sidebar, rather than crashing.

---

## 10. Scoring it honestly (Task 5)

**ROUGE** is the standard summarization metric. It asks: *how much of the
human's summary did the model's summary recover?*

- **ROUGE-1** — overlap of single words
- **ROUGE-2** — overlap of word pairs (rewards correct phrasing)
- **ROUGE-L** — longest matching sequence (rewards correct order)

Scores are compared against two baselines so the number means something:

1. **Plain t5-small**, not fine-tuned — shows what the training actually bought.
2. **Lead-1** (just take the review's first sentence) — the classic "did we beat
   the dumbest possible method?" check.

A word of caution recorded honestly in the report: ROUGE only rewards *matching
words*. A summary can be perfectly accurate, use different vocabulary, and score
badly. The numbers are read alongside the actual generated text, never alone.

---

## 11. Progress checklist

- [x] Identify the correct problem statement (PS-11)
- [x] Survey the machine; discover the ARM64 / PyTorch constraint
- [x] Build an isolated `.venv` and install the stack
- [x] Find a dataset that loads and has review + headline pairs
- [x] Write `clean_text` / preprocessing (Task 2)
- [x] Write `train.py` and smoke-test it end to end
- [x] Fine-tune t5-small on 4,000 reviews (Task 3)
- [x] Write the aspect-mining logic
- [x] Build the Streamlit app (Task 4)
- [x] Score ROUGE against both baselines (Task 5)
- [x] Capture app screenshots
- [x] Run the notebook end to end and export it to PDF + HTML
- [ ] **Fill in group member names, BITS IDs, contribution %** (see `one.md` Q1)
- [x] **Rename the export to `Group140.pdf`** — group number confirmed as 140
- [ ] **Re-run on the BITS OSHA Virtual Lab** (1 mark, see `one.md` Q2)

---

## 11a. Two more traps, found the hard way

### Streamlit and PyTorch fight each other

Clicking any button in the app did nothing. The cause was in the Streamlit log,
not the browser: Streamlit's auto-reload watcher walks every imported module,
and PyTorch's `torch._classes` registry raises an exception when inspected that
way. The crash killed the re-run that a button click triggers.

Fixed with `.streamlit/config.toml`:

```toml
[server]
fileWatcherType = "none"
```

We do not need hot-reload to run the app, so nothing is lost.

### A "bad model output" that was really a bad regex

The app summarised one review as **"baby cow is milk"**. That looks like a
small language model producing nonsense, and it was written up as a model
failure. It was not.

`clean_text` expanded every `'s` into `" is"`. The original phrase was
*"a baby cow's milk"*, which became *"a baby cow is milk"* **before the model
ever saw it** — and the same corruption was applied to every training target.
Possessives are everywhere in product reviews (*"my daughter's snack"*,
*"the dog's bowl"*), so this quietly damaged a lot of text.

`'s` is the one genuinely ambiguous contraction: *"it's"* expands, *"cow's"*
must not. The rule now only expands after words that cannot take a possessive:

```python
_ITS_RE = re.compile(r"(it|he|she|that|there|here|what|who|this)'s")
```

> **Lesson:** when a model produces something strange, look at what you
> actually fed it before blaming the model. This was found by re-reading the
> preprocessing code, not by staring at the output.

### The notebook ran on the wrong Python

`jupyter nbconvert --execute` failed with `No module named 'matplotlib'`, even
though matplotlib was clearly installed. The reason: a notebook records a
*kernel name*, and the only kernel registered on this machine pointed at the
**native ARM64 Python** — the one that cannot even install PyTorch. The venv had
never been registered as a kernel.

```bash
.venv/Scripts/python.exe -m ipykernel install --user --name nlp-a2
```

> **Lesson:** "it works when I run the script" and "it works in the notebook"
> are different claims. A notebook has its own idea of which Python to use.

---

## 11b. Splitting the code by task and by owner

Once the project worked end to end, everything lived in three files. That is
fine for one person and wrong for a group of five: two people cannot own
`summarizer.py` at the same time without colliding in git.

The code was therefore split so that **each assignment task maps to a module,
and each module has exactly one owner**:

| Task | Modules | Owner |
|---|---|---|
| 2 — data | `config.py`, `data_prep.py` | Member 1 |
| 3.1 — LSTM baseline | `attention.py`, `model_lstm.py`, `train_lstm.py`, `infer_lstm.py` | Member 2 |
| 3.2 / 3.3 — Transformer | `model_t5.py`, `train_t5.py`, `aggregate.py`, `aspects.py` | Member 3 |
| 4 — application | `summarizer_service.py`, `app.py`, `flask_app.py`, `run_osha.sh` | Member 4 |
| 5 — evaluation | `evaluate_rouge.py`, `demo_cases.py` | Member 5 |

Nothing about the Transformer's behaviour changed — the code moved, it was not
rewritten. `summarizer.py` stayed behind as a thin re-export so the notebook
and any older script keep working.

Two genuinely new pieces came out of the split:

**Map–reduce aggregation** (`aggregate.py`). The encoder reads at most 256
tokens; fifty reviews are far longer than that, so feeding them in together
would silently discard most of them. Instead each review is summarised on its
own (*map*), then those summaries are summarised together (*reduce*). Every
review now influences the final verdict.

**A verdict bug the split exposed.** Running the new `demo_cases.py`, a set
with 3 positive, 3 negative and 2 neutral reviews was reported as *"Most
customers are unhappy"*. The mood was computed from
`positives / all reviews` = 0.375, so **neutral reviews dragged a balanced set
below the "mixed" threshold**. It now uses `positives / (positives + negatives)`
= 0.5, correctly "mixed".

> **Lesson:** writing the demo cases was what found the bug. Fixed inputs with
> known expected answers catch things that eyeballing one product never will.

---

## 12. If you have to rebuild this

```bash
"C:/ProgramData/anaconda3/python.exe" -m venv .venv --system-site-packages
./.venv/Scripts/python.exe -m pip install -r requirements.txt
./.venv/Scripts/python.exe train.py
./.venv/Scripts/python.exe -m streamlit run app.py
```

Things that will bite you, in order of likelihood:

1. **`transformers` v4 vs v5 argument names** — see the table in section 7.
2. **No PyTorch on ARM64 Python** — you must use the x64 Anaconda interpreter.
3. **Dataset loader errors** — old script-based Hub datasets no longer work;
   pick one stored as Parquet.
4. **Training feels frozen** — it is CPU-only under emulation. Time a few steps
   before assuming it has hung. Expect roughly 6 seconds per step.
5. **Sizing a run from a micro-benchmark** — see section 7. Start the real job,
   watch it for two minutes, then decide how big to make it.
6. **Training suddenly crawls** — one step took 24 minutes instead of 6 seconds.
   The laptop had only 1.3 GB of RAM free and had paged the trainer out. It
   recovered by itself, but closing browser tabs first would have avoided it.
7. **Buttons in the app do nothing** — the Streamlit/PyTorch watcher clash, see
   section 11a.
8. **Notebook says a package is missing that you know is installed** — wrong
   kernel, see section 11a.
