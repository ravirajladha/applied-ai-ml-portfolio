# Webinar #4 — Logical Agents & Introduction to Prolog

> Knowledge Representation using **Propositional Logic** and a hands-on introduction to
> **Prolog** — the classic *declarative*, logic-programming language.
> Companion notebook: [`practice.ipynb`](practice.ipynb) (fully solved, pure standard-library Python).

This note follows the webinar deck slide-by-slide and turns every idea into something you
can *run*. Read a section here, then execute the matching cells in the notebook.

---

## 0. The big picture (plain English first)

A **logical agent** is a program that *knows things* and *reasons* about them.

- It stores what it knows in a **Knowledge Base (KB)** — a pile of sentences written in a
  formal logic (so there is no ambiguity).
- It **infers** new facts that must be true given what it already knows.

Two ways to do the "knowing + reasoning" appear in this webinar:

| Approach | What you write | Who does the reasoning |
|----------|----------------|------------------------|
| **Propositional logic** | Sentences built from true/false symbols | You (truth tables, normal forms) or a solver |
| **Prolog** | Facts + rules | The Prolog engine (automatic search) |

---

## 1. Propositional logic — the vocabulary

**Propositional logic** = logic of whole statements that are each simply **true** or **false**.

- **Atom / proposition** — a single true-or-false statement, given a symbol. *e.g.* `R` = "it rains".
- **Literal** — an atom or its negation: `R`, `¬R`.
- **Connectives** — the "glue words":

| Symbol | Name | English | True when… |
|--------|------|---------|------------|
| `¬` | NOT (negation) | "not P" | P is false |
| `∧` | AND (conjunction) | "P and Q" | both true |
| `∨` | OR (disjunction) | "P or Q" | at least one true |
| `→` | IMPLIES (conditional) | "if P then Q" | P false **or** Q true |
| `↔` | IFF (biconditional) | "P if and only if Q" | both sides equal |

**Truth table** — a table listing every possible true/false combination of the atoms and
the resulting value of the whole sentence. With *n* atoms there are `2ⁿ` rows.

The gotcha everyone trips on: `P → Q` is **false only** when `P` is true and `Q` is false.
"If pigs fly, I'm a millionaire" is *true* simply because pigs don't fly.

---

## 2. Formalizing English sentences

Turning words into logic. Key phrases:

- **"unless"** means **"if not"** → `A unless B` becomes `¬B → A` (equivalently `A ∨ B`).
- **"only if"** introduces the **consequent** (right side of `→`). *"P only if Q"* = `P → Q`.
- **"but not both"** signals **exclusive-or (XOR)**.

### Worked examples from the deck

**Example 1** — *"If the alarm is set, then the house is secure, unless the door is unlocked."*
Let `A` = alarm set, `S` = house secure, `D` = door unlocked.

```
(A ∧ ¬D) → S
```
Reading: *if the alarm is set and the door is not unlocked, the house is secure.*
"unless D" carves out an exception, so it becomes `∧ ¬D` on the trigger.

**Example 2** — *"Either the server is down or the network is slow, but not both."*
Let `S` = server down, `N` = network slow. This is **XOR**:

```
(S ∨ N) ∧ ¬(S ∧ N)      ≡      (S ∧ ¬N) ∨ (¬S ∧ N)
```

**Example 3** — *"If it rains or snows, then the match is cancelled unless the stadium is covered."*
Let `R` = rains, `S` = snows, `C` = cancelled, `D` = stadium covered.

```
((R ∨ S) ∧ ¬D) → C
```

The notebook builds each of these and prints its truth table so you can *see* the meaning.

---

## 3. Normal forms — Conjunctive Normal Form (CNF)

A **normal form** is a standard "shape" for a formula. Solvers love CNF because it is
predictable.

> **CNF** = an **AND of clauses**, where each **clause** is an **OR of literals**.

```
(¬A ∨ B) ∧ (¬A ∨ C) ∧ (D ∨ ¬E)
└─ clause ─┘ └─ clause ─┘ └ clause ┘
```

- **Literal** — atom or negation (`A`, `¬A`).
- **Clause** — literals joined by OR (`A ∨ ¬B ∨ C`).
- **CNF** — clauses joined by AND.

### The 4 conversion steps (in order)

| Step | Rule | Rewrite |
|------|------|---------|
| 1. Eliminate `↔` | `A ↔ B` | `(A → B) ∧ (B → A)` |
| 2. Eliminate `→` | `A → B` | `¬A ∨ B` |
| 3. Push `¬` inward | De Morgan | `¬(A ∧ B) → ¬A ∨ ¬B`, `¬(A ∨ B) → ¬A ∧ ¬B`, `¬¬A → A` |
| 4. Distribute `∨` over `∧` | distributive law | `A ∨ (B ∧ C) → (A ∨ B) ∧ (A ∨ C)` |

**Worked example:** `A → (B ∧ C)`
1. no `↔`
2. `¬A ∨ (B ∧ C)`
3. no negations to push
4. `(¬A ∨ B) ∧ (¬A ∨ C)` ← **CNF** ✅

**Already-CNF example:** `(A ∧ B) → C` → `¬(A ∧ B) ∨ C` → `¬A ∨ ¬B ∨ C` (a single clause — already CNF).

The notebook implements all four steps as functions and runs them for you.

### Horn clauses

> A **Horn clause** is a disjunction (clause) with **at most one positive literal**.

*e.g.* `¬A ∨ ¬B ∨ C` (rewrite of `A ∧ B → C`) has one positive literal (`C`). Horn clauses
are exactly what Prolog rules are — which is why Prolog inference is fast.

---

## 4. Textbook problems (AIMA, Chapter 7)

A sentence is:

- **Valid (tautology)** — true in **every** model. *e.g.* `Smoke → Smoke`.
- **Satisfiable** — true in **at least one** model.
- **Unsatisfiable (contradiction)** — true in **no** model.
- **"Neither"** — satisfiable but *not* valid (contingent).

Classic exercise 7.10 — decide valid / neither for each:

| Sentence | Verdict |
|----------|---------|
| a) `Smoke → Smoke` | **Valid** |
| b) `Smoke → Fire` | Neither |
| c) `(Smoke → Fire) → (¬Smoke → ¬Fire)` | Neither |
| d) `Smoke ∨ Fire ∨ ¬Fire` | **Valid** |
| e) `((Smoke ∧ Heat) → Fire) ↔ ((Smoke → Fire) ∨ (Heat → Fire))` | **Valid** |
| f) `Big ∨ Dumb ∨ (Big → Dumb)` | **Valid** |
| g) `(Big ∧ Dumb) ∨ ¬Dumb` | Neither |

**Entailment** (`KB ⊨ α`): the KB entails α when α is true in every model where the KB is
true. Test: `KB ⊨ α` iff `(KB → α)` is **valid**.
The notebook checks, for instance, that `{F → P, D → P}` entails `(F ∧ D) → P`.

The notebook derives every one of these verdicts automatically by building truth tables.

---

## 5. Introduction to Prolog

**Prolog** (PROgramming in LOGic) is **declarative**: you state *what* is true, not *how* to
compute. You give the engine facts and rules, then ask questions (queries); it searches for
answers. Very different from imperative Python/Java/C++.

Official system: **SWI-Prolog** — <https://www.swi-prolog.org/> (free; install and try the
programs below).

### Building blocks

**Facts** — known information (always true):
```prolog
parent(john, mary).
parent(mary, sam).
```

**Rules** — derive new facts. `:-` reads as "if"; commas mean "and":
```prolog
grandparent(X, Y) :-
    parent(X, Z),
    parent(Z, Y).
```
*"X is a grandparent of Y **if** X is a parent of Z **and** Z is a parent of Y."*
Capitalized names (`X`, `Y`, `Z`) are **variables**; lowercase (`john`, `mary`) are **atoms**.

**Terms** — everything in Prolog is a *term*: atoms, numbers, variables, and compound terms
like `parent(john, mary)`.

**Queries** — questions to the engine (the `?-` prompt):
```prolog
?- parent(john, mary).
true.

?- grandparent(john, sam).
true.

?- grandparent(john, Who).
Who = sam.
```

### Two starter programs from the deck

Family relationship:
```prolog
parent(john, mary).
parent(mary, sam).
grandparent(X, Y) :- parent(X, Z), parent(Z, Y).
?- grandparent(john, sam).   % true.
```

Tiny expert system:
```prolog
fever(john).
cough(john).
covid(X) :- fever(X), cough(X).
?- covid(john).              % true.
```

### How Prolog answers a query (the engine's steps)

1. Take the goal (e.g. `covid(john)`).
2. **Match** it against a fact or the *head* of a rule using **unification** (making two
   terms identical by binding variables — e.g. `X = john`).
3. If it matched a rule, replace the goal with the rule's **body** goals and repeat for each.
4. If a path fails, **backtrack** — undo the last choice and try the next matching clause.
5. Succeed when all goals reduce to facts (answer `true`, plus any variable bindings).

This left-to-right, depth-first search with backtracking is called **SLD resolution**.

**Mortal philosophers** — the textbook first-order example, propositionalized to one rule:
```prolog
mortal(X) :- human(X).
human(socrates).
?- mortal(socrates).   % human(socrates)? yes  ⇒  mortal(socrates)? true.
```

The notebook ships a **~40-line pure-Python Prolog engine** (unification + backtracking) and
runs all three programs — so you can watch how the search actually produces the answers,
even without installing SWI-Prolog.

---

## 6. Exercises

1. **Textbook problem** — pick any sentence from the AIMA 7.10 list and confirm its verdict by
   hand, then check yourself against the notebook.
2. **Install SWI-Prolog** (<https://www.swi-prolog.org/>) and run the family and covid
   programs; extend the family tree with more `parent/2` facts and add a `sibling/2` rule.
3. **Bonus** — sketch the **Wumpus World** rules in Prolog (a cell is safe if it has no pit
   and no wumpus; `¬B → adjacent cells have no pit`, etc.).

Solutions to (1) and a `sibling/2` rule for (2) are worked out at the end of the notebook.

---

### Files in this folder
| File | Purpose |
|------|---------|
| `README.md` | This note — the theory, following the webinar deck. |
| `practice.ipynb` | Fully-solved, runnable notebook: propositional-logic toolkit, CNF converter, validity/entailment checker, and a mini Prolog engine. |

*Reference material adapted from AIMA (Russell & Norvig), Ch. 7, and standard Prolog
introductions.*
