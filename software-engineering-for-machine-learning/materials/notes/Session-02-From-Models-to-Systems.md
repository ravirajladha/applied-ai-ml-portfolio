# Session 2 — From Models to Systems

> **Module 1 · Lecture 2** · Slides: `Session 02 - From Models to Systems.pptx` · Companion: `friend notes/4.pdf`
>
> **One-line goal:** make one big point — *a trained model is a small part of a working product* — and map the three AI paradigms (predictive / generative / agentic).

### Contents
1. [ML in production: scope & challenges](#1-ml-in-production-scope--challenges)
2. [ML model vs ML system](#2-ml-model-vs-ml-system)
3. [Only a fraction is ML code (hidden technical debt)](#3-only-a-fraction-is-ml-code-hidden-technical-debt)
4. [ML as a component + designing for mistakes](#4-ml-as-a-component--designing-for-mistakes)
5. [The three AI paradigms](#5-the-three-ai-paradigms)
6. [Cloud Native ML systems](#6-cloud-native-ml-systems)
7. [Case study: Apollo](#7-case-study-apollo-self-driving)
8. [Case study: Microsoft's 9-stage workflow](#8-case-study-microsofts-nine-stage-workflow)
9. [Recap](#-recap)

---

## 1. ML in production: scope & challenges

**The running story:** *Sidney*, a researcher, builds strong domain-specific **speech recognition** models (medical, academic, technical talks). Manual transcription is expensive (~$1.50/min) and slow, and existing tools mishandle technical terms — a real market. Sidney launches a start-up for affordable transcription + live captioning… and discovers how much *engineering* stands between a model and a product.

> 🌍 A great model is a great **engine**. A business is a whole **car** — wheels, brakes, dashboard, fuel system. A home cook who bakes great bread is not yet a bakery (which needs a shopfront, till, supply chains, and consistency at 6 a.m.). **The bread — the model — was the easy part.**

### The challenges, in two buckets

| Technical & business | Engineering & operational |
|----------------------|---------------------------|
| Noisy audio lowers accuracy | Must build a whole ecosystem (website, backend, payments) |
| Customers expect results in *minutes*; live captioning needs near-real-time | Fragile ML pipeline (manual retraining, outdated libs, updates cause outages) |
| Cloud compute + LLM APIs + GPUs are expensive | ML ↔ engineering team communication gaps |
| Balancing speed/cost/quality while staying profitable | Weak monitoring & fairness (bias risk in medical/dialect cases) |

> 🧪 **The speed–cost–quality squeeze (per 60-min lecture).** Manual: $1.50×60 = **$90**, hours, high quality. Cheap-fast model at $0.10/min = **$6** in minutes, but weaker on technical terms. Add an LLM cleanup pass at $0.40/min → (0.10+0.40)×60 = **$30**, better quality but 5× the cheap-path compute. **Pick two of {fast, cheap, accurate}; the third gives.** Pricing = choosing where on that triangle to sit.

> 🎯 Moving prototype → production needs **far more engineering than ML**, and forces hard trade-offs. The model's accuracy is *necessary but not sufficient*.

---

## 2. ML model vs ML system

**This is the distinction the whole course turns on.**

| | ML **model** | ML **system** |
|---|---|---|
| What it is | the trained algorithm mapping inputs → predictions | the whole product: data pipelines, serving, UI, monitoring, glue code |
| View | **model-centric** — tune algorithm/features/hyperparameters for accuracy | **system-centric** — improve data, infra, deployment, UX for reliable real-world performance |
| Who leans this way | researchers | engineers |

> 🌍 A model-centric **chef** obsesses over the perfect sauce. A system-centric **restaurateur** also worries about table turnover, the dishwasher, and whether the waiter wrote the order down. Both matter — but only one keeps the restaurant open.

> 🧪 **Where a 2% accuracy gain disappears.** Tuning lifts accuracy 94% → 96% (errors 6% → 4%, a third fewer). But the serving pipeline drops **5%** of requests on timeouts and the UI shows stale results half the time. User-visible quality is dominated by the 5% drops, not the 2% model gain. **A system-centric view fixes the timeouts *first* — a bigger win than the tuning.**

> ⚠️ Chasing model accuracy while ignoring the system is the **#1 rookie mistake** in applied ML. The biggest wins are often in plumbing, not the model.

---

## 3. Only a fraction is ML code (hidden technical debt)

Landmark paper — **Sculley et al., "Hidden Technical Debt in Machine Learning Systems" (NeurIPS 2015)** — made this picture famous:

```
   ┌────────────────────────────────────────────────────────┐
   │  Data      Feature      Data        Config              │
   │ Collection Extraction  Verification                     │
   │                                                         │
   │  Process   ┌──────────┐  Machine     Analysis  Serving  │
   │  Mgmt      │ ML  CODE │  Resource    Tools     Infra    │
   │  Tools     └──────────┘  Mgmt                           │
   │                          Monitoring                     │
   └────────────────────────────────────────────────────────┘
        The little box in the middle is the ML code.
        Everything else is the system that feeds/serves/watches it.
```

> 🌍 The model is the visible **tip of an iceberg**. Below the waterline sits the vast, unglamorous machinery that feeds, serves, watches, and configures it — where most effort *and most risk* live.

> 🧪 **Putting a number on "a small fraction."** Rough code-size shares: ML code 5%, data plumbing 30%, serving 25%, monitoring 15%, config 15%, UI 10%. Non-ML = 30+25+15+15+10 = **95%** → the supporting system is **19× larger** than the ML code. Budget your team as if ML is the whole job and you under-resource 95% of the work — a leading cause of failed ML projects.

> ⚠️ **"Technical debt"** here = the hidden cost of shortcuts in that surrounding machinery (tangled data dependencies, undeclared consumers, glue code). It accrues quietly and is paid back painfully.

---

## 4. ML as a component + designing for mistakes

Because ML is small, see it as **one component among many** — sometimes the **core**, sometimes an **auxiliary add-on**.

| Role | Example | If it fails |
|------|---------|-------------|
| **Core** | Speech recognition *is* the transcription product | Everything stops |
| **Auxiliary** | "Audit-risk" prediction bolted onto deterministic tax software | Minor annoyance |

> 🌍 An electric motor is the **core** of an electric car but only **auxiliary** in an automatic car window. Same tech, very different role and risk. Knowing which you're building changes how careful you must be.

Real systems often contain **many** ML components (perception + detection + prediction) glued by traditional code. That demands **systems thinking**: understand the system's goals & its environment, design how ML + non-ML parts integrate, and coordinate many roles (interdisciplinary).

### What to do when the ML component is wrong

ML is probabilistic → it *will* be wrong sometimes. The design question: **what does the surrounding system do about it?** Show a confidence score · ask a human to confirm · fall back to a safe default · log the case for retraining.

> 🧪 **A confidence gate on transcription.** Attach a confidence to each sentence. **≥ 0.90** → auto-publish (say 90% of sentences flow untouched). **< 0.90** → route the remaining 10% to a human reviewer. The system stays fast & cheap on the easy 90% while protecting quality on the risky 10%. *This "handle the mistake" logic is non-ML code wrapped around the ML component.*

> 🎯 See ML as a component (core or auxiliary), think about the **whole system's** behaviour, and **always design for what happens when the model is wrong** — a model with no plan for its mistakes is a liability (especially in medical/legal settings).

---

## 5. The three AI paradigms

Each builds on the last:

```
Predictive AI  →  uses past data to predict a future outcome (number/label)
Generative AI  →  creates new content (text/image/video) from natural instructions
Agentic AI     →  acts autonomously toward a goal using reasoning + tools + feedback
```

$$\textbf{Agentic AI} = \text{Generative AI} + \text{Reasoning} + \text{Tools} + \text{Feedback Loops}$$

> 🌍 A **weather forecaster** (predictive): "70% chance of rain." A **novelist** (generative): writes a story about a rainy day. A **personal assistant** (agentic): notices the forecast, books a cab, moves your meeting, texts the client — pursuing "get to the meeting dry" on its own.

- **Generative AI** = built on a foundation model, generates digital artifacts from *natural* instructions (everyday language / sketches — no technical knowledge needed).
- **Agentic AI** = autonomy. Nvidia: "sophisticated reasoning and iterative planning to autonomously solve complex, multi-step problems." OpenAI: "pursue complex goals with limited direct supervision."

> 🧪 **Counting steps for "get me to the Tuesday meeting."** Predictive → one number: "delay ≈ 25 min" (no action). Generative → writes an itinerary when asked (still no action; you execute). Agentic → plans (calendar, traffic), acts (books cab), observes (cab delayed), re-plans (books another) — a **loop of ~4–5 steps, no further prompting.** The jump is from *"tell me"* to *"give me a goal and I'll figure out the steps."*

> ⚠️ Agentic systems **act in the world**, so mistakes have consequences (a wrong booking, a bad email). Autonomy raises the stakes — monitoring and guardrails are *not optional*.

---

## 6. Cloud Native ML systems

ML is increasingly a dominant cloud workload. **CNCF** defines Cloud Native as tech that lets orgs "build and run scalable applications in modern, dynamic environments" — exemplified by **containers, service meshes, microservices, immutable infrastructure, declarative APIs**.

> 💡 Recall S1's equation: *Cloud Native = Agile + DevOps + microservices + containers + cloud*. Wrapping a model as a containerised microservice behind a declarative API lets it **scale under load** and **roll back cleanly** on a bad update — exactly the fragilities Sidney's start-up hit.

> ⚠️ Cloud Native is a **means, not an end**. It makes scaling & reliability *possible*; it does not make a bad model good or a leaky pipeline clean.

---

## 7. Case study: Apollo (self-driving)

**Apollo** (Baidu's autonomous-driving platform) = a textbook complex ML system. Its lesson: **not one model, but many interacting ML components + traditional software logic.**

```mermaid
flowchart LR
    subgraph Sensors
      C[Camera] & L[LiDAR] & R[Radar] & M[Maps]
    end
    Sensors --> P[Perception models] --> D[Detection models] --> T[Trajectory prediction]
    T --> Code[Traditional code:<br/>validation + decision logic] --> Drive[Driving action]
```

> 🧪 **Reading the Apollo numbers.** ~**28 ML models** across perception/detection/prediction — not one "self-driving model." Outputs chain (one model's output = next model's input) → an early perception error **propagates downstream**. Inputs fused from **4 sensor sources** (camera, LiDAR, radar, maps). With 28 entangled models + fusion, the hard problems are **integration, testing, and system-level QA** — not any single model's accuracy.

> ⚠️ You **cannot** test a 28-model entangled system by checking each model in isolation. Outputs feed inputs, so quality must be assessed at the **system level**.

---

## 8. Case study: Microsoft's nine-stage workflow

A Microsoft study of real teams proposes a **9-stage workflow** and stresses that ML is **highly iterative with feedback loops** (not linear), with **data as the central component**.

```
1 Model Requirements → 2 Data Collection → 3 Data Cleaning → 4 Data Labeling
→ 5 Feature Engineering → 6 Model Training → 7 Model Evaluation
→ 8 Deployment → 9 Monitoring ──(loops back to any earlier stage)──┐
   ▲───────────────────────────────────────────────────────────────┘
```

> 🧪 **Why the loops matter — cost of a late data fix.** Monitoring (stage 9) reveals the labels from stage 4 were wrong → loop back to 4, re-label, re-run 5–9. That's **9 − 4 = 5 stages re-executed** because the problem surfaced late. Catching it early (a "shift-left" *for data*) reruns zero downstream stages — which is why **data quality sits at the centre**.

The study also shows ML needs **new roles** (data scientists, ML engineers) alongside developers, must integrate with **Agile/DevOps**, and benefits from a **process maturity model** (like CMM). Broader SE-in-ML adoption: automated end-to-end pipelines, **data engineering as a core SE activity**, experimentation-driven development, **versioning of models *and* data** (not just code), continuous evaluation & monitoring, model debugging/interpretability, cross-functional teams.

> ⚠️ Treating ML like a linear pipeline (each stage once, in order) ignores its most important feature — **the feedback loops**. Real ML work circles back constantly.

---

## 🎯 Recap

One thesis ran through everything: **a model is a sliver of a system.**
- Sidney's start-up → the engineering gap + the speed/cost/quality squeeze.
- Model-vs-system + hidden-debt picture → the ML code is ~5% of the whole.
- ML as a component (core/auxiliary) → systems thinking + **designing for mistakes**.
- Three paradigms (predictive → generative → agentic) → where AI is heading.
- Apollo (28 entangled models) + Microsoft (9-stage iterative workflow) → **integration is the real challenge**.

➡️ **Next:** [Session 3 — deciding *when* ML is even the right tool, and turning goals into requirements](Session-03-Requirements-Engineering-for-ML.md).
