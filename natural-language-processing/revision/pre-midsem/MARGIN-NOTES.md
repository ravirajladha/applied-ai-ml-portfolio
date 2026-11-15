# Pencil Margin Notes — Pre-Midsem

**What this is:** what to pencil into the corner of your printed handout, page by
page. Same format as the post-midsem pack:

```
RECIPE    the steps
Q ASKED   the real past-paper question, compressed  (and which paper)
A         the worked answer, short enough to fit in a margin
```

**Which document the page numbers refer to:**
`notes/NLP_Handout_Part1_Sessions_1-8 (1).pdf` — 116 pages, Sessions 1 → 8.
Page numbers are **PDF page numbers** (page 1 = title page). Each heading names
the slide title on that page so you can confirm you're on the right sheet.

---

## ⚠️ Read this before you pick up the pencil

In the **end-semester** paper, pre-midsem material is **only Q1 and Q2 = 10 of 40
marks**. Across all four past papers those two questions have been the **same two
topics every single time**:

| Q | Marks | Always asks | Handout pages |
|---|---|---|---|
| **Q1** | 5 | **(A)** bigram probability with **Laplace smoothing** · **(B)** a **neural LM forward pass** ending in **softmax** | **p61**, **p69** |
| **Q2** | 5 | **HMM** — **Viterbi** *or* **Forward** | **p98**, **p102** |

Plus the official paper structure lists *Module 2: Vector Semantics — Problem*
inside Q1, so **TF-IDF / cosine / PPMI are live** → **p17, p19**.

**Sessions 1, 7 and 8** — intro/ambiguity, LLMs, prompting — have **never**
appeared in Q1 or Q2 of an endsem. They were tested in the mid-sem. Annotate them
last, or not at all.

> **So: five pages carry all 10 marks — p17/p19, p61, p69, p98, p102.**
> If you have twenty minutes, do only those.

---

## First: the inside front cover

```
 Q1a  Laplace bigram ......... p61
 Q1a' TF-IDF / cosine / PPMI . p17, p19
 Q1b  Forward pass + softmax . p69  (network notation p73)
 Q2   Viterbi / Forward ...... p102 (probability types p98)

 THE FIVE FORMULAS
 Laplace   P = (count(w1w2) + 1) / (count(w1) + V)     <- add V, NOT 1
 Fwd pass  z = SUM(wi.xi) + b -> h = ReLU/sigmoid(z) -> scores -> softmax
 Softmax   e^zA / (e^zA + e^zB)
 VITERBI   cell = MAX(prev x transition) x emission   + backpointer
 FORWARD   cell = SUM(prev x transition) x emission

 VITERBI = MAX (best single path).  FORWARD = SUM (total probability).
 V includes <s> and </s> when the question says so.
```

---

# Session 1 — Introduction (handout p1–p10)

> Never asked in Q1/Q2 of an endsem. One note only, and only if you have time.

### p8 — "Levels of language understanding"

```
RECIPE  the levels, smallest to largest
  MORPHOLOGICAL  how words are built from morphemes (un-happy-ness)
  LEXICAL        what individual words mean, their POS
  SYNTACTIC      grammatical structure of the sentence
  SEMANTIC       literal meaning, independent of context
  DISCOURSE      meaning across sentences (what does "it" refer to?)
  PRAGMATIC      speaker intent, real-world knowledge
  AMBIGUITY exists at EVERY level — that is why NLP is hard
```

---

# Sessions 2 & 3 — Vector Semantics and Embeddings (handout p11–p52)

### ⭐ p17 — "Computing word similarity: Dot product and cosine"

```
RECIPE  cos(a,b) = ( a . b ) / ( |a| x |b| )
        |[2,0,1]| = sqrt(4+0+1) = sqrt(5) = 2.236
        range 0..1 for count vectors; 1 = same direction
        ALWAYS divide by both magnitudes — the raw dot product just
        rewards long vectors

Q ASKED  cosine similarity of A = [2, 0, 1] and B = [1, 1, 1]

A  dot = 2x1 + 0x1 + 1x1 = 3
   |a| = sqrt(5) = 2.236 ,  |b| = sqrt(3) = 1.732
   cos = 3 / (2.236 x 1.732) = 3 / 3.873 = 0.7746  ~ 0.77
```

### ⭐ p19 — "tf-idf" (second factor) — also write PPMI here

```
RECIPE  TF-IDF = TF x IDF ,  IDF = log10( N / df )
        N = total documents , df = documents containing the term
        a word in ALL documents -> log10(1) = 0 -> TF-IDF = 0
        (the formula saying "this word cannot discriminate")

Q ASKED  4 documents; "cloud" appears in 2 of them; in D1 it occurs
         3 times and D1 is 20 words long. TF-IDF of "cloud" in D1?

A  TF  = 3/20 = 0.15
   IDF = log10(4/2) = log10(2) = 0.301
   TF-IDF = 0.15 x 0.301 = 0.0452

--- PPMI, same page ---
RECIPE  PMI  = log2( P(w,c) / ( P(w) x P(c) ) )
        PPMI = max( 0 , PMI )     <- negative PMI clips to ZERO

Q ASKED  co-occurrence table, total 60
         cherry: computer 2, data 8  (row 10)
         digital: computer 30, data 20 (row 50) ; computer column 32

A  digital & computer
     P(w,c)=30/60=0.500 , P(w)=50/60=0.8333 , P(c)=32/60=0.5333
     PMI = log2(0.500 / 0.4444) = log2(1.125) = 0.170 -> PPMI 0.170
   cherry & computer
     P(w,c)=2/60=0.0333 , P(w)=10/60=0.1667 , P(c)=0.5333
     PMI = log2(0.0333 / 0.0889) = log2(0.375) = -1.415 -> PPMI 0
   POINT: cherry-computer co-occurs LESS than chance -> negative ->
   clipped to 0. That clipping is the whole reason for the "P" in PPMI.
```

### p20 — "tf-idf vectors are long and sparse"

```
RECIPE  SPARSE (tf-idf, PPMI): length |V| = 20k-50k, mostly zeros, COUNTED
        DENSE (word2vec, GloVe): length 50-1000, all non-zero, LEARNED
        dense wins: fewer parameters, generalises to similar words
```

### p38–p41 — word2vec / skip-gram with negative sampling

```
RECIPE  SKIP-GRAM: given the TARGET word, predict the CONTEXT words
        CBOW: given the context, predict the target  (the opposite)
        turns the dot product into a probability with the sigmoid:
             P(+ | w,c) = sigmoid(w . c) = 1 / (1 + e^-(w.c))
        NEGATIVE SAMPLING: for each real (target, context) pair grab k
        random words as negative examples, sampled by frequency
        goal: maximise similarity to the real context, minimise it to
        the k negatives
```

### p31 / p48 — window size

```
RECIPE  small window (+/-2) -> SYNTACTIC neighbours, same taxonomy
        large window (+/-5+) -> TOPICAL neighbours, same subject area
```

### p52 — GloVe

```
RECIPE  word2vec PREDICTS (local windows, one at a time)
        GloVe COUNTS then factorises the global co-occurrence matrix
        GloVe idea: the RATIO of conditional probabilities carries meaning
        analogy: king - man + woman = queen  (parallelogram model, p34/p51)
```

---

# Session 4 — N-gram Language Models (handout p53–p66)

### p55–p56 — chain rule / bigram model

```
RECIPE  chain rule  P(w1..wn) = PRODUCT of P(wk | w1..wk-1)
        MARKOV ASSUMPTION: only look back n-1 words
        bigram  P(w1..wn) = PRODUCT of P(wk | wk-1)
        eg P(I want to eat) = P(I|<s>)P(want|I)P(to|want)P(eat|to)
        unsmoothed MLE:  P(wk|wk-1) = count(wk-1 wk) / count(wk-1)
```

### ⭐⭐ p61 — "Laplace-smoothed bigrams" — THE Q1(A) PAGE

```
RECIPE                count(w1 w2) + 1
        P_Laplace = --------------------      <- add V to the BOTTOM, not 1
                       count(w1) + V

        V = number of UNIQUE tokens in the corpus.
        If the question says "including <s> and </s>", COUNT THEM.
        Why: zero counts would kill the whole sentence probability;
        Laplace steals mass from seen bigrams and shares it out.

Q ASKED (Feb 2026 Q1A, 2m)
  Corpus:  <s> deep learning </s>
           <s> machine learning </s>
           <s> deep thought </s>
  Laplace-smoothed P(learning | deep)? V includes <s> and </s>.

A  V = { <s>, </s>, deep, learning, machine, thought }  ->  V = 6
   count("deep learning") = 1        count("deep") = 2
   P = (1 + 1) / (2 + 6) = 2/8 = 0.25
   compare unsmoothed MLE = 1/2 = 0.5 — Laplace HALVED it, because it
   must give mass to the 4 words that never follow "deep"

Q VARIANT (Mar 2026 Q1A) same shape, weather corpus
  <s> sun hot </s> / <s> rain cold </s> / <s> sun bright </s>
  P(bright | sun)?
A  V = {<s>,</s>,sun,hot,rain,cold,bright} = 7 ; counts 1 and 2
   Laplace = (1+1)/(2+7) = 2/9 = 0.2222 ; MLE = 1/2 = 0.50
   The makeup paper never says the word "Laplace" — GIVE 0.2222 as the
   main answer, show MLE 0.50 in one line, and STATE YOUR ASSUMPTION.
```

### p60 — Maximum Likelihood Estimates

```
RECIPE  MLE = the estimate that maximises the probability of the
        training set = just the raw relative frequency
        P(wk|wk-1) = count(wk-1 wk) / count(wk-1)
        its fatal flaw: any unseen bigram = 0 -> whole sentence = 0
```

### p62 — Backoff and Interpolation

```
RECIPE  BACKOFF      use the trigram if you have good evidence,
                     otherwise fall back to bigram, then unigram
        INTERPOLATION always MIX all three with weights that sum to 1
                     P = L1.P(w|w-2,w-1) + L2.P(w|w-1) + L3.P(w)
        interpolation usually works better than backoff
```

### ⭐ p65 — "Perplexity as branching factor"

```
RECIPE  PP(W) = P(w1..wN) ^ (-1/N)     = the Nth root of 1/P
        lower perplexity = better model
        read it as the AVERAGE BRANCHING FACTOR: how many words the
        model thinks could come next

Q ASKED (from the slide) random digits 0-9, model assigns P = 1/10 each
A  PP = (1/10 ^ N) ^ (-1/N) = 10
   i.e. the model is "as confused as" a fair 10-way choice — which is
   exactly right, so 10 is the correct perplexity.
```

### p64 — evaluation

```
RECIPE  EXTRINSIC = plug the model into a real task (speller, MT) and
        measure the task accuracy. Best, but slow.
        INTRINSIC = perplexity on a held-out test set. Fast, approximate.
```

---

# Session 5 — Neural Networks and Neural LM (handout p67–p81)

### p68 — "Final function the unit is computing"

```
RECIPE  one neuron:  z = w.x + b  then  y = activation(z)
        sigmoid(z) = 1 / (1 + e^-z)      range 0..1 ,  sigmoid(0) = 0.5
        ReLU(z)    = max(0, z)           kills negatives, keeps positives
        tanh(z)                          range -1..1
```

### ⭐⭐ p69 — "An example" (w = [0.2,0.3,0.9], b = 0.5) — THE Q1(B) PAGE

```
RECIPE  THE FOUR STEPS, EVERY TIME
        1  z = SUM(wi x xi) + b
        2  h = ReLU(z) = max(z,0)   or   sigmoid(z) = 1/(1+e^-z)
        3  output scores  z_A = (weight_A) x h  ,  z_B = (weight_B) x h
        4  softmax  P(A) = e^zA / (e^zA + e^zB)
        WATCH: negative x negative = POSITIVE in step 1.

Q ASKED (Feb 2026 Q1B, 3m)
  x = [0.4, -0.2] , 1 hidden neuron with ReLU , w = [0.5, -0.5] , b = 0.1
  z(learning) = 2h , z(thought) = 0.5h. Softmax probability of "learning"?

A  1  z = (0.5)(0.4) + (-0.5)(-0.2) + 0.1 = 0.20 + 0.10 + 0.10 = 0.40
   2  h = ReLU(0.4) = 0.4
   3  z(learning) = 2 x 0.4 = 0.8 ; z(thought) = 0.5 x 0.4 = 0.2
   4  e^0.8 = 2.2255 , e^0.2 = 1.2214 , sum = 3.4469
      P(learning) = 2.2255 / 3.4469 = 0.6457  ~ 0.65

Q VARIANT (Mar 2026 Q1B) SIGMOID instead of ReLU
  x = [0.5, 1.0] , w = [0.2, 0.4] , b = -0.5
  z(bright) = 1.5h , z(hot) = 0.5h
A  1  z = (0.2)(0.5) + (0.4)(1.0) - 0.5 = 0.10 + 0.40 - 0.50 = 0.00
   2  h = sigmoid(0) = 1/(1+1) = 0.5        <- sigmoid(0) is ALWAYS 0.5
   3  z(bright) = 0.75 , z(hot) = 0.25
   4  e^0.75 = 2.1170 , e^0.25 = 1.2840 , sum = 3.4010
      P(bright) = 2.1170 / 3.4010 = 0.6225  ~ 0.62

USEFUL e^x VALUES TO PENCIL IN
  e^0.1=1.105  e^0.2=1.221  e^0.25=1.284  e^0.5=1.649
  e^0.75=2.117 e^0.8=2.226  e^1.0=2.718   e^1.5=4.482  e^2=7.389
```

### p71 — "Decision boundaries" / XOR

```
RECIPE  a single perceptron draws ONE straight line
        AND and OR are linearly separable -> one unit is enough
        XOR is NOT -> you need a HIDDEN LAYER
        that is the entire argument for multi-layer networks
```

### ⭐ p73–p74 — two-layer network / multi-layer notation

```
RECIPE  h = g( W.x + b )        hidden layer, g = ReLU or tanh
        z = U.h                 output layer
        y = softmax(z)          for multi-class ; sigmoid for binary
        shape check: W is [hidden x input] , U is [output x hidden]
```

### ⭐ p77 — "Reminder: Multiclass Outputs" (softmax)

```
RECIPE  softmax(z_i) = e^(z_i) / SUM over all j of e^(z_j)
        outputs are all positive and SUM TO 1 -> a probability distribution
        two classes only:  P(A) = e^zA / (e^zA + e^zB)
        FREE CHECK: your two answers must add to 1.0
        (0.6457 + 0.3543 = 1.0 ✓)
```

### p80–p81 — Neural language models

```
RECIPE  n-gram LM: words are ATOMS — "dog" and "cat" share nothing,
        so an unseen context is a dead end
        NEURAL LM: words are EMBEDDINGS — a sentence like one in
        training scores well even with different words
        that generalisation is the whole reason neural LMs beat n-grams
```

---

# Session 6 — POS Tagging and HMMs (handout p89–p108)

### p90–p91 — POS tagging / Penn tagset

```
RECIPE  POS tagging = assign a lexical class to every word
        Penn tags worth knowing:
        DT determiner | NN noun sg | NNS noun pl | NNP proper noun
        JJ adjective  | VB verb base | VBD past | VBG -ing | VBZ -s
        IN preposition/subordinating conj | PRP pronoun | RB adverb
        eg The/DT grand/JJ jury/NN commented/VBD on/IN a/DT number/NN
```

### p96–p97 — Statistical POS tagging

```
RECIPE  we want  argmax over t1..tn of  P(t1..tn | w1..wn)
        Bayes -> = argmax P(w1..wn | t1..tn) x P(t1..tn)
                          \ emission /         \ transition /
        P(words) is the same for every tag sequence, so it DROPS OUT
```

### ⭐ p98 — "Two Kinds of Probabilities" — write the distinction here

```
RECIPE  TRANSITION  P(t_i | t_i-1)   tag -> tag     (the FROM/TO table)
        EMISSION    P(w_i | t_i)     tag -> word    (the tag/word table)
        In the exam you are handed two tables. Label them before you start.
        Rows of BOTH tables sum to 1.
        every cell you ever compute is  (something) x transition x emission
```

### ⭐⭐ p102 — "Viterbi Backpointers" — THE Q2 PAGE

```
RECIPE
  INIT       cell(tag, word1) = P(tag | START) x P(word1 | tag)
  RECURSION  cell(tag, wt) = MAX over prev of [ cell(prev) x P(tag|prev) ]
                             x P(wt | tag)
             and RECORD which prev won  <- the BACKPOINTER
  TERMINATE  take the biggest cell in the LAST column
  BACKTRACE  follow the backpointers left to read the tag sequence

  VITERBI = MAX   (the single best path)
  FORWARD = SUM   (total probability of the observation)
  Same table, one word changes. That word is the whole question.

Q ASKED (Feb 2026 Q2A, 3m)  "a dog barks", tags DT NN VB
  transitions  START: DT .4 NN .4 VB .2 | DT: .2 .7 .1
               NN: .1 .3 .6 | VB: .5 .4 .1
  emissions    DT: a .85 dog .10 barks .05
               NN: a .10 dog .80 barks .10
               VB: a .05 dog .10 barks .85

A  INIT "a"   DT 0.4x0.85 = 0.34   NN 0.4x0.10 = 0.04   VB 0.2x0.05 = 0.01
   "dog"  DT max(.34x.2=.068, .04x.1, .01x.5) = .068 x .10 = 0.0068   bp DT
          NN max(.34x.7=.238, .04x.3, .01x.4) = .238 x .80 = 0.1904   bp DT
          VB max(.34x.1=.034, .04x.6, .01x.1) = .034 x .10 = 0.0034   bp DT
   "barks" DT max(.0068x.2, .1904x.1=.01904, .0034x.5) x .05 = 0.000952 bp NN
           NN max(.0068x.7, .1904x.3=.05712, .0034x.4) x .10 = 0.005712 bp NN
           VB max(.0068x.1, .1904x.6=.11424, .0034x.1) x .85 = 0.097104 bp NN
   BIGGEST last column = VB 0.097104 -> backtrace VB <- NN <- DT
   ANSWER   a/DT   dog/NN   barks/VB
```

### ⭐ p101 — "HMM for Ice Cream" — write the FORWARD version here

```
RECIPE  FORWARD  alpha1(j) = pi(j) x P(o1 | j)
                 alpha_t(j) = [ SUM over i of alpha_t-1(i) x a(i->j) ]
                              x P(o_t | j)
        P(O) = SUM of the final column
        posterior at time t = each alpha divided by that total
        THE ARROW MUST POINT AT the state you are computing: a(i -> j).
        (the Oct 2024 answer key got this backwards — see below)

Q ASKED (Feb 2026 Q2B, 2m)  states V, C, S ; pi = .5 / .3 / .2
  transitions V: .6 .3 .1 | C: .4 .4 .2 | S: .3 .3 .4
  emissions "ah": .8 .1 .1  |  "sh": .1 .7 .2
  O = ("ah","sh"). Posterior over states at t=2, and which is most likely?

A  alpha1  V .5x.8 = 0.40   C .3x.1 = 0.03   S .2x.1 = 0.02
   alpha2  V [.40x.6 + .03x.4 + .02x.3] x .1 = .258 x .1 = 0.0258
           C [.40x.3 + .03x.4 + .02x.3] x .7 = .138 x .7 = 0.0966
           S [.40x.1 + .03x.2 + .02x.4] x .2 = .054 x .2 = 0.0108
   P(O) = 0.0258 + 0.0966 + 0.0108 = 0.1332
   posterior  V .194   C .725   S .081
   MOST LIKELY = C (Consonant). WHY: "sh" has a very high emission
   probability from C (0.7), and enough mass transitions into C.

Q VARIANT (Oct 2024 Q2) 2 states, O = "X Y", pi = .6/.4
   trans S1: .7 .3 | S2: .6 .4    emis X: .6 .4 | Y: .3 .7
A  alpha1  S1 .6x.6 = 0.36   S2 .4x.4 = 0.16
   alpha2  S1 [.36x.7 + .16x.6] x .3 = .348 x .3 = 0.1044
           S2 [.36x.3 + .16x.4] x .7 = .172 x .7 = 0.1204
   P("X Y") = 0.2248
   NOTE: the PRINTED ANSWER KEY IS WRONG here — it swapped a(S2->S1)
   with a(S2->S2). Use this method. Defence sentence: "to reach state j
   you sum over every predecessor i using a(i -> j)."
```

### p103–p104 — Viterbi worked examples on the slides

```
Q ASKED (Oct 2024 Q1, 5m) FORWARD for "cat jumps quickly"
  emissions cat: N .9 Adj .1 | jumps: N .3 V .7 | quickly: V .3 Adj .7
  transitions N->N .5, N->V .5, V->V .7, V->Adj .3
A  no initial probabilities given -> ASSUME 1/2 each and SAY SO
   "cat"     P(N) = 0.5 x 0.9 = 0.45   (V impossible, emission is "-")
   "jumps"   P(V) = 0.45 x 0.5 x 0.7 = 0.1575
   "quickly" P(Adj) = 0.1575 x 0.3 x 0.7 = 0.033075
   P = 0.0331. Only one path survives — every other route hits a zero.

Q ASKED (undated Q1) VITERBI for "run fast", tags Noun/Verb/Adj
  trans N: .4 .3 .3 | V: .1 .8 .1 | Adj: .6 .3 .1
  emis run: N .8 V .2 | fast: N .6 Adj .4
A  same MAX recipe as p102: init, recurse, take the biggest final cell,
   backtrace. Show the backpointer column or you lose the method marks.
```

### p105–p106 — bidirectionality / MEMM

```
RECIPE  HMM is GENERATIVE: models P(words, tags), uses Bayes
        MEMM is DISCRIMINATIVE: models P(tags | words) directly,
        so it can use arbitrary features (suffixes, capitalisation,
        neighbouring words) — HMM cannot
        bidirectional = run extra passes so a tag can see the right context
```

---

# Sessions 7 & 8 — LLMs, Prompting, Transfer Learning (p82–p88, p109–p116)

> Never asked in endsem Q1/Q2. Two notes only, purely as insurance.

### p111–p113 — prompt engineering

```
RECIPE  ZERO-SHOT  instruction only, no examples
        FEW-SHOT   a handful of worked examples in the prompt
                   ("in-context learning" — no weights change)
        CHAIN-OF-THOUGHT  "think step by step" — the model writes its
                   reasoning before the answer; helps on arithmetic/logic
        GENERATED KNOWLEDGE  make the model produce background facts
                   first, then answer using them
```

### p87 / p116 — transfer learning

```
RECIPE  TRANSDUCTIVE  no labelled data in the target domain
                      (domain adaptation)
        INDUCTIVE     labelled target data exists
        PRETRAIN then FINE-TUNE: generic knowledge first, task second
        why: deep learning is data-hungry (>50k items); transfer lets a
        small labelled set work
```

---

# If you only have 20 minutes with a pencil

These five blocks are the entire 10 marks.

| p | Write | The number from the real paper |
|---|---|---|
| **p61** | `P = (c(w1w2)+1) / (c(w1)+V)` | deep→learning: `(1+1)/(2+6)` = **0.25** (V counts `<s>`,`</s>`) |
| **p69** | `z → h → scores → softmax` | `z=0.4`, `h=0.4`, `0.8/0.2` → **0.6457** |
| **p102** | Viterbi = `MAX(prev×trans)×emis` + backpointer | *a dog barks* → **DT NN VB**, final cell 0.097104 |
| **p101** | Forward = `SUM(prev×trans)×emis` | `P(O)=0.1332`, posterior C = **0.725** |
| **p17/p19** | `cos = dot/(\|a\|·\|b\|)`, `TF-IDF = TF·log10(N/df)`, `PPMI = max(0,PMI)` | cos = **0.7746**; TF-IDF = **0.0452** |

---

# Reminders for the exam itself

- **Q1 and Q2 are only 10 of 40 marks.** If you are short on revision time, the
  post-midsem pack (Q3–Q7 = 30 marks) comes first. Do these five pages, then go.
- **Laplace: add `V` to the denominator, not 1.** Adding 1 to the bottom is the
  single most common error on this question.
- **Viterbi = MAX, Forward = SUM.** Write which one you're doing at the top of
  your table — examiners look for it, and it stops you drifting mid-question.
- **State assumptions.** Both the Mar 2026 Laplace question and the Oct 2024
  forward question are under-specified; one sentence of stated assumption
  protects the marks.
- **Softmax sanity check:** your probabilities must sum to 1.
- Full worked solutions: `SOLVED-NUMERICALS`. Theory: `CHEATSHEET`. Extra short
  sums (TF-IDF, cosine, PPMI): `../scheme-drill/SIMPLE-NUMERICALS` §1.
