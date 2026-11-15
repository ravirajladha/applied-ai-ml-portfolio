# ACI (AIMLCZG557) — EC-3 Mock Papers

**Open Book · 40 Marks · 2.5 Hours · Answer all questions**

> ### Why this file exists
> `ACI-EC2-Practice-Sheet`, `ACI-EC2-Supplement-Module3` and
> `ACI-EC3-PostMidsem-Practice` are **lookup documents** — every question there
> is printed with its solution directly underneath, so they cannot test you.
> This file is the missing piece: **two full papers you can sit blind**, plus a
> rapid drill, with every solution held back until you click or turn the page.
>
> Both papers use **fresh numbers** and follow the exact shape of the
> **Apr 2025 EC-3 Regular** paper, question by question and mark by mark.
> Every figure in the solutions was computed independently and cross-checked.

## How to use it tonight

| | |
|---|---|
| **1** | Print **Papers A and B** only. The Solutions part starts on its own page. |
| **2** | Sit **Paper A** against a clock. 150 minutes, notes open, phone away. |
| **3** | Mark it yourself against the Solutions. Write your score per question. |
| **4** | Whatever you lost marks on, drill that pattern in the **Rapid Drill**. |
| **5** | If time remains, sit **Paper B**. If not, at least do its Q3 and Q4. |

**Do not read a solution before attempting the question.** Reading a solved sum
feels like learning and isn't. The exam is speed at executing a procedure, and
you only build that by executing it.

### The paper shape both mocks follow

| Q | Topic | Chapter | Marks |
|---|---|---|---|
| Q1 | Game tree · static evaluation · Minimax / alpha–beta | 6–7 | **9** |
| Q2 | Logic → CNF → DPLL, or FOL → resolution | 8–9 | **7** |
| Q3 | Bayesian network · CPTs · D-separation · query | 10 | **9** |
| Q4 | HMM · transition & emission matrices · Viterbi / Forward | 11 | **8** |
| Q5 | Short answers (2 + 2 + 3) | 2–4, 11–13 | **7** |

Standing instructions on the real paper, worth free marks every time:
*"Assumptions made if any, should be stated clearly at the beginning of your
answer."* · *"Depict them with neat diagrams in addition to tabular
representation."* · *"Vague answers will not be awarded marks."*

---

# PAPER A

## Q1 — Connect Three [3 + 3 + 3 = 9 Marks]

Consider the **Connect Three** game on a **3 × 3** board. Player 1 has Blue
checkers, Player 2 has Green checkers. The objective is to align three of your
checkers horizontally, vertically or diagonally before your opponent does. On
your turn you place one checker into an open slot at the top of the board; it
falls to the lowest unoccupied space in that column. **Blue moves first.**

**Initial State** (row 1 is the bottom row; columns numbered 1–3, left to right):

```
        col1  col2  col3
 row3     .     .     .
 row2     .     .     .
 row1     B     G     .
```

a) Construct the game tree (with a neat diagram) from the given current state
   as the Start Node (0th level) up to **exactly 2 levels** — i.e. one round
   for each player.

b) Calculate the utility of the leaves of the tree with the static evaluation
   function below.

   > **Board value = 5 × (MAX player chance of Win) − 2 × (MIN player chance of Win)**
   >
   > **Player Chance of Win** = the number of three-in-a-row lines this player
   > could still complete *if that player alone were allowed to fill every
   > empty cell with its own checkers*.

c) Apply the **Min-Max** algorithm to the game tree constructed in part (a),
   using the static evaluation values from part (b), and highlight the best
   path chosen by the players. State your tie-breaking rule.

## Q2 — Data-centre fault knowledge base [2 + 2.5 + 2.5 = 7 Marks]

Not all instances of a **Server Outage (S)** in a data centre are caused by a
**Power failure (P)**. Some outages may occur due to a **Network fault (N)** or
a **Cooling failure (C)**. When both a **Disk error (D)** and a **Backup
failure (B)** are detected, the system declares **Data loss (L)**.

A **Latency spike (T)** may also be triggered by a **Routing change (R)**, a
**Traffic surge (G)**, or a **Memory leak (M)**. Additionally, if a **Server
outage (S)** occurs **without** a latency spike (¬T), it must indicate a
**Hardware fault (H)**.

The monitoring log for the current incident further records that **a server
outage has occurred**, that **no power failure was logged**, and that **no
cooling failure was logged**.

a) Use propositional logic (without quantifiers) to efficiently represent the
   knowledge base given above.

b) W.r.t. the knowledge base from the results of part (a), convert it into
   **CNF**.

c) Find a sample complete **BSAT** (Binary Satisfiability) solution for the
   variables using the **DPLL** algorithm, as explained in class. Provide a
   step-by-step approach and **name the rule used at every step**.

## Q3 — Smart warehouse [4 + 3 + 2 = 9 Marks]

Achieving a high **Order Fulfilment (OF)** rate in an automated warehouse
depends on several interrelated operational factors.

- **Robot Uptime (RU)** determines how much of the picking fleet is available,
  and is **positively influenced** by **Preventive Maintenance (PM)** and
  **Battery Health (BH)**.
- **Inventory Accuracy (IA)** determines whether stock records match reality,
  and is **positively influenced** by **Preventive Maintenance (PM)** and
  **Barcode Scanning quality (BS)**.
- **Order Fulfilment (OF)** is directly determined by **Robot Uptime (RU)** and
  **Inventory Accuracy (IA)**.
- The combined status of **Order Fulfilment (OF)** and **Staff Availability
  (SA)** contributes to **Customer Satisfaction (CS)**.

When both robot uptime and inventory accuracy are high, order fulfilment is
highly likely (**95 %**) to be met. If uptime is high but inventory is
inaccurate, fulfilment is still likely (**75 %**). If uptime is low but
inventory is accurate, fulfilment has a moderate (**55 %**) chance. When both
are poor, fulfilment drops to **15 %**.

Historical logs additionally give:

| PM | BH | P(RU = T \| PM, BH) |
|---|---|---|
| T | T | 0.90 |
| T | F | 0.60 |
| F | T | 0.50 |
| F | F | 0.20 |

| PM | BS | P(IA = T \| PM, BS) |
|---|---|---|
| T | T | 0.90 |
| T | F | 0.70 |
| F | T | 0.60 |
| F | F | 0.20 |

**NOTE:** every variable is binary — True / False.

a) Draw the complete Bayes net with **fully filled conditional probability
   tables**. Consider the random variables embedded and highlighted in the
   problem statement as significant events, and **assume all the events
   (conditional or unconditional) are equally likely to occur except those
   which are explicitly specified in the problem statement.**

b) Use the **D-Separation** approach to prove whether each statement is true or
   false. Justify each with the blocking rule you applied.
   1. *"Order Fulfilment (OF) is independent of Preventive Maintenance (PM),
      given that we already know Robot Uptime (RU) and Inventory Accuracy (IA)."*
   2. *"Order Fulfilment (OF) is independent of Battery Health (BH), given that
      we already know Robot Uptime (RU)."*

c) What is the probability that a warehouse with preventive maintenance done,
   good battery health, working barcode scanning, high robot uptime, accurate
   inventory and available staff will achieve **both** high order fulfilment
   **and** high customer satisfaction?

## Q4 — Network link quality [3 + 5 = 8 Marks]

A network operations centre models a link as being in one of three states:
**Good**, **Degraded**, or **Congested**. A link in the **Good** state has a
60 % chance of staying Good, a 30 % chance of moving to Degraded, and a 10 %
chance of becoming Congested. A link in the **Degraded** state has a 10 %
chance of recovering to Good, a 60 % chance of remaining Degraded, and a 30 %
chance of becoming Congested. A link in the **Congested** state has a 70 %
chance of remaining Congested and a 30 % chance of improving to Degraded; it
never recovers to Good in a single step.

The observed condition of the link each minute is reported as either
**"Fast"** or **"Slow"**. Links in the Good state report Fast 80 % of the time;
links in the Degraded state report Fast 40 % of the time; links in the
Congested state report Slow 90 % of the time.

a) Construct the Markov Model by extracting the **transition** and **emission**
   probability matrices from the above pattern. **Depict them with neat
   diagrams in addition to tabular representation.** Assume equal likelihood
   for the initial state.

b) Using the sequence of observed reports **("Slow", "Fast")**, apply the
   **Viterbi** algorithm to determine the most likely sequence of link states
   followed by the link. **Strictly follow the approach as discussed in class
   only** — show the trellis and the backpointers.

## Q5 — Short answers [2 + 2 + 3 = 7 Marks]

*Answer all the following questions. Vague answers will not be awarded marks.*

a) Is it possible that the heuristic designed for an informed search technique
   turns out to be **admissible but not consistent**? Explain with a numerical
   example and a relatable real-world case study.

b) Explain the evaluation process of the **Iterative Deepening Search (IDS)**
   algorithm using an example.

c) Calculate the missing probability values and determine the likelihood that a
   streaming subscriber's monthly plan behaviour follows this specific
   sequence: *(Retain, Retain, Upgrade, Retain)*. Calculate the initial
   probability using the given sequence.

```
                    from U    from R    from D
      to U           0.5       0.2       0.1
      to R           0.3        ?        0.3
      to D            ?        0.3        ?
```

---

# PAPER B

## Q1 — Adversarial search [3 + 4 + 2 = 9 Marks]

A two-player game has been expanded to depth 2. The root is a **MAX** node with
three children, each a **MIN** node with three leaves. The static evaluation
values of the leaves are shown, read strictly **left to right**:

```
                        S0  (MAX)
             ___________|___________
            |           |           |
           S1          S2          S3        (MIN)
          / | \       / | \       / | \
         8  5  6     4  9  3     7  2  10    (leaves)
```

a) Apply the **Min-Max** algorithm. Give the backed-up value of S1, S2, S3 and
   of the root, and state the move MAX will play.

b) Apply **alpha–beta pruning**, traversing the tree **left to right**. Show
   the α and β values at every node as they change, state exactly **which
   leaves are never evaluated**, and give the reason (α-cut or β-cut) for each
   cut-off. How many of the nine leaves did you evaluate?

c) The final backed-up value of the root is the same with and without pruning.
   Explain why, and show with **one** re-ordering of the leaves that the
   *number* of leaves evaluated does depend on move ordering.

## Q2 — First-Order Logic [2 + 2 + 3 = 7 Marks]

a) Convert the following into **FOL** using quantifiers. Define your predicates
   before you use them.
   1. All robots that are charged can operate.
   2. Every technician maintains at least one robot.
   3. Some robots are not charged.
   4. No robot operates without being charged.
   5. Not all technicians maintain every robot.

b) For each pair, state the **most general unifier**, or explain precisely why
   unification fails.
   1. `Maintains(Ravi, x)` and `Maintains(y, Robot7)`
   2. `Maintains(Ravi, x)` and `Maintains(x, Robot7)`
   3. `Status(f(x), y)` and `Status(z, g(z))`
   4. `Status(x)` and `Status(f(x))`

c) Given the knowledge base

   ```
   1.  ∀x ( Robot(x) ∧ Charged(x) → Operates(x) )
   2.  Robot(R7)
   3.  Charged(R7)
   ```

   prove **∃x ( Robot(x) ∧ Operates(x) )** by **resolution refutation**. Show
   the CNF conversion, the negated goal, and every resolvent with its unifier.

## Q3 — Account-security Bayesian network [3 + 3 + 3 = 9 Marks]

An identity-protection service models account compromise as follows. A
**Credential Leak (CL)** can be caused by a **Phishing campaign (Ph)** or by a
**Weak Password (WP)**, which occur independently of one another. A credential
leak may then lead to an **Account Takeover (AT)**, and independently may cause
the monitoring system to raise an **Alert (AR)**.

```
        Ph        WP
          \      /
           v    v
            (CL)
           /     \
          v       v
        (AT)     (AR)
```

| | |
|---|---|
| P(Ph = T) | 0.2 |
| P(WP = T) | 0.4 |

| Ph | WP | P(CL = T \| Ph, WP) |
|---|---|---|
| T | T | 0.95 |
| T | F | 0.70 |
| F | T | 0.50 |
| F | F | 0.05 |

| CL | P(AT = T \| CL) | P(AR = T \| CL) |
|---|---|---|
| T | 0.80 | 0.90 |
| F | 0.05 | 0.10 |

a) Compute **P(CL = T)** by **variable elimination**, eliminating Ph and WP.
   Show the intermediate factor.

b) An account takeover has been detected. Compute **P(Ph = T | AT = T)** by
   **inference by enumeration**. Show the query extraction, the summation over
   hidden variables, and the normalisation.

c) Using **D-separation**, decide with reasons:
   1. Is Ph independent of WP?
   2. Is Ph independent of WP **given CL = T**?
   3. A **likelihood-weighting** run is used to estimate P(Ph | AT = T, AR = T).
      One sample fixes the evidence and draws Ph = T, WP = F, CL = T. Compute
      the weight of that sample and state how the final estimate is formed.

## Q4 — Predictive maintenance HMM [3 + 5 = 8 Marks]

A vibration sensor on a pump reports either **"Normal"** or **"Vibration"**
each hour. The pump itself is either **Healthy** or **Faulty**, and this state
is not directly observable. Maintenance records show that a Healthy pump stays
Healthy 80 % of the time and becomes Faulty 20 % of the time; a Faulty pump
returns to Healthy 30 % of the time and stays Faulty 70 % of the time. A
Healthy pump reports "Normal" 90 % of the time; a Faulty pump reports
"Vibration" 80 % of the time. At the start of a shift, the pump is Healthy with
probability 0.7.

a) Extract the **transition** and **emission** probability matrices and the
   initial distribution. Depict them with **neat diagrams in addition to the
   tabular representation**.

b) The sequence observed over three hours is **("Normal", "Vibration",
   "Vibration")**. Using the **Forward algorithm**, compute **P(O)**, the
   likelihood of that observation sequence. Show the full trellis. Then state
   the **filtered** probability that the pump is Faulty at hour 3, and explain
   in one line why you must not normalise inside the Forward recursion.

## Q5 — Short answers [2 + 2 + 3 = 7 Marks]

*Answer all the following questions. Vague answers will not be awarded marks.*

a) Define **consistency** (the monotonicity condition) of a heuristic and prove
   in two lines that **consistency implies admissibility**. State which
   property A\* graph-search needs in order to be optimal, and why.

b) A **simulated annealing** search is at a state with value 62. It proposes a
   neighbour with value 59. Compute the probability that this move is accepted
   at temperature **T = 15** and at temperature **T = 1**. Comment on what the
   two numbers say about the annealing schedule.

c) Two players play the following zero-sum game; the entries are the **row
   player's** payoff.

   | | C1 | C2 |
   |---|---|---|
   | **R1** | 4 | −2 |
   | **R2** | −1 | 3 |

   Show there is no saddle point, find the optimal **mixed strategy** for both
   players, and give the **value of the game**. Verify your answer on both
   expected-payoff lines.

---

# RAPID NUMERICAL DRILL

Eighteen short numericals, one pattern each, covering the rest of the syllabus.
Each takes 3–8 minutes. Do the ones matching the questions you lost marks on.

**D1 · Uniform Cost Search.** Trace UCS from S to G. Give the expansion order
with the g-value at expansion, the path found, and its cost.

```
   S -> A (2)     A -> C (4)     C -> G (3)
   S -> B (4)     A -> G (9)     B -> C (1)     B -> G (8)
```

**D2 · A\*.** On the same graph with `h(S)=7, h(A)=6, h(B)=4, h(C)=3, h(G)=0`,
trace A\*. Give the expansion order with f-values. Then verify whether h is
**admissible** and whether it is **consistent**, showing the test for each.
Break ties alphabetically.

**D3 · Admissible but not consistent.** For the graph `S→A (1)`, `A→G (4)`,
`S→G (6)` with `h(S)=5, h(A)=1, h(G)=0`: show h is admissible, then find the
edge on which consistency fails and give the numbers.

**D4 · IDS vs BFS node counts.** For branching factor b = 3 with the goal at
depth d = 3, compute the number of nodes generated by IDS and by BFS, and the
percentage overhead of IDS. State the two formulas first.

**D5 · Random-restart hill climbing.** Each restart succeeds with probability
p = 0.15. How many restarts are expected before success? State the formula.

**D6 · Simulated annealing.** Current value 40, proposed neighbour value 37
(minimising is *not* the goal — higher is better). Compute P(accept) at
T = 15 and at T = 1.

**D7 · Genetic algorithm, one generation.** Population `{00011, 00101, 01000,
00010}` decoded as unsigned binary, fitness f(x) = x².
(a) Fitness and roulette-wheel selection probability of each individual, plus
its expected number of copies in a population of 4.
(b) Single-point crossover of `01000` and `00101` **after bit 2** — give both
children with their fitness.
(c) Mutate bit 5 of the first child and give the new fitness.

**D8 · Ant Colony Optimization.** An ant at node A may move to B, C or D.
Pheromone `τ(AB)=2.0, τ(AC)=4.0, τ(AD)=1.0`; distances `d(AB)=4, d(AC)=10,
d(AD)=2`; `α = 1`, `β = 2`, `η = 1/d`.
(a) Compute the transition probability to each node. (b) With evaporation
`ρ = 0.5`, `Q = 100` and a completed tour of length 25 that used edge AD,
update τ(AD).

**D9 · MCTS / UCB1.** A parent node has been visited 100 times. Its children:
X (20 wins / 30 visits), Y (12/15), Z (30/55). With `C = √2`, compute UCB1 for
each and say which child is selected. Explain in one line which term dominates
for Y.

**D10 · TT-entailment.** `KB = (P ∨ Q) ∧ (¬P ∨ R)`. Build the truth table.
How many models satisfy KB? Does `KB ⊨ R`? Give the counter-model if not.

**D11 · Propositional resolution.** `KB = { A → B, B → C, A }`. Prove `C` by
resolution refutation. Show CNF, the negated goal, and every resolvent.

**D12 · Bayes rule / base rate.** A disease affects 0.5 % of a population. A
test has sensitivity 0.98 and specificity 0.95. A patient tests positive.
Compute P(disease | positive) and comment in one line.

**D13 · Markov chain.** `P = [[0.7, 0.3], [0.4, 0.6]]` with rows = "from".
(a) Compute P², and read off the probability of being in state 1 two steps
after starting in state 1. (b) Compute the steady-state distribution.

**D14 · Maximin / saddle point.** Row player's payoffs:

| | X | Y | Z |
|---|---|---|---|
| **A** | 8 | 5 | 6 |
| **B** | 4 | 2 | 3 |
| **C** | 7 | 4 | 9 |

Find maximin and minimax, decide whether a saddle point exists, give the value
and the optimal pure strategies — and show you could have got there faster by
**dominance**.

**D15 · Shapley value and the Core.** Three firms:
`v(∅)=0, v(1)=20, v(2)=30, v(3)=40, v(1,2)=60, v(1,3)=80, v(2,3)=100,
v(1,2,3)=120`.
(a) Compute the Shapley value from all six orderings. (b) Verify efficiency.
(c) Test whether the Shapley allocation lies in the **Core**; if not, name the
blocking coalition.

**D16 · Auctions.** Sealed bids: A 220, B 180, C 250, D 240.
(a) Under a **Vickrey** auction, who wins and what is paid? (b) If C's true
value is 250, what is C's surplus? (c) What changes under a **first-price**
sealed-bid auction, and what incentive does that create?

**D17 · Voting, four ways.** 15 voters: 6 rank `A ≫ C ≫ B`, 5 rank
`B ≫ C ≫ A`, 4 rank `C ≫ B ≫ A`. Find the winner under **plurality**,
**Borda**, **instant-runoff** and **Condorcet**. Comment on what you find.

**D18 · Nash bargaining.** Two firms divide a surplus of 100 with linear
utilities. The disagreement point is d = (30, 10). Give the Nash bargaining
solution and verify it maximises the Nash product against two alternatives.

---

# SOLUTIONS

*Stop here unless you have attempted the question.*

## Paper A — Solutions

<details><summary><b>Show solution — Paper A Q1 (Connect Three, 9 marks)</b></summary>

**Assumption to state first:** columns are explored left to right (1, 2, 3),
and ties at any node are broken by choosing the **leftmost** child. Blue = MAX,
Green = MIN.

**(a) Level 1 — MAX (Blue) drops [1 mark]**

```
 S1 (Blue -> col1)     S2 (Blue -> col2)     S3 (Blue -> col3)
   .  .  .               .  .  .               .  .  .
   B  .  .               .  B  .               .  .  .
   B  G  .               B  G  .               B  G  B
```

**Level 2 — MIN (Green) drops [2 marks]** — nine leaves, three per branch:

```
 S4  (S1,c1)   S5  (S1,c2)   S6  (S1,c3)
   G  .  .       .  .  .       .  .  .
   B  .  .       B  G  .       B  .  .
   B  G  .       B  G  .       B  G  G

 S7  (S2,c1)   S8  (S2,c2)   S9  (S2,c3)
   .  .  .       .  G  .       .  .  .
   G  B  .       .  B  .       .  B  .
   B  G  .       B  G  .       B  G  G

 S10 (S3,c1)   S11 (S3,c2)   S12 (S3,c3)
   .  .  .       .  .  .       .  .  .
   G  .  .       .  G  .       .  .  G
   B  G  B       B  G  B       B  G  B
```

**(b) Static evaluation [3 marks]**

There are **8 lines** on a 3 × 3 board: 3 rows, 3 columns, 2 diagonals. A
player's "chance of win" is the count of those 8 lines that contain **none of
the opponent's** checkers.

```
 node   Blue chances   Green chances   value = 5*B - 2*G
 -----------------------------------------------------------
 S4          3               4          15 -  8 =   7
 S5          3               4          15 -  8 =   7
 S6          4               4          20 -  8 =  12
 S7          4               2          20 -  4 =  16
 S8          5               2          25 -  4 =  21
 S9          4               2          20 -  4 =  16
 S10         4               3          20 -  6 =  14
 S11         3               3          15 -  6 =   9
 S12         4               3          20 -  6 =  14
```

Worked count for **S8** (the highest), as a model for your own working:

```
   .  G  .          lines with NO Green (Blue's chances):
   .  B  .            row2, col1, col3, main-diag, anti-diag      = 5
   B  G  .          lines with NO Blue (Green's chances):
                      row3, col3                                  = 2
   value = 5*5 - 2*2 = 21
```

**(c) Minimax [2 marks] + best path [1 mark]**

```
 S1 (MIN) = min( 7, 7, 12) =  7
 S2 (MIN) = min(16, 21, 16) = 16
 S3 (MIN) = min(14,  9, 14) =  9

 S0 (MAX) = max( 7, 16, 9) = 16
```

```
                      S0 = 16  (MAX)
             _____________|_____________
            |             |             |
          S1 = 7      *S2 = 16*        S3 = 9      (MIN)
          / | \        / | \           / | \
         7  7  12   *16* 21  16      14  9  14
```

**Best path: S0 → S2 → S7.** MAX plays **column 2**. At S2 the MIN value 16
occurs at both S7 and S9; by the stated leftmost tie-break, S7 is chosen.

> **Where the marks are.** The Apr 2025 scheme gave *3 of 9 marks for the
> static evaluation values alone* — the single biggest chunk. If you are short
> of time, get the leaf values right before you draw anything pretty.

</details>

<details><summary><b>Show solution — Paper A Q2 (CNF + DPLL, 7 marks)</b></summary>

**(a) Knowledge base in propositional logic [2 marks]**

```
 R1 :  S → (P ∨ N ∨ C)          an outage implies one of the three causes
 R2 :  (D ∧ B) → L              disk error AND backup failure implies data loss
 R3 :  T → (R ∨ G ∨ M)          a latency spike implies one of its three triggers
 R4 :  (S ∧ ¬T) → H             outage without a latency spike implies hardware fault
 R5 :  S                        observed
 R6 :  ¬P                       observed
 R7 :  ¬C                       observed
```

**(b) Conversion to CNF [2.5 marks]** — *name the rule at each step.*

```
 R1 :  S → (P ∨ N ∨ C)      implication elimination →   ¬S ∨ P ∨ N ∨ C
 R2 :  (D ∧ B) → L          implication elimination →   ¬(D ∧ B) ∨ L
                            De Morgan               →   ¬D ∨ ¬B ∨ L
 R3 :  T → (R ∨ G ∨ M)      implication elimination →   ¬T ∨ R ∨ G ∨ M
 R4 :  (S ∧ ¬T) → H         implication elimination →   ¬(S ∧ ¬T) ∨ H
                            De Morgan               →   ¬S ∨ T ∨ H     (¬¬T = T)
 R5 :  S           R6 :  ¬P            R7 :  ¬C        (already unit clauses)
```

Clause set:

```
 C1 : { ¬S, P, N, C }      C4 : { ¬S, T, H }      C6 : { ¬P }
 C2 : { ¬D, ¬B, L }        C5 : { S }             C7 : { ¬C }
 C3 : { ¬T, R, G, M }
```

**(c) DPLL [2.5 marks]**

```
 STEP 1  UNIT PROPAGATION on C5 = {S}          ->  S = TRUE
         C1 loses ¬S  ->  { P, N, C }
         C4 loses ¬S  ->  { T, H }

 STEP 2  UNIT PROPAGATION on C6 = {¬P}         ->  P = FALSE
         C1 loses P   ->  { N, C }

 STEP 3  UNIT PROPAGATION on C7 = {¬C}         ->  C = FALSE
         C1 loses C   ->  { N }        <- now a UNIT clause

 STEP 4  UNIT PROPAGATION on { N }             ->  N = TRUE      C1 satisfied

 Remaining clauses:  C2 { ¬D, ¬B, L }   C3 { ¬T, R, G, M }   C4 { T, H }

 STEP 5  PURE LITERAL.  D appears only negatively  ->  D = FALSE    C2 satisfied
         (B = FALSE or L = TRUE would do equally well — say so.)

 STEP 6  PURE LITERAL.  R appears only positively  ->  R = TRUE     C3 satisfied

 STEP 7  PURE LITERAL.  H appears only positively  ->  H = TRUE     C4 satisfied

 ALL CLAUSES SATISFIED — no split was ever needed.
```

**Pure symbols in the original set** (state these explicitly, the scheme asks
for it): `P, N, C, D, B, L, R, G, M, H` are each of one sign only; **only T and
S appear in both polarities**, and S is fixed by observation.

**A complete BSAT model:**

```
 S = T   P = F   N = T   C = F   D = F   B = F   L = F
 T = F   R = T   G = F   M = F   H = T
```

Check every clause: C1 ✓ (N), C2 ✓ (¬D), C3 ✓ (¬T), C4 ✓ (H), C5 ✓, C6 ✓, C7 ✓.
The KB is **satisfiable**, and the model says the outage was caused by a
**network fault** with a **hardware fault** also indicated.

> **Trap.** T is the one symbol that is not pure. Any assignment of T works here
> because C3 is satisfied by R and C4 by H — but you must *say* that, not leave
> T unassigned. A "complete" BSAT solution assigns every symbol.

</details>

<details><summary><b>Show solution — Paper A Q3 (Bayesian network, 9 marks)</b></summary>

**(a) Network + CPTs [4 marks — structure 2, CPTs 2]**

**Build it one sentence at a time.** Each sentence of the prose gives you one
or two arrows, and the arrow always points **from the cause to the effect**:

```
 "RU is positively influenced by PM and BH"   ->   PM -> RU     BH -> RU
 "IA is positively influenced by PM and BS"   ->   PM -> IA     BS -> IA
 "OF is directly determined by RU and IA"     ->   RU -> OF     IA -> OF
 "OF and SA contribute to CS"                 ->   OF -> CS     SA -> CS
```

Eight arrows, four sentences. Now stack the nodes in layers — roots on top,
and every arrow points straight down:

```
  LAYER 0        BH        PM        BS              SA
  (roots)          \      /  \      /                |
                    \    /    \    /                 |
                     v  v      v  v                  |
  LAYER 1             RU        IA                   |
                       \        /                    |
                        \      /                     |
                         v    v                      |
  LAYER 2                  OF                        |
                             \                      /
                              \                    /
                               v                  v
  LAYER 3                          CS
```

Read it back to check: **RU has two arrows coming in** (BH, PM) · **IA has two**
(PM, BS) · **OF has two** (RU, IA) · **CS has two** (OF, SA). Every node except
the four roots has exactly two parents, so every CPT has 4 rows.

> **Notice PM appears in two of those sentences**, so PM has **two children**,
> RU and IA. That single fact is what makes part (b) claim 2 false — it creates
> a second route from BH to OF that does not go straight down. Mark any node
> with two children on your diagram; that is where the traps live.

Written as parent lists — this is the safer thing to put on paper:

```
 PM, BH, BS, SA : roots (no parents)
 RU  : parents PM, BH
 IA  : parents PM, BS
 OF  : parents RU, IA
 CS  : parents OF, SA
```

CPTs. **Everything not specified in the problem is 0.5**, per the instruction:

```
 P(PM=T) = 0.5    P(BH=T) = 0.5    P(BS=T) = 0.5    P(SA=T) = 0.5

 PM BH | P(RU=T)   0.10/0.40/0.50/0.80 for RU=F        (given)
  T  T |  0.90
  T  F |  0.60
  F  T |  0.50
  F  F |  0.20

 PM BS | P(IA=T)                                        (given)
  T  T |  0.90
  T  F |  0.70
  F  T |  0.60
  F  F |  0.20

 RU IA | P(OF=T)                                        (given, from the prose)
  T  T |  0.95
  T  F |  0.75
  F  T |  0.55
  F  F |  0.15

 OF SA | P(CS=T)                                        (NOT specified -> 0.5)
  T  T |  0.50
  T  F |  0.50
  F  T |  0.50
  F  F |  0.50
```

Say in one line: *8 binary variables would need 2⁸ − 1 = 255 numbers as a full
joint; this network needs 4 + 4 + 4 + 4 + 4 = 20.*

**(b) D-separation [3 marks]**

*Rules:* a path is blocked at M when — **chain** `X→M→Y`: M **is** observed ·
**fork** `X←M→Y`: M **is** observed · **collider** `X→M←Y`: M is **not**
observed **and** no descendant of M is observed.

**(1) OF ⊥ PM | {RU, IA} — TRUE.**

```
 Path 1:  PM -> RU -> OF     CHAIN at RU,  RU IS observed   -> BLOCKED
 Path 2:  PM -> IA -> OF     CHAIN at IA,  IA IS observed   -> BLOCKED
 Every path is blocked  ->  d-separated  ->  the statement is TRUE.
```

RU and IA are OF's only parents, so they screen OF off from everything upstream.
*(Numerical confirmation: P(OF | RU=T, IA=T, PM=T) = P(OF | RU=T, IA=T, PM=F)
= 0.95 — you read it straight off the CPT row.)*

**(2) OF ⊥ BH | RU — FALSE.**

```
 Path 1:  BH -> RU -> OF                CHAIN at RU, RU IS observed -> BLOCKED
 Path 2:  BH -> RU <- PM -> IA -> OF
            at RU : COLLIDER, and RU IS observed          -> OPEN
            at PM : FORK,     PM is NOT observed          -> OPEN
            at IA : CHAIN,    IA is NOT observed          -> OPEN
          -> the whole path is OPEN
 One open path is enough  ->  d-CONNECTED  ->  the statement is FALSE.
```

**Explanation to write down:** observing RU *opens* the collider — this is
"explaining away". If uptime is high but the batteries are known to be bad,
preventive maintenance becomes the likely reason; and PM also raises inventory
accuracy, which feeds order fulfilment. So BH carries information about OF even
after RU is known.

*Numerical confirmation, worth quoting:*
`P(OF=T | RU=T, BH=T) = 0.8814` but `P(OF=T | RU=T, BH=F) = 0.8900`. They
differ, therefore not independent.

> **This is trap #34 and it is the most examined idea in Ch 10.** The collider
> rule runs *backwards* from chain and fork. Part (1) looks harder and is the
> easy one; part (2) looks obvious and is the trap.

**(c) The query [2 marks]**

**Query extraction first** (0.5 marks before any arithmetic):

```
 P(PM, BH, BS, SA, RU, IA, OF, CS)   -- all eight variables are instantiated TRUE,
                                        so this is a FULL JOINT, not a conditional.
 BN chain rule:
   = P(PM)·P(BH)·P(BS)·P(SA)·P(RU|PM,BH)·P(IA|PM,BS)·P(OF|RU,IA)·P(CS|OF,SA)
```

Substitute:

```
   = 0.5 × 0.5 × 0.5 × 0.5 × 0.90 × 0.90 × 0.95 × 0.5
   = 0.0625 × 0.90            = 0.05625
   = 0.05625 × 0.90           = 0.050625
   = 0.050625 × 0.95          = 0.04809375
   = 0.04809375 × 0.5         = 0.024046875
```

**Answer ≈ 0.0240 (about 2.4 %).**

</details>

<details><summary><b>Show solution — Paper A Q4 (HMM + Viterbi, 8 marks)</b></summary>

**(a) The model [3 marks]**

States `G = Good`, `D = Degraded`, `C = Congested`. Observations `F = Fast`,
`S = Slow`.

**Transition matrix** — rows are the **from** state; each row sums to 1 [1 mark]:

```
 from \ to |   Good   Degraded  Congested   row sum
 ----------+----------------------------------------
   Good    |   0.6      0.3        0.1        1.0 ✓
 Degraded  |   0.1      0.6        0.3        1.0 ✓
 Congested |   0.0      0.3        0.7        1.0 ✓
```

**Emission matrix** — each row sums to 1 [1 mark]:

```
   state   |   Fast    Slow     row sum
 ----------+---------------------------
   Good    |   0.8      0.2       1.0 ✓
 Degraded  |   0.4      0.6       1.0 ✓
 Congested |   0.1      0.9       1.0 ✓
```

*(Note the two given the other way round in the prose: "Good reports Fast 80 %"
gives Slow = 0.2, and "Congested reports Slow 90 %" gives Fast = 0.1.)*

**Initial distribution:** equal likelihood → π(G) = π(D) = π(C) = **1/3**.

**Diagrams [1 mark]** — draw both; the marking scheme allocates marks to the
diagram separately from the table.

```
 TRANSITION                              EMISSION
      0.6                                  G --0.8--> Fast
     ,---.                                 G --0.2--> Slow
     v   |     0.3                         D --0.4--> Fast
    (G) -+---------> (D) <--.              D --0.6--> Slow
     ^ \            / ^  0.6 |             C --0.1--> Fast
     |  \0.1       /0.1      '             C --0.9--> Slow
   0.1   \        /
     |    v      v      0.3
     '--- (C) <-------- (D)
           |   0.7
           '---'
      (no arc C -> G : 0.0)
```

**(b) Viterbi for O = (Slow, Fast) [5 marks]**

```
 v1(j)  = π(j) · b_j(o1)
 vt(j)  = [ MAX over i of  v(t-1)(i) · a_ij ] · b_j(ot)
 bp t(j)= argmax over i of [ v(t-1)(i) · a_ij ]
```

**t = 1, observation = "Slow" [0.5 marks]**

```
 v1(Good)      = 1/3 × 0.2 = 0.066667
 v1(Degraded)  = 1/3 × 0.6 = 0.200000
 v1(Congested) = 1/3 × 0.9 = 0.300000
                             --------
                       sum =  0.566667
```

**Normalise at t = 1 — class convention [1 mark]**

```
 v1(Good)      = 0.066667 / 0.566667 = 0.117647
 v1(Degraded)  = 0.200000 / 0.566667 = 0.352941
 v1(Congested) = 0.300000 / 0.566667 = 0.529412
```

**t = 2, observation = "Fast" — MAX, not SUM [3 marks]**

```
 into Good:
   max( 0.117647×0.6 , 0.352941×0.1 , 0.529412×0.0 )
 = max( 0.070588    , 0.035294     , 0.000000     ) = 0.070588   bp = Good
   v2(Good)      = 0.070588 × 0.8 = 0.056471

 into Degraded:
   max( 0.117647×0.3 , 0.352941×0.6 , 0.529412×0.3 )
 = max( 0.035294    , 0.211765     , 0.158824     ) = 0.211765   bp = Degraded
   v2(Degraded)  = 0.211765 × 0.4 = 0.084706

 into Congested:
   max( 0.117647×0.1 , 0.352941×0.3 , 0.529412×0.7 )
 = max( 0.011765    , 0.105882     , 0.370588     ) = 0.370588   bp = Congested
   v2(Congested) = 0.370588 × 0.1 = 0.037059
```

**Trellis**

```
              t = 1 (Slow)     t = 2 (Fast)
 Good           0.117647       0.056471   (bp Good)
 Degraded       0.352941     * 0.084706 * (bp Degraded)
 Congested      0.529412       0.037059   (bp Congested)
```

**Termination and backtrace [0.5 marks]**

```
 max at t=2  =  0.084706  at DEGRADED
 bp2(Degraded) = Degraded
 => MOST LIKELY SEQUENCE :  DEGRADED  ->  DEGRADED
```

**Answer: Degraded → Degraded.** It reads correctly: "Slow" points hardest at
Congested, but Congested cannot emit "Fast" easily (0.1) and cannot reach Good
at all, so Degraded — decent on both observations — wins the *path*.

> **Two marks people lose here.** (1) Using SUM: that is the Forward algorithm.
> Viterbi is MAX plus backpointers. (2) Not normalising at t = 1: the paper says
> *"strictly follow the approach as discussed in class"* and the scheme gives a
> mark for that line. The normalisation cannot change the answer — it scales
> every later value by the same constant — but write it anyway.

</details>

<details><summary><b>Show solution — Paper A Q5 (short answers, 7 marks)</b></summary>

**(a) Admissible but not consistent — YES, it is possible [2 marks]**

*Definitions first:*
**Admissible** — h(n) ≤ h\*(n) for every n: the heuristic never overestimates
the true remaining cost.
**Consistent (monotonic)** — h(n) ≤ c(n, n′) + h(n′) for every edge: the
estimate never drops by more than the step cost.

Consistency is the **stronger** condition. Consistent ⇒ admissible, but not the
other way round.

*Numerical example:*

```
        1          4
    S -----> A -----> G          and a direct edge  S -----> G  (cost 6)
    h(S) = 5     h(A) = 1     h(G) = 0

 True costs:  h*(S) = min(1+4, 6) = 5      h*(A) = 4      h*(G) = 0
 ADMISSIBLE?   5 ≤ 5 ✓      1 ≤ 4 ✓      0 ≤ 0 ✓         -> yes, admissible
 CONSISTENT?   edge S→A :  h(S) ≤ c(S,A) + h(A)
                           5    ≤   1     +   1  = 2      -> 5 > 2, FAILS
```

So h is admissible but **not** consistent: the estimate collapses from 5 to 1
across a step that only costs 1.

*Real-world case study:* a delivery-routing app estimates remaining time from
straight-line distance, but for one leg it also happens to know a *measured*
door-to-door time from a partner's data, which is much tighter. Every estimate
is still a lower bound on the true time (admissible), but the estimate drops
sharply as soon as you enter that one well-measured leg (inconsistent).

*Consequence to state:* with an admissible-but-inconsistent heuristic, **A\*
tree search is still optimal**, but **A\* graph search is not** unless you
re-open closed nodes when a cheaper path to them is found.

**(b) IDS evaluation [2 marks]** — *answer in a list, not a paragraph.*

IDS runs **depth-limited DFS** with limit L = 0, 1, 2, … until the goal is
found, restarting from scratch each round.

| Dimension | IDS | Reason |
|---|---|---|
| **Complete** | Yes (finite b) | every depth is eventually reached |
| **Optimal** | Yes, if step costs are uniform | the shallowest goal is found first |
| **Time** | O(b^d) | the last iteration dominates |
| **Space** | **O(bd)** | it is a DFS — only one branch is in memory |

*Example.* b = 3, goal at depth d = 3.

```
 IDS nodes generated = (d+1)·b^0 + d·b^1 + (d−1)·b^2 + 1·b^3
                     =    4      +  3·3  +   2·9     +  27   = 58
 BFS nodes generated =  b + b^2 + b^3    =    3 + 9 + 27     = 39
```

IDS generates ~49 % more nodes, and that is the price for using O(bd) memory
instead of O(b^d). **IDS is the preferred uninformed method when the depth of
the solution is unknown** — it has DFS's space and BFS's optimality.

**(c) Markov chain [3 marks]**

*State the convention first — this is the trap.* The table is headed **"from"**
across the top, so **each COLUMN sums to 1**, not each row.

```
 STEP 1 — fill the missing entries (each column must sum to 1)

              from U   from R   from D
   to U        0.5      0.2      0.1
   to R        0.3      [0.5]    0.3
   to D       [0.2]     0.3     [0.6]
              -----    -----    -----
   col sum      1.0      1.0      1.0  ✓

   P(D|U) = 1 − (0.5 + 0.3) = 0.2
   P(R|R) = 1 − (0.2 + 0.3) = 0.5
   P(D|D) = 1 − (0.1 + 0.3) = 0.6
```

```
 STEP 2 — initial probability from the given sequence
   Assumption (state it): π is estimated by the relative frequency of the
   states in the observed sequence (maximum-likelihood estimate).
   Sequence (R, R, U, R):  R appears 3 times, U once, D never.
   π(R) = 3/4 = 0.75      π(U) = 1/4 = 0.25      π(D) = 0
```

```
 STEP 3 — sequence likelihood
   P(s1 … sT) = π(s1) · Π P(st | s(t−1))

   P(R, R, U, R) = π(R) · P(R|R) · P(U|R) · P(R|U)
                 = 0.75 ×  0.5   ×  0.2   ×  0.3
                 = 0.0225
```

**Answer: 0.0225 (2.25 %).**

> Read each factor off the **column** of the *previous* state. `P(U|R)` is the
> "to U" row of the "from R" column = 0.2, **not** the "to R" row of the
> "from U" column. Getting this backwards transposes the whole matrix and
> silently changes every number.

</details>

## Paper B — Solutions

<details><summary><b>Show solution — Paper B Q1 (alpha–beta, 9 marks)</b></summary>

**(a) Minimax [3 marks]**

```
 S1 (MIN) = min( 8, 5,  6) =  5
 S2 (MIN) = min( 4, 9,  3) =  3
 S3 (MIN) = min( 7, 2, 10) =  2

 S0 (MAX) = max( 5, 3,  2) =  5     ->  MAX plays the move to S1
```

**(b) Alpha–beta, left to right [4 marks]**

```
 root S0:  α = −∞, β = +∞

 --- S1 (MIN), inherits α = −∞, β = +∞
     leaf 8   β = min(+∞, 8) = 8      8 > α  -> continue
     leaf 5   β = min(8, 5)   = 5     5 > α  -> continue
     leaf 6   β = min(5, 6)   = 5
     S1 returns 5.        root: α = max(−∞, 5) = 5

 --- S2 (MIN), inherits α = 5, β = +∞
     leaf 4   β = min(+∞, 4) = 4
              β (4) ≤ α (5)   ->  *** α-CUT ***
     PRUNE leaves 9 and 3 — never evaluated.
     S2 returns ≤ 4.      root: α stays 5

 --- S3 (MIN), inherits α = 5, β = +∞
     leaf 7   β = min(+∞, 7) = 7      7 > 5  -> continue
     leaf 2   β = min(7, 2)   = 2
              β (2) ≤ α (5)   ->  *** α-CUT ***
     PRUNE leaf 10 — never evaluated.
     S3 returns ≤ 2.      root: α stays 5

 ROOT VALUE = 5, move to S1.  (Same as part (a).)
```

**Leaves never evaluated: the 9 and the 3 under S2, and the 10 under S3.**
**6 of the 9 leaves were evaluated; 3 were pruned.**

State the reason in words: once MAX has secured 5 on the left, any MIN branch
that can already be driven to 4 or lower can never improve on 5, so the rest of
that branch is irrelevant *no matter what it contains* — including the 10.

**(c) Why the value is unchanged, and why the count is not [2 marks]**

Alpha–beta prunes only branches that **provably cannot affect** the root value:
a cut happens when β ≤ α, i.e. when MIN can already guarantee something MAX
would never choose. The pruned subtree can only make that branch *worse* for
MAX. So the backed-up root value is **always identical** to plain minimax —
alpha–beta changes the *cost*, never the *answer*.

The count, however, depends entirely on ordering. Re-order the children as
**S2, S3, S1**:

```
 S2 first (α = −∞): all 3 leaves evaluated -> 3.  α = 3
 S3 (α = 3): leaf 7 (>3), leaf 2 -> β = 2 ≤ 3  -> α-cut, prune leaf 10.  2 leaves
 S1 (α = 3): leaf 8 (>3), leaf 5 (>3), leaf 6 -> 5.                      3 leaves
 TOTAL = 8 of 9 evaluated, only 1 pruned  (vs 6 and 3 in the printed order)
```

And in the **best** case — best branch first, and smallest leaf first inside
each MIN node (`S1: 5,8,6 · S2: 3,4,9 · S3: 2,7,10`) — S1 costs 3 leaves and
sets α = 5, then S2 cuts after its first leaf (3 ≤ 5) and S3 cuts after its
first leaf (2 ≤ 5): **5 of 9 evaluated, 4 pruned**.

*This is the standard result to quote:* with perfect ordering alpha–beta
examines O(b^(d/2)) leaves instead of O(b^d), effectively **doubling the search
depth** for the same work.

</details>

<details><summary><b>Show solution — Paper B Q2 (FOL, 7 marks)</b></summary>

**(a) Translation [2 marks]** — predicates: `Robot(x)`, `Charged(x)`,
`Operates(x)`, `Tech(x)`, `Maintains(x, y)`.

```
 1. All robots that are charged can operate.
      ∀x ( Robot(x) ∧ Charged(x) → Operates(x) )

 2. Every technician maintains at least one robot.
      ∀x ( Tech(x) → ∃y ( Robot(y) ∧ Maintains(x, y) ) )

 3. Some robots are not charged.
      ∃x ( Robot(x) ∧ ¬Charged(x) )

 4. No robot operates without being charged.
      ∀x ( Robot(x) ∧ Operates(x) → Charged(x) )
      equivalently  ¬∃x ( Robot(x) ∧ Operates(x) ∧ ¬Charged(x) )

 5. Not all technicians maintain every robot.
      ¬∀x ( Tech(x) → ∀y ( Robot(y) → Maintains(x, y) ) )
      equivalently  ∃x ( Tech(x) ∧ ∃y ( Robot(y) ∧ ¬Maintains(x, y) ) )
```

> **The pattern that decides these marks:** `∀` goes with `→`, `∃` goes with
> `∧`. `∀x (Robot(x) ∧ Charged(x))` would assert that *everything* in the
> universe is a charged robot. `∃x (Robot(x) → Charged(x))` is satisfied
> vacuously by anything that is not a robot.

**(b) Unification [2 marks]**

```
 1. Maintains(Ravi, x)  &  Maintains(y, Robot7)
      θ = { y/Ravi , x/Robot7 }                              SUCCEEDS

 2. Maintains(Ravi, x)  &  Maintains(x, Robot7)
      FAILS. x must bind to Robot7 from argument 2 and to Ravi from
      argument 1. The same variable cannot take two values.
      -> This is why you STANDARDISE APART first: rename the second
         sentence's x to x', and it unifies as { x'/Ravi , x/Robot7 }.

 3. Status(f(x), y)  &  Status(z, g(z))
      arg1: z / f(x)
      arg2: y / g(z) = g(f(x)) after applying the first binding
      θ = { z/f(x) , y/g(f(x)) }                             SUCCEEDS

 4. Status(x)  &  Status(f(x))
      FAILS the OCCUR CHECK. x would have to equal f(x), which has no
      finite solution — x = f(f(f(…))).
```

**(c) Resolution refutation [3 marks]**

```
 STEP 1 — CNF of the KB
   1. ∀x (Robot(x) ∧ Charged(x) → Operates(x))
        implication elimination : ¬(Robot(x) ∧ Charged(x)) ∨ Operates(x)
        De Morgan               : ¬Robot(x) ∨ ¬Charged(x) ∨ Operates(x)     [C1]
   2. Robot(R7)                                                             [C2]
   3. Charged(R7)                                                           [C3]

 STEP 2 — NEGATE THE GOAL and convert  (write "assume ¬α" as your first line)
   goal   :  ∃x ( Robot(x) ∧ Operates(x) )
   ¬goal  : ¬∃x ( Robot(x) ∧ Operates(x) )
          =  ∀x ¬( Robot(x) ∧ Operates(x) )        quantifier duality
          =  ∀x ( ¬Robot(x) ∨ ¬Operates(x) )       De Morgan                [C4]

 STEP 3 — RESOLVE
   R1 :  C1 { ¬Robot(x), ¬Charged(x), Operates(x) }
         C2 { Robot(R7) }                       unifier { x / R7 }
      -> { ¬Charged(R7), Operates(R7) }                                     [C5]

   R2 :  C5 { ¬Charged(R7), Operates(R7) }
         C3 { Charged(R7) }
      -> { Operates(R7) }                                                   [C6]

   R3 :  C4 { ¬Robot(x), ¬Operates(x) }
         C2 { Robot(R7) }                       unifier { x / R7 }
      -> { ¬Operates(R7) }                                                  [C7]

   R4 :  C6 { Operates(R7) }
         C7 { ¬Operates(R7) }
      -> { }        *** THE EMPTY CLAUSE ***

 STEP 4 — CONCLUDE
   KB ∧ ¬goal is UNSATISFIABLE, therefore  KB ⊨ ∃x (Robot(x) ∧ Operates(x)).
   The witness produced along the way is x = R7.
```

> **The single commonest error:** adding the *goal* instead of its negation.
> Resolution is a **refutation** method — you assume the opposite and derive a
> contradiction. Write that assumption as your first line and you protect the
> mark even if the resolvents go wrong.

</details>

<details><summary><b>Show solution — Paper B Q3 (Bayesian network, 9 marks)</b></summary>

**(a) P(CL = T) by variable elimination [3 marks]**

```
 STEP 0 — PRUNE.  AT and AR are leaves that are neither query nor evidence
                  -> irrelevant, delete them.  (Saying this is worth a mark.)
   Relevant factors:  f_Ph(Ph) = P(Ph),  f_WP(WP) = P(WP),  f_CL(CL,Ph,WP)

 STEP 1 — eliminate Ph and WP together against f_CL:
   P(CL=T) = Σ over ph, wp of  P(ph)·P(wp)·P(CL=T | ph, wp)

     Ph=T, WP=T : 0.2 × 0.4 × 0.95 = 0.08 × 0.95 = 0.0760
     Ph=T, WP=F : 0.2 × 0.6 × 0.70 = 0.12 × 0.70 = 0.0840
     Ph=F, WP=T : 0.8 × 0.4 × 0.50 = 0.32 × 0.50 = 0.1600
     Ph=F, WP=F : 0.8 × 0.6 × 0.05 = 0.48 × 0.05 = 0.0240
                                                   ------
                                        P(CL=T) =  0.3440
```

Free check: the four *prior* weights 0.08 + 0.12 + 0.32 + 0.48 = 1.00 ✓.
**P(CL = T) = 0.344, P(CL = F) = 0.656.**

**(b) P(Ph = T | AT = T) by enumeration [3 marks]**

```
 STEP 1 — identify the pieces (0.5 marks; always write this line)
   Query X = Ph      Evidence e = { AT = T }      Hidden Y = { WP, CL }
   AR is a leaf, neither query nor evidence -> IRRELEVANT, prune it.

 STEP 2 — standard form
   P(Ph | AT=T) = α · P(Ph, AT=T) = α · Σ over wp, cl of P(Ph)P(wp)P(cl|Ph,wp)P(AT=T|cl)

 STEP 3 — evaluate P(Ph=T, AT=T)
   From (a) the Ph=T rows give   P(Ph=T, CL=T) = 0.0760 + 0.0840 = 0.1600
                                 P(Ph=T, CL=F) = 0.2 − 0.1600     = 0.0400
   P(Ph=T, AT=T) = 0.1600 × 0.80 + 0.0400 × 0.05
                 = 0.1280 + 0.0020 = 0.1300

 STEP 4 — evaluate P(Ph=F, AT=T)
                                 P(Ph=F, CL=T) = 0.1600 + 0.0240 = 0.1840
                                 P(Ph=F, CL=F) = 0.8 − 0.1840     = 0.6160
   P(Ph=F, AT=T) = 0.1840 × 0.80 + 0.6160 × 0.05
                 = 0.1472 + 0.0308 = 0.1780

 STEP 5 — NORMALISE
   P(AT=T) = 0.1300 + 0.1780 = 0.3080
   α = 1 / 0.3080
   P(Ph=T | AT=T) = 0.1300 / 0.3080 = 0.4221
   P(Ph=F | AT=T) = 0.1780 / 0.3080 = 0.5779
                                      ------
                             CHECK =  1.0000 ✓
```

**Answer ≈ 0.422.** The prior was 0.20; a detected takeover more than doubles
it. Also confirm P(CL = T) = 0.344 from (a) is consistent: 0.1600 + 0.1840 =
0.3440 ✓.

**(c) D-separation and likelihood weighting [3 marks]**

```
 1. Ph ⊥ WP ?
      The only path is  Ph -> CL <- WP : a COLLIDER at CL.
      CL is NOT observed, and no descendant of CL (AT, AR) is observed.
      -> path BLOCKED  ->  YES, independent.  This is how the net was built.
      Numerically: P(Ph|WP=T) = P(Ph|WP=F) = 0.20 ✓

 2. Ph ⊥ WP | CL = T ?
      Same collider at CL, but CL IS NOW OBSERVED  ->  the path is OPENED.
      -> NO, dependent.  This is EXPLAINING AWAY.
      Numerically: P(Ph=T | WP=T, CL=T) = 0.3220
                   P(Ph=T | WP=F, CL=T) = 0.7778
      Knowing the password was weak explains the leak, so phishing becomes
      much less likely. They differ hugely — quote both numbers.

 3. LIKELIHOOD WEIGHTING
      w = Π over EVIDENCE nodes e of  P( e | Parents(e) )
      Evidence: AT = T (parent CL = T, sampled) and AR = T (parent CL = T).
      w = P(AT=T | CL=T) × P(AR=T | CL=T)
        = 0.80 × 0.90
        = 0.72
      The SAMPLED variables Ph, WP and CL do NOT enter w — they were drawn
      from their own CPTs, so their probabilities are already accounted for.

      Final estimate over N samples:
        P(Ph=T | AT=T, AR=T) = ( Σ w over samples with Ph = T ) / ( Σ w over ALL samples )
      Nothing is rejected, which is why LW beats rejection sampling when the
      evidence is unlikely.
```

> Note how (1) and (2) are the *same path* with opposite answers. That is the
> collider rule, and it is backwards from chain and fork on purpose.

</details>

<details><summary><b>Show solution — Paper B Q4 (HMM + Forward, 8 marks)</b></summary>

**(a) The model [3 marks]**

```
 TRANSITION (rows = from)          EMISSION
  from \ to  Healthy  Faulty        state   Normal  Vibration
  Healthy      0.8     0.2          Healthy   0.9      0.1
  Faulty       0.3     0.7          Faulty    0.2      0.8
             (rows sum to 1 ✓)              (rows sum to 1 ✓)

 INITIAL  π(Healthy) = 0.7   π(Faulty) = 0.3
```

*(Read the prose carefully: "Healthy reports Normal 90 %" gives Vibration = 0.1;
"Faulty reports Vibration 80 %" gives Normal = 0.2.)*

```
 TRANSITION DIAGRAM                 EMISSION DIAGRAM
     0.8                              Healthy --0.9--> Normal
    ,---.        0.2                  Healthy --0.1--> Vibration
    v   |  ------------->             Faulty  --0.2--> Normal
  (Healthy)          (Faulty) 0.7     Faulty  --0.8--> Vibration
        ^  <-------------  |   ,--.
        |       0.3        '---'
```

**(b) Forward algorithm, O = (Normal, Vibration, Vibration) [5 marks]**

```
 α1(j)  = π(j) · b_j(o1)
 αt(j)  = [ SUM over i of  α(t−1)(i) · a_ij ] · b_j(ot)
 P(O)   = SUM over j of  αT(j)
```

**t = 1, "Normal"** — initialisation, **do not normalise**:

```
 α1(Healthy) = 0.7 × 0.9 = 0.630000
 α1(Faulty)  = 0.3 × 0.2 = 0.060000
```

**t = 2, "Vibration"** — SUM over predecessors:

```
 into Healthy : [ 0.630000×0.8 + 0.060000×0.3 ] = [ 0.504000 + 0.018000 ] = 0.522000
   α2(Healthy) = 0.522000 × 0.1 = 0.052200
 into Faulty  : [ 0.630000×0.2 + 0.060000×0.7 ] = [ 0.126000 + 0.042000 ] = 0.168000
   α2(Faulty)  = 0.168000 × 0.8 = 0.134400
```

**t = 3, "Vibration"**:

```
 into Healthy : [ 0.052200×0.8 + 0.134400×0.3 ] = [ 0.041760 + 0.040320 ] = 0.082080
   α3(Healthy) = 0.082080 × 0.1 = 0.008208
 into Faulty  : [ 0.052200×0.2 + 0.134400×0.7 ] = [ 0.010440 + 0.094080 ] = 0.104520
   α3(Faulty)  = 0.104520 × 0.8 = 0.083616
```

**Trellis**

```
                t=1 (Normal)   t=2 (Vibration)   t=3 (Vibration)
 Healthy          0.630000        0.052200          0.008208
 Faulty           0.060000        0.134400          0.083616
 Σ                0.690000        0.186600          0.091824  = P(O)
```

**Termination: P(O) = 0.091824 ≈ 0.0918.**

**Filtering at t = 3:**

```
 P(Faulty | O) = α3(Faulty) / P(O) = 0.083616 / 0.091824 = 0.9106
```

Two consecutive "Vibration" readings put the pump at a **91 % chance of being
Faulty** — raise the work order.

**Why you must not normalise inside the recursion:** P(O) *is* the answer, and
it is the product of the column sums you would be dividing away. Normalising
destroys it. If you want filtered probabilities at an intermediate step,
normalise a **copy** of that column and say so. (The normalise-at-t = 1
convention belongs to Viterbi only.)

</details>

<details><summary><b>Show solution — Paper B Q5 (short answers, 7 marks)</b></summary>

**(a) Consistency ⇒ admissibility [2 marks]**

**Consistency (monotonicity):** for every node n and every successor n′
reached by an action of cost c(n, n′),

```
        h(n)  ≤  c(n, n′) + h(n′)        and     h(goal) = 0
```

**Proof that consistency implies admissibility** (induction on the number of
steps k from n to the nearest goal):

```
 Base   k = 0 : n is a goal, h(n) = 0 = h*(n).  ✓
 Step   assume h(n′) ≤ h*(n′) for all nodes k−1 steps from a goal.
        For n at k steps, let n′ be the next node on an optimal path:
            h(n)  ≤  c(n, n′) + h(n′)        (consistency)
                  ≤  c(n, n′) + h*(n′)       (induction hypothesis)
                  =  h*(n)                   (n′ is on an optimal path)
        Therefore h(n) ≤ h*(n) — admissible.  ∎
```

**Which property A\* needs:**
- **A\* tree search** is optimal with **admissibility** alone.
- **A\* graph search** needs **consistency**. With a CLOSED list, a node is
  expanded once and never reconsidered; consistency guarantees f is
  non-decreasing along any path, so the first time A\* expands a node it has
  already found the cheapest route to it. Without consistency you can close a
  node on an expensive path and later discover a cheaper one — so you must
  either use a consistent h or re-open closed nodes.

**(b) Simulated annealing [2 marks]**

Higher is better, so moving 62 → 59 is a **worsening** move of ΔE = −3, which
SA accepts with probability e^(ΔE/T):

```
 T = 15 :  P = e^(−3/15) = e^(−0.2)  = 0.8187      about 82 %
 T =  1 :  P = e^(−3/1)  = e^(−3)    = 0.0498      about  5 %
```

**Comment.** Early in the run (high T) the search accepts almost any downhill
move — it explores freely and can climb out of local optima. Late in the run
(low T) it accepts a downhill move only about one time in twenty — it behaves
almost like plain hill climbing and settles into the best basin it has found.
That transition *is* the annealing schedule. As T → 0 SA becomes hill climbing;
if T is lowered slowly enough, SA finds the global optimum with probability
approaching 1. *(An improving move is always accepted, ΔE ≥ 0 ⇒ P = 1.)*

**(c) Mixed strategy [3 marks]**

```
 (i) NO SADDLE POINT
     row minima :  min(4, −2) = −2 ,  min(−1, 3) = −1   ->  MAXIMIN = −1
     col maxima :  max(4, −1) =  4 ,  max(−2, 3) =  3   ->  MINIMAX =  3
     MAXIMIN (−1)  ≠  MINIMAX (3)   ->  no saddle point, go MIXED.
     (No dominance either: neither row nor column dominates.)
```

```
 (ii) ROW player plays R1 with probability p, R2 with (1 − p).
      Expected payoff against each pure reply of the column player:

        against C1 :  E1(p) =  4p + (−1)(1 − p) =  4p − 1 + p  = 5p − 1
        against C2 :  E2(p) = (−2)p +  3 (1 − p) = −2p + 3 − 3p = 3 − 5p

      INDIFFERENCE CONDITION — set them equal:
        5p − 1 = 3 − 5p
        10p    = 4
        p      = 0.4          so  1 − p = 0.6

      VALUE  V = 5(0.4) − 1 = 2 − 1 = 1.0
      CHECK  V = 3 − 5(0.4) = 3 − 2 = 1.0  ✓  both lines agree
```

```
 (iii) COLUMN player plays C1 with probability q:
        row R1 :   4q + (−2)(1 − q) = 6q − 2
        row R2 : (−1)q +  3 (1 − q) = 3 − 4q
        6q − 2 = 3 − 4q   ->   10q = 5   ->   q = 0.5
```

```
 SOLUTION   Row plays (R1, R2) = (0.4, 0.6)
            Column plays (C1, C2) = (0.5, 0.5)
            VALUE of the game V = 1.0, in the ROW player's favour.

 Closed form, same answer:  p = (d − c)/((a − c) + (d − b))
                              = (3 − (−1)) / ((4 − (−1)) + (3 − (−2))) = 4/10 = 0.4
                            V = (ad − bc)/((a − c) + (d − b)) = (12 − 2)/10 = 1.0
```

**What "making the opponent indifferent" means:** you choose p so your opponent
earns the same expected payoff whichever pure strategy they pick. That removes
their ability to exploit you — if one reply were better against your mix they
would always play it, and you could then improve by shifting p. Only at the
indifference point can neither side gain by deviating alone, which is exactly
a mixed-strategy Nash equilibrium.

> **Sign errors end this question.** Write `(−2)(1 − p)` with brackets, never
> `−2 − 2p`, and always verify V on both lines. If E1(p) and E2(p) disagree you
> have an algebra slip, and you can catch it before the examiner does.

</details>

## Rapid Drill — Solutions

<details><summary><b>Show solutions — D1 to D6 (search)</b></summary>

**D1 · UCS.** Expand the frontier node with the smallest **g** (path cost so
far). No heuristic is used.

```
 Expand S (g=0)  -> frontier: A(2), B(4)
 Expand A (g=2)  -> C via A = 2+4 = 6 ; G via A = 2+9 = 11
                    frontier: B(4), C(6), G(11)
 Expand B (g=4)  -> C via B = 4+1 = 5  (BETTER than 6, replace)
                    G via B = 4+8 = 12 (worse than 11, discard)
                    frontier: C(5), G(11)
 Expand C (g=5)  -> G via C = 5+3 = 8  (BETTER than 11, replace)
                    frontier: G(8)
 Expand G (g=8)  -> GOAL
```

**Expansion order: S, A, B, C, G. Path S → B → C → G, cost 8.**
Note UCS expanded A before B even though A is not on the solution path — it
had the smaller g. UCS is optimal but blind to where the goal is.

---

**D2 · A\*.** f(n) = g(n) + h(n). Ties broken alphabetically.

```
 f(S) = 0 + 7 = 7                 expand S
   A : g=2, f = 2 + 6 = 8
   B : g=4, f = 4 + 4 = 8         tie at 8 -> alphabetical -> A first
 expand A (f=8)
   C via A : g=6, f = 6 + 3 = 9
   G via A : g=11, f = 11 + 0 = 11
 expand B (f=8)
   C via B : g=5, f = 5 + 3 = 8   BETTER, replace the f=9 entry
   G via B : g=12, f = 12         worse, discard
 expand C (f=8)
   G via C : g=8, f = 8 + 0 = 8   BETTER, replace
 expand G (f=8)                    GOAL
```

**Expansion order: S, A, B, C, G. Path S → B → C → G, cost 8.**
Note every f on the solution path is 8 — the signature of a well-behaved
heuristic.

**Admissibility audit** — true remaining costs h\*:

```
 h*(G)=0   h*(C)=3   h*(B)=min(1+3, 8)=4   h*(A)=min(4+3, 9)=7   h*(S)=min(2+7, 4+4)=8

 node   h(n)   h*(n)   h ≤ h* ?
   S      7      8      ✓
   A      6      7      ✓
   B      4      4      ✓ (tight)
   C      3      3      ✓ (tight)
   G      0      0      ✓
 -> ADMISSIBLE.
```

**Consistency audit** — test h(n) ≤ c(n, n′) + h(n′) on **every edge**:

```
 S→A : 7 ≤ 2 + 6 = 8  ✓      A→C : 6 ≤ 4 + 3 = 7  ✓      C→G : 3 ≤ 3 + 0 = 3  ✓
 S→B : 7 ≤ 4 + 4 = 8  ✓      A→G : 6 ≤ 9 + 0 = 9  ✓
 B→C : 4 ≤ 1 + 3 = 4  ✓      B→G : 4 ≤ 8 + 0 = 8  ✓
 -> CONSISTENT (so A* graph search is optimal here).
```

---

**D3 · Admissible but not consistent.**

```
 True costs:  h*(G) = 0 ,  h*(A) = 4 ,  h*(S) = min(1 + 4, 6) = 5

 ADMISSIBLE:  h(S)=5 ≤ 5 ✓    h(A)=1 ≤ 4 ✓    h(G)=0 ≤ 0 ✓

 CONSISTENCY, edge by edge:
   S→A :  h(S) ≤ c + h(A)  ->  5 ≤ 1 + 1 = 2   ***  5 > 2 — VIOLATED  ***
   A→G :  h(A) ≤ c + h(G)  ->  1 ≤ 4 + 0 = 4   ✓
   S→G :  h(S) ≤ c + h(G)  ->  5 ≤ 6 + 0 = 6   ✓
```

One violated edge is enough. h is **admissible but not consistent**: the
estimate falls from 5 to 1 across a step costing only 1.

---

**D4 · IDS vs BFS node counts.**

```
 N(IDS) = (d+1)·b^0 + d·b^1 + (d−1)·b^2 + … + 1·b^d
 N(BFS) = b + b^2 + … + b^d

 b = 3, d = 3:
   IDS = 4·1 + 3·3 + 2·9 + 1·27 = 4 + 9 + 18 + 27 = 58
   BFS = 3 + 9 + 27                                = 39
   overhead = 58/39 = 1.487  ->  about 49 % more nodes
```

The shallow levels are regenerated on every iteration, but they are cheap:
the **deepest level dominates**, so IDS stays O(b^d) in time while using only
**O(bd) space** instead of BFS's O(b^d). That trade is why IDS is the default
uninformed strategy when the solution depth is unknown.

---

**D5 · Random-restart hill climbing.** Each restart is an independent Bernoulli
trial, so the number of restarts is geometric:

```
 E[restarts until success] = 1 / p = 1 / 0.15 = 6.67  ->  about 7 restarts
```

If a successful run costs S steps and a failed run costs F steps, the expected
total is `S + ((1 − p)/p)·F` — quote that if the question gives you both costs.

---

**D6 · Simulated annealing.** Higher is better, so 40 → 37 is ΔE = −3:

```
 T = 15 :  P = e^(−3/15) = e^(−0.2) = 0.8187   ->  ~82 % accepted
 T =  1 :  P = e^(−3/1)  = e^(−3)   = 0.0498   ->  ~5 % accepted
```

Same move, same ΔE, completely different behaviour — the temperature alone
controls exploration versus exploitation.

</details>

<details><summary><b>Show solutions — D7 to D9 (GA, ACO, MCTS)</b></summary>

**D7 · Genetic algorithm, one generation.**

**(a) Fitness and selection**

```
 chromosome   x    f = x²    p = f / Σf       expected copies (×4)
   00011      3       9      9/102 = 0.0882        0.353
   00101      5      25     25/102 = 0.2451        0.980
   01000      8      64     64/102 = 0.6275        2.510
   00010      2       4      4/102 = 0.0392        0.157
                    -----                          -----
              Σf = 102        Σp = 1.0000          4.000 ✓
```

Both checks — probabilities summing to 1 and expected copies summing to the
population size — are free marks. Note the pressure: `01000` alone takes 63 %
of the wheel.

**(b) Single-point crossover after bit 2**

```
   parent 1 :  01 | 000
   parent 2 :  00 | 101
   ---------------------
   child  1 :  01   101  =  01101  =  13    f = 169
   child  2 :  00   000  =  00000  =   0    f =   0
```

Child 1 (fitness 169) beats every parent — this is crossover doing its job,
recombining the high bit of one parent with the low bits of the other.

**(c) Mutation of bit 5 of child 1**

```
   01101  ->  01100  =  12    f = 144
```

Fitness fell from 169 to 144. That is expected and healthy: mutation is a
**diversity** operator, not an improvement operator. Its job is to reintroduce
alleles that selection has wiped out, so the population cannot converge
prematurely.

---

**D8 · Ant Colony Optimization.**

**(a) Transition probability**

```
 P(edge) = [τ^α · η^β] / Σ over allowed edges of [τ^α · η^β] ,  η = 1/d

 edge   τ     η = 1/d    τ^1 · η^2
  AB   2.0   1/4 = 0.25   2.0 × 0.0625 = 0.1250
  AC   4.0   1/10 = 0.10  4.0 × 0.0100 = 0.0400
  AD   1.0   1/2 = 0.50   1.0 × 0.2500 = 0.2500
                                          ------
                                   Σ  =   0.4150

  P(AB) = 0.1250 / 0.4150 = 0.3012
  P(AC) = 0.0400 / 0.4150 = 0.0964
  P(AD) = 0.2500 / 0.4150 = 0.6024
                            ------
                            1.0000 ✓
```

AC has **twice** the pheromone of AB but is the least likely choice — because
β = 2 squares the visibility term, and AC is 10 units away. **The exponents are
the whole point of the question:** α weights learned experience, β weights
greedy short-term distance.

**(b) Pheromone update**

```
 τ ← (1 − ρ)·τ  +  Δτ         with  Δτ = Q / L  on edges used by the ant

 τ(AD) = (1 − 0.5)(1.0)  +  100/25
       =      0.5        +    4.0
       =      4.5
```

Evaporation first, deposit second. Evaporation is what stops early random tours
from locking the colony into a bad route.

---

**D9 · MCTS / UCB1.**

```
 UCB1(i) = w_i/n_i  +  C · sqrt( ln(N) / n_i )      N = 100, ln(100) = 4.6052, C = √2 = 1.4142

 X : 20/30 = 0.6667  +  1.4142·sqrt(4.6052/30) = 1.4142 × 0.3918 = 0.5541  ->  1.2208
 Y : 12/15 = 0.8000  +  1.4142·sqrt(4.6052/15) = 1.4142 × 0.5541 = 0.7836  ->  1.5836
 Z : 30/55 = 0.5455  +  1.4142·sqrt(4.6052/55) = 1.4142 × 0.2894 = 0.4092  ->  0.9547
```

**Select Y (1.5836).**

Y wins on *both* terms: it has the best win rate **and**, having been visited
only 15 times, the largest exploration bonus. Z is the instructive contrast —
30 wins is the largest raw count, but 30/55 is the worst rate and 55 visits
have shrunk its bonus to the smallest of the three, so it ranks last. **That is
UCB1 balancing exploitation (the first term) against exploration (the second):
the bonus grows with ln N and shrinks as 1/√n, so a node that keeps being
ignored eventually gets tried anyway.**

</details>

<details><summary><b>Show solutions — D10 to D13 (logic, probability, Markov)</b></summary>

**D10 · TT-entailment.** `KB = (P ∨ Q) ∧ (¬P ∨ R)`, query R.

```
  P     Q     R  | (P∨Q) | (¬P∨R) |  KB   |  R
 ---------------------------------------------------
  T     T     T  |   T   |   T    |   T   |  T
  T     T     F  |   T   |   F    |   F   |  -
  T     F     T  |   T   |   T    |   T   |  T
  T     F     F  |   T   |   F    |   F   |  -
  F     T     T  |   T   |   T    |   T   |  T
  F     T     F  |   T   |   T    |   T   |  F   <-- COUNTER-MODEL
  F     F     T  |   F   |   T    |   F   |  -
  F     F     F  |   F   |   T    |   F   |  -
```

**KB has 4 models.** `KB ⊭ R`: entailment requires α true in **every** model of
KB, and the model `P = F, Q = T, R = F` satisfies KB while falsifying R.
Complexity: n symbols → 2ⁿ models, **time O(2ⁿ), space O(n)** (the enumeration
is depth-first).

---

**D11 · Propositional resolution.** `KB = { A → B, B → C, A }`, prove C.

```
 STEP 1 — CNF
   A → B   ->   { ¬A, B }        [C1]
   B → C   ->   { ¬B, C }        [C2]
   A       ->   { A }            [C3]

 STEP 2 — ADD THE NEGATED GOAL   (write "assume ¬C" as your first line)
   ¬C      ->   { ¬C }           [C4]

 STEP 3 — RESOLVE
   C1 { ¬A, B }  +  C3 { A }   ->  { B }        [C5]
   C2 { ¬B, C }  +  C5 { B }   ->  { C }        [C6]
   C4 { ¬C }     +  C6 { C }   ->  { }   *** EMPTY CLAUSE ***

 STEP 4 — CONCLUDE
   KB ∧ ¬C is unsatisfiable, therefore KB ⊨ C.
```

Drop any resolvent containing both a literal and its negation — a tautology is
useless.

---

**D12 · Bayes rule / base rate.**

```
 P(D) = 0.005 ,  P(+|D) = 0.98 (sensitivity) ,  P(−|¬D) = 0.95 so P(+|¬D) = 0.05

 P(D|+) = P(+|D)·P(D) / [ P(+|D)·P(D) + P(+|¬D)·P(¬D) ]
        = (0.98 × 0.005) / [ (0.98 × 0.005) + (0.05 × 0.995) ]
        = 0.004900 / [ 0.004900 + 0.049750 ]
        = 0.004900 / 0.054650
        = 0.0897
```

**About 9 %.** Even with a 98 %-sensitive test, a positive result means the
patient probably does **not** have the disease — because the 0.5 % base rate is
so much smaller than the 5 % false-positive rate, false positives outnumber
true positives ten to one. This is the **base-rate fallacy**, and it is the
standard one-line comment the examiner wants.

---

**D13 · Markov chain.** `P = [[0.7, 0.3], [0.4, 0.6]]`, rows = "from".

**(a) Two-step**

```
 P² = P × P

   P²[1][1] = 0.7×0.7 + 0.3×0.4 = 0.49 + 0.12 = 0.61
   P²[1][2] = 0.7×0.3 + 0.3×0.6 = 0.21 + 0.18 = 0.39     (row sums to 1.00 ✓)
   P²[2][1] = 0.4×0.7 + 0.6×0.4 = 0.28 + 0.24 = 0.52
   P²[2][2] = 0.4×0.3 + 0.6×0.6 = 0.12 + 0.36 = 0.48     (row sums to 1.00 ✓)

 P² = [ [0.61, 0.39],
        [0.52, 0.48] ]
```

**P(state 1 at t + 2 | state 1 at t) = 0.61.**

**(b) Steady state.** Solve π = πP with π₁ + π₂ = 1:

```
 π₁ = 0.7π₁ + 0.4π₂
 0.3π₁ = 0.4π₂        ->   π₁ / π₂ = 4/3

 π₁ = 4/7 = 0.5714     π₂ = 3/7 = 0.4286
 CHECK:  0.5714×0.7 + 0.4286×0.4 = 0.4000 + 0.1714 = 0.5714 ✓
```

Note P² is already close to the steady state in both rows — the chain mixes
quickly, and the starting state stops mattering after a few steps.

</details>

<details><summary><b>Show solutions — D14 to D18 (game theory, auctions, voting)</b></summary>

**D14 · Maximin / saddle point.**

```
 ROW takes the minimum of each row, then the maximum of those:
   A : min(8, 5, 6) = 5     <- best
   B : min(4, 2, 3) = 2
   C : min(7, 4, 9) = 4
   MAXIMIN = 5, at row A

 COLUMN takes the maximum of each column, then the minimum of those:
   X : max(8, 4, 7) = 8
   Y : max(5, 2, 4) = 5     <- best
   Z : max(6, 3, 9) = 9
   MINIMAX = 5, at column Y

 MAXIMIN = MINIMAX = 5  ->  SADDLE POINT at (A, Y).
 VALUE V = 5.  Optimal PURE strategies: row plays A, column plays Y.
```

**Faster, via dominance** — always try this first:

```
 Row A = (8, 5, 6) dominates row B = (4, 2, 3)  — bigger in every column. Delete B.
 Column Y = (5, 2, 4) dominates X = (8, 4, 7) and Z = (6, 3, 9) FOR THE COLUMN
 PLAYER — the entries are the ROW player's payoff, so the column player wants
 them SMALL, and Y is smaller in every row. Delete X and Z.
 The game collapses to column Y = (5, 2, 4); the row player maximises -> 5 at A.
 Same answer in three lines.
```

> **The check that tells you which method to use.** maximin = minimax ⇒ saddle
> point ⇒ the solution is **pure**, and you stop. maximin < minimax ⇒ no saddle
> ⇒ you must go to mixed strategies. Doing the mixed-strategy algebra on a game
> that has a saddle point wastes ten minutes and earns nothing.

---

**D15 · Shapley value and the Core.**

**(a) All 3! = 6 orderings.** A player's marginal contribution is
`v(those already present + me) − v(those already present)`.

```
 ordering    player 1                player 2                player 3
 -------------------------------------------------------------------------------
 1,2,3    v(1)−v(∅)     = 20    v(12)−v(1)   = 40      v(123)−v(12)  = 60
 1,3,2    v(1)−v(∅)     = 20    v(123)−v(13) = 40      v(13)−v(1)    = 60
 2,1,3    v(12)−v(2)    = 30    v(2)−v(∅)    = 30      v(123)−v(12)  = 60
 2,3,1    v(123)−v(23)  = 20    v(2)−v(∅)    = 30      v(23)−v(2)    = 70
 3,1,2    v(13)−v(3)    = 40    v(123)−v(13) = 40      v(3)−v(∅)     = 40
 3,2,1    v(123)−v(23)  = 20    v(23)−v(3)   = 60      v(3)−v(∅)     = 40
 -------------------------------------------------------------------------------
 TOTAL                   150                    240                    330

   φ₁ = 150/6 = 25       φ₂ = 240/6 = 40       φ₃ = 330/6 = 55
```

**(b) Efficiency check** — free, do it every time:
`25 + 40 + 55 = 120 = v({1,2,3})` ✓

**(c) Core test** — x is in the Core iff x(C) ≥ v(C) for **every** coalition C:

```
 C        x(C)    v(C)    x(C) ≥ v(C) ?
 {1}       25      20      ✓
 {2}       40      30      ✓
 {3}       55      40      ✓
 {1,2}     65      60      ✓
 {1,3}     80      80      ✓ (tight)
 {2,3}     95     100      ✗  *** VIOLATED ***
 {1,2,3}  120     120      ✓ (efficiency)
```

**The Shapley allocation is NOT in the Core.** The **blocking coalition is
{2, 3}**: together they are paid 95 but can secure 100 on their own, so they
would walk away from player 1 and split 100 between them, each better off.

**The conceptual point the examiner wants:** Shapley answers *"what is
FAIR?"* — unique, always exists, satisfies efficiency, symmetry, dummy and
additivity. The Core answers *"what is STABLE?"* — a set, possibly large,
possibly empty. Different questions, and here they disagree. Answer both
separately and say whether they agree.

> **Two Core traps.** (1) Violations hide in the **pairs** — the singletons all
> pass comfortably here and the answer is still no. (2) In a **cost** game the
> inequality flips to `x(C) ≤ v(C)`. Read whether v is a value or a cost before
> writing a line.

---

**D16 · Auctions.**

```
 sorted bids:  C 250  >  D 240  >  A 220  >  B 180

 (a) VICKREY = second-price sealed bid.
     WINNER = C (highest bid).   C PAYS 240 (the SECOND-highest bid, D's).

 (b) SURPLUS = true value − price paid = 250 − 240 = 10.

 (c) FIRST-PRICE sealed bid: the winner pays their OWN bid.
     C would pay 250 and take a surplus of 0.
```

**Why Vickrey is truthful (dominant strategy).** Split the decision in two:
your bid decides **whether** you win; the *second-highest* bid decides **what
you pay**. Since your own bid never affects your price, changing it can only
change whether you win — bidding above your value only wins auctions where the
price exceeds your value (a loss), and bidding below it only loses auctions you
would have won profitably. So truth-telling is at least as good as any
alternative **whatever the others do**, which is exactly what *dominant* means.
Vickrey is therefore **strategy-proof** and **truth-revealing**.

**What changes under first-price.** Zero surplus at a truthful bid creates a
direct incentive to **shade** the bid below true value — but shading requires
guessing the others' bids, so the auction stops being truthful, effort shifts
from valuation to strategy, and seller revenue becomes less predictable.
*(English/ascending auctions are strategically similar to Vickrey: you drop out
at your value, so the price lands just above the second-highest valuation.)*

---

**D17 · Voting, four ways.** 15 voters: 6 `A ≫ C ≫ B`, 5 `B ≫ C ≫ A`,
4 `C ≫ B ≫ A`. Majority needs 8.

```
 (a) PLURALITY — first choices only
     A = 6 ,  B = 5 ,  C = 4          ->  WINNER: A   (no majority: 6 < 8)

 (b) BORDA — m = 3 candidates, so points are 2 / 1 / 0  (NOT 3/2/1)
     A : 6×2 + 5×0 + 4×0 = 12
     B : 6×0 + 5×2 + 4×1 = 14
     C : 6×1 + 5×1 + 4×2 = 19        ->  WINNER: C
     CHECK total = 12 + 14 + 19 = 45 = 15 voters × (0+1+2) ✓

 (c) INSTANT-RUNOFF
     Round 1 : A = 6, B = 5, C = 4 — nobody has 8. ELIMINATE C (fewest).
     Redistribute C's 4 ballots (C ≫ B ≫ A) to their next choice, B.
     Round 2 : A = 6, B = 5 + 4 = 9  ->  9 ≥ 8   ->  WINNER: B

 (d) CONDORCET — every pair, head to head
     A vs B :  A preferred by 6      ;  B preferred by 5 + 4 = 9   ->  B beats A
     A vs C :  A preferred by 6      ;  C preferred by 5 + 4 = 9   ->  C beats A
     B vs C :  B preferred by 5      ;  C preferred by 6 + 4 = 10  ->  C beats B
     C beats EVERY rival             ->  WINNER: C  (the Condorcet winner)
```

| Method | Winner |
|---|---|
| Plurality | **A** |
| Borda | **C** |
| Instant-runoff | **B** |
| Condorcet | **C** |

**Comment.** One fixed set of preferences, **three different winners**. C is
the Condorcet winner — a majority prefers C to each rival taken separately —
yet plurality elects A, who is ranked **last** by 9 of the 15 voters, purely on
the largest bloc of first-place votes (6 of 15 = 40 %). That is the **spoiler
effect**: plurality throws away everything below first place. IRV elects a
third candidate again. The general lesson is that **the voting rule, not just
the preferences, decides the outcome** — which is what **Arrow's theorem** (no
ranked rule can satisfy Non-Dictatorship, Pareto and IIA at once) and
**Gibbard–Satterthwaite** (the only strategy-proof single-winner rule is a
dictatorship) formalise.

> **The Borda trap costs marks every year.** For m candidates the points are
> m−1, m−2, …, 1, 0 — for three candidates that is **2 / 1 / 0, not 3/2/1**.
> Using 3/2/1 adds a constant to every candidate and inflates the total, and the
> marking scheme checks the total.

---

**D18 · Nash bargaining.**

```
 Total to divide       = 100
 Disagreement point d  = (30, 10)   -- what each gets if they walk away

 SURPLUS = 100 − 30 − 10 = 60
 With LINEAR utilities the Nash solution SPLITS THE SURPLUS EQUALLY:
   player 1 : 30 + 30 = 60
   player 2 : 10 + 30 = 40

 NASH BARGAINING SOLUTION = (60, 40)
```

Verification against alternatives — the Nash solution maximises the **Nash
product** `(u₁ − d₁)(u₂ − d₂)`:

```
 (60, 40) :  (60−30)(40−10) = 30 × 30 = 900    <- MAXIMUM
 (70, 30) :  (70−30)(30−10) = 40 × 20 = 800
 (50, 50) :  (50−30)(50−10) = 20 × 40 = 800
 (65, 35) :  (65−30)(35−10) = 35 × 25 = 875
```

**Answer (60, 40), Nash product 900.** Note it is **not** a 50/50 split of the
total — the disagreement point matters. Player 1 has the stronger fallback (30
vs 10) and keeps that advantage; the *surplus created by cooperating* is what
gets shared equally. Getting this the wrong way round — splitting the 100
equally instead of the 60 — is the standard error.

</details>

---

## After you have marked it

| If you dropped marks on | Go straight to |
|---|---|
| Q1 game tree / alpha–beta | `ACI-EC2-Supplement-Module3` N15–N18 · `ch06-07-minimax-alphabeta-mcts.md` |
| Q2 CNF / DPLL / resolution / FOL | `ACI-EC3-PostMidsem-Practice` P1–P5 · `ch08-09-logic-cnf-dpll-fol.md` |
| Q3 Bayesian networks | `ACI-EC3-PostMidsem-Practice` P6–P11 · `ch10-probabilistic-reasoning.md` |
| Q4 HMM / Viterbi / Forward | `ACI-EC3-PostMidsem-Practice` P12–P14 · `ch11-markov-hmm-viterbi.md` |
| Q5 search / local search | `ACI-EC2-Practice-Sheet` N1–N13 · `ch02`–`ch04` |
| Game theory / Shapley / voting | `ACI-EC3-PostMidsem-Practice` P15–P21 · `ch12`, `ch13` |

**The one page to have physically open in the exam:** `formula-sheet.md`, plus
Part B of `ACI-EC3-PostMidsem-Practice` and its trap list.

*Every numerical answer in this file was computed independently and
cross-checked. Question style, mark split and phrasing follow the Apr 2025 EC-3
Regular paper and the EC3 makeup sample in `materials/old question papers/`.*
