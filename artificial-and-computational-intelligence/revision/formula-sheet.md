# ACI — Complete Formula Sheet

Transcribed from **"ACI Quick Revision – Formulas / Notations"**, the official
appendix at the end of `materials/ACI Post midsem and formula.pdf` (pages 92–98),
which is images and does not copy-paste. Session numbers (`CS-n`) are theirs.

Where the official sheet says *"Others – Refer Slides"*, I have filled the gap
from the lecture slides and marked it **[from slides]**.

---

## CS-1 — Agents

```
Agent function       f : P*  ->  A
    P*  = percept histories        A = actions
    The agent function maps percept histories to actions.

agent = architecture + program
    Architecture -> physical system on which the agent program runs
    Program      -> implements the agent function

PEAS
    P -> Performance measure
    E -> Environment
    A -> Actuators
    S -> Sensors
```

---

## CS-2 — Problem formulation & search parameters

```
Problem formulation, 5 components:
    Initial state · Actions · Transition model RESULT(s,a) · Goal test · Path cost

Path cost           g(n) = cost of the path from the initial state to node n

Vacuum world, number of states       n × 2^n        (n = 2  ->  8)
8-puzzle, possible states            9! / 2  = 181,440
15-puzzle                            16! / 2 ≈ 1.05 × 10^13

Search complexity parameters:
    b = maximum branching factor
    d = depth of the least-cost solution
    m = maximum depth of the state space
```

---

## CS-3 — Uninformed & informed search

| # | Formula | Topic |
|---|---|---|
| 1 | `(d+1)b⁰ + d·b¹ + (d−1)b² + … + b^d = O(b^d)` | **IDS — time** |
| 2 | `O(bd)` | **IDS — space** |
| 3 | `Step cost = 1` | IDS — optimality condition |
| 4 | `f(n) = h(n)` | **Greedy Best-First Search** |
| 5 | `f(n) = g(n) + h(n)` | **A\* Search** |
| 6 | `0 ≤ h(n) ≤ h*(n)` | **Admissible heuristic** |
| 7 | `h(n) ≤ c(n, a, n′) + h(n′)` | **Consistent heuristic** |

**[from slides] — the full complexity table**

|  | BFS | UCS | DFS | DLS | IDS | Bidirectional |
|---|---|---|---|---|---|---|
| Complete? | Yes¹ | Yes² | No | No | Yes¹ | Yes¹ |
| Time | O(b^d) | O(b^(1+⌊C*/ε⌋)) | O(b^m) | O(b^l) | O(b^d) | O(b^(d/2)) |
| Space | O(b^d) | O(b^(1+⌊C*/ε⌋)) | **O(bm)** | **O(bl)** | **O(bd)** | O(b^(d/2)) |
| Optimal? | Yes³ | **Yes** | No | No | Yes³ | Yes³ |

¹ if b finite · ² if step cost ≥ ε > 0 · ³ if all step costs identical

---

## CS-4 — Heuristics & stochastic hill climbing

| # | Formula | Topic |
|---|---|---|
| 1 | `h1(n) = number of misplaced tiles` | Heuristic — 8-puzzle |
| 2 | `h2(n) = sum of Manhattan distances of tiles from their goal positions` | Heuristic — 8-puzzle |
| 3 | `h(n) = number of CONFLICTING pairs of queens` | 8-Queens fitness (**minimise**) |
| 4 | `h(n) = number of NON-CONFLICTING pairs of queens` | 8-Queens fitness (**maximise**) |
| 5 | `Probability = Frequency / Total number of observations` | **Stochastic Hill Climbing** |

**[from slides]**
```
Effective branching factor     N + 1 = 1 + b* + (b*)^2 + ... + (b*)^d
Dominance                      h2(n) ≥ h1(n), both admissible  =>  h2 is better
Combining heuristics           h(n) = max(h1(n), h2(n))   -- stays admissible
Simulated annealing            p = e^(−ΔE / T)            -- accept a worse move
Queens conflict on             same row, or |Δrow| = |Δcol|  (never columns)
Conflicting + non-conflicting  = C(n,2)   -- 6 for n=4, 28 for n=8
```

---

## CS-5 — Ant Colony Optimization

| # | Formula | Topic |
|---|---|---|
| 1 | `P^k_ij = ([τij]^α · [ηij]^β) / Σ_{l ∈ N^k_i} ([τil]^α · [ηil]^β)` | **Transition probability** |
| 2 | `ηij = 1 / dij` | **Visibility / heuristic information** |
| 3 | `Δτ^k_ij = Q / L_k` | Pheromone deposited by ant `k` |
| 4 | `τij ← (1 − ρ)·τij + Σ Δτ^k_ij` | **Pheromone update** |
| 5 | `τij ← (1 − ρ)·τij` | **Pheromone evaporation** |

### Symbols to remember

| Symbol | Meaning |
|---|---|
| `τij` | Pheromone amount on link `i, j` |
| `α` | Importance of **pheromone** |
| `β` | Importance of **route cost / visibility** |
| `dij` | Cost / distance |
| `Q` | Constant related to the pheromone trail |
| `L_k` (`f_k`) | **Route cost obtained by ant k** |
| `ρ` | **Evaporation coefficient**, `0 < ρ < 1` |
| `N` | Total number of ants, `N > 1` |
| `τ₀` | Initial pheromone amount |
| `visit_k` | Visited-nodes table of the `k`th ant |

> The denominator sums **only over unvisited nodes**. `Δτ = 0` if ant `k` did not
> use edge `(i,j)` — that edge then gets evaporation only.

**[from slides] — Genetic Algorithms**
```
Roulette wheel selection     p_i = fitness_i / Σ fitness      (must sum to 1)
7 steps:  represent -> initial population -> fitness -> selection
          -> crossover -> mutation -> repeat
Crossover strategies:  single-point · multi-point · uniform
Selection methods:     roulette wheel · tournament · rank
Stop on: threshold fitness · max generations · no change from last iteration
"No convergence rule or guarantee."
```

---

## CS-6 — Neural Architecture Search / Neuroevolution

| # | Formula | Topic |
|---|---|---|
| 1 | `Normalized value = Pixel value / 255` | Image normalization |
| 2 | `ReLU(x) = max(0, x)` | ReLU activation |
| 3 | `Accuracy = (Correct predictions / Total predictions) × 100` | Network performance |
| 4 | `Fitness = Validation Performance` | Architecture evaluation |

---

## CS-7 — Adversarial search / Minimax

```
Evaluation = Material advantage + King safety + Mobility + Board control

Score      = MAX pieces − MIN pieces

Evaluation = 2 × Soldier Advantage + 3 × Gate Damage
           + 2 × MAX Safety + 4 × Supply Control
```

---

## CS-8 — Alpha-Beta pruning & MCTS

| # | Formula | Topic |
|---|---|---|
| 1 | `α = −∞ , β = +∞` | **Alpha-Beta — initial values** |
| 2 | `If VAL ≥ α, then α = VAL` | **Alpha update** (at MAX nodes) |
| 3 | `If VAL < β, then β = VAL` | **Beta update** (at MIN nodes) |
| 4 | **`Prune when β ≤ α`** | **Alpha-Beta pruning condition** |
| 5 | `Utility = 3(MAX win chance − MIN win chance) + 2(MAX adjacent pairs − MIN adjacent pairs)` | Static evaluation |
| 6 | **`UCB = v_i + C · √( ln(N) / n_i )`** | **Monte Carlo Tree Search** |

UCB symbols: `v_i` = average value of node `i` · `n_i` = visits to node `i` ·
`N` = visits to the parent · `C` = exploration constant.

> `v_i` is **exploitation**; the square-root term is **exploration**. A node with
> few visits (`n_i` small) gets a large bonus.

---

## CS-9 — Propositional logic

### Logical equivalences — *learn all eleven*

```
(α ∧ β) ≡ (β ∧ α)                              commutativity of ∧
(α ∨ β) ≡ (β ∨ α)                              commutativity of ∨
((α ∧ β) ∧ γ) ≡ (α ∧ (β ∧ γ))                  associativity of ∧
((α ∨ β) ∨ γ) ≡ (α ∨ (β ∨ γ))                  associativity of ∨
¬(¬α) ≡ α                                      double-negation elimination
(α ⇒ β) ≡ (¬β ⇒ ¬α)                            contraposition
(α ⇒ β) ≡ (¬α ∨ β)                             IMPLICATION ELIMINATION
(α ⇔ β) ≡ ((α ⇒ β) ∧ (β ⇒ α))                  biconditional elimination
¬(α ∧ β) ≡ (¬α ∨ ¬β)                           De Morgan
¬(α ∨ β) ≡ (¬α ∧ ¬β)                           De Morgan
(α ∧ (β ∨ γ)) ≡ ((α ∧ β) ∨ (α ∧ γ))            distributivity of ∧ over ∨
(α ∨ (β ∧ γ)) ≡ ((α ∨ β) ∧ (α ∨ γ))            distributivity of ∨ over ∧
```

| Formula | Topic |
|---|---|
| `2ⁿ` | **Number of models** (n symbols) |
| `O(2ⁿ)` | Time complexity (truth-table entailment) |
| `O(n)` | Space complexity |
| `p ∧ q` | AND |
| `p ∨ q` | OR |
| `¬p` | NOT |
| `p → q` | Implication |
| `p ↔ q` | Biconditional |
| `p ↔ q ≡ (p → q) ∧ (q → p)` | Biconditional equivalence |

---

## CS-10 — First-Order Logic

| # | Formula | Topic |
|---|---|---|
| 1 | `∀v α  ⇒  Subst({v/g}, α)` | **Universal Instantiation (UI)** |
| 2 | `∃v α  ⇒  Subst({v/k}, α)` | **Existential Instantiation (EI)** |
| 3 | `∀x man(x) → drink(x, coffee)` | Universal quantifier example |
| 4 | `∃x : boys(x) ∧ intelligent(x)` | Existential quantifier example |
| 5 | `∃x, c, s Teaching(X, C, S)` | Predicate logic example |
| 6 | `∀p Sells(S, P, C)` | Universal quantification example |

- **UI:** `g` is a **ground term**.
- **EI:** `k` is a **new constant symbol (a Skolem constant)** that does not
  appear elsewhere in the knowledge base.

> **The pattern to memorise:** `∀` goes with **`→`** (implication);
> `∃` goes with **`∧`** (conjunction). Swapping them is the classic FOL error.

---

## CS-11 & 12 — Probability & Bayesian Networks

```
Disjunction      P(A ∨ B) = P(A) + P(B) − P(A ∧ B)

Conditional      P(A | B) = P(A ∧ B) / P(B)
                 "Assumes that B is the only info known."

Chain / Product rule
    P(X1, ..., Xn) = P(Xn | X1..X(n−1)) · P(X(n−1) | X1..X(n−2)) · ... · P(X1)
                   = Π P(Xi | X1 ... X(i−1))

Independence     A and B are independent iff
                     P(A | B) = P(A)
                     P(B | A) = P(B)
                 (these two constraints are logically equivalent)
                 Therefore, if independent:  P(A ∧ B) = P(A)·P(B)

Bayes Rule       P(A | B) = ( P(B | A) · P(A) ) / P(B)
    A, B          = events
    P(A|B)        = probability of A given B is true
    P(B|A)        = probability of B given A is true
    P(A), P(B)    = the independent probabilities of A and B
```

**[from slides] — Bayesian networks**
```
BN chain rule           P(x1,...,xn) = Π P( xi | Parents(Xi) )
Conditional query       P(X | e) = α · P(X, e),  α = 1 / Σ_x P(X=x, e)
                        -> sum out hidden variables, then NORMALISE
Enumeration complexity  O(d^n)      d = max arity, n = number of variables
Markov blanket          parents + children + children's other parents

D-separation (blocked when...):
    CHAIN     X → M → Y     blocked  <=>  M observed
    FORK      X ← M → Y     blocked  <=>  M observed
    COLLIDER  X → M ← Y     blocked  <=>  M NOT observed and no descendant observed

Likelihood weighting    w = Π P(e | Parents(e))   over EVIDENCE nodes only
                        P(q|e) = (Σ w where q holds) / (Σ all w)
```

---

## CS-13 — Markov models & HMM  *(not on the official sheet)*

```
Markov assumption       P(St | S1..S(t−1)) = P(St | S(t−1))

Forward algorithm       α_t(j) = [ Σ_i α_(t−1)(i) · a_ij ] · b_j(o_t)
Viterbi                 v_t(j) = max_i [ v_(t−1)(i) · a_ij ] · b_j(o_t)
                        -- SAME recursion, SUM replaced by MAX, plus backpointers
```

---

## CS-14 & 15 — Game theory  *(not on the official sheet)*

### Non-cooperative (Ch 12)

```
Maximin (row player)    maximin = max_i ( min_j u(i,j) )     your guarantee
Minimax (col player)    minimax = min_j ( max_i u(i,j) )
                        maximin = minimax -> SADDLE POINT, pure strategy
                        maximin < minimax -> no pure solution, go MIXED

Nash equilibrium        no player can improve by unilaterally changing strategy
Mixed strategy          make the opponent INDIFFERENT between their pure strategies

2x2 mixed strategy      Row plays R1 with prob p:
                            vs C1:  E1(p) = a·p + c·(1−p)
                            vs C2:  E2(p) = b·p + d·(1−p)
                        SET E1(p) = E2(p) AND SOLVE.  That crossing point is
                        the maximin mixed strategy; V is the common value.

Morra (slide example)   lines 5p − 3 and 4 − 7p  ->  p = 7/12,  V = −1/12
                        (deck typo: the leaf is −3p + 4(1−p), NOT 3p + 4(1−p))

SPNE                    Nash equilibrium in EVERY subgame; found by backward
                        induction; REMOVES NON-CREDIBLE THREATS.
                        At each node read THAT player's own entry in the tuple.
```

### Cooperative (Ch 13)

```
Characteristic fn       v(C) = what coalition C secures ALONE.  v(∅) = 0
Superadditivity         v(C ∪ D) ≥ v(C) + v(D)  ->  grand coalition is best

Imputation              Efficiency  Σ x_i = v(N)
                        Individual rationality  x_i ≥ v({i})

THE CORE  (stability)   x(C) ≥ v(C)  for EVERY coalition C
   ⚠ COST GAME          x(C) ≤ v(C)   -- the inequality FLIPS
   check the PAIRS      violations hide in 2-player subsets, not singletons

SHAPLEY  (fairness)     mc_i(C) = v(C ∪ {i}) − v(C)
                        φ_i = average marginal contribution over all n! orderings

                                     |C|! (n − |C| − 1)!
                        φ_i =  Σ     -------------------- [ v(C∪{i}) − v(C) ]
                            C ⊆ N\{i}         n!

   n = 3 weights        1/3  (arrive 1st) · 1/6 · 1/6 (2nd) · 1/3 (3rd)
   Four axioms          Efficiency · Dummy Player · Symmetry · Additivity
   FREE CHECK           Σ φ_i must equal v(N)
   FREE SHORTCUT        symmetric players get identical payoffs — stop computing

   worked answers       taxi 6/12/42, cost = max  ->  φ = (2, 5, 35)
                        board 45/45/10, majority  ->  φ = (33.3, 33.3, 33.3)

Mechanism design        3 pillars: Strategy Language · Center · Outcome Rule
                        Strategy-proof = you have a dominant strategy
                        Truth-revealing = that dominant strategy is HONESTY (stricter)
                        Revelation Principle: any mechanism -> an equivalent
                        truth-revealing one

Contract Net            Recognise -> Announce -> Bid -> Award

AUCTIONS
   English (ascending)  bid while price < v_i ;  final price = b_o + d
   First-price sealed   pay YOUR OWN bid  ->  NOT truthful, agents shade b_i < v_i
   Vickrey (2nd price)  pay the SECOND-highest bid  ->  TRUTHFUL, dominant strategy
                        your bid decides IF you win; the 2nd bid decides WHAT YOU PAY
   VCG                  generalises Vickrey to combinatorial goods

BARGAINING
   Nash Product         arg max  (u1 − d1)(u2 − d2)      d = disagreement point
   linear frontier      SPLIT THE SURPLUS EQUALLY, not the total:
                            surplus = total − (d1 + d2) ;  each gets d_i + surplus/2
   4 Nash axioms        Pareto Efficiency · Symmetry · Invariance to Affine
                        Transformations · IIA
   Rubinstein           alternating offers, discount δ ∈ (0,1); settles in round 1;
                        first-mover advantage vanishes as δ -> 1

VOTING
   Plurality            top choice only  ->  spoiler effect
   Borda                m alternatives: points m−1, m−2, …, 0
                        ⚠ for 3 candidates that is 2 / 1 / 0, NOT 3/2/1
                        check: total points = voters × (0+1+…+(m−1))
   Instant-Runoff       drop the lowest first-place count, redistribute, repeat
   Condorcet winner     beats every rival head-to-head; may NOT EXIST
   Condorcet paradox    A ≻ B ≻ C ≻ A  ->  cycle  ->  agenda manipulation
   Arrow                no ranked system gives a stable group RANKING
                        (Non-Dictatorship · Pareto · IIA)
   Gibbard-Satterthwaite  the only strategy-proof SINGLE-WINNER rule is a DICTATORSHIP
```

---

## How to use this sheet in the last hour

1. **CS-3, CS-4, CS-5, CS-8, CS-11&12** are the ones with real numericals
   attached. If you can reproduce those five blocks from memory, you can attempt
   every calculation question on the paper.
2. **Three checks that catch most arithmetic errors, free:**
   - probabilities **sum to 1**
   - conflicting + non-conflicting queen pairs **= C(n,2)**
   - a single-variable Bayesian factor **sums to 1**
3. **Three sign/direction traps that cost whole questions:**
   - `η = 1/d`, **not** `d` (ACO)
   - complement `P(¬X|…) = 1 − P(X|…)` (Bayesian nets)
   - conflicting vs non-conflicting pairs — **read which one is asked**
