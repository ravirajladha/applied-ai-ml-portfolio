from helpers import mcq, tf, out, fill

SUBJECT = "ml-splits"

TOPICS = [
    ("purpose", "Why train / validation / test"),
    ("ratios", "Split ratios and dataset size"),
    ("tts", "train_test_split: random_state, stratify, shuffle"),
    ("kfold", "K-fold, stratified k-fold and leave-one-out"),
    ("group", "Group splits (same user, same patient)"),
    ("time-series", "Time-series splits and walk-forward"),
    ("nested-cv", "Hyperparameter tuning and nested CV"),
    ("leakage", "Data leakage"),
    ("pipelines", "Pipelines to prevent leakage"),
    ("test-reuse", "Test-set reuse and distribution mismatch"),
    ("llm-evals", "Splits for LLM evals and contamination"),
    ("compare", "Comparing models fairly (same folds, baselines, repeated CV)"),
]

QUESTIONS = [
    # ------------------------------------------------------------------ purpose
    mcq("Which part of the data does the model actually learn its weights from?",
        ["The training set", "The validation set", "The test set", "All three equally"], 0,
        "Weights = what gets adjusted during learning.",
        "Only the training set is used to fit weights. Validation is for choosing settings, test is for the final score.",
        topic="purpose", level=1),
    mcq("You report one final number to your manager: 'the model is 91% accurate on new data'. Which set should that number come from?",
        ["The test set, used once at the end", "The training set", "The validation set you tuned on", "Whichever set gives the best number"], 0,
        "Which set has had no influence on any decision?",
        "The test set is the untouched final exam. Validation scores are slightly optimistic because you picked the model that did best on them.",
        analogy="Like a release check on a staging box nobody has been tweaking: it tells you how prod will behave.",
        topic="purpose", level=1),
    tf("A 'hyperparameter' is a setting you choose before training (like tree depth), not a weight the model learns.", True,
       "Who sets it: you or the training loop?",
       "Hyperparameters are knobs you pick (depth, learning rate, regularisation strength). The validation set helps you pick them.",
       topic="purpose", level=1),
    mcq("A model gets 100% on the training set. What does that tell you about how it will do on new data?",
        ["Almost nothing on its own: it may have memorised", "It will also get about 100%", "It will get about 50%", "The test set is now unnecessary"], 0,
        "Can a lookup table also score 100% on data it has seen?",
        "Training accuracy only says the model fits what it saw. A held-out set is needed to measure generalisation (doing well on unseen data).",
        analogy="A unit test that checks a hard-coded return value passes, but proves nothing about real inputs.",
        topic="purpose", level=1),
    fill("The set used to compare models and pick hyperparameters, between train and test, is the ________ set.",
         "validation",
         "Also called the dev set.",
         "Train fits weights, validation picks settings, test gives the final unbiased score.",
         topic="purpose", level=1),
    mcq("Why is it a problem to choose hyperparameters using the test set?",
        ["The test score is then biased upward: it no longer measures unseen data",
         "It makes training slower",
         "sklearn raises an error",
         "The test set becomes smaller"], 0,
        "Each time you pick based on a score, that score stops being 'unseen'.",
        "Every decision made by looking at a set leaks a little information from it. Keep the test set for one final check.",
        topic="purpose", level=2),
    mcq("After tuning on validation and checking the test set once, what is a common and acceptable final step before deploying?",
        ["Retrain the chosen configuration on train + validation (or all data) and ship that",
         "Keep tuning until the test score improves",
         "Throw away the test set and report the validation score",
         "Train a new model on the test set only"], 0,
        "Once decisions are frozen, more data usually helps.",
        "With the configuration fixed, refitting on more data typically gives a slightly better model. The test score you already measured is the estimate you report.",
        topic="purpose", level=3),

    # ------------------------------------------------------------------ ratios
    mcq("Which split is a common default for a medium-sized dataset (say 10,000 rows)?",
        ["70 / 15 / 15 (train / val / test)", "10 / 10 / 80", "50 / 0 / 50", "99 / 1 / 0"], 0,
        "Most data goes to learning.",
        "Most rows train the model; enough are held back for reliable validation and test scores. 70/15/15 or 80/10/10 are typical.",
        topic="ratios", level=1),
    out("from sklearn.model_selection import train_test_split\nX = list(range(100))\nX_train, X_test = train_test_split(X, test_size=0.2, random_state=0)\nprint(len(X_train), len(X_test))",
        ["80 20", "20 80", "100 20", "80 19"], 0,
        "test_size=0.2 means 20% of 100.",
        "test_size is the fraction held out: 20 rows for test, the other 80 for training.",
        topic="ratios", level=1),
    out("from sklearn.model_selection import train_test_split\nX = list(range(10))\na, b = train_test_split(X, test_size=0.25, random_state=0)\nprint(len(a), len(b))",
        ["7 3", "8 2", "7.5 2.5", "ValueError"], 0,
        "0.25 x 10 = 2.5. Which way does sklearn round the test side?",
        "sklearn rounds the test size UP (ceil(2.5) = 3) and gives the rest to train.",
        topic="ratios", level=2),
    mcq("You have 10 million labelled rows. Why might a 98 / 1 / 1 split be perfectly sensible?",
        ["1% is still 100,000 rows, plenty for a stable score",
         "Big datasets must always use 98/1/1",
         "Test sets above 1% cause overfitting",
         "Validation is not needed for large data"], 0,
        "What matters for a reliable score: the percentage or the count?",
        "The noise in a measured accuracy depends on the number of test examples, not the percentage. With huge data, a small fraction is already a large count.",
        topic="ratios", level=2),
    mcq("A test set has 100 examples and the model scores 90% accuracy. Roughly how uncertain is that number (one standard error)?",
        ["About +/- 3 percentage points", "About +/- 0.1 points", "About +/- 30 points", "Zero: accuracy is exact"], 0,
        "Standard error of a proportion is sqrt(p(1-p)/n).",
        "sqrt(0.9 x 0.1 / 100) = 0.03. Two models 2 points apart on 100 test examples are not reliably different.",
        topic="ratios", level=3),
    out("import math\np, n = 0.9, 1000\nse = math.sqrt(p * (1 - p) / n)\nprint(round(se * 100, 1))",
        ["0.9", "3.0", "0.3", "9.0"], 0,
        "Ten times more test rows shrinks the error by sqrt(10), not by 10.",
        "sqrt(0.09/1000) = 0.0095, about 0.9 points. Going from 100 to 1000 test rows cut the error from 3.0 to about 0.9.",
        topic="ratios", level=3),
    tf("With a very small dataset (say 150 rows), a single 80/20 split gives a reliable estimate of model quality.", False,
       "How many rows land in that 20%?",
       "Only 30 test rows: the score swings a lot depending on which rows land there. Use k-fold cross-validation instead.",
       topic="ratios", level=2),

    # ------------------------------------------------------------------ tts
    mcq("What does random_state=42 do in train_test_split?",
        ["Fixes the shuffle so you get the same split every run", "Puts 42% of rows in test", "Uses 42 rows for test", "Sets the number of folds"], 0,
        "Think of it as a seed.",
        "random_state seeds the shuffle. Same seed, same data, same split: results are reproducible.",
        analogy="Like pinning a dependency version so every build is the same.",
        topic="tts", level=1),
    out("from sklearn.model_selection import train_test_split\nX = list(range(10))\na, _ = train_test_split(X, test_size=0.3, random_state=1)\nb, _ = train_test_split(X, test_size=0.3, random_state=1)\nprint(a == b)",
        ["True", "False", "None", "ValueError"], 0,
        "Same seed, same input.",
        "The same random_state on the same data gives the identical split, so the training lists are equal.",
        topic="tts", level=1),
    out("from sklearn.model_selection import train_test_split\nX = list(range(10))\na, b = train_test_split(X, test_size=0.3, shuffle=False)\nprint(b)",
        ["[7, 8, 9]", "[0, 1, 2]", "[2, 5, 8]", "[9, 8, 7]"], 0,
        "No shuffling means the order is kept.",
        "With shuffle=False the last 30% of rows (in original order) become the test set.",
        topic="tts", level=2),
    mcq("What does stratify=y do in train_test_split?",
        ["Keeps the class proportions of y the same in train and test",
         "Sorts the rows by y",
         "Removes rare classes",
         "Balances the classes to 50/50"], 0,
        "Strata = layers. Each class is a layer.",
        "Stratifying samples each class separately, so a 10% minority class is about 10% of both train and test. It does not rebalance.",
        topic="tts", level=1),
    out("import numpy as np\nfrom sklearn.model_selection import train_test_split\ny = np.array([0] * 90 + [1] * 10)\nX = np.arange(100).reshape(-1, 1)\n_, _, _, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=0)\nprint(len(y_te), int(y_te.sum()))",
        ["20 2", "20 10", "20 0", "10 2"], 0,
        "10% of the rows are class 1. What is 10% of the test set?",
        "Stratified: the test set keeps the 10% ratio, so 2 of its 20 rows are class 1.",
        topic="tts", level=2),
    tf("stratify=y rebalances an imbalanced dataset so both classes are 50/50 in training.", False,
       "Stratify copies proportions; it does not change them.",
       "Stratify preserves the original ratio in each split. Rebalancing is a separate step (class weights, resampling) done on training data only.",
       topic="tts", level=2),
    out("import numpy as np\nfrom sklearn.model_selection import train_test_split\nX = np.arange(10)\ny = np.array([0] * 5 + [1] * 5)\ntrain_test_split(X, y, stratify=y, shuffle=False)\nprint('done')",
        ["ValueError", "done", "TypeError", "IndexError"], 0,
        "Can you keep the original order AND sample each class evenly?",
        "sklearn raises ValueError: stratified splitting is not implemented for shuffle=False.",
        topic="tts", level=3),
    out("import numpy as np\nfrom sklearn.model_selection import train_test_split\nX = np.arange(10)\ny = np.array([0] * 9 + [1])\ntrain_test_split(X, y, test_size=0.3, stratify=y, random_state=0)\nprint('done')",
        ["ValueError", "done", "KeyError", "UserWarning"], 0,
        "How do you put a class with one example into BOTH sides?",
        "The least populated class has only 1 member, so it cannot appear in both splits. sklearn raises ValueError.",
        topic="tts", level=3),
    mcq("You need train/val/test from one array with train_test_split. What is the usual way?",
        ["Call it twice: first split off test, then split the remainder into train and val",
         "Pass test_size=0.15, val_size=0.15",
         "Pass three arrays and get three back automatically",
         "Use stratify='3way'"], 0,
        "train_test_split only ever makes two pieces per array.",
        "There is no val_size argument. Split off test first, then split the rest. Remember the second test_size is a fraction of the remainder.",
        topic="tts", level=2),
    out("from sklearn.model_selection import train_test_split\nX = list(range(100))\nrest, test = train_test_split(X, test_size=0.2, random_state=0)\ntrain, val = train_test_split(rest, test_size=0.25, random_state=0)\nprint(len(train), len(val), len(test))",
        ["60 20 20", "55 25 20", "60 25 15", "75 5 20"], 0,
        "The second split works on the 80 rows that are left.",
        "20 rows go to test; 25% of the remaining 80 is 20 for val; 60 are left for training.",
        topic="tts", level=2),
    mcq("Your regression target is house price and you want price levels balanced across train and test. stratify=y with float prices fails. What do you do?",
        ["Bin the target into quantiles (e.g. pd.qcut) and stratify on the bins",
         "Stratify on the raw floats after rounding to 2 decimals",
         "Regression cannot be split fairly",
         "Sort by price and use shuffle=False"], 0,
        "Stratify needs a small number of categories.",
        "Stratification needs discrete classes. Quantile bins give a handful of groups with enough members each. Rounded floats still leave most values unique.",
        topic="tts", level=3),

    # ------------------------------------------------------------------ kfold
    mcq("What is k-fold cross-validation?",
        ["Split data into k parts; train on k-1 and test on the remaining one, k times; average the scores",
         "Train k different models on the same data",
         "Repeat the train/test split with k different test sizes",
         "Train for k epochs"], 0,
        "Every row gets to be in the test part exactly once.",
        "Each fold is the held-out piece once. Averaging k scores is more reliable than one split.",
        diagram="""
 fold 1: [TEST][train][train][train][train]
 fold 2: [train][TEST][train][train][train]
 fold 3: [train][train][TEST][train][train]
 ...      score = mean of the 5 test scores
""",
        topic="kfold", level=1),
    out("from sklearn.model_selection import KFold\nX = list(range(10))\nfor _, test in KFold(n_splits=3).split(X):\n    print(test.tolist())",
        ["[0, 1, 2, 3]\n[4, 5, 6]\n[7, 8, 9]", "[0, 1, 2]\n[3, 4, 5]\n[6, 7, 8, 9]", "[0, 3, 6, 9]\n[1, 4, 7]\n[2, 5, 8]", "ValueError"], 0,
        "10 does not divide by 3. Which folds get the extra row?",
        "KFold without shuffle takes consecutive blocks; the first n % k folds get one extra row, so sizes are 4, 3, 3.",
        topic="kfold", level=2),
    tf("KFold shuffles the rows by default.", False,
       "Check the default of the shuffle argument.",
       "KFold(shuffle=False) is the default: folds are consecutive blocks. If your data is sorted (by class, by date), that matters a lot.",
       topic="kfold", level=2),
    out("import numpy as np\nfrom sklearn.model_selection import KFold\ny = np.array([0] * 5 + [1] * 5)\nfor _, test in KFold(n_splits=2).split(y):\n    print(np.bincount(y[test], minlength=2))",
        ["[5 0]\n[0 5]", "[3 2]\n[2 3]", "[2 3]\n[3 2]", "[5 5]\n[5 5]"], 0,
        "The labels are sorted and KFold does not shuffle.",
        "Each test fold is a single class, so the model trains on one class and is tested on the other. Use StratifiedKFold or shuffle=True.",
        topic="kfold", level=2),
    out("import numpy as np\nfrom sklearn.model_selection import StratifiedKFold\ny = np.array([0] * 5 + [1] * 5)\nX = np.zeros((10, 1))\nfor _, test in StratifiedKFold(n_splits=5).split(X, y):\n    print(np.bincount(y[test]), end=' ')",
        ["[1 1] [1 1] [1 1] [1 1] [1 1] ", "[2] [2] [1 1] [0 2] [0 2] ", "[2 0] [2 0] [1 1] [0 2] [0 2] ", "ValueError"], 0,
        "Stratified folds copy the 50/50 ratio into every fold.",
        "Each of the 5 test folds gets one row of each class, even though y is sorted.",
        topic="kfold", level=2),
    mcq("For a classifier, what does cross_val_score(model, X, y, cv=5) use as the splitter by default?",
        ["StratifiedKFold(5) without shuffling", "KFold(5) with shuffling", "ShuffleSplit(5)", "LeaveOneOut"], 0,
        "For classification, sklearn tries to keep class ratios.",
        "An integer cv with a classifier and a binary/multiclass y means StratifiedKFold(n_splits=5, shuffle=False). For a regressor it is plain KFold.",
        topic="kfold", level=3),
    out("from sklearn.model_selection import LeaveOneOut\nX = list(range(7))\nprint(LeaveOneOut().get_n_splits(X))",
        ["7", "1", "6", "2"], 0,
        "Each split leaves out exactly one row.",
        "Leave-one-out = k-fold with k = n. 7 rows give 7 splits, each with a test set of one row.",
        topic="kfold", level=1),
    mcq("Why is leave-one-out (LOO) rarely used on a dataset of 100,000 rows?",
        ["It trains 100,000 models and its estimate is often high-variance anyway",
         "It is not implemented in sklearn",
         "It leaks the test row into training",
         "It only works for regression"], 0,
        "Count the model fits.",
        "LOO needs n fits. Its estimate is nearly unbiased but can have high variance because the n training sets are almost identical. 5 or 10 folds are the usual trade-off.",
        topic="kfold", level=3),
    out("from sklearn.model_selection import KFold\nKFold(n_splits=5, random_state=0)\nprint('ok')",
        ["ValueError", "ok", "TypeError", "UserWarning"], 0,
        "Does a seed mean anything if nothing is shuffled?",
        "Since sklearn 0.24, setting random_state with shuffle=False raises ValueError: the seed would have no effect.",
        topic="kfold", level=3),
    mcq("You run 5-fold CV and get fold accuracies 0.81, 0.79, 0.95, 0.80, 0.82. What is the most useful thing to report?",
        ["The mean and the spread (e.g. 0.83 +/- 0.06), and look into why fold 3 differs",
         "Only 0.95, the best fold",
         "Only the last fold, 0.82",
         "Only the mean; the spread is noise"], 0,
        "One fold is out of line.",
        "The mean is your estimate; the spread tells you how stable it is. An outlier fold often means an odd slice of data (a duplicate cluster, a different time period).",
        topic="kfold", level=2),
    tf("In k-fold CV, every row is used for testing exactly once and for training k-1 times.", True,
       "Count how many folds each row sits in as the test part.",
       "The k test folds partition the data, so each row is tested once and trained on in the other k-1 rounds.",
       topic="kfold", level=1),

    # ------------------------------------------------------------------ group
    mcq("A dataset has 50 photos per patient. You split photos randomly into train and test. What goes wrong?",
        ["Photos of the same patient land on both sides, so the model can recognise the patient instead of the disease",
         "Nothing; random splits are always fine",
         "The test set becomes too small",
         "Stratification breaks"], 0,
        "Would a real new patient have any photos in the training set?",
        "Rows from the same patient are correlated. Random splitting lets the model 'remember' a person, so test scores are too high. Split by patient.",
        topic="group", level=2),
    out("import numpy as np\nfrom sklearn.model_selection import GroupKFold\nX = np.zeros((6, 1))\ngroups = np.array(['a', 'a', 'b', 'b', 'c', 'c'])\nfor tr, te in GroupKFold(n_splits=3).split(X, groups=groups):\n    print(sorted(set(groups[tr]) & set(groups[te])), end=' ')",
        ["[] [] [] ", "['a'] ['b'] ['c'] ", "['a', 'b'] [] [] ", "ValueError"], 0,
        "That is the whole promise of GroupKFold.",
        "GroupKFold never puts the same group in both train and test, so every overlap is empty.",
        topic="group", level=2),
    fill("The sklearn splitter that keeps all rows of one user in the same fold is ________.",
         "GroupKFold",
         "Like KFold, but it takes groups=.",
         "GroupKFold (and GroupShuffleSplit, LeaveOneGroupOut) split by a group id such as user, patient or session.",
         topic="group", level=1),
    mcq("You need folds that keep users separate AND keep the class ratio similar in each fold. Which splitter fits?",
        ["StratifiedGroupKFold", "StratifiedKFold", "GroupShuffleSplit with stratify=y", "TimeSeriesSplit"], 0,
        "Combine the two names.",
        "StratifiedGroupKFold keeps groups intact while trying to balance class proportions across folds.",
        topic="group", level=3),
    out("import numpy as np\nfrom sklearn.model_selection import GroupKFold\nX = np.zeros((6, 1))\ngroups = np.array([1, 1, 1, 1, 2, 3])\nprint(GroupKFold(n_splits=4).get_n_splits(X, groups=groups))\nlist(GroupKFold(n_splits=4).split(X, groups=groups))",
        ["4\nValueError", "4", "3", "3\nValueError"], 0,
        "get_n_splits just echoes the setting. Then count distinct groups.",
        "get_n_splits returns n_splits (4). Splitting needs at least 4 distinct groups but there are only 3, so split raises ValueError.",
        topic="group", level=3),
    mcq("A recommender model is evaluated with a random row split of (user, item, rating). The team ships it for brand-new users. Why is the offline score misleading?",
        ["Every test user also had ratings in training, so it never measured the cold-start case",
         "Ratings are not numbers",
         "Random splits remove popular items",
         "It is not misleading; rows are independent"], 0,
        "Match the split to the deployment situation.",
        "The split should copy how the model is used. For new users, hold out whole users (group split). For existing users predicting the future, split by time.",
        analogy="Like load-testing only with warm caches and then launching to traffic that always misses the cache.",
        topic="group", level=4),

    # ------------------------------------------------------------------ time-series
    mcq("You predict tomorrow's sales. Why is a random shuffled split a bad idea?",
        ["Training would contain days after the test days: the model peeks at the future",
         "Shuffling deletes rows",
         "Dates cannot be shuffled",
         "It makes the test set too large"], 0,
        "In production, what data will you have when you predict?",
        "In real use you only have the past. Train on earlier dates, test on later ones.",
        diagram="""
 time --->
 random:  T t T T t T t T   (future rows in training)
 correct: T T T T T | t t t  (train past, test future)
""",
        topic="time-series", level=1),
    out("from sklearn.model_selection import TimeSeriesSplit\nX = list(range(12))\nfor tr, te in TimeSeriesSplit(n_splits=3).split(X):\n    print(len(tr), te.tolist())",
        ["3 [3, 4, 5]\n6 [6, 7, 8]\n9 [9, 10, 11]", "4 [4, 5, 6, 7]\n8 [8, 9, 10, 11]\n12 []", "8 [8, 9, 10, 11]\n8 [4, 5, 6, 7]\n8 [0, 1, 2, 3]", "9 [9, 10, 11]\n9 [9, 10, 11]\n9 [9, 10, 11]"], 0,
        "The training window grows; the test window always comes right after it.",
        "TimeSeriesSplit uses test blocks of n // (n_splits + 1) = 3 rows, and trains on everything before each block (an expanding window).",
        topic="time-series", level=2),
    tf("In TimeSeriesSplit, every training index is smaller than every test index in the same split.", True,
       "That is the 'no peeking' rule.",
       "Training always comes from earlier rows, testing from later ones. This only works if your rows are sorted by time first.",
       topic="time-series", level=2),
    out("from sklearn.model_selection import TimeSeriesSplit\nX = list(range(10))\nfor tr, te in TimeSeriesSplit(n_splits=2, max_train_size=3).split(X):\n    print(tr.tolist(), te.tolist())",
        ["[1, 2, 3] [4, 5, 6]\n[4, 5, 6] [7, 8, 9]", "[0, 1, 2, 3] [4, 5, 6]\n[0, 1, 2, 3, 4, 5, 6] [7, 8, 9]", "[0, 1, 2] [3, 4, 5]\n[3, 4, 5] [6, 7, 8]", "ValueError"], 0,
        "max_train_size turns the expanding window into a sliding one, keeping the most recent rows.",
        "Test blocks are 10 // 3 = 3 rows: [4,5,6] and [7,8,9]. With max_train_size=3 only the 3 rows just before each test block are used.",
        topic="time-series", level=3),
    mcq("What is 'walk-forward' validation?",
        ["Repeatedly train on data up to time t, test on the next period, then move t forward",
         "Shuffling the rows before each epoch",
         "Testing on the oldest data first",
         "Training once and testing on every future day"], 0,
        "It walks along the timeline.",
        "Walk-forward (rolling-origin) evaluation copies how a forecasting model is retrained and used in production over time.",
        topic="time-series", level=2),
    mcq("Your label is 'did the customer churn in the next 30 days', and features use the last 7 days. Why add a gap (TimeSeriesSplit(gap=...)) between train and test?",
        ["Training rows near the boundary have labels that overlap the test period, which leaks future information",
         "Gaps make training faster",
         "sklearn requires gap > 0 for daily data",
         "To make the test set larger"], 0,
        "A training row's label looks 30 days ahead. Where does that window end?",
        "A row just before the test period has a label computed from days inside the test period. Dropping a buffer (a gap, also called purging or an embargo) removes that overlap.",
        topic="time-series", level=4),
    out("from sklearn.model_selection import TimeSeriesSplit\nX = list(range(10))\ntr, te = list(TimeSeriesSplit(n_splits=2, gap=2).split(X))[-1]\nprint(tr.tolist(), te.tolist())",
        ["[0, 1, 2, 3, 4] [7, 8, 9]", "[0, 1, 2, 3, 4, 5, 6] [7, 8, 9]", "[0, 1, 2, 3, 4] [5, 6, 7]", "[2, 3, 4, 5, 6] [7, 8, 9]"], 0,
        "The gap removes rows from the END of the training window.",
        "The last test block is still [7, 8, 9]; gap=2 drops rows 5 and 6 from training, leaving [0..4].",
        topic="time-series", level=4),
    mcq("Your fraud model has 0.97 AUC in shuffled 5-fold CV but 0.81 in a time-based backtest. Which explanation is most likely?",
        ["Fraud patterns drift over time, and shuffled CV let the model learn from future patterns",
         "Time-based splits are always pessimistic, so ignore them",
         "AUC is broken on time data",
         "The time-based test set had too many rows"], 0,
        "Fraudsters change tactics. Which split copies production?",
        "Shuffled CV mixes future fraud patterns into training. The backtest is the honest number; the gap measures how much the world shifts.",
        topic="time-series", level=3),

    # ------------------------------------------------------------------ nested-cv
    mcq("What does GridSearchCV do?",
        ["Tries every combination of the given hyperparameters with cross-validation and keeps the best",
         "Draws a grid plot of the data",
         "Splits the data into a grid of folds by row and column",
         "Trains one model on a grid of GPUs"], 0,
        "Grid = all combinations.",
        "It cross-validates each setting (e.g. every max_depth in a list) and refits the best one on all the data you gave it.",
        topic="nested-cv", level=1),
    out("from sklearn.model_selection import GridSearchCV\nfrom sklearn.tree import DecisionTreeClassifier\nfrom sklearn.datasets import load_iris\nX, y = load_iris(return_X_y=True)\ng = GridSearchCV(DecisionTreeClassifier(random_state=0), {'max_depth': [1, 2, 3, 4], 'min_samples_leaf': [1, 5]}, cv=5)\ng.fit(X, y)\nprint(len(g.cv_results_['params']), 8 * 5)",
        ["8 40", "6 30", "40 40", "8 8"], 0,
        "4 depths x 2 leaf sizes; each is run on 5 folds.",
        "The grid has 4 x 2 = 8 combinations, so 8 x 5 = 40 fits (plus one final refit of the best on all data).",
        topic="nested-cv", level=2),
    tf("gs.best_score_ from GridSearchCV is an unbiased estimate of how the chosen model will do on new data.", False,
       "You picked the maximum of many noisy scores.",
       "best_score_ is the best of many CV scores, so it is optimistically biased (the 'winner's curse'). Score on a held-out test set or use nested CV.",
       topic="nested-cv", level=3),
    mcq("What is nested cross-validation?",
        ["An inner CV loop picks hyperparameters; an outer CV loop scores the whole 'tune-then-fit' procedure on folds the tuning never saw",
         "Running k-fold twice with different seeds and averaging",
         "Cross-validating inside each tree of a random forest",
         "Using CV on the test set"], 0,
        "Two loops: one chooses, one judges.",
        "The outer loop treats 'run GridSearchCV' as the model. Its score is an honest estimate of the tuning process, not of one fixed setting.",
        diagram="""
 outer fold k:  [ outer-train            ][outer-test]
   inner CV on outer-train -> best params
   refit best on outer-train -> score on outer-test
 report: mean over outer folds
""",
        topic="nested-cv", level=3),
    out("from sklearn.model_selection import GridSearchCV, cross_val_score\nfrom sklearn.svm import SVC\nfrom sklearn.datasets import load_iris\nX, y = load_iris(return_X_y=True)\ninner = GridSearchCV(SVC(), {'C': [0.1, 1, 10]}, cv=3)\nscores = cross_val_score(inner, X, y, cv=4)\nprint(len(scores), 3 * 3 * 4)",
        ["4 36", "3 36", "12 36", "4 12"], 0,
        "cross_val_score returns one score per OUTER fold.",
        "4 outer scores. Inside each outer fold: 3 values of C x 3 inner folds = 9 fits (plus a refit), so 36 inner fits in total.",
        topic="nested-cv", level=3),
    mcq("With nested CV, different outer folds pick different best hyperparameters. What does that tell you?",
        ["The choice is unstable; the outer score estimates the tuning procedure, not one specific setting",
         "Nested CV is broken",
         "You must report the hyperparameters from the best outer fold",
         "The data has leakage"], 0,
        "What exactly is the outer loop evaluating?",
        "Nested CV evaluates 'tune then fit'. Unstable picks suggest the scores are close or the data is small. To ship, rerun the inner search on all data.",
        topic="nested-cv", level=4),
    mcq("You try 500 random hyperparameter settings and pick the best by 5-fold CV on 300 rows. The best CV accuracy is 0.88. Which statement is most accurate?",
        ["The true accuracy is probably lower; with many tries, some settings score high just by luck",
         "0.88 is exact because CV averages 5 folds",
         "More settings always make the estimate more accurate",
         "The estimate is pessimistic because each fold trains on less data"], 0,
        "The max of 500 noisy numbers is biased upward.",
        "Searching hard over noisy scores overfits the validation procedure itself. The more configurations tried, the bigger the optimism. Nested CV or a fresh test set corrects it.",
        topic="nested-cv", level=4),
    fill("In GridSearchCV the attribute that holds the winning setting is gs.________.",
         "best_params_",
         "It ends with an underscore like every fitted attribute.",
         "best_params_ is a dict of the chosen hyperparameters; best_estimator_ is the refitted model.",
         topic="nested-cv", level=2),

    # ------------------------------------------------------------------ leakage
    mcq("Which feature is an example of target leakage when predicting 'will this loan default?'",
        ["'number of collection calls made', which only happens after a default",
         "'applicant income at application time'",
         "'loan amount requested'",
         "'applicant age'"], 0,
        "Would you know the value at the moment you make the prediction?",
        "Target leakage = a feature that is only available because of (or after) the outcome. It gives great offline scores and fails in production.",
        topic="leakage", level=1),
    out("import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import cross_val_score\nrng = np.random.default_rng(0)\ny = rng.integers(0, 2, 200)\nX = np.c_[rng.normal(size=200), y + rng.normal(0, 0.1, 200)]\nprint(round(cross_val_score(LogisticRegression(), X, y, cv=5).mean(), 2))",
        ["1.0", "0.5", "0.75", "0.0"], 0,
        "The second column is basically the label plus a tiny bit of noise.",
        "A feature that is the label in disguise gives near-perfect scores. When a score looks too good to be true, look for leakage first.",
        topic="leakage", level=2),
    mcq("Which of these is preprocessing leakage?",
        ["Fitting a StandardScaler on the full dataset, then splitting into train and test",
         "Fitting the scaler on train, then transforming train and test with it",
         "Using a Pipeline with cross_val_score",
         "Dropping an ID column before training"], 0,
        "Where did the mean and standard deviation come from?",
        "If the scaler is fit on all data, the training data has been shaped by test-set statistics. Fit any preprocessing on train only.",
        analogy="Like seeding your unit tests with fixtures copied from the production database you're about to test against.",
        topic="leakage", level=2),
    out("import numpy as np\nfrom sklearn.preprocessing import StandardScaler\nX = np.array([[1.0], [2.0], [3.0], [100.0]])\ntrain, test = X[:3], X[3:]\nleaky = StandardScaler().fit(X)\nclean = StandardScaler().fit(train)\nprint(round(leaky.mean_[0], 1), round(clean.mean_[0], 1))",
        ["26.5 2.0", "2.0 2.0", "26.5 26.5", "2.0 26.5"], 0,
        "One scaler saw the test row with value 100.",
        "The leaky scaler's mean (26.5) is pulled by the test row. The clean one only knows the training rows (mean 2.0).",
        topic="leakage", level=2),
    tf("Removing exact duplicate rows before splitting can be important, because a duplicate in both train and test lets the model 'remember' the answer.", True,
       "What does the model do with a test row it has already seen?",
       "Duplicates across splits turn part of the test into a memory check. Deduplicate (or group near-duplicates) before splitting.",
       topic="leakage", level=2),
    out("import numpy as np\nfrom sklearn.model_selection import train_test_split\nX = np.array([[i % 5] for i in range(20)])\ntr, te = train_test_split(X, test_size=0.25, random_state=0)\nseen = {tuple(r) for r in tr}\nprint(sum(tuple(r) in seen for r in te), len(te))",
        ["5 5", "0 5", "1 5", "5 15"], 0,
        "There are only 5 distinct rows, each repeated 4 times.",
        "Every test row also appears in training, so the 'test' measures memory, not generalisation.",
        topic="leakage", level=3),
    mcq("You oversample the minority class (copying rows, or SMOTE) BEFORE splitting into train and test. What happens?",
        ["Copies or near-copies of the same rows land in both sets, so test scores are inflated",
         "Nothing; resampling before or after the split is the same",
         "The test set ends up with no minority rows",
         "sklearn refuses to split resampled data"], 0,
        "Where do the copies of one row end up?",
        "Resample only inside the training data (inside each CV fold). The test set must look like the real class distribution and contain no copies of training rows.",
        topic="leakage", level=3),
    mcq("You compute 'customer's average purchase over ALL their orders' and use it to predict whether a given order is returned. Why is that leaky in a time-based setting?",
        ["The average includes orders placed after the one being predicted",
         "Averages are not allowed as features",
         "It is a categorical feature",
         "It makes the model underfit"], 0,
        "At prediction time, which orders exist yet?",
        "Aggregates must be computed 'as of' the prediction time, only from earlier rows. Using the whole history pulls future information into each row.",
        topic="leakage", level=3),
    out("import numpy as np\nfrom sklearn.feature_selection import SelectKBest, f_classif\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import cross_val_score\nfrom sklearn.pipeline import make_pipeline\nrng = np.random.default_rng(0)\nX = rng.normal(size=(60, 2000)); y = rng.integers(0, 2, 60)\nXs = SelectKBest(f_classif, k=10).fit_transform(X, y)\nleaky = cross_val_score(LogisticRegression(), Xs, y, cv=5).mean()\nhonest = cross_val_score(make_pipeline(SelectKBest(f_classif, k=10), LogisticRegression()), X, y, cv=5).mean()\nprint(leaky > 0.8, honest < 0.65)",
        ["True True", "False True", "True False", "False False"], 0,
        "The features are pure noise. Where did the selection happen?",
        "Picking the 10 'best' noise features using all labels bakes the labels into X, so CV looks great. Inside a pipeline the selection is redone per fold and the score drops to chance.",
        topic="leakage", level=4),
    mcq("sklearn's TargetEncoder (replace a category by the mean target for that category) behaves differently in fit_transform(X, y) and fit(X, y).transform(X). Why?",
        ["fit_transform uses internal cross-fitting so each row's encoding is computed without its own label",
         "fit_transform ignores y",
         "transform adds random noise",
         "They are identical; it is a documentation error"], 0,
        "Encoding a row with a mean that includes its own label is leakage.",
        "Training rows get out-of-fold encodings from fit_transform, which stops the model learning from its own labels. Use fit_transform on train, transform on test.",
        topic="leakage", level=4),
    fill("A feature that is only known because of the outcome (e.g. 'refund issued' when predicting fraud) is called ________ leakage.",
         "target",
         "It leaks the target.",
         "Target leakage: the feature is a consequence of the label. Drop features that wouldn't exist at prediction time.",
         topic="leakage", level=1),

    # ------------------------------------------------------------------ pipelines
    mcq("How does an sklearn Pipeline help prevent leakage during cross-validation?",
        ["It refits every step (scaler, encoder, selector) on the training folds only, each round",
         "It encrypts the test set",
         "It removes duplicate rows",
         "It shuffles the data before each fold"], 0,
        "What gets fit inside each fold?",
        "cross_val_score clones and fits the whole pipeline per fold, so preprocessing never sees that fold's test rows.",
        analogy="Like building each CI run from a clean container instead of reusing a dirty workspace.",
        topic="pipelines", level=1),
    out("from sklearn.pipeline import make_pipeline\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.linear_model import LogisticRegression\npipe = make_pipeline(StandardScaler(), LogisticRegression())\nprint(list(pipe.named_steps))",
        ["['standardscaler', 'logisticregression']", "['StandardScaler', 'LogisticRegression']", "['step0', 'step1']", "['scaler', 'model']"], 0,
        "make_pipeline names steps automatically from the class names.",
        "make_pipeline uses the lower-cased class names as step names, so grid keys look like 'logisticregression__C'.",
        topic="pipelines", level=2),
    fill("In GridSearchCV over a pipeline, the grid key for the C of a step named 'clf' is '________'.",
         "clf__C",
         "Step name, double underscore, parameter name.",
         "Pipeline parameters are addressed as <step>__<param>, e.g. {'clf__C': [0.1, 1, 10]}.",
         topic="pipelines", level=2),
    tf("If you put a StandardScaler inside a Pipeline and pass the pipeline to GridSearchCV, the scaler is refit on each training fold.", True,
       "GridSearchCV clones the whole estimator it is given.",
       "The pipeline is the estimator, so every inner fold refits the scaler on its own training part. That's the point.",
       topic="pipelines", level=2),
    mcq("Which code has leakage?",
        ["X_s = StandardScaler().fit_transform(X); cross_val_score(SVC(), X_s, y, cv=5)",
         "cross_val_score(make_pipeline(StandardScaler(), SVC()), X, y, cv=5)",
         "sc = StandardScaler().fit(X_tr); SVC().fit(sc.transform(X_tr), y_tr)",
         "X_tr2 = StandardScaler().fit_transform(X_tr) (training data only)"], 0,
        "Look for a fit that sees all rows before CV starts.",
        "The first one fits the scaler on all of X, including every future test fold. The others only fit on training data.",
        topic="pipelines", level=2),
    mcq("You use ColumnTransformer with SimpleImputer(strategy='mean') and OneHotEncoder, wrapped in a Pipeline with a model. At predict time a new category appears. What setting keeps prediction from crashing?",
        ["OneHotEncoder(handle_unknown='ignore')", "SimpleImputer(strategy='most_frequent')", "Pipeline(memory=True)", "OneHotEncoder(sparse_output=False)"], 0,
        "By default the encoder raises on unseen categories.",
        "handle_unknown='ignore' encodes an unseen category as all zeros. Learning categories from the training data only is correct; the setting just handles surprises safely.",
        topic="pipelines", level=3),
    mcq("Why is the scaling leak in 'fit StandardScaler on all data' usually small, while feature selection on all data is often a huge leak?",
        ["The scaler uses only X (no labels); selection uses y, so it directly picks features that match the test labels",
         "Scaling never leaks anything",
         "Feature selection is not allowed in sklearn",
         "Scalers are refit automatically by sklearn"], 0,
        "Which step looks at the labels?",
        "Unsupervised steps leak only a little distribution information. Steps that use y (selection, target encoding, resampling) leak label information and can make noise look predictive.",
        topic="pipelines", level=4),

    # ------------------------------------------------------------------ test-reuse
    mcq("A team checks test accuracy after every experiment for three months and keeps the changes that raise it. What has happened?",
        ["They have slowly fit the test set; its score is now optimistic",
         "Nothing; looking at a score doesn't change the model",
         "The test set became a training set, so accuracy is now exact",
         "The model underfits"], 0,
        "Each decision based on the test score leaks a bit of it.",
        "Repeated peeking turns the test set into a validation set. Use a separate validation set for decisions and a fresh test set for the final number.",
        analogy="Like tweaking code until one flaky integration test passes, then calling the build green.",
        topic="test-reuse", level=2),
    tf("On Kaggle, a model that tops the public leaderboard often drops on the private leaderboard because people tuned to the public split.", True,
       "The public leaderboard is checked many times.",
       "Repeated submissions overfit the public split. The private split is the true held-out test, which is why rankings 'shake up'.",
       topic="test-reuse", level=2),
    mcq("Your training data is from 2023 and the test set is from 2025. Validation accuracy is 0.92 but test is 0.78. What is the most likely cause?",
        ["Distribution shift: the 2025 data differs from what the model learned on",
         "The model underfits the training data",
         "The test set is too large",
         "random_state was not set"], 0,
        "Did the world change between the two years?",
        "When validation is drawn like training but test comes from a different period or source, the drop measures shift. Build validation to look like the target data.",
        topic="test-reuse", level=3),
    mcq("What is 'adversarial validation'?",
        ["Train a classifier to tell training rows from test rows; if it succeeds (AUC well above 0.5) the splits differ",
         "Attack the model with adversarial examples",
         "Use the test set as validation",
         "Train two models and keep the one that disagrees most"], 0,
        "If you can tell them apart, they are not from the same distribution.",
        "Label train rows 0 and test rows 1 and fit a model. An AUC near 0.5 means similar distributions; a high AUC shows which features drifted.",
        topic="test-reuse", level=4),
    mcq("You must build a validation set when the test data comes from a different source (e.g. new hospital) than most training data. Best approach?",
        ["Make validation look like the target: hold out data from the new source (or the most similar source)",
         "Sample validation randomly from the training data",
         "Skip validation and use the test set",
         "Use the oldest data for validation"], 0,
        "Validation should predict test performance.",
        "Validation and test should come from the same distribution you care about. Otherwise you tune for the wrong target.",
        topic="test-reuse", level=3),
    mcq("A research field has used the same benchmark test set for 10 years. Why might published gains overstate real progress?",
        ["Many papers made design choices that suit that specific test set (adaptive overfitting to the benchmark)",
         "Benchmarks get easier over time",
         "Old test sets lose labels",
         "Accuracy can't be compared across years"], 0,
        "Thousands of researchers, one shared test set.",
        "The community as a whole has selected methods that do well on that set. Fresh test sets built the same way often show lower scores, though rankings are usually stable.",
        topic="test-reuse", level=4),

    # ------------------------------------------------------------------ llm-evals
    mcq("What does 'benchmark contamination' mean for an LLM?",
        ["Test questions (or their answers) appeared in the model's training data",
         "The benchmark has wrong labels",
         "The model is run on a dirty GPU",
         "The benchmark is too hard"], 0,
        "LLMs are trained on huge web crawls. What else is on the web?",
        "If the questions were in the pre-training data, a high score can be memorisation rather than ability.",
        analogy="Like a candidate who has already seen the exact interview questions online.",
        topic="llm-evals", level=1),
    tf("When you build an eval set for your own LLM app, you should not reuse the same examples as the few-shot examples in your prompt.", True,
       "Few-shot examples are part of the input.",
       "If an eval item is also a few-shot example, the model sees the answer in the prompt. Keep prompt examples, tuning examples and eval examples separate.",
       topic="llm-evals", level=1),
    mcq("You tweak a RAG prompt 30 times, each time checking the same 50 eval questions. What is the risk?",
        ["The prompt is tuned to those 50 questions; keep a held-out eval set for the final check",
         "No risk; prompts are not trained",
         "The model's weights change",
         "The vector database gets contaminated"], 0,
        "Prompt edits are hyperparameter choices too.",
        "Prompt engineering against one eval set overfits it like any tuning. Use a dev set for iteration and a separate test set you rarely look at.",
        topic="llm-evals", level=2),
    mcq("A common way labs check for contamination is n-gram overlap (e.g. 13-gram matches between test items and training text). What does it miss?",
        ["Paraphrased or translated copies of test items",
         "Exact copies of test items",
         "Test items with numbers",
         "It misses nothing"], 0,
        "Exact string matching only finds exact strings.",
        "Rewritten, reformatted or translated versions slip past n-gram filters but can still teach the answers. That's why fresh, dated or private benchmarks matter.",
        topic="llm-evals", level=3),
    mcq("A model scores much higher on a benchmark's original questions than on newly written questions of the same type and difficulty. What does this suggest?",
        ["Likely contamination or overfitting to the original benchmark",
         "The new questions have wrong labels",
         "The model has improved",
         "Benchmarks always get harder over time"], 0,
        "Same skill, different questions, big gap.",
        "If ability were the only factor, scores would be similar. A gap like this is evidence of memorisation or benchmark-specific tuning.",
        topic="llm-evals", level=3),
    mcq("You fine-tune an LLM on support tickets and evaluate on a random 10% of tickets. Many tickets are near-identical templates ('reset my password'). What split is more honest?",
        ["Deduplicate near-duplicates and split by time or by customer, so templates don't sit on both sides",
         "Random 10% is fine because tickets are text",
         "Use a bigger random test set",
         "Evaluate on the training set to check memorisation"], 0,
        "Near-duplicates across splits = memory test.",
        "Near-duplicate templates in both sets inflate scores. Deduplicate (e.g. MinHash), and split by time or group to match deployment.",
        topic="llm-evals", level=3),
    mcq("Some benchmarks embed a unique 'canary string' (a random GUID) in their files. What is it for?",
        ["If a model can complete the canary string, the benchmark was in its training data",
         "It encrypts the answers",
         "It speeds up evaluation",
         "It marks which questions are hard"], 0,
        "A random string has no other way into the model's memory.",
        "Data builders are asked to filter documents with the canary. If a model can reproduce it, the benchmark leaked into training.",
        topic="llm-evals", level=4),
    mcq("Your team uses an LLM-as-judge to grade outputs, and you tuned the judge prompt on the same 200 items you use to report final quality. What is wrong?",
        ["The judge was fit to those items, so the reported quality is optimistic; calibrate the judge on a separate labelled set",
         "Nothing; the judge isn't the model being evaluated",
         "LLM judges cannot be tuned",
         "200 items is too many"], 0,
        "The judge is part of the measuring instrument.",
        "Tuning the grader on your test items fits the measurement to that set. Keep a judge-calibration set separate from the final eval set.",
        topic="llm-evals", level=4),

    # ================================================================== added set 2
    # ------------------------------------------------------------------ purpose
    tf("On a medium-sized dataset you can skip a separate validation set by running cross-validation on the training data for tuning, keeping the test set for the end.", True,
       "CV does the validation set's job, many times over.",
       "Train+CV for choices, test once for the final number. CV uses data more efficiently than a single fixed validation split, at the cost of k times more training.",
       topic="purpose", level=2),
    mcq("You use early stopping: training halts when validation loss stops improving, at epoch 37. You then report that validation loss as the model's expected loss. What is the issue?",
        ["The validation set chose the stopping epoch, so it's now a tuning set and its score is optimistic; report a separate test score",
         "Early stopping can't use a validation set",
         "Nothing, validation loss is unbiased",
         "Epoch 37 is too early"], 0,
        "The epoch count is a hyperparameter. Who picked it?",
        "Early stopping is tuning: it selects the epoch with the best validation loss, which includes some luck. Like any selection, that score is biased upward. The test set gives the honest number.",
        diagram="""
 loss
  |  train  `-._____________
  |  val     `-.__.-'''''     <- lowest at epoch 37
  +--------------------------> epochs
 val picked 37, so val is now a tuning set
""",
        analogy='Like running a benchmark 50 times and quoting the fastest run as the typical latency.',
        topic="purpose", level=3),
    mcq("After early stopping picked 37 epochs on 'train', you want to refit on train + validation (25% more data) for production. What is a sensible way to choose the epoch count, given there is no validation set left to stop on?",
        ["Reuse the chosen budget, often scaled for the extra data (e.g. about 37 epochs or the same number of update steps), and fix it before training",
         "Train until the training loss reaches zero",
         "Use the test set for early stopping",
         "Pick a random number of epochs"], 0,
        "Freeze the decision first, then refit.",
        "When refitting on more data, hyperparameters (including the epoch budget) are frozen from the tuning phase. Some teams scale by steps rather than epochs. Never peek at test to stop. The test score you measured earlier remains the estimate.",
        topic="purpose", level=4),
    mcq("Which statement best describes the three sets in SDE terms?",
        ["Train = writing code, validation = your local test runs while iterating, test = the release gate you run once",
         "Train = prod, validation = dev, test = staging",
         "All three are the same test suite run three times",
         "Test = the code; train = the tests"], 0,
        "Which one do you run over and over while iterating?",
        "You iterate against validation as often as you like; the test set is a gate you pass once. If you keep fixing things until the gate passes, it stops being a gate.",
        analogy="Unit tests you rerun all day vs a final acceptance run before release.",
        topic="purpose", level=1),

    # ------------------------------------------------------------------ ratios
    out("""import math
p, target_se = 0.9, 0.01
n = p * (1 - p) / target_se ** 2
print(round(n))""",
        ["900", "90", "9000", "100"], 0,
        "Rearrange SE = sqrt(p(1-p)/n) for n.",
        "n = p(1-p) / SE^2 = 0.09 / 0.0001 = 900 test examples for +/- 1 point at 90% accuracy. Halving the error needs 4x the rows.",
        topic="ratios", level=3),
    mcq("Your fraud test set has 10,000 transactions at 0.5% fraud. You report fraud recall = 0.80. Why is that number shakier than it looks?",
        ["Recall is computed over only the ~50 fraud cases, so its standard error is about +/- 6 points",
         "10,000 rows is a huge test set, so recall is exact",
         "Recall doesn't depend on the number of positives",
         "Fraud recall should be computed on the training set"], 0,
        "Which rows does recall actually divide by?",
        "A metric's noise depends on the rows it's computed from: sqrt(0.8 x 0.2 / 50) = 0.057. For rare classes, plan the test set by the count of positives, not total rows.",
        topic="ratios", level=3),
    out("""import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
X, y = load_breast_cancer(return_X_y=True)
X, y = X[:150], y[:150]
acc = []
for seed in range(20):
    a, b, c, d = train_test_split(X, y, test_size=0.2, random_state=seed)
    acc.append(make_pipeline(StandardScaler(), LogisticRegression()).fit(a, c).score(b, d))
print(round(max(acc) - min(acc), 2))""",
        ["0.1", "0.0", "0.01", "0.5"], 0,
        "Same model, same data, only the split seed changes. 30 test rows each time.",
        "The score moves by about 10 points just from which 30 rows land in test. On small data a single split is a lottery ticket; use (repeated) cross-validation and report the spread.",
        diagram="""
 seed:  0    1    2    3   ...  19
 acc:  .93  .97  .90  1.0  ...  .93
        |-------- range ~0.10 -------|
""",
        topic="ratios", level=3),

    # ------------------------------------------------------------------ tts
    out("""from sklearn.model_selection import train_test_split
X = list(range(10))
a, b = train_test_split(X, test_size=3, random_state=0)
print(len(a), len(b))""",
        ["7 3", "7 0", "3 7", "ValueError"], 0,
        "An int means a row count, a float means a fraction.",
        "test_size=3 asks for exactly 3 test rows. Ints are counts, floats in (0, 1) are fractions, a common source of confusion when someone writes test_size=20 meaning 20%.",
        analogy='Like an API where limit=3 means 3 rows but limit=0.3 means 30%: one parameter, two meanings.',
        topic="tts", level=2),
    out("""import pandas as pd
from sklearn.model_selection import train_test_split
df = pd.DataFrame({"x": range(10)}, index=[f"r{i}" for i in range(10)])
tr, te = train_test_split(df, test_size=0.2, shuffle=False)
print(te.index.tolist())""",
        ["['r8', 'r9']", "[8, 9]", "['r0', 'r1']", "[0, 1]"], 0,
        "DataFrames keep their index labels through the split.",
        "train_test_split returns DataFrames with the original index, so you can always trace a test row back to its source (and join predictions back later).",
        topic="tts", level=2),
    out("""from sklearn.model_selection import train_test_split
X = list(range(10))
a, b = train_test_split(X, train_size=0.5, test_size=0.2, random_state=0)
print(len(a), len(b))""",
        ["5 2", "8 2", "5 5", "ValueError"], 0,
        "Both sizes are given explicitly; they don't have to add up to 1.",
        "With both train_size and test_size set, sklearn returns exactly those sizes (5 and 2) and silently leaves 3 rows out. Handy for quick subsampling, surprising if you forgot you set both.",
        topic="tts", level=3),
    out("""import numpy as np
from sklearn.model_selection import train_test_split
y = np.array([0, 1, 2] * 3)
train_test_split(np.arange(9), y, test_size=2, stratify=y, random_state=0)
print("done")""",
        ["ValueError", "done", "IndexError", "KeyError"], 0,
        "How do you fit 3 classes into a 2-row test set while keeping every class?",
        "A stratified test set must hold at least one row per class. With 3 classes and test_size=2, sklearn raises ValueError (test_size should be >= the number of classes).",
        topic="tts", level=3),
    mcq("You need splits that keep BOTH the class ratio and the region ratio (north/south) balanced. A simple way with train_test_split?",
        ["Stratify on a combined key such as y.astype(str) + '_' + region",
         "Pass stratify=[y, region]",
         "Call train_test_split twice with different stratify columns",
         "It's impossible"], 0,
        "stratify takes ONE label per row; make that label carry both facts.",
        "Concatenating the columns creates joint strata (0_north, 1_south...). Watch out: every combination needs at least 2 rows, so rare combinations may need merging.",
        diagram="""
 y  region   key
 0  north -> 0_north
 1  south -> 1_south
 stratify=key keeps the share of every combination
""",
        topic="tts", level=3),

    # ------------------------------------------------------------------ kfold
    out("""from sklearn.model_selection import KFold
X = list(range(10))
print([len(te) for _, te in KFold(4, shuffle=True, random_state=0).split(X)])""",
        ["[3, 3, 2, 2]", "[2, 2, 3, 3]", "[2, 2, 2, 4]", "[3, 3, 3, 1]"], 0,
        "Shuffling changes which rows go where, not the fold sizes.",
        "10 rows into 4 folds: 10 % 4 = 2 folds get an extra row, so sizes 3, 3, 2, 2 (first folds get the extra), shuffled or not.",
        topic="kfold", level=2),
    out("""import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeRegressor
X = np.arange(100, dtype=float).reshape(-1, 1)
y = 2 * X.ravel()
s = cross_val_score(DecisionTreeRegressor(random_state=0), X, y, cv=5)
print(bool((s < 0).all()))""",
        ["True", "False", "ValueError", "nan"], 0,
        "For a regressor, cv=5 means KFold without shuffling. y is sorted.",
        "Each test fold is a block of y values the tree never saw, and trees can't extrapolate, so every R^2 is negative (worse than predicting the mean). Shuffle (KFold(shuffle=True)) when rows are sorted, unless order is time.",
        topic="kfold", level=3),
    out("""from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import cross_validate
from sklearn.tree import DecisionTreeClassifier
X, y = load_breast_cancer(return_X_y=True)
r = cross_validate(DecisionTreeClassifier(random_state=0), X, y, cv=5, return_train_score=True)
print(r["train_score"].mean() == 1.0, r["test_score"].mean() < 0.95)""",
        ["True True", "True False", "False True", "False False"], 0,
        "An unpruned tree can memorise its training folds.",
        "return_train_score shows the gap: perfect on training folds, lower on held-out folds. A big gap = overfitting (variance); both low = underfitting.",
        topic="kfold", level=2),
    out("""from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict
X, y = load_breast_cancer(return_X_y=True)
pred = cross_val_predict(LogisticRegression(max_iter=5000), X, y, cv=5)
print(len(pred) == len(y))""",
        ["True", "False", "ValueError", "None"], 0,
        "Every row sits in exactly one test fold.",
        "cross_val_predict returns one out-of-fold prediction per row, made by the model that didn't train on it. Useful for confusion matrices, error analysis and stacking.",
        topic="kfold", level=2),
    tf("The accuracy of cross_val_predict's pooled predictions is always exactly equal to the mean of cross_val_score's fold accuracies.", False,
       "Mean of per-fold ratios vs one ratio over all rows: same thing when folds differ in size?",
       "The two match only when folds are equal-sized and the metric averages nicely. sklearn warns that pooled out-of-fold predictions are not a substitute for per-fold scores, especially for metrics like AUC or F1.",
       topic="kfold", level=4),
    out("""import numpy as np
from sklearn.model_selection import ShuffleSplit
tested = set()
for _, te in ShuffleSplit(n_splits=3, test_size=0.2, random_state=0).split(np.zeros(20)):
    tested |= set(te.tolist())
print(20 - len(tested))""",
        ["10", "0", "8", "4"], 0,
        "Each ShuffleSplit draws its test set independently.",
        "Unlike k-fold, ShuffleSplit's test sets can overlap and some rows are never tested (here 10 of 20). Fine for many cheap repeats; for 'each row tested once', use KFold.",
        diagram="""
 KFold:        every row in exactly one test fold
 ShuffleSplit: split1 [..xx..x.x.]  split2 [x...x..x.x]
               overlaps allowed, some rows never tested
""",
        topic="kfold", level=3),

    # ------------------------------------------------------------------ group
    out("""import numpy as np
from sklearn.model_selection import GroupShuffleSplit
groups = np.array(list("aabbccddee"))
gss = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=0)
tr, te = next(gss.split(np.zeros(10), groups=groups))
print(sorted(set(groups[te].tolist())), len(te))""",
        ["['a', 'c'] 4", "['a'] 2", "['a', 'c'] 2", "['a', 'b', 'c'] 3"], 0,
        "test_size counts GROUPS here, and ceil(0.25 x 5) = 2.",
        "GroupShuffleSplit picks whole groups for the test side: 2 of the 5 groups, i.e. 4 rows. Note test_size refers to groups, so the row share can differ from what you asked for.",
        topic="group", level=2),
    out("""import numpy as np
from sklearn.model_selection import LeaveOneGroupOut
groups = np.array(list("aabbccddee"))
print(LeaveOneGroupOut().get_n_splits(groups=groups))""",
        ["5", "10", "2", "1"], 0,
        "One split per distinct group.",
        "LeaveOneGroupOut holds out each group once: 5 groups, 5 splits. Natural for 'leave one hospital/site/store out' to test generalisation to a new site.",
        topic="group", level=2),
    out("""import numpy as np
from sklearn.model_selection import GroupKFold
g = np.array(list("aaaaabbbcc"))
for tr, te in GroupKFold(n_splits=2).split(np.zeros((10, 1)), groups=g):
    print(len(te), sorted(set(g[te].tolist())))""",
        ["5 ['a']\n5 ['b', 'c']", "5 ['a', 'b']\n5 ['c']", "4 ['a']\n6 ['b', 'c']", "ValueError"], 0,
        "GroupKFold tries to make fold sizes (in rows) as even as possible.",
        "The biggest group (a, 5 rows) fills one fold; b (3) and c (2) together fill the other. Groups stay whole, and folds are balanced by row count, not by number of groups.",
        diagram="""
 groups: a = 5 rows   b = 3   c = 2
 fold 1 test: [a a a a a]
 fold 2 test: [b b b c c]
""",
        topic="group", level=3),
    out("""import numpy as np
from sklearn.model_selection import train_test_split
users = np.repeat(np.arange(20), 5)
tr, te = train_test_split(users, test_size=0.2, random_state=0)
shared = set(tr.tolist()) & set(te.tolist())
print(len(shared), len(set(te.tolist())))""",
        ["14 14", "0 4", "4 4", "20 20"], 0,
        "Each user has 5 rows. A random row split doesn't know that.",
        "Every user who appears in test also appears in train: a random row split leaks users. Always run this overlap check on your ID columns; with GroupShuffleSplit the first number would be 0.",
        topic="group", level=3),
    mcq("A video-frame classifier gets 99% on a random frame split and 70% on new videos. Why?",
        ["Neighbouring frames of the same video are near-duplicates, so a random split puts copies of test frames in training; split by video",
         "Videos have too many frames",
         "Frames must be shuffled more",
         "The model needs a bigger image size"], 0,
        "How different is frame 101 from frame 100?",
        "Hidden groups (video, recording session, device, household) create near-duplicate rows. The group id is whatever unit you will see NEW at deployment: here, the video.",
        analogy="Like testing a cache with the same requests you warmed it with.",
        topic="group", level=4),
    mcq("A churn model will score users who already exist, for the next month. The team insists on a GroupKFold by user. Is that the right split?",
        ["Not necessarily: deployment is 'known users, future period', so a time-based split (train on past months, test on a later month) matches better",
         "Yes, user-grouping is always the safest split",
         "Use a random row split instead",
         "Use LeaveOneOut"], 0,
        "Copy the deployment situation, not a rule of thumb.",
        "Group splits answer 'how well on NEW users?'. If the model will only score existing users going forward, the honest question is 'how well next month?', which is a time split. Sometimes you need both (new users AND future period).",
        topic="group", level=4),
    mcq("Your dataset has users AND time. The model will score new sign-ups next quarter. Which evaluation best matches?",
        ["Train on users who signed up before a cutoff date; test on users who signed up after it, using only their data after the cutoff",
         "GroupKFold by user ignoring time",
         "TimeSeriesSplit on rows ignoring users",
         "A random 80/20 row split"], 0,
        "Two kinds of 'new' at once: new people and a new period.",
        "A cutoff on sign-up date gives test users that are both unseen and in the future, just like production. Either split alone leaks one dimension.",
        diagram="""
          users who joined before | after cutoff
 past   [======= train ======] |
 future                        | [==== test ====]
""",
        topic="group", level=4),

    # ------------------------------------------------------------------ time-series
    tf("TimeSeriesSplit sorts your rows by date before splitting.", False,
       "It receives X, not your date column.",
       "TimeSeriesSplit only uses row positions. If the rows aren't already sorted by time, its 'past' and 'future' are meaningless. Sort by timestamp first.",
       analogy="Like paging through a table in insertion order: 'page 2' only means 'later' if rows were inserted chronologically.",
       topic="time-series", level=2),
    out("""from sklearn.model_selection import TimeSeriesSplit
for tr, te in TimeSeriesSplit(n_splits=3, test_size=2).split(list(range(10))):
    print(len(tr), te.tolist())""",
        ["4 [4, 5]\n6 [6, 7]\n8 [8, 9]", "2 [2, 3]\n4 [4, 5]\n6 [6, 7]", "6 [6, 7]\n6 [8, 9]\n6 [4, 5]", "ValueError"], 0,
        "Test blocks are fixed at 2 rows and end at the last row.",
        "With test_size=2 the three test blocks are the last 6 rows, two at a time, and training is everything before each block (4, 6, 8 rows).",
        topic="time-series", level=3),
    mcq("You forecast sales for 50 stores. The data is one table sorted by store, then date. What goes wrong with TimeSeriesSplit on this table as-is?",
        ["Its 'future' blocks are just later stores, not later dates; split by a date cutoff applied to all stores instead",
         "Nothing, TimeSeriesSplit handles multiple series",
         "It raises an error for more than one store",
         "It only uses the first store"], 0,
        "TimeSeriesSplit cuts by row position. What does row position mean here?",
        "For many series (panel data), define folds by date: train on all stores before date d, test on all stores in the next window. Otherwise the 'test' contains earlier dates than training.",
        diagram="""
 rows: store1 Jan..Dec | store2 Jan..Dec | store3 Jan..Dec
 TSS:  [ train ...................... ][ test = store3 ]
 right: every store, Jan..Sep = train | Oct..Dec = test
""",
        topic="time-series", level=4),
    mcq("A forecasting pipeline standardises each feature with the mean and std of the whole series, then runs walk-forward validation. What is the leak?",
        ["Early training windows are scaled with statistics that include future values; fit the scaler inside each window",
         "There is none; scaling is harmless",
         "Walk-forward forbids scaling",
         "The std should use ddof=1"], 0,
        "When was the full-series mean known?",
        "A mean computed over all time carries information about the future level and trend. Put the scaler in a Pipeline so each walk-forward step fits it on past data only.",
        topic="time-series", level=3),
    mcq("You evaluate a model that forecasts 7 days ahead. Features are computed up to day t. Which test setup is honest?",
        ["For each origin t, use features as of t and score the prediction for day t+7, leaving a 7-day gap between the last label used in training and the origin",
         "Score the prediction for day t+1 because it's easier",
         "Use features up to day t+7",
         "Shuffle days and use 5-fold CV"], 0,
        "Copy what you will know on the day you make the forecast.",
        "The horizon defines both the target and the gap. Training labels that end inside the test horizon leak future information; testing on t+1 overstates a t+7 model.",
        diagram="""
 [ train: labels end by t ] t ----- 7 days -----> t+7
                            ^ features as of t    ^ score
""",
        topic="time-series", level=4),
    mcq("Your new demand model's backtest MAE is 120 units. Before celebrating, what should you compare it with?",
        ["A naive baseline, such as 'same as last week' (seasonal naive), on the same backtest windows",
         "Its training MAE",
         "A model trained on shuffled folds",
         "Nothing; 120 is a good number"], 0,
        "Is 120 good? Compared with what?",
        "Many forecasting models barely beat 'repeat last week'. A naive baseline on identical windows tells you whether the model adds value at all.",
        analogy="Like benchmarking a new cache against no cache: a speed-up means nothing without the baseline.",
        topic="time-series", level=3),

    # ------------------------------------------------------------------ nested-cv
    out("""from sklearn.datasets import load_iris
from sklearn.model_selection import RandomizedSearchCV
from sklearn.tree import DecisionTreeClassifier
X, y = load_iris(return_X_y=True)
rs = RandomizedSearchCV(DecisionTreeClassifier(random_state=0),
                        {"max_depth": list(range(1, 20))}, n_iter=5, cv=3, random_state=0).fit(X, y)
print(len(rs.cv_results_["params"]), 5 * 3)""",
        ["5 15", "19 57", "5 5", "3 15"], 0,
        "n_iter = number of settings sampled.",
        "RandomizedSearchCV samples n_iter=5 settings, each cross-validated 3 times: 15 fits (plus one refit). The budget is fixed by n_iter, not by the grid size.",
        topic="nested-cv", level=2),
    out("""import numpy as np
rng = np.random.default_rng(0)
y_val, y_test = rng.integers(0, 2, 50), rng.integers(0, 2, 1000)
val_preds = rng.integers(0, 2, (100, 50))
test_preds = rng.integers(0, 2, (100, 1000))
val_acc = (val_preds == y_val).mean(axis=1)
best = val_acc.argmax()
print(round(val_acc[best], 2), round((test_preds[best] == y_test).mean(), 2))""",
        ["0.66 0.51", "0.5 0.5", "0.66 0.66", "0.51 0.66"], 0,
        "All 100 'models' are coin flips. What does the best of 100 coin flips look like?",
        "Picking the best of 100 random guessers on 50 validation rows gives 66% by luck alone; on fresh test data it's 51%, chance. This is the winner's curse: selection on a noisy score biases it upward.",
        diagram="""
 100 coin-flip models scored on 50 val rows
 val acc:   .40 ... .50 ... .58 ... .66 <- picked
 test acc of the pick:  .51  (just luck, gone)
""",
        topic="nested-cv", level=4),
    out("""import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, GroupKFold
X = np.arange(10, dtype=float).reshape(-1, 1)
y = [0, 1] * 5
GridSearchCV(LogisticRegression(), {"C": [1]}, cv=GroupKFold(2)).fit(X, y)
print("ok")""",
        ["ValueError", "ok", "TypeError", "KeyError"], 0,
        "GroupKFold needs to know the groups. Were they passed?",
        "GridSearchCV(cv=GroupKFold()) requires fit(X, y, groups=...). Forgetting it raises ValueError, which is lucky: a splitter that silently ignored groups would leak.",
        analogy='Like a required config flag: failing loudly at startup beats silently running with the wrong setting.',
        topic="nested-cv", level=4),
    tf("Nested cross-validation gives you the final model to deploy.", False,
       "What does the outer loop produce: a model or a number?",
       "Nested CV produces an honest performance ESTIMATE of the tuning procedure. To deploy, run the inner search (e.g. GridSearchCV) once on all the data and ship its best_estimator_.",
       topic="nested-cv", level=3),
    mcq("After GridSearchCV(refit=True).fit(X_train, y_train), what does gs.score(X_test, y_test) use?",
        ["best_estimator_: the best setting refit on all of X_train",
         "The model from the best CV fold only",
         "An average of all candidate models",
         "The last setting in the grid"], 0,
        "refit=True does one more fit at the end.",
        "With refit=True the winning parameters are retrained on the whole training set, and predict/score delegate to that best_estimator_. That's the model you evaluate once on test.",
        topic="nested-cv", level=3),
    mcq("You tune 3 hyperparameters with 5-fold CV on 5,000 rows, then score once on a held-out test set of 2,000 rows. Is nested CV still necessary?",
        ["Usually not: the untouched test set already gives an unbiased estimate; nested CV matters most when data is too small to spare a test set",
         "Yes, always use nested CV",
         "Yes, the test score is biased by the tuning",
         "No, and the test set isn't needed either"], 0,
        "What problem does nested CV solve?",
        "Nested CV replaces the held-out test set when you can't afford one. With enough data, tune with CV on train and confirm once on test: simpler and cheaper.",
        topic="nested-cv", level=3),

    # ------------------------------------------------------------------ leakage
    out("""import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.tree import DecisionTreeClassifier
y = np.array([0] * 80 + [1] * 20)
X = np.arange(100).reshape(-1, 1)
cv = StratifiedKFold(5, shuffle=True, random_state=0)
print(round(cross_val_score(DecisionTreeClassifier(random_state=0), X, y, cv=cv).mean(), 2))""",
        ["0.98", "0.8", "0.5", "0.2"], 0,
        "The only feature is the row number. The positives were appended at the end of the file.",
        "The row index alone gets 98%: positives were added in a later batch, so 'index > 79' is a perfect rule. Leakage hunt rule: if an ID, row number or timestamp predicts the label, your data was assembled in a label-dependent way.",
        analogy='Like a test suite where all the failing cases sit at the bottom of the file: the line number alone predicts pass or fail.',
        topic="leakage", level=3),
    mcq("A model predicts a support ticket's priority at creation time. The top feature is 'time_to_resolution'. What is the verdict?",
        ["Target leakage: resolution time is only known after the ticket is closed, long after the prediction is needed",
         "A great feature: keep it",
         "It just needs log-scaling",
         "It is a group-split problem"], 0,
        "At the moment the ticket is created, what is its time to resolution?",
        "Check every feature's timestamp against the prediction moment. Anything produced later (resolution time, final status, agent notes) must go.",
        topic="leakage", level=2),
    mcq("A pneumonia model trained on X-rays from two hospitals scores 0.95 AUC, but on a third hospital 0.70. Investigation shows sick patients mostly came from hospital A, whose scanner prints a text marker in the corner. What happened?",
        ["Shortcut learning: the model learned the hospital marker (a proxy for the label) instead of the disease",
         "The third hospital has wrong labels",
         "The model needs more epochs",
         "AUC is the wrong metric"], 0,
        "What is the easiest pixel pattern that separates sick from healthy in that training set?",
        "When collection source correlates with the label, any source artefact becomes a leaky feature. Test with leave-one-site-out splits and inspect what the model looks at.",
        diagram="""
 hospital A: 90% sick  [marker 'A' in the corner]
 hospital B: 10% sick  [no marker]
 easiest rule learned: marker present -> sick
""",
        topic="leakage", level=4),
    mcq("A colleague uses the test set for early stopping ('just to pick the epoch') and then reports test accuracy. What is the problem?",
        ["The test set chose a hyperparameter (the epoch), so its score is optimistic; use a validation split for stopping",
         "Early stopping always overfits",
         "There's none: the epoch isn't a weight",
         "Test sets can't measure accuracy"], 0,
        "Any choice made by looking at a set uses that set.",
        "Choosing the best epoch by test loss picks the luckiest point on the test curve. It looks harmless because no weights were trained on test, but the decision was.",
        topic="leakage", level=3),
    mcq("A fraud model uses the feature 'was the previous transaction on this card fraud?'. Offline it's the top feature. In production, fraud labels arrive 30-60 days later via chargebacks. What is the problem?",
        ["Label latency: at prediction time the previous transaction's label usually isn't known yet, so the feature is filled with information production won't have",
         "Nothing, the previous transaction happened in the past",
         "The feature needs one-hot encoding",
         "It should be computed over the whole card history"], 0,
        "The event is in the past. Is its LABEL already known?",
        "'As of' rules apply to labels too: a past event's outcome counts only once it is recorded. Build features from labels available by the prediction time (e.g. chargebacks received so far), or offline scores will be far too optimistic.",
        diagram="""
 txn 1 (fraud) --- txn 2 (predict now) --- chargeback for txn 1
     day 0             day 3                    day 45
 at day 3 the label of txn 1 is still unknown
""",
        topic="leakage", level=4),
    mcq("You build a churn dataset by joining today's 'customer_tier' table (updated whenever a customer upgrades or cancels) to labels from last year. What leaks?",
        ["Tier changes caused by last year's churn or upgrades are now in the features; you need the tier as of each label's date",
         "Nothing, tier is a stable attribute",
         "Only the customer ID",
         "The join adds duplicates, nothing else"], 0,
        "When was today's tier value written?",
        "Mutable tables overwrite history. Joining their current values onto past events smuggles outcomes into features. Use snapshot/history tables or a feature store with point-in-time joins.",
        diagram="""
 label date: 2025-06 (churned)
 tier table today: 'cancelled'  <- written 2025-07
 feature should be: tier as of 2025-06 = 'gold'
""",
        topic="leakage", level=4),

    # ------------------------------------------------------------------ pipelines
    out("""from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
X, y = load_iris(return_X_y=True)
pipe = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
g = GridSearchCV(pipe, {"logisticregression__C": [0.1, 1]}, cv=3).fit(X, y)
print(list(g.best_params_))""",
        ["['logisticregression__C']", "['C']", "['LogisticRegression__C']", "['standardscaler', 'logisticregression']"], 0,
        "best_params_ uses the same keys as the grid.",
        "Pipeline parameters are named <step>__<param>, and best_params_ echoes those keys. To use them on a fresh pipeline: pipe.set_params(**g.best_params_).",
        topic="pipelines", level=2),
    out("""import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
X = np.random.default_rng(0).normal(size=(20, 2)); y = [0, 1] * 10
pipe = make_pipeline(StandardScaler(), LogisticRegression())
GridSearchCV(pipe, {"C": [0.1, 1]}).fit(X, y)""",
        ["ValueError", "TypeError", "KeyError", "AttributeError"], 0,
        "The pipeline itself has no parameter called C.",
        "Grid keys must name the step: 'logisticregression__C'. A bare 'C' raises ValueError (invalid parameter). The error is your friend: a typo can't silently tune nothing.",
        question="What does this print (or raise)?",
        topic="pipelines", level=3),
    out("""import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
X = np.array([[1.0], [2.0], [3.0], [10.0]]); y = [0, 0, 1, 1]
pipe = make_pipeline(StandardScaler(), LogisticRegression()).fit(X[:3], y[:3])
print(pipe.named_steps["standardscaler"].mean_[0])""",
        ["2.0", "4.0", "10.0", "0.0"], 0,
        "fit was called on the first 3 rows only.",
        "The pipeline's scaler learned its mean from exactly the rows passed to fit (1, 2, 3). Inspecting fitted steps like this is a quick way to prove no test data reached preprocessing.",
        topic="pipelines", level=2),
    mcq("You need random oversampling of the minority class inside cross-validation. Why can't you simply put it as a step in a standard sklearn Pipeline?",
        ["sklearn Pipeline steps can only transform X, not change the number of rows or y; use imblearn's Pipeline, which resamples only during fit",
         "sklearn forbids oversampling",
         "Oversampling must happen before the pipeline",
         "Pipelines don't support classifiers"], 0,
        "Oversampling adds rows AND labels.",
        "imblearn.pipeline.Pipeline applies samplers only in fit (on each training fold) and skips them in predict, so validation folds keep their real distribution. Oversampling outside the pipeline leaks copies across folds.",
        diagram="""
 fit:     X_train -> sampler (adds rows) -> model.fit
 predict: X_val   -> sampler skipped     -> model.predict
""",
        topic="pipelines", level=4),
    mcq("Why is it fine to fit a TfidfVectorizer inside a Pipeline but questionable to fit it once on train + test documents before splitting?",
        ["Fitting on all documents puts test-set vocabulary and IDF counts into the features; inside a pipeline it only learns from training folds",
         "TfidfVectorizer can't be used in pipelines",
         "IDF is identical regardless of which documents are used",
         "It's questionable in both cases"], 0,
        "IDF = how rare a word is across the documents it was fit on.",
        "It's an unsupervised leak (no labels), usually small, but test-only words get columns and IDF weights shaped by the test set. Pipelines remove the question entirely.",
        topic="pipelines", level=3),

    # ------------------------------------------------------------------ test-reuse
    mcq("Your team must report test accuracy to leadership every sprint. What practice keeps that number honest over months?",
        ["Log every test-set evaluation, limit how often it's used, and periodically refresh the test set with new labelled data",
         "Evaluate on test after every commit",
         "Use the test set as extra training data each sprint",
         "Report validation accuracy instead and call it test"], 0,
        "Each look at the test set spends a little of its credibility.",
        "Treat the test set as a budget. A log of evaluations shows how much has been 'spent'; fresh data restores an unseen set. Keep the old set too for regression checks.",
        analogy="Like a production canary you only consult at release time; if you route every experiment through it, it no longer tells you anything new.",
        topic="test-reuse", level=3),
    mcq("A model's offline test score has been stable for a year, but production complaints are rising. Your test set was frozen in 2025. What is the likely gap?",
        ["The frozen test set no longer looks like current traffic; refresh it from recent production data",
         "The model weights decayed",
         "Test sets must be frozen forever",
         "The complaints are noise"], 0,
        "A test set is a snapshot of the world at one time.",
        "A static test set measures yesterday's distribution. Sample new labelled examples from recent traffic for a current test set, and keep the old one to catch regressions.",
        topic="test-reuse", level=3),
    mcq("Adversarial validation shows test rows differ from training rows mainly in 'account_age'. You can't get more test-like data. One way to make validation more test-like?",
        ["Use the adversarial classifier's p(test) to pick or weight the training rows that look most like test as the validation set",
         "Drop the test set",
         "Shuffle account_age",
         "Use a larger random validation split"], 0,
        "The adversarial model already scores how 'test-like' each training row is.",
        "Selecting (or importance-weighting) the most test-like training rows for validation makes your tuning target resemble the real target. Also consider dropping or fixing the drifting feature if it isn't causal.",
        topic="test-reuse", level=4),
    mcq("Two teams evaluate on the same public benchmark. Team A picked its architecture after 200 runs scored on the benchmark's test split; team B tuned on a separate dev split and ran the test once. Both report 85%. Whose number do you trust more, and why?",
        ["Team B: team A's 85% includes selection on the test set (adaptive overfitting), so it is optimistic",
         "Team A, because they ran more experiments",
         "Both equally, the number is the same",
         "Neither, benchmarks are meaningless"], 0,
        "Same number, different amount of peeking.",
        "A score's trustworthiness depends on how it was produced. 200 test-set looks turn the test into a validation set. Ask 'how many times was this set used to make decisions?'",
        topic="test-reuse", level=4),

    # ------------------------------------------------------------------ llm-evals
    mcq("You are building an eval set for a production LLM support bot. Which source and split is most honest?",
        ["Sample real user queries from logs, label the answers, and keep the most recent period as the test set",
         "Have the team write 20 questions they think are typical",
         "Use the few-shot examples from the prompt",
         "Use a public benchmark only"], 0,
        "Your eval should look like the traffic the bot will see next.",
        "Real queries capture phrasing, typos and topics the team wouldn't invent. A time-based holdout (latest weeks) checks the bot on what's coming, not what it was tuned on.",
        topic="llm-evals", level=2),
    out("""def ngrams(text, n=3):
    w = text.lower().split()
    return {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}
test = "what is the capital city of france"
train = "quiz: what is the capital city of spain"
t = ngrams(test)
print(len(t & ngrams(train)), len(t))""",
        ["4 5", "4", "5 5", "3 5"], 0,
        "List the 3-grams of the test sentence and check which appear in the train text.",
        "Test has 5 trigrams; 4 (what is the / is the capital / the capital city / capital city of) also appear in the train text. Overlap checks flag such items, but a paraphrase ('which city is France's capital') would score 0.",
        topic="llm-evals", level=3),
    mcq("Your prompt eval set has 50 items; prompt v2 scores 82% vs v1's 78%. Is v2 clearly better?",
        ["No: with 50 items the standard error is about 5.5 points, so a 4-point gap is within noise; use a bigger set or paired comparison on the same items",
         "Yes, 4 points is a big gain",
         "Yes, because LLM outputs are deterministic",
         "No, prompts can't be compared"], 0,
        "sqrt(0.8 x 0.2 / 50) = ?",
        "Small eval sets are noisy, just like small test sets in classic ML. Compare versions on the same items and look at which items flipped (a paired view), and grow the set for decisions that matter.",
        topic="llm-evals", level=3),
    mcq("You fine-tune a model on 30,000 Q&A pairs generated by a teacher LLM, which you prompted with examples from your eval set to 'match the style'. What is wrong?",
        ["The teacher may paraphrase eval items into training data, contaminating the eval through the back door",
         "Teacher models can't write Q&A",
         "Style matching never helps",
         "Nothing, since no eval item was copied verbatim"], 0,
        "Where did the teacher's inspiration come from?",
        "Anything derived from the eval set (paraphrases, style seeds, generated variants) leaks it. Seed generators with dev or training data only, and run near-duplicate checks against the eval set.",
        analogy='Like a candidate coached by someone who has seen the interview questions: nothing is copied word for word, but the questions are no longer unseen.',
        topic="llm-evals", level=4),
    mcq("Why do some LLM benchmarks only use questions created after a model's training cutoff date?",
        ["Questions published after the cutoff can't have been in pre-training data, so the score can't be memorisation",
         "Newer questions are easier",
         "Old questions have wrong answers",
         "Cutoff dates make evaluation faster"], 0,
        "It's a time-based split applied to the whole internet.",
        "A dated, rolling benchmark is the LLM version of 'train on the past, test on the future'. It defeats contamination without needing to inspect secret training data.",
        diagram="""
 internet text ------------------| cutoff |------------->
 pre-training data  [===========]
 eval questions                          [ written later ]
""",
        topic="llm-evals", level=4),
    mcq("You build a RAG eval by generating questions from document chunks, then use the same questions to pick chunk size and prompt. What should the final report use?",
        ["A separate set of questions (ideally real user queries) not used for any tuning",
         "The same generated questions; they were never trained on",
         "Only the retrieval recall on the tuning set",
         "No eval: RAG doesn't overfit"], 0,
        "Chunk size and prompt are hyperparameters.",
        "Every design choice tuned against a question set fits that set. Keep a dev set for chunking/prompt/retriever tuning and a held-out test set for the final number.",
        topic="llm-evals", level=4),

    # ------------------------------------------------------------------ compare
    out("""import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import cross_val_score
y = np.array([0] * 80 + [1] * 20)
X = np.zeros((100, 1))
print(cross_val_score(DummyClassifier(), X, y, cv=5).mean())""",
        ["0.8", "0.5", "0.2", "1.0"], 0,
        "The default DummyClassifier always predicts the most frequent class.",
        "A dummy baseline scores 0.8 here with zero learning. Always put a baseline through the SAME CV: a real model at 0.82 accuracy has learned almost nothing.",
        analogy="Like comparing a new endpoint's latency with a stub that just returns 200: the floor every real implementation must beat.",
        topic="compare", level=2),
    mcq("You compare model A and model B with 5-fold CV. Why should both use the exact same folds (same splitter with a fixed random_state)?",
        ["So differences come from the models, not from one model getting easier folds; it also allows a paired, fold-by-fold comparison",
         "sklearn requires it",
         "It makes training faster",
         "So the models can share weights"], 0,
        "If A's folds were easier, what would you be measuring?",
        "Fold-to-fold variation is often bigger than the difference between models. Same folds turn the comparison into paired differences, which cancels out fold difficulty.",
        analogy="Like A/B testing two builds on the same benchmark machine and input set, not on different machines.",
        topic="compare", level=2),
    out("""import numpy as np
a = np.array([0.81, 0.79, 0.95, 0.80, 0.82])
b = np.array([0.80, 0.77, 0.94, 0.78, 0.81])
d = a - b
print(round(a.mean() - b.mean(), 3), bool((d > 0).all()), round(b.std(), 3) > round(d.std(), 3))""",
        ["0.014 True True", "0.014 False True", "0.014 True False", "0.0 True True"], 0,
        "Look at the per-fold differences, not just the two means.",
        "The means differ by only 0.014 and each model's scores swing a lot (fold 3 is easy for both), but A wins on every fold and the differences barely vary. Paired differences remove shared fold difficulty, the right lens for 'is A better than B?'.",
        diagram="""
 fold:   1    2    3    4    5
 A:     .81  .79  .95  .80  .82
 B:     .80  .77  .94  .78  .81
 A-B:  +.01 +.02 +.01 +.02 +.01   <- consistent
""",
        topic="compare", level=3),
    out("""from sklearn.model_selection import RepeatedStratifiedKFold
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=0)
print(cv.get_n_splits())""",
        ["15", "5", "3", "8"], 0,
        "Each repeat is a full 5-fold run with a new shuffle.",
        "5 folds x 3 repeats = 15 fits. Repeating with different shuffles averages out the luck of one particular fold assignment, giving a steadier estimate.",
        topic="compare", level=2),
    mcq("You run 10-fold CV, get the mean and std of fold scores, and compute a t-test assuming the 10 scores are independent. Why is that test overconfident?",
        ["The 10 training sets overlap by about 89%, so fold scores are correlated; corrected tests (e.g. Nadeau-Bengio) inflate the variance to account for it",
         "10 folds is too few for any test",
         "The t-test requires accuracy above 0.5",
         "Fold scores are perfectly independent, so it's fine"], 0,
        "How different are the training sets of fold 1 and fold 2?",
        "Fold scores share most of their training data, so they move together and the naive standard error is too small. Use a corrected resampled t-test, or McNemar's test on a single held-out set.",
        topic="compare", level=4),
    mcq("You have one fixed test set and two classifiers. Which test compares them using the items where they disagree?",
        ["McNemar's test: it looks at the counts of items only A got right vs only B got right",
         "A two-sample t-test on their accuracies",
         "The KS test on their predicted labels",
         "Chi-squared on the class balance"], 0,
        "Items both get right (or both get wrong) tell you nothing about which is better.",
        "McNemar's test uses the paired 2x2 table of correct/incorrect. If only-A-right = 30 and only-B-right = 12, that imbalance is evidence A is better on this data.",
        diagram="""
             B right   B wrong
 A right       850        30
 A wrong        12       108
 only 30 vs 12 (the disagreements) decide it
""",
        topic="compare", level=4),
    mcq("Model A beats model B by 0.4 points of CV accuracy, but A takes 10x longer to train, 5x longer to serve and its fold scores swing by +/- 2 points. What is the sensible engineering call?",
        ["Prefer B unless the 0.4 points matter for the business: the gain is inside the noise and A costs far more to run",
         "Always ship the model with the higher mean",
         "Ship both and average them",
         "Retune A until it wins by more"], 0,
        "Is the gap bigger than the noise? And what does it cost?",
        "Model selection is a trade-off: a difference smaller than the CV spread isn't evidence of improvement, and latency, cost and maintainability count too. Interviewers like candidates who say this out loud.",
        topic="compare", level=4),
    tf("Repeated k-fold CV (several shuffles) fixes the problem of having too little data.", False,
       "Repeats reshuffle the same rows. Do they add information?",
       "Repeats reduce the variance that comes from one particular fold assignment, but every repeat uses the same rows. The uncertainty from a small sample remains; only more data fixes that.",
       analogy='Like rerunning the same 20 integration tests in random order: you learn about flakiness, not about code paths no test covers.',
       topic="compare", level=4),
    mcq("A Kaggle-style leaderboard shows your model 0.3 points above the next one on a 1,000-row test set. What is the most accurate statement?",
        ["The gap is likely within noise; rankings this close can easily swap on a new sample",
         "Your model is definitely better",
         "The other model is overfitting",
         "Leaderboards have no noise"], 0,
        "SE at ~90% accuracy on 1,000 rows is about 1 point.",
        "With a standard error near 1 point, a 0.3-point lead is noise. Private leaderboards 'shake up' for exactly this reason, plus public-set overfitting.",
        topic="compare", level=3),
    fill("The sklearn baseline estimator that ignores the features and predicts the majority class (or the mean) is called ________.",
         "DummyClassifier",
         "It's in sklearn.dummy; the regression version is DummyRegressor.",
         "DummyClassifier (strategy='most_frequent', 'stratified', 'prior'...) gives the floor every real model must beat under the same CV.",
         topic="compare", level=1),
    fill("To get exactly 3 repeats of 5-fold stratified CV with different shuffles, use RepeatedStratifiedKFold(n_splits=5, n_repeats=____).",
         "3",
         "The parameter name says it.",
         "n_repeats=3 reruns 5-fold CV three times with different shuffles: 15 scores in total.",
         topic="compare", level=2),
    fill("In time-series CV, the TimeSeriesSplit argument that drops rows between the training window and the test block is ____.",
         "gap",
         "A buffer zone between past and future.",
         "TimeSeriesSplit(gap=k) removes the last k training rows before each test block, so labels that look ahead can't overlap the test period.",
         topic="time-series", level=3),
]
