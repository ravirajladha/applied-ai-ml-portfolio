# Classic Models: coverage spec

**Ladder:** L1 · ML Fundamentals › Evaluating Models   ·   **Prerequisites:** ml-splits, ml-overfitting, ml-metrics, basic NumPy
**Why it matters for AI/ML:** Classic models are still what most production tabular systems run (fraud, churn, pricing), the baselines every LLM or deep model must beat, and a staple of ML interviews. The scikit-learn API (fit / predict / transform / Pipeline) is the shared vocabulary of the whole Python ML stack.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `linear-regression` | Linear regression | slope/intercept, coefficient meaning, OLS = least squares, one coef per column | predict output, coefficients depend on units, polynomial terms incl. interactions | OLS assumptions, residual funnel (heteroscedasticity), multicollinearity, high-degree overfitting | Ridge vs Lasso behaviour, Ridge splits / Lasso picks among duplicates |
| 2 | `logistic-regression` | Logistic regression | sigmoid, predict_proba shape | linear decision boundary, log-odds, e^coef as odds ratio, coefficient sign, custom threshold, sorted classes_ order | C is inverse regularisation, L2 on by default, decision_function = log-odds, boundary at -b/w, multiclass softmax coef_ shape | separable data -> weights diverge, why LR is roughly calibrated (proper scoring rule) |
| 3 | `knn` | k-Nearest Neighbours | voting with different k, lazy learner, vote-share probabilities | k=1 memorises, scaling matters, kNN regression averages (no extrapolation) | unscaled distance example, k vs bias/variance, distance weighting and ties | curse of dimensionality, embeddings, weighting one-hot blocks vs numeric features |
| 4 | `trees` | Decision trees | Gini/entropy of a 50/50 node, purity-based splits, no scaling needed | unlimited depth memorises noise, max_depth and leaves, regression trees (variance, leaf mean), importances | trees can't extrapolate, weighted Gini decrease, axis-aligned staircase, instability | impurity importance favours high-cardinality features, greedy splitting misses XOR-like interactions |
| 5 | `ensembles` | Random forests and gradient boosting | forest = many voting trees, bagging vs boosting, estimators_ | bagging, staged boosting by hand, learning_rate vs n_estimators, boosting is sequential | more trees don't overfit a forest, feature randomness, XGBoost/LightGBM, soft vs hard voting | out-of-bag score, deep vs shallow trees, 'gradient' = fitting the loss gradient, HGB early_stopping='auto', leaf-wise growth |
| 6 | `svm` | Support vector machines | maximum margin, support vectors | support vectors in a tiny fit, meaning of C, decision_function sign | RBF kernel and gamma (memorising), scaling, no predict_proba by default, LinearSVC, one-vs-one multiclass | scaling cost with n, margin = 2/norm(w), hinge vs log loss |
| 7 | `naive-bayes` | Naive Bayes | the independence assumption, the prior | tiny text classifier, Laplace smoothing by hand | zero-count problem and smoothing, poor calibration, log-probabilities vs underflow, negative inputs rejected | Multinomial vs Bernoulli vs Gaussian, duplicated features -> over-confidence, ComplementNB for imbalance |
| 8 | `kmeans` | k-means clustering | unsupervised, centres and inertia, assign/update loop, cluster_centers_ | elbow method, k-means++ and n_init, predict on new points | scaling (unscaled example), silhouette to pick k, MiniBatchKMeans | non-convex / unequal clusters (moons vs DBSCAN), Gaussian mixtures |
| 9 | `pca` | PCA | what it is for | variance explained on correlated data, standardise first, cumulative variance | n_components as a fraction, fit inside the split, centres but doesn't scale, inverse_transform, PCA vs t-SNE/UMAP for plots | variance is not predictive power (code demo), TruncatedSVD for sparse TF-IDF |
| 10 | `choosing` | Choosing a model | tabular -> gradient boosting, simple baseline first | text baseline, latency constraints, clustering unlabelled tickets, classic model vs LLM call | no free lunch, bias vs variance by model, interactions favour trees | small gain vs cost of complexity, monotonic constraints |
| 11 | `interpretability` | Interpretability | shallow trees are readable | raw coefficients mislead, SHAP idea, export_text rules, local vs global explanations | permutation importance (code), raw vs standardised coefficients | correlated features, importance is not causation, flat PDP hiding opposite effects, one-hot baseline category |
| 12 | `sklearn-api` | The scikit-learn API | fit, 2D X, 1D-X error, default hyperparameters | scaler fit/transform, estimator vs transformer, NotFittedError, make_pipeline names | Pipeline prevents leakage, fit_transform on test bug, step__param | clone and GridSearchCV refit, trailing-underscore attributes, no logic in a custom estimator's __init__ |

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
- predict uses a 0.5 cut-off on predict_proba; pick the threshold from business costs. predict_proba columns follow the sorted classes_.
- Logistic regression's decision_function is the log-odds w.x + b; SVC's decision_function is a signed distance, and SVC has no predict_proba unless probability=True.
- Linear SVM margin = 2 / ||w||; hinge loss is zero beyond the margin, so only support vectors shape the boundary.
- Gradient boosting fits each tree to the negative gradient of the loss; forests use deep trees, boosting shallow ones.
- Naive Bayes sums log-probabilities to avoid underflow; repeated or correlated features are double-counted, which inflates confidence.
- Silhouette (unlike inertia) peaks at a sensible k; k-means cuts space with straight boundaries, so curved clusters need DBSCAN or mixtures.
- PCA centres but does not scale; sparse TF-IDF is reduced with TruncatedSVD (LSA).

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
- Assuming predict_proba column 0 is the first label you saw -> columns follow the sorted classes_.
- Treating the default 0.5 threshold as fixed -> move it to trade precision against recall.
- Calling predict_proba on a default SVC -> AttributeError; use decision_function or probability=True.
- Huge RBF gamma -> each point gets its own bubble and the SVM memorises noise.
- Putting StandardScaler (negative values) before MultinomialNB -> ValueError.
- Feeding Naive Bayes duplicated or correlated features -> over-confident probabilities.
- Reading 'Lasso dropped this feature' as 'useless' -> among correlated features the pick is arbitrary.
- Assuming a linear model finds interactions (discount only on weekends) -> add the product term or use trees.
- A flat partial dependence plot means 'no effect' -> opposite effects in subgroups can cancel.
- Putting logic in a custom estimator's __init__ -> breaks clone/get_params and grid search.
- Centring a sparse TF-IDF matrix for PCA -> it becomes dense; use TruncatedSVD.
- Scaling then assuming kNN distances are 'fair' -> the weight of each column group (e.g. one-hot blocks) is still a choice.

## Interview angle
- **"Random forest vs gradient boosting?"** Forest: many deep trees in parallel on bootstrap samples with random features, averaged, reduces variance, hard to overfit by adding trees. Boosting: shallow trees in sequence, each fitting the remaining errors, reduces bias, needs learning rate + early stopping. SDE analogy: forest = N independent replicas voting; boosting = a chain of patches, each fixing what the previous release broke.
- **"Explain logistic regression in one minute."** A weighted sum of features turned into a probability by a sigmoid. It models log-odds linearly, so the boundary is a hyperplane and each coefficient multiplies the odds by e^w. Regularised by C (inverse strength).
- **"Why scale features, and for which models?"** Distance- and gradient-based models (kNN, SVM, k-means, linear models with regularisation, neural nets) because large-range features dominate. Not trees. Do it inside a Pipeline to avoid leakage.
- **"What would you try first on a tabular problem?"** A dummy baseline, then logistic/linear regression, then LightGBM/XGBoost with early stopping, compared with the same CV and the business metric; explain with SHAP / permutation importance.
- **"How do you explain a black-box model's prediction?"** SHAP for per-row contributions, permutation importance for global reliance, with caveats on correlated features and that importance is not causation.
- **"When would you use a classic model instead of calling an LLM?"** Structured, tabular, high-volume predictions (churn, fraud, pricing): a boosted tree scores a row in microseconds, costs nothing per call and is easy to evaluate. Use LLMs for unstructured text, and feed LLM-extracted features into classic models when it helps.

## Source material
To be added.
