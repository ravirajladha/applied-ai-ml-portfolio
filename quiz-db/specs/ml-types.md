# Types of Learning: coverage spec

**Ladder:** L1 · ML Fundamentals › Core Ideas   ·   **Prerequisites:** `ml-what`
**Why it matters for AI/ML:** The first design decision on any ML problem is "what kind of learning is this?". It decides what data you need (labels or not), which models and metrics apply, and how LLMs (self-supervised pre-training, then supervised fine-tuning, then RL from feedback) are built.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `supervised` | Supervised: classification and regression | labels present; category vs number | binary vs multiclass vs multilabel; `type_of_target` | multilabel shape and one-vs-rest; ordinal targets | regression-vs-classification framing trade-offs (e.g. binning a number) |
| 2 | `unsupervised` | Unsupervised: clustering, dimensionality reduction, anomaly detection | no labels, find structure | KMeans `n_clusters`, PCA output shape | cluster IDs are arbitrary; anomaly detectors return -1/1 | evaluating without labels; clusters you ask for always appear |
| 3 | `semi-self` | Semi-supervised and self-supervised | few labels + many unlabelled; labels from the data itself | -1 means unlabelled in sklearn; next-token pairs | masked vs next-token objectives; contrastive learning | why self-supervision scales; pseudo-label confirmation bias |
| 4 | `rl` | Reinforcement learning | agent, environment, reward, action | policy, episode, exploration vs exploitation | discounted return; epsilon-greedy | delayed credit assignment; reward hacking; RLHF's place |
| 5 | `online-batch` | Online vs batch learning | train once on everything vs learn as data arrives | `partial_fit` | when to choose online; catastrophic forgetting risk | poisoning and drift in online systems |
| 6 | `transfer` | Transfer learning and fine-tuning | reuse a pretrained model | freeze backbone, train head | how much to unfreeze vs data size | domain mismatch / negative transfer |
| 7 | `gen-disc` | Generative vs discriminative models | creates data vs draws boundaries | Naive Bayes vs logistic regression | p(x, y) vs p(y given x) | which needs more data; LLMs as generative models used discriminatively |
| 8 | `scenarios` | Picking the learning type for a scenario | everyday examples | mixed cases | multi-stage systems | combining types in one product |

## Must-know facts
- Supervised = every training example has the correct answer (label). Unsupervised = no labels.
- Classification predicts a category; regression predicts a number.
- Binary = 2 classes; multiclass = one of many; multilabel = several labels can be on at once.
- sklearn's `type_of_target` returns 'binary', 'multiclass', 'continuous', 'multilabel-indicator'.
- Clustering groups similar items; dimensionality reduction (PCA) compresses features; anomaly detection flags rare points.
- Cluster numbers are arbitrary names: cluster 0 in one run can be cluster 1 in another.
- sklearn outlier detectors (IsolationForest) predict 1 for inliers and -1 for outliers.
- Semi-supervised = a few labels + many unlabelled examples; sklearn marks unlabelled rows with -1.
- Self-supervised = labels are created from the data itself (next token, masked word, two views of the same image). This is how LLMs pre-train.
- Contrastive learning pulls two views of the same item together and pushes different items apart.
- RL = an agent acts in an environment, gets rewards, and learns a policy (state -> action) to maximise total (discounted) reward.
- Exploration = try new actions to learn; exploitation = use the best known action.
- Online learning updates the model incrementally as data arrives (`partial_fit`); batch learning retrains on the full dataset.
- Transfer learning reuses a model trained on a big task as the starting point for a smaller one.
- Generative models learn p(x, y) or p(x) and can create data; discriminative models learn p(y | x) and draw decision boundaries.
- LLM pipeline: self-supervised pre-training -> supervised fine-tuning -> RL from human feedback (or a preference method).

## Common traps (each one must have at least one question)
- "Predicting a number like a rating 1-5 is always classification" -> it can be framed either way; order matters.
- "Multiclass and multilabel are the same" -> multilabel allows several labels per example.
- "Cluster 0 means the same thing across runs" -> labels are arbitrary IDs.
- "KMeans found 5 clusters, so the data has 5 groups" -> it returns as many clusters as you ask for.
- "Self-supervised is the same as unsupervised with no learning signal" -> it creates supervised-style targets from the data.
- "LLMs are pre-trained with human-labelled data" -> pre-training uses the text itself as labels.
- "RL is supervised learning with a reward as the label" -> there is no correct action given, rewards can be delayed, and the agent's actions change its data.
- "Always exploit the best action" -> without exploration you may never find a better one.
- "Online learning means the model is served online" -> it means it learns incrementally.
- "Fine-tuning always helps" -> with very different domains or tiny data it can hurt (negative transfer / overfitting).
- "Generative models are only for creating images and text" -> Naive Bayes is generative and is used for classification.
- "Anomaly detection needs labelled anomalies" -> it is usually unsupervised.
- "sklearn IsolationForest returns 0/1" -> it returns 1 (inlier) and -1 (outlier).

## Interview angle
- **Supervised vs unsupervised vs RL?** Supervised learns input -> known answer; unsupervised finds structure with no answers; RL learns actions from rewards through trial and error.
- **What is self-supervised learning and why does it matter for LLMs?** The data labels itself (predict the next token), so you can train on trillions of tokens without humans labelling anything.
- **Generative vs discriminative?** Discriminative models learn p(y|x) directly and usually classify better with lots of data; generative models learn how the data is produced, p(x, y), can sample new data and can cope with less data.
- **When would you use online learning?** When data arrives as a stream and the pattern drifts (ads, fraud), or data is too big to retrain on at once.
- **How would you build a classifier with 500 labelled images?** Transfer learning: start from a pretrained backbone, freeze it, train a small head, then maybe unfreeze top layers.

## Source material
To be added
