# Features, Labels & Data: coverage spec

**Ladder:** L1 · ML Fundamentals › Core Ideas   ·   **Prerequisites:** `ml-what`, basic pandas
**Why it matters for AI/ML:** Models are only as good as the data fed to them. Most production ML bugs are data bugs: leakage from scaling on all data, wrong encodings, silent missing values, imbalanced classes, shifted distributions. Interviewers probe this heavily because it separates people who have shipped models from people who have only run tutorials.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `features-labels` | Features vs labels (X and y) | what X and y are | splitting a DataFrame into X, y; `train_test_split` sizes | stratified splits | features that are proxies for the label |
| 2 | `data-kinds` | Tabular, text, image, time-series data | recognise each kind | image array shapes; text must be tokenised | time-series lags; never shuffle-split time | grouped / temporal splits to avoid leakage |
| 3 | `feature-types` | Numeric and categorical (nominal vs ordinal) | numeric vs categorical | nominal vs ordinal; IDs/zip codes are categorical | high-cardinality categoricals | cyclical features (hour, month) |
| 4 | `encoding` | Encoding categoricals | why encode | one-hot shapes, `get_dummies` | OrdinalEncoder's alphabetical order; unseen categories | target encoding leakage and cross-fitting |
| 5 | `scaling` | Scaling | why scale | StandardScaler vs MinMaxScaler outputs | fit on train only; which models need scaling | scaler inside a pipeline in CV |
| 6 | `missing` | Missing data | what NaN means | `isna`, SimpleImputer; pandas vs NumPy mean | add a missing-indicator; impute after split | missing-not-at-random |
| 7 | `outliers` | Outliers | what an outlier is | mean vs median; IQR rule | RobustScaler; error vs real extreme | when to keep outliers (fraud) |
| 8 | `imbalance` | Class imbalance | what imbalance is | accuracy paradox; stratify | class weights; resample only the training set | threshold moving and calibration |
| 9 | `quality` | Data quality and label noise | garbage in, garbage out | duplicates, conflicting labels | label noise effects; train/test duplicates | auditing labels; confident learning idea |
| 10 | `feature-eng` | Feature engineering and the curse of dimensionality | creating a new useful column | date parts, ratios, log transform | why distances break in high dimensions | feature selection vs more data |
| 11 | `shift` | Sampling bias and dataset shift | sample must look like the real world | sampling bias examples | covariate vs label vs concept shift | detecting shift (adversarial validation) |
| 12 | `versioning` | Data versioning and lineage | — | — | why data needs versioning like code | content hashing, DVC-style pointers, reproducibility |

## Must-know facts
- X = features (inputs, one column each); y = label/target (what you predict). One row = one example.
- Tabular, text, image and time-series data all end up as numbers; images are arrays (H, W, C), text becomes token IDs.
- Nominal categories have no order (city); ordinal categories do (low < medium < high).
- One-hot makes one 0/1 column per category; `drop="first"` makes k-1.
- `OneHotEncoder` raises on unseen categories by default; `handle_unknown="ignore"` gives an all-zeros row.
- `OrdinalEncoder` sorts categories alphabetically unless you pass `categories=`.
- Target encoding replaces a category with the mean label for it; done naively it leaks the label. sklearn's `TargetEncoder.fit_transform` uses cross-fitting, so it differs from `fit().transform()`.
- StandardScaler: (x - mean) / std with population std (ddof=0). MinMaxScaler maps the TRAIN min/max to 0/1; test values can fall outside [0, 1].
- Fit scalers, imputers and encoders on the training set only, then transform val/test.
- Tree models don't need scaling; distance- and gradient-based models (kNN, SVM, linear, neural nets) do.
- pandas `mean()` skips NaN; NumPy `np.mean` returns nan.
- Outliers pull the mean, not the median. IQR rule: outside [Q1 - 1.5 IQR, Q3 + 1.5 IQR].
- With 99:1 imbalance, predicting the majority class gives 99% accuracy: use recall/precision/PR-AUC.
- Resample (over/undersample, SMOTE) only the training data, never the test set.
- `class_weight="balanced"` weights class c by n_samples / (n_classes * count_c).
- `train_test_split` rounds the test size up (ceil).
- Never shuffle-split time series; train on the past, test on the future.
- In high dimensions, distances between random points become nearly equal (curse of dimensionality).
- Covariate shift: p(x) changes; label shift: p(y) changes; concept drift: p(y|x) changes.
- Version data like code: hash the content, record which data + code produced each model.

## Common traps (each one must have at least one question)
- "Scale the whole dataset before splitting" -> test statistics leak into training.
- "Label-encode a nominal category as 0, 1, 2 for a linear model" -> invents a fake order and distance.
- "OrdinalEncoder keeps my order low < medium < high" -> it sorts alphabetically (high, low, medium).
- "OneHotEncoder handles new categories at inference" -> by default it raises ValueError.
- "Target-encode with the full training labels" -> leaks the label; use cross-fitting/smoothing.
- "Min-max scaled test data is always in [0, 1]" -> only the training data is.
- "StandardScaler uses the sample std (ddof=1)" -> it uses ddof=0.
- "Zip code / user ID is numeric so treat it as a number" -> it's a categorical identifier.
- "Fill missing values with 0 always" -> 0 may be a real value; consider mean/median plus an indicator.
- "np.mean ignores NaN like pandas" -> it returns nan.
- "Delete all outliers" -> some are the signal (fraud) or real extremes.
- "99% accuracy is great" on 99:1 data -> it may be predicting the majority class only.
- "Oversample before splitting" -> duplicates leak into the test set.
- "Random split time-series data" -> future leaks into training.
- "More features always help" -> curse of dimensionality, noise, overfitting.
- "test_size=0.25 of 10 rows gives 2 test rows" -> sklearn rounds up to 3.
- "A dataset collected from app users represents all customers" -> sampling bias.
- "Duplicates across train and test are harmless" -> they inflate the test score.

## Interview angle
- **How do you handle categorical features?** One-hot for low-cardinality nominal, ordinal encoding with an explicit order for ordinal, target/hash encoding or embeddings for high cardinality, with cross-fitting to avoid leakage.
- **Why fit the scaler only on training data?** Test data stands in for the future; using its mean/std leaks information and inflates scores. Put preprocessing in a Pipeline so CV handles it automatically.
- **How do you deal with class imbalance?** Pick the right metric first (recall, PR-AUC), stratify splits, then use class weights or resample the training set only, and tune the decision threshold.
- **What is dataset shift and how do you detect it?** The production distribution differs from training (covariate, label or concept shift). Monitor feature distributions, train a classifier to tell train from prod (adversarial validation), and track live accuracy when labels arrive.
- **How do you make an ML experiment reproducible?** Version the data (content hashes / DVC), the code (git), the config and seeds, and record which data version trained each model.

## Source material
To be added
