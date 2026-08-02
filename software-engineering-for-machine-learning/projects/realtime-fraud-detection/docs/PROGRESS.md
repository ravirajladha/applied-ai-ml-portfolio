# Progress

Where this project actually stands, what has been built, and every problem hit
along the way with how it was resolved.

The [build log](BUILD-LOG.md) is the narrative, session by session. This page is
the checklist and the problem register.

**Last updated:** 2026-08-02

---

## At a glance

| | |
| --- | --- |
| **Milestone** | M1 of M7 — in progress |
| **Overall** | ~18% (M0 complete, M1 roughly two-thirds) |
| **Tests** | 27 passing |
| **Lint / format / types** | `ruff`, `ruff format`, `mypy` all clean |
| **Environment** | Working — Redpanda and Redis running, all dependencies installed |
| **Blocked on** | Kaggle credentials, to download the dataset |
| **Problems hit** | 13 — 12 resolved, 1 accepted |

---

## The journey

### M0 — Documentation and planning ✅

Everything written before a line of code, on purpose.

- [x] Problem statement, including the cost model that drives the whole design
- [x] Architecture walkthrough, component by component
- [x] Tool selection with reasoning *and* the alternatives rejected
- [x] Roadmap, M0 through M7
- [x] Glossary — ML jargon translated for a software engineer
- [x] Decision log opened (now 8 ADRs)
- [x] Build log opened, with the rule that every session gets an entry

**What this bought.** Two decisions came out of writing that would otherwise
have been made by accident:

1. The decision threshold must come from the **cost of the two mistakes**, not
   from a 0.5 cutoff or an F1-optimal point. A missed fraud costs roughly 25× a
   false alarm, so any threshold ignoring that asymmetry is chosen at random.
   → [ADR-0004](06-decisions.md)
2. The hardest part is not the model — it is guaranteeing a feature computed
   live in Redis equals the same feature computed over history in SQL. That was
   promoted to its own milestone (M2) with a parity test as its acceptance
   criterion.

### M1 — The stream and the offline store 🔄

**Foundations — done**

- [x] Repository skeleton: `src/` layout, `uv`, hatchling, console scripts
- [x] Tooling: ruff, mypy (`disallow_untyped_defs`), pre-commit, CI workflow
- [x] Dependencies split into core / `train` / `serve` / `monitor` / `orchestrate`
      so a serving container never installs LightGBM
- [x] `config.py` — all settings in one place, from the environment; cost
      constants live here because they decide system behaviour
- [x] `logging_setup.py` — structlog, JSON when not attached to a terminal
- [x] Canonical `Transaction` contract — pydantic for single events at the
      message boundary, pandera for tables in batch
- [x] A test asserting the two representations cannot drift apart
- [x] `.gitattributes` enforcing LF, since the tree is touched from Windows and Linux

**Environment — done**

- [x] WSL2 + Ubuntu 24.04 LTS (aarch64)
- [x] All dependencies installed and *imported*, not just resolved
- [x] Redpanda v26.2.1 running as a systemd service on port 19092
- [x] Redis 7.0.15 running
- [x] Verified by real round trips: create topic → produce 5 → consume 5 →
      delete topic, and a Redis sorted-set range query (the exact operation the
      feature store will use)
- [x] `docker-compose.yml` for anyone who prefers containers
- [x] `docs/07-setup.md` written from commands that actually ran, with a
      "gotchas" section for the ones that did not

**Data profiling — done**

- [x] `rtfd-download` — dataset fetch with a readable failure path when
      credentials are missing, rather than a stack trace
- [x] `rtfd-profile` — DuckDB-based profiler that reads the CSV without loading
      it into memory
- [x] Synthetic PaySim-shaped fixture, so the pipeline is testable in CI without
      a 470 MB download
- [x] 27 tests covering the contract, the config, and the profiler's arithmetic

**Remaining**

- [ ] Kaggle credentials in place *(needs you — see below)*
- [ ] Dataset downloaded (~470 MB, onto the `A:` drive)
- [ ] **Profile run, and `share of transactions from repeat accounts` read**
      — below roughly 0.2 the per-account feature plan is dead and must be
      rebuilt around the counterparty. Nothing gets built until this is known.
- [ ] pandera schema for the raw PaySim columns, written *from the profile*
- [ ] PaySim adapter onto the canonical contract, with the deterministic
      sub-hour timestamp spreading from ADR-0002
- [ ] Replay producer — publishes at wall-clock speed, preserving inter-arrival gaps
- [ ] Archiver consumer — writes partitioned Parquet
- [ ] Round-trip test proving nothing is lost between producer and archiver

### M2 — Features, computed twice and proven identical ⬜

The most important milestone in the project.

- [ ] Feature specification — every feature named, defined, window written down
- [ ] Online path: rolling aggregates in Redis with key expiry
- [ ] Offline path: DuckDB SQL with backward-only window frames
- [ ] **Parity test** — both paths over the same history, numbers must match
- [ ] **Leakage test** — plant a feature that peeks at the future, assert rejection
- [ ] Redis read benchmark

### M3 — A model, tracked and exported ⬜

- [ ] Point-in-time-correct training set
- [ ] Time-based split (never random — a random split leaks the future)
- [ ] LightGBM baseline with class weighting
- [ ] Evaluation: precision, recall, AUC-PR, confusion matrix
- [ ] **Cost curve** across every candidate threshold, optimum marked
- [ ] MLflow: parameters, metrics, code commit, data version, plots
- [ ] ONNX export, with a test asserting it agrees with LightGBM on 1000 rows

### M4 — Serving it, fast ⬜

- [ ] FastAPI service — `/score`, `/health`, `/metrics`
- [ ] Model loaded from the registry by stage, not by file path
- [ ] Redis feature lookup on the request path
- [ ] Asynchronous logging, never blocking the response
- [ ] Locust load test, p99 under 50 ms, recorded with the hardware

### M5 — Watching it ⬜

- [ ] Grafana dashboard: traffic, latency, score distribution, null rates
- [ ] Evidently drift job, PSI per feature
- [ ] Alert rules
- [ ] **A deliberate break**, and proof the monitoring caught it
- [ ] Incident write-up

### M6 — The loop that keeps it alive ⬜

- [ ] Labels arriving on a realistic 30–60 day delay
- [ ] Label join and delayed performance reporting
- [ ] Prefect retraining flow
- [ ] **Promotion gate as code** — challenger must beat champion on expected cost
- [ ] Shadow mode
- [ ] One-command rollback, with a test that exercises it

### M7 — Making it presentable ⬜

- [ ] README rewritten around results
- [ ] Three or more incident write-ups
- [ ] Fresh-clone test

---

## Problems hit

Thirteen so far. Every one is recorded because the failures are the part worth
reading — a repository where nothing ever went wrong is a repository where
nothing was ever run.

| # | Problem | Status |
| --- | --- | --- |
| 1 | Obvious dataset choice would have made the project pointless | Resolved |
| 2 | DuckDB cannot use parameters in DDL | Resolved |
| 3 | pandera raises two unrelated exception types | Resolved |
| 4 | Windows console mangled all non-ASCII output | Resolved |
| 5 | `.gitignore` silently excluded source code | Resolved |
| 6 | Five core packages have no Windows ARM64 wheels | Resolved |
| 7 | LightGBM wheel needs a system library | Resolved |
| 8 | Redpanda ran "healthy" on the wrong port | Resolved |
| 9 | Two Python environments disagreed about formatting | Resolved |
| 10 | Git Bash silently rewrote Unix paths | Resolved |
| 11 | Config bug that would have caused silent data loss | Resolved |
| 12 | Disk exhaustion during setup | Resolved |
| 13 | CI workflow is inert inside a subfolder | Accepted |

### The five worth understanding

**#6 — Five core packages have no Windows ARM64 wheels.**
The machine is Windows 11 on ARM64 with a native ARM64 Python. `pyarrow`,
`lightgbm`, `confluent-kafka`, `mlflow` and `fastparquet` all publish no wheel
for that platform; each falls back to a source build and fails. Not a
version-pinning problem, and no flag works around it.

*Found by* probing each dependency individually **before** writing the
dependency list, which turned a wall of build errors into a precise five-line
finding. *Fixed by* moving development into WSL2, where linux-aarch64 wheels
exist for all of them — which also solved the broker problem, since Redpanda
has no Windows build at all. → [ADR-0007](06-decisions.md)

**#8 — Redpanda ran "healthy" on the wrong port for ten minutes.**
`systemctl` reported `active (running)`. The log said "Successfully started
Redpanda!". Every client connection was refused.

Installing the `.deb` starts the service immediately with its default config,
*before* the config was edited — so it bound 9092 while everything pointed at
19092. And `systemctl enable --now` on an already-running service does nothing,
so the change never took effect. A plain `restart` fixed it.

Worth dwelling on: the signature was **a healthy service and a refused
connection**. `systemctl is-active` was actively misleading. What found it was
reading the log line stating which port had been bound, plus `ss -tlnp` showing
nothing on 19092. *Checking what a process is actually listening on beats
trusting what the supervisor claims* — which is precisely the distinction the
monitoring milestone is about, met on day one on a laptop rather than in
production.

**#11 — A config bug that would have caused silent data loss.**
`Settings` had `data_dir`, `raw_dir` and `offline_dir` as three independent
fields with three independent defaults. Setting `RTFD_DATA_DIR` to another drive
therefore moved **nothing** — the sub-directories kept pointing beside the code,
and the 470 MB dataset would have landed on a nearly-full disk. No error, no
warning; the symptom would have been a failed download with no obvious cause.

*Found by* the disk actually filling, which forced the data directory to move.
*Fixed by* making `raw_dir` and `offline_dir` derived properties. A first
attempt typed them `Path | None`, which pushed `None`-handling into every
consumer and broke `mypy` — the property approach keeps the public type a plain
`Path`. Four tests added, including one asserting an explicit override still
wins.

**The general rule this produced:** when one setting is conceptually the parent
of others, express that relationship in code. Repeating a default in three
places means the three can disagree, and nothing will tell you when they do.

**#5 — `.gitignore` silently excluded source code.**
The rule was written `data/`, which git matches *at any depth* — including
`src/rtfd/data/`, the module holding the download and profile code. Three source
files were simply absent from `git status`. *Found by* reading the staged file
list carefully rather than glancing at it. *Fixed by* anchoring to the
repository root as `/data/`. The kind of bug that stays invisible until a
stranger clones the repository and finds it does not run.

**#12 — Disk exhaustion during setup.**
Free space on `C:` fell from 14.3 GB to 2.2 GB. Investigated with measurements
rather than assumption: the WSL image accounted for 4.1 GB, and the largest
single consumer on the machine was an unrelated 72 GB `Downloads` folder, with
antivirus writing a further 6 GB of scan cache during the same window.

Bulk data was moved to a second partition with 95 GB free, via `RTFD_DATA_DIR`.
Sparse VHD — which would let the WSL image shrink after deletions — is disabled
by default in this WSL version due to a data-corruption risk, and was
deliberately **not** force-enabled. → [ADR-0008](06-decisions.md)

### The one that is accepted rather than fixed

**#13 — The CI workflow is inert.** This project lives inside a larger
coursework repository, and GitHub only runs workflows from `.github/workflows/`
at the *repository root*. The pipeline is committed and readable as a design
artifact, but it does not execute on push. Fixing it means either a root-level
workflow scoped to this path, or moving the project to its own repository.

---

## What is needed to continue

**Kaggle credentials.** The single manual step, and the only thing blocking M1.

1. Sign in at kaggle.com → Settings → API → **Create New Token**
2. Save `kaggle.json` to `~/.kaggle/kaggle.json` **inside WSL**
3. `chmod 600 ~/.kaggle/kaggle.json`

Then:

```bash
uv run rtfd-download    # ~470 MB
uv run rtfd-profile     # writes reports/dataset-profile.md
```

**And read one number before anything else gets built:**
`share of transactions from repeat accounts`. Almost every planned feature is a
per-account rolling aggregate. If most accounts appear exactly once, none of
those features carry signal, and the feature plan has to be rebuilt around the
counterparty instead. Finding that out now costs an afternoon; finding it out at
M3 costs a fortnight.

---

## Running totals

| Metric | Value |
| --- | --- |
| Documentation pages | 9 |
| Architecture decisions recorded | 8 |
| Source modules | 7 |
| Tests | 27 |
| Problems hit and resolved | 12 of 13 |
| Milestones complete | 1 of 8 (M0) |
