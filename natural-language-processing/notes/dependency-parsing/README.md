# Dependency Parsing — Transition-Based (Arc-Eager)

> Study notes + a from-scratch parser. Companion notebook: [`arc_eager_parser.ipynb`](arc_eager_parser.ipynb).

---

## 1. What is dependency parsing?

**Dependency parsing** figures out the **grammatical structure** of a sentence by
connecting words with directed, labelled links. Instead of nesting phrases (like a
constituency tree), it says *which word depends on which*.

- **Head** — the word that governs/controls another (the "parent"). A verb typically
  heads its subject and objects.
- **Dependent** — the word that modifies or completes the head (the "child").
- Every word has **exactly one head** (except the sentence root). The result is a
  **tree** rooted at an artificial `ROOT` node.
- Each link carries a **relation label** describing *how* the dependent relates to the head.

An arc is written **`head → dependent (label)`**.

### Common relation labels

| Label | Meaning | Example (head → dependent) |
|-------|---------|-----------------------------|
| `nsubj` | nominal subject | *sent* → *He* |
| `dobj` | direct object | *sent* → *letter* |
| `iobj` | indirect object | *sent* → *her* |
| `det` | determiner | *letter* → *a* |
| `punct` | punctuation | *sent* → *.* |
| `root` | the head of the whole sentence (attached to `ROOT`) | *ROOT* → *sent* |

> These are **Universal Dependencies (UD)** style labels. Older schemes call `dobj`→`obj`,
> `iobj`→`iobj`; the idea is identical.

---

## 2. Transition-based parsing: the configuration

Rather than searching over all possible trees, a **transition-based** parser reads the
sentence **left to right** and builds the tree by applying a sequence of **actions**
(transitions). It is like a tiny state machine.

The state is called a **configuration** `c = (Stack, Buffer, Arcs)`:

| Part | What it holds | Starts as |
|------|---------------|-----------|
| **Stack** (`σ`) | words we're currently working on (partially processed) | `[ROOT]` |
| **Buffer** (`β`) | words not yet read, left to right | `[w₁, w₂, …, wₙ]` |
| **Arcs** (`A`) | the dependency links committed so far | `{}` (empty) |

- **Initial** configuration: stack `[ROOT]`, buffer = the whole sentence, no arcs.
- **Terminal** configuration: the **buffer is empty** (nothing left to read).
  Everything on the stack (except `ROOT`) already has a head.

A parser consumes a sentence of *n* words in **2n transitions** → **linear time, O(n)**.

---

## 3. Arc-eager transitions

Arc-eager (Nivre, 2003) uses **four** transitions. In every step we look at:

- `s` = **top of the stack**
- `b` = **front of the buffer**

Notation for an added arc: `(head, label, dependent)`.

| Transition | Effect | Precondition |
|------------|--------|--------------|
| **SHIFT** | move `b` from buffer → onto stack | buffer is not empty |
| **LEFT-ARC(l)** | add arc `b →ₗ s` (buffer word is head of stack top); **pop `s`** | `s ≠ ROOT` **and** `s` has **no head yet** |
| **RIGHT-ARC(l)** | add arc `s →ₗ b` (stack top is head of buffer word); **push `b`** onto stack | *(b never has a head yet — always safe)* |
| **REDUCE** | **pop `s`** off the stack (we're done with it) | `s` **already has a head** |

Why "eager"? A **right dependent is attached as soon as it appears** (via `RIGHT-ARC`),
*before* that dependent's own children are known. `REDUCE` later pops it once it can take
no more dependents. This makes parsing **incremental** — arcs are committed early.

### The decision rule (which transition to apply?)

Given the current `(s, b)`, an **oracle** (the "correct answer" during training) picks:

1. **LEFT-ARC(l)** — if the gold tree has `b` as the head of `s`
   *(and `s` has no head yet, `s ≠ ROOT`)*.
2. **RIGHT-ARC(l)** — else if the gold tree has `s` as the head of `b`.
3. **REDUCE** — else if `s` **already has a head** *and* `b` still has a gold link
   (head or dependent) to some word **deeper in the stack** (so `s` is blocking it).
4. **SHIFT** — otherwise (read the next word).

Check the rules **in this order**; the first one whose condition holds wins.
At prediction time a trained classifier replaces the oracle, scoring the four actions
from features of the configuration.

---

## 4. Worked trace — *"He sent her a letter."*

Tokens (with indices): `0 ROOT`, `1 He`, `2 sent`, `3 her`, `4 a`, `5 letter`, `6 .`

**Gold tree we want to build:**

```
ROOT ──root──▶ sent
sent ──nsubj─▶ He
sent ──iobj──▶ her
sent ──dobj──▶ letter
letter ─det──▶ a
sent ──punct─▶ .
```

**Trace** (stack & buffer shown *before* each transition; top of stack = right end):

| Step | Stack | Buffer | Transition | Arc added |
|------|-------|--------|------------|-----------|
| 0 | `[ROOT]` | `[He, sent, her, a, letter, .]` | **SHIFT** | — |
| 1 | `[ROOT, He]` | `[sent, her, a, letter, .]` | **LEFT-ARC(nsubj)** | sent → He (nsubj) |
| 2 | `[ROOT]` | `[sent, her, a, letter, .]` | **RIGHT-ARC(root)** | ROOT → sent (root) |
| 3 | `[ROOT, sent]` | `[her, a, letter, .]` | **RIGHT-ARC(iobj)** | sent → her (iobj) |
| 4 | `[ROOT, sent, her]` | `[a, letter, .]` | **SHIFT** | — |
| 5 | `[ROOT, sent, her, a]` | `[letter, .]` | **LEFT-ARC(det)** | letter → a (det) |
| 6 | `[ROOT, sent, her]` | `[letter, .]` | **REDUCE** | — |
| 7 | `[ROOT, sent]` | `[letter, .]` | **RIGHT-ARC(dobj)** | sent → letter (dobj) |
| 8 | `[ROOT, sent, letter]` | `[.]` | **REDUCE** | — |
| 9 | `[ROOT, sent]` | `[.]` | **RIGHT-ARC(punct)** | sent → . (punct) |
| — | `[ROOT, sent, .]` | `[]` | *(terminal: buffer empty)* | — |

Notice the two `REDUCE` steps (6 and 8): `her` and `letter` were pushed by earlier
`RIGHT-ARC`s, and once they can take no more dependents they must be popped so the
buffer word can reach `sent` beneath them. All **6 gold arcs** are recovered in **10 transitions**.
(Arc-eager takes **≤ 2n** transitions: each of the *n* words enters the stack once via `SHIFT`
or `RIGHT-ARC`, plus one pop — `LEFT-ARC`/`REDUCE` — per word at most. Here n = 6.)

---

## 5. Arc-eager vs arc-standard

Both are transition-based, linear-time, and produce **projective** trees (no crossing arcs),
but they differ in *where* they act and *when* they attach right dependents.

| | **Arc-standard** | **Arc-eager** |
|---|---|---|
| Transitions | 3: SHIFT, LEFT-ARC, RIGHT-ARC | 4: SHIFT, **REDUCE**, LEFT-ARC, RIGHT-ARC |
| Operates on | **top two stack** elements (`s1`, `s2`) | **stack top + buffer front** (`s`, `b`) |
| Right dependents | attached **late** — only after the dependent's *whole subtree* is built (bottom-up) | attached **eagerly** — as soon as the dependent appears, then `REDUCE` later |
| Incrementality | less incremental | **more incremental** (arcs committed early) |
| Terminal | stack = `[ROOT]`, buffer empty | buffer empty |
| Steps | 2n | 2n |

**Rule of thumb:** arc-standard is *bottom-up and lazy*; arc-eager is *eager and incremental*.
Arc-eager's early attachments make it popular and closer to how humans seem to parse
left-to-right — at the cost of needing the extra `REDUCE` action.

---

## 6. Where it's used in practice

- **spaCy** ships a fast **transition-based** dependency parser (a neural, imitation-learning
  variant of these systems). It runs in **linear time O(n)** and parses **incrementally**,
  which is why spaCy is fast enough for production pipelines.
- Classic uses: **information extraction** (subject–verb–object triples), **relation
  extraction**, question answering, grammar checking, and **linguistic/interpretability**
  analysis where you need an explicit structure.

**Why explicit parsing became less common:** large language models learn syntax
*implicitly* from data — they don't need a separate parse tree to answer questions or
extract information, and end-to-end models often beat pipelines that first parse then act.
So a standalone "parse the sentence" step is used less in modern NLP apps.

**Where it still matters:** interpretability and linguistic analysis, low-resource or
domain-specific settings, rule-based/structured extraction where you want an auditable
tree, and anywhere a lightweight CPU-only component beats a heavyweight LLM.

---

## 7. Exam-style quick-reference cheat sheet

**Configuration** `c = (σ Stack, β Buffer, A Arcs)` · start `([ROOT], [w₁…wₙ], {})` ·
terminal = **buffer empty** · `s` = stack top, `b` = buffer front · arc = `(head, label, dep)`.

**Arc-eager transitions & preconditions**

| Action | Does | Precondition |
|--------|------|--------------|
| SHIFT | push `b` onto stack | buffer not empty |
| LEFT-ARC(l) | add `b →ₗ s`; pop `s` | `s ≠ ROOT` and `s` has no head |
| RIGHT-ARC(l) | add `s →ₗ b`; push `b` | *(always ok — `b` has no head yet)* |
| REDUCE | pop `s` | `s` already has a head |

**Oracle order (first match wins):**
`LEFT-ARC` (b is head of s) → `RIGHT-ARC` (s is head of b) →
`REDUCE` (s has head & b links deeper in stack) → else `SHIFT`.

**Mnemonics**
- *LEFT-ARC* attaches a **left** dependent (`s`) and **removes it** immediately.
- *RIGHT-ARC* attaches a **right** dependent (`b`) but **keeps it** (it may get children) — clean up later with *REDUCE*.
- *REDUCE* = "I'm finished with the stack top." Needs the top to already have a head.

**Key facts:** n words → **2n transitions**, **O(n)** time, **projective** trees only.
Arc-standard = top-two-stack, right-dependents-late (3 actions).
Arc-eager = stack-top+buffer, right-dependents-eager + REDUCE (4 actions).

---

*See the companion notebook for a runnable Configuration class, a static oracle, and this
exact trace generated from code.*
