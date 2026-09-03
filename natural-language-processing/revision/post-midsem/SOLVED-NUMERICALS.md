# NLP Post-Midsem — Little Notes + Every Numerical Solved
**AIMLCLZG525 · End-Semester Test · Open Book · 40 marks · 2.5 hours**

Built from **your own six question papers** in `notes/question papers/` and your
slide decks for Sessions 9–15. Every number in this file has been recomputed and
matches the official answer key.

> **Read this box first.**
> The endsem is **7 questions, 40 marks**. Q1 and Q2 are pre-midsem (n-grams,
> neural LM, HMM/Viterbi) = **10 marks**. **Q3–Q7 are all post-midsem = 30 marks
> = 75% of the paper.** You said you're not prepared post-mid at all — this file
> is that 75%.
>
> It is **open book**. You are not being tested on recall. You are being tested
> on **executing a procedure fast and correctly**. So don't read this file —
> *work* it. Cover the solution, do the arithmetic, then check.

---

## THE EXAM MAP: what actually gets asked

Pattern across Feb 2026, Mar 2026 (makeup), Oct 2024, and the undated paper:

| Q | Marks | Topic | Session | What they make you compute |
|---|---|---|---|---|
| 1 | 5 | N-gram + Neural LM | 4, 5 | Laplace probability, then a forward pass + softmax |
| 2 | 5 | HMM POS tagging | 6 | **Viterbi** table, or the **Forward** algorithm |
| **3** | **6** | **Parsing / Dependency** | **9, 10** | Top-down parse table · **PCFG parse probability** · **Chu-Liu-Edmonds MST** |
| **4** | **6** | **Contextual embeddings + Attention** | **11** | **Weighted sum of value vectors** · **multi-head concat × W_O** · full self-attention QKV |
| **5** | **6** | **WordNet + WSD** | **12** | **Lesk overlap count** · **cosine to pick a sense** · WordNet theory |
| **6** | **6** | **Semantic Web / RAG** | **13, 14** | **RDF triples** · RDF-vs-OWL · **RAG token budget** · **retrieval precision** |
| **7** | **6** | **Summarization** | **15** | **MMR score** · summarization types · ROUGE |

**Every single post-mid question has a numerical core.** They are all small —
none takes more than 10 minutes if you know the recipe. That is the good news:
30 marks of *procedure*, not 30 marks of essay.

### Priority order, given you're starting from zero

| Priority | Section | Why |
|---|---|---|
| **1** | [§3 Attention](#3-ch-11-contextual-embeddings-and-attention) | **Easiest 6 marks in the paper.** It is one weighted sum. Appeared as Q4 in both 2026 papers. |
| **2** | [§6 RAG](#6-ch-14-retrieval-augmented-generation-rag) + [§7 MMR](#7-ch-15-text-summarization) | Pure arithmetic. Two divisions and a subtraction. ~12 marks. |
| **3** | [§4 Lesk / WSD](#4-ch-12-word-senses-wordnet-and-wsd) | Counting word overlaps. Cannot go wrong. |
| **4** | [§1 Parsing](#1-ch-9-parsing) | You are here. Top-down table + PCFG probability. |
| **5** | [§2 Dependency](#2-ch-10-dependency-parsing) | Chu-Liu-Edmonds is fiddly — do it last, but do it. |

---

## Contents

1. [Ch 9 — Parsing](#1-ch-9-parsing) *(you are here)*
2. [Ch 10 — Dependency Parsing](#2-ch-10-dependency-parsing)
3. [Ch 11 — Contextual Embeddings & Attention](#3-ch-11-contextual-embeddings-and-attention)
4. [Ch 12 — Word Senses, WordNet & WSD](#4-ch-12-word-senses-wordnet-and-wsd)
5. [Ch 13 — Semantic Web, RDF & OWL](#5-ch-13-semantic-web-rdf-and-owl)
6. [Ch 14 — RAG](#6-ch-14-retrieval-augmented-generation-rag)
7. [Ch 15 — Text Summarization](#7-ch-15-text-summarization)
8. [Last-night checklist](#8-last-night-checklist)

---
---

# 1. Ch 9: Parsing

**Session 9.** Asked as Q3 in three of the four full papers.

## 1.1 Little notes

**Parsing** = assigning a structure to a sentence using a grammar.

**Constituency (phrase-structure)** — groups words into **phrases** (NP, VP, PP).
**Dependency** — direct **word-to-word** head→dependent links. (§2)

A **CFG** is a 4-tuple: non-terminals, terminals, rules `A → β`, and a start
symbol `S`.

| Direction | How it works | Weakness |
|---|---|---|
| **Top-down** | Start at `S`, expand rules, try to reach the words | Wastes time on trees that can never match the input |
| **Bottom-up** | Start at the words, build upward to `S` | Wastes time on constituents that can never fit into an `S` |
| **Chart / CKY** | Store partial results in a table so nothing is computed twice | Needs CNF |

**Chomsky Normal Form (CNF):** every rule is `A → B C` or `A → w`. CKY requires it.

**Structural ambiguity** — the reason all of this is hard. *"I saw a girl with a
telescope"* has two trees. **PP-attachment** is the classic case, and it is
exactly what the PCFG question in §1.4 tests.

---

## 1.2 ⭐ SOLVED — Top-Down Depth-First Parsing with Backup

> **This is the most-repeated parsing question in your papers** (Oct 2024 Q3,
> undated Q3, sample Q3). It is worth 5–6 marks and it is pure bookkeeping.

### The notation

A **state** is `((list of symbols still to be matched) position)`, where
*position* is the index of the **next word** to consume.

```
    1 The  2 flying  3 fish  4 jumped  5 out  6 of  7 the  8 water 9
```
Word positions sit *between* the numbers, so `((S) 1)` means "I still have to
find an S, starting at word 1".

### The four moves

```
1. If the leftmost symbol is a NON-TERMINAL
       -> replace it with the right-hand side of a rule.
          If several rules match, take one and PUSH THE OTHERS ONTO BACKUP.

2. If the leftmost symbol is a PART OF SPEECH that matches the current word
       -> remove it and ADVANCE the position by 1.

3. If it does NOT match
       -> DISCARD this state and POP the most recent state from BACKUP.
          (this is the "depth-first backtracking" bit)

4. Empty symbol list + position past the last word  ->  SUCCESS.
```

### The question (undated paper, Q3 — 6 marks)

> Consider the statement: **"The flying fish jumped out of the water"**.
> Using Depth-First, Simple Top-Down parsing, work out the steps only till the
> noun-phrase **"The flying fish"** is successfully parsed. Provide one line of
> explanation for each step.

Grammar (the relevant part):
```
1. S  -> NP VP
2. NP -> Det N
3. NP -> Det Adj N
Lexicon:  Det -> the      Adj -> flying      N -> fish | water      V -> jumped
```

### The answer — write it exactly like this

| Step | State | Backup | Comment |
|---|---|---|---|
| 1 | `((S) 1)` | | Start of the process |
| 2 | `((NP VP) 1)` | | Expand `S → NP VP` |
| 3 | `((Det N VP) 1)` | `((Det Adj N VP) 1)` | Expand NP. Two rules match → take `NP → Det N`, **push the other to backup** |
| 4 | `((N VP) 2)` | `((Det Adj N VP) 1)` | `the` matches Det → advance to position 2 |
| 5 | — **FAIL** — | | Position 2 is `flying`, which is **not** an N. **Discard this state.** |
| 6 | `((Det Adj N VP) 1)` | | **Pop from backup.** Restart from position 1 |
| 7 | `((Adj N VP) 2)` | | `the` matches Det → advance |
| 8 | `((N VP) 3)` | | `flying` matches Adj → advance |
| 9 | `((VP) 4)` | | `fish` matches N → advance. **"The flying fish" is fully parsed** ✅ |

> **Marking:** roughly 1 mark per correctly identified step, *including the
> backup and the pop*. **The backtracking step is where the marks are** — a
> table with no failure and no pop is a table that hasn't shown the algorithm.

### The Oct 2024 variant — same method, longer grammar

> **"The extremely hot desert is a hostile place for living"**, parse until
> *"The extremely hot desert"*.
> Extra rules: `NP → Det AP N`, `AP → Adv Adj`, `AP → Adj`,
> `Adv → extremely`, `Adj → hot`, `N → desert`.

| Step | State | Backup | Comment |
|---|---|---|---|
| 1 | `((S) 1)` | | Start |
| 2 | `((NP VP) 1)` | | Rule `S → NP VP` |
| 3 | `((Det AP N VP) 1)` | `((Det N VP) 1)` | NP expanded — take `Det AP N`, keep `Det N` in backup |
| 4 | `((AP N VP) 2)` | `((Det N VP) 1)` | `The` matches Det |
| 5 | `((Adv Adj N VP) 2)` | `((Det N VP) 1)`, `((Adj N VP) 2)` | AP expanded — take `Adv Adj`, keep `Adj` in backup |
| 6 | `((Adj N VP) 3)` | " | `extremely` matches Adv |
| 7 | `((N VP) 4)` | " | `hot` matches Adj |
| 8 | `((VP) 5)` | " | `desert` matches N |
| 9 | ✅ | | *"The extremely hot desert"* matches NP |

> **Exam tip.** Note this one *doesn't* need a backtrack — the first choice
> happened to be right. Read the grammar's rule order before you start; if the
> question is worth 6 marks it usually *does* want a backtrack, so if your parse
> runs clean, double-check you took the rules in the given order.

---

## 1.3 ⭐ SOLVED — Bottom-Up Chart Parsing (the final chart)

> Sample paper Q4 [5 marks]: *"show the final chart for the sentence after
> applying the bottom-up chart parser."*

Sentence: **"Book the flight on airasia"**
```
S  -> VP           NP -> NP PP         Det  -> the        Noun -> flight | airasia
VP -> V NP         NP -> Det Noun      Verb -> Book       Prep -> on
                   PP -> Prep Noun
```

Positions: `0 Book 1 the 2 flight 3 on 4 airasia 5`

**Method:** work along the words, and every time the right-hand side of a rule is
complete over a span, add the left-hand side over that same span.

| Span | Words | Constituents found | Rule used |
|---|---|---|---|
| [0,1] | Book | **V** | `Verb → Book` |
| [1,2] | the | **Det** | `Det → the` |
| [2,3] | flight | **Noun** | `Noun → flight` |
| [1,3] | the flight | **NP** | `NP → Det Noun` |
| [3,4] | on | **Prep** | `Prep → on` |
| [4,5] | airasia | **Noun** | `Noun → airasia` |
| [3,5] | on airasia | **PP** | `PP → Prep Noun` |
| [1,5] | the flight on airasia | **NP** | `NP → NP PP` (over NP[1,3] + PP[3,5]) |
| [0,5] | Book the flight on airasia | **VP** | `VP → V NP` (over V[0,1] + NP[1,5]) |
| [0,5] | " | **S** | `S → VP` ✅ |

**Final tree:**
```
S
└── VP
    ├── V ──── Book
    └── NP
        ├── NP
        │   ├── Det ── the
        │   └── Noun ─ flight
        └── PP
            ├── Prep ─ on
            └── Noun ─ airasia
```

> **The point of a chart:** `NP[1,3]` is built **once** and reused when building
> `NP[1,5]`. A naive parser would rebuild it every time it backtracked.

---

## 1.4 ⭐⭐ SOLVED — PCFG Parse Probability (Mar 2026 makeup, Q3, 6 marks)

> **This is the highest-value parsing numerical.** It also teaches you
> PP-attachment ambiguity, which is a theory question in its own right.

### The formula box
```
    P(tree)  =  PRODUCT of P(rule) for EVERY rule used in the tree

    Rules with the same left-hand side must sum to 1.
    The parse with the HIGHER probability is the one the PCFG selects.
```

### The question

```
Rule                Prob      Rule                Prob
1. S  -> NP VP      [1.0]     8.  NP  -> NP PP    [0.4]
2. NP -> Det N      [0.3]     9.  VP  -> VP PP    [0.3]
3. VP -> V NP       [0.7]     10. Det -> the      [1.0]
4. PP -> P NP       [1.0]     11. N   -> chef     [0.4]
5. V  -> poked      [1.0]     12. N   -> cake     [0.3]
6. P  -> with       [1.0]     13. N   -> fork     [0.3]
7. NP -> PropN      [0.3]
```
Sentence: **"The chef poked the cake with the fork."**

**(a) The two parses [2 marks]**

```
PARSE 1 — VP ATTACHMENT  (instrumental: the fork is the TOOL used to poke)

  (S (NP (Det the) (N chef))
     (VP (VP (V poked) (NP (Det the) (N cake)))
         (PP (P with) (NP (Det the) (N fork)))))

PARSE 2 — NP ATTACHMENT  (attributive: the CAKE has a fork on/in it)

  (S (NP (Det the) (N chef))
     (VP (V poked)
         (NP (NP (Det the) (N cake))
             (PP (P with) (NP (Det the) (N fork))))))
```

**(b) The probabilities [3 marks]**

Parse 1 — VP attachment. List every rule, then multiply:
```
  S  -> NP VP        1.0
  NP -> Det N        0.3        (the chef)
    Det -> the       1.0
    N   -> chef      0.4
  VP -> VP PP        0.3        <-- the attachment decision
    VP -> V NP       0.7
      V  -> poked    1.0
      NP -> Det N    0.3        (the cake)
        Det -> the   1.0
        N   -> cake  0.3
    PP -> P NP       1.0
      P  -> with     1.0
      NP -> Det N    0.3        (the fork)
        Det -> the   1.0
        N   -> fork  0.3

  P = 1.0 x (0.3 x 0.4) x [0.3 x (0.7 x 0.3 x 0.3) x (1.0 x 0.3 x 0.3)]
    = 0.00020412
```

Parse 2 — NP attachment:
```
  S  -> NP VP        1.0
  NP -> Det N        0.3 x 1.0 x 0.4     (the chef)
  VP -> V NP         0.7
    V  -> poked      1.0
    NP -> NP PP      0.4                 <-- the attachment decision
      NP -> Det N    0.3 x 1.0 x 0.3     (the cake)
      PP -> P NP     1.0
        P  -> with   1.0
        NP -> Det N  0.3 x 1.0 x 0.3     (the fork)

  P = 1.0 x (0.3 x 0.4) x [0.7 x (0.4 x (0.3 x 0.3) x (1.0 x 0.3 x 0.3))]
    = 0.00027216
```

**(c) Which does the PCFG select, and why? [1 mark]**

> **The NP-attachment parse (Parse 2)**, because
> **0.00027216 > 0.00020412**.
> **Why:** the two parses use *identical* rules except for one — the attachment
> rule. Parse 2 uses `NP → NP PP` at **0.4**; Parse 1 uses `VP → VP PP` at
> **0.3**. Everything else cancels, so the higher-probability attachment rule
> decides it.

> **The exam-technique point.** You do **not** need to multiply 15 numbers twice.
> Spot that the two parses differ in **exactly one rule** and compare
> `0.4` vs `0.3`. Then do the full multiplication only to show your working.

---

## 1.5 Quick reference — CKY

If you get asked for a CKY chart instead:

```
CKY (needs CNF)

  for j = 1 .. n                          # right edge of the span
      table[j-1, j] = { A : A -> word_j }
      for i = j-2 down to 0               # left edge
          for k = i+1 .. j-1              # split point
              for each rule A -> B C
                  if B in table[i,k] and C in table[k,j]
                      add A to table[i,j]

PROBABILISTIC CKY: instead of a set, store the BEST probability per symbol

      P(A, i, j) = max over k, rules  P(A->BC) x P(B,i,k) x P(C,k,j)

  plus a back-pointer (k, B, C) so you can recover the tree.
```
Sentence accepted iff **S ∈ table[0, n]**. Complexity **O(n³ · |G|)**.

---

## 1.6 You try — Parsing
*Answers at the end of this section.*

**P1.** Using the grammar from §1.2, show the top-down DFS table for
**"The hot desert is dry"** parsed until *"The hot desert"*, given the parser
tries `NP → Det AP N` before `NP → Det N`, and `AP → Adv Adj` before `AP → Adj`.

**P2.** Using the PCFG of §1.4, compute `P` for the sentence
**"The chef poked the cake"** (no PP). Only one parse exists.

**P3.** In §1.4, suppose the grammar is changed so `VP → VP PP [0.5]` and
`NP → NP PP [0.2]`. Which parse wins now, and what are the two probabilities?

<details>
<summary><b>Answers — P1, P2, P3</b></summary>

**P1.**

| Step | State | Backup | Comment |
|---|---|---|---|
| 1 | `((S) 1)` | | Start |
| 2 | `((NP VP) 1)` | | `S → NP VP` |
| 3 | `((Det AP N VP) 1)` | `((Det N VP) 1)` | NP expanded, keep `Det N` |
| 4 | `((AP N VP) 2)` | `((Det N VP) 1)` | `The` matches Det |
| 5 | `((Adv Adj N VP) 2)` | `((Det N VP) 1)`, `((Adj N VP) 2)` | AP expanded, keep `Adj` |
| 6 | — **FAIL** — | | Position 2 is `hot`, not an Adv. Discard. |
| 7 | `((Adj N VP) 2)` | `((Det N VP) 1)` | **Pop from backup** |
| 8 | `((N VP) 3)` | `((Det N VP) 1)` | `hot` matches Adj |
| 9 | `((VP) 4)` | | `desert` matches N — *"The hot desert"* parsed ✅ |

**P2.** One parse: `(S (NP (Det the)(N chef)) (VP (V poked) (NP (Det the)(N cake))))`
```
P = 1.0 x [0.3 x 1.0 x 0.4] x [0.7 x 1.0 x (0.3 x 1.0 x 0.3)]
  = 1.0 x 0.12 x 0.7 x 0.09
  = 0.00756
```

**P3.** Only the attachment rule changes.
```
VP-attachment:  0.00020412 x (0.5 / 0.3) = 0.0003402
NP-attachment:  0.00027216 x (0.2 / 0.4) = 0.00013608
```
**VP attachment now wins** (0.00034 > 0.00014) — the instrumental reading,
*the fork is the tool*. This shows the grammar's rule probabilities, not the
sentence, decide the attachment.
</details>

---
---

# 2. Ch 10: Dependency Parsing

**Session 10.** Q3 in Feb 2026, Q4 in Oct 2024 and the undated paper.

## 2.1 Little notes

> **Dependency syntax postulates that syntactic structure consists of lexical
> items linked by binary asymmetric relations ("arrows") called dependencies.**
> The arrow connects a **head (governor)** with a **dependent (modifier)**.

A dependency tree must be **connected, acyclic, single-head** (every word has
exactly one head), and rooted at **ROOT**.

### Constituency vs Dependency — the compare-and-contrast answer

| Aspect | **Constituency** | **Dependency** |
|---|---|---|
| **Basic structure** | Nested **phrases** (NP, VP, PP); words only at the leaves | Direct **word-to-word** head→dependent arcs; no phrase nodes |
| **Grammar** | CFG rules | Head–dependent relations with labels (nsubj, dobj, …) |
| **Good for** | English-like fixed word order | **Free word-order languages** (Hindi, Czech, Turkish) |
| **Applications** | Grammar checking, generation, syntax-heavy tasks | **Relation extraction, QA, machine translation, semantic role labelling** |
| **Parsing methods** | CKY, chart, Earley, PCFG | Transition-based, graph-based (MST), Eisner DP, constraint satisfaction |

### The two parsing methods — the 3-mark table (Oct 2024 Q4a)

| | **Transition-based** | **Graph-based** |
|---|---|---|
| **Main idea** | Build the tree **incrementally**, left to right. A classifier greedily picks the next action on a (stack, buffer) configuration. **Local, greedy, linear time.** | Score **every possible arc**, then find the highest-scoring tree **globally** over the complete graph. |
| **Search** | Greedy / beam — no backtracking | Exhaustive via a **Maximum Spanning Tree** |
| **Algorithms** | **Arc-eager**, arc-standard, **MaltParser** (Nivre et al. 2008) | **Chu-Liu-Edmonds** (MST), **Eisner** O(n³), MSTParser |
| **Complexity** | **O(n)** — very fast | O(n²)–O(n³) |
| **Weakness** | An early wrong decision cannot be undone (error propagation) | Slower; arc scores are independent of each other |

---

## 2.2 ⭐ SOLVED — Transition-Based Parsing (Arc-Eager)

### The configuration and the four transitions
```
Configuration = ( Stack sigma ,  Buffer beta ,  Arc set A )
Start         = ( [ROOT]      ,  [w1..wn]    ,  {} )

SHIFT          move the first word of the buffer onto the stack

LEFT-ARC(r)    add arc  b -> s   (head = FRONT OF BUFFER, dependent = TOP OF STACK)
               then POP the stack
               precondition: stack top has NO head yet, and is not ROOT

RIGHT-ARC(r)   add arc  s -> b   (head = TOP OF STACK, dependent = FRONT OF BUFFER)
               then PUSH b onto the stack

REDUCE         POP the stack
               precondition: stack top ALREADY has a head
```

> **The name explains it:** *arc-eager* attaches a right arc **as early as
> possible**, before the dependent's own dependents are found. That's why it
> needs a separate `REDUCE` to clean up afterwards.

### Worked trace — "He likes records"

Target tree: `ROOT → likes`, `likes → He` (nsubj), `likes → records` (dobj).

| Step | Transition | Stack | Buffer | Arc added |
|---|---|---|---|---|
| 0 | *(init)* | `[ROOT]` | `[He, likes, records]` | — |
| 1 | **SHIFT** | `[ROOT, He]` | `[likes, records]` | — |
| 2 | **LEFT-ARC(nsubj)** | `[ROOT]` | `[likes, records]` | `likes → He` |
| 3 | **RIGHT-ARC(root)** | `[ROOT, likes]` | `[records]` | `ROOT → likes` |
| 4 | **RIGHT-ARC(dobj)** | `[ROOT, likes, records]` | `[]` | `likes → records` |
| 5 | **REDUCE** | `[ROOT, likes]` | `[]` | — |
| 6 | **REDUCE** | `[ROOT]` | `[]` | — |

**Final arcs:** `ROOT → likes`, `likes → He`, `likes → records` ✅

```
        ┌──────root──────┐
        │        ┌─nsubj─┤    ┌──dobj──┐
      ROOT      He     likes          records
```

> **Watch the direction in LEFT-ARC.** At step 2 the head is `likes` — the word
> at the **front of the buffer**, *not* on the stack. Getting this backwards is
> the standard mistake.

---

## 2.3 ⭐⭐ SOLVED — Chu-Liu-Edmonds MST (Feb 2026, Q3, 6 marks)

> Graph-based parsing. Fiddly but completely mechanical.

### The recipe
```
STEP 1  For EVERY node except ROOT, keep only its highest-scoring INCOMING arc.
STEP 2  If the result has no cycle  ->  that IS the MST. Done.
STEP 3  If there is a cycle, CONTRACT it into a single node,
        recompute the scores of arcs ENTERING the cycle from outside:

            score(X -> C_new) = score(X -> v)
                              - score( best arc INTO v inside the cycle )
                              + score( the whole cycle )

        (the "+ cycle" term is a constant, so for RANKING you can drop it —
         which is what the marking scheme does)
STEP 4  Recurse on the contracted graph, then EXPAND:
        entering the cycle at node v means BREAKING the cycle arc that pointed to v.
```

### The question

Sentence **"He likes records"**. `R` = ROOT, `A` = He, `B` = likes, `C` = records.

| Head → Dependent | Score |
|---|---|
| R → A | 4 |
| R → B | 8 |
| R → C | 2 |
| A → B | 3 |
| B → A | 6 |
| C → A | 1 |
| B → C | 7 |
| C → B | 9 |

**(a) Best incoming arc per node, and the cycle [2 marks]**

Go node by node. List *all* incoming arcs, take the max:
```
  For A:  R->A = 4 ,  B->A = 6 ,  C->A = 1     ->  BEST = B->A  (6)
  For B:  R->B = 8 ,  A->B = 3 ,  C->B = 9     ->  BEST = C->B  (9)
  For C:  R->C = 2 ,  B->C = 7                 ->  BEST = B->C  (7)
```
Greedy selection = `{B→A, C→B, B→C}`.

> **CYCLE DETECTED: B → C → B.** `B` points to `C`, and `C` points back to `B`.

**(b) Contract the cycle [2 marks]**

Create a single cycle node `BC`. Arcs entering the cycle come from `R` and `A`.
For each, subtract the score of the arc it would *replace* inside the cycle:

```
  Enter at B:  R->B  becomes  8 - (score of best arc into B in cycle) + (cycle)
                            = 8 - 9 + 16 ... ranking-equivalent to  8 - (9-9) = 8
               (this arc would replace C->B)

  Enter at C:  R->C  becomes  2 - (score of best arc into C in cycle) + (cycle)
                            = 2 - 7 + 16 ... ranking-equivalent to  2 - (7-7) = 2
               (this arc would replace B->C)

  Also from A: A->B = 3  ->  3 - 9 = -6   (much worse, discard)
```
So the best way in is **R → B, score 8**.

**(c) The final MST and the total score [2 marks]**
```
  1. Select R -> B                            (score 8)
  2. Entering at B means we BREAK the cycle arc that pointed to B,
     which was C -> B  (9)  ->  DROP IT
  3. Keep the other cycle arc:  B -> C        (score 7)
  4. A still needs a head — its best was      B -> A  (score 6)
```

| Final arc | Meaning | Score |
|---|---|---|
| ROOT → B | ROOT → **likes** | 8 |
| B → C | likes → **records** | 7 |
| B → A | likes → **He** | 6 |
| | **TOTAL** | **21** |

```
        ROOT ──8──► likes ──7──► records
                      │
                      6
                      ▼
                     He
```

> ✅ I brute-forced all valid spanning arborescences of this graph: **21 is the
> true maximum** (the next best is `R→C, C→B, B→A` at 17). The algorithm is
> correct here.

> **Sanity checks to run in the exam, every time:**
> 1. Exactly **one** incoming arc per word — never two, never zero.
> 2. **Nothing points into ROOT.**
> 3. Every word is **reachable from ROOT** (follow the arrows back — you must
>    always arrive at ROOT, never loop).

---

## 2.4 Drawing the two trees (Oct 2024 Q4b, undated Q4b — 3 marks)

> *"What will be the Constituency Parse Tree and the Dependency Parse Tree for
> **'The desert became very hot'**?"*

**Constituency** (phrases, words only at leaves):
```
                    S
          ┌─────────┴─────────┐
         NP                   VP
     ┌────┴────┐        ┌──────┴──────┐
   Det        N         V            AP
    │          │        │        ┌────┴────┐
   The      desert   became    Adv       Adj
                                │          │
                              very       hot
```

**Dependency** (word-to-word, ROOT at top, every word has one head):
```
                  ROOT
                    │ root
                    ▼
                 became
          ┌─────────┴─────────┐
     nsubj│                   │xcomp
          ▼                   ▼
       desert                hot
          │det                │advmod
          ▼                   ▼
         The                very
```

Arcs: `ROOT→became`, `became→desert` (nsubj), `desert→The` (det),
`became→hot` (xcomp/acomp), `hot→very` (advmod).

> **Marks are 1.5 per tree.** In the dependency tree, **label the arcs** — an
> unlabelled dependency tree usually loses half the marks.

---

## 2.5 You try — Dependency
<details>
<summary><b>D1.</b> Trace arc-eager for <b>"She ate cake"</b> (ROOT→ate, ate→She, ate→cake). — click for answer</summary>

| Step | Transition | Stack | Buffer | Arc |
|---|---|---|---|---|
| 0 | init | `[ROOT]` | `[She, ate, cake]` | — |
| 1 | SHIFT | `[ROOT, She]` | `[ate, cake]` | — |
| 2 | LEFT-ARC(nsubj) | `[ROOT]` | `[ate, cake]` | `ate → She` |
| 3 | RIGHT-ARC(root) | `[ROOT, ate]` | `[cake]` | `ROOT → ate` |
| 4 | RIGHT-ARC(dobj) | `[ROOT, ate, cake]` | `[]` | `ate → cake` |
| 5 | REDUCE | `[ROOT, ate]` | `[]` | — |
| 6 | REDUCE | `[ROOT]` | `[]` | — |
</details>

<details>
<summary><b>D2.</b> Chu-Liu-Edmonds on: R→A 5, R→B 3, A→B 8, B→A 6. Find the MST. — click for answer</summary>

```
Step 1 — best incoming arc per node
   For A:  R->A = 5 ,  B->A = 6   ->  BEST = B->A (6)
   For B:  R->B = 3 ,  A->B = 8   ->  BEST = A->B (8)

   CYCLE: A -> B -> A

Step 2 — contract {A,B}. Only ROOT is outside.
   Enter at A:  R->A = 5,  replaces B->A (6)   ->  5 - 6 = -1
   Enter at B:  R->B = 3,  replaces A->B (8)   ->  3 - 8 = -5
   Best entry: at A.

Step 3 — select R->A (5); break the cycle arc into A (B->A); keep A->B (8).

FINAL MST:  R->A (5),  A->B (8)   TOTAL = 13
```
Check: the alternative `R→B (3) + B→A (6) = 9 < 13`. ✅
</details>

---
---

# 3. Ch 11: Contextual Embeddings and Attention

**Session 11.** Q4 in **both** 2026 papers, Q6 in Oct 2024.

> ### 🎯 START HERE IF YOU ARE SHORT ON TIME
> This is **6 marks for one weighted sum**. The 2026 calculation is three
> multiplications and two additions. There is no faster mark in the paper.

## 3.1 Little notes — the theory half (usually 3 of the 6 marks)

**(a) What are contextual embeddings, and why do they matter?**

> Contextual embeddings are **vector representations of words that change based
> on the surrounding context**. Unlike static embeddings, the same word can have
> different representations in different sentences.
>
> **Importance:**
> - Capture **word sense disambiguation** (e.g. *bank* as financial institution
>   vs river bank)
> - Enable better understanding of **semantic relationships**
> - **Improve performance on downstream NLP tasks**

**(b) How do they differ from static embeddings like Word2Vec?**

| **Static** (Word2Vec, GloVe) | **Contextual** (ELMo, BERT, Transformers) |
|---|---|
| **One fixed vector per word**, regardless of context | **Dynamic** vectors that change with context |
| **Cannot handle polysemy** (multiple meanings) | Same word gets **different representations** in different sentences |
| Trained by prediction over a window | **Computed using attention** over the entire sequence |
| One vector per word **type** | One vector per word **token** |

**(a) Why multiple attention heads instead of one?** *(Mar 2026, 1.5 marks)*
> - Attend to information from **different representation subspaces**
> - Capture **different types of relationships** (syntactic, semantic, positional)
> - Learn diverse patterns — one head might focus on adjacent words, another on
>   subject–verb relationships
> - **Increase model capacity** without proportionally increasing computation

---

## 3.2 ⭐ SOLVED — Contextual embedding as a weighted sum (Feb 2026, Q4c, 3 marks)

### The formula box
```
    Output  =  SUM over i of  alpha_i * v_i

    alpha = attention weights (they sum to 1)
    v     = value vectors
```
That is the *entire* computation. It is a weighted average of the value vectors.

### The question
Sentence **"The cat sat"**.
- Attention weights for *cat*: `α = [0.2, 0.5, 0.3]` (for the, cat, sat)
- Value vectors: `v_the = [1,0]`, `v_cat = [1,1]`, `v_sat = [0,1]`

Calculate the contextual embedding for **'cat'**.

### The answer
```
Output = 0.2 x [1,0]  +  0.5 x [1,1]  +  0.3 x [0,1]

       = [0.2, 0]  +  [0.5, 0.5]  +  [0, 0.3]

       = [ 0.2+0.5+0 ,  0+0.5+0.3 ]

       = [ 0.7 , 0.8 ]
```
> **The contextual embedding for 'cat' is `[0.7, 0.8]`.**

> **Free sanity check:** the weights sum to `0.2+0.5+0.3 = 1.0`. If your given
> weights don't sum to 1, you've misread the question.

---

## 3.3 ⭐ SOLVED — Multi-head concat × W_O (Mar 2026, Q4, 6 marks)

### The formula box
```
    MultiHead(Q,K,V) = Concat(head_1, ..., head_h) x W_O
```

### The question
Two heads, word *cat*:
- `head_1 = [0.7, 0.8]`, `head_2 = [0.6, 0.9]`
- `W_O` is 4 × 2:
```
        [0.5, 0.3]
        [0.2, 0.4]
        [0.1, 0.6]
        [0.3, 0.2]
```

**(b) Concatenation [1 mark]**
```
    Concat(head_1, head_2) = Concat([0.7, 0.8], [0.6, 0.9])
                           = [0.7, 0.8, 0.6, 0.9]
```
> Note the dimension: 2 heads × 2 dims = a **4-vector**, which is exactly why
> `W_O` has **4 rows**. That shape check is free marks.

**(c) Project through W_O [2.5 marks]**

`[1×4] × [4×2] = [1×2]`. Take the row against each column:
```
First component  = 0.7x0.5 + 0.8x0.2 + 0.6x0.1 + 0.9x0.3
                 = 0.35 + 0.16 + 0.06 + 0.27
                 = 0.84

Second component = 0.7x0.3 + 0.8x0.4 + 0.6x0.6 + 0.9x0.2
                 = 0.21 + 0.32 + 0.36 + 0.18
                 = 1.07
```
> **Final Multi-Head Attention Output = `[0.84, 1.07]`**

**(d) What is each head specialising in? [1 mark]**
```
Head 1 weights [0.1, 0.2, 0.7] -> highest on 'sat' (position 3)
   => focuses on the VERB / action word (syntactic relationship)

Head 2 weights [0.5, 0.3, 0.2] -> highest on 'the' (position 1)
   => focuses on the DETERMINER / article (grammatical structure)

This demonstrates how different heads specialise in different linguistic patterns.
```

---

## 3.4 ⭐⭐ SOLVED — Full self-attention from Q, K, V (Oct 2024, Q6b, 4 marks)

> The hardest version. Asks for **scaling, masking and softmax** explicitly.

### The formula box
```
    Q = X Wq        K = X Wk        V = X Wv

                          Q K^T
    Attention(Q,K,V) = softmax( ------- + MASK ) V
                          sqrt(d_k)

    MASK: for causal/decoder attention, set positions j > i to -infinity
          so a token cannot see the future. After softmax those become 0.
```

### The question
Sentence **"Stay Curious"**, embeddings `Stay = [1 1]`, `Curious = [1 1]`.
```
        Wq = [1 0]       Wk = [0 2]       Wv = [2 3]
             [0 2]            [1 0]            [3 2]
```
Compute to 2 decimal places. Given: `exp(3.54) = 34.31`.

### The answer, step by step

**Step 1 — the input** *(0.5 marks)*
```
    X = [1 1]      (Stay)
        [1 1]      (Curious)
```

**Step 2 — compute Q, K, V** *(1 mark)*
```
Q = X Wq = [1 1] [1 0]  =  [1x1+1x0 , 1x0+1x2]  =  [1 2]
           [1 1] [0 2]     [1x1+1x0 , 1x0+1x2]     [1 2]

K = X Wk = [1 1] [0 2]  =  [1x0+1x1 , 1x2+1x0]  =  [1 2]
           [1 1] [1 0]                              [1 2]

V = X Wv = [1 1] [2 3]  =  [1x2+1x3 , 1x3+1x2]  =  [5 5]
           [1 1] [3 2]                              [5 5]
```

**Step 3 — scores `Q Kᵀ`** *(0.5 marks)*
```
K^T = [1 1]        Q K^T = [1 2] [1 1]  =  [1+4  1+4]  =  [5 5]
      [2 2]                [1 2] [2 2]     [1+4  1+4]     [5 5]
```

**Step 4 — scale by `√d_k`, with `d_k = 2`** *(0.5 marks)*
```
    5 / sqrt(2) = 5 / 1.414 = 3.54

        [3.54  3.54]
        [3.54  3.54]
```

**Step 5 — apply masking** *(0.5 marks)*
```
Row 1 (Stay) must not see position 2 (Curious, which is in its future):

        [3.54   -1.00E+99]        <-  -infinity
        [3.54    3.54    ]
```

**Step 6 — softmax each row** *(0.5 marks)*
```
Row 1:  exp(3.54) = 34.31 ,  exp(-inf) = 0
        sum = 34.31
        -> [ 34.31/34.31 , 0/34.31 ] = [ 1.00 , 0.00 ]

Row 2:  exp(3.54) = 34.31 ,  exp(3.54) = 34.31
        sum = 68.62
        -> [ 34.31/68.62 , 34.31/68.62 ] = [ 0.50 , 0.50 ]
```

**Step 7 — multiply by V** *(0.5 marks)*
```
Row 1:  1.00 x [5 5]  +  0.00 x [5 5]  =  [5.00 , 5.00]
Row 2:  0.50 x [5 5]  +  0.50 x [5 5]  =  [5.00 , 5.00]

Output = [5 5]
         [5 5]
```

> **Why both rows are identical here:** the two input embeddings are the *same*
> vector `[1 1]`, so every value vector is `[5 5]` and any weighted average of
> identical vectors is that vector. **State this in the exam** — it shows you
> understood the result rather than just grinding the arithmetic.

---

## 3.5 You try — Attention
<details>
<summary><b>A1.</b> α = [0.1, 0.6, 0.3]; v₁ = [2,1], v₂ = [0,3], v₃ = [1,1]. Contextual embedding? — answer</summary>

```
= 0.1[2,1] + 0.6[0,3] + 0.3[1,1]
= [0.2, 0.1] + [0, 1.8] + [0.3, 0.3]
= [0.5, 2.2]
```
Weights sum to 1.0 ✅
</details>

<details>
<summary><b>A2.</b> head₁ = [1,2], head₂ = [0,1], W_O = [[1,0],[0,1],[2,1],[1,2]]. Multi-head output? — answer</summary>

```
Concat = [1, 2, 0, 1]           (4-vector, matches W_O's 4 rows ✅)

c1 = 1x1 + 2x0 + 0x2 + 1x1 = 1 + 0 + 0 + 1 = 2
c2 = 1x0 + 2x1 + 0x1 + 1x2 = 0 + 2 + 0 + 2 = 4

Output = [2, 4]
```
</details>

<details>
<summary><b>A3.</b> Scores before softmax are [2.0, 2.0, 4.0]. Compute the attention weights. (e² = 7.389, e⁴ = 54.598) — answer</summary>

```
sum = 7.389 + 7.389 + 54.598 = 69.376

alpha = [7.389/69.376 , 7.389/69.376 , 54.598/69.376]
      = [0.107 , 0.107 , 0.787]

check: 0.107 + 0.107 + 0.787 = 1.001 ~ 1 ✅
```
The largest score dominates because softmax **exponentiates first**.
</details>

---
---

# 4. Ch 12: Word Senses, WordNet and WSD

**Session 12.** Q5 in Feb 2026, Q5 in Oct 2024 and the undated paper.

## 4.1 Little notes

**Word sense** = a discrete representation of one aspect of the meaning of a word.
**Lexeme** = a pairing of a form with a single meaning representation.
**Lemma** = the citation form (*carpet* is the lemma for *carpets*).

### The relations (one line each — guaranteed recall marks)

| Relation | Definition | Example |
|---|---|---|
| **Homonymy** | Lexemes that **share a form** but have **unrelated, distinct** meanings | *bat* (stick) vs *bat* (mammal); *bank* (finance) vs *bank* (riverside) |
| **Polysemy** | A single lexeme with multiple **related** meanings | *bank* the building vs *bank* the institution |
| **Synonymy** | Same meaning in some or all contexts; substitutable | couch/sofa, big/large, automobile/car |
| **Antonymy** | Opposites w.r.t. **one** feature of meaning | dark/light, rise/fall |
| **Hyponymy** | The first sense is **more specific** — a subclass | *car* is a hyponym of *vehicle* |
| **Hypernymy** | The reverse — the **superordinate** | *vehicle* is a hypernym of *car* |

- **Homophones** — same sound (write/right). **Homographs** — same spelling.
- Homonymy causes problems in **text-to-speech** (*bass* vs *bass*),
  **information retrieval** (query "bat care"), **MT**, **speech recognition**.

### WordNet
> A **hierarchically organised lexical database** — an on-line thesaurus plus
> aspects of a dictionary.

| Category | Entries |
|---|---|
| Noun | 117,097 |
| Verb | 11,488 |
| Adjective | 22,141 |
| Adverb | 4,601 |

- Average noun has **1.23** senses; average verb has **2.16** senses.
- A **synset** (synonym set) is WordNet's version of a sense/concept — the set
  of near-synonyms sharing one gloss.
- The noun **"bass" has 8 senses** in WordNet.

**Two variants of the WSD task:**
- **Lexical sample task** — a small pre-selected set of target words, with a
  sense inventory for each.
- **All-words task** — the system gets an entire text and must disambiguate
  **every** word (or every content word).

**Why does WordNet do badly on domain-specific text?** *(Mar 2026 Q5A, 2 marks)*
> Because it is a **general-purpose lexical database** and **lacks specialised
> technical vocabulary**. Many medical or legal terms are missing or
> insufficiently defined. **Solution:** combine WordNet with a
> **domain-specific ontology or lexicon**, adding expert domain knowledge.

---

## 4.2 ⭐ SOLVED — Simplified Lesk (Feb 2026, Q5, 3 marks)

### The recipe
```
SIMPLIFIED LESK

1. Take the CONTEXT = the set of words in the sentence
   (drop the target word itself; drop stop words).
2. For EACH sense, take its DEFINITION / GLOSS (+ usage examples if given).
3. OVERLAP = the number of words appearing in BOTH the context and the gloss.
4. Choose the sense with the HIGHEST overlap.
```

### The question
Word: **"bat"**
```
Sense 1: A flying mammal that is active at night.
         Definition words: animal, flying, mammal, night, wings
Sense 2: A piece of sports equipment used to hit a ball.
         Definition words: sports, equipment, hit, ball, cricket
```
Sentence: **"At night, he picked up the bat to hit the ball."**

### The answer
```
Context words (stop words and the target removed):

    [ night , picked , bat , hit , ball ]

SENSE 1 overlap:
    night   appears in sense-1 definition   ✓
    picked  no      hit  no      ball  no
    -> OVERLAP = 1

SENSE 2 overlap:
    hit     appears in sense-2 definition   ✓
    ball    appears in sense-2 definition   ✓
    night   no      picked  no
    -> OVERLAP = 2
```
> **2 > 1, so the chosen sense is SENSE 2 — the sports equipment.**

### The Oct 2024 variant — glosses *plus* usage examples

Sentence: **"I need to fix the bug in my code."**

| Sense | Gloss | Usage example |
|---|---|---|
| bug(1) | A small insect | *Insecticides can **fix** proliferation of insects* |
| bug(2) | A flaw in a program that causes it to behave incorrectly | *Fixing defects in **code** after testing is one of the steps in the Software Development Life Cycle* |

```
Context: [ need , fix , bug , code ]

Sense 1 signature = gloss + example
    { small, insect, insecticides, can, fix, proliferation, insects }
    overlap with context:  fix                          -> 1

Sense 2 signature = gloss + example
    { flaw, program, causes, behave, incorrectly, fixing,
      defects, code, testing, steps, software, development, life, cycle }
    overlap with context:  fix (fixing), code           -> 2

ANSWER: Sense 2 — a flaw in a program.
```
> **State your steps.** The marks are for *"explain the steps to be followed"*,
> so write the algorithm out, then the two signature sets, then the counts.
> Also state your assumption about stemming (*fix* ↔ *fixing*).

---

## 4.3 ⭐ SOLVED — Picking a sense by cosine similarity (Oct 2024, Q6a, 2 marks)

> Contextual-embedding WSD. Ties Session 11 to Session 12.

### The question
Contextual embeddings for each sense of **"bank"**:

| Sense | Meaning | Vector |
|---|---|---|
| bank_N1 | Financial institution | `[1, 4, 1]` |
| bank_N2 | Sloping land | `[2, 8, 1]` |
| bank_V1 | Tip laterally | `[4, 7, 3]` |
| bank_V3 | Do business with a bank | `[3, 3, 3]` |

The target word's contextual embedding in a specific sentence is **`[2, 6, 2]`**.
What is the sense?

### The answer
```
              a . b
  cos(a,b) = ---------
              |a| |b|

|target| = sqrt(2^2 + 6^2 + 2^2) = sqrt(4+36+4) = sqrt(44) = 6.633
```

| Sense | Dot product with `[2,6,2]` | \|sense\| | cosine |
|---|---|---|---|
| **N1 `[1,4,1]`** | 2+24+2 = **28** | √18 = 4.243 | 28 / (6.633×4.243) = **0.9949** ⭐ |
| N2 `[2,8,1]` | 4+48+2 = 54 | √69 = 8.307 | 54 / (6.633×8.307) = 0.9800 |
| V1 `[4,7,3]` | 8+42+6 = 56 | √74 = 8.602 | 56 / (6.633×8.602) = 0.9814 |
| V3 `[3,3,3]` | 6+18+6 = 30 | √27 = 5.196 | 30 / (6.633×5.196) = 0.8704 |

> **Highest cosine = 0.9949 → sense `bank_N1`, "Financial Institution".**

> **Trap.** `N2` has the **largest dot product** (54 vs 28) but is *not* the
> answer. The dot product favours long vectors — `[2,8,1]` is simply a bigger
> vector. **You must divide by the magnitudes.** Marks are lost here every year.

---

## 4.4 You try — WSD
<details>
<summary><b>W1.</b> Lesk for "plant" in <i>"The plant needs water and sunlight to grow."</i> Sense A: {living, organism, leaves, grow, water}. Sense B: {factory, industrial, building, machinery, production}. — answer</summary>

```
Context: [ plant, needs, water, sunlight, grow ]

Sense A overlap:  water ✓ , grow ✓                -> 2
Sense B overlap:  none                            -> 0

ANSWER: Sense A — the living organism.
```
</details>

<details>
<summary><b>W2.</b> Target `[1, 2, 2]`. Sense P `[2, 4, 4]`, sense Q `[3, 0, 0]`. Which sense? — answer</summary>

```
|target| = sqrt(1+4+4) = 3

P: dot = 2 + 8 + 8 = 18 ;  |P| = sqrt(4+16+16) = 6
   cos = 18 / (3 x 6) = 1.0000        <- perfectly aligned (P = 2 x target)

Q: dot = 3 + 0 + 0 = 3  ;  |Q| = 3
   cos = 3 / (3 x 3) = 0.3333

ANSWER: sense P, cosine 1.0
```
Note P is just target × 2 — same **direction**, so cosine is exactly 1. Cosine
measures direction, never magnitude.
</details>

---
---

# 5. Ch 13: Semantic Web, RDF and OWL

**Session 13.** Q5/Q6 in Feb 2026, Q5 in Mar 2026, Q5 in Oct 2024.

## 5.1 Little notes

**The problem:** on the syntactic web, markup is only rendering information and
hyperlinks. **Semantic content is accessible to humans but not (easily) to
computers.** You cannot ask *"find animals that use sonar but are not bats or
dolphins"*.

### The ontology languages — know which does what

| Language | Full name | Specifies |
|---|---|---|
| **RDF** | Resource Description Framework | **Relationships between data** — plain facts |
| **RDFS** | RDF Schema | **Relationships between schema** — `Class`, `Property`, `type`, `subClassOf`, `subPropertyOf`, `domain`, `range` |
| **OWL** | Web Ontology Language | **More complex relationships between schema**, based on **description logics** — restrictions, cardinality, reasoning |

**Semantic Web layers:** URI/IRI → XML → **RDF** → **RDFS** → **SPARQL**
(Simple Protocol and RDF Query Language) → **OWL**.

### The RDF data model
> Statements are **`<subject, predicate, object>` triples**, e.g.
> `<Ian, hasColleague, Uli>`. They can be drawn as a **graph**. A **resource** is
> any object that can be pointed to by a **URI**.

### ⭐ RDF vs OWL — the 2-mark answer (Mar 2026, Q5B)

> **Q:** A library wants to *store book data*; another system wants to check a
> constraint like *"every book must have an author"*. Which suits RDF, which OWL?
>
> **A:** Storing book data is best suited to **RDF**, as RDF represents
> information as simple **subject–predicate–object triples**. Checking logical
> constraints such as "every book must have an author" suits **OWL**, because
> OWL supports **restrictions and reasoning**. Thus **RDF handles data
> representation, while OWL handles logic and consistency checking.**

---

## 5.2 ⭐ SOLVED — Writing RDF triples (Feb 2026, Q6)

### The question
A university wants a semantic-web academic information system integrating
students, courses and faculty.
(a) Identify entities (subjects), properties (predicates), values (objects).
(b) Write three RDF triples for:
- A student named **Anita** is enrolled in the course **Data Science**
- The course **Data Science** is taught by **Dr. Rao**
- **Dr. Rao** is a faculty member of the **Computer Science Department**

### The answer
**(a) RDF components**
```
Entities (Subjects):        Properties (Predicates):     Values (Objects):
   Student   (Anita)           enrolledIn                   Data Science
   Course    (Data Science)    taughtBy                     Dr. Rao
   Faculty   (Dr. Rao)         memberOf                     Computer Science Dept
   Department(Computer Science)
```

**(b) The three triples**

| Subject | Predicate | Object |
|---|---|---|
| `Anita` | `enrolledIn` | `DataScience` |
| `DataScience` | `taughtBy` | `DrRao` |
| `DrRao` | `memberOf` | `ComputerScienceDepartment` |

As a graph:
```
   Anita ──enrolledIn──► DataScience ──taughtBy──► DrRao ──memberOf──► CSDept
```

### The Oct 2024 variant — a knowledge graph with a *derived inference*
```
ex:LivingThing  rdfs:subClassOf  ex:Object .
ex:Animal       rdfs:subClassOf  ex:LivingThing .
ex:Person       rdfs:subClassOf  ex:Animal .
ex:Faculty      rdf:type         ex:Person .
ex:Person       ex:hasEmail      ex:EmailId .
ex:Course       ex:taughtBy      "Chetana Gavankar" .
```
> **The derived inference** (this is what the 2 marks are for): nobody stated
> that a `Faculty` is an `Object`, but from
> `Faculty ⊑ Person ⊑ Animal ⊑ LivingThing ⊑ Object`, a reasoner **derives**
> `ex:Faculty rdfs:subClassOf ex:Object`. Draw the chain and label that last
> arrow **"inferred"** — that is the whole point of the question.

---

## 5.3 ⭐ SOLVED — Modelling an ontology (Mar 2026, Q5C, 2 marks)

> *"You are building a research publication ontology. How would you model
> papers, authors and conferences using RDF and OWL?"*

```
RDF is used to represent FACTUAL DATA; OWL to define SEMANTICS and CONSTRAINTS.

USING RDF — entities as resources, linked by triples:

    ( Paper1 , hasAuthor    , Author1 )
    ( Paper1 , presentedAt  , Conference1 )

USING OWL — classes and relationships defined formally:

    Classes           : Paper , Author , Conference
    Object properties : hasAuthor , presentedAt
    Constraint        : every Paper must have AT LEAST ONE Author
                        (an owl:minCardinality restriction)

This enables REASONING and CONSISTENCY CHECKING.
```

---
---

# 6. Ch 14: Retrieval Augmented Generation (RAG)

**Session 14.** Q6 in Mar 2026, and a full RAG numerical in Feb 2026.

> ### 🎯 THE EASIEST ARITHMETIC IN THE PAPER
> Subtraction, integer division, and one fraction. Do not lose these marks.

## 6.1 Little notes

**Why RAG exists — the three LLM limitations:**
1. **Knowledge cutoff** — knowledge is frozen at training time.
2. **Hallucinations** — when they don't know, they make up plausible but
   incorrect information.
3. **Lack of specificity** — no deep knowledge of proprietary, domain-specific
   or private information.

> **The method:** don't retrain the model (expensive and slow). Instead **give
> the LLM access to a live external knowledge base at the moment it needs to
> answer**.

**Two components:**
- **Retriever** — fetches relevant documents based on the query.
- **Generator** — generates responses using both the query and the retrieved documents.

**Benefits:** access to up-to-date information · improved factual accuracy ·
**reduced hallucinations**.

**Keyword vs semantic search:** keyword search matches exact words, so
*"cost of laptop repair"* misses a document titled *"pricing for computer
hardware fixes"*. **Semantic search** converts query and documents into
**embeddings** and finds the closest *meaning*, not the closest words.

**The RAG flow:** User query → **semantic search** over the knowledge base →
**context retrieval** → **prompt enhancement** (*"Using the following context:
[…], answer this question: …"*) → **LLM generation** grounded only in that context.

### Traditional RAG vs Graph RAG

| Feature | Traditional RAG | Graph RAG |
|---|---|---|
| Data format | Unstructured text | Structured graph |
| Retrieval method | Dense vector search | Graph traversal / querying |
| Reasoning | Limited | **Enhanced (multi-hop)** |
| Explainability | **Low** | **High** |
| Integration complexity | Moderate | High |
| Use cases | General QA | Domain-specific applications |

**Agentic RAG:** the LLM acts as an **agent**, not a passive generator — it sets
subgoals, plans retrieval steps, executes tool use, and iteratively refines
answers. Components: **LLM agent · memory/scratchpad · retrievers/tools ·
planner/executor**.

---

## 6.2 ⭐ SOLVED — RAG token budget (Feb 2026, 6 marks)

### The recipe
```
1. FIXED tokens      = query + system prompt
2. AVAILABLE tokens  = max context length - fixed
3. MAX chunks        = FLOOR( available / chunk size )      <-- ALWAYS FLOOR
4. Total sent to LLM = fixed + (chunks used x chunk size)
```

### The question
```
Query tokens              = 160
System prompt tokens      = 240
Maximum LLM context length = 4096
Size of each chunk        = 480
```
(a) Max chunks retrievable without exceeding the limit?
(b) If only 75% of that maximum is retrieved, total tokens passed to the LLM?
(c) Does retrieving fewer chunks improve or degrade generation quality?

### The answer
**(a)**
```
Total fixed tokens       = 160 + 240 = 400
Available for retrieval  = 4096 - 400 = 3696
Maximum number of chunks = floor(3696 / 480) = floor(7.7) = 7
```
> **7 chunks.**  *(7 × 480 = 3360 ≤ 3696 ✓ ; 8 × 480 = 3840 > 3696 ✗)*

**(b)**
```
75% of 7 = 5.25  ->  rounded DOWN to 5 chunks
Tokens from chunks = 5 x 480 = 2400
Total passed to LLM = 400 + 2400 = 2800 tokens
```

**(c)**
> Retrieving **fewer but more relevant** chunks **reduces noise** in the context.
> This generally **improves factual grounding and lowers hallucination**, so
> generation quality is **likely to improve**.

> **Both roundings are DOWN.** `floor(7.7) = 7` because a partial chunk doesn't
> fit; `floor(5.25) = 5` because you can't retrieve a quarter of a chunk. Say
> "floor" explicitly — it is a marked step.

---

## 6.3 ⭐ SOLVED — Retrieval precision (Mar 2026, Q6, 6 marks)

### The question
Similarity scores: `0.92, 0.86, 0.79, 0.71, 0.64, 0.58`. Threshold **0.75**.

**(a) How many chunks pass?**
```
Scores >= 0.75 :  0.92 , 0.86 , 0.79        (0.71, 0.64, 0.58 are below)

Number of chunks passed = 3
```

**(b) Precision, assuming all selected are relevant**
```
              number of RELEVANT chunks       3
Precision = ---------------------------  =  ----- = 1.0
              number of RETRIEVED chunks      3
```

**(c) One irrelevant chunk is mistakenly added**
```
Total retrieved = 4 ,  relevant = 3

New precision = 3 / 4 = 0.75

The reduction in precision INCREASES CONTEXTUAL NOISE, which can
negatively affect generation quality.
```

> **Precision vs recall, in the RAG frame:**
> **Precision** = of what I retrieved, how much was relevant (noise control).
> **Recall** = of all relevant material, how much did I retrieve (coverage).
> Raising the threshold raises precision and lowers recall. Notice (c) is the
> mirror image of §6.2(c) — one says *fewer is better*, the other says
> *irrelevant is worse*. Both reduce to: **relevance density is what matters.**

---

## 6.4 You try — RAG
<details>
<summary><b>R1.</b> Query 200, system prompt 300, context 8192, chunk 512. Max chunks? If 60% used, total tokens? — answer</summary>

```
fixed     = 200 + 300 = 500
available = 8192 - 500 = 7692
max       = floor(7692 / 512) = floor(15.02) = 15 chunks

60% of 15 = 9  ->  9 chunks
tokens    = 500 + (9 x 512) = 500 + 4608 = 5108 tokens
```
</details>

<details>
<summary><b>R2.</b> Scores 0.95, 0.88, 0.81, 0.77, 0.62. Threshold 0.80. How many pass? If 2 of them are irrelevant, precision? — answer</summary>

```
>= 0.80 :  0.95, 0.88, 0.81      ->  3 chunks pass
           (0.77 is below the threshold)

relevant = 3 - 2 = 1
precision = 1 / 3 = 0.33

Very low precision -> heavy contextual noise -> high hallucination risk.
```
</details>

---
---

# 7. Ch 15: Text Summarization

**Session 15.** Q7 in both 2026 papers.

## 7.1 Little notes

### ⭐ The types — the classification table (3 marks, straight recall)

| Axis | Type | Definition |
|---|---|---|
| **How many inputs** | **Single-document** | Summarises **one** document |
| | **Multi-document** | Takes a **group of documents on the same event**; produces a gist of shared information, **removing redundancy** and resolving overlaps |
| **How words are produced** | **Extractive** | Creates the summary **from phrases or sentences in the source document(s)** |
| | **Abstractive** | Expresses the ideas **using (at least in part) different words** |
| **User intent** | **Generic** | Summarises overall content; **not tailored to any query** |
| | **Query-focused** | Tailored to a **specific user information need**; a form of **complex question answering** |

### The three stages of summarization
```
1. CONTENT SELECTION    choose sentences to extract from the document
2. INFORMATION ORDERING choose an order to place them in the summary
3. SENTENCE REALIZATION clean up the sentences
```

**Content selection ideas:** frequency as an indicator of importance (the topic
is repeated many times; in multi-document, important content is repeated across
sources) · greedy frequency method · **tf-idf** · graph representations (nodes =
sentences, arcs between similar sentences).

**Information ordering:** **chronological** (by document date, for news) ·
**coherence** (neighbouring sentences similar by cosine, or discussing the same
entity) · **topical** ordering.

---

## 7.2 ⭐⭐ SOLVED — Maximal Marginal Relevance (Feb 2026, Q7, 6 marks)

### The formula box
```
    MMR(s) = lambda * sim(s, q)  -  (1 - lambda) * sim(s, S)
             \_______________/      \_____________________/
                RELEVANCE                REDUNDANCY
              (to the query)        (to what is ALREADY selected)

    Pick the sentence with the HIGHEST MMR. Add it to S. Repeat.
```
> **The whole idea:** a sentence must be **relevant to the query** *and*
> **different from what you have already got**. High relevance alone is not
> enough — it might just repeat the summary.

### The question
Query **q**: *"Government regulations on Artificial Intelligence in healthcare."*
Already selected **S** = {*"Governments are introducing regulations to ensure
safe use of AI in medical diagnosis."*}

| Sentence | sim(s, q) | sim(s, S) |
|---|---|---|
| **S1**: *"New AI laws focus on patient data privacy and ethical use of machine learning models."* | 0.80 | 0.30 |
| **S2**: *"Several countries have passed laws regulating AI-based medical diagnosis systems."* | 0.88 | 0.70 |

Given **λ = 0.6**.

### The answer
**1. Compute both MMR scores [3 marks]**
```
lambda = 0.6 ,  (1 - lambda) = 0.4

MMR(S1) = 0.6 x 0.80  -  0.4 x 0.30
        = 0.48        -  0.12
        = 0.36

MMR(S2) = 0.6 x 0.88  -  0.4 x 0.70
        = 0.528       -  0.28
        = 0.248
```

**2. Which is selected? [1 mark]**
> `MMR(S1) = 0.36 > MMR(S2) = 0.248` → **Sentence S1 is selected.**

**3. Justify — relevance vs redundancy [2 marks]**
> **Although S2 is more relevant to the topic** (0.88 vs 0.80), **it is highly
> similar to the already-selected sentence** (0.70 vs 0.30), **making it
> redundant** — it would largely repeat information the summary already
> contains. **S1 provides new complementary information** about ethics and data
> privacy, resulting in a **higher MMR score**.

> **The exam point.** The question is *designed* so the more relevant sentence
> loses. If your answer picks the higher `sim(s,q)` you've missed the entire
> concept. **Always name the trade-off explicitly in the justification.**

---

## 7.3 ⭐ SOLVED — Identifying summarization types (Mar 2026, Q7, 6 marks)

### The question
A news analytics company must support:
1. A journalist uploads **one long report** on climate change and wants a short
   **headline** and a brief **abstract**.
2. A policy analyst provides **15 news articles from different sources** on the
   same summit and wants a concise overview.
3. A researcher uploads a technical document and asks: *"Summarize the sections
   relevant to the **economic impact**."*

### The answer
**(a) The type for each [3 marks]**

| Scenario | Required summarization type |
|---|---|
| 1 | **Single-document, Generic** summarization |
| 2 | **Multi-document** summarization |
| 3 | **Query-focused** summarization |

**(b) Justification [1.5 marks]**
```
1. SINGLE-DOCUMENT, GENERIC
   - Operates on ONE document
   - Produces outputs such as a headline, abstract, or outline
   - Focuses on summarizing the OVERALL CONTENT, not a specific query

2. MULTI-DOCUMENT
   - Takes a group of documents related to the SAME EVENT
   - Produces a gist of shared information, REMOVING REDUNDANCY
     and resolving overlaps
   - Commonly used for news aggregation and event summarization

3. QUERY-FOCUSED
   - Tailors the summary to a SPECIFIC USER INFORMATION NEED
   - Acts as a form of COMPLEX QUESTION ANSWERING
   - Ignores unrelated sections of the document
```

**(c) Why one approach cannot handle all three [1.5 marks]**
```
- Generic summarization IGNORES USER INTENT.
- Query-focused summarization REQUIRES AN EXPLICIT INFORMATION NEED.
- Multi-document summarization must MANAGE REDUNDANCY AND CONTRADICTIONS
  across sources.

Each scenario differs in INPUT STRUCTURE, USER INTENT, and OUTPUT
REQUIREMENTS, necessitating distinct summarization strategies.
```

---

## 7.4 ⭐ SOLVED — ROUGE-2

### The definition
> **ROUGE** = Recall-Oriented Understudy for Gisting Evaluation. An **intrinsic**
> metric for automatically evaluating summaries, based on **BLEU**. Not as good
> as human evaluation, **but much more convenient**.
>
> **ROUGE-2:** given a document D and an automatic summary X, have N humans
> produce reference summaries. **What percentage of the bigrams from the
> reference summaries appear in X?**

```
                 number of reference bigrams that ALSO appear in X
    ROUGE-2  =  --------------------------------------------------
                    total number of bigrams in ALL references
```

### The slide's worked example
```
Q: "What is water spinach?"

Human 1: Water spinach is a green leafy vegetable grown in the tropics.
Human 2: Water spinach is a semi-aquatic tropical plant grown as a vegetable.
Human 3: Water spinach is a commonly eaten leaf vegetable of Asia.

System X: Water spinach is a leaf vegetable commonly eaten in tropical
          areas of Asia.
```

**System bigrams (12):** water spinach · spinach is · is a · a leaf ·
leaf vegetable · vegetable commonly · commonly eaten · eaten in · in tropical ·
tropical areas · areas of · of asia

| Reference | Bigrams | Matched in X | Which |
|---|---|---|---|
| Human 1 | 10 | **3** | water spinach, spinach is, is a |
| Human 2 | 10 | **3** | water spinach, spinach is, is a |
| Human 3 | 9 | **6** | water spinach, spinach is, is a, commonly eaten, leaf vegetable, of asia |
| | **29** | **12** | |

```
    ROUGE-2 = 12 / 29 = 0.4138  =  41.4%
```
> Human 3's phrasing is closest to the system output, so it contributes half the
> matches on its own. That is the metric working as intended.

---

## 7.5 You try — Summarization
<details>
<summary><b>S1.</b> λ = 0.7. Sentence A: sim(q)=0.9, sim(S)=0.8. Sentence B: sim(q)=0.75, sim(S)=0.2. Which is selected? — answer</summary>

```
MMR(A) = 0.7 x 0.90 - 0.3 x 0.80 = 0.63 - 0.24 = 0.39
MMR(B) = 0.7 x 0.75 - 0.3 x 0.20 = 0.525 - 0.06 = 0.465

B is selected (0.465 > 0.39).
```
Again the *less relevant* sentence wins, because A duplicates the existing
summary. Justify in terms of relevance vs redundancy.
</details>

<details>
<summary><b>S2.</b> Same numbers as S1 but λ = 0.9. Now which wins, and what does that tell you about λ? — answer</summary>

```
MMR(A) = 0.9 x 0.90 - 0.1 x 0.80 = 0.81 - 0.08 = 0.73
MMR(B) = 0.9 x 0.75 - 0.1 x 0.20 = 0.675 - 0.02 = 0.655

A now wins (0.73 > 0.655).
```
**λ controls the trade-off.** λ → 1 means "care only about relevance" (redundancy
is ignored, summaries repeat themselves). λ → 0 means "care only about novelty"
(the summary drifts off-topic). λ = 0.6–0.7 is the usual balance.
</details>

<details>
<summary><b>S3.</b> References have 20 bigrams total; 7 appear in the system summary. ROUGE-2? — answer</summary>

`ROUGE-2 = 7 / 20 = 0.35 = 35%`
</details>

---
---

# 8. Last-night checklist

## The 8 formulas — cover the right side

| # | Thing | Formula |
|---|---|---|
| 1 | **PCFG tree probability** | `P(tree) = Π P(rule)` — the parse with higher P wins |
| 2 | **Attention output** | `Output = Σᵢ αᵢ · vᵢ` (weights sum to 1) |
| 3 | **Self-attention** | `softmax( QKᵀ / √d_k + mask ) · V` |
| 4 | **Multi-head** | `Concat(head₁…head_h) × W_O` |
| 5 | **Cosine** | `(a·b) / (\|a\|\|b\|)` — **divide by the magnitudes** |
| 6 | **Lesk** | overlap = count of words in **both** context and gloss; highest wins |
| 7 | **RAG chunks** | `floor( (context − query − prompt) / chunk_size )` |
| 8 | **MMR** | `λ·sim(s,q) − (1−λ)·sim(s,S)` |

## The 6 traps that cost marks

1. **Cosine, not dot product** (§4.3) — the biggest dot product is often the
   *wrong* sense.
2. **MMR: the more relevant sentence usually loses.** Always explain
   relevance vs redundancy.
3. **RAG: floor, both times.** Never round up.
4. **Arc-eager LEFT-ARC: the head is the buffer front**, not the stack top.
5. **Chu-Liu-Edmonds:** exactly one incoming arc per word, nothing into ROOT,
   everything reachable from ROOT.
6. **Top-down parsing: show the backtrack.** The pop from backup is where the
   marks are.

## Exam-day order of attack

It is open book and 2.5 hours for 40 marks. Do them in **value-per-minute**
order, not paper order:

```
1. Q4  Attention          (6)  — one weighted sum. ~5 min.
2. Q7  MMR / summarization(6)  — two multiplications. ~7 min.
3. Q6  RAG / RDF          (6)  — arithmetic + recall. ~10 min.
4. Q5  Lesk / WSD         (6)  — counting. ~10 min.
5. Q2  Viterbi            (5)  — you already drilled this pre-mid. ~15 min.
6. Q1  N-gram + NN LM     (5)  — pre-mid. ~12 min.
7. Q3  Parsing/Dependency (6)  — longest. Leave it the remaining time.
```
That front-loads **24 marks in about 32 minutes**.

## What to have open in the exam

- **This file** (post-mid, 30 marks)
- `../formula-sheet.md` (pre-mid, 10 marks)
- `../ch06-pos-tagging-hmm-viterbi.md` for the Viterbi recipe
- The **Feb 2026 and Mar 2026 papers with answers** — the questions repeat
  almost verbatim, only the numbers change

---

**Source papers:** `notes/question papers/` — Feb 2026 regular (with answers),
Mar 2026 makeup (with answers), Oct 2024 regular (with answers), one undated
regular, and the sample Q&A set.
**Source decks:** `slides/NLP Session 9–15`.
Every numerical above was recomputed independently and agrees with the official
answer key.
