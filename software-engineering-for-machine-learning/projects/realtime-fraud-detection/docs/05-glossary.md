# 5. Glossary

Machine learning vocabulary, translated for someone who already knows software
engineering. Terms are grouped by where they show up in this project.

---

## The basics

**Feature** — an input column to the model. Not the raw data, but a number
derived from it. `amount` is a feature; so is `transactions_by_this_account_in_last_hour`.
Think of it as a computed property on a request object.

**Label** — the correct answer for a historical example. Here: was this
transaction actually fraud, yes or no. The whole discipline depends on having
these, and this project's central difficulty is that they arrive weeks late.

**Training** — the batch process that reads historical features and labels and
produces a model. Slow, offline, run occasionally.

**Inference** (or **scoring**, or **prediction**) — running a trained model on
one new input to get an answer. Fast, online, run constantly. Roughly: training
is the build, inference is the runtime.

**Model** — in practice, a binary artifact. You feed it a fixed-length array of
numbers in a fixed order and it returns a number. Everything else is plumbing
around that.

**Model artifact** — the serialised trained model as a file. Should be treated
like a compiled binary: versioned, immutable, promoted through stages.

---

## Evaluating a model

**Class imbalance** — when one answer is far rarer than the other. Fraud is
about 1 in 1,000. This breaks most naive metrics.

**Accuracy** — the fraction of predictions that were right. **Useless here.**
Predicting "not fraud" for everything gives 99.9% accuracy and catches nothing.
If a portfolio project reports accuracy on a fraud dataset, the author has not
understood the problem.

**Precision** — of the transactions we flagged as fraud, what fraction really
were? Low precision means annoying a lot of real customers.

**Recall** — of the transactions that really were fraud, what fraction did we
catch? Low recall means losing money.

These two trade off against each other. Push the threshold down and recall rises
while precision falls. There is no setting that maximises both, which is why the
threshold has to be chosen with a cost model.

**Precision-recall curve** — precision plotted against recall across every
possible threshold. **AUC-PR** is the area under it, a single summary number
that, unlike accuracy or ROC-AUC, does not flatter a model on rare-event data.
This is the headline metric for this project.

**ROC-AUC** — a similar summary that is popular but misleading on heavily
imbalanced data, because it is dominated by the enormous number of easy negative
cases. Reported for completeness, not relied on.

**Confusion matrix** — the two-by-two table of predicted versus actual. The four
cells are true positives, false positives (false alarms), true negatives, and
false negatives (missed fraud). Everything above is derived from this table.

**Threshold** — the cutoff that turns a probability into a decision. The model
says 0.83; is that a block? Only if the threshold is below 0.83. Choosing this
number is a business decision, not a modelling one.

---

## The hard problems

**Train/serve skew** — when the features computed during training differ from
the features computed during serving, even slightly. Different window boundary,
different null handling, different rounding. Nothing crashes; the model just
quietly gets worse. This is the most common serious bug in production machine
learning, and this project measures it explicitly rather than assuming it away.

**Leakage** — when a training feature contains information that would not have
been available at prediction time. The classic version: computing an account's
average transaction amount over the entire dataset, which includes transactions
from after the one being predicted. The model looks superb in testing and fails
on day one. The software analogy is a test that passes because it asserts against
the same value it computed.

**Point-in-time correctness** — building each training row using only
information that existed strictly before that row's timestamp. The defence
against leakage. In SQL terms, a window frame that is explicitly bounded to the
past.

**Time-based split** — splitting training and test data by date rather than
randomly. A random split puts April transactions in the training set and March
transactions in the test set, letting the model learn from the future. Any
time-series problem must split chronologically.

**Delayed labels** — the truth arriving long after the prediction. Here, 30 to
60 days, when the cardholder disputes the charge. This means recent data looks
artificially fraud-free, and a retraining job that does not account for it will
learn that fraud is disappearing.

**Data drift** — the incoming data starts to look different from the training
data. A new market launched, a new payment type went live, festival season
doubled transaction sizes.

**Concept drift** — the data looks the same but its meaning changed. Fraudsters
worked out that transactions under a certain amount are not scrutinised, so they
all moved below it. Harder to detect than data drift, and more dangerous.

**Population Stability Index (PSI)** — a number summarising how far a feature's
distribution has moved from a reference distribution. The conventional reading:
under 0.1 is stable, 0.1 to 0.25 is worth watching, above 0.25 needs
investigation.

---

## Systems and operations

**Feature store** — the system that computes features once and serves them to
both training and serving, so both get identical numbers. Has two halves: an
**online store** (fast, key-value, holds only current values — Redis here) and
an **offline store** (large, historical, used to build training data — Parquet
here). The existence of exactly one definition of each feature is the entire
point.

**Model registry** — a catalogue of trained models with versions and stages.
Version 7 is Production, version 8 is Staging, earlier versions are Archived.
The serving code asks the registry what is in Production instead of hardcoding a
path. Roughly a package registry, for models.

**Champion / challenger** — the model currently in production is the champion;
a newly trained candidate is the challenger. The challenger only gets promoted
if it beats the champion on a defined evaluation.

**Promotion gate** — the automated checks a challenger must pass to become the
champion. In this project: beat the champion on expected cost, do not regress on
any major segment, produce a sane score distribution. Written as a script, so no
human can wave a bad model through.

**Shadow mode** — running a new model on live traffic in parallel with the
current one, recording its decisions but not acting on them. Catches problems
that only appear on real data, with zero customer impact. The machine learning
equivalent of dark launching.

**Canary deployment** — sending a small percentage of real traffic to the new
model and acting on its decisions, then increasing the share if nothing breaks.
Riskier than shadow mode but the only way to observe real feedback effects.

**Rollback** — putting the previous model version back. Trivial to describe,
routinely untested, and therefore routinely broken when needed. This project has
a test for it.

**Backfill** — going back and filling in data that was not available at the
time. Here: attaching fraud labels to transactions once the disputes arrive.

**p50 / p95 / p99** — latency percentiles. p99 of 50 ms means 99 out of 100
requests finished faster than 50 ms. Averages hide the failures that customers
actually notice; percentiles do not.

**MLOps** — applying software engineering discipline to machine learning
systems: version control, testing, CI/CD, monitoring, reproducibility, and
automated deployment. In practice, most of the work of running machine learning
in production is this rather than modelling — which is why a software
engineering background is an advantage rather than a gap.

---

## Things this project deliberately does not involve

**Neural network / deep learning** — layered models that excel on images, audio
and text. On tables of numbers they are usually beaten by gradient boosted trees,
which is why they are not used here.

**LLM / RAG / embeddings** — language model machinery. There is no natural
language in a payment record. Adding it would be decoration.

**GPU** — not needed. Gradient boosted trees train on a laptop CPU in seconds.

---

Next: [6. Decisions](06-decisions.md)
