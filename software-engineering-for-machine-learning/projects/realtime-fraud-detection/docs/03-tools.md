# 3. The Tools

Every tool in this project, what it actually is, why it is here, and what was
considered instead. Nothing is included because it is fashionable — if a
component could be replaced by a Python dictionary, it was.

---

## Streaming

### Redpanda
**What it is:** a message broker. Producers write messages onto named topics,
consumers read them. It speaks the Kafka protocol, so every Kafka client library
and tool works against it unchanged.

**Why it is here:** transactions genuinely arrive as a stream, and building
against a stream forces the system to be honest about ordering, replay and
back-pressure.

**Why Redpanda over Kafka:** Kafka historically needed ZooKeeper and a JVM,
which is heavy for a laptop. Redpanda is a single binary with no ZooKeeper, uses
a fraction of the memory, and is drop-in compatible. On a résumé it reads as
"Kafka", because the API is Kafka.

**Considered instead:** Kafka (heavier locally, identical to learn), Redis
Streams (would collapse two components into one and hide the distinction between
a log and a cache), RabbitMQ (a queue, not a replayable log — replay is the whole
point of the transaction stream here).

---

## Storage

### Redis
**What it is:** an in-memory key-value store. Reads and writes take microseconds
because nothing touches disk on the hot path.

**Why it is here:** it is the **online feature store**. The scoring API must
fetch an account's recent behaviour inside a few milliseconds, and no disk-based
database will reliably do that under load.

**What is stored in it:** per account, a sorted set of recent transaction
timestamps and amounts, plus precomputed aggregates. Keys carry a time-to-live so
dormant accounts fall out of memory automatically.

**Considered instead:** Feast (a real, purpose-built feature store — genuinely
the right answer at company scale, but it adds a large amount of configuration
that would obscure what a feature store actually *does*; using Redis directly and
documenting the gap is more instructive), Postgres (too slow at the tail),
in-process memory (would not survive a restart and could not be shared across
API replicas).

### Parquet
**What it is:** a columnar file format for tabular data. It stores values
column-by-column rather than row-by-row, so reading three columns out of fifty
reads roughly three fiftieths of the bytes. It compresses extremely well.

**Why it is here:** it is the **offline store** — the permanent record of every
transaction, the features that were computed for it, and the decision made.

**Considered instead:** CSV (no types, no compression, no column pruning; fine
for ten thousand rows, painful at ten million), Postgres (a server to run and
back up for data that is append-only and never updated), Delta Lake / Iceberg
(the right answer once you need transactions and schema evolution over a data
lake — noted as a future upgrade in the decisions log).

### DuckDB
**What it is:** an analytical database that runs inside the Python process, with
no server. It reads Parquet files directly and runs standard SQL over them —
effectively SQLite, but built for analytics instead of transactions.

**Why it is here:** building point-in-time-correct training data is a windowed
SQL problem. Expressing it as SQL with explicit window frames makes the
correctness auditable in a way that a hundred lines of pandas never is.

**Considered instead:** pandas (workable, but window logic becomes hard to read
and hard to prove correct, and it needs everything in memory), Spark (correct
choice at a hundred times this data volume, enormous overhead below that).

---

## The model

### LightGBM
**What it is:** a gradient boosted decision tree library. It builds hundreds of
small decision trees in sequence, each one correcting the mistakes of the ones
before it.

**Why it is here:** on tabular data — rows and columns of numbers and
categories — gradient boosted trees consistently beat neural networks. They train
in seconds rather than hours, need no GPU, handle missing values natively, and
report which features mattered.

**Why explainability matters here specifically:** a customer whose payment was
blocked may be legally entitled to a reason. "The model is a neural network" is
not a reason. Feature importances and SHAP values on a tree model are.

**Considered instead:** XGBoost (equivalent; LightGBM trains faster on wide
data), scikit-learn's random forest (simpler but noticeably weaker), a neural
network (slower, worse on this data type, harder to explain — the wrong tool
chosen for the wrong reason).

### ONNX Runtime
**What it is:** ONNX is an open format for trained models. ONNX Runtime is the
engine that executes them.

**Why it is here:** exporting the trained model to ONNX means the serving
container does not need LightGBM, scikit-learn, or a matching Python version. The
model becomes a self-contained versioned binary. It also runs faster than calling
the training library.

**The real reason:** it removes an entire category of production failure — the
serving environment quietly having a different library version than the training
environment, producing subtly different predictions.

**Considered instead:** pickling the LightGBM model (fragile across versions,
and unpickling arbitrary files in a serving process is a security problem),
Treelite (faster still, narrower ecosystem).

---

## Serving

### FastAPI + Uvicorn
**What they are:** FastAPI is a Python web framework; Uvicorn is the server that
runs it.

**Why they are here:** FastAPI validates request bodies automatically from type
hints, which matters enormously when the input is a financial transaction and a
missing field must fail loudly rather than default to zero. It is asynchronous,
so logging can be pushed off the response path. It generates OpenAPI docs for
free.

**Considered instead:** Flask (already used in the coursework projects; no
built-in validation, synchronous by default), BentoML or Seldon (purpose-built
model servers — they would do a lot of this automatically, which is precisely why
they are not used here: the point is to understand what they are doing).

---

## The machine learning lifecycle

### MLflow
**What it is:** two things in one. An **experiment tracker** that records every
training run — parameters, metrics, code version, output files — and a **model
registry** that catalogues trained models with versions and stages (Staging,
Production, Archived).

**Why it is here:** without it, "which model is live and how was it made?" is
answered by reading filenames and hoping. The registry is also what makes
rollback a one-line operation: re-point the Production stage at the previous
version.

**Considered instead:** Weights & Biases (excellent, but hosted and
subscription-based), DVC alone (versions data and models well, no registry
concept), a spreadsheet (this is what most people actually do, and it is exactly
the failure this project is meant to demonstrate solving).

### Prefect
**What it is:** a workflow orchestrator. It runs multi-step pipelines on a
schedule, retries failures, and shows you what ran, when, and whether it worked.

**Why it is here:** retraining is not one script. It is: wait for labels to
settle → rebuild training data → validate it → train → evaluate against the
champion → promote or refuse. Each step can fail and each needs to be visible.

**Why Prefect over Airflow:** Airflow is the industry default and worth knowing,
but it wants a scheduler, a webserver and a metadata database before it does
anything. Prefect runs from a Python file. Below a certain scale Airflow is
mostly ceremony.

**Considered instead:** Airflow (the enterprise default; a reasonable swap later
and noted as such), Dagster (excellent data-asset model, more concepts to learn
first), cron (no retries, no visibility, no dependency handling).

---

## Data quality and monitoring

### pandera
**What it is:** schema validation for dataframes. You declare what each column
should be — type, range, nullability, uniqueness — and it checks real data
against that declaration.

**Why it is here:** the most common production failure in machine learning is
not a bad model, it is bad data arriving quietly. An amount column that starts
containing negative numbers, an ID column that starts being null 30% of the time.
The schema turns that into a loud failure at the boundary.

**Considered instead:** Great Expectations (more powerful, more machinery;
pandera is enough at this scale and reads like normal Python).

### Evidently
**What it is:** a library that compares two datasets and reports how their
distributions differ, feature by feature, with HTML reports.

**Why it is here:** this is the drift detection. It answers "does this week's
traffic look like the data the live model was trained on?" — which is the
question that predicts model decay before any labels arrive.

**Considered instead:** hand-rolled Population Stability Index (about forty
lines, and worth writing once to understand it — but Evidently's reports are
genuinely good and it handles the categorical cases correctly).

### Prometheus + Grafana
**What they are:** Prometheus scrapes numeric metrics from services and stores
them as time series. Grafana draws them.

**Why they are here:** this is the standard operational monitoring stack, and
using it signals familiarity with how services are actually run. The scoring API
exposes request rate, latency percentiles, error rate, score distribution and
feature-null rates; Grafana turns them into the dashboard that is the single most
screenshot-worthy artifact of the whole project.

**Considered instead:** logging to a file and grepping it (no percentiles, no
alerts, no history), a hosted vendor (works, costs money, and hides the mechanics).

---

## Testing and delivery

### pytest
Standard Python testing. The interesting tests here are not the usual ones:

- Feature computation produces identical results offline and online.
- A deliberately leaky feature is caught and rejected.
- The promotion gate refuses a model that is worse than the champion.
- Rollback restores the previous model version.

### Locust
**What it is:** a load testing tool where the load scenario is written in Python.

**Why it is here:** the 50 ms latency claim in the README is worthless unless it
was measured under concurrent load. Locust produces the percentile numbers that
back it up.

**Considered instead:** k6 (excellent, JavaScript scenarios), ab / wrk (fine for
a flat endpoint, awkward for realistic varied payloads).

### Docker Compose
**What it is:** runs several containers together from one configuration file.

**Why it is here:** the system is six services. Anyone evaluating this project
should be able to run `docker compose up` and have all of it working. A portfolio
project that cannot be started by a stranger in one command has failed at its
only job.

### GitHub Actions
**What it is:** the CI system built into GitHub.

**Why it is here:** and specifically, what it runs is the point. Beyond linting
and unit tests, the pipeline runs **data validation** and a **model quality
gate** — the build fails if the model's expected cost regresses beyond a
threshold. Treating model quality as a build failure rather than a dashboard is
the core idea of MLOps.

### uv
**What it is:** a fast Python package and environment manager, a replacement for
pip and virtualenv.

**Why it is here:** it resolves and installs in seconds rather than minutes, and
produces a genuine lockfile, so the training environment is reproducible.

**Considered instead:** pip + requirements.txt (no real lockfile), Poetry
(good, considerably slower), conda (heavy, and unnecessary without native
scientific dependencies).

---

## Deliberately not used

| Not used | Why not |
| --- | --- |
| Kubernetes | Adds weeks of work and teaches nothing about machine learning. Docker Compose demonstrates the same containerisation understanding. |
| A deep learning framework | Worse than gradient boosted trees on tabular data. Using one here would signal reaching for the impressive tool over the correct one. |
| A cloud provider | Locks the project to an account, costs money, and makes it unrunnable by a reviewer. Every component chosen has a direct managed equivalent, listed in the decisions log. |
| A front-end | Nobody evaluating this will look at a web page. The Grafana dashboard is the interface. |
| A large language model | There is no natural language in this problem. Adding one would be decoration. |

---

Next: [4. The Roadmap](04-roadmap.md)
