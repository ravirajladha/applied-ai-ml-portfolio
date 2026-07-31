# Machine Learning — subject deep dive

80 questions at interview depth. Format for each:

> **The spoken answer** — what you actually say first, in plain words.

…then the explanation, then **the follow-up they chain onto it**. Interviewers rarely ask one question; they
ask one question and then push three levels deeper. The follow-ups are where candidates fall apart, so they are
written out here.

⭐ = very high frequency.

**Contents**

| # | Section |
|---|---------|
| 1–8 | [The learning problem](#1-the-learning-problem) |
| 9–15 | [Linear regression](#2-linear-regression) |
| 16–22 | [Logistic regression](#3-logistic-regression) |
| 23–27 | [Regularisation](#4-regularisation) |
| 28–34 | [Decision trees](#5-decision-trees) |
| 35–44 | [Ensembles: bagging, random forest, boosting](#6-ensembles) |
| 45–49 | [Support Vector Machines](#7-support-vector-machines) |
| 50–54 | [KNN and Naive Bayes](#8-knn-and-naive-bayes) |
| 55–62 | [Unsupervised learning](#9-unsupervised-learning) |
| 63–71 | [Evaluation, validation and tuning](#10-evaluation-validation-and-tuning) |
| 72–80 | [Data problems and applied judgment](#11-data-problems-and-applied-judgment) |

---

## 1. The learning problem

**Q1. What is machine learning, formally?** ⭐

> A program learns from experience E at task T measured by P, if its performance at T, measured by P, improves
> with experience E.

That's Tom Mitchell's definition and it's worth memorising because it forces you to name three things: the
**task** (classify emails), the **experience** (10,000 labelled emails), and the **performance measure**
(F1 score). Interviewers use it to check you think in terms of a measurable objective, not "the AI learns".

Underneath, every supervised ML problem is the same shape: assume data comes from an unknown distribution
P(X, Y); find a function f from a hypothesis space H that minimises expected loss on *unseen* data drawn from
that same distribution. You can only measure loss on your sample, so everything in ML is a strategy for making
sample performance predict population performance.

**They'll follow up with:** *"So why can't we just minimise training error?"* → Because minimising training
error perfectly is trivial (memorise the data) and tells you nothing about new data. The gap between training
error and true error is what generalisation theory, regularisation and cross-validation all exist to control.

**Q2. What is the difference between parametric and non-parametric models?**

> Parametric models have a fixed number of parameters decided before training; non-parametric models grow their
> complexity with the data.

- **Parametric**: linear regression, logistic regression, Naive Bayes, neural networks (fixed architecture).
  Fast, need less data, strong assumptions, limited flexibility.
- **Non-parametric**: KNN, decision trees, SVM with RBF kernel, Random Forest. Flexible, need more data, risk
  overfitting, slower.

"Non-parametric" does **not** mean "no parameters" — KNN effectively stores the entire training set.

**Q3. Explain the bias-variance trade-off, with the decomposition.** ⭐⭐

> Bias is error from wrong assumptions — the model is too simple. Variance is error from sensitivity to the
> particular training sample — the model is too complex. You can usually trade one for the other, and the goal
> is the minimum of their sum.

Formally, expected squared error at a point decomposes as:

```
E[(y - f̂(x))²]  =  Bias[f̂(x)]²  +  Var[f̂(x)]  +  σ²
                    (wrong model)   (unstable fit)  (irreducible noise)
```

The third term is noise in the data itself — no model can beat it, which is why 100% accuracy is a red flag,
not a triumph.

Concretely: predicting house prices with a straight line through a curved relationship = **high bias**.
A depth-30 decision tree that changes completely if you swap ten rows = **high variance**.

**They'll follow up with:** *"How do you tell which one you have?"* → Compare train and validation error.
Both high and close together → high bias (underfitting), add capacity or features. Train much lower than
validation → high variance (overfitting), regularise or get more data. Plotting a **learning curve** (error vs
training-set size) makes it obvious: with high variance the two curves have a persistent gap that more data
would close; with high bias they converge early at a bad value and more data won't help.

**Q4. What is the curse of dimensionality — and give a concrete consequence.** ⭐

> As the number of features grows, the volume of the space grows exponentially, so your data becomes sparse and
> the notion of "nearest neighbour" stops meaning anything.

Concrete consequence: in high dimensions, the distance to the nearest point and the distance to the farthest
point become almost the same. Since KNN, K-Means, SVM with RBF, and anomaly detection are all built on
distances, they degrade badly.

Second consequence: the number of samples needed to cover the space at a fixed density grows exponentially with
dimensions, so models overfit.

Fixes: feature selection, PCA/embeddings, regularisation, or algorithms that are less distance-dependent
(tree ensembles).

**Q5. What is inductive bias?**

> The set of assumptions a model makes in order to generalise to data it has never seen.

Without assumptions, learning is impossible — any function fitting the training data is equally valid. Linear
regression assumes linearity; KNN assumes nearby points share labels; CNNs assume translation invariance and
locality; Naive Bayes assumes conditional independence.

Choosing a model *is* choosing an inductive bias. When the bias matches the problem, you need far less data.

**They'll follow up with:** *"What's the No Free Lunch theorem then?"* → Averaged over all possible problems,
no algorithm beats any other. There is no universally best model, which is why you always baseline several and
why domain knowledge (which lets you pick a sensible bias) matters more than algorithm hunting.

**Q6. What are the assumptions behind almost every supervised model?**

> That training and future data are drawn from the same distribution (i.i.d.), and that the relationship between
> features and target is stable.

When this breaks you get **distribution shift**: covariate shift (P(X) changes), label shift (P(Y) changes), or
concept drift (P(Y|X) changes). This is why models decay in production and why monitoring is not optional.

**Q7. Walk me through your end-to-end approach to a new ML problem.** ⭐

> Frame the business problem and the metric first, then data, EDA, cleaning, features, a baseline, then models,
> then evaluation, then deployment and monitoring.

Say it as a numbered flow and pause on the parts interviewers actually care about:

1. **Frame it** — is it even ML? What decision does the prediction drive? What's the cost of a false positive
   versus a false negative? That determines the metric.
2. **Data** — what's available, how much, how it's labelled, any leakage risk.
3. **EDA** — distributions, missingness, class balance, correlations, obvious errors.
4. **Split first**, then preprocess (this ordering is the leakage answer).
5. **Baseline** — predict the majority class or the mean. Every later model must beat this.
6. **Models** — start simple and interpretable, then try a tree ensemble; deep learning only if the data is
   unstructured or huge.
7. **Evaluate** with cross-validation on the metric you chose in step 1, not accuracy by default.
8. **Deploy** — API or batch, then **monitor** for drift and set a retraining trigger.

**They'll follow up with:** *"Where does most of the time go?"* → Steps 2–4. Say 70–80% and mean it; claiming
the modelling is the hard part signals inexperience.

**Q8. When would you *not* use machine learning?**

> When a rule solves it, when you can't measure success, when you don't have enough labelled data, or when a
> wrong answer is unacceptable and you can't explain the model.

Also: when the relationship is deterministic and known (use physics/business logic), when the data is tiny,
when the target moves faster than you can retrain, or when regulation demands a fully auditable decision.
Interviewers love this question because most candidates never consider saying no.

---

## 2. Linear regression

**Q9. Explain linear regression and its assumptions.** ⭐⭐

> It fits the straight line — or hyperplane — that minimises the sum of squared errors between the predicted
> and actual values.

Model: ŷ = β₀ + β₁x₁ + … + βₙxₙ. Cost: MSE = (1/n)Σ(yᵢ − ŷᵢ)².

**The five assumptions (LINE + no multicollinearity):**

| Assumption | What it means | What breaks if violated |
|---|---|---|
| **Linearity** | The relationship is genuinely linear in the parameters | Systematically biased predictions |
| **Independence** of errors | No autocorrelation (matters in time series) | Standard errors wrong, false significance |
| **Normality** of residuals | Errors are normally distributed | p-values and confidence intervals unreliable (predictions still OK) |
| **Equal variance** (homoscedasticity) | Error spread is constant across the range | Inefficient estimates, misleading confidence intervals |
| **No multicollinearity** | Features aren't highly correlated with each other | Unstable, uninterpretable coefficients |

Diagnose by plotting **residuals vs fitted values** — you want a shapeless cloud. A curve means non-linearity;
a funnel means heteroscedasticity. A Q-Q plot checks normality.

**They'll follow up with:** *"Does linear regression need normally distributed features?"* → No. The normality
assumption is on the **residuals**, not on X or y. This trips up most candidates.

**Q10. Why squared error and not absolute error?**

> Squared error is differentiable everywhere, gives a convex problem with a closed-form solution, and
> corresponds to the maximum likelihood estimate under Gaussian noise.

The cost: it punishes large errors quadratically, so it is **sensitive to outliers**. MAE is robust but not
differentiable at zero; **Huber loss** is the compromise — quadratic near zero, linear in the tails.

**Q11. Normal equation vs gradient descent — when do you use which?** ⭐

> Normal equation gives the exact answer in one shot but requires inverting a d×d matrix, so it's only practical
> for a modest number of features. Gradient descent is iterative and scales to millions of rows and features.

```
Normal equation:  β = (XᵀX)⁻¹Xᵀy      — O(d³), no learning rate, no iterations
Gradient descent: β := β − α·(2/n)Xᵀ(Xβ − y)  — O(n·d) per step, needs α and scaling
```

Rule of thumb: normal equation below ~10,000 features, gradient descent above. Also, `XᵀX` is **not invertible**
when features are perfectly collinear or when d > n — use the pseudo-inverse, or Ridge, which adds λI and
guarantees invertibility.

**Q12. How do you interpret a coefficient?** ⭐

> Holding all other features constant, a one-unit increase in this feature changes the prediction by β units.

Two traps interviewers set:
- **"Holding all else constant" is often impossible** in practice (you can't change square footage without
  changing number of rooms), which is why coefficients are correlational, not causal.
- **Magnitudes are only comparable if features are standardised.** A coefficient of 0.5 on "years" and 0.001 on
  "salary in rupees" says nothing about relative importance until you scale.

**Q13. What is R², and what's wrong with it?** ⭐

> R² is the proportion of variance in the target explained by the model — 1 is perfect, 0 is no better than
> predicting the mean, and it can go negative for a truly bad model.

R² = 1 − SS_res/SS_tot.

Problems: **R² never decreases when you add a feature**, even a random one — so it rewards bloat. Use
**Adjusted R²**, which penalises the number of predictors and can decrease. Also, a high R² doesn't mean the
model is correct (it could be overfit, or the assumptions violated), and a low R² isn't always bad — in noisy
domains like human behaviour, R² of 0.3 can be genuinely useful.

**Q14. What is multicollinearity? How do you detect and fix it?** ⭐

> Two or more predictors are strongly correlated with each other, so the model can't tell which one deserves
> credit. Predictions stay fine; the coefficients become unstable and uninterpretable.

**Detect:** correlation matrix (|r| > 0.8 is suspicious) or, better, **VIF**:

```
VIF_i = 1 / (1 - R²_i)      where R²_i is from regressing feature i on all other features
VIF > 5  → moderate concern;  VIF > 10 → serious
```

**Fix:** drop one of the correlated pair, combine them into one feature, apply PCA, or use **Ridge regression**
(L2 shrinkage stabilises correlated coefficients by splitting the weight between them).

**They'll follow up with:** *"Does it hurt prediction accuracy?"* → Usually not much on the same distribution.
It hurts **interpretation** and makes the model fragile to new data. Tree models are largely unaffected.

**Q15. How do you handle a non-linear relationship with a linear model?**

> Transform the features — polynomial terms, log/sqrt transforms, interactions, or binning — so the model stays
> linear in the parameters while capturing curvature.

`y = β₀ + β₁x + β₂x²` is still *linear regression* because it's linear in β. Log-transforming a skewed target
often fixes both non-linearity and heteroscedasticity at once. If you need many such transforms, that's the
signal to move to a tree ensemble instead.

---

## 3. Logistic regression

**Q16. Explain logistic regression.** ⭐⭐

> It's a classification model that estimates the probability of a class by passing a linear combination of the
> features through a sigmoid, which squashes any real number into the range 0 to 1.

```
z = β₀ + β₁x₁ + … + βₙxₙ
p = σ(z) = 1 / (1 + e⁻ᶻ)
predict class 1 if p ≥ threshold (default 0.5)
```

**They'll follow up with:** *"Why can't you use linear regression for classification?"* → Three reasons: it
outputs values outside [0,1] which can't be probabilities; it's badly affected by outliers shifting the fitted
line; and with a 0/1 target the squared-error surface with a sigmoid is non-convex, so optimisation gets stuck.

**Q17. What is the cost function and why not MSE?** ⭐

> Binary cross-entropy, also called log loss.

```
L = -(1/n) Σ [ yᵢ·log(pᵢ) + (1-yᵢ)·log(1-pᵢ) ]
```

Read it as: when the true label is 1, the loss is −log(p) — confidently wrong (p→0) costs infinitely much;
confidently right (p→1) costs zero. That's the whole intuition.

MSE with a sigmoid gives a **non-convex** loss surface with local minima, and its gradients vanish when the
sigmoid saturates. Cross-entropy is convex in the parameters and its gradient conveniently simplifies to
`Xᵀ(p − y)/n`.

**Q18. Is logistic regression a linear model?** ⭐

> Yes — the decision boundary is linear. Only the output is transformed non-linearly.

Setting p = 0.5 gives z = 0, i.e. β₀ + βᵀx = 0, which is a hyperplane. To get a curved boundary you must add
polynomial or interaction features, or switch models. Candidates who say "no, because of the sigmoid" fail this.

**Q19. How do you interpret logistic regression coefficients?**

> A one-unit increase in the feature multiplies the **odds** of the positive class by e^β.

The model is linear in the **log-odds**: log(p/(1−p)) = β₀ + βᵀx. So β = 0.7 means odds multiply by
e^0.7 ≈ 2 — the odds double. Interviewers who ask this want "odds ratio", not "probability increases by β".

**Q20. Can logistic regression handle multi-class?**

> Yes, two ways: one-vs-rest, which trains one binary classifier per class, or multinomial/softmax regression,
> which models all classes jointly.

Softmax generalises the sigmoid: p(class k) = e^{z_k} / Σⱼ e^{z_j}, with probabilities summing to 1. Softmax is
usually better calibrated; OvR is simpler and parallelises.

**Q21. How do you choose the classification threshold?** ⭐

> Not by defaulting to 0.5 — pick it from the business cost of false positives versus false negatives.

Method: get predicted probabilities on the validation set, sweep the threshold, and plot precision and recall
against it. Then either maximise F1, or fix the metric that matters (e.g. "recall must be ≥ 0.9, maximise
precision subject to that"). For fraud, a threshold of 0.2 may be right; for auto-approving a loan, 0.9.

**They'll follow up with:** *"Does changing the threshold change the AUC?"* → No. ROC-AUC is computed across
**all** thresholds, so it's threshold-independent. That's exactly why AUC is used to compare models and the
threshold is chosen afterwards, for deployment.

**Q22. What is model calibration and why does it matter?**

> A model is calibrated if, among all the cases where it says 70%, about 70% really are positive.

Logistic regression is naturally well calibrated (it optimises log loss directly). Random Forest and SVM are
often poorly calibrated — RF probabilities cluster toward the middle, boosted trees toward the extremes.
Fix with **Platt scaling** (fit a logistic regression on the scores) or **isotonic regression**; check with a
reliability/calibration curve. It matters whenever the probability itself drives a decision — expected loss,
pricing, ranking by risk.

---

## 4. Regularisation

**Q23. What is regularisation and why does it work?** ⭐⭐

> It adds a penalty on the size of the coefficients to the loss, so the model is discouraged from fitting noise
> with large, precise weights.

```
Ridge (L2):  Loss = MSE + λ·Σ βⱼ²
Lasso (L1):  Loss = MSE + λ·Σ |βⱼ|
```

Why it works in bias-variance terms: it **deliberately adds a little bias to buy a large reduction in
variance**. Large coefficients mean the prediction swings wildly for small input changes — exactly the
signature of overfitting.

Note: the intercept β₀ is not penalised, and features **must be standardised first**, otherwise the penalty
falls unevenly across features with different units.

**Q24. L1 vs L2 — and why does L1 produce exact zeros?** ⭐⭐

> L2 shrinks all coefficients smoothly toward zero but never to zero. L1 can push them exactly to zero, which
> makes it an automatic feature selector.

The geometric answer they're fishing for: the L1 constraint region is a **diamond** (rotated square) with sharp
corners on the axes; the L2 region is a **circle**. The optimum is where the elliptical contours of the loss
first touch the constraint region — and a diamond is most likely to be touched at a corner, where one
coefficient is exactly zero. A circle has no corners, so it touches at a point where all coefficients are small
but non-zero.

| | Lasso (L1) | Ridge (L2) |
|---|---|---|
| Coefficients | Some exactly 0 | All small, non-zero |
| Feature selection | Yes | No |
| Correlated features | Picks one arbitrarily, drops the rest | Spreads weight across them |
| Solution | No closed form (coordinate descent) | Closed form: (XᵀX + λI)⁻¹Xᵀy |
| Use when | Many irrelevant features | Many features that all matter a bit, multicollinearity |

**Elastic Net** = αL1 + (1−α)L2, and it's the right answer when you have correlated features *and* want
sparsity — it selects groups of correlated features together rather than picking one at random.

**Q25. What does λ (alpha) control, and how do you choose it?**

> It's the strength of the penalty. λ = 0 gives ordinary least squares; λ → ∞ shrinks every coefficient to zero
> and you predict the mean.

So λ directly slides you along the bias-variance curve: **too small → overfitting, too large → underfitting**.
Choose it by cross-validation over a log-spaced grid (`LassoCV`, `RidgeCV`, or `GridSearchCV`), picking the λ
with the best validation score — or the largest λ within one standard error of the best, if you want the
simpler model.

**Q26. Name regularisation techniques that aren't L1/L2.** ⭐

> Early stopping, dropout, data augmentation, tree pruning, bagging, and simply getting more data.

Anything that constrains effective model capacity is regularisation. **Early stopping** halts training when
validation loss stops improving — cheap and very effective. **Dropout** randomly zeroes neurons so the network
can't over-rely on any one path. **Max-depth / min-samples-leaf** on a tree. **Batch normalisation** has a mild
regularising side effect. And more data is the only "regulariser" with no bias cost.

**Q27. Why does Ridge help with multicollinearity specifically?**

> Because `XᵀX + λI` is always invertible, and the penalty forces correlated features to share the weight
> instead of taking huge opposing values.

With two nearly identical features, OLS can set β₁ = +1000 and β₂ = −995 — a huge, unstable pair that cancels.
Ridge penalises the sum of squares, and 500² + 500² < 1000² + 995², so it prefers splitting the weight evenly.
That's the whole mechanism.

---

## 5. Decision trees

**Q28. How does a decision tree decide where to split?** ⭐⭐

> It tries every feature and every candidate threshold, and picks the split that most reduces impurity in the
> resulting child nodes.

Greedy, top-down, recursive. For classification the impurity measure is Gini or entropy; for regression it's
variance (equivalently MSE) reduction.

```
Entropy = -Σ pᵢ log₂(pᵢ)               range 0 to 1 (binary); 0 = pure
Gini    = 1 - Σ pᵢ²                     range 0 to 0.5 (binary); 0 = pure
Information Gain = Impurity(parent) - Σ (nⱼ/n)·Impurity(childⱼ)
```

**They'll follow up with:** *"Gini or entropy — which is better?"* → Practically identical results. Gini is
slightly faster (no logarithm) and is scikit-learn's default; entropy comes from information theory and is what
ID3/C4.5 used. Say "the choice rarely matters; tree depth and pruning matter far more" — that's the answer they
want.

**Q29. Work through a Gini calculation.**

A node with 10 samples: 6 positive, 4 negative.

```
Gini(parent) = 1 - (0.6² + 0.4²) = 1 - (0.36 + 0.16) = 0.48
```

Split gives Left = [4 pos, 0 neg], Right = [2 pos, 4 neg]:

```
Gini(left)  = 1 - (1.0² + 0²)         = 0
Gini(right) = 1 - ((2/6)² + (4/6)²)   = 1 - (0.111 + 0.444) = 0.445
Weighted    = (4/10)(0) + (6/10)(0.445) = 0.267
Gain        = 0.48 - 0.267 = 0.213
```

The tree keeps whichever split has the largest gain. Being able to do this arithmetic out loud separates you
from people who only memorised the formula.

**Q30. Why do decision trees overfit, and how do you stop them?** ⭐

> Because if you let a tree grow until every leaf is pure, it has effectively memorised the training set —
> it can always isolate a single noisy point in its own leaf.

**Pre-pruning** (stop early): `max_depth`, `min_samples_split`, `min_samples_leaf`, `max_leaf_nodes`,
`min_impurity_decrease`. **Post-pruning**: grow fully, then cut back branches that don't improve validation
performance — scikit-learn's `ccp_alpha` (cost-complexity pruning) does this.

The most robust answer: use an **ensemble**. A single tree is high variance by nature; that's precisely the
problem Random Forest solves.

**Q31. Advantages and disadvantages of decision trees.** ⭐

**Advantages:** highly interpretable (you can draw the rules), no feature scaling needed, handles numeric and
categorical data, captures non-linear relationships and interactions automatically, robust to outliers, and
gives feature importance.

**Disadvantages:** overfits easily, **unstable** (a small data change can produce a completely different tree),
greedy so not globally optimal, biased toward features with many levels, poor at extrapolating (a regression
tree can never predict outside the range of the training target), and struggles with diagonal decision
boundaries because splits are axis-parallel.

**Q32. How do trees handle missing values and categorical features?**

> Some implementations handle missing values natively by learning a default direction; scikit-learn's does not
> and requires imputation.

XGBoost and LightGBM learn, per split, which way missing values should go — treating missingness as
information. CART traditionally used **surrogate splits** (a backup feature correlated with the primary one).
For categoricals: LightGBM and CatBoost handle them natively; scikit-learn needs encoding, and one-hot on a
high-cardinality feature hurts trees badly because it fragments the splits.

**Q33. Why is tree feature importance sometimes misleading?**

> Impurity-based importance is biased toward high-cardinality and continuous features, because they offer more
> possible split points and can look useful by chance.

It also splits credit arbitrarily between correlated features. Use **permutation importance** (shuffle a column,
measure the drop in validation score) or **SHAP** instead, and compute importance on held-out data, not training
data.

**Q34. What is a regression tree predicting at a leaf?**

> The mean of the training targets that landed in that leaf.

Which is why the prediction surface is a step function, and why trees can't extrapolate: no matter how far out
your input is, it lands in some existing leaf and gets that leaf's mean. For trending time series, this makes
tree models a poor choice unless you model differences or detrend first.

---

## 6. Ensembles

**Q35. What is ensemble learning and why does it work?** ⭐

> Combining several models so their errors cancel out, giving a prediction that's more accurate and more stable
> than any single member.

It works when the members are **individually better than random and make uncorrelated errors**. If three models
each get 70% right but are wrong on different examples, a majority vote is right far more than 70% of the time.
The whole design goal of Random Forest is to *force* the errors to be uncorrelated.

**Q36. Bagging vs boosting — the full comparison.** ⭐⭐

| | Bagging | Boosting |
|---|---|---|
| Training | Parallel, independent | Sequential, each depends on the last |
| Data per model | Bootstrap sample (random with replacement) | Full data, reweighted / residuals |
| Base learners | Deep, low-bias, high-variance trees | Shallow, high-bias "weak" learners (stumps) |
| Primarily reduces | **Variance** | **Bias** |
| Overfitting risk | Low; more trees never hurts | Higher; too many rounds overfits |
| Speed | Parallelisable | Sequential, slower to train |
| Examples | Random Forest, Extra Trees | AdaBoost, Gradient Boosting, XGBoost, LightGBM |

The one-line memory hook: **bagging averages many strong learners to cut variance; boosting stacks many weak
learners to cut bias.**

**Q37. Explain bootstrapping and out-of-bag error.**

> Bootstrapping is sampling n rows from a dataset of size n **with replacement**, so some rows repeat and some
> are left out.

Each bootstrap sample leaves out about **37%** of rows (the limit of (1 − 1/n)ⁿ → 1/e ≈ 0.368). Those held-out
rows are the **out-of-bag** set for that tree, and averaging performance over them gives a free, unbiased
validation estimate — no separate holdout or cross-validation needed. That's a favourite follow-up.

**Q38. Explain Random Forest precisely.** ⭐⭐

> Bagging over decision trees, plus a second source of randomness: at each split, only a random subset of
> features is considered.

Both randomisations matter, and candidates usually forget the second:
1. **Row randomness** — each tree trains on its own bootstrap sample.
2. **Feature randomness** — at every split, sample `max_features` of the features (default √p for
   classification, p/3 for regression) and split only among those.

Without step 2, if one feature is dominant every tree would split on it first and all the trees would look
alike — correlated errors, and averaging gains you nothing. Feature subsampling **decorrelates** the trees,
which is the entire trick.

Aggregation: majority vote (classification) or mean (regression).

**They'll follow up with:** *"Can Random Forest overfit?"* → Adding more trees does **not** cause overfitting —
the variance keeps reducing and the error plateaus. But a forest of fully grown trees on a small, noisy dataset
can still overfit somewhat; control it with `min_samples_leaf` and `max_depth`. The honest answer is "far less
than a single tree, and more trees is always safe, just slower."

**Q39. Random Forest hyperparameters that actually matter.**

- `n_estimators` — more is better until it plateaus; 100–500 typical. Cost is time, not accuracy.
- `max_features` — the key tuning knob. Lower = more decorrelation and less overfitting, but weaker individual trees.
- `max_depth` / `min_samples_leaf` — the main overfitting controls.
- `class_weight='balanced'` — for imbalanced targets.
- `n_jobs=-1` — use all cores (free speed, mention it).

**Q40. How does AdaBoost work?**

> It trains a sequence of weak learners, and after each one it increases the weight on the examples that were
> misclassified so the next learner concentrates on them.

Final prediction is a weighted vote, where each learner's vote weight depends on its accuracy. Base learner is
usually a **decision stump** (depth-1 tree). Because it chases misclassified points, AdaBoost is **sensitive to
noisy data and outliers** — they get up-weighted repeatedly. That's the standard follow-up.

**Q41. How does Gradient Boosting differ from AdaBoost?** ⭐

> AdaBoost re-weights the misclassified samples; gradient boosting fits each new tree to the **residual errors**
> — more precisely, to the negative gradient of the loss — of the ensemble so far.

That generalisation is the point: by fitting the negative gradient, gradient boosting works with **any
differentiable loss** (squared error, log loss, Huber, ranking losses), while AdaBoost is tied to exponential
loss.

Process: start with a constant prediction → compute residuals → fit a small tree to the residuals → add it,
scaled by the **learning rate** → repeat.

**Q42. What's the relationship between learning rate and number of trees in boosting?** ⭐

> They trade off: a smaller learning rate needs more trees, and that combination usually generalises better.

Each tree's contribution is scaled by the learning rate (shrinkage), typically 0.01–0.1. Low rate + many trees
+ **early stopping on a validation set** is the standard recipe. Setting the learning rate to 1.0 with few trees
overfits fast and unstably.

**Q43. Why does XGBoost win on tabular data?** ⭐

> It's gradient boosting with regularisation built into the objective, plus a lot of systems engineering.

Algorithmic:
- **Regularised objective** — penalises the number of leaves (γ) and leaf weights (λ), so each tree is
  constrained. Plain GBM has no such term.
- **Second-order optimisation** — uses gradient *and* Hessian (a second-order Taylor approximation of the loss),
  giving better split decisions.
- **Sparsity aware** — learns a default direction for missing values.
- **Built-in cross-validation and early stopping**, column and row subsampling, tree pruning.

Systems: parallelised split-finding, cache-aware access, out-of-core computation.

Key hyperparameters: `n_estimators`, `learning_rate`, `max_depth` (3–8), `subsample`, `colsample_bytree`,
`min_child_weight`, `gamma`, `reg_lambda`.

**They'll follow up with:** *"LightGBM vs XGBoost?"* → LightGBM grows trees **leaf-wise** (splitting the leaf
with the highest loss reduction) instead of level-wise, so it's much faster on large data and often more
accurate — but it overfits more easily on small data. It also uses histogram binning of features and handles
categoricals natively. CatBoost is the third option, strongest with heavy categorical data via ordered target
encoding.

**Q44. What is stacking?**

> Train several diverse base models, then train a **meta-model** on their predictions to learn how best to
> combine them.

The critical detail: the meta-model must be trained on **out-of-fold predictions**, not on predictions the base
models made on their own training data — otherwise it learns from leaked, overconfident inputs. Base models
should be diverse (a linear model + a tree ensemble + a KNN beats three tree ensembles). The meta-model is
usually something simple like logistic regression.

---

## 7. Support Vector Machines

**Q45. Explain SVM.** ⭐⭐

> It finds the decision boundary that maximises the margin — the distance from the boundary to the closest
> points of each class. Those closest points are the support vectors.

Why maximise the margin? A wider margin means the boundary is as far as possible from both classes, which
generalises better to new points that fall near the boundary.

```
Optimisation:  minimise ½‖w‖²   subject to   yᵢ(wᵀxᵢ + b) ≥ 1  for all i
Margin width = 2 / ‖w‖   →  minimising ‖w‖ maximises the margin
```

Only the support vectors determine the boundary — you could delete every other training point and get the same
model. That's a good detail to volunteer.

**Q46. What is the kernel trick?** ⭐⭐

> A way of computing the similarity between points *as if* they had been mapped into a much higher-dimensional
> space, without ever actually computing that mapping.

The SVM optimisation, in its dual form, only ever needs **dot products** between pairs of points. A kernel
function K(xᵢ, xⱼ) computes what the dot product *would be* in the higher-dimensional space directly from the
original features. So you get a non-linear boundary at the cost of a linear one.

Common kernels:
- **Linear** K = xᵢᵀxⱼ — for high-dimensional sparse data like text.
- **Polynomial** K = (γxᵢᵀxⱼ + r)^d.
- **RBF / Gaussian** K = exp(−γ‖xᵢ − xⱼ‖²) — the default; corresponds to an *infinite*-dimensional space.

**Q47. What do C and gamma control?** ⭐

> C is the penalty for misclassifying a training point — it controls the hard/soft margin trade-off. Gamma is
> the reach of a single training example in the RBF kernel.

- **Low C** → wide margin, more violations tolerated → more regularisation, may underfit.
- **High C** → narrow margin, few violations tolerated → may overfit.
- **Low gamma** → each point influences a large region → smoother, simpler boundary.
- **High gamma** → influence is very local → wiggly boundary that wraps individual points → overfits.

Tune them together on a log grid (C and gamma in powers of 10) — they interact.

**Q48. What is a soft margin?**

> Allowing some points to fall inside the margin or on the wrong side, using slack variables, because real data
> is rarely perfectly separable.

Objective becomes `½‖w‖² + C·Σξᵢ` where ξᵢ is how badly point i violates the margin. This is equivalent to
minimising **hinge loss** plus L2 regularisation — a nice connection to mention.

**Q49. Pros, cons, and when do you actually use SVM?**

**Pros:** effective in high dimensions (even when d > n), memory-efficient (stores only support vectors),
flexible via kernels, strong theoretical grounding, robust when the margin is clear.

**Cons:** scales poorly — roughly O(n²) to O(n³), so it's impractical beyond ~100k rows; needs feature scaling;
no native probability output (needs Platt scaling); kernel and hyperparameter choice is fiddly; hard to
interpret.

**Use it** for small-to-medium datasets with many features — text classification, bioinformatics, image
classification before deep learning. On large tabular data, gradient boosting has largely replaced it.

---

## 8. KNN and Naive Bayes

**Q50. Explain KNN and why it's called a lazy learner.** ⭐

> To predict, it finds the k closest training points and takes a majority vote, or an average for regression.
> It's lazy because there's no training phase — it just stores the data and does all the work at prediction time.

Consequence: training is O(1), prediction is O(n·d) per query. That's backwards from most models and it makes
KNN unusable for low-latency serving on large data (mitigate with KD-trees, ball trees, or approximate nearest
neighbour indexes like FAISS/HNSW — the same structures that power vector databases).

**Q51. How do you choose k, and what does it do to bias and variance?** ⭐

> Small k means low bias and high variance — the boundary is jagged and follows noise. Large k means high bias
> and low variance — the boundary smooths out, and at k = n you just predict the majority class.

Choose by cross-validation. Use an **odd** k for binary classification to avoid ties. A common starting point is
k ≈ √n. Optionally weight neighbours by inverse distance so closer points count more.

**Q52. What must you do before using KNN?** ⭐

> Scale the features — otherwise a feature measured in thousands dominates the distance calculation entirely.

Also consider the distance metric: Euclidean by default, Manhattan for high dimensions or mixed scales, cosine
for text/embeddings, Hamming for categorical. And reduce dimensionality — KNN is the algorithm most damaged by
the curse of dimensionality.

**Q53. Explain Naive Bayes and the "naive" assumption.** ⭐⭐

> It applies Bayes' theorem to pick the most probable class, assuming all features are conditionally
> independent given the class.

```
P(class | features) ∝ P(class) · Π P(featureᵢ | class)
```

The independence assumption is almost always false — in text, "New" and "York" are obviously not independent —
but the classifier still works well, because for *classification* you only need the correct class to have the
highest score, not the probabilities to be accurate. That's the insight to state; it's the real answer to
"why does it work despite the assumption being wrong?"

Side effect: the probabilities it outputs are **poorly calibrated** (pushed toward 0 and 1), so use the ranking,
not the number.

**Q54. What is Laplace smoothing and why is it needed?** ⭐

> If a feature value never appeared with a class in training, its probability is zero, and because Naive Bayes
> multiplies probabilities, that single zero wipes out the entire product.

Fix by adding a small count α (usually 1) to every count:

```
P(word | class) = (count(word, class) + α) / (count(class) + α·V)
```

Also mention: implementations sum **log** probabilities instead of multiplying raw ones, to avoid floating-point
underflow on long documents.

Variants: **Multinomial** (word counts — text), **Bernoulli** (binary presence/absence), **Gaussian**
(continuous features, assumes each is normally distributed per class).

---

## 9. Unsupervised learning

**Q55. Explain K-Means and its objective.** ⭐⭐

> It partitions the data into k clusters by alternating between assigning each point to its nearest centroid and
> recomputing each centroid as the mean of its points, until nothing changes.

Objective: minimise **within-cluster sum of squares** (inertia), Σ Σ ‖x − μⱼ‖².

Important honesty point: this objective is NP-hard, so Lloyd's algorithm only finds a **local** optimum — the
result depends on initialisation. Run it multiple times (`n_init=10`) and keep the best inertia, and use
**k-means++** initialisation, which spreads the initial centroids out probabilistically instead of choosing
them uniformly at random.

**Q56. What are K-Means's assumptions and failure modes?** ⭐

> It assumes clusters are spherical, similarly sized, and similarly dense — and it forces every point into a
> cluster.

Fails on: elongated or crescent-shaped clusters, clusters of very different sizes or densities, categorical data
(no meaningful mean), and outliers (which drag centroids). It's also sensitive to feature scale, so
**standardise first**, and k must be specified in advance.

When these break, reach for DBSCAN (arbitrary shapes, handles noise), Gaussian Mixture Models (soft assignment,
elliptical clusters), or hierarchical clustering.

**Q57. How do you choose k?** ⭐

> Elbow method on inertia, silhouette score, or a business constraint — and honestly, often the business
> constraint wins.

- **Elbow**: plot inertia vs k; inertia always decreases, so look for the bend where the improvement flattens.
  Subjective, and sometimes there's no visible elbow.
- **Silhouette score**: for each point, (b − a)/max(a, b) where a is the mean distance to its own cluster and b
  to the nearest other cluster. Range −1 to 1; pick the k with the highest mean. More principled than the elbow.
- **Gap statistic**, or **BIC/AIC** if you use a Gaussian Mixture Model.
- **Domain**: marketing wants 4 actionable segments, so k = 4.

**Q58. K-Means vs Hierarchical vs DBSCAN vs GMM.**

| | K-Means | Hierarchical | DBSCAN | GMM |
|---|---|---|---|---|
| Need k upfront | Yes | No (cut the dendrogram later) | No | Yes |
| Cluster shape | Spherical | Any (depends on linkage) | **Arbitrary** | Elliptical |
| Handles outliers | No | No | **Yes — labels them noise** | Somewhat |
| Assignment | Hard | Hard | Hard + noise | **Soft (probabilities)** |
| Scalability | O(n·k·i) — excellent | O(n²)–O(n³) — poor | O(n log n) with an index | Moderate |
| Key parameters | k | linkage, distance | eps, min_samples | k, covariance type |

DBSCAN's `eps` is chosen with a k-distance plot (sort each point's distance to its k-th neighbour, look for the
knee). Its weakness is clusters of **varying density** — one eps can't serve both.

**Q59. Explain PCA — mechanically and intuitively.** ⭐⭐

> PCA finds new axes, called principal components, that are ordered by how much of the data's variance they
> capture, so you can keep the first few and throw away the rest with minimal information loss.

Mechanics: standardise the data → compute the covariance matrix → take its eigenvectors and eigenvalues (or run
SVD directly on the centred data, which is what scikit-learn does for numerical stability) → the eigenvectors
are the components, and each eigenvalue is the variance captured by its component → keep enough components to
reach ~95% of cumulative explained variance.

Properties to state: components are **orthogonal** (uncorrelated), ordered by variance, and each is a **linear
combination of all original features** — which is why they're not interpretable as "the age feature".

**They'll follow up with:** *"Why must you standardise before PCA?"* → Because PCA maximises variance, and
variance depends on units. A feature in rupees will dwarf a feature in years and hijack the first component, not
because it's informative but because its numbers are bigger.

**Q60. Is PCA supervised? When would you use LDA instead?**

> PCA is unsupervised — it never looks at the target. It maximises variance, which is not the same as maximising
> class separability.

So PCA can discard a low-variance direction that happens to perfectly separate your classes. **LDA (Linear
Discriminant Analysis)** is the supervised counterpart: it maximises between-class separation relative to
within-class scatter, and produces at most (number of classes − 1) components. Use LDA when the goal is
classification and you have labels; PCA when you're compressing, denoising, or visualising.

**Q61. What are the downsides of PCA?**

Loss of interpretability; assumes linear relationships (use kernel PCA, autoencoders, or UMAP for non-linear
structure); sensitive to outliers; requires scaling; and the components are chosen without regard to the target,
so it can hurt supervised performance. Also, PCA is not a feature-selection method — every original feature
still contributes to every component, so you can't drop any of them at data-collection time.

**Q62. What is t-SNE and what's the trap with it?**

> A non-linear method that maps high-dimensional data to 2D by preserving local neighbourhoods — it's for
> **visualisation only**.

The traps interviewers probe: distances *between* clusters in a t-SNE plot are **not meaningful**, cluster sizes
are not meaningful, results change with the random seed and with the `perplexity` parameter, and you must never
fit t-SNE on train and "transform" test — it has no meaningful out-of-sample transform. UMAP is faster and
preserves more global structure, and does support transforming new points.

---

## 10. Evaluation, validation and tuning

**Q63. Why is accuracy a bad default metric?** ⭐⭐

> Because with imbalanced classes, a model that predicts the majority class every time gets a high accuracy
> while being completely useless.

The stock example: 1% fraud → predict "not fraud" always → 99% accuracy, 0 frauds caught. Always ask about
class balance before quoting accuracy, and switch to precision, recall, F1, PR-AUC and the confusion matrix.
Accuracy is also blind to the *cost asymmetry* between error types.

**Q64. Explain precision and recall, and when each dominates.** ⭐⭐

```
Precision = TP / (TP + FP)   "of everything I flagged, how much was actually positive"
Recall    = TP / (TP + FN)   "of all the actual positives, how many did I find"
```

- Optimise **recall** when a miss is expensive: cancer screening, fraud, predictive maintenance, security. You
  accept false alarms because a human will filter them.
- Optimise **precision** when a false alarm is expensive: spam filtering (deleting a real email is worse than
  letting spam through), auto-blocking accounts, expensive interventions.

They're in tension because both are controlled by the same threshold. F1 (harmonic mean) balances them; the
harmonic mean is used because it collapses toward the *worse* of the two — precision 1.0 with recall 0.0 gives
F1 = 0, not 0.5.

**Q65. ROC-AUC vs PR-AUC.** ⭐

> ROC-AUC is the probability that the model ranks a random positive above a random negative. PR-AUC focuses only
> on the positive class, which is what you want when positives are rare.

ROC plots TPR vs **FPR**, and FPR = FP/(FP+TN). With 99% negatives, TN is enormous, so FPR stays tiny even when
you generate lots of false positives — the ROC curve looks great and hides the problem. Precision, by contrast,
has FP in the denominator without TN, so it reacts immediately. **On heavy imbalance, quote PR-AUC (average
precision).**

Baselines to know: random ROC-AUC = 0.5 always; random PR-AUC = the positive class prevalence.

**Q66. Explain cross-validation and its variants.** ⭐⭐

> Split the data into K folds, train on K−1 and validate on the held-out one, rotate through all K, and average
> the scores.

Why: a single train/validation split gives a noisy estimate that depends heavily on which rows landed where.
CV uses every row for both training and validation, and the standard deviation across folds tells you how stable
your model is — quote that, not just the mean.

Variants:
- **Stratified K-fold** — preserves the class ratio in each fold. Default for classification, essential when
  imbalanced.
- **TimeSeriesSplit** — always train on the past, validate on the future. Never shuffle time series.
- **GroupKFold** — keeps all rows from the same entity (patient, user, device) in one fold, so the model can't
  memorise an individual and be tested on them.
- **Leave-One-Out** — K = n. Nearly unbiased but very high variance and n model fits; rarely worth it.
- **Nested CV** — an inner loop tunes hyperparameters, an outer loop estimates performance. Use it when you'd
  otherwise be reporting the tuned score as your performance estimate, which is optimistically biased.

**Q67. What's wrong with tuning hyperparameters and then reporting the best CV score?**

> That score is biased upward, because you selected the hyperparameters *using* those folds — you've partly
> fitted to the validation data.

With enough configurations tried, you'll find one that looks good by chance. The fixes: keep a completely
untouched **test set** for the final number, or use **nested cross-validation**. This question separates people
who've read about CV from people who've been burned by it.

**Q68. How do you decide which hyperparameter search to use?**

> Grid search when the space is small and you know the ranges; random search when the space is large; Bayesian
> optimisation when each training run is expensive.

Random search beats grid search in practice because typically only a few hyperparameters matter much — grid
search wastes most of its budget varying the unimportant ones at fixed values of the important ones, while
random search samples many distinct values of every parameter. Sample from log-uniform distributions for
learning rates and regularisation strengths. Bayesian methods (Optuna, Hyperopt) build a surrogate model of the
score surface and choose the next trial intelligently; combine with **early stopping / pruning** to kill bad
trials fast.

**Q69. What's a learning curve and how do you read it?** ⭐

> Plot training and validation error against the size of the training set. The shape tells you whether more data
> will help.

- **Both converge to a high error, close together** → high bias. More data will not help. Add capacity or
  better features.
- **Large persistent gap, validation error still falling** → high variance. More data *will* help; so will
  regularisation.
- **Both low and close** → you're in good shape.

Say this instead of guessing when they ask "would more data help?" — it's the diagnostic answer.

**Q70. How do you evaluate a regression model beyond RMSE?**

Compare against a **naive baseline** (predict the mean; for time series, predict the last value) — RMSE alone is
meaningless without that reference. Plot residuals against predictions to check for structure the model missed.
Check whether errors are uniform across segments (a model can be great overall and terrible on the segment that
matters commercially). Use MAE if outliers shouldn't dominate, MAPE if the business thinks in percentages
(watch for near-zero actuals), and quantile loss if you need prediction intervals.

**Q71. Your CV score is 0.85 but production performance is 0.62. What happened?** ⭐

Work through it as a checklist out loud:

1. **Data leakage** — a feature that isn't genuinely available at prediction time. Most common cause.
2. **Train/serve skew** — preprocessing differs between the training pipeline and the serving code.
3. **Distribution shift** — production traffic isn't like the training sample (different time period, different
   user mix).
4. **Target definition drift** — the label meant something slightly different when it was collected.
5. **Temporal validation error** — you shuffled time-series data, so you trained on the future.
6. **Duplicate rows** across the split, inflating CV.

Then say how you'd find it: compare training and production feature distributions column by column, and check
feature importance — if one feature dominates suspiciously, it's usually leakage.

---

## 11. Data problems and applied judgment

**Q72. What is data leakage? Give three concrete examples.** ⭐⭐

> Information that wouldn't be available at prediction time getting into training, producing a great validation
> score that collapses in production.

Examples that are worth naming specifically:
1. **Preprocessing before splitting** — fitting a scaler or imputer on the whole dataset lets test-set
   statistics into training.
2. **A target-derived feature** — e.g. `total_amount_paid` when predicting default, or `discharge_date` when
   predicting hospital admission. The feature exists in the table only *because* the outcome happened.
3. **Temporal leakage** — random-shuffling a time series so future rows train the model that's evaluated on the
   past.
4. **Duplicate or near-duplicate rows** split across train and test.
5. **Group leakage** — the same patient/user appearing in both train and test with different rows.

Prevention: split first, wrap all transformations in a `Pipeline`, use `TimeSeriesSplit`/`GroupKFold`, and be
suspicious of any feature with a near-perfect relationship to the target.

**Q73. How do you handle imbalanced data?** ⭐⭐

> Start with the metric and the threshold before touching the data — most imbalance problems are actually
> metric problems.

In order of what I'd try:
1. **Change the metric** — precision/recall/F1/PR-AUC, not accuracy.
2. **Class weights** — `class_weight='balanced'` makes minority errors cost more. No data distortion, usually
   the best first move.
3. **Threshold tuning** — pick the operating point from the precision-recall curve.
4. **Resampling** — undersample the majority (loses data), oversample the minority (risks overfitting on
   duplicates), or **SMOTE**, which interpolates new synthetic minority points between existing neighbours.
5. **Collect more minority data** if that's possible at all.
6. **Reframe as anomaly detection** if the minority is under ~0.1%.

Two rules to state: apply resampling **inside the CV folds, on training data only**, and always use
**stratified** splits.

**They'll follow up with:** *"What's the downside of SMOTE?"* → It interpolates in feature space, which can
create unrealistic samples (especially with categorical or high-dimensional data), can blur the class boundary
by generating points in overlapping regions, and it doesn't add real information. Class weights are often as
good and simpler.

**Q74. Which models need feature scaling, and which don't?** ⭐

> Anything based on distances, gradients, or variance needs it. Tree-based models don't, because they split on
> thresholds within a single feature at a time.

| Needs scaling | Doesn't need scaling |
|---|---|
| KNN, K-Means, SVM, PCA, LDA | Decision Tree, Random Forest, XGBoost/LightGBM |
| Neural networks | Naive Bayes |
| Linear/logistic regression **with regularisation** | Plain OLS (coefficients just rescale) |

**Standardisation** (z-score) when the data is roughly normal or has outliers; **normalisation** (min-max) when
you need a bounded range, as for image pixels or some neural network inputs; **RobustScaler** (median and IQR)
when outliers are severe.

**Q75. How do you handle missing data properly?** ⭐

> First diagnose *why* it's missing, because that determines whether imputing is safe.

- **MCAR** (missing completely at random) — safe to impute or drop.
- **MAR** (missing at random, given other features) — impute using the other features (KNN imputer, iterative
  imputer).
- **MNAR** (missing not at random — the missingness depends on the unobserved value itself, e.g. high earners
  refusing to state income) — imputing introduces bias. Add a **missingness indicator** and treat the
  missingness as a feature.

Practical rules: median for skewed numeric, mode for categorical or an explicit "Unknown" level, forward-fill
for time series, and always fit the imputer on training data only.

**Q76. How would you approach a problem with only 500 labelled rows?**

> Prefer high-bias models, lean on cross-validation instead of a holdout, and consider transfer learning or
> data augmentation before more modelling.

Concretely: use logistic regression or a shallow tree/small Random Forest, heavy regularisation, few features
(aggressive selection informed by domain knowledge), **repeated stratified k-fold** rather than a single split
(a 100-row test set has huge error bars — quote the confidence interval). Then look outside the model: transfer
learning from a pre-trained model, data augmentation, semi-supervised learning on unlabelled data, active
learning to label the most informative rows next, or simply buying/collecting more labels.

**Q77. How do you decide which features to keep?** ⭐

> Start from domain knowledge, then use methods that account for interactions — not just univariate correlation.

- **Filter** (fast, model-free): variance threshold, correlation with target, chi-square, mutual information.
  Cheap but blind to feature interactions.
- **Wrapper**: recursive feature elimination, forward/backward selection. Accurate, expensive.
- **Embedded**: Lasso, tree importances, or better, **permutation importance** and **SHAP** on a validation set.

Also drop features that leak, that won't be available at serving time, or that are proxies for protected
attributes. And note that removing features is not always good — regularised models handle mild redundancy fine,
and aggressive selection based on the full dataset is itself a form of leakage.

**Q78. When would you choose a simpler model over a more accurate one?** ⭐

> When the gain is small and the cost of complexity is real — explainability, latency, maintenance, or the risk
> of silent failure.

Specifics worth naming: regulated domains (credit, insurance, healthcare) need an explainable decision;
low-latency serving can't afford a 500-tree ensemble; a model retrained weekly by a small team needs to be
debuggable; and a 0.3% AUC gain rarely moves a business metric. Also mention that a simple model is a
**baseline you must always build anyway**, so you'll know the true size of the gain.

**Q79. The business asks for "95% accuracy". How do you respond?**

> Ask what decision the model drives and what a mistake costs in each direction — then propose a metric that
> reflects that, and a baseline to compare against.

Points to make: accuracy may be the wrong metric entirely (class balance); 95% may be unachievable given the
irreducible noise, or trivially achievable and useless; and the real question is whether the model beats the
current process (a rule, or a human) on the business outcome. Offer to define success as "reduce manual review
by X% while keeping fraud caught above Y%" — a statement in their units, not yours.

**Q80. How do you know when a model is ready to deploy?** ⭐

> When it beats the existing baseline on the business metric, on a held-out set that resembles production, and
> you have a way to detect when it stops working.

Checklist to say out loud: performance validated on a **temporally held-out** set (not just random CV);
performance checked per segment, not just in aggregate; the model is calibrated if probabilities are used;
errors reviewed qualitatively (look at the worst mistakes); fairness checked across relevant groups; latency and
cost measured; the full preprocessing pipeline serialised together with the model; monitoring and a retraining
trigger defined; and a rollback plan plus a shadow or canary rollout rather than a full switch.

---

## Rapid-fire round

These get fired at you in quick succession. One line each.

| Question | Answer |
|---|---|
| Classification or regression: predicting temperature? | Regression |
| Generative vs discriminative? | Discriminative models P(y\|x) directly (logistic regression, SVM); generative models P(x,y) and can sample data (Naive Bayes, GMM, GANs) |
| Is Random Forest affected by outliers? | Barely — splits depend on order, not magnitude |
| Does PCA reduce overfitting? | Indirectly, by reducing dimensionality — but it can also drop discriminative signal |
| Can you use MSE for classification? | You can compute it, but cross-entropy trains far better (convex, stronger gradients) |
| Why shuffle before splitting? | Data is often sorted by class or time, so an unshuffled split is unrepresentative |
| Bagging on a stable model — useful? | No. Bagging reduces variance; a low-variance model has little to gain |
| More trees in a Random Forest — overfitting? | No, error plateaus. More boosting rounds *can* overfit |
| Difference between `fit`, `transform`, `fit_transform`? | `fit` learns the parameters, `transform` applies them, `fit_transform` does both — use `fit_transform` on train, `transform` on test |
| Why `random_state`? | Reproducibility — bootstrap samples, shuffling and initialisation are all random |
| One model for tabular data if you could only pick one? | Gradient boosting (XGBoost/LightGBM) — but always baseline against logistic regression first |

---

## What to do with this file

Don't read it linearly the night before. Instead:

1. Cover the answer and try to say each ⭐ question out loud. If you hesitate, mark it.
2. For your marked questions, learn the **explanation**, not the one-liner — the follow-up is where interviews
   are decided.
3. Be able to draw three things on a whiteboard: the bias-variance curve, a confusion matrix with all four
   metrics derived from it, and the L1-diamond vs L2-circle picture.
4. Have a real answer ready for Q7, Q71, Q78 and Q80 taken from your own project. Those four are judgment
   questions, and a specific personal example beats a textbook answer every time.
