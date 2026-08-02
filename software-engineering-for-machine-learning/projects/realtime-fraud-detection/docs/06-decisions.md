# 6. Decisions

A running log of significant design decisions. Each entry records what was
decided, why, what was given up, and when it should be revisited.

New entries are appended, never edited. If a decision is reversed, a new entry
supersedes the old one and the old one is marked.

**Format:** context → decision → consequences.

---

## ADR-0001 — Record decisions in this file

**Date:** 2026-08-02
**Status:** Accepted

**Context.** In a system with this many moving parts, the reasoning behind a
choice is more valuable than the choice itself, and it evaporates within weeks.
The most common question asked about a portfolio project is "why did you do it
that way", and the most common failure is not remembering.

**Decision.** Every significant decision gets an entry here, written at the time
it is made. Significant means: it constrains future work, it was a close call
between real alternatives, or it would surprise a reader.

**Consequences.** Slight overhead per decision. In exchange, the "design
decisions and trade-offs" section of the final README writes itself, and
interview answers are grounded in written reasoning rather than reconstruction.

---

## ADR-0002 — Use PaySim as the primary dataset

**Date:** 2026-08-02
**Status:** Accepted

**Context.** The project needs a transaction dataset with fraud labels, entity
identifiers to build per-account history from, and timestamps. Three realistic
candidates:

| Dataset | Rows | Strengths | Problems |
| --- | --- | --- | --- |
| PaySim (synthetic mobile money) | ~6.3M | Clear account IDs, transaction types, amounts, balances; large enough to be interesting | Timestamps only at hour granularity; synthetic, so fraud patterns are simpler than real life |
| IEEE-CIS Fraud Detection | ~590K | Real data, second-level timestamps, rich device and card fields | 434 columns, heavily anonymised, large amounts of missing data, no clean account identifier |
| ULB Credit Card Fraud | ~285K | Small, clean, widely known | Features are already PCA-transformed, so no feature engineering is possible at all |

**Decision.** PaySim for the initial build. ULB is disqualified outright — its
columns are anonymised principal components, which eliminates the feature
engineering that is the entire point of this project. IEEE-CIS is kept as a
Milestone 7 stretch goal, because its messiness is realistic but would slow the
first pass through the pipeline considerably.

**Consequences.**
- PaySim's `step` column is an hour index, not a real timestamp. Short-window
  features ("last 60 seconds") need sub-hour resolution to be meaningful.
  **Mitigation:** the replay producer distributes each hour's transactions
  across that hour using a deterministic pseudo-random offset seeded by
  transaction ID, so timestamps are reproducible but realistically spaced. This
  is a synthetic assumption and must be stated plainly in the README — presenting
  invented timestamps as real would be dishonest.
- Fraud patterns in PaySim are simpler than real fraud, so model performance
  will look better than it would in reality. The README will say so.
- Moving to IEEE-CIS later will exercise the pipeline's tolerance for missing
  data and wide schemas, which is a genuine test of the design.

**Revisit when:** the pipeline is complete end to end (after M6).

---

## ADR-0003 — Use Redis directly instead of a purpose-built feature store

**Date:** 2026-08-02
**Status:** Accepted

**Context.** Feast is the standard open-source feature store. It manages feature
definitions, materialises them to an online store, and serves them consistently
to training and inference — exactly the problem this project is about.

**Decision.** Use Redis directly, with the online and offline feature paths
written by hand and a parity test proving they agree.

**Reasoning.** Feast would solve the train/serve consistency problem by hiding
it. The purpose of this project is to demonstrate understanding of that problem,
which requires implementing both sides and proving they match. Building it once
by hand also makes it possible to explain, in an interview, precisely what a
feature store does and why it exists.

**Consequences.**
- More code to write and maintain, particularly the parity test.
- No feature versioning or point-in-time join machinery for free — both must be
  implemented deliberately.
- The decision must be defended, not apologised for. `docs/03-tools.md` states
  it explicitly, and the README notes what adopting Feast would change.

**Revisit when:** feature count exceeds roughly thirty, or if a second consumer
of the same features appears.

---

## ADR-0004 — Choose the decision threshold by expected cost, not by F1

**Date:** 2026-08-02
**Status:** Accepted

**Context.** The model outputs a probability; something must convert it to
approve or block. The common defaults are 0.5, or the threshold that maximises
the F1 score.

**Decision.** Compute the threshold that minimises expected monetary cost, using
explicit assumed costs for a missed fraud and for a false alarm. Publish the
assumptions, publish the full cost curve, and store the resulting threshold
alongside the model as part of its versioned artifact.

**Reasoning.** 0.5 is arbitrary. F1 implicitly assumes precision and recall are
equally valuable, which is flatly untrue here — a missed fraud costs roughly
twenty-five times a false alarm. Any threshold not derived from the cost
asymmetry is being chosen by accident.

**Consequences.**
- The cost assumptions become a documented, challengeable input. This is a
  feature: it makes the reasoning inspectable rather than buried.
- Changing the threshold is a deployment, versioned with the model, because it
  changes system behaviour as surely as changing the model does.
- The cost curve becomes one of the more compelling artifacts in the README.

**Revisit when:** real cost figures are available, or if costs vary by
transaction size enough to justify a per-transaction threshold.

---

## ADR-0005 — Ship a boring model on purpose

**Date:** 2026-08-02
**Status:** Accepted

**Context.** There is a standing temptation in portfolio projects to reach for
the most impressive-sounding model available.

**Decision.** LightGBM with sensible defaults and light tuning. No neural
networks, no ensembling, no architecture search. Effort goes into the system
around the model.

**Reasoning.** On tabular data, gradient boosted trees outperform neural
networks. They also train in seconds, explain their predictions, and need no
GPU. For a target role in ML engineering and MLOps, an extra point of AUC is
worth nothing while a working promotion gate is worth a great deal. Choosing the
correct simple tool over the impressive complex one is itself the signal.

**Consequences.**
- The project will not top any leaderboard. It is not entering one.
- The README must state this choice explicitly, or a reader may mistake it for
  a limitation rather than a decision.
- Model training stays fast, which keeps the retraining loop practical to
  develop and demonstrate.

**Revisit when:** never, for this project.

---

## ADR-0006 — Run everything locally with Docker Compose, no cloud

**Date:** 2026-08-02
**Status:** Accepted

**Context.** The system has six services. They could run on a cloud provider
with managed equivalents (MSK for Kafka, ElastiCache for Redis, SageMaker for
model hosting).

**Decision.** Everything runs locally via `docker compose up`. No cloud account
is required to run or evaluate the project.

**Reasoning.** A portfolio project must be runnable by a stranger in one command.
A cloud deployment costs money, expires, requires credentials nobody will
request, and is usually dead by the time anyone looks at the repository. The
architecture stays cloud-shaped, and `docs/03-tools.md` lists the managed
equivalent for each component, so the migration path is visible without being
built.

**Consequences.**
- No demonstration of cloud-specific skills. Accepted; a live cloud deployment
  is listed as a stretch goal if the core is genuinely finished.
- Scale is limited to one machine, which is fine at this data volume.
- The fresh-clone test in M7 becomes a real acceptance criterion rather than a
  formality.

**Revisit when:** the core project is complete through M7.

---

## ADR-0007 — Development environment on Windows ARM64

**Date:** 2026-08-02
**Status:** Accepted — WSL2 with Ubuntu 24.04 LTS

**Context.** The development machine is Windows 11 on ARM64, running a native
ARM64 build of Python 3.12. That combination turns out to have no wheels for
several of this project's core dependencies. Measured directly, not assumed:

| Package | Native win-arm64 | Needed for |
| --- | --- | --- |
| pyarrow | **no wheel** | Parquet, the offline store |
| lightgbm | **no wheel** | the model |
| confluent-kafka | **no wheel** | the Kafka client |
| mlflow | **no wheel** (depends on pyarrow) | tracking and registry |
| fastparquet | **no wheel** | Parquet fallback |
| pandas, numpy, scipy, scikit-learn, polars, duckdb, onnxruntime, redis, pydantic, pandera, fastapi, structlog | wheel available | — |

Each missing package falls back to building from source, which then fails for
want of MSVC build tools — and even with them, building Arrow and LightGBM from
source on ARM64 is not a reasonable prerequisite for a project anyone should be
able to clone and run.

Separately, there is no Docker and no WSL distribution installed, and Redpanda
has no Windows build at all. Free disk is 14.3 GB, which rules out anything
extravagant.

**Options.**

1. **WSL2 with Ubuntu (arm64).** Every missing package has a linux-aarch64
   wheel. Redis installs with `apt`. Redpanda ships an arm64 Linux build.
   Solves the packaging problem and the broker problem together, and is how
   machine learning work on Windows is normally done. Costs roughly 3–5 GB and
   a one-time setup.
2. **An x64 build of Python, under Windows-on-ARM emulation.** Every package
   has a `win_amd64` wheel, so the Python side is fixed immediately with a
   single install. Does nothing for Redpanda or Redis, which still need Docker
   Desktop — another 2–4 GB, and Docker Desktop also wants WSL2 underneath.
   Emulation costs perhaps 20–40% CPU, irrelevant at this data volume.
3. **Substitute every unavailable package.** DuckDB writes Parquet natively,
   `kafka-python-ng` is pure Python, and scikit-learn's
   `HistGradientBoostingClassifier` is a credible stand-in for LightGBM. This
   works for the Python layer, but there is still no broker and no Redis on
   native Windows ARM64, so it does not actually unblock M1. It also means
   diverging from the tools the project claims to use, which weakens the point
   of the exercise.

**Decision.** Option 1 — WSL2 with Ubuntu 24.04 LTS. Development happens inside
the Linux environment; Windows is the host only.

**Reasoning.** It is the only option that fixes both problems with one install.
Option 2 fixes the Python packaging but still requires Docker Desktop for the
broker, and Docker Desktop needs WSL2 underneath in any case — so it is strictly
more setup for a strictly worse result. Option 3 avoids installing anything but
does not unblock M1 at all, since there is no broker on native Windows ARM64
regardless of which Python packages are used, and it would mean the project
quietly stops using the tools it says it uses.

The wider argument: production machine learning runs on Linux. A project whose
whole premise is production discipline should be developed on the platform it
would be deployed to. Every path difference, permission quirk and line-ending
problem found now is one not found later.

Ubuntu 24.04 LTS rather than 26.04: it is the version with the longest track
record of working wheels for this stack, and a portfolio project is the wrong
place to be the first person to hit a packaging bug.

**Consequences.**
- The repository lives in the Linux filesystem (`~/dev/...`), not under
  `/mnt/c/`. Cross-filesystem access in WSL2 is slow enough to matter when
  reading a 470 MB CSV, and file-watching does not work reliably across the
  boundary.
- Windows-side tooling loses direct access. Editors reach the code through
  their WSL remote support, which is standard practice.
- Roughly 3–5 GB of the 14.3 GB free is consumed. Enough headroom remains for
  the dataset and the Parquet offline store, but disk should be watched before
  the Prometheus and Grafana services arrive at M5.
- Docker is no longer required at all: Redis installs from `apt` and Redpanda
  ships an arm64 `.deb`. `docker-compose.yml` is kept and maintained anyway,
  because it is how a reviewer will expect to start the project, and ADR-0006
  still stands.
- Line endings need care. Git on the Windows side was converting to CRLF; the
  repository gets a `.gitattributes` enforcing LF so the same checkout behaves
  identically from both sides.

**Revisit when:** never, unless the machine changes.

---

## ADR-0008 — Split the repository across three locations

**Date:** 2026-08-02
**Status:** Accepted

**Context.** Setting up the WSL2 environment (ADR-0007) exposed a disk problem.
The `C:` drive went from 14.3 GB free to 2.2 GB: the Ubuntu image, the Python
environment and the package caches together are several gigabytes, and the
dataset (~470 MB) plus the Parquet offline store had not even arrived yet.

The machine turned out to have a second fixed NTFS partition, `A:`, with 95 GB
free on the same NVMe disk.

There are also two performance considerations specific to WSL2:

- Access to Windows drives (`/mnt/c`, `/mnt/a`) goes through a translation
  layer and is markedly slower than the Linux filesystem, especially for
  operations touching many small files.
- A virtual environment contains thousands of small files and is exactly the
  worst case for that.

**Decision.** Three locations, each chosen for what lives there:

| What | Where | Why |
| --- | --- | --- |
| Code and docs | Inside the coursework repository, under `software-engineering-for-machine-learning/projects/` (reached as `/mnt/c/...` from Linux) | One copy, editable from either side. Small enough that the slower path does not matter. |
| Virtual environment | `~/.venvs/rtfd` inside WSL | Thousands of small files; belongs on the Linux filesystem. Also keeps a Linux venv from colliding with a Windows one in the same directory. |
| Dataset and offline store | `/mnt/a/rtfd-data` (the `A:` drive) | The only volume with room. Sequential reads of large Parquet and CSV files tolerate the translation layer well. |

Set via `RTFD_DATA_DIR` in `.env`, and `UV_PROJECT_ENVIRONMENT` in the shell.

**Consequences.**
- The repository is not self-contained: a fresh clone needs `.env` pointing at
  a data directory with several gigabytes free. `docs/07-setup.md` says so
  explicitly, and `.env.example` carries the warning.
- `raw_dir` and `offline_dir` had to become derived properties rather than
  independent settings. As originally written, setting `RTFD_DATA_DIR` moved
  nothing — the sub-directories kept their own defaults and data would still
  have landed on the full disk, silently. Fixed, with a test.
- Sparse VHD, which would let the WSL disk image shrink when files are deleted,
  is disabled by default in this WSL version because of a data-corruption risk.
  It was **not** force-enabled. The image therefore only grows, which is a
  further argument for keeping bulk data outside it.
- `C:` remains tight. If it becomes a problem the WSL image can be moved to
  `A:` with `wsl --manage Ubuntu-24.04 --move`, which would return 4.1 GB and
  give the Linux filesystem room to grow.

**Revisit when:** `C:` free space drops below 2 GB, or the offline store starts
being read often enough for the translation layer to show up in profiling.

---

*Next entries are appended as decisions are made during the build.*

---

Back to: [README](../README.md)
