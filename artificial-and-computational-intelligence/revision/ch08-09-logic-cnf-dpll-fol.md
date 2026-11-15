# Ch 8 & 9 — Knowledge Representation using Logics
**Slides: CS#9 (Propositional Logic) and CS#10 (First-Order Logic)**
(post-midsem deck, pages 1–22)

> **~14% of the marks.** A whole 7-mark question on the Apr 2025 endsem
> (`KB → CNF → DPLL`) and a 4-mark FOL resolution question on the makeup.
> Both are worked in full below, §9 and §16.
>
> You already saw this in session 9, so **skip the explainer and work straight
> through the MD.**

---

## PART A — PROPOSITIONAL LOGIC

## 1. Model and entailment — get the vocabulary exact

> **Model** — any **possible world**. Not necessarily reality. Any combination of
> assignments of truth values to the sentences in our KB.

With two sentences `S1, S2` there are 4 possible models:
```
m1: {S1:T, S2:T}   m2: {S1:F, S2:T}   m3: {S1:T, S2:F}   m4: {S1:F, S2:F}
```
`S1` is true in `m1` and `m3` → we say **m1 satisfies S1**.
`M(S1)` = the **set of models that satisfy S1** = `[m1, m3]`.

> **Entailment** `X ⊨ Y` — "X entails Y".
> **In every model where X is true, Y is also true.**

That definition is the whole chapter. Every technique below is just a different
way of checking it without listing every model.

---

## 2. Propositional logic — syntax

> A **proposition** is a **declarative sentence that is either True or False, but
> not both**.

| Sentence | Proposition? |
|---|---|
| The sun rises in the East and sets in the West | ✓ (True) |
| 1 + 1 = 2 | ✓ (True) |
| 'b' is a vowel | ✓ (**False** — still a proposition) |
| Will you go to office today? | ✗ no truth value |
| X − 3 = 6 | ✗ could be either — **not** a proposition |

- **Atomic sentence** — a single propositional symbol, e.g. `W1,3` = "Wumpus in [1,3]".
- **Complex sentence** — atomic sentences joined by connectives and parentheses.
- **Literal** — an atomic sentence (**positive literal**) or a negated atomic
  sentence (**negative literal**).

### The five connectives

| Symbol | Name | Parts are called |
|---|---|---|
| `¬` | negation (not) | — |
| `∧` | **conjunction** (and) | **conjuncts** |
| `∨` | **disjunction** (or) | **disjuncts** |
| `⟹` | implication / conditional | premise (**antecedent**) ⟹ conclusion (**consequent**) |
| `⟺` | biconditional (if and only if) | — |

### Operator precedence — *worth a mark on its own*
```
¬   ,   ∧   ,   ∨   ,   ⟹   ,   ⟺
```
Highest → lowest. So `¬A ∧ B` means `(¬A) ∧ B`, **not** `¬(A ∧ B)`.

### The implication truth table — the row people get wrong

`p ⟹ q` is **False only when p is True and q is False.** Otherwise True.

> **Why is `F ⟹ anything` true?** The slides put it well: *the implication
> guarantees that when p is true, q is true. It guarantees nothing when p is
> false. There is no way of knowing whether the implication is false, since p
> did not happen.*
>
> "If it rains, I'll bring an umbrella." It didn't rain. You didn't lie.

`p ⟺ q` has the same truth value as `(p ⟹ q) ∧ (q ⟹ p)`, i.e. true when p and
q have the **same** truth value.

---

## 3. The Wumpus KB — the running example

```
Px,y  true if there is a PIT in [x,y]
Wx,y  true if there is a WUMPUS in [x,y]
Bx,y  true if the agent perceives a BREEZE in [x,y]
Sx,y  true if the agent perceives a STENCH in [x,y]
```

The knowledge base:
```
R1 : ¬P1,1
R2 : B1,1 ⟺ (P1,2 ∨ P2,1)
R3 : B2,1 ⟺ (P1,1 ∨ P2,2 ∨ P3,1)
R4 : ¬B1,1
R5 : B2,1
```
**Query: is `¬P1,2` entailed by the KB?**

We will answer it **three different ways** — truth tables, theorem proving, and
resolution. The exam can ask for any of them.

---

## 4. Method 1 — Truth-Table Entailment (TT-Entails)

The five steps, straight off the slide:
```
1. Get the sufficient symbols:  B1,1, B2,1, P1,1, P1,2, P2,1, P2,2, P3,1   (7 symbols)
2. Enumerate ALL models — every combination of truth values
3. Find the models where the KB is TRUE (every one of R1..R5 true)
4. In those models, check whether the query is true
5. If the query is true in ALL models where KB is true -> it is ENTAILED
```

**Result:** the KB is true in exactly **3** models. `¬P1,2` is true in **all
three**, so **`¬P1,2` is entailed — there is no pit in [1,2]**.

> **The nuance that earns the extra mark:** `P2,2` is true in **two** of the
> three models and false in one — so we **cannot infer** whether there is a pit
> in [2,2]. Entailment requires truth in *every* KB-satisfying model, not most.

### Complexity — memorise
```
n symbols  ->  2^n models
Time  : O(2^n)
Space : O(n)      because the enumeration is DEPTH-FIRST
```
> Space is only `O(n)` because you walk the truth-table tree depth-first and only
> ever hold one path. That contrast (exponential time, linear space) is exactly
> what gets asked.

---

## 5. Method 2 — Theorem proving with inference rules

> **Theorem proving** — applying rules of inference directly to sentences in the
> KB to prove the query, **without consulting models**.

**Logical equivalence:** `α ≡ β` if they are true in the same set of models.

### The inference rules

| Rule | Form | Example |
|---|---|---|
| **Modus Ponens** ("mode that affirms") | `(α ⟹ β), α  ⊢  β` | "If I am tired I need rest" + "I am tired" ⟹ "I need rest" |
| **And-Elimination** | `(α ∧ β) ⊢ α`  or  `⊢ β` | From `Tired ∧ Sleepy`, infer `Tired` |

### The eleven logical equivalences — *from the official formula sheet*

```
(α ∧ β) ≡ (β ∧ α)                              commutativity of ∧
(α ∨ β) ≡ (β ∨ α)                              commutativity of ∨
((α ∧ β) ∧ γ) ≡ (α ∧ (β ∧ γ))                  associativity of ∧
((α ∨ β) ∨ γ) ≡ (α ∨ (β ∨ γ))                  associativity of ∨
¬(¬α) ≡ α                                      double-negation elimination
(α ⟹ β) ≡ (¬β ⟹ ¬α)                            CONTRAPOSITION
(α ⟹ β) ≡ (¬α ∨ β)                             IMPLICATION ELIMINATION
(α ⟺ β) ≡ ((α ⟹ β) ∧ (β ⟹ α))                  BICONDITIONAL ELIMINATION
¬(α ∧ β) ≡ (¬α ∨ ¬β)                           DE MORGAN
¬(α ∨ β) ≡ (¬α ∧ ¬β)                           DE MORGAN
(α ∧ (β ∨ γ)) ≡ ((α ∧ β) ∨ (α ∧ γ))            distributivity of ∧ over ∨
(α ∨ (β ∧ γ)) ≡ ((α ∨ β) ∧ (α ∨ γ))            DISTRIBUTIVITY of ∨ over ∧
```

The four in CAPS are the ones you use constantly in CNF conversion.

### WORKED — proving `¬P1,2` by theorem proving

**Name the rule on every line.** The marking scheme says *"Rule name should be
specified."*

| # | Sentence | Rule used |
|---|---|---|
| R2 | `B1,1 ⟺ (P1,2 ∨ P2,1)` | given |
| R6 | `(B1,1 ⟹ (P1,2 ∨ P2,1)) ∧ ((P1,2 ∨ P2,1) ⟹ B1,1)` | **Biconditional Elimination** |
| R7 | `(P1,2 ∨ P2,1) ⟹ B1,1` | **And-Elimination** |
| R8 | `¬B1,1 ⟹ ¬(P1,2 ∨ P2,1)` | **Contraposition** |
| R9 | `¬(P1,2 ∨ P2,1)` | **Modus Ponens** (with R4: `¬B1,1`) |
| R10 | `¬P1,2 ∧ ¬P2,1` | **De Morgan** |
| R11 | **`¬P1,2`** | **And-Elimination** |

Six rules, six lines. That is the model answer.

---

## 6. Method 3 — Resolution (the one the exam uses)

### CNF — what it is

> A formula is in **Conjunctive Normal Form** if it is a **conjunction of
> clauses**, where each **clause is a disjunction of literals**.
> A **product of sums**: `∧` between clauses, `∨` inside them.

```
Example CNF:   (A ∨ ¬B) ∧ (A ∨ B ∨ ¬C) ∧ ¬A
```

### The CNF conversion recipe — *four steps, in this order*

```
1. BICONDITIONAL ELIMINATION    α ⟺ β    ->  (α ⟹ β) ∧ (β ⟹ α)
2. IMPLICATION ELIMINATION      α ⟹ β    ->  ¬α ∨ β
3. MOVE ¬ INWARDS               De Morgan + double-negation elimination
4. DISTRIBUTE ∨ OVER ∧          α ∨ (β ∧ γ)  ->  (α ∨ β) ∧ (α ∨ γ)
```

> **Do them in that order.** Doing step 4 before step 3 creates a mess you cannot
> recover from.

### The resolution rule
```
From    A ∨ B      and      ¬B ∨ C
Derive               A ∨ C
```
`B` and `¬B` are **complementary literals**. You cancel them because one of them
must be false whatever `B`'s truth value is.

### Proof by contradiction — how resolution proves a query

You never prove the query directly. You **assume its negation** and derive a
contradiction (the **empty clause `{ }`**).

| Assumption | Inference | Conclusion |
|---|---|---|
| Assume query is **False** | derives **FALSE** (empty clause) | Assumption is false ⟹ **query is TRUE** |
| Assume query is **True** | derives **FALSE** | Assumption is false ⟹ query is FALSE |

### WORKED — Wumpus CNF conversion

| Step | `R2 : B1,1 ⟺ (P1,2 ∨ P2,1)` | `R3 : B2,1 ⟺ (P1,1 ∨ P2,2 ∨ P3,1)` |
|---|---|---|
| **Biconditional Elim** | `(B1,1 ⟹ (P1,2 ∨ P2,1)) ∧ ((P1,2 ∨ P2,1) ⟹ B1,1)` | `(B2,1 ⟹ (…)) ∧ ((…) ⟹ B2,1)` |
| **Implication Elim** | `¬B1,1 ∨ (P1,2 ∨ P2,1)` and `¬(P1,2 ∨ P2,1) ∨ B1,1` | `¬B2,1 ∨ (P1,1 ∨ P2,2 ∨ P3,1)` and `¬(P1,1∨P2,2∨P3,1) ∨ B2,1` |
| **De Morgan** | `(¬P1,2 ∧ ¬P2,1) ∨ B1,1` | `(¬P1,1 ∧ ¬P2,2 ∧ ¬P3,1) ∨ B2,1` |
| **Distribute ∨ over ∧** | `(¬P1,2 ∨ B1,1) ∧ (¬P2,1 ∨ B1,1)` | `(¬P1,1∨B2,1) ∧ (¬P2,2∨B2,1) ∧ (¬P3,1∨B2,1)` |

Final clause set:
```
R6  : ¬B1,1 ∨ P1,2 ∨ P2,1
R7  : ¬P1,2 ∨ B1,1
R8  : ¬P2,1 ∨ B1,1
R9  : ¬B2,1 ∨ P1,1 ∨ P2,2 ∨ P3,1
R10 : ¬P1,1 ∨ B2,1
R11 : ¬P2,2 ∨ B2,1
R12 : ¬P3,1 ∨ B2,1
```

### The refutation

Query `¬P1,2`. **Negate it** → add `P1,2` to the clause set.

```
       R4 : ¬B1,1          R7 : ¬P1,2 ∨ B1,1
              \                  /
               \                /       resolve on B1,1
                 ¬P1,2                              (negated query) P1,2
                     \                                    /
                      \                                  /   resolve on P1,2
                                    { }   EMPTY CLAUSE
```

Empty clause derived → contradiction → **`¬P1,2` is entailed.**

---

## 7. DPLL

> The **Davis–Putnam–Logemann–Loveland** algorithm is a **complete,
> backtracking-based search algorithm for deciding the satisfiability** of
> propositional formulae **in CNF**.

### The three improvements over naive enumeration — *name all three*

| # | Heuristic | What it does |
|---|---|---|
| 1 | **Early Termination** | Stop as soon as the outcome is known. A clause is true if **any** literal is true; the whole formula is false if **any** clause is false. No need to assign the rest. |
| 2 | **Pure Symbol Heuristic** | A symbol that appears with **only one sign** across all clauses is **pure**. Assign it the sign that makes its literals true — this can never hurt. |
| 3 | **Unit Clause Heuristic** | A clause with only **one unassigned literal** forces that literal's value. Cascades (unit propagation). |

> **How to spot a pure symbol in 10 seconds:** scan the clause list for the
> symbol. If you only ever see `X` (never `¬X`), it is pure-positive → set it
> **True**. If you only ever see `¬X`, it is pure-negative → set it **False**.
> If you see **both**, it is **not pure**.

---

## 8. Pros and cons of propositional logic

| Pros | Cons |
|---|---|
| **Declarative** | **Very limited expressive power** |
| Allows **partial / disjunctive / negated** information (unlike most data structures and databases) | Cannot say *"pits cause breezes in adjacent squares"* — **except by writing one sentence per square** |
| **Compositional** — the meaning of `B1,1 ∧ P1,2` derives from the meanings of `B1,1` and `P1,2` | Cannot express *"Some students are brilliant"* |
| Meaning is **context-independent** (unlike natural language) | |

**That last cons row is the entire motivation for First-Order Logic.**

---

## 9. ⭐ PAST PAPER — Apr 2025, Q2 (7 marks) fully worked

> *"Not all instances of a low-voltage alert (V) in a smart city's power grid are
> caused by an absent power station (P). Some alerts may occur due to faulty
> connections (F) or energy leakage (E). When both a high-load condition (H) and
> a missing load balancer (L) are detected, the system identifies it as an
> overloaded segment (O). Power fluctuations (W) may also be triggered by faulty
> lines, energy surges (S), or timing mismatches (T). Additionally, if a
> low-voltage alert (V) occurs without a power fluctuation (¬W), it must indicate
> a critical failure (C)."*
>
> **(a)** Represent the KB in propositional logic **[2]**
> **(b)** Convert to CNF **[2.5]** — *"Rule name should be specified"*
> **(c)** Find a sample complete BSAT solution using DPLL, step by step **[2.5]**

### (a) The knowledge base — 2 marks

```
R1 : V → (P ∨ F ∨ E)          low voltage implies one of the three causes
R2 : H ∧ L → O                 high load AND missing balancer implies overload
R3 : W → (F ∨ S ∨ T)          fluctuation implies faulty line / surge / timing
R4 : V ∧ ¬W → C                low voltage WITHOUT fluctuation implies critical
```

> **Read the direction carefully.** "Alerts *may occur due to* faulty
> connections" becomes `V → (P ∨ F ∨ E)` — the **alert implies the causes**, not
> the other way round. Reversing an arrow loses the mark.

### (b) Conversion to CNF — 2.5 marks. **Name the rule on every line.**

```
R1 : V → (P ∨ F ∨ E)
     Implication Elimination  (α ⟹ β ≡ ¬α ∨ β)
     ->  ¬V ∨ P ∨ F ∨ E

R2 : H ∧ L → O
     Implication Elimination  ->  ¬(H ∧ L) ∨ O
     De Morgan                ->  ¬H ∨ ¬L ∨ O

R3 : W → (F ∨ S ∨ T)
     Implication Elimination  ->  ¬W ∨ F ∨ S ∨ T

R4 : V ∧ ¬W → C
     Implication Elimination  ->  ¬(V ∧ ¬W) ∨ C
     De Morgan                ->  ¬V ∨ ¬¬W ∨ C
     Double-negation elim     ->  ¬V ∨ W ∨ C
```

**Final CNF:**
```
R1 : ¬V ∨ P ∨ F ∨ E
R2 : ¬H ∨ ¬L ∨ O
R3 : ¬W ∨ F ∨ S ∨ T
R4 : ¬V ∨ W ∨ C
```
✓ matches the official key exactly.

> **R4 is the one that trips people.** `¬(V ∧ ¬W)` → De Morgan → `¬V ∨ ¬(¬W)` →
> double negation → `¬V ∨ W`. Two rules, not one. Show both.

### (c) DPLL — 2.5 marks

**Step 1: find the pure symbols.** *(The key says "Need to be specified" — so
write out the scan.)*

| Symbol | Appears as | Pure? | Assign |
|---|---|---|---|
| V | `¬V` (R1), `¬V` (R4) | **pure negative** | **False** |
| P | `P` (R1) | pure positive | True |
| F | `F` (R1), `F` (R3) | pure positive | True |
| E | `E` (R1) | pure positive | True |
| H | `¬H` (R2) | pure negative | False |
| L | `¬L` (R2) | pure negative | False |
| O | `O` (R2) | pure positive | True |
| S | `S` (R3) | pure positive | True |
| T | `T` (R3) | pure positive | True |
| C | `C` (R4) | pure positive | True |
| **W** | `¬W` (R3) **and** `W` (R4) | ✗ **BOTH SIGNS — not pure** | free |

**Pure symbols: `V, P, F, E, H, L, O, S, T, C`** ✓ exactly the official key.
**`W` is the only impure symbol.**

**Step 2: assign every pure symbol the sign that satisfies its literals.**

**Step 3: check each clause (early termination).**
```
R1 : ¬V ∨ P ∨ F ∨ E     V=False   -> ¬V is TRUE   -> clause SATISFIED
R2 : ¬H ∨ ¬L ∨ O        H=False   -> ¬H is TRUE   -> clause SATISFIED
R3 : ¬W ∨ F ∨ S ∨ T     F=True                    -> clause SATISFIED
R4 : ¬V ∨ W ∨ C         V=False   -> ¬V is TRUE   -> clause SATISFIED
```

All four clauses satisfied **without ever assigning W**, so `W` may take either
value. **No backtracking was needed.**

### A sample complete BSAT solution

```
V = False    P = True     F = True     E = True
H = False    L = False    O = True
S = True     T = True     C = True
W = True     (or False — both work)
```

> **Sanity check worth stating:** the model has `V = False`, which makes R1 and
> R4 vacuously true — consistent with the implication truth table, where
> `F ⟹ anything` is True. That is the logic behind the whole answer.

*(For reference: the full formula has **1386 satisfying models out of 2^11 =
2048**. The question only asks for one — but the pure-symbol route finds one
without any search, which is exactly why the heuristic exists.)*

---

## PART B — FIRST-ORDER LOGIC

## 10. Why FOL exists

Propositional logic cannot say *"pits cause breezes in adjacent squares"* except
by writing one sentence per square. FOL adds **objects, relations and
quantifiers**, so one sentence covers everything.

| | Propositional Logic | First-Order Logic |
|---|---|---|
| World is made of | facts | **objects, relations, functions** |
| Can generalise? | no | **yes, via quantifiers** |
| `Some students are brilliant` | impossible | `∃x student(x) ∧ brilliant(x)` |

---

## 11. The two quantifiers — and the rule everyone gets wrong

| | Read as | Pairs with |
|---|---|---|
| **`∀x`** universal | "for all x", "for each x", "for every x" | **`→` (implication)** |
| **`∃x`** existential | "there exists an x", "for some x", "for at least one x" | **`∧` (conjunction)** |

```
All men drink coffee        ->   ∀x  man(x) → drink(x, coffee)
Some boys are intelligent   ->   ∃x  boys(x) ∧ intelligent(x)
```

> ### ⚠ **`∀` goes with `→`. `∃` goes with `∧`.** This is the #1 FOL exam error.
>
> **Why?** `∀x man(x) ∧ drink(x,coffee)` would claim **everything in the
> universe is a man who drinks coffee** — including your chair. The implication
> restricts the claim to men only.
>
> And `∃x boys(x) → play(x,cricket)` is trivially true the moment **anything**
> in the universe is not a boy (`F ⟹ anything = T`), so it says nothing at all.

More slide examples:
```
Prof John is teaching ML for WILP students   ->  ∃x,c,s  Teaching(X, C, S)
Seller sells all products to customers        ->  ∀p  Sells(S, P, C)
```

---

## 12. Instantiation rules — from the official formula sheet

```
UNIVERSAL INSTANTIATION (UI)      ∀v α   ⟹   Subst({v/g}, α)
    where g is a GROUND TERM (contains no variables)

EXISTENTIAL INSTANTIATION (EI)    ∃v α   ⟹   Subst({v/k}, α)
    where k is a NEW CONSTANT SYMBOL (a SKOLEM CONSTANT) that
    does NOT appear elsewhere in the knowledge base
```

> **The difference that carries the mark:** UI lets you substitute **any** ground
> term, and you may do it **as many times as you like**. EI may be applied
> **once**, and the constant must be **brand new** — because "something exists"
> tells you nothing about *which* thing it is, so you must invent a fresh name
> for it. Reusing an existing name would assert more than you know.

---

## 13. FOL translation exercises (from the slides)

| English | FOL |
|---|---|
| 1. All birds fly | `∀x bird(x) → fly(x)` |
| 2. Every man respects his parent | `∀x man(x) → respects(x, parent(x))` |
| 3. Some boys play cricket | `∃x boys(x) ∧ play(x, cricket)` |
| 4. Not all students like both Maths and Science | `¬∀x [student(x) → (likes(x,Maths) ∧ likes(x,Science))]`<br>≡ `∃x student(x) ∧ ¬(likes(x,Maths) ∧ likes(x,Science))` |
| 5. Only one student failed in Mathematics | `∃x [student(x) ∧ failed(x,Maths) ∧ ∀y ((student(y) ∧ failed(y,Maths)) → (x = y))]` |

> #5 is the pattern for **"exactly one"**: assert one exists, then assert
> anything with the same property **is** that one.
> #2 shows a **function** (`parent(x)`) rather than a predicate — functions
> return an object, predicates return true/false.

---

## 14. Forward chaining

```
Algorithm:
1. Start from the FACTS
2. Trigger all rules whose premises are satisfied
3. Add the conclusion to the known facts
4. Repeat until no new facts are added, or the query is answered
```

The slides annotate each step with its practical difficulty:

| Step | Issue |
|---|---|
| 1. Start from the facts | **Conjunct ordering** |
| 2. Trigger satisfied rules | **Pattern matching** |
| 3. Add conclusions | **Irrelevant facts** |
| 4. Repeat | **Redundant rule matching** |

### WORKED — the "Nono / Colonel West" example

Facts: `Missile(M1)`, `Owns(Nono, M1)`, `American(West)`, `Enemy(Nono, America)`

Rules:
```
r1: Missile(x)                                          → Weapon(x)
r2: Missile(x) ∧ Owns(Nono, x)                          → Sells(West, x, Nono)
r3: Enemy(x, America)                                   → Hostile(x)
r4: American(x) ∧ Weapon(y) ∧ Sells(x,y,z) ∧ Hostile(z) → Criminal(x)
```
**Query: `Criminal(West)`?**

| Round | Rule fired | Substitution | New fact |
|---|---|---|---|
| 1 | r1 | `{x/M1}` | `Weapon(M1)` |
| 1 | r2 | `{x/M1}` | `Sells(West, M1, Nono)` |
| 1 | r3 | `{x/Nono}` | `Hostile(Nono)` |
| 2 | r4 | `{x/West, y/M1, z/Nono}` | **`Criminal(West)`** ✓ |

**Answer: yes, `Criminal(West)` is entailed** — reached in 2 rounds.

---

## 15. Backward chaining

```
Algorithm:
1. Form definite clauses
2. Start from the GOAL
3. Search through rules to find facts that support the proof
4. Stop when you reach the facts to be proved -> Empty Set on the LHS
```
Uses a **divide & conquer strategy** with **substitution by unification**.

| | Forward chaining | Backward chaining |
|---|---|---|
| Starts from | **facts** | **the goal** |
| Direction | data-driven, **bottom-up** | goal-driven, **top-down** |
| Derives | everything derivable | only what is relevant to the goal |
| Weakness | **irrelevant facts** — may derive masses of useless conclusions | can loop on recursive rules |
| Good when | you have few facts and want all consequences | you have one specific query |

Same example, backwards: `Criminal(West)` → needs `American(West)` ✓ (fact),
`Weapon(y)` → `Missile(M1)` ✓, `Sells(West,M1,Nono)` → `Missile(M1) ∧
Owns(Nono,M1)` ✓, `Hostile(Nono)` → `Enemy(Nono,America)` ✓. All subgoals bottom
out in facts → proved.

---

## 16. ⭐ PAST PAPER — Makeup Q1B (4 marks) fully worked

> *"Using resolution check whether the following is a tautology:*
> `∀x∃y∃z [ [P(x,y,z) ∨ ¬∃z∃u(¬P(x,z,u))] → ∃x∃y P(f(a), x, y) ]`
> *where `a` is a constant. Showcase all the steps."*

### Step 1 — simplify the inner negation
```
¬∃z∃u ( ¬P(x,z,u) )   ≡   ∀z∀u ¬¬P(x,z,u)   ≡   ∀z'∀u P(x,z',u)
```
*(rename the inner `z` to `z'` — it **shadows** the outer `∃z`, they are
different variables.)*

So the formula is:
```
∀x ∃y ∃z [ ( P(x,y,z) ∨ ∀z'∀u P(x,z',u) )  →  ∃x'∃y' P(f(a), x', y') ]
```

### Step 2 — to test validity, NEGATE and look for a contradiction
```
¬∀x∃y∃z [ A → B ]
  ≡  ∃x ∀y ∀z ¬[ A → B ]
  ≡  ∃x ∀y ∀z [ A ∧ ¬B ]                    since ¬(A→B) ≡ A ∧ ¬B

  =  ∃x ∀y ∀z [ ( P(x,y,z) ∨ ∀z'∀u P(x,z',u) ) ∧ ∀x'∀y' ¬P(f(a),x',y') ]
```

### Step 3 — Skolemise
`∃x` is **outermost**, so it becomes a **Skolem constant** `c` (a brand-new
constant, by EI).
```
∀y ∀z ∀z' ∀u ∀x' ∀y' [ ( P(c,y,z) ∨ P(c,z',u) ) ∧ ¬P(f(a),x',y') ]
```

### Step 4 — the clause set
```
C1 :  P(c,y,z) ∨ P(c,z',u)
C2 :  ¬P(f(a), x', y')
```

### Step 5 — attempt resolution
To resolve `C1` against `C2` we must unify a positive literal `P(c, ·, ·)` with
the negative literal `P(f(a), ·, ·)`.

```
UNIFY( P(c, y, z) , P(f(a), x', y') )
  first arguments:   c   vs   f(a)
      c    is a CONSTANT (a fresh Skolem constant)
      f(a) is a COMPOUND TERM (function f applied to constant a)
  -> a constant cannot unify with a compound term
  -> UNIFICATION FAILS
```

No other pair of complementary literals exists. The clause set is **saturated** —
no resolvent can be produced, so **the empty clause is NOT derivable**.

### Step 6 — conclusion

> **The negation is satisfiable, therefore the original formula is NOT a
> tautology (not valid).**

### Step 7 — confirm with a counter-model *(worth adding; it proves the point)*

```
Domain D = {0, 1},    a = 0,    f(0) = 0
P(0, y, z) = False   for all y, z
P(1, y, z) = True    for all y, z
```
Then:
- `f(a) = 0`, so the consequent `∃x'∃y' P(0,x',y') = False`.
- Take `x = 1`: the antecedent `P(1,y,z) ∨ ∀z'∀u P(1,z',u)` = `True ∨ True` = **True**
  for every `y, z`.
- So `antecedent → consequent` = `True → False` = **False** for every `y, z` —
  there is **no** `y, z` witness for `x = 1`.
- Hence `∀x∃y∃z[…]` is **False** in this model. ∎

> **The insight to state in one line:** the consequent only ever talks about
> `P(f(a), …)`, but the antecedent can be made true using a completely different
> object. Nothing forces the two to be about the same thing, so the implication
> can fail. **Resolution detects exactly this — `c` and `f(a)` will not unify.**

---

## 17. You try

**Q1 (KB → CNF, past-paper style).** *"A server raises an outage alert (A) only
if there is a network failure (N), a power cut (P), or a software crash (S). If
the backup is offline (B) and the cluster is unhealthy (U), the system declares
data loss (D). An outage alert without a power cut (¬P) means a hardware fault
(H)."*
(a) Write the KB in propositional logic.
(b) Convert to CNF, **naming the rule on every line**.

**Q2 (DPLL).** For your CNF from Q1, list the **pure symbols** with their signs,
identify any impure symbol, and give one complete satisfying assignment.

**Q3 (CNF conversion).** Convert `(A ⟺ B) ⟹ C` to CNF. Name every rule.

**Q4 (resolution).** Given the clause set
`{ ¬A ∨ B , ¬B ∨ C , A , ¬C }`, use resolution to derive the empty clause.
Show each resolution step and which literal you cancelled.

**Q5 (TT-entailment).** KB = `{ P ⟹ Q , Q ⟹ R , P }`. How many models must you
enumerate? Is `R` entailed? State the time and space complexity of the method.

**Q6 (inference rules).** From `X ⟺ (Y ∨ Z)` and `¬X`, derive `¬Y`. Name the
rule on every line.

**Q7 (FOL translation).** Translate:
(a) Every student who studies passes.
(b) Some employees do not attend any meeting.
(c) All cats are mammals but not all mammals are cats.
(d) Exactly one person owns this car.

**Q8 (FOL concepts).** State Universal Instantiation and Existential
Instantiation. Give the restriction on the term in each, and explain in one line
**why EI needs a brand-new constant**.

**Q9 (chaining).** Facts: `Student(Ravi)`, `Enrolled(Ravi, ACI)`.
Rules: `Student(x) ∧ Enrolled(x,c) → Attends(x,c)` ·
`Attends(x,c) → Eligible(x,c)`.
Run **forward chaining** to answer `Eligible(Ravi, ACI)?`, showing the
substitution at each step. Then do the same **backwards**.

---

## 18. Answers

<details>
<summary>Open only after attempting</summary>

**Q1 (a) — knowledge base**
```
R1 : A → (N ∨ P ∨ S)
R2 : B ∧ U → D
R3 : A ∧ ¬P → H
```

**(b) — CNF**
```
R1 : A → (N ∨ P ∨ S)
     Implication Elimination      ->  ¬A ∨ N ∨ P ∨ S

R2 : B ∧ U → D
     Implication Elimination      ->  ¬(B ∧ U) ∨ D
     De Morgan                    ->  ¬B ∨ ¬U ∨ D

R3 : A ∧ ¬P → H
     Implication Elimination      ->  ¬(A ∧ ¬P) ∨ H
     De Morgan                    ->  ¬A ∨ ¬¬P ∨ H
     Double-negation elimination  ->  ¬A ∨ P ∨ H
```

**Q2 — DPLL**

| Symbol | Appears as | Pure? | Assign |
|---|---|---|---|
| A | `¬A` (R1), `¬A` (R3) | pure negative | **False** |
| N | `N` (R1) | pure positive | True |
| **P** | `P` (R1) **and** `P` (R3) | both **positive** → still **pure** | True |
| S | `S` (R1) | pure positive | True |
| B | `¬B` (R2) | pure negative | False |
| U | `¬U` (R2) | pure negative | False |
| D | `D` (R2) | pure positive | True |
| H | `H` (R3) | pure positive | True |

**Every symbol is pure here** — there is no impure symbol, because `P` happens to
appear positively in *both* clauses. (Contrast the real past paper, where `W`
appeared as `¬W` in R3 and `W` in R4 and so was impure.)

Satisfying assignment: `A=F, N=T, P=T, S=T, B=F, U=F, D=T, H=T`.
Check: R1 `¬A`=T ✓ · R2 `¬B`=T ✓ · R3 `¬A`=T ✓.

**Q3 — `(A ⟺ B) ⟹ C`**
```
1. Biconditional Elimination   ->  ((A ⟹ B) ∧ (B ⟹ A)) ⟹ C
2. Implication Elimination (inner) ->  ((¬A ∨ B) ∧ (¬B ∨ A)) ⟹ C
3. Implication Elimination (outer) ->  ¬((¬A ∨ B) ∧ (¬B ∨ A)) ∨ C
4. De Morgan                   ->  (¬(¬A ∨ B) ∨ ¬(¬B ∨ A)) ∨ C
5. De Morgan (twice)           ->  ((A ∧ ¬B) ∨ (B ∧ ¬A)) ∨ C
6. Distribute ∨ over ∧         ->  (A ∨ B ∨ C) ∧ (A ∨ ¬A ∨ C)
                                   ∧ (¬B ∨ B ∨ C) ∧ (¬B ∨ ¬A ∨ C)
```
The middle two clauses contain a literal and its negation, so they are
**tautologies** and can be dropped:
```
CNF :  (A ∨ B ∨ C) ∧ (¬A ∨ ¬B ∨ C)
```

**Q4 — Resolution**
```
1. A            and  ¬A ∨ B     -> resolve on A    ->  B
2. B            and  ¬B ∨ C     -> resolve on B    ->  C
3. C            and  ¬C         -> resolve on C    ->  { }  EMPTY CLAUSE
```
The empty clause is derived, so the clause set is **unsatisfiable**.

**Q5 — TT-entailment**
3 symbols (`P, Q, R`) → **`2³ = 8` models** to enumerate.

The KB is true only when `P=T` (from the fact `P`), which forces `Q=T` (Modus
Ponens on `P⟹Q`), which forces `R=T`. So the KB is true in exactly **one**
model: `{P=T, Q=T, R=T}` — and `R` is true in it.
**`R` IS entailed.**

Complexity: **time `O(2ⁿ)`, space `O(n)`** — space is linear because the
enumeration is **depth-first**.

**Q6 — Inference**

| # | Sentence | Rule |
|---|---|---|
| 1 | `X ⟺ (Y ∨ Z)` | given |
| 2 | `(X ⟹ (Y∨Z)) ∧ ((Y∨Z) ⟹ X)` | **Biconditional Elimination** |
| 3 | `(Y ∨ Z) ⟹ X` | **And-Elimination** |
| 4 | `¬X ⟹ ¬(Y ∨ Z)` | **Contraposition** |
| 5 | `¬(Y ∨ Z)` | **Modus Ponens** (with `¬X`) |
| 6 | `¬Y ∧ ¬Z` | **De Morgan** |
| 7 | **`¬Y`** | **And-Elimination** |

Same seven-line shape as the Wumpus proof — the pattern is reusable.

**Q7 — FOL translations**

(a) `∀x [ (student(x) ∧ studies(x)) → passes(x) ]`

(b) `∃x [ employee(x) ∧ ∀m ( meeting(m) → ¬attends(x, m) ) ]`
*"does not attend **any**" = "attends **no**" — the negation goes inside the
inner quantifier. `¬∃m attends(x,m)` is an equally correct form.*

(c) `∀x [ cat(x) → mammal(x) ] ∧ ∃y [ mammal(y) ∧ ¬cat(y) ]`
*Two separate claims joined by `∧`. Note the first uses `∀…→` and the second
uses `∃…∧` — a clean demonstration of the pairing rule.*

(d) `∃x [ owns(x, car) ∧ ∀y ( owns(y, car) → (x = y) ) ]`

**Q8 — Instantiation**

```
UNIVERSAL INSTANTIATION   ∀v α  ⟹  Subst({v/g}, α)   where g is a GROUND TERM
EXISTENTIAL INSTANTIATION ∃v α  ⟹  Subst({v/k}, α)   where k is a NEW CONSTANT
                                                      (Skolem constant) not
                                                      appearing elsewhere in the KB
```

**Why EI needs a brand-new constant:** `∃x P(x)` tells you *something* has the
property but not *which* thing. If you instantiated with an existing name — say
`P(John)` — you would be asserting something strictly stronger than you know.
A fresh constant names the unknown witness without claiming it is anything you
already have a name for.

Also: UI can be applied **any number of times** with different ground terms;
EI is applied **once**.

**Q9 — Chaining**

**Forward** (start from facts):

| Round | Rule | Substitution | New fact |
|---|---|---|---|
| 1 | `Student(x) ∧ Enrolled(x,c) → Attends(x,c)` | `{x/Ravi, c/ACI}` | `Attends(Ravi, ACI)` |
| 2 | `Attends(x,c) → Eligible(x,c)` | `{x/Ravi, c/ACI}` | **`Eligible(Ravi, ACI)`** ✓ |

Query answered in 2 rounds.

**Backward** (start from the goal):
```
GOAL: Eligible(Ravi, ACI)
  matches rule 2 with {x/Ravi, c/ACI}
  -> subgoal: Attends(Ravi, ACI)
       matches rule 1 with {x/Ravi, c/ACI}
       -> subgoals: Student(Ravi)        -> FACT ✓
                    Enrolled(Ravi, ACI)  -> FACT ✓
  All subgoals bottom out in facts -> LHS empty -> PROVED
```

Both prove it. Forward chaining derived `Attends(Ravi,ACI)` whether or not it was
needed; backward chaining only ever pursued facts relevant to the goal.

</details>

---

## 19. Two-minute recall card

**Propositional logic**
- **Entailment `X ⊨ Y`:** in every model where X is true, Y is also true.
- Precedence: **`¬ , ∧ , ∨ , ⟹ , ⟺`**. So `¬A ∧ B` = `(¬A) ∧ B`.
- `p ⟹ q` is **false only when p=T, q=F**. `F ⟹ anything = T`.
- TT-entailment: `2ⁿ` models · **time `O(2ⁿ)`, space `O(n)`** (depth-first).
- Inference rules: **Modus Ponens**, **And-Elimination**.
- **CNF recipe, in order:** biconditional elim → implication elim → move ¬ inwards (De Morgan) → distribute ∨ over ∧.
- `α ⟹ β ≡ ¬α ∨ β` · `¬(α∧β) ≡ ¬α∨¬β` · `α ⟺ β ≡ (α⟹β)∧(β⟹α)`.
- **Resolution:** `A∨B` and `¬B∨C` give `A∨C`. Prove by **contradiction** — negate the query, derive the **empty clause `{ }`**.
- **DPLL** = complete backtracking SAT solver for CNF. Three improvements:
  **Early Termination · Pure Symbol Heuristic · Unit Clause Heuristic**.
- **Pure symbol** = appears with only ONE sign everywhere. Assign it that sign.
- **"Rule name should be specified"** — name the rule on every CNF line.

**First-Order Logic**
- **`∀` pairs with `→`. `∃` pairs with `∧`.** The #1 error in the paper.
- **UI:** `∀v α ⟹ Subst({v/g},α)`, `g` a **ground term**, usable **many times**.
- **EI:** `∃v α ⟹ Subst({v/k},α)`, `k` a **new Skolem constant**, used **once**.
- "Exactly one": `∃x [ P(x) ∧ ∀y (P(y) → x=y) ]`.
- **Forward chaining** = facts → conclusions, data-driven; issues are conjunct
  ordering, pattern matching, irrelevant facts, redundant rule matching.
- **Backward chaining** = goal → facts, divide & conquer, unification; stops with
  an **empty LHS**.
- **FOL resolution:** negate, Skolemise, clause set, unify. **A Skolem constant
  cannot unify with a compound term** — that failure is what proved the makeup
  paper's formula is *not* a tautology.
