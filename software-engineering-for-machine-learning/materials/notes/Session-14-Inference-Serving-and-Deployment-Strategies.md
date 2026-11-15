# Session 14 — Inference, Feature Encoding, Serving Infrastructure & Deployment Strategies

> **Module 6 · Lecture 14** · Slides: `Session 14.pptx`
>
> **One-line goal:** the four ways to **serve** a model, the four ways to **release** a new version with zero downtime, and how **MLOps / LLMOps / AgentOps** differ.

### Contents
1. [The model inference function](#1-the-model-inference-function)
2. [Feature encoding](#2-feature-encoding--and-the-skew-trap)
3. [Four designs for serving a model](#3-four-designs-for-serving-a-model-exam-favourite)
4. [Deployment strategies](#4-deployment-strategies--zero-downtime-releases-exam-favourite)
5. [MLOps vs LLMOps vs AgentOps](#5-mlops-vs-llmops-vs-agentops-exam-favourite)
6. [The metrics comparison table](#6-the-metrics-comparison-table)
7. [Recap](#-recap)

---

## 1. The model inference function

The **model inference function** is the **operational logic that transforms new input data into predictions using a trained model**.

> **Prediction = f(Input Features, Trained Model)**

| Term | Definition |
|---|---|
| **Input features** | the set of input variables (attributes) describing the **new data instance** for which a prediction is required |
| **Trained model** | the model whose parameters were **already learned during training**. **The model remains fixed during inference.** |
| **Prediction** | the output produced by the model for the given input |

> 💡 **"The model remains fixed during inference"** is the whole distinction between training and serving. Training *changes* the parameters; inference only *reads* them.

**Worked example — Iris flower classifier:**

```
Input                          Inference function                      Output
─────                          ──────────────────                      ──────
Sepal Length = 5.1     def predict_species(features):
Sepal Width  = 3.5         processed  = preprocess(features)    ──▶   Iris-setosa
Petal Length = 1.4         prediction = model.predict(processed)
Petal Width  = 0.2         return prediction
```

> 🎯 Note the shape: **preprocess → predict → return.** The preprocessing step is *part of the inference function*, not an afterthought.

---

## 2. Feature encoding — and the skew trap

**Feature encoding** is the process of **converting non-numerical (categorical or text) data into numerical values** so the model can understand and use it.

| Stage | Example |
|---|---|
| **Raw inputs** — user-provided | Sepal Length = 5.1 cm; Sepal Width = 3.5 cm … |
| **Feature encoding** — converted to a numerical vector the model can process | `[5.1, 3.5, 1.4, 0.2]` — the **feature vector** |

> ⚠️ **The single most important rule in this session:**
>
> **The feature-encoding code used for training must be the SAME code used for encoding runtime data during inference.**
>
> **It is useful to factor the shared code into a reusable library.**

> 🌍 **Why this bites so hard.** Training scales `income` by dividing by 100,000. The serving code, written three months later by someone else, divides by 1,000. Nothing crashes. No test fails. The model just quietly becomes wrong for every customer. This is called **training/serving skew**, and sharing one library is the standard cure.

### Common encodings

| Encoding | What it does | Use when |
|---|---|---|
| **One-hot** | one binary column per category | few, unordered categories (colour, city) |
| **Label / ordinal** | maps each category to an integer | categories have a genuine order (low/medium/high) |
| **Target/mean encoding** | replaces category with the mean target value | high-cardinality categories |
| **Embeddings** | learned dense vector per category/token | very high cardinality, text |
| **Scaling / normalisation** | rescales numeric ranges | models sensitive to magnitude |

---

## 3. Four designs for serving a model (exam favourite)

| # | Design | How it works | Example from the deck |
|---|---|---|---|
| **1** | **Model inference as a Library** | the model and inference function are **embedded as a local function or library in the target system**. The model is **loaded into memory** and inference is a **local function call**. | OCR models like **Tesseract** are available as libraries |
| **2** | **Model inference as a Service** (locally or in the Cloud) | a **dedicated server** responds to client requests via a **RESTful API**. Can be **replicated across several machines / VMs / containers in the cloud**. | **Iris model** inference deployed locally via a **FastAPI** interface |
| **3** | **Batch processing** | making predictions for **a large amount of data all at once**, instead of one record at a time. Approach: **move the model to the data, not the data to the model.** | **Netflix** periodically runs its recommendation model over **millions of users' viewing histories at once**, storing updated recommendations so they are ready when users log in the next day |
| **4** | **Cached predictions** | when predictions are **expensive but there are not many distinct inputs**, **cache or even precompute all predictions**. Inference reduces to **looking up a previous prediction in a database** — like translations for common words. | a video streaming platform classifies a movie **once**; *"Frozen"* is cached as a **"U" rating** |

### Choosing between them

| Choose | When |
|---|---|
| **Library** | low latency essential, no network hop wanted, model is small, one language |
| **Service** | multiple/heterogeneous clients, GPU needed, independent scaling and updates (the Session 11 argument) |
| **Batch** | predictions are needed *later*, not *now*; huge volume; data already sits in a warehouse |
| **Cached** | expensive model, **small set of distinct inputs**, results are stable over time |

> 🎯 **The deciding question is "when is the answer needed?"** — *right now, per request* → service or library. *Tomorrow morning, for everyone* → batch. *Right now, but I've computed it before* → cache.

---

## 4. Deployment strategies — zero-downtime releases (exam favourite)

These are the strategies organisations use in production to ensure **zero-downtime deployments**, also known as **hot deployment** — one in which the actual switching of users from one release to another happens **nearly instantaneously**.

The four: **Basic · Ramped · Blue/Green · Canary**.

### 1. Basic Deployment

**All nodes in a target environment are updated at the same time** with the new service or artifact version.

- ❌ Because of this, basic deployments are **not outage-proof** and they **slow down rollback**.
- ✅ **Preferable only for very small applications/services.**

```
before:  [v1][v1][v1][v1]
after:   [v2][v2][v2][v2]     ← all at once
```

### 2. Ramped (rolling-update / incremental)

**Slowly replaces one node at a time to avoid downtime.** Version 2 is gradually rolled out, replacing version 1. Running instances are **incrementally updated in batches**.

> 💡 **This is the default deployment strategy in Kubernetes.**

```
[v1][v1][v1][v1]
[v2][v1][v1][v1]
[v2][v2][v1][v1]
[v2][v2][v2][v2]
```

| Pros | Cons |
|---|---|
| relatively **simple to roll back** | since nodes are updated in batches, it **requires services to support both new and old versions** of the artifact simultaneously |
| **less risky than a basic deployment** | **verification at every incremental change makes it slow** |

### 3. Blue / Green

Release a new version **while the current version is still running**. Version 2 is deployed **alongside** version 1, then **traffic is switched** to version 2.

It uses **two identical environments**: a **"blue"** (staging) and a **"green"** (production) environment holding different versions. **QA and user-acceptance testing** happen in the **blue** environment that hosts the new changes. Once tested and accepted, **user traffic is shifted from green to blue**.

```
        ┌─────────┐
users ─▶│ GREEN v1│  (live)
        └─────────┘
        ┌─────────┐
        │ BLUE v2 │  (QA + UAT here)
        └─────────┘
                       ── flip the router ──▶ users now hit BLUE
```

| Pros | Cons |
|---|---|
| **simple, fast, well-understood, easy to implement** | **cost** — replicating a production environment is **complex and expensive**, especially with microservices |
| **rollback is straightforward** — just flip traffic back to the old environment | **QA and UAT may not identify all anomalies or regressions**, and **shifting all user traffic at once presents risk** |
| **not as risky** as other strategies | |

### 4. Canary

**Allow customers to test your deployment by releasing the new version to a small group of them.** Version 2 goes to a **subset of users**, then proceeds to a **full rollout**.

> 🧪 **Example:** Facebook releases a new feature **only to the Asia-Pacific region**; if successful, it rolls out to other regions.

```
 95% users ──▶ [v1]
  5% users ──▶ [v2]   ← healthy? expand to 25%, 50%, 100%. Sick? route back to v1.
```

> 🌍 **Why "canary"?** Miners carried a canary into the shaft — if the bird stopped singing, the air was bad and everyone got out. The canary group is the early-warning bird.

### The comparison table to memorise

| Strategy | Update pattern | Downtime | Rollback | Cost | Risk |
|---|---|---|---|---|---|
| **Basic** | all nodes at once | possible outage | **slow** | lowest | **highest** |
| **Ramped** | one node/batch at a time | none | relatively simple | low | medium — **both versions must coexist** |
| **Blue/Green** | full parallel environment, then switch | none | **easiest — flip back** | **highest (2× env)** | medium — all users move at once |
| **Canary** | small subset, then expand | none | easy — reroute the subset | medium | **lowest** |

> 🎯 **How to answer a "which strategy?" question:** name the constraint the scenario gives you. *Cheap and tiny app* → Basic. *Kubernetes default, no extra infra* → Ramped. *Need an instant, clean rollback and can afford two environments* → Blue/Green. *Unproven model, want real users but limited blast radius* → **Canary**.

---

## 5. MLOps vs LLMOps vs AgentOps (exam favourite)

### MLOps — Machine Learning Operations

**Core focus: predictive models.** Applies **DevOps principles to traditional ML systems** and smaller, task-specific models (regression, classification, recommendation). It manages the **end-to-end lifecycle of data, code and model artifacts**.

| Aspect | Detail |
|---|---|
| **Data type** | highly **structured, numerical or tabular** |
| **Key challenges** | managing **feature stores**, preventing **data and model drift** (real-world data no longer matching training data), **retraining pipelines** |
| **Success metrics** | **F1-score, accuracy, precision, recall, latency** |
| **Tools** | **MLflow, SageMaker Pipelines, Databricks, Apache Airflow, Prefect / Prefect Cloud, Kubeflow Pipelines** |

### LLMOps — Large Language Model Operations

**Core focus: language and generation.** Emerged to handle **foundation models and generative AI**. Instead of training from scratch on tabular data, it focuses on **adapting and grounding pre-trained models** using **prompt engineering** and **RAG**.

| Aspect | Detail |
|---|---|
| **Data type** | **unstructured text, documents, vector embeddings** |
| **Key challenges** | **prompt versioning**, managing **hallucinations**, **context-window management**, **optimising token costs** |
| **Success metrics** | **hallucination rates, toxicity/bias measurement, coherence, token usage, latency** |
| **Tools** | **LangChain, LlamaIndex, Weights & Biases, PromptLayer** |

### AgentOps — Agent Operations

**Core focus: autonomous execution and decisions.** The **newest and most complex frontier** — manages **autonomous, long-running AI agents** that don't just generate text but **reason, plan, use tools and make decisions** to complete complex goals.

| Aspect | Detail |
|---|---|
| **Data type** | **real-time execution states, API interactions, environment variables** |
| **Key challenges** | tracking **multi-step reasoning traces**, managing **agent memory**, **authorising tool usage**, handling **infinite loops**, implementing safe **human-in-the-loop (HITL) guardrails** |
| **Success metrics** | **goal achievement, task success rates, tool-call correctness** |
| **Tools** | **LangGraph, CrewAI, AutoGen**, and dedicated AgentOps tracking platforms |

> 🎯 **The progression in one line:** *MLOps ships a **number**, LLMOps ships **text**, AgentOps ships an **action** — and each step makes the thing harder to verify.*

---

## 6. The metrics comparison table

*(The deck's full table — the most likely source of a "compare these three" question.)*

| Category | **MLOps** (predictive models) | **LLMOps** (large language models) | **AgentOps** (AI agents) |
|---|---|---|---|
| **Primary goal** | accurate predictions | high-quality text generation | successful autonomous task execution |
| **Model quality metrics** | Accuracy, Precision, Recall, F1, ROC-AUC, RMSE, MAE | BLEU, ROUGE, BERTScore, Exact Match, Semantic Similarity, Hallucination Rate | Task Success Rate, Goal Completion Rate, Decision Accuracy |
| **Operational metrics** | Inference latency, throughput, model drift, data drift | Token latency (TTFT, tokens/sec), response time, cost per request, token usage | End-to-end task latency, workflow completion time, agent utilisation |
| **Reliability metrics** | Model availability, prediction error rate | Response consistency, hallucination rate, safety violations | Task failure rate, recovery rate, retry success rate |
| **Data metrics** | Data quality, missing values, feature drift, data freshness | Prompt quality, context-window utilisation, retrieval accuracy (RAG) | Memory retrieval accuracy, context retention, knowledge freshness |
| **Efficiency metrics** | CPU/GPU utilisation, batch throughput | Token consumption, cost per 1K tokens, GPU utilisation, cache hit rate | Number of tool calls, planning efficiency, resource utilisation |
| **User-centric metrics** | Prediction accuracy, business KPIs | User satisfaction, helpfulness, relevance, human evaluation scores | User task success, satisfaction, **number of human interventions** |
| **Monitoring focus** | model degradation and data drift | prompt performance, hallucinations, token usage, response quality | agent reasoning, planning, tool usage, memory, collaboration, task execution |

*(demo: **Pima-MLOps Simulator**, code `PIMA-MLOPS-SIMULATOR`)*

---

## 🎯 Recap

- **Inference function:** **Prediction = f(input features, trained model)**; the model is **fixed during inference**. Shape: **preprocess → predict → return**.
- **Feature encoding** turns categorical/text data into numbers. **The encoding code used at training MUST be the same code used at inference** — factor it into a **shared library** or you get training/serving skew.
- **Four serving designs:** **Library** (embedded, local call — Tesseract) · **Service** (REST API, replicable in cloud — FastAPI Iris) · **Batch** (predict for everyone at once; *move the model to the data* — Netflix) · **Cached** (precompute/look up; few distinct inputs — *Frozen* → "U").
- **Four deployment strategies (zero-downtime / hot deployment):** **Basic** (all at once, not outage-proof, small apps only) · **Ramped** (one node at a time, **Kubernetes default**, needs both versions to coexist) · **Blue/Green** (two identical environments, QA/UAT in blue, flip traffic; easiest rollback but **expensive**) · **Canary** (small subset first, then full rollout; **lowest risk**).
- **MLOps** = predictive models, tabular data, drift & feature stores, F1/accuracy, MLflow/Airflow/Kubeflow.
- **LLMOps** = generation, unstructured text & embeddings, prompt versioning/hallucination/context window/token cost, LangChain/LlamaIndex/W&B/PromptLayer.
- **AgentOps** = autonomous action, execution states & tool calls, reasoning traces/memory/tool authorisation/infinite loops/**HITL guardrails**, LangGraph/CrewAI/AutoGen.

⬅️ **Prev:** [Session 13 — Deployment, Docker & Kubernetes](Session-13-Deployment-Docker-and-Kubernetes.md) · ➡️ **Next:** [Session 15 — Responsible ML Engineering](Session-15-Responsible-ML-Engineering.md) · 🏠 [Back to index](README.md)
