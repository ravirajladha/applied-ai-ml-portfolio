# NLP Post-Midsem — Practice Papers (exam format)
**AIMLCLZG525 · End-Semester Test · Open Book · Q3–Q7 = 30 marks**

Three full mock sets of **Q3–Q7**, written in the exact format of your real
papers — same question numbering, same mark splits, same phrasing style. Numbers
are **fresh** so this is real practice, not memory.

> **How to use this today.**
> Do **Set A** closed-book against a clock: **45 minutes for the five questions.**
> Mark it. Then do **Set B**, then **Set C**. Reveal an answer only after you have
> written something. Reading a solved sum feels like learning and isn't.

Every answer here was recomputed independently. Full method write-ups live in
[`SOLVED-NUMERICALS.md`](SOLVED-NUMERICALS.md) — go there when an answer surprises you.

---
---

# SET A

## Question 3. [2 + 2 + 2 = 6 Marks]

Consider the sentence **"Dogs chase cats"** with the following possible
dependency arc scores. Let `R` be the ROOT node, `A` = Dogs, `B` = chase,
`C` = cats.

| Head → Dependent | Score |
|---|---|
| R → A | 3 |
| R → B | 9 |
| R → C | 4 |
| A → B | 5 |
| B → A | 8 |
| C → A | 2 |
| B → C | 7 |
| C → B | 10 |

**(a)** For each node (A, B, C), pick the incoming arc with the highest score.
Identify the cycle that forms. **[2 Marks]**

**(b)** Apply Chu-Liu-Edmonds: show the calculation for the "contracted" node
scores after detecting the cycle. **[2 Marks]**

**(c)** Write down the final Maximum Spanning Tree (MST) arcs and the total
score. **[2 Marks]**

<details><summary><b>Show answer — Q3 Set A</b></summary>

**(a) Best incoming arc per node [2 marks]**
```
For A:  R->A = 3 ,  B->A = 8 ,  C->A = 2      ->  BEST = B->A  (8)
For B:  R->B = 9 ,  A->B = 5 ,  C->B = 10     ->  BEST = C->B  (10)
For C:  R->C = 4 ,  B->C = 7                  ->  BEST = B->C  (7)
```
Greedy selection = `{B→A, C→B, B→C}`.
> **CYCLE DETECTED: B → C → B** (B points to C, C points back to B).

**(b) Contract the cycle {B, C} [2 marks]**

Arcs entering the cycle come from `R` and `A`. Subtract the score of the arc
each would replace inside the cycle:
```
Enter at B:  R->B = 9 ,  would replace C->B (10)   ->  9 - 10 = -1
Enter at C:  R->C = 4 ,  would replace B->C (7)    ->  4 -  7 = -3
Enter at B:  A->B = 5 ,  would replace C->B (10)   ->  5 - 10 = -5

BEST ENTRY = R -> B   (-1 is the largest)
```

**(c) Final MST [2 marks]**
```
1. Select R -> B                                     (9)
2. Entering at B breaks the cycle arc into B, i.e. C -> B (10)  -> DROP
3. Keep the other cycle arc:  B -> C                 (7)
4. A still needs a head — its best was B -> A        (8)
```

| Final arc | Meaning | Score |
|---|---|---|
| ROOT → B | ROOT → **chase** | 9 |
| B → C | chase → **cats** | 7 |
| B → A | chase → **Dogs** | 8 |
| | **TOTAL** | **24** |

*Verified: 24 is the true maximum over all valid spanning arborescences.*
</details>

---

## Question 4. [1.5 + 1.5 + 3 = 6 Marks]

Consider the sentence: **"Birds build nests"**

You are given:
- Attention weights for **'build'**: `α = [0.3, 0.5, 0.2]` (for Birds, build, nests)
- Value vectors: `v_Birds = [2,1]`, `v_build = [1,3]`, `v_nests = [0,2]`

**(a)** Explain what contextual embeddings are and why they are important in
NLP. **[1.5 marks]**

**(b)** How do contextual embeddings differ from static word embeddings like
Word2Vec? **[1.5 marks]**

**(c)** Using the given attention weights and value vectors, calculate the
contextual embedding (output) for the word **'build'**. Then, given a second
attention head produced `head₂ = [0.5, 0.8]`, compute the final multi-head
output using
`W_O = [[0.2,0.5],[0.4,0.1],[0.6,0.3],[0.1,0.2]]`. Show all steps. **[3 marks]**

<details><summary><b>Show answer — Q4 Set A</b></summary>

**(a)** Contextual embeddings are **vector representations of words that change
based on the surrounding context**. Unlike static embeddings, the same word can
have different representations in different sentences.
**Importance:** capture **word sense disambiguation** (*bank* financial vs river);
enable better understanding of **semantic relationships**; **improve performance
on downstream NLP tasks**.

**(b)**

| Static (Word2Vec, GloVe) | Contextual (BERT, ELMo) |
|---|---|
| **One fixed vector per word**, regardless of context | **Dynamic** vectors that change with context |
| **Cannot handle polysemy** | Same word gets different representations per sentence |
| One vector per word **type** | One vector per word **token** |
| Trained by prediction over a window | **Computed using attention** over the whole sequence |

**(c) [3 marks]**
```
Step 1 — contextual embedding = weighted sum of value vectors

  Output = 0.3 x [2,1]  +  0.5 x [1,3]  +  0.2 x [0,2]
         = [0.6, 0.3]   +  [0.5, 1.5]   +  [0, 0.4]
         = [ 0.6+0.5+0 , 0.3+1.5+0.4 ]
         = [ 1.1 , 2.2 ]                    <- head_1

  (check: weights sum to 0.3+0.5+0.2 = 1.0 ✓)

Step 2 — concatenate the two heads

  Concat(head_1, head_2) = [1.1, 2.2, 0.5, 0.8]      (4-vector, matches W_O's 4 rows ✓)

Step 3 — project through W_O

  c1 = 1.1x0.2 + 2.2x0.4 + 0.5x0.6 + 0.8x0.1
     = 0.22 + 0.88 + 0.30 + 0.08 = 1.48

  c2 = 1.1x0.5 + 2.2x0.1 + 0.5x0.3 + 0.8x0.2
     = 0.55 + 0.22 + 0.15 + 0.16 = 1.08

  FINAL MULTI-HEAD OUTPUT = [1.48 , 1.08]
```
</details>

---

## Question 5. [3 + 3 = 6 Marks]

**(a)** Suppose you are using the **Lesk Algorithm** for Word Sense
Disambiguation. Given the following definitions and sentence, calculate the
overlap score and find which sense is more suitable for the ambiguous word
**"crane"**. **[3 marks]**

```
Crane (sense 1): A tall bird with a long neck.
   Definition: tall, bird, long, neck, wetland, wading
Crane (sense 2): A machine for lifting heavy objects.
   Definition: machine, lifting, heavy, construction, site, load
```
Sentence: **"The crane at the construction site lifted a heavy load."**

**(b)** The contextual embeddings for the senses of a target word are given
below. The contextual embedding for the target word in a specific sentence was
derived as **`[1, 3, 2]`**. What is the sense of the target word? **[3 marks]**

| Sense | Vector |
|---|---|
| S1 | `[2, 6, 4]` |
| S2 | `[3, 1, 1]` |
| S3 | `[0, 4, 1]` |

<details><summary><b>Show answer — Q5 Set A</b></summary>

**(a) Lesk [3 marks]**
```
Context words (target and stop words removed):

    [ construction , site , lifted , heavy , load ]

SENSE 1 overlap:  none of {tall, bird, long, neck, wetland, wading}   ->  0

SENSE 2 overlap:  construction ✓ , site ✓ , heavy ✓ , load ✓          ->  4
                  (5 if "lifted"/"lifting" are stemmed to the same root)

4 > 0  =>  SENSE 2, the machine for lifting heavy objects.
```
*State your stemming assumption — it is a marked step.*

**(b) Cosine [3 marks]**
```
              a . b
  cos(a,b) = ---------           |target| = sqrt(1+9+4) = sqrt(14) = 3.742
              |a| |b|
```

| Sense | Dot with `[1,3,2]` | \|sense\| | cosine |
|---|---|---|---|
| **S1 `[2,6,4]`** | 2+18+8 = **28** | √56 = 7.483 | 28/(3.742×7.483) = **1.0000** ⭐ |
| S2 `[3,1,1]` | 3+3+2 = 8 | √11 = 3.317 | 8/(3.742×3.317) = 0.6447 |
| S3 `[0,4,1]` | 0+12+2 = 14 | √17 = 4.123 | 14/(3.742×4.123) = 0.9075 |

> **Answer: sense S1**, cosine = 1.0.
> Note `[2,6,4] = 2 × [1,3,2]` — the **same direction**, so cosine is exactly 1.
> Cosine measures direction, never magnitude.
</details>

---

## Question 6. [3 + 3 = 6 Marks]

**(a)** A Retrieval Augmented Generation (RAG) system uses the following
configuration: **[3 marks]**
```
Query tokens              = 180
System prompt tokens      = 320
Maximum LLM context length = 8192 tokens
Size of each retrieved chunk = 600 tokens
```
(i) Calculate the maximum number of document chunks that can be retrieved
without exceeding the context limit.
(ii) If only 60% of that maximum is actually retrieved, calculate the total
number of tokens passed to the LLM.

**(b)** A RAG retriever computes the similarity scores
`0.91, 0.84, 0.78, 0.73, 0.69, 0.61`. The system applies a similarity threshold
of **0.75**. **[3 marks]**
(i) How many chunks are passed to the LLM after thresholding?
(ii) Assuming all selected chunks are relevant, compute the precision.
(iii) If one of the selected chunks is in fact irrelevant, recompute the
precision and comment on the impact on generation quality.

<details><summary><b>Show answer — Q6 Set A</b></summary>

**(a)**
```
(i) Total fixed tokens      = 180 + 320 = 500
    Available for retrieval = 8192 - 500 = 7692
    Maximum chunks          = floor(7692 / 600) = floor(12.82) = 12

    check: 12 x 600 = 7200 <= 7692 ✓   13 x 600 = 7800 > 7692 ✗

(ii) 60% of 12 = 7.2  ->  rounded DOWN to 7 chunks
     Tokens from chunks   = 7 x 600 = 4200
     Total passed to LLM  = 500 + 4200 = 4700 tokens
```
> **Both roundings are FLOOR.** Say "floor" explicitly — it is a marked step.

**(b)**
```
(i)  Scores >= 0.75 :  0.91 , 0.84 , 0.78        ->  3 chunks
     (0.73, 0.69, 0.61 fall below the threshold)

(ii) Precision = relevant / retrieved = 3 / 3 = 1.0

(iii) If one selected chunk is actually irrelevant:
      relevant = 2 , retrieved = 3
      New precision = 2 / 3 = 0.67

      The drop in precision INCREASES CONTEXTUAL NOISE. The LLM is now
      grounding partly on irrelevant text, which raises hallucination risk
      and degrades generation quality.
```
</details>

---

## Question 7. [3 + 1 + 2 = 6 Marks]

Consider a document summarization task with the topic (query):

> **q:** *"Impact of electric vehicles on urban air quality."*

One sentence has already been selected in the summary:

> **S** = {*"Electric vehicles reduce tailpipe emissions in city centres."*}

Two candidate sentences are being evaluated next:

- **S1:** *"EV adoption has cut nitrogen dioxide levels across major metropolitan areas."*
- **S2:** *"Electric cars produce no exhaust emissions in urban areas."*

| Sentence | sim(s, q) | sim(s, S) |
|---|---|---|
| S1 | 0.85 | 0.60 |
| S2 | 0.78 | 0.25 |

Given **λ = 0.7**:

1. Compute the MMR score for both sentences. **[3 marks]**
2. Identify which sentence will be selected next. **[1 mark]**
3. Justify your answer logically (relevance vs redundancy). **[2 marks]**

<details><summary><b>Show answer — Q7 Set A</b></summary>

```
MMR(s) = lambda * sim(s,q)  -  (1 - lambda) * sim(s,S)

lambda = 0.7 ,  (1 - lambda) = 0.3

1. MMR(S1) = 0.7 x 0.85  -  0.3 x 0.60
           = 0.595       -  0.18
           = 0.415                                  (1.5 marks)

   MMR(S2) = 0.7 x 0.78  -  0.3 x 0.25
           = 0.546       -  0.075
           = 0.471                                  (1.5 marks)

2. MMR(S2) > MMR(S1)  =>  SENTENCE S2 IS SELECTED.   (1 mark)
```
**3. Justification [2 marks]**
> Although **S1 is more relevant** to the topic (0.85 vs 0.78), it is **far more
> similar to the already-selected sentence** (0.60 vs 0.25), making it
> **redundant** — it would largely repeat information the summary already
> contains. **S2 contributes lower redundancy** and therefore achieves a higher
> MMR score. MMR deliberately trades a little relevance for **novelty**, so the
> summary covers more distinct information overall.
</details>

---
---

# SET B

## Question 3. [2 + 3 + 1 = 6 Marks]

Consider the following PCFG:

| Rule | Prob | Rule | Prob |
|---|---|---|---|
| 1. S → NP VP | [1.0] | 7. Det → the | [1.0] |
| 2. NP → Det N | [0.4] | 8. N → man | [0.5] |
| 3. NP → NP PP | [0.3] | 9. N → girl | [0.2] |
| 4. NP → PropN | [0.3] | 10. N → telescope | [0.3] |
| 5. VP → V NP | [0.6] | 11. V → saw | [1.0] |
| 6. VP → VP PP | [0.4] | 12. P → with | [1.0] |
| | | 13. PP → P NP | [1.0] |

Sentence: **"The man saw the girl with the telescope."**

**(a)** Provide the two distinct bracketed parses for the sentence. **[2 Marks]**
**(b)** Calculate the probability for both parses. Show your multiplication
steps clearly. **[3 Marks]**
**(c)** Which interpretation does the PCFG select as the most likely, and
why? **[1 Mark]**

<details><summary><b>Show answer — Q3 Set B</b></summary>

**(a) The two parses [2 marks]**
```
PARSE 1 — VP ATTACHMENT  (he USED the telescope to see)

  (S (NP (Det the)(N man))
     (VP (VP (V saw) (NP (Det the)(N girl)))
         (PP (P with) (NP (Det the)(N telescope)))))

PARSE 2 — NP ATTACHMENT  (the GIRL had the telescope)

  (S (NP (Det the)(N man))
     (VP (V saw)
         (NP (NP (Det the)(N girl))
             (PP (P with) (NP (Det the)(N telescope))))))
```

**(b) Probabilities [3 marks]**
```
PARSE 1 (VP attachment)
  S -> NP VP            1.0
  NP -> Det N           0.4 x 1.0 x 0.5      (the man)
  VP -> VP PP           0.4                  <-- attachment decision
    VP -> V NP          0.6
      V -> saw          1.0
      NP -> Det N       0.4 x 1.0 x 0.2      (the girl)
    PP -> P NP          1.0
      P -> with         1.0
      NP -> Det N       0.4 x 1.0 x 0.3      (the telescope)

  P = 1.0 x (0.4x0.5) x [0.4 x (0.6 x (0.4x0.2)) x (1.0 x (0.4x0.3))]
    = 1.0 x 0.2 x [0.4 x 0.048 x 0.12]
    = 0.00046080

PARSE 2 (NP attachment)
  S -> NP VP            1.0
  NP -> Det N           0.4 x 1.0 x 0.5      (the man)
  VP -> V NP            0.6
    V -> saw            1.0
    NP -> NP PP         0.3                  <-- attachment decision
      NP -> Det N       0.4 x 1.0 x 0.2      (the girl)
      PP -> P NP        1.0 x 1.0 x (0.4 x 1.0 x 0.3)

  P = 1.0 x 0.2 x [0.6 x (0.3 x 0.08 x 0.12)]
    = 0.00034560
```

**(c) [1 mark]**
> **The VP-attachment parse (Parse 1)** is selected, because
> **0.00046080 > 0.00034560**. The two parses use identical rules except the
> attachment rule: Parse 1 uses `VP → VP PP` at **0.4**, Parse 2 uses
> `NP → NP PP` at **0.3**. Everything else cancels, so the higher-probability
> attachment rule decides it (ratio 0.4/0.3 = **1.333**, and indeed
> 0.0004608/0.0003456 = 1.333).
>
> Interpretation: the grammar prefers *"the man used the telescope to see"*.
</details>

---

## Question 4. [6 Marks]

Given the sentence **"Deep learning"** and the information below, demonstrate
the mathematical application of a **single attention head** to derive Self
Attention. Detail all steps, applying **score normalization, masking and
softmax**.

```
Embeddings                  Weight matrix Wq       Weight matrix Wk       Weight matrix Wv
  Deep     = [1  0]            [1  1]                  [1  0]                 [1  2]
  learning = [0  1]            [0  1]                  [1  1]                 [2  1]
```
Compute all fractions to two decimal places. Given: `e^0.71 = 2.034`, `e^0 = 1`.

<details><summary><b>Show answer — Q4 Set B</b></summary>

```
STEP 1 — Input                                                  (0.5 marks)
    X = [1 0]      (Deep)
        [0 1]      (learning)

STEP 2 — Compute Q, K, V                                        (1 mark)
    Q = X Wq = [1 0][1 1]  =  [1 1]
               [0 1][0 1]     [0 1]

    K = X Wk = [1 0][1 0]  =  [1 0]
               [0 1][1 1]     [1 1]

    V = X Wv = [1 0][1 2]  =  [1 2]
               [0 1][2 1]     [2 1]

STEP 3 — Scores Q K^T                                           (1 mark)
    K^T = [1 1]
          [0 1]

    Q K^T = [1 1][1 1]  =  [1x1+1x0 , 1x1+1x1]  =  [1 2]
            [0 1][0 1]     [0x1+1x0 , 0x1+1x1]     [0 1]

STEP 4 — Normalize by sqrt(d_k), d_k = 2, sqrt(2) = 1.41        (1 mark)
    [1/1.41  2/1.41]     [0.71  1.41]
    [0/1.41  1/1.41]  =  [0.00  0.71]

STEP 5 — Masking (a token must not see the future)              (1 mark)
    [0.71   -1.00E+99]
    [0.00    0.71    ]

STEP 6 — Softmax each row                                       (1 mark)
    Row 1:  e^0.71 = 2.034 ,  e^-inf = 0 ,  sum = 2.034
            -> [2.034/2.034 , 0] = [1.00 , 0.00]

    Row 2:  e^0.00 = 1.000 ,  e^0.71 = 2.034 ,  sum = 3.034
            -> [1.000/3.034 , 2.034/3.034] = [0.33 , 0.67]

STEP 7 — Multiply by V                                          (0.5 marks)
    Row 1 = 1.00 x [1 2] + 0.00 x [2 1] = [1.00 , 2.00]
    Row 2 = 0.33 x [1 2] + 0.67 x [2 1] = [0.33+1.34 , 0.66+0.67]
                                        = [1.67 , 1.33]

    OUTPUT = [1.00  2.00]
             [1.67  1.33]
```
> **Read the result:** row 1 ("Deep") attends only to itself because masking
> blocks the future. Row 2 ("learning") mixes both, weighted **0.33 / 0.67**
> toward itself. That asymmetry is exactly what masking is for.
</details>

---

## Question 5. [2 + 2 + 2 = 6 Marks]

**(a)** Define **homonymy** and **polysemy**, giving one example of each, and
state why homonymy causes problems for NLP applications. Name two such
applications. **[2 marks]**

**(b)** Why does **WordNet** perform poorly in domain-specific texts (e.g.
medical or legal)? Suggest one solution. **[2 marks]**

**(c)** Explain the difference between the **lexical sample task** and the
**all-words task** in Word Sense Disambiguation. **[2 marks]**

<details><summary><b>Show answer — Q5 Set B</b></summary>

**(a) [2 marks]**
> **Homonymy** — lexemes that **share a form** (phonological, orthographic or
> both) but have **unrelated, distinct meanings**.
> Example: *bat* (wooden stick) vs *bat* (flying mammal); *bank* (financial
> institution) vs *bank* (riverside).
>
> **Polysemy** — a **single lexeme with multiple related meanings**.
> Example: *bank* the building vs *bank* the financial institution.
>
> **Why homonymy is a problem:** the same form must be resolved to different
> meanings or pronunciations.
> - **Text-to-speech** — same orthographic form, different phonological form
>   (*bass* the fish vs *bass* the voice).
> - **Information retrieval** — the query *"bat care"* is ambiguous.
> - Also **machine translation** and **speech recognition**.

**(b) [2 marks]**
> WordNet performs poorly in domain-specific texts because it is a
> **general-purpose lexical database** and **lacks specialised technical
> vocabulary**. Many medical or legal terms are missing or insufficiently
> defined.
> **Solution:** combine WordNet with a **domain-specific ontology or lexicon**,
> which improves accuracy by adding expert domain knowledge.

**(c) [2 marks]**
> **Lexical sample task** — a **small pre-selected set of target words**, with an
> inventory of senses for each. Because the word set and sense set are small,
> simple supervised classification approaches work very well.
>
> **All-words task** — the system is given **entire texts** plus a lexicon with a
> sense inventory for each entry, and must disambiguate **every word** in the
> text (or sometimes just every content word).
</details>

---

## Question 6. [2 + 2 + 2 = 6 Marks]

A hospital wants to build a **semantic-web-based patient information system**
integrating data about patients, doctors and departments.

**(a)** Identify the entities (subjects), properties (predicates) and values
(objects) required to model this system using **RDF**. **[2 marks]**

**(b)** Write any three RDF triples to represent: **[2 marks]**
- A patient named **Meera** is treated by **Dr. Iyer**
- **Dr. Iyer** works in the **Cardiology** department
- The **Cardiology** department is located in **Building B**

**(c)** The hospital also wants to enforce the rule *"every patient must have at
least one assigned doctor"*, and to record simple factual data. Which task suits
**RDF** and which suits **OWL**? Explain briefly. **[2 marks]**

<details><summary><b>Show answer — Q6 Set B</b></summary>

**(a) RDF components [2 marks]**
```
Entities (Subjects):          Properties (Predicates):     Values (Objects):
   Patient    (Meera)            treatedBy                    Dr. Iyer
   Doctor     (Dr. Iyer)         worksIn                      Cardiology
   Department (Cardiology)       locatedIn                    Building B
   Building   (Building B)
```

**(b) Three RDF triples [2 marks]**

| Subject | Predicate | Object |
|---|---|---|
| `Meera` | `treatedBy` | `DrIyer` |
| `DrIyer` | `worksIn` | `Cardiology` |
| `Cardiology` | `locatedIn` | `BuildingB` |

As a graph:
```
  Meera ──treatedBy──► DrIyer ──worksIn──► Cardiology ──locatedIn──► BuildingB
```

**(c) RDF vs OWL [2 marks]**
> **Recording simple factual data** is best suited to **RDF**, as RDF represents
> information as simple **subject–predicate–object triples**.
>
> **Enforcing the constraint** *"every patient must have at least one assigned
> doctor"* suits **OWL**, because OWL supports **restrictions and reasoning**
> (here, an `owl:minCardinality` restriction of 1 on the `treatedBy` property).
>
> Thus **RDF handles data representation, while OWL handles logic and
> consistency checking.**
</details>

---

## Question 7. [2 + 2 + 2 = 6 Marks]

**(a)** Define **ROUGE** and state what **ROUGE-2** measures. **[2 marks]**

**(b)** Compute the **ROUGE-2** score for the system summary below. **[2 marks]**
```
Reference 1: "The company reported record profits this quarter"
Reference 2: "Record quarterly profits were announced by the company"

System X   : "The company announced record profits this quarter"
```

**(c)** State the three stages of summarization and name one technique used in
the first stage. **[2 marks]**

<details><summary><b>Show answer — Q7 Set B</b></summary>

**(a) [2 marks]**
> **ROUGE** = **Recall-Oriented Understudy for Gisting Evaluation**. An
> **intrinsic** metric for automatically evaluating summaries, based on **BLEU**
> (a machine-translation metric). Not as good as human evaluation, **but much
> more convenient**.
>
> **ROUGE-2:** given a document D and an automatic summary X, have N humans
> produce reference summaries. It measures **what percentage of the bigrams from
> the reference summaries appear in X**.

**(b) [2 marks]**
```
System bigrams (6):
   the company | company announced | announced record |
   record profits | profits this | this quarter

Reference 1 bigrams (6):
   the company ✓ | company reported | reported record |
   record profits ✓ | profits this ✓ | this quarter ✓        -> 4 matched

Reference 2 bigrams (7):
   record quarterly | quarterly profits | profits were |
   were announced | announced by | by the | the company ✓     -> 1 matched

                     4 + 1          5
   ROUGE-2  =  ---------------  =  ----  =  0.3846  =  38.5%
                     6 + 7          13
```

**(c) [2 marks]**
```
1. CONTENT SELECTION    — choose sentences to extract from the document
2. INFORMATION ORDERING — choose an order to place them in the summary
3. SENTENCE REALIZATION — clean up the sentences
```
> **Technique for stage 1:** frequency as an indicator of importance (the topic
> is repeated many times), implemented as the **greedy frequency method** or via
> **tf-idf** sentence weighting; or graph representations with nodes as
> sentences and arcs between similar sentences; or **MMR** for non-redundancy.
</details>

---
---

# SET C

## Question 3. [6 Marks]

Consider the statement: **"The small dog barked loudly"**

Using **Depth-First, Simple Top-Down parsing**, work out the steps only till the
noun-phrase **"The small dog"** is successfully parsed. Provide one line of
explanation for each step.

```
CFG Rules                       Lexicon
1. S  -> NP VP                    Det -> the
2. NP -> Det AP N                 Adj -> small
3. NP -> Det N                    N   -> dog
4. AP -> Adv Adj                  V   -> barked
5. AP -> Adj                      Adv -> loudly
```
The parser applies rules in the order listed (rule 2 before rule 3, rule 4
before rule 5).

<details><summary><b>Show answer — Q3 Set C</b></summary>

```
    1 The  2 small  3 dog  4 barked  5 loudly 6
```

| Step | State | Backup | Comment |
|---|---|---|---|
| 1 | `((S) 1)` | | Start of the process |
| 2 | `((NP VP) 1)` | | Expand `S → NP VP` (Rule 1) |
| 3 | `((Det AP N VP) 1)` | `((Det N VP) 1)` | NP expanded — Rule 2 taken, **Rule 3 pushed to backup** |
| 4 | `((AP N VP) 2)` | `((Det N VP) 1)` | `The` matches Det → advance to position 2 |
| 5 | `((Adv Adj N VP) 2)` | `((Det N VP) 1)`, `((Adj N VP) 2)` | AP expanded — Rule 4 taken, **Rule 5 pushed to backup** |
| 6 | — **FAIL** — | | Position 2 is `small`, which is **not** an Adv. **Discard this state.** |
| 7 | `((Adj N VP) 2)` | `((Det N VP) 1)` | **Pop from backup** |
| 8 | `((N VP) 3)` | `((Det N VP) 1)` | `small` matches Adj → advance |
| 9 | `((VP) 4)` | | `dog` matches N → advance. **"The small dog" is fully parsed** ✅ |

> The marks are for **showing the failure and the pop**. A table with no
> backtracking hasn't demonstrated depth-first parsing with backup.
</details>

---

## Question 4. [2 + 2 + 2 = 6 Marks]

In a transformer model processing the sentence **"The cat sat"**:

- Attention weights for **'sat'**: `α = [0.2, 0.3, 0.5]` (for The, cat, sat)
- Value vectors: `v_The = [1,2]`, `v_cat = [2,0]`, `v_sat = [0,3]`

**(a)** Explain why transformers use **multiple attention heads** instead of a
single head. **[2 marks]**

**(b)** Calculate the contextual embedding (output) for the word **'sat'**.
Show all steps. **[2 marks]**

**(c)** Given that Head 1 has attention weights `[0.1, 0.2, 0.7]` and Head 2 has
`[0.6, 0.2, 0.2]` for positions (The, cat, sat), what might each head be
specialising in? **[2 marks]**

<details><summary><b>Show answer — Q4 Set C</b></summary>

**(a) [2 marks]** Multiple attention heads allow the model to:
> - Attend to information from **different representation subspaces**
> - Capture **different types of relationships** (syntactic, semantic, positional)
> - **Learn diverse patterns** — one head might focus on adjacent words, another
>   on subject–verb relationships
> - **Increase model capacity** without proportionally increasing computation

**(b) [2 marks]**
```
Output = SUM alpha_i x v_i

       = 0.2 x [1,2]  +  0.3 x [2,0]  +  0.5 x [0,3]
       = [0.2, 0.4]   +  [0.6, 0]     +  [0, 1.5]
       = [ 0.2+0.6+0 , 0.4+0+1.5 ]
       = [ 0.8 , 1.9 ]

(check: 0.2 + 0.3 + 0.5 = 1.0 ✓)
```

**(c) [2 marks]**
```
Head 1 weights [0.1, 0.2, 0.7] -> highest attention on 'sat' (position 3)
   => Head 1 focuses on the VERB / action word (syntactic relationship)

Head 2 weights [0.6, 0.2, 0.2] -> highest attention on 'The' (position 1)
   => Head 2 focuses on the DETERMINER / article (grammatical structure)

This demonstrates how different heads specialise in capturing different
linguistic patterns.
```
</details>

---

## Question 5. [3 + 3 = 6 Marks]

**(a)** The contextual embeddings for the senses of the word **"mouse"** are
given below. The contextual embedding for the target word in a specific sentence
was derived as **`[3, 1, 4]`**. What is the sense of the target word? Show your
calculation. **[3 marks]**

| Sense | Meaning | Vector |
|---|---|---|
| mouse_N1 | small rodent | `[6, 2, 8]` |
| mouse_N2 | computer pointing device | `[1, 5, 2]` |
| mouse_N3 | timid person | `[2, 2, 1]` |

**(b)** Define **hyponymy** and **hypernymy** with one example each, and explain
what a **synset** is in WordNet. **[3 marks]**

<details><summary><b>Show answer — Q5 Set C</b></summary>

**(a) [3 marks]**
```
|target| = sqrt(3^2 + 1^2 + 4^2) = sqrt(9+1+16) = sqrt(26) = 5.099
```

| Sense | Dot with `[3,1,4]` | \|sense\| | cosine |
|---|---|---|---|
| **N1 `[6,2,8]`** | 18+2+32 = **52** | √104 = 10.198 | 52/(5.099×10.198) = **1.0000** ⭐ |
| N2 `[1,5,2]` | 3+5+8 = 16 | √30 = 5.477 | 16/(5.099×5.477) = 0.5729 |
| N3 `[2,2,1]` | 6+2+4 = 12 | √9 = 3.000 | 12/(5.099×3.000) = 0.7845 |

> **Answer: `mouse_N1`, the small rodent** (cosine = 1.0).
>
> **Trap avoided:** N1 also has the largest dot product here, but that is not
> the reason — always divide by the magnitudes. `[6,2,8] = 2 × [3,1,4]`, the
> same direction, hence cosine exactly 1.

**(b) [3 marks]**
> **Hyponymy** — one sense is a **hyponym** of another if the first is **more
> specific**, denoting a **subclass** of the other.
> *car* is a hyponym of *vehicle*; *dog* is a hyponym of *animal*;
> *mango* is a hyponym of *fruit*.
>
> **Hypernymy** — the converse relation, the **superordinate**.
> *vehicle* is a hypernym of *car*; *animal* is a hypernym of *dog*.
>
> **Synset** — the set of **near-synonyms** for a WordNet sense is called a
> **synset** (synonym set). It is WordNet's version of a **sense or concept**;
> all members share the same **gloss**, and for WordNet the meaning of that
> sense *is* this list.
</details>

---

## Question 6. [2 + 2 + 2 = 6 Marks]

**(a)** Name the three ontology languages in the Semantic Web stack and state in
one line what each specifies. **[2 marks]**

**(b)** Draw the knowledge graph for the RDF statements below and identify one
**derived inference** — a fact that is *not* stated but can be concluded by a
reasoner. **[2 marks]**
```
ex:Vehicle     rdfs:subClassOf  ex:Machine .
ex:Car         rdfs:subClassOf  ex:Vehicle .
ex:ElectricCar rdfs:subClassOf  ex:Car .
ex:Tesla       rdf:type         ex:ElectricCar .
```

**(c)** You are building a **research publication ontology**. How would you
model papers, authors and conferences using RDF and OWL? Explain
briefly. **[2 marks]**

<details><summary><b>Show answer — Q6 Set C</b></summary>

**(a) [2 marks]**

| Language | Full name | Specifies |
|---|---|---|
| **RDF** | Resource Description Framework | **Relationships between data** — facts as subject–predicate–object triples |
| **RDFS** | RDF Schema | **Relationships between schema** — `Class`, `Property`, `type`, `subClassOf`, `subPropertyOf`, `domain`, `range` |
| **OWL** | Web Ontology Language | **More complex relationships between schema**, based on **description logics** — restrictions, cardinality, reasoning |

**(b) [2 marks]**
```
    ex:Machine
        ▲ subClassOf
    ex:Vehicle
        ▲ subClassOf
    ex:Car
        ▲ subClassOf
    ex:ElectricCar
        ▲ type
    ex:Tesla

DERIVED INFERENCE (not stated anywhere, concluded by the reasoner):

    ex:Tesla  rdf:type  ex:Machine

    because  Tesla : ElectricCar ⊑ Car ⊑ Vehicle ⊑ Machine

Other valid derived inferences:
    ex:ElectricCar rdfs:subClassOf ex:Machine
    ex:Car         rdfs:subClassOf ex:Machine
```
> Label the inferred arrow **"inferred"** on your diagram — that is what the
> marks are for. `subClassOf` is **transitive**, which is what makes the chain work.

**(c) [2 marks]**
> In a research publication ontology, **RDF** is used to represent **factual
> data**, while **OWL** is used to define **semantics and constraints**.
>
> **Using RDF**, entities such as `Paper`, `Author` and `Conference` are
> represented as resources and linked using triples:
> `(Paper1, hasAuthor, Author1)`, `(Paper1, presentedAt, Conference1)`.
>
> **Using OWL**, classes and relationships are formally defined. Classes include
> `Paper`, `Author`, `Conference`; object properties include `hasAuthor` and
> `presentedAt`. OWL can also specify constraints such as **every Paper must
> have at least one Author**, enabling **reasoning and consistency checking**.
</details>

---

## Question 7. [3 + 1.5 + 1.5 = 6 Marks]

A media monitoring company is building an NLP summarization system. It must
support:

1. An editor uploads **a single long investigative report** and wants a
   **headline** and a short **abstract**.
2. An analyst supplies **20 articles from different agencies** covering the same
   election result and wants one concise overview.
3. A lawyer uploads a contract and asks: *"Summarize only the clauses relevant
   to **termination penalties**."*

**(a)** Identify the type of summarization required for each scenario. **[3 marks]**
**(b)** Justify your choices by explaining the key characteristics of each
type. **[1.5 marks]**
**(c)** Two candidate sentences are scored against a query with `λ = 0.8`:
`S1: sim(q)=0.90, sim(S)=0.40` and `S2: sim(q)=0.70, sim(S)=0.15`. Compute both
MMR scores and state which is selected. **[1.5 marks]**

<details><summary><b>Show answer — Q7 Set C</b></summary>

**(a) [3 marks]**

| Scenario | Required summarization type |
|---|---|
| 1 | **Single-document, Generic** summarization |
| 2 | **Multi-document** summarization |
| 3 | **Query-focused** summarization |

**(b) [1.5 marks]**
```
1. SINGLE-DOCUMENT, GENERIC
   - Operates on ONE document
   - Produces outputs such as a headline, abstract, or outline
   - Focuses on the OVERALL CONTENT, not a specific query

2. MULTI-DOCUMENT
   - Takes a group of documents related to the SAME EVENT
   - Produces a gist of shared information, REMOVING REDUNDANCY and
     resolving overlaps across sources
   - Commonly used for news aggregation and event summarization

3. QUERY-FOCUSED
   - Tailors the summary to a SPECIFIC USER INFORMATION NEED
   - Acts as a form of COMPLEX QUESTION ANSWERING
   - Ignores unrelated sections of the document
```

**(c) [1.5 marks]**
```
MMR(s) = lambda x sim(s,q) - (1 - lambda) x sim(s,S)
lambda = 0.8 ,  (1 - lambda) = 0.2

MMR(S1) = 0.8 x 0.90 - 0.2 x 0.40 = 0.72 - 0.08 = 0.64
MMR(S2) = 0.8 x 0.70 - 0.2 x 0.15 = 0.56 - 0.03 = 0.53

MMR(S1) > MMR(S2)  =>  SENTENCE S1 IS SELECTED.
```
> **Note the contrast with Set A.** Here the **more relevant** sentence wins,
> because **λ = 0.8** weights relevance heavily and S1's redundancy (0.40) is
> not high enough to overcome its 0.20 relevance advantage. **λ controls the
> trade-off** — do not assume the less-relevant sentence always wins.
</details>

---
---

# Self-marking sheet

Tick each as you get it right **unaided**. Anything unticked after a set is
where your remaining study time should go.

| Skill | A | B | C |
|---|---|---|---|
| Chu-Liu-Edmonds MST | ☐ | | |
| PCFG parse probability | | ☐ | |
| Top-down parse table with backup | | | ☐ |
| Attention weighted sum | ☐ | | ☐ |
| Multi-head concat × W_O | ☐ | | |
| Full self-attention (Q,K,V, mask, softmax) | | ☐ | |
| Lesk overlap | ☐ | | |
| Cosine sense selection | ☐ | | ☐ |
| WordNet theory (homonymy/polysemy/synset) | | ☐ | ☐ |
| RDF triples | | ☐ | ☐ |
| RDF vs OWL | | ☐ | ☐ |
| Derived inference in a knowledge graph | | | ☐ |
| RAG token budget | ☐ | | |
| RAG precision | ☐ | | |
| MMR | ☐ | | ☐ |
| ROUGE-2 | | ☐ | |
| Summarization types | | | ☐ |

**Target:** 45 minutes per set. If a set takes you 90 minutes, you are
*learning*, not *practising* — go back to
[`SOLVED-NUMERICALS.md`](SOLVED-NUMERICALS.md) for that topic, then retry.
