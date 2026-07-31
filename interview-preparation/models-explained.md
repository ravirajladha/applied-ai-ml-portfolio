# Every model, explained in four levels

Each model is described at four increasing depths. Read **Level 1** for all of them first to build the map, then
go deeper only where you need to.

| Level | What it gives you | When to use it |
|---|---|---|
| **① The one-liner** | Plain English + an analogy | The opening sentence of your answer |
| **② How it works** | The actual mechanics, step by step | The explanation after they say "go on" |
| **③ The math** | Objective function or formula | When they ask "what is it optimising?" |
| **④ In practice** | Hyperparameters, gotchas, code | When they ask "would you use it here?" |

---

## The map

**Supervised** — you have labels, learn input → output.

| Model | Type | Boundary | Scaling? |
|---|---|---|---|
| [Linear Regression](#1-linear-regression) | Regression | Straight line | Only with regularisation |
| [Ridge / Lasso / Elastic Net](#2-ridge-lasso-and-elastic-net) | Regression | Straight line | **Yes** |
| [Logistic Regression](#3-logistic-regression) | Classification | Straight line | **Yes** |
| [KNN](#4-k-nearest-neighbours-knn) | Both | Any shape | **Yes** |
| [Naive Bayes](#5-naive-bayes) | Classification | Curved | No |
| [SVM](#6-support-vector-machine-svm) | Both | Straight, or any with a kernel | **Yes** |
| [Decision Tree](#7-decision-tree) | Both | Boxes (axis-parallel) | No |
| [Random Forest](#8-random-forest) | Both | Many boxes averaged | No |
| [XGBoost / Gradient Boosting](#9-gradient-boosting--xgboost) | Both | Many boxes stacked | No |
| [Neural Network](#10-neural-network) | Both | Any shape | **Yes** |

**Unsupervised** — no labels, find structure.

| Model | Purpose | Scaling? |
|---|---|---|
| [K-Means](#11-k-means) | Group into k clusters | **Yes** |
| [Hierarchical clustering](#12-hierarchical-clustering) | Nested groups, no k needed | **Yes** |
| [DBSCAN](#13-dbscan) | Arbitrary shapes + outlier detection | **Yes** |
| [PCA](#14-pca) | Compress features | **Yes** |

**The scaling rule in one line:** anything based on **distance, gradients, or variance** needs scaling. Trees
don't, because they only ever compare values *within* one feature at a time.

---

## 1. Linear Regression

### ① The one-liner
> It draws the straight line that sits as close as possible to all your data points, and uses that line to
> predict.

Analogy: you're plotting house price against size. You lay a ruler across the scatter of dots so the total
distance from the dots to the ruler is as small as possible. That ruler is your model.

### ② How it works
1. Guess a line: `price = β₀ + β₁ × size`.
2. For every house, measure the vertical gap between the real price and the line (the **residual**).
3. Square each gap (so positives and negatives don't cancel, and big misses hurt more).
4. Adjust the line until the total of those squares is as small as it can be.

With more features it's the same thing in more dimensions — a flat plane through a 3-D cloud, or a hyperplane
beyond that.

### ③ The math
```
Prediction:  ŷ = β₀ + β₁x₁ + β₂x₂ + … + βₙxₙ
Cost (MSE):  J = (1/n) Σ (yᵢ - ŷᵢ)²
Solution:    β = (XᵀX)⁻¹Xᵀy          (exact, "normal equation")
        or:  β := β - α·∇J           (iterative, gradient descent)
```
The cost is **convex**, so there is exactly one minimum — no getting stuck.

### ④ In practice
**Assumptions:** linear relationship, independent errors, constant error variance, normally distributed
residuals, no multicollinearity. Check with a residuals-vs-fitted plot — you want a shapeless cloud.

**Interpretation:** "holding everything else constant, one more unit of x changes y by β."

**Watch out for:** outliers (squared error makes them dominate), multicollinearity (unstable coefficients — check
VIF > 10), and the fact that it can't capture curves unless you add polynomial features.

```python
from sklearn.linear_model import LinearRegression
model = LinearRegression().fit(X_train, y_train)
model.coef_, model.intercept_
```

---

## 2. Ridge, Lasso and Elastic Net

### ① The one-liner
> Linear regression with a penalty on large coefficients, so the model can't contort itself to fit every noisy
> point.

Analogy: the ruler from before, but now on a spring. It *can* tilt steeply to chase an odd data point, but the
spring resists — so it only does so if the evidence is strong.

### ② How it works
You add a term to the cost that grows with the size of the coefficients. The model now has to balance two goals:
fit the data, and keep the coefficients small. The parameter **λ** decides how much the second goal matters.

- **Ridge (L2)** penalises the *squares* of the coefficients → shrinks them all smoothly toward zero, never
  reaching it.
- **Lasso (L1)** penalises the *absolute values* → can push coefficients to **exactly zero**, deleting features.
- **Elastic Net** uses both.

### ③ The math
```
Ridge:        J = MSE + λ Σ βⱼ²           closed form: β = (XᵀX + λI)⁻¹Xᵀy
Lasso:        J = MSE + λ Σ |βⱼ|          no closed form → coordinate descent
Elastic Net:  J = MSE + λ₁Σ|βⱼ| + λ₂Σβⱼ²
```

**Why Lasso produces exact zeros:** the L1 constraint region is a **diamond** with sharp corners on the axes;
L2's is a **circle**. The solution is where the loss contours first touch the region — and a diamond is most
likely to be touched at a corner, where a coefficient is exactly 0. A circle has no corners.

### ④ In practice
| | Ridge | Lasso |
|---|---|---|
| Feature selection | No | **Yes** |
| Correlated features | Splits weight between them | Picks one, drops the rest |
| Use when | Many features that all matter a bit; multicollinearity | Many irrelevant features |

**Must scale features first** — otherwise the penalty hits features with large units unfairly. λ is chosen by
cross-validation: λ = 0 is plain linear regression, λ → ∞ shrinks everything to zero.

```python
from sklearn.linear_model import RidgeCV, LassoCV
model = RidgeCV(alphas=[0.01, 0.1, 1, 10, 100]).fit(X_train_scaled, y_train)
```

---

## 3. Logistic Regression

### ① The one-liner
> Despite the name it's a **classifier** — it draws a straight boundary between two classes and reports how
> confident it is on each side.

Analogy: a dimmer switch, not an on/off switch. Far on one side of the line it says "95% spam"; right on the
line it says "50%, I genuinely don't know".

### ② How it works
1. Compute a weighted sum of the features, exactly like linear regression: `z = β₀ + βᵀx`.
2. Squash that number into the range 0–1 with the **sigmoid**, turning it into a probability.
3. Predict class 1 if the probability clears a threshold (0.5 by default — but you should tune it).

### ③ The math
```
z = β₀ + β₁x₁ + … + βₙxₙ
p = σ(z) = 1 / (1 + e⁻ᶻ)

Loss (binary cross-entropy):
J = -(1/n) Σ [ y·log(p) + (1-y)·log(1-p) ]
```
Read the loss as: if the true label is 1, you pay `−log(p)`. Predict 0.99 → pay almost nothing. Predict 0.01 →
pay a lot. Confidently wrong is the expensive mistake.

The model is linear in the **log-odds**: `log(p/(1−p)) = β₀ + βᵀx`, which is why a coefficient β means
"the odds multiply by e^β".

### ④ In practice
**It is a linear model** — the decision boundary is a straight line. For curves you must add polynomial or
interaction features.

**Why not MSE for the loss?** With a sigmoid it becomes non-convex and its gradients vanish when the model is
confidently wrong — so it learns slowest exactly when it should learn fastest.

**Strengths:** fast, interpretable, gives well-calibrated probabilities, a perfect baseline. **Weaknesses:**
can't capture non-linearity on its own; sensitive to outliers and multicollinearity.

```python
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(C=1.0, class_weight='balanced', max_iter=1000)
```
Note: sklearn's `C` is the **inverse** of regularisation strength — smaller C means *more* regularisation.

---

## 4. K-Nearest Neighbours (KNN)

### ① The one-liner
> To classify something new, look at the k most similar examples you've already seen and take a vote.

Analogy: you move to a new street and want to guess the house price. You look at the 5 nearest houses and take
their average. No theory, no formula — just "what do the neighbours look like?"

### ② How it works
There is **no training**. The model just memorises the dataset. At prediction time:
1. Compute the distance from the new point to every training point.
2. Take the k closest.
3. Classification → majority vote. Regression → average.

This is why it's called a **lazy learner**: all the work happens at prediction time, not training time.

### ③ The math
```
Euclidean distance:  d(x, x') = √( Σ (xᵢ - x'ᵢ)² )
Manhattan:           d = Σ |xᵢ - x'ᵢ|
Cosine (for text/embeddings): 1 - (x·x') / (‖x‖‖x'‖)

Prediction = mode (or mean) of the k points with smallest d
```

### ④ In practice
**k controls bias and variance directly:** small k → jagged boundary, follows noise (high variance). Large k →
smooth boundary, eventually just predicts the majority class (high bias). Choose by cross-validation; use an
**odd** k for binary classification to avoid ties.

**You must scale the features.** Salary in rupees and age in years — without scaling, salary dominates the
distance completely and age is ignored.

**Fatal weakness:** the curse of dimensionality. In high dimensions all points become roughly equidistant, so
"nearest" stops meaning anything. Also slow at prediction — O(n) per query, which rules it out for large-scale
low-latency serving.

Interesting connection: **vector databases in RAG systems are industrial-scale KNN** — approximate nearest
neighbour search over millions of embeddings.

```python
from sklearn.neighbors import KNeighborsClassifier
model = KNeighborsClassifier(n_neighbors=5, weights='distance')  # on SCALED data
```

---

## 5. Naive Bayes

### ① The one-liner
> It uses probability to ask "which class was most likely to have produced these features?", assuming naively
> that all the features are independent.

Analogy: an email contains "free", "winner" and "click". You know spam contains those words often and normal
mail rarely does. You multiply those probabilities together and see which class wins — pretending the words
appear independently of each other, which they obviously don't.

### ② How it works
1. From the training data, count how often each class occurs → the **prior**.
2. Count how often each feature value occurs within each class → the **likelihood**.
3. For a new example, multiply the prior by all the likelihoods, once per class.
4. Predict whichever class scores highest.

### ③ The math
```
Bayes:  P(class | features) = P(features | class) · P(class) / P(features)

Naive assumption (conditional independence):
P(features | class) = P(f₁|class) · P(f₂|class) · … · P(fₙ|class)

So:  predicted class = argmax_c  P(c) · Π P(fᵢ | c)
```
`P(features)` is dropped because it's the same for every class and doesn't change which one wins.

**Laplace smoothing** — if a word never appeared with a class, its probability is 0, and one zero destroys the
entire product. So add a small count to everything:
```
P(word | class) = (count + α) / (total + α·V)      α = 1 typically
```

### ④ In practice
**Why does it work when the assumption is false?** Because for *classification* you only need the correct class
to score highest — you don't need the probabilities to be accurate. Its probability outputs are badly
calibrated (pushed toward 0 and 1), so use the ranking, not the number.

**Variants:** Multinomial (word counts — text), Bernoulli (binary presence), Gaussian (continuous features).

**Strengths:** extremely fast, works with very little data, excellent text-classification baseline, handles high
dimensions well. **Weaknesses:** the independence assumption, poor calibration, and it can't learn feature
interactions at all.

```python
from sklearn.naive_bayes import MultinomialNB
model = MultinomialNB(alpha=1.0).fit(X_tfidf, y_train)
```

---

## 6. Support Vector Machine (SVM)

### ① The one-liner
> It finds the boundary that leaves the widest possible gap between the two classes.

Analogy: you're drawing a line to separate red and blue marbles on a table. Many lines separate them — SVM picks
the one with the most clearance on both sides, so a new marble landing near the boundary is still likely to be
classified correctly.

### ② How it works
1. Find the boundary that maximises the **margin** — the distance to the nearest point of each class.
2. Those nearest points are the **support vectors**. They alone define the boundary; you could delete every
   other training point and get the identical model.
3. If the classes can't be separated cleanly, allow a few violations (a **soft margin**), penalised by `C`.
4. If the data isn't linearly separable at all, apply the **kernel trick**.

**The kernel trick:** imagine red marbles in a ring surrounding blue ones — no straight line works. Now lift the
blue ones upward into a third dimension; suddenly a flat sheet separates them. The kernel computes similarities
*as if* you'd done that lift, without ever actually computing the higher-dimensional coordinates.

### ③ The math
```
Objective:  minimise ½‖w‖²   subject to   yᵢ(wᵀxᵢ + b) ≥ 1

Margin width = 2/‖w‖   →   minimising ‖w‖ maximises the margin

Soft margin:  minimise ½‖w‖² + C·Σξᵢ        ξ = how far a point violates the margin

Kernels:
  Linear      K(x, x') = xᵀx'
  Polynomial  K(x, x') = (γ xᵀx' + r)^d
  RBF         K(x, x') = exp(−γ‖x − x'‖²)      ← the default
```

### ④ In practice
**The two knobs:**
- **C** — penalty for misclassification. Low C = wide margin, more tolerance, more regularisation (may
  underfit). High C = narrow margin, fewer violations (may overfit).
- **gamma** (RBF) — how far one training point's influence reaches. Low gamma = smooth boundary. High gamma =
  boundary wraps individual points → overfits.

Tune them **together** on a log grid; they interact.

**Must scale features.** **Doesn't scale to big data** — roughly O(n²)–O(n³), so it's impractical past ~100k
rows. No native probabilities (needs Platt scaling). Hard to interpret.

**Use it for:** small-to-medium datasets with many features — text classification, bioinformatics. On large
tabular data, gradient boosting has replaced it.

```python
from sklearn.svm import SVC
model = SVC(kernel='rbf', C=1.0, gamma='scale', probability=True)  # on SCALED data
```

---

## 7. Decision Tree

### ① The one-liner
> A flowchart of yes/no questions, learned automatically from the data, that funnels each example down to a
> prediction.

Analogy: how a doctor triages. "Fever above 38°? Yes → cough? Yes → …" Each question splits the remaining
possibilities until you reach a conclusion.

### ② How it works
1. Look at every feature and every possible split point.
2. Score each candidate split by how much **purer** it makes the two resulting groups.
3. Keep the best split, then repeat the process on each side, recursively.
4. Stop when a node is pure, too small, or hits the depth limit. The leaf predicts the majority class (or the
   mean, for regression).

It's **greedy** — it takes the best split now, never reconsidering, so it doesn't find the globally optimal tree.

### ③ The math
```
Gini impurity  = 1 - Σ pᵢ²              0 = pure, 0.5 = worst (binary)
Entropy        = -Σ pᵢ log₂(pᵢ)         0 = pure, 1 = worst (binary)

Information Gain = Impurity(parent) - Σ (nⱼ/n) · Impurity(childⱼ)
```

Worked example — a node with 6 positive, 4 negative:
```
Gini(parent) = 1 - (0.6² + 0.4²) = 0.48
Split → Left [4 pos, 0 neg], Right [2 pos, 4 neg]
Gini(left)  = 0
Gini(right) = 1 - (0.333² + 0.667²) = 0.445
Weighted    = 0.4(0) + 0.6(0.445) = 0.267
Gain        = 0.48 - 0.267 = 0.213
```
Gini vs entropy: near-identical results. Gini is faster (no logarithm) and is the default.

### ④ In practice
**Strengths:** genuinely interpretable (you can print the rules), no scaling needed, handles numeric and
categorical data, captures interactions automatically, robust to outliers.

**Weaknesses:** **overfits badly** if left unpruned; **unstable** (change a few rows and the whole tree can
change); axis-parallel splits struggle with diagonal boundaries; a regression tree **cannot extrapolate** beyond
the range of its training targets.

**Control overfitting with:** `max_depth`, `min_samples_leaf`, `min_samples_split`, `ccp_alpha` (pruning).

The real answer to a single tree's instability is to use many of them — which is the next two models.

```python
from sklearn.tree import DecisionTreeClassifier, plot_tree
model = DecisionTreeClassifier(max_depth=5, min_samples_leaf=10, random_state=42)
```

---

## 8. Random Forest

### ① The one-liner
> Hundreds of decision trees, each trained on a different random slice of the data and features, voting
> together.

Analogy: instead of asking one doctor, you ask 500 — and each one has seen a slightly different set of patients
and is allowed to consider only a random subset of symptoms. Individually they're imperfect; collectively their
mistakes cancel out.

### ② How it works
Two independent sources of randomness, and **both matter**:

1. **Row randomness (bagging)** — each tree trains on its own bootstrap sample (n rows drawn *with
   replacement*, so ~37% of rows are left out).
2. **Feature randomness** — at *every split*, only a random subset of features is even considered.

Then: majority vote (classification) or average (regression).

Why the second one is essential: if one feature is strongly predictive, every tree would split on it first and
all 500 trees would look nearly identical — their errors would be correlated, and averaging correlated errors
gains you nothing. Feature subsampling **decorrelates** the trees. That's the whole trick.

### ③ The math
```
Bootstrap: sample n rows with replacement → ~63.2% unique, ~36.8% out-of-bag
           (the limit of (1 - 1/n)ⁿ → 1/e ≈ 0.368)

max_features default: √p for classification, p/3 for regression

Prediction = mode{ tree₁(x), …, tree_B(x) }   or   (1/B) Σ treeᵢ(x)
```

**Out-of-bag error:** each tree has ~37% of rows it never saw. Score each tree on its own held-out rows and
average — a free, unbiased validation estimate with no separate holdout needed.

### ④ In practice
**Can it overfit?** Adding more trees never causes overfitting — the error just plateaus. (Boosting is
different; more rounds *can* overfit.) A forest of fully-grown trees on small noisy data can still overfit a
little; control with `min_samples_leaf`.

**Key hyperparameters:** `n_estimators` (more is safe, just slower), `max_features` (the real tuning knob),
`max_depth` / `min_samples_leaf`, `class_weight='balanced'`, `n_jobs=-1` for free speed.

**Strengths:** excellent accuracy out of the box, hard to break, no scaling, gives feature importance, handles
mixed data. **Weaknesses:** slow and memory-heavy at prediction, not interpretable, and can't extrapolate.

**Caution on feature importance:** the built-in impurity-based version is biased toward high-cardinality
features. Prefer permutation importance or SHAP.

```python
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=300, max_features='sqrt',
                               min_samples_leaf=2, n_jobs=-1, random_state=42)
```

---

## 9. Gradient Boosting / XGBoost

### ① The one-liner
> Trees built one after another, where each new tree is trained specifically to fix the mistakes the previous
> ones made.

Analogy: a student takes a practice test, marks the wrong answers, and studies only those. Then takes another,
and studies the remaining errors. Each round is small and targeted, but they compound.

Contrast with Random Forest: those trees are built **in parallel and independently**, then averaged. Boosting
trees are built **sequentially and dependently**, then summed.

### ② How it works
1. Start with a trivial prediction (the overall mean).
2. Compute the **residuals** — how wrong you are on each example.
3. Fit a small tree to predict those residuals.
4. Add it to the running prediction, scaled down by the **learning rate**.
5. Repeat, each time targeting whatever error is left.

The learning rate matters enormously: each tree only contributes a fraction (say 5%) of its correction, so no
single tree can dominate and the ensemble improves gradually.

### ③ The math
```
Fₘ(x) = Fₘ₋₁(x) + η · hₘ(x)      η = learning rate, hₘ = the new tree

hₘ is fitted to the NEGATIVE GRADIENT of the loss w.r.t. current predictions
(for squared error, that's just the residual y - ŷ — hence "fit the residuals")

XGBoost's regularised objective:
Obj = Σ L(yᵢ, ŷᵢ) + Σ Ω(treeₖ)      where  Ω(tree) = γT + ½λ‖w‖²
                                            T = number of leaves, w = leaf weights
```

Fitting the *gradient* rather than the raw residual is what generalises the method to any differentiable loss —
log loss, Huber, ranking losses.

### ④ In practice
**Why XGBoost specifically wins on tabular data:**
- Regularisation built into the objective (γ on leaf count, λ on leaf weights) — plain GBM has none.
- Uses the second derivative (Hessian) too, for better split decisions.
- Learns a default direction for **missing values** automatically.
- Parallelised split-finding, early stopping, subsampling.

**The learning rate / n_estimators trade-off:** lower learning rate needs more trees, and that combination
generalises better. The standard recipe is `learning_rate=0.05`, a high `n_estimators`, and **early stopping on
a validation set**.

**Key hyperparameters:** `learning_rate` (0.01–0.1), `max_depth` (3–8 — shallower than a Random Forest's trees),
`subsample`, `colsample_bytree`, `min_child_weight`, `reg_lambda`.

**LightGBM vs XGBoost:** LightGBM grows trees **leaf-wise** (always splitting the highest-loss leaf) rather than
level-wise — much faster on large data, often more accurate, but overfits more easily on small data. **CatBoost**
is strongest when you have heavy categorical features.

```python
from xgboost import XGBClassifier
model = XGBClassifier(n_estimators=1000, learning_rate=0.05, max_depth=5,
                      subsample=0.8, colsample_bytree=0.8,
                      early_stopping_rounds=50, eval_metric='logloss')
model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)
```

---

## 10. Neural Network

### ① The one-liner
> Layers of simple units, each computing a weighted sum and a squash, stacked so that early layers find simple
> patterns and later layers combine them into complex ones.

Analogy: recognising a face. The first layer notices edges. The next combines edges into eyes and noses. The
next combines those into a face. Nobody programmed "eye" — the network discovered that it was a useful
intermediate concept.

### ② How it works
**Forward pass:** input → each layer multiplies by weights, adds a bias, applies a non-linear activation →
output → compare to the truth with a loss function.

**Backward pass (backpropagation):** use the chain rule to work out how much each individual weight contributed
to the error, then nudge every weight slightly in the direction that reduces it.

Repeat over millions of mini-batches. That's the entire algorithm.

**Why the non-linear activation is essential:** without it, stacking layers is pointless —
`W₂(W₁x) = (W₂W₁)x = Wx`, so a hundred layers collapse into one matrix and you're back to a linear model.

### ③ The math
```
Per layer:   z = Wx + b        a = f(z)         f = ReLU, GELU, …

Loss:        MSE (regression)  or  cross-entropy (classification)

Backprop:    ∂L/∂w = ∂L/∂a · ∂a/∂z · ∂z/∂w     (chain rule, layer by layer)

Update:      w := w - α · ∂L/∂w                 (gradient descent)
```

**Output layer must match the task:**

| Task | Units | Activation | Loss |
|---|---|---|---|
| Regression | 1 | none | MSE |
| Binary | 1 | sigmoid | binary cross-entropy |
| Multi-class (one label) | C | softmax | categorical cross-entropy |
| Multi-label (many labels) | C | **sigmoid on each** | BCE per output |

### ④ In practice
**Families:** dense/MLP for tabular, **CNN** for images (parameter sharing + locality), **RNN/LSTM** for
sequences (largely superseded), **Transformer** for text and increasingly everything else.

**The knobs that matter, in order:** learning rate (by far the most important — 1e-3 for Adam is the default
starting point), architecture size, batch size (32–256), regularisation (dropout 0.2–0.5, weight decay),
schedule (cosine decay).

**The debugging move to remember:** if it won't learn, first try to **deliberately overfit 10 samples**. If it
can't drive the loss to near zero on 10 examples, the bug is in your code, not your hyperparameters.

**Honest positioning:** on tabular data, gradient boosting usually beats a neural network with far less effort.
Reach for deep learning when the data is unstructured — images, text, audio — or when you can start from a
pre-trained model.

```python
import torch.nn as nn
model = nn.Sequential(
    nn.Linear(n_features, 128), nn.ReLU(), nn.Dropout(0.3),
    nn.Linear(128, 64), nn.ReLU(),
    nn.Linear(64, n_classes)           # raw logits — CrossEntropyLoss adds softmax
)
```

---

## 11. K-Means

### ① The one-liner
> You tell it how many groups you want, and it finds where the centres of those groups should sit.

Analogy: you're placing k ice-cream vans in a park so everyone's walk is as short as possible. Put them
anywhere, send each person to their nearest van, then move each van to the middle of its own crowd. Repeat until
the vans stop moving.

### ② How it works
1. Pick k starting centroids.
2. **Assign** each point to its nearest centroid.
3. **Update** each centroid to the mean of the points assigned to it.
4. Repeat 2–3 until nothing changes.

That's it — two alternating steps. It always converges, but only to a **local** optimum, so the starting
positions matter.

### ③ The math
```
Objective (inertia / within-cluster sum of squares):
    minimise  Σⱼ Σ_{x ∈ Cⱼ} ‖x - μⱼ‖²

Assignment step: labelᵢ = argminⱼ ‖xᵢ - μⱼ‖²
Update step:     μⱼ = mean of all points with label j
```
This objective is NP-hard, so the algorithm (Lloyd's) is a heuristic. Run it multiple times with different
starts (`n_init=10`) and keep the lowest inertia. **k-means++** initialisation spreads the starting centroids
out probabilistically and works much better than random.

### ④ In practice
**Choosing k:**
- **Elbow method** — plot inertia vs k, look for the bend. (Inertia always decreases, so you can't just
  minimise it.)
- **Silhouette score** — `(b − a)/max(a,b)` per point; pick the k with the highest average. More principled.
- **Business constraint** — marketing wants 4 segments, so k = 4. Often this wins.

**Assumptions and failure modes:** it assumes clusters are **spherical, similarly sized and similarly dense**.
It fails on elongated or crescent shapes, on very different cluster sizes, and on outliers (which drag
centroids). It forces every point into a cluster — there is no "noise" label.

**Must scale features.**

```python
from sklearn.cluster import KMeans
km = KMeans(n_clusters=4, init='k-means++', n_init=10, random_state=42)
labels = km.fit_predict(X_scaled)
km.inertia_, km.cluster_centers_
```

---

## 12. Hierarchical clustering

### ① The one-liner
> It builds a family tree of your data — every point starts alone, then the closest pairs merge, then those
> merge, until everything is one group. You cut the tree wherever you like.

Analogy: a knockout tournament run backwards. The most similar things pair up first, then those pairs pair up,
and the diagram of who joined whom (the **dendrogram**) shows the whole structure at every level of granularity.

### ② How it works
**Agglomerative** (the common direction, bottom-up):
1. Every point is its own cluster.
2. Merge the two closest clusters.
3. Repeat until one cluster remains.
4. Draw the dendrogram; cut it at a height that gives the number of clusters you want.

The big advantage: **you don't have to choose k in advance** — you decide after seeing the structure.

### ③ The math
The "distance between clusters" depends on the **linkage**:
```
Single    = min distance between any two members     → long, chain-like clusters
Complete  = max distance between any two members     → compact, similar-sized clusters
Average   = mean distance between all pairs          → a middle ground
Ward      = merge whichever pair increases within-cluster variance least   ← usually best
```
Complexity is **O(n² log n)** time and O(n²) memory — that's the killer.

### ④ In practice
**Use it when:** the dataset is small (under ~10,000 rows), you want to *see* the structure, the number of
clusters isn't known, or the hierarchy itself is meaningful (taxonomy, gene expression, document topics).

**Don't use it when:** the data is large. It doesn't scale, full stop.

Also note it's **deterministic** (no random initialisation, unlike K-Means) but **greedy** — a merge, once made,
is never undone.

```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
labels = AgglomerativeClustering(n_clusters=4, linkage='ward').fit_predict(X_scaled)
dendrogram(linkage(X_scaled, method='ward'))     # plot to choose the cut
```

---

## 13. DBSCAN

### ① The one-liner
> It finds clusters by looking for dense crowds of points, and anything sitting alone in a sparse region is
> labelled noise rather than forced into a cluster.

Analogy: an aerial photo of a festival. Wherever people are packed together, that's a stage — whatever shape the
crowd happens to be. The few people wandering across empty grass aren't at any stage, and DBSCAN is happy to
say so.

### ② How it works
Two parameters: **eps** (how far is "nearby") and **min_samples** (how many neighbours make a crowd).

Every point is then one of three things:
- **Core point** — has at least `min_samples` neighbours within `eps`.
- **Border point** — within `eps` of a core point, but not dense enough itself.
- **Noise** — neither. Labelled `-1` and left out of every cluster.

Clusters grow by chaining core points together, so a cluster can be any shape at all.

### ③ The math
```
N_eps(p) = { q : distance(p, q) ≤ eps }        the neighbourhood

p is a core point  ⟺  |N_eps(p)| ≥ min_samples

Clusters = connected components of the core points, plus their border points
```
Complexity is O(n log n) with a spatial index, O(n²) without.

### ④ In practice
**What makes it worth knowing:** it discovers k by itself, finds **arbitrary shapes** (the classic two-crescents
dataset that defeats K-Means), and does **outlier detection for free**.

**Choosing eps:** plot each point's distance to its k-th nearest neighbour, sort those distances, and look for
the knee in the curve. Set `min_samples ≈ 2 × dimensions` as a starting rule.

**Its weakness:** clusters of **varying density**. One eps value can't serve both a tight cluster and a loose
one — that's what HDBSCAN was invented to fix. It also degrades in high dimensions, like anything
distance-based, and **needs scaling**.

```python
from sklearn.cluster import DBSCAN
labels = DBSCAN(eps=0.5, min_samples=5).fit_predict(X_scaled)
# labels == -1  →  noise
```

---

## 14. PCA

### ① The one-liner
> It finds new directions to measure your data along — ordered so the first one captures the most variation —
> letting you keep a few and discard the rest with minimal loss.

Analogy: photographing a chair. Shoot it from the front and you get a clear, informative silhouette. Shoot it
from directly above and it's an unreadable blob. PCA finds the most informative angles, and the "informative"
angle is the one along which the data is most spread out.

### ② How it works
1. **Standardise** the features (mandatory — see below).
2. Compute the covariance matrix: how every feature varies with every other.
3. Find its **eigenvectors** and **eigenvalues**. Each eigenvector is a direction (a principal component); its
   eigenvalue is how much variance lies along it.
4. Sort by eigenvalue, keep enough components to reach ~95% of the total variance, and project the data onto
   them.

Each component is a **linear combination of all your original features**, which is why they're not interpretable
as "the age column".

### ③ The math
```
Covariance matrix:   C = (1/n) XᵀX          (on centred X)
Eigen-decomposition: C vᵢ = λᵢ vᵢ

  vᵢ = i-th principal component (direction)
  λᵢ = variance captured along it

Explained variance ratio = λᵢ / Σλⱼ

Projection: X_reduced = X · V_k             V_k = the top k eigenvectors
```
In practice libraries use **SVD** on the centred data instead of forming the covariance matrix — same result,
better numerical stability.

Properties: components are **orthogonal** (uncorrelated) and ordered by variance.

### ④ In practice
**Why standardising is mandatory:** PCA maximises variance, and variance depends on units. A salary column in
rupees will hijack the first component purely because its numbers are large, not because it's informative.

**It's unsupervised** — it never looks at the target. So it can discard a low-variance direction that happened
to separate your classes perfectly. When you have labels and classification is the goal, **LDA** is the
supervised counterpart (maximises class separation, gives at most C−1 components).

**Use it for:** speeding up training, removing multicollinearity, denoising, compression, and 2-D visualisation.

**Don't use it for:** feature *selection* — every original feature still contributes to every component, so you
can't stop collecting any of them. And don't expect interpretability.

```python
from sklearn.decomposition import PCA
pca = PCA(n_components=0.95)          # keep 95% of the variance
X_reduced = pca.fit_transform(X_scaled)
pca.explained_variance_ratio_.cumsum()
```

---

## Choosing between them

**By the data you have:**

| Situation | Reach for |
|---|---|
| Tabular data, any size | **Gradient boosting** (XGBoost/LightGBM) — baseline with logistic regression first |
| Tabular, must explain every decision | Logistic regression, or a shallow decision tree |
| Very few rows (< 1,000) | Logistic/Ridge regression, Naive Bayes, small Random Forest |
| Many features, few rows | SVM, or Lasso |
| Text | Naive Bayes or logistic regression on TF-IDF → then a fine-tuned Transformer |
| Images / audio | CNN, or transfer learning from a pre-trained model |
| Sequences / language | Transformer |
| No labels, want k groups | K-Means |
| No labels, odd shapes or outliers | DBSCAN |
| No labels, want to see structure | Hierarchical clustering |
| Too many features | PCA (or Lasso, if you need to keep the original features) |

**By constraint:**

| Constraint | Choose | Avoid |
|---|---|---|
| Must be interpretable | Linear/logistic regression, single tree | Neural nets, large ensembles |
| Prediction must be fast | Linear models, small trees | KNN, large forests |
| Training must be fast | Naive Bayes, linear models | SVM on large data, deep nets |
| Data has outliers | Tree-based models | Linear regression, K-Means |
| Features are unscaled and you're in a hurry | Tree-based models | Everything distance-based |
| Missing values everywhere | XGBoost/LightGBM (handle them natively) | KNN, SVM |

**The honest default:** start with logistic/linear regression as a baseline, then try gradient boosting. If
neither is good enough, the problem is usually the *features* or the *data*, not the algorithm.

---

## One-line summaries, for memorising

| Model | In one line |
|---|---|
| Linear Regression | Best-fit straight line, minimising squared error |
| Ridge / Lasso | Linear regression with a leash on the coefficients — Lasso can cut them to zero |
| Logistic Regression | Linear boundary, sigmoid output, gives probabilities |
| KNN | Ask the k most similar examples and take a vote |
| Naive Bayes | Multiply probabilities, pretending features are independent |
| SVM | The boundary with the widest gap; kernels bend it |
| Decision Tree | An automatically learned flowchart of yes/no questions |
| Random Forest | Hundreds of trees on random rows *and* random features, averaged |
| XGBoost | Trees added one by one, each fixing the last one's mistakes |
| Neural Network | Layers of weighted sums and squashes, learned by backpropagation |
| K-Means | Move k centres until each sits at the middle of its own crowd |
| Hierarchical | Merge the closest pair repeatedly; cut the resulting tree where you like |
| DBSCAN | Dense crowds are clusters; loners are noise |
| PCA | New axes ordered by how much variation they capture |
