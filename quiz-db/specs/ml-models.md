# Classic Models: coverage spec

**Ladder:** L1 · ML Fundamentals › Evaluating Models   ·   **Prerequisites:** ml-splits, ml-overfitting, ml-metrics, basic NumPy
**Why it matters for AI/ML:** Classic models are still what most production tabular systems run (fraud, churn, pricing), the baselines every LLM or deep model must beat, and a staple of ML interviews. The scikit-learn API (fit / predict / transform / Pipeline) is the shared vocabulary of the whole Python ML stack.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `linear-regression` | Linear regression | slope/intercept, coefficient meaning, OLS = least squares | predict output, coefficients depend on units | OLS assumptions, multicollinearity, polynomial features | Ridge vs Lasso behaviour |
| 2 | `logistic-regression` | Logistic regression | sigmoid, predict_proba shape | linear decision boundary, log-odds, e^coef as odds ratio | C is inverse regularisation, L2 on by default | separable data -> weights diverge |
| 3 | `knn` | k-Nearest Neighbours | voting with different k, lazy learner | k=1 memorises, scaling matters | unscaled distance example, k vs bias/variance | curse of dimensionality, embeddings |
| 4 | `trees` | Decision trees | Gini/entropy of a 50/50 node, purity-based splits, no scaling needed | unlimited depth memorises noise, max_depth and leaves | trees can't extrapolate | impurity importance favours high-cardinality features |
| 5 | `ensembles` | Random forests and gradient boosting | forest = many voting trees, bagging vs boosting | bagging, staged boosting by hand, learning_rate vs n_estimators | more trees don't overfit a forest, feature randomness, XGBoost/LightGBM | out-of-bag score |
| 6 | `svm` | Support vector machines | maximum margin, support vectors | support vectors in a tiny fit, meaning of C | RBF kernel and gamma, scaling | scaling cost with n |
| 7 | `naive-bayes` | Naive Bayes | the independence assumption | tiny text classifier | zero-count problem and smoothing, poor calibration | Multinomial vs Bernoulli vs Gaussian |
| 8 | `kmeans` | k-means clustering | unsupervised, centres and inertia | elbow method, k-means++ and n_init | scaling | non-convex / unequal clusters |
| 9 | `pca` | PCA | what it is for | variance explained on correlated data, standardise first | n_components as a fraction, fit inside the split | variance is not predictive power |
| 10 | `choosing` | Choosing a model | tabular -> gradient boosting, simple baseline first | text baseline, latency constraints | no free lunch, bias vs variance by model | small gain vs cost of complexity |
| 11 | `interpretability` | Interpretability | shallow trees are readable | raw coefficients mislead, SHAP idea | permutation importance | correlated features, importance is not causation |
| 12 | `sklearn-api` | The scikit-learn API | fit, 2D X, 1D-X error | scaler fit/transform, estimator vs transformer, NotFittedError, make_pipeline names | Pipeline prevents leakage, fit_transform on test bug, step__param | clone and GridSearchCV refit, trailing-underscore attributes |

## Must-know facts
- Linear regression: y = w.x + b fitted by least squares; a coefficient is the change in y per unit of x holding others fixed, and it scales with the units of x.
- OLS assumptions concern the errors (independent, constant variance, normal for inference), not the feature distributions.
- "Linear" means linear in the weights; polynomial features let it fit curves.
- Lasso (L1) zeroes coefficients; Ridge (L2) shrinks them.
- Logistic regression: sigmoid(w.x + b) = P(class 1); it models log-odds linearly, so the boundary is a hyperplane and e^coef is an odds multiplier.
- sklearn LogisticRegression uses L2 with C = 1.0 by default; C is the INVERSE of regularisation strength (same for SVC).
- kNN stores the data; prediction cost grows with the training set; k = 1 memorises; scale features first.
- Trees split to maximise impurity decrease (Gini/entropy), need no scaling, overfit without depth limits, and can't extrapolate.
- Random forest = bagging + random feature subsets per split; more trees don't cause overfitting; OOB score is a free validation estimate.
- Gradient boosting adds shallow trees fitted to residuals, scaled by learning_rate; smaller learning rate needs more trees; use early stopping.
- SVM maximises the margin; only support vectors matter; RBF kernel + gamma give non-linear boundaries; kernel SVMs scale badly with n.
- Naive Bayes assumes conditional independence; smoothing (alpha) avoids zero probabilities; strong for text, over-confident probabilities.
- k-means: unsupervised, inertia always drops as k grows (use the elbow / silhouette), k-means++ and n_init avoid bad starts, assumes round clusters.
- PCA: components ordered by explained variance; standardise first; it ignores labels.
- Tabular data: gradient-boosted trees usually win; always start from a simple baseline.
- sklearn: X is 2D (n_samples, n_features); fit learns, transform/predict apply; learned attributes end in `_`; Pipelines refit preprocessing inside each CV fold.

## Common traps (each one must have at least one question)
- Comparing raw coefficients to judge importance -> they depend on units.
- Thinking features must be normally distributed for OLS -> the assumptions are about residuals.
- "Linear regression can't fit curves" -> add polynomial features.
- Treating C like alpha -> larger C means LESS regularisation.
- Forgetting sklearn's LogisticRegression is regularised by default -> coefficients differ from statsmodels.
- Reading a logistic coefficient as a change in probability -> it is a change in log-odds.
- Running kNN, SVM or k-means on unscaled features -> the largest-range feature dominates.
- Scaling features for trees -> pointless; splits are threshold-based.
- Unlimited-depth tree with 100% training accuracy -> memorised noise.
- Expecting trees/forests to extrapolate -> predictions go flat outside the training range.
- Trusting impurity feature importance for high-cardinality columns -> biased; use permutation importance.
- "More trees make a random forest overfit" -> they don't (boosting can).
- Lowering learning_rate without adding trees -> underfits.
- Naive Bayes with zero counts -> probability 0 without smoothing.
- Choosing k by minimising inertia -> always picks k = n.
- Fitting PCA or a scaler on the full dataset before splitting -> leakage.
- Assuming PCA keeps the predictive signal -> it keeps variance, not label information.
- Passing a 1D array to fit -> ValueError; reshape(-1, 1).
- Predicting before fit -> NotFittedError.
- fit_transform on the test set -> must be transform with train statistics.
- Reading importance/SHAP as causal -> it describes the model, and proxies can encode bias.

## Interview angle
- **"Random forest vs gradient boosting?"** Forest: many deep trees in parallel on bootstrap samples with random features, averaged, reduces variance, hard to overfit by adding trees. Boosting: shallow trees in sequence, each fitting the remaining errors, reduces bias, needs learning rate + early stopping. SDE analogy: forest = N independent replicas voting; boosting = a chain of patches, each fixing what the previous release broke.
- **"Explain logistic regression in one minute."** A weighted sum of features turned into a probability by a sigmoid. It models log-odds linearly, so the boundary is a hyperplane and each coefficient multiplies the odds by e^w. Regularised by C (inverse strength).
- **"Why scale features, and for which models?"** Distance- and gradient-based models (kNN, SVM, k-means, linear models with regularisation, neural nets) because large-range features dominate. Not trees. Do it inside a Pipeline to avoid leakage.
- **"What would you try first on a tabular problem?"** A dummy baseline, then logistic/linear regression, then LightGBM/XGBoost with early stopping, compared with the same CV and the business metric; explain with SHAP / permutation importance.
- **"How do you explain a black-box model's prediction?"** SHAP for per-row contributions, permutation importance for global reliance, with caveats on correlated features and that importance is not causation.

## Source material
To be added.
