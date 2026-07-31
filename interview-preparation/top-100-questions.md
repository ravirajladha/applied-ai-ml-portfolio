# Top 100 AI/ML Interview Questions — with brief theory

Compiled from the questions that repeat most often in AI/ML interviews at service and product companies
(fresher + early-career rounds). Each answer starts with a **one-line definition you can say out loud**,
followed by 2–4 lines of depth for the inevitable follow-up.

⭐ = very high frequency. If you are short on time, do all the ⭐ ones first.

**Contents**

| # | Section |
|---|---------|
| 1–12 | [AI/ML fundamentals](#1-aiml-fundamentals) |
| 13–20 | [Statistics & probability](#2-statistics--probability) |
| 21–31 | [Data preprocessing & feature engineering](#3-data-preprocessing--feature-engineering) |
| 32–45 | [Supervised learning algorithms](#4-supervised-learning-algorithms) |
| 46–57 | [Model evaluation & tuning](#5-model-evaluation--tuning) |
| 58–64 | [Unsupervised learning & dimensionality reduction](#6-unsupervised-learning--dimensionality-reduction) |
| 65–76 | [Deep learning](#7-deep-learning) |
| 77–83 | [Natural Language Processing](#8-natural-language-processing) |
| 84–91 | [Transformers, LLMs & Generative AI](#9-transformers-llms--generative-ai) |
| 92–94 | [Reinforcement learning](#10-reinforcement-learning) |
| 95–100 | [MLOps, deployment & responsible AI](#11-mlops-deployment--responsible-ai) |

---

## 1. AI/ML fundamentals

**Q1. What is Artificial Intelligence?** ⭐
AI is the field of building systems that perform tasks which normally need human intelligence — understanding
language, recognising images, planning, deciding.
It is the umbrella term. Traditional AI includes rule-based/expert systems and search algorithms; modern AI is
mostly learning-based. Think of AI as the goal, ML as one way of reaching it.

**Q2. What is Machine Learning?** ⭐
ML is a subset of AI where a system learns patterns from data instead of being explicitly programmed with rules.
Formal line (Tom Mitchell): a program learns from experience **E** with respect to task **T** and performance
measure **P**, if its performance at T, measured by P, improves with E.
Example: instead of writing rules for spam, you show the model 10,000 labelled emails and it learns the rule itself.

**Q3. Difference between AI, ML and Deep Learning?** ⭐
Nested circles: **AI ⊃ ML ⊃ DL**.
- **AI** — any technique that makes machines act smart (including hard-coded rules).
- **ML** — learns the mapping from data; usually needs hand-made features.
- **DL** — ML using multi-layer neural networks that learn the features themselves; needs more data and GPUs.

**Q4. What is Data Science and how is it different from ML?**
Data Science is the broader practice of extracting insight from data — collection, cleaning, analysis,
visualisation, statistics, and modelling. ML is one tool inside it.
A data scientist may spend most of the time on EDA and business framing; an ML engineer focuses on building,
training and shipping the model.

**Q5. Types of Machine Learning?** ⭐
1. **Supervised** — labelled data, learn input → output (classification, regression).
2. **Unsupervised** — unlabelled data, find structure (clustering, dimensionality reduction).
3. **Semi-supervised** — small labelled set + large unlabelled set.
4. **Reinforcement** — an agent learns by acting in an environment and receiving rewards.

**Q6. What is supervised learning? Give examples.** ⭐
Learning from data where each input already has the correct answer (label) attached.
- **Classification** (discrete output): spam / not spam, disease / no disease.
- **Regression** (continuous output): house price, tomorrow's temperature.
Algorithms: Linear & Logistic Regression, Decision Tree, Random Forest, SVM, KNN, Naive Bayes, XGBoost.

**Q7. What is unsupervised learning? Give examples.** ⭐
Learning from data with **no labels** — the model groups or compresses the data by itself.
Uses: customer segmentation, anomaly detection, topic discovery, recommendation, market-basket analysis.
Algorithms: K-Means, Hierarchical clustering, DBSCAN, PCA, t-SNE, Autoencoders, Apriori.

**Q8. What is reinforcement learning?**
An **agent** takes an **action** in an **environment**, moves to a new **state**, and gets a **reward**; over
many episodes it learns a **policy** that maximises long-term reward.
No labelled dataset — the feedback is delayed and evaluative, not instructive.
Uses: game playing, robotics, dynamic pricing, traffic-signal control, recommendation ordering.

**Q9. Difference between training data, validation data and test data?** ⭐
- **Training set** (~70%) — the model learns its parameters here.
- **Validation set** (~15%) — used to tune hyperparameters and pick the best model.
- **Test set** (~15%) — touched only once at the end, to estimate real-world performance.
If you tune on the test set, your reported accuracy is optimistic and meaningless.

**Q10. What is a parameter vs a hyperparameter?** ⭐
- **Parameter** — learned by the model from data (weights, coefficients, split points).
- **Hyperparameter** — set by you before training (learning rate, number of trees, k in KNN, epochs, max depth).
Hyperparameters are tuned via Grid Search, Random Search, or Bayesian optimisation.

**Q11. What is inductive bias / why is "no free lunch" relevant?**
Inductive bias is the set of assumptions a model makes to generalise beyond the training data (e.g. linear
regression assumes a straight-line relationship).
**No Free Lunch theorem**: no single algorithm is best for every problem — which is why you baseline several
models rather than always reaching for the fanciest one.

**Q12. What are the main steps of an end-to-end ML project?** ⭐
1. Understand the business problem and define the metric.
2. Collect data → 3. EDA → 4. Clean & preprocess → 5. Feature engineering →
6. Split data → 7. Train baseline + candidate models → 8. Evaluate & tune →
9. Deploy (API/batch) → 10. Monitor for drift and retrain.
Say honestly: "roughly 70–80% of the effort is steps 2–5."

---

## 2. Statistics & probability

**Q13. Mean, median, mode — when do you use which?**
Mean = average, median = middle value, mode = most frequent.
Use **median** when data is skewed or has outliers (income, house price); mean when data is roughly symmetric;
mode for categorical data.

**Q14. What is variance and standard deviation?**
Variance is the average squared distance of values from the mean; standard deviation is its square root
(back in the original unit, so easier to interpret).
High std dev = data is spread out. Std dev is what you use in standardisation (z-score).

**Q15. What is the Normal distribution and the empirical rule?**
A symmetric bell curve defined by mean μ and std dev σ. Mean = median = mode.
**68–95–99.7 rule**: ~68% of data lies within 1σ, ~95% within 2σ, ~99.7% within 3σ. That is why "beyond 3σ" is a
common outlier rule.

**Q16. What is the Central Limit Theorem?** ⭐
The distribution of *sample means* approaches a normal distribution as sample size grows (n ≥ 30 as a rule of
thumb), **regardless of the population's own distribution**.
This is why we can use normal-based confidence intervals and t-tests on non-normal data.

**Q17. What is a p-value?** ⭐
The probability of observing a result at least as extreme as yours, *assuming the null hypothesis is true*.
Small p (< 0.05) → the data is unlikely under the null → reject the null.
A p-value is **not** the probability that the hypothesis is true, and statistical significance ≠ practical importance.

**Q18. Type I vs Type II error?**
- **Type I (α)** — false positive: rejecting a true null. (Telling a healthy patient they are sick.)
- **Type II (β)** — false negative: failing to reject a false null. (Missing a real disease.)
Lowering one usually raises the other; the business cost decides which you protect against.

**Q19. Difference between correlation and causation? And covariance vs correlation?** ⭐
Correlation means two variables move together; causation means one *makes* the other change. Correlation can come
from coincidence or a hidden confounder — only a controlled experiment (A/B test) establishes causation.
**Covariance** shows direction but its magnitude is unit-dependent; **correlation** is covariance normalised to
[-1, 1], so it also shows strength and is comparable across features.

**Q20. What is Bayes' theorem?** ⭐
P(A|B) = P(B|A) · P(A) / P(B) — it updates a prior belief with new evidence to give a posterior.
It is the basis of Naive Bayes classifiers. Classic interview example: even a 99%-accurate test for a rare disease
gives a low probability of actually having it, because the prior P(disease) is tiny.

---

## 3. Data preprocessing & feature engineering

**Q21. How do you handle missing values?** ⭐
First ask *why* it is missing (random vs systematic). Then:
- Drop rows (only if few) or drop the column (if mostly empty).
- Impute: mean/median (median if skewed), mode for categorical, forward/backward fill for time series.
- Model-based: KNN imputer, MICE / iterative imputer.
- Add a "was_missing" flag — missingness itself is sometimes predictive.
Always fit the imputer on train only, then apply to test (else you leak).

**Q22. How do you detect and handle outliers?** ⭐
Detect: box plot / **IQR rule** (below Q1−1.5·IQR or above Q3+1.5·IQR), z-score > 3, scatter plots, Isolation
Forest, DBSCAN.
Handle: remove (if a genuine error), cap/winsorise, log-transform, or keep them and use a robust model (tree-based
models handle outliers well; linear regression and K-Means do not).

**Q23. What is feature scaling? Normalisation vs standardisation?** ⭐
Bringing features to a comparable range so no feature dominates just because of its unit.
- **Normalisation (Min-Max)**: (x − min)/(max − min) → range [0, 1]. Good for neural nets, image pixels.
- **Standardisation (Z-score)**: (x − μ)/σ → mean 0, std 1. Better when data is roughly normal or has outliers.
**Needed for**: KNN, K-Means, SVM, PCA, linear/logistic regression with regularisation, neural networks.
**Not needed for**: Decision Tree, Random Forest, XGBoost (they split on thresholds, scale-invariant).

**Q24. How do you encode categorical variables?** ⭐
- **Label encoding** — categories → 0,1,2… Fine for tree models and ordinal data (Low/Medium/High); risky for
  linear models because it invents a fake order.
- **One-hot encoding** — one binary column per category. Safe, but explodes with high cardinality.
- **Target/mean encoding** — replace category with the mean of the target; powerful but leaks easily, so compute
  it inside cross-validation folds.
- **Frequency / hashing / embeddings** for very high cardinality.

**Q25. What is the dummy variable trap?**
If you one-hot encode k categories into k columns and also keep an intercept, the columns are perfectly
collinear (they sum to 1). Fix by dropping one column (`drop_first=True`). Matters for linear/logistic
regression, not for trees.

**Q26. What is feature engineering? Give examples.** ⭐
Creating new input variables from raw data so the model can learn more easily — often the single biggest lever
on accuracy.
Examples: extracting day/month/weekend from a timestamp, ratios (debt-to-income), aggregations (avg spend per
customer), binning age into groups, text length, interaction terms, log transform of skewed features.

**Q27. What is feature selection and what are the three families of methods?**
Keeping only the useful features — improves accuracy, speed, and interpretability while reducing overfitting.
- **Filter** — statistics before modelling: correlation, chi-square, ANOVA, mutual information, variance threshold.
- **Wrapper** — search using the model: forward selection, backward elimination, RFE.
- **Embedded** — selection happens during training: Lasso (L1), tree feature importance.

**Q28. What is the curse of dimensionality?** ⭐
As the number of features grows, the data becomes sparse in that space, distances between points become
meaningless, and the data needed to generalise grows exponentially — so models overfit.
Fix: feature selection, PCA, regularisation, or gathering more data.

**Q29. What is multicollinearity, how do you detect and fix it?**
Two or more independent variables are highly correlated with each other. The model's overall predictions stay
fine, but coefficients become unstable and uninterpretable.
Detect: correlation matrix, or **VIF** (Variance Inflation Factor > 5–10 is a red flag).
Fix: drop one of the pair, combine them, use PCA, or use Ridge regression.

**Q30. What is data leakage?** ⭐
When information that would not be available at prediction time sneaks into training, giving a great validation
score that collapses in production.
Common causes: scaling/imputing before the train-test split, target-derived features, using future data in time
series, duplicate rows across splits.
Fix: split first, then fit all transformations on train only — use a `Pipeline`.

**Q31. How do you handle imbalanced datasets?** ⭐
(e.g. 99% legit, 1% fraud — accuracy is useless here.)
- **Metrics first**: use precision, recall, F1, PR-AUC, confusion matrix — not accuracy.
- **Resampling**: oversample the minority (**SMOTE** creates synthetic points), undersample the majority.
- **Algorithmic**: `class_weight='balanced'`, cost-sensitive loss, focal loss.
- **Threshold tuning**: move the decision threshold away from 0.5.
- Use **stratified** splits/CV so every fold keeps the class ratio.

---

## 4. Supervised learning algorithms

**Q32. Explain Linear Regression and its assumptions.** ⭐
Fits a straight line y = β₀ + β₁x₁ + … + βₙxₙ that minimises the sum of squared errors between predicted and
actual values.
Assumptions: **linearity**, **independence** of errors, **homoscedasticity** (constant error variance),
**normality of residuals**, **no multicollinearity**.
Coefficient meaning: "holding everything else constant, a 1-unit increase in x changes y by β."

**Q33. What is the cost function of linear regression and how is it minimised?**
**MSE** = (1/n)·Σ(yᵢ − ŷᵢ)². It is convex, so it has a single global minimum.
Minimised either by the **Normal Equation** (closed form, fine for small feature counts) or by **Gradient
Descent** (scales to large data).

**Q34. What is Logistic Regression? Why not use linear regression for classification?** ⭐
Logistic regression models the *probability* of a class by passing the linear combination through a **sigmoid**:
σ(z) = 1/(1+e⁻ᶻ), which squashes any number into (0, 1). Predict class 1 if p > threshold (default 0.5).
Linear regression is unsuitable because it can output values below 0 and above 1, is sensitive to outliers, and
its squared-error cost is non-convex with the sigmoid.
Its cost function is **log loss / binary cross-entropy**, not MSE.

**Q35. Is logistic regression a linear model?**
Yes — the *decision boundary* is linear in the features; only the output is transformed non-linearly by the
sigmoid. For non-linear boundaries you add polynomial/interaction features or use a different model.

**Q36. Explain Decision Trees. How does the tree decide where to split?** ⭐
A flowchart of if-else questions; each internal node splits on the feature that best separates the classes, each
leaf gives a prediction.
Split criteria — **Gini impurity** and **Entropy / Information Gain** for classification, **variance reduction /
MSE** for regression. Gini is slightly faster; results are usually similar.
Pros: interpretable, no scaling needed, handles mixed data. Con: **overfits** easily → control with `max_depth`,
`min_samples_leaf`, or pruning.

**Q37. What is entropy and information gain?**
**Entropy** = −Σ p·log₂(p) measures impurity/disorder of a node (0 = pure, 1 = 50-50 for binary).
**Information Gain** = entropy(parent) − weighted entropy(children). The tree picks the split with the highest
information gain.

**Q38. What is ensemble learning? Bagging vs Boosting?** ⭐
Combining several weak models to get one stronger, more stable model.
- **Bagging** (Bootstrap Aggregating) — train many models **in parallel** on random bootstrap samples and average
  their votes. Reduces **variance**. Example: Random Forest.
- **Boosting** — train models **sequentially**, each one focusing on the errors of the previous. Reduces **bias**.
  Examples: AdaBoost, Gradient Boosting, XGBoost, LightGBM.
- **Stacking** — a meta-model learns how to combine the base models' predictions.

**Q39. Explain Random Forest.** ⭐
Bagging over decision trees with an extra twist: at each split only a **random subset of features** is
considered, which decorrelates the trees.
Final answer = majority vote (classification) or average (regression).
Strengths: strong out-of-the-box accuracy, resistant to overfitting, gives feature importance, handles missing
and unscaled data. Weakness: slower and far less interpretable than a single tree.

**Q40. What is out-of-bag (OOB) error?**
Each bootstrap sample leaves out ~37% of rows; those out-of-bag rows act as a free validation set for that tree.
Averaging over all trees gives an unbiased error estimate without a separate holdout or cross-validation.

**Q41. Why is XGBoost so popular for tabular data?**
Gradient boosting done efficiently: it adds trees that fit the *residual errors* of the current ensemble, using
second-order gradients.
Extras that make it win competitions: built-in **L1/L2 regularisation**, handling of missing values, parallelised
tree construction, early stopping, and tree pruning.
Key hyperparameters: `n_estimators`, `learning_rate`, `max_depth`, `subsample`, `colsample_bytree`.

**Q42. Explain SVM and the kernel trick.** ⭐
SVM finds the **hyperplane that maximises the margin** — the distance to the closest points of each class
(the **support vectors**).
The **kernel trick** computes similarities as if the data were mapped into a much higher-dimensional space,
without ever computing that mapping — letting a linear separator handle non-linear data.
Kernels: linear, polynomial, **RBF** (most common), sigmoid. `C` controls the margin/error trade-off, `gamma`
controls how far one training point's influence reaches.

**Q43. Explain KNN. Why is it called a lazy learner?** ⭐
To classify a point, look at its **k nearest neighbours** (usually Euclidean distance) and take the majority
vote; for regression take the average.
It is **lazy** because there is no training phase — it just stores the data and does all the work at prediction
time, which makes inference slow on large datasets.
Requires **feature scaling**; small k → overfits (noisy), large k → underfits. Pick odd k to avoid ties.

**Q44. Explain Naive Bayes. Why "naive"?** ⭐
A probabilistic classifier applying Bayes' theorem, picking the class with the highest posterior probability.
"**Naive**" because it assumes all features are **conditionally independent** given the class — rarely true, yet
it works remarkably well.
Very fast, needs little data, excellent baseline for text/spam classification. Variants: Multinomial (counts),
Bernoulli (binary), Gaussian (continuous). Use **Laplace smoothing** so an unseen word doesn't zero out the
whole probability.

**Q45. When would you choose a simple model over a complex one?**
When data is small, when the relationship is genuinely simple, when latency is tight, and — importantly — when
the business needs **explainability** (credit, insurance, healthcare are regulated).
Always start with a simple baseline: it sets the bar that any complex model must beat.

---

## 5. Model evaluation & tuning

**Q46. What is overfitting and underfitting? How do you fix each?** ⭐
- **Overfitting** — model memorises training data including noise; train accuracy high, test accuracy low.
  Fix: more data, fewer features, regularisation (L1/L2), simpler model, pruning, dropout, early stopping,
  cross-validation, data augmentation.
- **Underfitting** — model is too simple to capture the pattern; both train and test accuracy are low.
  Fix: more complex model, better features, less regularisation, train longer.

**Q47. Explain the bias-variance trade-off.** ⭐
- **Bias** — error from wrong assumptions; high bias = underfitting.
- **Variance** — sensitivity to the particular training set; high variance = overfitting.
Total error = bias² + variance + irreducible noise. Reducing one typically increases the other; the goal is the
sweet spot in the middle. Linear regression = high bias/low variance; deep trees and KNN with k=1 = low
bias/high variance.

**Q48. What is cross-validation? What is K-fold?** ⭐
Splitting the data into K folds, training on K−1 and validating on the remaining one, rotating K times and
averaging the scores. Gives a far more reliable estimate than a single split and uses all data for both roles.
K = 5 or 10 typically. **Stratified K-fold** preserves class ratios (use it for imbalanced classification).
**Time-series split** must respect chronology — never shuffle time-series data.

**Q49. Explain the confusion matrix.** ⭐
A 2×2 table of actual vs predicted: **TP, FP (Type I), FN (Type II), TN**.
Everything else is derived from it:
- Accuracy = (TP+TN)/Total
- Precision = TP/(TP+FP) — "of those I flagged, how many were right?"
- Recall / Sensitivity = TP/(TP+FN) — "of all the real positives, how many did I catch?"
- Specificity = TN/(TN+FP)

**Q50. Precision vs Recall — which matters when?** ⭐
- **Precision** matters when a false positive is expensive: spam filter (don't kill a real email), recommending a
  product, marketing spend.
- **Recall** matters when a false negative is expensive: cancer screening, fraud detection, defect detection —
  missing a real case is the disaster.
There is a trade-off; you tune the decision threshold to move along it.

**Q51. What is the F1 score and why the harmonic mean?**
F1 = 2·(Precision·Recall)/(Precision+Recall) — one number balancing both, useful on imbalanced data.
The **harmonic** mean punishes imbalance: if precision is 1.0 and recall 0.0, the arithmetic mean is 0.5 but F1 is
0. Use **F-beta** (β>1) when recall matters more.

**Q52. What is ROC-AUC? When do you prefer PR-AUC?** ⭐
The ROC curve plots **TPR (recall) vs FPR** at every threshold; **AUC** is the area under it — the probability
that the model ranks a random positive above a random negative. 0.5 = random, 1.0 = perfect.
AUC is threshold-independent. On **heavily imbalanced** data, ROC-AUC looks optimistic because TN dominates —
prefer **Precision-Recall AUC** there.

**Q53. Which metrics do you use for regression?** ⭐
- **MAE** — average absolute error; robust to outliers, same unit as target.
- **MSE / RMSE** — squares the errors so large mistakes are punished harder; RMSE is in the target's unit.
- **R²** — proportion of variance explained (1 = perfect, 0 = no better than predicting the mean, can be negative).
- **Adjusted R²** — penalises useless extra features; R² can only go up when you add features, adjusted R² can go down.
- **MAPE** — percentage error, easy for business to read, breaks when actuals are near zero.

**Q54. What is regularisation? L1 vs L2?** ⭐
Adding a penalty on the size of the coefficients to the loss function, discouraging over-complex models and so
reducing overfitting.
- **L1 (Lasso)** — penalty λΣ|w|. Can shrink weights exactly to **zero** → automatic feature selection.
- **L2 (Ridge)** — penalty λΣw². Shrinks weights smoothly toward zero but never to zero; handles multicollinearity.
- **Elastic Net** — combines both.
λ (alpha) controls strength: too high → underfitting.

**Q55. What is gradient descent? Batch vs Stochastic vs Mini-batch?** ⭐
An optimisation algorithm that repeatedly moves the parameters in the direction of the negative gradient of the
loss: w := w − α·∂L/∂w, where α is the **learning rate**.
- **Batch GD** — uses the whole dataset per step: stable but slow.
- **Stochastic GD** — one sample per step: fast and noisy, the noise can escape local minima.
- **Mini-batch GD** — 32/64/128 samples per step: the practical default.
Learning rate too high → overshoot/diverge; too low → very slow training.

**Q56. How do you tune hyperparameters?** ⭐
- **Grid Search** — try every combination; exhaustive but expensive.
- **Random Search** — sample combinations randomly; usually finds a good setting far faster.
- **Bayesian optimisation** (Optuna, Hyperopt) — uses past trials to choose the next one intelligently.
Always tune with cross-validation, and keep the test set out of the loop.

**Q57. Your model gets 95% train accuracy and 65% test accuracy. What do you do?** ⭐
Classic overfitting. Walk through it out loud:
check for data leakage and train/test distribution mismatch → simplify the model / reduce depth → add
regularisation or dropout → get more data or augment → do proper cross-validation → check whether the metric
itself is right for the class balance.

---

## 6. Unsupervised learning & dimensionality reduction

**Q58. Explain K-Means clustering.** ⭐
1. Pick k initial centroids → 2. assign each point to the nearest centroid → 3. recompute centroids as the mean
of their cluster → 4. repeat until assignments stop changing.
It minimises within-cluster sum of squares (**inertia**). Needs scaled features, assumes roughly spherical and
similar-sized clusters, and is sensitive to initialisation — **k-means++** fixes the seeding.

**Q59. How do you choose the value of k?** ⭐
- **Elbow method** — plot inertia vs k and pick the "elbow" where the drop flattens.
- **Silhouette score** — measures how well each point fits its own cluster vs the next nearest (−1 to 1, higher
  is better).
- Domain knowledge / business constraint (e.g. marketing wants 4 segments).

**Q60. K-Means vs Hierarchical vs DBSCAN?**
- **K-Means** — fast, must specify k, spherical clusters, every point gets assigned.
- **Hierarchical** — builds a dendrogram (agglomerative bottom-up), no need to pre-specify k, but O(n²)–O(n³) so
  it doesn't scale.
- **DBSCAN** — density-based: finds arbitrarily shaped clusters, discovers k itself, and labels sparse points as
  **noise/outliers**. Needs `eps` and `min_samples`, struggles with varying densities.

**Q61. Explain PCA.** ⭐
Principal Component Analysis projects data onto new orthogonal axes (**principal components**) ordered by how
much **variance** they capture, letting you keep the first few and drop the rest.
Mechanically: standardise → covariance matrix → eigenvectors/eigenvalues (or SVD) → keep components covering
~95% of variance.
It is **unsupervised** (ignores the target) and the new components are **not interpretable** as original features.
Always scale before PCA.

**Q62. PCA vs LDA?**
Both reduce dimensions, but **PCA is unsupervised** and maximises variance, while **LDA (Linear Discriminant
Analysis) is supervised** and maximises separation between classes. LDA can give at most (number of classes − 1)
components.

**Q63. What is t-SNE / UMAP and when do you use them?**
Non-linear techniques that map high-dimensional data to 2D/3D while preserving local neighbourhoods — used for
**visualisation** and exploration, not as a preprocessing step for a model.
t-SNE is slow and non-deterministic; distances *between* clusters in a t-SNE plot are not meaningful. UMAP is
faster and preserves more global structure.

**Q64. What is anomaly detection and how would you approach it?**
Finding rare points that deviate from normal behaviour — fraud, machine failure, intrusion.
Approaches: statistical (z-score, IQR), distance/density-based (KNN, DBSCAN, Local Outlier Factor), **Isolation
Forest**, One-Class SVM, or autoencoder reconstruction error.
Labels are usually scarce, so evaluation leans on precision@k and expert review.

---

## 7. Deep learning

**Q65. What is a neural network / perceptron?** ⭐
A perceptron takes inputs, multiplies them by weights, adds a bias, and passes the sum through an activation
function: y = f(Σwᵢxᵢ + b).
A neural network stacks these into an **input layer**, one or more **hidden layers**, and an **output layer**.
With enough hidden units it can approximate any continuous function (universal approximation theorem).

**Q66. What is an activation function and why is it needed?** ⭐
It introduces **non-linearity**. Without it, stacking layers is still just one linear transformation, so the
network could never learn curves.
- **Sigmoid** (0,1) — output layer for binary classification; saturates → vanishing gradients.
- **Tanh** (−1,1) — zero-centred, still saturates.
- **ReLU** max(0,x) — the default for hidden layers: fast, no saturation for positives; can suffer "dying ReLU".
- **Leaky ReLU / ELU / GELU** — fix dying ReLU (GELU is standard in Transformers).
- **Softmax** — output layer for multi-class; converts scores to probabilities summing to 1.

**Q67. Explain forward propagation and backpropagation.** ⭐
**Forward pass**: inputs flow through the layers to produce a prediction, and the loss is computed.
**Backpropagation**: using the chain rule, the loss gradient is propagated backwards layer by layer to get
∂Loss/∂w for every weight; the optimiser then updates the weights.
One forward + one backward pass over a mini-batch = one training iteration.

**Q68. What is the vanishing/exploding gradient problem?** ⭐
In deep networks, gradients are products of many terms. If those terms are < 1 the gradient shrinks toward zero
(**vanishing**) and early layers stop learning; if > 1 it blows up (**exploding**) and training diverges to NaN.
Fixes: ReLU-family activations, proper initialisation (He/Xavier), batch normalisation, residual/skip
connections, gradient clipping (for exploding), LSTM/GRU gates in RNNs.

**Q69. What are epoch, batch size and iteration?** ⭐
- **Epoch** — one full pass through the training data.
- **Batch size** — number of samples processed before one weight update.
- **Iteration** — one weight update. Iterations per epoch = dataset size ÷ batch size.
1000 samples, batch size 100 → 10 iterations per epoch.

**Q70. Compare optimisers: SGD, Momentum, RMSprop, Adam.** ⭐
- **SGD** — plain gradient steps; can zig-zag and get stuck.
- **Momentum** — adds a fraction of the previous update, smoothing the path and accelerating through ravines.
- **RMSprop** — per-parameter adaptive learning rate using a moving average of squared gradients.
- **Adam** — Momentum + RMSprop; the default choice (lr ≈ 0.001), fast and robust. AdamW (decoupled weight decay)
  is standard for Transformers.

**Q71. What is dropout?** ⭐
During training, randomly "switch off" a fraction of neurons (e.g. 0.5) on each forward pass, so the network
cannot rely on any single neuron — a regularisation technique that acts like averaging many sub-networks.
At **inference time dropout is turned off** and activations are scaled accordingly.

**Q72. What is batch normalisation?**
Normalising each layer's inputs (per mini-batch) to zero mean and unit variance, then rescaling with learnable
γ and β.
Benefits: faster and more stable training, allows higher learning rates, reduces internal covariate shift, and
gives a mild regularisation effect. LayerNorm is the variant used in Transformers/NLP.

**Q73. What loss functions do you use where?** ⭐
- Regression → **MSE** (or MAE / Huber when outliers matter).
- Binary classification → **Binary cross-entropy** (log loss).
- Multi-class → **Categorical cross-entropy** (with softmax).
- Imbalanced detection → focal loss. Ranking/metric learning → triplet/contrastive loss.

**Q74. Explain CNNs. Why are they better than ANNs for images?** ⭐
A CNN slides small learnable **filters (kernels)** across the image to detect local patterns — edges, then
textures, then objects.
Key ideas: **local receptive fields**, **parameter sharing** (the same filter is reused everywhere → far fewer
weights), and **translation invariance**.
Layers: Conv → activation → **Pooling** (max pooling downsamples and adds robustness) → … → Flatten → Dense →
Softmax. A fully-connected net on a 224×224 image would need hundreds of millions of weights and would ignore
spatial structure.

**Q75. Explain RNN, LSTM and GRU.** ⭐
**RNN** processes sequences step by step, carrying a hidden state as memory — but suffers vanishing gradients, so
it forgets long-range context.
**LSTM** adds a **cell state** and three gates — **forget**, **input**, **output** — that decide what to discard,
add, and expose, letting it keep long-term dependencies.
**GRU** is a lighter version with two gates (update, reset); trains faster with similar performance.
All three are largely displaced by Transformers today, but remain a standard interview question.

**Q76. What is transfer learning? What is fine-tuning vs feature extraction?** ⭐
Taking a model pre-trained on a huge dataset (ResNet on ImageNet, BERT on web text) and reusing it for your own
smaller task — you get strong results with far less data, time, and compute.
- **Feature extraction** — freeze the pre-trained layers, train only the new head.
- **Fine-tuning** — unfreeze some/all layers and train with a small learning rate.
Rule of thumb: little data → freeze more; lots of data + different domain → fine-tune more.

---

## 8. Natural Language Processing

**Q77. What are the standard NLP preprocessing steps?** ⭐
Lowercasing → removing punctuation/HTML/special characters → **tokenisation** (splitting text into words or
subwords) → **stop-word removal** → **stemming or lemmatisation** → vectorisation.
Careful: stop-word removal hurts sentiment and question-answering tasks ("not good" loses its meaning).

**Q78. Stemming vs lemmatisation?** ⭐
Both reduce a word to a base form.
- **Stemming** chops suffixes with crude rules — fast, but the output may not be a real word ("studies" →
  "studi"). Porter stemmer.
- **Lemmatisation** uses a dictionary and part-of-speech to return a valid root ("studies" → "study", "better" →
  "good"). Slower but accurate.

**Q79. Bag of Words vs TF-IDF?** ⭐
- **BoW** — counts how many times each word appears; ignores order and treats every word as equally important.
- **TF-IDF** — Term Frequency × Inverse Document Frequency, down-weighting words that appear in many documents
  and up-weighting words distinctive to a document. IDF = log(N / documents containing the term).
Both produce sparse, high-dimensional vectors with no notion of meaning — "good" and "great" are unrelated.

**Q80. What are word embeddings? Explain Word2Vec.** ⭐
Dense, low-dimensional vectors (typically 100–300 dims) where **semantically similar words sit close together**,
learned from context. Famous property: king − man + woman ≈ queen.
**Word2Vec** has two training styles: **CBOW** (predict the target word from its context — faster) and
**Skip-gram** (predict the context from the target word — better on rare words).
Others: GloVe (co-occurrence-based), FastText (uses sub-word character n-grams, so it handles unseen words).

**Q81. What is the limitation of Word2Vec that BERT solves?** ⭐
Word2Vec gives **one static vector per word**, so "bank" in *river bank* and *bank account* share the same vector.
BERT produces **contextual embeddings** — the vector for a word changes with the sentence around it.

**Q82. What is NER, POS tagging, and sentiment analysis?**
- **POS tagging** — labelling each token with its grammatical role (noun, verb, adjective).
- **NER (Named Entity Recognition)** — extracting entities: person, organisation, location, date, amount.
- **Sentiment analysis** — classifying text as positive/negative/neutral; done with lexicons (VADER), classical
  ML on TF-IDF, or a fine-tuned transformer.

**Q83. What is a confusion point interviewers love: how do you evaluate a text-generation model?**
Classification-style metrics don't apply. Use **perplexity** (how surprised the model is by the true next token —
lower is better), **BLEU / ROUGE / METEOR** for translation and summarisation (n-gram overlap with a reference),
**BERTScore** for semantic similarity, and — most importantly in practice — human or model-based evaluation on
relevance, factuality and tone.

---

## 9. Transformers, LLMs & Generative AI

**Q84. What is a Transformer and why did it replace RNNs?** ⭐
An architecture built entirely on **attention**, from the paper *Attention Is All You Need* (2017).
Because it drops recurrence, all tokens are processed **in parallel** (huge speed-up on GPUs) and any token can
attend directly to any other, so long-range dependencies are captured far better than by an RNN.
Structure: input embeddings + **positional encoding** → N blocks of (multi-head self-attention → add & norm →
feed-forward → add & norm).

**Q85. Explain self-attention, Q/K/V and multi-head attention.** ⭐
Each token creates three vectors: **Query** (what I'm looking for), **Key** (what I offer), **Value** (what I
carry).
Attention(Q,K,V) = softmax(QKᵀ/√dₖ)·V — dot products score how relevant every other token is, softmax turns them
into weights, and the output is the weighted sum of values. The √dₖ scaling keeps the softmax from saturating.
**Multi-head**: run this several times in parallel with different projections so different heads capture
different relationships (syntax, coreference, …), then concatenate.

**Q86. Why does a Transformer need positional encoding?**
Self-attention is permutation-invariant — it sees a *set* of tokens, not a sequence. Positional encodings
(original: sine/cosine of different frequencies; modern: learned or **RoPE**) inject word-order information into
the embeddings.

**Q87. BERT vs GPT?** ⭐
- **BERT** — **encoder**-only, **bidirectional** (sees left and right context), pre-trained with Masked Language
  Modelling + Next Sentence Prediction. Best for *understanding* tasks: classification, NER, extractive QA.
- **GPT** — **decoder**-only, **autoregressive** (predicts the next token, sees only the left), pre-trained with
  causal LM. Best for *generation*: chat, summarisation, code.
T5/BART are encoder-decoder, framing everything as text-to-text.

**Q88. What is an LLM, and what are tokens, context window, temperature and top-p?** ⭐
An LLM is a Transformer with billions of parameters trained on massive text to predict the next token.
- **Token** — a sub-word chunk (~4 characters / ~0.75 words in English); models bill and limit by tokens.
- **Context window** — the maximum tokens (prompt + response) the model can attend to at once.
- **Temperature** — randomness of sampling: 0 = deterministic/factual, higher = more creative.
- **Top-p (nucleus)** — sample only from the smallest set of tokens whose probabilities sum to p.

**Q89. What is hallucination and how do you reduce it?** ⭐
When a model produces fluent, confident text that is factually wrong — because it is optimising for *plausible
next token*, not truth.
Mitigations: **RAG** (ground answers in retrieved documents), demand citations, lower temperature, better
prompting ("say 'I don't know' if unsure"), fine-tuning on domain data, output validation/guardrails, and a
human in the loop for high-stakes use.

**Q90. What is RAG, and when do you choose RAG vs fine-tuning?** ⭐⭐ *(the single most asked GenAI question)*
**RAG (Retrieval-Augmented Generation)**: chunk your documents → embed them → store in a **vector database** →
at query time embed the question, retrieve the top-k most similar chunks (cosine similarity), and paste them
into the prompt as context.
Decision framework to say out loud:
- **RAG** when the model needs **fresh, private, or frequently changing knowledge**, when you need citations and
  auditability, and when you want low cost / fast iteration.
- **Fine-tuning** when you need to change **behaviour, format, or tone**, teach a specialised style or task, or
  cut prompt length and latency.
- **Both** in most serious systems: fine-tune for how it answers, RAG for what it knows.

**Q91. What is LoRA / QLoRA and PEFT?**
Full fine-tuning updates every weight — expensive in memory. **PEFT (Parameter-Efficient Fine-Tuning)** updates
only a tiny fraction.
**LoRA** freezes the base model and injects small trainable low-rank matrices into the attention layers,
training ~0.1–1% of the parameters with near-full-fine-tuning quality.
**QLoRA** adds 4-bit quantisation of the frozen base model, so large models fine-tune on a single GPU.
Related: **RLHF** (Reinforcement Learning from Human Feedback) aligns a model with human preferences after
supervised fine-tuning.

---

## 10. Reinforcement learning

**Q92. What is a Markov Decision Process?**
The formal frame for RL: **(S, A, P, R, γ)** — states, actions, transition probabilities, rewards, and a discount
factor γ ∈ [0,1] that trades off immediate vs future reward.
**Markov property**: the next state depends only on the current state and action, not the full history.

**Q93. Explain the exploration vs exploitation dilemma.** ⭐
**Exploit** = take the action currently believed best; **explore** = try something else to discover a possibly
better one. Pure exploitation locks in a mediocre policy; pure exploration never cashes in.
Common strategy: **ε-greedy** — act randomly with probability ε, decayed over time. Others: UCB, softmax,
Thompson sampling.

**Q94. What is Q-learning?**
A model-free, **off-policy** algorithm that learns Q(s,a) — the expected total reward of taking action a in state
s and behaving optimally afterwards.
Update: Q(s,a) ← Q(s,a) + α[r + γ·maxₐ' Q(s',a') − Q(s,a)].
**Deep Q-Networks (DQN)** replace the lookup table with a neural network, plus experience replay and a target
network for stability.

---

## 11. MLOps, deployment & responsible AI

**Q95. How do you deploy an ML model to production?** ⭐
Serialise the model (pickle/joblib/ONNX/SavedModel) → wrap it in a **REST API** (FastAPI/Flask) → containerise
with **Docker** → deploy to a cloud service or Kubernetes → add logging, monitoring and versioning.
Patterns: **real-time API** (low latency), **batch scoring** (nightly predictions), **streaming**, or **edge**.
Mention CI/CD, a model registry (MLflow) and a feature store if you want to sound senior.

**Q96. What is model drift and how do you detect it?** ⭐
Model performance decays because the world changed.
- **Data drift** — the input distribution shifts (new customer mix).
- **Concept drift** — the input→output relationship itself shifts (fraud tactics change).
Detect: monitor input feature distributions (PSI, KL divergence, KS test) and live metrics against a baseline;
alert on thresholds and retrain on a schedule or trigger.

**Q97. How do you A/B test a model?**
Route a small slice of traffic to the new model (challenger) and the rest to the current one (champion), then
compare a pre-declared business metric with statistical significance.
Safer rollouts: **shadow deployment** (new model scores live traffic but its output isn't used), then canary,
then full rollout — with an instant rollback path.

**Q98. What is explainability? What are SHAP and LIME?** ⭐
Making a model's decisions understandable — required in regulated domains and for debugging and trust.
- **SHAP** — game-theoretic Shapley values; gives consistent global *and* per-prediction feature contributions.
- **LIME** — fits a simple interpretable model locally around one prediction.
Also: coefficients (linear models), tree feature importance, permutation importance, partial dependence plots.

**Q99. What is bias in ML and how do you address it?** ⭐
Systematic unfairness against a group, usually inherited from historical data, unbalanced sampling, or proxy
features (pin code standing in for ethnicity).
Address it across the lifecycle: audit and rebalance the data, drop or test proxy features, measure fairness
metrics per subgroup (demographic parity, equal opportunity), apply constraints or reweighting during training,
and keep humans in the loop for consequential decisions.
Note the wording trap: "bias" here is **societal bias**, different from the "bias" in the bias-variance trade-off.

**Q100. What are the main ethical/governance concerns with AI systems today?**
Privacy and consent over training data, fairness and discrimination, hallucination and misinformation,
transparency and the right to an explanation, security (**prompt injection**, data exfiltration, model theft),
intellectual property, environmental cost, and accountability for automated decisions.
Practical answer: version data and models, document with model cards, red-team before launch, log everything,
and define who owns the decision when the model is wrong.

---

## Bonus: questions they ask *after* the theory

These decide the outcome more often than the definitions do.

1. **"Walk me through a project you've built."** — Use STAR: Situation → Task → Action → Result. Include the
   dataset size, the baseline, why you chose the model, the metric, the number, and what you'd do differently.
2. **"Why did you choose that algorithm?"** — Never say "it gave the best accuracy" alone. Say: data size,
   linearity, interpretability need, training cost, and that you compared against a baseline.
3. **"What was the hardest bug/problem in that project?"** — Have one specific, honest story ready.
4. **"Your accuracy is 99% — are you happy?"** — Ask about class balance first. This is a trap.
5. **"How would you approach [business problem]?"** — Frame it: clarify the objective → what data exists → how
   success is measured → baseline → model → deployment and monitoring. They score the framing, not the answer.
6. **"What do you do when you don't know something?"** — Say you'd say so, then explain how you'd find out.
   Guessing confidently is the worst outcome in an AI role.
7. **"Where do you see yourself / why this company?"** — Have two concrete sentences ready.

**The rule for tomorrow:** it is better to explain three concepts clearly with a real-world analogy than to
recite thirty definitions. If you don't know something, say "I haven't worked with that, but my understanding
is…" — interviewers reward honesty plus reasoning far more than a bluff.
