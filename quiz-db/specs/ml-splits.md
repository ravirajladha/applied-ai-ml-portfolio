# Train / Validation / Test: coverage spec

**Ladder:** L1 · ML Fundamentals › Evaluating Models   ·   **Prerequisites:** ml-what, ml-data (features, labels, rows)
**Why it matters for AI/ML:** Every number you report about a model is only as honest as the split behind it. Most "great offline, bad in prod" failures are a bad split or leakage, not a bad model. The same rules apply to LLM evals and prompt tuning.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `purpose` | Why train / validation / test | which set fits weights, which gives the final score, what a hyperparameter is | why tuning on test biases the score | refit on train+val after tuning | — |
| 2 | `ratios` | Split ratios and dataset size | 70/15/15 style defaults, test_size=0.2 sizes | sklearn rounding (test side is ceil), tiny data needs CV, huge data can use 98/1/1 | standard error of an accuracy, sqrt(n) scaling | — |
| 3 | `tts` | train_test_split | random_state = reproducible split, what stratify does | shuffle=False takes the tail, stratify keeps ratios (not rebalancing), two-step train/val/test | stratify + shuffle=False error, class with 1 member error, binning a regression target | — |
| 4 | `kfold` | K-fold, stratified, LOO | what k-fold is, LOO = n splits, each row tested once | KFold fold sizes, no shuffle by default, sorted labels break KFold, StratifiedKFold, reporting mean +/- spread | cross_val_score default splitter, LOO cost/variance, random_state without shuffle error | — |
| 5 | `group` | Group splits | GroupKFold name | same patient on both sides, GroupKFold never overlaps | StratifiedGroupKFold, too few groups error | split must copy deployment (cold-start users) |
| 6 | `time-series` | Time-series splits | why not to shuffle time data | TimeSeriesSplit indices, train always before test, walk-forward | max_train_size sliding window, shuffled CV vs backtest gap | gap/purging when labels look ahead |
| 7 | `nested-cv` | Tuning and nested CV | what GridSearchCV does | number of fits, best_params_ | best_score_ is optimistic, nested CV structure and fit counts | unstable inner picks, winner's curse from many trials |
| 8 | `leakage` | Data leakage | target leakage example, name | label-in-disguise feature, scaler fit on all data, duplicates across splits | exact duplicates, oversampling before split, "as of" aggregates | feature selection on all data with pure noise, TargetEncoder cross-fitting |
| 9 | `pipelines` | Pipelines to prevent leakage | why a Pipeline refits per fold | make_pipeline step names, step__param keys, spotting leaky code | handle_unknown='ignore' in a ColumnTransformer pipeline | why label-using steps leak far more than scaling |
| 10 | `test-reuse` | Test-set reuse and mismatch | — | repeated peeking, Kaggle public vs private | distribution shift between val and test, building validation like the target | adversarial validation, benchmark-level adaptive overfitting |
| 11 | `llm-evals` | Splits for LLM evals | what contamination is, few-shot examples vs eval items | prompt tuning overfits a fixed eval set | n-gram overlap misses paraphrases, original vs rewritten benchmark gap, near-duplicate tickets | canary strings, tuning an LLM judge on the final eval set |
| 12 | `compare` | Comparing models fairly (same folds, baselines, repeated CV) | DummyClassifier baseline name | dummy baseline under the same CV, same folds for both models, RepeatedStratifiedKFold counts | paired fold differences, leaderboard gaps vs standard error | correlated fold scores (corrected t-test), McNemar on one test set, repeats don't add data, cost vs tiny gains |

## Must-know facts
- Train fits weights, validation picks hyperparameters and models, test is touched once for the final score.
- Every decision made by looking at a set leaks information from it; a set used for decisions is no longer "unseen".
- train_test_split: test size is rounded up (ceil), train gets the rest; random_state fixes the shuffle; shuffle=False takes the last rows as test.
- stratify=y preserves class proportions in each split; it does not rebalance. It needs every class to have at least 2 members, and cannot be combined with shuffle=False.
- The noise in a measured accuracy depends on the count of test examples: SE = sqrt(p(1-p)/n).
- KFold does not shuffle by default; folds are consecutive blocks, first n % k folds get one extra row. random_state with shuffle=False raises ValueError.
- cross_val_score with an integer cv and a classifier uses StratifiedKFold (no shuffle); with a regressor, KFold.
- LOO = k-fold with k = n: n fits, low bias, can be high variance.
- Correlated rows (same user, patient, session) must stay in one fold: GroupKFold / StratifiedGroupKFold.
- Time data: train on the past, test on the future (TimeSeriesSplit; test block = n // (n_splits + 1)); use gap= when labels look ahead.
- GridSearchCV's best_score_ is optimistic; nested CV (inner tune, outer score) estimates the whole tuning procedure.
- Leakage types: target leakage, preprocessing fit on all data, duplicates across splits, future information in features, resampling before splitting.
- A Pipeline inside cross_val_score / GridSearchCV refits every step on training folds only.
- Label-using steps (feature selection, target encoding, oversampling) leak far more than unsupervised scaling.
- Validation and test should come from the distribution you will deploy on.
- LLM benchmarks can be contaminated by pre-training data; n-gram checks miss paraphrases; prompt and judge tuning overfit a fixed eval set too.
- Early stopping is tuning: the validation set that picked the epoch is no longer unbiased.
- train_test_split: an int test_size is a row count, a float is a fraction; with both train_size and test_size set, leftover rows are dropped.
- ShuffleSplit test sets can overlap and some rows are never tested; KFold tests every row once.
- GroupKFold balances folds by row count; GroupShuffleSplit's test_size counts groups. CV splitters that need groups raise if groups= isn't passed to fit.
- Several series (stores, users) in one table: split by a date cutoff across all series, not by row position.
- Compare models on identical folds and look at paired per-fold differences; always include a DummyClassifier/naive baseline.
- CV fold scores are correlated (overlapping training sets), so naive t-tests are overconfident; repeated CV reduces split noise but adds no data.

## Common traps (each one must have at least one question)
- "Tune on test, it's just looking" -> the test score becomes optimistic.
- "test_size=0.25 of 10 rows gives 2 test rows" -> sklearn rounds the test side up to 3.
- "stratify balances the classes" -> it copies the original ratio.
- "stratify works with shuffle=False" -> ValueError.
- "KFold shuffles" -> it doesn't; on sorted labels each fold can be one class.
- "Setting random_state on KFold is harmless" -> ValueError unless shuffle=True.
- "Random row split is fine for per-patient/per-user data" -> the model memorises the person.
- "Shuffled CV is fine for time series" -> the model peeks at the future; scores collapse in a backtest.
- "best_score_ is my expected accuracy" -> it's the max of noisy scores, biased upward.
- "Fitting the scaler on all data is harmless" -> small leak; selection on all data is a big one (noise looks predictive).
- "Oversample, then split" -> copies of the same row land in both sets.
- "Aggregates over a customer's full history are fine" -> they include the future.
- "With n test rows a 2-point gain is real" -> on 100 rows the standard error is about 3 points.
- "The public leaderboard is the test" -> repeated submissions overfit it.
- "Prompt tweaking can't overfit" -> it overfits the eval set like any tuning.
- "n-gram dedup proves no contamination" -> paraphrases slip through.
- "The early-stopping validation loss is my expected loss" -> it chose the epoch, so it is optimistic.
- "test_size=3 means 3%" -> an int is a row count.
- "TimeSeriesSplit sorts by date" -> it uses row order only.
- "TimeSeriesSplit on a table sorted by store is fine" -> 'future' becomes 'later stores'.
- "KFold on a sorted regression target is fine" -> each fold is out of range; R^2 goes negative.
- "A row ID can't leak" -> if rows were assembled by label, the index predicts the label.
- "Teacher-generated training data seeded with eval items is clean" -> paraphrase contamination.
- "A beats B on mean CV score, so A is better" -> check the gap against the spread and use paired comparisons.
- "Repeated CV fixes small data" -> it only averages over split luck.

## Interview angle
- **Why three splits, not two?** Training fits weights, validation absorbs all the choosing, test stays untouched so its number is honest. SDE analogy: dev, staging, prod; you don't debug in prod.
- **What is data leakage and how do you prevent it?** Information the model wouldn't have at prediction time gets into training: target-derived features, preprocessing fit on all data, duplicates, future rows. Prevent with Pipelines, group/time splits, "as of" features, and suspicion of too-good scores.
- **How do you split time-series data?** By time, never shuffled: expanding or sliding window (TimeSeriesSplit / walk-forward), with a gap when labels look ahead.
- **What is nested CV and when do you need it?** Inner loop tunes, outer loop scores the tune-then-fit procedure. Needed when you want an unbiased estimate after heavy tuning on small data.
- **How do you decide model A really beats model B?** Same folds for both, compare paired per-fold differences against their spread, include a dummy baseline, and weigh a tiny gain against latency and cost. On one test set, McNemar's test on the disagreements.
- **How do you trust an LLM benchmark score?** Check contamination (n-gram overlap, canaries, rewritten questions), keep a private held-out set, don't tune prompts or judges on the reporting set.

## Source material
To be added.
