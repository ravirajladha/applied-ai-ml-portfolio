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
        analogy="Like learning with an answer key: every practice question comes with the correct answer to check against.",
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
        analogy="Like sorting a box of mixed LEGO with no instructions: you group pieces by what they look like.",
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
        diagram="""
[pretrained backbone] --> [new head] --> your classes
  (big generic data)      (your small data)
""",
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


TOPICS += [
    ("rlhf", "RLHF and preference tuning (RL for LLMs)"),
    ("label-strategy", "Getting labels: weak supervision and active learning"),
]

QUESTIONS += [
    # ============================================================ more L1
    mcq("A photo app predicts the exact price (in rupees) a used phone will sell for. This is:",
        ["Regression: the output is a number on a scale", "Classification: the output is a category", "Clustering", "Reinforcement learning"], 0,
        "Is the answer a category or an amount?",
        "Prices are continuous numbers, so it's regression. If you only predicted 'cheap / mid / premium', it would become classification.",
        diagram="""
classification:  input --> [cat | dog | bird]
regression:      input --> 18,450.75  (any number)
""",
        topic="supervised", level=1),
    mcq("A shop wants to split its customers into groups with similar shopping habits, but nobody has defined the groups. Which technique fits?",
        ["Clustering", "Regression", "Binary classification", "Reinforcement learning"], 0,
        "No labels, and you want groups.",
        "Clustering (e.g. KMeans) finds groups of similar items without labels. The business then looks at each group and gives it a name like 'weekend bargain hunters'.",
        diagram="""
 spend
   |  o o          x x
   |   o o        x x x     o, x, + = groups found
   |        + + +              without any labels
   +--------------------- visits
""",
        topic="unsupervised", level=1),
    tf("Semi-supervised learning trains one model using a small set of labelled examples together with a much larger set of unlabelled ones.", True,
       "'Semi' = partly labelled.",
       "Labels are expensive, raw data is cheap. Semi-supervised methods use the unlabelled data's structure (which points sit close together) to spread the few labels further.",
       diagram="""
labelled:    A  B            (few, expensive)
unlabelled:  . . . . . . . . . . . . (many, cheap)
model uses both: labels spread to nearby dots
""",
       topic="semi-self", level=1),
    mcq("In reinforcement learning, the 'environment' is:",
        ["The world the agent acts in, which responds with a new situation and a reward", "The computer the code runs on", "The training dataset of correct answers", "The neural network inside the agent"], 0,
        "The agent acts; something reacts.",
        "The agent picks an action, the environment (a game, a robot's room, a market) responds with a new state and a reward. The agent learns from that loop.",
        diagram="""
      action
agent ------> environment
  ^               |
  +-- state, -----+
      reward
""",
        topic="rl", level=1),
    mcq("A model that is retrained from scratch every Sunday night on all the data collected so far is doing:",
        ["Batch (offline) learning", "Online learning", "Reinforcement learning", "Unsupervised learning"], 0,
        "Does it learn continuously, or in one big job?",
        "Batch learning trains on a full dataset in one job and then serves that fixed model until the next job. Online learning would update it as each new example arrives.",
        analogy="Batch learning is a weekly release; online learning is continuous deployment.",
        topic="online-batch", level=1),
    mcq("A startup has only 300 labelled photos of its products. What is usually the fastest way to get a good image classifier?",
        ["Start from a model already trained on millions of images and fine-tune it", "Train a huge model from scratch on the 300 photos", "Use clustering instead", "Label nothing and use reinforcement learning"], 0,
        "Reuse what someone else already learned.",
        "A pretrained model already knows edges, shapes and textures. Fine-tuning it on 300 photos only has to learn your specific classes, which is transfer learning.",
        analogy="Like hiring an experienced developer and teaching them your codebase, instead of teaching someone to code from zero.",
        topic="transfer", level=1),
    mcq("A model that only learns to tell spam from not-spam, without being able to write emails, is called:",
        ["Discriminative", "Generative", "Unsupervised", "Reinforcement"], 0,
        "It discriminates (separates) between classes.",
        "Discriminative models learn the boundary between classes. A generative model would learn what emails look like and could produce new ones.",
        diagram="""
generative:      learns what each class looks like
discriminative:  learns only the line between them
   spam x x x  |  o o o ham
""",
        topic="gen-disc", level=1),
    mcq("After an LLM is pre-trained, people compare pairs of its answers and pick the better one, and the model is tuned to give answers people prefer. This step is often called:",
        ["RLHF: reinforcement learning from human feedback", "Clustering", "Pre-training", "Data augmentation"], 0,
        "The human gives a judgement, not a correct answer to copy.",
        "RLHF turns human preferences into a reward signal and uses RL to make the model's answers more helpful and safe. It comes after pre-training and supervised fine-tuning.",
        topic="rlhf", level=1),
    tf("Labelling data by hand is often the slowest and most expensive part of building a supervised model.", True,
       "Think about paying experts to read 100,000 medical notes.",
       "That is why teams use tricks like labelling only the most useful examples (active learning) or writing rough rules that label data automatically (weak supervision).",
       analogy="Labels are the hand-written test fixtures of ML: valuable, slow to write, and always in short supply.",
       topic="label-strategy", level=1),
    mcq("A phone keyboard suggests the next word as you type, learned from lots of text. Which learning type mostly powers it?",
        ["Self-supervised learning: the text itself supplies the next-word answers", "Reinforcement learning from game scores", "Clustering", "Hand-written rules"], 0,
        "Where do the training answers come from?",
        "Next-word prediction is trained by hiding the next word in real sentences. It's the same idea as LLM pre-training, at a smaller scale.",
        topic="scenarios", level=1),

    # ============================================================ more L2
    out("from sklearn.utils.multiclass import type_of_target\nprint(type_of_target([\"cat\", \"dog\", \"cat\"]), type_of_target([\"a\", \"b\", \"c\"]))",
        ["binary multiclass", "multiclass multiclass", "unknown unknown", "binary binary"], 0,
        "Count the distinct values in each list.",
        "String labels are fine: two distinct values make it binary, three make it multiclass. type_of_target looks at the number and kind of distinct values, not their type.",
        topic="supervised", level=2),
    out("from sklearn.linear_model import LogisticRegression\nLogisticRegression().fit([[1], [2], [3]], [1.5, 2.7, 3.1])",
        ["ValueError", "TypeError", "NotFittedError", "Nothing; it fits fine"], 0,
        "What kind of target is [1.5, 2.7, 3.1]?",
        "A classifier needs discrete classes; sklearn detects a 'continuous' target and raises ValueError ('Unknown label type'). Use a regressor such as LinearRegression for numeric targets.",
        question="What happens when this runs?",
        topic="supervised", level=2),
    out("import numpy as np\nfrom sklearn.decomposition import PCA\na = np.arange(10.0)\nX = np.column_stack([a, 2 * a])\nprint(round(PCA().fit(X).explained_variance_ratio_[0], 2))",
        ["1.0", "0.5", "0.67", "2.0"], 0,
        "The second column is just twice the first.",
        "Both columns move together exactly, so all the variation lies along one direction. The first component explains 100% of the variance; the second explains nothing. Redundant features compress perfectly.",
        topic="unsupervised", level=2),
    out("tokens = \"the cat sat on the mat\".split()\ni = 2\ninputs = tokens[:i] + [\"[MASK]\"] + tokens[i + 1:]\nprint(\" \".join(inputs), \"->\", tokens[i])",
        ["the cat [MASK] on the mat -> sat", "the [MASK] sat on the mat -> cat", "the cat sat [MASK] the mat -> on", "the cat [MASK] on the mat -> [MASK]"], 0,
        "Index 2 is the third token.",
        "This is one masked-language-model training example (BERT style): hide a token and use the original as the label. The data labels itself, so this is self-supervised.",
        topic="semi-self", level=2),
    out("import numpy as np\nQ = [0.0, 0.0]\ncounts = [0, 0]\ntrue_reward = [1.0, 2.0]   # arm 1 is better\nfor t in range(100):\n    a = int(np.argmax(Q))       # always greedy\n    counts[a] += 1\n    Q[a] += (true_reward[a] - Q[a]) / counts[a]\nprint(counts)",
        ["[100, 0]", "[0, 100]", "[50, 50]", "[1, 99]"], 0,
        "On a tie, argmax picks index 0. Then what is Q[0]?",
        "The greedy agent tries arm 0 first (tie), sees reward 1, and now Q[0] = 1 > Q[1] = 0 forever. It never tries the better arm. A little exploration (epsilon-greedy) would find it.",
        question="A greedy agent with two slot-machine arms. What does this print?",
        topic="rl", level=2),
    out("from sklearn.linear_model import LinearRegression, SGDRegressor\nprint(hasattr(LinearRegression(), \"partial_fit\"), hasattr(SGDRegressor(), \"partial_fit\"))",
        ["False True", "True True", "True False", "False False"], 0,
        "Which one is trained step by step with gradient descent?",
        "LinearRegression solves the whole problem at once from all the data, so it has only fit. SGD-based models update in small steps and support partial_fit for online learning.",
        topic="online-batch", level=2),
    tf("In transfer learning, 'freezing' the backbone means its weights are not updated during fine-tuning; only the new head learns.", True,
       "Frozen = doesn't change.",
       "Freezing keeps the general features the backbone learned and trains only the small task-specific head. It's faster, needs less data and reduces overfitting.",
       topic="transfer", level=2),
    mcq("Naive Bayes classifies spam by learning, for each class, how likely each word is. Why is it called a generative model?",
        ["It models how the data (words) is produced for each class, p(x given y), then uses Bayes' rule to classify", "It writes new emails as its main job", "It needs no labels", "It is a neural network"], 0,
        "What does it learn about each class?",
        "Generative = learns how examples of each class are generated, p(x | y) p(y). Classification then comes from Bayes' rule. Logistic regression skips that and learns p(y | x) directly.",
        topic="gen-disc", level=2),
    mcq("In RLHF, why do people compare two answers ('A is better than B') instead of writing the perfect answer for each prompt?",
        ["Judging which answer is better is much faster and more consistent than writing an ideal answer", "Comparisons need no humans at all", "RL can only use yes/no labels", "Writing answers is not allowed"], 0,
        "Think about grading essays vs writing them.",
        "Humans are better at ranking than at producing perfect outputs. Pairwise preferences train a reward model, which then scores many more answers than humans could ever label.",
        analogy="Like code review: it is much easier to say 'version B is better' than to write the perfect version yourself.",
        topic="rlhf", level=2),
    out("import numpy as np\nprobs = np.array([0.98, 0.51, 0.75, 0.03])   # model's P(spam) on unlabelled emails\nprint(int(np.argmin(np.abs(probs - 0.5))))",
        ["1", "0", "3", "2"], 0,
        "Which email is the model least sure about?",
        "Uncertainty sampling, the simplest active-learning rule: send the example closest to 0.5 to a human. Labelling confident cases (0.98, 0.03) teaches the model little.",
        question="Active learning picks which email to send to a human labeller. What does this print?",
        analogy="Like spending QA time on the flaky tests, not the ones that always pass.",
        topic="label-strategy", level=2),

    # ============================================================ more L3
    out("import numpy as np\nfrom sklearn.datasets import load_iris\nfrom sklearn.linear_model import LogisticRegression\nX, y = load_iris(return_X_y=True)\np = LogisticRegression(max_iter=500).fit(X, y).predict_proba(X[:4])\nprint(p.shape, round(p.sum(axis=1)[0], 2))",
        ["(4, 3) 1.0", "(4,) 1.0", "(4, 3) 3.0", "(3, 4) 1.0"], 0,
        "One row per flower, one column per class.",
        "Multiclass: each row is a probability distribution over 3 classes that sums to 1, and predict picks the largest. In multilabel problems, rows do NOT have to sum to 1.",
        topic="supervised", level=3),
    out("import numpy as np\nfrom sklearn.multiclass import OneVsRestClassifier\nfrom sklearn.linear_model import LogisticRegression\nX = np.array([[0, 0], [1, 1], [2, 2], [3, 3], [0, 3], [3, 0]])\nY = np.array([[1, 0, 1], [0, 1, 1], [1, 1, 0], [0, 0, 1], [1, 0, 0], [0, 1, 0]])\nclf = OneVsRestClassifier(LogisticRegression()).fit(X, Y)\nprint(len(clf.estimators_), clf.predict(X).shape)",
        ["3 (6, 3)", "1 (6,)", "6 (6, 3)", "3 (6,)"], 0,
        "One yes/no model per tag.",
        "For a multilabel target, one-vs-rest trains a separate binary classifier per label (3 here) and predicts a 0/1 matrix with one column per label.",
        diagram="""
x --> clf_tag0 --> 1
  \\-> clf_tag1 --> 0      -> [1, 0, 1]
   \\> clf_tag2 --> 1
""",
        topic="supervised", level=3),
    out("from sklearn.cluster import KMeans\nfrom sklearn.datasets import make_blobs\nX, _ = make_blobs(n_samples=300, centers=3, cluster_std=0.6, random_state=0)\nine = [KMeans(n_clusters=k, n_init=10, random_state=0).fit(X).inertia_ for k in (1, 2, 3, 4, 5)]\nprint([round(a / ine[0], 2) for a in ine])",
        ["[1.0, 0.43, 0.14, 0.12, 0.1]", "[1.0, 1.0, 1.0, 1.0, 1.0]", "[0.1, 0.12, 0.14, 0.43, 1.0]", "[1.0, 0.5, 0.33, 0.25, 0.2]"], 0,
        "Inertia (total distance to centres) always drops as k grows. Where does it stop dropping fast?",
        "Inertia keeps falling with more clusters, so 'lowest inertia' would always pick the largest k. The 'elbow' where the big drops stop (k = 3 here) is a hint, not proof, of the natural number of groups.",
        diagram="""
inertia
1.0 |*
    |  *
    |     *____*____*   <- elbow at k=3
    +----------------- k
     1  2  3    4    5
""",
        topic="unsupervised", level=3),
    out("from sklearn.metrics import adjusted_rand_score\nprint(adjusted_rand_score([0, 0, 1, 1], [1, 1, 0, 0]))",
        ["1.0", "0.0", "-1.0", "0.5"], 0,
        "Are the same items grouped together, whatever the names?",
        "Both labelings put items {0,1} together and {2,3} together; only the cluster names are swapped. Adjusted Rand index ignores names, so it is a perfect 1.0. Compare clusterings with ARI, never with plain accuracy.",
        topic="unsupervised", level=3),
    out("import numpy as np\nfrom sklearn.semi_supervised import SelfTrainingClassifier\nfrom sklearn.linear_model import LogisticRegression\nX = np.array([[0.0], [0.5], [1.0], [1.5], [8.0], [8.5], [9.0], [9.5]])\ny = np.array([0, -1, -1, -1, 1, -1, -1, -1])\nst = SelfTrainingClassifier(LogisticRegression(), threshold=0.6).fit(X, y)\nprint(st.transduction_.tolist())",
        ["[0, 0, 0, 0, 1, 1, 1, 1]", "[0, -1, -1, -1, 1, -1, -1, -1]", "[0, 1, 0, 1, 0, 1, 0, 1]", "[0, 0, 0, 0, 0, 0, 0, 0]"], 0,
        "-1 means 'no label yet'. Which points are near the 0 and near the 1?",
        "Self-training fits on the 2 labelled points, labels the unlabelled ones it is confident about (above 0.6), and refits. Here the clusters are clear, so every -1 gets a sensible pseudo-label.",
        topic="semi-self", level=3),
    mcq("Why are masked-language models (BERT) usually used for understanding tasks like classification, while next-token models (GPT) are used for generating text?",
        ["BERT sees words on both sides of the gap, which is great for understanding; GPT only sees the past, which matches writing text left to right", "BERT has no weights", "GPT can't be fine-tuned", "BERT is trained with RL"], 0,
        "What context does each model get to look at during training?",
        "Masked prediction uses both left and right context, giving strong representations for a whole input. Next-token prediction matches generation exactly: produce one token, append, repeat.",
        diagram="""
BERT: the cat [MASK] on the mat   (sees both sides)
GPT : the cat sat on  ->  ?       (sees only the past)
""",
        analogy="BERT reads the whole sentence like an editor filling a gap; GPT writes like someone typing, one word at a time.",
        topic="semi-self", level=3),
    out("q, alpha, gamma = 0.0, 0.5, 0.9\nreward, best_next_q = 1.0, 2.0\nq = q + alpha * (reward + gamma * best_next_q - q)\nprint(round(q, 2))",
        ["1.4", "2.8", "1.0", "0.5"], 0,
        "Target = reward + gamma * best next value; move halfway there.",
        "Q-learning target = 1 + 0.9 * 2 = 2.8. With learning rate 0.5, q moves halfway from 0 to 2.8, so 1.4. The agent learns from its own estimate of the future (bootstrapping), not from a given correct answer.",
        question="One Q-learning update. What does this print?",
        diagram="""
target = r + gamma * max Q(next)
       = 1 + 0.9 * 2 = 2.8
q: 0.0 ------- 1.4 ------- 2.8
         (moves alpha=0.5 of the way)
""",
        topic="rl", level=3),
    out("rewards = [0, 0, 0, 10]   # reward only at the end\nfor gamma in (0.5, 0.99):\n    G = sum(r * gamma ** t for t, r in enumerate(rewards))\n    print(gamma, round(G, 2))",
        ["0.5 1.25\n0.99 9.7", "0.5 10\n0.99 10", "0.5 5.0\n0.99 9.9", "0.5 1.25\n0.99 10.0"], 0,
        "The 10 arrives 3 steps later: multiply by gamma three times.",
        "With gamma 0.5 the delayed 10 is worth only 10 * 0.5^3 = 1.25 now; with 0.99 it keeps 10 * 0.99^3 = 9.7. A short-sighted agent may ignore a big delayed payoff, so long tasks (games, dialogues) use gamma close to 1.",
        topic="rl", level=3),
    out("eps, n_actions = 0.1, 4\np_best = (1 - eps) + eps / n_actions\nprint(round(p_best, 3))",
        ["0.925", "0.9", "0.1", "0.975"], 0,
        "A random action can also land on the best one.",
        "With probability 0.9 it exploits (picks the best); with probability 0.1 it picks uniformly at random, which hits the best action 1 time in 4. Total 0.9 + 0.025 = 0.925.",
        question="Under epsilon-greedy, how often is the current best action chosen?",
        analogy="Most nights you order from your favourite restaurant; one night in ten you try a random one, and sometimes that random pick is your favourite anyway.",
        topic="rl", level=3),
    out("import numpy as np\nfrom sklearn.linear_model import SGDClassifier\nrng = np.random.default_rng(0)\nXA = rng.normal(size=(500, 2)); yA = (XA[:, 0] > 0).astype(int)\nclf = SGDClassifier(random_state=0)\nclf.partial_fit(XA, yA, classes=[0, 1])\nbefore = clf.score(XA, yA)\nfor _ in range(20):\n    XB = rng.normal(size=(500, 2)); yB = (XB[:, 0] < 0).astype(int)  # rule flipped\n    clf.partial_fit(XB, yB)\nprint(before > 0.9, clf.score(XA, yA) < 0.2)",
        ["True True", "True False", "False True", "False False"], 0,
        "After 20 updates on the flipped rule, how does it do on the old data?",
        "The online model adapts to the new pattern and forgets the old one: accuracy on old data falls from >0.9 to <0.2. Good for real drift, bad if the old pattern still matters (catastrophic forgetting).",
        topic="online-batch", level=3),
    mcq("A news site's 'trending' model must react within minutes to a sudden event. Which design fits best?",
        ["Online updates (or very frequent small retrains) with safeguards, because the pattern changes faster than a nightly batch", "Retrain once a year", "Batch training on 10 years of news, never updated", "Clustering once at launch"], 0,
        "How fast does the world change here?",
        "When the data shifts in minutes, a nightly batch is always stale. Online learning adapts quickly; add rate limits, monitoring and a fallback because it also adapts to noise and attacks.",
        analogy="Nightly batch is a daily cron job; online learning is an event-driven consumer reacting to each message.",
        topic="online-batch", level=3),
    out("import torch, torch.nn as nn\ntorch.manual_seed(0)\nbackbone, head = nn.Linear(4, 3), nn.Linear(3, 2)\nfor p in backbone.parameters():\n    p.requires_grad = False\nmodel = nn.Sequential(backbone, head)\nopt = torch.optim.SGD([p for p in model.parameters() if p.requires_grad], lr=0.1)\nb0, h0 = backbone.weight.clone(), head.weight.clone()\nmodel(torch.randn(8, 4)).pow(2).mean().backward()\nopt.step()\nprint(torch.equal(b0, backbone.weight), torch.equal(h0, head.weight))",
        ["True False", "False False", "True True", "False True"], 0,
        "Which weights got gradients and were given to the optimizer?",
        "The frozen backbone gets no gradient and isn't in the optimizer, so it stays identical (True). The head is updated (False: it changed). That's the 'freeze backbone, train head' recipe.",
        topic="transfer", level=3),
    mcq("You have 50,000 labelled examples in your domain and a pretrained model from a similar domain. Compared with having 500 examples, what changes in the fine-tuning plan?",
        ["With more data you can safely unfreeze more (or all) layers and use a small learning rate; with 500 you mostly freeze and train the head", "Nothing changes", "With more data you should freeze more layers", "With more data you shouldn't use the pretrained model"], 0,
        "More data = more weights you can afford to adjust without overfitting.",
        "Rule of thumb: little data -> freeze most of the backbone; lots of data -> fine-tune deeper layers too. A small learning rate keeps the useful pretrained features from being wiped out.",
        diagram="""
  500 examples:  [frozen][frozen][frozen][train head]
50000 examples:  [frozen][ tune ][ tune ][train head]
                 small learning rate for tuned layers
""",
        topic="transfer", level=3),
    out("counts = {(\"free\", \"spam\"): 30, (\"free\", \"ham\"): 10, (\"hi\", \"spam\"): 5, (\"hi\", \"ham\"): 55}\nfree_total = counts[(\"free\", \"spam\")] + counts[(\"free\", \"ham\")]\nprint(counts[(\"free\", \"spam\")] / free_total)",
        ["0.75", "0.3", "0.857", "0.4"], 0,
        "Among emails containing 'free', what fraction is spam?",
        "A generative model stores the joint counts p(word, class). The classifier you need, p(spam | 'free') = 30 / 40 = 0.75, falls out by dividing. A discriminative model would learn that 0.75 directly.",
        question="From a generative model's joint counts to a classifier. What does this print?",
        topic="gen-disc", level=3),
    out("import math\nr_chosen, r_rejected = 2.0, 0.5   # reward-model scores\np = 1 / (1 + math.exp(-(r_chosen - r_rejected)))\nprint(round(p, 3))",
        ["0.818", "0.5", "0.8", "1.5"], 0,
        "It's a sigmoid of the score difference.",
        "The reward model is trained so that sigmoid(r_chosen - r_rejected) is high for the answer humans preferred (the Bradley-Terry model). Only the difference matters: adding 10 to both scores changes nothing.",
        question="How a reward model turns two scores into a preference probability. What does this print?",
        topic="rlhf", level=3),
    mcq("What are the three main stages of RLHF, in order?",
        ["Supervised fine-tuning on demonstrations -> train a reward model on human preference pairs -> optimise the LLM against that reward with RL (e.g. PPO)", "Train the reward model -> pre-train -> cluster", "RL from scratch -> supervised fine-tuning -> pre-training", "Collect preferences -> delete the base model -> train a new one"], 0,
        "You need a reward before you can do RL.",
        "SFT teaches the format; the reward model learns to predict which answer people prefer; RL then nudges the LLM towards high-reward answers. All of this happens after self-supervised pre-training.",
        diagram="""
pretrained LLM -> SFT -> sample answers -> humans rank
                                              |
          RL (PPO) <---- reward model <-------+
""",
        topic="rlhf", level=3),
    tf("DPO (Direct Preference Optimization) trains on the same human preference pairs as RLHF but skips the separate reward model and the RL loop, using a classification-style loss instead.", True,
       "Same data, simpler training loop?",
       "DPO shows the RLHF objective can be optimised directly on preference pairs. It's simpler and more stable to run, which is why many open models use it or its variants.",
       topic="rlhf", level=3),
    out("import numpy as np\n# 3 labelling functions vote per row: 1=spam, 0=ham, -1=abstain\nvotes = np.array([[1, 1, -1], [0, 1, 0], [-1, -1, 1], [-1, -1, -1]])\nlabels = []\nfor row in votes:\n    v = row[row != -1]\n    labels.append(int(np.bincount(v).argmax()) if v.size else -1)\nprint(labels)",
        ["[1, 0, 1, -1]", "[1, 1, 1, -1]", "[1, 0, -1, -1]", "[1, 0, 1, 0]"], 0,
        "Ignore abstentions; a row where everyone abstains stays unlabelled.",
        "Weak supervision: cheap, noisy rules ('contains a payment link' -> spam) vote, and a combiner (here majority vote) produces training labels. Rows with no votes stay unlabelled (-1).",
        analogy="Like several flaky but independent health checks: one alone is unreliable, a vote across them is much better.",
        topic="label-strategy", level=3),
    mcq("A medical startup can afford expert labels for only 2,000 of its 200,000 scans. Which plan gets the most out of the budget?",
        ["Active learning: label a seed set, train, then repeatedly send the scans the model is most unsure about to the experts", "Label 2,000 random scans and stop", "Label the 2,000 scans the model is most confident about", "Skip labels and use clustering as the diagnosis"], 0,
        "Which labels teach the model the most?",
        "Uncertain examples sit near the decision boundary, where labels change the model most. Keep a random labelled test set too: actively chosen examples are not representative for evaluation.",
        analogy="Like a code reviewer spending time on the risky diffs, not the typo fixes.",
        topic="label-strategy", level=3),
    mcq("An app wants to (1) detect unusual login attempts with no labelled attacks, then (2) once analysts have reviewed a few thousand alerts, improve detection. Which sequence of learning types fits?",
        ["Unsupervised anomaly detection first, then a supervised classifier trained on the analyst-labelled alerts", "Reinforcement learning only", "Supervised learning from day one", "Clustering forever, never using the labels"], 0,
        "What do you have on day 1, and what do you have later?",
        "Start without labels (anomaly scores), and use the analysts' reviews as labels for a supervised model later. Real systems often move from unsupervised to supervised as labels pile up.",
        topic="scenarios", level=3),
    mcq("A code-completion tool logs whether developers accept a suggestion (press Tab) or keep typing. The team wants to use these logs to improve suggestions. What kind of learning signal is this?",
        ["Implicit feedback on the tool's own outputs: a reward-like preference signal, only for suggestions it actually showed", "Clean supervised labels of the correct code", "Unsupervised data with no signal", "Self-supervised next-token labels"], 0,
        "Does the log tell you the right code, or only how users reacted to what was shown?",
        "Accept/ignore says how users reacted to one shown option, not what the right answer was. It is noisy and biased by what was shown, so teams treat it like bandit/preference data (rewards, pairwise wins) rather than ground-truth labels.",
        topic="scenarios", level=3),

    # ============================================================ more L4
    mcq("A team predicts customer satisfaction on a 1-5 scale. Plain multiclass classification treats 'predicted 1, actual 5' as just as wrong as 'predicted 4, actual 5'. What is the better framing?",
        ["Treat it as ordinal: use regression (then round) or an ordinal method, and measure with an error that respects distance, like MAE", "Multilabel classification", "Clustering into 5 groups", "Binary classification of 1 vs not-1"], 0,
        "The classes have an order. Does multiclass know that?",
        "Ordinal targets carry order that multiclass loss ignores. Regression or ordinal models use it, and MAE punishes far misses more than near ones. Report both MAE and per-class results.",
        diagram="""
actual = 5
 predict 4:  |----|          error 1 (close)
 predict 1:  |----------------|  error 4 (far)
 multiclass loss treats both as just 'wrong'
""",
        topic="supervised", level=4),
    mcq("A multilabel tagger uses one independent yes/no classifier per tag. Tags 'python' and 'pandas' almost always appear together. What does this design miss, and what helps?",
        ["Independent classifiers ignore correlations between labels; classifier chains (feed earlier predictions to later ones) or a shared model can use them", "Nothing; tags are always independent", "It must switch to multiclass", "It needs clustering of the tags first"], 0,
        "Does the 'pandas' model know what the 'python' model said?",
        "Binary relevance (one model per label) is simple and strong, but it can't use label co-occurrence. Classifier chains or one network with a shared body and one output per label capture it.",
        topic="supervised", level=4),
    out("import numpy as np\nfrom sklearn.cluster import KMeans\nfrom sklearn.metrics import silhouette_score\nfrom sklearn.datasets import make_blobs\nXb, _ = make_blobs(n_samples=300, centers=3, cluster_std=0.5, random_state=0)\nXn = np.random.default_rng(0).uniform(size=(300, 2))\nfor Z in (Xb, Xn):\n    lab = KMeans(n_clusters=3, n_init=10, random_state=0).fit_predict(Z)\n    print(round(silhouette_score(Z, lab), 1))",
        ["0.7\n0.4", "0.4\n0.7", "1.0\n0.0", "0.7\n0.7"], 0,
        "Silhouette is near 1 for tight, well-separated clusters.",
        "Real blobs score about 0.7; uniform noise still gets 3 clusters and a non-zero score (about 0.4). A silhouette is a relative hint, not a yes/no test that groups exist. Check stability across seeds and whether the groups mean something to the business.",
        topic="unsupervised", level=4),
    mcq("You run PCA on raw customer features: 'annual income in rupees' (values in lakhs) and 'number of logins per week' (0-50). The first component is almost exactly 'income'. Why?",
        ["PCA follows variance, and income's huge numeric scale dominates; standardise features before PCA", "Income is the most important feature for the business", "PCA always picks the first column", "Logins are categorical"], 0,
        "What does PCA maximise, and in which units?",
        "PCA finds directions of maximum variance. Unscaled, the feature with the biggest numbers wins regardless of meaning. Standardising puts features on equal footing. Unsupervised methods depend heavily on these choices.",
        topic="unsupervised", level=4),
    mcq("Contrastive models like CLIP learn by pulling matching (image, caption) pairs together. Why do they need many negatives (non-matching pairs) in each batch?",
        ["Without pushing different items apart, the model could map everything to the same vector and still look 'correct' (collapse)", "Negatives are the labels humans wrote", "Negatives make the model generative", "They don't; one positive pair is enough"], 0,
        "What's the laziest way to make every pair 'similar'?",
        "If the loss only rewarded similarity, outputting a constant vector would win. Negatives force the model to separate things. That's why contrastive training uses big batches (or tricks like momentum encoders).",
        diagram="""
 img_dog  <-pull->  'a dog'
    |
  push apart
    |
 'a car', 'a pizza', ... (negatives)
""",
        topic="semi-self", level=4),
    mcq("Self-supervised pre-training on web text gives an LLM broad skills. Which limitation comes directly from where the labels came from?",
        ["The model learns to continue text the way the internet does, including errors and biases, rather than to be correct or helpful", "It can only learn one language", "It needs human labels for every token", "It can't learn grammar"], 0,
        "The target was 'what comes next on the web', not 'what is true'.",
        "The objective rewards plausible continuation, so falsehoods and toxic patterns are learned too. That gap is what instruction tuning and preference tuning (RLHF/DPO) try to close.",
        topic="semi-self", level=4),
    mcq("Chess rewards only arrive at the end: win, lose or draw. What is the core difficulty this creates for an RL agent?",
        ["Credit assignment: figuring out which of the many earlier moves actually caused the result", "Too many rewards", "The board has no states", "It turns into supervised learning"], 0,
        "One number at the end, 40 moves earlier...",
        "With delayed rewards the agent must spread credit backwards over many actions. Value functions, discounting and bootstrapped updates (like TD learning) exist to solve exactly this.",
        diagram="""
move 1 -> move 2 -> ... -> move 40 -> WIN (+1)
   ?        ?                 ?
which moves deserve the credit?
""",
        topic="rl", level=4),
    mcq("A recommender is trained only on logs of what it previously showed and what got clicked. Why is this closer to an RL/bandit problem than plain supervised learning?",
        ["Its own past choices decide which data it sees; items never shown have no feedback, so it needs exploration to learn about them", "Clicks are continuous numbers", "There are no labels at all", "Recommenders can't be trained offline"], 0,
        "Do you know how users would have reacted to items you never showed?",
        "Feedback exists only for the action taken (partial feedback). Without exploration the system keeps confirming its own choices. Bandit methods and off-policy evaluation handle this.",
        topic="rl", level=4),
    mcq("In RLHF, the LLM is optimised to get high scores from a learned reward model. Why is a KL penalty (staying close to the original model) added?",
        ["Without it the policy drifts to strange outputs that exploit flaws in the reward model (reward hacking) while losing general ability", "To make training faster", "Because KL is the reward", "To increase the number of tokens"], 0,
        "The reward model is only a proxy for human judgement.",
        "Push hard on a learned proxy and the policy finds its blind spots: verbose, flattering or odd text that scores high. The KL term keeps the policy near the SFT model, where the reward model is reliable.",
        analogy="Like optimising only for a linter score: push hard enough and you get code that passes the linter but is worse.",
        topic="rlhf", level=4),
    out("reward, beta = 2.0, 0.1\nlog_ratio = 5.0   # log p_policy(answer) - log p_reference(answer)\nprint(reward - beta * log_ratio)",
        ["1.5", "2.0", "2.5", "-3.0"], 0,
        "The further the policy drifts, the more is subtracted.",
        "The RLHF objective is roughly reward - beta * KL. A high reward from an answer the reference model finds unlikely gets penalised: 2.0 - 0.1 * 5 = 1.5. Larger beta = stay closer to the original model.",
        question="The KL-penalised reward used in RLHF. What does this print?",
        topic="rlhf", level=4),
    tf("Because RLHF optimises for what human raters prefer, it can make a model more sycophantic, agreeing with the user or sounding confident even when that isn't correct.", True,
       "Do raters always prefer the correct answer, or sometimes the pleasing one?",
       "The reward reflects rater preferences, which can favour agreeable, confident or long answers. That's a known side effect; mitigations include better rater guidelines, targeted evals and mixing in correctness checks.",
       topic="rlhf", level=4),
    mcq("A team trains a model on labels produced by an active-learning loop and then reports accuracy on the actively selected examples it labelled. Why is that number misleading?",
        ["Those examples were chosen because they're hard and unusual, so they don't represent real traffic; evaluate on a separate random sample", "Active learning makes labels perfect", "The model has already seen them, so the score is too low", "Accuracy can't be computed with active learning"], 0,
        "How were those examples picked?",
        "Active selection biases the labelled pool toward the boundary. It's great for training and terrible as a test set. Always label an independent random sample for evaluation.",
        analogy="Like measuring app speed only on the slowest endpoints you picked to optimise: the number says nothing about typical traffic.",
        topic="label-strategy", level=4),
    mcq("Weak supervision combines several noisy rules that each label part of the data. Why not simply train on the output of the single most accurate rule?",
        ["Rules cover different cases and make different mistakes; combining them (weighting by estimated accuracy) gives more coverage and less noise than any single rule", "Rules are always 100% accurate", "Models can't learn from rule-generated labels", "Combining rules removes the need for any evaluation"], 0,
        "One rule fires on 10% of the data. What about the other 90%?",
        "Each rule is precise on a slice; together they cover more. A label model estimates each rule's accuracy and how rules correlate. The end model then generalises beyond the rules, but you still need a small hand-labelled test set.",
        topic="label-strategy", level=4),
    mcq("A team fine-tunes all layers of a large pretrained model on 300 examples with a high learning rate. Training accuracy hits 100% but the model is now worse on general inputs than before. What happened?",
        ["Overfitting plus catastrophic forgetting: large updates on tiny data overwrote the pretrained knowledge", "Negative transfer from a different domain", "The model became non-parametric", "Too much exploration"], 0,
        "What do big steps on 300 examples do to billions of weights?",
        "With tiny data, freeze most layers or use parameter-efficient methods (LoRA, adapters) with a small learning rate. Keep a general-ability eval to catch forgetting.",
        analogy="Like force-pushing a quick hotfix over main: it passes your one test and wipes out work that was already there.",
        topic="transfer", level=4),
    mcq("You need to decide for a payments product: what is the most important reason a generative LLM classifier (prompted with labels) might lose to a small discriminative model trained on 100,000 labelled payments?",
        ["The discriminative model targets p(label given input) directly on in-domain data, so with lots of labels it is usually more accurate, calibrated, cheaper and faster", "Generative models can't output labels", "Discriminative models need no labels", "LLMs never work for classification"], 0,
        "Which one was trained for exactly this task on this data?",
        "With abundant labels, a task-specific discriminative model usually wins on accuracy, latency and cost. LLM prompting wins when labels are scarce, classes change often, or inputs need world knowledge.",
        topic="gen-disc", level=4),
    mcq("A product for detecting fraudulent sellers combines: embeddings pre-trained with self-supervision, clustering to find seller rings, a supervised classifier on investigated cases, and a bandit that decides which flagged sellers to investigate. What is the main reason to include the bandit?",
        ["Investigations produce the labels; choosing only the top-scored sellers would never generate labels for borderline cases, so some exploration keeps the classifier learning", "Bandits replace the classifier", "Bandits are needed to compute embeddings", "It makes the clustering deterministic"], 0,
        "Where do future training labels come from?",
        "The system's own decisions create its training data. Pure exploitation creates a blind spot; a bandit trades a few 'less likely' investigations for information. Combining learning types is normal in real products.",
        diagram="""
self-sup embeddings -> clustering (rings)
         |
         v
  supervised scorer -> bandit picks cases -> investigators
         ^                                       |
         +--------------- new labels ------------+
""",
        topic="scenarios", level=4),
]
