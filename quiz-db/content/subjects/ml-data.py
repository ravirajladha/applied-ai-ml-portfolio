from helpers import mcq, tf, out, fill

SUBJECT = "ml-data"

TOPICS = [
    ("features-labels", "Features vs labels (X and y)"),
    ("data-kinds", "Tabular, text, image, time-series data"),
    ("feature-types", "Numeric and categorical (nominal vs ordinal)"),
    ("encoding", "Encoding categoricals"),
    ("scaling", "Scaling"),
    ("missing", "Missing data"),
    ("outliers", "Outliers"),
    ("imbalance", "Class imbalance"),
    ("quality", "Data quality and label noise"),
    ("feature-eng", "Feature engineering and the curse of dimensionality"),
    ("shift", "Sampling bias and dataset shift"),
    ("versioning", "Data versioning and lineage"),
]

QUESTIONS = [
    # ------------------------------------------------------------------ L1
    tf("In ML code, X usually holds the input features and y holds the labels (the answers to predict).", True,
       "Think model.fit(X, y).",
       "X is the table of inputs (one column per feature); y is the target column. fit learns the mapping X -> y.",
       topic="features-labels", level=1),
    mcq("For a model that predicts whether a customer will cancel their subscription, which column is a FEATURE (input)?",
        ["Number of logins last month", "Cancelled (yes/no)", "The model's prediction", "The row number"], 0,
        "Features are facts you know before the answer.",
        "Login count is an input fact about the customer. 'Cancelled' is the label you're trying to predict.",
        topic="features-labels", level=1),
    mcq("A folder of 10,000 cat and dog photos is which kind of data?",
        ["Image data", "Tabular data", "Time-series data", "Text data"], 0,
        "What are the files?",
        "Photos are image data. To a model, each one is a grid of pixel numbers.",
        topic="data-kinds", level=1),
    mcq("Hourly electricity usage for a city over two years is best described as:",
        ["Time-series data", "Image data", "Text data", "Unordered tabular data"], 0,
        "The order of the rows matters.",
        "Each value is tied to a time, and the order matters (yesterday influences today). That's time-series data.",
        topic="data-kinds", level=1),
    mcq("Which feature is CATEGORICAL?",
        ["Payment method: card / UPI / cash", "Order value in rupees", "Delivery distance in km", "Number of items"], 0,
        "Categorical = one of a fixed set of named options.",
        "Payment method is a category. The others are numbers you can add or average.",
        topic="feature-types", level=1),
    mcq("T-shirt size (S, M, L, XL) is which kind of categorical feature?",
        ["Ordinal: the categories have a natural order", "Nominal: no order", "Continuous numeric", "Not a feature"], 0,
        "Is S < M < L < XL meaningful?",
        "Sizes have an order, so they're ordinal. Colours (red, blue) have no order, so they're nominal.",
        topic="feature-types", level=1),
    mcq("One-hot encoding turns the column city = [BLR, MUM, BLR] into:",
        ["One 0/1 column per city, with a 1 in the row's city column", "A single column [0, 1, 0] only", "The city's population", "A random number per city"], 0,
        "'One hot' = exactly one 1 in each row.",
        "One-hot creates a column per category (city_BLR, city_MUM) and puts a 1 in the matching column, 0 elsewhere.",
        diagram="""
 city   ->  city_BLR  city_MUM
 BLR           1         0
 MUM           0         1
 BLR           1         0
""",
        topic="encoding", level=1),
    mcq("Why do we often scale features (e.g. bring 'salary' and 'age' to similar ranges)?",
        ["So a feature with big numbers doesn't dominate models that use distances or gradients", "To make the dataset smaller", "To remove missing values", "Because models only accept values between 0 and 1"], 0,
        "Salary ~ 1,000,000 vs age ~ 30.",
        "Without scaling, salary's huge numbers swamp age in distance calculations (kNN) and slow gradient-based training.",
        topic="scaling", level=1),
    out("""import numpy as np
import pandas as pd
df = pd.DataFrame({"age": [25, np.nan, 40], "city": ["BLR", "MUM", None]})
print(df.isna().sum().tolist())""",
        ["[1, 1]", "[0, 0]", "[2, 0]", "[1, 0]"], 0,
        "isna() is True wherever a value is missing; sum counts the Trues per column.",
        "Each column has one missing value (np.nan in age, None in city), so the counts are [1, 1].",
        topic="missing", level=1),
    tf("NaN in a pandas DataFrame means the value is missing.", True,
       "NaN = Not a Number.",
       "pandas uses NaN (and None/NaT/pd.NA) to mark missing values. Most models can't accept them, so you must handle them.",
       topic="missing", level=1),
    mcq("In a table of salaries where almost everyone earns 5-30 lakh, one row says 900 lakh. That row is:",
        ["An outlier: far from the rest of the data", "A label", "A categorical feature", "A missing value"], 0,
        "It sits far away from everything else.",
        "An outlier is a point far from the others. It might be a typo or a real (rare) CEO salary; you must check which.",
        topic="outliers", level=1),
    mcq("A fraud dataset has 9,900 normal transactions and 100 frauds. This is called:",
        ["Class imbalance", "Overfitting", "Missing data", "Dimensionality reduction"], 0,
        "One class is much rarer than the other.",
        "When one class is much rarer (here 1%), the data is imbalanced. Models tend to ignore the rare class unless you correct for it.",
        topic="imbalance", level=1),
    mcq("Which is a DATA QUALITY problem?",
        ["The same customer appears 3 times with different birthdates", "The dataset has 10 columns", "The labels are numbers", "The data is stored in a CSV"], 0,
        "Which one means the data is wrong or inconsistent?",
        "Duplicate, conflicting records are a quality issue: the model learns from contradictory facts.",
        topic="quality", level=1),
    mcq("You have 'price' and 'area_sqft' for houses. Adding a new column 'price_per_sqft' is an example of:",
        ["Feature engineering", "Label encoding", "Data versioning", "Clustering"], 0,
        "You created a new useful input from existing ones.",
        "Feature engineering = building new features from raw data that make the pattern easier for the model to learn.",
        topic="feature-eng", level=1),
    mcq("A survey to learn what all Indians think about online shopping is only sent to people who already use a shopping app. The results will be:",
        ["Biased: the sample doesn't represent everyone", "Perfectly representative", "Unaffected, as long as the sample is large", "Better than a random sample"], 0,
        "Who is missing from the sample?",
        "Non-users never get the survey, so the sample is skewed. This is sampling bias; a model trained on it inherits the bias.",
        topic="shift", level=1),
    out("""import pandas as pd
df = pd.DataFrame({"rooms": [2, 3, 4], "area": [800, 1200, 1500], "price": [50, 75, 95]})
X = df.drop(columns="price")
y = df["price"]
print(X.shape, y.shape)""",
        ["(3, 2) (3,)", "(3, 3) (3,)", "(2, 3) (3,)", "(3, 2) (3, 1)"], 0,
        "drop removes the label column from the features.",
        "X keeps 3 rows and the 2 feature columns; y is a single column (a Series), shape (3,).",
        topic="features-labels", level=1),
    fill("A feature like colour (red, green, blue) whose categories have NO natural order is called ____.",
         "nominal",
         "Nominal comes from 'name': just names.",
         "Nominal = unordered categories. Ordinal = ordered (small < medium < large).",
         topic="feature-types", level=1),

    # ------------------------------------------------------------------ L2
    out("""import numpy as np
from sklearn.model_selection import train_test_split
X = np.arange(20).reshape(10, 2)
y = np.arange(10)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=0)
print(Xtr.shape, Xte.shape)""",
        ["(7, 2) (3, 2)", "(8, 2) (2, 2)", "(7, 2) (2, 2)", "(7, 1) (3, 1)"], 0,
        "25% of 10 is 2.5; which way does sklearn round the test set?",
        "sklearn rounds the test size UP: ceil(2.5) = 3 test rows, 7 train rows. Columns are unchanged.",
        topic="features-labels", level=2),
    out("""import numpy as np
batch = np.zeros((32, 64, 64, 3))
print(batch.ndim, batch[0].shape)""",
        ["4 (64, 64, 3)", "3 (64, 64, 3)", "4 (32, 64, 64)", "4 (64, 3)"], 0,
        "(batch, height, width, colour channels).",
        "A batch of 32 RGB images of 64x64 is a 4-D array. One image is (64, 64, 3): height, width and 3 colour channels.",
        topic="data-kinds", level=2),
    mcq("Before a model can use raw text like 'great product, fast delivery', you must first:",
        ["Turn it into numbers, e.g. tokenise and map tokens to IDs or vectors", "Sort the words alphabetically", "Remove all vowels", "Store it in a bigger column"], 0,
        "Models only do arithmetic.",
        "Text is tokenised (split into pieces) and converted to numbers (IDs, counts like TF-IDF, or embeddings).",
        topic="data-kinds", level=2),
    tf("A 6-digit PIN code like 560001 should be treated as a numeric feature, since it's a number.", False,
       "Is 560002 'one more' than 560001 in any meaningful way?",
       "PIN codes, user IDs and phone numbers are identifiers. Their numeric size means nothing, so treat them as categorical (or derive features like region).",
       topic="feature-types", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"city": ["BLR", "MUM", "DEL", "BLR"]})
print(pd.get_dummies(df, columns=["city"]).columns.tolist())""",
        ["['city_BLR', 'city_DEL', 'city_MUM']", "['city_BLR', 'city_MUM', 'city_DEL']", "['city']", "['BLR', 'DEL', 'MUM']"], 0,
        "get_dummies sorts the categories and prefixes the column name.",
        "One column per distinct city, sorted alphabetically and prefixed with 'city_'.",
        topic="encoding", level=2),
    out("""import numpy as np
from sklearn.preprocessing import OneHotEncoder
X = np.array([["red"], ["green"], ["blue"], ["green"]])
enc = OneHotEncoder(drop="first", sparse_output=False).fit(X)
print(enc.transform(X).shape)""",
        ["(4, 2)", "(4, 3)", "(3, 4)", "(4, 1)"], 0,
        "3 categories, minus the dropped one.",
        "drop='first' removes one column (here 'blue'), so 3 colours become 2 columns. That avoids perfectly redundant columns for linear models.",
        topic="encoding", level=2),
    tf("Encoding a nominal feature city as BLR=0, DEL=1, MUM=2 and feeding it to linear regression is fine, because the numbers are just labels.", False,
       "What does a linear model do with the value 2 vs 0?",
       "A linear model treats the numbers as quantities: MUM becomes '2x BLR-to-DEL'. That fake order misleads it. Use one-hot for nominal features.",
       topic="encoding", level=2),
    out("""import numpy as np
from sklearn.preprocessing import StandardScaler
X = np.array([[1.0], [2.0], [3.0]])
print(np.round(StandardScaler().fit_transform(X).ravel(), 2))""",
        ["[-1.22  0.    1.22]", "[-1.  0.  1.]", "[0.  0.5 1. ]", "[1. 2. 3.]"], 0,
        "Mean 2; std computed with ddof=0 is sqrt(2/3).",
        "StandardScaler does (x - mean) / std with the population std (ddof=0) = 0.816, so the values are about -1.22, 0, 1.22.",
        topic="scaling", level=2),
    out("""import numpy as np
from sklearn.preprocessing import MinMaxScaler
train = np.array([[0.0], [5.0], [10.0]])
test = np.array([[20.0]])
s = MinMaxScaler().fit(train)
print(s.transform(test))""",
        ["[[2.]]", "[[1.]]", "[[0.5]]", "ValueError"], 0,
        "The min and max come from the training data only.",
        "Train min = 0, max = 10, so (20 - 0) / 10 = 2.0. Test values can fall outside [0, 1]; the scaler doesn't clip.",
        topic="scaling", level=2),
    out("""import numpy as np
import pandas as pd
s = pd.Series([1.0, np.nan, 3.0])
print(s.mean(), np.mean(s.to_numpy()))""",
        ["2.0 nan", "2.0 2.0", "nan nan", "1.3333333333333333 nan"], 0,
        "One library skips NaN by default; the other propagates it.",
        "pandas skips NaN (skipna=True), giving 2.0. NumPy's np.mean on the raw array returns nan; use np.nanmean instead.",
        topic="missing", level=2),
    out("""import numpy as np
from sklearn.impute import SimpleImputer
X = np.array([[1.0], [np.nan], [3.0], [100.0]])
print(SimpleImputer(strategy="median").fit_transform(X).ravel())""",
        ["[  1.   3.   3. 100.]", "[  1.          34.66666667   3.         100.        ]", "[  1.   0.   3. 100.]", "[  1.   2.   3. 100.]"], 0,
        "Median of the observed values 1, 3, 100.",
        "The median of [1, 3, 100] is 3, so the gap becomes 3. The mean (34.7) would be dragged by the 100.",
        topic="missing", level=2),
    tf("Filling every missing value with 0 is always a safe default.", False,
       "What if 0 is a real, meaningful value?",
       "If 0 means something (balance = 0, age 0), filling with 0 blends missing with real values. Prefer median/mode or a learned imputer, often with an 'is_missing' flag.",
       topic="missing", level=2),
    out("""import numpy as np
x = np.array([10, 12, 11, 13, 12, 500])
print(np.mean(x), np.median(x))""",
        ["93.0 12.0", "12.0 12.0", "93.0 93.0", "11.6 12.0"], 0,
        "Which one is pulled by the 500?",
        "The single outlier drags the mean to 93, while the median stays at 12, a robust centre.",
        topic="outliers", level=2),
    out("""import numpy as np
x = np.array([10, 12, 11, 13, 12, 14, 11, 60])
q1, q3 = np.percentile(x, [25, 75])
iqr = q3 - q1
mask = (x < q1 - 1.5 * iqr) | (x > q3 + 1.5 * iqr)
print(x[mask])""",
        ["[60]", "[10 60]", "[]", "[13 14 60]"], 0,
        "IQR rule: further than 1.5 * IQR beyond the quartiles.",
        "Q1 = 11, Q3 = 13.25, IQR = 2.25, so the fence is [7.6, 16.6]. Only 60 falls outside.",
        diagram="""
   Q1-1.5IQR   Q1   Q3   Q3+1.5IQR
 ------|--------[====]--------|------- * 60
     normal range of the box        outlier
""",
        topic="outliers", level=2),
    mcq("A model for a 99:1 imbalanced fraud dataset reports 99% accuracy. What's the first thing to check?",
        ["Whether it just predicts 'not fraud' for everything: look at recall and precision on the fraud class", "Nothing, 99% is excellent", "Whether the dataset is too small", "Whether the learning rate is too low"], 0,
        "What does a do-nothing model score here?",
        "Always predicting the majority class already gives 99%. This is the accuracy paradox; check fraud-class recall, precision and PR-AUC.",
        topic="imbalance", level=2),
    out("""import numpy as np
from sklearn.model_selection import train_test_split
y = np.array([0] * 90 + [1] * 10)
X = np.arange(100).reshape(-1, 1)
_, _, _, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=0)
print(len(yte), int(yte.sum()))""",
        ["20 2", "20 10", "20 0", "10 2"], 0,
        "stratify keeps the class ratio the same in each split.",
        "10% of the data is class 1, so a stratified 20-row test set gets exactly 2 positives. Without stratify you could easily get 0 or 5.",
        topic="imbalance", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"text": ["good", "bad", "good", "ok"], "label": [1, 0, 0, 1]})
conflicts = df.groupby("text")["label"].nunique()
print(conflicts[conflicts > 1].index.tolist())""",
        ["['good']", "['good', 'ok']", "[]", "['bad']"], 0,
        "Same input, more than one distinct label.",
        "'good' appears with labels 1 and 0: a conflicting (noisy) label. Finding these is a cheap data-quality check.",
        topic="quality", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"ts": pd.to_datetime(["2026-11-14 09:30", "2026-11-15 22:10"])})
df["dow"] = df["ts"].dt.dayofweek
df["hour"] = df["ts"].dt.hour
print(df[["dow", "hour"]].values.tolist())""",
        ["[[5, 9], [6, 22]]", "[[6, 9], [0, 22]]", "[[14, 9], [15, 22]]", "[[5, 30], [6, 10]]"], 0,
        "dayofweek counts Monday as 0. 14 Nov 2026 is a Saturday.",
        "Saturday = 5, Sunday = 6, plus the hour. Turning a raw timestamp into day-of-week and hour is classic feature engineering.",
        topic="feature-eng", level=2),

    # ------------------------------------------------------------------ L3
    mcq("Why use stratify=y in train_test_split for a classification problem with a rare class?",
        ["So train and test keep the same class proportions and the rare class isn't missing from the test set", "To make the split faster", "To balance the classes 50/50", "To remove duplicates"], 0,
        "A random split of 1% positives can easily give 0 positives in a small test set.",
        "Stratification preserves the class ratio in each split. It does NOT balance the classes; it just keeps the original ratio.",
        topic="features-labels", level=3),
    out("""import pandas as pd
s = pd.Series([100, 120, 130, 125], index=pd.date_range("2026-01-01", periods=4))
df = pd.DataFrame({"sales": s, "lag1": s.shift(1)})
print(df["lag1"].tolist())""",
        ["[nan, 100.0, 120.0, 130.0]", "[120.0, 130.0, 125.0, nan]", "[100, 120, 130, 125]", "[nan, nan, 100.0, 120.0]"], 0,
        "shift(1) moves values one step later in time.",
        "A lag feature gives each day yesterday's value. The first day has no yesterday, so it's NaN (and the ints become floats).",
        topic="data-kinds", level=3),
    mcq("For predicting next month's sales from 3 years of monthly data, how should you split?",
        ["Train on the earlier months, test on the most recent months (no shuffling)", "Shuffle all months randomly, then split 80/20", "Use every other month as test", "Test on the oldest months"], 0,
        "In production you'll always predict the future from the past.",
        "A random split lets the model see the future during training (leakage). Time-ordered splits mimic real use.",
        diagram="""
 time --->
 [=========== train ===========][== test ==]
 shuffle split would mix future rows into train
""",
        topic="data-kinds", level=3),
    out("""import numpy as np
from sklearn.preprocessing import OrdinalEncoder
X = np.array([["low"], ["medium"], ["high"]])
print(OrdinalEncoder().fit_transform(X).ravel())""",
        ["[1. 2. 0.]", "[0. 1. 2.]", "[2. 1. 0.]", "[0. 2. 1.]"], 0,
        "OrdinalEncoder doesn't know English; it sorts strings.",
        "Without categories=..., it sorts alphabetically: high=0, low=1, medium=2. So low->1, medium->2, high->0, which breaks the real order.",
        topic="encoding", level=3),
    out("""import numpy as np
from sklearn.preprocessing import OrdinalEncoder
enc = OrdinalEncoder(categories=[["low", "medium", "high"]])
print(enc.fit_transform(np.array([["low"], ["medium"], ["high"]])).ravel())""",
        ["[0. 1. 2.]", "[1. 2. 0.]", "[2. 1. 0.]", "ValueError"], 0,
        "You told it the order explicitly.",
        "Passing categories=[[...]] fixes the order you want, so low=0 < medium=1 < high=2.",
        topic="encoding", level=3),
    out("""import numpy as np
from sklearn.preprocessing import OneHotEncoder
enc = OneHotEncoder(sparse_output=False).fit(np.array([["BLR"], ["MUM"]]))
print(enc.transform(np.array([["DEL"]])))""",
        ["ValueError", "[[0. 0.]]", "[[0. 0. 1.]]", "[[1. 0.]]"], 0,
        "DEL never appeared during fit. What's the default for unknown categories?",
        "handle_unknown defaults to 'error', so an unseen category raises ValueError at inference.",
        topic="encoding", level=3),
    out("""import numpy as np
from sklearn.preprocessing import OneHotEncoder
enc = OneHotEncoder(handle_unknown="ignore", sparse_output=False).fit(np.array([["BLR"], ["MUM"]]))
print(enc.transform(np.array([["DEL"], ["MUM"]])))""",
        ["[[0. 0.]\n [0. 1.]]", "[[0. 0. 1.]\n [0. 1. 0.]]", "[[1. 0.]\n [0. 1.]]", "ValueError"], 0,
        "'ignore' means: no column lights up.",
        "With handle_unknown='ignore', an unseen category becomes an all-zeros row; known ones encode normally. Production pipelines usually need this.",
        topic="encoding", level=3),
    mcq("A colleague runs StandardScaler().fit_transform(X) on the whole dataset, then splits into train and test. What is wrong?",
        ["The test set's mean and std leaked into the training features (data leakage)", "Nothing, scaling doesn't affect the score", "StandardScaler can't be used before a split", "The scaler should be fit on the test set"], 0,
        "The test set should be unseen in every way.",
        "Fit preprocessing on training data only, then transform test. Better: put the scaler in a Pipeline so cross-validation refits it per fold.",
        analogy="Like letting a load test peek at production traffic to tune caches, then reporting the numbers as if blind.",
        topic="scaling", level=3),
    out("""import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
X = np.arange(10, dtype=float).reshape(-1, 1)
Xtr, Xte = train_test_split(X, test_size=0.3, random_state=0)
s = StandardScaler().fit(Xtr)
print(s.mean_[0] == Xtr.mean(), s.mean_[0] == X.mean())""",
        ["True False", "True True", "False True", "False False"], 0,
        "The scaler only saw Xtr.",
        "The scaler remembers the training mean only. That's what you want: test is transformed with statistics it never contributed to.",
        topic="scaling", level=3),
    mcq("Which model does NOT need feature scaling to work well?",
        ["A decision tree / random forest", "k-nearest neighbours", "An SVM with an RBF kernel", "Logistic regression trained with gradient descent"], 0,
        "Which one only asks 'is x above some threshold?'",
        "Trees split on thresholds per feature, so rescaling doesn't change their splits. Distance- and gradient-based models are sensitive to scale.",
        topic="scaling", level=3),
    mcq("You impute missing 'income' with the median. Why also add a 0/1 column 'income_missing'?",
        ["The fact that a value is missing can itself carry signal (e.g. people who skip the question differ)", "To make the dataset bigger", "Because imputation fails without it", "So the scaler works"], 0,
        "Who tends to leave income blank?",
        "Missingness is often informative. The indicator lets the model use it, while the imputed value keeps the column numeric. sklearn: SimpleImputer(add_indicator=True).",
        topic="missing", level=3),
    out("""import numpy as np
from sklearn.preprocessing import RobustScaler, StandardScaler
x = np.array([[1.0], [2.0], [3.0], [4.0], [1000.0]])
r = RobustScaler().fit_transform(x).ravel()
s = StandardScaler().fit_transform(x).ravel()
print(np.round(r[:4], 2), np.round(s[:4], 2))""",
        ["[-1.  -0.5  0.   0.5] [-0.5 -0.5 -0.5 -0.5]", "[-0.5 -0.5 -0.5 -0.5] [-1.  -0.5  0.   0.5]", "[0. 0. 0. 0.] [0. 0. 0. 0.]", "[-1.  -0.5  0.   0.5] [-1.  -0.5  0.   0.5]"], 0,
        "One scaler uses median and IQR, the other mean and std.",
        "RobustScaler (median 3, IQR 2) keeps the normal points spread out. StandardScaler's std is inflated by 1000, squashing them all to about -0.5.",
        topic="outliers", level=3),
    out("""import numpy as np
from sklearn.utils.class_weight import compute_class_weight
y = np.array([0] * 90 + [1] * 10)
w = compute_class_weight("balanced", classes=np.array([0, 1]), y=y)
print(np.round(w, 2))""",
        ["[0.56 5.  ]", "[0.9 0.1]", "[1. 9.]", "[0.5 0.5]"], 0,
        "weight_c = n_samples / (n_classes * count_c).",
        "100 / (2 * 90) = 0.56 and 100 / (2 * 10) = 5.0. Mistakes on the rare class now cost 9x more in the loss.",
        topic="imbalance", level=3),
    mcq("When is it correct to oversample the minority class (e.g. random oversampling or SMOTE)?",
        ["After splitting, on the training set only (inside each CV fold)", "Before splitting, on the whole dataset", "On the test set only", "On both train and test, so they match"], 0,
        "What happens if a copied row lands in both train and test?",
        "Oversampling before the split puts copies (or near-copies) of the same point in train and test, inflating the score. The test set must keep the real ratio.",
        topic="imbalance", level=3),
    mcq("After deduplicating, you find 8% of test-set rows also appear exactly in the training set. What does this do to your test score?",
        ["Inflates it: the model is partly graded on examples it memorised", "Nothing, duplicates are harmless", "Lowers it", "Makes it more reliable"], 0,
        "Tests that already appear in the training data...",
        "Train/test overlap makes the test set partly a memory test. Deduplicate before splitting (and dedupe near-duplicates for text/images).",
        topic="quality", level=3),
    tf("If 5% of training labels are randomly flipped, a very flexible model trained to 100% training accuracy will have memorised those wrong labels.", True,
       "100% training accuracy means it fits every label, right or wrong.",
       "Fitting noisy labels perfectly is overfitting to noise. Regularisation, early stopping and cleaning labels reduce the harm.",
       topic="quality", level=3),
    out("""import numpy as np
rng = np.random.default_rng(0)
for d in (2, 1000):
    X = rng.uniform(size=(200, d))
    dist = np.linalg.norm(X[1:] - X[0], axis=1)
    print(d, round(dist.max() / dist.min(), 1) > 2)""",
        ["2 True\n1000 False", "2 False\n1000 True", "2 True\n1000 True", "2 False\n1000 False"], 0,
        "In very high dimensions, are 'near' and 'far' still different?",
        "In 2-D the farthest point is many times further than the nearest. In 1000-D all distances are nearly equal, so 'nearest neighbour' loses meaning: the curse of dimensionality.",
        topic="feature-eng", level=3),
    out("""import numpy as np
income = np.array([20_000, 50_000, 80_000, 10_000_000])
print(np.round(np.log10(income), 1))""",
        ["[4.3 4.7 4.9 7. ]", "[2.3 2.7 2.9 5. ]", "[20000. 50000. 80000. 10000000.]", "[9.9 10.8 11.3 16.1]"], 0,
        "log10 counts powers of ten.",
        "A log transform squeezes a long right tail: the 10-million value becomes 7, close to the rest. Common for income, prices and counts.",
        topic="feature-eng", level=3),
    mcq("A model is trained in 2024; in 2026 the share of customers aged 18-25 doubled, but for any given age the chance of buying is unchanged. This is:",
        ["Covariate shift: p(x) changed, p(y given x) did not", "Concept drift: p(y given x) changed", "Label noise", "Class imbalance"], 0,
        "What changed: the inputs' distribution, or the rule linking inputs to labels?",
        "Only the input distribution moved. Concept drift would mean the same customer now behaves differently.",
        topic="shift", level=3),
    mcq("During COVID, the same browsing behaviour suddenly predicted very different purchases than before. This is:",
        ["Concept drift: the relationship between features and label changed", "Covariate shift only", "Sampling bias at collection time", "A missing-data problem"], 0,
        "Same x, different y.",
        "When p(y | x) changes, the learned rule is simply out of date. You need fresh labels and retraining, not just reweighting.",
        topic="shift", level=3),
    mcq("Why should training data be versioned, just like code?",
        ["A model is produced by data + code; without the exact data version you can't reproduce or debug it", "Data never changes, so versioning is just a formality", "Git stores large datasets efficiently", "It makes training faster"], 0,
        "Your model changed but the code didn't. Why?",
        "Same code + different data = a different model. Versioning data lets you reproduce, compare and roll back models.",
        analogy="Data is a build input like a dependency lockfile: pin it or builds aren't reproducible.",
        topic="versioning", level=3),

    # ------------------------------------------------------------------ L4
    mcq("A loan model doesn't use 'race', but uses PIN code, and still produces racially skewed decisions. Why?",
        ["PIN code acts as a proxy feature strongly correlated with the protected attribute", "The model secretly reads the race column", "PIN codes are random", "Because of class weights"], 0,
        "Removing a column doesn't remove information correlated with it.",
        "Proxy features (PIN code, school, name) can encode a protected attribute. Fairness needs measuring outcomes by group, not just dropping columns.",
        topic="features-labels", level=4),
    mcq("A model predicts patient readmission. Each patient has many visits; you randomly split visits into train/test and get great scores, but performance on new patients is poor. What's the fix?",
        ["Group-based split (e.g. GroupKFold by patient) so a patient's visits are all in train or all in test", "Use stratify=y", "Shuffle the data more", "Use a bigger test set"], 0,
        "The model recognises patients it already met.",
        "Visits of the same patient are correlated. Splitting by group measures what you actually care about: performance on unseen patients.",
        topic="data-kinds", level=4),
    out("""import numpy as np
hours = np.array([0, 6, 12, 23])
sin_h = np.sin(2 * np.pi * hours / 24)
cos_h = np.cos(2 * np.pi * hours / 24)
d = lambda a, b: np.hypot(sin_h[a] - sin_h[b], cos_h[a] - cos_h[b])
print(round(d(0, 3), 2), round(d(0, 2), 2))""",
        ["0.26 2.0", "23 12", "2.0 0.26", "0.26 0.26"], 0,
        "On a clock, 23:00 is right next to 00:00.",
        "Encoding the hour as (sin, cos) puts it on a circle: 23:00 is 0.26 away from midnight, 12:00 is the opposite side (2.0). As a raw number, 23 looks far from 0.",
        topic="feature-types", level=4),
    out("""import numpy as np
from sklearn.preprocessing import TargetEncoder
rng = np.random.default_rng(0)
X = rng.choice(["a", "b", "c", "d"], size=(200, 1))
y = rng.integers(0, 2, size=200)
enc = TargetEncoder(random_state=0)
a = enc.fit_transform(X, y)
b = enc.transform(X)
print(np.allclose(a, b))""",
        ["False", "True", "ValueError", "NotFittedError"], 0,
        "fit_transform for TargetEncoder uses cross-fitting.",
        "fit_transform encodes each training row using folds that exclude it, so it doesn't see its own label. transform uses the full-data means, so they differ by design.",
        topic="encoding", level=4),
    mcq("Why is naive target encoding (replace each category with the mean label over the whole training set) dangerous for a high-cardinality feature like user_id?",
        ["Rare categories get an encoding that is basically their own label, leaking y into X and causing overfitting", "It makes the data too large", "It only works for regression", "It can't handle strings"], 0,
        "A user who appears once: their encoded value equals their label.",
        "For rare categories, the mean label IS the row's label. Use cross-fitting (as sklearn's TargetEncoder.fit_transform does) and smoothing towards the global mean.",
        topic="encoding", level=4),
    mcq("You run cross_val_score on a Pipeline(StandardScaler, SVC) instead of scaling first and then cross-validating an SVC. Why is the pipeline version more honest?",
        ["The scaler is refit inside each fold on that fold's training part only, so the validation fold never leaks into preprocessing", "Pipelines train faster", "It uses a different SVM", "There is no difference"], 0,
        "Where does each fold's scaler get its mean and std from?",
        "Preprocessing fitted outside CV has seen the validation folds. A Pipeline makes every fit/transform happen per fold, exactly like in production.",
        topic="scaling", level=4),
    mcq("A clinic's 'last cholesterol test' is missing mostly for healthy patients whose doctors didn't order the test. This missingness is:",
        ["Missing not at random (MNAR): missingness depends on the patient's health itself", "Missing completely at random", "Not a problem for any model", "Fixed by mean imputation"], 0,
        "Is the missingness related to the thing you're trying to predict?",
        "When the reason a value is missing depends on the outcome, imputing a mean hides real signal. A missing-indicator or modelling the process is needed.",
        topic="missing", level=4),
    tf("In a fraud model, you should remove all outliers from the training data to improve the model.", False,
       "What does a fraudulent transaction usually look like?",
       "Fraud often IS the outlier. Remove only errors (typos, sensor glitches); keep real extremes, especially when they're the signal.",
       topic="outliers", level=4),
    mcq("You trained with class_weight='balanced' on 1:99 data. The predicted probabilities are now much higher than the real fraud rate. What's the best way to use the model?",
        ["Choose the decision threshold on validation data for the business cost, and recalibrate probabilities if they're consumed as probabilities", "Always use 0.5 as the threshold", "Retrain without any weights and ignore the rare class", "Report accuracy only"], 0,
        "Weighting changes the effective class prior the model learns.",
        "Class weights shift outputs towards the rare class, so probabilities are no longer calibrated. Tune the threshold for cost and calibrate (e.g. CalibratedClassifierCV) if needed.",
        topic="imbalance", level=4),
    mcq("Your image classifier keeps failing on a few classes. A review finds ~10% of those training labels are wrong. Which approach targets the root cause?",
        ["Find likely mislabels (e.g. examples where out-of-fold predictions confidently disagree with the label) and send them for relabelling", "Train a bigger model", "Add more epochs", "Increase the learning rate"], 0,
        "Fix the data, not the model.",
        "Out-of-fold predicted probabilities that confidently disagree with the given label (the 'confident learning' idea) flag the rows most likely to be mislabelled.",
        topic="quality", level=4),
    mcq("You have 500 rows and 2,000 features. What is the most sensible response?",
        ["Reduce dimensions (feature selection, regularisation like L1, or PCA) and validate carefully; the model can easily fit noise", "Add more features to help the model", "Use kNN, since it handles high dimensions best", "Nothing, more features always help"], 0,
        "More columns than rows.",
        "With p >> n, many models can fit the training data perfectly by chance. Constrain the model and validate honestly; kNN suffers most from high dimensions.",
        topic="feature-eng", level=4),
    mcq("To check if production data has shifted away from training data, you label train rows 0 and production rows 1 and train a classifier to tell them apart. Its AUC is 0.93. What does that mean?",
        ["Strong shift: the two datasets are easy to tell apart; its top features show what moved", "No shift at all", "The model is overfitting", "The labels are noisy"], 0,
        "If there were no shift, could any classifier tell them apart?",
        "This is adversarial validation. AUC near 0.5 = indistinguishable (no shift); 0.93 = clearly different. Feature importances point to the drifting columns.",
        topic="shift", level=4),
    out("""import hashlib
import pandas as pd
def h(df):
    return hashlib.sha256(df.to_csv(index=False).encode()).hexdigest()[:8]
a = pd.DataFrame({"x": [1, 2, 3]})
b = pd.DataFrame({"x": [1, 2, 3]})
c = pd.DataFrame({"x": [1, 2, 4]})
print(h(a) == h(b), h(a) == h(c))""",
        ["True False", "False False", "True True", "False True"], 0,
        "A content hash depends only on the bytes.",
        "Same content -> same hash; any change -> a new hash. Tools like DVC store a hash pointer in git and the data itself in remote storage.",
        topic="versioning", level=4),
    mcq("A model in production misbehaves. To reproduce exactly how it was built, which set of things must you have recorded?",
        ["Data version (hash), code commit, config/hyperparameters, random seeds and library versions", "Only the code commit", "Only the model file", "Only the dataset name"], 0,
        "Training = function(data, code, config, randomness, environment).",
        "All five inputs determine the trained model. Lineage tools (DVC, MLflow) tie each model to the exact data hash and commit that made it.",
        topic="versioning", level=4),
    fill("sklearn's StandardScaler computes the standard deviation with ddof = ____.",
         "0",
         "Population vs sample standard deviation.",
         "StandardScaler uses the population std (ddof=0), like np.std's default. pandas .std() defaults to ddof=1, so the numbers differ slightly.",
         topic="scaling", level=3),
    fill("Upweighting the rare class in the loss, e.g. LogisticRegression(class_weight='____'), sets weights inversely proportional to class frequency.",
         "balanced",
         "The option name says what it tries to make the classes.",
         "class_weight='balanced' uses n_samples / (n_classes * count_c) per class.",
         topic="imbalance", level=2),
]
