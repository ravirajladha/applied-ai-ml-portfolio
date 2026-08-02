# 4. The Roadmap

Seven milestones. Each one ends with something that runs and something that can
be shown to another person. Nothing is built ahead of the milestone that needs
it.

Progress is recorded in [`BUILD-LOG.md`](BUILD-LOG.md) as each session happens.

---

## M0 — Documentation and planning ✅

**Goal:** know what is being built and why, before writing any code.

- [x] Problem statement with the cost model
- [x] Architecture walkthrough
- [x] Tool selection with reasoning and alternatives
- [x] Glossary
- [x] This roadmap
- [x] Decision log started
- [x] Build log started

**Shows:** that the project was designed rather than accumulated.

---

## M1 — The stream and the offline store

**Goal:** transactions flowing through a real message broker, landing on disk.

- [x] Repository skeleton, `uv` project, ruff, mypy, pre-commit, CI workflow
- [x] Canonical `Transaction` contract — pydantic for single events, pandera for
      tables, with a test that stops the two drifting apart
- [x] Dataset profiler, built on DuckDB so it reads the CSV without loading it
- [x] 27 tests passing; `ruff`, `ruff format` and `mypy` all clean
- [x] `docker-compose.yml` with Redpanda and Redis
- [x] Working environment: WSL2 + Ubuntu 24.04, every dependency installed,
      Redpanda and Redis running and verified by an actual round trip
      ([`docs/07-setup.md`](07-setup.md))
- [ ] Dataset downloaded and profiled — **read `share of transactions from
      repeat accounts` first**; below ~0.2 the feature plan has to be rebuilt
- [ ] pandera schema for the raw PaySim columns, written *after* profiling
- [ ] PaySim adapter mapping raw columns onto the canonical contract
- [ ] Replay producer: reads history, publishes to the topic at configurable
      speed, preserving real inter-arrival gaps
- [ ] Archiver consumer: writes everything to partitioned Parquet
- [ ] DuckDB queries confirming the round trip lost nothing

**Shows:** streaming and data engineering fundamentals.

**Done when:** `make replay` streams a day of transactions and the Parquet
files contain exactly the same rows, verified by a test.

---

## M2 — Features, computed twice and proven identical

The most important milestone in the project. Everything else is downstream of
getting this right.

- [ ] Feature specification: every feature named, defined precisely, with its
      time window written down
- [ ] Online path: stream consumer maintaining rolling aggregates in Redis, with
      key expiry
- [ ] Offline path: DuckDB SQL producing the same features over history, using
      window frames that can only look backwards
- [ ] **Parity test** — run both paths over the same slice of history and assert
      the numbers match to within floating point tolerance
- [ ] **Leakage test** — plant a feature that peeks at the future, assert the
      pipeline rejects it
- [ ] Redis read benchmark, documented

**Shows:** understanding of train/serve skew and point-in-time correctness — the
two things that separate people who have run machine learning in production from
people who have not.

**Done when:** the parity test passes in CI and the feature specification is
written down clearly enough that a stranger could reimplement either path.

---

## M3 — A model, tracked and exported

- [ ] Training script building a point-in-time-correct dataset
- [ ] Time-based train/validation/test split — never a random split, because a
      random split leaks the future into the past
- [ ] LightGBM baseline with class weighting
- [ ] Evaluation: precision, recall, area under the precision-recall curve, and
      a confusion matrix at the chosen threshold
- [ ] **Cost curve** — expected cost across every candidate threshold, plotted,
      with the optimum marked
- [ ] Everything logged to MLflow: parameters, metrics, code commit, data
      version, plots
- [ ] ONNX export with a test asserting the ONNX model and the LightGBM model
      agree on a thousand sample rows

**Shows:** modelling competence with the parts that actually matter — honest
evaluation on imbalanced data, and a business-grounded decision threshold.

**Done when:** a model exists in the MLflow registry with its threshold and its
cost curve attached.

---

## M4 — Serving it, fast

- [ ] FastAPI service, `/score`, `/health`, `/metrics`
- [ ] Model loaded from the MLflow registry by stage, not by file path
- [ ] Redis feature lookup on the request path
- [ ] Asynchronous logging of features, score and decision — never blocking the
      response
- [ ] Prometheus metrics exported
- [ ] Locust load test, percentiles recorded in the README
- [ ] Latency profiling: where the milliseconds actually go, documented
- [ ] Dockerfile, service added to compose

**Shows:** that a model was turned into a service with a real latency budget.

**Done when:** p99 is under 50 ms at realistic concurrency, measured and written
down with the hardware it was measured on.

---

## M5 — Watching it

- [ ] Grafana dashboard: traffic, latency percentiles, error rate, score
      distribution, feature null rates
- [ ] Evidently drift job comparing recent traffic to the training distribution
- [ ] Population Stability Index per feature, exported as a metric
- [ ] Alert rules: latency breach, error rate, score distribution shift, drift
      threshold
- [ ] **A deliberate break** — inject a realistic data fault (a unit change, a
      null flood, a stale feature) and demonstrate the monitoring catching it
- [ ] Write up that break in `docs/incidents/`

**Shows:** operational maturity. The deliberate break is the part that gets
remembered.

**Done when:** the dashboard screenshot is in the README and at least one
incident is written up.

---

## M6 — The loop that keeps it alive

- [ ] Label simulator: labels arrive on a realistic 30–60 day delay
- [ ] Label join job, backfilling truth onto logged decisions
- [ ] Delayed performance reporting — what the model's precision and cost
      actually were, once known
- [ ] Prefect retraining flow on a schedule
- [ ] **Promotion gate** as code: challenger must beat champion on expected cost,
      must not regress on any major segment, must have a sane score distribution
- [ ] Shadow mode: challenger scores live traffic, decisions recorded and discarded
- [ ] One-command rollback, with a test that exercises it
- [ ] CI model quality gate — build fails if the model regresses

**Shows:** the full MLOps lifecycle, including the parts most portfolio projects
stop before.

**Done when:** a scheduled retrain runs unattended, is refused by the gate for a
deliberately bad model, and accepted for a good one.

---

## M7 — Making it presentable

- [ ] README rewritten around results: architecture diagram, latency numbers,
      cost curve, dashboard screenshot
- [ ] "Design decisions and trade-offs" section — the part reviewers actually read
- [ ] Three or more incident write-ups
- [ ] A short recorded walkthrough
- [ ] Fresh-clone test: wipe everything, clone, `docker compose up`, confirm it
      works with no undocumented steps

**Shows:** that the work can be communicated, which is half of what is being
assessed.

---

## Stretch, only if the above is genuinely finished

- Swap the dataset for IEEE-CIS — messier, wider, closer to real data
- Replace direct Redis use with Feast, and write up what changed
- Add SHAP explanations to the API response, so a blocked transaction comes with
  a reason
- Deploy to one cloud provider and record the cost
- Multi-armed bandit for threshold tuning instead of a fixed value

---

## What "finished" is not

- Not a better score. Model accuracy is not what is being evaluated here.
- Not more models. One well-served model beats five in a notebook.
- Not a web interface. Grafana is the interface.
- Not Kubernetes.

---

Next: [5. Glossary](05-glossary.md)
