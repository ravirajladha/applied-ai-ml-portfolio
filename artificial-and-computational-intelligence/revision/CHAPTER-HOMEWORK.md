# ACI — Chapter Homework from the Slide Decks, Solved

Every slide in `materials/ACI Pre midsem.pdf` and
`materials/ACI Post midsem and formula.pdf` that is titled **Exercise**,
**Exercises**, **Try it & Test** or is otherwise set as homework, with the
question **as printed** and a full worked solution.

Each solution is hidden behind a **Show solution** toggle in the HTML, and
starts on its own block in the PDF. **Attempt first.**

## Index

| # | Deck | PDF p. | Slide | Topic | Chapter |
|---|---|---|---|---|---|
| **HW1** | Pre-midsem | 29 | 50 | Exercise 1 — problem formulation ×3 | 2 |
| **HW2** | Pre-midsem | 29 | 51 | Exercise 2 — **A\*** on a graph | 3 |
| **HW3** | Post-midsem | 19 | 22 | Exercises — **FOL** translation ×5 | 9 |
| **HW4** | Post-midsem | 22 | 35 | Exercise — *"Did Curiosity kill the cat?"* **resolution** | 9 |
| **HW5** | Post-midsem | 35 | 49 | Exercise — **Alarm network**, P(JohnCalls \| Earthquake) | 10 |
| **HW6** | Post-midsem | 35 | 52 | Try it & Test — **D-separation** ×4 | 10 |
| **HW7** | Post-midsem | 40 | 70 | Exercise Problems — Viral / Flu / Fever network | 10 |
| **HW8** | Post-midsem | 40 | 71 | Exercise Problem 2 — **WILP cricket network** | 10 |
| **HW9** | Post-midsem | 52 | 45 | Explain HMM & Viterbi — **student concentration** | 11 |

> **HW8 is the one to do first.** Its query is *the same shape* as Q3(c) of the
> Apr 2025 real paper, and both come out to `0.5⁶ = 0.015625`. The examiner
> reused the deck's own exercise. **HW5** and **HW9** are the next most
> valuable — Ch 10 + Ch 11 are ~46 % of the marks.

---

## HW1 · Exercise 1 — Problem formulation *(Pre-midsem, slide 50)*

> For the below tasks:
> 1. Planning a trip with a delivery drone
> 2. Solving a maze
> 3. Scheduling patient appointments in a clinic
>
> **Formulate the problem** by specifying: Initial state · Possible actions ·
> Transition model (effects of actions) · Goal test · Path cost (optional).
>
> Think about: any **missing components**; assess **well-formulated-ness**
> (does it meet the criteria for a well-formed problem?).

<details><summary><b>Show solution — HW1</b></summary>

A problem is **well-formulated** when all five components are stated
unambiguously and the state space they define is *closed*: every action maps a
legal state to a legal state, and the goal test is decidable on any state.

**1 · Delivery drone trip**

```
 Initial state    Drone at depot D0, battery = 100 %, carrying parcel P,
                  weather = current forecast.
 Actions          FlyTo(waypoint) · Ascend(h) · Descend(h) · Hover(t) ·
                  Recharge(station) · Release(parcel)
 Transition model FlyTo(w): position ← w, battery ← battery − energy(distance,
                  wind, payload). Release: carrying ← none, only if at the
                  delivery address and altitude = 0.
 Goal test        Parcel released at the customer address AND drone has enough
                  battery to reach a landing site.
 Path cost        Energy consumed (or flight time), plus a penalty for
                  no-fly-zone proximity.
```

**Missing components in the question:** no-fly zones and airspace constraints ·
battery as a *hard* constraint (a state with battery = 0 in mid-air is not a
legal state) · wind as a stochastic factor. **Assessment:** as literally
stated this is **not** well formulated — it is **non-deterministic** (wind,
battery drain) and **partially observable** (forecast, not actual weather). To
make it a classical search problem you must assume deterministic energy use and
a fully known map, and *state that assumption*.

**2 · Solving a maze**

```
 Initial state    Agent at the entry cell (r0, c0).
 Actions          Up · Down · Left · Right
 Transition model Move to the adjacent cell if it is not a wall and is inside
                  the grid; otherwise the state is unchanged.
 Goal test        Agent is at the exit cell.
 Path cost        1 per move (uniform step cost).
```

**Assessment: well formulated.** Discrete, deterministic, fully observable,
static, single-agent — the textbook case. Because step costs are uniform, BFS
is optimal here and UCS gives no benefit.

**3 · Scheduling patient appointments**

```
 Initial state    Empty diary; a set of N patient requests, each with a
                  duration, a preferred window and a required doctor.
 Actions          Assign(patient, doctor, slot) · Unassign(patient)
 Transition model Assign places the patient in that slot if the doctor is free
                  for the whole duration and the slot is inside the clinic's
                  hours; otherwise the action is not applicable.
 Goal test        Every patient is assigned, and no constraint is violated.
 Path cost        Total patient waiting time + overtime + preference violations.
```

**Missing components:** no-show probability, emergency arrivals, doctor breaks.
**Assessment:** this is really a **constraint-satisfaction / optimisation**
problem rather than a path-finding one — the *path* to the schedule is
irrelevant, only the final assignment matters. Say so: it is well formulated as
a CSP, and local search (hill climbing, simulated annealing) suits it better
than BFS/A\*.

> **The generalisable answer.** For any "formulate this problem" question,
> write the five headings first, fill them, then add two lines: **what is
> missing** and **which search family fits** (path-finding → BFS/UCS/A\*;
> final-state-only → local search / CSP). Those two lines are usually where the
> marks beyond the bare list are.

</details>

---

## HW2 · Exercise 2 — A\* on a graph *(Pre-midsem, slide 51)*

> Apply the **A\*** algorithm on the graph below, given the heuristics
> `h(S)=5, h(A)=3, h(B)=4, h(C)=2, h(D)=6, h(G)=0`.

```
              A ---2--- B
            /   \         \
           1     1         5
          /       \         \
        (S)        C ---3--- D
          \       /  \        \
           \     4    \        2
            \   /      \        \
             \ /        `------ (G)
              `-----10-----------'

   edges:  S–A = 1   A–B = 2   A–C = 1   B–D = 5
           C–D = 3   C–G = 4   D–G = 2   S–G = 10
```

<details><summary><b>Show solution — HW2</b></summary>

**The A\* trace.** `f(n) = g(n) + h(n)`. Expand the frontier node with the
smallest f; ties alphabetically.

```
 f(S) = 0 + 5 = 5            EXPAND S
   A : g = 1 ,  f = 1 + 3 = 4
   G : g = 10,  f = 10 + 0 = 10
   frontier: A(4), G(10)

 EXPAND A  (f = 4)
   B : g = 1+2 = 3 ,  f = 3 + 4 = 7
   C : g = 1+1 = 2 ,  f = 2 + 2 = 4
   frontier: C(4), B(7), G(10)

 EXPAND C  (f = 4)
   D : g = 2+3 = 5 ,  f = 5 + 6 = 11
   G : g = 2+4 = 6 ,  f = 6 + 0 = 6      BETTER than the earlier G(10) — replace
   frontier: G(6), B(7), D(11)

 EXPAND G  (f = 6)  ->  GOAL
```

**Expansion order: S → A → C → G. Solution path S → A → C → G, cost 6.**

Verify it is optimal by listing every S–G path:

```
 S-A-C-G     = 1 + 1 + 4     =  6    <- returned by A*, and it is the cheapest
 S-A-C-D-G   = 1 + 1 + 3 + 2 =  7
 S-A-B-D-G   = 1 + 2 + 5 + 2 = 10
 S-G         =                  10
```

Note A\* expanded only **4 of the 6 nodes**. B and D were generated but never
expanded — their f-values (7 and 11) never became the smallest. That is the
heuristic doing its job: compare with UCS on the same graph, which would have
expanded D as well.

### ⚠ The heuristic in this exercise is **not admissible** — flag it

This is worth knowing, because it is exactly the *"admissible but not
consistent"* question the exam asks, in reverse.

```
 True remaining costs h*(n):
   h*(G) = 0
   h*(D) = 2                       (D → G)
   h*(C) = min(4, 3 + 2) = 4       (C → G directly, or via D)
   h*(B) = 5 + 2 = 7               (B → D → G)
   h*(A) = min(1 + 4, 2 + 7) = 5   (A → C → G)
   h*(S) = min(1 + 5, 10) = 6      (S → A → …)

 ADMISSIBILITY  h(n) ≤ h*(n) ?
   S : 5 ≤ 6 ✓      A : 3 ≤ 5 ✓      B : 4 ≤ 7 ✓
   C : 2 ≤ 4 ✓      D : 6 ≤ 2 ✗  *** VIOLATED — h(D) OVERESTIMATES by 4 ***
   G : 0 ≤ 0 ✓
```

```
 CONSISTENCY   h(n) ≤ c(n, n′) + h(n′) on every edge ?
   S→A : 5 ≤ 1 + 3 = 4   ✗  VIOLATED
   D→G : 6 ≤ 2 + 0 = 2   ✗  VIOLATED
   A→B : 3 ≤ 2 + 4 = 6   ✓      A→C : 3 ≤ 1 + 2 = 3  ✓ (tight)
   B→D : 4 ≤ 5 + 6 = 11  ✓      C→D : 2 ≤ 3 + 6 = 9  ✓
   C→G : 2 ≤ 4 + 0 = 4   ✓      S→G : 5 ≤ 10 + 0 = 10 ✓
```

**So h is neither admissible nor consistent.** A\* still returned the optimal
path here **by luck** — the one overestimating node, D, does not lie on the
optimal path, so the overestimate never suppressed the right answer. Had D been
on the cheapest route, h(D) = 6 would have pushed it down the queue and A\*
could have returned a sub-optimal path.

**Write this in your answer.** "A\* returns S–A–C–G with cost 6. Note h is not
admissible — h(D) = 6 > h\*(D) = 2 — so optimality is not guaranteed in
general; it holds here only because D is off the optimal path." That
observation is worth more than the trace, because it shows you know *why* the
admissibility condition exists rather than just how to run the algorithm.

</details>

---

## HW3 · Exercises — FOL translation *(Post-midsem, slide 22)*

> Convert the following into **FOL** using quantifiers:
> 1. All birds fly.
> 2. Every man respects his parent.
> 3. Some boys play cricket.
> 4. Not all students like both Mathematics and Science.
> 5. Only one student failed in Mathematics.

<details><summary><b>Show solution — HW3</b></summary>

**Declare the predicates first** — it earns marks and prevents ambiguity:
`Bird(x)`, `Fly(x)`, `Man(x)`, `Parent(y, x)` ("y is a parent of x"),
`Respects(x, y)`, `Boy(x)`, `Plays(x, g)`, `Student(x)`, `Likes(x, s)`,
`Failed(x, s)`.

```
 1. All birds fly.
      ∀x ( Bird(x) → Fly(x) )

 2. Every man respects his parent.
      ∀x ( Man(x) → ∀y ( Parent(y, x) → Respects(x, y) ) )
    (Reading "his parent" as "each of his parents". If the intended reading is
     "at least one parent", it is ∀x (Man(x) → ∃y (Parent(y,x) ∧ Respects(x,y))).
     STATE which reading you took — the ambiguity is in the English, not in you.)

 3. Some boys play cricket.
      ∃x ( Boy(x) ∧ Plays(x, Cricket) )

 4. Not all students like both Mathematics and Science.
      ¬ ∀x ( Student(x) → ( Likes(x, Maths) ∧ Likes(x, Science) ) )
    Push the negation in (quantifier duality, then De Morgan):
      ≡ ∃x ( Student(x) ∧ ¬( Likes(x, Maths) ∧ Likes(x, Science) ) )
      ≡ ∃x ( Student(x) ∧ ( ¬Likes(x, Maths) ∨ ¬Likes(x, Science) ) )

 5. Only one student failed in Mathematics.
      ∃x ( Student(x) ∧ Failed(x, Maths)
           ∧ ∀y ( ( Student(y) ∧ Failed(y, Maths) ) → y = x ) )
    In words: at least one did (the ∃ part) and any that did IS that one
    (the ∀ part). "Exactly one" ALWAYS needs both halves.
```

> **The pattern that decides these marks.** `∀` goes with `→`. `∃` goes with
> `∧`. `∀x (Bird(x) ∧ Fly(x))` asserts that *everything in the universe* is a
> flying bird. `∃x (Boy(x) → Plays(x, Cricket))` is satisfied vacuously by
> anything that is not a boy. Both are the standard way to lose the mark.
>
> **Quantifier duality**, which drives (4): `¬∀x P ≡ ∃x ¬P` and
> `¬∃x P ≡ ∀x ¬P`.

</details>

---

## HW4 · Exercise — Did Curiosity kill the cat? *(Post-midsem, slide 35)*

> Jack owns a dog. Every dog owner is an animal lover. No animal lover kills an
> animal. Either Jack or Curiosity killed the cat, who is named Tuna. **Did
> Curiosity kill the cat?**
>
> These can be represented as follows:
>
> ```
> A. (∃x) Dog(x) ∧ Owns(Jack, x)
> B. (∀x) ( ((∃y) Dog(y) ∧ Owns(x, y)) ⇒ AnimalLover(x) )
> C. (∀x) ( AnimalLover(x) ∧ (∀y) Animal(y) ⇒ ¬Kills(x, y) )
> D. Kills(Jack, Tuna) ∨ Kills(Curiosity, Tuna)
> E. Cat(Tuna)
> F. (∀x) ( Cat(x) ⇒ Animal(x) )
> Q. Kills(Curiosity, Tuna)
> ```

<details><summary><b>Show solution — HW4</b></summary>

**STEP 1 — Convert the KB to CNF.**

The only interesting step is A: it is existentially quantified, so
**Existential Instantiation** replaces `x` with a **brand-new Skolem constant**
— call it `D0` (the dog). Use it once and never again.

```
 A1 : Dog(D0)
 A2 : Owns(Jack, D0)
 B  : ¬Dog(y) ∨ ¬Owns(x, y) ∨ AnimalLover(x)
 C  : ¬AnimalLover(x) ∨ ¬Animal(y) ∨ ¬Kills(x, y)
 D  : Kills(Jack, Tuna) ∨ Kills(Curiosity, Tuna)
 E  : Cat(Tuna)
 F  : ¬Cat(x) ∨ Animal(x)
```

**STEP 2 — Negate the goal.** *Write this line first; it is the whole method.*

```
 ¬Q : ¬Kills(Curiosity, Tuna)
```

**STEP 3 — Resolve.**

```
 R1 :  ¬Q  { ¬Kills(Curiosity, Tuna) }
       D   { Kills(Jack, Tuna), Kills(Curiosity, Tuna) }
    -> { Kills(Jack, Tuna) }                                          [C1]

 R2 :  C   { ¬AnimalLover(x), ¬Animal(y), ¬Kills(x, y) }
       C1  { Kills(Jack, Tuna) }         unifier { x/Jack , y/Tuna }
    -> { ¬AnimalLover(Jack), ¬Animal(Tuna) }                          [C2]

 R3 :  B   { ¬Dog(y), ¬Owns(x, y), AnimalLover(x) }
       A1  { Dog(D0) }                   unifier { y/D0 }
    -> { ¬Owns(x, D0), AnimalLover(x) }                               [C3]

 R4 :  C3  { ¬Owns(x, D0), AnimalLover(x) }
       A2  { Owns(Jack, D0) }            unifier { x/Jack }
    -> { AnimalLover(Jack) }                                          [C4]

 R5 :  C2  { ¬AnimalLover(Jack), ¬Animal(Tuna) }
       C4  { AnimalLover(Jack) }
    -> { ¬Animal(Tuna) }                                              [C5]

 R6 :  F   { ¬Cat(x), Animal(x) }
       E   { Cat(Tuna) }                 unifier { x/Tuna }
    -> { Animal(Tuna) }                                               [C6]

 R7 :  C5  { ¬Animal(Tuna) }
       C6  { Animal(Tuna) }
    -> { }        *** THE EMPTY CLAUSE ***
```

**STEP 4 — Conclude.** `KB ∧ ¬Q` is unsatisfiable, therefore
`KB ⊨ Kills(Curiosity, Tuna)`.

**Yes — Curiosity killed the cat.**

**The argument in English**, which is what the "explain" marks are for: Jack
owns a dog, so Jack is an animal lover; animal lovers do not kill animals; Tuna
is a cat and therefore an animal; so Jack did not kill Tuna. Since one of the
two did, it must have been Curiosity.

> **Three traps in this one question.**
> 1. **Add ¬Q, not Q.** Resolution is refutation. Adding the goal itself proves
>    nothing.
> 2. **Existential Instantiation needs a NEW constant.** Writing
>    `Dog(Rex)` where Rex already appears in the KB is wrong, and reusing the
>    Skolem constant for a second `∃` is wrong too.
> 3. **Standardise apart** before unifying. B and C both use `x` and `y`; they
>    are different variables and must be renamed, or you will produce
>    unifications that do not exist.

</details>

---

## HW5 · Exercise — Alarm network *(Post-midsem, slide 49)*

> **What is the probability that John calls given earthquake occurred?**

```
        Burglary  P(B) = .001          Earthquake  P(E) = .002
              \                        /
               v                      v
                     (  Alarm  )              B   E   P(A)
                     /         \              t   t   .95
                    v           v             t   f   .94
             JohnCalls      MaryCalls         f   t   .29
                                              f   f   .001
      A  P(J)                A  P(M)
      t  .90                 t  .70
      f  .05                 f  .01
```

<details><summary><b>Show solution — HW5</b></summary>

**STEP 1 — Identify the pieces** *(always write this line — the Apr 2025
scheme pays 0.5 marks for it before any arithmetic)*

```
 Query X   = J (JohnCalls)
 Evidence e = { E = true }
 Hidden Y  = { B, A }
 MaryCalls is a LEAF that is neither query nor evidence  ->  IRRELEVANT, prune it.
```

Saying that M is irrelevant is itself worth a mark, and it halves the work.

**STEP 2 — Symbolic expansion**

```
 P(J | E) = Σ over b, a of  P(b) · P(a | b, E) · P(J | a)
```

*No normalisation constant is needed here:* E is a root with no parents, so
conditioning on it does not change the priors of B, and the CPTs already give
the conditional directly. (If in doubt, compute `P(J, E)` and divide by
`P(E) = 0.002` — you get the same number.)

**STEP 3 — Evaluate, splitting on B**

```
 CASE B = true   (prior 0.001)
   A = true  : P(A | B, E) = 0.95   ->  0.95 × P(J|A)  = 0.95 × 0.90 = 0.8550
   A = false : P(¬A| B, E) = 0.05   ->  0.05 × P(J|¬A) = 0.05 × 0.05 = 0.0025
                                                          sub-total  = 0.8575

 CASE B = false  (prior 0.999)
   A = true  : P(A | ¬B, E) = 0.29  ->  0.29 × 0.90 = 0.2610
   A = false : P(¬A| ¬B, E) = 0.71  ->  0.71 × 0.05 = 0.0355
                                                       sub-total  = 0.2965
```

**STEP 4 — Combine**

```
 P(J | E) = 0.001 × 0.8575  +  0.999 × 0.2965
          = 0.0008575       +  0.2962035
          = 0.2970610
```

**Answer: P(JohnCalls | Earthquake) ≈ 0.2971, about 29.7 %.**

**The sanity check worth quoting.** The *prior* P(J) on this network is only
**0.0521** (about 5 %). Knowing an earthquake occurred raises John's chance of
calling roughly **six-fold** — but it is still under 30 %, because even given an
earthquake the alarm only fires 29 % of the time (P(A | ¬B, E) = 0.29), and
burglary is so rare (0.001) that it contributes almost nothing to the total.
Reading the answer back like that is the difference between "a number" and
"vague answers will not be awarded marks".

</details>

---

## HW6 · Try it & Test — D-separation *(Post-midsem, slide 52)*

> ```
>    Festival (F)              Weather @ Delhi (D)
>        |                            |
>        v                            v
>    Road block (R)               weekend (W)
>        \                        /        \
>         v                      v          v
>          `----> Cars routed (C)      All Bars are full (B)
>                      |
>                      v
>            Late for BGLR airport (L)
> ```
>
> | X | Y | Evidence Z | d-sep? |
> |---|---|---|---|
> | F | W | C | ? |
> | L | W | R | ? |
> | R | L | C | ? |
> | B | R | C | ? |

<details><summary><b>Show solution — HW6</b></summary>

**Edges used:** `F → R`, `D → W`, `R → C`, `W → C`, `W → B`, `C → L`.
*(Weather @ Delhi plays no part in any of the four queries.)*

**The three blocking rules.** A path is **blocked** at node M when:

```
 CHAIN     X → M → Y      blocked  <=>  M IS observed
 FORK      X ← M → Y      blocked  <=>  M IS observed
 COLLIDER  X → M ← Y      blocked  <=>  M is NOT observed
                                        AND no descendant of M is observed
```

X and Y are d-separated given Z **only if every path between them is blocked**.
One open path is enough to make them d-connected.

---

**Row 1 — F ⊥ W | C ?**

```
 Path:  F → R → C ← W
   at R : CHAIN,    R is NOT observed  ->  OPEN
   at C : COLLIDER, C IS observed      ->  OPEN   (the collider rule is backwards!)
 -> the path is OPEN  ->  NOT d-separated.        ANSWER: No ✓
```

Intuition: once you know the cars *were* re-routed, the two possible causes
compete. Learning there was a festival explains the re-routing and makes the
weekend less necessary as an explanation. **Explaining away.**

---

**Row 2 — L ⊥ W | R ?**

```
 Path:  W → C → L
   at C : CHAIN, C is NOT observed  ->  OPEN
 -> OPEN  ->  NOT d-separated.                    ANSWER: No ✓
```

Observing R does not help — R is not on this path at all. A weekend still
raises the chance of re-routing, which still raises the chance of being late.

---

**Row 3 — R ⊥ L | C ?**

```
 Every path from R to L must pass through C:
 Path:  R → C → L
   at C : CHAIN, C IS observed  ->  BLOCKED
 (No other route exists: R's only child is C, and L's only parent is C.)
 -> ALL paths blocked  ->  D-SEPARATED.           ANSWER: Yes ✓
```

This is the deck's own stated conclusion: `P(R | L, C) = P(R | C)` — R and L are
conditionally independent given C. Once you know whether the cars were
re-routed, knowing you were late adds nothing about the road block.

---

**Row 4 — B ⊥ R | C ?**

```
 Path:  B ← W → C ← R
   at W : FORK,     W is NOT observed  ->  OPEN
   at C : COLLIDER, C IS observed      ->  OPEN
 -> OPEN  ->  NOT d-separated.                    ANSWER: No ✓
```

Two reasons stacked: the common cause W is unobserved, *and* the collider C is
observed. Either alone would open the path.

---

| X | Y | Evidence Z | d-separated? | Why |
|---|---|---|---|---|
| F | W | C | **No** | collider at C is **opened** by observing C |
| L | W | R | **No** | chain through C, and C is unobserved |
| R | L | C | **Yes** | the only path is a chain through C, and C is observed |
| B | R | C | **No** | fork at W unobserved **and** collider at C observed |

> **The single idea this table is testing:** the collider rule runs
> **backwards** from chain and fork. Chains and forks are blocked **by**
> observation; a collider is **opened by** it — and by observing any
> **descendant** of it. Three of the four rows here turn on exactly that.

</details>

---

## HW7 · Exercise Problems — Viral / Flu / Fever *(Post-midsem, slide 70)*

> Consider the below Bayesian network and answer the following questions:
>
> **Exact Inference:** What is the chance that a person **doesn't get fever**
> given the evidence that his/her blood test results show **viral infection**
> and **severe dehydration**?
>
> **Approximate inference** — Prior Sampling, Rejection sampling, Likelihood
> weighting, using the random numbers
> *"0.3, 0.6, 0.2, 0.1, 0.7, 0.5, 0.5, 0.25, 0.45, 0.85, 0.35, 0.9, 0.15,
> 0.65, 0.51, 0.2, 0.7, 0.10, 0.6, 0.8"*.

<details><summary><b>Show solution — HW7</b></summary>

> ### ⚠ Read this before you attempt it
> On the printed slide, **the CPTs for Fever and for DeHydration are all
> `0.25`** — every row of both tables. Those are placeholder values, not real
> ones. Taken literally the question is degenerate: Fever would be independent
> of its own parents, so the answer would simply be
> `P(¬Fever) = 0.75` regardless of any evidence.
>
> The **properly specified** version of this same network is the one on the
> previous slide (Likelihood Weighting, slide 69), and it is also the network in
> `EC3_SolvedSamples.pdf`. Solve that one — it is the version that reaches the
> exam. **Check the CPT numbers below against your own copy of the deck
> before you rely on them.**

**Network and CPTs (slide 69 version)**

```
              (Viral V)          (fooDPoison D)
                  |                 |
                  v                 |
              (fLu L)               |
                   \                /
                    v              v
                       ( Fever F )

 P(V) = 0.6                        P(D) = 0.1

 V | P(L | V)                      L  D | P(F | L, D)
 T |   0.80                        T  T |   0.99
 F |   0.01                        T  F |   0.80
                                   F  T |   0.80
                                   F  F |   0.05
```

**Exact inference — P(¬F | V = T, D = T)**

```
 STEP 1 — pieces
   Query X = F      Evidence e = { V = T, D = T }      Hidden Y = { L }

 STEP 2 — symbolic form.  V and D are given, so only L must be summed out:
   P(¬F | V=T, D=T) = Σ over l of  P(l | V=T) · P(¬F | l, D=T)

 STEP 3 — evaluate
   l = L=T :  P(L=T | V=T) = 0.80  ,  P(¬F | L=T, D=T) = 1 − 0.99 = 0.01
              contribution = 0.80 × 0.01 = 0.008
   l = L=F :  P(L=F | V=T) = 0.20  ,  P(¬F | L=F, D=T) = 1 − 0.80 = 0.20
              contribution = 0.20 × 0.20 = 0.040
                                                        -----
   P(¬F | V=T, D=T)                                   =  0.048
```

**Answer: 0.048, about 4.8 %** — so P(Fever | Viral, Dehydration) = 0.952. With
both a viral infection and dehydration present, fever is nearly certain, which
is exactly what the CPT's 0.99 / 0.80 rows are saying.

*(No normalisation was needed: V and D are roots and are both observed, so the
expression is already a conditional. If you compute it as `α · P(¬F, V, D)`
instead, you will get the same 0.048 after dividing by `P(V=T)·P(D=T)`.)*

**Approximate inference — how to use the random-number list**

You will not be asked to run twenty samples by hand; you will be asked for
**one or two samples and the method**. State the procedure and do one of each:

```
 PRIOR SAMPLING
   Sample every variable in TOPOLOGICAL ORDER: V, D, L, F  (parents before children).
   For each, compare the next random number r to the CPT entry: assign TRUE if
   r < P(node = T | parents already sampled), else FALSE.
   e.g. r = 0.3 < P(V) = 0.6  ->  V = T
        r = 0.6 > P(D) = 0.1  ->  D = F
        r = 0.2 < P(L|V=T) = 0.8 -> L = T
        r = 0.1 < P(F|L=T,D=F) = 0.8 -> F = T      sample = (T, F, T, T)
   Estimate P(q | e) = (count of samples with q AND e) / (count with e).

 REJECTION SAMPLING
   Do prior sampling, then THROW AWAY every sample inconsistent with the
   evidence V = T, D = T. Here P(V=T, D=T) = 0.6 × 0.1 = 0.06, so about
   94 % of the samples are discarded — that is the weakness of the method,
   and it gets worse the rarer the evidence is.

 LIKELIHOOD WEIGHTING
   FIX the evidence (V = T, D = T), sample only the non-evidence nodes
   (L, then F), and weight each sample by the evidence nodes only:
       w = Π over evidence nodes e of P( e | Parents(e) )
         = P(V = T) × P(D = T) = 0.6 × 0.1 = 0.06
   The SAMPLED variables L and F do NOT enter w — they were drawn from their
   own CPTs, so their probabilities are already accounted for.
   Estimate P(¬F | e) = ( Σ w over samples with F = false ) / ( Σ w over all samples ).
   Nothing is rejected, which is why LW converges far faster than rejection
   sampling when the evidence is unlikely.
```

> **The error that costs this question:** multiplying the *sampled* variables'
> probabilities into `w` as well. `w` uses **evidence nodes only**.

</details>

---

## HW8 · Exercise Problem 2 — the WILP cricket network *(Post-midsem, slide 71)*

> Most of the WILP students are **fans (F)** of cricket irrespective of their
> gender. With the new season of IPL having started in the exam month, almost
> every cricket fan spends time to **watch (W)** the live play. Sometimes being
> a **parent (P)** reduces the probability of watching the IPL live season. A
> likely consequence of watching matches is **reduced concentration (C)** on
> the following day/s. A consequence of the reduced concentration is increased
> **stress (S)** with the work environment, leading to reduced **productivity
> (D)** in the project. Lack of concentration might also be caused by **viral
> infection (V)**, which is common in this **rainy season (R)**. WILP students
> have the comprehensive exams, and reduced concentration would reduce the
> probability of **good grades (G)** in the exam, which reflects the
> performance of students in the examination.
>
> Assume an AI agent is fed with this information and answers certain queries
> that can be inferred. **Assume all the events (conditional or unconditional)
> are equally likely to occur.**
>
> 1. Construct the Bayesian network.
> 2. What is the chance that *"an ardent fan of cricket who is a parent of two
>    kids, never misses an IPL match, doesn't get stressed in work environment,
>    is affected by viral infection and performs well in the comprehensive
>    examination"*?
> 3. *"Performance in the examination is independent of stress in the work
>    environment, given it is known that the student is affected by viral
>    infection."* Check for D-separation.

<details><summary><b>Show solution — HW8</b></summary>

> **Do this one first.** Part 2 is the same shape as **Q3(c) of the Apr 2025
> real paper**, and both land on `0.5⁶ = 0.015625`. The examiner reused the
> deck's own exercise.

**Part 1 — the network**

Read the causal verbs out of the prose, one edge per clause:

```
   (F) Fan          (P) Parent            (R) Rainy season
      \              /                          |
       \            /                           v
        v          v                        (V) Viral
        (W) Watch IPL                          /
              \                               /
               v                             v
                    ( C ) Reduced concentration
                        /                \
                       v                  v
              (S) Stress            (G) Good grades
                    |
                    v
              (D) Reduced productivity
```

```
 Parent lists — write these, they are unambiguous:
   F : none        P : none        R : none
   W : F, P
   V : R
   C : W, V
   S : C           G : C           D : S
```

**CPTs.** The instruction *"assume all the events (conditional or
unconditional) are equally likely to occur"* means **every entry is 0.5** —
roots and conditionals alike. Write the tables out anyway; the marking scheme
allocates marks to them.

```
 P(F=T)=0.5   P(P=T)=0.5   P(R=T)=0.5
 P(W=T | f,p) = 0.5  for all 4 rows        P(V=T | r)   = 0.5  for both rows
 P(C=T | w,v) = 0.5  for all 4 rows        P(S=T | c)   = 0.5  for both rows
 P(G=T | c)   = 0.5  for both rows         P(D=T | s)   = 0.5  for both rows
```

**Part 2 — the query**

Translate the sentence into variables **before computing anything**:

```
 "ardent fan of cricket"                 ->  F = true
 "is a parent of two kids"               ->  P = true
 "never misses an IPL match"             ->  W = true
 "doesn't get stressed in work env."     ->  S = FALSE     <- the negation
 "is affected by viral infection"        ->  V = true
 "performs well in the comprehensive"    ->  G = true

 R, C and D are NOT mentioned  ->  they are HIDDEN and must be summed out.

 QUERY :  P( F, P, W, ¬S, V, G )
```

**Symbolic expansion first (free marks):**

```
 P(F, P, W, ¬S, V, G)
   = Σ over r, c, d of  P(F)·P(P)·P(r)·P(W|F,P)·P(V|r)·P(c|W,V)·P(¬S|c)·P(G|c)·P(d|¬S)
```

**Then the shortcut, and say why it is valid:**

```
 Every CPT entry equals 0.5, so each variable is Bernoulli(0.5) INDEPENDENTLY
 of its parents. Summing a hidden variable out therefore contributes exactly 1
 ( 0.5 + 0.5 = 1 ), and each of the six SPECIFIED variables contributes 0.5.

   P(F, P, W, ¬S, V, G)  =  0.5^6
                         =  1 / 64
                         =  0.015625
```

**Answer: 0.015625, about 1.6 %.**

*Note that `¬S` costs the same 0.5 as `S` — with a uniform CPT, negating a
variable does not change its probability. Six named variables ⇒ exponent 6.
**Count the variables actually named in the sentence** — that is the whole
question, and it is where the marks are lost.*

**Part 3 — D-separation: is G ⊥ S | V ?**

```
 Find every path from G to S.
   Path:  G ← C → S          a FORK at C
   at C : FORK, and C is NOT in the evidence set (only V is)  ->  OPEN

 One open path is enough  ->  G and S are D-CONNECTED.
 -> THE STATEMENT IS FALSE. They are NOT independent given V.
```

**Justification to write down.** S and G share a single common cause,
**reduced concentration (C)**. Learning that a student is *not* stressed is
evidence that concentration was *not* reduced, which in turn raises the chance
of good grades. Conditioning on **V** does not help at all — V is a *parent of
C*, not on the G–S path, so it blocks nothing.

**What would make the statement true:** observe **C** itself. `G ⊥ S | C`
holds, because then the fork at C is blocked and no other path exists. Say this
explicitly — it shows you have understood the fork rule rather than guessed.

</details>

---

## HW9 · Explain HMM & Viterbi *(Post-midsem, slide 45)*

> In general it's observed that **low concentration/focus among students leads
> to low grades 80 % of the time**, and **high concentration/focus produces
> good grades 95 % of the time**. **60 % of the time students realize that low
> concentration had led to challenges in completed exams and they decide to
> concentrate more in the upcoming next exams. 30 % of the time students are
> always prudent and proactively prepare with concentration for every exam.**
> At the start of the course enrolment, **usually 98 % of students are willing
> to concentrate more** for evaluations.
>
> An AI agent is designed to perform learner behavioural analysis based on the
> given model. With inputs of grades scored by students for a few semesters,
> how does the AI system answer the query, where **B = Scoring Low Grade,
> G = Scoring High Grade**?
>
> **Example query:** *"What is the most likely explanation of the student
> behaviour if the pattern observed is **B - G - B**?"* — Apply the **Viterbi**
> algorithm.

<details><summary><b>Show solution — HW9</b></summary>

**STEP 1 — Extract the HMM from the prose [this is half the marks]**

```
 HIDDEN STATES     L = Low concentration      H = High concentration
 OBSERVATIONS      B = Scoring Low Grade      G = Scoring High Grade

 EMISSION  b_j(o)          B       G          from "low concentration leads to low
   L (low  concentration)  0.80    0.20       grades 80 % of the time" and "high
   H (high concentration)  0.05    0.95       concentration produces good grades 95 %"
                          (rows sum to 1 ✓)

 TRANSITION  a_ij      to L    to H
   from L               0.40    0.60          "60 % of the time students realise …
   from H               0.70    0.30          and concentrate more next time"
                       (rows sum to 1 ✓)      "30 % are always prudent" = stay High

 INITIAL   π(H) = 0.98   π(L) = 0.02          "98 % are willing to concentrate more"
```

State the two inferences explicitly — they are the reading-comprehension marks:
"60 % decide to concentrate more" is the **L → H** transition, so **L → L =
0.40**; "30 % are always prudent … for every exam" is the **H → H**
transition, so **H → L = 0.70**.

**STEP 2 — Viterbi, observation sequence B, G, B**

```
 v1(j)   = π(j) · b_j(o1)
 vt(j)   = [ MAX over i of  v(t−1)(i) · a_ij ] · b_j(ot)
 bp_t(j) = argmax over i of [ v(t−1)(i) · a_ij ]
```

**t = 1, observation = B**

```
 v1(L) = 0.02 × 0.80 = 0.016
 v1(H) = 0.98 × 0.05 = 0.049
                       -----
                sum =  0.065
```

**Normalise at t = 1 — the deck's own convention** (it does exactly this in the
S-S-R example, 0.1 → 0.25 and 0.3 → 0.75):

```
 v1(L) = 0.016 / 0.065 = 0.246154
 v1(H) = 0.049 / 0.065 = 0.753846
```

**t = 2, observation = G**

```
 into L : max( 0.246154 × 0.40 , 0.753846 × 0.70 )
        = max( 0.098462        , 0.527692        ) = 0.527692     bp = H
   v2(L) = 0.527692 × 0.20 = 0.105538

 into H : max( 0.246154 × 0.60 , 0.753846 × 0.30 )
        = max( 0.147692        , 0.226154        ) = 0.226154     bp = H
   v2(H) = 0.226154 × 0.95 = 0.214846
```

**t = 3, observation = B**

```
 into L : max( 0.105538 × 0.40 , 0.214846 × 0.70 )
        = max( 0.042215        , 0.150392        ) = 0.150392     bp = H
   v3(L) = 0.150392 × 0.80 = 0.120314

 into H : max( 0.105538 × 0.60 , 0.214846 × 0.30 )
        = max( 0.063323        , 0.064454        ) = 0.064454     bp = H
   v3(H) = 0.064454 × 0.05 = 0.003223
```

**Trellis**

```
                 t=1 (B)      t=2 (G)                t=3 (B)
 L (low)         0.246154     0.105538  (bp H)     * 0.120314 * (bp H)
 H (high)        0.753846     0.214846  (bp H)       0.003223   (bp H)
```

**STEP 3 — Termination and backtrace**

```
 max at t = 3  =  0.120314  at  L
 bp3(L) = H    ->  t = 2 state is H
 bp2(H) = H    ->  t = 1 state is H

 MOST LIKELY EXPLANATION :   H  ->  H  ->  L
                            (High, High, Low concentration)
```

**Answer: High → High → Low concentration.**

**Read it back — this is where the "explain" marks are.** The student starts in
High concentration (the prior is 0.98, overwhelming) and the first low grade B
is treated as a fluke, since High still emits B 5 % of the time and the prior is
so strong. The good grade G at t = 2 confirms High (0.95 emission). The second
B at t = 3 is finally enough to flip the state to Low, because by then the prior
advantage has been used up and `P(B | L) = 0.80` is sixteen times
`P(B | H) = 0.05`. The AI agent's conclusion for the learner-analytics system:
**concentration dropped in the last exam**, not throughout.

> **Three marks lost every time.**
> 1. **MAX, not SUM.** If you add the two incoming products you have written
>    the Forward algorithm and answered a different question.
> 2. **The answer is the state SEQUENCE, not the final number.** Store the
>    backpointers and walk them back. Writing "0.120314" alone earns almost
>    nothing.
> 3. **Normalise at t = 1 only**, and only in Viterbi. It cannot change the
>    path — it scales every later value by the same constant — but the paper
>    says *"strictly follow the approach as discussed in class"* and the deck
>    normalises, so the line is worth a mark.

</details>

---

## What is *not* in this file

- **Slides 34 (backward chaining, `Criminal(West)`) and 44/47 (Markov and
  Forward, S-S-R)** are **worked examples** in the deck, not homework — the
  deck prints their answers. They are covered in `ch08-09-logic-cnf-dpll-fol.md`
  and `ch11-markov-hmm-viterbi.md`.
- **Slides 12–19 of CS#15 (`PROBLEM 1: STABILITY`, `PROBLEM 2: TAXI SHARING`)**
  are likewise worked in the deck; both are reproduced with full workings in
  `ch13-cooperative-gt-shapley-auctions-voting.md` (the taxi Shapley value
  comes out to **(2, 5, 35)**).
- Fresh, unseen practice in exam format is in **`MOCK-PAPERS.md`** — two full
  40-mark papers plus an 18-item rapid drill.

*Every numerical answer above was recomputed independently. Where the deck's own
printed values are inconsistent or incomplete — the inadmissible heuristic in
HW2 and the placeholder CPTs in HW7 — that is flagged in place rather than
quietly corrected.*
