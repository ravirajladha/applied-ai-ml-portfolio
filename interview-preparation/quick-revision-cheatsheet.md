# Quick revision cheat sheet

For the last 30 minutes before the interview. Nothing new here — only what is easiest to blank on.

---

## The one-liners you must not fumble

| Term | Say this |
|------|----------|
| AI vs ML vs DL | Nested circles: AI ⊃ ML ⊃ DL. AI = act smart, ML = learn from data, DL = neural nets that learn features too |
| Supervised | Labelled data, learn input → output |
| Unsupervised | No labels, find hidden structure |
| Overfitting | Great on train, poor on test — memorised the noise |
| Underfitting | Poor on both — model too simple |
| Bias | Wrong assumptions → underfits |
| Variance | Too sensitive to the training set → overfits |
| Regularisation | Penalty on large weights to reduce overfitting |
| L1 (Lasso) | Can shrink weights to exactly zero → feature selection |
| L2 (Ridge) | Shrinks weights smoothly, never to zero |
| Cross-validation | K folds, rotate the validation fold, average the score |
| Data leakage | Info from test/future sneaks into training → fake good score |
| Curse of dimensionality | Too many features → sparse data → overfitting |
| Ensemble | Many weak models combined into one strong one |
| Bagging | Parallel, on bootstrap samples → reduces **variance** (Random Forest) |
| Boosting | Sequential, each fixes the last one's errors → reduces **bias** (XGBoost) |
| Kernel trick | Similarity in a higher dimension without computing the mapping |
| Lazy learner | KNN — no training phase, all work at prediction time |
| "Naive" in Naive Bayes | Assumes features are conditionally independent |
| Transfer learning | Reuse a pre-trained model on a new, smaller task |
| Attention | Every token looks at every other token and weights what matters |
| RAG | Retrieve relevant chunks from a vector DB, put them in the prompt |
| Hallucination | Fluent but factually wrong output |
| Model drift | The world changed, so the model's accuracy decayed |

---

## Formulas worth memorising

```
Accuracy    = (TP + TN) / (TP + TN + FP + FN)
Precision   = TP / (TP + FP)        "of what I flagged, how much was right"
Recall      = TP / (TP + FN)        "of all real positives, how many I caught"
F1          = 2 * (P * R) / (P + R)
Specificity = TN / (TN + FP)

MSE  = (1/n) * Σ(y - ŷ)²        RMSE = √MSE        MAE = (1/n) * Σ|y - ŷ|
R²   = 1 - (SS_res / SS_tot)

Sigmoid  σ(z) = 1 / (1 + e^-z)
Entropy       = -Σ p·log₂(p)
Gini          = 1 - Σ p²
Bayes    P(A|B) = P(B|A)·P(A) / P(B)
GD update     w := w - α · ∂L/∂w
Attention     softmax(QKᵀ / √dₖ) · V
```

---

## Decision tables interviewers probe

**Does this model need feature scaling?**

| Needs scaling | Doesn't need scaling |
|---|---|
| KNN, K-Means, SVM, PCA, neural networks, regression with regularisation | Decision Tree, Random Forest, XGBoost, Naive Bayes |

**Which metric?**

| Situation | Metric |
|---|---|
| Balanced classification | Accuracy, ROC-AUC |
| Imbalanced classification | Precision, Recall, F1, **PR-AUC**, confusion matrix |
| False positive is costly (spam filter) | Precision |
| False negative is costly (cancer, fraud) | Recall |
| Regression, outliers present | MAE |
| Regression, big errors must hurt | RMSE |
| Comparing models with different feature counts | Adjusted R² |

**Which activation?**

| Place | Use |
|---|---|
| Hidden layers | ReLU (GELU in Transformers) |
| Binary output | Sigmoid |
| Multi-class output | Softmax |
| Regression output | Linear (none) |

---

## Python / pandas snippets they may ask you to write

```python
df.isnull().sum()                          # missing values per column
df['col'].fillna(df['col'].median(), inplace=True)
df.drop_duplicates(inplace=True)
df.describe(); df.info(); df.corr()

from sklearn.model_selection import train_test_split, cross_val_score
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)        # fit ONLY on train
X_test  = sc.transform(X_test)             # transform test

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print(classification_report(y_test, model.predict(X_test)))

# groupby — very commonly asked
df.groupby('category')['sales'].agg(['mean', 'sum', 'count'])
```

Python trivia that shows up: `list` vs `tuple` (mutable vs immutable), `is` vs `==`,
list comprehension, `*args` / `**kwargs`, shallow vs deep copy, `apply` vs `map` vs vectorised ops.

---

## SQL they usually slip in

```sql
-- second highest salary
SELECT MAX(salary) FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);

-- top earner per department (window function)
SELECT * FROM (
  SELECT name, dept, salary,
         RANK() OVER (PARTITION BY dept ORDER BY salary DESC) rnk
  FROM employees
) t WHERE rnk = 1;

-- find duplicates
SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1;
```

Know: INNER vs LEFT vs RIGHT vs FULL JOIN, `WHERE` (before grouping) vs `HAVING` (after),
`GROUP BY`, `DISTINCT`, and that `RANK` leaves gaps while `DENSE_RANK` doesn't.

---

## If your mind goes blank

Fall back to this structure for *any* "how would you solve X" question:

> **Problem → Data → EDA → Preprocess → Baseline → Model → Evaluate → Deploy → Monitor**

Say the steps out loud and fill in details as you go. Interviewers grade the structure of the thinking, not the
speed of recall.
