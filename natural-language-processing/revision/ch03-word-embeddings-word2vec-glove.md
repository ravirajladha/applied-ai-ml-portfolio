# Ch 3 — Word Embeddings: word2vec (Skip-gram, CBOW) and GloVe
**Session 3** (decks: *NLP Session 2 and 3 — Vector Semantics and Embedding*,
*NLP Session 3 — Word Embedding*)
**Textbook: Jurafsky & Martin, Chapter 6**

This is the **dense** half of the sparse-vs-dense table in
[`ch02`](ch02-vector-semantics-tfidf.md#5--sparse-vs-dense-vectors--the-thing-to-actually-understand).
Chapter 2 built vectors by **counting**. This chapter builds them by
**predicting**.

---

## 0. The one-paragraph version

Instead of counting how often each word `w` occurs near *apricot*, train a
classifier on a fake binary task: **"is `w` likely to show up near *apricot*?"**
We do not care about the classifier's answers at all. We train it, then
**throw the classifier away and keep its weights** — those weights *are* the
embeddings.

That trick is called **self-supervision**: the corpus provides its own labels
(a word that genuinely occurs near *apricot* is the gold "yes"), so **no human
labelling is needed**.

---

## 1. Common methods for short dense vectors

| Family | Methods | Note |
|---|---|---|
| Neural-LM-inspired ("static" embeddings) | **word2vec** (skip-gram, CBOW), **GloVe** | One fixed vector per word **type** |
| **Contextual** embeddings | **ELMo**, **BERT** | A distinct embedding per **token**, computed from its context. Session 11. |

> **Static vs contextual — the standard 2-mark question.** Static: *bank* has ONE
> vector, whether it is a river bank or a money bank. Contextual: *bank* gets a
> different vector in each sentence.

Downloadable pre-trained sets named in the slides:
- word2vec (Mikolov et al.) — `code.google.com/archive/p/word2vec/`
- GloVe (Pennington, Socher, Manning) — `nlp.stanford.edu/projects/glove/`

---

## 2. word2vec — the framework

Unsupervised method from Google, 2013 (Mikolov et al.). Fast to train.
**Idea: predict rather than count.**

The general recipe:
1. Take a large corpus — a long list of words.
2. Every word in a fixed vocabulary gets a vector.
3. Go through each position `t` in the text. It has a **centre word `c`** and
   **context ("outside") words `o`**.
4. Use the **similarity of the vectors** for `c` and `o` to compute the
   probability of `o` given `c` (or vice versa).
5. **Keep adjusting the vectors to maximise that probability.**

The course does the specific variant **skip-gram with negative sampling (SGNS)**.

### The two directions — memorise which is which

```
        SKIP-GRAM                          CBOW
                                   (Continuous Bag Of Words)

    centre word  ->  context          context words  ->  centre word

    "apricot"  =>  jam, tablespoon    "I am ___ because I"  =>  "happy"
```

| | **Skip-gram** | **CBOW** |
|---|---|---|
| Predicts | Context, from the centre word | Centre word, from the context |
| Works well with | **Small** training data | Large data |
| Rare words | Represents rare words/phrases **well** | Weaker on rare words |
| Speed | Slower | **Several times faster** to train |
| Accuracy | — | Slightly **better on frequent words** |

CBOW example from the slides (corpus = *"I am happy because I am learning"*):

| Context words | Centre word |
|---|---|
| I am / because I | **happy** |
| am happy / I am | **because** |
| happy because / am learning | **I** |

---

## 3. Skip-gram with negative sampling (SGNS) — the full walk-through

### Step 1: build the training pairs
Assume a **±2 word window**:

```
…lemon, a [tablespoon  of   apricot   jam,   a]  pinch…
              c1        c2  [target]   c3    c4
```

Positive examples: `(apricot, tablespoon)`, `(apricot, of)`, `(apricot, jam)`,
`(apricot, a)`.

### Step 2: add negative examples
**For every positive example, sample `k` negative examples** — random words from
the lexicon, sampled by frequency. `(apricot, aardvark)`, `(apricot, Tolstoy)`,
`(apricot, matrix)` …

> **Number to remember (Mikolov et al. 2013):**
> **k = 2–5** for large datasets, **k = 5–20** for small datasets.

### Step 3: the classifier
Given a candidate `(word, context)` pair, assign a probability:
```
    P(+ | w, c)          "yes, c is a real neighbour of w"
    P(− | w, c) = 1 − P(+ | w, c)
```

### Step 4: similarity → probability

```
Similarity(w, c)  ∝  w · c            (dot product; cosine is just a normalised
                                       dot product, and neither is a probability)

Squash it with the logistic/sigmoid function:

    P(+ | w, c) =  σ(w · c)  =  1 / (1 + e^(−w·c))

    P(− | w, c) =  1 − σ(w·c)  =  σ(−w·c)

For a whole context window c1…cL, ASSUME INDEPENDENCE and multiply:

    P(+ | w, c1:L) = Π_{i=1..L} σ(w · cᵢ)
```

### Step 5: two embedding matrices

> **SGNS learns TWO sets of embeddings:**
> - **W** — the *target* embedding matrix
> - **C** — the *context* embedding matrix
>
> Each holds one embedding for every one of the |V| vocabulary words.
> It is common to just **add them**: word *i* is represented by **wᵢ + cᵢ**.

This is a classic exam question. Do not say "word2vec learns one matrix".

### Step 6: the loss

```
Goal:  MAXIMISE similarity of (w, c_pos) pairs from the positive data
       MINIMISE similarity of (w, c_neg) pairs from the negative data

Loss for one target w with one c_pos and k negatives c_neg1…c_negk:

    L_CE = − [  log σ(c_pos · w)  +  Σ_{i=1..k} log σ(−c_negᵢ · w)  ]
```

### Step 7: learn with stochastic gradient descent
Adjust the word vectors to make positive pairs more likely and negative pairs
less likely, over the whole training set.

**Update equations** (start from randomly initialised `W` and `C`):
```
    c_pos  ←  c_pos  −  η [ σ(c_pos · w) − 1 ] w
    c_neg  ←  c_neg  −  η [ σ(c_neg · w) − 0 ] w
    w      ←  w      −  η [ ( σ(c_pos·w) − 1 ) c_pos
                            + Σᵢ ( σ(c_negᵢ·w) − 0 ) c_negᵢ ]
```
Intuition: shift *apricot*'s embedding **closer to** (higher dot product with)
*jam*, and **further from** *Tolstoy* and *matrix*.

### Step 8: throw the classifier away, keep the embeddings

Full summary in five lines (worth memorising verbatim):
1. Start with |V| random d-dimensional vectors as initial embeddings.
2. Train a classifier based on embedding similarity.
3. Positive examples = pairs of words that co-occur.
4. Negative examples = pairs of words that do not co-occur.
5. Train the classifier to distinguish them by slowly adjusting all the
   embeddings — then **throw away the classifier code and keep the embeddings**.

---

## 4. ⭐ Worked numerical — the "Ned Stark" SGNS step

This is the slides' fully worked one-step example. Learn its **shape** — the
exam will hand you tiny 3-dimensional vectors and ask for one update.

**Setup**
```
Corpus            : "Ned Stark is the most honourable man"
Positive pair     : (ned, stark)                  -> target t = 1
Negative words    : pimples, zebra, idiot         -> target t = 0
Learning rate  η  : 0.05
```

**Initial input (target) embeddings W**

| word | | | |
|---|---|---|---|
| ned | −0.018 | 0.404 | −0.317 |
| stark | 0.204 | −0.007 | −0.733 |
| pimples | −0.706 | 0.745 | 0.002 |
| zebra | −0.492 | −0.709 | 0.133 |
| idiot | −0.628 | −0.073 | 0.502 |

**Initial context embeddings C**

| word | | | |
|---|---|---|---|
| ned | −0.572 | −0.588 | −0.501 |
| stark | 0.116 | 0.723 | −0.689 |
| pimples | −0.94 | 0.601 | 0.146 |
| zebra | −0.622 | 0.811 | 0.64 |
| idiot | −0.077 | −0.375 | −0.056 |

### (a) Forward pass — dot product then sigmoid
Input word is **ned**, `w = [−0.018, 0.404, −0.317]`. Take `w · c` against each
context vector:

| context word | c | w · c | σ(w·c) |
|---|---|---|---|
| stark | [0.116, 0.723, −0.689] | 0.508 | **0.624** |
| pimples | [−0.94, 0.601, 0.146] | 0.213 | 0.553 |
| zebra | [−0.622, 0.811, 0.64] | 0.136 | 0.534 |
| idiot | [−0.077, −0.375, −0.056] | −0.132 | 0.467 |

### (b) Backward pass — prediction error `σ − t`

| σ | t | error = σ − t |
|---|---|---|
| 0.624 | **1** (stark is the positive) | **−0.376** |
| 0.553 | 0 | +0.553 |
| 0.534 | 0 | +0.534 |
| 0.467 | 0 | +0.467 |

> Sign check: the positive pair has a **negative** error (push them together),
> the negatives have **positive** errors (push them apart).

### (c) Gradient w.r.t. the input word embedding
Multiply each context vector by its error and **sum down the columns**:
```
∂L/∂w = Σ_j (σ_j − t_j) · c_j  =  [ −0.93154,  0.318454,  0.65541 ]
```

### (d) Update the input word embedding
```
w_new = w_old − η · ∂L/∂w
      = [−0.018, 0.404, −0.317] − 0.05 × [−0.93154, 0.318454, 0.65541]
      = [−0.018, 0.404, −0.317] − [−0.04658, 0.015923, 0.032771]
      = [ 0.029,  0.388, −0.350 ]
```

### (e) Update the context embeddings
Gradient for each context word = `(σ_j − t_j) × w_old`, then `c − η·grad`:

| word | old c | new c |
|---|---|---|
| stark | [0.116, 0.723, −0.689] | [0.116, **0.731**, **−0.695**] |
| pimples | [−0.94, 0.601, 0.146] | [−0.94, **0.590**, **0.155**] |
| zebra | [−0.622, 0.811, 0.64] | [−0.622, **0.800**, **0.648**] |
| idiot | [−0.077, −0.375, −0.056] | [−0.077, **−0.384**, **−0.049**] |

Reference for the worked arithmetic:
`aegis4048.github.io/optimize_computational_efficiency_of_skip-gram_with_negative_sampling`

---

## 5. Window size changes what "similar" means

| Window | Neighbours you get | *Hogwarts* example |
|---|---|---|
| **Small, C = ±2** | **Syntactically** similar words in the **same taxonomy** | Sunnydale, Evernight, Blandings (other fictional schools) |
| **Large, C = ±5** | **Related** words in the same **semantic field** | Dumbledore, half-blood, Malfoy (the Harry Potter world) |

> Small window → *similarity* (same kind of thing).
> Large window → *relatedness* (same topic). Ties straight back to the
> similar-vs-related distinction in Ch 2.

---

## 6. GloVe — Global Vectors for Word Representation

Stanford (Pennington, Socher, Manning). Unsupervised algorithm for generating
word embeddings.

**The pitch:** word2vec only looks at **local** context windows. GloVe
**aggregates the global word–word co-occurrence matrix** over the whole corpus,
so it captures **both global and local statistics**.

> **Key idea:** learning should be based on **ratios of co-occurrence
> probabilities**, rather than on the probabilities themselves.

| | **Count-based** (e.g. LSA, raw co-occurrence) | **Prediction-based** (word2vec) | **GloVe** |
|---|---|---|---|
| Uses | Global corpus statistics | Local context windows | **Both** |
| Training | Fast | Slower, scales with corpus size | Fast |
| Statistics | Efficiently used | Inefficiently used | Efficiently used |

**One-line exam answer:** *The advantage of GloVe is that, unlike word2vec, it
does not rely only on local statistics (local context information of words) but
incorporates global statistics (word–word co-occurrence) to obtain word vectors.*

---

## 7. Analogies — the parallelogram model

Classic model of analogical reasoning: *"apple is to tree as grape is to ____"*.

```
For a problem  a : a*  ::  b : b*

    b̂*  =  argmax_{x}   cos( x ,  a* − a + b )

i.e. take the vector b, subtract a, add a*, then find the nearest word.
```

The famous results (Turney & Littman 2005; Mikolov et al. 2013b — the method
works with **both sparse and dense** embeddings):

```
    king − man + woman     ≈  queen
    Paris − France + Italy ≈  Rome
```

---

## 8. Embeddings as a lens on culture

### Historical semantics
Train embeddings on **different decades** of historical text (~30 million books,
1850–1990, Google Books) to watch word meanings **shift over time**.
(Hamilton, Leskovec & Jurafsky, ACL 2016.)

### Embeddings reflect cultural bias
Ask the parallelogram model for analogies and you get:

| Analogy | Answer |
|---|---|
| Paris : France :: Tokyo : x | Japan ✅ |
| father : doctor :: mother : x | **nurse** ⚠️ |
| man : computer programmer :: woman : x | **homemaker** ⚠️ |

(Bolukbasi et al., NeurIPS 2016 — *"Man is to computer programmer as woman is to
homemaker? Debiasing word embeddings"*.)

**Why it matters:** algorithms using embeddings in, e.g., hiring searches for
programmers might lead to **bias in hiring**.

### Historical embeddings as a tool for studying bias
(Garg, Schiebinger, Jurafsky & Zou, PNAS 2018.) Compute a gender or ethnic bias
score per adjective — how much closer it sits to "woman" synonyms than "man"
synonyms:
- **Competence** adjectives (smart, wise, brilliant, resourceful, thoughtful,
  logical) were biased toward men, a bias slowly **decreasing 1960–1990**.
- **Dehumanizing** adjectives (barbaric, monstrous, bizarre) were biased toward
  Asians in the 1930s, decreasing over the 20th century.
- These match the results of **actual surveys done in the 1930s** — which is what
  makes the method credible.

---

## 9. Quick recall table (cover the right column)

| Question | Answer |
|---|---|
| The core word2vec trick? | Train a binary classifier, throw it away, keep the weights |
| Name for "the corpus provides its own labels"? | **Self-supervision** |
| Skip-gram predicts…? | **Context** from the centre word |
| CBOW predicts…? | **Centre word** from the context |
| Which is better on rare words? | **Skip-gram** |
| Which trains faster? | **CBOW** |
| How many negatives per positive? | k = 2–5 (large data), 5–20 (small data) |
| How many embedding matrices does SGNS learn? | **Two** — target `W` and context `C`; commonly added as `wᵢ + cᵢ` |
| Function turning `w·c` into a probability? | **Sigmoid** σ |
| Optimiser? | Stochastic gradient descent |
| Window ±2 gives? | Syntactically similar, same taxonomy |
| Window ±5 gives? | Related words, same semantic field |
| GloVe stands for? | **Glo**bal **Ve**ctors for word representation |
| GloVe's one advantage over word2vec? | Uses **global** co-occurrence statistics, not just local context |
| GloVe's key idea? | Learn from **ratios** of co-occurrence probabilities |
| Analogy formula? | `b̂* = argmax cos(x, a* − a + b)` |

---

## 10. You try
*Attempt on paper before scrolling. Answers at the very bottom.*

**Q1 (pairs).** Sentence: `…lemon, a tablespoon of apricot jam, a pinch…`
with target `apricot` and a **±2** window. (i) List every positive
`(target, context)` pair. (ii) With **k = 2**, how many negative examples are
generated in total for this target?

**Q2 (forward pass).** Target embedding `w = [0.2, −0.1, 0.4]`, context
embedding `c = [0.5, 0.3, −0.2]`. Compute `w · c` and `P(+ | w, c) = σ(w·c)`.
Then compute `P(− | w, c)`.

**Q3 (gradient sign).** In Q2, suppose `c` is a **negative** sample (`t = 0`).
Is the prediction error `σ − t` positive or negative? Will the update push `w`
and `c` closer together or further apart? Explain in one sentence.

**Q4 (concept).** In two sentences, state the difference between skip-gram and
CBOW, and say which you would pick for a 50,000-word corpus of a low-resource
language, with a reason.

**Q5 (GloVe).** A colleague says "GloVe and word2vec are the same thing, both
are dense embeddings". Give the one-sentence correction.

**Q6 (analogy).** Using the parallelogram method, write the vector expression
you would evaluate for *"Tokyo is to Japan as Paris is to ____"*.

---

## Next
**Chapter 4 — N-gram Language Models.** Back to counting, but this time counting
*sequences* instead of contexts.
→ [`ch04-ngram-language-models.md`](ch04-ngram-language-models.md)

---
---
---

<!-- ANSWERS BELOW - stop scrolling until you have attempted -->

## Answers

**A1.**
(i) With a ±2 window around `apricot`, the context words are
`tablespoon`, `of`, `jam`, `a` — so four positive pairs:
`(apricot, tablespoon)`, `(apricot, of)`, `(apricot, jam)`, `(apricot, a)`.
(ii) k = 2 negatives **per positive example**, and there are 4 positives, so
**8** negative examples.

**A2.**
```
w · c = (0.2)(0.5) + (−0.1)(0.3) + (0.4)(−0.2)
      = 0.10 − 0.03 − 0.08 = −0.01

P(+|w,c) = σ(−0.01) = 1 / (1 + e^0.01) = 1 / (1 + 1.01005) = 0.4975
P(−|w,c) = 1 − 0.4975 = 0.5025
```
A dot product near zero gives a sigmoid near 0.5 — the model is undecided,
which is exactly right for two near-orthogonal vectors.

**A3.**
`σ − t = 0.4975 − 0 = +0.4975`, i.e. **positive**. The update is
`w ← w − η(σ−t)c`, so a positive error **subtracts** a multiple of `c` from `w`,
lowering the future dot product — the vectors are pushed **further apart**,
which is what you want for a randomly sampled non-neighbour.

**A4.**
Skip-gram predicts the **context words from the centre word**; CBOW predicts the
**centre word from its context words**. For a 50,000-word corpus of a
low-resource language I would pick **skip-gram**, because it works well with a
small amount of training data and represents rare words and phrases well — and
in a small corpus almost every word is rare.

**A5.**
Both produce dense embeddings, but word2vec learns from **local context windows
only**, while GloVe additionally aggregates the **global word–word co-occurrence
matrix** of the whole corpus and learns from **ratios of co-occurrence
probabilities** — so GloVe uses global statistics that word2vec never sees.

**A6.**
`a : a* :: b : b*` with a = Tokyo, a* = Japan, b = Paris. So evaluate
```
    b̂* = argmax_x  cos( x ,  Japan − Tokyo + Paris )
```
and the nearest word should be **France**.
