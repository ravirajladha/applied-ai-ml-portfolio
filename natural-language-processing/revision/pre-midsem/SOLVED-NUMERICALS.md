# NLP Pre-Midsem — Every Q1 & Q2 Solved
**AIMLCLZG525 · End-Semester · Q1 + Q2 = 10 of 40 marks**

Every **real** Q1 and Q2 from all four past papers, with the question exactly as
printed and the solution worked line by line — then fresh practice questions.

Read [`CHEATSHEET.md`](CHEATSHEET.md) first if you don't know the theory.

> **The pattern, across all four papers:**
> **Q1** = bigram Laplace probability **+** a neural-LM forward pass ending in softmax.
> **Q2** = an HMM — **Viterbi** (best tag sequence) or **Forward** (total probability).
> Nothing else from pre-midsem has ever appeared.

## Contents
- [Q1 — Feb 2026: Laplace + ReLU network](#q1--feb-2026-regular)
- [Q1 — Mar 2026: bigram + Sigmoid network](#q1--mar-2026-makeup)
- [Q2 — Feb 2026: Viterbi + Forward](#q2--feb-2026-regular)
- [Q2 — Mar 2026: Viterbi + Forward + prediction](#q2--mar-2026-makeup)
- [Q1/Q2 — Oct 2024: two Forward questions](#q1q2--oct-2024-regular)
- [Q1/Q2 — Undated paper: two Viterbi questions](#q1q2--undated-paper)
- [Practice questions](#practice-questions)

---
---

# Q1 — Feb 2026 (regular)
### `[2 + 3 = 5 Marks]`

> You are developing a text completion system and want to compare a statistical
> Bigram model against a simple Feedforward Neural Language Model (FFNN-LM).
> The training data consists of only these three sentences:
> ```
> <s> deep learning </s>
> <s> machine learning </s>
> <s> deep thought </s>
> ```
> You need to predict the next word following the context word **"deep"**.
>
> **Part A [2 Marks]:** Calculate the **Laplace Smoothed** probability of the word
> "learning" occurring after "deep". (Assume the Vocabulary V consists of all
> unique words in the corpus, **including `<s>` and `</s>`**.)
>
> **Part B [3 Marks]:** Model architecture — Input: word embedding for "deep"
> `x = [0.4, -0.2]`. Hidden layer: 1 neuron with **ReLU**. Weights `w = [0.5, -0.5]`,
> bias `b = 0.1`. Output layer computes unnormalized scores:
> `z(learning) = 2*h`, `z(thought) = 0.5*h`.
> Perform the forward pass to calculate the final **Softmax probability** for "learning".

## Solution — Part A `[2 marks]`

```
STEP 1  Identify the vocabulary V                              (0.5 marks)

        Unique tokens, INCLUDING <s> and </s>:
            <s> , </s> , deep , learning , machine , thought

            V = 6

STEP 2  Get the counts                                         (0.5 marks)

        count("deep learning") = 1      (sentence 1 only)
        count("deep")          = 2      (sentences 1 and 3)

STEP 3  Substitute into the Laplace formula                    (0.5 marks)

                    count(deep learning) + 1        1 + 1
        P  =  ------------------------------  =  ---------
                    count(deep) + V                2 + 6

STEP 4  Final answer                                           (0.5 marks)

        P  =  2 / 8  =  0.25      (or 1/4)
```

> **Compare with unsmoothed MLE:** `1/2 = 0.5`. Laplace halved it, because it
> had to give probability mass to the four words that never follow *deep*.

## Solution — Part B `[3 marks]`

```
STEP 1  Pre-activation (the weighted sum)                      (1.0 mark)

        z = (w1 × x1) + (w2 × x2) + b
          = (0.5 × 0.4) + (-0.5 × -0.2) + 0.1
          = 0.20 + 0.10 + 0.10
          = 0.40
                        ^^^^ note: negative × negative = POSITIVE

STEP 2  Apply ReLU                                             (0.5 marks)

        h = ReLU(0.4) = max(0.4, 0) = 0.4

STEP 3  Output layer scores                                    (0.5 marks)

        z(learning) = 2   × 0.4 = 0.8
        z(thought)  = 0.5 × 0.4 = 0.2

STEP 4  Softmax                                                (1.0 mark)

        e^0.8 = 2.2255
        e^0.2 = 1.2214
        sum   = 3.4469

                          e^0.8            2.2255
        P(learning) = ------------- = ------------- = 0.6457
                      e^0.8 + e^0.2      3.4469

        P(learning) ≈ 0.65
```
*(Official key: 0.4 / 0.4 / 0.8 and 0.2 / ≈0.645 — all confirmed.)*

---
---

# Q1 — Mar 2026 (makeup)
### `[2 + 3 = 5 Marks]`

> Comparing a Bigram model against an FFNN-LM for a weather prediction system.
> ```
> <s> sun hot </s>
> <s> rain cold </s>
> <s> sun bright </s>
> ```
> Predict the next word following **"sun"**.
>
> **Part A [2 Marks]:** Calculate the probability of "bright" occurring after "sun".
> (Assume V consists of all unique words in the corpus, including `<s>` and `</s>`.)
>
> **Part B [3 Marks]:** Input `x = [0.5, 1.0]`. Hidden layer: 1 neuron with
> **Sigmoid**. Weights `w = [0.2, 0.4]`, bias `b = -0.5`.
> `z(bright) = 1.5*h`, `z(hot) = 0.5*h`. Find the softmax probability of "bright".

## Solution — Part A `[2 marks]`

```
Vocabulary:  <s> , </s> , sun , hot , rain , cold , bright     ->  V = 7

Counts:      count("sun bright") = 1        count("sun") = 2

UNSMOOTHED (MLE):
        P = 1 / 2 = 0.50

LAPLACE (add-1):
             1 + 1        2
        P = -------- = ------- = 0.2222
             2 + 7        9
```

> ⚠️ **The question is ambiguous here.** Unlike the Feb paper it does not say the
> word "Laplace" — but it *does* hand you V and tell you to include `<s>`/`</s>`,
> which is only needed for smoothing. **Give the Laplace answer (0.2222) as your
> main one, show the MLE (0.5) in one line, and state your assumption.** That
> covers you either way, and "state assumptions clearly" is printed on the front
> of your exam paper.

## Solution — Part B `[3 marks]`

```
STEP 1  z = (0.2 × 0.5) + (0.4 × 1.0) + (-0.5)
          = 0.10 + 0.40 - 0.50
          = 0.00

STEP 2  h = sigmoid(0) = 1 / (1 + e^0) = 1 / (1 + 1) = 0.5
                                                        ^^^ sigmoid(0) is ALWAYS 0.5

STEP 3  z(bright) = 1.5 × 0.5 = 0.75
        z(hot)    = 0.5 × 0.5 = 0.25

STEP 4  e^0.75 = 2.1170
        e^0.25 = 1.2840
        sum    = 3.4010

        P(bright) = 2.1170 / 3.4010 = 0.6225   ≈ 0.62
```

---
---

# Q2 — Feb 2026 (regular)
### `[3 + 2 = 5 Marks]`

> **(A)** An HMM-based POS tagger uses the following probabilities.
>
> | Current / Next | DT | NN | VB |
> |---|---|---|---|
> | **START** | 0.4 | 0.4 | 0.2 |
> | **DT** | 0.2 | 0.7 | 0.1 |
> | **NN** | 0.1 | 0.3 | 0.6 |
> | **VB** | 0.5 | 0.4 | 0.1 |
>
> | Tag / Word | "a" | "dog" | "barks" |
> |---|---|---|---|
> | **DT** | 0.85 | 0.10 | 0.05 |
> | **NN** | 0.10 | 0.80 | 0.10 |
> | **VB** | 0.05 | 0.10 | 0.85 |
>
> For the phrase **"a dog barks"**, determine the most likely sequence of POS
> tags using the **Viterbi** algorithm. Show all intermediate calculations,
> including initialization, recursion and termination. **[3 Marks]**
>
> **(B)** A speech recognition system uses an HMM with states Vowel (V),
> Consonant (C), Silence (S). `π(V)=0.5, π(C)=0.3, π(S)=0.2`.
>
> | From / To | V | C | S |  | Observation | V | C | S |
> |---|---|---|---|---|---|---|---|---|
> | **V** | 0.6 | 0.3 | 0.1 | | **"ah"** | 0.8 | 0.1 | 0.1 |
> | **C** | 0.4 | 0.4 | 0.2 | | **"sh"** | 0.1 | 0.7 | 0.2 |
> | **S** | 0.3 | 0.3 | 0.4 | | **sil** | 0.05 | 0.05 | 0.9 |
>
> Observed `O = ("ah","sh")`. Compute the posterior distribution over hidden
> states at time step 2 using the **Forward** algorithm **[1 Mark]**, and say
> which state is most likely and why **[1 Mark]**.

## Solution — (A) Viterbi `[3 marks]`

**1. Initialization — word 1 = "a"**   `P(tag|START) × P(a|tag)`
```
DT:  0.4 × 0.85  =  0.34         <- only real survivor
NN:  0.4 × 0.10  =  0.04
VB:  0.2 × 0.05  =  0.01
```

**2. Recursion — word 2 = "dog"**   `max(prev × transition) × P(dog|tag)`
```
DT at "dog":   from DT 0.34 × 0.2 = 0.068    <- max
               from NN 0.04 × 0.1 = 0.004
               from VB 0.01 × 0.5 = 0.005
               0.068 × 0.10  =  0.0068                 backpointer: DT

NN at "dog":   from DT 0.34 × 0.7 = 0.238    <- max
               from NN 0.04 × 0.3 = 0.012
               from VB 0.01 × 0.4 = 0.004
               0.238 × 0.80  =  0.1904                 backpointer: DT

VB at "dog":   from DT 0.34 × 0.1 = 0.034    <- max
               from NN 0.04 × 0.6 = 0.024
               from VB 0.01 × 0.1 = 0.001
               0.034 × 0.10  =  0.0034                 backpointer: DT
```

**3. Recursion — word 3 = "barks"**
```
DT:  max(0.0068×0.2, 0.1904×0.1, 0.0034×0.5) = 0.01904 × 0.05 = 0.000952   bp: NN
NN:  max(0.0068×0.7, 0.1904×0.3, 0.0034×0.4) = 0.05712 × 0.10 = 0.005712   bp: NN
VB:  max(0.0068×0.1, 0.1904×0.6, 0.0034×0.1) = 0.11424 × 0.85 = 0.097104   bp: NN
                                 ^^^^^^^^^^^ max
```

**Completed table**

| | a | dog | barks |
|---|---|---|---|
| **DT** | **0.34** | 0.0068 | 0.000952 |
| **NN** | 0.04 | **0.1904** | 0.005712 |
| **VB** | 0.01 | 0.0034 | **0.097104** |

**4. Termination and backtrace**
```
Largest final cell:  VB  =  0.097104
    VB  <- backpointer NN  <- backpointer DT

ANSWER:   a/DT    dog/NN    barks/VB
```

## Solution — (B) Forward `[2 marks]`

```
alpha1 (after "ah")  =  pi(state) × P(ah|state)

    V:  0.5 × 0.8  =  0.40
    C:  0.3 × 0.1  =  0.03
    S:  0.2 × 0.1  =  0.02

alpha2 (after "sh")  =  [ SUM over i of alpha1(i) × a(i->j) ] × P(sh|j)
                          ^^^ SUM, because this is FORWARD, not Viterbi

    V:  [0.40×0.6 + 0.03×0.4 + 0.02×0.3] × 0.1
      = [0.240 + 0.012 + 0.006] × 0.1  =  0.258 × 0.1  =  0.0258

    C:  [0.40×0.3 + 0.03×0.4 + 0.02×0.3] × 0.7
      = [0.120 + 0.012 + 0.006] × 0.7  =  0.138 × 0.7  =  0.0966

    S:  [0.40×0.1 + 0.03×0.2 + 0.02×0.4] × 0.2
      = [0.040 + 0.006 + 0.008] × 0.2  =  0.054 × 0.2  =  0.0108

P(O)  =  0.0258 + 0.0966 + 0.0108  =  0.1332

POSTERIOR  =  each alpha2 divided by the total:

    P(V2 | O)  =  0.0258 / 0.1332  =  0.194
    P(C2 | O)  =  0.0966 / 0.1332  =  0.725     <- highest
    P(S2 | O)  =  0.0108 / 0.1332  =  0.081
```
**Most likely state at time 2: Consonant (C).**
> **Why:** the observation *"sh"* has a **very high emission probability from the
> Consonant state (0.7)**, and sufficient probability mass transitions into C
> from the earlier states.

---
---

# Q2 — Mar 2026 (makeup)
### `[3 + 2 = 5 Marks]`

> **(A)** Same setup, tags DT / NN / VB:
>
> | Current / Next | DT | NN | VB |
> |---|---|---|---|
> | **START** | 0.3 | 0.4 | 0.3 |
> | **DT** | 0.2 | 0.5 | 0.3 |
> | **NN** | 0.1 | 0.3 | 0.6 |
> | **VB** | 0.4 | 0.4 | 0.2 |
>
> | Tag / Word | "that" | "fish" | "swims" |
> |---|---|---|---|
> | **DT** | 0.6 | 0.2 | 0.2 |
> | **NN** | 0.2 | 0.6 | 0.2 |
> | **VB** | 0.1 | 0.3 | 0.6 |
>
> For **"that fish swims"**, apply Viterbi. Show initialization, recursion and
> backtracking. **[3 Marks]**
>
> **(B)** HMM with states V, C, N. `π(V)=0.2, π(C)=0.5, π(N)=0.3`.
>
> | From / To | V | C | N | | Obs | V | C | N |
> |---|---|---|---|---|---|---|---|---|
> | **V** | 0.1 | 0.7 | 0.2 | | **"ah"** | 0.4 | 0.4 | 0.2 |
> | **C** | 0.6 | 0.2 | 0.2 | | **"sh"** | 0.2 | 0.2 | 0.6 |
> | **N** | 0.3 | 0.3 | 0.4 | | **"uh"** | 0.6 | 0.1 | 0.3 |
>
> `O = ("ah","sh","uh")`. Compute the filtered posterior `P(q₂ | o₁,o₂)`
> **[1 Mark]**. Then, **without any new forward computation**, determine
> `P(q₃ | o₁,o₂)` — the one-step prediction before observing "uh". **[1 Mark]**

## Solution — (A) Viterbi `[3 marks]`

**1. Initialization — "that"**
```
DT:  0.3 × 0.6  =  0.18        <- best
NN:  0.4 × 0.2  =  0.08
VB:  0.3 × 0.1  =  0.03
```

**2. Recursion — "fish"**
```
DT:  max(0.18×0.2, 0.08×0.1, 0.03×0.4) = max(0.036, 0.008, 0.012)
     = 0.036 × 0.2  =  0.0072                            bp: DT

NN:  max(0.18×0.5, 0.08×0.3, 0.03×0.4) = max(0.090, 0.024, 0.012)
     = 0.090 × 0.6  =  0.054                             bp: DT

VB:  max(0.18×0.3, 0.08×0.6, 0.03×0.2) = max(0.054, 0.048, 0.006)
     = 0.054 × 0.3  =  0.0162                            bp: DT
```

**3. Recursion — "swims"**
```
DT:  max(0.0072×0.2, 0.054×0.1, 0.0162×0.4) = max(0.00144, 0.0054, 0.00648)
     = 0.00648 × 0.2  =  0.001296                        bp: VB

NN:  max(0.0072×0.5, 0.054×0.3, 0.0162×0.4) = max(0.0036, 0.0162, 0.00648)
     = 0.0162 × 0.2  =  0.00324                          bp: NN

VB:  max(0.0072×0.3, 0.054×0.6, 0.0162×0.2) = max(0.00216, 0.0324, 0.00324)
     = 0.0324 × 0.6  =  0.01944                          bp: NN
                            ^^^^^^^ largest
```

**4. Backtracking**
```
Highest final probability = VB (0.01944)
    VB  <-  NN  <-  DT

ANSWER:   that/DT   fish/NN   swims/VB
```

## Solution — (B) Forward + prediction `[2 marks]`

```
alpha1 (after "ah"):
    V:  0.2 × 0.4  =  0.08
    C:  0.5 × 0.4  =  0.20
    N:  0.3 × 0.2  =  0.06

alpha2 (after "sh"):
    V:  [0.08×0.1 + 0.20×0.6 + 0.06×0.3] × 0.2
      = [0.008 + 0.120 + 0.018] × 0.2 = 0.146 × 0.2 = 0.0292

    C:  [0.08×0.7 + 0.20×0.2 + 0.06×0.3] × 0.2
      = [0.056 + 0.040 + 0.018] × 0.2 = 0.114 × 0.2 = 0.0228

    N:  [0.08×0.2 + 0.20×0.2 + 0.06×0.4] × 0.6
      = [0.016 + 0.040 + 0.024] × 0.6 = 0.080 × 0.6 = 0.0480

Total = 0.0292 + 0.0228 + 0.0480 = 0.1000        (conveniently exactly 0.1)

FILTERED POSTERIOR  P(q2 | o1,o2):
    V:  0.0292 / 0.1  =  0.292
    C:  0.0228 / 0.1  =  0.228
    N:  0.0480 / 0.1  =  0.480      <- most likely at t=2
```

**One-step prediction — no new forward computation needed.** Just push the
posterior through the transition matrix:
```
P(q3 = j | o1,o2)  =  SUM over i of  P(q2 = i | o1,o2) × a(i -> j)

V:  0.292×0.1 + 0.228×0.6 + 0.480×0.3
  = 0.0292 + 0.1368 + 0.1440  =  0.310

C:  0.292×0.7 + 0.228×0.2 + 0.480×0.3
  = 0.2044 + 0.0456 + 0.1440  =  0.394      <- most likely at t=3

N:  0.292×0.2 + 0.228×0.2 + 0.480×0.4
  = 0.0584 + 0.0456 + 0.1920  =  0.296

    P(q3 | o1,o2)  =  ( V = 0.310 , C = 0.394 , N = 0.296 )
    check: 0.310 + 0.394 + 0.296 = 1.000  ✓
```
> **The trick this question tests:** *prediction* = take the posterior you already
> have and multiply by the transition matrix. **No emission is involved**, because
> you haven't observed the next symbol yet.

---
---

# Q1/Q2 — Oct 2024 (regular)

## Q1 `[5 Marks]` — Forward algorithm

> Emission probabilities:
>
> | Word | Noun | Verb | Adj |
> |---|---|---|---|
> | "cat" | 0.9 | – | 0.1 |
> | "jumps" | 0.3 | 0.7 | – |
> | "quickly" | – | 0.3 | 0.7 |
>
> Transitions: `Noun→Noun 0.5`, `Noun→Verb 0.5`, `Verb→Verb 0.7`, `Verb→Adj 0.3`.
> Using the **forward algorithm**, calculate the probability of the observation
> sequence **"cat jumps quickly"**.

### Solution
```
1. Initialization
   Initial state equally likely for Noun or Verb  ->  P = 1/2 each
   (state this assumption — the question doesn't give initial probabilities)

2. Forward step 1 — "cat"
   P(Noun) = 1/2 × 0.9 = 0.45
   Verb is not an option: the emission for "cat" as a Verb is "–" (zero)

3. Forward step 2 — "jumps"
   P(Verb) = P(Noun) × P(Noun→Verb) × P(jumps|Verb)
           = 0.45 × 0.5 × 0.7
           = 0.1575

4. Forward step 3 — "quickly"
   P(Adj)  = P(Verb) × P(Verb→Adj) × P(quickly|Adj)
           = 0.1575 × 0.3 × 0.7
           = 0.033075

5. Conclusion
   P("cat jumps quickly") = 0.0331
```
> Only one path survives, because every other route hits a `–` (zero emission).
> That's why the sums collapse to single terms here.

---

## Q2 `[5 Marks]` — Forward algorithm ⚠️ *official answer contains an error*

> | Transitions | S1 | S2 | | Emissions | S1 | S2 |
> |---|---|---|---|---|---|---|
> | **S1** | 0.7 | 0.3 | | **"X"** | 0.6 | 0.4 |
> | **S2** | 0.6 | 0.4 | | **"Y"** | 0.3 | 0.7 |
>
> Use the **Forward** algorithm for the sequence **"X Y"**, with initial
> probabilities `P(S1)=0.6`, `P(S2)=0.4`.

### Solution
```
1. Initialization (observation "X")
   alpha1(S1) = 0.6 × 0.6 = 0.36
   alpha1(S2) = 0.4 × 0.4 = 0.16

2. Forward step (observation "Y")

   alpha2(S1) = [ alpha1(S1) × a(S1->S1)  +  alpha1(S2) × a(S2->S1) ] × P(Y|S1)
              = [ 0.36 × 0.7  +  0.16 × 0.6 ] × 0.3
              = [ 0.252 + 0.096 ] × 0.3
              = 0.348 × 0.3  =  0.1044

   alpha2(S2) = [ alpha1(S1) × a(S1->S2)  +  alpha1(S2) × a(S2->S2) ] × P(Y|S2)
              = [ 0.36 × 0.3  +  0.16 × 0.4 ] × 0.7
              = [ 0.108 + 0.064 ] × 0.7
              = 0.172 × 0.7  =  0.1204

3. Total
   P("X Y") = 0.1044 + 0.1204 = 0.2248
```

> ### ⚠️ Read this — the printed answer key is wrong
> The official solution writes:
> ```
> P(S1) = (0.36 × 0.7 × 0.3) + (0.16 × 0.4 × 0.3) = 0.0756
> P(S2) = (0.36 × 0.3 × 0.7) + (0.16 × 0.6 × 0.7) = 0.1032
> ```
> It used **`a(S2→S2) = 0.4`** where it needed **`a(S2→S1) = 0.6`**, and
> **`a(S2→S1) = 0.6`** where it needed **`a(S2→S2) = 0.4`** — the two second
> terms are swapped. Its printed totals don't even match its own arithmetic.
>
> **Use the method above, not those numbers.** To reach state `j`, you sum over
> every predecessor `i` using **`a(i → j)`** — the arrow must *point at* the state
> you are computing. If a marker challenges you, that one sentence is your defence.

---
---

# Q1/Q2 — Undated paper

## Q1 `[2+2+1 = 5 Marks]` — Viterbi

> | Transitions | Noun | Verb | Adj | | Emissions | Noun | Verb | Adj |
> |---|---|---|---|---|---|---|---|---|
> | **Noun** | 0.4 | 0.3 | 0.3 | | **"run"** | 0.8 | 0.2 | – |
> | **Verb** | 0.1 | 0.8 | 0.1 | | **"fast"** | 0.6 | – | 0.4 |
> | **Adj** | 0.6 | 0.3 | 0.1 | | **"dog"** | 0.7 | 0.3 | – |
>
> Find the most likely POS tag sequence for **"run fast"** using Viterbi.

### Solution
```
No initial probabilities given  ->  assume equal, 1/3 each. STATE THIS.

t = 1  ("run")
    V(Noun) = 1/3 × 0.8 = 0.2667
    V(Verb) = 1/3 × 0.2 = 0.0667
    V(Adj)  = 1/3 × 0   = 0            ("run" is never an Adj)

t = 2  ("fast")

    For Noun:   from Noun  0.2667 × 0.4 × 0.6 = 0.0640    <- max
                from Verb  0.0667 × 0.1 × 0.6 = 0.0040
                from Adj   0      × 0.6 × 0.6 = 0
                => 0.0640, backpointer Noun

    For Verb:   emission P(fast|Verb) is "–" = 0
                => every path is 0. Verb is impossible here.

    For Adj:    from Noun  0.2667 × 0.3 × 0.4 = 0.0320    <- max
                from Verb  0.0667 × 0.1 × 0.4 = 0.0027
                from Adj   0                  = 0
                => 0.0320, backpointer Noun

Highest final value: Noun (0.0640), ahead of Adj (0.0320).
Backtracking gives Noun at t=1 too.

ANSWER:   run/Noun    fast/Noun
```

---

## Q2 `[5 Marks]` — Viterbi

> | Transitions | S1 | S2 | | Emissions | S1 | S2 |
> |---|---|---|---|---|---|---|
> | **S1** | 0.6 | 0.4 | | **"A"** | 0.5 | 0.5 |
> | **S2** | 0.3 | 0.7 | | **"B"** | 0.4 | 0.6 |
>
> Using **Viterbi**, calculate the most probable hidden state sequence for the
> observation sequence **"A B"**.

### Solution
```
STEP 1  Initialization ("A") — initial probabilities assumed equal (0.5 each)

    P(S1) = 0.5 × 0.5 = 0.25
    P(S2) = 0.5 × 0.5 = 0.25

STEP 2  Recursion ("B") — take the MAX path into each state

    For S1:  max( 0.25 × 0.6 , 0.25 × 0.3 ) × 0.4
           = max( 0.150 , 0.075 ) × 0.4
           = 0.150 × 0.4  =  0.06            backpointer: S1

    For S2:  max( 0.25 × 0.4 , 0.25 × 0.7 ) × 0.6
           = max( 0.100 , 0.175 ) × 0.6
           = 0.175 × 0.6  =  0.105           backpointer: S2

STEP 3  Termination

    P(S2) = 0.105  >  P(S1) = 0.06
    => the most probable final state is S2, and its backpointer is S2

ANSWER:   S2  S2
```

---
---

# Practice questions

Fresh numbers, same shapes. Attempt before revealing.

### P1 — Laplace `[2 marks]`
```
Corpus:  <s> big data </s>
         <s> big model </s>
         <s> open data </s>
```
Calculate the **Laplace smoothed** probability of **"data"** following **"big"**.
Include `<s>` and `</s>` in V.

<details><summary><b>Answer P1</b></summary>

```
Vocabulary: <s>, </s>, big, data, model, open      ->  V = 6

count("big data") = 1          count("big") = 2

           1 + 1       2
    P  =  ------- =  ----- =  0.25
           2 + 6       8

(unsmoothed MLE would be 1/2 = 0.5)
```
</details>

---

### P2 — Forward pass with ReLU `[3 marks]`
Input `x = [1.0, -0.5]`, weights `w = [0.3, 0.4]`, bias `b = 0.1`, **ReLU**.
Scores: `z(A) = 3*h`, `z(B) = 1*h`. Find `P(A)`.
*(Given `e^0.3 = 1.3499`, `e^0.1 = 1.1052`.)*

<details><summary><b>Answer P2</b></summary>

```
z = (0.3 × 1.0) + (0.4 × -0.5) + 0.1
  = 0.30 - 0.20 + 0.10
  = 0.20

h = ReLU(0.2) = 0.2

z(A) = 3 × 0.2 = 0.6
z(B) = 1 × 0.2 = 0.2

e^0.6 = 1.8221     e^0.2 = 1.2214     sum = 3.0435

P(A) = 1.8221 / 3.0435 = 0.5987  ≈ 0.60
```
*(The e-values in the question were a distractor — you need e^0.6 and e^0.2.
In the exam, if a needed value isn't given, compute it or leave the fraction
symbolically and say so.)*
</details>

---

### P3 — Forward pass with a negative z `[2 marks]`
Input `x = [0.2, 0.1]`, weights `w = [0.5, -1.0]`, bias `b = -0.3`, **ReLU**.
Scores `z(A) = 2*h`, `z(B) = 4*h`. Find `P(A)`.

<details><summary><b>Answer P3</b></summary>

```
z = (0.5 × 0.2) + (-1.0 × 0.1) + (-0.3)
  = 0.10 - 0.10 - 0.30
  = -0.30

h = ReLU(-0.3) = max(-0.3, 0) = 0        <-- the neuron is DEAD

z(A) = 2 × 0 = 0        z(B) = 4 × 0 = 0

P(A) = e^0 / (e^0 + e^0) = 1 / 2 = 0.5
```
> **The lesson:** when ReLU kills the neuron, both scores are 0 and softmax
> returns **exactly 0.5** — the model has no opinion. If you get 0.5, check
> whether `z` went negative. That's a real answer here, not a mistake.
</details>

---

### P4 — Viterbi `[3 marks]`
Tags **N** and **V**. Sentence **"time flies"**.
```
Transitions           N     V          Emissions       time   flies
   START           | 0.6   0.4            N          |  0.5    0.3
   N               | 0.3   0.7            V          |  0.1    0.6
   V               | 0.5   0.5
```
Find the most likely tag sequence.

<details><summary><b>Answer P4</b></summary>

```
Initialization ("time"):
    N:  0.6 × 0.5  =  0.30      <- best
    V:  0.4 × 0.1  =  0.04

Recursion ("flies"):
    N:  max( 0.30 × 0.3 , 0.04 × 0.5 ) × 0.3
      = max( 0.090 , 0.020 ) × 0.3
      = 0.090 × 0.3  =  0.027                 bp: N

    V:  max( 0.30 × 0.7 , 0.04 × 0.5 ) × 0.6
      = max( 0.210 , 0.020 ) × 0.6
      = 0.210 × 0.6  =  0.126                 bp: N
                                 ^^^^^ largest

Backtrace:  V  <-  N

ANSWER:   time/N    flies/V
```
</details>

---

### P5 — Forward `[3 marks]`
Same numbers as P4. Compute `P("time flies")` using the **Forward** algorithm,
and note how the working differs from P4.

<details><summary><b>Answer P5</b></summary>

```
alpha1 ("time"):
    N:  0.6 × 0.5  =  0.30
    V:  0.4 × 0.1  =  0.04

alpha2 ("flies")  —  SUM this time, not MAX:

    N:  [ 0.30 × 0.3  +  0.04 × 0.5 ] × 0.3
      = [ 0.090 + 0.020 ] × 0.3  =  0.110 × 0.3  =  0.033

    V:  [ 0.30 × 0.7  +  0.04 × 0.5 ] × 0.6
      = [ 0.210 + 0.020 ] × 0.6  =  0.230 × 0.6  =  0.138

P("time flies") = 0.033 + 0.138 = 0.171
```
> **The difference from P4:** identical setup, identical multiplications — the
> only change is `max` → `sum`, and there are **no backpointers** because you are
> not choosing a path. Viterbi gave 0.126 (the best *single* path); Forward gives
> 0.171 (the total over *all* paths). Forward is always ≥ Viterbi.
</details>

---

# Self-check

| Skill | Can do unaided |
|---|---|
| Identify V correctly (including `<s>`, `</s>`) | ☐ |
| Laplace formula with `+ V` on the bottom | ☐ |
| Weighted sum `z` with negative numbers | ☐ |
| ReLU vs Sigmoid, including ReLU(negative) = 0 | ☐ |
| Two-way softmax | ☐ |
| Viterbi initialization column | ☐ |
| Viterbi recursion with backpointers | ☐ |
| Viterbi backtrace | ☐ |
| Forward = the same but SUM | ☐ |
| Posterior = each alpha ÷ the total | ☐ |
| One-step prediction (posterior × transitions, no emission) | ☐ |

**All ticked → your 10 pre-midsem marks are secure.** Go back to the
post-midsem pack, which is worth 30.
