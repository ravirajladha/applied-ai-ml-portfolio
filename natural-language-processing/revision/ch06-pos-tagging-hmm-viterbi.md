# Ch 6 — POS Tagging: Word Classes, HMMs, Viterbi and MEMMs
**Session 6** (deck: *NLP Session 6 — POS Tagging and its applications*)
**Textbook: Jurafsky & Martin, Chapter 8**

**This is the heaviest numerical chapter in the pre-midsem half.** A Viterbi
table is almost always asked. Everything else here is definitions; the Viterbi
walk-through in §7 is the part to drill until it is automatic.

---

## 1. What POS tagging is

> **POS tagging** = the process of assigning a **part-of-speech** or lexical class
> marker to each word in a sentence (and to all sentences in a collection).

```
    Input :  the lead paint is unsafe
    Output:  the/Det  lead/N  paint/N  is/V  unsafe/Adj
```

### Why it is useful — the five applications
1. Helps in **stemming / lemmatization**.
2. **Parsing** — you need to know whether a word is N or V before you can parse;
   parsers can build trees directly on POS tags instead of maintaining a lexicon.
3. **Named Entity Recognition and Information Extraction** — finding names,
   relations, etc.
4. **Machine translation**.
5. **Selecting words of specific parts of speech** (e.g. nouns) when
   pre-processing documents for information retrieval.

### Related sequence-labelling tasks (same machinery, different labels)
- **Information extraction** — *"Michael Dell is the CEO of Dell Computer
  Corporation and lives in Austin Texas"* → people / organizations / places.
  Or used-car ads → make, model, year, mileage, price.
- **Semantic role labelling** — for each clause, the role each noun phrase plays:
  *"John drove Mary from Austin to Dallas in his Toyota Prius"* →
  agent / patient / source / destination / instrument. Also called *case role
  analysis*, *thematic analysis*, *shallow semantic parsing*.
- **Bioinformatics** — labelling genetic sequences, e.g. **extron / intron** in
  `AGCTAACGTTCGATACGGATTACAGCCT`.

---

## 2. Word classes

**8 (ish) traditional parts of speech:** noun, verb, adjective, preposition,
adverb, article, interjection, pronoun, conjunction.
Also called **lexical categories, word classes, morphological classes, lexical
tags**. (The slides note there is a lot of linguistic debate about the number and
universality of these, and then cheerfully ignore it.)

### ⭐ Open vs closed classes

| | **Closed class** | **Open class** |
|---|---|---|
| Membership | A **small fixed** membership | **New ones can be created all the time** |
| Examples | Prepositions (*of, in, by*), auxiliaries (*may, can, will, had, been*), pronouns (*I, you, she, mine, his, them*) | English has **4**: **Nouns, Verbs, Adjectives, Adverbs** |
| Usually | **Function words** — short, common, play a role in grammar | Content words |

> **Exam answer:** English has exactly **four** open classes. Many languages have
> these four, but not all.

### Choosing a tagset
- Coarse: N, V, Adj, Adv.
- **The Penn Treebank tagset — 45 tags.** ← the one this course uses.
  Examples: `PRP$` (possessive pronoun), `WRB` (wh-adverb), `WP$` (possessive
  wh-pronoun), `VBG` (verb, gerund).
- Even finer-grained tagsets exist.

Tags you should recognise on sight:

| Tag | Meaning | Tag | Meaning |
|---|---|---|---|
| `DT` | Determiner | `VB` | Verb, base form |
| `NN` | Noun, singular | `VBD` | Verb, past tense |
| `NNS` | Noun, plural | `VBG` | Verb, gerund / present participle |
| `NNP` | Proper noun | `VBN` | Verb, past participle |
| `JJ` | Adjective | `VBZ` | Verb, 3rd person singular present |
| `RB` | Adverb | `MD` | Modal |
| `IN` | Preposition / subordinating conjunction | `TO` | the word *to* |
| `PRP` | Personal pronoun | `.` | Sentence-final punctuation |

Worked tagging from the slides:
```
The/DT grand/JJ jury/NN commented/VBD on/IN a/DT number/NN of/IN other/JJ topics/NNS ./.
```
> **Two conventions to remember:** prepositions **and** subordinating conjunctions
> are both marked `IN` (*"although/IN I/PRP…"*), **except** the preposition *to*,
> which gets its own tag `TO`.

---

## 3. Why it is not just a dictionary lookup

**Words often have more than one POS.** The slide's example, *back*:

| Sentence | Tag |
|---|---|
| The **back** door | `JJ` (adjective) |
| On my **back** | `NN` (noun) |
| Win the voters **back** | `RB` (adverb) |
| Promised to **back** the bill | `VB` (verb) |

> **The POS tagging problem is to determine the POS tag for a particular
> *instance* of a word.** Context decides, not the word.

### POS tagging as sequence classification
Given an *observation* (a sentence) `w₁…wₙ`, find the **best sequence of tags**.
Probabilistic view: consider all possible tag sequences and choose the one that
is **most probable given the observed words**.

### Why you cannot just classify each word independently
1. It is **not easy to integrate information from the categories of tokens on
   both sides**.
2. It is **difficult to propagate uncertainty between decisions** and
   *collectively* determine the most likely joint assignment for the whole
   sequence.

→ Hence **probabilistic sequence models**, which integrate uncertainty over
multiple interdependent classifications and determine the most likely **global**
assignment. The standard model: the **Hidden Markov Model**.

---

## 4. Markov chains, then HMMs

### Markov chain — "first-order observable Markov model"

```
    A set of STATES              Q = q₁, q₂ … q_N ; state at time t is qₜ
    TRANSITION probabilities     A = {aᵢⱼ}, aᵢⱼ = P(qₜ = j | qₜ₋₁ = i)
                                 A is the transition probability matrix
    INITIAL probability vector   π

    MARKOV PROPERTY: the current state depends ONLY on the previous state.
```

**Worked example — the weather chain.** States: 1 = rainy, 2 = cloudy,
3 = warm. Given `π₃ = 0.2` and `a₃₃ = 0.6`, what is the probability of
**4 consecutive warm days** (state sequence 3-3-3-3)?

```
    P(3,3,3,3) = π₃ · a₃₃ · a₃₃ · a₃₃
               = 0.2 × (0.6)³
               = 0.2 × 0.216
               = 0.0432
```
> Note there are only **three** transitions for four days. Off-by-one here is a
> classic lost mark.

### Hidden Markov Model
A Markov chain where **you cannot see the states, only their outputs**.

> An HMM is a **sequence model**: it assigns a label or class to each unit in a
> sequence, mapping a sequence of **observations** to a sequence of **labels**.
> Given a sequence of units (words, letters, morphemes, sentences), it computes a
> probability distribution over possible label sequences and chooses the best.
> **It is a kind of generative model.**

### Formula box — HMM components for POS tagging

```
    STATES (hidden)      T = t₁ … t_N          the TAGS
    OBSERVATIONS         W = w₁ … w_N          the WORDS
                         each from a vocabulary V = {v₁ … v_V}

    TRANSITION matrix    A = {aᵢⱼ} = P(tⱼ | tᵢ)        tag-to-tag
    EMISSION matrix      B = {bᵢ(k)} = P(wₖ | tᵢ)      tag-to-word
    INITIAL vector       π
```

**The two kinds of probability — know which is which:**

| Name | Formula | Intuition | Counted as |
|---|---|---|---|
| **Transition** (tag transition / state transition) | `P(tᵢ \| tᵢ₋₁)` | Determiners are likely to precede adjectives and nouns — *That/DT flight/NN*, *The/DT yellow/JJ hat/NN* — so `P(NN\|DT)` and `P(JJ\|DT)` are high | `C(tᵢ₋₁, tᵢ) / C(tᵢ₋₁)` |
| **Emission** (word likelihood / observation) | `P(wᵢ \| tᵢ)` | `VBZ` (3sg present verb) is likely to be *is*, so `P(is\|VBZ)` is high | `C(tᵢ, wᵢ) / C(tᵢ)` |

> **Exam trap.** The emission probability is `P(word | tag)`, **not**
> `P(tag | word)`. Writing it upside down costs the whole question, because it
> silently turns your HMM into a discriminative model.

### Deriving the tagging equation

```
We want:      t̂₁ⁿ = argmax_{t₁ⁿ}  P(t₁ⁿ | w₁ⁿ)

Bayes rule:                        P(w₁ⁿ | t₁ⁿ) P(t₁ⁿ)
              t̂₁ⁿ = argmax        ---------------------
                                          P(w₁ⁿ)

P(w₁ⁿ) is the same for every candidate tag sequence, so DROP it:

              t̂₁ⁿ = argmax  P(w₁ⁿ | t₁ⁿ)  ·  P(t₁ⁿ)
                            \___________/   \_______/
                             LIKELIHOOD       PRIOR

Two simplifying assumptions:
   (1) MARKOV assumption      P(t₁ⁿ)      ≈ Π P(tᵢ | tᵢ₋₁)
   (2) INDEPENDENCE assumption P(w₁ⁿ|t₁ⁿ) ≈ Π P(wᵢ | tᵢ)
       (a word depends only on its own tag)

Put them together — THE HMM TAGGING EQUATION:

              t̂₁ⁿ  =  argmax_{t₁ⁿ}   Π_{i=1..n}  P(wᵢ | tᵢ) · P(tᵢ | tᵢ₋₁)
                                                 \_________/  \___________/
                                                  emission     transition
```

### Second-order HMM
Condition on the **two** previous tags. For *"the dog barks"* tagged `DT NN VB`
with two sentinel `*` symbols:
```
P(w,y) = T(DT|*,*) × T(NN|*,DT) × T(VB|DT,NN) × T(STOP|NN,VB)
       × E(the|DT) × E(dog|NN) × E(barks|VB)
```

---

## 5. Building the matrices from a tagged corpus

The slides' three-sentence corpus:
```
S1: the/DT  Employees/NNS  pass/VB  an/DT  exam/NN  ./STOP
S2: the/DT  employees/NNS  wait/VB  for/IN  the/DT  pass/VB  ./STOP
S3: employers/NNS  fire/VB  employees/NNS  ./STOP
```

**Tag transition matrix** — rows = first tag, columns = second tag:

|  | \* | DT | NNS | VB | NN | IN | STOP |
|---|---|---|---|---|---|---|---|
| **\*** |  | 2/3 | 1/3 |  |  |  |  |
| **DT** |  |  | 2/4 | 1/4 | 1/4 |  |  |
| **NNS** |  |  |  | 3/4 |  |  | 1/4 |
| **VB** |  | 1/4 | 1/4 |  |  | 1/4 | 1/4 |
| **NN** |  |  |  |  |  |  | 1 |
| **IN** |  | 1 |  |  |  |  |  |

**Emission matrix** — `P(word | tag)`:

|  | \* | DT | NNS | VB | NN | IN | STOP |
|---|---|---|---|---|---|---|---|
| \* | 1 |  |  |  |  |  |  |
| the |  | 3/4 |  |  |  |  |  |
| employees |  |  | 3/4 |  |  |  |  |
| pass |  |  |  | 2/4 |  |  |  |
| an |  | 1/4 |  |  |  |  |  |
| exam |  |  |  |  | 1 |  |  |
| wait |  |  |  | 1/4 |  |  |  |
| for |  |  |  |  |  | 1 |  |
| employers |  |  | 1/4 |  |  |  |  |
| fire |  |  |  | 1/4 |  |  |  |
| . |  |  |  |  |  |  | 1 |

> **How to read a denominator.** `P(NNS|DT) = 2/4` because `DT` occurs 4 times in
> the corpus and is followed by `NNS` twice. `P(the|DT) = 3/4` because of the 4
> `DT` tags, 3 emit *the*. **Denominator = the count of the conditioning thing.**

---

## 6. Worked example — disambiguating "race"

```
Secretariat/NNP is/VBZ expected/VBN to/TO race/VB tomorrow/NR
People/NNS continue/VB to/TO inquire/VB the/DT reason/NN for/IN the/DT race/NN for/IN outer/JJ space/NN
```
**How do we pick the right tag for *race*?** Multiply the relevant transition and
emission probabilities for each candidate and compare.

```
Given:  P(NN|TO) = .00047     P(VB|TO) = .83
        P(race|NN) = .00057   P(race|VB) = .00012
        P(NR|NN) = .0012      P(NR|VB) = .0027
        (NR = adverbial noun, e.g. "tomorrow";  TO = the word "to")

VB path: P(VB|TO) × P(NR|VB) × P(race|VB)
       = .83 × .0027 × .00012          = 0.00000027    = 2.7e-7

NN path: P(NN|TO) × P(NR|NN) × P(race|NN)
       = .00047 × .0012 × .00057       = 0.00000000032 = 3.2e-10
```
`2.7e-7` beats `3.2e-10` by a factor of ~840, **so we correctly choose the verb
tag** for *race*.

> Notice **which** factor decided it: `P(VB|TO) = .83` vs `P(NN|TO) = .00047`.
> The emission probabilities actually favour `NN` (.00057 > .00012). **The
> transition probability overrules the word's own preference** — that is the
> sequence model earning its keep.

---

## 7. ⭐⭐ The Viterbi algorithm — the exam question

### What it is for
Given the observations and the two matrices, find the **single most likely hidden
state sequence**. Brute force is hopeless: for the ice-cream sequence `1 3 1`
with 2 states there are `2³ = 8` sequences (HHH, HHC, HCH, HCC, CCC, CCH, CHC,
CHH); for a 20-word sentence with 45 tags there are `45²⁰` — about 10³³.
Viterbi finds the best one in **O(N²T)** by dynamic programming.

### Formula box

```
Table V with N states (rows) x T observations (columns).

INITIALISATION (first column, j = 1)
    V[t, 1]  =  P(t | <S>) · P(w₁ | t)              = π_t · b_t(w₁)
    backpointer[t, 1] = 0

RECURSION (columns j = 2 … T)
    V[t, j]  =  max_{t'}  [  V[t', j−1] · P(t | t') ]  ·  P(wⱼ | t)
                          \_______________________/     \_________/
                        best way to arrive in state t     emission

    backpointer[t, j] = argmax_{t'} [ V[t', j−1] · P(t | t') ]

TERMINATION
    best final score = max_t  V[t, T] · P(STOP | t)

BACKTRACE
    Follow the backpointers from the winning final cell back to column 1.
```

> **The single most important habit:** the `max` is taken over **where you came
> from**, and the emission `P(wⱼ | t)` is multiplied in **once**, *after* the max.
> Do not put the emission inside the max.

### ⭐ Fully worked Viterbi — *"the doctor is in"*

**Transition matrix `P(tᵢ | tᵢ₋₁)`** (rows = previous tag):

|  | NOUN | Verb | Det | Prep | ADV | STOP |
|---|---|---|---|---|---|---|
| **⟨S⟩** | .3 | .1 | .3 | .2 | .1 | 0 |
| **Noun** | .2 | .4 | .01 | .3 | .04 | .05 |
| **Verb** | .3 | .05 | .3 | .2 | .1 | .05 |
| **Det** | .9 | .01 | .01 | .01 | .07 | 0 |
| **Prep** | .4 | .05 | .4 | .1 | .05 | 0 |
| **Adv** | .1 | .5 | .1 | .1 | .1 | .1 |

**Emission matrix `P(wᵢ | tᵢ)`:**

|  | a | cat | doctor | in | is | the | very |
|---|---|---|---|---|---|---|---|
| **Noun** | 0 | .5 | .4 | 0 | .1 | 0 | 0 |
| **Verb** | 0 | 0 | .1 | 0 | .9 | 0 | 0 |
| **Det** | .3 | 0 | 0 | 0 | 0 | .7 | 0 |
| **Prep** | 0 | 0 | 0 | 1.0 | 0 | 0 | 0 |
| **Adv** | 0 | 0 | 0 | .1 | 0 | 0 | .9 |

---

**Column 1 — `w₁ = the`.** Initialisation: `π_t × P(the | t)`.
```
V(Noun, the) = P(Noun|<S>) × P(the|Noun) = .3 × 0   = 0
V(Verb, the) = P(Verb|<S>) × P(the|Verb) = .1 × 0   = 0
V(Det , the) = P(Det |<S>) × P(the|Det ) = .3 × .7  = .21     ← only survivor
V(Prep, the) = P(Prep|<S>) × P(the|Prep) = .2 × 0   = 0
V(Adv , the) = P(Adv |<S>) × P(the|Adv ) = .1 × 0   = 0
```

**Column 2 — `w₂ = doctor`.** Only `Det` has non-zero mass to come from.
```
V(Noun, doctor) = max{ 0, 0, .21×.9, 0, 0 } × P(doctor|Noun)
                = .189 × .4    = .0756       ← backpointer: Det
V(Verb, doctor) = max{ 0, 0, .21×.01, 0, 0 } × P(doctor|Verb)
                = .0021 × .1   = .00021      ← backpointer: Det
V(Det , doctor) = (…) × P(doctor|Det ) = (…) × 0 = 0
V(Prep, doctor) = (…) × 0 = 0
V(Adv , doctor) = (…) × 0 = 0
```

**Column 3 — `w₃ = is`.**
```
V(Noun, is): candidates  Noun: .0756 × P(Noun|Noun)=.2  = .01512
                         Verb: .00021 × P(Noun|Verb)=.3 = .000063
             max = .01512   × P(is|Noun) = .1
                                          = .001512     ← backpointer: Noun

V(Verb, is): candidates  Noun: .0756 × P(Verb|Noun)=.4  = .03024
                         Verb: .00021 × P(Verb|Verb)=.05= .0000105
             max = .03024   × P(is|Verb) = .9
                                          = .027216     ← backpointer: Noun

V(Det, is) = (…) × P(is|Det) = 0     V(Prep, is) = 0     V(Adv, is) = 0
```

**Column 4 — `w₄ = in`.**
```
V(Prep, in): candidates  Noun: .001512 × P(Prep|Noun)=.3 = .0004536
                         Verb: .027216 × P(Prep|Verb)=.2 = .0054432
             max = .0054432 × P(in|Prep) = 1.0
                                          = .005443     ← backpointer: Verb

V(Adv , in): candidates  Noun: .001512 × P(Adv|Noun)=.04 = .00006048
                         Verb: .027216 × P(Adv|Verb)=.1  = .0027216
             max = .0027216 × P(in|Adv) = .1
                                          = .000272     ← backpointer: Verb

V(Noun, in) = (…) × P(in|Noun) = 0    V(Verb, in) = 0    V(Det, in) = 0
```

### The completed table

|  | w₁ = the | w₂ = doctor | w₃ = is | w₄ = in |
|---|---|---|---|---|
| **Noun** | 0 | **.0756** | .001512 | 0 |
| **Verb** | 0 | .00021 | **.027216** | 0 |
| **Det** | **.21** | 0 | 0 | 0 |
| **Prep** | 0 | 0 | 0 | **.005443** |
| **Adv** | 0 | 0 | 0 | .000272 |

### Backtrace
```
    Best final cell: Prep at w₄  (.005443)
        ← came from Verb at w₃
            ← came from Noun at w₂
                ← came from Det at w₁

    ANSWER:   the/Det   doctor/Noun   is/Verb   in/Prep
```

> **Note on the STOP column.** This worked example reads the answer straight off
> the last column. If your exam question supplies an explicit `STOP` / `</s>`
> transition, do the termination step properly — multiply each final cell by
> `P(STOP | t)` **before** taking the max, exactly as in the formula box.

### The ice-cream HMM (the other classic setup)
> You are a climatologist in 2799 studying global warming. You cannot find any
> weather records for Baltimore in summer 2007, but you find Jason Eisner's diary
> listing **how many ice creams he ate each day**. Your job: figure out **how hot
> it was** each day.

```
    Observations (visible)  :  1, 2, 3, 2, 2, 2, 3 …     ice creams eaten
    Hidden states           :  H, C, H, H, H, C, C …     Hot / Cold
```
Scoring one specific path for the observation `1 3 1`, path `C H C`:
```
P(C H C, 1 3 1) = P(Cold|Start) × P(1|Cold) × P(Hot|Cold) × P(3|Hot)
                  × P(Cold|Hot) × P(1|Cold)
                = 0.2 × 0.5 × 0.4 × 0.4 × 0.3 × 0.5
                = 0.0024
```
Viterbi is what saves you from doing that for all 8 paths.

---

## 8. Problems with HMM tagging

| Issue | Fix |
|---|---|
| **Unknown words** — no probabilities for them | Use **smoothing** (Ch 4 machinery) |
| **Limited context** — only one previous tag | Use **trigram / 4-gram** HMMs |
| **Sparsity** | Smoothing again |

### Bidirectionality
The problem: HMM taggers as presented run **exclusively left-to-right** — though
Viterbi does let present decisions be influenced *indirectly* by future ones,
since the whole path is optimised.

**Any sequence model can be made bidirectional using multiple passes:**
- **Two-pass:** the first pass uses POS features only from already-disambiguated
  words on the **left**; the second pass can use tags for **all** words,
  including those on the right.
- **Two-direction:** run the tagger twice — once left-to-right, once
  right-to-left — and in Viterbi decoding pick the **higher-scoring** of the two
  sequences.

> **Modern taggers are generally run bidirectionally.** (This is exactly what the
> "Bi-" in Bi-LSTM and the "B" in BERT are for. → Ch 7.)

---

## 9. MEMM — Maximum Entropy Markov Model

### The idea
Turn logistic regression into a **discriminative sequence model** simply by
running it on successive words, **using the class assigned to the prior word as a
feature** in classifying the next word. Applied this way, multinomial logistic
regression is called a **maximum entropy Markov model**.

### ⭐ HMM vs MEMM — the comparison that gets asked

| | **HMM** | **MEMM** |
|---|---|---|
| Type | **Generative** | **Discriminative** |
| Computes | **Likelihood** — `P(word \| tag)`, observation conditioned on tags | **Posterior** — `P(tag \| word)` directly |
| Model | `T̂ = argmax Π P(wᵢ\|tᵢ) P(tᵢ\|tᵢ₋₁)` | `T̂ = argmax Π P(tᵢ \| wᵢ, tᵢ₋₁)` |
| Features | Only the word identity | **Any features you like** ← the whole reason to use it |
| Training | Counting | Gradient descent (same as logistic regression) |

> **The reason to use a discriminative sequence model is that it is much easier to
> incorporate a lot of features.**

### The features
Identify a heterogeneous set — the **previous tag**, the **word**, and any other
feature that may contribute. For `Janet/NNP will/MD back/VB the/DT bill/NN`, when
`wᵢ` = *back*, an MEMM can fire features such as:
```
    wᵢ = back            tᵢ₋₁ = MD           tᵢ₋₂tᵢ₋₁ = NNP MD
    wᵢ₋₁ = will          wᵢ₊₁ = the
    wᵢ contains no digit        wᵢ is lowercase
    suffix(wᵢ) = "ack"          prefix(wᵢ) = "b"
```
None of these are expressible in an HMM.

### Formula box

```
    T̂ = argmax_T  P(T | W)
      = argmax_T  Π_i  P( tᵢ | wᵢ₊ₗ_{i−l},  t_{i−1}^{i−k} )

    With features f and weights θ (θ is used instead of w to avoid clashing
    with w for "word"):

                                exp( Σ_j θ_j f_j(tᵢ, wᵢ₋ₗⁱ⁺ˡ, tᵢ₋ₖⁱ⁻¹) )
    P(tᵢ | …)  =  ------------------------------------------------------
                    Σ_{t' ∈ tagset} exp( Σ_j θ_j f_j(t', …) )
```

### Decoding an MEMM

| Method | How | Verdict |
|---|---|---|
| **Greedy decoding** | Classify each word left to right, making a **hard decision** on each before moving on | Very fast, occasionally accurate enough — but the classifier **cannot use evidence from future decisions**, and the hard decision causes too great a drop in performance. **We do not use it.** |
| **Viterbi** | Same DP as the HMM, finding the sequence optimal for the **whole sentence** | ✅ What is actually used |

```
    Viterbi value at time t for state j:

    HMM :   vₜ(j) = max_{i}  v_{t−1}(i)  ·  aᵢⱼ  ·  bⱼ(oₜ)
    MEMM:   vₜ(j) = max_{i}  v_{t−1}(i)  ·  P( sⱼ | s_i, oₜ )
```
Note the MEMM collapses the two HMM factors into one conditional term.

### Training
Learning in MEMMs uses **the same supervised algorithms as logistic regression**:
given observations, feature functions and hidden states, use **gradient descent**
to train the weights to **maximise the log-likelihood of the training corpus**.

---

## 10. Quick recall table (cover the right column)

| Question | Answer |
|---|---|
| POS tagging is? | Assigning a part-of-speech / lexical class marker to each word |
| How many open classes in English, and which? | **4** — Noun, Verb, Adjective, Adverb |
| Penn Treebank tagset size? | **45** tags |
| Which tag do prepositions get? Exception? | `IN`; except *to*, which gets `TO` |
| Transition probability? | `P(tᵢ \| tᵢ₋₁)` — tag to tag |
| Emission probability? | `P(wᵢ \| tᵢ)` — tag to **word** (not word to tag!) |
| The HMM tagging equation? | `argmax Π P(wᵢ\|tᵢ) · P(tᵢ\|tᵢ₋₁)` |
| Two assumptions used to get there? | Markov (tags) + independence (each word depends only on its own tag) |
| Why can we drop `P(W)` after Bayes? | It is identical for every candidate tag sequence |
| Is an HMM generative or discriminative? | **Generative** |
| Viterbi initialisation? | `V[t,1] = P(t\|⟨S⟩) × P(w₁\|t)` |
| Viterbi recursion? | `V[t,j] = max_{t'} [ V[t',j−1] · P(t\|t') ] × P(wⱼ\|t)` |
| Viterbi complexity? | O(N²T) |
| Three problems with HMM tagging? | Unknown words, limited context, sparsity |
| Two ways to make a tagger bidirectional? | Two passes (left-context then all-context), or run both directions and take the higher-scoring sequence |
| MEMM stands for? | Maximum Entropy Markov Model |
| HMM computes … MEMM computes …? | HMM = **likelihood** `P(w\|t)`; MEMM = **posterior** `P(t\|w)` |
| The reason to prefer an MEMM? | Easy to incorporate **many features** |
| Why not greedy decoding for MEMMs? | Hard decisions cannot use evidence from future words |

---

## 11. You try
*Attempt on paper before scrolling. Answers at the very bottom.*

**Q1 (matrices).** From this tagged corpus, compute `P(NN|DT)`, `P(VB|NN)` and
`P(dog|NN)`:
```
the/DT dog/NN barks/VB
the/DT cat/NN sleeps/VB
a/DT dog/NN runs/VB
```

**Q2 (Markov chain).** A weather chain has `π_cold = 0.3` and `a_cold,cold = 0.7`.
What is the probability of **5 consecutive cold days**?

**Q3 (Viterbi, initialisation + one step).** Using the *"the doctor is in"*
matrices from §7, tag the two-word sentence **"a cat"**. Fill both columns and
give the best tag sequence.

**Q4 (disambiguation).** Given
`P(VB|TO) = .83`, `P(NN|TO) = .00047`, `P(race|VB) = .00012`,
`P(race|NN) = .00057`, `P(NR|VB) = .0027`, `P(NR|NN) = .0012` — recompute both
paths and state, in one sentence, which factor decides the outcome and why.

**Q5 (concept).** State two differences between an HMM tagger and an MEMM
tagger, and give one concrete feature an MEMM can use that an HMM cannot.

**Q6 (Viterbi complexity).** A sentence has 20 words and the tagset has 45 tags.
(i) How many tag sequences are there in total? (ii) How many cell-computations
does Viterbi do instead? (iii) State the complexity class.

---

## Next
**Chapter 7 — Neural / LLM / agentic approaches to POS tagging.** Same task,
modern machinery: Bi-LSTM-CRF, Transformers, BERT fine-tuning, prompting.
→ [`ch07-neural-llm-pos-tagging.md`](ch07-neural-llm-pos-tagging.md)

---
---
---

<!-- ANSWERS BELOW - stop scrolling until you have attempted -->

## Answers

**A1.**
Counts: `DT` occurs 3 times; `NN` occurs 3 times.
```
P(NN|DT)  = C(DT,NN) / C(DT) = 3/3 = 1.0
P(VB|NN)  = C(NN,VB) / C(NN) = 3/3 = 1.0
P(dog|NN) = C(NN,dog)/ C(NN) = 2/3 = 0.667
```
(`dog` is emitted by `NN` twice out of the three `NN` tokens.)

**A2.**
Five days means the initial state plus **four** transitions:
```
P = π_cold × (a_cold,cold)⁴ = 0.3 × (0.7)⁴ = 0.3 × 0.2401 = 0.0720
```

**A3.**
**Column 1, `w₁ = a`.** Only `Det` emits *a* (`P(a|Det) = .3`).
```
V(Noun,a) = .3 × 0  = 0        V(Verb,a) = .1 × 0  = 0
V(Det ,a) = .3 × .3 = .09  ←   V(Prep,a) = .2 × 0  = 0
V(Adv ,a) = .1 × 0  = 0
```
**Column 2, `w₂ = cat`.** Only `Noun` emits *cat* (`P(cat|Noun) = .5`).
```
V(Noun,cat) = max{ .09 × P(Noun|Det)=.9 } × .5
            = .081 × .5 = .0405        ← backpointer: Det
all other rows = 0 (emission of "cat" is 0 for every other tag)
```
**Backtrace:** `a/Det  cat/Noun`, score **0.0405**.

**A4.**
```
VB: .83 × .0027 × .00012      = 2.69e-7
NN: .00047 × .0012 × .00057   = 3.21e-10
```
`VB` wins by a factor of ~840. **The transition probability `P(VB|TO) = .83` vs
`P(NN|TO) = .00047` decides it** — a ~1770× advantage that easily overwhelms the
emission probabilities, which actually favour `NN` (.00057 > .00012); in other
words, the fact that *to* is overwhelmingly followed by a verb matters far more
than the fact that *race* is more often a noun.

**A5.**
Two differences: (1) an HMM is **generative** and models the likelihood
`P(word | tag)`, whereas an MEMM is **discriminative** and models the posterior
`P(tag | word, previous tag)` directly; (2) an HMM can only condition on the word
identity, whereas an MEMM can condition on **arbitrary features** of the input.
A concrete MEMM-only feature: **`suffix(wᵢ) = "-ing"`** (or capitalisation, or
"contains a digit") — an HMM has no slot for it, but for an MEMM it is one more
feature function with its own weight, and it is precisely what lets an MEMM tag
unknown words sensibly.

**A6.**
```
(i)   45²⁰  ≈ 1.16 × 10³³ possible tag sequences
(ii)  Viterbi fills a 45 × 20 table = 900 cells, and each cell takes a max over
      45 predecessors  ->  45 × 45 × 20 = 40,500 multiply-and-compare steps
(iii) O(N²T), with N = number of states (tags) and T = sequence length
```
That is 10³³ down to about 4 × 10⁴ — the dynamic-programming win, in one line.
