# Assignment 2 - fix notes

Notes on the review pass over `Vivek_Group_95_Q_learning_DQN_DDQN_Solution.ipynb`
(LunarLander-v3, DQN vs DDQN under stochastic action failure).

Every changed line in the notebook carries a one-line marker comment above it,
`# [EDIT n - NEW]` or `# [EDIT n - CHANGED]`, where `n` is the item number below.
Search the notebook for `[EDIT` to walk through them. The first cell of the
notebook repeats this as a change-log table.

---

## 1. Target network was refreshing too rarely

**Problem.** In `DQNAgent.learn_if_ready`, the target-copy check
`environment_steps % target_update_steps == 0` sat *after* the
`environment_steps % train_every_steps != 0: return` guard. Both tests ran on the
same counter, so a refresh only happened when the two periods coincided, that is
at their lowest common multiple.

**Fix.** `__init__` now computes
`target_update_period = max(1, target_update_steps // train_every_steps)`, and the
check became `optimization_steps % target_update_period == 0`. The period is also
written into the saved checkpoint so the cadence stays auditable.

**Evidence.** Quick run: 189 optimizer steps produced 3 refreshes, one per 248
environment steps, against 1 refresh before the fix.

**Scope caveat.** With `FULL_CONFIG` (1000 / 4) the old rule coincidentally gave
the right cadence, so this does not invalidate an earlier full run. It was
genuinely wrong in `QUICK_CONFIG` (250 / 4, firing every 500 steps).

## 2. All four plots used a moving average

**Problem.** The assignment asks for a 100-episode moving average *only* on the
landing rate. Reward and Q-value were smoothed as well, hiding the per-episode
variance the plots are supposed to show.

**Fix.** `plot_metric` now takes `show_raw_series` and `show_moving_average`
instead of a single `use_moving_average` flag. Episode reward and predicted
Q-value draw the raw per-episode series at `alpha=0.25` with the 100-episode
moving average overlaid in the same colour; landing rate and thruster count are
unchanged and stay moving-average only.

## 3. Rewards were not comparable across environments

**Problem.** The modified environment's `episode_reward` includes the -0.3
per-thruster-step fuel penalty and the +50 safe-landing bonus. Plotting it against
the original environment on one axis compares two different quantities: two agents
flying identically would still produce different curves.

**Fix.** `train_agent` records a per-episode `base_reward` (the difference of the
wrapper's `base_reward_sum`, which equals `episode_reward` on the original
environment), plus `base_reward_ma100`, a `last100_base_reward_mean` column in the
summary table, and a fifth plot `05_base_environment_reward.png`.

**Evidence.** In the quick run the modified curves shift up in plot 05 while the
original curves stay identical to plot 01, which is exactly the confound being
removed.

## 4. Part (a) evidence was too thin for 2.5 marks

Three additions to the verification cell:

* **Step-level trace** with columns `step, selected_action a, random r,
  executed_action a_exec, penalty_applied`, mirroring the example table in the
  question. `r` is captured by a proxy placed over the wrapper's `_rng`, and the
  executed action and penalty are read back from the wrapper's own counters, so
  the table is evidence *about* the wrapper rather than a re-implementation of its
  logic. The first 20 steps happened to contain no misfire, so 500 steps are
  traced and two views printed: the first 20 in order (showing that `a = 0` rows
  draw no random number at all) and the steps where a replacement happened. Quick
  run: 58 misfires in 500 traced steps.
* **Confidence interval.** `assert abs(rate - 0.15) < 0.03` was replaced by a
  Wilson 95% binomial confidence interval and `assert lower <= 0.15 <= upper`. A
  fixed tolerance ignores the sample size; the interval does not. Quick run:
  185/1285 = 0.1440, interval [0.1258, 0.1642].
* **Near-miss counter.** Episodes ending with both legs in contact but with
  |velocity| or |angle| >= 0.10, together with an assertion that the total bonus
  paid equals 50 x safe_landings. Quick run: 3 near misses, 0.0 bonus paid on them.

## 5. Notebook read as machine-generated (explicit grading criterion)

**Problem.** `generate_discussion()` emitted five paragraphs of prose, the part (e)
answers only said "refer to cell 87cf18a8", and a markdown cell described the
answers as draft text to be edited for clarity.

**Fix.** `generate_discussion()` is now a numeric extractor only: it prints a
labelled table of the quantities the five questions are answered from (Q-gaps,
thruster deltas, base rewards, evaluation rewards, landing rates, thruster counts)
and writes `discussion_metrics.csv`. No prose, and `discussion_draft.md` is no
longer produced. The (d) and (e) cells are headings only, five plot headings and
Q1-Q5, to be written by hand.

## 6. RUN_MODE

Left at `"quick"` for fast smoke tests, with a banner comment stating that it must
be `"full"` for the final run and that quick-mode numbers are pipeline checks, not
results.

## 7. Extra fix found along the way: unquoted pip spec

`%pip install gymnasium[box2d]>=1.0.0 torch ...` was unquoted, so the shell read
`>=1.0.0` as an output redirection. The version constraint was silently dropped
*and* the pip log was written to a file named `1.0.0` in this folder instead of
appearing as cell output. The spec is now quoted, the stray file was deleted, and
a re-run confirmed it no longer appears.

---

## Also done

* Every new function has a docstring and inline comments (1 mark is deducted for
  missing comments).
* The wrapper's reward and failure semantics were not touched; they were already
  correct against the specification.
* All four runs still share one `CONFIG` and one `SEED`. The only differences
  remain the environment flag and the DQN/DDQN target rule.
* The notebook was run end to end in quick mode: no cell errors, all five plots
  render.
* Box2D and swig were installed into the Anaconda environment, which was missing
  them, so `LunarLander-v3` can now be created locally.

## Left to do

1. Write the part (d) per-plot interpretations and the part (e) Q1-Q5 answers.
2. Rewrite the (b)/(c) answer cell. It was left untouched but is still in the
   "the `QNetwork` class in cell `59f6a8a4` defines..." pointer style, which reads
   as machine-generated.
3. Fill in the BITS IDs and the real contribution percentages.
4. Run `python strip_edit_markers.py`, set `RUN_MODE = "full"`, restart the
   kernel, run all cells, and export the PDF.

## Files in this folder

| File | Purpose |
|---|---|
| `Vivek_Group_95_Q_learning_DQN_DDQN_Solution.ipynb` | The solution notebook. Currently carries the `[EDIT]` markers and quick-mode outputs. |
| `strip_edit_markers.py` | Removes the change-log cell and all `[EDIT]` markers. Run before the final full-mode run. |
| `FIX_NOTES.md` | This file. |
| `group95_drl_artifacts/` | Plots, CSVs and checkpoints. Regenerated on every run, so it does not need to be shared. |
