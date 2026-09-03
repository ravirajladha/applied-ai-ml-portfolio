# NLP Pre-Midsem — Cheat Sheet (endsem Q1 & Q2 only)
**AIMLCLZG525 · 10 of 40 marks**

## Read this box first — it saves you hours

In the End-Semester exam, the pre-midsem half is **only Q1 and Q2 = 10 marks**.
Across **all four** past papers those two questions have been the *same two
topics every single time*:

| Q | Marks | Always asks | Chapter |
|---|---|---|---|
| **Q1** | 5 | **(A)** bigram probability with **Laplace smoothing** · **(B)** a **neural LM forward pass** ending in **softmax** | 4 and 5 |
| **Q2** | 5 | **HMM** — either the **Viterbi** algorithm or the **Forward** algorithm | 6 |

**So for the endsem you need exactly three things:** Laplace smoothing, a
one-neuron forward pass, and the HMM table. That's it.

**Chapters 1, 2, 3, 7 and 8** — intro/ambiguity, vector semantics, TF-IDF,
word2vec, Bi-LSTM, prompting — **have never appeared in Q1 or Q2.** Skip them
unless you have spare time. (They were examined in the mid-semester test; they
could in principle return, but four papers say otherwise.)

---

# Part 1 — Laplace Smoothing  *(Q1 Part A, ~2 marks)*

### What it's for
A **language model** guesses the next word. A **bigram** model looks at just one
previous word: *"how often does **learning** follow **deep**?"*

**The problem:** if a word pair never appeared in the training text, its count is
0, so its probability is 0 — and since sentence probabilities are **multiplied**,
one zero makes the whole sentence impossible. **Laplace smoothing fixes this by
pretending you saw every pair one extra time.**

### Words you must know
| Word | Means |
|---|---|
| **Corpus** | The training sentences you were given |
| **Bigram** | A pair of consecutive words, e.g. *deep learning* |
| **`<s>` / `</s>`** | Fake "start of sentence" and "end of sentence" tokens |
| **V** | **Vocabulary size** = how many **distinct** words there are (count `<s>` and `</s>` if the question says to) |
| **MLE** | Plain counting, no smoothing |
| **Laplace / add-1** | Add 1 to every count so nothing is ever zero |

### The two formulas
```
MLE (no smoothing)          count(w1 w2)
                     P  =  --------------
                             count(w1)

LAPLACE (add-1)             count(w1 w2)  +  1
                     P  =  ---------------------
                             count(w1)  +  V
```
**Add `V` on the bottom, not 1.** That's the whole trick.

### Worked example — the real Feb 2026 question
```
Corpus:  <s> deep learning </s>
         <s> machine learning </s>
         <s> deep thought </s>

Find the Laplace probability of "learning" after "deep".

STEP 1  Vocabulary (question says INCLUDE <s> and </s>):
        { <s> , </s> , deep , learning , machine , thought }   ->  V = 6

STEP 2  Counts:
        count("deep learning") = 1        (appears in sentence 1)
        count("deep")          = 2        (sentences 1 and 3)

STEP 3  Apply the formula:
                    1 + 1        2
        P  =  ------------- =  -----  =  0.25
                  2 + 6          8
```

### How to count, without slipping
- **count(w1)** = how many times that word appears **as a first word of a pair**
  — in practice just how many times it appears (ignoring the very last position).
- **V** = count the *distinct* words once each. Read the question: it will tell
  you whether `<s>` and `</s>` are included.

### Trap ⚠️
The denominator is **`count(w1) + V`**, **not** `count(w1) + 1`. Marking schemes
give a separate mark just for identifying V correctly — write it down explicitly.

---

# Part 2 — Neural LM Forward Pass  *(Q1 Part B, ~3 marks)*

### What it's for
Instead of counting, a small neural network **predicts** the next word. You are
asked to push one input through it by hand and report a probability.

### Words you must know
| Word | Means |
|---|---|
| **Embedding** | The input word as a list of numbers, e.g. `x = [0.4, -0.2]` |
| **Weights `w`, bias `b`** | The numbers the network multiplies and adds |
| **Pre-activation `z`** | The weighted sum, **before** squashing |
| **Activation** | The squashing function — **ReLU** or **Sigmoid** |
| **Score / logit** | The raw output number for each candidate word |
| **Softmax** | Turns scores into probabilities that **add up to 1** |

### The recipe — always these four steps
```
STEP 1   z = (w1 × x1) + (w2 × x2) + b            the weighted sum

STEP 2   h = activation(z)
             ReLU(z)    = max(z, 0)               ("if negative, use 0")
             Sigmoid(z) = 1 / (1 + e^(−z))        (always between 0 and 1)

STEP 3   scores:  z_A = (given multiplier) × h
                  z_B = (given multiplier) × h

STEP 4                       e^(z_A)
         P(A)  =  ------------------------
                    e^(z_A)  +  e^(z_B)
```

### Worked example — the real Feb 2026 question
```
x = [0.4, -0.2]    w = [0.5, -0.5]    b = 0.1    activation = ReLU
scores:  z(learning) = 2 × h        z(thought) = 0.5 × h

STEP 1   z = (0.5 × 0.4) + (-0.5 × -0.2) + 0.1
           = 0.20 + 0.10 + 0.10
           = 0.40                                        <- watch the double negative

STEP 2   h = ReLU(0.4) = max(0.4, 0) = 0.4

STEP 3   z(learning) = 2   × 0.4 = 0.8
         z(thought)  = 0.5 × 0.4 = 0.2

STEP 4   e^0.8 = 2.2255       e^0.2 = 1.2214
         sum   = 3.4469

                    2.2255
         P(learning) = -------- = 0.6457   ≈ 0.65
                    3.4469
```

### Sigmoid variant (the Mar 2026 paper)
```
x = [0.5, 1.0]    w = [0.2, 0.4]    b = -0.5    activation = Sigmoid

z = (0.2 × 0.5) + (0.4 × 1.0) + (-0.5) = 0.1 + 0.4 - 0.5 = 0.0
h = sigmoid(0) = 1 / (1 + e^0) = 1 / 2 = 0.5              <- sigmoid(0) is ALWAYS 0.5

z(bright) = 1.5 × 0.5 = 0.75      z(hot) = 0.5 × 0.5 = 0.25
e^0.75 = 2.1170   e^0.25 = 1.2840   sum = 3.4010

P(bright) = 2.1170 / 3.4010 = 0.6225
```

### Numbers worth memorising
```
e^0    = 1.0000      e^0.5  = 1.6487      sigmoid(0)  = 0.5
e^0.2  = 1.2214      e^0.75 = 2.1170      ReLU(neg)   = 0
e^0.25 = 1.2840      e^0.8  = 2.2255
```

### Trap ⚠️
Two sign slips cost most of the marks here:
1. `(-0.5) × (-0.2) = +0.10` — **negative times negative is positive**.
2. **ReLU of a negative number is 0**, and then every score becomes 0 and the
   softmax gives 0.5 / 0.5. If you get exactly 0.5, check whether that's real.

---

# Part 3 — HMM: Viterbi and Forward  *(Q2, 5 marks)*

### What it's for
You can see the **words**. You cannot see their **tags** (Noun/Verb/…) — the tags
are *hidden*. An **HMM** works out the hidden tags from the visible words.

> **The weather analogy:** you can't see the weather, but you can see how many
> ice creams someone ate each day. From the ice creams, work out the weather.

### Words you must know
| Word | Means |
|---|---|
| **Hidden state** | The thing you can't see — the **tag** (DT, NN, VB) |
| **Observation** | The thing you can see — the **word** |
| **Transition probability** | `P(tag → next tag)`. Tag to tag |
| **Emission probability** | `P(word \| tag)`. Tag **produces** word. **NOT** `P(tag\|word)` |
| **Initial / START** | Probability of each tag starting a sentence |
| **Viterbi** | Finds the **single best tag sequence**. Uses **MAX** |
| **Forward** | Finds the **total probability of the words**. Uses **SUM** |
| **Backpointer** | A note of which tag you came from, so you can trace back |

### ⭐ The one thing that decides which algorithm to use
```
   Question says "MOST LIKELY SEQUENCE / best tags"   ->  VITERBI   ->  use MAX
   Question says "PROBABILITY OF THE OBSERVATIONS"    ->  FORWARD   ->  use SUM
   Question says "posterior / distribution over states" -> FORWARD  ->  use SUM
```
**The two algorithms are otherwise identical.** Same table, same multiplications.
Only `max` vs `sum` changes. Learn one and you have both.

### The recipe
```
Build a table:  rows = tags,  columns = words.

COLUMN 1 (first word):
    cell = P(tag | START)  ×  P(word1 | tag)

EVERY LATER COLUMN:
    VITERBI:  cell = MAX over previous tags [ prev cell × P(tag | prev tag) ]  × P(word | tag)
    FORWARD:  cell = SUM over previous tags [ prev cell × P(tag | prev tag) ]  × P(word | tag)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                     do this FIRST, then multiply the emission ONCE at the end

VITERBI FINISH:  take the biggest cell in the last column,
                 follow the backpointers left to read off the tags.

FORWARD FINISH:  ADD UP the last column  =  P(the observations).
```

### Worked example — Viterbi, the real Feb 2026 question
Sentence **"a dog barks"**, tags DT / NN / VB.

```
Transitions              DT    NN    VB          Emissions      a    dog   barks
  START               |  0.4   0.4   0.2           DT        | 0.85  0.10  0.05
  DT                  |  0.2   0.7   0.1           NN        | 0.10  0.80  0.10
  NN                  |  0.1   0.3   0.6           VB        | 0.05  0.10  0.85
  VB                  |  0.5   0.4   0.1
```

**Column 1 — "a"** = `P(tag|START) × P(a|tag)`
```
DT:  0.4 × 0.85 = 0.34          <- clear winner
NN:  0.4 × 0.10 = 0.04
VB:  0.2 × 0.05 = 0.01
```

**Column 2 — "dog"** = `max(prev × transition) × P(dog|tag)`
```
NN:  from DT 0.34×0.7 = 0.238   <- max
     from NN 0.04×0.3 = 0.012
     from VB 0.01×0.4 = 0.004
     0.238 × 0.80 (emission) = 0.1904        backpointer: DT

DT:  max(0.34×0.2, 0.04×0.1, 0.01×0.5) = 0.068 × 0.10 = 0.0068     bp: DT
VB:  max(0.34×0.1, 0.04×0.6, 0.01×0.1) = 0.034 × 0.10 = 0.0034     bp: DT
```

**Column 3 — "barks"**
```
VB:  from NN 0.1904×0.6 = 0.11424   <- max
     0.11424 × 0.85 = 0.097104               backpointer: NN

NN:  max(...) = 0.05712      DT: max(...) = 0.000952
```

**Backtrace** — start at the biggest final cell and walk left:
```
   VB (0.0971)  <- came from NN  <- came from DT

   ANSWER:   a/DT   dog/NN   barks/VB
```

### Worked example — Forward, same idea but SUM
`O = ("ah","sh")`, states V / C / S, π = (0.5, 0.3, 0.2)
```
alpha1 = P(state) × P(ah|state)
   V: 0.5 × 0.8 = 0.40      C: 0.3 × 0.1 = 0.03      S: 0.2 × 0.1 = 0.02

alpha2(C) = [ 0.40×0.3  +  0.03×0.4  +  0.02×0.3 ] × P(sh|C)
          = [ 0.12 + 0.012 + 0.006 ] × 0.7
          = 0.138 × 0.7  =  0.0966
                ^^^^^ ADDED all three, not MAX

alpha2(V) = 0.0258      alpha2(S) = 0.0108

P(observations) = 0.0258 + 0.0966 + 0.0108 = 0.1332

Posterior (if asked) — divide each by the total:
   P(V) = 0.0258/0.1332 = 0.194
   P(C) = 0.0966/0.1332 = 0.725      <- most likely state at time 2
   P(S) = 0.0108/0.1332 = 0.081
```
> **Why C?** *"sh"* has a very high emission probability from C (0.7), and
> enough probability mass transitions into C from earlier states.

### Traps ⚠️
1. **Emission is `P(word | tag)`.** Tag first, word second. Writing it upside
   down turns your model into something else and loses the question.
2. **Multiply the emission once, at the end** — *after* the max/sum, not inside it.
3. If a cell's emission is `0` or `–`, **that cell is 0**. Whole rows can die.
4. **Viterbi = max. Forward = sum.** Read the question wording before you start.
5. Some papers give **no initial probabilities** — then assume **equal**
   (1/2 each for 2 tags, 1/3 each for 3) and **state that assumption**.

---

# The whole 10 marks on one page

| | Formula |
|---|---|
| **Laplace** | `P = (count(w1 w2) + 1) / (count(w1) + V)` — **add V, not 1** |
| **Forward pass** | `z = Σ wᵢxᵢ + b` → `h = ReLU/Sigmoid(z)` → scores → softmax |
| **Softmax** | `e^(z_A) / (e^(z_A) + e^(z_B))` |
| **Viterbi cell** | `MAX(prev × transition) × emission`, keep a backpointer |
| **Forward cell** | `SUM(prev × transition) × emission` |
| **Column 1** | `P(tag \| START) × P(word1 \| tag)` |

### The 5 things that cost marks
1. Laplace denominator: **`+ V`**, not `+ 1`.
2. **ReLU(negative) = 0**; **sigmoid(0) = 0.5**; negative × negative = positive.
3. Emission is **`P(word | tag)`**, never `P(tag | word)`.
4. Emission multiplies in **once, after** the max/sum.
5. **Viterbi = MAX** (best sequence). **Forward = SUM** (total probability).

### Timing
Q1 and Q2 are **10 marks / 40** — about **35 minutes** of a 2.5-hour paper.
Do them **after** the easy post-midsem questions (Q4 attention, Q7 MMR), not
before.

---

**Next:** `SOLVED-NUMERICALS.pdf` — every real Q1 and Q2 from all four past
papers, worked in full, plus practice questions with answers.
