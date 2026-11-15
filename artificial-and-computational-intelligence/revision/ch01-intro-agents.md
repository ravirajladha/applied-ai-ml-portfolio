# Ch 1 — Intro to AI, Agents & Environments
**Slides: CS#1 and CS#2** (pre-midsem deck, pages 1–13)

> Open `explainers/ch01-agents-and-environments.html` first — it has a PEAS
> builder and an environment-classification drill you can click through.

This chapter is **light on maths and heavy on marks**. It is almost all
definitions, and definitions are the cheapest marks in the paper. The two things
that actually get *asked* are: **write the PEAS for X**, and **classify the
environment of X along all six axes**. Everything else is background.

---

## 1. The four definitions of AI

The classic 2×2. Rows = thought vs behaviour. Columns = human-like vs rational.

|  | Human Performance | Rational Performance |
|---|---|---|
| **Thought / Reasoning** | (1) Thinking Humanly | (3) Thinking Rationally |
| **Acting** | (2) Acting Humanly | (4) Acting Rationally |

### (1) Thinking Humanly — Cognitive Modelling
Uses **cognitive science**. Capture human thinking via **introspection**,
**psychological experiments**, **brain imaging**.
- Example: **General Problem Solver** (Newell & Simon, 1961). Problems
  represented by **Horn clauses**. First AI machine with **KB + inference
  separation**. Judged by comparing its *reasoning trace* to human traces.
- Problem: very hard to know how humans really think; we post-rationalise.
- Slide's own jab: *aeronautical engineering does not define its goal as
  "machines that fly so exactly like pigeons they fool other pigeons".*

### (2) Acting Humanly — Turing Test
If an interrogator cannot tell whether replies come from a human or a computer,
the computer is intelligent.

**Skills needed to pass:** NLP, Knowledge Representation, Automated Reasoning,
Machine Learning. Add **Computer Vision + Robotics** for the **Total Turing Test**.

- **Loebner Prize** — annual, Boston.
- **Eugene Goostman** — chatbot pretending to be a 13-year-old Ukrainian boy;
  fooled **10 of 30** judges.
- Problems: not **reproducible**, not **constructive**, not **mathematically
  analysable**. Also the reverse failure — real experts get called machines
  (Shakespeare experts, Shakuntala Devi).

### (3) Thinking Rationally — Laws of Thought
**Aristotle**, 3rd century BC, invented **formal logic** and **syllogisms**.

```
All boring classes put students to sleep
This is a boring class
--------------------------------------
Students sleep in this class
```

Two problems: (a) not all intelligent behaviour goes through logical
deliberation — **reflexes** don't; (b) **computationally exhaustive** even with a
few hundred facts, so it does not scale.

### (4) Acting Rationally — The Rational Agent  ← **this course**
> **Rational agent** = one that acts so as to achieve the best outcome, or when
> there is uncertainty, the best **expected** outcome.

Rationality covers three cases:
- **Correct inference** — logical reasoning to pick an action (when to brake).
- **Inference where no correct inference exists** — a self-driving car choosing
  during an unavoidable accident to minimise harm.
- **Acting without inferring** — recoiling from a hot stove. A reflex.

**Computational limits make perfect rationality unachievable** — so we design
the best program for the machine resources available.

---

## 2. Rationality: four words people confuse

| Term | One-line meaning |
|---|---|
| **Rational** | Does what maximises *expected* performance, given percepts so far + built-in knowledge |
| **Omniscient** | Knows the *actual* outcome of every action. Impossible. **Rationality ≠ omniscience.** |
| **Autonomous** | Behaviour determined by its **own experience** — it learns and adapts, rather than relying only on the designer's built-in knowledge |
| **Bounded rationality** | Optimise the performance measure given our state of knowledge **and limited computational resources** |

The full definition, worth quoting verbatim:

> "For each possible percept sequence, [a rational agent] does whatever action is
> expected to **maximise its performance measure**, on the basis of the evidence
> perceived so far and whatever built-in knowledge the agent has."

A rational agent also does **information gathering / exploration** — it can act
purely to change its own future percepts.

---

## 3. Agents — the core definitions

> An **agent** is anything that can be viewed as **perceiving its environment
> through sensors** and **acting upon that environment through actuators**.

| Agent | Sensors | Actuators |
|---|---|---|
| Human | eyes, ears, other organs | hands, legs, mouth |
| Robotic | cameras, infrared range finders | motors |
| Software (softbot) | keyboard/file/network input | screen, file writes, network |

### Formula box

```
Agent function     f : P*  ->  A       maps PERCEPT HISTORIES to ACTIONS
     P*  = percept sequences (all histories)
     A   = actions

agent = architecture + program
     architecture = the physical system the program runs on
     program      = implements the agent function f
```

> **Exam trap:** the agent *function* is the abstract mapping (a maths object);
> the agent *program* is the concrete implementation. They are not the same
> thing, and the difference is a favourite one-mark question.

**AI agent vs Agentic AI** (from the slides — the difference is **autonomy**):
- *AI agent*: a support bot answering FAQs from scripts or learnt rules.
- *Agentic AI*: a network of bots that escalate issues, analyse sentiment, adapt,
  and coordinate with backends — where **task bifurcation, orchestration and
  pipelining are themselves learnt autonomously**.

### The vacuum-cleaner agent (the running example)
- **Percepts:** location and contents, e.g. `[A, Dirty]`
- **Actions:** `Left`, `Right`, `Suck`, `NoOp`
- Possible performance measures: dirt cleaned, time taken, electricity consumed,
  noise generated.

---

## 4. PEAS — the #1 exam question in this chapter

> Before designing an agent, specify the **task environment** with **PEAS**:
> **P**erformance measure, **E**nvironment, **A**ctuators, **S**ensors.

### The three worked PEAS from your slides — learn these verbatim

**Automated taxi driver**

| | |
|---|---|
| **P** | Safe, fast, legal, comfortable trip; maximise profits |
| **E** | Roads, other traffic, signals, pedestrians, carts, customers |
| **A** | Steering wheel, accelerator, brake, signal, horn |
| **S** | Cameras, sonar, speedometer, GPS, odometer, engine sensors, keyboard |

**Medical diagnosis system**

| | |
|---|---|
| **P** | Healthy patient, minimise costs, minimise lawsuits |
| **E** | Patient, hospital, staff |
| **A** | Screen display — questions, tests, diagnoses, treatments, referrals |
| **S** | Keyboard — entry of symptoms, findings, patient's answers |

**Part-picking robot**

| | |
|---|---|
| **P** | Percentage of parts in correct bins |
| **E** | Conveyor belt with parts, bins |
| **A** | Jointed arm and hand |
| **S** | Camera, joint angle sensors |

### How to write a PEAS you have never seen

1. **P** — *how is it scored?* Give 2–4 measures, and include at least one
   **cost/efficiency** one (time, money, energy) alongside the obvious success one.
2. **E** — *what is out there?* List the physical things AND the other agents.
3. **A** — *what can it change?* Only things that act ON the environment.
4. **S** — *what can it read?* Only things that read FROM the environment.

> **The mistake that loses marks:** putting a sensor in the Actuators row.
> A camera is a **sensor**. A screen display is an **actuator** (it changes the
> world by showing something). Ask "does this push out, or pull in?"

---

## 5. Properties of environments — the #2 exam question

Six axes. Learn them as three-word triggers.

| Axis | Definition | Examples |
|---|---|---|
| **Fully / Partially / Non observable** | Do the sensors give access to the **complete state** at each point in time? | Full: tic-tac-toe, chess. Partial: **poker** (can't see opponents' cards) |
| **Deterministic / Stochastic** | Is the next state **completely determined** by current state + action? | Deterministic: chess. Stochastic: robot football, poker, autonomous driving, agricultural robot + rain |
| **Episodic / Sequential** | Does the current decision **affect future** decisions? | Episodic: "is there a cat in this image?", expert-advice Q&A. Sequential: Pac-Man, investment portfolio bot |
| **Static / Semi-dynamic / Dynamic** | Can the environment **change while the agent is thinking**? | Static: puzzle, Rubik's cube. Semi-dynamic: **chess with a clock** (world static, *score* changes with time). Dynamic: driving in rain, traffic signals |
| **Discrete / Continuous** | Finitely many distinct percepts and actions? | Discrete: chess. Continuous: taxi driving |
| **Single / Multi agent** | Are there other agents that sense and act? Multi splits into **cooperative**, **competitive**, **self-interested** | Single: crossword. Multi: chess, driving |

> **"Strategic" environment** — a special case worth one mark: an environment
> that is deterministic **except for the actions of other agents** is called
> **strategic**.

### The one sentence to memorise

> **The real world is: partially observable, stochastic, sequential, dynamic,
> continuous, multi-agent.** (The hardest setting on every axis.)

And: **the environment type largely determines the agent design.**

### Worked classification (slide activity)

| | **Deep Blue** (chess computer) | **A robot in the real world** |
|---|---|---|
| Observability | Observable | **Partially** observable |
| Determinism | Deterministic | **Stochastic** |
| Episodic? | Sequential | Sequential |
| Static? | **Static / Semi-dynamic** | **Dynamic** |
| Discrete? | Discrete | **Continuous** |
| Agents | Multi-agent | Multi-agent |

> Note Deep Blue is **semi-dynamic** if the chess clock is running — the board
> doesn't change while you think, but your score does. That distinction is
> exactly what the examiner is fishing for.

---

## 6. Agent architectures — five types

Order matters: each one adds a capability the previous one lacked.

### 0. Table-driven agent (the strawman)
```
function TABLE-DRIVEN-AGENT(percept) returns an action
    persistent: percepts, a sequence, initially empty
                table, actions indexed by percept sequences, fully specified
    append percept to the end of percepts
    action <- LOOKUP(percepts, table)
    return action
```
**Four drawbacks (a standard 4-mark answer):** huge table; takes a long time to
build; **no autonomy**; even with learning, takes a long time to learn the entries.

### 1. Simple reflex agent
Condition–action rules on the **current percept only**. `if dirty then Suck`.
No memory. Fails whenever the environment is partially observable.

### 2. Model-based reflex agent
Keeps **internal state** so it can handle partial observability. Needs two models:
- **Transition model** — how the next state depends on current state and action.
- **Sensor model** — how the world state is reflected in the agent's percepts.

```
function MODEL-BASED-REFLEX-AGENT(percept) returns an action
    persistent: state, transition model, sensor model, rules, action
    state  <- UPDATE-STATE(state, action, percept, transition model, sensor model)
    rule   <- RULE-MATCH(state, rules)
    action <- rule.ACTION
    return action
```

### 3. Goal-based agent
Adds **goal information**. Now it can ask "will this action get me closer to what
I want?" — this is where **search and planning** enter. Slower than reflex, but
flexible: change the goal, behaviour changes, no rule rewrite.

### 4. Utility-based agent
Goals are binary (achieved / not). **Utility** is a number. Needed when:
- there are **conflicting goals** (fast vs safe), or
- **no goal is certain** — then maximise **expected utility**.

### 5. Learning agent
Four components — **this is a guaranteed exam question**, learn all four:

| Component | Job |
|---|---|
| **Performance element** | Takes the decision/action based on percepts. *(This is the whole agent from types 1–4.)* |
| **Learning element** | Improves the performance element so the utility function is optimised |
| **Critic** | Provides **feedback** on the actions taken, against a fixed performance standard |
| **Problem generator** | Deliberately suggests **sub-optimal / exploratory** actions so the agent learns from unseen situations |

> **The problem generator is the one people forget.** Its whole job is to make
> the agent do something it wouldn't otherwise do — that is exploration. One
> line: *"without it the agent would only ever exploit what it already knows."*

---

## 7. Risks of AI (short theory answer, from CS#1)

Six named risks. Each needs one sentence.

1. **Lethal autonomous weapons** — UN definition: weapons that **locate, select
   and eliminate human targets without human intervention**. Primary concern is
   **scalability** — no human supervision means a small group can deploy
   arbitrarily many.
2. **Surveillance and persuasion** — mass surveillance at scale; tailoring
   information flows via social media modifies political behaviour.
3. **Biased decision making** — parole and loan decisions biased by race, gender
   or other protected categories. Often **the data itself reflects existing
   societal bias**.
4. **Impact on employment** — AI does some tasks humans would, but also makes
   humans more productive. Net effect: increases wealth but **shifts wealth from
   labour to capital**, worsening inequality.
5. **Safety-critical applications** — driving, city water supplies. AI needs
   technical and ethical standards comparable to other engineering and
   healthcare disciplines.
6. **Cybersecurity** — useful for defence (detecting unusual behaviour), but also
   boosts malware potency and proliferation; RL has been used for automated,
   personalised blackmail and phishing.

---

## 8. You try

**Q1 (PEAS).** Write the full PEAS description for an **automated web-page
crawler that ranks search results**.

**Q2 (PEAS).** Write PEAS for an **agricultural robot that sprays weeds in a
field**.

**Q3 (classify).** Classify **online poker against 5 human players** on all six
environment axes. For each, give the reason in ≤ 6 words.

**Q4 (classify).** Classify a **thermostat** on all six axes. *(It is more
interesting than it looks — think hard about episodic vs sequential.)*

**Q5 (architecture).** For each, name the **minimum** agent type that suffices,
and say why the one below it fails:
- (a) a spam filter that labels each email independently
- (b) a Roomba in a house whose layout it cannot see all at once
- (c) a taxi choosing between a fast risky route and a slow safe one

**Q6 (definitions).** In one line each: how is *rationality* different from
*omniscience*? And what makes an agent *autonomous*?

Send me your answers — "I don't know" is fine and costs nothing.

---

## 9. Answers

<details>
<summary>Open only after attempting</summary>

**Q1 — Search-engine crawler/ranker**

| | |
|---|---|
| **P** | Relevance of top results, coverage/freshness of the index, query latency, crawl bandwidth cost |
| **E** | The web (pages, links, servers), users issuing queries, other crawlers, robots.txt policies |
| **A** | Issue HTTP fetches, follow/skip links, write to index, return a ranked result page |
| **S** | HTTP responses (page HTML, headers, status codes), user clicks and dwell time, query strings |

Note user clicks are a **sensor** — that is how it perceives whether it did well.

**Q2 — Weed-spraying agricultural robot**

| | |
|---|---|
| **P** | % weeds killed, % crop damaged, herbicide used, area covered per hour, battery/fuel |
| **E** | Field, crop plants, weeds, soil, weather, obstacles, humans, other robots |
| **A** | Wheels/motors for movement, steering, spray nozzle, nozzle arm positioning |
| **S** | Camera, GPS, soil-moisture sensor, tank-level sensor, wheel odometry, bump sensors |

**Q3 — Online poker vs 5 humans**

| Axis | Answer | Reason |
|---|---|---|
| Observability | **Partially observable** | Cannot see opponents' cards |
| Determinism | **Stochastic** | Card deal is random |
| Episodic? | **Sequential** | Chip stack and read on opponents carry over |
| Static? | **Semi-dynamic** (dynamic if timed) | Table waits, but timers penalise you |
| Discrete? | **Discrete** | Finite cards, finite bet sizes |
| Agents | **Multi-agent, competitive** | Five opponents, opposed goals |

**Q4 — Thermostat**

| Axis | Answer | Reason |
|---|---|---|
| Observability | **Partially observable** | Reads one temperature, not the whole house |
| Determinism | **Stochastic** | Weather, doors opening, occupancy |
| Episodic? | **Sequential** | Heating now changes the temperature later |
| Static? | **Dynamic** | Room temperature drifts while it decides |
| Discrete? | **Continuous** | Temperature is a real number |
| Agents | **Single agent** | Nothing else senses and acts |

The trap is *episodic*: a thermostat looks like it makes one isolated decision
per reading, but its own action changes the next reading — that is the definition
of **sequential**.

**Q5 — Minimum agent type**
- (a) **Simple reflex agent.** Each email is judged on the current percept alone;
  nothing carries over. No memory needed.
- (b) **Model-based reflex agent.** A simple reflex agent fails because the house
  is **partially observable** — the Roomba must maintain internal state (a map,
  where it has already been) to avoid re-cleaning and missing rooms.
- (c) **Utility-based agent.** A goal-based agent fails because both routes
  **achieve the goal** — "reach the destination" is satisfied either way. You
  need a number to trade off speed against safety, i.e. a utility function.

**Q6 — Definitions**
- **Rationality** = doing what maximises **expected** performance given the
  percepts so far and built-in knowledge. **Omniscience** = knowing the **actual**
  outcome of every action in advance. A rational agent can still get an unlucky
  outcome and remain rational; omniscience is impossible in practice.
- An agent is **autonomous** if its behaviour is determined by **its own
  experience** — it learns and adapts, rather than relying solely on the
  designer's built-in knowledge.

</details>

---

## 10. Two-minute recall card

- Four definitions: think/act × humanly/rationally. This course = **acting rationally**.
- Turing Test skills: NLP, KR, Automated Reasoning, ML (+ Vision, Robotics = Total).
- `f : P* → A` · `agent = architecture + program`.
- **PEAS** = Performance, Environment, Actuators, Sensors. Sensors pull in, actuators push out.
- Six environment axes: observable / deterministic / episodic / static / discrete / single-agent.
- Real world = partially observable, stochastic, sequential, dynamic, continuous, multi-agent.
- Semi-dynamic = world static but **score** changes with time (chess clock).
- Strategic = deterministic except for other agents' actions.
- Five agent types: reflex → model-based → goal-based → utility-based → learning.
- Learning agent's four parts: **Performance element, Learning element, Critic, Problem generator**.
- Table-driven drawbacks: huge table, slow to build, **no autonomy**, slow to learn.
