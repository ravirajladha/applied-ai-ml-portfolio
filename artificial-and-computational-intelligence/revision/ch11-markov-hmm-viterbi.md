# Ch 11 — Reasoning Over Time: Markov Models, HMM, Forward & Viterbi
**Slides: CS#13 / Module 6** (post-midsem deck, pages 42–52)

> ### ⚠ This is the highest-value chapter in the course.
> **~22% of the marks** across the two past papers — an 8-mark question **plus** a
> 3-mark question on the Apr 2025 endsem, and a 6-mark question on the makeup.
> You marked it as never studied. Start here.

> Open `explainers/ch11-hmm-viterbi.html` first — it builds the trellis one
> column at a time so you can see what the numbers mean before you compute them.

---

## 1. Why "reasoning over time"?

| Static world | Dynamic world |
|---|---|
| Each random variable has a **single fixed value** | State information **keeps changing with time** |
| Diagnosing a broken car | Treating a diabetic patient · tracking a robot's location · tracking a nation's economic activity |

The world is observed in **time slices**. Each slice has a set of random
variables, **some observable and some not**.

```
E_t  =  set of OBSERVABLE random variables at time t     (Evidence)
X_t  =  set of UNOBSERVED random variables at time t     (hidden State)
```
Assumption: the **same subset** of variables is observable in every time slice.

An agent in a partially observable environment keeps a **belief state** — the set
of currently possible world states — and uses a **transition model** to work out
how the world might evolve next.

---

## 2. The Markov assumption — the whole idea in one line

> **The current state depends only on a finite number of previous states.**

For a **first-order** Markov chain, that finite number is **one**:

```
P( S_t | S_1, S_2, ..., S_(t−1) )  =  P( S_t | S_(t−1) )
```

> **The analogy:** a board game like Snakes and Ladders. To know your chances on
> the next roll, all that matters is **which square you are on now**. How you
> got there — lucky ladder or long slog — changes nothing. The present square
> **screens off** the entire past.

**Markov chain** = modelling sequences of random events and the transitions
between states over time.

---

## 3. Transition matrix — read the direction carefully

A transition matrix holds `P(current | previous)`.

> **⚠ The single most dangerous thing in this chapter.** The past paper lays its
> matrix out with **columns = previous state** and **rows = current state**, so
> **each COLUMN sums to 1**. Most textbooks do the opposite (rows sum to 1).
>
> **Before you compute anything, check which way the given matrix sums to 1.**
> Getting this backwards makes every subsequent number wrong.

### Worked — the slides' Computer / Media example

Two states: **C** = Computer Electronics, **M** = Media accessories.

```
P(C|C) = 0.4      P(M|C) = 0.6
P(C|M) = 0.2      P(M|M) = 0.8
```

The slides run **three inference types** on this. All three use the same trick.

### The initial-probability convention — *learn this, it is worth marks*

> **The slides set the initial probability to 1 for whichever state the sequence
> starts in, and 0 for all others.**
>
> Slide wording: *"Initial Probability Matrix is P(C) = 1, P(M) = 0"*.
> The Apr 2025 paper asks you to *"Calculate the initial probability using the
> given sequence"* — this is what it means.

### Inference Type 1 — probability of an exact sequence

**Q: What is the probability the customer's purchasing behaviour follows exactly
`(Computer, Media, Media, Computer)`?**

```
Apply the Bayes chain rule with the Markov assumption:

P(C, M, M, C) = P(C) · P(M|C) · P(M|M) · P(C|M)
              =  1  ×   0.6   ×   0.8   ×   0.2
              = 0.096
```

### Inference Type 2 — derive the initial values first

**Q: A customer who purchased Media accessories — what is the probability they
keep coming back for media accessories on the next 2 consecutive visits only?**

Sequence is `(Media, Media, Media, Computer)`, so `P(M) = 1, P(C) = 0`.

```
P(M, M, M, C) = P(M) · P(M|M) · P(M|M) · P(C|M)
              =  1  ×  0.8   ×  0.8   ×  0.2
              = 0.128
```

### Inference Type 3 — the *most likely* pattern (this is Viterbi in miniature)

**Q: Given the customer bought Computer electronics, find the expected purchase
pattern over the next 3 visits.**

Now the later states are unknowns `X, Y, Z`, and you **choose each one to
maximise the product**:

```
P(Computer, X, Y, Z) = P(C) · P(X|C) · P(Y|X) · P(Z|Y)

  From C: P(M|C) = 0.6  >  P(C|C) = 0.4     ->  X = Media
  From M: P(M|M) = 0.8  >  P(C|M) = 0.2     ->  Y = Media
  From M: P(M|M) = 0.8  >  P(C|M) = 0.2     ->  Z = Media

  = 1 × 0.6 × 0.8 × 0.8  =  0.384    <- the maximum
```
**Answer: `(Computer, Media, Media, Media)`.**

> The slides call this *"reverse predict the combination on the most likely
> pattern (similar to Viterbi Algorithm)"*. That is exactly what it is — Viterbi
> **without** the hidden layer.

---

## 4. Hidden Markov Model — adding the hidden layer

In a plain Markov chain you **see the states**. In an HMM you **cannot** — you
only see noisy signals they emit.

```
   X1  ->  X2  ->  X3  ->  ...        HIDDEN states     (what you want to know)
   |       |       |
   v       v       v
   E1      E2      E3                 EVIDENCE / observations  (what you can see)
```

> **The analogy your textbook uses** (and the slides tell you to work through):
> a **security guard in an underground installation** who never sees the sky.
> Every day the guard sees whether the visiting employee **carries an umbrella**.
> From that alone, they infer whether it is **raining** outside.
> Rain is hidden; umbrella is evidence.

### An HMM is fully specified by three things

| Symbol | Name | What it holds |
|---|---|---|
| **π** | **Initial probabilities** | `P(X1)` — where you start |
| **A** | **Transition matrix** | `P(X_t | X_(t−1))` — hidden → hidden |
| **B** | **Emission matrix** | `P(E_t | X_t)` — hidden → observed |

> **"Assume equal likelihood for initial state"** appears in the past paper. With
> 3 states that means **π = 1/3 each**. With 2 states, **0.5 each**.

---

## 5. The four inference tasks — *name them correctly, they carry marks*

| Task | Formula | Plain English | Time asked about |
|---|---|---|---|
| **Filtering** | `P(X_t | E_1…t)` | Where am I **now**, given everything seen so far? | **now** |
| **Prediction** | `P(X_(t+k) | E_1…t)` | Where will I be **later**? | **future** |
| **Smoothing** | `P(X_k | E_1…t)`, `0 < k < t` | Where **was** I at an earlier point, now that I know more? | **past** |
| **Most Likely Explanation** | `argmax_(X_1…t) P(X_1…t | E_1…t)` | What is the **single best whole path**? | **whole sequence** |

- **Filtering / Prediction / Smoothing** → the **Forward algorithm** (and
  forward-backward for smoothing). These give you **probabilities**.
- **Most Likely Explanation** → the **Viterbi algorithm**. This gives you a
  **sequence of states**.

> **The distinction that gets tested:** Forward answers *"how likely?"*;
> Viterbi answers *"which path?"*. Forward **sums**, Viterbi **maximises**.
> Everything else about them is identical.

---

## 6. Formula box

```
FORWARD  (sum over predecessors)

    alpha_1(j)  =  pi(j) · b_j(o_1)                          initialisation
    alpha_t(j)  =  [ SUM_i  alpha_(t−1)(i) · a_ij ] · b_j(o_t)    recursion
    P(O)        =  SUM_j alpha_T(j)                          termination


VITERBI  (max over predecessors + remember which one)

    v_1(j)  =  pi(j) · b_j(o_1)
    v_t(j)  =  [ MAX_i  v_(t−1)(i) · a_ij ] · b_j(o_t)
    bp_t(j) =  argmax_i [ v_(t−1)(i) · a_ij ]                 BACKPOINTER

    a_ij    = P(state j | state i)      transition
    b_j(o)  = P(observation o | state j) emission
```

> **They are the SAME recursion with SUM replaced by MAX.** If you can do one you
> can do the other. Viterbi additionally records **backpointers** so you can
> reconstruct the path at the end.

### ⚠ The class-specific quirk: normalise at t = 1

Both the slides **and** the official answer key **normalise after the
initialisation step only**, then stop normalising. In the Apr 2025 solution:

```
   P(St at t=1) = (1/3)(0.30) = 0.1
   P(Uo at t=1) = (1/3)(0.60) = 0.2
   P(Cr at t=1) = (1/3)(0.90) = 0.3       sum = 0.6

   "After normalized weights are:"
   V1(St) = 0.1/0.6 = 0.167
   V1(Uo) = 0.2/0.6 = 0.333
   V1(Cr) = 0.3/0.6 = 0.500              <- 1 full mark for this step
```

The paper says **"Strictly follow the approach as discussed in class only."**
So **do normalise at t = 1**, and do not normalise afterwards. It is worth a mark
on its own.

---

## 7. NUMERICAL — Forward algorithm (the slides' own worked example)

**Hidden states:** `L` = Low pressure, `H` = High pressure
**Observations:** `S` = Sunny, `R` = Rainy

| | π |
|---|---|
| L | 0.5 |
| H | 0.5 |

**Transition A** `P(to | from)`

| from \ to | L | H |
|---|---|---|
| **L** | 0.5 | 0.5 |
| **H** | 0.2 | 0.8 |

**Emission B** `P(obs | state)`

| state | S | R |
|---|---|---|
| **L** | 0.2 | 0.8 |
| **H** | 0.6 | 0.4 |

**Q: Find the probability of the observation sequence `S – S – R`.**

### Initialization (t = 1, observe S)
```
alpha(L) = P(L)·P(S|L) = 0.5 × 0.2 = 0.1
alpha(H) = P(H)·P(S|H) = 0.5 × 0.6 = 0.3
                                     sum = 0.4

NORMALISE:   L -> 0.1/0.4 = 0.25        H -> 0.3/0.4 = 0.75
```

### Recursion, t = 2 (observe S)
```
alpha(L) = 0.25 × P(L|L) × P(S|L)  +  0.75 × P(L|H) × P(S|L)
         = 0.25 × 0.5 × 0.2        +  0.75 × 0.2 × 0.2
         =        0.025            +        0.030          =  0.055

alpha(H) = 0.25 × 0.5 × 0.6        +  0.75 × 0.8 × 0.6
         =        0.075            +        0.360          =  0.435
```

### Recursion, t = 3 (observe R)
```
alpha(L) = 0.055 × 0.5 × 0.8       +  0.435 × 0.2 × 0.8
         =        0.022            +        0.0696         =  0.0916

alpha(H) = 0.055 × 0.5 × 0.4       +  0.435 × 0.8 × 0.4
         =        0.011            +        0.1392         =  0.1502
```

### Termination
```
P(S-S-R) = 0.0916 + 0.1502 = 0.2418
```

The trellis, laid out as the slides draw it:

| | t=1 (S) | t=2 (S) | t=3 (R) |
|---|---|---|---|
| **L** | 0.25 | 0.055 | 0.0916 |
| **H** | 0.75 | 0.435 | 0.1502 |
| | | | **Σ = 0.2418** |

> **Why 0.2418 and not 0.09672?** Because of the normalisation at t = 1 — you
> divided by 0.4 and never put it back. The true joint `P(S,S,R) = 0.4 × 0.2418
> = 0.09672`. **Give 0.2418**, because that is the class method and what the
> marking scheme expects. If you want to be safe, add one line: *"normalised at
> t=1 as per class approach; un-normalised joint = 0.09672."*

---

## 8. PAST PAPER — Apr 2025, Q4 (8 marks) fully worked

> *"In a hospital, patients can be in one of three health states: Stable, Under
> Observation, or Critical… Using the sequence of patient outcomes ("Severe",
> "Mild"), apply the Viterbi algorithm to determine the most likely sequence of
> health states."*

### Marking scheme (from the paper)
```
a)  Transition matrix (table)          1 mark
    Transition DIAGRAM                 0.5 mark
    Emission matrix (table)            1 mark
    Emission DIAGRAM                   0.5 mark
b)  Initial probabilities              0.5 mark
    Diagram at t=1                     0.5 mark
    Normalised V1 values               1 mark
    V2(St)  0.5 · V2(Uo) 0.5 · V2(Cr) 0.5
    Final trellis diagram              0.5 mark
    Answer + justification             1 mark
```

> **Read that again: 1.5 of 8 marks are for DIAGRAMS.** The question says
> *"Depict them with neat diagrams **in addition to** tabular representation."*
> **Draw the state diagram. It is free marks and takes 60 seconds.**

### Part (a) — extract the matrices

States: `St` (Stable), `Uo` (Under Observation), `Cr` (Critical).
Observations: `M` (Mild), `Sv` (Severe).

**Transition Probability Matrix** — rows sum to 1 here:

| from \ to | Stable | Under Obs | Critical |
|---|---|---|---|
| **Stable** | 0.5 | 0.4 | 0.1 |
| **Under Observation** | 0.2 | 0.6 | 0.2 |
| **Critical** | **0.0** | 0.2 | 0.8 |

> `P(Stable | Critical) = 0.0` — the text never mentions Critical → Stable, and
> the other two (0.8 + 0.2) already sum to 1. **Say this explicitly in your
> answer**; the instructions ask you to state assumptions.

**Emission Probability Matrix:**

| state | Mild | Severe |
|---|---|---|
| **Stable** | 0.7 | 0.3 |
| **Under Observation** | 0.4 | 0.6 |
| **Critical** | 0.1 | 0.9 |

> The question only gives you one number per row ("Stable exhibits Mild 70% of
> the time"). The other is the **complement**. Row sums = 1.

**Diagram** — draw 3 circles with self-loops and labelled arrows for transitions,
then a second diagram with arrows from each state to `Mild` / `Severe`.

### Part (b) — Viterbi on `("Severe", "Mild")`

**Initial:** *"Assume equal likelihood"* → `P(St) = P(Uo) = P(Cr) = 1/3`.

**t = 1, observe "Severe":**
```
P(St at t=1) = (1/3) × P(Sv|St) = (1/3)(0.30) = 0.1
P(Uo at t=1) = (1/3) × P(Sv|Uo) = (1/3)(0.60) = 0.2
P(Cr at t=1) = (1/3) × P(Sv|Cr) = (1/3)(0.90) = 0.3
                                          sum = 0.6

NORMALISE:
V1(St) = 0.1/0.6 = 0.167
V1(Uo) = 0.2/0.6 = 0.333
V1(Cr) = 0.3/0.6 = 0.500
```

**t = 2, observe "Mild":**

```
V2(St) = Max[ V1(St)×P(St|St), V1(Uo)×P(St|Uo), V1(Cr)×P(St|Cr) ] × P(Mild|St)
       = Max[ 0.167×0.50,      0.333×0.20,      0.500×0.00      ] × 0.70
       = Max[ 0.05845,         0.04662,         0               ]
       = 0.058                                    <- best predecessor: St

V2(Uo) = Max[ 0.167×0.40,      0.333×0.60,      0.500×0.20      ] × 0.40
       = Max[ 0.02672,         0.07992,         0.04000         ]
       = 0.079                                    <- best predecessor: Uo

V2(Cr) = Max[ 0.167×0.10,      0.333×0.20,      0.500×0.80      ] × 0.10
       = Max[ 0.00167,         0.00666,         0.04000         ]
       = 0.040                                    <- best predecessor: Cr
```

The trellis:

| | t=1 ("Severe") | t=2 ("Mild") | best predecessor |
|---|---|---|---|
| **St** | 0.167 | 0.058 | St |
| **Uo** | 0.333 | **0.079** ← max | **Uo** |
| **Cr** | **0.500** ← max | 0.040 | Cr |

### ⚠ The answer key and correct Viterbi disagree here — read this

**The official answer key states: `Critical → Under Observation`.**

It gets there by taking the **argmax at each time step independently**: `Cr` is
highest at t=1 (0.500), `Uo` is highest at t=2 (0.079).

**Proper Viterbi backtracking gives `Under Observation → Under Observation`**,
because `V2(Uo)`'s maximising predecessor is `Uo` (0.07992), not `Cr` (0.04000).

Check the three full paths directly:

| path | joint score | |
|---|---|---|
| `St → Uo` | `0.167 × 0.4 × 0.4 = 0.0267` | |
| **`Uo → Uo`** | **`0.333 × 0.6 × 0.4 = 0.0799`** | ← **genuinely the maximum** |
| `Cr → Uo` | `0.500 × 0.2 × 0.4 = 0.0400` | ← the paper's answer |

`Uo → Uo` scores twice what `Cr → Uo` does. The marking scheme is wrong on this
step — it skipped the backpointer.

**What to actually do in the exam:**
1. Lay it out **exactly** as the scheme does — normalise at t=1, then the three
   `Max[...]` lines. That is where 3.5 of the marks are, and it is identical
   either way.
2. **Add a backpointer column** to your trellis. It costs one column.
3. State the answer from backtracking, and add one sentence:
   *"By backtracking the stored pointer from V2(Uo), the most likely sequence is
   Uo → Uo (score 0.0799). Note the per-step argmax would suggest Cr → Uo, but
   that path scores only 0.0400."*

That sentence protects you under either marking. A grader following the scheme
sees their answer named; a grader who knows Viterbi sees you did it properly.

---

## 9. PAST PAPER — Apr 2025, Q5c (3 marks) fully worked

> *"Calculate the missing probability values and determine the likelihood that a
> Tata Sky customer's behavior follows this sequence: (purchase new channel
> subscription, Continue Existing Subscription, purchase new channel
> subscription, purchase new channel subscription). Calculate the initial
> probability using the given sequence."*

### The matrices as printed (note the layout!)

**Transition Probability Matrix** — the header says
`← Previous` across the top and `Current ↓` down the side. So **columns are the
previous state and each COLUMN sums to 1.**

| Current ↓ \ Previous → | Continue Existing (C) | Purchase New (P) |
|---|---|---|
| **Continue Existing** | 0.6 | **??** |
| **Purchase New** | **??** | 0.2 |

**Fill the gaps so each column sums to 1:**
```
column C:  0.6 + ?? = 1   ->  P(P|C) = 0.4
column P:  ?? + 0.2 = 1   ->  P(C|P) = 0.8
```

| | from C | from P |
|---|---|---|
| **to C** | 0.6 | **0.8** |
| **to P** | **0.4** | 0.2 |

**Emission Probability Matrix** — same layout, columns sum to 1:

| Evidence ↓ | Continue Existing | Purchase New |
|---|---|---|
| Opt for the Deal of the Day | 0.1 | 0.4 |
| Rent a movie | **??** | 0.3 |
| Watch free channels | 0.4 | **??** |

```
column C:  0.1 + ?? + 0.4 = 1   ->  ?? = 0.5
column P:  0.4 + 0.3 + ?? = 1   ->  ?? = 0.3
```

| | Continue Existing | Purchase New |
|---|---|---|
| Deal of the Day | 0.1 | 0.4 |
| Rent a movie | **0.5** | 0.3 |
| Watch free channels | 0.4 | **0.3** |

### Initial probability
The sequence **starts with** "purchase new channel subscription", so by the class
convention: **`P(P) = 1`, `P(C) = 0`.**

### The likelihood
The sequence is over **states**, not observations, so the emission matrix is
**not used here** — it was only needed for the "missing values" part.

```
Sequence: P -> C -> P -> P

P(P, C, P, P) = P(P) · P(C|P) · P(P|C) · P(P|P)
              =  1  ×   0.8   ×   0.4   ×   0.2
              = 0.064
```

**Final answer: 0.064** ✓ (matches the official key)

> **The trap here is the matrix orientation.** If you had read the matrix
> row-wise you would have used `P(C|P) = 0.4` and `P(P|C) = 0.8`, giving
> `1 × 0.4 × 0.8 × 0.2 = 0.064` — the same number by coincidence, because the two
> values simply swap in the product. **You will not always be that lucky.**
> Always check which direction sums to 1.

---

## 10. Solved-samples deck — the ride-sharing HMM

> *"Users choose between Economy, Premium, or Luxury… For the observations
> (short-trip, long-trip), what is the most likely sequence of ride category?"*

**Transitions** (from the text — "60% of users who chose Economy upgrade to
Premium, 40% continue with Economy"):

| from \ to | Economy | Premium | Luxury |
|---|---|---|---|
| **Economy** | 0.40 | 0.60 | 0.00 |
| **Premium** | 0.05 | 0.75 | 0.20 |
| **Luxury** | 0.00 | 0.10 | 0.90 |

**Emissions** ("Economy for short trips 80%, Premium for longer trips 70%,
Luxury for longer trips 30%"):

| state | short-trip | long-trip |
|---|---|---|
| **Economy** | 0.80 | 0.20 |
| **Premium** | 0.30 | 0.70 |
| **Luxury** | 0.70 | 0.30 |

> **Be careful reading emission percentages out of prose.** "Economy for short
> trips 80% of the time" is `P(short | Economy) = 0.8`, so
> `P(long | Economy) = 0.2`. Check every row sums to 1 and **state your reading
> as an assumption** — the instructions explicitly invite that.

Then run Viterbi on `(short-trip, long-trip)` exactly as in §8.

---

## 11. You try

**Q1 (Markov chain).** Using the Computer/Media transition matrix from §3
(`P(C|C)=0.4, P(M|C)=0.6, P(C|M)=0.2, P(M|M)=0.8`), find the probability of the
sequence `(Media, Computer, Computer, Media)`. State the initial probability you
use and why.

**Q2 (most likely pattern).** Same matrix. A customer starts with **Media**.
What is the most likely pattern over the next 2 visits, and its probability?

**Q3 (missing values).** Complete this transition matrix, where **columns are the
previous state**:

| Current ↓ \ Previous → | A | B |
|---|---|---|
| **A** | ?? | 0.35 |
| **B** | 0.30 | ?? |

Then compute `P(A, B, B, A)` given the sequence starts at A.

**Q4 (Forward).** Using the L/H pressure HMM from §7, compute
`P(R – S)` — a two-step observation sequence, Rainy then Sunny. Normalise at
t = 1 as per the class method. Show the trellis.

**Q5 (Viterbi, full past-paper style).** Same L/H HMM. Find the **most likely
hidden state sequence** for the observations `(S, R)`. Normalise at t=1, show
`V1`, `V2`, **and a backpointer column**, then state the answer.

**Q6 (build the model from prose).** A website classifies visitors as
**Browsing**, **Comparing** or **Buying**.
- A Browsing visitor stays Browsing 60% of the time, moves to Comparing 30%, Buying 10%.
- A Comparing visitor returns to Browsing 20%, stays Comparing 50%, moves to Buying 30%.
- A Buying visitor stays Buying 70% and drops to Browsing 30%.
- Browsing visitors view **many pages** 80% of the time; Comparing visitors view
  many pages 60% of the time; Buying visitors view many pages 20% of the time.
  (The alternative observation is **few pages**.)

(a) Write both matrices, checking each row sums to 1.
(b) Assuming equal initial likelihood, run **Viterbi** on the observation
sequence `(few pages, many pages)`. Normalise at t=1. Give the most likely state
sequence **with backpointers**.

**Q7 (concept).** Name the four inference tasks in temporal models, give the
formula for each, and say which algorithm you would use.

**Q8 (concept).** Forward and Viterbi have almost the same recursion. State the
**one** difference in the recursion and the **one** extra thing Viterbi stores.

---

## 12. Answers

<details>
<summary>Open only after attempting</summary>

**Q1.** The sequence starts with **Media**, so `P(M) = 1, P(C) = 0` — the class
convention is to set the initial probability to 1 for the state the sequence
begins in.

```
P(M, C, C, M) = P(M) · P(C|M) · P(C|C) · P(M|C)
              =  1  ×   0.2   ×   0.4   ×   0.6
              = 0.048
```

**Q2.** Starting at Media, choose each next state to maximise the product:
```
From M:  P(M|M) = 0.8  >  P(C|M) = 0.2   ->  Media
From M:  P(M|M) = 0.8  >  P(C|M) = 0.2   ->  Media

P(M, M, M) = 1 × 0.8 × 0.8 = 0.64
```
**Most likely pattern: `(Media, Media, Media)`, probability 0.64.**
Media is a "sticky" state — once there, the customer tends to stay.

**Q3.** Columns must sum to 1:
```
column A:  ?? + 0.30 = 1   ->  P(A|A) = 0.70
column B:  0.35 + ?? = 1   ->  P(B|B) = 0.65
```

| | from A | from B |
|---|---|---|
| **to A** | **0.70** | 0.35 |
| **to B** | 0.30 | **0.65** |

```
P(A, B, B, A) = P(A) · P(B|A) · P(B|B) · P(A|B)
              =  1  ×  0.30   ×  0.65   ×  0.35
              = 0.068  (0.06825)
```

**Q4 — Forward on `R – S`**

t = 1, observe **R**:
```
alpha(L) = 0.5 × P(R|L) = 0.5 × 0.8 = 0.40
alpha(H) = 0.5 × P(R|H) = 0.5 × 0.4 = 0.20
                                sum = 0.60

NORMALISE:  L -> 0.40/0.60 = 0.667      H -> 0.20/0.60 = 0.333
```

t = 2, observe **S**:
```
alpha(L) = 0.667 × P(L|L) × P(S|L)  +  0.333 × P(L|H) × P(S|L)
         = 0.667 × 0.5 × 0.2        +  0.333 × 0.2 × 0.2
         = 0.0667                   +  0.0133          = 0.0800

alpha(H) = 0.667 × 0.5 × 0.6        +  0.333 × 0.8 × 0.6
         = 0.2000                   +  0.1600          = 0.3600
```

| | t=1 (R) | t=2 (S) |
|---|---|---|
| **L** | 0.667 | 0.080 |
| **H** | 0.333 | 0.360 |

```
P(R-S) = 0.080 + 0.360 = 0.440
```

**Q5 — Viterbi on `(S, R)`**

t = 1, observe **S** (same as §7):
```
L: 0.5 × 0.2 = 0.1        H: 0.5 × 0.6 = 0.3        sum = 0.4
NORMALISE:  V1(L) = 0.25        V1(H) = 0.75
```

t = 2, observe **R**:
```
V2(L) = Max[ V1(L)×P(L|L), V1(H)×P(L|H) ] × P(R|L)
      = Max[ 0.25×0.5,     0.75×0.2     ] × 0.8
      = Max[ 0.125,        0.150        ] × 0.8
      = 0.150 × 0.8 = 0.120              backpointer -> H

V2(H) = Max[ 0.25×0.5,     0.75×0.8     ] × 0.4
      = Max[ 0.125,        0.600        ] × 0.4
      = 0.600 × 0.4 = 0.240              backpointer -> H
```

| | t=1 (S) | t=2 (R) | backpointer |
|---|---|---|---|
| **L** | 0.25 | 0.120 | H |
| **H** | **0.75** | **0.240** ← max | **H** |

Best at t=2 is `H` (0.240); its backpointer is `H`.

**Most likely sequence: `High → High`**, score 0.240.

Here the per-step argmax (`H` at t=1, `H` at t=2) and proper backtracking
**agree** — so no ambiguity in this one. Note that in §8 they did **not**.

**Q6 — Website visitor HMM**

(a) **Transition matrix** (rows sum to 1):

| from \ to | Browsing | Comparing | Buying |
|---|---|---|---|
| **Browsing** | 0.60 | 0.30 | 0.10 |
| **Comparing** | 0.20 | 0.50 | 0.30 |
| **Buying** | 0.30 | 0.00 | 0.70 |

`P(Comparing | Buying) = 0.00` — only two destinations are given for Buying and
they already sum to 1. **State this as an assumption.**

**Emission matrix** (rows sum to 1):

| state | many pages | few pages |
|---|---|---|
| **Browsing** | 0.80 | 0.20 |
| **Comparing** | 0.60 | 0.40 |
| **Buying** | 0.20 | 0.80 |

(b) **Viterbi on `(few pages, many pages)`**, π = 1/3 each.

t = 1, observe **few pages**:
```
Br: (1/3)(0.20) = 0.0667
Co: (1/3)(0.40) = 0.1333
Bu: (1/3)(0.80) = 0.2667
                sum = 0.4667

NORMALISE:
V1(Br) = 0.0667/0.4667 = 0.143
V1(Co) = 0.1333/0.4667 = 0.286
V1(Bu) = 0.2667/0.4667 = 0.571
```

t = 2, observe **many pages**:
```
V2(Br) = Max[0.143×0.60, 0.286×0.20, 0.571×0.30] × 0.80
       = Max[0.0858,     0.0572,     0.1713    ] × 0.80
       = 0.1713 × 0.80 = 0.137           backpointer -> Bu

V2(Co) = Max[0.143×0.30, 0.286×0.50, 0.571×0.00] × 0.60
       = Max[0.0429,     0.1430,     0         ] × 0.60
       = 0.1430 × 0.60 = 0.086           backpointer -> Co

V2(Bu) = Max[0.143×0.10, 0.286×0.30, 0.571×0.70] × 0.20
       = Max[0.0143,     0.0858,     0.3997    ] × 0.20
       = 0.3997 × 0.20 = 0.080           backpointer -> Bu
```

| | t=1 (few) | t=2 (many) | backpointer |
|---|---|---|---|
| **Browsing** | 0.143 | **0.137** ← max | **Buying** |
| **Comparing** | 0.286 | 0.086 | Comparing |
| **Buying** | **0.571** | 0.080 | Buying |

Best at t=2 is **Browsing** (0.137); backpointer says **Buying**.

**Most likely sequence: `Buying → Browsing`.**

Here per-step argmax gives `Buying → Browsing` too (Bu highest at t=1, Br highest
at t=2) — so they agree. But **write the backpointer column anyway**; it is what
makes the answer defensible.

**Q7 — The four inference tasks**

| Task | Formula | Algorithm |
|---|---|---|
| **Filtering** | `P(X_t | E_1…t)` | Forward |
| **Prediction** | `P(X_(t+k) | E_1…t)` | Forward, then project forward |
| **Smoothing** | `P(X_k | E_1…t)`, `0 < k < t` | Forward–Backward |
| **Most Likely Explanation** | `argmax_(X_1…t) P(X_1…t | E_1…t)` | **Viterbi** |

**Q8.** The **only** difference in the recursion is that Forward takes a
**SUM** over predecessors while Viterbi takes a **MAX**:

```
Forward:  alpha_t(j) = [ SUM_i alpha_(t−1)(i) · a_ij ] · b_j(o_t)
Viterbi:  v_t(j)     = [ MAX_i v_(t−1)(i) · a_ij ] · b_j(o_t)
```

The extra thing Viterbi stores is the **backpointer**
`bp_t(j) = argmax_i [ v_(t−1)(i) · a_ij ]` — which predecessor won the max — so
the best path can be reconstructed by backtracking from the highest final value.

Conceptually: Forward asks *"how likely is this observation sequence, over all
possible paths?"*; Viterbi asks *"which single path is best?"*

</details>

---

## 13. Two-minute recall card

- **Markov assumption:** `P(S_t | S_1…S_(t−1)) = P(S_t | S_(t−1))`. The present screens off the past.
- **⚠ Check which way the transition matrix sums to 1** — the past paper uses **columns = previous state**.
- **Initial probability convention:** set it to **1** for whichever state the sequence starts in.
- Sequence probability = `P(start) × chain of transitions`. Slide answers: `0.096`, `0.128`, `0.384`.
- HMM = **π** (initial) + **A** (transition, hidden→hidden) + **B** (emission, hidden→observed).
- "Equal likelihood for initial state" → **1/3 each** for 3 states.
- Emission rows: the question gives one number, **the other is the complement**.
- **Four tasks:** Filtering `P(X_t|E_1..t)` · Prediction `P(X_t+k|E_1..t)` · Smoothing `P(X_k|E_1..t)` · **MLE** `argmax P(X_1..t|E_1..t)`.
- **Forward = SUM. Viterbi = MAX.** Same recursion otherwise. Viterbi also stores **backpointers**.
- **NORMALISE at t = 1 only** — class method, worth a full mark.
- Slide forward example: `P(S-S-R) = 0.2418`.
- Past paper Viterbi: `V1 = 0.167 / 0.333 / 0.500`, `V2 = 0.058 / 0.079 / 0.040`.
- Past paper Tata Sky: **0.064**.
- **1.5 of 8 marks are for DIAGRAMS.** Always draw the transition and emission diagrams.
- Write the **backpointer column** — the official key skipped it and got the path wrong.
