# ACI — Theory Revision: Modules 7 & 8 (Ch 12, 13, 14)

**No arithmetic in this file.** Definitions, comparison tables and answer
templates only. The numericals for these chapters are in
`ACI-EC3-PostMidsem-Practice` P15–P21.

> ### Why these chapters, on exam morning
> **Ch 12, 13 and 14 are the newest content in your syllabus.** The Apr 2025
> endsem predates CS#14–16 entirely, so they have **never been examined at
> endsem** — which makes them *more* likely to appear, not less.
>
> And across **all four** of your session's Jun-2026 midsem sets, **every single
> Q1 was an ethics / critique question**. This examiner writes them by habit.
>
> These are also the cheapest marks on the paper: no trellis, no CPT, no
> algebra. You write words and you get marks.

---

# PART 0 · How to answer THIS examiner

Read the pattern off your own Jun-2026 papers. It is very consistent.

| What they do | What you must do |
|---|---|
| Wrap everything in a **real-world scenario** (hiring bot, flood system, campus AI) | **Never answer in the abstract.** Name the scenario's own entities in your answer. |
| Impose **word limits** — *"under 70 words"*, *"under 30 words"* | Respect them. Over-writing is penalised, not rewarded. |
| Print *"Vague answers will not be awarded marks"* | Give **named concepts** and **numbers**, not opinions. |
| Award marks in **0.5 increments** across sub-points | **Use bullets or a table**, never a paragraph. One bullet ≈ one 0.5. |
| Ask you to **"critique"** or **"analyse"** | Give **both sides**, then commit to a verdict in one line. |

### The universal template for a 3-mark scenario question

```
 1. NAME the concept(s) being tested.               (~0.5M)
 2. DEFINE each in one line.                        (~0.5M)
 3. APPLY it to the scenario's own nouns.           (~1M)   <- most marks here
 4. Give 2 RISKS / LIMITATIONS, named.              (~1M)
 5. One-line VERDICT.                               (~0.5M)
```

**Step 3 is where the marks are and where people lose them.** If the question is
about a hiring bot, your answer must contain the words *candidate*, *CV*,
*interview*, *hiring*. A generic paragraph about bias earns roughly half.

### A safe two-sentence closer for any ethics question

> *"The system is therefore not unsafe because it is inaccurate, but because it
> is inaccurate in ways nobody can detect or correct. Adding [FAT / a
> corrigibility layer / human escalation] addresses that directly."*

---

# PART 1 · Ch 14 — Responsible AI **(most likely to appear)**

## 1.1 The Three Layers of AI Safety — *learn this cold*

This is the most examinable slide in the deck. It was the answer to the EC3
makeup Q3B.

| # | Layer | The one-line request | Meaning | Example |
|---|---|---|---|---|
| **1** | **Alignment** | *"Do what I mean given this environment."* | Works in **intended** use-cases | **bias and fairness** |
| **2** | **Robustness** | *"Keep doing what I mean in an unforeseen environment."* | Safe in **unintended** use-cases | **ethics in decisions, adversarial attacks** |
| **3** | **Corrigibility** | *"Enable me to detect and correct your mistakes."* | Imperfect tech can be **detected and improved** | **white box models** |

**Memory hook — three tenses:**

```
 ALIGNMENT      did we build the RIGHT thing?      -> design time
 ROBUSTNESS     does it hold up OUT THERE?         -> deployment time
 CORRIGIBILITY  can we FIX it once we notice?      -> after the fact
```

They are **cumulative**. Alignment without robustness fails the first time
reality differs from the lab. Robustness without corrigibility means that when
it does fail, you can neither detect nor repair it.

> **How to spot that this is the answer.** If the question says *"adapt to new
> environments"* → **Robustness**. *"without compromising safety / values"* →
> **Alignment**. *"detect and correct / oversight"* → **Corrigibility**. The
> EC3 makeup question used exactly those phrases.

## 1.2 FAT — the three key challenges

| Challenge | The problem |
|---|---|
| **Fairness** | **Whose values decide?** Different cultures answer the trolley problem differently (*moralmachine.net*) |
| **Accountability** | **Who or what is responsible** when it goes wrong? |
| **Transparency** | *"Almost no idea why Deep Learning works, or doesn't work."* Motivates **XAI** |

**The accountability question, spelled out** — the self-driving car. Name all
four candidates; that *is* the answer:

```
 - the COMPANY   that designed the car
 - the ENGINEER  who designed the ML algorithms
 - the OWNER     who bought the car
 - the DRIVER    who drove it and supplied the training data
```

> **There is deliberately no answer on the slide.** The examinable observation:
> **AI breaks the normal chain of responsibility.** The decision is made by a
> system whose behaviour nobody fully specified, using data a fourth party
> supplied.

## 1.3 Bias — and the proxy problem

**Bias** = supporting or opposing a person or thing in an unfair way.

The trap, and the thing that earns the mark: **removing the sensitive attribute
does not remove the bias.**

```
 Delete "gender" from the CV screener   ->   the model finds PROXIES instead:
     women's college  ·  career gap  ·  certain sports/clubs  ·  name
     postcode  ·  part-time history
 The model reconstructs the protected attribute from correlated features.
```

So the answer to *"can't we just fix it?"* is **"not so easy"** — you must audit
**outcomes**, not just **inputs**.

## 1.4 Why fair AI is hard — quick list

- Historical data encodes **past** discrimination; the model learns it as signal
- **Fairness has no single definition** — equal rates, equal errors and equal
  treatment are mathematically **incompatible**
- Proxy variables (above)
- Feedback loops — biased predictions create the data for the next model
- Whose values? Fairness is **culturally contested**, not technical

## 1.5 Explainability — a priori vs a posteriori

| | Approach | Meaning |
|---|---|---|
| **A priori** | **Use explainable models** | Choose an interpretable model from the start — decision tree, rules, linear model. Explainability is built in. |
| **A posteriori** | **Explain black-box models** | Keep the accurate black box, add explanation afterwards — LIME, SHAP, saliency maps, surrogate models. |

**The trade-off to state:** *a priori* costs accuracy but gives trustworthy
explanation; *a posteriori* keeps accuracy but the explanation is an
**approximation of** the model, not the model itself.

## 1.6 Ethics by design vs pro-ethical design

| | Meaning |
|---|---|
| **Ethics by design** | Ethical constraints **built into** the system — it *prevents* the unethical action |
| **Pro-ethical design** | The system **makes ethical choices easier and visible**, but leaves the human free to choose |

*Ethics by design decides for you; pro-ethical design helps you decide.*

## 1.7 The broader-perspective points

| Topic | The examinable line |
|---|---|
| **Who owns AI?** | Compute, data and talent concentrate in a few firms — power, not just profit |
| **Myth of democratization** | Open models still need data and compute most people cannot access |
| **Privacy & ownership** | Who owns the training data, the model, and the outputs? |
| **Climate** | Training large models has a large **carbon footprint** |
| **Singularity** (Hinton) | Debate over AI exceeding human capability; cited as a governance concern |

## 1.8 High-risk applications

Deepfakes and media generation · hiring · credit scoring · healthcare
diagnosis · criminal justice / policing · autonomous weapons · **AI proctoring**
· mental-health chatbots.

> **Standard exam pattern:** name the domain, name the harm, name the
> countermeasure. E.g. *proctoring → wrongly flags students with disabilities,
> anxiety or poor lighting → require human review before any penalty.*

---

# PART 2 · Ch 12 — Non-cooperative Game Theory (theory only)

## 2.1 The five elements of a game

Any answer beginning *"a game consists of…"* must list exactly these five.

| # | Element | Definition |
|---|---|---|
| 1 | **Players** | The decision makers |
| 2 | **Actions** | Possible moves available to each player |
| 3 | **Strategy** | A **complete plan** saying what to do in **every** situation |
| 4 | **Payoff (Utility)** | The reward obtained when the game ends |
| 5 | **Information** | What a player knows before deciding — complete / partial / imperfect |

> **⚠ Action ≠ Strategy** — markers look for this.
> An **action** is *"I play Left, once."*
> A **strategy** is *"if he goes Left I go Right; if he goes Right I go Left."*
> A strategy is the whole rulebook; an action is one line of it.

## 2.2 Four types of games

| Type | Rule | Examples |
|---|---|---|
| **Zero-sum** | One's gain **equals** another's loss | Chess, Tic-Tac-Toe |
| **Non-zero-sum** | Both may gain or both may lose | Trade deals, climate agreements |
| **Cooperative** | Players **communicate**, binding agreements | Multi-robot coordination |
| **Non-cooperative** | Players act **independently** | Chess, Poker, auctions |

> **Classify with TWO labels.** *"Which category is Poker?"* →
> **Non-cooperative, imperfect information.** Cooperation and information are
> separate axes. Chess is zero-sum **and** non-cooperative — they are not
> synonyms.

## 2.3 Four ways to represent a game

| # | Representation | Use when | Shows |
|---|---|---|---|
| 1 | **Payoff matrix** (normal form) | **Simultaneous** moves | Payoff for every action combination |
| 2 | **Game tree** | **Sequential** moves | Every move from start to end |
| 3 | **Extensive form** | Sequential **+ uncertainty** | Decision nodes, **chance nodes**, **information sets** |
| 4 | **Finite State Machine** | **Repeated** games | Memory-based strategies, compactly |

*Extensive form adds **information sets** — a dotted line grouping nodes a player
cannot tell apart.*

## 2.4 Pure vs mixed, and the saddle-point test

```
 PURE strategy    always play the same action
 MIXED strategy   randomise over actions with fixed probabilities

 CHECK FIRST:  maximin = minimax  ->  SADDLE POINT exists -> PURE solution, STOP
               maximin < minimax  ->  no saddle point     -> go MIXED
```

**Why mix at all?** A predictable agent is exploitable. Randomising makes the
opponent **indifferent**, removing their ability to counter you.

## 2.5 Repeated games — the five strategies *(very examinable)*

| Strategy | First move | Reaction to defection | Forgiving? | Suits |
|---|---|---|---|---|
| **Hawk** | Defect | Always defect | No | Highly competitive |
| **Dove** | Cooperate | Keeps cooperating | Yes | Cooperative systems |
| **Grim** | Cooperate | **Defect forever** | **No** | Stable environments |
| **Tit-for-Tat** | Cooperate | **Defect once**, then mirror | **Yes** | Most real systems |
| **Tat-for-Tit** | **Defect** | Mimics opponent | Limited | Defensive scenarios |

**Tit-for-Tat's four properties — memorise the four words:**

| Property | Meaning |
|---|---|
| **Nice** | Never defects first |
| **Forgiving** | Returns to cooperation as soon as they do |
| **Retaliatory** | Punishes betrayal immediately |
| **Clear** | Simple enough that opponents learn to cooperate with it |

**Grim's weakness, in one line:** *extremely unforgiving — one accidental defection
destroys cooperation permanently, so it is unsuitable for **noisy** environments
where signals get garbled.* That contrast is the standard 2-mark question.

## 2.6 Sequential games, backward induction, SPNE

```
 BACKWARD INDUCTION   solve from the LEAVES back to the root; at each node the
                      player to move picks the branch maximising THEIR OWN payoff
 SPNE                 a strategy profile that is a Nash equilibrium in EVERY subgame
```

**Non-credible threat — the concept that gets examined.** *"If you enter, I will
fight"* can be a Nash equilibrium of the whole game, but if fighting actually
hurts the threatener once the moment arrives, they wouldn't do it. **SPNE
eliminates equilibria supported by threats a rational player would not carry
out.**

> A **strategy** must specify an action at **every** node — including nodes never
> reached on the equilibrium path. That is why the SPNE is written as
> *"Enter; Accommodate if entry occurs"*, not just *"Enter"*.

## 2.7 Imperfect information, and assistance games

- **Imperfect information** — players cannot observe everything. **Poker**:
  hidden cards, bluffing, belief over opponents' hands, information sets.
- **Assistance games (the Paperclip Game)** — the AI is **uncertain about the
  human's true objective** and must learn it from behaviour. Uncertainty about
  the goal is what makes the agent **deferential and correctable** — it links
  straight back to **corrigibility** in Ch 14.

---

# PART 3 · Ch 13 — Cooperative Game Theory (theory only)

## 3.1 Cooperative vs non-cooperative

> **Non-cooperative:** the unit of analysis is the **individual**.
> **Cooperative:** the unit of analysis is the **coalition**, and agreements are
> **binding**. The questions become *which coalitions form* and *how do they
> split the value*.

## 3.2 Building blocks

| Term | Meaning |
|---|---|
| **Coalition** | Any subset of players acting together |
| **Grand coalition** | All players together |
| **Characteristic function v(C)** | The value coalition C can guarantee **on its own** |
| **Superadditivity** | `v(C ∪ D) ≥ v(C) + v(D)` for disjoint C, D — merging never hurts, so the grand coalition is worth forming |
| **Imputation** | A payoff split that is **efficient** (sums to v(N)) and **individually rational** (each gets ≥ v({i})) |

## 3.3 The Core vs the Shapley value — *know the difference*

| | **The Core** | **The Shapley value** |
|---|---|---|
| Question it answers | **Is it STABLE?** | **Is it FAIR?** |
| Definition | `x(C) ≥ v(C)` for **every** coalition C | Average marginal contribution over all orderings |
| Is it unique? | It is a **set** — may be large | **Unique** |
| Can it be empty? | **Yes** | **Never** — always exists |

> **They can disagree, and questions exploit that.** A Shapley allocation can sit
> **outside** the Core. If asked for both, answer them **separately** and state
> whether they agree.
>
> **Two traps:** violations hide in the **pairs**, not the singletons. And in a
> **cost** game the inequality **flips** to `x(C) ≤ v(C)`.

**Shapley's four axioms — learn the four names:**

| Axiom | Meaning |
|---|---|
| **Efficiency** | The payoffs sum exactly to v(N) |
| **Symmetry** | Two players who contribute identically to every coalition get the same |
| **Dummy / Null player** | A player adding nothing to any coalition gets zero |
| **Additivity** | For two combined games, the value is the sum of the separate values |

## 3.4 Mechanism design — three pillars, three properties

Core challenge: **information asymmetry** — agents hold **private values** they
may **lie about**.

| Property | Definition |
|---|---|
| **Strategy-Proof** | Every agent has a **dominant strategy** — best regardless of what others do |
| **Truth-Revealing** (incentive-compatible) | Strategy-proof **and** that dominant strategy is to **report the truth** |
| **Revelation Principle** | **Any** mechanism can be transformed into an equivalent **truth-revealing** one |

> **⚠ Strategy-proof ≠ truth-revealing.** Strategy-proof = *"you have a dominant
> strategy."* Truth-revealing = *"that dominant strategy is honesty."*
> Truth-revealing is the **stricter** property. Questions ask you to distinguish
> them.

## 3.5 The Contract Net Protocol — four phases

```
 1. RECOGNISE   the manager identifies a task it cannot do alone
 2. ANNOUNCE    it broadcasts the task specification to potential contractors
 3. BID         capable agents evaluate and submit bids
 4. AWARD       the manager selects the best bid and awards the contract
```

Used for **distributed task allocation** in multi-agent systems.

## 3.6 Auctions

| Auction | Rule | Truth-revealing? |
|---|---|---|
| **English (ascending)** | Price rises by increment d while bidders remain | Effectively **yes** |
| **First-price sealed-bid** | Highest bidder wins, **pays their own bid** | **NO** |
| **Vickrey (second-price sealed-bid)** | Highest bidder wins, **pays the SECOND-highest bid** | **YES** |

**Why Vickrey is truthful — the argument to write:**

> Your bid decides **whether** you win; the **second-highest** bid decides **what
> you pay**. Since your own bid never affects your price, bidding above your
> value only wins auctions where the price exceeds it (a loss), and bidding below
> it only loses auctions you'd have won profitably. So truth-telling is at least
> as good as anything else, **whatever the others do** — that is *dominant*.

**Flaws in the English auction:** high **communication overhead** over many
rounds · **discourages entry** when one bidder is known to be dominant · open
multi-round bidding is **vulnerable to collusion**.

## 3.7 Bargaining

- **Nash bargaining solution** — maximise the **Nash product**
  `(u₁ − d₁)(u₂ − d₂)`, where `d` is the **disagreement point**.
- With **linear** utilities this reduces to: **split the SURPLUS equally**, not
  the total. The disagreement point is kept first.
- **Rubinstein alternating offers** — the game-theoretic version; players take
  turns offering, and **patience (the discount factor) determines bargaining
  power**.

## 3.8 Voting

| Protocol | Rule | Flaw |
|---|---|---|
| **Plurality** | Most first-choice votes wins | **Spoiler effect** — ignores everything below first place |
| **Borda count** | Points `m−1 … 1, 0`; highest total wins | Sensitive to irrelevant alternatives |
| **Instant-runoff (IRV)** | Drop the lowest, redistribute, repeat until majority | Can eliminate a broadly-liked compromise early |
| **Condorcet** | Must beat **every** rival head-to-head | **May not exist** |

**Condorcet paradox:** majority preference can **cycle** — A beats B, B beats C,
C beats A — so no Condorcet winner exists.

**The two impossibility theorems:**

| | Statement |
|---|---|
| **Arrow** | With **3+ alternatives**, no ranked-voting system can produce a community **ranking** while satisfying **Non-Dictatorship**, **Pareto Efficiency** and **Independence of Irrelevant Alternatives** |
| **Gibbard–Satterthwaite** | The only **strategy-proof** single-winner rule over 3+ alternatives is a **dictatorship** — every other rule can be manipulated by tactical voting |

*Arrow is about producing a fair **ranking**. Gibbard–Satterthwaite is about
resisting **manipulation**. Different targets, same conclusion: no perfect rule.*

---

# PART 4 · Self-test

Attempt before opening. These are the shapes most likely to be asked.

**T1.** A hospital deploys an AI triage system. It works well in the trial
hospital but misclassifies patients at a rural clinic with different equipment,
and nobody notices for six months. Diagnose the failure using the **Three Layers
of AI Safety**.

<details><summary><b>&#9989; Answer — T1</b></summary>

- **Alignment — partially satisfied.** In the trial hospital it did what was
  intended, so the objective and training data matched the intended use-case.
- **Robustness — FAILED.** The rural clinic is an **unforeseen environment**
  (different equipment, different patient distribution). Robustness is precisely
  *"keep doing what I mean in an unforeseen environment"*, and it did not.
- **Corrigibility — FAILED, and this is the worse failure.** Nobody detected the
  problem for six months. Corrigibility is *"enable me to detect and correct your
  mistakes"* — there was no monitoring, no outcome audit, no white-box view.

**Verdict:** the system was aligned but neither robust nor corrigible. Fix:
distribution-shift monitoring and per-site outcome audits (robustness), plus an
interpretable model or explanation layer so clinicians can flag bad calls
(corrigibility).

*Note the structure — three named layers, each with a verdict and a reason,
then one fix line. That maps directly onto 0.5-mark increments.*
</details>

**T2.** Distinguish **strategy-proof** from **truth-revealing**, with an example
of each.

<details><summary><b>&#9989; Answer — T2</b></summary>

- **Strategy-proof**: every agent has a **dominant strategy** — one that is best
  *regardless of what everyone else does*. They never need to model rivals.
- **Truth-revealing**: strategy-proof **and** that dominant strategy happens to
  be **reporting your true private value**. It is the **stricter** property.

**Example — Vickrey auction:** strategy-proof *and* truth-revealing. Your bid
decides only whether you win, never what you pay, so honest bidding is dominant.

**Example — first-price sealed-bid:** **neither**. Bidding your true value gives
zero surplus, so you must shade — and how much to shade depends on guessing
others' bids, so there is no dominant strategy at all.

**Revelation Principle:** any mechanism can be transformed into an equivalent
truth-revealing one — so a designer may as well design for honesty directly.
</details>

**T3.** Why is **Tit-for-Tat** usually more effective than **Grim** in real
multi-agent systems?

<details><summary><b>&#9989; Answer — T3</b></summary>

Both start by cooperating and both punish defection, but they differ in
**forgiveness**:

- **Grim** defects **forever** after a single defection. Effective as a deterrent
  in a clean, stable environment.
- **Tit-for-Tat** defects **once**, then mirrors — so it returns to cooperation
  as soon as the opponent does.

**Real systems are noisy.** Messages get lost, sensors misread, an action looks
like defection when it was an accident. Under Grim, one such error **permanently
destroys** cooperation and both sides lose payoff forever. Tit-for-Tat recovers
after a single round.

Tit-for-Tat is also **Nice** (never defects first), **Retaliatory** (punishes at
once, so it is not exploitable), and **Clear** (simple enough that opponents
learn cooperating with it pays).

**Verdict:** Grim is optimal only in noiseless environments; Tit-for-Tat is
robust to noise, which is why it wins in practice.
</details>

**T4.** A recruitment model has had the *gender* field deleted, yet still
under-selects women. Explain, and say what you would do instead.

<details><summary><b>&#9989; Answer — T4</b></summary>

**Why it still happens — the proxy problem.** Removing the protected attribute
does not remove the information. The model reconstructs gender from correlated
features: **women's college**, **career gaps**, certain sports or clubs,
**name**, part-time work history, even postcode. It learns the same historical
pattern through a side door.

**The deeper cause:** the training labels encode **past hiring decisions**, which
were themselves biased. The model is accurately reproducing a biased history.

**What to do instead:**
1. Audit **outcomes**, not inputs — measure selection and error rates *by group*
2. Test explicitly for proxies (can a classifier predict gender from the
   remaining features? if yes, they are proxies)
3. Choose an explicit **fairness definition** and state it — equal selection
   rate, equal false-negative rate, etc. — noting these are **mathematically
   incompatible**, so the choice is a policy decision, not a technical one
4. **Human review** before any rejection (corrigibility)

**Verdict:** fairness cannot be achieved by deletion; it requires measurement of
outcomes and an explicit, stated definition of what fair means here.
</details>

**T5.** The Shapley value of a 3-player game is (30, 40, 50) but it is **not** in
the Core. Explain how both can be true.

<details><summary><b>&#9989; Answer — T5</b></summary>

They answer **different questions**:

- **Shapley** asks *"what is FAIR?"* — each player's average marginal
  contribution over all orderings. It always exists, is unique, and satisfies
  Efficiency, Symmetry, Dummy and Additivity.
- **The Core** asks *"what is STABLE?"* — the set of allocations where **no
  coalition can do better by walking away**, i.e. `x(C) ≥ v(C)` for every C.

A fair split can still be unstable. If `v({2,3}) = 100` but Shapley pays them
`40 + 50 = 90`, players 2 and 3 can leave, split 100 between themselves and both
do better. `{2,3}` is the **blocking coalition**. Nothing about fairness prevents
this — fairness averages contributions, stability compares against outside
options.

**Two traps:** violations usually hide in the **pairs**, not the singletons or
grand coalition. And in a **cost** game the inequality flips to `x(C) ≤ v(C)`.
</details>

---

## Two-minute recall card

```
THREE LAYERS OF AI SAFETY
  ALIGNMENT       do what I mean, intended env    -> bias & fairness
  ROBUSTNESS      keep doing it, UNFORESEEN env   -> adversarial, ethics
  CORRIGIBILITY   let me detect & correct you     -> white box models

FAT   Fairness (whose values?) · Accountability (who is responsible?)
      Transparency (why did it do that? -> XAI)
ACCOUNTABILITY 4 candidates: company · engineer · owner · driver
BIAS  deleting the attribute leaves PROXIES -> audit OUTCOMES not inputs
EXPLAINABILITY  a priori = use explainable model
                a posteriori = explain the black box (LIME/SHAP)
ETHICS BY DESIGN prevents · PRO-ETHICAL DESIGN makes the ethical choice easy

FIVE ELEMENTS OF A GAME  Players · Actions · Strategy · Payoff · Information
   ACTION = one move.  STRATEGY = a complete plan for every situation.
GAME TYPES  zero-sum / non-zero-sum  ×  cooperative / non-cooperative
   classify with BOTH axes (Poker = non-cooperative, imperfect information)
REPRESENTATIONS  payoff matrix · game tree · extensive form · FSM
SADDLE POINT  maximin = minimax -> pure, STOP.  else -> mixed.
REPEATED  Hawk · Dove · Grim · Tit-for-Tat · Tat-for-Tit
   TfT = Nice, Forgiving, Retaliatory, Clear
   GRIM fails in NOISY environments (never forgives)
SPNE  Nash in EVERY subgame; removes NON-CREDIBLE THREATS
   a strategy specifies an action at EVERY node, even unreached ones

CORE = STABLE  x(C) >= v(C) for EVERY C ; a SET ; may be EMPTY
   cost game -> flips to x(C) <= v(C) ; violations hide in the PAIRS
SHAPLEY = FAIR  average marginal contribution ; UNIQUE ; always exists
   axioms: Efficiency · Symmetry · Dummy · Additivity
MECHANISM  strategy-proof (dominant strategy exists)
           truth-revealing (that dominant strategy is HONESTY) - STRICTER
           revelation principle (any mechanism -> a truthful equivalent)
CONTRACT NET  Recognise -> Announce -> Bid -> Award
AUCTIONS  English (yes) · First-price (NO) · Vickrey 2nd-price (YES)
NASH BARGAIN  max (u1-d1)(u2-d2) ; linear -> split the SURPLUS, not the total
VOTING  Plurality (spoiler) · Borda m-1..0 · IRV · Condorcet (may NOT EXIST)
   ARROW: no ranked rule keeps ND + Pareto + IIA
   GIBBARD-SATTERTHWAITE: only strategy-proof rule is a DICTATORSHIP
```

---

*Sourced from `ch12-game-theory-noncooperative.md`,
`ch13-cooperative-gt-shapley-auctions-voting.md` and
`ch14-responsible-ai-ethics.md`, which were built from
`materials/ACI Post midsem and formula.pdf` CS#14–16. Numericals for these
chapters are in `ACI-EC3-PostMidsem-Practice` P15–P21.*
