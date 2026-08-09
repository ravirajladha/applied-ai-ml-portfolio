# Repo sync log — where this project lives, and how the two copies stay in step

This assignment is maintained in **two** places. This file records which is
which, which direction changes flow, and what has been synced so far.

> **For the group:** the canonical copy of this project is maintained inside a
> personal AI/ML portfolio repo and mirrored here. That is why the git history
> in this repo arrives in large, squashed chunks rather than commit by commit.
> Nothing here depends on that — clone this repo and everything works.

---

## The two repos

| | Ours (source of truth) | Team |
|---|---|---|
| Remote | `origin` | `team` |
| URL | `git@github.com:ravirajladha/applied-ai-ml-portfolio.git` | `git@github.com:sumanthtps/customer-review-text-summarization.git` |
| Default branch | `master` | `main` |
| Where the project sits | `natural-language-processing/assignments/assignment-2/` | repo root |
| Contains | the whole AI/ML portfolio, all subjects | this assignment only |

**The path differs.** Ours is nested three levels deep; theirs is at the root.
So the two repos can never share history directly — a plain `git push` from
ours to theirs would dump the entire portfolio into their repo. Syncing is done
by copying the folder's *contents* onto a branch cut from `team/main`.

## Direction of flow

```
  edit here  ──►  commit to origin/master  ──►  branch off team/main  ──►  PR into team/main
 (portfolio)        (ours, always first)         (contents copied to root)
```

Rule: **nothing goes to the team repo that is not already committed to ours.**
Ours is the record of the work; theirs is the group's shared submission copy.

## How to push a sync to the team repo

From a scratch directory, not from inside the portfolio repo:

```bash
git clone git@github.com:sumanthtps/customer-review-text-summarization.git team-sync
cd team-sync
git checkout -b <branch-name> main

# wipe tracked files, then copy our folder's contents over the top
git rm -r --quiet .
cp -r "<portfolio>/natural-language-processing/assignments/assignment-2/." .
rm -rf .venv models __pycache__ .ipynb_checkpoints   # never push these

git add -A && git commit && git push -u origin <branch-name>
```

Then open a PR into `main` so the group can review before it lands.

### Never pushed to the team repo

- `.venv/`, `models/`, `__pycache__/`, `.ipynb_checkpoints/` — build artefacts
  and the 234 MB model, all git-ignored. `train.py` rebuilds the model.

---

## Sync history

| Date | Ours (`origin/master`) | Team (`team`) | What went across |
|---|---|---|---|
| 2026-08-07 | not yet tracked | `main` @ `9ee93dc` | First working end-to-end version, pushed before the portfolio started tracking this folder. Pre-split layout: `train.py`, `summarizer.py`, `app.py`. |
| 2026-08-09 | `master` @ `42507f9` | `split-by-task-and-owner` @ `d4b21e0` | The by-task/by-owner split, Group 140 details, regenerated `Group140.pdf`/`.html`. **Branch pushed, PR into `main` not yet opened.** |

Diff of `d4b21e0` against their `main`: 29 files changed, 17 of them new
modules — `+3130 / -1699`.

### What changed in the 2026-08-09 sync

`team/main` is still the **pre-split** three-file layout. Everything below is
new to the team repo:

- **Split by task and owner** (5 members, one owner per module):
  `config.py`, `data_prep.py` · `attention.py`, `model_lstm.py`,
  `train_lstm.py`, `infer_lstm.py` · `model_t5.py`, `train_t5.py`,
  `aggregate.py`, `aspects.py` · `summarizer_service.py`, `flask_app.py`,
  `run_osha.sh` · `evaluate_rouge.py`, `demo_cases.py`
- `verify.py` — whole-project health check
- Notebook restructured into sections 1–6 matching the PS-11 mark scheme
- **Group number 140** recorded; exports renamed `Group_TBD.*` → `Group140.*`
- Report re-exported from the current notebook (22 → 23 pages)

`summarizer.py` and `train.py` are kept as thin compatibility wrappers, so
anything the group already had running against the old layout still works.
