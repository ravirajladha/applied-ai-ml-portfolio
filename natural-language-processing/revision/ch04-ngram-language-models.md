# Ch 4 — N-gram Language Models: MLE, Smoothing, Backoff, Perplexity
**Session 4** (deck: *NLP Session 4 — Language modelling*)
**Textbook: Jurafsky & Martin, Chapter 3**

This chapter is **heavily numerical**. Expect to be asked to (a) fill a bigram
probability table, (b) apply add-1 smoothing to it, and (c) compute a sentence
probability or a perplexity. The concepts take an hour; the arithmetic speed
takes practice.

---

## 1. What a language model is

> A model that computes either **P(W)** — the probability of a sentence — or
> **P(wₙ | w₁, w₂, …, wₙ₋₁)** — the probability of an upcoming word — is called a
> **language model**.
>
> Put simply: **a language model learns to predict the probability of a sequence
> of words.**

### The three applications on the slides

| Application | What the LM decides |
|---|---|
| **Machine translation** | `P(high winds tonight) > P(large winds tonight)` |
| **Spelling correction** | `P(about fifteen minutes from) > P(about fifteen minuets from)` |
| **Speech recognition** | `P(I saw a van) >> P(eyes awe of an)` |

Note the third one: the two candidates sound almost identical. Only the language
model can tell them apart.

---

## 2. From the chain rule to the Markov assumption

### Formula box — the exact computation

```
CONDITIONAL PROBABILITY
    P(B|A) = P(A,B) / P(A)      =>      P(A,B) = P(A) P(B|A)

CHAIN RULE (general)
    P(x₁, x₂, …, xₙ) = P(x₁) P(x₂|x₁) P(x₃|x₁,x₂) … P(xₙ|x₁…xₙ₋₁)
```

Applied to a sentence:
```
P(its water is so transparent) =
      P(its)
    × P(water | its)
    × P(is    | its water)
    × P(so    | its water is)
    × P(transparent | its water is so)
```

with each factor estimated by counting:
```
    P(the | its water is so transparent)
        = count(its water is so transparent the) / count(its water is so transparent)
```

**Why this cannot work.** You would never see most of those long strings even
once in any corpus, so almost every numerator is 0. Too many parameters, too
little data.

### The Markov assumption (Andrei Markov)

> **Limit the history to a fixed number of words `n`.**
```
    P(wᵢ | w₁ … wᵢ₋₁)  ≈  P(wᵢ | wᵢ₋ₙ₊₁ … wᵢ₋₁)
```

---

## 3. N-gram models

An **n-gram** is a sequence of `n` tokens (words).

```
UNIGRAM  (n = 1)   P(w₁…wₙ) ≈ Π P(wᵢ)
    P(I want to eat healthy food) ≈ P(I)P(want)P(to)P(eat)P(healthy)P(food)

BIGRAM   (n = 2)   P(w₁…wₙ) ≈ Π P(wᵢ | wᵢ₋₁)
    P(I want to eat healthy food)
      ≈ P(I|<s>) P(want|I) P(to|want) P(eat|to) P(healthy|eat) P(food|healthy) P(</s>|food)

TRIGRAM  (n = 3)   P(w₁…wₙ) ≈ Π P(wᵢ | wᵢ₋₂, wᵢ₋₁)
```

> **Do not forget `<s>` and `</s>`.** The start symbol gives the first word a
> context; the end symbol makes the probabilities of all sentences of all lengths
> sum to 1. Dropping `</s>` is the single most common lost mark here.

### Why n-grams are, in general, an insufficient model of language
Language has **long-distance dependencies**. The slide's example:

> *"The **computer(s)** which I had just put into the machine room on the fifth
> floor **is (are)** crashing."*

The agreement is decided by a word **nine positions back**. No practical n-gram
sees that far.

### Maximum Likelihood Estimation (MLE)

```
                    count(wᵢ₋₁, wᵢ)          c(wᵢ₋₁, wᵢ)
    P(wᵢ | wᵢ₋₁) = -------------------  =  ---------------
                   Σ_w count(wᵢ₋₁, w)         c(wᵢ₋₁)
```

**What "maximum likelihood" means** (the slide spells it out): the MLE of a
parameter from a training set T is the value that **maximises the likelihood of
T given the model**. If *bagel* occurs 400 times in a million-word corpus, the
MLE is 400/1,000,000 = 0.0004. That may be a poor estimate for some *other*
corpus — but it is the estimate that makes it most likely that *bagel* occurs
exactly 400 times in a million words.

---

## 4. ⭐ Worked example 1 — bigram MLE on a 3-sentence corpus

```
<s> I am Sam </s>
<s> Sam I am </s>
<s> I do not like green eggs and ham </s>
```

**Step 1 — unigram context counts.**
```
c(<s>) = 3      c(I) = 3      c(am) = 2      c(Sam) = 2      c(do) = 1
```

**Step 2 — apply the MLE formula.**
```
P(I    | <s>) = c(<s> I)  / c(<s>) = 2/3 = 0.67
P(Sam  | <s>) = c(<s> Sam)/ c(<s>) = 1/3 = 0.33
P(am   | I)   = c(I am)   / c(I)   = 2/3 = 0.67
P(do   | I)   = c(I do)   / c(I)   = 1/3 = 0.33
P(Sam  | am)  = c(am Sam) / c(am)  = 1/2 = 0.50
P(</s> | Sam) = c(Sam </s>)/c(Sam) = 1/2 = 0.50
```

**Step 3 — probability of a full sentence.**
```
P(<s> I am Sam </s>) = P(I|<s>) × P(am|I) × P(Sam|am) × P(</s>|Sam)
                     = (2/3)   × (2/3)   × (1/2)     × (1/2)
                     = 4/36 ÷ ... = 0.111 × 1        = 0.111
```
(Arithmetic: 0.667 × 0.667 = 0.444; × 0.5 = 0.222; × 0.5 = **0.111**.)

---

## 5. Worked example 2 — the Berkeley Restaurant Project (the slide's numbers)

Corpus of 9222 sentences. Unigram counts include `c(i) = 2533`, `c(want) = 927`,
`c(to) = 2417`. Vocabulary **V = 1446**.

### Raw bigram probabilities
```
P(i|i)      = 5   / 2533 = 0.002
P(want|i)   = 827 / 2533 = 0.33
P(to|i)     = 0   / 2533 = 0            <- a ZERO
P(eat|i)    = 9   / 2533 = 0.0036
P(i|want)   = 2   / 927  = 0.0022
P(to|want)  = 608 / 927  = 0.66
P(eat|to)   = 686 / 2417 = 0.28
```

### A whole sentence
```
P(<s> I want english food </s>)
    = P(I|<s>) × P(want|I) × P(english|want) × P(food|english) × P(</s>|food)
    = 0.000031
```

### What kind of knowledge is hiding in those numbers?
```
P(to|want)     = .66      <- SYNTAX: "want to" is a common construction
P(eat|to)      = .28      <- SYNTAX: "to" takes a bare infinitive
P(english|want)= .0011    \  WORLD KNOWLEDGE: at this restaurant,
P(chinese|want)= .0065    /  people ask for Chinese more than English food
P(food|to)     = 0        <- SYNTAX: "to food" is ungrammatical
P(want|spend)  = 0        <- SYNTAX
P(i|<s>)       = .25      <- DISCOURSE: sentences often start with "I"
```
> That table is a nice short-answer question: *"What kinds of knowledge does a
> bigram model capture?"* → **syntax, world knowledge, and discourse structure**,
> all as a side effect of counting.

### Practical issue: work in log space
```
    log(p₁ × p₂ × p₃ × p₄)  =  log p₁ + log p₂ + log p₃ + log p₄
```
Two reasons: **avoid underflow** (multiplying thousands of small probabilities
drives the product to 0 in floating point), and **adding is faster than
multiplying**.

---

## 6. Zeros, and why smoothing exists

**The perils of overfitting:** n-grams only work well if the test corpus looks
like the training corpus. In real life it does not. One kind of generalisation we
need is handling **zeros** — things that never occur in training but do occur in
test.

The slide's example:
```
Training set                    Test set
… denied the allegations        … denied the offer
… denied the reports            … denied the loan
… denied the claims
… denied the request

    P("offer" | denied the) = 0
```

**Why that is fatal, not just inconvenient:** a single zero bigram makes the
probability of the **entire test set zero** (you are multiplying), and perplexity
is `1/P`, so perplexity becomes **infinite**. You cannot even evaluate.

---

## 7. Laplace (add-1) smoothing

> **Pretend we saw each word one more time than we did. Just add one to all the
> counts.**

### Formula box

```
MLE                       P(wᵢ|wᵢ₋₁) = c(wᵢ₋₁,wᵢ) / c(wᵢ₋₁)

ADD-1 (Laplace)                          c(wᵢ₋₁,wᵢ) + 1
                     P_Laplace(wᵢ|wᵢ₋₁) = -----------------
                                          c(wᵢ₋₁)  +  V

    V = the number of UNIQUE words (vocabulary size) — NOT the corpus size.

RECONSTITUTED (adjusted) COUNT — what the smoothed count "would have been"

                     c*(wᵢ₋₁,wᵢ) = [ c(wᵢ₋₁,wᵢ) + 1 ] × c(wᵢ₋₁)
                                   -----------------------------
                                        c(wᵢ₋₁) + V
```

> **Exam trap.** The denominator adds **V**, not 1. `V` is the count of *distinct*
> word types. In the Berkeley corpus V = 1446, so the denominator jumps from 2533
> to 3979 — that is why every smoothed probability drops so hard.

### ⭐ Worked example — Laplace on the Berkeley numbers (V = 1446)

```
P(want|i) = (827 + 1) / (2533 + 1446) =  828 / 3979 = 0.21     was 0.33
P(to|i)   = (0   + 1) / (2533 + 1446) =    1 / 3979 = 0.00025  was 0    ← fixed
P(eat|i)  = (9   + 1) / (2533 + 1446) =   10 / 3979 = 0.0025   was 0.0036
P(to|want)= (608 + 1) / (927  + 1446) =  609 / 2373 = 0.26     was 0.66  ← crushed
P(eat|to) = (686 + 1) / (2417 + 1446) =  687 / 3863 = 0.18     was 0.28
```

**Reconstituted count for (i, want):**
```
c*(i,want) = (827 + 1) × 2533 / (2533 + 1446)
           = 828 × 2533 / 3979
           = 2,097,324 / 3979
           = 527          (down from 827!)
```

### Add-1 is a blunt instrument
Look at `P(to|want)`: **0.66 → 0.26**. Add-1 took a well-attested bigram and cut
its probability by 60%, because it had to give probability mass to 1446 words
that never followed *want*.

> **Conclusion the slide draws:**
> **Add-1 is NOT used for n-grams.** Better methods exist (Good-Turing, Kneser-Ney).
> But add-1 **is** used to smooth other NLP models — text classification, and any
> domain where the number of zeros is not so huge.

---

## 8. Backoff and interpolation

> **Sometimes it helps to use less context.** Condition on less context for
> contexts you have not learned much about.

| | Definition |
|---|---|
| **Backoff** | Use the trigram **if you have good evidence**; otherwise fall back to the bigram; otherwise the unigram. |
| **Interpolation** | **Mix** unigram, bigram and trigram — always, in fixed proportion. |

> **Interpolation works better.**

### Formula box

```
SIMPLE LINEAR INTERPOLATION

    P̂(wₙ | wₙ₋₂, wₙ₋₁) = λ₁ P(wₙ | wₙ₋₂ wₙ₋₁)
                        + λ₂ P(wₙ | wₙ₋₁)
                        + λ₃ P(wₙ)

    subject to     Σᵢ λᵢ = 1

LAMBDAS CONDITIONAL ON CONTEXT — a different λ set per context bucket:
    P̂(wₙ|wₙ₋₂wₙ₋₁) = λ₁(wₙ₋₂ⁿ⁻¹) P(wₙ|wₙ₋₂wₙ₋₁) + …
```

### How to set the lambdas
Use a **held-out corpus** — a third split, separate from training and test:
```
    | ---- Training Data ---- | -- Held-Out Data -- | -- Test Data -- |
```
1. **Fix** the n-gram probabilities on the training data.
2. **Search** for the λs that give the largest probability to the held-out set.

### Stupid backoff — smoothing for web-scale n-grams
(Brants et al. 2007.) **No discounting, just use relative frequencies:**
```
                    count(wᵢ₋ₖ₊₁ … wᵢ)
    S(wᵢ | wᵢ₋ₖ₊₁ⁱ⁻¹) = -------------------      if count(wᵢ₋ₖ₊₁ⁱ) > 0
                    count(wᵢ₋ₖ₊₁ … wᵢ₋₁)

    S(wᵢ | …)  =  0.4 × S(wᵢ | shorter context)   otherwise
```
It is not a real probability distribution (hence "stupid") — but at Google
N-gram scale it works as well as anything more principled.

**Pruning** is the other web-scale trick: only store n-grams with count above a
threshold; remove singletons of higher-order n-grams.

---

## 9. Unknown words: open vs closed vocabulary

| | |
|---|---|
| **Closed vocabulary task** | We know all the words in advance; V is fixed. |
| **Open vocabulary task** | We do not. Words we have never seen are **OOV** — Out Of Vocabulary. |

**The `<UNK>` recipe:**
1. Create a **fixed lexicon L** of size V.
2. At the **text normalisation** phase, change any training word **not in L** to
   `<UNK>`.
3. Now **train `<UNK>`'s probabilities like a normal word**.
4. At decoding time, use the `<UNK>` probabilities for any unseen input word.

---

## 10. ⭐ Evaluation: extrinsic vs intrinsic, and perplexity

### The two kinds of evaluation

| | **Extrinsic (in-vivo)** | **Intrinsic** |
|---|---|---|
| How | Put each model in a real task (spell corrector, speech recogniser, MT) and compare accuracies | Compute **perplexity** on a test set |
| Pro | The **best** evaluation for comparing two models | Fast |
| Con | **Time-consuming — days or weeks** | A **bad approximation** unless the test data looks just like the training data; generally only useful in pilot experiments |

### The Shannon game — the intuition for perplexity
> **How well can we predict the next word?**
```
I always order pizza with cheese and ____
    mushrooms 0.1 | pepperoni 0.1 | anchovies 0.01 | … | fried rice 0.0001 | and 1e-100

The 33rd President of the US was ____
I saw a ____
```
**Unigrams are terrible at this game** — they ignore the context entirely and
always predict the same distribution.

> **A better model of a text is one that assigns a higher probability to the word
> that actually occurs.**

### Formula box

```
PERPLEXITY = the inverse probability of the test set, normalised by word count

    PP(W)  =  P(w₁ w₂ … w_N)^(−1/N)

           =  N-th root of  1 / P(w₁ … w_N)

Via the chain rule:
                  ___________________________
    PP(W)  =  ᴺ√  Π_{i=1..N}  1 / P(wᵢ | w₁…wᵢ₋₁)

For bigrams:
                  ___________________________
    PP(W)  =  ᴺ√  Π_{i=1..N}  1 / P(wᵢ | wᵢ₋₁)

In log space (what you actually compute):
    PP(W) = exp( −(1/N) Σ ln P(wᵢ|wᵢ₋₁) )
```

> **MINIMISING PERPLEXITY = MAXIMISING PROBABILITY.**
> The best language model is the one that best predicts an unseen test set, i.e.
> gives the highest P(sentence). **Lower perplexity = better model.**

### Perplexity as a branching factor
The cleanest intuition, straight off the slide:

> A sentence of random digits 0–9. A model assigns P = 1/10 to each digit.
> What is the perplexity?
```
    PP = ( (1/10)^N )^(−1/N)  =  (1/10)^(−1) = 10
```
**Perplexity 10 = "the model is as confused as if it had to choose uniformly
among 10 options at every step."** That is why it is called a *branching factor*.

### The number to remember
Trained on 38 million words of WSJ, tested on 1.5 million:

| N-gram order | Unigram | Bigram | Trigram |
|---|---|---|---|
| **Perplexity** | **962** | **170** | **109** |

More context → lower perplexity → better model.

### Corpora named on the slides
Brown Corpus · Wall Street Journal · AP newswire · Hansards ·
DARPA/NIST text & speech corpora (CallHome, ATIS, Switchboard, Broadcast News,
TDT, Communicator) · TRAINS · Radio News.

---

## 11. Quick recall table (cover the right column)

| Question | Answer |
|---|---|
| A language model computes? | P(W), or P(wₙ \| w₁…wₙ₋₁) |
| Chain rule for a sentence? | P(x₁)P(x₂\|x₁)P(x₃\|x₁x₂)… |
| The Markov assumption? | Limit the history to a fixed number of previous words |
| Bigram MLE formula? | c(wᵢ₋₁, wᵢ) / c(wᵢ₋₁) |
| Why compute in log space? | Avoid underflow; adding is faster than multiplying |
| Why do zeros break everything? | One zero → P(test set) = 0 → perplexity = ∞ |
| Add-1 formula? | (c(wᵢ₋₁,wᵢ) + 1) / (c(wᵢ₋₁) + V) |
| What is V? | Number of **unique** words (types) in the vocabulary |
| Is add-1 used for n-grams? | **No** — too blunt. Used for text classification instead |
| Backoff vs interpolation? | Backoff = fall back only when needed; interpolation = always mix. **Interpolation works better** |
| How are λs set? | Maximise the probability of a **held-out** corpus |
| Stupid backoff? | Brants et al. 2007 — no discounting, relative frequencies, ×0.4 per backoff step |
| Handling OOV words? | Fixed lexicon L; map unseen training words to `<UNK>`; train `<UNK>` as a normal word |
| Perplexity formula? | P(w₁…w_N)^(−1/N) |
| Lower perplexity means? | **Better** model |
| Perplexity of a uniform 10-way choice? | **10** |
| WSJ perplexities (uni/bi/tri)? | 962 / 170 / 109 |

---

## 12. You try
*Attempt on paper before scrolling. Answers at the very bottom.*

**Q1 (bigram MLE).** Corpus:
```
<s> the cat sat </s>
<s> the cat ran </s>
<s> a dog sat </s>
```
Compute `P(the|<s>)`, `P(cat|the)`, `P(sat|cat)`, `P(</s>|sat)`, and then
`P(<s> the cat sat </s>)`.

**Q2 (Laplace).** Same corpus. The vocabulary (excluding `<s>`) is
{the, a, cat, dog, sat, ran, </s>}, so V = 7. Recompute `P(cat|the)` and
`P(dog|the)` with add-1 smoothing. Comment on what happened to each.

**Q3 (reconstituted count).** For Q2's `(the, cat)`, compute the reconstituted
count `c*`. Was the original count 2 revised up or down?

**Q4 (perplexity).** A bigram model assigns these probabilities to the 4
transitions of a 4-word test sentence: 0.5, 0.25, 0.5, 0.125. Compute the
perplexity. (N = 4.)

**Q5 (perplexity intuition).** Model A has perplexity 120 on a test set; Model B
has 95. Which is better, and what does the number 95 mean in plain English?

**Q6 (concept).** Explain in two sentences why a single unseen bigram in the test
set makes an unsmoothed model's perplexity infinite.

---

## Next
**Chapter 5 — Neural Networks and Neural Language Models.** Same task (predict
the next word), but the counting is replaced by a network, and the words are
replaced by the embeddings from Ch 3.
→ [`ch05-neural-networks-neural-lm.md`](ch05-neural-networks-neural-lm.md)

---
---
---

<!-- ANSWERS BELOW - stop scrolling until you have attempted -->

## Answers

**A1.**
Counts: `c(<s>) = 3`, `c(the) = 2`, `c(cat) = 2`, `c(sat) = 2`.
```
P(the  | <s>) = 2/3 = 0.667
P(cat  | the) = 2/2 = 1.0
P(sat  | cat) = 1/2 = 0.5
P(</s> | sat) = 2/2 = 1.0

P(<s> the cat sat </s>) = 0.667 × 1.0 × 0.5 × 1.0 = 0.333
```

**A2.**
```
P(cat|the) = (2 + 1) / (2 + 7) = 3/9 = 0.333     was 1.0   — crushed
P(dog|the) = (0 + 1) / (2 + 7) = 1/9 = 0.111     was 0     — rescued
```
Add-1 does exactly what it promises and exactly what is wrong with it: the
impossible bigram *the dog* now has non-zero probability (good — no more infinite
perplexity), but the perfectly attested *the cat* fell from 1.0 to 0.33 (bad).
With V = 7 and a context count of only 2, the smoothing mass swamps the evidence.
That is the "blunt instrument" complaint, in miniature.

**A3.**
```
c*(the,cat) = (2 + 1) × c(the) / (c(the) + V)
            = 3 × 2 / (2 + 7)
            = 6 / 9 = 0.667
```
Revised sharply **down**, from 2 to 0.67 — the count was discounted to free up
probability mass for the six words that never followed *the*.

**A4.**
```
P(W) = 0.5 × 0.25 × 0.5 × 0.125 = 0.0078125     (= 1/128)

PP = P(W)^(−1/4) = 128^(1/4) = (2⁷)^(1/4) = 2^1.75 = 3.364
```
So the model is about as uncertain as a uniform choice among **3.36** options at
each word.

**A5.**
**Model B** is better — lower perplexity is better, because minimising perplexity
is the same as maximising the probability assigned to the test set. A perplexity
of 95 means that, on average at each word, the model is as uncertain as if it
were choosing uniformly among **95 equally likely words** — its effective
branching factor.

**A6.**
Sentence probability is a **product** over every transition, so one factor of
zero drives `P(test set)` to exactly 0. Perplexity is defined as
`P(W)^(−1/N)`, i.e. a root of `1/P(W)` — and `1/0` is undefined/infinite, so a
single unseen bigram makes the model not merely bad but **impossible to
evaluate at all**. That, and not accuracy, is the reason smoothing is
non-optional.
