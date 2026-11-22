# FAccT Machine Learning, "FIT ML" (course code not stated) — Study spec

> Making models fair, explainable, robust and private, not just accurate. · Status: spec only (not built yet)

## 1. What it is and why an AI engineer should care

**What "FIT ML" stands for:** the handout's course title is **"FAccT Machine Leaning"** [sic], where FAccT = **Fairness,
Accountability and Transparency**. The course covers fairness, interpretability, robustness, accountability (auditing)
and privacy. Course number: not stated in Part A; Part B says "Course No ZG 565" under the title "Machine Learning",
which looks like a template leftover, so the real code is uncertain.

Most ML courses ask "is the model accurate?". This one asks: is it fair to different groups (fairness), can we explain
its decisions (interpretability / transparency), does it break when someone tweaks the input on purpose (robustness),
can we audit it (accountability), and does it leak private data (privacy)? These are now legal and business
requirements: lenders must explain rejections, regulations such as the EU AI Act demand bias testing, and SHAP plots
are standard in model reviews. Every topic has a practical library (Fairlearn, AIF360, SHAP, Captum, Opacus).

**Job relevance: 3/5** — SHAP/LIME, fairness checks and model cards appear in many ML roles; dedicated "responsible AI" jobs are fewer.

## 2. Sources in this folder

| Kind | File (relative path) | Notes |
|---|---|---|
| Handout | `handouts/FIT ML - handout.pdf` | v1.0, 11 Jan 2023, content author Dr. Sugata Ghosal; 12 content modules, 16 sessions (session 7 adds disentangled fair representations), 6 labs; textbooks Barocas, Hardt & Narayanan "Fairness and Machine Learning" (T1) and Molnar "Interpretable Machine Learning" (T2) |

Gaps: only one handout (not marked current or older), no slides, no past papers, no lab sheets. Handout learning
outcomes (LO1–LO4) are generic ML outcomes, not specific to FAccT. Mid-term and comprehensive are both **open book**.

## 3. Running scenario

**QuickLoan** is a Pune fintech that gives small personal loans through an app. A gradient-boosted credit model
approves or rejects applicants from income, job, age, gender, pincode and repayment history (data shaped like the UCI
Adult Income dataset), a text classifier reads the free-text "loan purpose", and a CNN checks the selfie and ID
photo for KYC. The regulator and an internal audit ask four questions: are women and some pincodes rejected unfairly,
can we tell each rejected applicant why, can a fraudster fool the KYC model with a doctored photo, and does any model
leak customers' personal data? Each module answers part of this audit.

## 4. Module map

Modules follow the handout's content structure; session numbers are from the learning plan. Contact hours per
module: not stated (each module is about one session).

### M1 · Introduction (session 1)

Topics: traditional performance criteria; emerging requirements: fairness, accountability, transparency, privacy, robustness; motivating use cases.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Fairness | The model's decisions do not unjustly disadvantage people because of group membership. | An API that rate-limits all clients by the same rule |
| Accountability | Someone can audit, explain and take responsibility for model decisions. | Audit logs plus an on-call owner |
| Transparency | People can understand how and why the model reaches decisions. | Readable source code vs a binary |
| Robustness | Performance holds under noise, shift or deliberate attacks. | Fuzz-tested input handling |
| Privacy | The model and its outputs do not reveal individuals' personal data. | Not logging passwords |

Diagram ideas: five FAccT pillars around the "accuracy" box; ML lifecycle with where each pillar is checked.
Scenario step: write QuickLoan's audit checklist.
Notebook idea: train the baseline credit model on Adult Income (`sklearn`/`fairlearn.datasets`), report accuracy, AUC, then group-wise approval rates. CPU.
Production angle: model cards, risk registers. Breaks: accuracy is reported only overall, hiding a group with much worse error.

### M2 · Fairness and bias (session 2)

Topics: sources of bias; real-world examples (school admissions, criminal justice, hiring, gender/occupation bias); sensitive features; fairness through unawareness.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Sensitive feature | An attribute such as gender, caste, religion or age that must not drive unfair outcomes. | A field under compliance rules |
| Historical bias | Labels reflect past unfair decisions, so the model learns them. | Tests written against buggy expected output |
| Representation bias | Some groups are under-represented in training data. | Load testing only from one region |
| Proxy variable | A feature (pincode) that strongly predicts a sensitive one (religion, income group). | A user ID that leaks the email |
| Fairness through unawareness | Dropping sensitive features; fails because proxies remain. | Removing a column but keeping its foreign key |

Diagram ideas: bias sources along the pipeline (collection → labelling → features → model → feedback loop); proxy correlation heat map.
Scenario step: drop gender and show the model still rejects women more via proxies.
Notebook idea: remove `sex` from Adult, retrain, measure group gap again; predict `sex` from other features to show proxies. CPU.
Production angle: bias reviews before launch. Breaks: feedback loop, where rejected applicants never get a chance to prove repayment.

### M3 · Learning fair representations (session 3)

Topics: fairness criteria; direct solution method; demographic parity; equality of odds / opportunity; FICO case study; prejudice remover regulariser and prejudice index (PI); Adult Income case study.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Demographic parity | Each group gets positive decisions at the same rate. | Equal quota per region |
| Equalised odds | True-positive and false-positive rates are equal across groups. | Same bug-detection and false-alarm rate per team |
| Equal opportunity | Only true-positive rates must match: qualified people are approved equally. | Every good PR gets merged at the same rate |
| Impossibility trade-off | When base rates differ, these criteria cannot all hold at once. | CAP theorem for fairness |
| Prejudice index (PI) | Mutual information between prediction and sensitive feature, a measure of dependence. | Correlation between output and a field that should not matter |
| Prejudice remover regulariser | Adds PI to the training loss so the model learns less dependence. | A lint rule enforced during build |

Diagram ideas: confusion matrices per group with TPR/FPR; FICO-style threshold per group plot.
Scenario step: QuickLoan reports demographic parity difference and equal-opportunity difference.
Notebook idea: lab 2/3 style: `fairlearn.metrics.MetricFrame`, `ThresholdOptimizer` for equalised odds; AIF360 `PrejudiceRemover`. CPU.
Production angle: Fairlearn, AIF360 in CI checks. Breaks: optimising one metric worsens another nobody monitors.

### M4 · Fairness through input manipulation (session 4)

Topics: reweighing; uniform sampling; preferential sampling; individual fairness; optimised pre-processing; learning to defer.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Pre-processing | Fix the data before training so the model learns less bias. | Cleaning input before it hits the service |
| Reweighing | Give training examples weights so each group-label combination counts fairly. | Weighted load balancing |
| Preferential sampling | Duplicate or drop examples near the decision boundary to balance groups. | Rebalancing shards |
| Individual fairness | Similar individuals should receive similar decisions. | Same input, same output, regardless of user name |
| Learning to defer | The model hands uncertain cases to a human instead of deciding. | Escalating to L2 support |

Diagram ideas: pre / in / post-processing map of mitigation methods; reweighing table (group x label weights).
Scenario step: reweigh training data and route borderline applicants to a human underwriter.
Notebook idea: lab 1 style: AIF360 `Reweighing` on Adult; compare accuracy and parity before/after; defer rule on low-confidence predictions. CPU.
Production angle: AIF360, human review queues. Breaks: human reviewers carry their own bias, so the deferred cases still need audits.

### M5 · Fair causal reasoning (session 5)

Topics: causal fairness and inherent bias; counterfactual fairness (formal methods, law-school success and crime-rate/arrest case studies); equalised counterfactual odds; multiple causal worlds.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Causal graph | Arrows showing which variables cause which. | A service dependency diagram |
| Counterfactual | "What would the decision be if this person's gender were different, all else following causally?" | Replaying a request with one header changed |
| Counterfactual fairness | The decision stays the same in the counterfactual world. | Output independent of a flag that should not matter |
| Multiple causal worlds | Check fairness under several plausible causal graphs when unsure which is true. | Testing against several config environments |

Diagram ideas: law-school causal DAG (race, sex → GPA, LSAT → success); counterfactual swap illustration.
Scenario step: does pincode affect approval only through income (acceptable) or directly (not)?
Notebook idea: simulate a linear structural causal model in numpy, build a predictor from non-descendant parts, verify counterfactual invariance with an assert. CPU.
Production angle: DoWhy, causal reviews. Breaks: the assumed causal graph is wrong, so "fair" is fair only on paper.

### M6 · Fairness in NLP and computer vision (session 6) + disentangled fair representation (session 7)

Topics: biases in NLP models; data augmentation; debiasing word embeddings; counterfactual fairness; counterfactual face
attribution; gender-equalised image captioning; adversarial removal of gender features. Session 7 (not in the content
structure): disentangled representations, flexibly fair representation, orthogonal disentangled fair representations, measurements.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Embedding bias | Word vectors encode stereotypes, e.g. "nurse" closer to "she" than "he". | A default config that bakes in an old assumption |
| Hard debiasing | Find the gender direction in embedding space and remove it from neutral words. | Stripping one field from every record |
| Counterfactual data augmentation | Add copies of text with swapped gender terms to training data. | Adding mirrored test cases |
| Adversarial feature removal | Train an adversary to predict gender; train the encoder to make it fail. | Red team vs blue team on the same model |
| Disentangled representation | Separate vector parts for sensitive and non-sensitive factors. | Separating PII columns from business columns |

Diagram ideas: he-she axis projection of occupation words; encoder + task head + adversary head.
Scenario step: loan-purpose classifier treats "my wife's business" and "my husband's business" the same.
Notebook idea: GloVe 50-d via gensim downloader, measure occupation bias and apply hard debiasing; gender-swap test on a text classifier. CPU.
Production angle: counterfactual test suites for NLP. Breaks: debiasing hides bias from one metric while it persists in others.

### M7 · Interpretability and transparency (session 9)

Topics: ML interpretability; intrinsically interpretable models (simple models, interpretable deep techniques); intrinsic vs post-hoc; model-specific vs model-agnostic; local vs global; interpretability-performance trade-offs; instance-based learning.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Intrinsically interpretable model | A model simple enough to read: linear model, short tree, rule list. | Readable source code |
| Post-hoc explanation | Explaining a trained black-box model after the fact. | Reverse-engineering a binary |
| Model-agnostic | Works on any model by probing inputs and outputs. | Black-box API testing |
| Local vs global | Explain one prediction vs the model's overall behaviour. | One request's trace vs the system architecture |
| Accuracy-interpretability trade-off | Simpler readable models may lose some accuracy. | Readable code vs hand-optimised assembly |

Diagram ideas: 2 x 2 grid (intrinsic/post-hoc x local/global) with methods placed; depth-3 decision tree for credit.
Scenario step: compare a readable scorecard (logistic regression) with the boosted model's accuracy.
Notebook idea: logistic regression coefficients and a depth-3 tree on Adult vs gradient boosting: accuracy gap table. CPU.
Production angle: scorecards still used in credit. Breaks: a "readable" model with 200 features is not actually readable.

### M8 · Feature interaction for interpretability (session 10)

Topics: feature interaction; layer-wise relevance propagation (LRP); DeepLIFT; SHAP (coalitional games, Shapley values, Kernel SHAP, Deep SHAP, Tree SHAP); equitable value of data.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Shapley value | A feature's average contribution over all orders of adding features. | Fair credit split among teammates for a release |
| SHAP | Shapley-value explanations; per-prediction feature contributions that sum to the output. | An itemised bill for one prediction |
| Tree SHAP | Fast exact SHAP for tree models. | An optimised query for one database type |
| LRP / DeepLIFT | Pass relevance backwards through a network to inputs, relative to a reference. | Tracing blame upstream through a call stack |
| Feature interaction | Two features together affect output more than the sum of each alone. | Two config flags that only break together |
| Data Shapley | Shapley values applied to training examples to value each data point. | Measuring which tests catch the most bugs |

Diagram ideas: SHAP waterfall for one rejected applicant; Shapley worked example with 3 features (all 6 orderings).
Scenario step: every rejected applicant gets "top 3 reasons" from SHAP.
Notebook idea: lab 4 style: `shap.TreeExplainer` on the credit model (waterfall, beeswarm) and `lime` for the same applicant; compare. CPU.
Production angle: SHAP in model monitoring, adverse-action notices. Breaks: correlated features split credit oddly and explanations mislead.

### M9 · Example and visualisation based methods for interpretability (session 11)

Topics: example-based methods; counterfactual explanations (targeted, untargeted); contrastive examples; concept-based methods.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Counterfactual explanation | The smallest change to inputs that flips the decision. | "Change this one config value and the test passes" |
| Targeted vs untargeted | Flip to a specific class vs any different class. | Fixing to a specific version vs any working version |
| Contrastive example | Explain "why A and not B" by comparing with a similar case. | Diffing two similar requests |
| Prototype / example-based | Explain using representative training examples. | Linking to a known similar bug |
| Concept-based (TCAV) | Measure how much a human concept (e.g. "stripes") drives a prediction. | Tracing a business rule, not individual lines |

Diagram ideas: decision boundary with counterfactual arrow to the nearest point on the approved side; nearest prototypes grid.
Scenario step: "If your monthly income were ₹4,000 higher, the loan would be approved."
Notebook idea: `dice-ml` counterfactuals on the credit model; nearest-neighbour prototypes with sklearn. CPU.
Production angle: DiCE, Alibi. Breaks: counterfactual suggests changing age or gender, which is not actionable or lawful.

### M10 · Interpreting deep networks (session 12)

Topics: visualisation-based methods; activation visualisation; saliency maps; GoogLeNet activation atlas; gradient-based attribution; integrated gradients and their baselines.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Saliency map | Gradient of the output with respect to each pixel, showing sensitive regions. | A heat map of which inputs the code reads |
| Activation visualisation | Showing what a neuron or layer responds to. | Inspecting intermediate variables in a debugger |
| Integrated gradients | Average gradients along a path from a baseline image to the input. | Summing changes step by step from a blank state |
| Baseline choice | The "neutral" reference input (black image, blur); results depend on it. | The "before" snapshot in a diff |

Diagram ideas: saliency vs integrated gradients on the same image; baseline-to-input path drawn as frames.
Scenario step: confirm the KYC CNN looks at the face, not the background.
Notebook idea: lab 5 style: pretrained ResNet-18 (torchvision) + `captum` saliency and integrated gradients on a few images. CPU.
Production angle: Captum, Grad-CAM in model reviews. Breaks: saliency looks plausible even for a randomised model (sanity checks fail).

### M11 · Robustness and adversarial attacks / defence (sessions 13–14)

Topics: adversarial attacks; white-box evasion (FGSM, C&W, physical attacks); transferability; black-box evasion (Jacobian-based data augmentation); defences: adversarial training, input transformations, stochastic gradients, obfuscated gradients and BPDA; robust optimisation; certified defence.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Adversarial example | An input changed slightly, often invisibly, so the model gets it wrong. | A crafted payload that slips past validation |
| FGSM | Move each pixel a small step in the sign of the loss gradient. | One-shot fuzzing guided by the source code |
| White-box vs black-box | Attacker knows the model weights vs can only query it. | Code audit vs external pen test |
| Transferability | Attacks crafted on one model often fool another. | One exploit working on several similar servers |
| Adversarial training | Train on adversarial examples so the model resists them. | Adding exploit payloads to the test suite |
| Obfuscated gradients | Defences that hide gradients but are broken by approximations (BPDA). | Security through obscurity |
| Certified defence | Proves no attack within a size limit can change the prediction. | A formal verification guarantee |

Diagram ideas: panda + noise = gibbon style figure; attack taxonomy tree (white/black box, evasion/physical).
Scenario step: a doctored ID photo fools the KYC model; adversarial training closes the gap.
Notebook idea: lab 6 style: FGSM and PGD on a small MNIST CNN in torch (CPU, minutes); accuracy vs epsilon; one epoch of adversarial training. CPU.
Production angle: ART (Adversarial Robustness Toolbox), rate limits on model queries. Breaks: a defence tested only against FGSM falls to stronger attacks.

### M12 · ML auditing and privacy (sessions 14–15)

Topics: ML auditing; distill-and-compare; differential privacy with deep learning; model inversion attack and DP; local differential privacy; federated learning.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Distill-and-compare | Train a transparent student to mimic a black-box model, then compare with a model trained on true labels. | Rebuilding a service from its outputs to audit it |
| Differential privacy (DP) | Results barely change whether or not any one person's data is included. | Adding noise so no single row is identifiable |
| Epsilon (privacy budget) | How much privacy is spent; smaller epsilon = stronger privacy, less accuracy. | A rate limit on information leakage |
| DP-SGD | Clip each example's gradient and add noise during training. | Capping and blurring each contributor's influence |
| Model inversion | Recover training data features (e.g. faces) by querying a model. | Reconstructing a database from API responses |
| Local DP | Each user adds noise before sending data, so the server never sees raw values. | Client-side encryption |
| Federated learning | Train across devices; only updates leave the device. | Branches sending summaries, not raw files |

Diagram ideas: DP mechanism (true count + Laplace noise) with epsilon slider; federated round diagram.
Scenario step: audit report; train the credit model with DP-SGD and measure the accuracy cost.
Notebook idea: Laplace mechanism on counts in numpy; `opacus` DP-SGD on a small tabular MLP, accuracy vs epsilon; distill-and-compare with a tree student. CPU.
Production angle: Opacus, TensorFlow Privacy, Flower. Breaks: epsilon is reported per run but repeated retraining spends the budget many times.

## 5. Codebase plan

`quickloan-audit`: a reusable audit toolkit run against the QuickLoan models.

```
codebase/
├── README.md                   how to run; which module added which file           (M1)
├── data/load_adult.py          Adult Income loader + synthetic pincode feature      (M1, M2)
├── src/audit/
│   ├── baseline.py             train credit model + group metrics                  (M1)
│   ├── fairness.py             parity, equalised odds, PI metrics                  (M3)
│   ├── mitigate.py             reweighing, threshold optimiser, defer rule          (M4)
│   ├── text_bias.py            embedding bias + gender-swap test                    (M6)
│   ├── explain.py              SHAP, LIME, counterfactuals                          (M8, M9)
│   ├── vision.py               saliency + integrated gradients                      (M10)
│   ├── attacks.py              FGSM / PGD + adversarial training                    (M11)
│   ├── privacy.py              Laplace mechanism, DP-SGD wrapper                    (M12)
│   └── report.py               audit report (Markdown model card)                   (M12)
└── tests/
    ├── test_fairness.py        metrics on hand-built confusion matrices            (M3)
    ├── test_mitigate.py        parity gap shrinks after reweighing                 (M4)
    ├── test_explain.py         SHAP values sum to model output                     (M8)
    └── test_attacks.py         FGSM lowers accuracy; adversarial training recovers part (M11)
```

## 6. Practice topics plan

1. 01 FAccT overview and sources of bias — M1, M2 — 3 h
2. 02 Fairness metrics and the impossibility trade-off — M3 — 4 h
3. 03 Bias mitigation: pre, in and post-processing — M3, M4 — 4 h
4. 04 Causal and counterfactual fairness — M5 — 3 h
5. 05 Fairness in NLP and vision — M6 — 3 h
6. 06 Interpretable models and SHAP/LIME — M7, M8 — 5 h
7. 07 Counterfactual explanations — M9 — 3 h
8. 08 Explaining deep networks — M10 — 3 h
9. 09 Adversarial attacks and defences — M11 — 4 h
10. 10 Auditing, differential privacy and federated learning — M12 — 4 h

## 7. Exam signal

No past question papers in this folder. Evaluation scheme (handout):

| Component | Type | Weight |
|---|---|---|
| EC-1 Quiz (best 2 of 3) | Online, ~1 h | 10% |
| Assignment I | Take home, 2–3 weeks | 10% |
| Assignment II | Take home, 2–3 weeks | 10% |
| EC-2 Mid-Semester Test | Open book | 30% |
| EC-3 Comprehensive Exam | Open book | 40% |

Mid-sem = sessions 1–8 (fairness half: M1–M6 + disentangled representations); compre = all 16 sessions. Both are open
book, so expect applied questions: compute parity / equalised-odds gaps from a confusion matrix, Shapley values for 2–3
features, an FGSM step, a Laplace-mechanism noise scale.

## 8. Interview angle

1. **Demographic parity vs equalised odds?** Equal approval rates vs equal error rates (TPR and FPR) across groups.
2. **Why doesn't dropping the sensitive column fix bias?** Proxy features still carry the information.
3. **How does SHAP work?** Shapley values from game theory: average marginal contribution of a feature over all coalitions.
4. **LIME vs SHAP?** LIME fits a local linear surrogate on perturbations; SHAP has consistency guarantees and additive contributions.
5. **What is a counterfactual explanation?** The smallest actionable input change that flips the decision.
6. **What is FGSM?** One gradient-sign step of size epsilon that increases the loss; a fast adversarial attack.
7. **How do you defend against adversarial examples?** Adversarial training is the strongest practical defence; beware obfuscated-gradient defences.
8. **What does differential privacy guarantee?** Outputs are almost the same with or without any single individual's data, bounded by epsilon.
9. **Where would you put fairness checks in an ML pipeline?** Data audit, training metrics by group, pre-release gate in CI, post-deploy monitoring.
10. **Can a model be fair by all definitions?** Not when base rates differ between groups; choose the metric with stakeholders.

## 9. Repetition plan

| Concept | First met (module) | Revisited in (modules) |
|---|---|---|
| Sensitive feature / proxy | M2 | M3, M4, M5, M6 |
| Group fairness metrics | M3 | M4 (mitigation), M12 (audit) |
| Counterfactual | M5 | M6 (NLP/face), M9 (explanations) |
| Local vs global explanation | M7 | M8, M9, M10 |
| Gradient as sensitivity | M10 | M11 (FGSM uses the same gradient) |
| Adversary / adversarial training | M6 (feature removal) | M11 |
| Privacy | M1 | M12 |
| Human-in-the-loop | M4 (learning to defer) | M12 (auditing) |

## 10. Overlap with my other courses

- [../../natural-language-processing/](../../natural-language-processing/) — word embeddings (revision ch03) are the substrate for embedding-debiasing in M6.
- [../../software-engineering-for-machine-learning/](../../software-engineering-for-machine-learning/) — responsible-AI checks, model documentation and testing gates in the ML lifecycle.
- [../mlops/](../mlops/) — fairness and drift monitoring after deployment; model cards in the registry.
- [../ml-system-optimisation/](../ml-system-optimisation/) — federated learning appears there from the systems side (M3).

## 11. Build checklist

- [ ] SPEC reviewed
- [ ] cards.json (M1…M12, 5–7 cards each)
- [ ] practice/01 FAccT overview and sources of bias
- [ ] practice/02 Fairness metrics and the impossibility trade-off
- [ ] practice/03 Bias mitigation
- [ ] practice/04 Causal and counterfactual fairness
- [ ] practice/05 Fairness in NLP and vision
- [ ] practice/06 Interpretable models and SHAP/LIME
- [ ] practice/07 Counterfactual explanations
- [ ] practice/08 Explaining deep networks
- [ ] practice/09 Adversarial attacks and defences
- [ ] practice/10 Auditing, differential privacy and federated learning
- [ ] codebase/ runs + tests

Total estimated study hours: ≈ 36 h practice + ≈ 10 h codebase + ≈ 5 h cards/revision = **≈ 51 h**.
