# Overfitting & Underfitting: coverage spec

**Ladder:** L1 · ML Fundamentals › Evaluating Models   ·   **Prerequisites:** ml-splits (train / validation / test), ml-data
**Why it matters for AI/ML:** Every model, from a decision tree to a fine-tuned LLM, sits somewhere between "too simple" and "memorising". Reading train vs validation curves and picking the right fix (more data, regularisation, smaller model, early stopping) is the daily job of model building and a staple interview question.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `symptoms` | Spotting under- and overfitting | definitions, low/low = underfit, train/val gap | unlimited tree scores 1.0 on train, reading loss pairs, 100% train alone is not proof | val loss below train loss (dropout), huge permanent reverse gap = leakage, small gap but bad prod = not overfitting | val loss up while val accuracy up (over-confidence) |
| 2 | `curves` | Learning curves, validation curves, CV | learning curve vs validation curve | reading high-variance vs high-bias learning curves, CV to measure the gap, train score falls with size | learning_curve sizes and shapes, validation_curve over depth and k, cross_validate train vs test, fold-variance bands | one-standard-error rule (by hand, SE = std / sqrt(k)) |
| 3 | `bias-variance` | Bias-variance trade-off | bias vs variance, underfit ~ bias, overfit ~ variance | bias^2 + variance + noise arithmetic, irreducible error, bias^2 and variance from predictions, regularisation moves bias up | simulating bias and variance of polynomials, more rows don't cut noise, more data cuts variance not bias | why cross terms vanish, no clean decomposition for 0-1 loss, kNN error sigma^2 + bias^2 + sigma^2/k |
| 4 | `capacity` | Model capacity | what capacity means, ranking simple vs flexible models | polynomial through every point, which tree settings add capacity, kNN k=1, leaf counts | kNN train vs test by k, parameter count vs effective capacity, PolynomialFeatures term count | VC dimension of a linear classifier |
| 5 | `regularisation` | L1 / L2 regularisation | what it does, L1 vs L2 penalty values and sparsity | Lasso zeros vs Ridge shrinks, C vs alpha direction, alpha sweep, never pick alpha on training score | C sweep on LogisticRegression, LogisticRegression is L2 by default, scale features first (units demo), correlated features, ElasticNet, Lasso path, diamond vs circle picture | Gaussian/Laplace priors, soft-thresholding vs shrinking, AdamW vs L2, no decay on biases/LayerNorm, intercept not penalised |
| 6 | `nn-regularisers` | Dropout, early stopping, augmentation | what each one is, early stopping watches validation | dropout off in eval(), patience logic, no augmentation on val/test, weight_decay argument | inverted dropout scaling, train vs eval determinism, BatchNorm in eval, min_delta, label smoothing, mixup, label-changing augmentation | dropout as an implicit ensemble, early stopping ~ L2, little dropout in LLM pre-training |
| 7 | `data-ensembles` | More data and ensembling | more data helps variance, what bagging is | bagging cuts variance, boosting cuts bias, more trees don't overfit, duplicated rows are not new data | tree vs forest test score, boosting rounds can overfit (staged_predict), 63.2% bootstrap, OOB score | variance of correlated averages (rho term), max_features decorrelates, stacking needs out-of-fold predictions, bagging stumps barely helps |
| 8 | `double-descent` | Double descent and big networks | — | — | double descent curve, nets fit random labels, "more params than rows" myth, pinv picks the min-norm solution | why the peak is at p = n, min-norm simulation, implicit regularisation, grokking, sample-wise and epoch-wise double descent, tuned ridge flattens the peak |
| 9 | `llm-finetune` | Overfitting in LLM fine-tuning | rising eval loss, pick the best checkpoint, falling train loss alone proves nothing | perplexity near 1 on train, what reduces overfitting, verbatim regurgitation, 1-3 epochs | catastrophic forgetting vs overfitting, deduplication, LoRA parameter count, benchmark contamination | in-distribution eval loss vs real quality, eval loss up but task metric up, high-rank LoRA still memorises |
| 10 | `val-overfit` | Overfitting the validation set | — | what it means, public vs private leaderboard shake-up | best of many random models on a small val set, GridSearchCV best_score_ is optimistic | nested CV, reusing one eval set for hundreds of variants |

## Must-know facts
- Overfitting: low training error, much higher validation error (high variance). Underfitting: both errors high and close (high bias).
- A small train/val gap is not "good" on its own; both could be bad, or validation could be unrepresentative.
- Learning curve = score vs training-set size; validation curve = score vs one hyperparameter.
- Gap that closes with more data -> more data helps. Curves that meet low -> more data won't help; add capacity or features.
- Expected squared error = bias^2 + variance + irreducible noise.
- An unrestricted decision tree, or kNN with k = 1, scores 1.0 on (distinct) training data.
- L1 (Lasso) drives some weights exactly to zero; L2 (Ridge) shrinks all weights but keeps them non-zero.
- sklearn direction: Ridge/Lasso alpha bigger = stronger; LogisticRegression/SVC C smaller = stronger (C = 1/lambda).
- Scale features before penalised models; the intercept is not penalised.
- Dropout is active only in train mode; PyTorch scales kept units by 1/(1-p). Forgetting model.eval() is a classic bug.
- Early stopping keeps the best validation checkpoint; patience counts epochs without improvement.
- Augmentation must preserve the label and applies to training data only.
- Bagging / random forests reduce variance; boosting reduces bias; more forest trees don't overfit, more boosting rounds can.
- Averaging B models with correlation rho leaves variance rho*s^2 + (1-rho)*s^2/B.
- Double descent: test error peaks at the interpolation threshold (params ~ samples) and can fall again beyond it.
- sklearn LogisticRegression is L2-regularised by default (C=1.0). Hyperparameters like alpha are chosen on validation/CV, never on the training score.
- Bootstrap samples hold about 63.2% of distinct rows; the out-of-bag rows give a free validation score.
- Tuning against the same validation set many times overfits it; GridSearchCV best_score_ is optimistic; nested CV or an untouched test set gives an honest number.
- For LLM fine-tuning: falling train loss with rising eval loss = memorising; keep the best checkpoint, fewer epochs, lower LR, LoRA, dedup.

## Common traps (each one must have at least one question)
- "Small gap = good model" -> could be underfitting.
- "Val loss below train loss means a bug" -> dropout/augmentation make training harder; small reverse gaps are normal.
- "Bad production score = overfitting" -> if train ~ val, suspect leakage or shift.
- "More data fixes underfitting" -> flat, converged learning curves won't move.
- "Bigger C means more regularisation" -> it means less (opposite of alpha).
- "Ridge zeros out useless features" -> only Lasso (L1) does.
- "Regularisation works fine without scaling" -> penalty depends on units.
- "Dropout still runs at inference" -> off after model.eval(); kept units are scaled during training instead.
- "Augment the test set too" -> training only (TTA is a separate, deliberate trick).
- "Any augmentation helps" -> a 180-degree rotation turns a 6 into a 9.
- "More trees make a random forest overfit" -> no; more boosting rounds can.
- "Bias-variance splits neatly for classification accuracy" -> only for squared loss.
- "More parameters than examples = overfitting" -> not for deep nets; measure.
- "A polynomial through every point is perfect" -> zero training error says nothing about new points.
- "Frozen base + LoRA can't overfit" -> a large adapter can memorise a small dataset.
- "Low eval loss on my fine-tuning split = better product" -> needs task-level evals on real prompts; watch for catastrophic forgetting.
- "Validation loss rising means validation accuracy must be falling" -> over-confidence can raise loss while accuracy still improves.
- "sklearn LogisticRegression() is unregularised" -> default is L2 with C=1.0.
- "Pick alpha by the training score" -> the weakest penalty always wins on training data.
- "Duplicating rows = more data" -> copies add no information, they act like extra epochs.
- "Bagging fixes any weak model" -> bagging cuts variance; high-bias stumps barely improve.
- "Stack on in-sample predictions" -> overfit base models look perfect; use out-of-fold predictions.
- "GridSearchCV best_score_ is an unbiased estimate" -> the max of many noisy scores is optimistic; use nested CV.
- "An eval set never used for training can't be overfit" -> hundreds of decisions made by looking at it fit its noise.

## Interview angle
- **How do you tell overfitting from underfitting?** Compare training and validation error: big gap = overfit (variance), both high = underfit (bias). Confirm with a learning curve. SDE analogy: overfitting = tests with hard-coded expected values.
- **Explain the bias-variance trade-off.** Error = bias^2 + variance + noise. Simple models are consistently off (bias); flexible models swing with the training sample (variance). Tune capacity and regularisation on validation to minimise the sum.
- **L1 vs L2?** Both penalise weight size. L1's corner at zero gives sparse models (feature selection); L2 shrinks smoothly and spreads weight across correlated features. In sklearn, alpha up or C down = stronger.
- **How do you reduce overfitting in a neural net?** More/augmented data, weight decay, dropout, early stopping on validation loss, a smaller model, ensembling.
- **Why do huge networks generalise despite having more parameters than data?** Implicit regularisation of SGD and architecture pick smooth solutions among many zero-error ones; double descent shows error can fall again past the interpolation threshold.
- **Your validation score kept climbing over months of tuning. Do you trust it?** No: every decision made by looking at it fits its noise. Confirm once on a fresh holdout (or nested CV) and report an interval. SDE analogy: a test suite you have tuned against is no longer a blind test.

## Source material
To be added.
