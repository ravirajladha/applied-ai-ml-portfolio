# NLP Simple Numericals — one easy pass per module

> **These are deliberately easy.** The point is not difficulty — it is to run
> the *method* end to end on numbers small enough to check in your head, so that
> in the exam your hand already knows the shape of the answer.
>
> **Work each one on paper before clicking.** Every answer shows the full
> working, laid out the way you should write it in the script — examiners give
> marks for the substitution line even when the final number is wrong.

---

## Contents

| § | Module | Numericals |
|---|---|---|
| 1 | 2 — Vector Semantics | TF-IDF · cosine similarity · PPMI |
| 2 | 3 — Language Models | bigram MLE + Laplace · perplexity · neural LM forward pass |
| 3 | 5 — POS Tagging | estimating A and B from a tagged corpus · baseline accuracy |
| 4 | 6 — HMM | Viterbi (2 states, 2 words) · Forward + posterior |
| 5 | 9 — Statistical Parsing | PCFG parse probability · two competing parses |
| 6 | 10 — Dependency Parsing | best head + cycle check (MST) · well-formedness |
| 7 | 11 — Contextual Embeddings | weighted sum · softmax weights · scaled dot-product · multi-head |
| 8 | 12 — Word Sense | Lesk overlap · cosine sense selection |
| 9 | 13 — Semantic Web | *(no numerical exists — see THEORY-BANK §9)* |
| 10 | 14 — RAG | threshold · token budget · precision/recall/F1 · chunk count |
| 11 | 15 — Summarization | MMR · ROUGE-1 and ROUGE-2 · compression ratio |

---
---

# 1 · Module 2 — Vector Semantics

### The three formulas

```
TF-IDF   =  TF x IDF          where IDF = log10( N / df )
                              N  = total documents
                              df = documents containing the term

cosine   =  (a . b) / ( |a| x |b| )

PMI      =  log2 (  P(w,c)  /  ( P(w) x P(c) )  )
PPMI     =  max( 0 , PMI )
```

<details>
<summary><b>N1.1</b> A corpus has 4 documents. The word "cloud" appears in 2 of them. In document D1 it occurs 3 times and D1 is 20 words long. Compute the TF-IDF of "cloud" in D1. (use log base 10) — answer</summary>

```
TF  = 3 / 20                         = 0.15
IDF = log10( N / df ) = log10(4 / 2)
    = log10(2)                       = 0.301

TF-IDF = 0.15 x 0.301                = 0.0452
```

**Sanity check:** the word is in half the corpus, so IDF is small (0.301). A word
in *all* 4 documents would give `log10(1) = 0` and a TF-IDF of exactly **zero** —
that is the formula telling you the word is useless for discrimination.
</details>

<details>
<summary><b>N1.2</b> Compute the cosine similarity of A = [2, 0, 1] and B = [1, 1, 1]. — answer</summary>

```
Dot product   a . b = (2x1) + (0x1) + (1x1) = 2 + 0 + 1 = 3

Magnitudes    |a| = sqrt(2^2 + 0^2 + 1^2) = sqrt(5) = 2.236
              |b| = sqrt(1^2 + 1^2 + 1^2) = sqrt(3) = 1.732

cosine = 3 / (2.236 x 1.732) = 3 / 3.873 = 0.7746
```

**Answer ≈ 0.77** — fairly similar. Always state the range: cosine lies in
`[0, 1]` for count vectors, where 1 means identical direction.
</details>

<details>
<summary><b>N1.3</b> From this co-occurrence table, compute PPMI(digital, computer) and PPMI(cherry, computer). — answer</summary>

|  | computer | data | **row total** |
|---|---|---|---|
| **cherry** | 2 | 8 | 10 |
| **digital** | 30 | 20 | 50 |
| **col total** | 32 | 28 | **60** |

```
--- digital & computer ---
P(digital, computer) = 30 / 60 = 0.500
P(digital)           = 50 / 60 = 0.8333
P(computer)          = 32 / 60 = 0.5333

PMI  = log2( 0.500 / (0.8333 x 0.5333) )
     = log2( 0.500 / 0.4444 )
     = log2( 1.125 )                    = 0.170
PPMI = max(0, 0.170)                    = 0.170

--- cherry & computer ---
P(cherry, computer)  =  2 / 60 = 0.0333
P(cherry)            = 10 / 60 = 0.1667
P(computer)          = 32 / 60 = 0.5333

PMI  = log2( 0.0333 / (0.1667 x 0.5333) )
     = log2( 0.0333 / 0.0889 )
     = log2( 0.375 )                    = -1.415
PPMI = max(0, -1.415)                   = 0
```

**The teaching point:** *cherry–computer* co-occurs **less** than chance, so PMI
goes negative and PPMI clips it to **0**. That clipping is the whole reason the
"P" is in PPMI — see THEORY-BANK Q1.5.
</details>

---
---

# 2 · Module 3 — Language Models & Neural LM

<details>
<summary><b>N2.1</b> Corpus: <code>&lt;s&gt; i like nlp &lt;/s&gt;</code> · <code>&lt;s&gt; i like ml &lt;/s&gt;</code> · <code>&lt;s&gt; i study nlp &lt;/s&gt;</code>. Compute P(like | i) with MLE, then with Laplace smoothing. — answer</summary>

```
Step 1 — vocabulary (unique tokens INCLUDING <s> and </s>)
  <s>, i, like, nlp, </s>, ml, study            ->  V = 7

Step 2 — counts
  count(i like) = 2          (sentences 1 and 2)
  count(i)      = 3          (all three sentences)

Step 3 — MLE
  P(like | i) = 2 / 3 = 0.667

Step 4 — Laplace
  P(like | i) = (count(i like) + 1) / (count(i) + V)
              = (2 + 1) / (3 + 7)
              = 3 / 10 = 0.30
```

**The two marks people lose:**
1. Forgetting `<s>` and `</s>` in V. Read the question — it usually says
   "including" explicitly.
2. Adding **1** to the denominator instead of **V**.

Notice smoothing *lowers* a well-attested probability (0.667 → 0.30). That is
the price paid for giving unseen bigrams a non-zero probability.
</details>

<details>
<summary><b>N2.2</b> A bigram model assigns probabilities 0.5, 0.25, 0.5, 0.25 to the four words of a test sentence. Compute the perplexity. — answer</summary>

```
P(W) = 0.5 x 0.25 x 0.5 x 0.25 = 0.015625      ( = 1/64 )

N = 4 words

PP(W) = P(W)^(-1/N)
      = (1/64)^(-1/4)
      = 64^(1/4)
      = 2.828
```

**Answer ≈ 2.83.** Interpretation: at each step the model is about as uncertain
as if it were choosing uniformly among **2.83 words**. Lower is better.

**Shortcut for the exam:** the geometric mean of the probabilities is
`(1/64)^(1/4) = 0.354`, and perplexity is simply its reciprocal, `1/0.354 = 2.83`.
</details>

<details>
<summary><b>N2.3</b> Neural LM forward pass. x = [2.0, 1.0], w = [0.4, −0.2], b = 0.1, hidden activation = <b>sigmoid</b>. Scores: z(A) = 1.5h, z(B) = 0.5h. Find the softmax probability of A. — answer</summary>

```
Step 1 — pre-activation
  z = (2.0 x 0.4) + (1.0 x -0.2) + 0.1
    = 0.8 - 0.2 + 0.1
    = 0.7

Step 2 — sigmoid
  h = 1 / (1 + e^-0.7) = 1 / (1 + 0.4966) = 0.6682

Step 3 — output scores
  z(A) = 1.5 x 0.6682 = 1.0023
  z(B) = 0.5 x 0.6682 = 0.3341

Step 4 — softmax
  e^1.0023 = 2.7245
  e^0.3341 = 1.3967
  sum      = 4.1212

  P(A) = 2.7245 / 4.1212 = 0.6611
  P(B) = 1.3967 / 4.1212 = 0.3389
```

**Answer P(A) ≈ 0.661.** Free check: `0.661 + 0.339 = 1.000`.

**If the activation were ReLU instead:** `h = max(0, 0.7) = 0.7`, and everything
downstream repeats identically. Read which activation you were given — it is a
one-mark trap.
</details>

---
---

# 3 · Module 5 — POS Tagging

<details>
<summary><b>N3.1</b> From this tagged corpus, estimate P(NN | DT) and P(dog | NN).<br><code>the/DT dog/NN runs/VB</code> · <code>the/DT cat/NN sleeps/VB</code> · <code>a/DT dog/NN barks/VB</code> — answer</summary>

```
--- Transition:  P(NN | DT) = count(DT followed by NN) / count(DT)

  DT NN pairs : the-dog , the-cat , a-dog          =  3
  count(DT)                                        =  3

  P(NN | DT) = 3 / 3 = 1.0

--- Emission:   P(dog | NN) = count(NN emitting "dog") / count(NN)

  NN tokens : dog , cat , dog                      =  3
  "dog" among them                                 =  2

  P(dog | NN) = 2 / 3 = 0.667
```

**Remember the direction of each formula** — this is where marks vanish:
- **Transition** is `P(this tag | previous tag)` → divide by the count of the
  **previous** tag.
- **Emission** is `P(word | tag)` → divide by the count of the **tag**, never the
  count of the word.
</details>

<details>
<summary><b>N3.2</b> The word "book" appears 10 times in a test set: 7 as NN and 3 as VB. What accuracy does the most-frequent-tag baseline achieve on this word, and what does it get wrong? — answer</summary>

```
Most frequent tag for "book" = NN  (7 out of 10)

Baseline tags ALL 10 occurrences as NN.

Correct   = 7
Accuracy  = 7 / 10 = 0.70  =  70%
```

**What it gets wrong:** all **3 verb** uses — *"book a flight"*, *"book the
room"*. The baseline is context-blind by construction, so it can never recover
the minority tag. That is precisely the gap an HMM closes: the transition
probability `P(VB | DT)` is low while `P(NN | DT)` is high, so context tips the
decision.
</details>

---
---

# 4 · Module 6 — Hidden Markov Models

**The shared setup for both questions below.**

States: **H** (hot), **C** (cold). Observations: ice-creams eaten, `3` then `1`.

**Start probabilities (π)**

| state | P |
|---|---|
| H | 0.8 |
| C | 0.2 |

**Transition probabilities (A)** — read as `P(next | current)`

| from ↓ / to → | H | C |
|---|---|---|
| **H** | 0.7 | 0.3 |
| **C** | 0.4 | 0.6 |

**Emission probabilities (B)** — read as `P(word | tag)`

| state | "1" | "3" |
|---|---|---|
| **H** | 0.2 | 0.4 |
| **C** | 0.5 | 0.1 |

<details>
<summary><b>N4.1</b> Run <b>Viterbi</b> for the observation sequence (3, 1). Give the best state sequence. — answer</summary>

```
--- t = 1   (observation = "3")   initialisation: start x emission

  v1(H) = 0.8 x 0.4 = 0.32
  v1(C) = 0.2 x 0.1 = 0.02

--- t = 2   (observation = "1")   recursion: MAX(prev x transition) x emission

  v2(H) : from H  0.32 x 0.7 = 0.224   <-- max
          from C  0.02 x 0.4 = 0.008
          v2(H) = 0.224 x 0.2 = 0.0448      backpointer -> H

  v2(C) : from H  0.32 x 0.3 = 0.096   <-- max
          from C  0.02 x 0.6 = 0.012
          v2(C) = 0.096 x 0.5 = 0.0480      backpointer -> H

--- termination

  best final state = C   (0.0480 > 0.0448)

--- backtracking

  C at t=2  ->  backpointer says H at t=1
```

**Best sequence = H → C**, probability **0.048**.

**Layout marks:** always write the three labelled stages — *initialisation,
recursion, backtracking* — and always write the backpointer next to each cell.
The question asks for them by name.
</details>

<details>
<summary><b>N4.2</b> Same model, same observations. Run the <b>Forward</b> algorithm, give P(O), and the posterior distribution at t = 2. — answer</summary>

```
--- t = 1   (identical to Viterbi)

  a1(H) = 0.8 x 0.4 = 0.32
  a1(C) = 0.2 x 0.1 = 0.02

--- t = 2   SUM(prev x transition) x emission     <-- the only change

  a2(H) = (0.32 x 0.7  +  0.02 x 0.4) x 0.2
        = (0.224 + 0.008) x 0.2
        = 0.232 x 0.2 = 0.0464

  a2(C) = (0.32 x 0.3  +  0.02 x 0.6) x 0.5
        = (0.096 + 0.012) x 0.5
        = 0.108 x 0.5 = 0.0540

--- likelihood of the whole observation sequence

  P(O) = 0.0464 + 0.0540 = 0.1004

--- posterior at t = 2   (divide each cell by P(O))

  P(H at t=2 | O) = 0.0464 / 0.1004 = 0.462
  P(C at t=2 | O) = 0.0540 / 0.1004 = 0.538
```

**Most likely state at t = 2 is C (0.538)** — because C emits "1" with
probability 0.5 against H's 0.2, which outweighs H's higher prior.

**Compare with N4.1:** identical table, `SUM` instead of `MAX`, no backpointers.
Forward's numbers are slightly larger because they add all paths rather than
keeping the best. The posterior must sum to 1 — `0.462 + 0.538 = 1.000`.
</details>

---
---

# 5 · Module 9 — Statistical Parsing

<details>
<summary><b>N5.1</b> Using this PCFG, compute the probability of the only parse of "the dog ate the bone". — answer</summary>

| Rule | P | | Rule | P |
|---|---|---|---|---|
| S → NP VP | 1.0 | | Det → the | 1.0 |
| NP → Det N | 0.6 | | N → dog | 0.5 |
| NP → N | 0.4 | | N → bone | 0.5 |
| VP → V NP | 1.0 | | V → ate | 1.0 |

```
Parse:  S -> NP(Det N) VP( V NP(Det N) )

Rules used, in order:
  S  -> NP VP     1.0
  NP -> Det N     0.6        (subject)
  Det-> the       1.0
  N  -> dog       0.5
  VP -> V NP      1.0
  V  -> ate       1.0
  NP -> Det N     0.6        (object)
  Det-> the       1.0
  N  -> bone      0.5

P(parse) = 1.0 x 0.6 x 1.0 x 0.5 x 1.0 x 1.0 x 0.6 x 1.0 x 0.5
         = 0.09
```

**Method, every time:** the probability of a parse is the **product of the
probability of every rule used**, counting a rule once per *use*, not once per
rule. `NP → Det N` is used **twice** here, so 0.6 appears twice.
</details>

<details>
<summary><b>N5.2</b> Two parses of "I saw the man with the telescope". Compute both probabilities and say which the grammar prefers. — answer</summary>

| Rule | P | | Rule | P |
|---|---|---|---|---|
| S → NP VP | 1.0 | | Det → the | 1.0 |
| VP → V NP | 0.6 | | N → man | 0.5 |
| VP → VP PP | 0.4 | | N → telescope | 0.5 |
| NP → Det N | 0.5 | | V → saw | 1.0 |
| NP → NP PP | 0.3 | | P → with | 1.0 |
| NP → Pron | 0.2 | | Pron → I | 1.0 |
| PP → P NP | 1.0 | | | |

```
=== Parse A — VP attachment  (I used the telescope to see) ===
S -> NP(Pron) VP( VP(V NP) PP )

  S -> NP VP      1.0
  NP -> Pron      0.2      Pron -> I        1.0
  VP -> VP PP     0.4
    VP -> V NP    0.6      V -> saw         1.0
      NP -> Det N 0.5      Det 1.0 , N->man 0.5
    PP -> P NP    1.0      P -> with        1.0
      NP -> Det N 0.5      Det 1.0 , N->telescope 0.5

P(A) = 1.0 x 0.2 x [ 0.4 x (0.6 x 0.5 x 0.5) x (1.0 x 0.5 x 0.5) ]
     = 0.2 x [ 0.4 x 0.15 x 0.25 ]
     = 0.2 x 0.015
     = 0.00300

=== Parse B — NP attachment  (the man was holding the telescope) ===
S -> NP(Pron) VP( V NP( NP PP ) )

  S -> NP VP      1.0
  NP -> Pron      0.2      Pron -> I        1.0
  VP -> V NP      0.6      V -> saw         1.0
    NP -> NP PP   0.3
      NP -> Det N 0.5      Det 1.0 , N->man 0.5
      PP -> P NP  1.0      P -> with        1.0
        NP-> Det N 0.5     Det 1.0 , N->telescope 0.5

P(B) = 1.0 x 0.2 x [ 0.6 x ( 0.3 x (0.5 x 0.5) x (1.0 x 0.5 x 0.5) ) ]
     = 0.2 x [ 0.6 x 0.01875 ]
     = 0.2 x 0.01125
     = 0.00225
```

**The grammar selects Parse A, the VP attachment (0.00300 > 0.00225)** — the
telescope is the instrument of seeing.

**The "why" mark:** say *which rule* decided it. Here `VP → VP PP` (0.4) is more
probable than `NP → NP PP` (0.3), so the grammar prefers attaching the PP to the
verb phrase. In the Mar 2026 paper the numbers were the other way round and the
NP attachment won — so **never memorise the conclusion, only the method**.
</details>

---
---

# 6 · Module 10 — Dependency Parsing

<details>
<summary><b>N6.1</b> Sentence "dogs bark" with ROOT. Arc scores below. Find the maximum spanning tree. — answer</summary>

| From → To | Score |
|---|---|
| ROOT → dogs | 5 |
| ROOT → bark | 10 |
| dogs → bark | 8 |
| bark → dogs | 6 |

```
Step 1 — give every word its highest-scoring head

  dogs : ROOT gives 5 , bark gives 6   ->  best head = bark  (6)
  bark : ROOT gives 10 , dogs gives 8  ->  best head = ROOT  (10)

Step 2 — check for a cycle

  arcs = { ROOT -> bark , bark -> dogs }
  follow backwards from dogs : dogs -> bark -> ROOT     reaches ROOT
  no cycle  ->  this greedy answer is already the MST

Step 3 — total score

  10 + 6 = 16

  (the only other valid tree is ROOT->dogs + dogs->bark = 5 + 8 = 13)
```

**MST = ROOT → bark → dogs, total score 16.** *bark* is the root verb, *dogs*
is its subject (`nsubj`).

**When it is NOT this easy:** if step 1 produced a cycle (say dogs→bark and
bark→dogs), you would **contract the cycle into one node, re-score, and
re-solve** — that is Chu-Liu-Edmonds. See the full worked version in
`../post-midsem/SOLVED-NUMERICALS.md` §2.3.
</details>

<details>
<summary><b>N6.2</b> Draw the dependency tree for "She ate rice quickly" and verify it is well-formed. — answer</summary>

```
        ROOT
          |
         ate                         ate  is the ROOT (the main verb)
        / | \
      /   |   \
    She  rice quickly

Arcs with labels:
  ROOT -> ate        (root)
  ate  -> She        (nsubj  - the subject)
  ate  -> rice       (dobj   - the direct object)
  ate  -> quickly    (advmod - the adverbial modifier)
```

**Well-formedness check — write these three lines out, they carry marks:**

```
1. Single head  : She(1) rice(1) quickly(1) ate(1)      OK - each has exactly one
2. Root         : nothing points INTO ROOT              OK
3. Connected /
   acyclic      : She->ate->ROOT , rice->ate->ROOT ,
                  quickly->ate->ROOT                    OK - all reach ROOT
4. Projective   : no arcs cross when drawn above        OK
```

**Method for any sentence:** find the **main verb** first — it is almost always
the ROOT. Everything else hangs off it or off one of its dependents.
</details>

---
---

# 7 · Module 11 — Contextual Embeddings & Attention

### The formula box

```
Per token:      q_i = Q x_i      k_i = K x_i      v_i = V x_i
                e_ij = q_i . k_j  /  sqrt(d_k)
                alpha_ij = exp(e_ij) / SUM_j exp(e_ij)
                o_i = SUM_j  alpha_ij  x  v_j

Matrix form:    SelfAttention(Q,K,V) = softmax( Q K^T / sqrt(d_k) ) V

Multi-head:     MultiHead(X) = ( head_1 (+) head_2 (+) ... ) W_O
```
> Both of these are printed in **Part 2 of the handout, pages 45–46** — as
> images, so `Ctrl-F` will not find them. Tab those pages.

<details>
<summary><b>N7.1</b> α = [0.2, 0.3, 0.5] and v₁ = [1,0], v₂ = [0,2], v₃ = [2,2]. Compute the contextual embedding. — answer</summary>

```
Output = 0.2 x [1,0]  +  0.3 x [0,2]  +  0.5 x [2,2]

       = [0.2, 0.0]  +  [0.0, 0.6]  +  [1.0, 1.0]

       = [1.2, 1.6]
```

**Free check first, always:** `0.2 + 0.3 + 0.5 = 1.0`. If the given weights do
not sum to 1, you have misread the question.
</details>

<details>
<summary><b>N7.2</b> Attention scores before softmax are [1, 1, 2]. Compute the attention weights. (e¹ = 2.718, e² = 7.389) — answer</summary>

```
exponentiate :  e^1 = 2.718 ,  e^1 = 2.718 ,  e^2 = 7.389

sum          :  2.718 + 2.718 + 7.389 = 12.825

divide       :  2.718 / 12.825 = 0.212
                2.718 / 12.825 = 0.212
                7.389 / 12.825 = 0.576

alpha = [0.212, 0.212, 0.576]     check: sums to 1.000
```

**The point:** a score of 2 against 1 is only *double*, but the weight is nearly
**triple** (0.576 vs 0.212). Softmax **exponentiates first**, so it exaggerates
the leader. That is the intuition examiners want in the "comment" sub-part.
</details>

<details>
<summary><b>N7.3</b> q = [1,1], k₁ = [1,0], k₂ = [0,2], v₁ = [1,0], v₂ = [0,1], d_k = 2. Compute the output using <b>scaled</b> dot-product attention. — answer</summary>

```
Step 1 — raw dot products
  q . k1 = (1x1) + (1x0) = 1
  q . k2 = (1x0) + (1x2) = 2

Step 2 — scale by sqrt(d_k) = sqrt(2) = 1.414
  e1 = 1 / 1.414 = 0.707
  e2 = 2 / 1.414 = 1.414

Step 3 — softmax
  e^0.707 = 2.028
  e^1.414 = 4.113
  sum     = 6.141

  alpha = [ 2.028/6.141 , 4.113/6.141 ] = [0.330 , 0.670]

Step 4 — weighted sum of values
  out = 0.330 x [1,0]  +  0.670 x [0,1]
      = [0.330, 0.670]
```

**Answer = [0.330, 0.670].** Note what the scaling did: without dividing by
√d_k the scores would have been 1 and 2, giving weights [0.269, 0.731] — a
sharper, more saturated distribution. Scaling keeps softmax in its
well-behaved range. That is the answer to "why √d_k" (THEORY-BANK Q7.5).
</details>

<details>
<summary><b>N7.4</b> head₁ = [0.2, 0.5], head₂ = [0.4, 0.1], W_O = [[1,0],[0,2],[2,0],[0,1]]. Compute the multi-head output. — answer</summary>

```
Step 1 — concatenate
  Concat = [0.2, 0.5, 0.4, 0.1]          4 numbers

  Check: W_O has 4 ROWS, concat has 4 entries.  They must match.

Step 2 — multiply by W_O, one COLUMN at a time
  (go down the column, multiply element-wise, add)

  column 1 :  0.2x1 + 0.5x0 + 0.4x2 + 0.1x0
           =  0.2   + 0     + 0.8   + 0       = 1.0

  column 2 :  0.2x0 + 0.5x2 + 0.4x0 + 0.1x1
           =  0     + 1.0   + 0     + 0.1     = 1.1

Output = [1.0, 1.1]
```

**Answer = [1.0, 1.1].**

**Two things to say for the theory marks:** (i) `W_O` **projects back down to
the model dimension d**, so the output is the same size as the input and blocks
can be stacked; (ii) the number of `W_O` rows equalling the concatenated length
is your dimension check.
</details>

---
---

# 8 · Module 12 — Word Sense & WordNet

<details>
<summary><b>N8.1</b> Simplified Lesk. Which sense of "bank" is used in <i>"He sat on the river bank and watched the water."</i>? — answer</summary>

```
Sense 1 gloss : { sloping , land , river , water , edge }
Sense 2 gloss : { financial , institution , money , deposit , loan }

Step 1 — content words of the sentence (drop stop-words and the target itself)
  { sat , river , watched , water }

Step 2 — overlap with each gloss
  Sense 1 :  river , water                    ->  2
  Sense 2 :  (nothing)                        ->  0

Step 3 — pick the maximum
```

**Answer: Sense 1 — the sloping land beside a river.** Overlap 2 vs 0.

**Write the overlapping words out explicitly**, not just the count — the marking
scheme gives credit for identifying which words matched. Drop stop-words
(*he, on, the, and*) and drop the ambiguous word itself before counting.
</details>

<details>
<summary><b>N8.2</b> Context vector c = [1, 2]. Sense A = [2, 1], Sense B = [1, 3]. Which sense is selected? — answer</summary>

```
--- cosine( c , A )
  dot  = (1x2) + (2x1) = 4
  |c|  = sqrt(1 + 4)  = sqrt(5)  = 2.236
  |A|  = sqrt(4 + 1)  = sqrt(5)  = 2.236
  cos  = 4 / (2.236 x 2.236) = 4 / 5 = 0.800

--- cosine( c , B )
  dot  = (1x1) + (2x3) = 7
  |c|  = 2.236
  |B|  = sqrt(1 + 9)  = sqrt(10) = 3.162
  cos  = 7 / (2.236 x 3.162) = 7 / 7.071 = 0.990
```

**Sense B is selected (0.990 > 0.800).**

**The justification sentence:** B points in almost the same *direction* as the
context vector even though its magnitude differs — and cosine ignores magnitude,
measuring only direction. That is exactly why cosine is the right tool here.
</details>

---
---

# 9 · Module 13 — Semantic Web & Ontology

> **There is no numerical in this module.** The scheme lists it as *Application /
> Case Study*, and both past papers asked for RDF triples and a modelling
> justification in prose.
>
> Go to **THEORY-BANK §9** — questions Q9.2 (write triples), Q9.3 (RDF vs OWL)
> and Q9.4 (the publication-ontology case study) are the three that have actually
> been asked.

---
---

# 10 · Module 14 — Retrieval-Augmented Generation

<details>
<summary><b>N10.1</b> A retriever returns similarity scores 0.91, 0.83, 0.77, 0.68, 0.55 with a threshold of 0.75. How many chunks reach the LLM? — answer</summary>

```
Keep every score >= 0.75 :

  0.91  >= 0.75   keep
  0.83  >= 0.75   keep
  0.77  >= 0.75   keep
  0.68  <  0.75   drop
  0.55  <  0.75   drop

Chunks passed to the LLM = 3
```

**State the boundary rule you used** ("greater than or equal to"), because a
score sitting exactly on the threshold is a favourite trap. Then add the reason
a threshold exists at all: low-similarity chunks are **contextual noise** that
consumes the context window and degrades generation.
</details>

<details>
<summary><b>N10.2</b> Context window = 8000 tokens. System prompt 300, user query 100, and 1000 reserved for the answer. Each chunk is 450 tokens. How many chunks fit? — answer</summary>

```
Step 1 — subtract everything that is not a chunk

  8000  total window
  - 300  system prompt
  - 100  user query
  -1000  reserved for the generated answer
  ------
   6600  available for retrieved chunks

Step 2 — divide by the chunk size

  6600 / 450 = 14.67

Step 3 — round DOWN (a partial chunk is not usable)

  14 chunks
```

**Answer: 14 chunks**, using 6300 tokens and leaving 300 spare.

**Always round down and say why.** And never forget the **reserve for the
answer** — if you fill the window with context, the model has no room to reply.
</details>

<details>
<summary><b>N10.3</b> 8 chunks are retrieved, of which 5 are relevant. The corpus contains 10 relevant chunks in total. Compute precision, recall and F1. — answer</summary>

```
Precision = relevant retrieved / total retrieved
          = 5 / 8  = 0.625

Recall    = relevant retrieved / total relevant that exist
          = 5 / 10 = 0.500

F1 = 2PR / (P + R)
   = (2 x 0.625 x 0.500) / (0.625 + 0.500)
   = 0.625 / 1.125
   = 0.556
```

**Precision 0.625 · Recall 0.50 · F1 0.556.**

**The comment sub-part:** precision below 1 means **irrelevant chunks are
polluting the prompt** — contextual noise that can pull the generated answer
off-course. Recall of 0.5 means **half the relevant evidence was never
retrieved**, so the answer may simply be incomplete. Lowering the similarity
threshold raises recall but lowers precision — that is the trade-off to name.
</details>

<details>
<summary><b>N10.4</b> A 2000-token document is chunked with chunk size 500 and overlap 100. How many chunks are produced? — answer</summary>

```
Stride (how far the window advances) = chunk size - overlap
                                     = 500 - 100 = 400

Chunk start positions: 0 , 400 , 800 , 1200 , 1600

  chunk 1 :    0 -  500
  chunk 2 :  400 -  900
  chunk 3 :  800 - 1300
  chunk 4 : 1200 - 1700
  chunk 5 : 1600 - 2000     (the last one, ends at the document end)

Number of chunks = 5

Formula: ceil( (2000 - 500) / 400 ) + 1 = ceil(3.75) + 1 = 4 + 1 = 5
```

**Answer: 5 chunks.** Without overlap it would be exactly 4 — the overlap costs
you one extra chunk of storage, and that is the price of not cutting an idea in
half at a boundary (THEORY-BANK Q10.3).
</details>

---
---

# 11 · Module 15 — Text Summarization

<details>
<summary><b>N11.1</b> MMR with λ = 0.7. S1: sim(q) = 0.90, sim(S) = 0.60. S2: sim(q) = 0.75, sim(S) = 0.20. Which is selected? — answer</summary>

```
MMR(s) = lambda x sim(s,q)  -  (1 - lambda) x sim(s,S)

lambda = 0.7   so   (1 - lambda) = 0.3

MMR(S1) = 0.7 x 0.90  -  0.3 x 0.60
        = 0.630 - 0.180
        = 0.450

MMR(S2) = 0.7 x 0.75  -  0.3 x 0.20
        = 0.525 - 0.060
        = 0.465
```

**S2 is selected (0.465 > 0.450).**

**The justification — this is where the marks are:** S1 is *more relevant* to the
query (0.90 vs 0.75), but it is also **highly redundant** with what has already
been chosen (0.60 vs 0.20), so the penalty term wipes out its advantage. S2
contributes **new, complementary information**. MMR deliberately trades a little
relevance for **diversity and coverage**, which is what stops a summary
repeating the same fact.
</details>

<details>
<summary><b>N11.2</b> Reference: "the cat sat on the mat". Candidate: "the cat sat on a mat". Compute ROUGE-1 and ROUGE-2 recall. — answer</summary>

```
=== ROUGE-1 (unigrams) ===

Reference tokens : the , cat , sat , on , the , mat      (6)
Candidate tokens : the , cat , sat , on , a  , mat       (6)

Overlapping unigrams (clipped to how often each appears in the candidate):
  the (1) , cat (1) , sat (1) , on (1) , mat (1)         = 5

  Recall    = 5 / 6 = 0.833
  Precision = 5 / 6 = 0.833

=== ROUGE-2 (bigrams) ===

Reference bigrams : (the cat)(cat sat)(sat on)(on the)(the mat)    = 5
Candidate bigrams : (the cat)(cat sat)(sat on)(on a )(a  mat)      = 5

Overlap : (the cat)(cat sat)(sat on)                               = 3

  Recall = 3 / 5 = 0.600
```

**ROUGE-1 = 0.833 · ROUGE-2 = 0.600.**

**Why ROUGE-2 is so much lower:** one substituted word (*the* → *a*) breaks
**two** bigrams, not one. Bigram overlap punishes local word changes far harder
than unigram overlap — which is exactly why ROUGE-2 is reported alongside
ROUGE-1, and why both are poor at recognising a valid paraphrase.
</details>

<details>
<summary><b>N11.3</b> A 500-word document is summarised in 75 words. Compute the compression ratio. — answer</summary>

```
Compression ratio = summary length / original length
                  = 75 / 500
                  = 0.15   =  15%
```

The summary is **15% of the original**; equivalently the text was compressed by
**85%**. Typical extractive summaries sit between 10% and 30% — tighter than
that and content selection starts dropping essential facts.

**If asked the other way round:** "compressed to 15%" and "compressed **by** 85%"
mean the same thing. State which one you are giving.
</details>
