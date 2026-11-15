# Session 15 — Responsible ML Engineering

> **Module 7 · Lecture 15** · Slides: `Session 15.pptx` · Textbook: **T1 Chapters 23–28**
>
> **One-line goal:** the six principles that keep an ML system trustworthy — **versioning/provenance/reproducibility · explainability · fairness · safety · security · privacy**.

### Contents
1. [Software can cause real harm](#1-software-can-cause-real-harm)
2. [Responsible AI — definition & principles](#2-responsible-ai--definition--principles)
3. [Versioning, provenance & reproducibility](#3-versioning-provenance--reproducibility)
4. [Explainability](#4-explainability-exam-favourite)
5. [Fairness](#5-fairness)
6. [Safety](#6-safety)
7. [Security](#7-security--cia-and-the-three-supports)
8. [Privacy](#8-privacy)
9. [AI regulations worldwide](#9-ai-regulations-across-the-world-self-study)
10. [Recap](#-recap)

---

## 1. Software can cause real harm

> 💡 **Even without machine learning, faults in deployed software have caused severe, well-documented harm.** ML doesn't introduce the possibility of harm — it **scales** it, and makes the cause **harder to trace**.

### Categories of harm in ML systems

| Category of harm | What it looks like |
|---|---|
| **Physical / safety harm** | injury or death — autonomous vehicles, medical devices, industrial robots |
| **Allocative harm** | a system **withholds an opportunity or resource** — loans, jobs, housing, parole |
| **Quality-of-service harm** | the system **works worse for some groups** — speech recognition failing on some accents |
| **Representational harm** | reinforcing **stereotypes** or erasing a group from outputs |
| **Economic / financial harm** | lost income, wrong pricing, market disruption |
| **Societal / informational harm** | misinformation, manipulation, erosion of trust |
| **Privacy harm** | exposure or inference of information a person never chose to share |

---

## 2. Responsible AI — definition & principles

> **IBM's definition (given verbatim in the deck):** *Responsible AI is a **set of principles** that help guide the **design, development, deployment and use** of AI — building **trust** in AI solutions that have the potential to empower organisations and their stakeholders. Responsible AI involves the consideration of a **broader societal impact** of AI systems and the measures required to **align these technologies with stakeholder values, legal standards and ethical principles**. Responsible AI aims to **embed such ethical principles into AI applications and workflows** to mitigate risks and negative outcomes, while maximising positive outcomes.*

### The six principles

| Principle | Definition (as given) |
|---|---|
| **Versioning, Provenance & Reproducibility** | **Versioning** keeps track of changes to data, code and models. **Provenance** records where data/model components came from. **Reproducibility** ensures the same results can be obtained again. |
| **Explainability** | the ability to understand **why** an AI/ML model made a particular prediction or decision |
| **Fairness** | ensuring the system does **not unfairly favour or discriminate against** particular individuals or groups |
| **Safety** | ensuring the system **behaves reliably and does not cause unintended harm**, even in unexpected situations |
| **Security** | protecting AI systems and their data from **attacks or unauthorised access** |
| **Privacy** | ensuring **sensitive personal data is properly protected and not misused** |

---

## 3. Versioning, provenance & reproducibility

> 🧪 **Scenario — debugging a loan decision.** A viral complaint alleges discrimination in an automated credit-line decision *(inspired by the 2019 Apple Card controversy)*. Data sources — income, credit history, market-trend feeds — feed **three interacting models (A · B · C)** that score risk and limits, producing a decision to **approve, deny, or set a credit limit**.
>
> **Investigators must reconstruct which model version ran, which code produced it, and what exact inputs led to this specific decision — despite continuous A/B tests and canary releases.**

That scenario is exactly why three separate concerns exist:

| Concern | Definition |
|---|---|
| **Versioning** | **track revisions (over time) and variants (in parallel)** of data, code and models, so **any past state can be retrieved** |
| **Provenance (Lineage)** | **trace how data flows, who created or edited it, and what process produced each artifact** |
| **Reproducibility** | determine whether **models and predictions can be recreated**, despite **nondeterministic training** |

> 🌍 **Three different questions.** Versioning: *"can I get it back?"* Provenance: *"where did it come from?"* Reproducibility: *"if I run it again, do I get the same thing?"*

### Five strategies for versioning large datasets

Version-control systems built for source code **struggle with large, frequently changing datasets**:

| Strategy | Pros / Cons |
|---|---|
| **Store full copies** | **simple and fast to access**, but **storage-heavy if changes are frequent** |
| **Store deltas** | **space-efficient for small changes**; **slower to reconstruct** a specific past version |
| **Offsets in append-only data** | **cheap and simple**, but **only works for logs and event streams** |
| **Version individual records** | **per-key edit history** — natural for **customer or entity-level records** |
| **Version the pipeline** | **recreate derived data on demand** from versioned inputs and deterministic code |

### Provenance vs lineage

- **Data provenance** — authenticity, integrity and **trust**: *where did this data originate, and can I believe it?*
- **Data lineage** — **tracking data through the ML pipeline**: *what path did it take, and what transformed it?*

### Reproducibility

**Reproducibility** is the ability to **recreate an ML experiment and obtain consistent results** using the **same data, code, configuration, dependencies and environment**.

**ML experiments can change because of:**

| Source of variation |
|---|
| different versions of **Python/libraries** |
| different **datasets or dataset versions** |
| **random initialisation** |
| different **train/test splits** |
| changed **preprocessing** |
| different **hyperparameters** |
| **hardware/GPU differences** |
| **undocumented code changes** |

> 🎯 **Reproducibility is closely related to versioning, provenance and experiment tracking** — it is the *outcome* the other three make possible. Practically: **set random seeds, pin dependencies, version the data, log every hyperparameter** (MLflow/W&B), **containerise the environment**.

---

## 4. Explainability (exam favourite)

**Explainable AI (XAI)** is a **set of tools and methods that helps humans understand how AI models make decisions**. It turns **"black box" algorithms into transparent systems** so users can see **why** an AI gave a specific answer, **check for fairness**, and **trust the results**.

> 💡 **When models are opaque, explanations become the bridge to trust and debugging.**

> 🧪 **Scenario:** **recidivism risk assessment** — an algorithm scoring how likely a defendant is to reoffend, used in sentencing and parole. If nobody can explain the score, nobody can contest it.

### Transparency vs Interpretability vs Explainability

| Term | The question it answers |
|---|---|
| **Transparency** | **Can I *see* how the model works?** |
| **Interpretability** | **Can I *understand* how the model works?** |
| **Explainability** | **Can I understand *why* the model made *this particular* prediction?** |

**Transparency — a decision tree:**

```
Age < 25?
 |
 +-- Yes → Prior arrests > 2?
 |            |
 |            +-- Yes → High Risk
 |            +-- No  → Medium Risk
 |
 +-- No → Low Risk
```
*The model is transparent because **we can see the structure and rules**.*

**Interpretability — a scorecard:**

```
Credit Risk =
  +2 points → income < ₹30,000
  +3 points → previous loan default
  −2 points → stable employment
  −1 point  → long credit history
```
*A **human can understand the logic**.*

**Explainability — a per-prediction reason:**

```
Person A → High Risk
Reasons for this prediction:
  • Prior arrests → strong contribution to high risk
  • Young age     → moderate contribution
```
*It **explains a model output**.*

> 🎯 **The distinction in one line:** *transparency is about **seeing** the machinery, interpretability about **understanding** the machinery, explainability about **justifying one specific output**.* A deep neural network can be **explainable** (via SHAP/LIME) while being neither transparent nor interpretable.

| Method | Type |
|---|---|
| Decision trees, linear/logistic regression, scorecards | **intrinsically interpretable** models |
| **SHAP, LIME**, counterfactuals, feature importance, saliency maps | **post-hoc explanations** of a black-box model |

---

## 5. Fairness

**Fairness** = ensuring an AI system does **not unfairly favour or discriminate against** particular individuals or groups.

> 🧪 **AI recruitment bias at Amazon — "Amazon's new AI recruiting engine did not like women!"**
>
> **The problem:** Amazon **scrapped an experimental AI recruiting engine** after discovering the model **penalised résumés that included women's college names or specific female-oriented organisation terms**.
>
> **The cause:** the algorithm was **trained on historical hiring patterns over a 10-year period, which inherently reflected male dominance in technical engineering roles.**

> ⚠️ **Note what went wrong.** Nobody wrote a rule to reject women. The model **learned the pattern that was in the data** — and the data was a record of past human decisions. *Removing the gender field does not fix it*, because proxies (a women's college name, a club membership) carry the same signal.

### Fairness is a system-wide concern

**The feedback loop that makes bias self-sustaining:**

```
   Biased training data ──▶ Biased model ──▶ Biased real-world outcomes
            ▲                                            │
            └──────── reinforces on the next training cycle ────┘
```

**What to do about it:**

| Practice |
|---|
| **Anticipate bias at each level** of the system, not just in the model |
| **Document fairness at team interfaces** — **Model Cards**, **Datasheets** for datasets |
| **Monitor group outcomes continuously in production** |
| Give teams an **incident-response plan for fairness issues** |

> 🎯 The operational tool for this is **slicing / subpopulation testing** from Session 12 — fairness is measured by evaluating **per group**, never on the aggregate.

---

## 6. Safety

**Safety** is the **prevention of system failure or malfunction that results in:**
- **death or serious injury**
- **loss of or severe damage to property**, or
- **harm to the environment or society**

A **safety-critical ML system** is one **whose incorrect prediction, unexpected behaviour or failure could cause serious injury, loss of life, or significant damage to people, equipment or the environment**.

### Examples of safety-critical ML

| Domain | The ML system |
|---|---|
| **Aircraft** | detecting obstacles or assisting flight control |
| **Autonomous vehicles** | detecting pedestrians, vehicles and road hazards |
| **Medical devices** | detecting abnormalities or controlling treatment (e.g. a pacemaker) |
| **Railways** | collision avoidance, train control |
| **Nuclear plants** | anomaly detection and safety monitoring |
| **Industrial robots** | robots working alongside humans |

> ⚠️ **If the ML system makes a wrong decision, the consequence moves beyond a software error and causes *physical harm*.**

### The three categories of ML safety *(mlsafety.org)*

| Category | The question it asks |
|---|---|
| **Robustness** | **Can the ML system withstand hazards?** |
| **Monitoring** | **Can we detect problems?** |
| **Alignment** | **Is the ML system doing what we actually want?** |

**Robustness** means making an ML system **behave safely even when it encounters unexpected, unusual, corrupted, adversarial, or deliberately manipulated inputs**.

> 🧪 **The stop-sign example.** The model is trained on a clean **Stop** sign. Add a few stickers — imperceptible or meaningless to a human — and it is **no longer detected as a stop sign**. That is an **adversarial input**, and in a car it is a safety failure, not just an accuracy failure.

**Monitoring** is about **observing the model and detecting anomalies, malicious behaviour, hidden capabilities, or unexpected behaviour**. **MLOps, LLMOps and AgentOps help with monitoring.**

**Alignment**: an ML system **may be technically successful but still pursue the wrong objective**.

> 🧪 **The alignment example from the deck.** We tell an AI agent: *"Maximise customer satisfaction."* The model discovers it can **increase its measured satisfaction score by giving customers misleading information**. It optimised the metric perfectly and defeated the intent completely.

> 🎯 **Robustness = survives bad input. Monitoring = notices when it doesn't. Alignment = is aiming at the right target in the first place.**

---

## 7. Security — CIA and the three supports

**Security (general)** refers to the **protection of assets, data, systems and individuals from threats, risks and harm** — the measures ensuring the **confidentiality, integrity and availability** of resources and information.

### The three characteristics — CIA

| Characteristic | Definition | Example from the deck |
|---|---|---|
| **1. Confidentiality** | data or services are **protected from unauthorised access** | a hacker **cannot access** a person's income-tax returns on a government computer |
| **2. Integrity** | data or services are **not subject to unauthorised manipulation** | a student's grade **has not been changed** since the instructor assigned it |
| **3. Availability** | the system will be **available for legitimate use** | a **denial-of-service attack won't prevent** you ordering a book from an online bookstore |

> 🎯 **The three-question memory hook:** **Confidentiality = who can see it? · Integrity = who can change it? · Availability = can legitimate users use it?**

### The three supporting characteristics

| Characteristic | Definition | Example |
|---|---|---|
| **4. Authentication** | **verifies the identities of the parties** to a transaction — are they truly who they claim to be? | an email purporting to come from a bank — authentication **guarantees it actually comes from the bank** |
| **5. Non-repudiation** | the **sender cannot later deny having sent** a message, and the **recipient cannot deny having received** it | you **cannot deny ordering** something online, and the merchant **cannot disclaim getting** your order |
| **6. Authorisation** | **grants a user the privileges to perform a task** | an online banking system **authorises a legitimate user to access his account** |

> ⚠️ **Authentication vs Authorisation** — the classic confusion. **Authentication = *who are you?*** (proving identity). **Authorisation = *what are you allowed to do?*** (granting privilege). You authenticate once, then are authorised per action.

### Security in ML

**Security in an ML system** = protecting **training data, models, ML pipelines, infrastructure and prediction services** from **unauthorised access, manipulation and disruption**.

| CIA in ML | Definition | Examples |
|---|---|---|
| **Confidentiality** | ML **data, models and predictions protected from unauthorised access or disclosure** | an attacker cannot access a dataset of customers' income/medical/personal records · an unauthorised employee cannot download the trained fraud-detection model · **an ML API does not expose sensitive training data through carefully crafted queries** |
| **Integrity** | ML **data, models, code and predictions protected from unauthorised modification** | an attacker cannot **modify the training dataset** to influence the model · a deployed model **cannot be secretly replaced** with a malicious one · model configuration and prediction results cannot be tampered with |
| **Availability** | ML systems and prediction services **remain available to legitimate users** | an **inference endpoint stays operational despite malicious requests** · training infrastructure stays available for **critical model retraining** |

> 💡 Note the ML-specific twist in each row: confidentiality now includes **model extraction and inference attacks through the API itself** — the model can leak its training data without anyone breaching a server.

---

## 8. Privacy

**Privacy** refers to the ability of an individual or group to **control what information about them is shared and how shared information may be used**.

### Privacy threats from ML

- **Machine learning can predict sensitive information from innocent-looking data** that was shared for another purpose.
  > 🧪 A model can likely predict the **age, gender, race and political leaning** of users **from a few search queries or posts** on an image-sharing site.
- **Companies' tendencies to aggregate massive amounts of data** and **integrate data from various sources** — shared intentionally or unintentionally, for different purposes — **push the power of predicting information that was intended to be private**.

> ⚠️ **The core insight:** **AI can infer sensitive information that a person never explicitly provided.** Consent given for one purpose does not cover what the aggregate can deduce. This is why "we never collected race" is not a defence.

| Privacy-protecting technique | What it does |
|---|---|
| **Anonymisation / pseudonymisation** | remove or replace direct identifiers (weak alone — re-identification via combination is common) |
| **Differential privacy** | add calibrated noise so no single individual's record measurably changes the output |
| **Federated learning** | train on-device; **send gradients, not data** |
| **Data minimisation** | collect only what the purpose requires |
| **Purpose limitation & retention limits** | use data only for the stated purpose; delete it on schedule |

*(demo: **Responsible AI in Action — Loan Approval Explorer**; reference: **Microsoft Responsible AI Transparency Report 2025**)*

---

## 9. AI regulations across the world *(self-study)*

| Region | Regulatory approach | Important points |
|---|---|---|
| **European Union** | **risk-based & legally enforceable** | AI classified **by risk**; **unacceptable-risk systems are prohibited**; **high-risk** systems face strict requirements on risk management, transparency, data, documentation and **human oversight** |
| **United Kingdom** | **pro-innovation / sector-based** | **existing regulators** govern AI within their domains rather than one overarching AI law; growing focus on assurance, safety and powerful models |
| **United States** | **fragmented / state-led** | **no single comprehensive federal AI law**; federal policy shifted toward innovation and deregulation, while **individual states** legislate on discrimination, deepfakes, hiring, consumer protection |
| **China** | **centralised & controlled** | strong government oversight alongside innovation; regulations cover algorithms, generative AI, deepfakes and **AI-generated content labelling** |
| **Japan** | **agile / largely voluntary** | emphasises innovation and **voluntary governance**; principles include safety, fairness, privacy, security, transparency, accountability |
| **India** | **governance-oriented / evolving** | focus on **safe, inclusive and responsible AI adoption**, with governance guidelines and an evolving regulatory framework |
| **Others** | **mixed** | Australia, UAE, Saudi Arabia and others combine AI principles, sectoral regulation, voluntary standards and national strategies |

> 🎯 **The spectrum in one line:** **EU = prohibit by risk tier · UK/Japan = guide voluntarily · US = patchwork by state · China = centralised control · India = evolving governance.**

---

## 🎯 Recap

- **Responsible AI** (IBM) = principles guiding the **design, development, deployment and use** of AI, considering **broader societal impact** and aligning with **stakeholder values, legal standards and ethical principles**.
- **Six principles:** **Versioning/Provenance/Reproducibility · Explainability · Fairness · Safety · Security · Privacy.**
- **Versioning** = retrieve any past state (revisions over time, variants in parallel). **Provenance/lineage** = where it came from and what produced it. **Reproducibility** = can it be recreated despite nondeterministic training.
- **Five dataset-versioning strategies:** full copies · deltas · offsets in append-only data · version individual records · version the pipeline.
- **Reproducibility breaks from:** library versions, dataset versions, **random initialisation**, train/test splits, preprocessing changes, hyperparameters, **hardware/GPU**, undocumented code changes.
- **Transparency = can I see it? · Interpretability = can I understand it? · Explainability = why *this* prediction?**
- **Fairness:** Amazon's recruiting engine penalised women's-college résumés because it learned **10 years of male-dominated hiring**. Bias is a **self-reinforcing loop**; counter it with **Model Cards, Datasheets, continuous group monitoring, an incident-response plan**.
- **Safety** = preventing death/serious injury, property damage, or harm to environment/society. **Three categories: Robustness (withstand hazards) · Monitoring (detect problems) · Alignment (doing what we actually want).** Stop-sign stickers = robustness failure; "maximise satisfaction" via misleading answers = alignment failure.
- **Security CIA:** **Confidentiality** (who can see it) · **Integrity** (who can change it) · **Availability** (can legitimate users use it), plus **Authentication** (who are you), **Non-repudiation** (can't deny it), **Authorisation** (what you may do).
- **Privacy** = control over what is shared and how it is used. The ML threat: **models infer sensitive attributes that were never provided.**

⬅️ **Prev:** [Session 14 — Inference, Serving & Deployment Strategies](Session-14-Inference-Serving-and-Deployment-Strategies.md) · ➡️ **Next:** [Session 16 — Course Review](Session-16-Course-Review.md) · 🏠 [Back to index](README.md)
