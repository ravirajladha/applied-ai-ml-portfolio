# 2. How It Works

A walk through the system, one component at a time. Written for someone who
knows software but is new to machine learning systems.

## The two halves

Every production machine learning system is really two systems that must agree
with each other:

- **The offline half** — slow, batch, runs on history. It builds training data,
  trains models, and evaluates them. Nobody is waiting.
- **The online half** — fast, streaming, runs on right now. It computes features
  and returns decisions. A customer is waiting.

Almost every hard problem in this project comes from keeping those two halves
telling the same story. Hold that idea while reading the rest of this page.

---

## Component 1: The transaction stream

**What it is:** a Kafka topic (served by Redpanda) that transactions flow
through, one message at a time.

**Why a stream and not a database table:** because the real thing is a stream.
Transactions do not arrive in a tidy batch at midnight; they arrive constantly,
out of order, in bursts. Building against a stream from day one means the system
is never quietly assuming it has all the data.

**How it is faked here:** a replay script reads a historical fraud dataset and
publishes each transaction onto the topic at wall-clock speed — a transaction
recorded three seconds after the previous one is published three seconds later.
The replay speed is configurable, so a day of traffic can be compressed into ten
minutes for testing, or run at 1× for realistic load.

**What this component proves:** that the rest of the system can handle a moving
target rather than a static file.

---

## Component 2: The feature builder

**What "features" means:** the numbers the model actually looks at. A raw
transaction has an amount, a timestamp, an account ID, a merchant. A model
cannot do much with an account ID. What it needs is derived numbers like:

| Feature | Why it matters |
| --- | --- |
| Transactions by this account in the last 1 / 5 / 60 minutes | Card testing shows up as a burst |
| Total amount by this account in the last hour / day | Cash-out attempts spike the total |
| This amount ÷ this account's average amount | Catches the unusually large purchase |
| Distinct merchants touched in the last hour | Stolen cards get spread around fast |
| Seconds since this account's previous transaction | Sub-second gaps mean automation |
| Is this a merchant this account has used before | New merchant + big amount is a classic pattern |

**What it is:** a consumer that reads every transaction off the stream and
updates a running summary for the account involved.

**Where the summaries live:** Redis. It is an in-memory key-value store, so a
read takes well under a millisecond. That matters because the scoring API needs
several of these lookups inside its 50 ms budget.

**How the rolling windows work:** for each account, a sorted set keyed by
timestamp holds recent transactions. On each new event, entries older than the
window are dropped and the aggregates recomputed. Old keys expire automatically
so memory does not grow forever.

**The trap here:** these same features must also be computable over history for
training. That is Component 3, and the two implementations must produce
identical numbers. See [Component 6](#component-6-the-training-job).

---

## Component 3: The offline store

**What it is:** the same transactions, plus the features that were computed for
them and the decision that was made, written to Parquet files on disk.

**Why Parquet:** it is a columnar file format. Reading "just the amount column
for March" does not require reading everything else. It compresses well, every
tool understands it, and it needs no database server.

**Why also log the features:** this is the single most valuable habit in
production machine learning. If in six months a transaction is disputed and
someone asks "why did the system approve this?", the answer requires knowing
*exactly what numbers the model saw at that moment*. Recomputing them later gives
a different answer, because the account's history has moved on.

Logging the features at scoring time is also how train/serve skew gets measured:
compare the logged live features against the same features recomputed offline. If
they differ, there is a bug.

**How it is queried:** DuckDB. It runs SQL directly over Parquet files with no
server to install — effectively SQLite for analytics.

---

## Component 4: The scoring API

**What it is:** a FastAPI service with one important endpoint.

```
POST /score
{ "transaction_id": "...", "account_id": "...", "amount": 8400.0,
  "merchant_id": "...", "timestamp": "..." }

→ { "fraud_probability": 0.83, "decision": "block",
    "model_version": "7", "features_used": {...}, "latency_ms": 11.4 }
```

**What happens inside, in order:**

1. Validate the request body. A malformed transaction must fail loudly, not get
   silently scored with default values.
2. Read the account's running features from Redis.
3. Assemble the feature vector in **exactly** the column order the model expects.
4. Run the model.
5. Compare the probability against the cost-derived threshold to produce a
   decision.
6. Log the request, the features, the score and the decision.
7. Return.

**Why ONNX Runtime and not just calling LightGBM:** ONNX is a portable format
for trained models. Exporting to ONNX means the serving process does not need
the training library, the Python objects, or the exact library version the model
was trained with. It also runs measurably faster. In practice it turns "the
model" from a fragile Python pickle into a versioned binary artifact.

**The latency budget, roughly:**

| Step | Target |
| --- | --- |
| Request parsing and validation | ~1 ms |
| Redis feature lookup | ~2 ms |
| Feature assembly | ~1 ms |
| Model inference | ~3 ms |
| Logging (asynchronous, off the hot path) | ~0 ms |
| Headroom | the rest |

Logging must not block the response. It goes onto a queue and is written by a
background worker.

---

## Component 5: The decision threshold

The model returns a probability between 0 and 1. Something has to turn that into
approve or block.

The naive answer is 0.5. The correct answer comes from the cost model in
[the problem document](01-problem.md#the-cost-of-being-wrong):

1. Score a held-out set of historical transactions.
2. For every candidate threshold from 0.001 to 0.999, count the resulting false
   negatives and false positives.
3. Multiply each by its cost and add them up.
4. Pick the threshold with the lowest total.
5. Plot the whole curve, because the shape of it is the interesting part — it
   shows how sensitive the business outcome is to getting this number right.

This threshold is stored alongside the model and versioned with it. Changing the
threshold *is* a deployment.

---

## Component 6: The training job

**What it does:** builds a training dataset from history, trains a model,
evaluates it, and registers it.

**The hard part — point-in-time correctness.** For every historical transaction,
the training row must contain the features **as they would have been at that
exact moment**, using only transactions that happened strictly before it.

The obvious wrong way is to compute "average transaction amount for this
account" over the whole dataset. That average includes the future. The model
learns from information it will never have in production, scores brilliantly in
testing, and collapses on day one of deployment. This is **leakage**.

The right way is a windowed aggregation ordered by timestamp, computed with
DuckDB SQL, that by construction can only see backwards. There is a test that
plants a deliberately leaky feature and asserts the pipeline rejects it.

**The model:** LightGBM, a gradient boosted decision tree. It is the correct
choice for tabular data — it beats neural networks on this kind of problem, it
trains in seconds, and it produces feature importances that make the model
explainable. Explainability is not a nice-to-have in finance; a blocked customer
can legally demand a reason.

**Handling the imbalance:** with fraud at ~0.1%, the model is trained with class
weights so it does not simply learn to always say "not fraud". Evaluation uses
area under the precision-recall curve, which unlike accuracy or ROC-AUC does not
flatter a model on imbalanced data.

**Everything is tracked in MLflow:** the parameters, the metrics, the exact code
commit, the dataset version, and the model artifact itself. Six months later it
must be possible to point at a model in production and reproduce it exactly.

---

## Component 7: The model registry and promotion gate

**What a registry is:** a catalogue of trained models with versions and stages.
Version 7 is in Production, version 8 is in Staging, versions 1–6 are archived.
The serving API asks the registry "what is in Production?" rather than having a
file path hardcoded.

**The promotion gate** is the rule that decides whether a newly trained model is
allowed to replace the live one. It is a script, not a human clicking a button:

- Evaluate the challenger and the current champion on the *same* held-out window.
- The challenger must beat the champion on expected cost by a meaningful margin.
- It must not regress badly on any major segment (high-value transactions, new
  accounts, each transaction type).
- Its score distribution must not be wildly different in shape, which usually
  indicates a data problem rather than a genuinely better model.

If any check fails, the promotion is refused and the reason is logged. This is
how you stop a broken retrain from silently reaching production at 3am.

**Shadow mode:** before promotion, the challenger scores real live traffic in
parallel with the champion, but its decisions are recorded and thrown away. This
catches problems that only appear on live data — a feature that is always null in
production, an unexpected latency cliff — without any customer being affected.

**Rollback:** one command, which re-points the Production stage at the previous
version. There is a test that exercises it. A rollback path that has never been
run is not a rollback path.

---

## Component 8: Monitoring

Four things are watched, because they fail in four different ways.

### Traffic and latency
Requests per second, error rate, and response time percentiles. Standard service
monitoring, exported to Prometheus and drawn in Grafana. This catches
infrastructure problems.

### Score distribution
A histogram of the fraud probabilities coming out of the model. If the model
suddenly starts outputting far more high scores than yesterday, something
changed — either the world or the pipeline. This is the earliest available
warning signal, because it needs no labels at all.

### Feature drift
For each feature, compare today's distribution to the distribution the model was
trained on, using Population Stability Index. Evidently generates the reports.
This is what catches "an upstream system started sending amounts in paise instead
of rupees" before it costs anything.

### Delayed performance
As real labels arrive weeks later, backfill them and compute what the model's
precision, recall and expected cost actually were. This is the only ground truth,
and it always arrives too late to be an alert — which is exactly why the three
signals above exist.

---

## Putting it together: the life of one transaction

1. `t+0ms` — Transaction published to the Kafka topic.
2. `t+2ms` — Feature builder consumes it, updates the account's rolling counters
   in Redis.
3. `t+5ms` — Scoring request hits the API.
4. `t+7ms` — Features read back from Redis.
5. `t+11ms` — Model returns 0.83. Threshold is 0.19. Decision: **block**.
6. `t+11ms` — Response returned. Customer's payment is declined.
7. `t+12ms` — Features, score and decision written asynchronously to Parquet.
8. `t+1min` — The transaction appears in the Grafana score-distribution panel.
9. `t+40days` — No chargeback was filed, because the block worked. A label of
   "confirmed fraud, prevented" is joined back onto the record.
10. `t+47days` — The weekly retrain includes this transaction in its training
    data. The model gets slightly better at recognising this pattern.

---

Next: [3. The Tools](03-tools.md)
