# Classification Metrics (and friends): coverage spec

**Ladder:** L1 · ML Fundamentals › Evaluating Models   ·   **Prerequisites:** ml-splits, ml-overfitting, basic NumPy
**Why it matters for AI/ML:** A metric is the test suite for a model. Picking the wrong one ships a model that "passes" while failing users (99%-accurate fraud models that catch nothing). Retrieval metrics (recall@k, MRR, nDCG) and LLM eval are the daily work of RAG and GenAI engineers.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `confusion-matrix` | The confusion matrix | TP/FP/FN/TN meaning, 4 cells, reading a sklearn matrix | rows = actual, cols = predicted, `ravel()` order, sorted string labels | `labels=` reorders the matrix | — |
| 2 | `core-rates` | Accuracy, precision, recall, specificity | formulas, sensitivity = recall | computing by hand and with sklearn, predict-all-positive, zero_division, accuracy paradox | specificity via `pos_label=0`, which metrics use TN | — |
| 3 | `f-scores` | F1 and F-beta | harmonic mean idea | F1 vs arithmetic mean, beta > 1 favours recall, count formula | F2/F0.5 by hand, F1 ignores TN | F1 depends on the chosen positive class |
| 4 | `thresholds` | Thresholds and the PR trade-off | default 0.5 cut-off | raising threshold: precision up, recall down; recall at two thresholds | recall monotonic, precision not; tune on validation not test; pick threshold for target recall | SVC predict vs predict_proba disagreement |
| 5 | `roc-auc` | ROC curve and AUC | AUC 0.5 = random, TPR vs FPR | AUC as pairwise ranking probability, tiny roc_auc_score | AUC < 0.5 = inverted, invariance to monotonic transforms, passing labels instead of scores | ties count half, AUC says nothing about calibration |
| 6 | `pr-curve` | PR curve and average precision | — | PR random baseline = prevalence | why PR beats ROC under heavy imbalance, AP by hand | AP vs trapezoid area, comparing models with ROC vs PR AUC |
| 7 | `probabilistic` | Log loss and calibration | log loss punishes confident mistakes | log loss by hand, same accuracy different log loss | confident-wrong cost, calibration meaning, Brier score | class weighting distorts probabilities, sigmoid vs isotonic |
| 8 | `multiclass` | Multiclass averaging | — | macro vs micro, micro F1 = accuracy, average=None | macro vs weighted on imbalance, default average='binary' raises | which average for rare critical classes |
| 9 | `regression` | Regression metrics | MAE meaning, RMSE units | MAE/MSE/RMSE by hand, outlier sensitivity, R² = 0 for the mean | negative R², MAPE pitfalls | median vs mean optimum, in-sample R² never drops with features |
| 10 | `ranking` | Ranking and retrieval metrics | precision@k for RAG | precision@k / recall@k by hand, reciprocal rank, MRR | MRR over queries incl. failures, nDCG idea | nDCG by hand, incomplete relevance labels |
| 11 | `choosing` | Choosing a metric, baselines, significance | cost of errors, majority-class baseline | DummyClassifier / DummyRegressor, precision-first scenarios | cost-based threshold, metric vs KPI mismatch, CV mean ± std | standard error of accuracy, McNemar / paired bootstrap, winner's curse |
| 12 | `llm-eval` | LLM evaluation metrics | exact match | BLEU/ROUGE limits, ROUGE recall vs BLEU precision | EM with normalisation, LLM-as-judge biases | validating the judge, golden-set design |

## Must-know facts
- sklearn `confusion_matrix`: rows = actual, columns = predicted, labels sorted; binary `ravel()` gives `tn, fp, fn, tp`.
- Precision = TP/(TP+FP); recall = sensitivity = TPR = TP/(TP+FN); specificity = TN/(TN+FP); FPR = 1 - specificity.
- Precision, recall and F1 never use TN; accuracy, specificity and FPR do.
- F1 = 2PR/(P+R) = 2TP/(2TP+FP+FN); it sits near the smaller of P and R. F-beta with beta > 1 favours recall.
- Raising the threshold never increases recall; precision usually rises but is not monotonic.
- The threshold is a hyperparameter: choose it on validation data, report on test.
- ROC AUC = P(random positive scored above random negative); 0.5 = random; ties count half; invariant to any increasing transform of scores.
- AUC needs scores (`predict_proba[:, 1]` or `decision_function`), not hard labels.
- PR curve random baseline = prevalence; under heavy imbalance PR/AP is far more informative than ROC.
- Log loss punishes confident mistakes heavily (-ln 0.01 = 4.61); calibration = predicted 0.8 means about 80% positive.
- Class weighting / resampling distorts probabilities; recalibrate (sigmoid for small data, isotonic for large).
- Micro F1 = accuracy for single-label multiclass; macro gives rare classes an equal vote; weighted can hide a failed rare class.
- MAE is robust to outliers, MSE/RMSE punish big misses; R² = 0 for predicting the mean and can be negative; MAPE explodes near 0.
- MRR averages 1/rank of the first hit (failed queries count 0); nDCG uses graded relevance with a log2 discount.
- Always compare against a baseline (DummyClassifier/DummyRegressor); a test score has a standard error (~sqrt(p(1-p)/n)).
- BLEU/ROUGE measure n-gram overlap, not meaning; LLM judges have position/length biases and must be validated against humans.

## Common traps (each one must have at least one question)
- High accuracy on imbalanced data -> may equal the always-majority baseline; check minority recall.
- Reading the sklearn confusion matrix as rows = predicted -> rows are actual.
- Assuming string labels keep the order you wrote them -> they are sorted ('ham' before 'spam').
- `labels=[1, 0]` then `ravel()` as tn, fp, fn, tp -> the order is now tp, fn, fp, tn.
- No positive predictions -> precision 0/0; sklearn returns the zero_division value, not an error.
- Predict-everything-positive -> recall 1.0 with poor precision.
- Averaging P and R arithmetically -> hides a terrible one; F1 does not.
- Thinking precision always rises with the threshold -> it can drop.
- Tuning the threshold on the test set -> leaked, inflated score.
- Passing `predict()` labels to `roc_auc_score` -> lower, misleading AUC.
- AUC below 0.5 means "useless" -> it means inverted signal (often swapped labels).
- High AUC means good probabilities -> AUC ignores calibration.
- PR random baseline is 0.5 -> it is the positive rate.
- `f1_score` on multiclass without `average=` -> ValueError.
- R² cannot be negative -> it can, when worse than the mean.
- MAPE with tiny or zero actuals -> explodes / dominated by small rows.
- Dropping failed queries from MRR -> flatters the system.
- Recall@k with incomplete relevance labels -> underestimated.
- Picking the best of many models by test score -> optimistic (winner's curse).
- A 2-point accuracy gain on 200 rows -> inside the noise.

## Interview angle
- **"Precision vs recall: when do you favour each?"** Precision when false alarms are expensive (spam filter hiding client emails), recall when misses are expensive (fraud, cancer screening). Then pick the threshold from the cost ratio on validation data. SDE analogy: precision = "alerts that page you are real", recall = "every outage pages you".
- **"ROC AUC or PR AUC for fraud with 0.1% positives?"** PR AUC / average precision. FPR divides by a huge number of negatives, so thousands of false alarms barely move ROC; precision shows them directly.
- **"What does AUC mean?"** The probability a random positive is scored above a random negative. Ranking only, threshold-free, says nothing about calibration.
- **"How would you evaluate a RAG system?"** Retrieval: recall@k / MRR / nDCG on a labeled set of question -> relevant chunks. Generation: faithfulness and answer correctness via task checks and a validated LLM judge on a golden set, tracked per release like a regression suite.
- **"Model B beats A by 1% accuracy. Ship it?"** Check the standard error and a paired test (McNemar / bootstrap) on the same rows, and check the metric matches the business cost.

## Source material
To be added.
