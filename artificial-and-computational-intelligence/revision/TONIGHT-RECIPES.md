# TONIGHT — Six Recipes. Nothing Else.

**This file replaces every other file until the exam.** Close the rest.

## Read this paragraph twice

The exam is **OPEN BOOK**. You are not being tested on whether you understand
the theory. You are being tested on whether you can **execute a procedure**
with your notes in front of you. There is a real difference between *"I don't
understand Hidden Markov Models"* and *"I can't yet fill in a 3 × 2 table of
multiplications"*. **The exam only asks for the second one.**

Six recipes below. Each is: *what the question looks like* → *the steps* → *a
tiny worked example* → *the one trap*. Learn them as procedures, the way you'd
learn to make tea. Understanding will follow later, and it is not needed
tomorrow.

## What these six are worth

| Recipe | Chapter | Marks it covers | Q on the paper |
|---|---|---|---|
| **1** Viterbi | 11 | ~8 | Q4 |
| **2** Forward | 11 | (alternative to Q4) | Q4 |
| **3** Bayes-net query | 10 | ~9 | Q3 |
| **4** D-separation | 10 | (part of Q3) | Q3 |
| **5** CNF → DPLL | 8 | ~7 | Q2 |
| **6** Markov sequence | 11 | ~3 | Q5c |

**Recipes 1 + 3 + 5 alone are 24 of 40 marks.** That is 60 %. You can learn all
three tonight, because none of them requires you to understand anything — they
are all arithmetic in a table.

---

# RECIPE 1 · VITERBI — "most likely sequence of states"

### How to spot it
The question gives you **hidden states** (weather, health, machine condition)
and **observations** (what you actually see), then asks for the **most likely
sequence of states** / *"best explanation"* / *"decode"*.

### The steps

```
 STEP 1  Write two tables from the prose.
         TRANSITION  a[from][to]   — each ROW must sum to 1
         EMISSION    b[state][obs] — each ROW must sum to 1
         Plus the INITIAL π. "Equal likelihood" means 1/n each.

 STEP 2  t = 1 :   v1(state) = π(state) × b[state][first obs]
         Then NORMALISE: divide each by their total.   <- class convention

 STEP 3  Every later t, for EACH state j:
             v_t(j)  = MAX over i of [ v_{t-1}(i) × a[i][j] ]  ×  b[j][obs_t]
             bp_t(j) = the i that WON that max        <- write it down!

 STEP 4  At the last column, take the BIGGEST v.
         Walk the backpointers backwards. THAT SEQUENCE is the answer.
```

### Tiny worked example

States Sunny / Rainy. π = (0.6, 0.4). Observations = **(Shop, Shop)**.

```
 TRANSITION            EMISSION
 from\to  Sunny Rainy   state   Walk  Shop
 Sunny     0.7   0.3    Sunny    0.6   0.4
 Rainy     0.4   0.6    Rainy    0.2   0.8
```

```
 t = 1, obs = Shop
   v1(Sunny) = 0.6 × 0.4 = 0.24
   v1(Rainy) = 0.4 × 0.8 = 0.32          sum = 0.56
   NORMALISE:  Sunny = 0.24/0.56 = 0.428571
               Rainy = 0.32/0.56 = 0.571429

 t = 2, obs = Shop
   into Sunny : max( 0.428571×0.7 , 0.571429×0.4 )
              = max( 0.300000     , 0.228571     ) = 0.300000   bp = Sunny
       v2(Sunny) = 0.300000 × 0.4 = 0.120000

   into Rainy : max( 0.428571×0.3 , 0.571429×0.6 )
              = max( 0.128571     , 0.342857     ) = 0.342857   bp = Rainy
       v2(Rainy) = 0.342857 × 0.8 = 0.274286

 BIGGEST at t=2 is Rainy (0.274286).  bp says the state before it was Rainy.

 ANSWER:  RAINY -> RAINY
```

That is the entire algorithm. **It is multiply, compare, write down the winner.**

### The trap
**MAX, not SUM.** If you find yourself adding the two incoming numbers, you
have written Recipe 2 by mistake. And **the answer is the sequence of state
names**, not the final number — so write the backpointers down as you go.

---

# RECIPE 2 · FORWARD — "probability of the observations"

### How to spot it
Same setup, but the question asks for **P(O)** — *"the likelihood of this
observation sequence"* / *"the probability of observing…"*. **No state sequence
is wanted.**

### The steps
**Identical to Recipe 1 with two changes:** use **SUM** instead of MAX, and
**never normalise**.

```
 α1(j) = π(j) × b[j][obs1]                       (no normalising!)
 α_t(j) = [ SUM over i of α_{t-1}(i) × a[i][j] ] × b[j][obs_t]
 P(O)  = SUM of the final column
```

### Same example, same numbers

```
 α1(Sunny) = 0.24        α1(Rainy) = 0.32

 α2(Sunny) = (0.24×0.7 + 0.32×0.4) × 0.4 = (0.168 + 0.128) × 0.4 = 0.118400
 α2(Rainy) = (0.24×0.3 + 0.32×0.6) × 0.8 = (0.072 + 0.192) × 0.8 = 0.211200

 P(O) = 0.118400 + 0.211200 = 0.3296
```

### The trap
**Do not normalise inside Forward.** P(O) *is* the answer, and normalising
throws it away. (Normalise-at-t=1 belongs to Viterbi only.)

> **The one line that gets you both:** Forward and Viterbi are *the same
> table*. `Σ` answers "how likely were these observations". `max` + backpointers
> answers "what most likely happened".

---

# RECIPE 3 · BAYES-NET QUERY

### How to spot it
A paragraph of prose describing causes and effects, then: *"draw the Bayes net
with CPTs"* and *"what is the probability that …"*.

### Part A — building the net (this is 4 of the 9 marks, and it is free)

```
 STEP 1  Every CAPITALISED / bracketed thing in the prose is a NODE.
 STEP 2  "X is influenced by Y"  /  "Y affects X"   =>  draw  Y -> X
 STEP 3  Write a PARENT LIST. e.g.  "OF : parents RU, IA"
 STEP 4  CPTs. A node with k parents needs 2^k rows.
         *** ANY NUMBER THE QUESTION DOESN'T GIVE YOU IS 0.5 ***
         The paper says so: "assume all events are equally likely except
         those explicitly specified". DO NOT INVENT NUMBERS.
```

### Part B — the query

```
 STEP 1  WRITE THE QUERY SYMBOLICALLY FIRST.  <- worth 0.5 marks on its own,
         before any arithmetic. Do this even if you then get stuck.
           Query = the thing asked for.  Evidence = the thing given.
           Hidden = everything else.
 STEP 2  Prune: any LEAF that is neither query nor evidence is IRRELEVANT.
         Say so in words. It is worth a mark and it halves your work.
 STEP 3  Expand with the CHAIN RULE:
           P(x1,…,xn) = PRODUCT of P( each node | its parents )
 STEP 4  If it's a conditional P(X | e), compute the top AND the bottom,
         then NORMALISE (divide by their sum, check it comes to 1).
```

### Two tiny worked examples

**(a) Everything is specified → it's just a product.** All eight variables
given as true, roots at 0.5:

```
 P(A,B,C,…) = P(A)·P(B)·P(C|A,B)·…       <- write this line first
            = 0.5 × 0.5 × 0.5 × 0.5 × 0.90 × 0.90 × 0.95 × 0.5
            = 0.024046875
```

If **every** CPT is 0.5 and **six** variables are named, the answer is just
`0.5⁶ = 0.015625`. That is literally Q3(c) of the real Apr 2025 paper.
**Count the variables named in the sentence. That's the exponent.**

**(b) There is evidence → normalise.** `P(B)=0.1, P(A|B)=0.9, P(A|¬B)=0.2`.
Find `P(B | A)`:

```
 P(B | A) = α · P(B, A)
   B true  : 0.1 × 0.9 = 0.09
   B false : 0.9 × 0.2 = 0.18
                         ----
   total  P(A)         = 0.27
   P(B|A) = 0.09 / 0.27 = 0.3333
   P(¬B|A)= 0.18 / 0.27 = 0.6667      check: sums to 1 ✓
```

### The trap
**Forgetting to normalise**, and **inventing CPT numbers** the question didn't
give. Unspecified = 0.5. Always.

---

# RECIPE 4 · D-SEPARATION — "prove X is independent of Y given Z"

### The three rules — this is the whole topic

```
 Look at each node M ALONG THE PATH from X to Y:

   CHAIN     X -> M -> Y      BLOCKED when M IS observed
   FORK      X <- M -> Y      BLOCKED when M IS observed
   COLLIDER  X -> M <- Y      BLOCKED when M is NOT observed
                              (and no CHILD of M is observed)

 X and Y are INDEPENDENT only if EVERY path is blocked.
 ONE open path anywhere  =>  they are DEPENDENT, statement is FALSE.
```

### How to answer, every time

```
 1. List every path from X to Y.
 2. For each path, name each middle node's TYPE (chain / fork / collider).
 3. Say observed or not, then blocked or open.
 4. All blocked -> TRUE (d-separated). Any open -> FALSE (d-connected).
```

### The one thing to burn in

**The collider rule is BACKWARDS from the other two.** Chains and forks are
**blocked by** observing the middle node. A collider is **opened by** it.

That is the single most examined idea in Chapter 10. If a question looks like
an obvious "true", check whether there's a collider that the evidence has
*opened*.

*Nickname it "explaining away": wet grass has two causes; learning it rained
makes the sprinkler less likely. Observing the effect makes the causes talk to
each other.*

---

# RECIPE 5 · CNF → DPLL

### How to spot it
A paragraph of rules about a system, then: *"represent in propositional
logic"* → *"convert to CNF"* → *"find a BSAT solution using DPLL"*.

### Part A — prose to logic (2 marks, mechanical)

```
 "A implies B or C"              ->   A -> (B ∨ C)
 "when both A and B, then C"     ->   (A ∧ B) -> C
 "A without B indicates C"       ->   (A ∧ ¬B) -> C
 "it is known that A happened"   ->   A            (a plain fact)
```

### Part B — CNF, five steps, always this order

```
 1. Remove <->     (a <-> b)  =>  (a -> b) ∧ (b -> a)
 2. Remove ->      (a -> b)   =>  (¬a ∨ b)          <- does 90% of the work
 3. Push ¬ inwards  De Morgan:  ¬(a ∧ b) = ¬a ∨ ¬b
                                ¬(a ∨ b) = ¬a ∧ ¬b
 4. Distribute ∨ over ∧        (a ∨ (b ∧ c)) => (a∨b) ∧ (a∨c)
 5. Write as a SET OF CLAUSES, one per line, in { } braces.
```

```
 Example:  (A ∧ B) -> C
   step 2 :  ¬(A ∧ B) ∨ C
   step 3 :  ¬A ∨ ¬B ∨ C          <- done, this is a clause
```

### Part C — DPLL, three moves in priority order

```
 Repeat until every clause is satisfied (or one is empty = fail):

 1. UNIT PROPAGATION   A clause with ONE literal left FORCES that literal.
                       Do this to exhaustion first — it cascades.
 2. PURE LITERAL       A symbol that appears with only ONE sign anywhere
                       can be set to that sign. It can never cause a conflict.
 3. SPLIT              Only if neither above applies: pick a symbol, try
                       true, and if that fails, backtrack and try false.

 NAME THE RULE at every step. The marking scheme asks for it.
```

### Tiny worked example

`KB = { P -> Q , Q -> R , P }`

```
 CNF:   C1 { ¬P, Q }    C2 { ¬Q, R }    C3 { P }

 UNIT PROPAGATION on C3   ->  P = TRUE
     C1 loses ¬P  ->  { Q }        now a unit clause
 UNIT PROPAGATION on { Q } ->  Q = TRUE
     C2 loses ¬Q  ->  { R }        now a unit clause
 UNIT PROPAGATION on { R } ->  R = TRUE

 ALL CLAUSES SATISFIED.  Model: P = T, Q = T, R = T.   No split needed.
```

### The trap
If the question says **prove** something (resolution / entailment), you must
**add the NEGATED goal** and derive a contradiction — the empty clause `{ }`.
Write *"assume ¬α and derive a contradiction"* as your very first line. Adding
the goal itself proves nothing.

---

# RECIPE 6 · MARKOV CHAIN — missing values + sequence likelihood

### The steps

```
 STEP 1  WHICH WAY DOES THE TABLE RUN?  Add up a row and add up a column.
         *** THE DIRECTION THAT SUMS TO 1 IS THE "FROM" DIRECTION. ***
         Write one line saying which convention you are using.

 STEP 2  Fill any missing entry so its row (or column) totals 1.

 STEP 3  If asked for the initial probability "from the given sequence":
         count how often each state appears in the sequence and divide by
         the length. Say you are using the maximum-likelihood estimate.

 STEP 4  Likelihood of a sequence:
             P(s1, s2, …) = π(s1) × P(s2|s1) × P(s3|s2) × …
```

### Tiny worked example

π = (Sunny 0.6, Rainy 0.4); `P(Sunny→Sunny) = 0.7`, `P(Sunny→Rainy) = 0.3`.

```
 P(Sunny, Sunny, Rainy) = π(Sunny) × P(S|S) × P(R|S)
                        = 0.6 × 0.7 × 0.3
                        = 0.126
```

### The trap
Reading the matrix the wrong way round. The Apr 2025 paper printed it with
**columns = the previous state**, which is the opposite of the textbook. Check,
then state which way you are reading it. Get it backwards and every later
number is wrong.

---

# WHEN YOU GET STUCK IN THE EXAM

You are marked on method, not just the final number. **Partial credit is
enormous on this paper.** So when the arithmetic won't come:

```
 1. Write the FORMULA you would use, by name.
 2. Write the SYMBOLIC set-up  ("P(X|e) = α · Σ_Y P(X,e,Y)").
 3. Write "assumptions: …" at the top of the answer.
 4. DRAW THE DIAGRAM. On a Bayes net or HMM question the diagram
    carries its own marks, separate from the table.
 5. Say what you would do next in one sentence.
```

The Apr 2025 marking scheme awards **0.5 marks for "query extraction"** and
**0.5 for "linearise the sequence"** — *before any arithmetic happens*. Those
are free. Take them on every single question, even ones you can't finish.

And write this at the top of your answer book, because both papers ask for it:

> *"Assumptions made, if any, are stated at the beginning of each answer."*

---

# YOUR SCHEDULE

### Tonight

| Time | Do this | Worth |
|---|---|---|
| **now → 6:00** | **Recipe 1 (Viterbi)**. Read it, then do Paper A Q4 from `MOCK-PAPERS`. Then do it *again* on blank paper. | 8 marks |
| 6:00 → 6:45 | **Eat. Walk. Screen off.** Not optional. | |
| **6:45 → 9:15** | **Recipes 3 + 4 (Bayes net + D-separation)**. Read, then Paper A Q3. | 9 marks |
| **9:15 → 10:45** | **Recipe 5 (CNF → DPLL)**. Read, then Paper A Q2. | 7 marks |
| 10:45 → 11:00 | Print. Tab the pages. Pack your bag. | |
| **11:00** | **SLEEP.** | |

**Sleep is part of the plan, not a reward for finishing.** An open-book exam is
2.5 hours of careful arithmetic. Tired arithmetic is wrong arithmetic, and no
amount of extra reading tonight buys back what a bad night costs you tomorrow.

### Tomorrow morning

| Time | Do this |
|---|---|
| 7:00 → 8:00 | Paper **B** Q4 (Forward) timed. Mark it. |
| 8:00 → 9:00 | Paper **B** Q3 (Bayes net) timed. Mark it. |
| 9:00 → 9:40 | Recipe 6 (Markov) + Paper A Q5c. Quick and cheap. |
| 9:40 → 10:15 | **Tab your printouts.** One sticky note per recipe, sticking out of the page. This *is* exam preparation — open book rewards knowing where things are. |
| **10:15** | **Stop.** Travel. Do not open a new topic. |

### In the exam

1. Read all five questions first. **Do them in order of confidence, not
   printed order.** Start with the HMM or the Bayes net — bank those marks.
2. ~3.75 minutes per mark. A 9-mark question gets ~30 minutes. **Move on when
   the time is up**, even mid-answer. Come back if there's time.
3. Never leave a question blank. The formula plus the symbolic set-up is worth
   real marks on a question you cannot finish.

---

## What you are deliberately NOT doing tonight

Say these out loud so you stop worrying about them:

- **Ch 12 / 13** (game theory, Shapley, auctions, voting) — scored **0 marks**
  across all three past papers. If it appears, it's small. Skip it.
- **Ch 14** (Responsible AI) — ~2.5 marks, and it's a write-what-you-think
  question. You can answer it cold with common sense plus one real example.
- **Ch 5** (GA / ACO / neuroevolution) — scored **0** across all three papers.
- **Deep understanding of anything.** Not tomorrow's problem. Recipes tomorrow,
  understanding later.

**Three recipes. 24 of 40 marks. That is the whole job tonight.**
