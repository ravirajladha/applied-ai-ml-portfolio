# Ch 14 — Responsible AI: Ethics, Bias, Transparency &amp; Safety
**Slides: CS#16** (post-midsem deck, PDF pages 82–91)

> ### The cheapest marks in the course
> **~3% of the marks (2.5 on the makeup paper), and there is no arithmetic to
> get wrong.** This is a one-hour chapter. Every answer is a named list plus a
> concrete example, and this file gives you both.

> **⚠ Most of CS#16 is image slides**, so a plain text search of the PDF returns
> almost nothing. Everything below was read off the slide images directly —
> including the two case studies, the Three Layers, and the countermeasures.

> **The past-paper question this chapter answers** (EC3 makeup, Q3B, 2.5 marks):
> *"How can learning agents in AI be designed to adapt to new environments
> without compromising the safety and ethical standards required in high-stakes
> applications such as healthcare or autonomous vehicles?"*
> That is the **Three Layers of AI Safety** slide, almost word for word. It is
> fully worked in §11.

---

## 1. What is ethics? What is AI ethics?

**Ethics.**
> *"Nobody really knows!"* — the slide's own opening line, followed by
> *"Is ethics contextual?"*
>
> **The discipline concerned with what is morally good and bad and morally right
> and wrong.** Its subject consists of the fundamental issues of practical
> decision making, and its major concerns include the nature of ultimate value
> and the standards by which human actions can be judged right or wrong.

**AI ethics.**
> **A set of guidelines that advise on the design and outcomes of artificial
> intelligence.** The definition of a set of **moral values** that AI must comply
> with, and the development of a set of **regulation, guidelines and constraints**
> that AI development must follow.

> **Note the two halves of that definition** — *values* (what is right) **and**
> *regulation* (what is enforced). A full-mark answer names both. The slide
> deliberately opens with "nobody really knows" and "is ethics contextual?" —
> if a question asks you to *discuss*, acknowledging that ethics is contested and
> culture-dependent is part of the answer, not a hedge.

---

## 2. Case study 1 — the healthcare model that looks perfect

This is the deck's narrative spine. Learn it as a story; it answers half the
possible questions on its own.

**The problem.**
> A healthcare system processes thousands of patients daily. Every patient is
> different, with their own medical history and different response to drugs,
> surgery, treatments. Some recover quickly without extra care; others need
> extra treatment or **re-hospitalization**. Healthcare resources are limited.

**The requirement.**
> An AI system that analyses a person's medical history and **predicts whether
> that person will require additional medical care in the future.**

Perfectly reasonable. Nothing suspicious. Hold that thought.

---

## 3. Case study 2 — the CV screener, and the trap

**The problem.**
> The company receives thousands of CVs daily, across many different openings
> (programmer, marketing, administrative, sales…). Skimming them takes enormous
> time and effort, and **good candidates can be erroneously discarded** in the
> preliminary phase.

**The requirement.** An AI system that analyses the CV and takes only the best
candidates.

**The "solution" — read this carefully, the flaw is in plain sight.**
> - Use the **CVs of current employees as ground truth data**.
> - *"We want to select candidates **similar to the people we already have** in
>   our company."*
> - Engineers built it with state-of-the-art models and techniques.

**The results.**
> - The selected people are very good candidates.
> - The system performs **better than our HRs** at selecting good candidates.
> - **All the ML metrics show stunning performance.**
>
> *"Are you happy? Do you approve the system? Did you give a raise to the
> engineers?"*

**Congrats. Here is what you actually built:**

> **"Amazon scraps secret AI recruiting tool that showed bias against women"**
> — Reuters. Amazon's ML specialists uncovered a big problem: their new
> recruiting engine did not like women.
>
> **"Racial Bias Found in a Major Health Care Risk Algorithm"** — Black patients
> lose out on critical care when systems equate health needs with **costs**.

> **⚠ The single most important sentence in this chapter.**
> *"We want to select candidates similar to the people we already have"* is
> **the bug**. If your historical workforce is skewed, a model trained to
> reproduce it will **launder that skew into an objective-looking score**. The
> metrics look great precisely **because** the model faithfully reproduced the
> bias in the label.

### "Well, we can try to fix this, right?" — *"Not so easy kiddo!"*

**Why it is hard to even notice:**
- The problem is **not easily detectable in the first place**.
- The people selected **are in fact good candidates**.
- The prediction of re-hospitalization **is very accurate**.
- The system **still performs better than humans**.
- All the ML metrics show **absolutely stunning performance**.

**"But if we remove all the gender/race info from the data?"**

> **The AI system can infer them.** The slide's own three examples:
> - from the **prevalent male–female colleges**, or from address / geographic info
> - from **sports and activities** (cheerleader) or from disorders more common in
>   one race
> - from **memberships** (female chess team, …) or from **level of care received**

> **This is the exam-ready answer to "why doesn't deleting the protected
> attribute fix bias?"** Because protected attributes are **redundantly encoded**
> across dozens of innocent-looking proxy features. Deleting the column deletes
> your ability to *measure* the bias, not the bias itself.

---

## 4. The main enemy: bias in the data

**Definition (from the slide).**
> **Bias** — the action of supporting or opposing a particular person or thing in
> an **unfair** way, because of allowing **personal opinions** to influence your
> judgement.

**Bias in everyday life — the word-embedding analogies the slide uses:**

```
     he : she   ::   surgeon      : nurse
     he : she   ::   brilliant    : lovely
     he : she   ::   architect    : interior designer
```

> These come out of embeddings trained on ordinary text. **Nobody programmed
> them.** The model learned them because the corpus contains them — which is
> exactly why "we just used the data" is not a defence.

**"Are you sure about your data?" — the four questions to quote:**

1. Have you even **checked the labels** when you downloaded a dataset?
2. Do you know **how** the data is labeled?
3. Do you know **who** labeled the data?
4. Do you **trust** who collected and labeled the data you use?

> If a question asks *"what would you do to reduce bias in an AI system?"*,
> **start with these four.** They are concrete, they are the slide's own words,
> and they beat a vague answer about "using diverse data".

---

## 5. XAI and FAT — the three key challenges

The deck's agenda item 4 is **XAI – FAT: Fairness, Accountability, Transparency.**

| Challenge | The problem, in the slide's words |
|---|---|
| **Fairness** | Whose values decide? The deck points at **moralmachine.net** — the trolley-problem survey showing that different cultures answer differently |
| **Transparency** | *"Almost no idea why Deep Learning works, or doesn't work."* Important for **human–AI teams**. New research agenda: **Explainable AI (XAI)** |
| **Accountability** | *"Who/What is responsible?"* |

**The accountability question, spelled out (the self-driving-car example):**

> Who is responsible when it goes wrong?
> - the **company** who designed the car
> - the **engineer** who designed the ML algorithms
> - the **owner** who bought the car
> - the **driver** who drove the car and gave the training data

> **There is no answer on the slide, and that is the point.** The examinable
> observation is that AI **breaks the normal chain of responsibility**: the
> decision is made by a system whose behaviour nobody fully specified, from data
> that a fourth party supplied. Name all four candidates and say why each is
> partially but not wholly responsible — that is the full-mark answer.

> **Memory hook: FAT = Fairness · Accountability · Transparency.**
> Transparency is *why did it decide that?* Accountability is *who answers for
> it?* Fairness is *whose values decided what "good" means?*

---

## 6. Playing devil's advocate — "humans are not perfect"

The deck deliberately argues **against** itself here. You need this section
because a good answer is balanced, not preachy.

**Human decisions are also biased:**
- **Juror decisions are affected by sport results.** In the US, the best day to
  have a trial is **Monday after a victory** of the local football team — and the
  worst is **Monday after a defeat**.
- Juror decisions are **highly biased toward race and wealth** of the defendant.
- Human decision making is heavily affected by **mood, personal concerns, stress,
  level of sleep, affinity with the assessed person, stereotypes**.
- **There is no universal way to take decisions** → different cultures = different
  decision-making processes.

### "But…" — the human–AI collaboration problem

> *Seems the perfect solution…* Put a human in the loop. Except:
>
> - What if the AI is right **99.999%** of the time?
> - Should the human **check every time**?
> - There are **cognitive biases** whereby, after some time, the human
>   **unconsciously trusts the AI** and is no longer able to spot the errors.
> - What if the AI is right but the human **overrides** the decision?
> - What if the AI is **wrong but so powerful that it convinces the human**?

> **"Just add a human in the loop" is not a complete answer, and examiners know
> it.** The failure mode has a name — **automation bias**: the more reliable the
> system, the less capable the human overseer becomes of catching the rare
> failure. Say that, and you are answering above the level of the question.

---

## 7. Ethics in a broader perspective

### Who owns AI?

**AI needs a (big) infrastructure.**
- The **algorithm is just a small part** of the product.
- **Computational capabilities** (power and memory) are fundamental.
- Only the **biggest companies** can maintain a solid infrastructure
  → substantial advantage over smaller companies **or academia**.

**AI needs a lot of data.**
- Data is essential to **reproduce results**.
- **Data is often more important than the algorithm** — *who owns the data?*
- Big tech acquires huge amounts of data **daily** → substantial advantage.

### The Myth of AI Democratization

**The claim.** Big companies say they are democratic: they share their
**research** (arXiv), **code** (GitHub), **frameworks** (TensorFlow), and
**infrastructure (?)** (Colab).

**What technology democratization actually means:**
> *"…at an increasing scale, consumers have greater access to use and purchase
> technologically sophisticated products, **as well as to participate
> meaningfully in the development** of those products."*

**The reality — AI is currently owned by few companies.** They have access to a
huge amount of data · they attract top AI scientists (huge salaries, freedom) ·
they have the power to **transform research ideas into products**.

**Why AI democracy is important:** avoid **monopolies** · democratization means
**everyone gets the opportunities and benefits** of AI · **openness is proved to
be beneficial** to the development of better technologies.

> **The sharp point:** sharing the *code* is not democratization if you keep the
> *data* and the *compute*. Meaningful participation requires all three.

### AI Singularity

*Exponential progress equals singularity.*
- A historical moment where the **acceleration of progress** is becoming more
  visible.
- AI is becoming more "intelligent" than humans **in many tasks**.
- We could potentially **substitute humans or delegate activities** to AI
  starting today.
- OpenAI is trying to raise **$100B** in coming years toward developing **AGI**.

*In recent times a sort of hysteria arises:*
- A **Google engineer claims an AI chatbot is sentient**.
- ***"Pause Giant AI Experiments: An Open Letter"***
- **The Godfather of AI leaves Google and warns of danger ahead** — **Geoffrey
  Hinton**. *(Name him. Named examples score.)*

### Privacy &amp; Ownership

- ***"ChatGPT Has a Big Privacy Problem"*** — Italy's ban on OpenAI's generative
  text tool.
- ***"Extracting Training Data from Diffusion Models"*** — diffusion models
  **memorise and regenerate individual training images**. The paper's figure shows
  a training-set photo reproduced almost exactly from a text prompt.
- ***"US Copyright Office: AI Generated Works Are Not Eligible for Copyright."***
  **What about code?** What license applies to generated code **is still not
  clear**, and the legal implications of using it in a commercial product are
  **still unknown**.

### Climate Change — the carbon footprint of training a model

> These are the deck's own numbers. **They are quotable and they are the only
> arithmetic in the chapter.**

```
   2019 paper:   280,000 kg CO2   for ONE training of a 213M-parameter NLP model

   GPT-4:        parameter count unknown; some sources say 100T (10^14),
                 a more accurate (and maybe way downward) estimate is 500-1,000B

   One GPT-4 training emits at least   560,000,000 kg CO2
                 (and that ignores much larger data-set costs)

   To stop climate change, a person must emit at most  600 kg CO2 per year.

   ->  560,000,000 / 600  ~=  1,000,000
   ->  ONE training run of GPT-4 consumes as much as ~1 MILLION PEOPLE in a year.
```

> That last line is the one to write down. It is memorable, it is the slide's own
> conclusion, and it converts an abstract worry into a number.

---

## 8. High-risk AI applications

**The framing, in the slide's own words:**
> *"Not a problem if we build course projects or even a thesis, but…"*

**The list — memorise these five:**
- **Diagnosis** applications
- **Control of critical infrastructure**
- **Law enforcement**
- **Scoring**
- **Hiring**

**Four more the deck treats separately:**

| Area | The concrete case on the slide |
|---|---|
| **Media generation** | *"a (mid)journey…"* — the AI-generated image of the Pope in a white puffer jacket that fooled a large part of the internet |
| **Deepfakes** | An app that generates non-consensual nude images from a single photo; and AI being used to generate child abuse imagery |
| **Military** | *"The military wants AI to replace human decision-making in battle"* — a medical **triage** program raises the question: when lives are at stake, should AI be involved? |
| **Education** | *"…and so on"* |

> **⚠ On "risk tiers".** The deck does **not** enumerate formal legal risk tiers.
> What it says is that *"the EU is planning to propose a regulation of AI and its
> applications"* (see §13), and it gives the list above as the informal
> high-risk category. **Answer with the deck's list**, and mention the EU
> regulation as the direction of travel. Don't invent a tier table.

> **The pattern behind the five.** They are all cases where the AI's output
> **directly changes a person's life chances** — their health, their liberty,
> their credit, their job — and where the person **cannot opt out** and often
> **cannot even see** that a model was involved. That sentence generalises the
> list and is worth writing.

---

## 9. Why fair AI is so difficult to obtain

The deck blames the **industrial culture of software**, not the mathematics.

**Industrial history.**

| Software development | Infrastructure / industrial-products engineering |
|---|---|
| Not economically valuable — *"just roll out v1.1 or a security patch"* | **Product recalls and failures** are enormously costly |
| Damage perceived as **cyber rather than physical** | Damage is **very physical** |

**Hype and startuppy culture.**

| Software development | Infrastructure / industrial products |
|---|---|
| **Minimise time to market**, "easy money", clients' care | **Entrenched industry**, public tenders, **educate the client** |

> **The argument in one line:** a bridge engineer who ships a flaw kills people
> and gets sued; a software engineer who ships a flaw ships **v1.1**. When AI
> started making decisions with **physical, human consequences**, it inherited the
> **software** safety culture rather than the **engineering** one. That mismatch —
> not a lack of algorithms — is why fair AI is hard.

---

## 10. The Three Layers of AI (and technology) Safety — *the most examinable slide*

| # | Layer | The one-line request | What it means | Example |
|---|---|---|---|---|
| **1** | **Alignment** | *"Do what I mean given this environment."* | Technology works in **intended** use-cases | **bias and fairness** |
| **2** | **Robustness** | *"Keep doing what I mean in an unforeseen environment."* | Technology is safe even in **unintended** use-cases | **ethics in decisions, adversarial attacks** |
| **3** | **Corrigibility** | *"Enable me to detect and correct your mistakes."* | Imperfect technology can be **detected and improved over time** | **white box models** |

> **Memory hook — the three layers are three tenses.**
> **Alignment** = did you build the *right* thing? (design time)
> **Robustness** = does it hold up *out there*? (deployment time)
> **Corrigibility** = can we *fix* it once we notice? (after the fact)
>
> They are cumulative. Alignment without robustness fails the first time reality
> differs from the lab. Robustness without corrigibility means that when it does
> eventually fail, you cannot tell, and you cannot repair it.

---

## 11. PAST PAPER — EC3 makeup, Q3B (2.5 marks) fully worked

> **"How can learning agents in AI be designed to adapt to new environments
> without compromising the safety and ethical standards required in high-stakes
> applications such as healthcare or autonomous vehicles?"**

**Notice what the question is made of.** *"Adapt to new environments"* is
literally the **Robustness** layer. *"Without compromising safety and ethical
standards"* is **Alignment**. *"High-stakes applications such as healthcare or
autonomous vehicles"* is the **high-risk applications** list. The examiner has
handed you the structure.

### Model answer

> **Assumption stated first:** the agent is a learning agent deployed in a
> high-risk domain (medical diagnosis, autonomous driving), where its output
> changes a person's health or safety and the affected person cannot opt out.
>
> Design it against the **three layers of AI safety**, in order.
>
> **1 · Alignment — "do what I mean in this environment."** Fix the objective
> before the model. The system must optimise the *intended* goal, not a proxy
> that correlates with it. The health-care risk algorithm failed exactly here: it
> **equated health needs with costs**, so Black patients — who historically had
> less spent on them — were scored as needing less care. Concretely: audit the
> **label** and the ground truth, not just the features, and apply the four data
> questions — how was it labeled, by whom, and do you trust them?
>
> **2 · Robustness — "keep doing what I mean in an unforeseen environment."** A
> learning agent that adapts is by definition leaving the distribution it was
> validated on. So bound the adaptation: validate on out-of-distribution and
> adversarial inputs, monitor for **distribution shift** in deployment, and
> constrain the agent to a safe operating envelope with a fallback (hand back to
> a clinician / disengage the autonomy) when confidence drops. Note that
> **removing the protected attribute does not make the agent safe** — it can
> re-infer gender or race from proxies such as college, address, activities or
> level of care received.
>
> **3 · Corrigibility — "enable me to detect and correct your mistakes."**
> Assume it will be wrong. Build for detection and repair: prefer **white-box
> models** where a full input–output audit is possible; where a black box is
> unavoidable, add **post-hoc explanation** (attention maps, occlusion tests,
> counterfactual probing) so a failure can be diagnosed. Log decisions so bias can
> be measured after the fact, and keep a route to retrain and roll back.
>
> **Governance around all three.** A human-in-the-loop is necessary but **not
> sufficient** — with a system that is right 99.999% of the time, **automation
> bias** means the overseer stops being able to spot the rare failure. So the
> human's role must be designed (audit sampling, mandatory justification on
> override) rather than assumed. Accountability must also be assigned in advance
> among the manufacturer, the engineer, the owner and the operator, because the
> normal chain of responsibility does not survive contact with a learned system.

*(Structure: assumption → three named layers, each with a mechanism AND a
concrete example → the governance caveat. Named lists plus real cases. That is
what "vague answers will not be awarded marks" is asking for.)*

---

## 12. How to insert ethics in AI, and the countermeasures

### Ethics by design vs pro-ethical design

| | **Ethics by design** | **Pro-ethical design** |
|---|---|---|
| **What it does** | **Constrains** the choice of agents | **Does not preclude** a course of action, but **requires agents to make up their mind** about it |
| **Character** | **Paternalistic** | Still forces a choice, but **less of a paternalistic nudge** |
| **The analogy** | A **speed bump** — permanent, and leaves **no real choice, especially in an emergency** | A **speed camera** — leaves you the **freedom to choose to pay the ticket**, especially in an emergency |

> **This distinction is a very likely short-answer question**, because the
> speed-bump / speed-camera pair is memorable and the deck states it explicitly.
> The key phrase is *"especially in an emergency"* — a speed bump also slows the
> ambulance; a camera does not.

### Countermeasure 1 — use explainable models (**explainability *a priori***)

- An AI model can be **white box by design** — e.g. **symbolic reasoning systems**.
- We can **theoretically know the output for every possible input**.
- We can **inspect the system** to find biases and weaknesses.
- A white box model is **easier to fix**.

The deck's own example — a rule-list recidivism model:
```
     IF       age between 18-20 and sex is male        THEN predict arrest (within 2 years)
     ELSE IF  age between 21-23 and 2-3 prior offenses THEN predict arrest
     ELSE IF  more than three priors                   THEN predict arrest
     ELSE                                              predict no arrest
```
> Look at line 1. **Because the model is white box, you can see the bias in
> plain text** — "sex is male" is right there. In a neural network the identical
> behaviour would be invisible. **That is the entire argument for white-box
> models**, and it is a better answer than "they are more interpretable."

### Countermeasure 2 — explain black box models (**explainability *a posteriori***)

- **Attention models.**
- **Test the model with different data until the reasons for the input–output
  mapping are inferred.** The two examples:
  - **cover portions of images** until the most important patch is found
    (occlusion testing)
  - **change the data in a loan request** until the bank's AI flips between
    accept and reject (counterfactual probing)

> **⚠ Get the a priori / a posteriori labels the right way round.**
> **White box by design = a priori** (explainable *before* you run it).
> **Probing a black box = a posteriori** (explanation reconstructed *after*).

---

## 13. Summary and advice — straight from the last two slides

**Ethics in AI is still an open issue.**
- Generally it was **not taught to AI scholars**.
- In the last few years ethics was **overshadowed by the incredible results** of
  AI systems.
- **Only now** is AI so pervasive that it can greatly affect people's lives.

**But it is becoming a highly considerable property of present and future AI
systems.**
- Many companies have started **hiring ethicists** in their AI teams.
- **The EU is planning to propose a regulation** of AI and its applications.
- Many **top conferences require** authors to discuss the ethics of any submission.

**Some advice (the deck's closing list — quotable as-is):**
1. **Always think about the possible (ethical) problems** of your AI system.
2. Spend **a lot of** time thinking about the **data** — how it was acquired, how
   it was labeled, the level of generalization.
3. Try to maintain a **collaboration with AI ethicists, AI philosophers**, people
   who care and know about ethics.
4. **Do not fall for easy and fast enthusiasm** — the possible bad outcomes are
   often **hidden and difficult to spot**.
5. Be an **advocate** for ethical AI systems.
6. **How AI takes decisions is often totally different from how humans take the
   same decision.**

> Point 6 is the deck's actual last line, and it is bolded on the slide. It is
> the best closing sentence you can give any ethics answer: an AI that reaches
> the *same* decision as a human may have reached it **for entirely different
> reasons** — which is why accuracy metrics alone can never establish that a
> system is safe.

---

## 14. You try

These are all theory. Write them in **lists with named examples**, not prose —
that is what the marking schemes reward.

**Q1 (2.5 marks).** *"How can learning agents be designed to adapt to new
environments without compromising safety and ethical standards in high-stakes
applications?"* — attempt it before reading §11.

**Q2 (2 marks).** A bank builds a loan-approval model. To avoid discrimination
the team **deletes race and gender from the training data**. Explain, with
examples, why this does **not** guarantee a fair model.

**Q3 (3 marks).** *"Explain the FAT framework in XAI with a relatable real-world
case study."*

**Q4 (2 marks).** Differentiate **ethics by design** from **pro-ethical design**,
with the analogy used in class.

**Q5 (2 marks).** Distinguish **explainability a priori** from **explainability a
posteriori**, and give one technique for each.

**Q6 (3 marks).** *"AI is more objective than humans, because humans are biased
by mood, stereotypes and even sports results. Discuss."*

---

## 15. Answers

### Q1 — see §11 (fully worked against the past paper).

### Q2 (model answer)

> **Deleting the protected attribute removes your ability to measure the bias,
> not the bias itself.** Two independent reasons:
>
> **1 · Proxy features re-encode it.** The model can **infer** gender and race
> from innocuous-looking columns. The class examples: prevalent male–female
> **colleges**; **address / geographic information**; **sports and activities**
> (e.g. cheerleader); **disorders more common in one race**; **memberships**
> (e.g. female chess team); and **level of care previously received**. A postcode
> plus a college name can reconstruct a protected attribute with high accuracy.
>
> **2 · The bias may live in the LABEL, not the features.** If the ground truth
> is historical approvals from biased human officers, the model learns to
> reproduce those officers. This is the **Amazon recruiting tool**: it was trained
> on the CVs of current employees — *"candidates similar to the people we already
> have"* — so it learned to down-rank women, and **all the ML metrics looked
> excellent** precisely because it reproduced the label faithfully.
>
> **What to do instead:** keep the protected attribute **for auditing** (you
> cannot measure disparate impact without it), audit the **label** as carefully as
> the features, apply the four data questions (how, who, and do you trust the
> labeller), and test the deployed model for outcome differences across groups.

### Q3 (model answer)

> **FAT = Fairness, Accountability, Transparency** — the three challenges that
> motivate **Explainable AI (XAI)**.
>
> **Transparency.** We have *almost no idea why deep learning works, or doesn't
> work*. This matters most for **human–AI teams**, where a person must decide
> whether to act on the system's output. XAI is the research agenda addressing it.
>
> **Accountability.** *Who or what is responsible* when the system causes harm?
> For a self-driving car the candidates are the **company** that designed the car,
> the **engineer** who designed the ML algorithms, the **owner** who bought it, and
> the **driver** who drove it and supplied the training data. Each is partly
> responsible and none is wholly responsible — AI breaks the normal chain of
> liability.
>
> **Fairness.** Whose values decide what a good outcome is? The **Moral Machine**
> experiment shows that people from different cultures answer the same
> trolley-style dilemma differently, so there is **no universal decision
> procedure** to encode.
>
> **Case study.** The **health-care risk algorithm** that scored Black patients as
> needing less care. *Fairness* failed because the system equated health needs
> with **costs**, and less had historically been spent on those patients.
> *Transparency* failed because nobody could see that substitution from the
> model's outputs — the accuracy metrics were excellent. *Accountability* failed
> because responsibility was diffused between the hospital that deployed it, the
> vendor that built it, and the billing data that encoded the disparity.

### Q4

| | Ethics by design | Pro-ethical design |
|---|---|---|
| Mechanism | **Constrains** the agent's choices | **Does not preclude** any action, but **requires the agent to make up its mind** |
| Character | **Paternalistic** | Less paternalistic; still forces a choice |
| Analogy | **Speed bump** — permanent, **no real choice, especially in an emergency** | **Speed camera** — you keep the **freedom to choose to pay the ticket**, especially in an emergency |

> **The discriminating detail is the emergency clause.** A speed bump also slows
> the ambulance; a speed camera does not. Ethics-by-design guarantees compliance
> at the cost of removing judgement; pro-ethical design preserves judgement and
> makes you own the consequence.

### Q5

| | **A priori** | **A posteriori** |
|---|---|---|
| Meaning | Explainable **by design**, before you run it | Explanation **reconstructed afterwards** from a black box |
| Model | **White box** — e.g. symbolic reasoning systems, rule lists | Black box — e.g. a deep network |
| Property | You can **know the output for every possible input** and inspect for bias; easier to fix | You **probe** until the input–output mapping is inferred |
| Technique | The rule-list recidivism model — the bias (`sex is male`) is **visible in the source text** | **Attention models**; **occlusion** (cover parts of an image to find the important patch); **counterfactual probing** (change a loan request until accept/reject flips) |

### Q6 (model answer — a balanced 3-mark discussion)

> **The premise is half right, and the conclusion does not follow.**
>
> **In favour.** Human decisions are demonstrably biased. Juror decisions in the
> US are affected by **sport results** — the best day for a trial is Monday after
> a local football victory, the worst is Monday after a defeat — and are
> **biased by the race and wealth of the defendant**. Human judgement varies with
> **mood, stress, sleep, personal concerns, affinity and stereotypes**, and there
> is **no universal decision procedure**: different cultures use different ones.
> An AI is at least **consistent** and **auditable in principle**.
>
> **Against.** Consistency is not objectivity — **a model trained on human
> decisions reproduces human bias at scale and with an objective-looking score.**
> Amazon's recruiting tool learned to reject women; a major health-care risk
> algorithm under-served Black patients. In both cases **every ML metric looked
> excellent**, because the model faithfully reproduced a biased label. And
> **removing the protected attribute does not help** — the system re-infers it
> from proxies such as college, address, activities or prior level of care.
>
> **The extra failure that AI adds.** Human bias is at least distributed across
> many decision makers and is contestable; a deployed model applies **one** bias
> **uniformly, invisibly, and to everyone**, and the affected person usually
> cannot see that a model was involved. Adding a human reviewer does not close the
> gap either: with a system that is right 99.999% of the time, **automation bias**
> means the overseer gradually loses the ability to spot the rare failure.
>
> **Conclusion.** The right claim is not *"AI is more objective"* but *"AI makes
> bias measurable and therefore fixable — if you build for it."* That means the
> **three layers**: alignment (audit the objective and the label), robustness
> (test out of distribution), corrigibility (white-box or post-hoc explanation so
> failures can be found and repaired). And remember the deck's closing line:
> **how AI takes decisions is often totally different from how humans take the
> same decision** — so matching a human's answer never proves it matched a
> human's reasoning.

---

## 16. Two-minute recall card

- **AI ethics = moral values AI must comply with + regulation/guidelines/
  constraints development must follow.** Name **both** halves.
- **The two case studies:** healthcare **re-hospitalization** prediction, and the
  **CV screener trained on current employees' CVs**.
- **The bug, in one phrase:** *"candidates similar to the people we already have."*
  Real outcomes: **Amazon's recruiting tool biased against women**; **racial bias
  in a major health-care risk algorithm** (it equated health needs with **costs**).
- **Why bias is hard to spot:** the selections really are good, the prediction
  really is accurate, it really does beat humans, and **all the metrics look
  stunning**.
- **Deleting race/gender does NOT work** — inferred from **colleges · address ·
  sports/activities · race-linked disorders · memberships · level of care received**.
- **Bias definition:** supporting or opposing something **unfairly** by letting
  personal opinions influence judgement.
- **Embedding bias:** `he:she :: surgeon:nurse · brilliant:lovely ·
  architect:interior designer`.
- **The four data questions:** checked the labels? how labeled? **who** labeled?
  do you **trust** them?
- **FAT = Fairness · Accountability · Transparency.** Transparency → **XAI**.
  Accountability → **company / engineer / owner / driver**. Fairness →
  **Moral Machine**, cultures differ.
- **Devil's advocate:** juror decisions swing on **football results**; the best
  day for a trial is **Monday after a win**.
- **Human-in-the-loop is not a fix — automation bias.** The human stops being
  able to spot errors in a system that is right 99.999% of the time.
- **Who owns AI:** the **algorithm is a small part** — **infrastructure** and
  **data** are the moat. **Data is often more important than the algorithm.**
- **Myth of democratization:** sharing arXiv/GitHub/TensorFlow/Colab is not
  democratization if you keep the **data** and the **compute**.
- **Singularity:** **Geoffrey Hinton** left Google and warned of danger; *"Pause
  Giant AI Experiments"*; OpenAI raising **$100B** toward AGI.
- **Privacy:** Italy banned ChatGPT; **diffusion models regenerate training
  images**; **US Copyright Office — AI-generated works are not copyrightable**,
  and the licence status of generated **code** is unclear.
- **Climate:** 2019 — **280,000 kg CO₂** for one 213M-parameter NLP training. One
  **GPT-4** training ≥ **560 million kg CO₂**; a person's budget is **600 kg/year**;
  so one training ≈ **1 million people for a year**.
- **High-risk list (5):** **Diagnosis · Critical infrastructure · Law enforcement
  · Scoring · Hiring.** Plus **media generation, deepfakes, military, education**.
- **Why fair AI is hard:** software culture ships **v1.1**; engineering culture
  faces **recalls**. AI inherited the wrong safety culture.
- **THE THREE LAYERS — Alignment · Robustness · Corrigibility.**
  *Do what I mean here* · *keep doing it in an unforeseen environment* ·
  *let me detect and correct your mistakes*.
  Examples: **bias/fairness** · **adversarial attacks** · **white box models**.
- **Ethics by design = speed bump** (paternalistic, no choice, blocks the
  ambulance too). **Pro-ethical design = speed camera** (you keep the choice).
- **A priori = white box by design** (rule lists, symbolic systems — the bias is
  visible in the text). **A posteriori = probe the black box** (attention,
  occlusion, counterfactual loan probing).
- **Direction of travel:** companies **hiring ethicists** · the **EU planning AI
  regulation** · top conferences **requiring** an ethics statement.
- **The closing line:** *how AI takes decisions is often totally different from
  how humans take the same decision.*
