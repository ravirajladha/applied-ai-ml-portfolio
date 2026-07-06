# Session 9 — Knowledge Representation using Logics

> **Course:** Artificial and Computational Intelligence (AIMLCZG557) · Module M4
> **Topic:** Propositional Logic, the Wumpus World, Inference by Entailment, Theorem Proving, Resolution, DPLL, and an intro to Predicate Logic.

This is a clean, readable write-up of the Session 9 slide deck so you can study it without opening the PDF. Companion practice notebook (exercises **with solutions**) lives in
`../practice/01 Propositional Logic - Knowledge Representation/practice.ipynb`.

---

## Table of contents

1. [Knowledge-based agents](#1-knowledge-based-agents)
2. [The Wumpus World](#2-the-wumpus-world)
3. [What "logic" means: syntax, semantics, models, entailment](#3-what-logic-means)
4. [Propositional logic](#4-propositional-logic)
5. [The connectives and their truth tables](#5-connectives-and-truth-tables)
6. [Representing the Wumpus World in propositional logic](#6-representing-the-wumpus-world)
7. [Inference 1 — TT-Entailment (model checking)](#7-inference-1--tt-entailment)
8. [Inference 2 — Theorem proving with inference rules](#8-inference-2--theorem-proving)
9. [Inference 3 — Proof by contradiction](#9-inference-3--proof-by-contradiction)
10. [Inference 4 — PL-Resolution via CNF](#10-inference-4--pl-resolution-via-cnf)
11. [DPLL algorithm](#11-dpll-algorithm)
12. [Pros & cons of propositional logic](#12-pros--cons-of-propositional-logic)
13. [Glossary](#13-glossary)

---

## 1. Knowledge-based agents

A **knowledge-based agent** solves problems by:

- **representing** knowledge about the world in a *state-space*, and
- **reasoning** about a solution in logical steps.

Its central component is the **Knowledge Base (KB)** — a set of *sentences*. These are **not** English sentences; they are statements written in a formal **knowledge-representation language**.

- A **sentence** is a representation of a piece of knowledge in that language.
- A sentence taken as given (not derived from other sentences) is called an **axiom**.

The KB supports two operations:

| Operation | Meaning |
|-----------|---------|
| **TELL**  | Add a new sentence to the KB. |
| **ASK**   | Query what is currently known. |

Every time a knowledge-based agent is called it does three things:

1. **TELL** the KB about its *percepts* (its inputs from sensors).
2. **ASK** the KB what action it should take — this involves extensive reasoning about the outcomes of possible actions and the current state.
3. **TELL** the KB about the action it chose (so the KB stays up to date), then execute the action.

---

## 2. The Wumpus World

A classic toy environment for demonstrating logical reasoning.

### PEAS (task environment)

**Performance measure**

- `+1000` for climbing out of the cave **with the gold**
- `-1000` for falling into a pit or being eaten by the Wumpus
- `-1` for each action taken
- `-10` for using the arrow

**Environment**

- A `4 × 4` grid of rooms.
- The agent always starts at `[1,1]` facing right.
- Locations of the Wumpus and the gold are random.
- The agent dies if it enters a pit or a square with a live Wumpus.

**Actuators (actions)**

- `Forward`
- `TurnLeft` (by 90°)
- `TurnRight` (by 90°)
- `Grab` — pick up the gold if it is in the current square
- `Shoot` — fire the single arrow; it flies straight and either hits a wall or kills the Wumpus (only **one** arrow)
- `Climb` — leave the cave, only possible from `[1,1]`

**Sensors** — the agent has five, and reports them as a percept vector
`[Stench?, Breeze?, Glitter?, Bump?, Scream?]`:

| Sensor  | Fires when… |
|---------|-------------|
| Stench  | in a square **adjacent** (not diagonal) to the Wumpus |
| Breeze  | in a square **adjacent** to a pit |
| Glitter | in the square that contains the gold |
| Bump    | the agent walks into a wall |
| Scream  | the Wumpus is killed (heard everywhere) |

Example percept: `[Stench, Breeze, None, None, None]`.

### How the Wumpus World is characterised

| Property | Value | Why |
|----------|-------|-----|
| Fully observable? | **No**  | only local perception |
| Deterministic?    | **Yes** | outcomes exactly specified |
| Episodic?         | **No**  | sequential at the level of actions |
| Static?           | **Yes** | Wumpus and pits do not move |
| Discrete?         | **Yes** | grid + discrete actions |
| Single-agent?     | **Yes** | the Wumpus is essentially a natural feature |

**Goal:** discover the locations of the Wumpus, pits, and gold so the agent can navigate to the gold without falling prey to a pit or the Wumpus.

### Symbolic notation used on the maps

`A` = Agent · `B` = Breeze · `G` = Glitter/Gold · `OK` = safe square · `P` = Pit · `S` = Stench · `V` = Visited · `W` = Wumpus.

### A short worked walk (reasoning from percepts)

1. **Percept `[None,None,None,None,None]` at `[1,1]`** → no breeze, no stench, so the neighbours `[1,2]` and `[2,1]` are safe (`OK`). Action: **Forward**.
2. **Percept `[None, Breeze, None, None, None]`** at `[2,1]` → there is a pit adjacent to `[2,1]`. Since `[1,1]` was safe, the pit must be in `[2,2]` or `[3,1]` — not yet decidable. Action: go back and try the other known-safe square `[1,2]`.
3. **Percept `[Stench,None,None,None,None]`** at `[1,2]` → the Wumpus is adjacent. Combined with earlier knowledge the agent can now deduce safe squares and move to `[2,2]`.

The whole point: the agent **deduces** hidden facts (pits, Wumpus) it never directly saw, purely from local percepts + logic.

---

## 3. What "logic" means

**Logical agents** combine the *current percept* with *existing knowledge* (the percept history) and perform logical reasoning to identify state information. Reasoning is done according to the available knowledge about the domain.

**Logics** are formal languages for representing information so that conclusions can be drawn. Two pieces define any logic:

- **Syntax** — the rules for which sentences are *well-formed*.
  *In arithmetic, `x + y = 4` is well-formed; `xy+4=` is not.*
- **Semantics** — the *meaning* of a sentence: it defines the sentence's truth in a *possible world*.
  *In a world where `x=2, y=2`, `x + y = 4` is **true**; in a world where `x=1, y=1`, it is **false**.*

In standard logic, every sentence is either **True** or **False** — never in between.

**Model** — any possible world; i.e. any assignment of truth values to the symbols in the KB. (A model need not match reality.)

- With two sentences `S1`, `S2` there are 4 possible models: `{T,T}`, `{F,T}`, `{T,F}`, `{F,F}`.
- A model **satisfies** a sentence if the sentence is true in it.
- `M(S1)` = the set of models that satisfy `S1`.

**Entailment** — logical reasoning is about *entailment*: a sentence following from another.

> `X ⊨ Y` means **X entails Y**: in *every* model where `X` is true, `Y` is also true.

Wumpus example: the agent is at `[2,1]` and detects a breeze. It cares about `[1,2]`, `[2,2]`, `[3,1]` for its next move. Each may or may not contain a pit → `2³ = 8` possible models. The KB tells us `[1,1]` had no breeze, so `[2,1]` has no pit — and we reason forward from there.

---

## 4. Propositional logic

A **proposition** is the basic building block of logic: a *declarative* sentence that is **either True or False, but not both**. The branch of logic that deals with propositions is **propositional logic**.

The **truth value** of a proposition is `True (T)` if it is a true statement and `False (F)` otherwise.

| Sentence | Proposition? | Truth value |
|----------|--------------|-------------|
| "The sun rises in the East and sets in the West." | Yes | True |
| "1 + 1 = 2" | Yes | True |
| "'b' is a vowel." | Yes | False |
| "Will you go to office today?" | **No** — it's a question | — |
| "X − 3 = 6" | **No** — depends on X | — |

- A **proposition symbol** stands for a proposition. e.g. `W₁,₃` = "Wumpus is in `[1,3]`".
  Symbols are usually uppercase and may carry subscripts: `P, Q, R, W₁,₃, North`.
- A **truth table** is a tabular compilation of *all* combinations of the propositions joined by connectives.

### Syntax

- **Atomic sentence** — a single proposition symbol.
- **Complex sentence** — built from atomic sentences using parentheses and **logical connectives**.
- A **literal** is either an atomic sentence (a *positive* literal) or a negated one (a *negative* literal).

---

## 5. Connectives and truth tables

There are **five** connectives. Operator precedence (highest → lowest):

> `¬`  ,  `∧`  ,  `∨`  ,  `⟹`  ,  `⟺`

So `¬A ∧ B` means `(¬A) ∧ B`, **not** `¬(A ∧ B)`.

### `¬` Negation
"It is not the case that p." `¬p` has the opposite truth value of `p`.

| p | ¬p |
|---|----|
| T | F  |
| F | T  |

### `∧` Conjunction ("p and q")
True only when **both** are true. Parts are called *conjuncts*.

| p | q | p ∧ q |
|---|---|-------|
| T | T | T |
| T | F | F |
| F | T | F |
| F | F | F |

### `∨` Disjunction ("p or q")
True when **either** is true. Parts are called *disjuncts*.

| p | q | p ∨ q |
|---|---|-------|
| T | T | T |
| T | F | T |
| F | T | T |
| F | F | F |

### `⟹` Implication ("if p then q")
`p` = antecedent/premise, `q` = consequent/conclusion. **False only when p is true and q is false.**

| p | q | p ⟹ q |
|---|---|--------|
| T | T | T |
| T | F | F |
| F | T | T |
| F | F | T |

> Why is `p ⟹ q` true whenever `p` is false? The implication only *guarantees* that when `p` is true, `q` follows. When `p` never happens, the implication was never put to the test, so there is no way to call it false — by convention it is **true** ("vacuously true").

### `⟺` Biconditional ("p if and only if q")
True when `p` and `q` have the **same** truth value. Note `p ⟺ q ≡ (p ⟹ q) ∧ (q ⟹ p)`.

| p | q | p ⟺ q |
|---|---|--------|
| T | T | T |
| T | F | F |
| F | T | F |
| F | F | T |

---

## 6. Representing the Wumpus World

For each location `[x,y]`:

- `Px,y` — true if there is a **pit** in `[x,y]`
- `Wx,y` — true if there is a **wumpus** in `[x,y]`
- `Bx,y` — true if the agent perceives a **breeze** in `[x,y]`
- `Sx,y` — true if the agent perceives a **stench** in `[x,y]`

A sample knowledge base (facts + rules):

```
R1 : ¬P1,1                              (no pit in [1,1])
R2 : B1,1 ⟺ (P1,2 ∨ P2,1)               (breeze in [1,1] iff a pit is adjacent)
R3 : B2,1 ⟺ (P1,1 ∨ P2,2 ∨ P3,1)        (breeze in [2,1] iff a pit is adjacent)
R4 : ¬B1,1                              (observed: no breeze in [1,1])
R5 :  B2,1                              (observed: breeze in [2,1])
```

**Query:** `¬P1,2` — is "there is no pit in `[1,2]`" entailed by the KB?

The next four sections prove this *same* query four different ways.

---

## 7. Inference 1 — TT-Entailment

**Model checking**: enumerate every model and check the query in the models where the KB holds.

Procedure to test whether `¬P1,2` is entailed:

1. Collect the relevant symbols: `B1,1, B2,1, P1,1, P1,2, P2,1, P2,2, P3,1`.
2. **Enumerate all models** — every combination of truth values for those symbols.
3. Keep only the models where the **KB is true** (all of `R1…R5` hold).
4. Among those, check whether the **query** `¬P1,2` is true.
5. If the query is true in **every** model where the KB is true → the KB **entails** it. Otherwise it does not.

**Result:** the KB is true in exactly **three** models. In all three, `¬P1,2` is true → **`¬P1,2` is entailed**: there is no pit in `[1,2]`.
By contrast `P2,2` is true in two of the three and false in one, so we **cannot** infer whether `[2,2]` has a pit from this KB.

### Cost of model checking

If the KB and the query `α` together contain `n` symbols there are `2ⁿ` models.

- **Time complexity:** `O(2ⁿ)`
- **Space complexity:** `O(n)` (enumeration is depth-first)

This exponential blow-up is why we want smarter inference methods.

---

## 8. Inference 2 — Theorem proving

**Theorem proving** applies **inference rules** directly to the KB sentences to prove the query — *without* consulting models.

**Logical equivalence:** two sentences `α` and `β` are logically equivalent (`α ≡ β`) if they are true in the same set of models.
*e.g.* `(P1,2 ∨ B2,1) ≡ (B2,1 ∨ P1,2)`.

### Key inference rules

- **Modus Ponens** — from `α ⟹ β` and `α`, infer `β`.
  > If I am tired then I need to rest (`α ⟹ β`); I am tired (`α`); therefore I need to rest (`β`).
- **And-Elimination** — from `α ∧ β` infer `α` (or infer `β`).
  > From `Tired ∧ Sleepy`, infer `Tired` (and also `Sleepy`).
- **Biconditional elimination** — `α ⟺ β` becomes `(α ⟹ β) ∧ (β ⟹ α)`.
- **Contraposition** — `α ⟹ β ≡ ¬β ⟹ ¬α`.
- **De Morgan's laws** — `¬(α ∧ β) ≡ ¬α ∨ ¬β` and `¬(α ∨ β) ≡ ¬α ∧ ¬β`.

### Proof that `¬P1,2` follows

| Step | Sentence | Rule used |
|------|----------|-----------|
| R2  | `B1,1 ⟺ (P1,2 ∨ P2,1)` | given |
| R6  | `(B1,1 ⟹ (P1,2 ∨ P2,1)) ∧ ((P1,2 ∨ P2,1) ⟹ B1,1)` | biconditional elimination |
| R7  | `(P1,2 ∨ P2,1) ⟹ B1,1` | and-elimination |
| R8  | `¬B1,1 ⟹ ¬(P1,2 ∨ P2,1)` | contraposition |
| R9  | `¬(P1,2 ∨ P2,1)` | modus ponens (with R4: `¬B1,1`) |
| R10 | `¬P1,2 ∧ ¬P2,1` | De Morgan |
| R11 | `¬P1,2` | and-elimination ∎ |

---

## 9. Inference 3 — Proof by contradiction

Idea: to prove a query is **true**, *assume its negation* and show the KB then leads to a contradiction (an inference of `FALSE`). A contradiction means the assumption was wrong, so the original query is true.

| If the derived inference is… | …and the assumption was… | …then the given query is… |
|---|---|---|
| `FALSE` | `False` (i.e. we assumed `¬query`) | **TRUE** |
| `TRUE`  | `True`  | query stands |

To prove `¬P1,2`: assume the opposite, `P1,2` (there *is* a pit), add it to the KB, and derive `FALSE`. Since that assumption breaks the KB, `¬P1,2` must hold.

---

## 10. Inference 4 — PL-Resolution via CNF

**Resolution** is a single, complete inference rule that works on sentences in **Conjunctive Normal Form (CNF)**.

### CNF

A formula is in **CNF** if it is a **conjunction (`∧`) of clauses**, where each **clause** is a **disjunction (`∨`) of literals**. (A "product of sums": `∧` between clauses, `∨` inside clauses.)

```
Example CNF:  (A ∨ B) ∧ (A ∨ B ∨ ¬C) ∧ ¬A
Unit clause:  ¬A          (a clause with a single literal)
```

### Converting the KB to CNF

Convert each biconditional/implication step by step. Working `R2` and `R3`:

| Stage | For `R2 : B1,1 ⟺ (P1,2 ∨ P2,1)` | For `R3 : B2,1 ⟺ (P1,1 ∨ P2,2 ∨ P3,1)` |
|-------|-------------------------------|----------------------------------------|
| Biconditional elimination | `(B1,1 ⟹ (P1,2 ∨ P2,1)) ∧ ((P1,2 ∨ P2,1) ⟹ B1,1)` | `(B2,1 ⟹ (P1,1 ∨ P2,2 ∨ P3,1)) ∧ ((P1,1 ∨ P2,2 ∨ P3,1) ⟹ B2,1)` |
| Implication elimination | `¬B1,1 ∨ (P1,2 ∨ P2,1)` and `¬(P1,2 ∨ P2,1) ∨ B1,1` | `¬B2,1 ∨ (P1,1 ∨ P2,2 ∨ P3,1)` and `¬(P1,1 ∨ P2,2 ∨ P3,1) ∨ B2,1` |
| De Morgan (push `¬` in) | `(¬P1,2 ∧ ¬P2,1) ∨ B1,1` | `(¬P1,1 ∧ ¬P2,2 ∧ ¬P3,1) ∨ B2,1` |
| Distribute `∨` over `∧` | `(¬P1,2 ∨ B1,1) ∧ (¬P2,1 ∨ B1,1)` | `(¬P1,1 ∨ B2,1) ∧ (¬P2,2 ∨ B2,1) ∧ (¬P3,1 ∨ B2,1)` |

Resulting clause set:

```
R6  : ¬B1,1 ∨ P1,2 ∨ P2,1
R7  : ¬P1,2 ∨ B1,1
R8  : ¬P2,1 ∨ B1,1
R9  : ¬B2,1 ∨ P1,1 ∨ P2,2 ∨ P3,1
R10 : ¬P1,1 ∨ B2,1
R11 : ¬P2,2 ∨ B2,1
R12 : ¬P3,1 ∨ B2,1
```

(plus the already-simple `R1: ¬P1,1`, `R4: ¬B1,1`, `R5: B2,1`).

### The resolution rule

Two clauses containing *complementary* literals (`ℓ` in one, `¬ℓ` in the other) **resolve** to a new clause with both removed:

```
(P ∨ ℓ)   and   (Q ∨ ¬ℓ)   ⟹   (P ∨ Q)
```

### Refuting the query

To prove `¬P1,2`, add its negation `P1,2` to the clause set and resolve toward the **empty clause `{ }`** (which represents `FALSE`):

```
R4  : ¬B1,1          R7 : ¬P1,2 ∨ B1,1
                     └── resolve on B1,1 ──> ¬P1,2
add  : P1,2          (negated query)
                     └── resolve on P1,2 ──> { }   (empty clause = contradiction)
```

Reaching `{ }` means the assumption `P1,2` is impossible, so **`¬P1,2` is entailed**. ✔

---

## 11. DPLL algorithm

The **Davis–Putnam–Logemann–Loveland (DPLL)** algorithm is a **complete, backtracking-based** search for deciding the **satisfiability** (SAT) of a propositional formula in **CNF**.

Three standard improvements over naive enumeration:

1. **Early termination** — a clause is true as soon as *any* literal is true; the whole formula is false as soon as *any* clause is false. Stop early instead of assigning every symbol.
2. **Pure symbol heuristic** — a symbol that appears with only one "sign" across all clauses (always positive or always negative) is *pure*; assign it the value that makes those clauses true.
3. **Unit clause heuristic** — a clause with a single unassigned literal (a *unit clause*) forces that literal's value; propagate this (unit propagation), which often cascades.

DPLL is the backbone of modern SAT solvers.

---

## 12. Pros & cons of propositional logic

**Pros**

- **Declarative** — knowledge is stated as facts, separate from how it's used.
- Allows **partial / disjunctive / negated** information (unlike most data structures and databases).
- **Compositional** — the meaning of `B1,1 ∧ P1,2` is built from the meanings of `B1,1` and `P1,2`.
- **Context-independent** meaning (unlike natural language, where meaning depends on context).

**Cons**

- **Very limited expressive power.** It cannot naturally state general rules like *"pits cause breezes in adjacent squares"* — you'd need one sentence per square.
- Cannot express quantified statements such as *"Some students are brilliant"* — this is what **predicate (first-order) logic** with quantifiers (`∀`, `∃`) is for, and it is the natural next topic.

---

## 13. Glossary

| Term | Meaning |
|------|---------|
| **KB** | Knowledge base — the set of sentences an agent knows. |
| **Sentence** | A statement in the knowledge-representation language. |
| **Axiom** | A sentence taken as given, not derived. |
| **Percept** | The input an agent receives from its sensors. |
| **Model** | An assignment of truth values to all symbols (a possible world). |
| **Satisfies** | A model *satisfies* a sentence if the sentence is true in it. |
| **Entailment (`⊨`)** | `X ⊨ Y`: `Y` is true in every model where `X` is true. |
| **Proposition** | A declarative statement that is exactly one of True/False. |
| **Literal** | An atomic symbol or its negation. |
| **Clause** | A disjunction (`∨`) of literals. |
| **CNF** | Conjunction (`∧`) of clauses. |
| **Modus Ponens** | From `α ⟹ β` and `α`, infer `β`. |
| **Resolution** | Combine two clauses with complementary literals into a new clause. |
| **DPLL** | Backtracking SAT-solving algorithm on CNF. |
| **SAT** | Satisfiability — does *some* model make the formula true? |

---

### Source

Converted from the Session 9 lecture deck for *Artificial and Computational Intelligence (AIMLCZG557)*, Module M4 — Knowledge Representation using Logics. Slide material is licensed CC BY-NC-SA 4.0.
