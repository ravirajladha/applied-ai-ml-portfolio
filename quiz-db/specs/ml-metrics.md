# Classification Metrics (and friends): coverage spec

**Ladder:** L1 · ML Fundamentals › Evaluating Models   ·   **Prerequisites:** ml-splits, ml-overfitting, basic NumPy
**Why it matters for AI/ML:** A metric is the test suite for a model. Picking the wrong one ships a model that "passes" while failing users (99%-accurate fraud models that catch nothing). Retrieval metrics (recall@k, MRR, nDCG) and LLM eval are the daily work of RAG and GenAI engineers.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `confusion-matrix` | The confusion matrix | TP/FP/FN/TN meaning, 4 cells, reading a sklearn matrix | rows = actual, cols = predicted, `ravel()` order, sorted string labels, reading a 3x3 matrix | `labels=` reorders the matrix, `normalize='true'` = per-class recall, `multilabel_confusion_matrix` | — |
| 2 | `core-rates` | Accuracy, precision, recall, specificity | formulas, sensitivity = recall, precision as 'real pages / all pages' | computing by hand and with sklearn, predict-all-positive, zero_division, accuracy paradox | specificity via `pos_label=0`, which metrics use TN, base-rate PPV for screening tests | precision shifts with prevalence when moving populations; recall/FPR don't |
| 3 | `f-scores` | F1 and F-beta | harmonic mean idea | F1 vs arithmetic mean, beta > 1 favours recall, count formula | F2/F0.5 by hand, F1 ignores TN | F1 depends on the chosen positive class, averaged-per-batch F1 != pooled F1, F1-optimal threshold = F1*/2 |
| 4 | `thresholds` | Thresholds and the PR trade-off | default 0.5 cut-off | raising threshold: precision up, recall down; recall at two thresholds; lowering it for screening | recall monotonic, precision not (by code); tune on validation not test; pick threshold for target recall; review budget (precision@k); TunedThresholdClassifierCV; LR decision_function 0 = proba 0.5 | SVC predict vs predict_proba disagreement |
| 5 | `roc-auc` | ROC curve and AUC | AUC 0.5 = random, AUC 1.0 = perfect ranking, TPR vs FPR | AUC as pairwise ranking probability, tiny roc_auc_score | AUC < 0.5 = inverted, invariance to monotonic transforms, passing labels instead of scores, roc_curve points, multiclass `multi_class='ovr'`, Gini = 2AUC - 1 | ties count half, AUC = Mann-Whitney U, crossing curves and partial AUC, AUC says nothing about calibration |
| 6 | `pr-curve` | PR curve and average precision | — | PR random baseline = prevalence, reading an operating point from a PR table | why PR beats ROC under heavy imbalance, AP by hand, random AP = prevalence (simulation) | AP vs trapezoid area, comparing models with ROC vs PR AUC, PR AUC not comparable across prevalences |
| 7 | `probabilistic` | Log loss and calibration | log loss punishes confident mistakes | log loss by hand, same accuracy different log loss | confident-wrong cost, calibration meaning, Brier score (bounded) vs log loss, calibration_curve by hand, Platt keeps AUC | class weighting distorts probabilities, sigmoid vs isotonic, ECE by hand, temperature scaling keeps accuracy |
| 8 | `multiclass` | Multiclass averaging | — | macro vs micro, micro F1 = accuracy, average=None | macro vs weighted on imbalance, default average='binary' raises, macro precision with a never-predicted class, top-k accuracy | which average for rare critical classes |
| 9 | `regression` | Regression metrics | MAE meaning, RMSE units, regression needs regression metrics | MAE/MSE/RMSE by hand, outlier sensitivity, R² = 0 for the mean, R² is not '% within' | negative R², MAPE pitfalls, median absolute error, MSLE punishes under-prediction | median vs mean optimum, in-sample R² never drops with features, R² not comparable across datasets, pinball (quantile) loss |
| 10 | `ranking` | Ranking and retrieval metrics | precision@k for RAG | precision@k / recall@k by hand, reciprocal rank, MRR | MRR over queries incl. failures, nDCG idea, hit rate@k, recall@20 vs recall@5 (reranking) | nDCG by hand, incomplete relevance labels, MAP vs MRR |
| 11 | `choosing` | Choosing a metric, baselines, significance | cost of errors, majority-class baseline | DummyClassifier / DummyRegressor, precision-first scenarios | cost-based threshold, comparing models by expected cost, metric vs KPI mismatch, slice-based evaluation, CV mean ± std | standard error of accuracy, McNemar by hand, paired bootstrap by code, winner's curse |
| 12 | `llm-eval` | LLM evaluation metrics | exact match | BLEU/ROUGE limits, ROUGE recall vs BLEU precision | EM with normalisation, token F1, RAG faithfulness vs relevance, LLM-as-judge biases | validating the judge, golden-set design, pass@k estimator, perplexity across tokenizers |
| 13 | `balanced-metrics` | Balanced accuracy, MCC and Cohen's kappa | — | balanced accuracy = mean per-class recall, always-majority = 0.5 | MCC = 0 for a constant model, why MCC over F1, MCC symmetric to class swap, kappa for judge-vs-human agreement | F1 vs MCC by hand when positives are the majority, kappa paradox under skewed labels |

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
- Precision (PPV) depends on prevalence: a 99%/99% test on a 0.1% disease gives about 9% precision. Recall, specificity and FPR don't depend on prevalence.
- Balanced accuracy = mean per-class recall (0.5 = no skill); MCC uses all four cells (0 = no skill) and doesn't change when classes are swapped; Cohen's kappa removes chance agreement.
- F1 is not additive: F1 averaged over batches or folds differs from F1 on the pooled rows.
- Temperature scaling and Platt scaling are monotonic: they fix calibration without changing ranking (AUC) or argmax accuracy.
- pass@k uses the unbiased estimator 1 - C(n-c, k) / C(n, k); perplexity is only comparable with the same tokenizer.

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
- Moving a model to a population with different prevalence and quoting the old precision -> precision changes; recall and FPR don't.
- Averaging F1 over batches/folds and calling it 'the F1' -> differs from pooled F1.
- High raw agreement between an LLM judge and humans means the judge is good -> with skewed labels chance agreement is huge; use kappa and per-class agreement.
- Comparing perplexity across models with different tokenizers -> not the same unit.
- Comparing R² or PR AUC across different datasets -> both depend on the data (target variance, prevalence).
- A great overall metric means every user group is served -> check slices.

## Interview angle
- **"Precision vs recall: when do you favour each?"** Precision when false alarms are expensive (spam filter hiding client emails), recall when misses are expensive (fraud, cancer screening). Then pick the threshold from the cost ratio on validation data. SDE analogy: precision = "alerts that page you are real", recall = "every outage pages you".
- **"ROC AUC or PR AUC for fraud with 0.1% positives?"** PR AUC / average precision. FPR divides by a huge number of negatives, so thousands of false alarms barely move ROC; precision shows them directly.
- **"What does AUC mean?"** The probability a random positive is scored above a random negative. Ranking only, threshold-free, says nothing about calibration.
- **"How would you evaluate a RAG system?"** Retrieval: recall@k / MRR / nDCG on a labeled set of question -> relevant chunks. Generation: faithfulness and answer correctness via task checks and a validated LLM judge on a golden set, tracked per release like a regression suite.
- **"Model B beats A by 1% accuracy. Ship it?"** Check the standard error and a paired test (McNemar / bootstrap) on the same rows, and check the metric matches the business cost.
- **"Your LLM judge agrees with humans 95% of the time. Good enough?"** Not by itself. Check Cohen's kappa and the judge's recall on the rare 'bad' label; with 94% 'good' answers, chance agreement alone is about 90%. SDE analogy: a test that passes 95% of builds when 94% of builds are fine has barely been tested on the bad ones.

## Source material
To be added.
