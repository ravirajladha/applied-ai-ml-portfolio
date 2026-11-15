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
