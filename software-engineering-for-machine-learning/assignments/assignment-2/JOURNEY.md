# The Journey — how this assignment was built, step by step

> **Read this if you are new to Python, new to ML, or just want to know *why* the code
> looks the way it does.** Nothing here assumes prior knowledge. Every new word is
> explained the first time it appears.

This is not a summary written after the fact. It is the actual order things happened in,
including the two tests that failed and what we changed to fix them.

**Course:** AIMLCZG546 — Software Engineering for Machine Learning
**Assignment:** II — Implementation, Code Quality & Quality Assurance
**Group:** 049

---

## Contents

- [Step 0 — What are we even building?](#step-0--what-are-we-even-building)
- [Step 1 — Read the requirements before writing a line of code](#step-1--read-the-requirements-before-writing-a-line-of-code)
- [Step 2 — Choose the problem](#step-2--choose-the-problem)
- [Step 3 — Set up the project skeleton](#step-3--set-up-the-project-skeleton)
- [Step 4 — Make the data](#step-4--make-the-data)
- [Step 5 — Build the data quality gate](#step-5--build-the-data-quality-gate)
- [Step 6 — Feature engineering](#step-6--feature-engineering)
- [Step 7 — Train the model](#step-7--train-the-model)
- [Step 8 — The first real problem: the model was bad](#step-8--the-first-real-problem-the-model-was-bad)
- [Step 9 — Inference](#step-9--inference)
- [Step 10 — The REST API](#step-10--the-rest-api)
- [Step 11 — Write the tests (and watch two of them fail)](#step-11--write-the-tests-and-watch-two-of-them-fail)
- [Step 12 — The research-code exhibit](#step-12--the-research-code-exhibit)
- [Step 13 — Formatting and linting: the before/after](#step-13--formatting-and-linting-the-beforeafter)
- [Step 14 — The monitor](#step-14--the-monitor)
- [Step 15 — The submission notebook](#step-15--the-submission-notebook)
- [The vocabulary list](#the-vocabulary-list)
- [If you want to run it yourself](#if-you-want-to-run-it-yourself)

---

## Step 0 — What are we even building?

Imagine you run an online store. Right now, someone is browsing. They have looked at
9 pages, spent 6 minutes, and put 2 items in their cart.

**Question:** will they actually buy something, or will they close the tab?

If we could answer that, we could do something useful — pop up a live-chat offer for the
people who are *almost* going to buy, and leave everyone else alone.

That is the whole system. Input: what a shopper has done so far in this visit.
Output: a probability between 0 and 1 that the visit ends in a purchase.

> **Jargon:** a *session* is one visit to the website, from arriving to leaving.
> *Conversion* means the session ended in a purchase.

But here is the thing — **Assignment II is not really about the model.** The model is a
50-line logistic regression. The assignment is about everything *around* the model:
is the code organised, does it log properly, does it have an API, is it tested?
So that is where almost all the effort went.

---

## Step 1 — Read the requirements before writing a line of code

The PDF asks for 9 things. Before starting, we turned them into a checklist, because
"I built something nice" is worth zero marks if it misses requirement 7b.

| # | Requirement | Our plan |
| --- | --- | --- |
| 1 | Modular design (OOP and/or functional) | Split into `ecom/` modules, one job each |
| 2 | Research code vs production code | Keep a messy prototype **on purpose**, next to the clean package |
| 3 | Logging + error handling in ≥3 modules | One logging setup, typed errors, 5 modules |
| 4 | black / flake8 / isort with before–after proof | Save real lint reports to `reports/` |
| 5 | REST API | FastAPI, 5 endpoints |
| 6 | ≥2 types of test | 3 types: data validation, unit, integration |
| 7 | ML tests: training + inference | Loss curve, overfit-a-batch, directional, invariance |
| 8 | ≥2 model metrics + ≥2 data metrics | 4 model metrics, 3 data metrics |
| 9 | Production testing + security | Shadow → canary → A/B; input validation |

**Lesson:** turn the requirements into a table first. It becomes your definition of "done".

---

## Step 2 — Choose the problem

The PDF allows either the Assignment I application or a new one. Assignment I was an
e-commerce recommender — good domain, but that codebase had grown big (two services,
CQRS, Docker, a dashboard).

Assignment II is graded on **code quality and testing**, not on architectural ambition.
A big codebase would have buried the very things being marked.

**Decision:** stay in the e-commerce world, but rebuild small and clean — *session
conversion prediction*. Same business story, a codebase you can read in one sitting.

**Lesson:** simple is not lazy. Simple is what makes the thing being graded visible.

---

## Step 3 — Set up the project skeleton

Before any ML, we decided where things live. The rule we followed: **one folder = one
kind of thing.**

```
assignment-2/
├── ecom/        the real code (a "package")
├── tests/       the tests
├── research/    the deliberately messy prototype
├── data/        CSV files
├── artifacts/   the trained model
├── reports/     lint reports, test reports, drift reports
└── 049.ipynb    the submission notebook
```

> **Jargon:** a *package* is just a folder of Python files with an `__init__.py` inside.
> That file can be empty — its presence is what lets you write `from ecom.features import ...`.

Three config files were written before any logic:

| File | What it controls |
| --- | --- |
| `pyproject.toml` | black (formatting), isort (import order), pytest settings |
| `setup.cfg` | flake8 (the linter) |
| `requirements.txt` | which libraries this project needs |

Then two files that everything else depends on:

**`ecom/config.py`** — every path, every column name, every threshold, in one place.
No magic numbers scattered through the code. If the data moves, you change one line.

**`ecom/logging_setup.py`** — logging configured once, for the whole package.

> **Jargon:** *logging* is `print()` grown up. A log line has a timestamp, a **level**
> (how serious it is), and the name of the module that produced it. And it goes to a
> file, so you can read it tomorrow — `print()` output vanishes when the terminal closes.

The three levels we use, and what each one means here:

| Level | Means | Real example from our logs |
| --- | --- | --- |
| `INFO` | Normal progress | `Loaded 5000 rows, 9 columns` |
| `WARNING` | Survivable, but a human should know | `Drift detected in 'pages_viewed' (PSI=1.690)` |
| `ERROR` | The operation failed | `Model artifact not found at artifacts/model.joblib` |

**Lesson:** config and logging are boring, which is exactly why you do them first.
Retro-fitting logging into finished code is miserable.

---

## Step 4 — Make the data

We have no real store, so `ecom/data_ingestion.py` generates a fake one.

Two classes:

- **`SessionDataGenerator`** — invents 5,000 browsing sessions.
- **`DataIngestor`** — reads a CSV from disk, and fails *clearly* when it cannot.

The generator does not throw dice blindly. It builds a hidden "purchase intent" score
from the things that genuinely drive buying:

```python
score = (-3.0
         + 0.18 * pages          # more browsing  -> more likely
         + 1.30 * cart_items     # items in cart  -> much more likely
         + 0.80 * returning      # loyal customer -> more likely
         + 0.70 * discount       # a deal         -> more likely
         - 0.0004 * price)       # expensive      -> less likely
```

That score is squashed into a probability, and a coin weighted by that probability decides
whether the session converted. So the pattern is real, but noisy — like real life.

Two deliberate touches of realism:

1. **1% of prices are missing.** Real data feeds are never complete. If our code cannot
   survive a `NaN`, better to find out now.
2. **A second "live traffic" file with drift.** Shorter, more mobile-heavy sessions —
   what happens after a marketing campaign changes who visits your store. We need this
   later to prove drift detection actually detects something.

> **Jargon:** `NaN` means "Not a Number" — pandas' way of saying this cell is empty.
> *Drift* is when live data stops looking like the data you trained on. Your model does
> not break loudly; it just quietly gets worse.

**The error handling in `DataIngestor.load()`** covers three failures, each with its own
log line and a typed error:

| What went wrong | What the user sees |
| --- | --- |
| File does not exist | `DataIngestionError: Data file not found: data/x.csv` |
| File is corrupt | `DataIngestionError: Could not read data/x.csv` |
| File is empty | `DataIngestionError: Data file is empty: data/x.csv` |

Compare that to what you get without it: a 40-line stack trace ending somewhere inside
pandas. Same bug, ten times longer to diagnose.

---

## Step 5 — Build the data quality gate

`ecom/data_validation.py` answers one question: **is this data safe to use?**

> **Why this exists:** in normal software, bad input causes a crash and you notice.
> In ML, bad input causes *slightly wrong predictions* and nobody notices for six months.
> Garbage in, garbage out — but silently.

Three checks, and each one produces a **number** (that matters — requirement 8b asks for
data quality *metrics*, not just checks):

**1. Schema conformance** — are all 8 agreed columns present, with the right type?
Score = fraction that pass. `1.0` is perfect; drop two columns and you get `0.75`.

> **Jargon:** a *schema* is the agreed shape of your data — which columns exist and what
> type each one is. It is a contract between whoever sends the data and whoever uses it.

**2. Missing value rate** — what fraction of each column is empty? Above 5%, we refuse
to train. Between 0% and 5%, we log a `WARNING` and continue.

**3. PSI (Population Stability Index)** — the drift number.

Here is PSI in plain English. Take the training data and chop it into 10 buckets by size
(the smallest 10% of sessions, the next 10%, and so on). Now take today's live data and
count how many of *its* rows fall into each of those same buckets. If the two sets of
counts match, nothing has changed. If today's data piles up in the low buckets and the
high buckets are empty, something has shifted.

PSI turns that comparison into one number:

| PSI | Meaning |
| --- | --- |
| < 0.10 | No real change |
| 0.10 – 0.20 | Worth watching |
| **> 0.20** | **Significant drift — consider retraining** |

The validator can run in two modes, which turned out to matter a lot:

- `strict=True` — raise an error and stop. Used during **training**: never train on data
  you do not trust.
- `strict=False` — report the problems and carry on. Used by the **monitor**: a monitoring
  job that crashes is a monitoring job nobody keeps running.

**Lesson:** the same check needs different behaviour in different places. Make that a
parameter, not two copies of the function.

---

## Step 6 — Feature engineering

`ecom/features.py` turns raw session data into numbers the model can learn from.

> **Jargon:** a *feature* is one input column to the model. *Feature engineering* is
> inventing better columns from the ones you already have.

This module is written as **pure functions** — no classes, no stored state. Same input,
same output, every time.

> **Jargon:** a *pure function* only looks at its arguments and only returns a value.
> It does not read global variables, does not write files, does not remember anything.
> That makes it trivially testable: call it, check the answer.

Every other module in this project uses classes. This one does not, on purpose — and the
reason is the single most common bug in production ML.

**Training–serving skew.** You clean your data one way in the training script, then write
the API separately and clean it *slightly* differently. The model now sees inputs at
serving time that do not match what it learned from. Nothing crashes. The predictions are
just quietly wrong.

The fix here is structural: there is exactly **one** `build_features()` function, and both
`train.py` and `predict.py` import it. There is no second copy to drift away.

The three derived features:

| Feature | Formula | The intuition |
| --- | --- | --- |
| `pages_per_minute` | `pages / (duration + 1)` | Fast clicking = skimming. Slow = actually reading. |
| `cart_value` | `cart_items × avg_price` | Three ₹100 items ≠ three ₹10,000 items |
| `has_cart` | `cart_items > 0` | Crossing from zero to one item is the big jump |

Why `+ 1` in the first formula? A session can last 0 minutes. Dividing by zero gives
infinity, and infinity breaks the model. Adding 1 costs almost nothing and makes the
function total — it works for every possible input.

**The device column** gets *one-hot encoded*: `device = "mobile"` becomes three columns,
`device_mobile = 1, device_desktop = 0, device_tablet = 0`. Models do maths on numbers,
and you cannot multiply the word "mobile".

We also handled a device we have never seen — say `"smart-fridge"`. It encodes as all
zeros and logs a `WARNING`. It does **not** crash. A new device type appearing in the wild
should degrade one prediction, not take the service down.

---

## Step 7 — Train the model

`ecom/train.py`, one class: `ModelTrainer`.

The model is a **sklearn Pipeline**, which is two steps glued together:

```
StandardScaler  ->  LogisticRegression
```

> **Jargon:** *StandardScaler* rescales every column to a comparable range. Without it,
> `avg_item_price` (values around 750) shouts over `cart_items` (values 0–3) purely
> because its numbers are bigger.
>
> *LogisticRegression*, despite the name, is a **classifier**. It draws a straight
> boundary through the data and outputs a probability of being on one side.

**Why a Pipeline instead of two separate steps?** Because a Pipeline is saved as *one*
object. When the API loads it, scaling comes along automatically. It is impossible to
forget — and forgetting to scale at serving time is a classic production bug. (The
research prototype in `research/` has exactly that bug. Deliberately.)

**Why logistic regression and not something fancier?** Because the business does not want
"yes/no" — it wants "how likely". Logistic regression naturally produces well-calibrated
probabilities.

> **Jargon:** a model is *calibrated* if, among all the sessions it scored at 70%, about
> 70% really do convert. An uncalibrated model can rank perfectly and still lie about the
> number — and if you price a discount off that number, you lose money.

We also added a **release gate**: accuracy ≥ 0.70 and F1 ≥ 0.60. If the trained model
falls below either, a `WARNING` is logged. This is the software-engineering habit applied
to ML — do not ship a build that fails its own quality bar.

Finally, a method that looks odd until you see the test that uses it:

```python
def loss_curve(self, X, y, steps=(1, 2, 5, 10, 50, 200)):
    """Training log-loss at increasing optimiser budgets."""
```

It trains the same model six times, each with more iterations allowed, and records how
wrong it is each time. If those numbers do not go **down**, the model is not learning.
More on this in Step 11.

> **Jargon:** *log-loss* measures how wrong the probabilities are, punishing confident
> mistakes hardest. Lower is better. During training the model tries to make it smaller —
> so watching it shrink is watching the model learn.

---

## Step 8 — The first real problem: the model was bad

First training run:

```
accuracy: 0.809    f1: 0.180    roc_auc: 0.745
```

80.9% accuracy! And it was **useless.**

Here is why. Only 19% of sessions converted. A model that ignores every input and always
answers "no purchase" scores **81%** — better than ours. Our F1 of 0.18 gave the game
away: the model had basically stopped predicting conversions at all.

> **Jargon:** this is *class imbalance*. When one answer is rare, accuracy stops being a
> useful measure. *F1* is the honest one — it looks only at how well you find the rare
> class you actually care about.

**Two things came out of this.**

*Fix 1 — the data.* Our generator was producing a problem too rare and too noisy to be
learnable. We raised the base rate and strengthened the signal (that is the coefficient
block in Step 4). New result:

```
accuracy: 0.716    f1: 0.683    roc_auc: 0.781    brier: 0.190
```

Lower accuracy, **far** better model. That sentence is worth re-reading.

*Fix 2 — the metrics.* One number can never tell you if a model is good. We settled on four:

| Metric | The question it answers | Ours |
| --- | --- | --- |
| Accuracy | How often is the yes/no right? | 0.716 |
| F1 | How well do we find the *converters*? | 0.683 |
| ROC-AUC | Can we *rank* a converter above a non-converter? | 0.781 |
| Brier score | Are the probabilities honest? (lower = better) | 0.190 |

Plus a **calibration table**, which turned out to be the most convincing evidence of all:

| Predicted band | Sessions | We said | Reality |
| --- | --- | --- | --- |
| 0.0 – 0.2 | 197 | 13% | 16% |
| 0.2 – 0.4 | 263 | 30% | 27% |
| 0.4 – 0.6 | 222 | 50% | 55% |
| 0.6 – 0.8 | 200 | 70% | 72% |
| 0.8 – 1.0 | 118 | 88% | 81% |

Read the last two columns. When the model says 70%, roughly 72% of those sessions really
convert. That is a model you can build a business rule on.

And we added a test for the trap we just fell into:
`test_model_beats_a_majority_class_baseline` — the model must beat "always guess the
common answer". If we ever regress into that hole again, the test suite catches it.

**Lesson:** a metric that goes up is not the same as a system that got better. And when a
number surprises you, that is the interesting moment — do not move past it.

---

## Step 9 — Inference

`ecom/predict.py` — `ConversionPredictor`. Load the saved model once, then score sessions.

Two details worth explaining.

**We save the feature *order* inside the model file.** The artifact is a dictionary:

```python
{"pipeline": <the model>, "features": [...12 column names...], "version": "1.0.0"}
```

Why? Because a model does not know column names — it knows position 0, position 1, and so
on. If serving ever reorders the columns, `cart_items` lands where `avg_item_price` should
be and every prediction becomes nonsense. Silently. Storing the order and re-applying it
at inference makes the bug impossible.

**We translate the probability into something a human can act on:**

| Probability | Band | What the business does |
| --- | --- | --- |
| ≥ 0.60 | `high` | Offer live chat |
| 0.25 – 0.60 | `medium` | Show a small nudge |
| < 0.25 | `low` | Leave them alone |

A number is not a decision. Somebody has to draw the line, and it belongs in the code,
named and visible, not in a marketer's spreadsheet.

---

## Step 10 — The REST API

`ecom/api.py` + `ecom/schemas.py`. Five endpoints:

| Endpoint | Purpose |
| --- | --- |
| `GET /health` | Is the service alive? |
| `GET /model-info` | Which model version is serving? |
| `GET /metrics` | How good was it at training time? |
| `POST /predict` | Score one session |
| `POST /predict/batch` | Score up to 100 sessions |

> **Jargon:** a *REST API* lets other programs talk to yours over HTTP. *FastAPI* is the
> Python library we used. `GET` = "give me something". `POST` = "here is some data, do
> something with it".

**Status codes were the most interesting design decision.**

> **Jargon:** the three-digit number in an HTTP response. `200` = fine.
> `422` = your input was invalid. `404` = no such thing. `500` = we are broken.
> `503` = we are temporarily unavailable, try again.

Three choices, each with a reason:

**1. Missing model returns `503`, not `500`.** `500` means "we have a bug". `503` means
"try again later". A missing model file is an operational problem, not a code defect —
and the on-call engineer's response is completely different for each. The status code is
a message to a human at 3am.

**2. `/health` always returns `200`,** even with no model — it reports
`{"status": "degraded", "model_loaded": false}`. If the health check returned an error,
Kubernetes would kill and restart the container in a loop, and nobody would ever get to
read the actual problem. Liveness ("is the process alive?") and readiness ("can it serve
traffic?") are different questions.

**3. Bad input returns `422` before the model is called.** This is Task 9's security
answer, and it is enforced by `ecom/schemas.py`:

```python
pages_viewed: int = Field(..., ge=0, le=500)          # 0-500 only
device: Literal["mobile", "desktop", "tablet"]         # nothing else allowed
model_config = {"extra": "forbid"}                     # unknown fields rejected
sessions: list[...] = Field(..., max_length=100)       # bounded payload
```

Why it matters: without these, someone can send `pages_viewed = 10_000_000` and probe the
model's decision boundary until they learn how to game it. Or send a 10-million-row batch
and take the service down. Every one of these rules is enforced by pydantic *before* our
code runs, and each one has a test proving it returns `422`.

> **Jargon:** *pydantic* checks that incoming JSON matches the shape you declared, and
> rejects it if not. It also generates the interactive API documentation at `/docs` from
> the same declaration — so the docs can never go stale, because they *are* the code.

---

## Step 11 — Write the tests (and watch two of them fail)

61 tests across six files. Five categories:

| File | Type | Tests | Guards |
| --- | --- | --- | --- |
| `test_data_validation.py` | Data validation | 10 | The input contract |
| `test_data_ingestion.py` | Unit | 6 | Reading data, and failing clearly when it cannot |
| `test_features.py` | Unit | 8 | Individual functions |
| `test_training.py` | ML — training | 6 | That the model learns |
| `test_inference.py` | ML — inference | 15 | That predictions behave sensibly |
| `test_api.py` | Integration | 16 | The whole stack over HTTP |

### The ML tests are the interesting ones

Normal tests ask "did this function return 4?". You cannot do that with a model — there is
no single right answer. So ML tests ask different questions:

**Does the loss actually go down?** Train with 1 iteration, then 2, then 5, 10, 50, 200:

```
   1  0.58530
   2  0.56512
   5  0.55588
  10  0.55427
  50  0.55421
 200  0.55421   <- flat: it has converged
```

Down and then flat. That is a model that learned and then finished. If this line were flat
from the start, something would be wired wrong — and no accuracy number would have told us.

**Can it memorise a tiny batch?** Give it 20 rows, turn regularisation off, and demand
100% accuracy on those same 20 rows. This is a *sanity* test, not a quality test. A model
that cannot even memorise 20 examples has a broken pipeline — a shuffled label, a
disconnected feature. It is the fastest possible smoke test for "is this thing plugged in".

**Directional tests.** These encode business knowledge that must always hold:

```
cart_items      0 -> 3 : 0.1515 -> 0.9067    must go UP
returning user  0 -> 1 : 0.3781 -> 0.5540    must go UP
discount        0 -> 1 : 0.3781 -> 0.5286    must go UP
```

You do not need to know the right answer to know the right *direction*. Adding items to a
cart cannot possibly make someone less likely to buy. If a future retrain breaks that,
the model has learned something backwards and the test suite says so.

**Invariance tests.** The mirror image — things that must **not** change the answer:

```
session_id  "x" vs "y" : 0.3781 == 0.3781
device "mobile"/"MOBILE": 0.3781 == 0.3781
row order in a batch    : identical
```

If changing a session's ID changed its score, we would have a leaked identifier in the
features. This test would catch that.

### Two tests failed. Both taught us something.

**Failure 1 — `TypeError` in the validator.**

The test set `pages_viewed` to the string `"not-a-number"` and expected a clean
`DataValidationError`. Instead Python threw a raw `TypeError`.

The cause: the schema check correctly recorded "this should be numeric", but then the
*range* check ran anyway and tried `"not-a-number" < 0`. You cannot compare text to zero.

The fix: skip the range check on columns the schema check already rejected.

```python
if not pd.api.types.is_numeric_dtype(df[column]):
    continue   # the schema check already flagged this one
```

**The real lesson:** when several validations run in sequence, a *later* check can crash
on data an *earlier* check already condemned. The error you finally see is not the real
error. Validation order matters.

**Failure 2 — the model could not overfit 30 rows.**

```
assert 0.8333333333333334 > 0.95
```

Our first instinct was that the pipeline was broken. It was not. This is a genuine piece
of maths: a straight-line model with 12 features can perfectly separate roughly `2 × 12 =
24` points. Ask it to separate 30 and it simply cannot — not a bug, a capacity limit.

We also found the first 12 rows of the data were all the same class, which crashes
sklearn entirely ("needs samples of at least 2 classes").

The fix was to make the batch both smaller **and** balanced — 10 converting sessions and
10 non-converting:

```python
index = list(y[y == 0].index[:10]) + list(y[y == 1].index[:10])
```

Result: 1.000. Test passes, and it is now testing what we meant it to test.

**The real lesson:** when an ML test fails, ask "is my code wrong, or is my *expectation*
wrong?" first. Half the time the test is the thing that needs fixing — and blindly
loosening the assertion until it passes teaches you nothing.

---

## Step 12 — The research-code exhibit

Requirement 2 asks us to show the difference between research code and production code.

Most people write the clean version and describe the messy one. We did the opposite —
we kept a **real, runnable, deliberately awful prototype** in `research/`:

- `research/research_prototype.ipynb` — the notebook, with outputs
- `research/prototype.py` — the same thing as a script, so linters can chew on it

It has hardcoded paths, no random seed, `from sklearn.metrics import *`, unused imports,
commented-out dead experiments, and a hand-typed 12-element feature list.

**Do not fix it.** It is the "before" photograph.

The single sharpest demonstration is in the submission notebook — run both styles three
times each:

```
research   (3 runs): [0.715, 0.727, 0.716]   <- a different answer every time
production (3 runs): [0.716, 0.716, 0.716]   <- identical, always
```

That is not a style preference. In research, "roughly 0.72" is a fine answer. In
production, a number that changes when nothing changed means you can never tell whether
your latest change helped, hurt, or did nothing at all.

Here is the full comparison we ended up with:

| | Research | Production |
| --- | --- | --- |
| Goal | Answer "does this work?" once | Run unattended for years |
| Paths | Hardcoded | `config.py` |
| Reproducibility | None | Fixed seed |
| Feature logic | In a cell | Shared module |
| Feature order | Hand-copied | Saved in the artifact |
| Scaling | Forgotten in one cell | Inside the Pipeline |
| Bad input | Cryptic sklearn error | Typed error naming the column |
| Output | `print()` | Levelled logging, to file |
| Correctness | "Looked right" | 61 tests |

---

## Step 13 — Formatting and linting: the before/after

Three tools:

| Tool | Job |
| --- | --- |
| **black** | Reformats code to one fixed style. It has almost no options — that is the feature. |
| **isort** | Sorts imports into standard-library / third-party / local blocks |
| **flake8** | Finds unused imports, undefined names, style violations |

> **Jargon:** a *linter* reads your code without running it and reports problems.
> A *formatter* rewrites the layout without changing behaviour.
>
> **Why bother?** Not neatness. It ends arguments. Nobody reviews a pull request
> complaining about spaces if a tool already decided. And flake8 catches genuine bugs —
> an unused import usually means you deleted the code that used it and forgot something.

We captured the reports honestly, in this order:

1. **Before** (`reports/lint_before.txt`) — ran all three tools on `research/`, `ecom/`
   and `tests/`, *before* formatting anything. Result: **52 flake8 violations**, 2 files
   needing reformatting, 2 files with unsorted imports.

   Note that one of those violations was in our own production code — a line 91
   characters long in `predict.py`. We had been writing carefully, and the tool still
   found something. That is the point of the tool.

2. **Then** ran `isort` and `black` on `ecom/` and `tests/`.

3. **After** (`reports/lint_after.txt`) — reran everything on the production code:
   **0 violations, 0 files to reformat, 0 unsorted imports.**

`research/` is excluded from linting in `setup.cfg` on purpose, with a comment saying so.
It is the exhibit; cleaning it would destroy the evidence.

The submission notebook re-runs all three tools live, so the "after" state is verifiable
rather than a screenshot you have to take on trust.

---

## Step 14 — The monitor

`ecom/monitor.py` is what you would run on a schedule — every night, say. It compares
today's live traffic against the training data and writes `reports/data_quality.json`.

We already had the drifted "live" file from Step 4. Running it:

```
pages_viewed           1.6902  DRIFT
session_duration_min   0.8272  DRIFT
cart_items             0.0012  ok
avg_item_price         0.0014  ok

columns needing attention: ['pages_viewed', 'session_duration_min']
```

Read that as a story. Sessions have got much shorter and people browse fewer pages, but
cart behaviour and prices are unchanged. That is exactly the mobile-heavy traffic shift we
built into the generator — the monitor found it without being told.

The model has not broken yet. It will, slowly, as live traffic drifts further from what it
learned. **That is the whole point of monitoring:** you get told to retrain *before* the
business notices, not after.

Note the monitor runs the validator with `strict=False` — it reports and keeps going. A
monitoring job that crashes on the first problem is a monitoring job that gets switched
off after a week.

---

## Step 15 — The submission notebook

`049.ipynb` (named for the group, per the PDF) walks through all 9 requirements in order,
with every cell executed and its output saved.

Deliberate choices:

- **It calls the real package.** Nothing is re-implemented for the notebook. Every cell
  imports from `ecom/`, so the notebook cannot drift away from the code it documents.
- **It runs the real test suite** via `subprocess`, so the "61 passed" you see is a live
  result, not a claim.
- **It re-runs the linters live**, so the "after" state is checkable.
- **It shows failures too** — five error scenarios are triggered on purpose in Task 3 so
  you can see the error handling and log levels working, not just read about them.

---

## The vocabulary list

Everything defined above, in one place:

| Word | Plain meaning |
| --- | --- |
| **Session** | One visit to the website, arrival to exit |
| **Conversion** | The session ended in a purchase |
| **Feature** | One input column to the model |
| **Feature engineering** | Inventing better columns from the ones you have |
| **Schema** | The agreed shape of your data — which columns, what type |
| **Pure function** | Only uses its arguments, only returns a value, remembers nothing |
| **Package** | A folder of Python files with `__init__.py`, importable as one unit |
| **Pipeline** | Preprocessing + model saved as one object, so serving cannot skip a step |
| **Training–serving skew** | Cleaning data one way in training and another at serving |
| **One-hot encoding** | Turning `"mobile"` into `mobile=1, desktop=0, tablet=0` |
| **Class imbalance** | One answer is rare, so accuracy stops being meaningful |
| **Calibration** | When the model says 70%, about 70% really happen |
| **Log-loss** | How wrong the probabilities are; lower is better |
| **Drift** | Live data no longer looks like training data |
| **PSI** | One number measuring drift; above 0.20 is significant |
| **Overfitting** | Memorising the training data instead of learning the pattern |
| **Regularisation** | Deliberately limiting the model so it generalises instead of memorising |
| **Linter / formatter** | Reads code and reports problems / rewrites layout |
| **REST API** | How other programs talk to yours over HTTP |
| **Status code** | The 3-digit number in an HTTP reply (200 ok, 422 bad input, 503 unavailable) |
| **Unit test** | Tests one function alone |
| **Integration test** | Tests several parts working together |
| **Directional test** | "This input goes up, so the prediction must go up" |
| **Invariance test** | "This input changed, and the prediction must NOT change" |
| **Shadow deployment** | Run the new model alongside the old, log its answers, use none of them |
| **Canary release** | Send a small slice of traffic to the new model first |
| **A/B test** | Split users, compare the *business* result, not the model metric |

---

## If you want to run it yourself

```bash
cd assignments/assignment-2
pip install -r requirements.txt

python -m ecom.data_ingestion   # 1. build the demo dataset (data/)
python -m ecom.train            # 2. train + evaluate + save (artifacts/)
python -m ecom.monitor          # 3. data quality + drift (reports/)
python -m pytest                # 4. run all 61 tests
uvicorn ecom.api:app --reload   # 5. serve the model
```

Then open <http://127.0.0.1:8000/docs> and click **Try it out** on `POST /predict`.

Read in this order:

1. `research/research_prototype.ipynb` — where it started
2. `049.ipynb` — the full walkthrough
3. `ecom/config.py` → `features.py` → `train.py` → `api.py` — the code itself

---

## The five things worth remembering

1. **A metric going up is not a system getting better.** Our 80.9%-accuracy model was
   worse than the 71.6% one.
2. **Write the boring parts first.** Config and logging retro-fitted into finished code
   is a bad afternoon.
3. **One copy of the feature logic.** Every duplicate is a future silent bug.
4. **When an ML test fails, suspect your expectation first.** Both of ours were wrong
   expectations, not wrong code.
5. **Keep the messy version.** You cannot show what "production code" means without
   something to hold it up against.
