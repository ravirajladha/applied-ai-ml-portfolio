# Coding questions asked in AI/ML interviews — with solutions

The coding round in an AI/ML interview is rarely hard algorithms. It is mostly:
**Python fluency → NumPy vectorisation → pandas data wrangling → implement one ML algorithm from scratch →
a scikit-learn pipeline → a SQL query.**

Every solution below is runnable. ⭐ = very frequently asked.

**Contents**

| # | Section |
|---|---------|
| 1–12 | [Python fundamentals & logic](#1-python-fundamentals--logic) |
| 13–21 | [NumPy](#2-numpy) |
| 22–33 | [Pandas](#3-pandas) |
| 34–44 | [ML algorithms from scratch (NumPy)](#4-ml-algorithms-from-scratch-numpy) |
| 45–50 | [scikit-learn / practical ML](#5-scikit-learn--practical-ml) |
| 51–55 | [SQL](#6-sql) |
| 56–60 | [PyTorch / deep learning](#7-pytorch--deep-learning) |

> **How to behave in a coding round:** say the approach out loud before typing, mention the time complexity, ask
> about edge cases (empty input, duplicates, nulls), and write the brute force first if the optimal escapes you.
> A silent perfect solution scores lower than a narrated good one.

---

## 1. Python fundamentals & logic

**Q1. Reverse a string and check if it is a palindrome.** ⭐

```python
def is_palindrome(s):
    s = ''.join(c.lower() for c in s if c.isalnum())   # ignore case/punctuation
    return s == s[::-1]

print(is_palindrome("A man, a plan, a canal: Panama"))   # True
```
`s[::-1]` is slicing with a step of −1. Two-pointer version is O(n) time, O(1) extra space.

**Q2. Count the frequency of each word in a sentence.** ⭐

```python
from collections import Counter

text = "the quick brown fox jumps over the lazy dog the fox"
counts = Counter(text.lower().split())
print(counts.most_common(3))     # [('the', 3), ('fox', 2), ('quick', 1)]
```
Without `Counter`: build a dict with `d[w] = d.get(w, 0) + 1`. This is also the base of Bag-of-Words.

**Q3. Find duplicate elements in a list.** ⭐

```python
def find_duplicates(nums):
    seen, dupes = set(), set()
    for n in nums:
        if n in seen:
            dupes.add(n)
        seen.add(n)
    return list(dupes)

print(find_duplicates([1, 2, 3, 2, 5, 1]))   # [1, 2]
```
O(n) using a set — a set lookup is O(1) versus O(n) for a list. Say that out loud; it's the point of the question.

**Q4. Find the second largest number in a list without `sort()`.**

```python
def second_largest(nums):
    first = second = float('-inf')
    for n in set(nums):                # set() handles duplicates
        if n > first:
            first, second = n, first
        elif n > second:
            second = n
    return second if second != float('-inf') else None

print(second_largest([10, 5, 20, 20, 8]))   # 10
```

**Q5. Two Sum — return indices of two numbers adding to a target.** ⭐

```python
def two_sum(nums, target):
    seen = {}                          # value -> index
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
    return []

print(two_sum([2, 7, 11, 15], 9))     # [0, 1]
```
Brute force is O(n²); the hash-map version is O(n). Mention both.

**Q6. Check if two strings are anagrams.**

```python
def is_anagram(a, b):
    return sorted(a.lower()) == sorted(b.lower())          # O(n log n)

from collections import Counter
def is_anagram_fast(a, b):
    return Counter(a.lower()) == Counter(b.lower())        # O(n)
```

**Q7. Fibonacci — iterative and memoised.**

```python
def fib_iter(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

from functools import lru_cache
@lru_cache(maxsize=None)
def fib_memo(n):
    return n if n < 2 else fib_memo(n - 1) + fib_memo(n - 2)
```
Plain recursion is O(2ⁿ); memoisation makes it O(n). Interviewers ask this to see if you know why.

**Q8. Flatten a nested list.**

```python
def flatten(lst):
    out = []
    for item in lst:
        if isinstance(item, list):
            out.extend(flatten(item))     # recurse
        else:
            out.append(item)
    return out

print(flatten([1, [2, [3, 4]], 5]))       # [1, 2, 3, 4, 5]
```

**Q9. Remove duplicates while preserving order.**

```python
def dedupe(items):
    seen = set()
    return [x for x in items if not (x in seen or seen.add(x))]
# or, Python 3.7+: list(dict.fromkeys(items))
```

**Q10. list vs tuple vs set vs dict — and the mutable default argument trap.** ⭐

| Type | Ordered | Mutable | Duplicates | Use |
|---|---|---|---|---|
| list | yes | yes | yes | general sequence |
| tuple | yes | **no** | yes | fixed record, dict key |
| set | no | yes | **no** | membership tests, dedupe |
| dict | yes (3.7+) | yes | keys unique | lookups |

```python
def bad(x, items=[]):      # BUG: the list is created ONCE, at definition time
    items.append(x)
    return items
print(bad(1), bad(2))      # [1] [1, 2]  <- shared!

def good(x, items=None):
    items = [] if items is None else items
    items.append(x)
    return items
```

**Q11. What is a generator and why does it matter for ML?**

```python
def read_batches(data, batch_size):
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]     # yields lazily, doesn't build the whole list

for batch in read_batches(range(10), 3):
    print(list(batch))
```
A generator produces values **one at a time** instead of holding them all in memory — exactly how data loaders
stream a dataset too large for RAM.

**Q12. Write a decorator that times a function.**

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start:.4f}s")
        return result
    return wrapper

@timer
def train():
    time.sleep(1)
```
`*args`/`**kwargs` pass through any arguments; a decorator is a function that wraps another function.

---

## 2. NumPy

**Q13. Create, reshape and inspect arrays.**

```python
import numpy as np

a = np.array([[1, 2, 3], [4, 5, 6]])
a.shape, a.ndim, a.dtype, a.size        # (2,3), 2, dtype('int64'), 6
a.reshape(3, 2)                          # reshape
a.reshape(-1)                            # flatten; -1 = "infer this dimension"
np.zeros((2,3)); np.ones(3); np.eye(3); np.arange(0,10,2); np.linspace(0,1,5)
np.random.default_rng(42).normal(0, 1, (2, 3))
```

**Q14. Why is NumPy faster than a Python list?** ⭐

```python
py_list = list(range(1_000_000))
np_arr  = np.arange(1_000_000)

# list: interpreted loop, boxed objects
squares = [x**2 for x in py_list]
# numpy: contiguous typed memory + vectorised C loop (SIMD), ~50-100x faster
squares = np_arr ** 2
```
Three reasons to say: fixed-type **contiguous memory**, operations run in **compiled C** instead of the Python
interpreter, and **no per-element object overhead**.

**Q15. Explain broadcasting.** ⭐

```python
X = np.array([[1, 2, 3], [4, 5, 6]])     # shape (2, 3)
col_mean = X.mean(axis=0)                # shape (3,)
X - col_mean                             # (2,3) - (3,) -> broadcast to (2,3)

X + np.array([[10], [20]])               # (2,3) + (2,1) -> works
```
Rule: compare shapes right to left; dimensions must be equal or one of them must be 1. This is what makes
`(X - mean) / std` work without a loop.

**Q16. Standardise (z-score) each column of a matrix.** ⭐

```python
def standardize(X):
    return (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-8)   # epsilon avoids /0
```
`axis=0` = down the rows (per column/feature), `axis=1` = across the columns (per row). Getting the axis right
is half of what they're testing.

**Q17. Compute pairwise Euclidean distances without a loop.** ⭐

```python
def pairwise_distances(A, B):
    # A: (n, d), B: (m, d) -> (n, m)
    return np.sqrt(((A[:, None, :] - B[None, :, :]) ** 2).sum(axis=2))

# memory-efficient alternative using (a-b)^2 = a^2 - 2ab + b^2
def pairwise_fast(A, B):
    d2 = (A**2).sum(1)[:, None] - 2 * A @ B.T + (B**2).sum(1)[None, :]
    return np.sqrt(np.maximum(d2, 0))
```
`None` (i.e. `np.newaxis`) inserts an axis so broadcasting produces every pair. Backbone of KNN and K-Means.

**Q18. Implement a numerically stable softmax.** ⭐

```python
def softmax(x, axis=-1):
    x = x - np.max(x, axis=axis, keepdims=True)    # subtract max -> prevents overflow
    e = np.exp(x)
    return e / e.sum(axis=axis, keepdims=True)

print(softmax(np.array([1000., 1001., 1002.])))    # works; naive exp() gives inf/nan
```
Subtracting the max doesn't change the result mathematically but stops `exp` overflowing — a classic follow-up.

**Q19. Implement sigmoid and its derivative.**

```python
def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))   # clip avoids overflow warnings

def sigmoid_derivative(z):
    s = sigmoid(z)
    return s * (1 - s)
```

**Q20. One-hot encode labels with NumPy.**

```python
def one_hot(y, num_classes=None):
    y = np.asarray(y).ravel()
    num_classes = num_classes or y.max() + 1
    out = np.zeros((y.size, num_classes))
    out[np.arange(y.size), y] = 1        # fancy indexing
    return out

print(one_hot([0, 2, 1]))
```

**Q21. Boolean masking, `where`, and top-k with `argsort`.**

```python
a = np.array([3, 8, 1, 9, 5])
a[a > 4]                       # array([8, 9, 5])   boolean mask
np.where(a > 4, a, 0)          # array([0, 8, 0, 9, 5])  vectorised if-else
np.argsort(a)[::-1][:3]        # indices of top 3 -> [3, 1, 4]
np.argmax(a), np.argmin(a)     # 3, 2
np.clip(a, 2, 6)               # cap values into a range
```

---

## 3. Pandas

Assume `df = pd.read_csv('data.csv')`.

**Q22. First five things you run on a new dataset.** ⭐

```python
df.head(); df.shape; df.info(); df.describe(); df.dtypes
df.isnull().sum()                          # missing per column
df.duplicated().sum()                      # duplicate rows
df['target'].value_counts(normalize=True)  # class balance
df.corr(numeric_only=True)                 # correlations
```

**Q23. Handle missing values.** ⭐

```python
df.isnull().sum() / len(df) * 100          # % missing per column
df.dropna(subset=['important_col'])        # drop rows missing a key field
df = df.drop(columns=['mostly_empty_col']) # drop a useless column

df['age'] = df['age'].fillna(df['age'].median())        # numeric, skewed -> median
df['city'] = df['city'].fillna(df['city'].mode()[0])    # categorical -> mode
df['sales'] = df['sales'].ffill()                        # time series -> forward fill
df['age_missing'] = df['age'].isnull().astype(int)       # missingness as a feature
```

**Q24. `loc` vs `iloc`, and filtering rows.** ⭐

```python
df.loc[0, 'salary']                  # label-based
df.iloc[0, 3]                        # integer position-based
df[df['salary'] > 50000]
df[(df['salary'] > 50000) & (df['dept'] == 'IT')]     # & | ~ , parentheses required
df[df['dept'].isin(['IT', 'HR'])]
df.query("salary > 50000 and dept == 'IT'")
```

**Q25. groupby with aggregation.** ⭐

```python
df.groupby('dept')['salary'].mean()
df.groupby('dept').agg(avg_sal=('salary', 'mean'),
                       headcount=('emp_id', 'count'),
                       top_sal=('salary', 'max')).reset_index()
df.groupby(['dept', 'gender'])['salary'].mean().unstack()
```

**Q26. Add a column with the group average, keeping every row (`transform`).**

```python
df['dept_avg'] = df.groupby('dept')['salary'].transform('mean')
df['above_avg'] = df['salary'] > df['dept_avg']
```
`agg` collapses to one row per group; **`transform` keeps the original shape** — a favourite distinction.

**Q27. Rank within a group / top-N per group.**

```python
df['rank_in_dept'] = df.groupby('dept')['salary'].rank(ascending=False, method='dense')
top3 = df.sort_values('salary', ascending=False).groupby('dept').head(3)
```

**Q28. Merge / join two DataFrames.** ⭐

```python
pd.merge(emp, dept, on='dept_id', how='inner')    # only matching rows
pd.merge(emp, dept, on='dept_id', how='left')     # all of emp, NaN where no match
pd.merge(emp, dept, left_on='d_id', right_on='dept_id', how='outer')
pd.concat([df1, df2], axis=0)                     # stack rows
```
`how`: inner / left / right / outer. Always check `len()` before and after — a many-to-many merge silently
duplicates rows.

**Q29. Pivot table / crosstab.**

```python
df.pivot_table(index='dept', columns='gender', values='salary',
               aggfunc='mean', fill_value=0)
pd.crosstab(df['dept'], df['gender'])
```

**Q30. `apply` vs `map` vs vectorised operations.** ⭐

```python
df['band'] = df['salary'].map({50000: 'low', 90000: 'high'})   # Series, dict/function
df['bonus'] = df.apply(lambda r: r['salary'] * (0.2 if r['dept'] == 'IT' else 0.1), axis=1)
df['tax'] = df['salary'] * 0.3                                  # vectorised — fastest
```
Prefer vectorised operations; `apply(axis=1)` loops in Python and is slow on large data. Say that.

**Q31. Extract features from a date column.** ⭐

```python
df['date'] = pd.to_datetime(df['date'])
df['year']       = df['date'].dt.year
df['month']      = df['date'].dt.month
df['dayofweek']  = df['date'].dt.dayofweek        # 0 = Monday
df['is_weekend'] = df['dayofweek'].isin([5, 6]).astype(int)
df['days_since'] = (pd.Timestamp.today() - df['date']).dt.days
```

**Q32. Rolling window / time-series aggregation.**

```python
df = df.sort_values('date')
df['ma_7']  = df['sales'].rolling(window=7).mean()
df['lag_1'] = df['sales'].shift(1)                 # previous day — a lag feature
df['pct_change'] = df['sales'].pct_change()
monthly = df.set_index('date')['sales'].resample('M').sum()
```
Note: `shift(1)` looks **backwards**; using future values here is the classic time-series data leak.

**Q33. Remove outliers using the IQR rule.** ⭐

```python
def remove_outliers_iqr(df, col):
    q1, q3 = df[col].quantile([0.25, 0.75])
    iqr = q3 - q1
    low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return df[(df[col] >= low) & (df[col] <= high)]
```

---

## 4. ML algorithms from scratch (NumPy)

This is the section that decides ML-specific interviews. Be able to write **at least** linear regression,
logistic regression, KNN and K-Means without help.

**Q34. Implement train-test split from scratch.**

```python
def train_test_split(X, y, test_size=0.2, seed=42):
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(X))
    cut = int(len(X) * (1 - test_size))
    tr, te = idx[:cut], idx[cut:]
    return X[tr], X[te], y[tr], y[te]
```
Shuffle **before** splitting (data is often sorted by class); fix the seed for reproducibility.

**Q35. Linear Regression with gradient descent.** ⭐⭐

```python
def linear_regression_gd(X, y, lr=0.01, epochs=1000):
    n, d = X.shape
    w, b = np.zeros(d), 0.0
    history = []
    for _ in range(epochs):
        y_pred = X @ w + b                     # forward
        error  = y_pred - y
        loss   = (error ** 2).mean()           # MSE
        dw = (2 / n) * (X.T @ error)           # gradients
        db = (2 / n) * error.sum()
        w -= lr * dw                           # update
        b -= lr * db
        history.append(loss)
    return w, b, history
```
Narrate it as **predict → measure error → compute gradient → step downhill**. If the loss increases, the
learning rate is too high. Standardise X first or convergence is painful.

**Q36. Linear Regression via the Normal Equation.**

```python
def linear_regression_normal(X, y):
    X_b = np.c_[np.ones(len(X)), X]                    # add bias column
    return np.linalg.pinv(X_b.T @ X_b) @ X_b.T @ y     # (XᵀX)⁻¹Xᵀy
```
Closed form, no learning rate — but O(d³), so it's impractical beyond a few thousand features. `pinv` handles
singular matrices caused by multicollinearity.

**Q37. Logistic Regression from scratch.** ⭐⭐

```python
def logistic_regression(X, y, lr=0.1, epochs=1000):
    n, d = X.shape
    w, b = np.zeros(d), 0.0
    for _ in range(epochs):
        z = X @ w + b
        p = 1 / (1 + np.exp(-z))                       # sigmoid
        # binary cross-entropy loss (for monitoring)
        # loss = -np.mean(y*np.log(p+1e-9) + (1-y)*np.log(1-p+1e-9))
        dw = (X.T @ (p - y)) / n                       # note: same form as linear!
        db = (p - y).mean()
        w -= lr * dw
        b -= lr * db
    return w, b

def predict(X, w, b, threshold=0.5):
    return (1 / (1 + np.exp(-(X @ w + b))) >= threshold).astype(int)
```
Nice thing to point out: with the sigmoid + cross-entropy pairing, the gradient simplifies to `Xᵀ(p − y)/n` —
the same shape as linear regression's.

**Q38. K-Nearest Neighbours from scratch.** ⭐

```python
def knn_predict(X_train, y_train, X_test, k=3):
    preds = []
    for x in X_test:
        dist = np.sqrt(((X_train - x) ** 2).sum(axis=1))   # Euclidean to all points
        nearest = np.argsort(dist)[:k]
        preds.append(np.bincount(y_train[nearest]).argmax())  # majority vote
    return np.array(preds)
```
Mention: scale the features first, use odd k to avoid ties, and prediction is O(n·d) per query — that's why KNN
is slow at inference.

**Q39. K-Means from scratch.** ⭐⭐

```python
def kmeans(X, k, max_iters=100, seed=42):
    rng = np.random.default_rng(seed)
    centroids = X[rng.choice(len(X), k, replace=False)]     # 1. init
    for _ in range(max_iters):
        d = np.linalg.norm(X[:, None, :] - centroids[None, :, :], axis=2)
        labels = d.argmin(axis=1)                            # 2. assign
        new_c = np.array([X[labels == j].mean(axis=0) if np.any(labels == j)
                          else centroids[j] for j in range(k)])   # 3. update
        if np.allclose(new_c, centroids):                    # 4. converged?
            break
        centroids = new_c
    inertia = ((X - centroids[labels]) ** 2).sum()
    return centroids, labels, inertia
```
Handle the empty-cluster case (shown above) — interviewers look for it.

**Q40. Confusion matrix, precision, recall, F1 from scratch.** ⭐

```python
def classification_metrics(y_true, y_pred):
    tp = np.sum((y_true == 1) & (y_pred == 1))
    tn = np.sum((y_true == 0) & (y_pred == 0))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))

    accuracy  = (tp + tn) / len(y_true)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall    = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return dict(confusion=[[tn, fp], [fn, tp]], accuracy=accuracy,
                precision=precision, recall=recall, f1=f1)
```
Guard the zero denominators — that's the bug they're watching for.

**Q41. RMSE, MAE and R² from scratch.**

```python
def regression_metrics(y, y_pred):
    mae  = np.abs(y - y_pred).mean()
    mse  = ((y - y_pred) ** 2).mean()
    rmse = np.sqrt(mse)
    r2   = 1 - ((y - y_pred) ** 2).sum() / ((y - y.mean()) ** 2).sum()
    return mae, rmse, r2
```

**Q42. Entropy and information gain (the decision-tree split).**

```python
def entropy(y):
    _, counts = np.unique(y, return_counts=True)
    p = counts / counts.sum()
    return -(p * np.log2(p)).sum()

def information_gain(y, y_left, y_right):
    n = len(y)
    weighted = (len(y_left)/n) * entropy(y_left) + (len(y_right)/n) * entropy(y_right)
    return entropy(y) - weighted
```
A tree tries every feature/threshold and keeps the split with the highest information gain.

**Q43. Cosine similarity and top-k retrieval (the RAG question).** ⭐

```python
def cosine_similarity(a, b):
    return (a @ b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)

def top_k_similar(query_vec, doc_matrix, k=3):
    # normalise once, then a single matrix multiply = all similarities
    docs = doc_matrix / (np.linalg.norm(doc_matrix, axis=1, keepdims=True) + 1e-9)
    q    = query_vec / (np.linalg.norm(query_vec) + 1e-9)
    scores = docs @ q
    idx = np.argsort(scores)[::-1][:k]
    return idx, scores[idx]
```
This *is* the retrieval step of RAG — a vector database does exactly this, just with an approximate-nearest-
neighbour index over millions of vectors. Cosine is preferred over Euclidean for embeddings because it ignores
magnitude and compares direction (meaning).

**Q44. Min-max and standard scalers as reusable classes.**

```python
class StandardScaler:
    def fit(self, X):
        self.mean_, self.std_ = X.mean(axis=0), X.std(axis=0) + 1e-8
        return self
    def transform(self, X):
        return (X - self.mean_) / self.std_
    def fit_transform(self, X):
        return self.fit(X).transform(X)
```
Key point to say aloud: **`fit` on train only, `transform` on test** — fitting on the full data is leakage.

---

## 5. scikit-learn / practical ML

**Q45. Build a complete pipeline with mixed column types.** ⭐

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

num_cols = ['age', 'salary']
cat_cols = ['dept', 'city']

num_pipe = Pipeline([('imp', SimpleImputer(strategy='median')),
                     ('sc',  StandardScaler())])
cat_pipe = Pipeline([('imp', SimpleImputer(strategy='most_frequent')),
                     ('ohe', OneHotEncoder(handle_unknown='ignore'))])

pre = ColumnTransformer([('num', num_pipe, num_cols),
                         ('cat', cat_pipe, cat_cols)])

model = Pipeline([('pre', pre),
                  ('clf', RandomForestClassifier(n_estimators=200, random_state=42))])
model.fit(X_train, y_train)
```
Why a pipeline: every transformation is fitted **inside** each CV fold, so it is leak-proof, and the whole thing
serialises as one object for deployment. `handle_unknown='ignore'` stops unseen categories crashing production.

**Q46. Cross-validation and hyperparameter tuning.** ⭐

```python
from sklearn.model_selection import StratifiedKFold, cross_val_score, GridSearchCV

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
print(cross_val_score(model, X, y, cv=cv, scoring='f1').mean())

params = {'clf__n_estimators': [100, 300],
          'clf__max_depth': [None, 10, 20],
          'clf__min_samples_leaf': [1, 5]}
gs = GridSearchCV(model, params, cv=cv, scoring='f1', n_jobs=-1)
gs.fit(X_train, y_train)
print(gs.best_params_, gs.best_score_)
```
Note the `clf__` prefix — that's how you address a step inside a pipeline. Use `RandomizedSearchCV` when the grid
is large.

**Q47. Handle an imbalanced dataset in code.** ⭐

```python
# 1. class weights — no data change, usually try this first
RandomForestClassifier(class_weight='balanced', random_state=42)

# 2. SMOTE — synthesise minority samples INSIDE the pipeline (train folds only)
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
pipe = ImbPipeline([('pre', pre), ('smote', SMOTE(random_state=42)),
                    ('clf', RandomForestClassifier(random_state=42))])

# 3. tune the decision threshold instead of using 0.5
from sklearn.metrics import precision_recall_curve
probs = model.predict_proba(X_test)[:, 1]
p, r, thr = precision_recall_curve(y_test, probs)
f1 = 2 * p * r / (p + r + 1e-9)
best_threshold = thr[f1[:-1].argmax()]
```
Never apply SMOTE before the split — that leaks synthetic minority points into the test set.

**Q48. Evaluate a classifier properly.**

```python
from sklearn.metrics import (classification_report, confusion_matrix,
                             roc_auc_score, average_precision_score)

y_pred  = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
print("ROC-AUC:", roc_auc_score(y_test, y_proba))
print("PR-AUC :", average_precision_score(y_test, y_proba))   # better when imbalanced
```

**Q49. Get feature importance and explain a prediction.**

```python
importances = pd.Series(model.named_steps['clf'].feature_importances_,
                        index=model.named_steps['pre'].get_feature_names_out()
                        ).sort_values(ascending=False)
print(importances.head(10))

# model-agnostic and more trustworthy:
from sklearn.inspection import permutation_importance
perm = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=42)

# per-prediction explanation:
# import shap; shap.TreeExplainer(clf).shap_values(X_test)
```
Tree `feature_importances_` is biased toward high-cardinality features — mention permutation importance or SHAP
as the better alternative.

**Q50. Save and load a model for deployment.**

```python
import joblib
joblib.dump(model, 'model.pkl')          # save the WHOLE pipeline, not just the estimator
model = joblib.load('model.pkl')

# minimal serving API
from fastapi import FastAPI
import pandas as pd
app = FastAPI()

@app.post("/predict")
def predict(payload: dict):
    df = pd.DataFrame([payload])
    return {"prediction": int(model.predict(df)[0]),
            "probability": float(model.predict_proba(df)[0, 1])}
```
Pin your library versions — a pickle saved with one scikit-learn version may not load in another.

---

## 6. SQL

**Q51. Second highest salary.** ⭐

```sql
-- subquery version
SELECT MAX(salary) FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);

-- window function version (handles Nth easily)
SELECT DISTINCT salary FROM (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
  FROM employees
) t WHERE rnk = 2;
```

**Q52. Highest paid employee per department.** ⭐

```sql
SELECT name, dept, salary FROM (
  SELECT name, dept, salary,
         RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS rnk
  FROM employees
) t
WHERE rnk = 1;
```
`RANK` leaves gaps after ties (1,1,3), `DENSE_RANK` doesn't (1,1,2), `ROW_NUMBER` never ties.

**Q53. Find and remove duplicate rows.**

```sql
SELECT email, COUNT(*) AS c
FROM users GROUP BY email HAVING COUNT(*) > 1;

DELETE FROM users
WHERE id NOT IN (SELECT MIN(id) FROM users GROUP BY email);
```

**Q54. Departments with more than 5 employees and average salary above 60k.**

```sql
SELECT dept, COUNT(*) AS headcount, AVG(salary) AS avg_salary
FROM employees
WHERE status = 'active'          -- WHERE filters rows BEFORE grouping
GROUP BY dept
HAVING COUNT(*) > 5 AND AVG(salary) > 60000   -- HAVING filters groups AFTER
ORDER BY avg_salary DESC;
```

**Q55. JOIN types — and find rows with no match.** ⭐

```sql
SELECT e.name, d.dept_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id
WHERE d.dept_id IS NULL;         -- employees with no department
```
INNER = only matches; LEFT = all left rows; RIGHT = all right rows; FULL OUTER = everything.
`LEFT JOIN … WHERE right IS NULL` is the standard "find the unmatched" idiom.

---

## 7. PyTorch / deep learning

**Q56. Define a simple neural network.** ⭐

```python
import torch
import torch.nn as nn

class Net(nn.Module):
    def __init__(self, in_features, hidden=64, n_classes=2):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, hidden), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(hidden, hidden // 2), nn.ReLU(),
            nn.Linear(hidden // 2, n_classes)      # raw logits, no softmax here
        )
    def forward(self, x):
        return self.net(x)
```
`nn.CrossEntropyLoss` applies log-softmax internally, so the final layer outputs **logits** — adding a softmax
yourself is a common bug.

**Q57. Write the training loop.** ⭐⭐

```python
model = Net(in_features=20)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

for epoch in range(epochs):
    model.train()                                  # enables dropout / batchnorm updates
    for xb, yb in train_loader:
        optimizer.zero_grad()                      # 1. clear old gradients
        out  = model(xb)                           # 2. forward
        loss = criterion(out, yb)                  # 3. loss
        loss.backward()                            # 4. backprop
        optimizer.step()                           # 5. update weights

    model.eval()                                   # disables dropout
    with torch.no_grad():                          # no gradient tracking = faster, less memory
        correct = sum((model(xb).argmax(1) == yb).sum().item() for xb, yb in val_loader)
    print(epoch, correct / len(val_loader.dataset))
```
The five lines in order are the answer they want. Forgetting `zero_grad()` makes gradients accumulate across
batches — the single most asked PyTorch gotcha, along with `model.train()` vs `model.eval()`.

**Q58. Custom Dataset and DataLoader.**

```python
from torch.utils.data import Dataset, DataLoader

class TabularDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.long)
    def __len__(self):
        return len(self.X)
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

train_loader = DataLoader(TabularDataset(X_train, y_train),
                          batch_size=32, shuffle=True)
```
The three required methods are `__init__`, `__len__`, `__getitem__`. Shuffle the training loader, not the
validation one.

**Q59. Transfer learning — freeze a backbone and swap the head.** ⭐

```python
from torchvision import models

model = models.resnet18(weights='IMAGENET1K_V1')
for p in model.parameters():
    p.requires_grad = False                        # freeze the pre-trained backbone

model.fc = nn.Linear(model.fc.in_features, num_classes)   # new head, trainable by default

optimizer = torch.optim.Adam(
    [p for p in model.parameters() if p.requires_grad], lr=1e-3)
```
To fine-tune instead, unfreeze the last block(s) and drop the learning rate to ~1e-4/1e-5.

**Q60. Implement scaled dot-product attention.** ⭐ *(asked whenever GenAI is on the JD)*

```python
import numpy as np

def attention(Q, K, V, mask=None):
    d_k = Q.shape[-1]
    scores = Q @ K.transpose(-2, -1) / np.sqrt(d_k)   # (seq, seq) relevance scores
    if mask is not None:
        scores = np.where(mask, scores, -1e9)         # causal mask for decoders
    weights = softmax(scores, axis=-1)                # rows sum to 1
    return weights @ V, weights
```
Be ready to explain each piece: Q = what I'm looking for, K = what I offer, V = what I carry; `√d_k` keeps the
softmax from saturating; the mask hides future tokens in a decoder.

---

## Debugging questions they slip in

| They say | You say |
|---|---|
| "Training loss won't go down." | Learning rate too low/high, bad initialisation, features not scaled, labels misaligned, model too small. Try overfitting 10 samples deliberately — if it can't, there's a bug, not a data problem. |
| "Loss is NaN." | Learning rate too high, `log(0)` or divide-by-zero, exploding gradients → clip them, or unstable softmax/exp. |
| "Train accuracy 99%, test 60%." | Overfitting or leakage. Check for duplicate rows across splits and target leakage first, then regularise. |
| "Validation accuracy is *higher* than training." | Dropout is active during training only, or the validation set is easier/smaller. Usually not a bug. |
| "The model is great offline, terrible in production." | Train/serve skew: different preprocessing at serve time, drift, or leakage in the offline features. |
| "It works but takes 3 hours." | Vectorise instead of looping, subsample for iteration, reduce features, use `n_jobs=-1`, batch the data. |

---

## Practice plan

If you only have a couple of hours, hand-write these five, from a blank file, without looking:

1. **Q35** linear regression with gradient descent
2. **Q37** logistic regression
3. **Q39** K-Means
4. **Q40** precision / recall / F1 from the confusion matrix
5. **Q45 + Q57** a scikit-learn pipeline and a PyTorch training loop

Everything else in this file is recall; those five are the ones that get typed live.
