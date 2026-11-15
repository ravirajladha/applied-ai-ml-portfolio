# SE4ML — Pre-Midsem Cheat Sheet (Sessions 1–7)

> **AIMLCZG546** · Modules 1–3: **Foundations · Requirements · Architecture & Design**
> Built for the **open-book end-sem (40%, 2.5 hrs)** — tables and decision rules, not prose.
>
> **The spine of these seven sessions:** *an ML model is a small box inside a much larger software system.*

---

## 1. SE vs ML — the fault line

| | **Software Engineering** | **Machine Learning** |
|---|---|---|
| Logic comes from | a programmer writing **rules** | **data** teaching the rules |
| Nature | **deterministic**, spec-driven | **inductive / probabilistic**, data-driven |
| Correctness | **binary** (right / bug) | **statistical** (metrics) that **decays** with data drift |
| Moving parts | **code** | **data + model + code** (3×) |
| Specification | written up front, in the code | emerges from the data |
| Where bugs get fixed | in the application logic | often in **data / features / training** |

**Roles ML adds on top of SE:** data engineer · data scientist · ML engineer · MLOps engineer.

**The SDLC:** Requirements → Design → Implementation → Testing → Deployment → Maintenance.
**Evolution:** monolith on a physical server → VMs → containers → **Cloud Native** (microservices, containers, orchestration, CI/CD).

---

## 2. Model vs System, and hidden technical debt

> ⭐ **Model-centric view** = focuses **only on the ML model and its algorithm.**
> ⭐ **System-centric view** = focuses on the **entire end-to-end system**: data, infrastructure, deployment, user experience.
>
> *(This exact distinction was a mid-term question. Expect it again.)*

**Hidden technical debt (Sculley et al., Google):** the ML code is a **small box** — often **~5% of the codebase**. Everything around it is the system:

```
┌────────────┬──────────────┬────────────┬──────────────┬─────────────┐
│Data        │ Feature      │ Config     │ Serving      │ Monitoring  │
│collection &│ extraction   │            │ infra        │             │
│verification│              │            │              │             │
├────────────┴──────┬───────┴────┬───────┴──────────────┴─────────────┤
│  Data pipelines   │ ML CODE ▪  │  Analysis tools · Process mgmt      │
└───────────────────┴────────────┴─────────────────────────────────────┘
```

> 🎯 **Optimise the end-to-end product** (latency, reliability, monitoring, UX) — **not just offline accuracy**.

**ML as a component:** it can be **core** (the product *is* the model — a recommender) or **auxiliary** (a helpful add-on — spell-check). Either way, **design for mistakes**: the model *will* be wrong, so the system needs guardrails, fallbacks, human override and undo.

### The three AI paradigms

| Paradigm | What it does | Output |
|---|---|---|
| **Predictive AI** | learns patterns to **predict / classify** | a number or a label |
| **Generative AI** | **produces new content** from a prompt | text, image, code |
| **Agentic AI** | **reasons, plans, uses tools, acts** toward a goal | an **action** |

**Case studies:** **Apollo** (self-driving — **28 entangled models**) and **Microsoft's nine-stage ML workflow** — both make the same point: **integration is the real challenge**, not the individual model.

---

## 3. Requirements Engineering (Session 3)

### When to use ML (Hulten)

Use ML when **all three** hold:

| Condition | Meaning |
|---|---|
| **The logic is complex or changing** | too many rules to hand-write, or the rules keep moving |
| **Patterns are learnable from data** | there *is* signal, and you have enough labelled examples |
| **Mistakes are tolerable** | a wrong answer is survivable — you can absorb or correct it |

> ⚠️ **Don't use ML** for small, stable, fully-specifiable problems (compute a tax rate), or where a **single mistake is catastrophic and unrecoverable**.

### Why ML requirements differ

Requirements must become **probabilistic → measurable**, **data-aware** (what data, how much, what quality) and **model-aware** (which metric, what threshold, retraining cadence).

### Goals — the four levels

| Level | Question | Example |
|---|---|---|
| **Organisational** | why does the business care? | reduce loan losses |
| **Product** | what must the product do? | flag risky applicants |
| **User** | what does the user get? | a fast, fair decision |
| **Model** | what must the model achieve? | recall ≥ 0.85 at precision ≥ 0.6 |

Goals **support** or **conflict** with each other → conflicts force explicit **trade-offs** (accuracy vs latency, personalisation vs privacy).

**From goals to requirements:** trace **decisions → predictions → ML**. Ask *what decision is being made?* → *what prediction would inform it?* → *can ML supply that prediction?*

### GR4ML — three views ⭐

| View | Answers | Contains |
|---|---|---|
| **Business view** | **WHY** | organisational goals, business questions, stakeholders |
| **Analytics view** | **WHAT** | the **analytics goal**, **soft goals** (quality attributes), and **algorithms** |
| **Data view** | **HOW** | data sources, entities, attributes, preparation |

> 🧪 **The exam pattern (seen in the mid-term):** *"A bank collects income, credit score, employment status, repayment history and wants to predict loan default (Yes/No). Draw the GR4ML Analytics Design View. Identify the analytics goal, two soft goals and two algorithms."*
>
> **Answer shape:**
> - **Analytics goal** — one sentence, a *prediction*: *"Predict whether a loan applicant will default."*
> - **Soft goals** — pick from: **interpretability, precision, robustness, accuracy, tolerance to missing values, fairness, explainability**.
> - **Algorithms** — any valid **binary classifier**: SVM, Naïve Bayes, Decision Tree, Random Forest, Logistic Regression.
>
> *Depicting any relevant quality attributes is acceptable.* Label the input entity with the scenario's own noun ("customer profile"), not the template's.

### Accuracy vs precision (keep distinct)

| Term | Meaning |
|---|---|
| **Accuracy** | **closeness to the truth** — are you hitting the bullseye? |
| **Precision** | **consistency / repeatability** — are your shots tightly grouped, wherever they land? |

---

## 4. Quality Attributes & Architecture (Session 4)

**Functionality = *what* the system does. Quality attributes = *how well* it does it.**
Two systems with identical features (Flipkart vs Hotstar) live or die on QAs — and QAs are won or lost at the **architecture** level, not in the code.

**A quality attribute is:** measurable & testable · always **qualifies a function** · must be **SMART** (Specific, Measurable, Achievable, Relevant, Time-bound).

> ❌ "The system should be fast." ✅ "**95% of prediction requests return in under 200 ms at 1,000 req/s.**"

### QAs that ML makes first-class

| QA | Question it answers |
|---|---|
| **Robustness** | does it hold up on unusual, corrupted or adversarial input? |
| **Explainability** | can we say *why* this prediction happened? |
| **Fairness** | does it treat groups equitably? |
| **Privacy** | is personal data protected and not inferable? |
| **Security** | can it be attacked, poisoned or stolen? |
| **Scalability / Latency** | volume and speed under real load |
| **Reproducibility** | can this exact result be recreated? |
| **Drift-adaptability** | does it keep working as the world changes? |

> 🎯 **Accuracy alone is not enough** — that is the whole point of Session 4.

**Software architecture** = the **structural decisions that are expensive to change**, chosen to make the key quality attributes easy to achieve.

**Thinking like an architect:** think **beyond the model** · think **for uncertainty** (the model will be wrong) · think **for evolution** (data, models and requirements will all change).

**Pipe-and-Filter** — data flows through independent, reusable, individually testable **stages**. It is the shape of most ML pipelines. ⭐ *A mid-term question asked whether Pipe-and-Filter applies to ML systems — **it does**, and **RAG is an example**.*

---

## 5. Architectural patterns (Session 5)

> **Architecture is recombination** — you rarely invent a pattern; you choose and combine known ones to meet your quality attributes.

### CQRS — Command Query Responsibility Segregation

Handle **writes** and **reads** with **separate models and stores**.

| | **Command side (write)** | **Query side (read)** |
|---|---|---|
| HTTP verbs | POST / PUT / DELETE | GET |
| In ML systems | updates data / models / features | serves predictions, metrics, dashboards |
| Optimised for | **correctness** | **speed** (denormalised, cached, indexed) |

Separated by **Kafka/Kinesis** (event streams), **RabbitMQ/ActiveMQ** (brokers) or **Airflow/Prefect** (async pipelines).

**Cost: eventual consistency** — an update appears on the read side only after it propagates; components **converge** rather than being identical instantly.

> 🎯 **CQRS shines when read and write workloads differ greatly** — an ML system that updates models *rarely* but serves predictions *constantly*. Accept the stale window only where it violates no requirement (fine for model metadata; **not** fine for a bank balance).

### RAG — Retrieval-Augmented Generation

**Retrieve** relevant documents from a vector store, then **generate** a grounded answer.

- Grounds an LLM in your own data **without retraining** it.
- Structurally it is **Pipe-and-Filter + CQRS**.
- Reduces hallucination and makes answers **citable**.
- Evaluated with **RAGAS** (Session 12).

### Monolith vs Microservices ⭐

| | **Monolithic ML pattern** | **Microservices ML pattern** |
|---|---|---|
| Structure | model + preprocessing + API in **one deployable unit** | independent services, each separately deployable |
| Repo / pipeline | **mono-repo, single pipeline** | **multi-repo — one repo per service — and one pipeline per service** |
| Scaling | scale the **whole** app | scale **each service independently** |
| Latency | **low** — in-process calls | higher — network hops |
| Complexity | simple to build, test, deploy | **distributed complexity**: networking, versioning, observability |
| Failure | one bug can take down everything | **isolated** failures |
| Team fit | small team, one language | many teams, polyglot |
| **Prefer when** | small/simple app, single model, low latency critical, small team, early stage | many models with **different scaling needs** (a GPU model + a light CPU model), independent release cycles, large teams |

> ⭐ **Mid-term fact to hold onto:** *microservices recommend **multi-repo**, one repository per service, and **multiple pipelines**, one per service* — the opposite of the mono-repo claim.

### Choosing a pattern from the quality you need

| Need | Reach for |
|---|---|
| read load ≫ write load | **CQRS** |
| ground an LLM in private data without retraining | **RAG** |
| simplicity & lowest latency, small team | **Monolith** |
| independent scaling & release of parts | **Microservices** |
| loose coupling, async, many consumers | **Event-driven** |
| modular, testable stages | **Pipe-and-Filter** |

> 🎯 **Let requirements, not fashion, drive the choice** — and say so in an exam answer.

---

## 6. Event-Driven Architecture & ML design patterns (Session 6)

### Event-Driven Architecture

**Publish/subscribe over a broker.** A producer emits an **event**; any number of consumers subscribe. Producer and consumer never know about each other.

| Gain | Why |
|---|---|
| **Loose coupling** | services depend on the *event*, not on each other |
| **Independent scaling** | slow consumers scale up without touching producers |
| **Extensibility** | add a new consumer without changing the producer |
| **Buffering** | the queue absorbs spikes |

Cost: **eventual consistency**, harder debugging (no single call stack), message-ordering and duplicate concerns.
It is the **backbone linking CQRS and streaming features**.

### The Model Registry pattern

The **source of truth** for models: **versions and governs** them with full **lineage**, enabling **promotion** (staging → production) and **rollback**.

| | **Git** | **Model registry** |
|---|---|---|
| Stores | **code** (lightweight text) | **model artifacts + metadata** |
| Tracks | diffs, branches | **version, metrics, lineage, stage, approval** |
| Big binaries | **bloats the repo — don't** | designed for it |

> ⚠️ **Git is not a model registry — don't put weights in Git.** Use **DVC** for data/model files and **MLflow** for experiments + registry.

### Batch vs Real-time serving

| | **Batch** | **Real-time (online)** |
|---|---|---|
| When predictions are made | on a schedule, for many records at once | on demand, per request |
| Latency | minutes–hours | milliseconds |
| Cost | low per prediction | higher (always-on infra) |
| Example | nightly churn scores, Netflix recommendations | fraud check at checkout |

> 🎯 **Pick freshness by use case: no more than you need** (extra freshness = extra cost and complexity) **and no less** (stale predictions lose their value).

---

## 7. Agentic AI & coordination patterns (Session 7)

**From chatbots to doers.** A chatbot *answers*; an agent *acts*.

> **Generative AI + Reasoning + Tools + Feedback loops → Agentic AI**

**An agent** = an **LLM reasoning engine + memory + tools** running a loop:

```
        ┌──────────────────────────────┐
        ▼                              │
  REASON (plan) ──▶ ACT (call tool) ──▶ OBSERVE (read result)
        │                                          │
        └────────── memory ◀───────────────────────┘
```

| Component | Role |
|---|---|
| **LLM** | the reasoning engine that decides the next step |
| **Memory** | short-term (conversation) + long-term (vector store) |
| **Tools** | APIs, search, code execution, databases — how it affects the world |
| **Feedback loop** | observe the result, re-plan |

### SAGA pattern — multi-step distributed transactions

A long transaction is split into a **sequence of local transactions**. If step *n* fails, run **compensating transactions** to undo steps *n−1 … 1*.

> 🌍 Book flight → book hotel → book car. The car booking fails → *compensate*: cancel the hotel, cancel the flight. There is no global rollback across services, so you **undo forward**.

**Two ways to run it:**

| | **Orchestration** | **Choreography** |
|---|---|---|
| Control | a **central coordinator** tells each service what to do | each service **reacts to events** from the previous one |
| In agents | a supervisor agent directing sub-agents | **prompt chaining** / event-driven agents |
| Pros | easy to follow, one place to debug | loose coupling, no single bottleneck |
| Cons | coordinator is a single point of failure | flow is **implicit** and hard to trace |

### Blackboard pattern — open-ended collaboration

A **shared state ("blackboard")** plus a **controller**. Specialist agents watch the blackboard, and whichever one can contribute next writes its partial result; the controller decides who goes next.

> 🎯 **Use Blackboard when there is no fixed algorithm** — the path to the solution is discovered, not planned. Use **SAGA** when the steps *are* known but can fail partway.

---

## ⭐ Most-likely exam targets (pre-midsem half)

| Topic | Be able to |
|---|---|
| **Model-centric vs system-centric** | state the difference in one line each |
| **Hidden technical debt** | say ML code is a small fraction and name the surrounding boxes |
| **When to use ML** | give the three Hulten conditions **and** a case where ML is wrong |
| **GR4ML** | draw the Analytics view; name analytics goal + 2 soft goals + 2 algorithms |
| **Quality attributes** | list ML-specific QAs; rewrite a vague QA as **SMART** |
| **Pipe-and-Filter** | agree it applies to ML; cite **RAG** as the example |
| **CQRS** | write vs read split, the separating tech, **eventual consistency** as the cost |
| **RAG** | retrieve-then-generate, grounding without retraining |
| **Monolith vs Microservices** | the table above + **multi-repo, one pipeline per service** |
| **Event-driven** | pub/sub, loose coupling, the trade-offs |
| **Model registry** | why Git is not one; lineage, promotion, rollback |
| **Batch vs real-time** | choose by freshness need, justify the cost |
| **Agentic AI** | the equation, the reason→act→observe loop |
| **SAGA vs Blackboard** | compensating transactions vs shared state; orchestration vs choreography |

### How to answer an "agree / disagree with justification" question
1. State **agree** or **disagree** plainly (1 mark).
2. Give the **correct version** of the statement, using the course's own vocabulary (1 mark).
3. Add one concrete example if there is room.

*Do not hedge. A hedged answer scores the agree/disagree mark and loses the justification mark.*
