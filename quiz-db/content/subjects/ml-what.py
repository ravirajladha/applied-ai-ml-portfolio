from helpers import mcq, tf, out, fill

SUBJECT = "ml-what"

TOPICS = [
    ("rules-vs-learned", "Rules vs learned functions"),
    ("params-hyper", "Model, parameters, hyperparameters"),
    ("train-infer", "Training vs inference"),
    ("workflow", "The ML workflow end-to-end"),
    ("when-not-ml", "When NOT to use ML"),
    ("ai-ml-dl", "AI vs ML vs DL vs GenAI"),
    ("generalisation", "Generalisation and bias-variance intuition"),
    ("inductive-bias", "Inductive bias and no free lunch"),
    ("parametric", "Parametric vs non-parametric"),
    ("framing", "Framing a business problem as an ML task"),
]

QUESTIONS = [
    # ------------------------------------------------------------------ L1
    mcq("A spam filter that you build by writing `if 'lottery' in subject: spam = True` by hand is an example of:",
        ["Rule-based programming", "Machine learning", "Deep learning", "Reinforcement learning"], 0,
        "Who wrote the if-statement: you, or the computer?",
        "You wrote the rule yourself, so it's ordinary rule-based code. ML would learn which words matter from labelled emails.",
        topic="rules-vs-learned", level=1),
    tf("In machine learning, a 'model' is basically a function: input goes in, a prediction comes out.", True,
       "Think of what you call after training: model.predict(x).",
       "A trained model maps inputs to outputs, just like a function, except its internal logic was learned from data.",
       analogy="A model is a function whose body was written by the training process, not by you.",
       topic="rules-vs-learned", level=1),
    mcq("What do you give an ML algorithm so it can learn a rule like 'which houses are expensive'?",
        ["Many examples, each with the correct answer", "The finished if/else rules", "Only the column names", "A list of programming languages"], 0,
        "Learning needs examples to learn from.",
        "You provide examples plus their answers (labels); the algorithm finds the rule that maps one to the other.",
        topic="rules-vs-learned", level=1),
    mcq("Which of these is a hyperparameter (a setting YOU choose before training)?",
        ["The maximum depth of a decision tree", "The slope learned by linear regression", "The weights of a neural network", "The intercept of a fitted line"], 0,
        "Hyperparameter = a knob you set; parameter = a number the model learns.",
        "max_depth is chosen before training. Slopes, weights and intercepts are learned from data, so they are parameters.",
        topic="params-hyper", level=1),
    tf("Hyperparameters are learned automatically from the data during training.", False,
       "Who sets the value of max_depth or the learning rate?",
       "Hyperparameters are set before training (and tuned by trying several values). Parameters are what training learns.",
       topic="params-hyper", level=1),
    out("""from sklearn.linear_model import LinearRegression
import numpy as np
X = np.array([[1], [2], [3], [4]])
y = np.array([3, 5, 7, 9])
m = LinearRegression().fit(X, y)
print(round(m.coef_[0], 2), round(m.intercept_, 2))""",
        ["2.0 1.0", "1.0 2.0", "3.0 0.0", "2.0 0.0"], 0,
        "Look at the pattern: y goes 3, 5, 7, 9 as x goes 1, 2, 3, 4.",
        "The data follows y = 2x + 1, so the learned slope (coef_) is 2 and the intercept is 1. Those two numbers ARE the model.",
        topic="params-hyper", level=1),
    mcq("You trained a model last week. Today a user asks for a prediction. What happens to the model's weights?",
        ["Nothing: they are used as-is to compute the answer", "They are re-learned from scratch", "They are deleted after each prediction", "They are randomly reset"], 0,
        "Inference reads the weights; it doesn't change them.",
        "At inference the weights are frozen. The model just runs its learned function on the new input.",
        topic="train-infer", level=1),
    mcq("Which step usually takes the most compute: training or a single prediction?",
        ["Training", "A single prediction", "They always cost the same", "Neither uses compute"], 0,
        "One step looks at the whole dataset many times.",
        "Training passes over the whole dataset (often many times). One prediction runs the learned function once.",
        analogy="Training is the slow build; inference is running the binary.",
        topic="train-infer", level=1),
    mcq("What is the usual order of an ML project?",
        ["Frame the problem -> get data -> train -> evaluate -> deploy -> monitor",
         "Train -> get data -> deploy -> frame the problem",
         "Deploy -> train -> evaluate -> get data",
         "Get data -> deploy -> train -> frame the problem"], 0,
        "You can't train before you know the question and have the data.",
        "First decide what you're predicting, then gather data, train, check it on unseen data, ship it, and keep watching it.",
        diagram="""
 frame -> data -> features -> train -> evaluate
                                          |
   retrain <- monitor <- deploy <---------+
""",
        topic="workflow", level=1),
    tf("Once a model is deployed, the ML work is finished.", False,
       "Does the world stop changing after you ship?",
       "Data changes over time, so deployed models are monitored and retrained. Deployment is a step in a loop, not the end.",
       topic="workflow", level=1),
    mcq("Which task does NOT need machine learning?",
        ["Calculating GST at a fixed 18% on an invoice", "Recognising faces in photos", "Recommending movies", "Translating Hindi to English"], 0,
        "Is there an exact formula?",
        "GST is a fixed formula: price * 0.18. Write the formula. ML is for patterns too fuzzy to write down by hand.",
        topic="when-not-ml", level=1),
    mcq("How do AI, ML and Deep Learning (DL) relate?",
        ["DL is a part of ML, and ML is a part of AI", "AI is a part of ML", "They are three unrelated fields", "ML is a part of DL"], 0,
        "Think of nested circles, biggest first.",
        "AI is the broad goal (smart machines). ML is one way to get there (learn from data). DL is ML using deep neural networks.",
        diagram="""
 +------------- AI ---------------+
 |  +---------- ML -------------+ |
 |  |  +------- DL ----------+  | |
 |  |  |  +--- GenAI ---+    |  | |
 |  |  |  +-------------+    |  | |
 |  |  +---------------------+  | |
 |  +---------------------------+ |
 +--------------------------------+
""",
        topic="ai-ml-dl", level=1),
    mcq("A chat LLM that writes new text is an example of:",
        ["Generative AI (built with deep learning)", "A rule-based expert system", "A spreadsheet formula", "Unsupervised clustering"], 0,
        "It generates new content.",
        "Chat LLMs are deep neural networks that generate content, i.e. generative AI.",
        topic="ai-ml-dl", level=1),
    mcq("What does it mean for a model to 'generalise' well?",
        ["It makes good predictions on new data it never saw", "It remembers every training example", "It trains very fast", "It uses many features"], 0,
        "The goal is to do well in the real world, after training.",
        "Generalisation = performance on unseen data. Doing well only on training data is memorisation.",
        analogy="A student who understood the subject vs one who memorised last year's paper.",
        topic="generalisation", level=1),
    tf("Every ML model makes some assumptions about what the true pattern looks like.", True,
       "A straight-line model assumes something about the data's shape.",
       "These built-in assumptions are called the inductive bias. Without any assumptions, a model can't guess beyond its training data.",
       topic="inductive-bias", level=1),
    mcq("A linear regression model with 3 input features always stores 4 learned numbers, no matter if you train it on 100 or 1 million rows. This kind of model is called:",
        ["Parametric", "Non-parametric", "Unsupervised", "Generative"], 0,
        "Does its size depend on the amount of data?",
        "Parametric models have a fixed number of parameters (here 3 weights + 1 intercept), regardless of dataset size.",
        topic="parametric", level=1),
    mcq("A shop wants to know 'how many units of each product will we sell next week?'. What is the target (the thing to predict)?",
        ["Units sold next week per product", "The product name", "The shop's address", "Last week's weather"], 0,
        "The target is the answer to the business question.",
        "The target is the quantity you want the model to output: next week's units sold for each product.",
        topic="framing", level=1),
    fill("After calling fit, scikit-learn's LinearRegression stores the learned slopes in the attribute ____.",
         "coef_",
         "Short for coefficients, with sklearn's trailing-underscore convention.",
         "coef_ holds the learned weights; intercept_ holds the bias. Attributes ending in _ only exist after fit.",
         topic="params-hyper", level=1),

    # ------------------------------------------------------------------ L2
    out("""from sklearn.tree import DecisionTreeClassifier
X = [[10], [20], [30], [60], [70], [80]]
y = [0, 0, 0, 1, 1, 1]
t = DecisionTreeClassifier(max_depth=1).fit(X, y)
print(t.tree_.threshold[0])""",
        ["45.0", "30.0", "60.0", "50.0"], 0,
        "The tree picks a cut point between the last 0 and the first 1.",
        "The tree learned the rule `if x <= 45: class 0 else class 1`. 45 is the midpoint of 30 and 60. You never wrote that if-statement; training did.",
        analogy="Training wrote the if/else for you and picked the magic number.",
        topic="rules-vs-learned", level=2),
    mcq("A fraud team has 200 hand-written rules that keep breaking as fraudsters change tactics. Why might ML help?",
        ["It can re-learn the patterns from fresh labelled data instead of someone rewriting rules", "ML never makes mistakes", "ML needs no data", "ML rules are easier to read than if-statements"], 0,
        "What happens when the pattern changes?",
        "When patterns shift often and are too complex to hand-code, retraining on new labelled examples is cheaper than maintaining rules.",
        topic="rules-vs-learned", level=2),
    out("""from sklearn.tree import DecisionTreeClassifier
m = DecisionTreeClassifier(max_depth=2)
print(m.get_params()["max_depth"], hasattr(m, "tree_"))""",
        ["2 False", "2 True", "None False", "None True"], 0,
        "The model has been configured but not fitted yet.",
        "max_depth is a hyperparameter, set at construction. tree_ is a learned attribute; it doesn't exist until fit runs.",
        topic="params-hyper", level=2),
    fill("A linear regression model trained on 10 numeric features learns ____ numbers in total (weights plus intercept).",
         "11",
         "One weight per feature, plus one more.",
         "10 weights (one per feature) + 1 intercept = 11 parameters.",
         topic="params-hyper", level=2),
    out("""from sklearn.linear_model import LinearRegression
m = LinearRegression()
r = m.fit([[0], [1], [2]], [1, 3, 5])
print(r is m)""",
        ["True", "False", "None", "TypeError"], 0,
        "Why can you write LinearRegression().fit(X, y).predict(...) on one line?",
        "fit trains the object in place and returns self, which is what allows method chaining.",
        topic="train-infer", level=2),
    out("""from sklearn.linear_model import LinearRegression
m = LinearRegression()
m.predict([[1]])""",
        ["NotFittedError", "ValueError", "[0.]", "AttributeError"], 0,
        "There are no learned weights yet.",
        "Calling predict before fit raises sklearn's NotFittedError: there is no learned function to run.",
        topic="train-infer", level=2),
    out("""import pickle
from sklearn.linear_model import LinearRegression
m = LinearRegression().fit([[0], [1], [2]], [1, 3, 5])
blob = pickle.dumps(m)
m2 = pickle.loads(blob)
print(m2.predict([[10]]))""",
        ["[21.]", "[20.]", "[10.]", "NotFittedError"], 0,
        "Saving a model saves its learned weights.",
        "The learned line is y = 2x + 1. Pickling saves the fitted weights, so the reloaded model predicts 21 for x = 10 without retraining.",
        analogy="Like shipping a compiled binary: build once, run anywhere.",
        topic="train-infer", level=2),
    tf("If you tell a chat LLM a fact during a conversation, its weights are updated so it permanently learns that fact.", False,
       "Is the model being trained while it answers you?",
       "At inference the weights are frozen. The fact only lives in the conversation context and is gone in a fresh chat.",
       topic="train-infer", level=2),
    mcq("In a typical real-world ML project, where does most of the time go?",
        ["Collecting, cleaning and understanding data", "Choosing between model libraries", "Writing the training loop", "Picking the GPU"], 0,
        "Garbage in, garbage out.",
        "Data work (getting labels, cleaning, fixing errors, building features) usually dominates. Model choice is often the smaller part.",
        topic="workflow", level=2),
    out("""from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
pipe = Pipeline([("scale", StandardScaler()), ("model", LogisticRegression())])
print(list(pipe.named_steps))""",
        ["['scale', 'model']", "['model', 'scale']", "['StandardScaler', 'LogisticRegression']", "[]"], 0,
        "named_steps is keyed by the names you gave each step.",
        "A Pipeline bundles preprocessing and the model so the exact same steps run in training and at inference, in order.",
        topic="workflow", level=2),
    mcq("You have 30 labelled examples, and the business needs a decision tomorrow. What's the most sensible first move?",
        ["Use a simple rule or heuristic and collect more data", "Train a large deep neural network", "Fine-tune an LLM on the 30 rows", "Wait until you have a perfect model"], 0,
        "How reliable can a model trained on 30 rows be?",
        "With tiny data, a simple heuristic is often as good and far cheaper. Ship it, log outcomes, and revisit ML when data exists.",
        topic="when-not-ml", level=2),
    tf("A hospital needs a dosage calculator that must be exactly correct every time for a known formula. ML is a good fit here.", False,
       "ML gives statistical answers, not guaranteed ones.",
       "When the formula is known and errors are unacceptable, use the formula. ML is right when the rule is unknown and some error is OK.",
       topic="when-not-ml", level=2),
    tf("A 1990s rule-based expert system for diagnosing diseases is AI but not machine learning.", True,
       "Did it learn anything from data?",
       "Expert systems encode human-written rules. They are AI (they act intelligently) but don't learn, so they aren't ML.",
       topic="ai-ml-dl", level=2),
    mcq("A model scores 100% on its training data and 61% on new data. What is most likely happening?",
        ["It memorised the training data (overfitting)", "It is underfitting", "The new data is too easy", "It is a perfect model"], 0,
        "Big gap between train and unseen performance.",
        "A big train/test gap means the model learned quirks of the training set rather than the real pattern.",
        analogy="Like unit tests that hard-code the expected outputs: all green, but the code is still wrong.",
        topic="generalisation", level=2),
    out("""import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
rng = np.random.default_rng(0)
X = rng.uniform(0, 10, size=(200, 1))
y = np.sin(X[:, 0]) + rng.normal(0, 0.5, 200)
Xtr, Xte, ytr, yte = train_test_split(X, y, random_state=0)
t = DecisionTreeRegressor(random_state=0).fit(Xtr, ytr)
print(t.score(Xtr, ytr), t.score(Xte, yte) < 0.9)""",
        ["1.0 True", "1.0 False", "0.5 True", "0.9 False"], 0,
        "An unlimited-depth tree can give every training point its own leaf.",
        "An unpruned tree memorises the noisy training data (R^2 = 1.0) but scores clearly worse on held-out data.",
        topic="generalisation", level=2),
    out("""from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
X = [[0, 0], [0, 1], [1, 0], [1, 1]]
y = [0, 1, 1, 0]
lin = LogisticRegression().fit(X, y).score(X, y)
tree = DecisionTreeClassifier(random_state=0).fit(X, y).score(X, y)
print(lin, tree)""",
        ["0.5 1.0", "1.0 1.0", "1.0 0.5", "0.75 0.75"], 0,
        "XOR can't be separated by a single straight line.",
        "Logistic regression assumes a straight decision boundary, which can't separate XOR (it gets 0.5). A tree's axis-aligned splits can.",
        diagram="""
 x2
 1 | 1   0      no single line puts
 0 | 0   1      both 1s on one side
   +-------- x1
     0   1
""",
        topic="inductive-bias", level=2),
    out("""import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
rng = np.random.default_rng(0)
for n in (100, 10000):
    X = rng.normal(size=(n, 3)); y = X.sum(axis=1)
    lr = LinearRegression().fit(X, y)
    knn = KNeighborsRegressor().fit(X, y)
    print(lr.coef_.size, knn.n_samples_fit_)""",
        ["3 100\n3 10000", "3 100\n3 100", "100 100\n10000 10000", "3 3\n3 3"], 0,
        "One model stores weights; the other stores the training rows.",
        "Linear regression keeps 3 weights whatever n is (parametric). kNN keeps every training sample to search at predict time (non-parametric).",
        topic="parametric", level=2),
    out("""from sklearn.dummy import DummyClassifier
import numpy as np
X = np.zeros((100, 1))
y = np.array([0] * 95 + [1] * 5)
d = DummyClassifier(strategy="most_frequent").fit(X, y)
print(d.score(X, y))""",
        ["0.95", "0.05", "0.5", "1.0"], 0,
        "It always predicts the most common class.",
        "Predicting 'not fraud' for everyone already scores 95% accuracy. Any real model must beat this baseline, and accuracy is a poor metric here.",
        topic="framing", level=2),
    mcq("An e-commerce site wants to 'reduce returns'. Which is the best-framed ML task?",
        ["At checkout, predict the probability this order will be returned within 30 days", "Predict returns", "Use AI to improve returns", "Cluster all products"], 0,
        "A good framing says when you predict, what exactly, and over what window.",
        "A precise framing fixes the prediction point (checkout), the target (returned or not) and the window (30 days).",
        topic="framing", level=2),

    # ------------------------------------------------------------------ L3
    mcq("A learned model says a transaction is 'fraud' with 0.97 probability. How should an engineer treat that output compared with a hand-written rule?",
        ["As a statistical estimate that can be wrong and needs evaluation and monitoring", "As a guaranteed fact, because it was learned from data", "As less reliable than any rule", "As something that never changes"], 0,
        "Learned rules come from patterns in past data.",
        "Model outputs are estimates from past data. They can be confidently wrong, especially on inputs unlike the training data.",
        topic="rules-vs-learned", level=3),
    mcq("Where should hyperparameters like max_depth be tuned?",
        ["On a validation set (or with cross-validation on the training data)", "On the test set", "On the training set score alone", "They should never be tuned"], 0,
        "The test set must stay untouched until the very end.",
        "Tuning on the test set leaks it into your choices, so the final score is optimistic. Tune with validation or cross-validation.",
        topic="params-hyper", level=3),
    mcq("Which of these is a hyperparameter of kNN, not a parameter?",
        ["k, the number of neighbours", "The stored training points", "The predicted label", "The distance between two specific points"], 0,
        "What do you pass to the constructor?",
        "k is chosen by you (n_neighbors). kNN has no learned weights; it stores the data and uses k at predict time.",
        topic="params-hyper", level=3),
    mcq("A recommendation model is retrained nightly on a GPU cluster, then serves 50,000 requests per second. Which concern belongs to inference rather than training?",
        ["Latency per request (e.g. under 20 ms)", "Number of epochs", "Learning rate schedule", "Size of the training dataset"], 0,
        "What does the user waiting for a response care about?",
        "Inference is about latency, throughput and cost per request. Epochs, learning rates and dataset size are training concerns.",
        topic="train-infer", level=3),
    mcq("Why should you build a dumb baseline (majority class, last value, a simple rule) before a complex model?",
        ["It shows whether the complex model adds real value and catches pipeline bugs", "Baselines are always good enough", "Complex models need a baseline to train", "It makes training faster"], 0,
        "How would you know your 92% accuracy is good?",
        "If a baseline already gets 90%, your 92% model may not be worth the cost. A model that loses to the baseline usually has a bug.",
        analogy="Like benchmarking a new service against the old one before migrating.",
        topic="workflow", level=3),
    tf("If monitoring shows the input data in production has drifted away from the training data, the usual fix is to retrain on recent data, which sends you back into the workflow loop.", True,
       "The workflow is a cycle, not a line.",
       "Drift is caught by monitoring and triggers retraining (and sometimes re-framing), closing the loop.",
       topic="workflow", level=3),
    mcq("A team is deciding between a hand-tuned heuristic that gets 88% and an ML model that gets 89%. Which factor most strongly favours the heuristic?",
        ["The ML model needs data pipelines, retraining and monitoring for a 1-point gain", "The heuristic is older", "ML models can't reach 89%", "Heuristics can't be tested"], 0,
        "ML has an ongoing running cost.",
        "ML systems carry maintenance cost (data, retraining, monitoring, debugging). A tiny gain rarely justifies it.",
        topic="when-not-ml", level=3),
    mcq("Which is the strongest reason NOT to use ML for a decision?",
        ["Each decision must be fully explainable by a fixed, auditable rule", "You have lots of labelled data", "The pattern is complex", "The task is repeated millions of times"], 0,
        "Three of these are reasons FOR ML.",
        "Lots of data, complex patterns and high volume favour ML. A hard requirement for exact, auditable rules favours explicit logic.",
        topic="when-not-ml", level=3),
    mcq("GPT-style LLMs are best described as:",
        ["Deep learning models trained to generate text by predicting the next token", "Rule-based systems with a huge dictionary", "Classical ML models like decision trees", "Unsupervised clustering models"], 0,
        "What does the model actually output at each step?",
        "An LLM is a deep neural network (transformer) that generates text one token at a time, learned from huge amounts of text.",
        topic="ai-ml-dl", level=3),
    mcq("A model is too simple for the problem (e.g. a straight line for a curved pattern). Adding 10x more training data will:",
        ["Barely help, because the model still can't represent the curve (high bias)", "Fix it completely", "Make it overfit", "Make training error go to zero"], 0,
        "Is the problem the amount of data or what the model can express?",
        "More data reduces variance, not bias. A straight line stays a straight line however much data you give it.",
        topic="generalisation", level=3),
    mcq("Which pair correctly matches the problem with the fix?",
        ["High variance -> more data or stronger regularisation; high bias -> a more flexible model or better features",
         "High variance -> a more flexible model; high bias -> more data",
         "High variance -> fewer training examples; high bias -> more regularisation",
         "Both are fixed only by training longer"], 0,
        "Variance = over-reacting to the sample; bias = too-simple assumptions.",
        "Overfitting (variance) is reduced by more data or constraints; underfitting (bias) needs more capacity or more informative features.",
        diagram="""
 error
  |\\                 /  total
  | \\  bias^2    __/
  |  \\_______ _/  variance
  +------------------> model complexity
     underfit   sweet   overfit
""",
        topic="generalisation", level=3),
    out("""import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
X = np.arange(10).reshape(-1, 1)
y = 2 * X[:, 0]
lr = LinearRegression().fit(X, y)
dt = DecisionTreeRegressor().fit(X, y)
print(round(lr.predict([[20]])[0]), dt.predict([[20]])[0])""",
        ["40 18.0", "40 40.0", "18 18.0", "20 20.0"], 0,
        "x = 20 is outside the training range 0..9.",
        "The linear model assumes a line and extrapolates to 40. A tree can only output values it saw in a leaf, so it returns 18 (the last leaf).",
        topic="inductive-bias", level=3),
    mcq("Which statement describes kNN's inductive bias?",
        ["Points that are close together in feature space tend to have the same label", "The output is a linear function of the inputs", "Features are independent given the class", "Nearby pixels matter more than distant ones"], 0,
        "How does kNN make a prediction?",
        "kNN predicts from the nearest training points, so it assumes nearby means similar. Linear = line; Naive Bayes = independence; CNN = locality.",
        topic="inductive-bias", level=3),
    tf("A k-nearest-neighbours model does almost no work in fit and most of its work in predict.", True,
       "What does kNN store, and when does it search?",
       "kNN is a 'lazy learner': fit just stores the data; predict computes distances to the stored points. That's why its inference is slow on big data.",
       topic="parametric", level=3),
    mcq("Which of these models is non-parametric?",
        ["A decision tree with no depth limit", "Logistic regression", "Linear regression", "A neural network with a fixed architecture"], 0,
        "Which one can keep growing as you add more data?",
        "An unlimited tree adds more splits and leaves as data grows. The others have a size fixed before training.",
        topic="parametric", level=3),
    mcq("A bank wants to catch fraud. Missing a fraud costs about 50,000 rupees; flagging a good transaction costs about 50 rupees of support time. Which metric fits best?",
        ["Recall on fraud (at an acceptable precision), or expected cost", "Plain accuracy", "Mean squared error", "Training loss"], 0,
        "Which mistake is 1000x more expensive?",
        "Misses are very costly, so you care about catching most frauds (recall) while keeping false alarms tolerable, ideally scoring by expected cost.",
        topic="framing", level=3),

    # ------------------------------------------------------------------ L4
    mcq("A loan-approval product uses an ML risk score, but a lawyer insists some applicants must always be rejected (e.g. under 18). What is the sound design?",
        ["Hard rules as guardrails before/after the model, with the model handling the fuzzy cases", "Add age as a feature and trust the model to learn the rule", "Drop the model and only use rules", "Retrain until the model never approves minors"], 0,
        "Some requirements are not statistical.",
        "Legal or safety invariants should be enforced by deterministic code. A model can learn 'usually', never 'always'.",
        analogy="Like validation in a backend: you don't trust the client, you enforce the invariant on the server.",
        topic="rules-vs-learned", level=4),
    mcq("You try 200 hyperparameter settings and pick the one with the best validation score. Why might that score still be optimistic?",
        ["You overfit to the validation set by selecting the luckiest setting; a separate test set (or nested CV) is needed",
         "Validation scores are always pessimistic", "Hyperparameters don't affect generalisation", "200 trials is too few to matter"], 0,
        "Selection itself is a form of fitting.",
        "Picking the max of many noisy scores biases the result upwards. Keep an untouched test set or use nested cross-validation for an honest estimate.",
        topic="params-hyper", level=4),
    mcq("A model scores well offline, but in production its accuracy is much lower. Investigation shows the training pipeline computed 'average order value' with pandas, while the serving code recomputes it in Java with a different rounding and time window. This is:",
        ["Training-serving skew", "Overfitting", "Underfitting", "Class imbalance"], 0,
        "The same feature is computed differently in two places.",
        "When features are computed differently at train and serve time, the model sees inputs it wasn't trained on. Share one feature pipeline (or a feature store).",
        topic="train-infer", level=4),
    mcq("A news app's model ranks articles; it is retrained every week on what users clicked. Over months, it shows mostly one type of article and the click data reflects only that. What has gone wrong?",
        ["A feedback loop: the model's own outputs now shape its training labels", "Overfitting to the test set", "Training-serving skew", "The learning rate is too high"], 0,
        "Where does the training data come from?",
        "Users can only click what the model showed them, so the labels are biased by past predictions. Add exploration or log what was shown, not just what was clicked.",
        topic="workflow", level=4),
    tf("A deployed model can degrade silently: the service keeps returning 200 OK with valid-looking predictions while accuracy drops.", True,
       "ML failures aren't exceptions.",
       "Unlike a crash, a wrong prediction looks normal. That's why you monitor input distributions, prediction distributions and, when labels arrive, real accuracy.",
       topic="workflow", level=4),
    mcq("Why is ML a risky fit for spam/fraud detection compared with, say, weather forecasting?",
        ["The data is adversarial: attackers change behaviour to beat the model, so the distribution shifts on purpose", "There's never any labelled data", "The patterns are too simple", "The costs of errors are always zero"], 0,
        "The weather doesn't try to fool your forecast.",
        "Adversaries probe and adapt, so a model decays faster and must be paired with rules, fast retraining and monitoring.",
        topic="when-not-ml", level=4),
    tf("Because 'AI' appears in a product's name, it must contain a model learned from data.", False,
       "Recall what counts as AI but not ML.",
       "Plenty of 'AI' features are rules, search or heuristics. AI is the goal; ML is just one way to reach it.",
       topic="ai-ml-dl", level=4),
    mcq("For squared-error regression, the expected test error at a point can be split into which three parts?",
        ["bias^2 + variance + irreducible noise", "bias + variance - noise", "training error + validation error + test error", "precision + recall + F1"], 0,
        "One part can't be removed by any model.",
        "Bias^2 (wrong assumptions) + variance (sensitivity to the sample) + noise (randomness in the labels themselves).",
        topic="generalisation", level=4),
    tf("Given enough data and a powerful enough model, test error can always be driven to zero.", False,
       "What if two identical inputs have different true outcomes?",
       "Irreducible noise remains: if the label isn't fully determined by the features (e.g. same profile, different outcome), no model can be perfect.",
       topic="generalisation", level=4),
    mcq("What does the No Free Lunch theorem actually say?",
        ["Averaged over ALL possible problems, every learning algorithm performs the same; any advantage comes from matching assumptions to a problem class",
         "All algorithms perform equally on every real dataset",
         "Deep learning is always the best algorithm",
         "You can't get good results without paying for cloud compute"], 0,
        "It's a statement about an average over every imaginable problem.",
        "NFL doesn't say algorithms are equal on YOUR problem. It says no algorithm wins everywhere, so you choose one whose inductive bias fits the data.",
        topic="inductive-bias", level=4),
    mcq("Convolutional neural networks work well on images mainly because their architecture builds in which inductive bias?",
        ["Locality and translation equivariance: nearby pixels matter together and a pattern means the same thing anywhere", "Feature independence", "Linear separability", "Every pixel is equally related to every other pixel"], 0,
        "A small filter slides across the whole image with the same weights.",
        "Small shared filters assume local structure and that a cat's ear is an ear wherever it appears. That's the assumption that matches images.",
        topic="inductive-bias", level=4),
    tf("A transformer with 70 billion weights is a non-parametric model because it has so many parameters.", False,
       "Parametric is about whether the size grows with the data, not how big it is.",
       "Its number of weights is fixed by the architecture before training, so it's parametric, just very large.",
       topic="parametric", level=4),
    tf("'Non-parametric' means the model has no parameters at all.", False,
       "Think of a decision tree's thresholds.",
       "Non-parametric models do have parameters (tree thresholds, stored points); their NUMBER grows with the data rather than being fixed.",
       topic="parametric", level=4),
    mcq("A support team is rewarded on 'average ticket close time', which a model is trained to predict and minimise. Agents start closing tickets early without solving them. This is an example of:",
        ["Goodhart's law: a proxy metric stops measuring what you care about once you optimise it", "Overfitting", "Training-serving skew", "Data leakage"], 0,
        "When a measure becomes a target...",
        "The proxy (close time) diverged from the goal (solved problems). Choose targets and guard-rail metrics that are hard to game.",
        topic="framing", level=4),
    mcq("A churn model gets 0.99 AUC offline. One feature is 'number of support calls in the 30 days after the prediction date'. What is wrong?",
        ["Label leakage: the feature uses information from the future that won't exist at prediction time", "Nothing, it's a strong feature", "The model is underfitting", "AUC can't be 0.99"], 0,
        "Ask: would this value be known at the moment you make the prediction?",
        "Features must be computed only from data available at the prediction point. Future information makes offline scores great and production useless.",
        diagram="""
 past data  | prediction point |  future (label window)
 features OK|        ^         |  NOT allowed as features
""",
        topic="framing", level=4),
    fill("The principle 'when a measure becomes a target, it ceases to be a good measure' is called ____'s law.",
         "Goodhart",
         "Named after a British economist.",
         "Goodhart's law: optimising a proxy hard enough makes it drift from the real goal (e.g. clicks -> clickbait).",
         topic="framing", level=4),
]


TOPICS += [
    ("genai-lens", "ML thinking for GenAI apps"),
]

QUESTIONS += [
    # ============================================================ more L1
    tf("In an ML project you still write plenty of code; the part you don't hand-write is the decision logic inside the model.", True,
       "Who writes the data loading, the API and the tests?",
       "You still write pipelines, training scripts, serving code and tests. Only the mapping from input to prediction is learned from examples instead of typed as if-statements.",
       topic="rules-vs-learned", level=1),
    out("from sklearn.linear_model import LinearRegression\nm = LinearRegression().fit([[1], [2], [3]], [2, 4, 6])\nprint(m.predict([[5], [6]]).round(1))",
        ["[10. 12.]", "[5. 6.]", "[2. 4.]", "[10 12]"], 0,
        "The model learned y = 2x once. Now it is just used.",
        "Training found the rule y = 2x. Inference applies the frozen rule to any number of new inputs: 2*5 = 10 and 2*6 = 12. predict returns floats, so NumPy prints `10.` and `12.`.",
        question="Train once, predict many. What does this print?",
        topic="train-infer", level=1),
    mcq("In a table of houses with columns size, bedrooms, city and price, what are size, bedrooms and city called when you predict price?",
        ["Features: the inputs the model uses", "Labels: the answers", "Hyperparameters", "Weights"], 0,
        "They are what the model gets to look at.",
        "Features are the input columns (X). The column you predict (price) is the label or target (y). Weights are what the model learns; hyperparameters are knobs you set.",
        diagram="""
 size  bedrooms  city  | price
 120   3         BLR   | 95 L
 \\_____ features (X) _/   label (y)
""",
        topic="workflow", level=1),
    out("def shipping_fee(order_total):\n    return 0 if order_total >= 500 else 40\n\nprint(shipping_fee(499), shipping_fee(500))",
        ["40 0", "0 40", "40 40", "0 0"], 0,
        "Follow the if-rule exactly; 500 counts as 'at least 500'.",
        "A business rule like 'free shipping from 500' is exact and known. Plain code does it perfectly; training a model to guess it would only add errors and cost.",
        question="This business rule needs no ML at all. What does it print?",
        topic="when-not-ml", level=1),
    mcq("'Deep learning' means machine learning that uses:",
        ["Neural networks with many layers", "Very large spreadsheets", "Rules written by experts", "Only image data"], 0,
        "The 'deep' is about stacking.",
        "Deep learning = neural networks with many stacked layers, each building on the one below. It works on text, audio and tables too, not just images.",
        analogy="Like a factory line: each layer (station) turns rough parts into more refined ones, and 'deep' just means many stations.",
        topic="ai-ml-dl", level=1),
    mcq("A student memorises the answers to last year's exam word for word, then fails this year's exam with new questions. In ML terms the student:",
        ["Overfit: memorised the examples instead of learning the pattern", "Generalised well", "Underfit: learned too little from the examples", "Used too much data"], 0,
        "Did the student learn the subject, or the specific questions?",
        "Memorising the training examples gives a perfect score on them and a poor one on new cases. Generalising means learning the pattern behind them.",
        analogy="Overfitting is a test suite that only passes because the code hard-codes the expected outputs.",
        topic="generalisation", level=1),
    mcq("A k-nearest-neighbours model keeps every training example and compares new points to them. If you train it on twice as much data, its saved model:",
        ["Gets about twice as big", "Stays exactly the same size", "Gets smaller", "Stops working"], 0,
        "What does kNN actually store?",
        "kNN stores the training data itself, so its size grows with the data. That is what 'non-parametric' means. A linear model would stay the same size.",
        diagram="""
linear model:  [w1 w2 w3 b]          same size at any n
kNN:           [row1 row2 ... rowN]  grows with N
""",
        topic="parametric", level=1),
    mcq("A telecom company asks 'will this customer cancel next month?'. What is a sensible label for each training row?",
        ["Yes/No: did that customer cancel in the following month", "The customer's name", "The total number of customers", "The model's accuracy"], 0,
        "The label is the answer you want the model to predict, taken from history.",
        "You take past customers, look at what happened next (cancelled or not) and use that as the label. It is a yes/no (binary classification) target.",
        topic="framing", level=1),
    mcq("Your web app sends a prompt to an LLM API and gets an answer back. In ML terms, that call is:",
        ["Inference: running an already-trained model on new input", "Training the model on your prompt", "Labelling data", "Hyperparameter tuning"], 0,
        "Did anyone change the model's weights?",
        "The provider trained the model earlier. Your request only runs it forward on your input, which is inference. Your prompt does not become training data at that moment.",
        topic="genai-lens", level=1),
    tf("An LLM is a machine-learning model: its behaviour came from training on huge amounts of text, not from rules typed in by hand.", True,
       "Nobody wrote an if-statement for every possible question.",
       "LLMs learn their weights from data (predicting the next token, then fine-tuning). That is why they can be wrong in surprising ways, like any learned function.",
       topic="genai-lens", level=1),

    # ============================================================ more L2
    out("from sklearn.linear_model import Ridge\nX = [[1, 0, 2], [0, 1, 1], [2, 1, 0], [1, 1, 1]]\ny = [3, 2, 4, 3]\nm = Ridge(alpha=1.0).fit(X, y)\nprint(m.alpha, m.coef_.shape)",
        ["1.0 (3,)", "(3,) 1.0", "1.0 (4,)", "AttributeError"], 0,
        "alpha is what you set; coef_ is one learned weight per feature.",
        "alpha (regularisation strength) is a hyperparameter you passed in. coef_ is learned: one weight per column, so 3 columns gives shape (3,). The underscore marks learned attributes.",
        topic="params-hyper", level=2),
    out("import numpy as np\nfrom sklearn.neighbors import KNeighborsClassifier\nfrom sklearn.model_selection import train_test_split\nrng = np.random.default_rng(0)\nX = rng.normal(size=(400, 2))\ny = (X[:, 0] + X[:, 1] + rng.normal(0, 1.2, 400) > 0).astype(int)\nXtr, Xte, ytr, yte = train_test_split(X, y, random_state=0)\nk1 = KNeighborsClassifier(n_neighbors=1).fit(Xtr, ytr)\nk15 = KNeighborsClassifier(n_neighbors=15).fit(Xtr, ytr)\nprint(k1.score(Xtr, ytr), k15.score(Xte, yte) > k1.score(Xte, yte))",
        ["1.0 True", "1.0 False", "0.78 True", "0.5 False"], 0,
        "With k=1, every training point's nearest neighbour is itself.",
        "k=1 scores 1.0 on training data because each point votes for itself, so it memorises the noise. On the test set the smoother k=15 wins (0.78 vs 0.74). The training score said nothing about the test score.",
        topic="generalisation", level=2),
    mcq("Why put the scaler inside a scikit-learn Pipeline with the model, instead of scaling the data once in a notebook?",
        ["The same fitted steps travel with the model, so serving and cross-validation apply them exactly as in training", "Pipelines make the model more accurate by themselves", "Scalers only work inside pipelines", "It removes the need for a test set"], 0,
        "Think about what the production server must repeat.",
        "A Pipeline bundles preprocessing and model into one object: fit learns the scaler's mean/std and the weights together, and predict replays both. That prevents train/serve mismatches and leakage inside cross-validation.",
        diagram="""
fit:     X --> [scaler.fit+transform] --> [model.fit]
predict: x --> [scaler.transform]     --> [model.predict]
          one object, saved and loaded together
""",
        topic="workflow", level=2),
    mcq("A PM wants ML to detect duplicate signups. Nobody has labelled duplicates, and 'same verified email or same phone number' already catches 99% of them. Best first move?",
        ["Ship the rule, log the cases it misses, and revisit ML only if those misses matter", "Train a deep model on all signups", "Use clustering and call every cluster a duplicate group", "Wait until 1 million duplicates are labelled"], 0,
        "What does a simple rule already give you?",
        "A cheap exact rule covers almost everything. Logging its misses also produces labelled examples, which you would need anyway if ML is ever justified.",
        topic="when-not-ml", level=2),
    mcq("Which of these is machine learning but NOT deep learning?",
        ["A random forest predicting loan default from a table of numbers", "A transformer translating text", "A convolutional network spotting cats in photos", "A hand-written chess rule engine"], 0,
        "Which one learns from data without a multi-layer neural network?",
        "Random forests learn from data (ML) but are ensembles of decision trees, not neural networks. The transformer and CNN are deep learning; the rule engine is not ML at all.",
        diagram="""
ML (learns from data)
 |-- classic: linear, trees, random forest, kNN
 +-- deep learning: CNN, RNN, transformer
""",
        topic="ai-ml-dl", level=2),
    mcq("You fit a linear regression of house price on size. Which assumption have you built in before seeing a single house?",
        ["Each extra square metre adds the same amount to the price, at any size", "Price depends only on the city", "Big houses are always cheaper", "Price can only take a few fixed values"], 0,
        "What shape can a linear model draw?",
        "That is the inductive bias of a linear model: a constant slope. If the real effect flattens out for huge houses, the model can't express it unless you add features like size squared.",
        topic="inductive-bias", level=2),
    mcq("For a model that predicts 'which customers will churn next month', what should ONE training row usually be?",
        ["One customer at one point in time, with features up to that date and the label from the month after", "One month of the whole company's data", "One support ticket", "One feature column"], 0,
        "What is the thing you make a prediction about, and when?",
        "The unit of prediction is a customer at a snapshot date. Picking it decides what the features and label mean; mixing units (tickets vs customers) quietly breaks the model.",
        topic="framing", level=2),
    mcq("In an LLM app, a fixed set of example inputs with the expected (or acceptable) answers that you run after every prompt change is called an eval set. Its closest SDE equivalent is:",
        ["A regression test suite", "A load balancer", "A database index", "A feature flag"], 0,
        "You run it to catch things that used to work and broke.",
        "Evals are to models what tests are to code: a change (new prompt, new model version) is only accepted if the scores don't drop. Without them every prompt tweak is a guess.",
        analogy="Changing a prompt without evals is like refactoring without tests: it 'looks fine' on the one case you tried.",
        topic="genai-lens", level=2),
    out("from sklearn.linear_model import LinearRegression\nm = LinearRegression()\nm.fit([[1], [2], [3]], [2, 4, 6])\nm.fit([[1], [2], [3]], [5, 10, 15])\nprint(round(m.coef_[0], 1))",
        ["5.0", "2.0", "3.5", "7.0"], 0,
        "Does the second fit continue from the first?",
        "In scikit-learn, fit starts over from scratch: the second call throws away the old weights. Only partial_fit (or warm_start on some models) continues learning.",
        analogy="fit is a clean rebuild, not an incremental build.",
        topic="train-infer", level=2),

    # ============================================================ more L3
    out("import numpy as np\nfrom sklearn.linear_model import LinearRegression\nrng = np.random.default_rng(0)\nfor n in (50, 5000):\n    X = rng.uniform(-3, 3, size=(n, 1))\n    y = X[:, 0] ** 2 + rng.normal(0, 0.3, n)\n    print(round(LinearRegression().fit(X, y).score(X, y), 1))",
        ["0.0\n0.0", "0.0\n0.9", "0.5\n1.0", "1.0\n1.0"], 0,
        "Can a straight line ever fit a U shape, however many points you give it?",
        "The data is a parabola; a straight line through a symmetric U is almost flat, so R^2 is about 0 even on training data. 100x more data doesn't help: this is high bias, and only a more flexible model or a better feature (x^2) fixes it.",
        topic="generalisation", level=3),
    out("import numpy as np\nfrom sklearn.dummy import DummyRegressor\nX = np.zeros((5, 1))\ny = np.array([10.0, 20.0, 30.0, 40.0, 50.0])\nbase = DummyRegressor(strategy=\"mean\").fit(X, y)\nprint(base.predict(X[:1]), base.score(X, y))",
        ["[30.] 0.0", "[30.] 1.0", "[10.] 0.0", "[50.] 0.5"], 0,
        "R^2 compares the model with always predicting the mean.",
        "The mean baseline always predicts 30, and its R^2 is exactly 0 by definition. Any real model must beat 0; a negative R^2 means it is worse than this one-line baseline.",
        topic="workflow", level=3),
    out("from sklearn.model_selection import GridSearchCV\nfrom sklearn.neighbors import KNeighborsClassifier\nfrom sklearn.datasets import load_iris\nX, y = load_iris(return_X_y=True)\ngrid = {\"n_neighbors\": [1, 3, 5], \"weights\": [\"uniform\", \"distance\"]}\ngs = GridSearchCV(KNeighborsClassifier(), grid, cv=5).fit(X, y)\nprint(len(gs.cv_results_[\"params\"]), gs.n_splits_)",
        ["6 5", "5 6", "3 5", "30 1"], 0,
        "Count the combinations of the two lists, then the folds.",
        "3 values x 2 values = 6 hyperparameter combinations, each scored with 5-fold CV: 30 fits, plus one refit of the winner on all data. Hyperparameter search multiplies training cost quickly.",
        topic="params-hyper", level=3),
    out("from sklearn.base import clone\nfrom sklearn.linear_model import LinearRegression\nm = LinearRegression(fit_intercept=False).fit([[1], [2]], [2, 4])\nc = clone(m)\nprint(c.get_params()[\"fit_intercept\"], hasattr(c, \"coef_\"))",
        ["False False", "False True", "True False", "True True"], 0,
        "clone copies the recipe, not the result.",
        "clone builds a fresh unfitted estimator with the same hyperparameters (fit_intercept=False) but no learned attributes, so coef_ is missing. Cross-validation uses this to train each fold from scratch.",
        analogy="clone copies the config file, not the compiled binary.",
        topic="train-infer", level=3),
    out("import numpy as np\nfrom sklearn.tree import DecisionTreeRegressor\nrng = np.random.default_rng(0)\nsizes = []\nfor n in (100, 1000):\n    X = rng.uniform(0, 10, size=(n, 1))\n    y = np.sin(X[:, 0]) + rng.normal(0, 0.3, n)\n    sizes.append(int(DecisionTreeRegressor(random_state=0).fit(X, y).get_n_leaves()))\nprint(sizes)",
        ["[100, 1000]", "[10, 10]", "[50, 500]", "[1, 1]"], 0,
        "An unlimited tree keeps splitting until every leaf is pure.",
        "With no max_depth, the tree grows one leaf per (distinct) training point, so its size scales with the data. That is non-parametric behaviour, and also why unpruned trees overfit.",
        topic="parametric", level=3),
    out("import numpy as np\nfrom sklearn.linear_model import LinearRegression\nx = np.arange(-3, 4).reshape(-1, 1)\ny = x[:, 0] ** 2\nlin = LinearRegression().fit(x, y).score(x, y)\nx2 = np.hstack([x, x ** 2])\nquad = LinearRegression().fit(x2, y).score(x2, y)\nprint(round(lin, 2), round(quad, 2))",
        ["0.0 1.0", "1.0 1.0", "0.0 0.0", "0.5 1.0"], 0,
        "The second model gets x squared as an extra input column.",
        "A line through a symmetric parabola has slope 0, so R^2 = 0. Adding x^2 as a feature lets the same linear model fit perfectly. Feature engineering changes what a model can express without changing the algorithm.",
        topic="inductive-bias", level=3),
    mcq("A model that spots potholes was trained only on daytime photos. At night it misses most potholes. What does this say about learned rules?",
        ["They are only reliable inside the kind of data they were trained on; outside it they can fail badly", "The model has a bug in its code", "Night photos must be labelled wrong", "More epochs on the daytime data will fix it"], 0,
        "Where did the model ever see a dark pothole?",
        "A learned function is a statistical summary of its training data. Inputs from a region it never saw (night) are out of distribution; you need data from that region, not more training on the old data.",
        diagram="""
   brightness
   high | x x x x x x    <- training data (day)
        |
   low  |      ?  ?  ?   <- night: never seen
        +------------------
""",
        topic="rules-vs-learned", level=3),
    tf("A trained neural network is as easy to debug as hand-written rules, because you can print all of its weights.", False,
       "Can you read a bug report out of a list of 10 million floats?",
       "You can print weights, but they don't map to readable reasons. Debugging ML means checking data, slices of errors and evals, not reading the logic line by line. Small trees and linear models are the exception.",
       analogy="Like trying to debug a program by reading the compiled binary: every byte is visible and none of it explains itself.",
       topic="rules-vs-learned", level=3),
    mcq("Which list contains ONLY hyperparameters?",
        ["Learning rate, number of trees, max_depth, regularisation strength C", "Learning rate, the split thresholds of a tree, max_depth", "coef_, intercept_, learning rate", "Number of layers, the layer weights, batch size"], 0,
        "Ask of each item: did I choose it, or did training compute it?",
        "Split thresholds, coef_, intercept_ and layer weights are learned (parameters). Learning rate, tree count, depth, C, number of layers and batch size are chosen before training.",
        analogy="Hyperparameters are build flags you set; parameters are the binary the build produces.",
        topic="params-hyper", level=3),
    mcq("Your new recommendation model beats the old one offline. What is the safest way to confirm it helps real users before switching everyone?",
        ["An A/B test (or a shadow run first): send a slice of traffic to the new model and compare business metrics", "Deploy it to everyone and watch social media", "Re-run the offline evaluation five times", "Ask the data scientists to vote"], 0,
        "Offline data is history; users react to what you show them.",
        "Offline metrics can miss how users respond to new recommendations. A shadow run checks it works on live traffic without showing results; an A/B test measures the real effect.",
        diagram="""
traffic --+--> 95% --> old model --> metrics A
          +-->  5% --> new model --> metrics B
             compare A vs B, then roll out
""",
        topic="workflow", level=3),
    tf("A nightly job that retrains the model and automatically deploys it, without comparing it against the current model on a held-out set, is a safe setup.", False,
       "What stops a bad data day from shipping a broken model?",
       "Retraining needs a gate: evaluate the new model on held-out data (and key slices) and only promote it if it beats or matches the current one. Otherwise one corrupt data load ships straight to users.",
       analogy="It's like auto-deploying every commit to production without running CI.",
       topic="workflow", level=3),
    mcq("For a 'is this message abusive?' model, two expert moderators agree on only 55% of the same messages. What does that tell you before any training?",
        ["The labels are too inconsistent; fix the labelling guidelines first, because a model can't learn a rule humans don't share", "Use a bigger model to resolve the disagreement", "This is perfect data for unsupervised learning", "Drop the experts and use accuracy as the only metric"], 0,
        "What would a 'correct' answer even mean here?",
        "Label agreement caps what any model can achieve and makes evaluation meaningless. Clear guidelines and agreement checks come first; sometimes the honest answer is that the task is not well-defined enough for ML yet.",
        topic="when-not-ml", level=3),
    mcq("A sentiment classifier built on BERT and a chatbot built on GPT are both deep learning. What is the key difference in what they output?",
        ["The classifier outputs a label for the input (discriminative); the chatbot generates new text token by token (generative)", "Only the chatbot uses a neural network", "The classifier is rule-based AI", "There is no difference; both generate text"], 0,
        "One answers 'which class?', the other writes something new.",
        "Discriminative models map input to a label, p(y given x). Generative models produce new content, p(next token given previous). GenAI is the generative part of deep learning.",
        diagram="""
+--------------- AI ----------------+
| rules   +-------- ML ----------+  |
|         | trees  +---- DL ---+ |  |
|         |        | BERT clf  | |  |
|         |        | [GenAI:   | |  |
|         |        |  GPT]     | |  |
|         |        +-----------+ |  |
|         +----------------------+  |
+-----------------------------------+
""",
        topic="ai-ml-dl", level=3),
    mcq("You plot training and validation error against training-set size. Both curves flatten out close together, at a high error. What is the diagnosis?",
        ["High bias: the model is too simple, so more data won't help; use a more flexible model or better features", "High variance: get more data", "Data leakage", "The model is perfect"], 0,
        "A small gap means it isn't memorising. A high floor means...?",
        "Curves that meet at a high error mean the model can't capture the pattern (underfitting). A big gap between low train error and high validation error would mean variance, which more data does help.",
        diagram="""
error
 |  val   \\_______________   <- both high,
 |  train /---------------      small gap
 |
 +------------------------> training size
""",
        topic="generalisation", level=3),
    tf("Regularisation (for example a larger alpha in Ridge) usually adds a little bias in exchange for a larger drop in variance.", True,
       "It pulls the weights towards zero. Is that simpler or more complex?",
       "Shrinking weights makes the model less flexible (more bias) but much less sensitive to the particular training sample (less variance). Tuning alpha on validation data finds the balance.",
       topic="generalisation", level=3),
    mcq("On tabular business data (mixed numeric and categorical columns, some irrelevant), gradient-boosted trees often beat neural networks. Which explanation fits best?",
        ["Trees' inductive bias (axis-aligned splits, no need for scaling, ignoring useless columns) matches tables well", "Neural networks can't take numbers as input", "Boosted trees have more parameters than any neural net", "No free lunch says trees always win"], 0,
        "Think about what shape of function each model finds easy.",
        "Tables have features with different units and sharp thresholds ('age > 65'), which split-based models express naturally. NNs prefer smooth functions and lots of data. It's a match of assumptions, not a universal law.",
        topic="inductive-bias", level=3),
    mcq("A fraud check must run on a phone in under 5 ms. The training set has 10 million rows. Which model family suits this better, and why?",
        ["A parametric model (e.g. logistic regression or a small NN): its size and prediction cost don't grow with the training data", "kNN: it learns fastest", "kNN: it has no parameters to store", "Any model, as size never matters"], 0,
        "What would kNN have to ship to the phone and search per prediction?",
        "kNN must store and search all 10M rows at prediction time. A parametric model compresses the data into a fixed set of weights, so it is small and fast to serve.",
        topic="parametric", level=3),
    mcq("A churn model predicts 'will this customer cancel TOMORROW?' with great accuracy, but the retention team needs two weeks to run a save campaign. What is wrong?",
        ["The prediction point is too late to act on; predict far enough ahead (e.g. 30 days) for the action to work", "Accuracy is the wrong metric", "Churn should be a regression problem", "Nothing; high accuracy is all that matters"], 0,
        "A correct prediction you can't act on is worth nothing.",
        "Framing includes WHEN you predict. The horizon must leave time for the business action. Predicting further ahead is harder (lower accuracy) but useful.",
        diagram="""
today ---- 14 days to act ----> cancel date
  ^ predict here            ^ 'tomorrow' model
    (useful)                  predicts here (too late)
""",
        topic="framing", level=3),
    mcq("A team must route support tickets into 5 categories. They have 200,000 labelled tickets, a 50 ms latency budget and millions of tickets a day. What fits best?",
        ["A small classifier trained on the labelled tickets (maybe on top of embeddings); an LLM prompt can help bootstrap or handle rare cases", "Send every ticket to the largest LLM with a prompt", "Clustering, since categories are known", "Hand-write keyword rules for all 5 categories"], 0,
        "Plenty of labels, strict latency, huge volume.",
        "With lots of labels and a fixed set of classes, a trained classifier is cheaper, faster and easier to evaluate. LLM prompting shines when you have few labels or open-ended outputs.",
        topic="genai-lens", level=3),
    tf("Because an LLM with sampling turned on can answer the same prompt differently each time, one passing run of an eval case is weaker evidence than one passing run of a deterministic unit test.", True,
       "Would you trust a flaky test that passed once?",
       "Non-deterministic outputs mean you should run cases several times, use temperature 0 where possible, and track pass rates, not single passes.",
       topic="genai-lens", level=3),
    mcq("Before building a RAG system with a re-ranker, query rewriting and agents, what should come first?",
        ["A simple version (basic retrieval + one prompt) plus a small eval set, so every later addition can be measured", "The most advanced pipeline you can find", "Fine-tuning the LLM on the documents", "A dashboard for the final product"], 0,
        "How will you know whether the re-ranker helped?",
        "Same rule as classic ML: baseline first. Without a baseline and evals you can't tell which part adds value and which only adds latency and cost.",
        analogy="Ship the MVP and its tests before the microservices.",
        topic="genai-lens", level=3),

    # ============================================================ more L4
    out("import numpy as np\npreds = np.array([2.0, 4.0, 6.0])   # 3 models trained on 3 samples\ntrue = 5.0\nbias2 = (preds.mean() - true) ** 2\nvar = preds.var()\nmse = ((preds - true) ** 2).mean()\nprint(bias2, round(var, 2), round(mse, 2))",
        ["1.0 2.67 3.67", "1.0 2.67 2.67", "4.0 2.67 6.67", "1.0 4.0 5.0"], 0,
        "Average prediction 4 vs truth 5; then the spread around 4.",
        "Bias^2 = (4 - 5)^2 = 1. Variance = mean of (2-4)^2, 0, (6-4)^2 = 8/3 = 2.67. Average squared error = (9 + 1 + 1)/3 = 3.67 = bias^2 + variance (no noise here). That is the decomposition, made concrete.",
        diagram="""
  2.0      4.0  5.0  6.0
   x--------o----*----x     o = mean prediction
            |<-->|          * = truth
           bias = 1, spread = variance
""",
        topic="generalisation", level=4),
    out("import numpy as np\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.linear_model import LogisticRegression\nX = np.array([[100], [200], [300], [400]]); y = [0, 0, 1, 1]\nsc = StandardScaler().fit(X)\nm = LogisticRegression().fit(sc.transform(X), y)\nq = np.array([[150]])\nprint(m.predict(sc.transform(q))[0], m.predict(q)[0])",
        ["0 1", "0 0", "1 1", "1 0"], 0,
        "The second call skips the scaler the model was trained with.",
        "Training saw scaled inputs (150 becomes about -0.9, class 0). The serving call passes the raw 150, which looks huge, so it flips to class 1. This is training-serving skew in two lines, and why preprocessing must ship inside the model pipeline.",
        topic="train-infer", level=4),
    mcq("A bank trains a default model on past loans. It only has outcomes (repaid or defaulted) for applicants it APPROVED. What is the subtle problem?",
        ["Selection bias: the model never sees outcomes for the kind of people the old policy rejected, so its scores for them are guesses", "Too much data", "Defaults should be predicted with clustering", "There is no problem if the test set is large"], 0,
        "Whose labels are missing, and were they missing at random?",
        "The labels exist only where the old decision said yes. The model learns about approved-looking applicants and can be badly wrong elsewhere. Teams fix this with small controlled approvals (exploration), reject inference or careful policy limits.",
        diagram="""
applicants -> old policy -+-> approved -> outcome known
                          +-> rejected -> NEVER seen
model trains only on the top branch
""",
        topic="framing", level=4),
    mcq("Your model's validation error stopped improving and now matches the rate at which two human experts disagree on the same cases. Best next step?",
        ["Look for new informative features or cleaner labels; a bigger model mostly can't beat this noise floor", "Train a much bigger model", "Train for 10x more epochs", "Remove the validation set"], 0,
        "Some error comes from the data itself, not the model.",
        "If identical-looking cases have different labels, that is irreducible error given these features. Only new information (features) or cleaner labels lower it; more capacity just fits the noise.",
        diagram="""
error
 | \\
 |  \\___________  <- plateau = noise floor
 |                  (experts disagree here too)
 +----------------- model size / epochs
""",
        topic="generalisation", level=4),
    mcq("Vision transformers have weaker built-in assumptions about images than CNNs (no built-in locality or translation sharing). What is the practical consequence?",
        ["They usually need far more training data (or big pre-training) to match CNNs, but can surpass them at large scale", "They can never match CNNs on images", "They need less data because they assume less", "Inductive bias has no effect on data needs"], 0,
        "Assumptions are a substitute for data.",
        "A strong, correct inductive bias lets a model learn from less data. Weaker bias means the model must learn those regularities from examples, which costs data but leaves room to learn things the bias would have ruled out.",
        diagram="""
data needed
 high |            ViT (weak bias)
      |   CNN (strong bias)
 low  +--------------------------
       assumptions built in: few -> many
""",
        topic="inductive-bias", level=4),
    tf("Flipping and cropping training images (data augmentation) is a way to give a model an inductive bias, such as 'a flipped cat is still a cat', through the data instead of the architecture.", True,
       "What assumption does each flipped copy teach?",
       "Augmentation encodes invariances you believe are true. It is also where the bias can be wrong: flipping images of text produces mirror writing, and rotating a 6 turns it into a 9.",
       topic="inductive-bias", level=4),
    mcq("Which statement about an RBF-kernel SVM is most accurate?",
        ["It stores support vectors, whose number tends to grow with the training data, so it behaves like a non-parametric model", "It is parametric, because it has hyperparameters C and gamma", "It has no learned values", "It always stores exactly d+1 numbers"], 0,
        "What does the fitted model keep in order to predict?",
        "A kernel SVM predicts by comparing new points to stored training points (the support vectors). Model size depends on the data, not just the number of features. Hyperparameters don't decide whether a model is parametric.",
        topic="parametric", level=4),
    mcq("A RAG system combines an LLM with a searchable index of company documents. In parametric/non-parametric terms, which description is right?",
        ["The LLM's weights are parametric memory (fixed size); the document index is non-parametric memory that grows as you add documents", "Both are parametric", "Both are non-parametric", "The index is parametric because it has embeddings"], 0,
        "Which part gets bigger when you add 10,000 new documents?",
        "This is the framing used in the original RAG paper. Knowledge baked into weights needs retraining to change; knowledge in the index can be added, fixed or deleted by editing data.",
        analogy="Weights are constants compiled into the binary; the index is a database you can update at runtime.",
        diagram="""
query --> [index: grows with docs] --> top passages
                                          |
             [LLM weights: fixed] <-------+
                    |
                  answer
""",
        topic="parametric", level=4),
    mcq("Which statement about parameter count and model capacity (how complex a pattern a model can fit) is correct?",
        ["Parameter count is only a rough guide: a model like y = sin(w*x) has one parameter yet can fit very wiggly data", "More parameters always means more capacity, exactly", "Capacity depends only on the training data size", "A model with fewer parameters can never overfit"], 0,
        "Can one number make a curve wiggle a lot?",
        "Capacity depends on how parameters are used, not just how many. Regularisation, architecture and training time also change effective capacity, which is why a huge regularised network can generalise well.",
        diagram="""
y = sin(w * x),  ONE parameter w
w small:  ~~~~          (smooth)
w large:  /\\/\\/\\/\\/\\/\\    (wiggly, fits almost anything)
""",
        topic="params-hyper", level=4),
    mcq("A chat product has thumbs-up/thumbs-down buttons and a 'memory' feature. A user says 'it learned my name instantly'. What is really happening?",
        ["Memory is stored text added to future prompts; feedback is logged and may be used in a later offline training run; the served weights don't change per chat", "Each thumbs-up runs gradient descent on the live model", "The model retrains after every message", "The user's browser trains a local copy"], 0,
        "Where could 'your name' live without touching the weights?",
        "Updating a giant model per user message would be slow, costly and unsafe. Products store facts as context and collect feedback for future versions. Weights change only when a new model version is trained and deployed.",
        topic="train-infer", level=4),
    mcq("A loan default model's true labels arrive 90 days after each prediction. How do you catch problems in the meantime?",
        ["Monitor input feature distributions and the prediction score distribution for drift, plus any early proxy labels (e.g. first missed payment)", "Wait 90 days; nothing can be checked earlier", "Check the training accuracy daily", "Retrain every hour on unlabelled data"], 0,
        "What can you observe on day 1 without the label?",
        "Delayed labels are common (fraud, churn, credit). Input and output drift are early warning signals; proxy labels give earlier, noisier feedback. Real accuracy is checked once labels mature.",
        diagram="""
day 0 predict -- day 1..89: drift, proxies -- day 90 label
      |              (early warnings)            |
      +--------------- real accuracy ------------+
""",
        topic="workflow", level=4),
    mcq("You retrain last month's model with the same script and get noticeably different results. To make training reproducible, what must be versioned?",
        ["The exact data snapshot, code, hyperparameters, random seeds and library versions", "Only the code in git", "Only the final model file", "Only the hyperparameters"], 0,
        "A model is code + data + config + environment.",
        "Unlike a normal build, the 'source' of a model includes the data. If the training table changed or a library update changed defaults, the same code produces a different model.",
        analogy="Like a build that needs the lockfile and the exact input assets, not just the source code.",
        topic="workflow", level=4),
    mcq("A team adds one new feature to a production model. Accuracy goes up overall, but a downstream fraud rule that used the model's score threshold starts firing far too often. What ML maintenance issue is this?",
        ["Entanglement (changing anything changes everything): the score's meaning shifted, and hidden consumers depended on it", "Underfitting", "Exploration vs exploitation", "Catastrophic forgetting"], 0,
        "Who else was reading the model's output?",
        "In ML, inputs are not independent: one change shifts all weights and the score distribution. Undeclared consumers of the score then break. Version model outputs, document consumers and re-calibrate thresholds on each release.",
        analogy="Like changing a shared global variable that half the codebase silently reads.",
        diagram="""
new feature --> model --> score dist shifts
                             |
          fraud rule (score > 0.8) fires 5x more
""",
        topic="when-not-ml", level=4),
    tf("An LLM 'agent' that calls tools in a loop to finish a task is a reinforcement-learning agent, learning from rewards while it runs.", False,
       "Do the model's weights change between steps of the loop?",
       "Most LLM agents are frozen models plus orchestration code: the 'learning' within a task is just new text in the context. RL may have been used to train the model earlier (e.g. RLHF), but the running agent isn't updating a policy from rewards.",
       topic="ai-ml-dl", level=4),
    mcq("Fraud labels come from chargebacks, which can arrive up to 60 days after a transaction. You build a training set that includes last week's transactions, labelled 'not fraud' if no chargeback exists yet. What goes wrong?",
        ["Recent rows are falsely labelled 'not fraud' because their labels haven't matured; exclude them or wait for the label window to close", "Nothing; recent data is always the most valuable", "The model will overfit to old fraud", "It turns into an unsupervised problem"], 0,
        "Has last week's fraud had time to show up?",
        "Label maturity: a missing chargeback isn't proof of no fraud yet. Training on immature labels teaches the model that recent fraud patterns are safe, exactly the ones you most need to catch.",
        diagram="""
txn date:  -90d ........ -60d ..... -7d  today
labels:    [   mature, trustworthy   ][ still open ]
train on:  <------------------------>   exclude
""",
        topic="framing", level=4),
    mcq("You use an LLM to grade your chatbot's answers ('LLM-as-judge'). Which risk is real and how do you handle it?",
        ["The judge has biases (prefers longer answers, the first option shown, or its own style); check its grades against a human-labelled sample and randomise order", "LLM judges are always objective, so no checks are needed", "The judge's weights get updated by grading", "LLM judges can only grade code"], 0,
        "A judge is also a model, with its own errors.",
        "An automated judge is a measuring instrument; you calibrate it. Measure agreement with human labels, swap answer positions, and keep a small human-reviewed set as ground truth.",
        topic="genai-lens", level=4),
    mcq("A model scores 95% on a famous public benchmark but only 60% on your company's internal test cases of the same kind. What are the two most likely explanations?",
        ["The benchmark leaked into its pre-training data (contamination), and your cases come from a different distribution than the benchmark", "Your test cases must be labelled wrong", "The model is underfitting the benchmark", "Benchmarks are always harder than real tasks"], 0,
        "Has the model maybe already seen the benchmark answers? Does the benchmark look like your data?",
        "Public test sets end up in web-scraped training data, inflating scores. And a benchmark is only a proxy for your task. This is why teams build their own eval sets from real traffic.",
        topic="genai-lens", level=4),
]
