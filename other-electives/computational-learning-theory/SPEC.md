# Computational Learning Theory (AIMLC ZG518) — Study spec

> The maths of *why* learning works: how much data you need, when a model will generalise, how to learn from a stream with guaranteed few mistakes, and why boosting, SVMs, RL, privacy and unlabeled data behave as they do. · Status: spec only (not built yet)

---

## 1. What it is and why an AI engineer should care

Most ML courses show *how* to train a model; this one asks **what can be learned, from how many examples, with what guarantee**.
It covers the PAC model (probably approximately correct learning), overfitting and Occam's razor, VC-dimension and Rademacher complexity (ways to measure how flexible a model class is), online learning with expert advice and regret, the perceptron and margins, boosting, kernels and SVMs, MDPs and reinforcement learning, differential privacy and semi-supervised learning.
For a software engineer it is the "big-O analysis" of machine learning: it explains sample-size planning, why simpler models generalise, why ensembles work, and how to bound damage when learning online.
It is proof-heavy; the job payoff is mostly better intuition and interview answers, not daily code.

**Job relevance: 2/5** — research and ML-theory roles value it; for applied roles it sharpens answers on generalisation, bias–variance, boosting and online learning but is rarely used directly.

---

## 2. Sources in this folder

| Kind | File (relative path) | Notes |
|---|---|---|
| Handout (older batch) | `handouts/Older batch - Computational Learning Theory (S2-25_AIMLCZG518) COURSE HANDOUT.docx` | v3 dated 05-10-2024, used for Second Semester 2025-26; author Srinath Naidu, lead instructor Prof. Pooja Harde; 7 modules, 16 contact sessions (CS) |

**Gaps:** handout only, older batch. No slides, past papers, assignments or books. Textbooks are named (T1 Mohri et al., *Foundations of Machine Learning*, 2nd ed.; T2 Shalev-Shwartz & Ben-David, *Understanding Machine Learning*; R1 Kearns & Vazirani) but not in the folder. Lab: "Not applicable". The course description also lists sleeping experts, the statistical query model and VC-dimension; VC-dimension is in CO2/LO2 but has no session of its own, so it is placed under M1/M4 here. Hours per session: not stated.

---

## 3. Running scenario

**ShieldMail** is the spam-and-phishing filter team at an email provider. Product asks hard questions the usual ML workflow doesn't answer:
*How many labelled emails do we need before the filter is reliably within 2% error? Why does the giant model overfit while the small one doesn't? Can we combine five vendor filters online so we're never much worse than the best one? Can we train on users' mail without leaking it, and use the millions of unlabeled emails?*
Data: a public spam corpus (e.g. SMS Spam Collection or Enron-spam) turned into simple features, plus synthetic data where the true rule is known so guarantees can be checked.
Each module answers one of ShieldMail's questions with a bound, an algorithm, and a small experiment that checks the bound.

---

## 4. Module map

Module names from the handout's Content Structure; sessions from Part B.

### M1 · Introduction to PAC learning, learning via uniform convergence, overfitting and Occam's razor (≈ CS 1–2)

Topics: PAC framework; generalisation error vs empirical error; learning via uniform convergence; overfitting; Occam's razor. (VC-dimension, named in the objectives, fits here.)

| Concept | One-line definition | Analogy |
|---|---|---|
| Hypothesis class H | The set of all models the learner is allowed to pick from | The set of configs your search space allows |
| Empirical vs true error | Error on training data vs expected error on new data | Passing unit tests vs working in production |
| PAC learning | With probability ≥ 1−δ, the learned model has true error ≤ ε, using enough samples | An SLA: "99% of the time, error under 2%" |
| Sample complexity | Number of examples needed for a PAC guarantee, e.g. m ≥ (1/ε)(ln\|H\| + ln(1/δ)) for finite H | Capacity planning for test coverage |
| Uniform convergence | Training error is close to true error for *every* model in H at once | Load test that covers every endpoint, not just one |
| Occam's razor | Smaller (simpler) hypothesis classes need fewer samples to generalise | Fewer config knobs = fewer ways to overfit the test |
| VC-dimension | Largest number of points the class can label in every possible way | How many independent switches the model really has |

Diagram ideas: ε–δ "SLA" picture; sample complexity curve vs ln\|H\|; shattering 3 points with a line but not 4.
Scenario step: ShieldMail computes how many labelled emails it needs for a 2% / 99% guarantee.
Notebook idea: compute finite-class sample bounds; simulate learning a threshold/interval on synthetic data and plot true vs empirical error as m grows; check the bound holds. numpy, laptop.
Production angle: sample-size planning, holdout sizing. **Breaks:** guarantees assume i.i.d. data; spam campaigns shift distribution, voiding the bound.

### M2 · Decision tree learning, and learning with perceptrons (≈ CS 3–4)

Topics: decision tree learning; learning with perceptrons (halfspaces).

| Concept | One-line definition | Analogy |
|---|---|---|
| Decision tree | A sequence of yes/no feature tests ending in a label | Nested if-else rules |
| Tree size vs generalisation | Bigger trees fit more but need more data to generalise | More rules = more ways to overfit |
| Halfspace / linear classifier | Label = sign(w·x + b), a flat boundary | A weighted score with a cutoff |
| Perceptron | Update weights only when a mistake is made | Fix-on-failure patching |
| Margin γ | Distance from the boundary to the closest point | Safety buffer around a threshold |
| Perceptron mistake bound | At most (R/γ)² mistakes on separable data | Guaranteed max number of incidents |

Diagram ideas: tree as nested boxes in feature space; perceptron update rotating the boundary; margin band.
Scenario step: ShieldMail compares a rule-tree filter vs a linear filter and bounds the perceptron's mistakes.
Notebook idea: perceptron from scratch on separable synthetic data; count mistakes and assert ≤ (R/γ)²; sklearn tree depth vs test error. Laptop.
Production angle: gradient-boosted trees, linear models at scale. **Breaks:** non-separable data — perceptron never converges.

### M3 · Online learning models and learning with expert advice (≈ CS 5–6)

Topics: online mistake-bound model; combining expert advice; weighted majority / multiplicative weights; regret minimisation (description also names sleeping experts).

| Concept | One-line definition | Analogy |
|---|---|---|
| Online learning | Predict one example at a time, then see the true label and update | Streaming processing with instant feedback |
| Mistake-bound model | Count total mistakes over any sequence, even adversarial | Worst-case incident count |
| Halving algorithm | Predict by majority of still-consistent hypotheses; drop the wrong ones | Bisect to find the bad commit |
| Weighted majority | Each expert has a weight; wrong experts get multiplied down | Reputation scores for vendors |
| Multiplicative weights | General update w ← w·(1−η·loss) | Exponential backoff on unreliable sources |
| Regret | Your total loss minus the best single expert's loss in hindsight | "How much worse than if we had picked the best vendor upfront" |

Diagram ideas: weights of 5 experts over time; regret growing like √T vs linear.
Scenario step: ShieldMail combines five vendor spam filters online, never far behind the best.
Notebook idea: weighted majority and Hedge on simulated expert predictions; plot regret vs √(T ln N) bound. Laptop.
Production angle: online ensembles, bandit-style routing between models. **Breaks:** learning rate too high → thrashing between experts; feedback delays.

### M4 · Rademacher bounds and computational hardness results for learning (≈ CS 7–9)

Topics: Rademacher complexity and generalisation bounds; growth function and VC-dimension (T1 ch. 3); computational hardness results for learning.

| Concept | One-line definition | Analogy |
|---|---|---|
| Rademacher complexity | How well the class can fit random ±1 noise on your data | How easily a test suite can be gamed by random code |
| Data-dependent bound | Generalisation bound computed from the actual sample | Profiling your real workload instead of worst case |
| Growth function | Number of distinct labellings H can produce on m points | Number of distinct behaviours a config can show |
| Sauer's lemma | Growth is polynomial once m exceeds VC-dimension | Capacity stops exploding past a point |
| Computational hardness | Some classes need few samples but no efficient algorithm is known to learn them | Problem is decidable but NP-hard |

Diagram ideas: fitting random labels — simple vs complex class; growth function 2^m then polynomial.
Scenario step: ShieldMail explains to product why the giant feature set overfits despite low training error.
Notebook idea: estimate empirical Rademacher complexity for linear classifiers of different norm limits by Monte Carlo; plot vs sample size. Laptop.
Production angle: model selection and regularisation reasoning. **Breaks:** bounds are often loose (vacuous) for deep nets; use them for intuition, not SLAs.

### M5 · Algorithms — boosting, kernels, SVMs, perceptrons for halfspaces (≈ CS 10–11)

| Concept | One-line definition | Analogy |
|---|---|---|
| Weak learner | A model only slightly better than random guessing | A junior reviewer who's right 55% of the time |
| AdaBoost | Train weak learners in sequence, up-weighting the examples previous ones got wrong | Focusing the next sprint on last sprint's bugs |
| Boosting training-error bound | Error drops exponentially with rounds if each learner beats 50% | Compounding small improvements |
| SVM | Linear classifier choosing the maximum-margin boundary | Widest safety buffer |
| Kernel trick | Compute inner products in a high-dimensional feature space without building it | Querying a view instead of materialising the table |
| Margin-based bound | Generalisation depends on margin, not raw dimension | Robustness from slack, not size |

Diagram ideas: AdaBoost re-weighting rounds; SVM margin and support vectors; kernel mapping 1-D → 2-D to separate.
Scenario step: ShieldMail boosts tiny keyword rules into a strong filter and tries an RBF-kernel SVM.
Notebook idea: AdaBoost with decision stumps from scratch, track training error vs exp(−2Σγₜ²) bound; sklearn SVC linear vs RBF on spam features. Laptop.
Production angle: XGBoost/LightGBM descend from boosting; kernels in small-data settings. **Breaks:** boosting on noisy labels over-focuses on mislabeled examples.

### M6 · MDPs and reinforcement learning (≈ CS 12–14)

Topics (T1 ch. 17): Markov decision processes, policies, planning (value/policy iteration), learning algorithms (Q-learning, TD), theory of convergence.

| Concept | One-line definition | Analogy |
|---|---|---|
| MDP | States, actions, transition probabilities, rewards | A state machine with probabilistic edges and payoffs |
| Policy | Rule choosing an action in each state | A routing table |
| Value function | Expected total (discounted) reward from a state | Lifetime value of a user in a given state |
| Value iteration | Repeatedly apply the Bellman update until values settle | Iterating a cache until it converges |
| Q-learning | Learn action values from experience without a model | Learning from logs instead of a spec |

Diagram ideas: small email-triage MDP graph; Bellman backup tree; Q-table filling over episodes.
Scenario step: ShieldMail models "warn / quarantine / deliver" decisions with delayed user feedback as an MDP.
Notebook idea: value iteration and tabular Q-learning on a tiny triage MDP with numpy; compare to the exact solution. Laptop.
Production angle: bandits and RL for notifications and ranking. **Breaks:** reward hacking; non-stationary user behaviour.

### M7 · Differential privacy and learning, semi-supervised learning (≈ CS 15–16)

Topics: differential privacy and learning; semi-supervised learning (T1 ch. 12.1–12.4 cited; online resources and research papers).

| Concept | One-line definition | Analogy |
|---|---|---|
| Differential privacy (ε) | Output barely changes whether or not any one person's data is included | Aggregated dashboards that can't reveal one user |
| Laplace mechanism | Add calibrated random noise to a query result | Jitter added to metrics before publishing |
| Privacy–accuracy trade-off | Smaller ε = more privacy, more noise, less accuracy | Security vs convenience |
| Semi-supervised learning | Use many unlabeled examples alongside few labelled ones | Inferring tags from a few tagged items plus structure |
| Cluster / smoothness assumption | Nearby points (in dense regions) likely share labels | Similar tickets usually have the same root cause |

Diagram ideas: two neighbouring datasets → nearly identical output distributions; label propagation on a similarity graph.
Scenario step: ShieldMail trains on users' mail with privacy guarantees and exploits unlabeled email.
Notebook idea: Laplace mechanism on counting queries (accuracy vs ε plot); sklearn `LabelSpreading` with 1% labels vs fully supervised. Laptop.
Production angle: Opacus / TensorFlow Privacy (DP-SGD), Apple/Google telemetry. **Breaks:** privacy budget silently exhausted by repeated queries.

---

## 5. Codebase plan

`codebase/` — **learnbounds**: tiny library of learners + bound calculators with experiments that check theory against simulation. numpy, scipy, sklearn, matplotlib.

```
codebase/
├── README.md                  how to run, module → file map                    (M1)
├── learnbounds/
│   ├── pac.py                 finite-H and VC sample-complexity calculators    (M1)
│   ├── synthetic.py           data with a known true rule                      (M1)
│   ├── perceptron.py          perceptron + mistake counter                     (M2)
│   ├── experts.py             halving, weighted majority, Hedge, regret        (M3)
│   ├── rademacher.py          Monte Carlo Rademacher estimate                  (M4)
│   ├── boosting.py            AdaBoost with stumps                             (M5)
│   ├── mdp.py                 value iteration, Q-learning                      (M6)
│   └── privacy.py             Laplace mechanism, label spreading wrapper       (M7)
├── experiments/run_all.py     regenerates every bound-vs-simulation plot       (M1–M7)
└── tests/
    ├── test_pac.py            bound monotone in ε, δ, |H|                      (M1)
    ├── test_online.py         perceptron mistakes ≤ (R/γ)²; regret ≤ bound     (M2, M3)
    └── test_boosting.py       training error ≤ exp bound                       (M5)
```

---

## 6. Practice topics plan

01 PAC learning, sample complexity, Occam and VC-dimension — M1 — 6 h
02 Decision trees, perceptron and mistake bounds — M2 — 4 h
03 Online learning: experts, weighted majority, regret — M3 — 5 h
04 Rademacher complexity and hardness — M4 — 6 h
05 Boosting, kernels and SVM margins — M5 — 5 h
06 MDPs and RL theory — M6 — 4 h
07 Differential privacy and semi-supervised learning — M7 — 4 h

---

## 7. Exam signal

No past papers in this folder. Evaluation scheme (older handout):

| No | Component | Type | Duration | Weight | Date (that term) |
|---|---|---|---|---|---|
| 1 | Assignment 1 (PAC learning, Occam's razor) | Online | – | 10% | TBA |
| 2 | Assignment 2 (online learning models) | Online | – | 10% | TBA |
| 3 | Quiz 1 | Online | – | 5% | TBA |
| 4 | Quiz 2 | Online | – | 5% | TBA |
| 5 | Mid-semester | Closed book | 90 min | 30% | 21-06-2026 (FN) |
| 6 | Comprehensive | Open book | 150 min | 40% | 06-09-2026 (FN) |

Midsem: weeks 1–8 (M1–M4 start). Comprehensive: all sessions 1–16. The handout says "best two out of the three" for EC-1 without saying three of what (not clear). Question style: not stated; textbook-style proofs and bound calculations are likely given the references, but that is an inference.

---

## 8. Interview angle

1. **What does PAC learning guarantee?** — With probability at least 1−δ, the learned model's true error is at most ε, given enough samples.
2. **Why do simpler models generalise better?** — Smaller hypothesis classes need fewer samples for training error to match test error (Occam / VC bounds).
3. **What is VC-dimension of a line in 2D?** — 3: a line can shatter 3 points in general position but not 4.
4. **Explain bias–variance through this lens.** — Bigger classes cut approximation error (bias) but raise estimation error (variance) for a fixed sample size.
5. **What is regret in online learning?** — Your cumulative loss minus the best fixed expert's loss in hindsight; good algorithms get O(√T).
6. **Why does boosting work?** — Each round focuses on previous mistakes; if every weak learner beats chance, training error falls exponentially.
7. **What is the kernel trick?** — Replace dot products with a kernel function to learn linear models in a huge feature space cheaply.
8. **Why maximise the margin in SVMs?** — Larger margins give generalisation bounds that don't depend on raw feature dimension.
9. **What is differential privacy in one line?** — A guarantee that the output barely changes if any single record is added or removed.
10. **When does semi-supervised learning help?** — When unlabeled data reveals structure (clusters, manifolds) that matches label boundaries.

---

## 9. Repetition plan

| Concept | First met | Revisited in |
|---|---|---|
| Hypothesis class size / capacity | M1 | M2 (tree size), M4 (Rademacher, VC), M5 (margins) |
| Generalisation gap | M1 | M2, M4, M5, M7 |
| Margin | M2 (perceptron) | M5 (SVM, boosting margins) |
| Mistake bound / regret | M2 | M3, M6 (RL regret) |
| Multiplicative weight updates | M3 | M5 (AdaBoost weights) |
| ε–δ guarantees | M1 (PAC) | M4 (bounds), M7 (differential privacy ε) |
| Linear classifiers | M2 | M5 (SVM, kernels) |

---

## 10. Overlap with my other courses

- [../../deep-reinforcement-learning/](../../deep-reinforcement-learning/) — MDPs, Bellman equations, value iteration (`practice/01 MDP - Value Iteration`) for M6.
- [../../artificial-and-computational-intelligence/](../../artificial-and-computational-intelligence/) — probabilistic reasoning and decision making background (`revision/ch10-probabilistic-reasoning.md`).
- [../../software-engineering-for-machine-learning/](../../software-engineering-for-machine-learning/) — privacy and responsible-ML practices connect to M7.
- No real overlap with the LLM or NLP courses.

---

## 11. Build checklist

- [ ] SPEC reviewed
- [ ] cards.json (M1, M2, M3, M4, M5, M6, M7)
- [ ] practice/01 PAC learning, sample complexity, Occam and VC-dimension
- [ ] practice/02 Decision trees, perceptron and mistake bounds
- [ ] practice/03 Online learning and regret
- [ ] practice/04 Rademacher complexity and hardness
- [ ] practice/05 Boosting, kernels and SVM margins
- [ ] practice/06 MDPs and RL theory
- [ ] practice/07 Differential privacy and semi-supervised learning
- [ ] codebase/ runs + tests

**Total estimated study hours: ≈ 40 h** (34 h practice topics + 6 h codebase).
