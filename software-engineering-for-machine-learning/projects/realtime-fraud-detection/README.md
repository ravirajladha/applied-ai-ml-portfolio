# Real-Time Fraud Detection Service

A production-style machine learning system that decides, in a few milliseconds,
whether a payment should be approved or blocked — and keeps working as fraud
patterns change.

This is not a notebook with a model in it. It is the whole system around the
model: the live data stream, the feature store, the scoring API, the monitoring,
and the retraining loop that keeps it honest.

---

## The problem, in plain English

A payment company processes thousands of transactions every second. A very small
number of them are fraud — someone using a stolen card or a hijacked account.

When a card is tapped, the company has about a tenth of a second to answer one
question: **approve or block?**

Both answers can be wrong, and they are wrong in different ways:

- **Block a real customer** → the customer is embarrassed at the counter, the
  sale is lost, and they may stop using the card.
- **Approve a fraudster** → the money is gone, and the company usually eats
  the loss.

So the job is not "find fraud". The job is "make the cheapest mistake, fast,
every single time, forever". That last word is the hard part — fraudsters change
their tactics, so a system that works in January quietly stops working by June
unless something is watching it.

## Why this is hard (and why a model alone is not enough)

| The difficulty | What it means here |
| --- | --- |
| **It has to be fast** | The card machine is waiting. Budget: under 50 ms at the 99th percentile. |
| **It needs history** | "Is this transaction weird?" only makes sense if you know this account made 1 transaction last month and 14 in the last five minutes. Those counts must be available *instantly*. |
| **The maths must match** | The numbers used to train the model must be calculated exactly the same way as the numbers used when scoring live. If they drift apart, the model is quietly wrong and nothing crashes. |
| **The answers arrive late** | You do not find out a transaction was fraud until the customer complains — often weeks later. |
| **Fraud is rare** | Roughly 1 in 1,000 transactions. A model that says "never fraud" is 99.9% accurate and completely useless. |
| **The two mistakes cost different amounts** | Blocking a good customer and missing a fraud are not equally bad. The decision threshold has to be chosen with money, not with a statistics textbook. |

This project is built to handle all six. The machine learning model itself is
deliberately simple and boring — the engineering around it is the point.

## How it works

```
  transaction stream                    ┌──────────────────────────┐
  (replayed at real speed)              │  Redis                   │
        │                               │  live running totals     │
        ▼                               │  per account / merchant  │
  ┌───────────┐    ┌──────────────┐     └───────────┬──────────────┘
  │ Redpanda  │───►│   feature    │─────────────────┘      ▲
  │  (Kafka)  │    │   builder    │───┐                    │ read
  └───────────┘    └──────────────┘   │                    │
                                      ▼            ┌───────┴────────┐
                            ┌──────────────────┐   │  Scoring API   │
                            │ Parquet history  │   │ FastAPI + ONNX │
                            │ (offline store)  │   └───────┬────────┘
                            └────────┬─────────┘           │
                                     │                     ▼
                                     ▼              approve / block
                            ┌──────────────────┐           │
                            │ training job     │           │
                            │  → MLflow        │           ▼
                            │  → promote if    │   ┌────────────────┐
                            │    better        │   │ Prometheus     │
                            └────────┬─────────┘   │ + Grafana      │
                                     │             │ + drift alerts │
                        late-arriving labels ◄─────┴────────────────┘
```

Step by step:

1. **Transactions arrive** on a stream, replayed from a real dataset at
   wall-clock speed so the system behaves like it is live.
2. **A feature builder** keeps a running summary for every account — how much
   they have spent in the last minute, hour and day, how many different
   merchants they have touched, how unusual this amount is for them. These live
   in Redis so they can be read back in under a millisecond.
3. **The scoring API** takes an incoming transaction, reads those running
   numbers, and asks the model for a fraud probability.
4. **A threshold turns that probability into a decision.** The threshold is
   picked by minimising expected cost in currency, not by maximising an
   accuracy score.
5. **Everything is logged** — the exact features used, the score, the decision.
   This is what makes the system debuggable six months later.
6. **Weeks later the truth arrives.** Real fraud labels are joined back onto
   the logged transactions.
7. **A scheduled job retrains** on the updated history, compares the new model
   against the one currently live, and only replaces it if it genuinely wins.
8. **Dashboards and alerts** watch response times, the shape of the score
   distribution, and whether the incoming data has drifted away from what the
   model was trained on.

## The tools

Every tool here was chosen because it is what a real team would reach for. See
[`docs/03-tools.md`](docs/03-tools.md) for what each one is, why it was picked,
and what the alternatives were.

| Layer | Tool |
| --- | --- |
| Streaming | Redpanda (Kafka-compatible) |
| Online feature store | Redis |
| Offline store / analytics | Parquet + DuckDB |
| Model | LightGBM |
| Fast inference | ONNX Runtime |
| API | FastAPI + Uvicorn |
| Experiment tracking & model registry | MLflow |
| Orchestration | Prefect |
| Data validation | pandera |
| Drift monitoring | Evidently |
| Metrics & dashboards | Prometheus + Grafana |
| Load testing | Locust |
| Tests | pytest |
| Packaging & local stack | Docker Compose |
| CI | GitHub Actions |

## Documentation

| Document | What is in it |
| --- | --- |
| [`docs/01-problem.md`](docs/01-problem.md) | The problem explained properly, with the money maths |
| [`docs/02-how-it-works.md`](docs/02-how-it-works.md) | A walk through the system, component by component |
| [`docs/03-tools.md`](docs/03-tools.md) | Every tool: what it is, why it is here, what else was considered |
| [`docs/04-roadmap.md`](docs/04-roadmap.md) | The build plan, milestone by milestone |
| [`docs/05-glossary.md`](docs/05-glossary.md) | Machine learning jargon translated for a software engineer |
| [`docs/06-decisions.md`](docs/06-decisions.md) | Every significant design decision and the reasoning behind it |
| [`docs/07-setup.md`](docs/07-setup.md) | How to get it running, including what failed the first time |
| [`docs/BUILD-LOG.md`](docs/BUILD-LOG.md) | A running journal of how this was built, session by session |
| [`docs/incidents/`](docs/incidents/) | Write-ups of things that broke and how they were fixed |

## Status

**Milestone 1 — in progress.** The repository skeleton, the canonical
transaction contract, and the dataset profiler are built and tested (27 tests,
lint and types clean). The development environment is up: Redpanda and Redis
running, every dependency installed and verified. The replay producer and the
Parquet archiver are next.

Setup is documented in [`docs/07-setup.md`](docs/07-setup.md), including the
parts that failed the first time.

See [`docs/04-roadmap.md`](docs/04-roadmap.md) for what remains and
[`docs/BUILD-LOG.md`](docs/BUILD-LOG.md) for how it was built, including what
broke along the way.

## Running it

Not runnable end to end yet. What works today:

```bash
uv sync --all-extras --dev   # install
uv run pytest                # 27 tests
uv run ruff check src tests  # lint
uv run rtfd-download         # fetch the dataset (needs Kaggle credentials)
uv run rtfd-profile          # profile it, writes reports/dataset-profile.md
```

The intended end state:

```bash
docker compose up -d         # Redpanda, Redis, MLflow, Prometheus, Grafana
uv run rtfd-download         # fetch and prepare the dataset
uv run rtfd-replay           # stream transactions at wall-clock speed
uv run rtfd-archive          # persist them to the offline store
uv run rtfd-serve            # scoring API on :8000
```
