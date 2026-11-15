# Ch 13 — Multi-Agent Decision Making II: Cooperative Game Theory
**Slides: CS#15** (post-midsem deck, PDF pages 67–82)

> ### ⚠ This is the most numerical of the two game-theory chapters
> Ch 12 has **one** calculation (the maximin crossing point). Ch 13 has **five
> separate procedures** that can each be set as a numerical: Core stability
> checks, the Shapley value, Vickrey auction payoffs, the Nash bargaining
> product, and Borda / instant-runoff vote counts. If a game-theory numerical
> appears on the paper, it is far more likely to come from **this** chapter.

> Open `explainers/ch13-shapley-auctions-voting.html` first — it walks the
> six taxi permutations one at a time and lets you click through the Condorcet
> cycle, so you see the shapes before you grind the arithmetic.

---

## 1. Cooperative vs non-cooperative — the one-line difference

| Non-cooperative (Ch 12) | Cooperative (Ch 13) |
|---|---|
| Agents compete, **no communication** | Agents can **talk, form groups, and make binding agreements** |
| Question: *what move do I make?* | Question: *who do I team up with, and how do we split the winnings?* |
| Prisoner's Dilemma | Coalition formation |
| Solution concept: Nash equilibrium, SPNE | Solution concepts: **the Core**, **the Shapley value** |

> **The slides' own analogy — memorise it, it explains the whole chapter.**
> Three students working on a mini project. Working **individually**, each scores
> **60**. Working **together**, the project scores **95**.
> **How should the 95 be divided among the three?** That is cooperative game
> theory in one sentence.

**Two things the chapter is trying to achieve, and they are NOT the same:**

- **Stability** — will anybody walk out? → **The Core**
- **Fairness** — does everyone get what they deserve? → **The Shapley Value**

> **⚠ Do not blur these.** The slides say it explicitly: *"The Core only tests
> for stability, not fairness."* A split can be perfectly stable and grossly
> unfair, and it can be perfectly fair and completely unstable. Two different
> questions, two different tools.

---

## 2. The building blocks

| Symbol | Name | Meaning |
|---|---|---|
| `N` | **Player set** | All players: `N = {1, 2, …, n}` |
| `C` | **Coalition** | Any **subset** of players who join forces |
| `N` | **Grand coalition** | The coalition containing **everyone** |
| `v(C)` | **Characteristic function** | The total value that coalition `C` can secure **on its own** |

**Basic rules:**
```
     v(∅)  =  0             an empty group gets nothing
     v(C)  ≥  0             values are generally non-negative
```

**The slides' example.** `N = {A, B, C}`. There are `2³ = 8` possible coalitions
(including the empty one):

| Coalition | Value |
|---|---|
| A | 2 |
| B | 3 |
| C | 1 |
| A, B | 10 |
| A, C | 7 |
| B, C | 8 |
| A, B, C | **15** |

> **Read `v` correctly.** `v({A,B}) = 10` does **not** mean A and B get 5 each.
> It means *"if A and B walk off and work alone as a pair, they can generate 10
> between them."* How they split it is a separate question — that is §4 and §5.

**Coalition Structure (CS)** = a **partition** of the players into **disjoint**
groups. For `N = {1,2,3,4}`, level 1 of the coalition-structure graph holds the
structures with a single coalition, level 2 those with two coalitions, and so on.

---

## 3. Superadditivity

> **Definition.** A game is **superadditive** if merging two disjoint coalitions
> is never worse than staying apart:
>
> ```
>      v(C ∪ D)  ≥  v(C) + v(D)        for all disjoint C, D
> ```

**The consequence that matters:** in a superadditive game, **the grand coalition
always yields the highest total value**. So the interesting question stops being
*"should we team up?"* (yes, obviously) and becomes *"how do we split it?"*

**Check the A/B/C table above is superadditive:**
```
     v(A) + v(B)  = 2 + 3 = 5   ≤  v(A,B)  = 10   ✓
     v(A) + v(C)  = 2 + 1 = 3   ≤  v(A,C)  =  7   ✓
     v(B) + v(C)  = 3 + 1 = 4   ≤  v(B,C)  =  8   ✓
     v(A,B) + v(C) = 10 + 1 = 11 ≤ v(A,B,C) = 15  ✓
     v(A,C) + v(B) =  7 + 3 = 10 ≤ v(A,B,C) = 15  ✓
     v(B,C) + v(A) =  8 + 2 = 10 ≤ v(A,B,C) = 15  ✓
```
Superadditive. ✓ *(If asked to "verify superadditivity", that six-line check
**is** the answer — don't just assert it.)*

---

## 4. Imputations and the Core

### Payoff vector and imputation

A proposed split is a **payoff vector** `x = (x₁, x₂, …, xₙ)`.
It is an **imputation** if it satisfies **two** conditions:

```
   1. EFFICIENCY            Σ xᵢ  =  v(N)          all the money is distributed
   2. INDIVIDUAL RATIONALITY  xᵢ  ≥  v({i})        nobody is paid less than
                                                   they could earn completely alone
```

### The Core

> **The Core** is the set of all imputations where **no sub-coalition has an
> incentive to defect**:
>
> ```
>      x(C)  ≥  v(C)        for EVERY coalition C ⊆ N
>
>      where  x(C) = Σ  xᵢ    (the sum of what the members of C are being paid)
>                  i ∈ C
> ```

If the condition **fails** for some group — i.e. `v(C) > x(C)` — those players
will say: *"Why are we staying in the grand coalition when we could break away
and make more on our own?"*

**Empty core.** If **no** split satisfies every constraint, the core is **empty**
and the grand coalition **cannot form sustainably** — someone will always want to
defect, no matter how you divide the money.

> **⚠ Individual rationality is just the core condition for singleton
> coalitions.** `x({i}) ≥ v({i})`. So in practice: check efficiency, then check
> **every** subset. The singletons are not a separate rule, they are the `|C| = 1`
> case.

### ⚠ The cost-game sign flip — this is a real trap

Everything above assumes `v(C)` is a **value to be shared** (bigger is better).
When `v(C)` is a **cost to be shared** (smaller is better) — like the taxi problem
in §7 — **every inequality flips**:

```
     VALUE game (share profit):     x(C)  ≥  v(C)      "we could earn more alone"
     COST  game (share a bill):     x(C)  ≤  v(C)      "we could pay less alone"
```

**Read the question and decide which one you are in before writing a single
inequality.** Getting this backwards inverts the entire answer.

---

## 5. NUMERICAL — Core stability check (the slides' Problem 1)

> **Scenario.** 3 players. `v(C) = 1` if `|C| ≥ 2`, else `v(C) = 0`.
> **Question.** Is the imputation `x = (1/3, 1/3, 1/3)` in the core?

**Step 1 — check efficiency.**
```
     1/3 + 1/3 + 1/3  =  1  =  v(N)        ✓  OK
```

**Step 2 — test a coalition.** Take `C = {1, 2}`:
```
     x(C)  =  x₁ + x₂  =  1/3 + 1/3  =  2/3
```

**Step 3 — compare against `v(C)`.**
```
     |C| = 2, so  v(C) = 1

          x(C) = 2/3   <   v(C) = 1        ✗  VIOLATED
```

**Result.**
> **Players 1 and 2 can do better alone by forming their own coalition. So
> x = (1/3, 1/3, 1/3) is NOT in the core.**

**And in fact the core of this game is empty.** Here is the one-line proof the
slides only assert — worth writing out, it is the kind of thing a "justify your
answer" question wants:

```
     For the core to be non-empty we would need, for all three pairs:
          x₁ + x₂ ≥ 1 ,   x₁ + x₃ ≥ 1 ,   x₂ + x₃ ≥ 1

     Add all three:      2(x₁ + x₂ + x₃)  ≥  3
                            x₁ + x₂ + x₃  ≥  1.5

     But efficiency demands  x₁ + x₂ + x₃ = v(N) = 1.
     1 ≥ 1.5 is impossible  ->  NO imputation satisfies all the constraints.
                             ->  THE CORE IS EMPTY.
```

> **Recognise this game.** It is the **majority voting game**: any two of the
> three players can seize the whole prize, so any two of them always want to
> ditch the third. There is no stable split. This is the canonical empty-core
> example — if a question asks *"give an example of a game with an empty core"*,
> this is your answer, with those three lines of proof.

### A second core check — the Tech Startup (also from the slides)

```
     v({A}) = 10 ,  v({B}) = 0 ,  v({C}) = 0
     v({A,B}) = 40 ,  v({A,C}) = 30 ,  v({B,C}) = 0
     v({A,B,C}) = 100
```
The Investor (C) dominates the negotiation and proposes `x = (A: 15, B: 5, C: 80)`.

```
     Efficiency:            15 + 5 + 80 = 100 = v(N)          ✓
     Individual rationality: x_A = 15 ≥ v(A) = 10             ✓
                             x_B =  5 ≥ v(B) =  0             ✓
                             x_C = 80 ≥ v(C) =  0             ✓
     Coalition {A, B}:       x(A,B) = 15 + 5 = 20
                             v(A,B) = 40
                                 20  <  40                    ✗  VIOLATED
```

> **Not in the core.** A and B are being offered 20 between them when they can
> make **40** by walking out and building the product without the investor. They
> will veto the proposal and defect. The Investor's 80 is not defensible.

**Note the shape of both examples:** efficiency and individual rationality both
pass, and the split still fails — because it is a **two-player sub-coalition**
that breaks it. **Always check the pairs.** That is where core violations hide.

---

## 6. The Shapley value — fairness by average marginal contribution

> **The core philosophy in one line:** *a player's reward should equal their
> **average marginal contribution**.*

### Marginal contribution

```
     mcᵢ(C)  =  v(C ∪ {i})  −  v(C)

     "how much extra value does i create by walking into a room
      where the players in C are already sitting?"
```

### The permutation method — *use this in the exam*

```
     1. List all n! orderings (permutations) of the players.
     2. For each ordering, walk the players in one at a time and record
        each player's marginal contribution AT THE MOMENT THEY ARRIVE.
     3. Sum each player's column.
     4. Divide by n!.
```

For `n = 3` that is **6 permutations**. For `n = 4` it is 24 — if a 4-player
question appears, use the weighted formula below instead.

### The closed-form (faster for n ≥ 4)

```
                     |C|! · (n − |C| − 1)!
     φᵢ  =    Σ      ---------------------  ·  [ v(C ∪ {i}) − v(C) ]
           C ⊆ N\{i}          n!
```

For **n = 3** the weights collapse to just three numbers — worth memorising:

| Size of `C` (the group already in the room) | Weight |
|---|---|
| `\|C\| = 0` — i arrives **first** | **1/3** |
| `\|C\| = 1` — i arrives **second** | **1/6** each (two such sets) |
| `\|C\| = 2` — i arrives **last** | **1/3** |

*(Sanity check: `1/3 + 1/6 + 1/6 + 1/3 = 1`.)*

### The Four Axioms of Fairness — *learn all four names*

The Shapley value is the **only** distribution method satisfying all four.

| Axiom | Statement |
|---|---|
| **Efficiency** | The total value `v(N)` is **entirely** distributed among the players |
| **Dummy Player** | If a player adds zero value to every coalition (`mcᵢ(C) = 0` for all `C`), their payoff is **0** |
| **Symmetry** | If two players contribute identically to all coalitions, they receive **identical** payoffs |
| **Additivity** | If players play two separate independent games, their total payout is the **sum** of their payouts from each |

> **Efficiency is your free check.** After computing all `φᵢ`, **add them up**.
> If they don't sum to `v(N)`, you have an arithmetic error. Do this every time —
> it costs five seconds and catches most mistakes.

> **Symmetry is your free shortcut.** If two players are interchangeable in the
> characteristic function, stop computing — they get the same number. That is the
> entire trick behind the 45/45/10 example in §8.

---

## 7. NUMERICAL — Taxi sharing (the slides' Problem 2), all six permutations

> **Scenario.** 3 players share a taxi. Individual costs are `c₁ = 6`, `c₂ = 12`,
> `c₃ = 42`. **The cost of any group is the maximum individual cost in that
> group** (because the taxi drives to the furthest destination anyway).
> **Task.** Find the Shapley value — the fair **cost** share.

### Step 1 — build the characteristic function

`v(C) = max(cᵢ for i in C)`:

```
     v({1})   =  6         v({1,2}) = max(6, 12)     = 12
     v({2})   = 12         v({1,3}) = max(6, 42)     = 42
     v({3})   = 42         v({2,3}) = max(12, 42)    = 42
                           v({1,2,3}) = max(6,12,42) = 42
```

> **Sense-check before computing.** The taxi costs 42 no matter what, because
> player 3 has to get home. So the whole exercise is: *how much of that 42 should
> players 1 and 2 chip in for the part of the ride they share?*

### Step 2 — all 6 permutations

Read each row left to right. When a player arrives, their marginal contribution is
`(cost of the group including them) − (cost of the group before them)`.

| Order | Player 1 | Player 2 | Player 3 |
|---|---|---|---|
| **(1, 2, 3)** | `6 − 0 = 6` | `12 − 6 = 6` | `42 − 12 = 30` |
| **(1, 3, 2)** | `6 − 0 = 6` | `42 − 42 = 0` | `42 − 6 = 36` |
| **(2, 1, 3)** | `12 − 12 = 0` | `12 − 0 = 12` | `42 − 12 = 30` |
| **(2, 3, 1)** | `42 − 42 = 0` | `12 − 0 = 12` | `42 − 12 = 30` |
| **(3, 1, 2)** | `42 − 42 = 0` | `42 − 42 = 0` | `42 − 0 = 42` |
| **(3, 2, 1)** | `42 − 42 = 0` | `42 − 42 = 0` | `42 − 0 = 42` |
| **TOTAL** | **12** | **30** | **210** |

> **The pattern to notice.** As soon as player 3 is already in the taxi, everyone
> arriving after them contributes **0** — the cost is already 42 and cannot go
> higher. That is why players 1 and 2 have so many zeros, and why player 3 carries
> almost the whole bill.

### Step 3 — divide by 3! = 6

```
     φ₁  =  12 / 6  =   2
     φ₂  =  30 / 6  =   5
     φ₃  = 210 / 6  =  35
```

### Answer

> **φ = (2, 5, 35)**

**Efficiency check:** `2 + 5 + 35 = 42 = v(N)` ✓

**Fairness check (the slides' own line): everyone saves money.**

| Player | Alone | Shapley share | Saves |
|---|---|---|---|
| 1 | 6 | **2** | 4 |
| 2 | 12 | **5** | 7 |
| 3 | 42 | **35** | 7 |

**Is it in the core?** This is a **cost** game, so the inequality is `x(C) ≤ v(C)`:

```
     {1}    :  2       ≤  6     ✓        {1,2}  :  2 + 5  =  7  ≤ 12   ✓
     {2}    :  5       ≤ 12     ✓        {1,3}  :  2 + 35 = 37  ≤ 42   ✓
     {3}    : 35       ≤ 42     ✓        {2,3}  :  5 + 35 = 40  ≤ 42   ✓
     {1,2,3}: 42       =  42    ✓
```
**Yes — stable as well as fair.** No subgroup can do better by splitting off.

### Cross-check with the closed-form weights (n = 3)

Verifying `φ₁` a second way, using the 1/3, 1/6, 1/6, 1/3 weights:
```
     φ₁ = 1/3·[v(1) − 0]        + 1/6·[v(1,2) − v(2)]
        + 1/6·[v(1,3) − v(3)]   + 1/3·[v(1,2,3) − v(2,3)]

        = 1/3·(6 − 0) + 1/6·(12 − 12) + 1/6·(42 − 42) + 1/3·(42 − 42)
        = 2 + 0 + 0 + 0
        = 2     ✓  matches the permutation table
```

---

## 8. NUMERICAL — The corporate board, 45 / 45 / 10 (the "missing link")

> **Scenario.** A corporate board vote as a cooperative game.
> Investor 1 holds **45%**, Investor 2 holds **45%**, Investor 3 holds **10%**.
> A resolution passes with a **simple majority (> 50%)**. A passing coalition is
> worth **100 points**; a failing one is worth **0**.
> **Task.** Find the Shapley value.

### Step 1 — build the characteristic function from the shares

```
     Singles:  v({1}) = 0   (45% alone — fails)
               v({2}) = 0   (45% alone — fails)
               v({3}) = 0   (10% alone — fails)

     Pairs:    v({1,2}) = 100    (45 + 45 = 90%  > 50  Pass)
               v({1,3}) = 100    (45 + 10 = 55%  > 50  Pass)
               v({2,3}) = 100    (45 + 10 = 55%  > 50  Pass)

     Trio:     v({1,2,3}) = 100  (100% Pass)
```

### Step 2 — spot the symmetry and stop

> Look at the characteristic function, **not at the share percentages.**
> Every singleton is worth 0. Every pair is worth 100. The trio is worth 100.
> Player 3 appears **nowhere** in that description as different from 1 or 2 —
> the function is completely symmetric in all three players.
>
> By the **Symmetry axiom**, all three receive identical payoffs.
> By the **Efficiency axiom**, they must sum to `v(N) = 100`.

```
     φ₁ = φ₂ = φ₃ = 100 / 3 = 33.33
```

### Answer

> **φ = (33.3, 33.3, 33.3)**

### Step 3 — the long way, if the question demands you show permutations

A player's marginal contribution here is **100 if they turn a losing coalition
into a winning one, and 0 otherwise** (they are the *pivotal* / *swing* voter).

| Order | Pivotal player (the one who crosses 50%) |
|---|---|
| (1, 2, 3) | 1 → 45% (lose); **2** → 90% (win) → **2** is pivotal |
| (1, 3, 2) | 1 → 45% (lose); **3** → 55% (win) → **3** is pivotal |
| (2, 1, 3) | 2 → 45% (lose); **1** → 90% (win) → **1** is pivotal |
| (2, 3, 1) | 2 → 45% (lose); **3** → 55% (win) → **3** is pivotal |
| (3, 1, 2) | 3 → 10% (lose); **1** → 55% (win) → **1** is pivotal |
| (3, 2, 1) | 3 → 10% (lose); **2** → 55% (win) → **2** is pivotal |

Each player is pivotal in exactly **2 of the 6** orderings:
```
     φᵢ  =  (2 × 100) / 6  =  200/6  =  33.33      for every i     ✓
```

### The interpretation — *this is the point of the whole example*

> **Investor 3 owns 10% of the company but has exactly the same power as the
> 45% shareholders.** Player 3 flips a losing coalition into a winning one in
> exactly as many orderings as players 1 and 2 do, so the Shapley value pays all
> three equally.
>
> **Strategic power in cooperative settings comes from CRITICALITY to a group,
> not from individual size.** Investor 3's optimal strategy is to point at this
> arithmetic and demand a full one-third of board control.

**Sanity check on what "criticality" means here.** Investor 1 needs a partner —
either one. Investor 3 needs a partner — either one. Nobody can win alone; every
pair wins. Under those rules the 10% is not a junior stake, it is a **full veto
block**. The percentages are a distraction; the *winning-coalition structure* is
what matters.

---

## 9. Strategy in cooperative games

In non-cooperative theory a strategy is *"what move do I make next?"* In
cooperative theory the question changes shape into **three** strategic questions:

| # | Strategy type | The question the player is asking | Tool |
|---|---|---|---|
| 1 | **Coalition strategy** | *"Which group should I join to maximise our collective value?"* | Coalition structures, superadditivity |
| 2 | **Negotiation strategy** | *"How much of the payout should I demand so I don't walk away?"* | Imputations |
| 3 | **Stability strategy** | *"Is there a side-deal with a subset that gets me more?"* | **The Core** |

**The strategic threat (Tech Startup, §5).** Even though the grand coalition
produces the most total value (100k), Player A may **threaten to stay in the
smaller {A, B} coalition worth 40k** during negotiations, to force B and C to
concede a larger share of the 100k pot. In a superadditive game the grand
coalition is always the efficient outcome — but **the threat of a smaller
coalition is the leverage that determines the split.**

---

## 10. Mechanism design — the three pillars

> **Mechanism design** is the task of **engineering the rules** — effectively
> designing a game — for self-interested agents to participate in, so that a
> **desirable collective outcome** is achieved.

It is game theory run **backwards**: normally you're given a game and you solve
it; here you're given the outcome you want and you design the game that produces it.

Any multi-agent collective decision mechanism has **three structural pillars**:

| Pillar | What it is |
|---|---|
| **Strategy Language** | The specification of the allowable protocol actions / strategies agents can adopt |
| **Center** | The designated agent that **collects** the reports, bids, or strategy actions from all participants |
| **Outcome Rule** | The transparent, deterministic rule the center uses to **resolve final payoffs and allocations** from the submitted strategy profile |

### Three strategic properties of ideal mechanisms

The core challenge is **information asymmetry**: agents hold **private values or
costs** that they may **lie about** to manipulate the outcome.

| Property | Definition |
|---|---|
| **Strategy-Proof** | Every agent has a **dominant strategy** — one that gives them their best payoff **regardless of what everyone else does**. They never need to model their rivals. |
| **Truth-Revealing** (Truthful / **Incentive-Compatible**) | A strategy-proof mechanism where that dominant strategy is to **report their true private preferences** to the center |
| **Revelation Principle** | **Any** mechanism can be mathematically transformed into an equivalent, structurally stable **truth-revealing** mechanism |

> **⚠ Strategy-proof and truth-revealing are not the same thing.**
> Strategy-proof = *"you have a dominant strategy."* Truth-revealing = *"that
> dominant strategy happens to be honesty."* Truth-revealing is the **stricter**
> property — it is strategy-proof **plus** the dominant strategy being truth.
> Questions ask you to distinguish these.

> **Why the Revelation Principle matters for a system designer.** If any outcome
> reachable by a complex, manipulative, strategic game can also be reached by a
> **direct truth-revealing** game, then you never have to design the complicated
> version. You can restrict your search to direct truthful mechanisms and lose
> nothing. That is why it is called a *foundational* theorem.

---

## 11. The Contract Net Protocol — the four phases

A foundational high-level protocol for **collaborative task sharing** among
distributed systems. Inspired by commercial corporate contracting: it structures
the interaction between an agent with a problem (**the Manager**) and potential
problem solvers (**the Contractors**).

| # | Phase | What happens |
|---|---|---|
| 1 | **Problem Recognition** | An agent decides a goal needs cooperation — either it **lacks the capability**, or outsourcing is **faster, cheaper, or more accurate** |
| 2 | **Task Announcement** | The agent becomes **manager** and **broadcasts** an advertisement with the full task specification, deadlines and quality requirements |
| 3 | **Bidding** | Recipient agents parse the spec against their own capabilities and preferences; if willing and able, they submit **formal bids** with their capabilities and terms |
| 4 | **Awarding** | The manager **evaluates the bids**, selects the most suitable contractor, and returns an **award notification**. The winner takes formal responsibility for execution |

### The slides' worked example

> A distributed manufacturing line. A **Central Scheduler** (Manager) must route
> a high-precision metal engraving task **T1**.
>
> - **Task Announcement Processing:** Agent 1 and Agent 2 evaluate the spec.
>   **Agent 1** computes a **low** internal execution cost — it is idle.
>   **Agent 2** computes a **higher** cost — it carries a penalty for interrupting
>   its current queue.
> - **Bid Processing:** The manager collects both submissions and runs a
>   **minimisation function** over the prices. It chooses **Agent 1**.
> - **Award Processing:** Agent 1 receives the notification and becomes the
>   primary contractor, initiating operations.

> **Memory hook for the four phases: Recognise → Announce → Bid → Award.**

---

## 12. Auctions

> An auction is **efficient** if it allocates the resource to the agent with the
> **highest true underlying valuation** — `argmaxᵢ vᵢ`.

Each bidder `i` holds an internal valuation `vᵢ`, of one of two kinds:

| Kind | Meaning | Example |
|---|---|---|
| **Private Value** | Value depends **entirely on the agent's own subjective preferences** | Individual taste in artwork |
| **Common Value** | The item has an **objective but uncertain** market value, the **same for everyone**; agents just hold different estimates from asymmetric information | Oil drilling rights |

### The three auction types

| Auction | Rule | Truth-revealing? |
|---|---|---|
| **English (Ascending-Bid)** | Center sets reserve `b_min` and raises by increment `d` while multiple bidders remain willing. Ends when one bidder is left. | Effectively yes |
| **First-Price Sealed-Bid** | All bids hidden and simultaneous. **Highest bidder wins and pays their own bid.** | **NO** |
| **Second-Price Sealed-Bid (Vickrey)** | All bids hidden and simultaneous. **Highest bidder wins but pays the SECOND-highest bid.** | **YES** |

**English auction — dominant strategy and outcome.**
```
     Dominant strategy: keep bidding while the current price < your true value vᵢ.
     Winner:            the agent with the highest valuation, v_max.
     Final price:       b_o + d
                        where b_o = the highest valuation among the RIVALS,
                              d   = the bid increment.
```

**Flaws in the English auction.** High **communication overhead** across many
rounds · **discourages entry** if one dominant agent is known to have a much
higher valuation · open multi-round bidding is **vulnerable to collusion** —
cooperative cheating among bidders to keep prices artificially low.

> **The 1999 German spectrum auction** (the slides' real-world failure case). Ten
> blocks of cellphone frequencies auctioned simultaneously; rules required any
> counter-bid to be **at least 10% above** the current high bid; only **two**
> operators competed — **Mannesman and T-Mobile**. The 10% rule plus two players
> turned the bid increments themselves into a **signalling channel** for
> collusion. *(This is the named example to cite in any "flaws of open auctions"
> question.)*

**First-price sealed-bid — why it is NOT truth-revealing.** If you bid your true
value and win, you pay exactly your value and your utility is **zero**. So every
agent has an incentive to **shade** their bid below their true valuation
(`bᵢ < vᵢ`) — which requires complex modelling of what the competitors will bid.
Sealed bids fix the collusion and communication problems of the English auction,
but they introduce a strategic-computation problem.

**Vickrey (second-price) — why it IS truth-revealing.** The payment is decoupled
from your own bid. Your bid decides only **whether** you win; the **second-highest
bid** decides what you pay. So manipulating your bid can change *whether* you win
but never *how much you pay*. Bidding `bᵢ = vᵢ` is the **unique dominant
strategy**.

**VCG.** The **Vickrey–Clarke–Groves** mechanism generalises this to complex and
**combinatorial** goods — a truth-revealing, utility-maximising mechanism for
allocating common or combinatorial goods.

---

## 13. The Vickrey strategic payoff matrix — *reproduce this table*

`Bmax` = the highest **competitor** bid. `vᵢ` = your true value. `bᵢ` = your bid.

| Competitor High Bid (Bmax) | Payoff from **Underbidding** (bᵢ < vᵢ) | Payoff from **Truthful Bidding** (bᵢ = vᵢ) | Payoff from **Overbidding** (bᵢ > vᵢ) |
|---|---|---|---|
| `Bmax < bᵢ < vᵢ` | `vᵢ − Bmax` | `vᵢ − Bmax` | `vᵢ − Bmax` |
| `bᵢ < Bmax < vᵢ` | **0 (loses item)** | **`vᵢ − Bmax > 0` (wins)** | `vᵢ − Bmax` |
| `vᵢ < Bmax < bᵢ` | 0 | **0 (safely loses)** | **`vᵢ − Bmax < 0` (financial loss)** |
| `vᵢ < bᵢ < Bmax` | 0 | 0 | 0 |

**How to read it in one sentence per column:**

- **Underbidding** never gains anything, and in row 2 it **costs you the item you
  should have won** — you forfeit a profit of `vᵢ − Bmax`.
- **Truthful bidding** is never worse than either alternative in **any** row.
- **Overbidding** never gains anything, and in row 3 it **wins you an item you
  should have lost** — at a price above your own valuation, so `vᵢ − Bmax < 0`,
  a real financial loss.

> **The conclusion, in the exam's words:** *"Truth-telling weakly dominates: it is
> never worse than lying in any scenario, and strictly better in two of them.
> Therefore bidding one's true valuation is the dominant strategy, and the
> Vickrey auction is incentive-compatible."*

### A concrete Vickrey example to anchor it

Three bidders with true values `A = 100`, `B = 80`, `C = 60`.

```
     TRUTHFUL:   A bids 100. A wins, pays the SECOND-highest bid = 80.
                 A's utility = 100 − 80 = +20.

     OVERBID:    A bids 120. A still wins, still pays 80.
                 Utility = +20. NO GAIN.   (raising your bid cannot lower your price)

     UNDERBID:   A bids 70.  B (80) now wins. A gets nothing.
                 Utility = 0. A LOST the 20 it should have earned.
```

---

## 14. Bargaining

> **Bargaining** handles scenarios where agents must reach an agreement on a
> matter of **common interest** where they have **conflicting preferences** but
> can **mutually benefit** from cooperation.

*Examples:* two companies agreeing a shared technological standard; two agents
dividing a surplus pool of utility.

**The disagreement point `d = (d₁, d₂)`** is the fixed fallback utility each
agent receives if **negotiations collapse**.

### The axiomatic approach — Nash's four axioms

John Nash asked what a "fair and rational" resolution should look like **without
modelling the messy step-by-step psychology of negotiation**. Let `S` be the set
of all feasible joint utility allocations `(u₁, u₂)`.

| Axiom | Statement |
|---|---|
| **Pareto Efficiency** | Agents won't pick an outcome if another feasible outcome makes at least one better off **without hurting the other** |
| **Symmetry** | If `S` is perfectly symmetric and both agents have the same bargaining power, they must receive **equal** utility |
| **Invariance to Affine Transformations** | Rescaling or shifting an agent's utility function linearly (Fahrenheit → Celsius) must **not change the physical outcome** |
| **Independence of Irrelevant Alternatives (IIA)** | Removing some **unchosen** alternatives from the feasible set must **not change the agreement** |

### The Nash Product

> The **unique** outcome satisfying all four axioms is the one that **maximises
> the product of the agents' net gains over their disagreement thresholds**:
>
> ```
>      arg max     ( u₁ − d₁ ) · ( u₂ − d₂ )
>    (u₁,u₂) ∈ S
> ```

> **Strategic insight (state this in any bargaining answer).** The disagreement
> point `dᵢ` **is** an agent's bargaining power. If Agent 1 has a very strong
> backup option (`d₁` is high), Agent 2 must **concede a larger share of the
> surplus** just to keep Agent 1 at the table.

### NUMERICAL — Nash bargaining on a linear frontier

> **Problem.** Two agents split **10 units** of utility. The disagreement point
> is `d = (2, 1)`. The feasible frontier is `u₁ + u₂ = 10`. Find the Nash
> bargaining solution.

**Method 1 — maximise the product directly.**
```
     Let u₁ = x,  so  u₂ = 10 − x.

     f(x) = (x − 2)((10 − x) − 1) = (x − 2)(9 − x)
          = 9x − x² − 18 + 2x
          = −x² + 11x − 18

     f'(x) = −2x + 11 = 0     ->     x = 5.5

     u₁ = 5.5 ,  u₂ = 10 − 5.5 = 4.5
     Nash product = (5.5 − 2)(4.5 − 1) = 3.5 × 3.5 = 12.25
```

**Method 2 — the shortcut, which you should actually use.**
```
     Total surplus above the disagreement point:
          10 − (2 + 1)  =  7

     On a LINEAR frontier the Nash solution SPLITS THE SURPLUS EQUALLY:
          each gets  7 / 2  =  3.5  above their own d

          u₁ = 2 + 3.5 = 5.5
          u₂ = 1 + 3.5 = 4.5        ✓  same answer, no calculus
```

> **The lesson in one line: Nash bargaining splits the SURPLUS equally, not the
> TOTAL.** Agent 1 walks away with more (5.5 vs 4.5) purely because its fallback
> was better — its `d₁ = 2` is bargaining power, converted directly into payoff.

### The game-theoretic approach — Rubinstein's Alternating Offers

The same problem modelled as a **sequential game** instead of an axiom system:

```
     Round 1:  Agent 1 proposes an allocation. Agent 2 can ACCEPT (game ends)
               or REJECT.
     Round 2:  If rejected, Agent 2 counters with a new allocation.
               Agent 1 can ACCEPT or REJECT.
     ... loop ...
```

**The critical caveat: time is money.** Both agents have a **discount factor
`δ ∈ (0, 1)`** reflecting impatience or the shrinking value of the asset. An
allocation of 100 today is worth only `δ × 100` tomorrow.

**Strategic insight.** This creates a **unique subgame perfect equilibrium**, and
the game **concludes instantly in Round 1** — Agent 1 can compute the exact
minimum share Agent 2 would accept later, discounted by `δ`, and offer precisely
that. This awards a **first-mover advantage** to Agent 1.

> **The elegant limit.** As the time between rounds shrinks to zero (`δ → 1`),
> the first-mover advantage **disappears**, and the equilibrium split converges
> **exactly** to the symmetric Nash Bargaining Solution. The two approaches — the
> axiomatic and the game-theoretic — agree in the limit.

---

## 15. Voting procedures

When self-interested agents must select a **single joint outcome** from **3 or
more** alternatives. Each agent holds a private **preference profile** — a strict
ordinal ranking, e.g. `A ≻ B ≻ C`.

### The three protocols and their flaws

| Protocol | Rule | Strategic flaw |
|---|---|---|
| **Plurality** | Each agent votes for their **top choice only**; most votes wins | **Spoiler effect** and **strategic compromise** — voters abandon their favourite for a "lesser evil" to block a hated candidate |
| **Borda Count** | For `m` alternatives: top choice gets `m − 1` points, second gets `m − 2`, … last gets **0**. Sum and take the highest | **Tactical misreporting** — an agent ranks their main rival's favourite **dead last**, even if they genuinely prefer it to other options, purely to depress its score |
| **Plurality with Elimination (Instant-Runoff)** | Voters rank all candidates. If nobody has a **strict majority** of first-place votes, eliminate the candidate with the **fewest**, redistribute their votes to those voters' next choices, repeat until someone clears **50%** | Also manipulable; sensitive to elimination order |

> **⚠ Borda points start at `m − 1`, not `m`.** For 3 candidates the points are
> **2 / 1 / 0**, not 3/2/1. Free marks lost every year on this.
> **Check:** total Borda points awarded = `(number of voters) × (0 + 1 + … + (m−1))`.

### NUMERICAL — one election, three protocols, three different answers

> **9 voters, 3 candidates (A, B, C).**
> - **4 voters:** `A ≻ B ≻ C`
> - **3 voters:** `B ≻ C ≻ A`
> - **2 voters:** `C ≻ B ≻ A`

**Plurality** — count first choices only:
```
     A = 4 ,  B = 3 ,  C = 2      ->   A WINS
```

**Borda** — `m = 3`, so points are **2 / 1 / 0**:
```
     A  =  4×2  +  3×0  +  2×0   =  8  +  0  +  0  =   8
     B  =  4×1  +  3×2  +  2×1   =  4  +  6  +  2  =  12
     C  =  4×0  +  3×1  +  2×2   =  0  +  3  +  4  =   7

     check:  8 + 12 + 7 = 27  =  9 voters × (2+1+0) = 27   ✓

     ->   B WINS
```

**Instant-Runoff** — majority needs 5 of 9:
```
     Round 1:  A = 4 ,  B = 3 ,  C = 2      no majority (nobody has 5)
               Eliminate C (fewest first-place votes).
               C's 2 voters ranked C ≻ B ≻ A, so their votes transfer to B.

     Round 2:  A = 4 ,  B = 3 + 2 = 5       B has 5 of 9 = majority

     ->   B WINS
```

**Condorcet check** — every head-to-head pair:
```
     A vs B :  A preferred by the 4 (A≻B≻C).  B preferred by 3 + 2 = 5.   B beats A  (5–4)
     B vs C :  B preferred by 4 + 3 = 7.       C preferred by 2.           B beats C  (7–2)
     A vs C :  A preferred by 4.               C preferred by 3 + 2 = 5.   C beats A  (5–4)
```
> **B beats every other candidate head-to-head → B is the Condorcet winner.**

**The verdict, and the point of the exercise:**

> **Plurality elects A. Borda, instant-runoff, and the Condorcet criterion all
> elect B.** Plurality picks the candidate that a **majority actively ranks
> last** (5 of 9 voters put A bottom). This is exactly the **spoiler effect** the
> slides warn about, in numbers.

### The Condorcet Paradox

> A candidate is a **Condorcet Winner** if they can defeat **every** other
> alternative in a **head-to-head, pairwise majority vote**.

A Condorcet winner is highly desirable — but one may **not exist**, because
collective preferences can be **cyclical and non-transitive**.

**The slides' own worked paradox.** Three agents, three choices:
```
     Agent 1:   A ≻ B ≻ C
     Agent 2:   B ≻ C ≻ A
     Agent 3:   C ≻ A ≻ B
```
Run all three pairwise elections:
```
     A vs B :  Agent 1 prefers A.  Agent 3 prefers A.  Agent 2 prefers B.   2–1   ->  A ≻ B
     B vs C :  Agent 1 prefers B.  Agent 2 prefers B.  Agent 3 prefers C.   2–1   ->  B ≻ C
     C vs A :  Agent 2 prefers C.  Agent 3 prefers C.  Agent 1 prefers A.   2–1   ->  C ≻ A
```
> **The group preference is `A ≻ B ≻ C ≻ A` — an infinite loop.**
> **No Condorcet winner exists.**

**Consequence:** the outcome becomes **highly sensitive to the order in which
items are voted on** — this is **agenda manipulation**. Whoever controls the order
of the pairwise votes controls the winner. *(Concretely: vote B-vs-C first, then
the winner against A — and A wins. Vote A-vs-B first, then the winner against C —
and C wins. Same preferences, different winner, purely from the agenda.)*

### The two impossibility theorems

Because every voting protocol has flaws, designers went looking for a perfect
rule. **Two theorems prove no perfect rule exists.**

**Arrow's Impossibility Theorem.**
> For any social choice problem with **3 or more alternatives**, **no
> ranked-voting system** can convert individual preferences into a stable
> community-wide **ranking** without violating at least one of:

| Condition | Statement |
|---|---|
| **Non-Dictatorship** | No single agent's preferences can dictate the community's choice regardless of everyone else |
| **Pareto Efficiency (Unanimity)** | If **every** agent prefers A over B, the community ranking must place A over B |
| **Independence of Irrelevant Alternatives (IIA)** | The community's relative ranking of A and B must depend **only** on how individuals rank A vs B. Introducing or removing a third option C must not flip A and B |

**The Gibbard–Satterthwaite Theorem.**
> For any voting protocol selecting a **single winner** from **3 or more**
> alternatives, the protocol can satisfy **strategy-proofness** (no agent ever
> has an incentive to lie about their preferences) **if and only if the system is
> a dictatorship**.

> **⚠ The distinction between the two theorems is a likely exam question.**
> **Arrow** is about producing a complete group **RANKING**. **Gibbard–
> Satterthwaite** is about choosing a **SINGLE WINNER** and about
> **manipulation**. Same pessimistic message, different targets.

**The strategic takeaway (the slides' closing line, and a great final sentence
for an essay answer):**

> With 3 or more choices, agents will **always** have a strategic incentive to
> manipulate the vote by misrepresenting their true preferences. AI system
> engineers **cannot** design a manipulation-free voting system. Instead they
> focus on making the **computational complexity of calculating the optimal lie**
> so high that agents give up trying to cheat.

---

## 16. You try

Attempt all of these before opening §17.

**Q1 — Shapley + Core, the slides' own value table.** `N = {A, B, C}` with
```
     v(A) = 2 ,  v(B) = 3 ,  v(C) = 1
     v(A,B) = 10 ,  v(A,C) = 7 ,  v(B,C) = 8
     v(A,B,C) = 15
```
(a) Verify the game is superadditive.
(b) Compute the Shapley value for all three players using the six permutations.
(c) Check efficiency.
(d) Is the Shapley value in the core? Show every constraint.

**Q2 — Shapley on the Tech Startup.** Using
`v(A)=10, v(B)=0, v(C)=0, v(A,B)=40, v(A,C)=30, v(B,C)=0, v(A,B,C)=100`,
compute the Shapley value for all three players. Check efficiency.
Then say in one sentence why the Investor (C) does **worse** under the Shapley
value than under their own proposed split of `(15, 5, 80)`.

**Q3 — Vickrey.** Four bidders, true values `W = 90`, `X = 75`, `Y = 75`,
`Z = 40`. All bid truthfully in a second-price sealed-bid auction.
(a) Who wins and what do they pay? What is the winner's utility?
(b) Bidder X now overbids at 95 while everyone else stays truthful. Who wins,
    what do they pay, and what is X's utility? Was the deviation worth it?
(c) State in one sentence why (b) is exactly row 3 of the Vickrey payoff matrix.

**Q4 — Nash bargaining.** Two agents split **20 units** of utility on the
frontier `u₁ + u₂ = 20`, with disagreement point `d = (6, 2)`.
(a) Find the Nash bargaining solution.
(b) State the value of the Nash product.
(c) Agent 1 now improves its outside option so that `d = (10, 2)`. Recompute.
    What does the change tell you about bargaining power?

**Q5 — Voting.** 11 voters, 3 candidates:
- **5 voters:** `X ≻ Y ≻ Z`
- **4 voters:** `Y ≻ Z ≻ X`
- **2 voters:** `Z ≻ Y ≻ X`

(a) Plurality winner? (b) Borda winner (show the scores and the total check)?
(c) Instant-runoff winner? (d) Is there a Condorcet winner?

**Q6 — Concept, exam-phrased.** *"Distinguish between the Core and the Shapley
value as solution concepts in cooperative game theory. Illustrate with a
relatable real-world case study where a payoff is fair but not stable."*
(3 marks)

---

## 17. Answers

### Q1

**(a) Superadditivity** — the six-line check is in §3 above. All six hold, so the
game **is superadditive**.

**(b) The six permutations.**

| Order | A | B | C |
|---|---|---|---|
| **A, B, C** | `v(A) = 2` | `v(AB) − v(A) = 10 − 2 = 8` | `v(ABC) − v(AB) = 15 − 10 = 5` |
| **A, C, B** | `v(A) = 2` | `v(ABC) − v(AC) = 15 − 7 = 8` | `v(AC) − v(A) = 7 − 2 = 5` |
| **B, A, C** | `v(AB) − v(B) = 10 − 3 = 7` | `v(B) = 3` | `v(ABC) − v(AB) = 15 − 10 = 5` |
| **B, C, A** | `v(ABC) − v(BC) = 15 − 8 = 7` | `v(B) = 3` | `v(BC) − v(B) = 8 − 3 = 5` |
| **C, A, B** | `v(AC) − v(C) = 7 − 1 = 6` | `v(ABC) − v(AC) = 15 − 7 = 8` | `v(C) = 1` |
| **C, B, A** | `v(ABC) − v(BC) = 15 − 8 = 7` | `v(BC) − v(C) = 8 − 1 = 7` | `v(C) = 1` |
| **TOTAL** | **31** | **37** | **22** |

```
     φ_A = 31/6 = 5.167
     φ_B = 37/6 = 6.167
     φ_C = 22/6 = 3.667
```

**(c) Efficiency check.**
```
     31 + 37 + 22 = 90       90 / 6 = 15 = v(N)     ✓
```
*(Doing it on the totals — before dividing — is faster and catches errors earlier.)*

**(d) Core check.** This is a **value** game, so `x(C) ≥ v(C)`:
```
     {A}   : 5.167                    ≥  2    ✓
     {B}   : 6.167                    ≥  3    ✓
     {C}   : 3.667                    ≥  1    ✓
     {A,B} : 5.167 + 6.167 = 11.333   ≥ 10    ✓
     {A,C} : 5.167 + 3.667 =  8.833   ≥  7    ✓
     {B,C} : 6.167 + 3.667 =  9.833   ≥  8    ✓
     {A,B,C}:                 15.000  =  15   ✓
```
> **Yes — the Shapley value is in the core here.** Fair **and** stable. Note that
> this is a **happy coincidence, not a rule** — §17-Q6 gives the counterexample.

### Q2

| Order | A | B | C |
|---|---|---|---|
| **A, B, C** | `10` | `40 − 10 = 30` | `100 − 40 = 60` |
| **A, C, B** | `10` | `100 − 30 = 70` | `30 − 10 = 20` |
| **B, A, C** | `40 − 0 = 40` | `0` | `100 − 40 = 60` |
| **B, C, A** | `100 − 0 = 100` | `0` | `0 − 0 = 0` |
| **C, A, B** | `30 − 0 = 30` | `100 − 30 = 70` | `0` |
| **C, B, A** | `100 − 0 = 100` | `0 − 0 = 0` | `0` |
| **TOTAL** | **290** | **170** | **140** |

```
     φ_A = 290/6 = 48.33
     φ_B = 170/6 = 28.33
     φ_C = 140/6 = 23.33

     Efficiency:  290 + 170 + 140 = 600 ;  600/6 = 100 = v(N)    ✓
```

> **Why the Investor does worse.** Their self-serving proposal gave them **80**;
> the Shapley value gives them **23.33**. The Investor's *marginal contribution*
> is small — the Developer can already produce 10 alone and 40 with the Marketer,
> so C mostly adds value only by being present at the very end. **Capital is not
> the same as criticality.** C's 80 was pure negotiating position, not merit —
> and §5 already showed it was not even stable.

### Q3

**(a) Truthful bidding.**
```
     Bids: W = 90, X = 75, Y = 75, Z = 40.
     Highest = W (90)  ->  W WINS.
     Pays the SECOND-highest bid = 75.
     W's utility = 90 − 75 = +15.
```

**(b) X overbids at 95.**
```
     Bids: W = 90, X = 95, Y = 75, Z = 40.
     Highest = X (95)  ->  X WINS.
     Pays the SECOND-highest bid = 90  (W's bid).
     X's utility = v_X − price = 75 − 90 = −15.
```
> **The deviation was NOT worth it.** X went from 0 (safely losing) to **−15**,
> a real financial loss. X now owns an item it values at 75 and paid 90 for.

**(c)** This is row 3 of the matrix: `vᵢ < Bmax < bᵢ` — here `75 < 90 < 95`. The
overbid wins an item the agent should have lost, at the second price `Bmax = 90`,
which exceeds the agent's own valuation, so `vᵢ − Bmax < 0`. Truthful bidding
would have given a **safe 0**.

### Q4

**(a)**
```
     Surplus above the disagreement point:  20 − (6 + 2) = 12
     Split equally:                         12 / 2 = 6 each

     u₁ = 6 + 6 = 12
     u₂ = 2 + 6 =  8
```
> **Nash bargaining solution = (12, 8).**

Verification by calculus:
```
     f(x) = (x − 6)(20 − x − 2) = (x − 6)(18 − x) = −x² + 24x − 108
     f'(x) = −2x + 24 = 0   ->   x = 12   ✓
```

**(b)** `Nash product = (12 − 6)(8 − 2) = 6 × 6 = 36`.

**(c)** With `d = (10, 2)`:
```
     Surplus = 20 − (10 + 2) = 8   ->   4 each

     u₁ = 10 + 4 = 14
     u₂ =  2 + 4 =  6
     Nash product = (14 − 10)(6 − 2) = 4 × 4 = 16
```
> **Agent 1's payoff rises from 12 to 14 without anything about the deal itself
> changing** — only its **fallback** improved. Agent 2 is forced to concede
> because Agent 2 needs the deal more. **The disagreement point IS bargaining
> power.** Note also that the total surplus being divided *shrank* (12 → 8), so
> the Nash product fell from 36 to 16 — a stronger outside option makes the
> negotiation less valuable overall, even as it makes your slice bigger.

### Q5

**(a) Plurality.**
```
     X = 5 ,  Y = 4 ,  Z = 2      ->   X WINS
```

**(b) Borda** (`m = 3`, points **2 / 1 / 0**):
```
     X  =  5×2  +  4×0  +  2×0  =  10 +  0 + 0  =  10
     Y  =  5×1  +  4×2  +  2×1  =   5 +  8 + 2  =  15
     Z  =  5×0  +  4×1  +  2×2  =   0 +  4 + 4  =   8

     check:  10 + 15 + 8 = 33  =  11 voters × 3  =  33   ✓

     ->   Y WINS
```

**(c) Instant-runoff** (majority = 6 of 11):
```
     Round 1:  X = 5 ,  Y = 4 ,  Z = 2      no majority
               Eliminate Z. Z's 2 voters ranked Z ≻ Y ≻ X  ->  transfer to Y.
     Round 2:  X = 5 ,  Y = 4 + 2 = 6       Y has 6 of 11 = majority

     ->   Y WINS
```

**(d) Condorcet.**
```
     X vs Y :  X preferred by 5.        Y preferred by 4 + 2 = 6.   Y beats X  (6–5)
     Y vs Z :  Y preferred by 5 + 4 = 9. Z preferred by 2.          Y beats Z  (9–2)
     X vs Z :  X preferred by 5.        Z preferred by 4 + 2 = 6.   Z beats X  (6–5)
```
> **Yes — Y is the Condorcet winner** (beats both X and Z head-to-head).

**The pattern, again:** plurality elects **X**, whom **6 of 11 voters rank last**.
Borda, instant-runoff and Condorcet all agree on **Y**. Same structure as the
worked example in §15 — if you got X for (a) and Y for (b), (c), (d), you have it.

### Q6 (model 3-mark answer)

> **The Core** is a **stability** concept. It is the set of imputations where no
> sub-coalition can do better by breaking away: `x(C) ≥ v(C)` for every coalition
> `C`. It answers *"will anybody walk out?"* It may be **empty**, and it says
> nothing about whether a split is deserved.
>
> **The Shapley value** is a **fairness** concept. It is a single, unique
> allocation giving each player their **average marginal contribution** across
> all `n!` orderings, and it is the only rule satisfying **Efficiency, Dummy
> Player, Symmetry and Additivity**. It answers *"what does each player
> deserve?"* It **always exists** — even when the core is empty.
>
> **Fair but not stable — the case study.** Three regional partners run a joint
> logistics venture. Any **two** of them own enough fleet capacity to serve the
> whole contract alone, so `v(any pair) = v(all three) = 100` and
> `v(any single) = 0`. All three are symmetric, so the Shapley value awards
> **33.3 each** — provably fair by all four axioms. But it is **not stable**: any
> two partners can see that they generate 100 by themselves while receiving only
> 66.6 together, so they will always be tempted to drop the third and split 100
> two ways. **The core of this game is empty**, so *no* division is stable —
> including the fair one. In practice the venture needs an external binding
> contract, because the arithmetic alone cannot hold it together.

*(That is the 45/45/10 board game from §8 with the shares removed — the same
structure, which is why the answer is 33.3 there too. Note the honest extra
point: the fair split is not stable, and there is **no** stable split, which is a
stronger and more interesting statement than "this particular split fails".)*

---

## 18. Two-minute recall card

- **Non-cooperative = compete, no binding deals. Cooperative = talk, form
  coalitions, sign binding agreements.**
- **`v(C)` = what coalition C can secure ON ITS OWN.** `v(∅) = 0`.
- **Superadditive:** `v(C ∪ D) ≥ v(C) + v(D)` → **the grand coalition is best**.
- **Imputation** = **Efficiency** (`Σxᵢ = v(N)`) **+ Individual Rationality**
  (`xᵢ ≥ v({i})`).
- **CORE = STABILITY. SHAPLEY = FAIRNESS.** *"The core only tests stability, not
  fairness."* Never conflate them.
- **Core condition: `x(C) ≥ v(C)` for every C.** **⚠ In a COST game it flips to
  `x(C) ≤ v(C)`.**
- **Check the PAIRS.** Core violations almost always hide in 2-player subsets,
  not in singletons.
- **Empty core example:** 3 players, `v(C) = 1` if `|C| ≥ 2` else 0. `(1/3,1/3,1/3)`
  fails because `x({1,2}) = 2/3 < 1`. Proof: pairs force `Σx ≥ 1.5` but efficiency
  forces `Σx = 1`.
- **Shapley = average marginal contribution.** `mcᵢ(C) = v(C ∪ {i}) − v(C)`.
  **n! orderings, then divide by n!.**
- **n = 3 closed-form weights: 1/3, 1/6, 1/6, 1/3.**
- **Four axioms: Efficiency · Dummy Player · Symmetry · Additivity.**
- **Always add the φᵢ up and check they equal `v(N)`.** Free error check.
- **Taxi: costs 6 / 12 / 42, group cost = max → φ = (2, 5, 35).** Sums to 42 ✓,
  and it IS in the core.
- **Board 45 / 45 / 10 → (33.3, 33.3, 33.3).** Every pair wins → fully symmetric
  → **power comes from CRITICALITY, not size**. Each player is pivotal in 2 of 6.
- **Mechanism design = 3 pillars: Strategy Language · Center · Outcome Rule.**
- **Strategy-proof** = you have a dominant strategy. **Truth-revealing** = that
  dominant strategy is honesty. Truth-revealing is the **stricter** one.
- **Revelation Principle:** any mechanism → an equivalent truth-revealing one.
- **Contract Net, 4 phases: Recognise → Announce → Bid → Award.**
- **English = ascending, pays `b_o + d`.** **First-price sealed = pay your own
  bid, NOT truthful (agents shade).** **Vickrey = second-price, IS truthful.**
- **Why Vickrey works: your bid decides IF you win; the second-highest bid decides
  WHAT YOU PAY.** Truth **weakly dominates** — never worse, strictly better twice.
- **VCG** generalises Vickrey to combinatorial goods.
- Collusion case study: **1999 German spectrum auction, Mannesman vs T-Mobile,
  the 10% counter-bid rule.**
- **Nash Product: maximise `(u₁ − d₁)(u₂ − d₂)`.** On a linear frontier this
  **splits the SURPLUS equally, not the total**.
- **The disagreement point IS bargaining power.**
- **Rubinstein:** alternating offers, discount `δ ∈ (0,1)`, **settles in round 1**,
  first-mover advantage → **vanishes as δ → 1**, converging to the Nash solution.
- **⚠ Borda points are `m−1` down to 0.** For 3 candidates: **2 / 1 / 0**.
  Total check: `voters × (0+1+…+(m−1))`.
- **Condorcet winner** beats everyone head-to-head; **Condorcet paradox** =
  `A ≻ B ≻ C ≻ A`, a cycle → no winner → **agenda manipulation**.
- **Arrow = no perfect group RANKING** (Non-Dictatorship, Pareto, IIA).
  **Gibbard–Satterthwaite = the only strategy-proof SINGLE-WINNER rule is a
  DICTATORSHIP.**
- **Closing line:** you cannot design a manipulation-free vote — you can only
  make the optimal lie **computationally too expensive to find**.
