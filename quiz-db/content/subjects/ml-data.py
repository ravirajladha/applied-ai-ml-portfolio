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
    ("col-pipelines", "ColumnTransformer and train/serve consistency"),
    ("genai-data", "Data for LLM apps and fine-tuning"),
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

    # ================================================================== added set 2
    # ------------------------------------------------------------------ features-labels
    tf("A unique row ID (like order_id) should usually be dropped from X before training.", True,
       "Does the number 10452 tell you anything about a NEW order?",
       "An ID is unique per row, so the model can only memorise it. Worse, IDs are often assigned in time order, so they can secretly encode 'when' and leak. Drop IDs from X; keep them for joins and group splits.",
       analogy='Like a cache keyed on request ID: a perfect hit rate on old requests, zero hits on new ones.',
       topic="features-labels", level=2),
    out("""import numpy as np
import pandas as pd
rng = np.random.default_rng(0)
n = 500
y = pd.Series(rng.integers(0, 2, n))
df = pd.DataFrame({"age": rng.normal(40, 10, n),
                   "visits": rng.poisson(3, n),
                   "refund_amt": y * rng.uniform(50, 100, n)})
print(df.corrwith(y).abs().idxmax())""",
        ["refund_amt", "age", "visits", "y"], 0,
        "One column is zero for every negative row. Why would that be?",
        "A quick leakage hunt: rank features by how strongly they track the label. refund_amt is only non-zero when y = 1 (a refund happens AFTER the fraud is confirmed). A feature that looks too good is usually a consequence of the label, not a cause.",
        analogy='Like a test that passes because it reads the expected value from the same fixture it checks against.',
        topic="features-labels", level=3),
    mcq("Label: 'churned = no login in the 30 days AFTER 1 March'. A feature 'days_since_last_login' is computed on 15 March, when the data was exported. What is wrong?",
        ["The feature uses information from inside the label window, so it partly IS the label; compute features as of 1 March",
         "Nothing, logins are a valid behaviour signal",
         "The feature should be one-hot encoded",
         "The label window should be shorter than the feature window"], 0,
        "Draw the timeline: feature cut-off vs label window.",
        "Features must be 'point-in-time correct': computed only from data available at the prediction moment. A churned user on 15 March already shows 14+ days without login, which is the label leaking in. Offline AUC soars, production collapses.",
        diagram="""
 feature data      | prediction time (1 Mar)
 <=================|----- label window (30d) ----->
                   |   15 Mar export: feature peeks here
""",
        topic="features-labels", level=4),
    mcq("You predict which job applicants a recruiter will shortlist. The best feature is 'recruiter opened the CV twice'. Why is it a bad feature for a tool meant to rank NEW applicants before any recruiter sees them?",
        ["It is only produced by the very process you want to replace, so it won't exist at prediction time",
         "Counts are not allowed as features",
         "It has too few distinct values",
         "It needs scaling first"], 0,
        "When does that click happen relative to your prediction?",
        "Ask of every feature: 'will I have this value at the moment I predict?' Behaviour caused by the outcome (opens, refunds, follow-up calls) is leakage, however predictive it looks offline.",
        topic="features-labels", level=3),

    # ------------------------------------------------------------------ data-kinds
    out("""import numpy as np
img = np.zeros((28, 28))
batch = img[None, :, :, None]
print(batch.shape)""",
        ["(1, 28, 28, 1)", "(28, 28)", "(1, 28, 28)", "(28, 28, 1, 1)"], 0,
        "Each None adds a new axis of size 1 at that position.",
        "A grayscale image has no colour axis. Models expect (batch, height, width, channels), so you add a batch axis in front and a channel axis at the end.",
        diagram="""
 (28, 28)  -- img[None, :, :, None] -->  (1, 28, 28, 1)
  H   W                                   N   H   W  C
""",
        topic="data-kinds", level=2),
    out("""import numpy as np
img = np.zeros((64, 48, 3))
print(img.transpose(2, 0, 1).shape)""",
        ["(3, 64, 48)", "(48, 64, 3)", "(3, 48, 64)", "(64, 3, 48)"], 0,
        "transpose(2, 0, 1) means: new axis 0 = old axis 2, then old 0, then old 1.",
        "PIL/NumPy images are (H, W, C) 'channels-last'; PyTorch wants (C, H, W) 'channels-first'. Mixing them up gives shape errors or, worse, silently scrambled images.",
        diagram="""
 (H, W, C) -- transpose(2, 0, 1) --> (C, H, W)
 (64,48,3)                           (3, 64, 48)
 NumPy / PIL                         PyTorch
""",
        topic="data-kinds", level=2),
    out("""import pandas as pd
s = pd.Series([10, 20, 30, 40])
print(s.shift(1).rolling(2).mean().tolist())""",
        ["[nan, nan, 15.0, 25.0]", "[nan, 15.0, 25.0, 35.0]", "[15.0, 25.0, 35.0, nan]", "[nan, nan, 10.0, 20.0]"], 0,
        "shift first (yesterday's values), then average the last 2 of those.",
        "Row t gets the mean of days t-1 and t-2, never day t itself. s.rolling(2).mean() alone would include today's value, which is the very thing you're predicting: a classic time-series leak.",
        topic="data-kinds", level=3),
    mcq("A teammate builds a smoothed sales feature with df['sales'].rolling(7, center=True).mean() to forecast daily sales. What is the problem?",
        ["center=True averages 3 days into the future, so each row sees values that won't exist at prediction time",
         "rolling() can't take a window of 7",
         "Rolling means remove the trend",
         "There is no problem; centring reduces lag"], 0,
        "Which 7 days does a centred window cover?",
        "A centred window at day t covers t-3 .. t+3. It's great for charts, but as a feature it smuggles in the future. Use trailing windows on shifted data: shift(1).rolling(7).",
        diagram="""
 day:      t-3 t-2 t-1  t  t+1 t+2 t+3
 center:   [==========  t  ==========]   uses future
 trailing: [==========] t                safe
""",
        analogy="Like backtesting a trading bot that is allowed to read tomorrow's newspaper.",
        topic="data-kinds", level=4),

    # ------------------------------------------------------------------ feature-types
    tf("'Number of children' (0, 1, 2, 3...) is a numeric feature: the values can be counted and compared.", True,
       "Does 2 children mean 'one more' than 1 child?",
       "Counts are numeric (discrete numeric). Contrast with a PIN code, which is a number in form but a category in meaning.",
       topic="feature-types", level=1),
    mcq("Which feature is ORDINAL?",
        ["Education level: school < bachelor's < master's < PhD", "Blood group: A, B, AB, O", "Country of birth", "Favourite colour"], 0,
        "Which one has a natural ranking?",
        "Education levels have a clear order but no fixed distance between steps. Blood group and country are nominal: no order.",
        topic="feature-types", level=2),
    out("""import pandas as pd
ids = [f"u{i % 800}" for i in range(2000)]
print(pd.get_dummies(pd.Series(ids)).shape)""",
        ["(2000, 800)", "(2000, 1)", "(800, 2000)", "(2000, 2000)"], 0,
        "One column per distinct value.",
        "800 distinct users means 800 one-hot columns, mostly zeros. With millions of users this explodes. That is the high-cardinality problem: use frequency/target encoding, hashing or learned embeddings instead.",
        topic="feature-types", level=3),
    mcq("A 'merchant_id' column has 200,000 distinct values, many seen only once. Which encoding is a reasonable choice for a gradient-boosted tree model?",
        ["Frequency or cross-fitted target encoding (or hashing), grouping rare merchants together",
         "One-hot encoding of all 200,000 values",
         "Use the raw ID as a number",
         "Drop every row whose merchant appears once"], 0,
        "You want a few informative numbers per row, not 200,000 sparse columns.",
        "High-cardinality categoricals need compact encodings. Frequency encoding says 'how common is this merchant', target encoding says 'how often do its transactions turn out to be fraud' (cross-fitted to avoid leaks). Rare values get pooled.",
        topic="feature-types", level=3),
    out("""import numpy as np
h = np.array([3, 9])
print(np.round(np.sin(2 * np.pi * h / 24), 3))""",
        ["[0.707 0.707]", "[ 0.707 -0.707]", "[0.25 0.75]", "[3. 9.]"], 0,
        "Sine is symmetric around its peak at 6 o'clock.",
        "3:00 and 9:00 get the same sine. That's why cyclical encoding uses BOTH sin and cos: the cos (0.707 vs -0.707) separates them, giving every hour a unique point on the circle.",
        diagram="""
           0h (cos=1)
            |
  18h ------+------ 6h (sin=1)
            |
           12h
 3h and 9h: same height (sin), opposite sides (cos)
""",
        topic="feature-types", level=3),
    mcq("For a gradient-boosted tree model, is sin/cos encoding of 'month' essential?",
        ["Not essential: trees can split raw month into ranges, though Dec-Jan adjacency costs extra splits; sin/cos matters most for linear and distance-based models",
         "Yes, trees can't use numeric months at all",
         "Yes, otherwise trees treat December as 12x January",
         "No, and sin/cos would break the tree"], 0,
        "How does a tree use a numeric feature: as a quantity, or through thresholds?",
        "Trees only ask 'month <= 6?', so magnitude doesn't matter, only order. The wrap-around (12 next to 1) needs two splits to capture. Linear models and kNN, which use distance and magnitude, benefit far more from cyclical encoding.",
        topic="feature-types", level=4),

    # ------------------------------------------------------------------ encoding
    out("""import pandas as pd
train = pd.DataFrame({"c": ["a", "b", "c"]})
test = pd.DataFrame({"c": ["a", "a"]})
print(pd.get_dummies(train).shape[1], pd.get_dummies(test).shape[1])""",
        ["3 1", "3 3", "1 1", "3 2"], 0,
        "get_dummies only knows the values it sees in THIS DataFrame.",
        "Calling get_dummies separately on train and test gives different columns, so the model gets the wrong number (or order) of features. Fit a OneHotEncoder on train and reuse it, or reindex test to the training columns.",
        analogy="Like two microservices each generating their own enum from whatever values they happen to see: the IDs won't line up.",
        diagram="""
 train columns: c_a  c_b  c_c   (3)
 test  columns: c_a             (1)
 model expects 3 inputs -> crash or wrong features
""",
        topic="encoding", level=3),
    tf("sklearn's LabelEncoder is meant for encoding the target y, not input feature columns.", True,
       "Check what its fit() signature takes.",
       "LabelEncoder works on a 1-D y. For input features use OrdinalEncoder (ordered categories) or OneHotEncoder (nominal); they handle 2-D X, multiple columns and unknown values.",
       topic="encoding", level=2),
    out("""import numpy as np
from sklearn.preprocessing import OneHotEncoder
X = np.array([["a"]] * 5 + [["b"]] * 4 + [["c"]] + [["d"]], dtype=object)
enc = OneHotEncoder(min_frequency=2, sparse_output=False).fit(X)
print(enc.get_feature_names_out().tolist())""",
        ["['x0_a', 'x0_b', 'x0_infrequent_sklearn']", "['x0_a', 'x0_b', 'x0_c', 'x0_d']", "['x0_a', 'x0_b']", "['a', 'b', 'other']"], 0,
        "Categories seen fewer than 2 times are pooled.",
        "min_frequency groups rare categories ('c', 'd') into one 'infrequent' column. That tames high cardinality and gives unseen-at-train values somewhere sensible to go (with handle_unknown='infrequent_if_exist').",
        topic="encoding", level=3),
    mcq("You fit unregularised LinearRegression (with an intercept) on a full one-hot encoding of 'city' (one column per city, no column dropped). What is the issue?",
        ["The one-hot columns always sum to 1, duplicating the intercept: perfect collinearity makes the coefficients non-unique",
         "One-hot columns can't be used in linear regression",
         "The model will refuse to fit",
         "It forces all cities to have the same coefficient"], 0,
        "Add up the city columns in any row.",
        "This is the 'dummy variable trap'. Predictions are fine, but the individual coefficients can't be interpreted. drop='first' (or regularisation, which picks one solution) fixes it. Tree models don't care.",
        diagram="""
 BLR DEL MUM | sum | intercept
  1   0   0  |  1  |    1
  0   0   1  |  1  |    1
 sum of dummies == intercept column -> collinear
""",
        topic="encoding", level=3),
    out("""import numpy as np
y = np.array([1, 0, 0, 0, 0])
global_mean = y.mean()
n_c, mean_c, m = 1, 1.0, 10
smoothed = (n_c * mean_c + m * global_mean) / (n_c + m)
print(round(global_mean, 2), round(smoothed, 2))""",
        ["0.2 0.27", "0.2 1.0", "1.0 0.27", "0.2 0.2"], 0,
        "With m=10 'pseudo-rows' at the global mean, how much can one row move the estimate?",
        "Smoothing blends a category's mean with the global mean, weighted by how many rows it has. A category seen once with label 1 gets 0.27, not 1.0, so a single row can't hand the model its own answer.",
        topic="encoding", level=4),
    mcq("Why might you choose the hashing trick (e.g. FeatureHasher into 2^18 columns) for a stream of ad-click categories?",
        ["No vocabulary to store and new categories are handled automatically; the cost is occasional collisions and no way to map columns back to names",
         "It is lossless and fully interpretable",
         "It sorts categories by frequency",
         "It removes the need for a model"], 0,
        "What does a hash function do with a value it has never seen?",
        "Hashing maps any string to a fixed column index, so there's no fit step and no 'unknown category' error, ideal for huge, changing vocabularies. Collisions add a little noise; you lose interpretability.",
        analogy="Like sharding keys with hash(key) % N: no lookup table, any new key has a home, but two keys can share a shard.",
        topic="encoding", level=4),
    mcq("A TargetEncoder is placed inside a Pipeline and evaluated with cross_val_score. Why is that safe while computing the encoding once on the whole dataset first is not?",
        ["Inside the pipeline each fold's encoder is fit only on that fold's training rows (with internal cross-fitting), so validation labels never enter the encoding",
         "Pipelines automatically drop the target column",
         "cross_val_score disables target encoding",
         "There is no difference"], 0,
        "Where do the category means come from in each case?",
        "Encoding on the full dataset puts every validation row's label into the category means the model trains on. In a pipeline, fit happens per fold, so the leak can't happen. Label-using steps must always live inside the CV loop.",
        topic="encoding", level=4),

    # ------------------------------------------------------------------ scaling
    tf("Standardising a 'price' column can change which house is the most expensive.", False,
       "Subtract a constant, divide by a positive constant: what happens to the order?",
       "Scaling is a monotonic transform: the order of values is unchanged. Only the units change, which is why trees, which only care about order, are unaffected.",
       topic="scaling", level=1),
    out("""import numpy as np
from sklearn.preprocessing import MinMaxScaler
x = np.array([[2.0], [4.0], [6.0], [10.0]])
print(MinMaxScaler().fit_transform(x).ravel())""",
        ["[0.   0.25 0.5  1.  ]", "[0.2 0.4 0.6 1. ]", "[-1.  -0.5  0.   1. ]", "[0.   0.33 0.67 1.  ]"], 0,
        "(x - min) / (max - min) with min 2 and max 10.",
        "(2-2)/8 = 0, (4-2)/8 = 0.25, (6-2)/8 = 0.5, (10-2)/8 = 1. The min maps to 0 and the max to 1.",
        topic="scaling", level=2),
    mcq("You have a fitted scaler `sc` from the training data. Which line correctly prepares the test set?",
        ["X_test_s = sc.transform(X_test)", "X_test_s = sc.fit_transform(X_test)", "X_test_s = StandardScaler().fit_transform(X_test)", "X_test_s = sc.fit(X_test).transform(X_train)"], 0,
        "fit = learn statistics; transform = apply them.",
        "Test data must be transformed with the TRAINING mean/std. fit_transform on test re-learns statistics from test, which both leaks and puts train and test on different scales.",
        analogy='fit is building the config from training data; transform is deploying that same config everywhere. Re-fitting on test is hot-patching prod with different settings.',
        topic="scaling", level=2),
    out("""import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
rng = np.random.default_rng(0)
y = rng.integers(0, 2, 400)
X = np.c_[y + rng.normal(0, 0.5, 400), rng.normal(0, 1000, 400)]
raw = cross_val_score(KNeighborsClassifier(), X, y, cv=5).mean()
sc = cross_val_score(make_pipeline(StandardScaler(), KNeighborsClassifier()), X, y, cv=5).mean()
print(raw < 0.6, sc > 0.8)""",
        ["True True", "False True", "True False", "False False"], 0,
        "Column 0 holds the signal (scale ~1); column 1 is noise with scale ~1000.",
        "Unscaled, kNN's distances are almost entirely the noise column, so it's near chance. After scaling both columns count equally and the signal wins. Distance-based models need scaling.",
        topic="scaling", level=3),
    mcq("Why does feature scale matter for Ridge or Lasso regression even though plain linear regression would just rescale its coefficients?",
        ["The penalty is on coefficient size, and a feature in small units needs a big coefficient, so it gets penalised more than an identical feature in large units",
         "Ridge can't handle values above 1",
         "Lasso only works on binary features",
         "Scaling changes the number of features"], 0,
        "Measure height in km instead of cm: what happens to its coefficient?",
        "Regularisation assumes coefficients are comparable. Without scaling, the penalty depends on arbitrary units, so feature selection by Lasso is meaningless. Standardise before regularised linear models.",
        topic="scaling", level=4),

    # ------------------------------------------------------------------ missing
    out("""import numpy as np
import pandas as pd
df = pd.DataFrame({"a": [1, np.nan, 3, 4], "b": [1, 2, np.nan, 4]})
print(len(df.dropna()))""",
        ["2", "3", "4", "0"], 0,
        "dropna drops a row if ANY value in it is missing.",
        "Rows 1 and 2 each have one NaN, so only 2 rows survive. Dropping rows is simple but throws away data fast when many columns have a few gaps.",
        topic="missing", level=1),
    out("""import numpy as np
from sklearn.impute import SimpleImputer
X = np.array([[1.0, 5.0], [np.nan, 6.0], [3.0, 7.0]])
print(SimpleImputer(add_indicator=True).fit_transform(X).shape)""",
        ["(3, 3)", "(3, 2)", "(3, 4)", "(2, 2)"], 0,
        "Indicator columns are added only for features that had missing values during fit.",
        "Two imputed columns plus one 0/1 'was missing' column for the first feature = 3 columns. The second feature had no NaN, so it gets no indicator.",
        topic="missing", level=2),
    out("""import numpy as np
from sklearn.impute import SimpleImputer
train = np.array([["a"], ["b"], ["b"]], dtype=object)
test = np.array([[np.nan]], dtype=object)
imp = SimpleImputer(strategy="most_frequent").fit(train)
print(imp.transform(test))""",
        ["[['b']]", "[['a']]", "[[nan]]", "ValueError"], 0,
        "The fill value was learned during fit.",
        "The imputer remembers the training mode ('b') and uses it on test. Like scalers, imputers are fit on training data only.",
        topic="missing", level=2),
    out("""import numpy as np
import pandas as pd
df = pd.DataFrame({"city": ["A", "A", "A", "B", "B"],
                   "rent": [10, 12, np.nan, 50, np.nan]})
df["rent"] = df.groupby("city")["rent"].transform(lambda s: s.fillna(s.median()))
print(df["rent"].tolist())""",
        ["[10.0, 12.0, 11.0, 50.0, 50.0]", "[10.0, 12.0, 12.0, 50.0, 12.0]", "[10.0, 12.0, 24.0, 50.0, 24.0]", "[10.0, 12.0, nan, 50.0, nan]"], 0,
        "Each city fills its gaps with its own median.",
        "Group-wise imputation (city A median 11, city B median 50) is usually better than one global median when groups differ a lot. In a real project compute the group medians on the training rows only.",
        topic="missing", level=3),
    tf("HistGradientBoostingClassifier can be trained directly on data containing NaN, without an imputer.", True,
       "Some tree models learn where to send missing values.",
       "At each split it learns whether rows with NaN should go left or right. Linear models, SVMs and kNN in sklearn still need imputation.",
       code="""import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
X = np.array([[1.0], [np.nan], [3.0], [4.0]] * 10)
y = np.array([0, 1, 0, 1] * 10)
HistGradientBoostingClassifier().fit(X, y)""",
       topic="missing", level=3),
    mcq("Survey 'income' is missing more often for younger respondents, but within an age group it's missing at random. This is:",
        ["Missing at random (MAR): missingness depends on another observed column (age)",
         "Missing completely at random (MCAR)",
         "Missing not at random (MNAR)",
         "Not missing data at all"], 0,
        "Does missingness depend on something you CAN see?",
        "MCAR: no pattern. MAR: depends on observed features (age), so imputing using age works well. MNAR: depends on the missing value itself (high earners hide income), the hardest case.",
        analogy='Like error rates that differ by client version: once you group by version (the observed column), the failures look random within each group.',
        topic="missing", level=3),
    mcq("You call df.dropna() and lose 30% of rows. Almost all dropped rows are from new customers who skipped optional profile fields. What is the risk?",
        ["The training set now under-represents new customers, so the model is worst exactly for them",
         "None, dropping rows always reduces noise",
         "The model will train faster, which is only good",
         "The labels will become missing"], 0,
        "Who disappeared from the data?",
        "When missingness is related to who the user is, dropping rows is a selection bias. Impute with indicators instead, and check metrics per segment (new vs old customers).",
        topic="missing", level=4),

    # ------------------------------------------------------------------ outliers
    mcq("A temperature sensor column has normal values 18-35 and a few rows with -999. What are those -999 rows most likely?",
        ["A sentinel code meaning 'missing', which should be converted to NaN, not treated as a real temperature",
         "A real cold snap that must be kept",
         "An ordinal category",
         "A label"], 0,
        "Is -999 degrees physically plausible?",
        "Legacy systems often store missing as -999, 0 or 9999. Left in, they become huge fake outliers that wreck means and scalers. Read the data dictionary and replace sentinels with NaN.",
        analogy="Like an API that returns -1 for 'not found': treat it as null, not as a real value.",
        topic="outliers", level=2),
    out("""import numpy as np
x = np.array([10.0, 11.0, 12.0, 13.0, 1000.0])
z = (x - x.mean()) / x.std()
print(bool(np.abs(z).max() > 3))""",
        ["False", "True", "nan", "ValueError"], 0,
        "The outlier inflates the very std used to judge it.",
        "With 5 points the largest possible |z| (ddof=0) is sqrt(n-1) = 2, so the 'z > 3' rule can never fire. The outlier masks itself. Use robust rules (IQR, median absolute deviation) on small samples.",
        topic="outliers", level=4),
    mcq("House prices in your regression target include a few genuine 50-crore mansions. Training with MSE, the model's errors on ordinary homes get worse. A good first fix?",
        ["Use a loss less sensitive to big errors (MAE / Huber) or model log(price)",
         "Delete every house above the 90th percentile from the test set",
         "Scale the features with MinMaxScaler",
         "Switch to accuracy"], 0,
        "MSE squares errors: what does that do to a 40-crore miss?",
        "Squared error lets a few extreme targets dominate training. Huber/MAE or a log target reduce their pull while keeping them in the data. Don't silently remove real points from the test set.",
        topic="outliers", level=3),

    # ------------------------------------------------------------------ imbalance
    out("""import pandas as pd
y = pd.Series(["ok"] * 95 + ["fraud"] * 5)
print(y.value_counts(normalize=True).to_dict())""",
        ["{'ok': 0.95, 'fraud': 0.05}", "{'ok': 95, 'fraud': 5}", "{'fraud': 0.05, 'ok': 0.95}", "{'ok': 0.5, 'fraud': 0.5}"], 0,
        "normalize=True gives fractions; value_counts sorts by count.",
        "The first thing to run on any classification target: value_counts(normalize=True). A 95/5 split immediately tells you accuracy will be misleading.",
        topic="imbalance", level=1),
    out("""import numpy as np
from sklearn.metrics import accuracy_score, balanced_accuracy_score
y = np.array([0] * 95 + [1] * 5)
pred = np.zeros(100, dtype=int)
print(accuracy_score(y, pred), balanced_accuracy_score(y, pred))""",
        ["0.95 0.5", "0.95 0.95", "0.5 0.5", "0.05 0.5"], 0,
        "Balanced accuracy averages the recall of each class.",
        "The do-nothing model gets 95% accuracy but recall 1.0 on class 0 and 0.0 on class 1, so balanced accuracy is 0.5: exactly chance. It exposes the accuracy paradox in one number.",
        topic="imbalance", level=2),
    out("""import numpy as np
y = np.array([1, 1, 1, 0, 0, 0, 0, 0])
p = np.array([0.9, 0.4, 0.3, 0.35, 0.2, 0.1, 0.1, 0.05])
for t in (0.5, 0.3):
    pred = p >= t
    tp = int((pred & (y == 1)).sum())
    print(t, tp / 3, tp / int(pred.sum()))""",
        ["0.5 0.3333333333333333 1.0\n0.3 1.0 0.75", "0.5 1.0 0.75\n0.3 0.3333333333333333 1.0", "0.5 0.3333333333333333 1.0\n0.3 0.6666666666666666 0.75", "0.5 1.0 1.0\n0.3 1.0 1.0"], 0,
        "Printed: threshold, recall, precision. Lower threshold = more positives flagged.",
        "At 0.5 only one fraud is caught (recall 0.33). At 0.3 all three are caught for one false alarm (precision 0.75). On imbalanced data the default 0.5 is rarely the right threshold; choose it on validation data from the business cost.",
        diagram="""
 p:  .05 .1 .1 .2 | .3 .35 .4 | .9
                  t=0.3      t=0.5
 lower t -> more flagged -> recall up, precision down
""",
        topic="imbalance", level=3),
    out("""import pandas as pd
train = pd.DataFrame({"y": [0] * 90 + [1] * 10})
neg = train[train.y == 0].sample(n=10, random_state=0)
balanced = pd.concat([neg, train[train.y == 1]])
print(balanced.y.value_counts().sort_index().tolist(), len(balanced))""",
        ["[10, 10] 20", "[90, 10] 100", "[10, 90] 100", "[45, 10] 55"], 0,
        "Keep all positives, sample 10 negatives.",
        "Random undersampling throws away majority rows so the classes balance. Do it ONLY on the training set; the test set keeps the real 90/10 ratio, and expect predicted probabilities to be inflated afterwards.",
        topic="imbalance", level=2),
    mcq("You train on a 50/50 undersampled set, but real traffic is 1% fraud. The model says p(fraud) = 0.5 for a transaction. What is the realistic probability?",
        ["Much lower than 0.5: undersampling inflated the prior, so outputs must be corrected (prior adjustment or recalibration on real-ratio data)",
         "Exactly 0.5, probabilities don't depend on the training ratio",
         "Exactly 0.01",
         "Higher than 0.5"], 0,
        "The model learned that fraud is 50x more common than it is.",
        "Resampling changes p(y) in training, so the model's probabilities reflect the fake 50/50 world. For ranking that's fine; for decisions or displayed risk scores, recalibrate on data with the true ratio.",
        diagram="""
 real:   [F][oooooooooooooooooooooooooooooooooooooooooo]
 train:  [FFFFF][ooooo]      (negatives thrown away)
 model's sense of 'how common is fraud' is 50x too high
""",
        topic="imbalance", level=4),
    mcq("On a dataset with 0.1% positives, model A has ROC-AUC 0.98 but PR-AUC 0.12. What explains the gap?",
        ["ROC's false-positive RATE hides huge numbers of false positives when negatives vastly outnumber positives; PR-AUC shows that most flagged items are false alarms",
         "One of the metrics is computed wrong",
         "PR-AUC is always lower than ROC-AUC by a fixed amount",
         "The model is overfitting"], 0,
        "1% FPR of 1,000,000 negatives is how many false alarms?",
        "With 1M negatives and 1,000 positives, a 1% FPR is 10,000 false alarms vs at most 1,000 true hits: precision below 10%. ROC looks great; the analysts drowning in alerts don't. Report PR-AUC / precision at your operating recall.",
        diagram="""
 1,000 fraud  |  1,000,000 normal
 FPR 1%   -> 10,000 false alarms
 TP max   ->  1,000
 precision <= 1,000 / 11,000 = 9%
""",
        topic="imbalance", level=4),
    mcq("A team applies SMOTE to the full dataset, then runs 5-fold CV and sees recall jump from 0.40 to 0.85. Why should you distrust the jump?",
        ["SMOTE creates synthetic points by interpolating between real neighbours, so validation folds contain near-copies of training points",
         "SMOTE always lowers recall",
         "CV can't be used with SMOTE in any way",
         "Recall isn't a valid metric for imbalance"], 0,
        "A synthetic point sits between two real points. Where can those real points end up?",
        "Resampling must happen inside each training fold (imblearn's Pipeline does this). Done globally, validation folds contain synthetic neighbours of training rows, and the 'gain' is memorisation.",
        diagram="""
 real a *-----o-----* real b      o = synthetic point
 a lands in a train fold, o in the validation fold
 -> validation contains a near-copy of training data
""",
        topic="imbalance", level=4),

    # ------------------------------------------------------------------ quality
    out("""import pandas as pd
df = pd.DataFrame({"a": [1, 1, 2, 1], "b": ["x", "x", "y", "x"]})
print(int(df.duplicated().sum()), len(df.drop_duplicates()))""",
        ["2 2", "1 3", "3 1", "0 4"], 0,
        "duplicated() marks every repeat after the first occurrence.",
        "Rows 1 and 3 repeat row 0, so 2 duplicates and 2 unique rows remain. Count duplicates before splitting; repeats inflate both training weight and test scores.",
        topic="quality", level=2),
    out("""import pandas as pd
s = pd.Series(["Reset password", "reset password ", "RESET PASSWORD", "Refund"])
print(int(s.duplicated().sum()), int(s.str.lower().str.strip().duplicated().sum()))""",
        ["0 2", "2 2", "0 0", "1 3"], 0,
        "Exact matching treats case and spaces as different.",
        "Exact dedup finds nothing; after normalising case and whitespace, 2 of the 3 'reset password' texts are duplicates. Real text dedup also needs near-duplicate methods (MinHash, embeddings).",
        topic="quality", level=3),
    out("""from sklearn.metrics import cohen_kappa_score
a = [1, 1, 0, 0]
b = [1, 0, 0, 0]
print(round(cohen_kappa_score(a, b), 2))""",
        ["0.5", "0.75", "0.25", "1.0"], 0,
        "Raw agreement is 0.75; how much of that is expected by chance?",
        "Cohen's kappa = (observed - chance) / (1 - chance) = (0.75 - 0.5) / 0.5 = 0.5. Low agreement between two labellers on the same items tells you the labels (or the guidelines) are noisy before you blame the model.",
        topic="quality", level=3),
    tf("Ranking rows by how confidently out-of-fold predictions disagree with their label finds far more of the flipped labels than picking 10 rows at random would (about 0.3 expected).", True,
       "Run the code: how many of the 10 suspects are in `flip`?",
       "This is the core idea of confident learning: an honest (out-of-fold) model that strongly disagrees with a label points at a likely mislabel. Here half the top-10 suspects are real flips vs 0.3 expected by chance.",
       code="""import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict
X, y = make_classification(n_samples=300, n_features=5, n_informative=3, class_sep=2, random_state=0)
yn = y.copy(); flip = np.arange(0, 300, 30); yn[flip] ^= 1
p = cross_val_predict(LogisticRegression(), X, yn, cv=5, method="predict_proba")
suspects = np.argsort(p[np.arange(300), yn])[:10]
print(len(set(suspects.tolist()) & set(flip.tolist())))""",
       topic="quality", level=4),
    mcq("Two annotators labelled support tickets. One labels every 'refund' ticket as 'billing', the other as 'complaint'. Compared with random label flips, this systematic noise is:",
        ["More harmful: the model learns the annotator's rule as if it were truth, and more data won't average it out",
         "Less harmful, because it's consistent",
         "Identical in effect to random noise",
         "Harmless if you use class weights"], 0,
        "Random errors cancel with more data. Do consistent errors cancel?",
        "Random noise mostly adds variance; systematic (class-conditional) noise adds bias. Fix it at the source: clearer guidelines, an adjudication step, and agreement metrics per class.",
        analogy='Like a test that is always wrong in the same way: rerunning it a thousand times never exposes the bug.',
        topic="quality", level=4),

    # ------------------------------------------------------------------ feature-eng
    out("""import numpy as np
print(np.log1p(np.array([0, 9, 99])).round(2))""",
        ["[0.   2.3  4.61]", "[-inf  2.2  4.6 ]", "[  1.  10. 100.]", "[0. 1. 2.]"], 0,
        "log1p(x) = log(1 + x).",
        "Counts and amounts often include 0, where log(0) = -inf. log1p keeps 0 at 0 and still compresses the long tail.",
        topic="feature-eng", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"user": ["a", "a", "b"], "spend": [100, 300, 50]})
df["user_avg"] = df.groupby("user")["spend"].transform("mean")
df["vs_avg"] = df["spend"] / df["user_avg"]
print(df["vs_avg"].tolist())""",
        ["[0.5, 1.5, 1.0]", "[1.0, 1.0, 1.0]", "[100.0, 300.0, 50.0]", "[0.25, 0.75, 1.0]"], 0,
        "transform('mean') puts each user's average back on every row.",
        "'This purchase vs the user's usual spend' is a classic fraud feature. Careful in a real system: compute the average from PAST purchases only, or it leaks the future.",
        topic="feature-eng", level=2),
    mcq("A linear model must learn 'risky if exactly one of (new_device, foreign_ip) is true'. It fails. What feature engineering helps most?",
        ["Add an interaction feature such as new_device XOR foreign_ip (or product terms)",
         "Scale both features",
         "One-hot encode both features",
         "Remove one of the features"], 0,
        "A linear model adds weighted features; can a sum express 'exactly one'?",
        "XOR isn't linearly separable, so no weighting of the two raw columns works. An interaction column makes it linear. Trees and neural nets can learn interactions themselves; linear models need them handed over.",
        topic="feature-eng", level=3),
    out("""import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
rng = np.random.default_rng(0)
y = rng.integers(0, 2, 300)
signal = (y + rng.normal(0, 0.6, 300)).reshape(-1, 1)
noisy = np.c_[signal, rng.normal(0, 1, (300, 200))]
a = cross_val_score(KNeighborsClassifier(), signal, y, cv=5).mean()
b = cross_val_score(KNeighborsClassifier(), noisy, y, cv=5).mean()
print(a > 0.75, b < 0.65)""",
        ["True True", "True False", "False True", "False False"], 0,
        "200 noise columns now dominate every distance.",
        "Adding 200 useless features drowns the one informative column, and kNN drops towards chance. More features is not more information: irrelevant columns add noise and cost, especially for distance-based models.",
        topic="feature-eng", level=3),
    mcq("Your learning curve shows training and validation scores already converged at a mediocre value as data grows. What is most likely to help?",
        ["Better features or a more expressive model; more data of the same kind won't move a converged curve",
         "Collecting 10x more rows of the same data",
         "More regularisation",
         "A larger test set"], 0,
        "Converged curves mean the model isn't limited by data; it's limited by what it can express.",
        "High bias (underfitting) is fixed by richer features/models; high variance (big train-val gap) is fixed by more data or regularisation. Reading the learning curve tells you where to spend effort.",
        diagram="""
 score
  |  train ----.___________
  |            ___________  <- converged, low
  |  val  ----'
  +-------------------------> rows
 gap ~ 0: more data won't help
""",
        topic="feature-eng", level=4),
    mcq("A random forest's impurity-based feature_importances_ ranks a random 'customer_id' column (thousands of unique values) as the top feature. What should you do?",
        ["Distrust it: impurity importance favours high-cardinality features; check with permutation importance on held-out data",
         "Keep customer_id, it is clearly the best predictor",
         "Increase the number of trees",
         "Scale customer_id first"], 0,
        "Many unique values = many possible split points to overfit on.",
        "Impurity importance is computed on training data and inflates features with many split points. Permutation importance on a validation set measures what actually helps generalisation.",
        topic="feature-eng", level=4),
    mcq("With 2,000 candidate features and 500 rows, you pick the 20 most correlated with y on the full dataset, then cross-validate. Scores look great. What is wrong?",
        ["The selection used all labels, including those of the validation folds, so noise features that match y by chance were chosen; selection must run inside each fold",
         "Nothing, correlation is a valid selection method",
         "20 features is too few",
         "Correlation can't be computed with 500 rows"], 0,
        "Among 2,000 pure-noise columns, how many correlate with y by luck?",
        "Feature selection is a fit step that uses y. Done outside CV it leaks the labels and makes noise look predictive. Wrap SelectKBest and the model in one Pipeline.",
        topic="feature-eng", level=4),

    # ------------------------------------------------------------------ shift
    tf("A demand model trained only on summer data and deployed in winter is exposed to dataset shift.", True,
       "Will winter inputs look like summer inputs?",
       "When deployment data comes from a different distribution than training data, the model is extrapolating. Train on data that covers the conditions it will face.",
       topic="shift", level=1),
    mcq("A loan model is trained only on applicants who were APPROVED (only they have repayment labels). What bias does this create?",
        ["Selection bias: rejected applicants never got labels, so the model knows little about the people it is now asked to judge",
         "Label noise",
         "Concept drift",
         "No bias, approved loans are representative"], 0,
        "Whose outcome is never observed?",
        "Labels exist only for one slice of the population, chosen by the old policy. Fixes include random exploration (approving a small random sample) and reject-inference methods. Any feedback-loop system has this.",
        diagram="""
 applicants -> old policy -> approved -> label (repaid?)
                   |
                   +-------> rejected -> no label, ever
""",
        topic="shift", level=4),
    mcq("Your spam model was trained when 50% of emails were spam; now only 10% are, but spam still looks like spam. Precision dropped. This is:",
        ["Label (prior) shift: p(y) changed while p(x given y) stayed the same; adjust the threshold or priors",
         "Concept drift",
         "Covariate shift in a single feature",
         "Data versioning failure"], 0,
        "What changed: how spam looks, or how much spam there is?",
        "Under label shift the class-conditional patterns are stable, so you can correct by re-estimating the new prior and adjusting probabilities/threshold, without retraining from scratch.",
        topic="shift", level=3),
    out("""import numpy as np
from scipy.stats import ks_2samp
rng = np.random.default_rng(0)
train_age = rng.normal(35, 8, 2000)
prod_same = rng.normal(35, 8, 2000)
prod_old = rng.normal(42, 8, 2000)
print(ks_2samp(train_age, prod_same).pvalue < 0.01, ks_2samp(train_age, prod_old).pvalue < 0.01)""",
        ["False True", "True True", "False False", "True False"], 0,
        "A small p-value means the two samples very likely come from different distributions.",
        "The Kolmogorov-Smirnov test compares two distributions of one feature. The +7-year shift is flagged; the same-distribution sample isn't. With huge samples even tiny, harmless shifts get flagged, so also look at the size of the change.",
        topic="shift", level=3),
    out("""import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
rng = np.random.default_rng(0)
train = rng.normal(0, 1, (300, 3))
prod = rng.normal(0, 1, (300, 3)); prod[:, 2] += 2
X = np.r_[train, prod]; is_prod = np.r_[np.zeros(300), np.ones(300)]
auc = cross_val_score(RandomForestClassifier(random_state=0), X, is_prod, cv=5, scoring="roc_auc").mean()
print(auc > 0.8)""",
        ["True", "False", "ValueError", "nan"], 0,
        "Column 2 moved by 2 standard deviations in production.",
        "Adversarial validation in code: if a classifier can tell train rows from production rows (AUC well above 0.5), the data shifted. Its feature importances would point at column 2.",
        topic="shift", level=4),
    mcq("A product team deploys a model that decides which users get a discount, then retrains monthly on the resulting purchases. What can go wrong over time?",
        ["A feedback loop: the model's own decisions shape the next training data, so it confirms its past choices and rarely learns about users it never treated",
         "Nothing, more data always helps",
         "The model will become perfectly calibrated",
         "Only the scaler will drift"], 0,
        "Who generates the labels the next model learns from?",
        "When predictions change the world that produces the labels, training data stops being a neutral sample. Keep a small random holdout group (exploration) to get unbiased labels and to measure true impact.",
        analogy="Like a cache that only stores what it already served: popular items get more popular, and you never learn about the rest.",
        diagram="""
 model --> decides who gets a discount --> purchases
   ^                                          |
   +------------- retrain on these -----------+
""",
        topic="shift", level=4),

    # ------------------------------------------------------------------ versioning
    mcq("Why not just commit your 50 GB training CSV to the git repo?",
        ["Git keeps every version forever in every clone, so repos become huge and slow; tools like DVC store the data elsewhere and commit a small hash pointer",
         "Git can't store CSV files",
         "CSV files can't be versioned",
         "Data doesn't need versioning"], 0,
        "What does git clone download?",
        "Git is built for small text diffs. Data tools (DVC, LakeFS, Delta tables) keep the bytes in object storage and put a tiny pointer file (content hash + path) in git, so the commit still pins the exact data.",
        diagram="""
 git repo:  train.py   data.csv.dvc  (md5: 3f2a...)
                             |
 object store:  s3://bucket/3f/2a...  (50 GB file)
""",
        topic="versioning", level=3),
    tf("Setting random_state in train_test_split is enough to make a whole training run reproducible.", False,
       "List everything else that influences the trained model.",
       "You also need the exact data version, code commit, library versions, hyperparameters and every other seed (model init, shuffling, GPU nondeterminism). The split seed is just one input.",
       topic="versioning", level=3),
    out("""import hashlib
import pandas as pd
def h(df):
    return hashlib.sha256(df.to_csv(index=False).encode()).hexdigest()[:8]
a = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
b = a.iloc[::-1]
c = a[["y", "x"]]
print(h(a) == h(b), h(a) == h(c), h(a) == h(b.sort_values("x")))""",
        ["False False True", "True True True", "False False False", "True False True"], 0,
        "A hash sees bytes; row order and column order change the bytes.",
        "Same logical data in a different row or column order gives a different hash. Canonicalise (sort rows, fix column order, fix float formatting) before hashing if you want 'same data, same hash'.",
        topic="versioning", level=4),
    mcq("Your training script loads data with SELECT * FROM orders WHERE order_date < '2026-10-01'. Rerunning it a month later gives a different model. Most likely cause?",
        ["Late-arriving or updated rows (refunds, corrections) changed the result of the same query; snapshot the extracted data and version the snapshot",
         "SQL is non-deterministic by design",
         "The date filter is wrong",
         "The model has a memory leak"], 0,
        "Does a query pin the data, or just describe it?",
        "A query is a recipe, not a version: backfills, late events and corrections change its output. Save the exact extract (with a content hash) or use a table format with time travel, and log which version trained each model.",
        analogy="Like depending on 'latest' instead of a pinned version: the same build script produces a different binary next month.",
        topic="versioning", level=4),
    mcq("A feature store offers 'point-in-time joins' when building training sets. What problem do they solve?",
        ["For each training row they join feature values as they were at that row's timestamp, not today's values, preventing future leakage",
         "They make joins faster",
         "They remove duplicate users",
         "They encrypt features"], 0,
        "A customer's 'lifetime spend' today is bigger than it was last March.",
        "Joining today's feature values to last year's labels leaks the future. Point-in-time joins look up the latest value BEFORE each event's timestamp, matching what production would have seen.",
        diagram="""
 label event at 10 Mar
 feature log:  1 Mar=500   8 Mar=520  |  20 Mar=900
                           ^ use this |  future: skip
""",
        topic="versioning", level=4),

    # ------------------------------------------------------------------ col-pipelines
    mcq("What does sklearn's ColumnTransformer do?",
        ["Applies different preprocessing to different columns (e.g. scale numeric, one-hot categorical) and joins the results",
         "Renames columns",
         "Converts a DataFrame to a list",
         "Splits columns into train and test"], 0,
        "Real tables have mixed column types.",
        "It routes each group of columns to its own transformer and concatenates the outputs side by side, so one object handles a whole mixed-type table.",
        diagram="""
 age, income ---> StandardScaler ---\\
                                     +--> [features]
 city        ---> OneHotEncoder  ---/
""",
        topic="col-pipelines", level=2),
    out("""import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
df = pd.DataFrame({"age": [20, 30, 40, 50], "income": [1, 2, 3, 4],
                   "city": ["BLR", "MUM", "DEL", "BLR"]})
ct = ColumnTransformer([("num", StandardScaler(), ["age", "income"]),
                        ("cat", OneHotEncoder(), ["city"])])
print(ct.fit_transform(df).shape)""",
        ["(4, 5)", "(4, 3)", "(4, 6)", "(3, 5)"], 0,
        "2 scaled numeric columns + one column per city.",
        "2 numeric + 3 one-hot (BLR, DEL, MUM) = 5 output columns, 4 rows.",
        topic="col-pipelines", level=2),
    out("""import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
df = pd.DataFrame({"age": [20, 30], "city": ["BLR", "MUM"]})
ct = ColumnTransformer([("num", StandardScaler(), ["age"]),
                        ("cat", OneHotEncoder(), ["city"])]).fit(df)
print(ct.get_feature_names_out().tolist())""",
        ["['num__age', 'cat__city_BLR', 'cat__city_MUM']", "['age', 'city_BLR', 'city_MUM']", "['num__age', 'cat__city']", "['x0', 'x1', 'x2']"], 0,
        "Names are prefixed with the transformer's name and a double underscore.",
        "get_feature_names_out tells you which output column is which, essential for reading coefficients or feature importances after preprocessing.",
        topic="col-pipelines", level=3),
    out("""import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
df = pd.DataFrame({"age": [20, 30, 40], "income": [1, 2, 3], "notes": ["a", "b", "c"]})
ct = ColumnTransformer([("num", StandardScaler(), ["age"])])
print(ct.fit_transform(df).shape)""",
        ["(3, 1)", "(3, 2)", "(3, 3)", "ValueError"], 0,
        "What is the default for columns you didn't list?",
        "remainder='drop' is the default: unlisted columns (income, notes) silently disappear. Use remainder='passthrough' if you want to keep them, and check the output shape.",
        topic="col-pipelines", level=3),
    out("""import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
df = pd.DataFrame({"age": [20, 30, 40, 50], "city": ["BLR", "MUM", "BLR", "DEL"], "y": [0, 1, 0, 1]})
ct = ColumnTransformer([("num", StandardScaler(), ["age"]), ("cat", OneHotEncoder(), ["city"])])
p = make_pipeline(ct, LogisticRegression()).fit(df[["age", "city"]], df.y)
print(p.predict(df[["city", "age"]]).tolist())""",
        ["[0, 1, 0, 1]", "ValueError", "[1, 0, 1, 0]", "KeyError"], 0,
        "The ColumnTransformer was told columns by NAME.",
        "When columns are selected by name from a DataFrame, reordered columns at predict time still route correctly. Pass a NumPy array instead and selection is by position, where a reorder silently scrambles features.",
        topic="col-pipelines", level=4),
    mcq("The data team trained with a Python Pipeline; the backend team re-implemented the scaling in Java using sample std (n-1) and a hand-written category map. Production accuracy is 6 points below offline. What is the best fix?",
        ["Ship the fitted preprocessing + model as one artifact (or export it, e.g. ONNX) so training and serving run identical transforms",
         "Retrain with more data",
         "Lower the decision threshold",
         "Add monitoring and accept the gap"], 0,
        "The model is fine; the inputs it sees in production are different.",
        "This is training/serving skew. Two implementations of 'the same' preprocessing drift apart (ddof, category order, rounding, missing handling). One artifact used in both places removes the whole class of bug.",
        analogy="Like building a release binary separately for staging and prod from slightly different code: tests pass in one and fail in the other.",
        topic="col-pipelines", level=4),
    tf("Saving the whole fitted Pipeline (preprocessing + model) with joblib is safer than saving only the model.", True,
       "What else does a raw request need before the model can read it?",
       "The model only understands scaled, encoded inputs. Saving the pipeline keeps the learned means, category lists and imputation values together with the weights, so serving can't forget or re-learn them.",
       topic="col-pipelines", level=2),
    mcq("A Pipeline is pickled with scikit-learn 1.6 and loaded in a service running 1.3. What should you expect?",
        ["It may fail to load or behave differently; pin the same library versions in training and serving (or use a portable format)",
         "It always works identically",
         "sklearn converts it automatically",
         "Only the predictions' dtype changes"], 0,
        "A pickle stores internal object state, not a stable file format.",
        "Pickled sklearn objects aren't guaranteed to work across versions; sklearn warns about it. Pin the environment (lockfile, Docker image) along with the model, the same way you pin dependencies for a service.",
        analogy='Like deserialising a Java object with a different class version: the bytes load into a class that no longer matches.',
        topic="col-pipelines", level=3),

    # ------------------------------------------------------------------ genai-data
    mcq("For fine-tuning an LLM on customer-support chats, what plays the role of X and y?",
        ["X = the conversation so far (prompt); y = the ideal assistant reply",
         "X = the reply; y = the customer's name",
         "X = ticket IDs; y = timestamps",
         "There are no X and y in fine-tuning"], 0,
        "Supervised fine-tuning is still supervised learning.",
        "Each training example is an input (system prompt + conversation) and a target (the reply you want). The model is trained to produce y given X, token by token.",
        topic="genai-data", level=1),
    mcq("Before fine-tuning on raw support transcripts, which step matters most for privacy and compliance?",
        ["Detect and remove or mask PII (names, phone numbers, emails, card numbers)",
         "Convert everything to upper case",
         "Shuffle the words in each chat",
         "Remove all punctuation"], 0,
        "Fine-tuned models can repeat what they were trained on.",
        "LLMs can memorise and regurgitate training text. Mask PII before training (and before sending data to any external API), and keep an audit trail of what was removed.",
        analogy="Like logging raw request bodies with passwords in them: once written, copies spread everywhere and can't be recalled.",
        topic="genai-data", level=2),
    out("""import json
rows = [{"messages": [{"role": "user", "content": "Hi"},
                      {"role": "assistant", "content": "Hello!"}]},
        {"messages": [{"role": "user", "content": "Bye"},
                      {"role": "assistant", "content": "See you"}]}]
jsonl = "\\n".join(json.dumps(r) for r in rows)
print(len(jsonl.splitlines()), json.loads(jsonl.splitlines()[1])["messages"][1]["content"])""",
        ["2 See you", "4 See you", "2 Bye", "1 Hello!"], 0,
        "JSONL = one JSON object per line.",
        "Fine-tuning data is usually JSONL: one example per line, each a list of chat messages. Easy to stream, append and count, and one bad line doesn't corrupt the whole file.",
        analogy='Like newline-delimited JSON logs: append-only, streamable and easy to grep.',
        topic="genai-data", level=2),
    out("""a = "how do i reset my password please"
b = "how can i reset my password"
A, B = set(a.split()), set(b.split())
print(round(len(A & B) / len(A | B), 2))""",
        ["0.62", "0.71", "0.83", "1.0"], 0,
        "Jaccard = shared words / all distinct words.",
        "5 shared words (how, i, reset, my, password) out of 8 distinct = 0.625, printed as 0.62. Near-duplicate detection (e.g. MinHash, which approximates Jaccard fast) flags pairs above a threshold so templates don't flood training or leak into the eval set.",
        diagram="""
 A: how do i reset my password please
 B: how can i reset my password
 shared (5): how i reset my password
 union  (8): + do please can
""",
        topic="genai-data", level=3),
    out("""texts = ["short one", "a " * 600, "medium length text " * 50, "ok"]
max_tokens = 512
lengths = [len(t.split()) for t in texts]
print(lengths, sum(n > max_tokens for n in lengths))""",
        ["[2, 600, 150, 1] 1", "[2, 600, 150, 1] 2", "[9, 1200, 950, 2] 2", "[2, 600, 50, 1] 1"], 0,
        "split() splits on whitespace; 'medium length text ' has 3 words.",
        "Check the length distribution before training: examples beyond the context limit get truncated, and the model may never see their endings. Real pipelines count tokens with the model's tokenizer, not words.",
        topic="genai-data", level=2),
    mcq("You generate 50,000 synthetic Q&A pairs with a strong LLM to fine-tune a smaller model. Which risk is most important to manage?",
        ["Synthetic data inherits the generator's errors and style, and may paraphrase your eval questions; filter for quality and dedupe against the eval set",
         "Synthetic data is always better than real data",
         "Small models can't learn from synthetic data",
         "There are no risks if the generator is strong"], 0,
        "What does the generator know, and what did you prompt it with?",
        "Synthetic data is fast but not free: mistakes become 'ground truth', diversity collapses to the generator's style, and if you seeded it with eval-like questions you've leaked the test. Check licences, too.",
        topic="genai-data", level=3),
    mcq("In supervised fine-tuning of a chat model, the loss is usually computed only on the assistant's tokens, not on the user's. Why?",
        ["You want the model to learn to produce replies, not to imitate user messages; prompt tokens are context, not targets",
         "User tokens can't be tokenised",
         "It doubles the training speed",
         "Assistant tokens are always shorter"], 0,
        "Which part of the example is y?",
        "Masking prompt tokens from the loss keeps the target equal to the reply. Training on everything teaches the model to also generate user-style text, and long prompts would dominate the loss.",
        topic="genai-data", level=3),
    mcq("You fine-tune on 20,000 instructions and evaluate on 500 held-out ones. Exact-hash dedup between the two sets found 0 overlaps, yet eval scores look too good. What is the likely issue?",
        ["Near-duplicates (same question with small wording or whitespace changes) slipped through; use fuzzy dedup such as MinHash or embedding similarity",
         "Exact-hash dedup is always sufficient",
         "The eval set is too large",
         "The tokenizer is wrong"], 0,
        "A hash changes completely if a single character changes.",
        "Exact hashes catch only byte-identical copies. Templates and lightly edited questions are near-duplicates: they need similarity-based dedup across the train/eval boundary.",
        topic="genai-data", level=4),
    mcq("Team A fine-tunes on 100,000 scraped, noisy Q&A pairs; team B on 2,000 carefully reviewed, diverse examples. For teaching an already-capable base model a response style, which usually wins?",
        ["Team B: for style/format alignment, quality and diversity matter more than raw volume",
         "Team A, because more data always wins",
         "They are always equal",
         "Neither; fine-tuning can't change style"], 0,
        "The base model already has the knowledge; what are you really teaching?",
        "Instruction tuning mostly teaches format and behaviour. A small, clean, diverse set often beats a large noisy one, which also teaches the noise. Budget for review, not just scraping.",
        analogy="Like onboarding a senior hire: a short, accurate style guide beats a dump of every old ticket, mistakes included.",
        topic="genai-data", level=4),
    mcq("Your RAG eval set was generated by asking an LLM to write questions from 200 document chunks. Retrieval recall is 0.97. Why might this overstate real performance?",
        ["Generated questions reuse the chunk's exact wording, so retrieval is easy; real users phrase things differently and ask across chunks",
         "Recall can't exceed 0.9",
         "LLM-written questions are always wrong",
         "The vector store was too small"], 0,
        "Where did the question's words come from?",
        "Questions written from a chunk share its vocabulary, an easy match for any retriever. Mix in real user queries from logs and multi-chunk questions, and keep that eval set separate from prompt tuning.",
        topic="genai-data", level=4),

    # ------------------------------------------------------------------ fills
    fill("ColumnTransformer silently drops columns you didn't list, unless you pass remainder='________'.",
         "passthrough",
         "The opposite of 'drop': let them pass.",
         "The default remainder='drop' is a common source of 'where did my column go?'. remainder='passthrough' keeps unlisted columns unchanged at the end of the output.",
         topic="col-pipelines", level=3),
    fill("The NumPy function that averages an array while skipping NaN values is np.________.",
         "nanmean",
         "NaN-aware versions of NumPy reductions start with 'nan'.",
         "np.mean propagates NaN; np.nanmean (and nansum, nanmedian, nanstd) ignore missing values, matching pandas' default skipna=True.",
         topic="missing", level=2),
    fill("The sklearn wrapper that refits a classifier's probabilities so they match real frequencies (e.g. after class weighting) is ________.",
         "CalibratedClassifierCV",
         "It lives in sklearn.calibration.",
         "CalibratedClassifierCV fits a sigmoid (Platt) or isotonic mapping on held-out folds, so a predicted 0.2 really means about 20% of such cases are positive.",
         topic="imbalance", level=3),
]
