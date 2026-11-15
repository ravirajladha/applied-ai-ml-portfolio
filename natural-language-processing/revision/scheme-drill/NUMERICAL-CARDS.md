# NLP Numerical Cards — every sum in the course, one card each

**No theory. No prose.** One card per type of numerical that can be set.
Each card is the same four lines:

```
WHEN YOU SEE   how to recognise the question
FORMULA        the one line you must remember
WORKED         a real past-paper example, done
TRAP           what loses the mark
```

18 cards. Read one, cover the WORKED half, redo it on scrap paper, move on.

| Where it appears | Cards |
|---|---|
| **Q1** — 5 marks | 1 Laplace · 2 TF-IDF · 3 Cosine · 4 PPMI · 5 Forward pass · 6 Perplexity |
| **Q2** — 5 marks | 7 Viterbi · 8 Forward algorithm |
| **Q3** — 6 marks | 9 PCFG · 10 CKY cell · 11 Chu-Liu-Edmonds · 12 Arc-eager |
| **Q4** — 6 marks | 13 Attention · 14 Multi-head |
| **Q5** — 6 marks | 15 Lesk · (cosine → card 3) |
| **Q6** — 6 marks | 16 Token budget · 17 Precision |
| **Q7** — 6 marks | 18 MMR · 19 ROUGE-2 |

---

# 1 · Laplace smoothed bigram

```
WHEN YOU SEE   a tiny corpus of 3 sentences and "probability of w2 after w1",
               with V defined for you

FORMULA        P = ( count(w1 w2) + 1 ) / ( count(w1) + V )

WORKED   <s> deep learning </s> / <s> machine learning </s> / <s> deep thought </s>
         V = {<s>, </s>, deep, learning, machine, thought} = 6
         count(deep learning) = 1 , count(deep) = 2
         P = (1+1)/(2+6) = 2/8 = 0.25          [unsmoothed MLE = 1/2 = 0.5]

TRAP     add V to the bottom, NOT 1.  Count <s> and </s> in V when told to.
```

---

# 2 · TF-IDF

```
WHEN YOU SEE   "N documents, the word appears in df of them, k times in this one"

FORMULA        TF-IDF = TF x IDF        IDF = log10( N / df )
               TF = (times in this doc) / (length of this doc)

WORKED   4 docs, "cloud" in 2 of them, 3 times in D1, D1 is 20 words
         TF  = 3/20 = 0.15
         IDF = log10(4/2) = log10(2) = 0.301
         TF-IDF = 0.15 x 0.301 = 0.0452

TRAP     a word in ALL documents gives log10(1) = 0, so TF-IDF = 0.
         That is correct, not an error — the word cannot discriminate.
```

---

# 3 · Cosine similarity

```
WHEN YOU SEE   two vectors and "how similar" — or several sense vectors
               and "which sense" (that is Q5, same sum)

FORMULA        cos(a,b) = ( a . b ) / ( |a| x |b| )
               |[2,0,1]| = sqrt(4+0+1) = sqrt(5) = 2.236

WORKED   A = [2,0,1] , B = [1,1,1]
         dot = 2 + 0 + 1 = 3
         |A| = sqrt5 = 2.236 , |B| = sqrt3 = 1.732
         cos = 3 / (2.236 x 1.732) = 3/3.873 = 0.7746

WORKED (Q5 version, Oct 2024)  target [2,6,2] vs senses of "bank"
         N1 [1,4,1]  dot 28  |v| 4.243  ->  28/(6.633x4.243) = 0.9949  WINS
         N2 [2,8,1]  dot 54  |v| 8.307  ->  54/(6.633x8.307) = 0.9800
         V1 [4,7,3]  dot 56  |v| 8.602  ->  0.9814
         V3 [3,3,3]  dot 30  |v| 5.196  ->  0.8704

TRAP     N2 has the BIGGEST dot product and is WRONG.
         Long vectors win the dot product. DIVIDE BY BOTH LENGTHS.
```

---

# 4 · PPMI

```
WHEN YOU SEE   a co-occurrence table with row and column totals

FORMULA        PMI  = log2( P(w,c) / ( P(w) x P(c) ) )
               PPMI = max( 0 , PMI )

WORKED   total 60. cherry row 10, digital row 50, computer column 32
         digital & computer:
           P(w,c)=30/60=.500  P(w)=50/60=.8333  P(c)=32/60=.5333
           PMI = log2(.500/.4444) = log2(1.125) = 0.170  -> PPMI 0.170
         cherry & computer:
           P(w,c)=2/60=.0333  P(w)=10/60=.1667  P(c)=.5333
           PMI = log2(.0333/.0889) = log2(0.375) = -1.415 -> PPMI 0

TRAP     negative PMI clips to ZERO, it does not stay negative.
         That clipping is the entire reason for the "P" in PPMI.
```

---

# 5 · Neural forward pass + softmax

```
WHEN YOU SEE   "input x, weights w, bias b, hidden neuron with ReLU/sigmoid,
               output scores, find the softmax probability"

FORMULA        1  z = SUM(wi.xi) + b
               2  h = ReLU(z) = max(z,0)   OR   sigmoid(z) = 1/(1+e^-z)
               3  z_A = (coef A) x h  ,  z_B = (coef B) x h
               4  P(A) = e^zA / ( e^zA + e^zB )

WORKED (Feb 2026)  x=[0.4,-0.2] w=[0.5,-0.5] b=0.1 ReLU
                   z(learning)=2h , z(thought)=0.5h
         z = (0.5)(0.4) + (-0.5)(-0.2) + 0.1 = 0.20 + 0.10 + 0.10 = 0.40
         h = ReLU(0.4) = 0.4
         scores 0.8 and 0.2
         e^0.8 = 2.2255 , e^0.2 = 1.2214 , sum 3.4469
         P(learning) = 2.2255/3.4469 = 0.6457

WORKED (Mar 2026, sigmoid)  x=[0.5,1.0] w=[0.2,0.4] b=-0.5
         z = 0.10 + 0.40 - 0.50 = 0.00
         h = sigmoid(0) = 0.5                    <- sigmoid(0) is ALWAYS 0.5
         scores 0.75 and 0.25 -> e^0.75=2.1170 , e^0.25=1.2840
         P(bright) = 2.1170/3.4010 = 0.6225

TRAP     negative x negative = POSITIVE in step 1.
         Check your two probabilities sum to 1.

e^x TABLE   0.1=1.105  0.2=1.221  0.25=1.284  0.5=1.649  0.75=2.117
            0.8=2.226  1.0=2.718  1.5=4.482   2.0=7.389
```

---

# 6 · Perplexity

```
WHEN YOU SEE   "perplexity of this sentence / this model"

FORMULA        PP(W) = P(w1..wN) ^ (-1/N)      = the Nth root of 1/P
               lower is better; read it as "average branching factor"

WORKED   random digits 0-9, model gives P = 1/10 to each of N digits
         PP = ( (1/10)^N ) ^ (-1/N) = 10
         i.e. as confused as a fair 10-way choice — correct.

TRAP     the exponent is NEGATIVE one over N. Forgetting the minus
         inverts the answer.
```

---

# 7 · Viterbi

```
WHEN YOU SEE   two tables (tag->tag, tag->word) and "most likely TAG SEQUENCE"

FORMULA        INIT      cell = P(tag|START) x P(word1|tag)
               RECURSE   cell = MAX over prev [ prev x P(tag|prev) ] x P(word|tag)
                         + record the winning prev  (BACKPOINTER)
               END       biggest cell in the last column, follow backpointers

WORKED (Feb 2026)  "a dog barks", tags DT NN VB
         INIT  DT .4x.85=0.34   NN .4x.10=0.04   VB .2x.05=0.01
         dog   DT max(.34x.2=.068 ...) x .10 = 0.0068     bp DT
               NN max(.34x.7=.238 ...) x .80 = 0.1904     bp DT
               VB max(.34x.1=.034 ...) x .10 = 0.0034     bp DT
         barks DT (.1904x.1=.01904) x .05 = 0.000952      bp NN
               NN (.1904x.3=.05712) x .10 = 0.005712      bp NN
               VB (.1904x.6=.11424) x .85 = 0.097104      bp NN  <- biggest
         backtrace VB <- NN <- DT
         ANSWER   a/DT  dog/NN  barks/VB

TRAP     VITERBI = MAX. Write "MAX" at the top of your table.
         No backpointer column = no method marks.
```

---

# 8 · Forward algorithm

```
WHEN YOU SEE   same two tables but "probability of the OBSERVATION SEQUENCE"
               or "posterior over states at time t"

FORMULA        alpha1(j)   = pi(j) x P(o1|j)
               alpha_t(j)  = [ SUM over i of alpha_t-1(i) x a(i->j) ] x P(ot|j)
               P(O) = sum of the last column
               posterior = each alpha / P(O)

WORKED (Feb 2026)  states V,C,S  pi = .5/.3/.2  O = ("ah","sh")
         alpha1  V .5x.8=0.40   C .3x.1=0.03   S .2x.1=0.02
         alpha2  V [.40x.6 + .03x.4 + .02x.3] x .1 = .258x.1 = 0.0258
                 C [.40x.3 + .03x.4 + .02x.3] x .7 = .138x.7 = 0.0966
                 S [.40x.1 + .03x.2 + .02x.4] x .2 = .054x.2 = 0.0108
         P(O) = 0.1332
         posterior  V 0.194   C 0.725   S 0.081   ->  most likely C
         why: "sh" emits from C with 0.7, the highest

TRAP     FORWARD = SUM (Viterbi = MAX). Same table, one word different.
         The arrow must POINT AT the state you are computing: a(i -> j).
         (The Oct 2024 answer key got this backwards.)
```

---

# 9 · PCFG parse probability

```
WHEN YOU SEE   a rule table with probabilities and a PP-attachment sentence
               ("... with the fork", "... with a telescope")

FORMULA        P(tree) = MULTIPLY P(rule) for every rule used
                         higher probability wins

WORKED (Mar 2026)  "The chef poked the cake with the fork"
         VP attachment (fork = tool used):  uses VP -> VP PP [0.3]
           1.0 x (0.3x0.4) x [0.3 x (0.7x0.3x0.3) x (1.0x0.3x0.3)]
           = 0.00020412
         NP attachment (cake has a fork):   uses NP -> NP PP [0.4]
           1.0 x (0.3x0.4) x [0.7 x (0.4 x (0.3x0.3) x (1.0x0.3x0.3))]
           = 0.00027216
         NP attachment WINS

TRAP     the two parses differ in EXACTLY ONE rule. Compare 0.4 vs 0.3
         first, then multiply out to show working.
```

---

# 10 · Probabilistic CKY cell

```
WHEN YOU SEE   a grid/chart to fill for a sentence

FORMULA        cell[i,j] = P(rule) x P(left cell) x P(right cell)
               diagonal first (lexical), then upward; answer = S top-right
               grammar must be CNF: RHS = 2 non-terminals OR 1 terminal

WORKED   "The flight includes a meal"
         S->NP VP .80 | NP->Det N .30 | VP->V NP .20
         Det->the .4 | N->flight .02 | V->includes .05 | Det->a .4 | N->meal .01
         NP[0,2] = 0.4 x 0.02 x 0.30 = 0.0024
         NP[3,5] = 0.4 x 0.01 x 0.30 = 0.0012
         VP[2,5] = 0.05 x 0.0012 x 0.20 = 0.000012
         S[0,5]  = 0.0024 x 0.000012 x 0.80 = 2.304e-8

TRAP     three numbers multiply per cell, not two. The rule probability
         is one of them.
```

---

# 11 · Chu-Liu-Edmonds (dependency MST)

```
WHEN YOU SEE   a table of arc scores head->dependent, "find the best tree"

FORMULA        1  each word: keep only its BEST incoming arc
               2  no cycle -> done
               3  cycle -> for each arc entering it from outside:
                  new = its score - (score of the arc it replaces)
               4  take the biggest; delete the cycle arc into that node,
                  keep the other

WORKED (Feb 2026)  R=ROOT A=He B=likes C=records
         R->A 4 | R->B 8 | R->C 2 | A->B 3 | B->A 6 | C->A 1 | B->C 7 | C->B 9
         1  into A: best B->A (6) | into B: best C->B (9) | into C: best B->C (7)
         2  CYCLE B -> C -> B
         3  enter at B: 8 - 9 = -1     enter at C: 2 - 7 = -5
            from A:     3 - 9 = -6     ->  best is R->B
         4  break C->B, keep B->C, A keeps B->A
         ANSWER  ROOT->likes 8 , likes->records 7 , likes->He 6   TOTAL 21

TRAP     check the 3 rules: one head per word, nothing into ROOT,
         every word reaches ROOT.
```

---

# 12 · Arc-eager transition trace

```
WHEN YOU SEE   "trace the transitions" / stack-buffer table

FORMULA        config = ( Stack , Buffer , Arcs )
               SHIFT      buffer word -> stack
               LEFT-ARC   BUFFER word is the head of the stack top, then pop
               RIGHT-ARC  STACK top is the head of the buffer word, then push
               REDUCE     pop the stack top — only if it already has a head

WORKED   "He likes records"
         0 init             [ROOT]               [He,likes,records]
         1 SHIFT            [ROOT,He]            [likes,records]
         2 LEFT-ARC nsubj   [ROOT]               [likes,records]   likes->He
         3 RIGHT-ARC root   [ROOT,likes]         [records]         ROOT->likes
         4 RIGHT-ARC dobj   [ROOT,likes,records] []                likes->records
         5 REDUCE           [ROOT,likes]         []
         6 REDUCE           [ROOT]               []

TRAP     in LEFT-ARC the head is the BUFFER word, not the stack word.
```

---

# 13 · Attention — contextual embedding

```
WHEN YOU SEE   attention weights alpha and value vectors v

FORMULA        output = SUM of ( alpha_i x v_i )        (a weighted average)
               the alphas ALWAYS sum to 1

WORKED (Feb 2026)  "The cat sat", alpha = [0.2, 0.5, 0.3]
                   v_the=[1,0]  v_cat=[1,1]  v_sat=[0,1]
         = 0.2[1,0] + 0.5[1,1] + 0.3[0,1]
         = [0.2,0] + [0.5,0.5] + [0,0.3]
         = [0.7, 0.8]
         check 0.2+0.5+0.3 = 1.0

FULL VERSION (Oct 2024, if Q,K,V are given)
         Q = X.Wq , K = X.Wk , V = X.Wv
         Attention = softmax( Q.K^T / sqrt(d_k) + MASK ) . V
         mask future positions to -infinity -> 0 after softmax

TRAP     none, really. Just check the alphas sum to 1. Easiest 3 marks
         in the paper.
```

---

# 14 · Multi-head concat x W_O

```
WHEN YOU SEE   two head outputs and a W_O matrix

FORMULA        MultiHead = Concat(head1, head2, ...) x W_O

WORKED (Mar 2026)  head1 = [0.7,0.8] , head2 = [0.6,0.9]
                   W_O = [.5 .3 / .2 .4 / .1 .6 / .3 .2]
         Concat = [0.7, 0.8, 0.6, 0.9]        4 numbers => W_O has 4 ROWS
         col1 = .7(.5) + .8(.2) + .6(.1) + .9(.3) = .35+.16+.06+.27 = 0.84
         col2 = .7(.3) + .8(.4) + .6(.6) + .9(.2) = .21+.32+.36+.18 = 1.07
         OUTPUT = [0.84, 1.07]

TRAP     state the shape check ([1x4] x [4x2] = [1x2]) — it is a free mark.
```

---

# 15 · Lesk overlap

```
WHEN YOU SEE   a sentence and two sense definitions, "which sense?"

FORMULA        1 context = content words of the sentence
                 (drop the target word and stop words)
               2 for each sense take its gloss (+ examples if given)
               3 overlap = how many words appear in BOTH
               4 highest overlap wins

WORKED (Feb 2026)  "At night, he picked up the bat to hit the ball."
         context = [night, picked, hit, ball]
         sense 1 mammal  {animal, flying, mammal, night, wings}  -> 1 (night)
         sense 2 sports  {sports, equipment, hit, ball, cricket} -> 2 (hit, ball)
         ANSWER sense 2

WORKED (Oct 2024)  "I need to fix the bug in my code."
         context = [need, fix, bug, code]
         bug(1) insect + "insecticides can FIX proliferation"    -> 1
         bug(2) program flaw + "FIXING defects in CODE ..."      -> 2
         ANSWER bug(2). State your stemming assumption: fix = fixing.

TRAP     write out WHICH words matched, not just the count.
```

---

# 16 · RAG token budget

```
WHEN YOU SEE   query tokens, system prompt tokens, context length, chunk size

FORMULA        fixed      = query + system prompt
               available  = context length - fixed
               chunks     = FLOOR( available / chunk size )
               total sent = fixed + chunks x chunk size

WORKED (Feb 2026)  query 160 , prompt 240 , context 4096 , chunk 480
         fixed = 400 , available = 4096 - 400 = 3696
         chunks = floor(3696/480) = floor(7.7) = 7
           check 7x480 = 3360 <= 3696 ok ; 8x480 = 3840 too big
         if only 75% used: 75% of 7 = 5.25 -> floor = 5
           5 x 480 = 2400 ; total = 400 + 2400 = 2800 tokens

TRAP     round DOWN both times. Write the word "floor" — it is a marked step.
```

---

# 17 · Retrieval precision

```
WHEN YOU SEE   a list of similarity scores and a threshold

FORMULA        precision = relevant retrieved / total retrieved
               recall    = relevant retrieved / all relevant that exist

WORKED (Mar 2026)  scores 0.92, 0.86, 0.79, 0.71, 0.64, 0.58 ; threshold 0.75
         pass: 0.92, 0.86, 0.79  ->  3 chunks
         all relevant:            3/3 = 1.0
         one irrelevant added:    3/4 = 0.75

         THE SENTENCE THEY WANT: lower precision means more irrelevant text
         in the context, which increases noise and raises the risk of
         hallucination, degrading generation quality.

TRAP     ">= threshold" includes the boundary. 0.79 passes, 0.71 does not.
```

---

# 18 · MMR

```
WHEN YOU SEE   sim(s,q) and sim(s,S) for two sentences, and a lambda

FORMULA        MMR = L x sim(s,q)  -  (1-L) x sim(s,S)
                     relevance          redundancy
               pick the HIGHEST

WORKED (Feb 2026)  L = 0.6
         S1  rel 0.80  red 0.30  ->  0.6(0.80) - 0.4(0.30) = 0.48 - 0.12 = 0.36
         S2  rel 0.88  red 0.70  ->  0.6(0.88) - 0.4(0.70) = 0.528 - 0.28 = 0.248
         S1 WINS

         JUSTIFY: although S2 is more relevant, it is highly similar to the
         already-selected sentence and therefore redundant; S1 adds new
         complementary information, giving a higher MMR score.

TRAP     the MORE relevant sentence usually LOSES — that is the point of the
         formula. But if L is 0.8+, relevance dominates and it wins.
         DO THE ARITHMETIC, never guess.
```

---

# 19 · ROUGE-2

```
WHEN YOU SEE   human reference summaries and a system summary

FORMULA        ROUGE-2 = reference bigrams that also appear in the system
                         -------------------------------------------------
                         total bigrams across ALL references
               bigrams in a sentence = (number of words) - 1

WORKED   "What is water spinach?", 3 human references
         H1  10 bigrams , 3 matched
         H2  10 bigrams , 3 matched
         H3   9 bigrams , 6 matched
         total 29 , matched 12
         ROUGE-2 = 12/29 = 0.4138 = 41.4%

TRAP     recall-oriented — the DENOMINATOR is the human summaries,
         not the system summary.
```

---

# The whole paper on one card

```
Q1  Laplace  P = (c(w1w2)+1)/(c(w1)+V)        add V, not 1
    Fwd pass z -> h -> scores -> softmax      neg x neg = pos
Q2  VITERBI = MAX x emission + backpointer
    FORWARD = SUM x emission , then divide by P(O) for the posterior
Q3  PCFG  multiply every rule; the parses differ in ONE rule
    CLE   best incoming arc -> cycle? -> score minus replaced score
Q4  out = SUM(alpha_i x v_i)                  alphas sum to 1
    multi-head: concat then x W_O
Q5  Lesk  count shared words
    cosine  DIVIDE BY BOTH LENGTHS
Q6  chunks = FLOOR(available / chunk)         round DOWN twice
    precision = relevant / retrieved
Q7  MMR = L.rel - (1-L).red                   the relevant one usually loses
    ROUGE-2 = matched bigrams / reference bigrams

ATTEMPT ORDER   Q4 -> Q7 -> Q6 -> Q5 -> Q1 -> Q2 -> Q3
```
