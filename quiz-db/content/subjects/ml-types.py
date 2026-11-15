from helpers import mcq, tf, out, fill

SUBJECT = "ml-types"

TOPICS = [
    ("supervised", "Supervised: classification and regression"),
    ("unsupervised", "Unsupervised: clustering, dimensionality reduction, anomaly detection"),
    ("semi-self", "Semi-supervised and self-supervised"),
    ("rl", "Reinforcement learning"),
    ("online-batch", "Online vs batch learning"),
    ("transfer", "Transfer learning and fine-tuning"),
    ("gen-disc", "Generative vs discriminative models"),
    ("scenarios", "Picking the learning type for a scenario"),
]

QUESTIONS = [
    # ------------------------------------------------------------------ L1
    mcq("'Supervised' learning gets its name because:",
        ["Each training example comes with the correct answer, like a teacher marking work", "A human watches the model train", "The model is checked by a supervisor program", "It only works in supervised environments"], 0,
        "What extra column does supervised data have?",
        "Supervised data has labels: the right answer for each example. The model learns to map inputs to those answers.",
        topic="supervised", level=1),
    mcq("Which of these is a CLASSIFICATION task?",
        ["Deciding if an X-ray shows pneumonia: yes or no", "Predicting a flat's rent in rupees", "Estimating a delivery time in minutes", "Forecasting next month's revenue"], 0,
        "Classification picks from a fixed set of categories.",
        "Yes/no is a category. Rent, minutes and revenue are numbers, so those are regression.",
        topic="supervised", level=1),
    tf("Predicting a customer's age in years from their purchases is a regression task.", True,
       "Is the output a category or a number?",
       "Age is a number on a continuous scale, so it's regression.",
       topic="supervised", level=1),
    mcq("Sorting emails into 'Primary', 'Social' or 'Promotions' (exactly one each) is:",
        ["Multiclass classification", "Binary classification", "Regression", "Clustering"], 0,
        "How many possible categories, and how many per email?",
        "More than two classes, exactly one per example = multiclass.",
        topic="supervised", level=1),
    mcq("In unsupervised learning, the training data has:",
        ["No labels: the model has to find structure by itself", "Labels for every row", "Rewards for every action", "Only images"], 0,
        "'Un'-supervised: no teacher.",
        "There are no correct answers given. The model looks for groups, patterns or compressed representations.",
        topic="unsupervised", level=1),
    mcq("A bank wants to flag card transactions that look very unusual compared with normal ones, without having labelled fraud examples. This is:",
        ["Anomaly detection (usually unsupervised)", "Regression", "Reinforcement learning", "Multiclass classification"], 0,
        "It's about finding the odd ones out.",
        "Anomaly detection learns what 'normal' looks like and flags points that don't fit; it doesn't need labelled anomalies.",
        topic="unsupervised", level=1),
    mcq("In reinforcement learning, what is the 'reward'?",
        ["A number the environment gives the agent saying how good its last action was", "The correct label for each example", "The model's accuracy on the test set", "The learning rate"], 0,
        "Think of points in a video game.",
        "The reward is a score signal from the environment. The agent learns actions that collect more reward over time.",
        diagram="""
        action
 Agent ---------> Environment
   ^                  |
   +-- state, reward -+
""",
        topic="rl", level=1),
    mcq("In reinforcement learning, the 'policy' is:",
        ["The agent's strategy: which action to take in each situation", "The reward the environment gives", "The list of all states", "The training dataset"], 0,
        "It's what the agent is trying to improve.",
        "A policy maps state -> action. RL is about learning a good policy.",
        analogy="Like a request router: given the current state, decide what to do next.",
        topic="rl", level=1),
    mcq("A model that is updated a little bit every time a new data point arrives is doing:",
        ["Online learning", "Batch learning", "Transfer learning", "Unsupervised learning"], 0,
        "It learns continuously, piece by piece.",
        "Online (incremental) learning updates as data streams in. Batch learning retrains on the whole dataset at once.",
        topic="online-batch", level=1),
    tf("'Online learning' means the model is served behind a web API.", False,
       "It's about how the model learns, not where it runs.",
       "Online learning = updating the model incrementally as new data arrives. A batch-trained model served via an API is still batch learning.",
       topic="online-batch", level=1),
    mcq("Transfer learning means:",
        ["Starting from a model already trained on a big task and adapting it to your task", "Copying data from one server to another", "Moving a model from Python to Java", "Training two models at the same time"], 0,
        "Reuse what was already learned.",
        "A pretrained model already knows general patterns (edges, words). You adapt it with a little data instead of training from zero.",
        analogy="Like forking a mature open-source library instead of writing one from scratch.",
        topic="transfer", level=1),
    mcq("Which model can CREATE new examples, like brand-new images of faces?",
        ["A generative model", "A discriminative classifier", "A linear regression", "A decision tree classifier"], 0,
        "One family 'generates'.",
        "Generative models learn what the data looks like, so they can sample new data. Discriminative models only separate classes.",
        topic="gen-disc", level=1),
    mcq("A music app learns your taste from songs you skipped or replayed and has no explicit ratings. Each song is labelled 'liked' if replayed. Predicting 'will they like this new song?' is:",
        ["Supervised binary classification", "Regression", "Clustering", "Dimensionality reduction"], 0,
        "There is a yes/no label for each past song.",
        "Replays give a label (liked or not) per song, so it's supervised, with two classes.",
        topic="scenarios", level=1),
    mcq("A robot vacuum learns which routes clean the room fastest by trying routes and getting a score for each run. This is:",
        ["Reinforcement learning", "Supervised learning", "Clustering", "Transfer learning"], 0,
        "Trial and error with a score.",
        "The robot acts, gets feedback (time, coverage), and improves its route-picking policy: RL.",
        topic="scenarios", level=1),
    tf("Grouping news articles by topic without knowing the topics in advance is unsupervised learning.", True,
       "Are topic labels given?",
       "No labels are given; the model groups similar articles (clustering or topic modelling).",
       topic="scenarios", level=1),
    tf("Self-supervised learning needs humans to label every example.", False,
       "Where do the labels come from in 'self'-supervised?",
       "The labels are created automatically from the data itself, e.g. hide a word and predict it.",
       topic="semi-self", level=1),
    fill("Classification with exactly two possible classes (like spam / not spam) is called ____ classification.",
         "binary",
         "Two = bi-.",
         "Binary = two classes. More than two (one per example) is multiclass.",
         topic="supervised", level=1),

    # ------------------------------------------------------------------ L2
    out("""from sklearn.utils.multiclass import type_of_target
print(type_of_target([0, 1, 1, 0]))
print(type_of_target([0, 1, 2, 1]))
print(type_of_target([1.5, 2.25, 3.0]))""",
        ["binary\nmulticlass\ncontinuous", "binary\nbinary\ncontinuous", "multiclass\nmulticlass\nmulticlass", "binary\nmulticlass\nmulticlass"], 0,
        "sklearn looks at the label values to guess the task.",
        "Two distinct values = binary, more distinct integers = multiclass, non-integer floats = continuous (regression).",
        topic="supervised", level=2),
    out("""from sklearn.utils.multiclass import type_of_target
print(type_of_target([[1, 0, 1], [0, 1, 1], [1, 0, 0]]))""",
        ["multilabel-indicator", "multiclass", "binary", "multiclass-multioutput"], 0,
        "Each row can have several 1s.",
        "A 0/1 matrix where each row can have more than one 1 is a multilabel target ('multilabel-indicator').",
        topic="supervised", level=2),
    mcq("A movie can be tagged 'action', 'comedy' and 'romance' at the same time. Predicting its tags is:",
        ["Multilabel classification", "Multiclass classification", "Binary classification", "Regression"], 0,
        "How many labels can one movie have?",
        "Several labels can be on at once = multilabel. Multiclass means exactly one class per example.",
        diagram="""
            action comedy romance
 multiclass:   0      1      0     (exactly one 1)
 multilabel:   1      1      0     (any number of 1s)
""",
        topic="supervised", level=2),
    out("""from sklearn.preprocessing import MultiLabelBinarizer
mlb = MultiLabelBinarizer()
Y = mlb.fit_transform([["action", "comedy"], ["drama"], ["action"]])
print(Y.shape, list(mlb.classes_))""",
        ["(3, 3) ['action', 'comedy', 'drama']", "(3, 2) ['action', 'comedy']", "(3, 1) ['action']", "(4, 3) ['action', 'comedy', 'drama']"], 0,
        "One row per movie, one column per distinct tag.",
        "3 movies x 3 distinct tags (sorted alphabetically). Each row has a 1 for every tag the movie has.",
        topic="supervised", level=2),
    out("""import numpy as np
from sklearn.decomposition import PCA
rng = np.random.default_rng(0)
X = rng.normal(size=(100, 10))
Z = PCA(n_components=2).fit_transform(X)
print(Z.shape)""",
        ["(100, 2)", "(2, 10)", "(10, 2)", "(100, 10)"], 0,
        "Rows stay, columns are compressed.",
        "PCA keeps every row and squeezes the 10 features down to 2 new ones: shape (100, 2).",
        topic="unsupervised", level=2),
    out("""import numpy as np
from sklearn.cluster import KMeans
X = np.array([[1, 1], [1, 2], [2, 1], [10, 10], [10, 11], [11, 10]])
km = KMeans(n_clusters=2, n_init=10, random_state=0).fit(X)
print(sorted(np.bincount(km.labels_).tolist()))""",
        ["[3, 3]", "[2, 4]", "[1, 5]", "[6]"], 0,
        "Look at where the points sit.",
        "Two tight groups of 3 points each, far apart. KMeans finds both; the sizes are 3 and 3.",
        topic="unsupervised", level=2),
    mcq("Which of these is a DIMENSIONALITY REDUCTION task?",
        ["Compressing 300 sensor readings per machine into 10 summary features", "Grouping customers into 5 segments", "Predicting next week's sales", "Flagging a single weird login"], 0,
        "Dimensions = number of features (columns).",
        "Dimensionality reduction (e.g. PCA) reduces the number of features while keeping most of the information.",
        topic="unsupervised", level=2),
    out("""tokens = "the cat sat on the mat".split()
pairs = list(zip(tokens[:-1], tokens[1:]))
print(len(pairs), pairs[0])""",
        ["5 ('the', 'cat')", "6 ('the', 'cat')", "5 ('cat', 'sat')", "6 ('the', 'the')"], 0,
        "Each word is paired with the word that follows it.",
        "6 tokens give 5 (input, next-word) pairs. This is exactly how next-token training data is made: the text labels itself.",
        topic="semi-self", level=2),
    mcq("A company has 1,000 labelled support tickets and 500,000 unlabelled ones. Using both together to train a classifier is called:",
        ["Semi-supervised learning", "Unsupervised learning", "Reinforcement learning", "Online learning"], 0,
        "A small labelled set plus a large unlabelled set.",
        "Semi-supervised learning uses a few labels plus lots of unlabelled data (e.g. pseudo-labelling, label propagation).",
        topic="semi-self", level=2),
    mcq("In RL, 'exploration vs exploitation' means choosing between:",
        ["Trying actions you're unsure about to learn more, vs using the action you currently think is best", "Training vs testing", "Using a GPU vs a CPU", "Big vs small rewards"], 0,
        "Your favourite restaurant vs a new one.",
        "Exploitation earns reward now; exploration gathers information that may earn more later. Good agents balance both.",
        analogy="Always ordering your usual dish vs occasionally trying something new on the menu.",
        topic="rl", level=2),
    tf("An RL agent that always picks the action with the highest estimated value (never exploring) is guaranteed to find the best policy.", False,
       "What if its first estimates are wrong?",
       "Pure exploitation can lock onto a mediocre action early and never try the one that is actually better.",
       topic="rl", level=2),
    out("""import numpy as np
from sklearn.linear_model import SGDClassifier
rng = np.random.default_rng(0)
clf = SGDClassifier(random_state=0)
for day in range(3):
    X = rng.normal(size=(50, 4)); y = (X[:, 0] > 0).astype(int)
    clf.partial_fit(X, y, classes=[0, 1])
print(clf.coef_.shape, clf.classes_.tolist())""",
        ["(1, 4) [0, 1]", "(4,) [0, 1]", "(3, 4) [0, 1]", "(2, 4) [0, 1]"], 0,
        "Binary linear classifiers keep one row of weights.",
        "partial_fit updates the same model with each new batch (online learning). A binary linear model has one weight row: shape (1, 4).",
        topic="online-batch", level=2),
    mcq("When you fine-tune a pretrained image model for a new task with little data, a common first step is:",
        ["Freeze the pretrained layers and train only a new final layer (the 'head')", "Re-initialise all weights randomly", "Delete the pretrained layers", "Train only the first layer"], 0,
        "Keep the general knowledge, learn the task-specific part.",
        "The backbone already extracts useful features. Training only a small head needs little data and is fast.",
        diagram="""
 [pretrained backbone: frozen] -> [new head: trained]
   edges, shapes, textures         your 5 classes
""",
        topic="transfer", level=2),
    mcq("Which pair is (generative, discriminative)?",
        ["(Naive Bayes, Logistic regression)", "(Logistic regression, Naive Bayes)", "(Decision tree, SVM)", "(Linear regression, kNN)"], 0,
        "One models how the features are produced for each class.",
        "Naive Bayes models p(x | y) and p(y), i.e. how data is generated per class. Logistic regression models p(y | x) directly.",
        topic="gen-disc", level=2),
    tf("Generative models are only useful for creating images or text; they can't classify.", False,
       "Naive Bayes is generative.",
       "Generative models can classify by using Bayes' rule: pick the class y that makes x most likely. Naive Bayes is a classic spam classifier.",
       topic="gen-disc", level=2),
    mcq("An app predicts a user's star rating (1 to 5) for a restaurant. Which statement is most accurate?",
        ["It can be framed as regression or classification; regression respects that 4 is closer to 5 than 1 is", "It must be multiclass classification because the values are integers", "It must be binary classification", "It is unsupervised"], 0,
        "Is there an order between the classes?",
        "Ratings are ordered numbers. Plain multiclass treats 1-vs-5 the same as 4-vs-5; regression (or ordinal methods) keeps the order.",
        topic="scenarios", level=2),
    mcq("A warehouse wants to predict how many minutes each order will take to pack, from past orders with recorded packing times. This is:",
        ["Supervised regression", "Supervised classification", "Clustering", "Reinforcement learning"], 0,
        "Labelled? And is the output a number?",
        "Past orders have the true time (label) and the output is a number, so supervised regression.",
        topic="scenarios", level=2),

    # ------------------------------------------------------------------ L3
    out("""from sklearn.utils.multiclass import type_of_target
print(type_of_target([1, 2, 3, 4, 5, 3]))
print(type_of_target([1.0, 2.0, 3.0]))""",
        ["multiclass\nmulticlass", "continuous\ncontinuous", "multiclass\ncontinuous", "binary\nmulticlass"], 0,
        "sklearn checks whether float values are whole numbers.",
        "Integer-valued targets look like class labels to sklearn, even as floats. A rating stored as 1..5 is treated as multiclass unless you choose a regressor yourself.",
        topic="supervised", level=3),
    mcq("For a multilabel problem with 20 tags, one simple approach is:",
        ["Train one binary classifier per tag (one-vs-rest)", "Train one multiclass classifier with softmax over 20 tags", "Use KMeans with 20 clusters", "Use linear regression on the tag IDs"], 0,
        "Each tag is an independent yes/no question.",
        "Multilabel = 20 yes/no decisions per item. Softmax forces exactly one label, which is wrong here; sigmoid per tag (or one-vs-rest) fits.",
        topic="supervised", level=3),
    mcq("You run KMeans twice with different random seeds on the same data. Run A calls the 'big spenders' cluster 0; run B calls them cluster 2. What does this mean?",
        ["Nothing: cluster numbers are arbitrary names, only the grouping matters", "Run B is wrong", "The data changed", "KMeans is broken"], 0,
        "Did anyone tell KMeans what 'cluster 0' means?",
        "Cluster IDs are just labels assigned in whatever order the algorithm finds them. Compare groupings, not IDs.",
        topic="unsupervised", level=3),
    out("""import numpy as np
from sklearn.ensemble import IsolationForest
rng = np.random.default_rng(0)
X = np.vstack([rng.normal(0, 1, size=(200, 2)), [[8, 8], [-9, 7]]])
pred = IsolationForest(random_state=0).fit(X).predict(X)
print(np.unique(pred), pred[-2:])""",
        ["[-1  1] [-1 -1]", "[0 1] [1 1]", "[0 1] [0 0]", "[-1  1] [1 1]"], 0,
        "sklearn outlier detectors don't use 0/1.",
        "IsolationForest predicts 1 for inliers and -1 for outliers. The two far-away points are flagged -1, with no labels used.",
        topic="unsupervised", level=3),
    out("""import numpy as np
from sklearn.semi_supervised import LabelPropagation
X = np.array([[0.0], [0.2], [0.4], [5.0], [5.2], [5.4]])
y = np.array([0, -1, -1, 1, -1, -1])
m = LabelPropagation().fit(X, y)
print(m.transduction_)""",
        ["[0 0 0 1 1 1]", "[0 -1 -1 1 -1 -1]", "[0 1 0 1 0 1]", "[0 0 0 0 0 0]"], 0,
        "In sklearn, -1 marks an unlabelled row.",
        "Labels spread to nearby unlabelled points, so each cluster takes the label of its one labelled member. That's semi-supervised learning.",
        topic="semi-self", level=3),
    mcq("BERT is pre-trained by hiding some words and predicting them; GPT by predicting the next word. Both are:",
        ["Self-supervised objectives: the hidden word is the label, taken from the text itself", "Supervised with human labels", "Reinforcement learning", "Clustering"], 0,
        "Who provides the 'correct' word?",
        "Masked-language modelling (BERT) and next-token prediction (GPT) both make labels from raw text, so no human labelling is needed.",
        topic="semi-self", level=3),
    mcq("In contrastive self-supervised learning (e.g. SimCLR, CLIP), what is the training signal?",
        ["Make embeddings of two views of the same item close, and of different items far apart", "Predict a human-given class label", "Maximise a game score", "Reconstruct every pixel exactly"], 0,
        "Positive pairs vs negative pairs.",
        "Two crops of one photo (or a photo and its caption) are a positive pair; other items in the batch are negatives. No class labels needed.",
        diagram="""
 view A of cat --\\  pull together
 view B of cat --/
 photo of car  <---- push apart ----> cat
""",
        topic="semi-self", level=3),
    out("""rewards = [1, 1, 1]
gamma = 0.9
G = sum(r * gamma ** t for t, r in enumerate(rewards))
print(round(G, 2))""",
        ["2.71", "3.0", "2.7", "0.73"], 0,
        "Each later reward is multiplied by one more factor of gamma.",
        "Discounted return G = 1 + 0.9*1 + 0.81*1 = 2.71. Discounting makes near rewards count more than far ones.",
        topic="rl", level=3),
    out("""import numpy as np
q = np.array([0.2, 0.5, 0.1])
rng = np.random.default_rng(0)
eps = 0.1
picks = [int(rng.integers(3)) if rng.random() < eps else int(np.argmax(q)) for _ in range(1000)]
print(np.bincount(picks).argmax(), picks.count(1) > 900)""",
        ["1 True", "0 True", "1 False", "2 False"], 0,
        "With probability 0.9 it takes the best-known action.",
        "Epsilon-greedy exploits argmax(q) = 1 about 90% of the time, plus 1/3 of the random 10%, so ~93% of picks are action 1.",
        topic="rl", level=3),
    out("""import numpy as np
from sklearn.linear_model import SGDClassifier
X = np.array([[0.0], [1.0]]); y = np.array([0, 1])
clf = SGDClassifier()
clf.partial_fit(X, y)""",
        ["ValueError", "NotFittedError", "TypeError", "Nothing is printed"], 0,
        "On the very first call, how would it know which classes might appear later?",
        "The first partial_fit call must get classes=[...] because future batches may contain classes not seen yet. Without it sklearn raises ValueError.",
        topic="online-batch", level=3),
    mcq("Which situation most favours online learning over nightly batch retraining?",
        ["Ad click prediction where user behaviour shifts within hours and data arrives as a stream", "A yearly tax-category model with stable data", "A one-off research analysis", "An image classifier trained on a fixed dataset"], 0,
        "How fast does the pattern change?",
        "Online learning shines when data streams in and the pattern drifts quickly. Stable data is easier to manage with batch retraining.",
        topic="online-batch", level=3),
    out("""import torch.nn as nn
backbone = nn.Linear(100, 50)
head = nn.Linear(50, 3)
for p in backbone.parameters():
    p.requires_grad = False
model = nn.Sequential(backbone, head)
print(sum(p.numel() for p in model.parameters() if p.requires_grad))""",
        ["153", "5203", "5050", "150"], 0,
        "Only the head is trainable: weights plus biases.",
        "The head has 50*3 weights + 3 biases = 153 trainable numbers; the frozen backbone's 5050 are not updated.",
        topic="transfer", level=3),
    mcq("You have 200 labelled X-rays and a model pretrained on ImageNet. What's the usual best plan?",
        ["Freeze most of the backbone, train the head, then optionally unfreeze the top layers with a small learning rate", "Unfreeze everything and train with a large learning rate", "Train a new network from scratch on the 200 images", "Skip training and use ImageNet labels"], 0,
        "With little data, how many weights should you let move?",
        "Small data + many trainable weights = overfitting. Train few weights first, then carefully unfreeze more if it helps.",
        topic="transfer", level=3),
    mcq("A discriminative model learns ____, while a generative model learns ____.",
        ["p(y | x); p(x, y) (or p(x | y) with p(y))", "p(x, y); p(y | x)", "p(x); p(y)", "rewards; policies"], 0,
        "Discriminative = 'given the input, which class?'.",
        "Discriminative models model the boundary p(y | x). Generative models model how the data is produced, p(x, y), so they can also sample x.",
        topic="gen-disc", level=3),
    out("""import numpy as np
from sklearn.naive_bayes import GaussianNB
X = np.array([[1.0], [1.2], [0.8], [5.0], [5.2], [4.8], [5.1], [4.9]])
y = np.array([0, 0, 0, 1, 1, 1, 1, 1])
nb = GaussianNB().fit(X, y)
print(nb.class_prior_, nb.predict([[3.5]]))""",
        ["[0.375 0.625] [1]", "[0.5 0.5] [0]", "[0.375 0.625] [0]", "[3 5] [1]"], 0,
        "A generative classifier learns p(y) and p(x | y) for each class.",
        "GaussianNB stores class priors (3/8, 5/8) and a Gaussian per class. 3.5 is closer to class 1's mean (5.0) than class 0's (1.0), so it predicts 1.",
        topic="gen-disc", level=3),
    mcq("A bank wants to (1) group customers into segments, then (2) predict, for each segment, who will take a loan offer using past offer outcomes. Which types are used?",
        ["(1) unsupervised clustering, (2) supervised classification", "(1) supervised regression, (2) clustering", "Both reinforcement learning", "Both unsupervised"], 0,
        "Which step has labels?",
        "Segments have no labels (clustering). Past offers have yes/no outcomes, so predicting acceptance is supervised classification.",
        topic="scenarios", level=3),

    # ------------------------------------------------------------------ L4
    mcq("A team bins house prices into 'low/medium/high' and trains a classifier instead of a regressor. What is the main cost?",
        ["Information is lost: a price just above a bin edge and one far above are treated the same, and the order of bins is ignored by plain multiclass loss", "Classifiers can't handle three classes", "It always improves accuracy, so there is no cost", "Regression can't predict prices"], 0,
        "What happens to the exact number and to the order of the bins?",
        "Binning discards within-bin detail and, with standard cross-entropy, treats 'low vs high' as no worse than 'low vs medium'. Do it only if the decision really is categorical.",
        topic="supervised", level=4),
    tf("If you run KMeans with n_clusters=5 on purely random uniform noise, it will still return 5 clusters.", True,
       "Does KMeans check whether real groups exist?",
       "KMeans always partitions data into exactly k groups, even if no structure exists. Use silhouette scores, stability checks or domain sense before trusting clusters.",
       code="""import numpy as np
from sklearn.cluster import KMeans
X = np.random.default_rng(0).uniform(size=(300, 2))
print(len(set(KMeans(n_clusters=5, n_init=10, random_state=0).fit_predict(X).tolist())))""",
       topic="unsupervised", level=4),
    mcq("You have no labels but must report whether a clustering is 'good'. Which is the most defensible approach?",
        ["Internal metrics (e.g. silhouette) plus checking whether clusters are stable across seeds and useful for the business decision", "Report accuracy against the cluster IDs", "Pick k with the lowest inertia, since lower is always better", "Assume the clusters are correct"], 0,
        "Inertia always decreases as k grows.",
        "Without labels there's no accuracy. Inertia keeps falling with k, so it can't pick k alone. Combine silhouette/elbow, stability and usefulness.",
        topic="unsupervised", level=4),
    mcq("Why did self-supervised pre-training make large language models possible?",
        ["Labels are free: every position in any text is a training example, so you can use trillions of tokens without human labelling", "It needs less compute than supervised learning", "It doesn't need neural networks", "It guarantees the model is truthful"], 0,
        "What's the bottleneck in supervised learning?",
        "Human labels are slow and expensive. Next-token prediction turns raw text into unlimited labelled examples, which is what lets models scale.",
        topic="semi-self", level=4),
    mcq("In self-training (pseudo-labelling), a model labels unlabelled data with its own confident predictions and retrains on them. What is the main risk?",
        ["Confirmation bias: early mistakes get labelled as truth and reinforced", "It needs more labelled data than supervised learning", "It can only be used for regression", "It makes the model forget its classes"], 0,
        "What if the model is confidently wrong?",
        "Wrong pseudo-labels are fed back as training data, so errors compound. Use high confidence thresholds and keep a clean labelled validation set.",
        topic="semi-self", level=4),
    mcq("Why is RL not just 'supervised learning with the reward as the label'?",
        ["No correct action is given, rewards can come many steps later, and the agent's own actions decide what data it sees", "RL never uses neural networks", "Rewards are always 0 or 1", "Supervised learning can't use numbers as labels"], 0,
        "Think about a chess move that only pays off 30 moves later.",
        "RL has delayed credit assignment, no target action, and non-i.i.d. data the agent collects itself. Those are exactly what supervised learning assumes away.",
        topic="rl", level=4),
    mcq("An RL agent in a boat-racing game learns to spin in circles hitting the same reward targets forever instead of finishing the race. This is:",
        ["Reward hacking: the agent maximised the reward as written, not the intended goal", "Underfitting", "Catastrophic forgetting", "Too much exploration"], 0,
        "The agent did exactly what the reward said.",
        "Agents exploit any gap between the reward function and the real goal. Reward design and human checks matter; RLHF faces the same risk with learned reward models.",
        topic="rl", level=4),
    mcq("In the usual LLM training recipe, which order is correct?",
        ["Self-supervised pre-training -> supervised fine-tuning on instructions -> RL from human preference feedback", "RL first -> pre-training -> fine-tuning", "Supervised fine-tuning -> self-supervised pre-training -> clustering", "Only RL from the start"], 0,
        "Start with the cheapest, largest data.",
        "Pre-training on raw text builds general knowledge; supervised fine-tuning teaches the instruction format; RLHF (or DPO-style methods) aligns answers with human preferences.",
        topic="scenarios", level=4),
    mcq("An online-learning fraud model updates from every flagged transaction. Attackers send many small, harmless-looking transactions labelled 'legit' to shift it. What is this risk called?",
        ["Data poisoning", "Underfitting", "Training-serving skew", "Exploration"], 0,
        "The attacker controls part of the training stream.",
        "Online learners trust incoming data immediately, so adversaries can steer them. Mitigate with rate limits, delayed/validated updates and monitoring.",
        topic="online-batch", level=4),
    tf("Continually updating a neural network only on the newest data can make it lose skills learned from older data.", True,
       "What happens to old knowledge when every update targets new data?",
       "This is catastrophic forgetting. Replay buffers, regularisation towards old weights, or periodic full retrains are common fixes.",
       topic="online-batch", level=4),
    mcq("Fine-tuning a model pretrained on everyday photos makes it WORSE than a small model trained from scratch on satellite radar images. The most likely reason is:",
        ["Negative transfer: the source domain is too different, so pretrained features mislead", "Pretrained models can never be fine-tuned", "The learning rate was 0", "Radar images have no labels"], 0,
        "Transfer helps when the source and target share structure.",
        "If the domains differ a lot, pretrained features can hurt. Check a from-scratch baseline and consider domain-specific pretraining.",
        topic="transfer", level=4),
    mcq("Which statement about generative vs discriminative classifiers is most accurate?",
        ["Generative models (e.g. Naive Bayes) often do better with very little data; discriminative models (e.g. logistic regression) usually win as data grows", "Discriminative models always win", "Generative models can't output probabilities", "Generative models need labels for p(x) but discriminative ones don't"], 0,
        "A classic Ng & Jordan result compared Naive Bayes and logistic regression.",
        "Generative models make strong assumptions that help with small data; discriminative models target p(y|x) directly and have lower error asymptotically.",
        topic="gen-disc", level=4),
    mcq("You use an LLM (a generative model) to label support tickets by prompting 'Answer with one of: billing, bug, other'. How should you think about this?",
        ["A generative model being used as a discriminative classifier; evaluate it like any classifier with a labelled test set", "It's unsupervised, so no evaluation is possible", "It's reinforcement learning", "Generative models can't classify, so this won't work"], 0,
        "The output is a class label.",
        "However it works inside, the task is classification. Measure precision/recall per class on labelled examples, exactly as for any classifier.",
        topic="gen-disc", level=4),
    fill("In reinforcement learning, the factor (usually written as gamma, between 0 and 1) that makes future rewards count less is called the ____ factor.",
         "discount",
         "It discounts the future.",
         "The discount factor gamma weights a reward t steps away by gamma^t. gamma near 0 = short-sighted; near 1 = far-sighted.",
         topic="rl", level=3),
    fill("In scikit-learn, the method that updates a model with one new batch of data, without retraining from scratch, is ____.",
         "partial_fit",
         "It fits partially.",
         "partial_fit is sklearn's online-learning API (SGDClassifier, MultinomialNB, MiniBatchKMeans...). fit retrains from scratch.",
         topic="online-batch", level=2),
]
