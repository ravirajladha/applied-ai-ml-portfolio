# Webinar 2 — CI/CD with GitHub Actions & DVC

> **Companion:** `friend notes/3.pdf` · (webinar — no slide deck in this set)
>
> **One-line goal:** automate the quality gate on every commit, and version data for **full reproducibility**.

### Contents
1. [What is a CI tool?](#1-what-is-a-ci-tool)
2. [CI best practices (Fowler's 10)](#2-ci-best-practices-fowlers-10)
3. [GitHub Actions](#3-github-actions)
4. [Git in one minute](#4-git-in-one-minute)
5. [DVC — data version control](#5-dvc--data-version-control)
6. [Recap](#-recap)

---

## 1. What is a CI tool?

A **Continuous Integration** tool automates **building, testing, and publishing** software. It integrates with version control to fetch the latest changes, and consists of:
- a **build server** — provides the UI, stores job definitions, starts runs;
- one or more **build agents / runners** — separate machines that actually execute the build & test steps (multiple runners → steps run in **parallel**).

> 🌍 CI is a **tireless teammate** who, every time anyone pushes code, checks out the latest version, builds it, runs all the tests, and shouts immediately if anything broke. The faster and more automatic that loop, the less "works on my machine" pain.

---

## 2. CI best practices (Fowler's 10)

| | | | |
|---|---|---|---|
| 1. Single code repository | 2. Automate the build (one command) | 3. Make the build self-testing | 4. Everyone commits to baseline daily |
| 5. Every commit is built | 6. Every bug-fix commit ships a test | 7. Keep the build fast | 8. Test in a clone of production |
| 9. Everyone sees the latest build result | 10. Automate deployment (CD) | | |

> 🎯 The thread through all ten: **integrate early, integrate often, automate the verification.** Small frequent commits, each automatically built & tested in a production-like environment, catch conflicts and regressions while they're still cheap to fix.

---

## 3. GitHub Actions

**GitHub Actions** = GitHub's native CI/CD (2018), on by default in every repo. A **workflow** is a YAML file in `.github/workflows/`, versioned alongside the code it tests, triggered by **events** (push, PR, schedule, webhook). The concepts nest:

```
event (push/PR) → workflow → job (on a runner) → step (command / action)
```

- **Runner** — a GitHub-hosted VM with an OS; each job runs on one (`runs-on: ubuntu-latest` mirrors a Linux prod box).
- **Step** — a shell command or an **action** (a reusable, shareable unit with inputs/outputs).
- **Job** — a set of steps; a **workflow** — one or more jobs triggered by an event.

> 🧪 **The fraud-demo `ci.yml`, top to bottom.** `on: push` triggers on every commit to `main`; `runs-on: ubuntu-latest` mirrors production; then five steps run in order: **checkout → setup-python 3.11 → pip install → generate data → train → pytest.** The workflow file lives in the repo, so the test recipe is **versioned with the code it tests**.

> 🧪 **Quality attributes drive design — live.** Change `LATENCY_THRESHOLD_MS` from 200 to 1, commit, push. Actions triggers within seconds; pytest **fails**: "prediction took X ms — exceeds 1 ms SLA." Revert to 200, push → **green**. The red/green of the pipeline *is* the quality attribute (performance) acting as an enforceable gate.

---

## 4. Git in one minute

CI can only trigger once code lives in Git. The everyday loop is three commands:

```
git pull            # get teammates' changes first
git add & commit    # a named snapshot — use a type prefix: feat/fix/ci/data/test
git push            # triggers CI
```

Work happens on **feature branches**; `main` is the protected, always-working production branch that Actions watches.

> ⚠️ **Not everything belongs in Git.** `.gitignore` excludes `venv/`, `__pycache__/`, MLflow's `mlruns/`, secrets (`.env`), and large/regenerable artifacts. **Rule of thumb:** if it can be regenerated, is large, or holds secrets — keep it out of Git.

---

## 5. DVC — data version control

That rule of thumb creates a problem: datasets and models are large → they stay out of Git → but then *"which data trained which model?"* is unanswerable. **DVC (Data Version Control)** brings Git-style versioning to data & models: the large file stays out of Git (in remote storage — S3, GDrive, a folder); only a small **fingerprint** (a `.dvc` file with an md5 hash) is committed.

> 🧪 **The `.dvc` fingerprint.** `dvc add data/fraud_data.csv` produces `fraud_data.csv.dvc` containing `md5: a3f2c1d8...`, size, path. That tiny file is committed to Git; the CSV goes into `.gitignore`. Six months later, `git checkout <commit>` + `dvc pull` restores the **exact dataset** that commit used — code version and data version now move together.

| **MLflow** | **DVC** |
|---|---|
| Tracks experiments, params, metrics, model registry | Versions data & model **files** |
| Answers *"which run/params gave this metric?"* | Answers *"which data produced this model?"* |

---

## 🎯 Recap

> **GitHub Actions** automates the quality gate (Webinar 1's pytest) on every push; **Git** versions the code; **DVC** versions the data & models. Together — **Git + DVC + MLflow** = code version + data version + experiment record → **full reproducibility**: any past result can be recreated exactly.

🏠 [Back to index](README.md)
