# SE4ML — Pre-Midsem Question Bank (Sessions 1–7)

> **AIMLCZG546** · Modules 1–3: **Foundations · Requirements · Architecture & Design**
> Built for the **open-book end-sem (40%, 2.5 hrs)**. **Conceptual + scenario only**, chapter by chapter.
> **§ numbers match the pre-midsem cheat sheet.**

---

## How to use this

Same drill as the post-midsem bank: **answer first, then open the box.** Mark ✅ / 🟡 / ❌ and go back only to the **§** you missed.

**Codes:** **C** = conceptual · **S** = scenario.

> ⚠️ This half carries **less weight** than post-midsem. Do the post-midsem bank first; use this one as the Saturday sweep.
>
> **The mid-term leaned hard on "agree/disagree with justification".** The scoring is: **1 mark for committing**, **1 mark for restating the correct version in the course's vocabulary**. **Do not hedge** — a hedged answer scores the first mark and loses the second.

---

# MODULE 1 — Foundations (S1–S2)

## 1. SE vs ML — the fault line → §1

**C1.1** Compare **Software Engineering** and **Machine Learning** across: where the logic comes from, nature, correctness, moving parts, specification, and where bugs get fixed.

<details><summary><b>Show answer</b></summary>

| | **Software Engineering** | **Machine Learning** |
|---|---|---|
| Logic comes from | a programmer writing **rules** | **data** teaching the rules |
| Nature | **deterministic**, spec-driven | **inductive / probabilistic**, data-driven |
| Correctness | **binary** (right / bug) | **statistical** (metrics) that **decays** with data drift |
| Moving parts | **code** | **data + model + code** (3×) |
| Specification | written up front, in the code | **emerges from the data** |
| Where bugs get fixed | in the application logic | often in **data / features / training** |

**Roles ML adds on top of SE:** data engineer · data scientist · ML engineer · MLOps engineer.
**The SDLC:** Requirements → Design → Implementation → Testing → Deployment → Maintenance.
**Evolution:** monolith on a physical server → VMs → containers → **Cloud Native** (microservices, containers, orchestration, CI/CD).
</details>

**C1.2** *"An ML system is just a software system with a model in it, so the same engineering practices apply unchanged."* Agree or disagree.

<details><summary><b>Show answer</b></summary>

**Disagree.**

**The correct version:** an ML system has **three moving parts — data, model and code — instead of one**, and that changes engineering in three concrete ways:
1. **Correctness is statistical, not binary.** There is no "right answer" to assert; there are **metrics**, and they **decay with data drift**. Traditional testing assumes a fixed expected output.
2. **The specification emerges from the data** rather than being written up front — so requirements must become **probabilistic, data-aware and model-aware** (§3).
3. **Bugs are often fixed in data, features or training**, not in the application logic — which means data and models need versioning, validation and testing of their own.

**Concede the true part:** everything ordinary software needs — version control, CI, testing, logging, deployment discipline — is still required. ML **adds** obligations; it does not remove any.
</details>

---

## 2. Model vs System & hidden technical debt → §2

**C2.1** Define the **model-centric** and **system-centric** views. *(This exact distinction was a mid-term question.)*

<details><summary><b>Show answer</b></summary>

> ⭐ **Model-centric view** = focuses **only on the ML model and its algorithm.**
> ⭐ **System-centric view** = focuses on the **entire end-to-end system**: data, infrastructure, deployment, user experience.

**Hidden technical debt (Sculley et al., Google):** the ML code is a **small box — often ~5% of the codebase.** Everything around it is the system:

```
┌────────────┬──────────────┬────────────┬──────────────┬─────────────┐
│Data        │ Feature      │ Config     │ Serving      │ Monitoring  │
│collection &│ extraction   │            │ infra        │             │
│verification│              │            │              │             │
├────────────┴──────┬───────┴────┬───────┴──────────────┴─────────────┤
│  Data pipelines   │ ML CODE ▪  │  Analysis tools · Process mgmt      │
└───────────────────┴────────────┴─────────────────────────────────────┘
```

> 🎯 **Optimise the end-to-end product** — latency, reliability, monitoring, UX — **not just offline accuracy.**
</details>

**C2.2** Distinguish ML as a **core** component from ML as an **auxiliary** component, and state the design rule that applies to both.

<details><summary><b>Show answer</b></summary>

- **Core** — the product **is** the model: a recommender system. Remove the model and there is no product.
- **Auxiliary** — the model is a helpful add-on: spell-check. Remove it and the product still works, slightly worse.

**The rule that applies either way: design for mistakes.** The model **will** be wrong, so the system needs **guardrails, fallbacks, human override and undo**. The difference is only how much of the product collapses when it is wrong.
</details>

**C2.3** Name the **three AI paradigms** with their output.

<details><summary><b>Show answer</b></summary>

| Paradigm | What it does | Output |
|---|---|---|
| **Predictive AI** | learns patterns to **predict / classify** | a **number or a label** |
| **Generative AI** | **produces new content** from a prompt | text, image, code |
| **Agentic AI** | **reasons, plans, uses tools, acts** toward a goal | an **action** |

> 🎯 This maps straight onto **MLOps / LLMOps / AgentOps** in the post-midsem half: *ships a number · ships text · ships an action.*
</details>

**S2.1 · Scenario.** A team proudly reports their new model beats the old one by 3 points of accuracy offline, and asks why the product manager is unimpressed. Using the **hidden technical debt** picture, explain what the PM is worried about.

<details><summary><b>Show answer</b></summary>

**The PM is taking a system-centric view; the team is taking a model-centric one.**

- **Model-centric** = focuses **only on the ML model and its algorithm** — which is exactly what "3 points of offline accuracy" measures.
- **System-centric** = focuses on the **entire end-to-end system**: data, infrastructure, deployment, user experience.

**Why the 3 points may be worth nothing:** the **ML code is roughly 5% of the codebase**. Around it sit **data collection and verification, feature extraction, configuration, serving infrastructure, data pipelines, analysis tools, process management and monitoring**. A better model that is slower, harder to serve, less explainable or dependent on a fragile new feature pipeline can make the **product** worse while making the **metric** better.

**The questions the PM is really asking:**
- What happens to **latency** and serving cost?
- Does the accuracy hold **per slice**, or only on average?
- Does it need new data that the collection pipeline does not reliably provide?
- Can we still explain a decision, and roll back if it misbehaves?

**Two case studies make the same point:** **Apollo** self-driving with **28 entangled models**, and **Microsoft's nine-stage ML workflow** — in both, **integration is the real challenge**, not the individual model.
</details>

---

# MODULE 2 — Requirements Engineering (S3)

## 3. When to use ML → §3

**C3.1** Give **Hulten's three conditions** for using ML, and two cases where ML is the wrong tool.

<details><summary><b>Show answer</b></summary>

Use ML when **all three** hold:

| Condition | Meaning |
|---|---|
| **The logic is complex or changing** | too many rules to hand-write, or the rules keep moving |
| **Patterns are learnable from data** | there *is* signal, and you have enough labelled examples |
| **Mistakes are tolerable** | a wrong answer is survivable — you can absorb or correct it |

> ⚠️ **Do not use ML** for **small, stable, fully-specifiable problems** (computing a tax rate), or where a **single mistake is catastrophic and unrecoverable**.
</details>

**S3.1 · Scenario.** Judge each proposal against Hulten's three conditions, and give a verdict.
(a) Computing statutory income tax owed from a filled tax return.
(b) Detecting fraudulent transactions on a card network.
(c) A model that decides, with no human in the loop, whether to fire a nuclear plant's emergency shutdown.

<details><summary><b>Show answer</b></summary>

**(a) Tax computation → do NOT use ML.**
- *Complex or changing logic?* **No** — it is **fully specifiable**: the statute states the rules exactly.
- *Learnable patterns?* Irrelevant — the rules are already known and exact.
- *Mistakes tolerable?* **No** — a wrong tax figure is a legal error.
**Verdict:** this is the deck's own counter-example. Write the rules. ML would be less accurate, less explainable and impossible to audit against the statute.

**(b) Fraud detection → YES, use ML.**
- *Complex or changing?* **Yes** — fraud patterns shift constantly as attackers adapt; hand-written rules go stale immediately.
- *Learnable?* **Yes** — huge volumes of labelled historical transactions.
- *Mistakes tolerable?* **Yes, with design** — a false positive is a declined card (annoying, recoverable), a false negative is money lost (absorbable and insurable). **Design for mistakes**: human review queue, customer confirmation, undo.
**Verdict:** all three hold. This is the canonical ML use case.

**(c) Autonomous nuclear shutdown → NO, not as specified.**
- *Complex?* **Yes.** *Learnable?* **Partly** — but true emergency events are vanishingly rare, so the labelled examples barely exist.
- *Mistakes tolerable?* **Absolutely not** — a **single mistake is catastrophic and unrecoverable**, in both directions: a missed shutdown, or a spurious one.
**Verdict:** the third condition fails, and it is the one that decides. ML may still assist as an **anomaly detector feeding a human operator** (a **safety-critical** system with **human oversight**), but it must not hold the authority to act alone.

> 🎯 **The pattern for this question type: test all three conditions explicitly, then say which one decides.**
</details>

**C3.2** Why do ML requirements differ from ordinary software requirements, and what are the **four goal levels**?

<details><summary><b>Show answer</b></summary>

**Requirements must become:** **probabilistic → measurable**, **data-aware** (what data, how much, what quality) and **model-aware** (which metric, what threshold, what retraining cadence).

| Level | Question | Example |
|---|---|---|
| **Organisational** | why does the business care? | reduce loan losses |
| **Product** | what must the product do? | flag risky applicants |
| **User** | what does the user get? | a fast, fair decision |
| **Model** | what must the model achieve? | **recall ≥ 0.85 at precision ≥ 0.6** |

Goals **support** or **conflict** with each other → conflicts force explicit **trade-offs** (accuracy vs latency, personalisation vs privacy).

**From goals to requirements — trace decisions → predictions → ML:** *what decision is being made?* → *what prediction would inform it?* → *can ML supply that prediction?*
</details>

---

## 4. GR4ML → §3 ⭐

**C4.1** Name the **three GR4ML views**, what each answers, and what each contains.

<details><summary><b>Show answer</b></summary>

| View | Answers | Contains |
|---|---|---|
| **Business view** | **WHY** | organisational goals, business questions, stakeholders |
| **Analytics view** | **WHAT** | the **analytics goal**, **soft goals** (quality attributes), and **algorithms** |
| **Data view** | **HOW** | data sources, entities, attributes, preparation |
</details>

**S4.1 · Scenario (the mid-term's own shape).** *A bank collects income, credit score, employment status and repayment history, and wants to predict loan default (Yes/No). Draw the GR4ML **Analytics Design View**. Identify the analytics goal, two soft goals and two algorithms.*

<details><summary><b>Show answer</b></summary>

**Analytics goal — one sentence, and it must be a *prediction*:**
> *"Predict whether a loan applicant will default."*

**Two soft goals** *(soft goals = quality attributes)* — pick any two from: **interpretability, precision, robustness, accuracy, tolerance to missing values, fairness, explainability.**
For a bank, the strongest pair is **interpretability** (the decision must be justifiable to the applicant and the regulator) and **fairness** (it must not discriminate across protected groups).

**Two algorithms** — any valid **binary classifier**: **Logistic Regression, Decision Tree, Random Forest, SVM, Naïve Bayes.**
*Say why:* Logistic Regression and Decision Tree also serve the **interpretability** soft goal, so the choice is consistent with the goals you named — that consistency is what earns the mark.

**Sketch shape:**
```
           ┌──────────────────────────────────────────┐
           │ ANALYTICS GOAL                           │
           │ Predict whether a loan applicant         │
           │ will default (Yes / No)                  │
           └────────────┬─────────────────────────────┘
              ┌─────────┴─────────┐
   SOFT GOALS │                   │ ALGORITHMS
   ○ Interpretability             ▣ Logistic Regression
   ○ Fairness                     ▣ Decision Tree
              └─────────┬─────────┘
           ┌────────────┴─────────────────────────────┐
           │ INPUT ENTITY — "Customer / loan profile" │
           │ income · credit score · employment       │
           │ status · repayment history               │
           └──────────────────────────────────────────┘
```

**Two marks people lose:**
- *Depicting any relevant quality attributes is acceptable* — do not agonise over which soft goals; name two and justify them.
- **Label the input entity with the scenario's own noun** ("customer profile", "loan application") — **not** the template's generic name.
</details>

**C4.2** Distinguish **accuracy** from **precision** in the Session-3 sense. *(Careful — this is not the §10 metric.)*

<details><summary><b>Show answer</b></summary>

| Term | Meaning |
|---|---|
| **Accuracy** | **closeness to the truth** — are you hitting the bullseye? |
| **Precision** | **consistency / repeatability** — are your shots tightly grouped, wherever they land? |

> ⚠️ **Do not confuse this with post-midsem §10**, where **precision = TP/(TP+FP)** as a classification metric. Here it is the measurement-science sense: you can be **precise but inaccurate** (tightly grouped, in the wrong place) and **accurate but imprecise** (scattered around the bullseye).
</details>

---

# MODULE 3 — Architecture & Design (S4–S7)

## 5. Quality attributes & architecture → §4

**C5.1** Distinguish **functionality** from **quality attributes**. What three properties must a quality attribute have?

<details><summary><b>Show answer</b></summary>

**Functionality = *what* the system does. Quality attributes = *how well* it does it.**
Two systems with identical features (Flipkart vs Hotstar) live or die on QAs — and **QAs are won or lost at the architecture level, not in the code.**

**A quality attribute is:**
1. **measurable and testable**,
2. always **qualifies a function** (it is never free-floating),
3. must be **SMART** — **S**pecific, **M**easurable, **A**chievable, **R**elevant, **T**ime-bound.

> ❌ *"The system should be fast."*
> ✅ *"**95% of prediction requests return in under 200 ms at 1,000 req/s.**"*
</details>

**S5.1 · Scenario.** A requirements document contains: *"The fraud model must be accurate, fast and fair."* Rewrite all three as SMART quality attributes, and say what the sentence gets wrong.

<details><summary><b>Show answer</b></summary>

**What it gets wrong:** none of the three is **measurable or testable**, and none **qualifies a function** — they float free of any operation the system performs. You cannot write a test for "fair", so nobody will, and nobody can tell whether the delivered system met the requirement.

**Rewritten SMART:**

| Vague | SMART |
|---|---|
| "accurate" | *"The fraud classifier achieves **recall ≥ 0.85 at precision ≥ 0.60** on a held-out month of transactions, re-measured every release."* |
| "fast" | *"**95% of prediction requests return in under 200 ms at 1,000 req/s**, measured at the API boundary."* |
| "fair" | *"**No demographic slice** (age band, region, card type) shows **recall more than 5 percentage points below the global figure**, evaluated per release and monitored monthly in production."* |

**Note what the rewrite forced:** the fairness requirement is now operationally **slicing** (post-midsem §11), and the latency one names the measurement point. **A quality attribute that does not say how it will be measured is a wish, not a requirement.**
</details>

**C5.2** Which quality attributes does ML make **first-class**, and what is the Session-4 headline?

<details><summary><b>Show answer</b></summary>

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

> 🎯 **Accuracy alone is not enough — that is the whole point of Session 4.**

**Software architecture** = the **structural decisions that are expensive to change**, chosen to make the key quality attributes easy to achieve.
**Thinking like an architect:** think **beyond the model** · think **for uncertainty** (the model will be wrong) · think **for evolution** (data, models and requirements all change).
</details>

**C5.3** *"Pipe-and-Filter is a traditional software pattern and does not apply to ML systems."* Agree or disagree. *(Asked at the mid-term.)*

<details><summary><b>Show answer</b></summary>

**Disagree — it applies, and it is arguably the default shape of ML systems.**

**The correct version:** **Pipe-and-Filter** means data flows through **independent, reusable, individually testable stages**. That is exactly an ML pipeline: ingest → validate → feature-engineer → train → evaluate → serve. Each filter has one responsibility, can be tested alone, and can be reused across pipelines.

**The example the deck names: RAG is a Pipe-and-Filter system** — retrieve → rank → augment the prompt → generate. Structurally, **RAG is Pipe-and-Filter + CQRS** (§5).

**Why it earns its place:** it delivers **modularity and testability** — which is what makes **pipeline quality** (post-midsem §9) and **idempotency** achievable at all.
</details>

---

## 6. Architectural patterns → §5

**C6.1** Explain **CQRS**: what it separates, how the sides differ, what separates them, and what it costs.

<details><summary><b>Show answer</b></summary>

**CQRS = Command Query Responsibility Segregation** — handle **writes** and **reads** with **separate models and stores**.

| | **Command side (write)** | **Query side (read)** |
|---|---|---|
| HTTP verbs | POST / PUT / DELETE | GET |
| In ML systems | updates data / models / features | serves predictions, metrics, dashboards |
| Optimised for | **correctness** | **speed** (denormalised, cached, indexed) |

**Separated by:** **Kafka / Kinesis** (event streams) · **RabbitMQ / ActiveMQ** (brokers) · **Airflow / Prefect** (async pipelines).

**Cost: eventual consistency** — an update appears on the read side only after it propagates; components **converge** rather than being identical instantly.

> 🎯 **CQRS shines when read and write workloads differ greatly** — an ML system that updates models *rarely* but serves predictions *constantly*.
</details>

**S6.1 · Scenario.** Where is CQRS's eventual consistency acceptable and where is it not? Give one case of each and state the deciding rule.

<details><summary><b>Show answer</b></summary>

**Acceptable — model metadata and prediction serving.** A model registry updated at 02:00 whose new version reaches every read replica by 02:00:30 is completely fine: nobody is harmed by a thirty-second window, and in exchange the read side is **denormalised, cached and indexed for speed**, serving predictions constantly while writes happen rarely. This is precisely where **CQRS shines: read and write workloads differ greatly.**

**Not acceptable — a bank balance.** If a withdrawal is written and the read side still shows the old balance, a second withdrawal can be authorised against money that is gone. The stale window **violates a hard requirement**, so the cost is not payable here.

**The deciding rule:** **accept the stale window only where it violates no requirement.** Do not ask *"is eventual consistency bad?"* — ask *"what specifically breaks during the window, and can the business survive it?"*

**And the general principle:** **let requirements, not fashion, drive the choice of pattern** — say that explicitly in an exam answer.
</details>

**C6.2** What is **RAG**, what does it buy you, and what is it structurally?

<details><summary><b>Show answer</b></summary>

**RAG = Retrieval-Augmented Generation** — **retrieve** relevant documents from a vector store, then **generate** a grounded answer.

- **Grounds an LLM in your own data without retraining it** — the headline benefit.
- Structurally it is **Pipe-and-Filter + CQRS**.
- **Reduces hallucination** and makes answers **citable**.
- Evaluated with **RAGAS** (post-midsem §15) — **faithfulness · answer relevance · context precision · context recall**.
</details>

**C6.3** Compare **Monolith** and **Microservices** for ML, and state the mid-term fact people get backwards.

<details><summary><b>Show answer</b></summary>

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

> ⭐ **The mid-term fact:** **microservices recommend *multi*-repo — one repository per service — and *multiple* pipelines, one per service.** The claim that microservices use a mono-repo with a single pipeline is **false**; that is the monolith.
</details>

**S6.2 · Scenario.** A startup of four engineers is building its first ML product: one model, tight latency budget, launching in three months. An advisor insists on microservices "because that is what scales". What is your recommendation?

<details><summary><b>Show answer</b></summary>

**Recommend the monolithic ML pattern**, and say why against each constraint the scenario gave:

| Constraint | Why it points to monolith |
|---|---|
| **Four engineers** | microservices fit **many teams, polyglot**; four people cannot staff distributed operations |
| **One model** | there is nothing to scale independently — the entire benefit of microservices is unavailable |
| **Tight latency** | monolith gives **low latency via in-process calls**; microservices add **network hops** |
| **Launching in three months, early stage** | monolith is **simple to build, test and deploy**; the deck names *"early stage"* explicitly |

**The advisor's error:** choosing for a scaling problem the team **does not have yet**, and paying **distributed complexity — networking, versioning, observability**, plus **multi-repo and one pipeline per service** — out of a three-month runway.

**Trade-off you are accepting, stated honestly:** **one bug can take down everything** (no failure isolation), and you must **scale the whole app** rather than parts of it.

**When you would revisit it:** when there are **many models with different scaling needs** — say a GPU vision model alongside a light CPU ranker — or when separate teams need **independent release cycles**. That is the trigger, not the advice.

> 🎯 **Let requirements, not fashion, drive the choice** — and say exactly that in the answer.
</details>

**C6.4** Give the **pattern-selection table**: which pattern for which need?

<details><summary><b>Show answer</b></summary>

| Need | Reach for |
|---|---|
| read load ≫ write load | **CQRS** |
| ground an LLM in private data without retraining | **RAG** |
| simplicity and lowest latency, small team | **Monolith** |
| independent scaling and release of parts | **Microservices** |
| loose coupling, async, many consumers | **Event-driven** |
| modular, testable stages | **Pipe-and-Filter** |

> **Architecture is recombination** — you rarely invent a pattern; you choose and combine known ones to meet your quality attributes.
</details>

---

## 7. Event-Driven Architecture & ML design patterns → §6

**C7.1** Explain **Event-Driven Architecture**: the mechanism, four gains, and the costs.

<details><summary><b>Show answer</b></summary>

**Mechanism: publish/subscribe over a broker.** A producer emits an **event**; any number of consumers subscribe. **Producer and consumer never know about each other.**

| Gain | Why |
|---|---|
| **Loose coupling** | services depend on the *event*, not on each other |
| **Independent scaling** | slow consumers scale up without touching producers |
| **Extensibility** | add a new consumer **without changing the producer** |
| **Buffering** | the queue absorbs spikes |

**Costs:** **eventual consistency** · harder debugging (**no single call stack**) · message-ordering and duplicate concerns.

It is the **backbone linking CQRS and streaming features**.
</details>

**C7.2** Why is **Git not a model registry**? Compare them.

<details><summary><b>Show answer</b></summary>

| | **Git** | **Model registry** |
|---|---|---|
| Stores | **code** (lightweight text) | **model artifacts + metadata** |
| Tracks | diffs, branches | **version, metrics, lineage, stage, approval** |
| Big binaries | **bloats the repo — do not** | designed for it |

**The Model Registry pattern** = the **source of truth** for models: it **versions and governs** them with full **lineage**, enabling **promotion** (staging → production) and **rollback**.

> ⚠️ **Git is not a model registry — do not put weights in Git.** Use **DVC** for data and model files, and **MLflow** for experiments plus the registry.
</details>

**S7.1 · Scenario.** A team commits `model.pkl` (400 MB) to Git on every retrain. Six months later `git clone` takes 40 minutes and nobody can say which version is live in production. Diagnose and fix.

<details><summary><b>Show answer</b></summary>

**Diagnosis — two separate failures:**

**1 · Wrong tool for the artifact.** Git stores **lightweight text** and tracks **diffs**; a 400 MB binary has no meaningful diff, so **every retrain stores a whole new copy**. The repo **bloats**, permanently — history cannot simply be deleted without a rewrite. Hence the 40-minute clone.

**2 · No governance, which is the more expensive problem.** Git tracks **diffs and branches**. It does **not** track **version, metrics, lineage, stage or approval**. So there is no record of which model is **promoted to production**, what data trained it, what it scored, or who approved it — which is exactly why nobody can say what is live.

**The fix:**
- **DVC** for the data and model files — Git keeps a small pointer, the binary lives in **cloud storage**. Clone time collapses; versioning survives.
- **MLflow** for experiments **and the registry** — the **source of truth** that **versions and governs models with full lineage**, enabling **promotion (staging → production)** and **rollback**.
- Git keeps doing what it is good at: the **code**.

**What this buys operationally:** a one-click **rollback** to the previous approved model, an auditable **lineage** trail (post-midsem §25 — *which model version ran, which code produced it, what inputs*), and a clean tie-in to **deployment strategies** (§22) since Blue/Green and Canary both assume you can name and retrieve the previous version.
</details>

**C7.3** Compare **batch** and **real-time** serving, and give the rule for choosing.

<details><summary><b>Show answer</b></summary>

| | **Batch** | **Real-time (online)** |
|---|---|---|
| When predictions are made | on a schedule, for many records at once | on demand, per request |
| Latency | minutes–hours | milliseconds |
| Cost | low per prediction | higher (always-on infrastructure) |
| Example | nightly churn scores, Netflix recommendations | fraud check at checkout |

> 🎯 **Pick freshness by use case: no more than you need** (extra freshness = extra cost and complexity) **and no less** (stale predictions lose their value).
</details>

---

## 8. Agentic AI & coordination patterns → §7

**C8.1** Give the agentic AI equation, the loop, and the four components.

<details><summary><b>Show answer</b></summary>

**From chatbots to doers.** A chatbot *answers*; an agent *acts*.

> **Generative AI + Reasoning + Tools + Feedback loops → Agentic AI**

An **agent** = an **LLM reasoning engine + memory + tools** running a loop:

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
</details>

**C8.2** Explain the **SAGA** pattern and the difference between **orchestration** and **choreography**.

<details><summary><b>Show answer</b></summary>

**SAGA** — a long transaction is split into a **sequence of local transactions**. If step *n* fails, run **compensating transactions** to undo steps *n−1 … 1*.

> 🌍 Book flight → book hotel → book car. The car booking fails → *compensate*: cancel the hotel, cancel the flight. **There is no global rollback across services, so you undo forward.**

| | **Orchestration** | **Choreography** |
|---|---|---|
| Control | a **central coordinator** tells each service what to do | each service **reacts to events** from the previous one |
| In agents | a supervisor agent directing sub-agents | **prompt chaining** / event-driven agents |
| Pros | easy to follow, one place to debug | loose coupling, no single bottleneck |
| Cons | the coordinator is a **single point of failure** | the flow is **implicit** and hard to trace |
</details>

**C8.3** Explain the **Blackboard** pattern and the rule for choosing between it and SAGA.

<details><summary><b>Show answer</b></summary>

**Blackboard** — a **shared state (the "blackboard")** plus a **controller**. Specialist agents watch the blackboard; whichever one can contribute next writes its partial result, and the **controller decides who goes next**.

> 🎯 **Use Blackboard when there is no fixed algorithm** — the path to the solution is **discovered, not planned**.
> **Use SAGA when the steps *are* known but can fail partway.**
</details>

**S8.1 · Scenario.** Choose the coordination pattern and justify.
(a) An agent that books a trip: flight, then hotel, then car — each through a different supplier API, any of which can fail.
(b) A team of specialist agents diagnosing a production incident from logs, metrics and traces, where nobody knows in advance which signal will identify the cause.

<details><summary><b>Show answer</b></summary>

**(a) Trip booking → SAGA.**
**Justify:** the steps **are known in advance** — flight, hotel, car, in that order — but **each can fail partway**, and they sit behind **different suppliers**, so there is **no global rollback across services**. SAGA splits it into a **sequence of local transactions** with **compensating transactions** to **undo forward**: the car fails → cancel the hotel → cancel the flight.
**Orchestration or choreography?** For an agent booking a trip, **orchestration** — a **supervisor agent directing sub-agents**. It is **easy to follow with one place to debug**, which matters when real money is being committed. **Trade-off accepted:** the coordinator is a **single point of failure**. Choreography would give **loose coupling and no bottleneck** but an **implicit flow that is hard to trace** — a poor bargain when you must explain a failed booking to a customer.

**(b) Incident diagnosis → Blackboard.**
**Justify:** **there is no fixed algorithm.** Nobody knows whether the answer will come from logs, metrics or traces — the **path to the solution is discovered, not planned**. So use a **shared blackboard** holding the evolving hypothesis, with **specialist agents** (a log agent, a metrics agent, a trace agent) watching it and **each contributing when it has something to add**, while the **controller decides who goes next** as evidence accumulates.
**Trade-off accepted:** the process is non-deterministic and harder to bound — you cannot promise how many steps it will take, or that it terminates without a step limit.

> 🎯 **The one-line discriminator: known steps that can fail → SAGA. Unknown path → Blackboard.**
</details>

---

# ⭐ Cross-cutting integration question

**S-X1 · Scenario.** A retailer wants an ML system that answers customer questions about their own order history and product policies. Walk from requirement to architecture, naming the course concept at each step.

<details><summary><b>Show answer</b></summary>

**1 · Should this be ML at all? (§3, Hulten)**
- *Complex or changing logic?* **Yes** — natural-language questions cannot be enumerated as rules.
- *Learnable from data?* **Yes** — and better still, most of it is **retrieval**, not learning.
- *Mistakes tolerable?* **Yes, with design** — a wrong policy answer is embarrassing but recoverable, provided there is escalation to a human. **Design for mistakes.**
**Verdict: use ML, as an auxiliary component** — the store works without it.

**2 · Goals (§3, four levels).**
Organisational: *cut support cost.* Product: *answer order and policy questions.* User: *a fast, correct answer.* Model: *a measurable grounding threshold*, e.g. faithfulness above an agreed bar.

**3 · Quality attributes, SMART (§4).**
Not "fast and accurate" but *"95% of answers return in under 2 s"* and *"every answer cites the policy document it came from."* Note which QAs ML makes first-class here: **explainability** (citations), **privacy** (order history is personal data), **security**, **robustness**.

**4 · Pattern selection (§5).**
- **RAG** — the requirement is literally *ground an LLM in private data without retraining*. It **reduces hallucination and makes answers citable**, which is what the explainability QA demanded.
- Structurally RAG is **Pipe-and-Filter + CQRS**: retrieve → rank → augment → generate, with reads (questions) far outnumbering writes (document updates) — **exactly where CQRS shines**.
- **Monolith or microservices?** Start **monolithic** unless there are already several models with different scaling needs. **Let requirements, not fashion, drive it.**

**5 · Serving freshness (§6).**
Answering a live customer is **real-time (milliseconds–seconds)**. But **embedding the policy documents** is a **batch** job on a schedule. **Pick freshness by use case: no more than you need, and no less.**

**6 · Event-driven glue (§6).**
When a policy document changes, emit an **event**; the re-embedding consumer subscribes. **Loose coupling** — the document system never needs to know the ML system exists — plus **extensibility** for the next consumer, at the cost of **eventual consistency**: a freshly edited policy is answerable only after re-embedding.

**7 · Model governance (§6).**
Prompts, retrievers and any fine-tuned models go in a **model registry** with **lineage, promotion and rollback** — **not Git**, which stores code, not artifacts and metadata.

**8 · If it becomes agentic (§7).**
The moment it can *act* — issue a refund, cancel an order — it stops being a chatbot: **Generative AI + Reasoning + Tools + Feedback loops → Agentic AI**. A refund flow is **SAGA** (known steps, can fail, needs **compensating transactions**), run by **orchestration** so there is one place to debug.

**9 · Then hand off to the post-midsem half.**
Evaluate with **RAGAS** (§15), test in production with **Shadow → Canary** (§13, §22), watch for **prediction-distribution drift** (§12), and review **fairness, privacy and security** (§27, §29, §30) before launch.
</details>

---

## ✅ Progress checklist

Tick only what you answered **without opening the box**.

| § | Chapter | C | S |
|---|---|:---:|:---:|
| 1 | SE vs ML | ☐ ☐ | — |
| 2 | Model vs system, technical debt | ☐ ☐ ☐ | ☐ |
| 3 | When to use ML · goals | ☐ ☐ | ☐ |
| 3 | **GR4ML** ⭐ | ☐ ☐ | ☐ |
| 4 | Quality attributes · Pipe-and-Filter | ☐ ☐ ☐ | ☐ |
| 5 | CQRS · RAG · Mono vs Micro ⭐ | ☐ ☐ ☐ ☐ | ☐ ☐ |
| 6 | Event-driven · registry · batch vs real-time | ☐ ☐ ☐ | ☐ |
| 7 | Agentic AI · SAGA · Blackboard | ☐ ☐ ☐ | ☐ |
| — | **Cross-cutting** | — | ☐ |

> If time runs out on this half, the rows that matter are **GR4ML**, **model-centric vs system-centric**, **Monolith vs Microservices (multi-repo!)**, and **SAGA vs Blackboard** — those are the four the mid-term actually asked.
