# Session 4 — Quality Attributes & System Architecture

> **Module 3 · Lecture 4** · Slides: `Session 04 - Quality Attributes & System Architecture.pptx` · Companion: `friend notes/6.pdf`
>
> **One-line goal:** the *how well*, not just the *what* — specify **quality attributes** and start **thinking like a software architect**.

### Contents
1. [A tale of two launches](#1-a-tale-of-two-launches)
2. [What is a quality attribute?](#2-what-is-a-quality-attribute)
3. [Make them SMART](#3-make-them-smart)
4. [Quality attributes unique to ML](#4-quality-attributes-unique-to-ml)
5. [What software architecture is](#5-what-software-architecture-is)
6. [Thinking like a system architect](#6-thinking-like-a-system-architect)
7. [Architectural patterns & Pipe-and-Filter](#7-architectural-patterns--pipe-and-filter)
8. [Recap](#-recap)

---

## 1. A tale of two launches

Two big systems, same stress, opposite outcomes:

| | **Flipkart** Big Billion Day (2014) | **Hotstar** (2019, Cricket WC semi-final) |
|---|---|---|
| Load | 3 lakh orders in 6 hours | **25 million** concurrent viewers |
| Outcome | ❌ Site crashed, carts emptied, money debited without orders | ✅ No meltdown |

**What did Hotstar do right / Flipkart do wrong?** Two reasons:
1. Identified the key **quality attributes** (scalability, performance).
2. Got the **system architecture** right (microservices, Kubernetes).

> 💡 Both systems had the same **features** (catalogue, cart, checkout / player, feed). What separated them was **how well** those features held up under load. That "how well" is **quality attributes**, and **architecture is how you deliver them** — won or lost at the architecture level, not in feature code.

---

## 2. What is a quality attribute?

A **quality attribute (QA)** — a.k.a. **non-functional requirement** — is a *measurable, testable property* describing **how well** a system meets a stakeholder need along one dimension. It always **qualifies a function**; it never stands alone.

> *"A measurable or testable property that specifies how well a system meets the needs of its stakeholders along a specific dimension of interest."* — Bass, Clements & Kazman, *Software Architecture in Practice*.

Classic QAs: **performance** (latency, throughput), **scalability**, **availability**, **reliability**, **security**, **modifiability**, **usability**, **testability**.

- *Function:* "check out the cart."
- *+ Quality:* "check out in under 2 seconds for 99% of requests at 10k concurrent users."

> 🌍 Buying a car: the **function** is "it drives." The **QAs** are the spec-sheet numbers — 0–100 in 8 s (performance), 5-star crash rating (safety), 18 km/l (efficiency). Two cars that both "drive" are separated entirely by these numbers.

---

## 3. Make them SMART

"The system should be fast" **cannot be tested**, so it cannot be engineered. A good QA is **SMART**:

| Letter | Meaning |
|--------|---------|
| **S**pecific | Names the exact property & condition |
| **M**easurable | Attaches a number / metric |
| **A**ttainable | Realistic for the system & budget |
| **R**elevant | Matters to a real stakeholder need |
| **T**ime-sensitive | States the window / condition it holds under |

> 🧪 **Turning a wish into a testable QA.** "The system should be reliable" → *specific*: checkout. *measurable*: 99.95% of checkout requests succeed. *attainable*: yes, with redundancy + retries. *relevant*: failed checkouts lose revenue. *time-sensitive*: measured monthly, during peak-sale windows. → **"99.95% of checkout requests succeed each month, including peak-sale windows"** — monitorable, alertable, contract-able. The original is none of these.

**Food-delivery app examples (Swiggy/Zomato):** Performance — menus load < 2 s, order placed < 3 s for 95% of requests. Availability — 99.95% uptime. Usability — ≥ 90% place an order unaided. Scalability — up to 10M requests/s at peak. Interoperability — 99% successful integration with Razorpay/Maps. Reliability — 99.9% order accuracy.

> ⚠️ Vague qualities ("reliable", "scalable", "user-friendly" with **no number**) are worthless — they can't be verified or held to. Always attach a **metric, target, and condition**.

---

## 4. Quality attributes unique to ML

ML systems inherit all classic QAs **and add their own**. What to specify depends on the **problem type** (classification/regression/detection/recommendation), the **approach** (deep learning / classical ML / RAG), the **training method**, and **data quality**.

| ML-specific QA | Meaning |
|----------------|---------|
| **Accuracy** | How correctly the model predicts/classifies |
| **Robustness** | Holds up on noisy / incomplete / adversarial inputs (fraud model works with missing data; self-driving vision works in rain/fog; ASR works with background noise) |
| **Explainability** | Can a prediction be justified to a user or regulator? |
| **Fairness** | Comparable performance across demographic groups (unbiased) |
| **Security & privacy** | Resist data leakage, model theft, poisoning |
| **Data-drift adaptability** | Detect & adapt to changing input patterns over time |
| **Model-drift monitoring** | Track performance degradation after deployment |
| **Reproducibility** | Same data + code + config → same model |
| **Maintainability / Scalability / Reliability** | Update easily / handle growing load / consistent under varied conditions |

> 🎯 For ML, **"accuracy" is necessary but nowhere near sufficient.** Robustness, explainability, fairness, privacy, drift-adaptability and reproducibility are **first-class** QAs — each must be made SMART just like latency.

> 💡 **Fraud-detection case study QAs:** accuracy, fast inference latency (real-time approval), scalability for huge transaction volumes, adaptability to changing fraud patterns, explainability + monitoring, privacy vs operating-cost trade-offs, reliability of infrastructure. *At this stage we identify **what** QA is relevant — not **how** to implement it.*

---

## 5. What software architecture is

> **IEEE:** *"The structure(s) of a system — its software elements, their externally visible properties, and the relationships among them."*
> Keywords: **Structure · System · Elements · Relationships · Design & Evolution**.

A **system architecture** is broader: **hardware + software + AI/ML + infrastructure + communication** together.

> 💡 Architecture = the decisions that are **expensive to change later** — how the big pieces are divided and how they talk. You choose it to make your important QAs *easy* and the forbidden ones *hard*.

**Example — RAG-based enterprise chatbot architecture:**

| Layer | Components |
|-------|-----------|
| Hardware / Infra | Cloud servers, GPU instances, storage |
| Software | Authentication service, API gateway, orchestration layer |
| **ML** | Embedding model, retriever, LLM, re-ranking model |
| Data | Vector DB, document store, logging DB |
| Deployment | Docker, Kubernetes, CI/CD pipeline |

---

## 6. Thinking like a system architect

| Principle | What it means |
|-----------|---------------|
| **Think beyond the ML model** | Consider APIs, DBs, workflows, UI, monitoring, infra *together* with the model |
| **Focus on system-level QAs** | Scalability, latency, reliability, security, explainability, cost — from the start |
| **Separate ML & non-ML responsibilities** | ML = prediction/inference; non-ML = orchestration, validation, business logic, UI, logging |
| **Architect for uncertainty & failure** | Models are probabilistic — add monitoring, fallbacks, human oversight, guardrails |
| **Balance experimentation with structure** | Allow experiments, but keep a stable, deployable structure |
| **Design for continuous evolution** | Support retraining, deployment automation, monitoring, version management |
| **Relate data, models & users** | Architecture shapes data flow, prediction quality, explainability, user trust |
| **Enable interdisciplinary collaboration** | A common structure for data scientists, engineers, domain experts, ops |

> 💡 **Quality requirements *drive* architecture design** — that is the architect's core job.

---

## 7. Architectural patterns & Pipe-and-Filter

An **architectural pattern** = a general, reusable solution to a recurring problem in a context. Expressed as a triple **{Context, Problem, Solution}** with defined roles.

> 🌍 A pattern outside software: NSP classroom (context) needs to schedule classes/exams (recurring problem) → solution: a **timetable**. In software, **MVC** (Model–View–Controller) applies *separation of concerns*.

**Patterns covered across this module (SE-based, applicable to ML):**
Pipe-and-Filter · CQRS · **RAG = Pipe-and-Filter + CQRS** · Event-driven · Broker · Monolithic · Microservices · Layered.

### Pipe-and-Filter (introduced here)

Organise a system as a sequence of independent **filters** connected by **pipes**. Each filter does one transformation and passes output downstream.

```
[Data Source] → (clean) → (extract features) → (infer) → (format) → [Data Sink]
                  filter        filter          filter    filter
     each box swappable/insertable without disturbing the others
```

> 🌍 A **water-treatment plant**: screening → sedimentation → filtration → chlorination. Each stage does one job on the stream and hands it on; you can upgrade filtration without touching the others.

**Why ML loves it:** **modularity + reusability + quality localisation** — you can attach a QA to a *single* stage ("feature extraction < 50 ms", "cleaner drops < 0.1% of valid rows") and test it independently. A **RAG ingestion pipeline** (load → chunk → embed → index) is exactly this shape, as is a classic **train → validate → serve** flow.

> ⚠️ Pipe-and-filter suits **batch-style transformation** flows. It's a poor fit when stages need rich back-and-forth or shared mutable state — there, **event-driven** or **blackboard** styles (later sessions) fit better. *Match the pattern to the quality you need.*

---

## 🎯 Recap

- Functionality = *what*; **quality attributes = how well** — and two systems with identical features (Flipkart vs Hotstar) live or die on QAs won at the **architecture** level.
- A QA is measurable & testable, always qualifies a function, and must be **SMART**.
- ML adds first-class QAs: robustness, explainability, fairness, privacy, drift-adaptability, reproducibility — *accuracy alone is not enough*.
- **Architecture** = expensive-to-change structural decisions chosen to make key QAs easy.
- **Think like an architect:** beyond the model, for uncertainty, for evolution.
- **Pipe-and-Filter** = modular, reusable stages — the shape of most ML pipelines.

➡️ **Next:** [Session 5 — the workhorse architectural patterns: CQRS, RAG, Monolith, Microservices](Session-05-Architectural-Patterns-for-ML-Systems.md).
