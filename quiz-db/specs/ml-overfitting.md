# Overfitting & Underfitting: coverage spec

**Ladder:** L1 · ML Fundamentals › Evaluating Models   ·   **Prerequisites:** ml-splits (train / validation / test), ml-data
**Why it matters for AI/ML:** Every model, from a decision tree to a fine-tuned LLM, sits somewhere between "too simple" and "memorising". Reading train vs validation curves and picking the right fix (more data, regularisation, smaller model, early stopping) is the daily job of model building and a staple interview question.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `symptoms` | Spotting under- and overfitting | definitions, low/low = underfit, train/val gap | unlimited tree scores 1.0 on train, reading loss pairs | val loss below train loss (dropout), small gap but bad prod = not overfitting | — |
| 2 | `curves` | Learning curves, validation curves, CV | learning curve vs validation curve | reading high-variance vs high-bias learning curves, CV to measure the gap | learning_curve sizes and shapes, validation_curve train scores vs depth | one-standard-error rule |
| 3 | `bias-variance` | Bias-variance trade-off | bias vs variance, underfit ~ bias, overfit ~ variance | bias^2 + variance + noise arithmetic, irreducible error | simulating bias and variance of polynomials | why cross terms vanish, no clean decomposition for 0-1 loss |
| 4 | `capacity` | Model capacity | what capacity means | polynomial through every point, which tree settings add capacity, kNN k=1 | kNN train vs test by k, parameter count vs effective capacity | — |
| 5 | `regularisation` | L1 / L2 regularisation | what it does, L1 vs L2 penalty values and sparsity | Lasso zeros vs Ridge shrinks, C vs alpha direction, alpha sweep | C sweep on LogisticRegression, scale features first, correlated features, ElasticNet | Gaussian/Laplace priors, AdamW vs L2, intercept not penalised |
| 6 | `nn-regularisers` | Dropout, early stopping, augmentation | what each one is | dropout off in eval(), patience logic, no augmentation on val/test | inverted dropout scaling, label-changing augmentation | dropout as an implicit ensemble, early stopping ~ L2 |
| 7 | `data-ensembles` | More data and ensembling | more data helps variance, what bagging is | bagging cuts variance, boosting cuts bias, more trees don't overfit | tree vs forest test score, boosting rounds can overfit | variance of correlated averages (rho term) |
| 8 | `double-descent` | Double descent and big networks | — | — | double descent curve, nets fit random labels, "more params than rows" myth | why the peak is at p = n, min-norm simulation, implicit regularisation, grokking |
| 9 | `llm-finetune` | Overfitting in LLM fine-tuning | rising eval loss, pick the best checkpoint | perplexity near 1 on train, what reduces overfitting, verbatim regurgitation | catastrophic forgetting vs overfitting, deduplication | in-distribution eval loss vs real quality, high-rank LoRA still memorises |

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

## Interview angle
- **How do you tell overfitting from underfitting?** Compare training and validation error: big gap = overfit (variance), both high = underfit (bias). Confirm with a learning curve. SDE analogy: overfitting = tests with hard-coded expected values.
- **Explain the bias-variance trade-off.** Error = bias^2 + variance + noise. Simple models are consistently off (bias); flexible models swing with the training sample (variance). Tune capacity and regularisation on validation to minimise the sum.
- **L1 vs L2?** Both penalise weight size. L1's corner at zero gives sparse models (feature selection); L2 shrinks smoothly and spreads weight across correlated features. In sklearn, alpha up or C down = stronger.
- **How do you reduce overfitting in a neural net?** More/augmented data, weight decay, dropout, early stopping on validation loss, a smaller model, ensembling.
- **Why do huge networks generalise despite having more parameters than data?** Implicit regularisation of SGD and architecture pick smooth solutions among many zero-error ones; double descent shows error can fall again past the interpolation threshold.

## Source material
To be added.
