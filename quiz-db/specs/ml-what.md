# What is Machine Learning?: coverage spec

**Ladder:** L1 · ML Fundamentals › Core Ideas   ·   **Prerequisites:** basic Python, `py-basics`
**Why it matters for AI/ML:** Every later topic (metrics, models, LLMs, MLOps) assumes you know what a model is, what training produces, and what the end-to-end workflow looks like. Interviewers open with these questions to see if you think like an ML engineer or just call `.fit()`.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `rules-vs-learned` | Rules vs learned functions | data + answers -> rules; model = function written from examples | a learned threshold is an if-rule the computer chose | learned rules are statistical, not guaranteed; brittle outside data | hybrid systems: rules as guardrails around a model |
| 2 | `params-hyper` | Model, parameters, hyperparameters | weights are learned; hyperparameters are set by you | sklearn `get_params` vs `coef_`; counting params of a linear model | which knobs are hyperparameters (depth, k, learning rate) and how they're tuned | hyperparameters chosen on validation, not test; params vs capacity |
| 3 | `train-infer` | Training vs inference | train once, predict many; weights frozen at inference | `fit` returns self; `predict` before `fit` fails; save/load | cost profile: training throughput vs inference latency | training-serving skew; an LLM doesn't learn from your chat |
| 4 | `workflow` | The ML workflow end-to-end | order of the steps | where most time goes (data); pipelines bundle preprocessing | baselines first; the loop back from monitoring to retraining | what breaks after deploy: drift, feedback loops, silent failures |
| 5 | `when-not-ml` | When NOT to use ML | fixed rules / formulas don't need ML | no data, no pattern, need for 100% correctness | heuristic baseline beats ML; cost of error and explainability | regulated decisions, adversarial settings, maintenance cost of ML |
| 6 | `ai-ml-dl` | AI vs ML vs DL vs GenAI | nested circles | an expert system is AI but not ML; LLM placement | discriminative vs generative framing of GenAI | why "AI" in a product doesn't imply learning |
| 7 | `generalisation` | Generalisation and bias-variance intuition | doing well on new data is the goal | train score 1.0 doesn't mean good; underfit vs overfit | bias vs variance; what more data does and doesn't fix | error = bias^2 + variance + noise; irreducible error |
| 8 | `inductive-bias` | Inductive bias and no free lunch | every model assumes something | linear can't fit XOR; trees can't extrapolate | inductive biases of kNN, trees, linear, CNNs | what no free lunch really says (and doesn't) |
| 9 | `parametric` | Parametric vs non-parametric | fixed-size vs grows-with-data | kNN stores the data; linear stores d+1 numbers | trees/kNN vs linear/NN; lazy vs eager learners | "non-parametric" still has parameters; NN with billions of weights is parametric |
| 10 | `framing` | Framing a business problem as an ML task | input, output, target | choosing the target and a baseline | metric aligned to business cost; prediction point in time | proxy targets and Goodhart's law; label leakage from the future |
| 11 | `genai-lens` | ML thinking for GenAI apps | calling an LLM API is inference; an LLM is a learned model | evals = regression test suite; prompting is not training | LLM vs small trained classifier (labels, latency, cost); non-deterministic evals; baseline first for RAG | LLM-as-judge bias; benchmark contamination; memory/feedback vs weight updates |

## Must-know facts
- Traditional programming: rules + data -> answers. ML: data + answers -> rules (the model).
- A model is a learned function; its parameters (weights) are learned by training.
- Hyperparameters (tree depth, k in kNN, learning rate) are chosen by you before training and tuned on a validation set.
- In scikit-learn, learned attributes end with an underscore (`coef_`, `tree_`, `classes_`) and only exist after `fit`.
- Training is slow, done rarely, and produces weights; inference is running those frozen weights on new input.
- Workflow: frame the problem -> get data -> prepare features -> train -> evaluate -> deploy -> monitor -> retrain.
- Most real ML time goes into data, not into model choice.
- Always build a simple baseline (majority class, mean, a rule) before a fancy model.
- If a fixed rule or formula solves it exactly, do not use ML.
- AI ⊃ ML ⊃ DL; GenAI (LLMs, diffusion) is a part of deep learning focused on generating content.
- Generalisation = doing well on unseen data from the same distribution. Training score alone proves nothing.
- High bias = too simple (underfits); high variance = too sensitive to the training sample (overfits).
- More data reduces variance; it does not fix a model that is too simple (high bias).
- Expected squared error = bias^2 + variance + irreducible noise.
- Inductive bias = the assumptions a learner uses to guess beyond the data it saw.
- No free lunch: averaged over all possible problems, no learner beats another; real-world wins come from assumptions that match the problem.
- Parametric = fixed number of parameters regardless of data size (linear, logistic, a fixed neural net). Non-parametric = model size grows with data (kNN, unpruned trees).
- Pick the target and the metric from the business cost of mistakes, and only use features available at prediction time.
- Calling an LLM is inference on frozen weights; an eval set is the model's regression test suite, built before the fancy pipeline.
- In RAG, the weights are parametric memory and the document index is non-parametric memory.

## Common traps (each one must have at least one question)
- "100% training accuracy means a great model" -> it often means memorisation; check unseen data.
- "Hyperparameters are learned during training" -> they are set before training and tuned on validation data.
- "The chatbot learns from my conversation as we talk" -> weights are frozen at inference; context is not training.
- "All AI is machine learning" -> rule-based expert systems are AI without learning.
- "Non-parametric means the model has no parameters" -> it means the number of parameters grows with the data.
- "A neural network with billions of weights is non-parametric" -> it is parametric: its size is fixed by the architecture.
- "More data always fixes a bad model" -> it fixes variance, not bias.
- "No free lunch means all algorithms are equally good on my problem" -> it is about the average over all possible problems.
- "Deploy is the last step" -> monitoring and retraining follow; models decay as data drifts.
- "ML is the right tool whenever data exists" -> deterministic rules, tiny data or zero-error requirements argue against it.
- "Tune hyperparameters on the test set" -> that leaks the test set into your choices; tune on validation.
- "Optimise the easiest-to-measure proxy" -> Goodhart's law: clicks become clickbait.
- "Decision trees extrapolate trends" -> they predict a constant beyond the training range.
- "Using a feature that is only known after the event" -> label leakage; great offline score, useless in production.
- "A second `fit` continues from the first" -> sklearn `fit` restarts from scratch; only `partial_fit`/`warm_start` continue.
- "No chargeback yet means not fraud" -> immature labels; exclude rows whose label window is still open.
- "An LLM agent is an RL agent learning as it runs" -> it is a frozen model plus orchestration code.
- "Always use the biggest LLM" -> with many labels, strict latency and high volume a small trained classifier is usually better.
- "A high public-benchmark score means it works on my task" -> contamination and distribution mismatch; build your own evals.

## Interview angle
- **What is ML, in one line?** Learning a function from examples instead of hand-writing the rules; you trade explicit logic for data plus an objective.
- **Parameters vs hyperparameters?** Parameters are learned by training (weights); hyperparameters are knobs you set (depth, learning rate) and tune on a validation set.
- **Explain bias-variance.** Bias is error from wrong/too-simple assumptions; variance is error from over-reacting to the particular training sample. Simple models underfit, complex ones overfit; you pick capacity, regularisation and data size to balance them.
- **When would you NOT use ML?** When a rule solves it exactly, when there's no data or no learnable pattern, when mistakes must be zero or fully explainable, or when the maintenance cost beats the gain over a heuristic.
- **How do you frame a business problem as ML?** Define the decision, the prediction point in time, the target label, a metric tied to the cost of errors, a baseline, and which features are actually available at prediction time.

- **When would you use a small trained model instead of an LLM?** When you have plenty of labels, a fixed set of outputs, strict latency or cost limits and huge volume; prompt an LLM when labels are scarce or outputs are open-ended, and either way measure with an eval set first.

## Source material
To be added
