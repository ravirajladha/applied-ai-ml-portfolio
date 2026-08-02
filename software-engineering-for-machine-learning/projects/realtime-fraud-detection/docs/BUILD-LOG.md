# Build Log

A running journal of how this system was built — session by session, in order,
including the things that went wrong.

## Why this file exists

Two reasons.

**For me.** Machine learning systems are built out of a hundred small decisions
made across many weeks. Without a log, the reasoning is gone within a fortnight
and the same problems get re-solved from scratch.

**For anyone reviewing this project.** A finished repository shows the
destination. This file shows the route — what was tried, what broke, what was
learned. That is usually the more interesting half.

## The rule

**Every working session gets an entry, written during or immediately after that
session — never reconstructed later.** An entry is added even if the session
achieved nothing, because "spent three hours on X and it did not work" is real
information.

## Entry format

```markdown
## Session N — YYYY-MM-DD

**Milestone:** which roadmap milestone this session serves
**Goal:** what this session set out to do, in one line

### What was done
Bullets. Concrete. Files, commands, numbers.

### What broke
What went wrong, what the symptom was, what the actual cause turned out to be.
This section is the most valuable one — never leave it empty by rounding a
struggle up to a success.

### What was learned
Anything that changed my understanding, especially about machine learning
concepts as opposed to tooling.

### Decisions made
Links to any ADR entries added in `06-decisions.md`.

### Next
The specific next action, precise enough to start on without re-reading anything.
```

---

## Session 1 — 2026-08-02

**Milestone:** M0 — documentation and planning
**Goal:** define the project properly before writing any code — what problem it
solves, how it will work, what it will be built with, and in what order.

### What was done

Created the repository at `C:\dev\realtime-fraud-detection` and wrote the full
documentation set:

- `README.md` — the front door. Problem in plain English, architecture diagram,
  tool table, links to everything else.
- `docs/01-problem.md` — the problem stated properly, including the cost model
  (a missed fraud costs roughly 25× a false alarm) and the five reasons this is
  a systems problem rather than a modelling problem.
- `docs/02-how-it-works.md` — a component-by-component walkthrough: the stream,
  the feature builder, the offline store, the scoring API, the threshold, the
  training job, the registry and promotion gate, and monitoring. Ends with the
  life of a single transaction from arrival to retraining, 47 days later.
- `docs/03-tools.md` — every tool, what it is, why it was chosen, what was
  considered instead, and a list of things deliberately not used.
- `docs/04-roadmap.md` — eight milestones (M0–M7), each ending in something
  runnable and demonstrable.
- `docs/05-glossary.md` — machine learning vocabulary translated for a software
  engineer.
- `docs/06-decisions.md` — the decision log, opened with six entries.
- `docs/incidents/` — created, with a note on what belongs there.

Also initialised git and added a `.gitignore` covering data files, model
artifacts, MLflow's local store and Python cruft. Data and models are never
committed — that is what the registry and the download script are for.

### What broke

Nothing yet — no code exists. The one thing that needed rethinking was the
dataset choice. The initial instinct was the well-known ULB credit card fraud
dataset, but its columns are already PCA-transformed, which would make feature
engineering impossible. Since feature engineering and the online/offline parity
problem are the entire point of this project, that dataset is disqualified
outright. PaySim was chosen instead, with its own drawback documented — hourly
timestamps that will need synthetic sub-hour spreading. Recorded as ADR-0002.

### What was learned

Writing the problem statement first forced a real decision that would otherwise
have been made by accident: **the decision threshold has to come from the cost
of the two kinds of mistake, not from a statistics metric.** Most tutorials use
0.5 or maximise an F1 score. Both quietly assume a false alarm and a missed
fraud are equally bad, which is untrue by roughly a factor of twenty-five. That
single realisation reshaped the evaluation plan for M3 and became ADR-0004.

The second thing that came out of writing rather than coding: the hardest part
of this system is not the model, it is guaranteeing that a feature computed live
in Redis equals the same feature computed over history in SQL. That has been
promoted to its own milestone (M2) with a parity test as its acceptance
criterion, rather than being buried inside the training work.

### Decisions made

- [ADR-0001](06-decisions.md#adr-0001--record-decisions-in-this-file) — keep a decision log
- [ADR-0002](06-decisions.md#adr-0002--use-paysim-as-the-primary-dataset) — PaySim as the primary dataset
- [ADR-0003](06-decisions.md#adr-0003--use-redis-directly-instead-of-a-purpose-built-feature-store) — Redis directly rather than Feast
- [ADR-0004](06-decisions.md#adr-0004--choose-the-decision-threshold-by-expected-cost-not-by-f1) — cost-based decision threshold
- [ADR-0005](06-decisions.md#adr-0005--ship-a-boring-model-on-purpose) — a deliberately boring model
- [ADR-0006](06-decisions.md#adr-0006--run-everything-locally-with-docker-compose-no-cloud) — local Docker Compose, no cloud

### Next

Start M1. In order:

1. `uv init`, project skeleton, ruff and pre-commit configured.
2. `docker-compose.yml` with Redpanda and Redis, and confirm both are reachable
   from the host.
3. Download PaySim and write a profiling notebook — row count, fraud rate,
   distribution of amounts per transaction type, how many distinct accounts,
   how many accounts appear more than once. That last number matters: if most
   accounts appear only once, per-account history features are worthless and the
   feature plan has to change.

---

## Session 2 — 2026-08-02

**Milestone:** M1 — the stream and the offline store
**Goal:** repository skeleton, local stack definition, and the dataset profiler.

### What was done

**Project skeleton, and it runs.**

- `pyproject.toml` — `src/` layout, hatchling, dependencies split into core /
  `train` / `serve` / `monitor` / `orchestrate` extras so a serving container
  never installs LightGBM. Ruff, mypy and pytest configured in the same file.
  Console scripts declared (`rtfd-download`, `rtfd-profile`, `rtfd-replay`,
  `rtfd-archive`) instead of a Makefile, since `make` is not available here and
  `uv run` is cross-platform anyway.
- `.pre-commit-config.yaml` — ruff, formatting, `nbstripout`, and a 1 MB file
  size ceiling so no dataset can ever be committed by accident.
- `src/rtfd/config.py` — all configuration in one place, read from the
  environment via pydantic-settings. The cost constants live here rather than in
  the training code, because they decide the block/approve threshold and
  therefore deserve to be visible.
- `src/rtfd/logging_setup.py` — structlog, JSON when not attached to a terminal.
- `src/rtfd/schemas.py` — the canonical `Transaction` contract, in two forms:
  pydantic for single events at the message boundary, pandera for whole tables
  in batch. A test asserts the two cannot drift apart.
- `docker-compose.yml` — Redpanda with correctly split internal/external
  listeners, the Redpanda Console UI, and Redis configured as a cache with no
  persistence. Services are commented by the milestone that introduces them.
- `.env.example`, `.gitignore` additions.
- `src/rtfd/data/download.py` — PaySim fetch with a readable failure path when
  Kaggle credentials are missing, rather than a stack trace.
- `src/rtfd/data/profile.py` — the profiler, built on DuckDB so it reads the CSV
  without loading 6M rows into memory.
- `tests/` — 22 tests, all passing. A synthetic PaySim-shaped CSV fixture means
  the data pipeline is testable in CI without a 470 MB download.

Verified working: `pytest` 22/22 green, `ruff check` and `ruff format --check`
clean, and the profiler run end to end against the fixture produces a complete
report.

### What broke

**Three real failures, all found by running the code rather than by reading it.**

1. **DuckDB cannot prepare DDL.** `CREATE VIEW ... read_csv_auto(?)` fails with
   `Binder Error: Unexpected prepared parameter`. Parameter binding does not
   apply to DDL statements. Switched to the relational API —
   `con.read_csv(path).create_view("tx")` — which takes the path as a Python
   argument and avoids interpolating it into SQL.

2. **pandera raises two different exception types.** A single failed check
   raises `SchemaError`; container-level validation that collects several
   raises `SchemaErrors` (plural), which is what a `strict=True`
   unexpected-column violation produces. They share no useful base class. Tests
   now assert against a tuple of both, with a comment explaining why, because
   this will otherwise be re-discovered later.

3. **Windows console mangled every non-ASCII character.** Em dashes and the ₹
   sign came out as replacement characters. The Windows console still defaults
   to a legacy code page. Worse than cosmetic: JSON log lines would be
   corrupted the same way. Fixed centrally in `configure_logging()` by
   reconfiguring stdout and stderr to UTF-8 at startup.

4. **`.gitignore` was silently excluding source code.** The data rule was
   written as `data/`, which in git matches a directory of that name *at any
   depth* — including `src/rtfd/data/`, the module holding the download and
   profile code. It only surfaced because `git status` was read carefully after
   staging rather than glanced at; three source files were simply absent from
   the list. Fixed by anchoring the pattern to the repository root as `/data/`
   (and `/reports/` for the same reason). The kind of bug that stays invisible
   until someone clones the repository and finds it does not run.

**And one blocker that stopped the milestone.**

This machine is Windows 11 on **ARM64**, running a native ARM64 Python. Probing
each dependency individually rather than assuming:

- **No win-arm64 wheel:** `pyarrow`, `lightgbm`, `confluent-kafka`, `mlflow`,
  `fastparquet`. Each falls back to a source build, which fails for want of
  MSVC build tools.
- **Wheel available:** pandas, numpy, scipy, scikit-learn, polars, duckdb,
  onnxruntime, redis, pydantic, pandera, fastapi, uvicorn, structlog,
  prometheus-client.

So `uv sync` on the full dependency list cannot succeed here at all. On top of
that there is no Docker and no WSL distribution, and Redpanda has no Windows
build in any case. Free disk is 14.3 GB.

Everything above was therefore built and tested in a venv containing only the
installable subset. Recorded as [ADR-0007](06-decisions.md#adr-0007--development-environment-on-windows-arm64),
left as *Proposed* because the fix requires installing software on the machine
and that is not my call to make.

### What was learned

**Probe the environment before writing the dependency list, not after.** The
instinct was to write `pyproject.toml` and run `uv sync`. Testing each package
individually first turned a confusing wall of build errors into a precise,
five-line finding — and the finding is the useful artifact, because it is what
makes the environment decision an informed one rather than a guess.

**A separate lesson about how the docs paid off.** `docs/02-how-it-works.md`
was written before any code, and defining the canonical `Transaction` contract
turned out to already be implied by it: the document promised that swapping
PaySim for IEEE-CIS would not disturb the feature builder or the model. That
promise is only keepable if source data is adapted into a fixed internal shape
at the boundary. So the adapter layer was not an invention during coding, it
was a consequence of something already written down.

**Something worth flagging about the label field.** `is_fraud` is
`bool | None`, and the `None` is load-bearing rather than laziness. Unknown and
"not fraud" are genuinely different states here — recent transactions are
unlabelled because the dispute window has not closed, not because they were
clean. Collapsing the two would teach the model that recent traffic is
fraud-free, which is the exact trap described in `docs/01-problem.md`. There is
a test pinning this, because a well-meaning future `.fillna(False)` would be
invisible otherwise.

### Decisions made

- [ADR-0007](06-decisions.md#adr-0007--development-environment-on-windows-arm64)
  — development environment on Windows ARM64 (**Proposed**, awaiting a choice)

### Next

Blocked on the ADR-0007 decision. Once the environment is settled:

1. `uv sync` with the full dependency list, and confirm every package imports.
2. `docker compose up -d`, confirm Redpanda is reachable from the host on
   `localhost:19092` and Redis on `6379`.
3. Kaggle credentials, then `uv run rtfd-download` and `uv run rtfd-profile`.
   **The number to read first is `share of transactions from repeat accounts`.**
   Below roughly 0.2 and the per-account feature plan is dead and has to be
   rebuilt around the counterparty — which is precisely why this is being
   checked before anything is built on top of it.
4. Then the PaySim adapter, the replay producer, and the Parquet archiver.

---

## Session 3 — 2026-08-02

**Milestone:** M1 — the stream and the offline store
**Goal:** unblock the environment, then get Redpanda and Redis actually running.

### What was done

**WSL2 with Ubuntu 24.04 LTS, and everything that was blocked now works.**

- Installed the distro with `--no-launch`, created a non-root user, enabled
  `systemd` in `/etc/wsl.conf`.
- `apt`: git, curl, redis-server, and `libgomp1`.
- Redpanda from the vendor's apt repository — v26.2.1, arm64. Configured as a
  single-node development cluster on port 19092, matching `docker-compose.yml`
  so client configuration is identical whichever way it is started.
- `uv` inside WSL, with `UV_PROJECT_ENVIRONMENT` pointing at `~/.venvs/rtfd` so
  the virtual environment sits on the Linux filesystem rather than on the slow
  translation layer.
- `uv sync --all-extras --dev` — **86 seconds, everything resolved**. Verified
  by importing each of the five previously-blocked packages: pyarrow 25.0.0,
  lightgbm 4.7.0, confluent-kafka 2.x, mlflow 3.15.0, plus duckdb, onnxruntime,
  scikit-learn and evidently.
- End-to-end verification, not just "the service is running": created a topic
  through `confluent-kafka`'s admin client, produced five messages, consumed all
  five back, deleted the topic. Then a Redis sorted-set range query — the exact
  operation the online feature store will use for rolling windows.
- Quality gates now all green on Linux: **27 tests**, `ruff check`,
  `ruff format --check`, and `mypy` with `disallow_untyped_defs`.
- Wrote `docs/07-setup.md` from the commands that actually worked, with a
  "gotchas" section for the ones that did not.
- Added `.gitattributes` enforcing LF, since the tree is now touched by git on
  both Windows and Linux.

### What broke

1. **`libgomp1` missing.** `import lightgbm` failed with
   `OSError: libgomp.so.1: cannot open shared object file`. The wheel installs
   fine but links against the OpenMP runtime at load time. Reads like a broken
   package; is actually a missing system library. One `apt install`.

2. **Redpanda ran healthy on the wrong port for ten minutes.** `systemctl` said
   `active (running)`, the logs said `Successfully started Redpanda!`, and every
   client connection was refused. Installing the deb starts the service
   immediately with the default config, *before* the config was edited —
   so it was listening on 9092 while everything was pointed at 19092. And
   `systemctl enable --now` on an already-running service does nothing, so the
   change never took effect. A plain `restart` fixed it.

   Worth dwelling on: the failure signature was *a healthy service and a
   refused connection*. `systemctl is-active` was actively misleading. The thing
   that found it was reading the log line stating which port the Kafka API had
   bound, and `ss -tlnp` showing nothing on 19092. Checking what a process is
   actually listening on beats trusting what the supervisor claims.

3. **`.gitignore` pattern matched source code** (carried over from Session 2's
   fix, noted here because it was found while staging this session's files).

4. **The Windows and Linux environments disagreed about formatting.** The
   Windows venv had an older `ruff` than the one `uv.lock` pins, so
   `ruff format --check` passed on one machine and failed on the other for the
   same files. Deleted the Windows environment. There is now exactly one, and
   the tool versions are locked.

5. **Git Bash silently rewrote Unix paths.** Passing `/tmp/rp.sh` through
   `wsl.exe` from Git Bash converted it to a Windows path, producing
   "No such file or directory" for a path that plainly existed. `MSYS_NO_PATHCONV=1`
   fixes it. Cost about ten minutes of believing the filesystem was broken.

6. **A configuration bug found only because the disk filled.** See below — this
   was the most useful failure of the session.

### The disk, and the bug it exposed

Free space on `C:` went from 14.3 GB to 2.2 GB during setup. Reclaimed about a
gigabyte by clearing the now-unused Windows-side `uv` and `pip` caches. Sparse
VHD, which would let the WSL image shrink again after deletions, is disabled by
default in this WSL version because of a data-corruption risk — deliberately
**not** force-enabled.

The machine turned out to have a second fixed partition, `A:`, with 95 GB free.
Bulk data now goes there via `RTFD_DATA_DIR=/mnt/a/rtfd-data`. Recorded as
[ADR-0008](06-decisions.md#adr-0008--split-the-repository-across-three-locations).

**And that is what exposed the bug.** `Settings` had `data_dir`, `raw_dir` and
`offline_dir` as three independent fields, each with its own default. So setting
`RTFD_DATA_DIR` to the other drive moved *nothing* — the two sub-directories
kept pointing beside the code, and the dataset would have landed on the full
disk. No error, no warning; the symptom would have been a failed download on a
full drive with no obvious cause.

Fixed by making `raw_dir` and `offline_dir` derived properties. The first
attempt typed them `Path | None`, which pushed `None`-handling out into every
consumer and broke `mypy` — the property approach keeps the public type a plain
`Path`. Four tests added, including one asserting an explicit override still
wins.

### What was learned

**"The service is running" is not the same as "the service is working."** The
Redpanda failure would have been invisible to a health check that only asked
systemd. This is precisely the distinction the monitoring milestone is about,
encountered on day one on my own laptop rather than in production — and it is
the first genuine entry for `docs/incidents/`.

**Configuration defaults should derive, not repeat.** Three independent path
settings looked harmless and was a silent data-loss trap. The general rule: when
one setting is conceptually the parent of others, express that relationship in
code. Repeating the default in three places means the three can disagree, and
nothing will tell you when they do.

**Verify the round trip, not the process.** Every environment check in this
session was written as an actual round trip — produce and consume five messages,
write and range-query a sorted set, import every package and print its version.
Each one is a few lines longer than checking a version string, and each one
would have caught a failure that a version string would have missed.

### Decisions made

- [ADR-0007](06-decisions.md#adr-0007--development-environment-on-windows-arm64)
  — WSL2 with Ubuntu 24.04 (now **Accepted**, with the reasoning against the
  alternatives)
- [ADR-0008](06-decisions.md#adr-0008--split-the-repository-across-three-locations)
  — code on `C:`, virtual environment on the Linux filesystem, bulk data on `A:`

### Next

The environment is no longer a blocker. Remaining for M1:

1. Kaggle credentials into `~/.kaggle/kaggle.json` inside WSL, then
   `uv run rtfd-download` (~470 MB onto the `A:` drive).
2. `uv run rtfd-profile`, and **read `share of transactions from repeat
   accounts` before writing another line of code.** Below roughly 0.2 the
   per-account feature plan is dead and has to be rebuilt around the
   counterparty.
3. The raw PaySim pandera schema, written from the profile rather than from
   assumption.
4. The PaySim adapter onto the canonical `Transaction` contract, including the
   deterministic sub-hour timestamp spreading from ADR-0002.
5. The replay producer and the Parquet archiver, with a round-trip test
   asserting nothing is lost between the two.

---

*Next entry goes here.*
