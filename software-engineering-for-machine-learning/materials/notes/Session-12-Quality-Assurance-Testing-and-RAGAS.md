# Session 12 — Quality Assurance: Testing, Data/Model/Pipeline Quality, Security & RAGAS

> **Module 5 · Lecture 12** · Slides: `Session 12.pptx`
>
> **One-line goal:** in ML you cannot test only the code — you must test the **data**, the **model**, the **pipeline** and the **system**, and keep testing **in production**.

### Contents
1. [OOP in Agentic AI — the Hollywood analogy](#1-oop-in-agentic-ai--the-hollywood-analogy)
2. [Traditional testing vs ML testing](#2-traditional-testing-vs-ml-testing-exam-favourite)
3. [Types of tests](#3-types-of-tests)
4. [The MLOps control loop](#4-the-mlops-control-loop)
5. [Data quality](#5-data-quality)
6. [Pipeline quality & CI for ML](#6-pipeline-quality--ci-for-ml)
7. [Model quality & metrics](#7-model-quality--metrics)
8. [Slicing & subpopulation testing](#8-slicing--subpopulation-testing)
9. [System quality, telemetry & monitoring](#9-system-quality-telemetry--monitoring)
10. [Testing in production](#10-testing--experimentation-in-production)
11. [Security for ML](#11-security-for-machine-learning)
12. [RAGAS](#12-ragas--evaluating-rag-systems-exam-favourite)
13. [Recap](#-recap)

---

## 1. OOP in Agentic AI — the Hollywood analogy

*(Carried over from Session 10 — the deck opens by finishing that thread.)*

> 🌍 **The core analogy: "The Hollywood Production Crew".**
>
> **The procedural approach (one giant loop):** a movie set where a **single director does everything** — holds the camera, applies makeup, writes the script line by line, adjusts lighting, sweeps the floor. If the lighting breaks, the director stops directing to change a bulb. That is what a **monolithic procedural script with dozens of `if/else` statements** guiding an LLM through a complex workflow looks like: **fragile, impossible to scale, crashes on minor changes.**
>
> **The OOP approach (the collaborative crew):** build a professional crew. Define a base role — **"Crew Member" = the base `Agent` class**. Every crew member has a name, a paycheck and an assignment. From this you hire specialised roles through **inheritance**:
> - the **"Director"** (`ValidationAgent`) checks if the scene is good
> - the **"Writer"** (`SummaryAgent`) compiles the script
> - the **"Cinematographer"** (`FormattingAgent`) styles the visual output
>
> Each worker operates in their **own bubble (encapsulation)**, keeping their own tools and notes. When the workflow runs (**composition**), the Executive Producer merely tells everyone to **"Execute!" (polymorphism)**. To add a "Sound Engineer" you **don't rewrite the movie set** — you spawn a new subclass and plug it into the coordinator.

---

## 2. Traditional testing vs ML testing (exam favourite)

**Shifting the paradigm:**

| | **Traditional software** | **Machine learning** |
|---|---|---|
| Where the logic lives | **explicitly programmed** by a developer | **learned from data** |
| What tests verify | whether the logic produces **expected outputs** | the **learning process**, the **data integrity**, and the **statistical outputs** |
| Failure modes | **bugs** | **concept drift**, **data corruption**, **biased training data** |
| Correctness | deterministic — same input, same output, forever | statistical — "good enough on average", and it **decays over time** |

> 💡 **The one-line reason ML testing is harder:** in traditional software the specification is in the code, so you can read it. In ML the specification is in the *data*, so you have to **test the data** to test the system.

---

## 3. Types of tests

### The traditional pyramid (still applies)

| Test type | Scope |
|---|---|
| **Unit** | one function/class in isolation |
| **Integration** | two or more components talking to each other |
| **System / End-to-end** | the whole application through its real interfaces |
| **Acceptance** | does it satisfy the stated requirement? |
| **Regression** | did a change break something that used to work? |

### ML-specific testing dimensions

| Dimension | What it validates |
|---|---|
| **Data tests** | validate **schemas**, check for **missing values**, monitor **feature distributions** |
| **Model tests** | evaluate **predictive performance**, **fairness**, and **robustness against edge cases** |
| **Infrastructure tests** | stress-test the **serving APIs** and measure **inference latency** |
| **Heuristic tests** | check the model obeys **common-sense rules** (e.g. *age cannot be negative*) |

> 🎯 Four words to recall this: **Data · Model · Infrastructure · Heuristic.**

---

## 4. The MLOps control loop

Read left to right, and notice that the last box feeds the first:

```
   Data ──▶ Features ──▶ Training ──▶ Registry ──▶ Serving ──▶ Monitoring
     ▲                                                             │
     └──────────────── triggers the next retraining ◀──────────────┘
```

> 💡 **Takeaway from the slide:** data flows into features, then training, then the registry, then serving, and finally **monitoring — which triggers the next retraining loop.** ML systems are not shipped once; they are **circulated**.

---

## 5. Data quality

> 🌍 **Garbage In, Garbage Out.**

| Statement from the deck | Why it matters |
|---|---|
| **Data quality dictates the upper bound of model performance** | no architecture rescues bad labels |
| **Historical data may contain human biases that the model will amplify** | the model learns the past, including its prejudices (see Amazon recruiting, Session 15) |
| **Errors in data-collection pipelines silently degrade production systems** | *silently* — no crash, no alert, just a metric drifting down |
| **Automated data validation is a strict requirement before any training begins** | validation is a **gate**, not a suggestion |

### Dimensions of data quality

| Dimension | Question it answers |
|---|---|
| **Accuracy** | do the values reflect reality? |
| **Completeness** | are required fields present, or missing? |
| **Consistency** | do the same facts agree across sources/tables? |
| **Timeliness / Freshness** | is the data recent enough to be relevant? |
| **Validity** | does it conform to the schema, types and allowed ranges? |
| **Uniqueness** | are there duplicate records inflating the signal? |

### The data validation pipeline

Automatic checks **before training and before serving** prevent silent failures:

```
Ingestion ──▶ Schema Check Gate ──▶ Value Check Gate ──▶ Label Health Gate ──▶ Action Gateway
 (product      (missing columns,     (impossible ranges    (extreme class        (halt the
  events,       type changes)         e.g. negative age,    imbalance, missing     pipeline if
  IoT, CRM)                           statistical outliers) target labels)         checks fail)
```

| Stage | Checks for |
|---|---|
| **Ingestion** | raw data arrives from product events, IoT streams, CRM tools |
| **Schema Check Gate** | **missing columns** or **type changes** |
| **Value Check Gate** | **impossible ranges** (e.g. negative age) and **statistical outliers** |
| **Label Health Gate** | **extreme class imbalance** or **missing target labels** |
| **Action Gateway** | if inputs do not match expectations, **the pipeline automatically halts** |

*(code: `data_validation.py`)*

> 🎯 **The gate must be able to stop the train.** A validation check that only logs a warning is not a gate.

---

## 6. Pipeline quality & CI for ML

**Definition:** pipeline quality is *the robustness of the automated sequence from data extraction to model deployment.*

| Property | Meaning |
|---|---|
| **Idempotency** | **re-running a pipeline with the same inputs must yield the exact same outputs** |
| **Version control** | **code, data and model artifacts must be explicitly linked and versioned together** |
| **Orchestration** | tools like **Airflow** or **Kubeflow** manage complex dependency graphs |

> 🌍 **Idempotency, everyday version.** Pressing a lift's call button five times summons one lift, not five. A pipeline should behave the same way — running it twice must not double-write, double-count or produce a different model.

### Continuous Integration in the ML context

| Trigger | What CI does |
|---|---|
| **Code commits** | run automated **syntax and unit tests** |
| **Changes to model architecture** | trigger **training on a small, synthetic dataset** (fast smoke-test that training still runs) |
| **Data schema updates** | trigger **validation checks against historical datasets** |
| **All tests pass** | produce a **deployable artifact stored in a central registry** |

---

## 7. Model quality & metrics

**Beyond simple accuracy:**

- **Accuracy is often misleading, especially on highly imbalanced datasets.**
- Model quality includes **interpretability, fairness and computational efficiency** — not just a score.
- Evaluating quality requires testing on data **strictly unseen during training**.
- **Quality degrades over time**, requiring **continuous validation**.

> ⚠️ **The imbalance trap.** If 1 in 1,000 transactions is fraud, a model that predicts "not fraud" every single time is **99.9% accurate** and **completely worthless**. This is exactly why precision/recall exist.

### The metrics

Start from the confusion matrix: **TP** (true positive), **FP** (false positive), **FN** (false negative), **TN** (true negative).

| Metric | Formula | Answers |
|---|---|---|
| **Precision** | **TP / (TP + FP)** | of everything I *flagged*, how much was right? → the **accuracy of positive predictions** |
| **Recall** | **TP / (TP + FN)** | of everything that *was* positive, how much did I catch? → the **ability to find all positive instances** |
| **F1-Score** | 2·(P·R)/(P+R) | **balances precision and recall for imbalanced data** |
| **RMSE** | √(mean of squared errors) | regression error, and it **penalises large errors heavily** |

> 🌍 **Which one do you optimise?**
> - **Spam filter** → optimise **precision**. A false positive buries a real email.
> - **Cancer screening** → optimise **recall**. A false negative sends a sick patient home.
> - **Can't choose / imbalanced** → **F1**.

---

## 8. Slicing & subpopulation testing

> 🧪 **The headline finding:** *a model with **95% global accuracy** might have **50% accuracy on a minority demographic**.* The average hides the failure.

| Step | What it means |
|---|---|
| **Data slicing** | divide the test set into distinct subgroups — e.g. by **gender, location, or device type** |
| **Critical evaluation** | calculate performance metrics **independently for each slice** |
| **Actionable insight** | identify the specific areas where the model needs **active mitigation or retraining** |

*(code: `slicing_subpopulation_testing.py`)*

> 🎯 **Never report a single aggregate number.** An average is a place for failures to hide. This is also the operational link to **fairness** (Session 15).

---

## 9. System quality, telemetry & monitoring

### System quality — the holistic view

- **The ML model is only a small fraction of the total system — often <5% of the codebase.**
- System quality encompasses **UI/UX, database reliability, and network stability**.
- **A perfect model with a failing front end results in zero business value.**
- Requires **cross-functional collaboration** between data scientists and software engineers.

### Telemetry & monitoring — observability in production

| Layer | What you watch | Examples |
|---|---|---|
| **System metrics** | the machine | CPU usage, memory consumption, network latency |
| **Model metrics** | the predictions | prediction **distribution**, **confidence scores**, anomaly rates |
| **Business metrics** | the outcome | click-through rate, conversion rate, revenue impact |
| **Alerting** | the response | automated thresholds that **page engineers** when metrics deviate significantly |

> 💡 **Why watch the prediction *distribution* and not just accuracy?** In production you usually don't have labels yet — nobody has told you if yesterday's prediction was right. But you *can* see that the model suddenly predicts "approve" 90% of the time when it used to be 60%. **A shifted distribution is the earliest available symptom of drift.**

---

## 10. Testing & experimentation in production

**Why offline testing isn't enough:**

- **Offline data is static; user behaviour is dynamic and constantly changing.**
- **Models change user behaviour**, creating **feedback loops that offline tests cannot simulate**.
- Production experimentation provides the **final, undeniable proof of business impact**.
- It requires **robust infrastructure to route traffic securely**.

> 🌍 **The feedback loop, concretely.** A recommender starts pushing action films. Users watch more action films. The next training run sees "users love action films" — a preference the model *created*, not discovered. No offline test can catch that, because offline data never reacts to you.

### Traffic routing: A/B vs Shadow vs Canary (exam favourite)

| Strategy | Who sees the new model | Real user impact if it's bad | Best for |
|---|---|---|---|
| **Shadow** | **nobody** — the new model receives a **copy** of live traffic, its predictions are logged but **not served** | **none** | validating correctness/latency at full production load, risk-free |
| **A/B test** | a **split** of users (e.g. 50/50), each group served a different version | half your users | **statistically comparing business impact** of two versions |
| **Canary** | a **small subset** first (e.g. 5%), expanded if healthy | limited to the canary group | **safe progressive rollout** with fast rollback |

> 🎯 **Shadow answers "does it work?" · Canary answers "is it safe to expand?" · A/B answers "is it better?"**

---

## 11. Security for Machine Learning

**The new attack surface:**

- ML models introduce **unique vulnerabilities distinct from traditional web applications**.
- Attackers can manipulate **the training data** or **the inference requests**.
- Security must defend both the **intellectual property (the model weights)** and **data privacy**.
- **Threat modelling must be integrated early in the ML lifecycle.**

### The lifecycle-centric threat landscape

Threat actors target **different phases** of the ML lifecycle:

| Lifecycle phase | Representative attack | What it does |
|---|---|---|
| **Data collection** ⚠️ | **Data poisoning** | attacker injects crafted samples into training data to corrupt or backdoor the model |
| **Training** | **Backdoor / trojan** | model behaves normally except on a secret trigger input |
| **Model storage** | **Model theft / extraction** | weights stolen directly, or reconstructed by querying the API repeatedly |
| **Inference / Deployment** ⚠️ | **Adversarial examples** | tiny, often invisible input perturbations flip the prediction |
| **Inference** | **Membership inference** | attacker determines whether a specific person's record was in the training set |
| **LLM serving** | **Prompt injection** | malicious instructions hidden in input or retrieved documents hijack the model |

> ⚠️ **Slide note:** **data collection and deployment phases are frequently the most targeted entry points** for threat actors — the two ends of the pipeline, where external input enters.

---

## 12. RAGAS — evaluating RAG systems (exam favourite)

**RAG** = **Retrieval-Augmented Generation**: combining LLMs with external databases.

**The problem:** traditional metrics (**BLEU, ROUGE**) are **inadequate for measuring hallucination and context relevance** — they compare word overlap with a reference answer, which says nothing about whether the answer was *made up*.

**RAGAS** = **Retrieval Augmented Generation Assessment**.
**Objective:** an automated framework using an **LLM evaluator** to score the **distinct components** of a RAG pipeline **without human labels**.

### The two-pipeline architecture

Every RAG system has **two distinct paths that must be optimised and evaluated independently**:

```
                     ┌─────────────────────────────┐
   question ────────▶│  RETRIEVER (vector search)  │──▶ retrieved context
                     └─────────────────────────────┘            │
                                                                ▼
                     ┌─────────────────────────────┐
                     │  GENERATOR (the LLM)        │──▶ answer
                     └─────────────────────────────┘
```

### The four core metrics

| Evaluates | Metric | Measures |
|---|---|---|
| **Generator (the LLM)** | **Faithfulness** | is the generated answer **strictly grounded in the retrieved context**? → **detects hallucination** |
| **Generator** | **Answer Relevance** | how well the answer **directly addresses the user's initial prompt** |
| **Retriever (vector search)** | **Context Precision** | are the top retrieved chunks **highly relevant**, rather than just noise? |
| **Retriever** | **Context Recall** | did retrieval **fetch all the necessary facts** required to answer the question? |

**Measurement tool:** RAGAS uses **foundation models as an automated judge** to score these dimensions.

> 🎯 **The balance, in the deck's words:** *high **precision** means no junk data; high **recall** means no missing facts.*

> 💡 **Diagnostic use — this is the exam angle.** If the answer is wrong, the four metrics tell you *which half to fix*:
> - **Low context recall** → the retriever never fetched the fact. Fix **retrieval** (chunking, embeddings, top-k).
> - **Good context, low faithfulness** → the fact was right there and the LLM invented something else. Fix the **generator** (prompt, model).
> - **Low context precision** → too much noise crowding the context window.
> - **Low answer relevance** → the answer is true but doesn't answer the question asked.

*(code: `RAGAS_demo.py`)*

---

## 🎯 Recap

- **Traditional vs ML testing:** logic is *programmed* vs *learned*; tests verify *outputs* vs *the learning process, data integrity and statistical outputs*; failure from *bugs* vs **concept drift, data corruption, biased training data**.
- **Four ML test dimensions:** **Data · Model · Infrastructure · Heuristic.**
- **MLOps loop:** Data → Features → Training → Registry → Serving → **Monitoring → back to retraining.**
- **Data quality** sets the **upper bound** of performance; validate at four gates — **Schema · Value · Label Health · Action (halt)**.
- **Pipeline quality:** **idempotency** (same inputs → same outputs), **version code+data+model together**, orchestrate with **Airflow/Kubeflow**.
- **Model quality:** accuracy misleads on imbalanced data. **Precision = TP/(TP+FP)** · **Recall = TP/(TP+FN)** · **F1** balances them · **RMSE** penalises large errors.
- **Slicing:** 95% global accuracy can hide **50% on a minority group**. Always evaluate per slice.
- **System quality:** the model is **<5% of the codebase**; a perfect model behind a broken front end is worth **zero**.
- **Monitoring layers:** System · Model · Business · Alerting.
- **Production experimentation:** **Shadow** (no user impact) · **Canary** (small subset, then expand) · **A/B** (split traffic to compare).
- **ML security:** poisoning, backdoors, model theft, adversarial examples, membership inference, prompt injection — **data collection and deployment are the most-targeted phases**.
- **RAGAS:** BLEU/ROUGE can't measure hallucination. Four metrics — generator: **Faithfulness, Answer Relevance**; retriever: **Context Precision, Context Recall** — scored by an **LLM judge, no human labels**.

⬅️ **Prev:** [Session 11 — Errors, Style, Refactoring, APIs & Packaging](Session-11-Errors-Style-Refactoring-APIs-and-Packaging.md) · ➡️ **Next:** [Session 13 — Deployment, Docker & Kubernetes](Session-13-Deployment-Docker-and-Kubernetes.md) · 🏠 [Back to index](README.md)
