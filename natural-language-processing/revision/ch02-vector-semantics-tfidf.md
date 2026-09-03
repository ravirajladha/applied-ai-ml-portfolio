# Ch 2 — Vector Semantics: Words as Vectors, Sparse vs Dense, TF-IDF & Cosine
**Session 2** (deck: *NLP Session 2 and 3 — Vector Semantics and Embedding*)
**Textbook: Jurafsky & Martin, Chapter 6**

> Open `explainers/ch02-sparse-vs-dense-vectors.html` first — it has a clickable
> co-occurrence matrix, a cosine-angle demo and a side-by-side sparse/dense
> comparison. Come back here for the numbers.

This is the session that turns *words* into *numbers*. Everything after it —
word2vec, neural LMs, BERT, RAG — is built on the one idea in this chapter. It
is worth over-learning.

---

## 0. The one-paragraph version

A computer cannot do arithmetic on the string `"dog"`. So we replace each word
with a **list of numbers** (a vector). We choose those numbers so that words
used in similar ways end up with similar numbers. Then "are these two words
similar?" becomes "are these two lists of numbers pointing the same way?" —
which is just geometry, and geometry is cheap.

There are two families of such lists:

- **Sparse vectors** — very long (20,000–50,000 numbers), almost all zeros, each
  slot *counts* something you can point at. Built by **counting**.
- **Dense vectors** — short (50–1000 numbers), almost all non-zero, no slot means
  anything you can name. Built by **predicting** (learning).

This chapter is the sparse half. Chapter 3 is the dense half.

---

## 1. Why not just use the word itself?

So far (n-grams, text classification) words were just **strings**, or indices
`w₁…w|V|` in a vocabulary list. The slide's complaint: *that's not very
satisfactory.*

Two dead ends the slides mock:

- **Logic-style meaning.** "The meaning of *dog* is DOG", `∀x DOG(x) → MAMMAL(x)`.
- Barbara Partee's 1967 joke: *Q: What's the meaning of life? A: LIFE.*
  Technically true, completely useless.

The real reason it matters — from the sentiment-analysis slide:

| Representation | Feature looks like | What breaks |
|---|---|---|
| Word identity | *"the previous word was **terrible**"* | The **exact same word** must appear in training AND test. See *awful* at test time → nothing fires. |
| Word vector | *"the previous word was `[35, 22, 17…]`"* | Test-time vector `[34, 21, 14]` is close → the feature still (partly) fires. **Generalises to unseen words.** |

> **This is the whole point of the chapter.** Vectors let you generalise to words
> you never saw in training. Strings cannot.

---

## 2. Lexical semantics — the vocabulary you must define

**Lexical semantics** = the linguistic study of word meaning. Three levels the
slide contrasts:

| Level | Studies |
|---|---|
| **Morphology** | Structure of words (how they are built from morphemes) |
| **Language modelling** | Distribution of words (what follows what) |
| **Lexical semantics** | **Meaning** of words |

### Lemma vs sense

- **Lemma** — the dictionary headword. `mouse`
- **Sense** — one meaning component of that lemma.
  - `mouse` sense 1: *any of numerous small rodents…*
  - `mouse` sense 2: *a hand-operated device that controls a cursor…*
- A lemma with more than one sense is **polysemous**.

### The five relations between senses (exam favourite — one line each)

| Relation | Definition | Example |
|---|---|---|
| **Synonymy** | Same meaning in *some or all* contexts. Substitutable, **truth-preserving**, same propositional meaning. | couch/sofa, vomit/throw up, car/automobile |
| **Similarity** | *Not* synonyms, but share some element of meaning. | cat/dog, car/bicycle, cow/horse |
| **Relatedness** ("word association") | Related in *any* way, often via a semantic frame/field. | coffee/cup (related, **not** similar); coffee/tea (similar) |
| **Antonymy** | Opposite on **exactly one** feature of meaning — otherwise very similar. | dark/light, fast/slow, rise/fall, up/down |
| **Connotation** | Affective / emotional meaning. | happy (+), sad (−), great (+), terrible (−) |

> **Exam trap — similar vs related.** `coffee, tea` = **similar**.
> `coffee, cup` = **related but not similar**. If a question gives you a pair
> where one is a container/tool/place for the other, the answer is *related*.

**Perfect synonymy basically does not exist.** The slides' counter-examples:
- *water / H₂O* — would you write "H₂O" in a surfing guide?
- *big / large* — "my **big** sister" ≠ "my **large** sister".

So in practice "synonym" means *approximate or rough synonymy*.

**Antonyms** more formally either
(a) define a **binary opposition** or sit at opposite ends of a **scale**
(long/short, fast/slow), or
(b) are **reversives** (rise/fall, up/down).

### Semantic field
A set of words covering one domain that bear structured relations to each other:
- hospitals → surgeon, scalpel, nurse, anaesthetic
- restaurants → waiter, menu, plate, food, chef
- houses → door, roof, kitchen, family, bed

### Connotation: the 3 affective dimensions (Osgood et al., 1957)

| Dimension | Meaning | High | Low |
|---|---|---|---|
| **Valence** | pleasantness of the stimulus | love 1.000, happy 1.000 | toxic 0.008, nightmare 0.005 |
| **Arousal** | intensity of emotion provoked | elated 0.960, frenzy 0.965 | mellow 0.069, napping 0.046 |
| **Dominance** | degree of control exerted | powerful 0.991, leadership 0.983 | weak 0.045, empty 0.081 |

(Values from the **NRC VAD Lexicon**, Mohammad 2018.)

### Similarity is *graded*, not binary — SimLex-999 (Hill et al., 2015)
Humans rate pairs 0–10:

| word1 | word2 | similarity |
|---|---|---|
| vanish | disappear | 9.8 |
| behave | obey | 7.3 |
| belief | impression | 5.95 |
| muscle | bone | 3.65 |
| modest | flexible | 0.98 |
| hole | agreement | 0.3 |

This dataset is how you *evaluate* embeddings: correlate your cosine scores with
these human scores.

### Applications named on the slides
Question answering (*"How tall is Mt. Everest?"* → the answer says *height*, so
you need `tall ≈ height`), plagiarism detection, paraphrasing, summarization.

---

## 3. The distributional hypothesis — the idea everything rests on

> **Words that occur in similar contexts tend to have similar meanings.**

- *oculist* and *eye-doctor* both occur near *eye*, *examined*.
- **Zellig Harris (1954):** "If A and B have almost identical environments we say
  that they are synonyms."
- The amount of meaning difference between two words corresponds roughly to the
  amount of difference in their **environments (contexts)**.

**The ongchoi example** (memorise this — it is the cleanest illustration):

You see:
```
Ong choi is delicious sautéed with garlic.
Ong choi is superb over rice.
Ong choi leaves with salty sauces.
```
You have also seen:
```
…spinach sautéed with garlic over rice
Chard stems and leaves are delicious
Collard greens and other salty leafy greens
```
**Conclusion:** ongchoi is a leafy green like spinach / chard / collard greens.
You worked that out from *leaves*, *delicious*, *sautéed* — never from a
definition.

### The two ideas of vector semantics
1. **Define meaning by linguistic distribution** (Harris).
2. **Meaning is a point in multidimensional space.**

Vectors representing words are called **embeddings** — "embedded" into a space.
Similar words are **nearby in semantic space**. Every modern NLP algorithm uses
embeddings as its representation of word meaning.

---

## 4. Where do the numbers come from? Two matrices

### (a) Term–document matrix
Each **document** is a dimension; each cell = how often the word occurs in that
document. This is the four-Shakespeare-plays table from J&M that the slides use:

|  | As You Like It | Twelfth Night | Julius Caesar | Henry V |
|---|---|---|---|---|
| **battle** | 1 | 0 | 7 | 13 |
| **good** | 114 | 80 | 62 | 89 |
| **fool** | 36 | 58 | 1 | 4 |
| **wit** | 20 | 15 | 2 | 3 |

Read it **column-wise** → each *document* is a vector of word counts. The two
comedies (*As You Like It*, *Twelfth Night*) have similar vectors — more *fool*
and *wit*, fewer *battles*. **This is the basis of information retrieval.**

Read it **row-wise** → each *word* is a vector over documents.
`battle` = "the kind of word that occurs in *Julius Caesar* and *Henry V*".
`fool` = "the kind of word that occurs in comedies, especially *Twelfth Night*".

### (b) Term–term matrix (word–word / "term–context" matrix)  ← more common
Each **word in the vocabulary** is a dimension; cell (i, j) = how often word *j*
occurred in a context window around word *i* (typically ±4 words).
Size |V| × |V|.

> **Two words are similar in meaning if their context vectors are similar.**

The slides' worked table:

|  | pie | data | computer |
|---|---|---|---|
| **cherry** | 442 | 8 | 2 |
| **digital** | 5 | 1683 | 1670 |
| **information** | 5 | 3982 | 3325 |

Eyeball it: `digital` and `information` look alike; `cherry` looks nothing like
either. §6 turns that eyeballing into a number.

---

## 5. ⭐ Sparse vs dense vectors — the thing to actually understand

This is the slide the whole session builds toward. Here it is as one table.

| | **Sparse (long) vectors** | **Dense (short) vectors** |
|---|---|---|
| **Built by** | **Counting** — "frequency-based" | **Predicting** — "prediction-based" |
| **Length** | \|V\| = **20,000 – 50,000** | **50 – 1000** |
| **Contents** | Mostly **zeros** | Mostly **non-zero**, real-valued |
| **Dimensions mean** | Something nameable: "how often *pie* appeared nearby", "count in document 3" | Nothing nameable — learned, uninterpretable |
| **Methods** | Count vector, **TF-IDF vector**, co-occurrence vector, PPMI | **word2vec** (skip-gram, CBOW), **GloVe** |
| **Where taught** | This chapter (Session 2) | Chapter 3 (Session 3) |

### Why zeros? Where the sparsity comes from
A term–term matrix is |V| × |V|. With |V| = 50,000 that is 2.5 **billion** cells —
but any single word only ever co-occurs with a few thousand others. So >99% of
every row is `0`. That is what "sparse" means: **mostly zero**, not "small".

### The four reasons dense wins (memorise this list — it is a guaranteed question)

1. **Fewer weights to tune.** A downstream classifier on 300-dim inputs has 300
   weights per class instead of 50,000. Easier to train, less overfitting.
2. **Generalise better** than explicit counts.
3. **They capture synonymy; sparse vectors cannot.**
   This is the argument to write out in full:
   > In a sparse vector, `car` and `automobile` are **two distinct, unrelated
   > dimensions**. A word whose neighbour is *car* and a word whose neighbour is
   > *automobile* get counts in two different slots — so the sparse
   > representation shows **zero** overlap between them and fails to see they are
   > similar. A dense vector has no per-word slot, so the two collapse into
   > nearly the same direction.
4. **In practice, they simply work better.**

> **Exam trap.** "Sparse" ≠ "bad" and "dense" ≠ "always better". Sparse TF-IDF
> vectors are still the standard for **information retrieval**, because a
> dimension you can *name* is a dimension you can *search*. Dense wins as
> **features for machine learning**.

### Where each method sits

```
                    WORD REPRESENTATIONS
                            |
        +-------------------+--------------------+
        |                                        |
  1. FREQUENCY-BASED                       2. PREDICTION-BASED
     (counting)                               (learning)
     SPARSE, LONG                             DENSE, SHORT
        |                                        |
   - Count vector                          - word2vec: Skip-gram
   - TF-IDF vector                         - word2vec: CBOW
   - Co-occurrence vector                  - GloVe
        |                                        |
    dimensions = words in V,              dimensions = nothing nameable;
    or documents in a collection          trained to predict "is w likely
                                          to appear near this word?"
```

### And one level beyond (forward reference)
word2vec and GloVe give **static embeddings** — one fixed vector per word type,
so *bank* (river) and *bank* (money) share one vector. **Contextual embeddings**
(**ELMo, BERT**) compute a **distinct embedding for each token in its context**.
That is Session 11, post-midsem.

### One-hot: the most sparse vector of all
`V = [a, aaron, …, zulu, <UNK>]`. Each word = a vector of length |V| with a
single `1`. `King` (index 4914), `Queen` (7157), `Apple` (456), `Orange` (6257).

Its fatal flaw: **every pair of one-hot vectors is orthogonal**, so the dot
product of *any* two different words is `0`. One-hot says *apple* and *orange*
are exactly as unrelated as *apple* and *king*. It carries **no similarity
information at all**.

Contrast with the featurised representation (Mikolov et al. 2013, via the
Andrew Ng slides):

| | Man (5391) | Woman (9853) | King (4914) | Queen (7157) | Apple (456) | Orange (6257) |
|---|---|---|---|---|---|---|
| Gender | −1 | 1 | −0.95 | 0.97 | 0.00 | 0.01 |
| Royal | 0.01 | 0.02 | 0.93 | 0.95 | −0.01 | 0.00 |
| Age | 0.03 | 0.02 | 0.70 | 0.69 | 0.03 | −0.02 |
| Food | 0.09 | 0.01 | 0.02 | 0.01 | 0.95 | 0.97 |

Now *apple* and *orange* are obviously close, and the model can transfer
"I want a glass of **orange** ___" to "I want a glass of **apple** ___".

> **Caveat the slide makes:** those row labels (Gender, Royal, Age, Food) are for
> *teaching only*. Real learned dimensions have no such names.

---

## 6. Measuring similarity — dot product, length, cosine

### Formula box

```
DOT PRODUCT (a scalar)
    a · b  =  Σᵢ aᵢ bᵢ  =  a₁b₁ + a₂b₂ + … + aₙbₙ

    High when the two vectors have large values in the SAME dimensions.

VECTOR LENGTH (Euclidean norm)
    |a|  =  sqrt( Σᵢ aᵢ² )

COSINE SIMILARITY   (= normalised dot product)
                a · b            Σᵢ aᵢ bᵢ
    cos(a,b) = ---------  =  ---------------------------
               |a| |b|      sqrt(Σaᵢ²) · sqrt(Σbᵢ²)

RANGE
    +1  vectors point in the SAME direction
     0  vectors are ORTHOGONAL (nothing in common)
    -1  vectors point in OPPOSITE directions

    Raw frequency values are non-negative  =>  for a term-term matrix
    the cosine is confined to  0 … 1.
```

### Why not just the dot product?

**The dot product favours long vectors.** A vector is long if it has high values
in many dimensions — and frequent words (*of, the, you*) co-occur with everything,
so their rows have huge counts and huge length. The raw dot product therefore
**overly favours frequent words**: *the* would come out "similar" to everything.

Cosine fixes this by dividing out both lengths — it measures **only the angle**,
i.e. the *pattern* of co-occurrence rather than its *volume*.

### ⭐ Worked example — cosine on the pie/data/computer table

|  | pie | data | computer |
|---|---|---|---|
| cherry | 442 | 8 | 2 |
| digital | 5 | 1683 | 1670 |
| information | 5 | 3982 | 3325 |

**Step 1 — lengths.**
```
|cherry|      = sqrt(442² + 8² + 2²)         = sqrt(195364 + 64 + 4)          = 442.08
|digital|     = sqrt(5² + 1683² + 1670²)     = sqrt(25 + 2832489 + 2788900)   = 2370.95
|information| = sqrt(5² + 3982² + 3325²)     = sqrt(25 + 15856324 + 11055625) = 5187.68
```

**Step 2 — cosine(cherry, information).**
```
dot = 442·5 + 8·3982 + 2·3325
    = 2210  + 31856  + 6650      = 40,716

cos = 40,716 / (442.08 × 5187.68)
    = 40,716 / 2,293,286         = 0.018        (angle ≈ 89°)
```

**Step 3 — cosine(digital, information).**
```
dot = 5·5 + 1683·3982 + 1670·3325
    = 25   + 6,701,706 + 5,552,750   = 12,254,481

cos = 12,254,481 / (2370.95 × 5187.68)
    = 12,254,481 / 12,299,982        = 0.996      (angle ≈ 5°)
```

**Read the answer out loud:**
`cos(digital, information) = 0.996` — nearly identical direction, ~5° apart.
`cos(cherry, information) = 0.018` — essentially orthogonal, ~89° apart.
So *digital* and *information* are similar words; *cherry* is unrelated to
both. **The geometry agrees with the intuition.** That is the win.

> **Exam habit.** Always compute the two lengths first and write them down. Most
> lost marks in this question are one squared term forgotten inside a norm.

---

## 7. TF-IDF — fixing "raw frequency is a bad representation"

### The paradox the slide states

- Frequency **is** useful. If *sugar* appears a lot near *apricot*, that is
  genuinely informative.
- But overly frequent words (*the*, *it*, *they*) appear near **everything**, so
  they tell you nothing about the context.

**How do we balance these two conflicting constraints?** → weight each cell by
**tf-idf** instead of the raw count.

### Formula box

```
TERM FREQUENCY  (squashed, so 100 occurrences isn't 100x more important than 1)

    tf(t,d)  =  log10( count(t,d) + 1 )        <- the "+1" keeps count=0 -> 0

DOCUMENT FREQUENCY
    df(t)  =  the NUMBER OF DOCUMENTS t occurs in
    (NOT collection frequency = total count across all documents)

INVERSE DOCUMENT FREQUENCY
    idf(t)  =  log10( N / df(t) )        N = total documents in the collection

    The FEWER documents a term occurs in, the HIGHER this weight.

TF-IDF
    w(t,d)  =  tf(t,d)  ×  idf(t)
```

### Reading the idf intuition

- *"Romeo"* appears in **1** of the 37 Shakespeare plays → `idf = log10(37/1) = 1.57`.
  Very distinctive → high weight.
- *"good"* appears in **all 37** → `idf = log10(37/37) = log10(1) = 0`
  → **tf-idf = 0 no matter how often it occurs.** It is thrown away entirely.
- *the*, *it* → very low idf, for the same reason.

> **Exam trap #1:** `df` counts **documents**, not occurrences. A word appearing
> 500 times but all inside one document has `df = 1`.
>
> **Exam trap #2:** if a word appears in **every** document, `idf = 0`, so
> `tf-idf = 0`. Say that explicitly — it is usually worth a mark.

### ⭐ Worked example — the slide's `wit` calculation
Collection = 37 Shakespeare plays (N = 37). `wit` occurs 20 times in *As You
Like It*, and appears in 34 of the 37 plays.

```
tf     = log10(20 + 1)  = log10(21)    = 1.322
idf    = log10(37 / 34) = log10(1.088) = 0.037
tf-idf = 1.322 × 0.037                 = 0.049
```

And the contrast case:
```
good:  appears in ALL 37 plays  ->  idf = log10(37/37) = 0  ->  tf-idf = 0
```

Even though *good* has a raw count of 114 — the biggest number in the whole
table — its weighted value is **zero**. That is tf-idf doing its job.

### After tf-idf, what have you got?
Still a **sparse** vector: length |V| = 20k–50k, most elements zero. Just
*better-weighted* sparse. The slides also name **PMI / PPMI** as the other
standard weighting for term–term matrices (same sparse family).

That is exactly why the next slide is "**Sparse versus dense vectors**" — you
have squeezed everything you can out of counting, and the remaining gains need
learning. → **Chapter 3.**

---

## 8. Quick recall table (cover the right column)

| Question | Answer |
|---|---|
| Distributional hypothesis? | Words in similar contexts have similar meanings |
| Who said it (1954)? | Zellig Harris |
| A vector representing a word is called? | An **embedding** |
| Two words that are *related but not similar*? | coffee, cup |
| Length of a sparse vector? | \|V\| ≈ 20,000–50,000 |
| Length of a dense vector? | 50–1000 |
| Sparse built by / dense built by? | **Counting** / **predicting** |
| Why does the raw dot product fail? | Favours long vectors → favours frequent words |
| Cosine range for a term–term matrix? | 0 to 1 (counts are non-negative) |
| `tf` formula? | log₁₀(count + 1) |
| `df` is? | Number of **documents** the term occurs in |
| `idf` formula? | log₁₀(N / df) |
| tf-idf of a word appearing in every document? | **0** |
| The synonymy argument for dense? | car/automobile are unrelated dimensions in a sparse vector |
| Static vs contextual embeddings? | word2vec/GloVe = one vector per type; ELMo/BERT = one per token-in-context |

---

## 9. You try
*Attempt on paper before scrolling. Answers at the very bottom.*

**Q1 (cosine).** Using the same term–term table, compute
`cos(cherry, digital)`. Is *cherry* closer to *digital* or to *information*?

**Q2 (tf-idf).** In the 37-play collection, `battle` occurs **13** times in
*Henry V* and appears in **21** of the 37 plays. Compute tf, idf and tf-idf.
Compare with the `wit` value of 0.049 — which word is more distinctive, and why?

**Q3 (sparse vs dense).** A vocabulary has |V| = 40,000. You build (a) a
tf-idf term–term matrix and (b) 300-dimensional word2vec embeddings.
(i) How many numbers does one word's vector have in each case?
(ii) Roughly what fraction of (a) is zero, and why?
(iii) Give the *synonymy* argument for why (b) may generalise better.

**Q4 (concept).** Explain, in two sentences each, why the **dot product alone**
is a poor similarity metric and how **cosine** repairs it.

**Q5 (relations).** Classify each pair as *synonym*, *similar*, *related (not
similar)*, or *antonym*: (a) sofa/couch (b) doctor/hospital (c) cat/dog
(d) rise/fall (e) coffee/tea (f) big/large.

---

## Next
**Chapter 3 — Word Embeddings**: word2vec, skip-gram with negative sampling,
CBOW, GloVe. That chapter is the *dense* half of the sparse-vs-dense table above.
→ [`ch03-word-embeddings-word2vec-glove.md`](ch03-word-embeddings-word2vec-glove.md)

---
---
---

<!-- ANSWERS BELOW - stop scrolling until you have attempted -->

## Answers

**A1.**
```
dot(cherry, digital) = 442·5 + 8·1683 + 2·1670
                     = 2210 + 13464 + 3340 = 19,014
cos = 19,014 / (442.08 × 2370.95) = 19,014 / 1,048,140 = 0.018   (≈ 89°)
```
Essentially the same as `cos(cherry, information) = 0.018`. *cherry* is
orthogonal to **both** — it is a food word and they are technology words.
Neither is "closer" in any meaningful sense; both sit at ~89°.

**A2.**
```
tf     = log10(13 + 1)  = log10(14)    = 1.146
idf    = log10(37 / 21) = log10(1.762) = 0.246
tf-idf = 1.146 × 0.246                 = 0.282
```
`battle` (0.282) scores far higher than `wit` (0.049). Note that *tf* is actually
**lower** for battle (13 occurrences vs 20) — the whole difference comes from
**idf**: battle appears in only 21 of 37 plays, wit in 34. Rarity across
documents, not raw count, is what makes a word distinctive.

**A3.**
(i) (a) 40,000 numbers. (b) 300 numbers.
(ii) Well over 99% of (a) is zero: the matrix has 40,000 × 40,000 = 1.6 billion
cells, but any given word only ever co-occurs with a few thousand distinct
words, so the rest of every row stays 0.
(iii) In (a), `car` and `automobile` occupy **two separate, unrelated
dimensions**. A word neighbouring *car* and a word neighbouring *automobile* get
counts in different slots, so the sparse representation sees **no** overlap and
misses the similarity. In (b) there are no per-word slots — both training
signals push the same 300 numbers in the same direction, so the two words end up
with nearly the same vector.

**A4.**
*Dot product fails:* it grows with vector **length**, and length grows with raw
frequency. Frequent words like *the* co-occur with everything, so they have huge
vectors and score a high dot product against every word — the metric rewards
being common rather than being similar.
*Cosine repairs it:* dividing by `|a||b|` cancels both lengths, leaving only the
**angle** between the vectors. That measures the *pattern* of co-occurrence
rather than its *volume*, so a rare word and a frequent word with the same
distribution now score as similar.

**A5.**
(a) sofa/couch — **synonym**
(b) doctor/hospital — **related, not similar** (same semantic field/frame)
(c) cat/dog — **similar** (share meaning elements, not substitutable)
(d) rise/fall — **antonym** (a reversive)
(e) coffee/tea — **similar**
(f) big/large — **synonym**, but only approximate: *my big sister* ≠ *my large sister*
