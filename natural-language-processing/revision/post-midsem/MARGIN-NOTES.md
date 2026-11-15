# Pencil Margin Notes — Post-Midsem

**What this is:** what to pencil into the corner of your printed handout, page by
page. Every entry now has three parts, so you can *recognise* the question, not
just recall a formula:

```
RECIPE    the steps
Q ASKED   the real past-paper question, compressed  (with which paper it came from)
A         the worked answer, short enough to fit in a margin
```

**Which document the page numbers refer to:**
`notes/NLP_Handout_Part2_Sessions_9-end (3).pdf` — 118 pages, Sessions 9 → 15.
Page numbers are **PDF page numbers** (page 1 = title page). Each heading names
the slide title on that page so you can confirm you're on the right sheet.

Sources: Feb 2026 regular, Mar 2026 makeup, Oct 2024 regular, one undated regular
paper — all in `notes/question papers/`.

⭐ = a numerical has actually been set from this page.

---

## First: the inside front cover

```
 Q3  Parsing / Dependency ...... p4, p9, p12, p33
 Q4  Attention (EASIEST) ....... p43, p45, p46, p49
 Q5  WordNet / WSD ............. p66, p67
 Q6  Semantic Web + RAG ........ p82, p85, p97
 Q7  Summarization ............. p112, p118

 ORDER TO ATTEMPT:  Q4 -> Q7 -> Q6 -> Q5 -> Q3

 5 THINGS THAT COST MARKS
 1. Cosine: DIVIDE by both lengths (biggest dot product is a trap)
 2. RAG chunks: round DOWN (floor) — BOTH times
 3. MMR: do the arithmetic, the more relevant one usually LOSES
 4. Top-down parse: SHOW the failure and the pop
 5. Dependency: 1 head/word, nothing into ROOT, all reach ROOT
```

---

# Session 9 — Parsing (handout p1–21)

### ⭐ p4 — "Top down Parsing" (deck slides 16–18)

```
RECIPE   STATE = ((symbols still to find) position)
  1 leftmost is a CATEGORY -> expand; 2 rules fit? take one,
    PUT THE OTHER IN BACKUP
  2 leftmost MATCHES the word -> delete it, position + 1
  3 does NOT match -> KILL the state, POP the backup
  4 nothing left -> parsed
  THE MARKS ARE IN THE FAIL + POP.

Q ASKED (undated paper Q3, 6m; same in Oct 2024)
  "The flying fish jumped out of the water" — using depth-first
  top-down parsing show the steps only until "The flying fish"
  is parsed, one line of explanation per step.
  Grammar: NP -> Det N   |   NP -> Det Adj N

A   Step State              Backup            Why
    1  ((S) 1)                                start
    2  ((NP VP) 1)                            S -> NP VP
    3  ((Det N VP) 1)     ((Det Adj N VP) 1)  took rule 2, SAVED rule 3
    4  ((N VP) 2)         "                   'the' = Det, advance
    5  FAIL                                   'flying' is NOT an N
    6  ((Det Adj N VP) 1)                     POP THE BACKUP
    7  ((Adj N VP) 2)                         'the' = Det
    8  ((N VP) 3)                             'flying' = Adj
    9  ((VP) 4)                               'fish' = N -> DONE
```

### p5–p6 — "Bottom up parsing" / "Chart Parsing" (slides 19–24)

```
RECIPE  chart = store partial matches so work is not redone
        ACTIVE ARC = rule matched so far, dot shows how far
        NP -> ART . N   means ART found, still need an N
        complete arc (dot at the end) -> add that constituent to the chart
```

### ⭐ p9 — "Formal Definition of a PCFG" (slides 35–36)

```
RECIPE  P(tree)     = MULTIPLY P(rule) for EVERY rule in the tree
        P(sentence) = ADD the probabilities of all its trees
        all rules sharing a left-hand side must sum to 1
        higher-probability parse is the one the PCFG selects
```

### ⭐ p12–p13 — "Parsing with a PCFG" / "astronomers saw stars" (slides 47–53)

```
RECIPE  PP-ATTACHMENT: the two parses differ in EXACTLY ONE rule
        VP -> VP PP  = the tool was USED to do the verb (instrumental)
        NP -> NP PP  = the noun HAS the thing (attributive)
        compare just those two probabilities -> the bigger one wins;
        then multiply the whole tree out to show working.

Q ASKED (Mar 2026 makeup Q3, 6m)
  "The chef poked the cake with the fork."
  Given: S->NP VP 1.0 | NP->Det N 0.3 | VP->V NP 0.7 | PP->P NP 1.0
         NP->NP PP 0.4 | VP->VP PP 0.3 | Det->the 1.0
         N->chef 0.4, cake 0.3, fork 0.3 | V->poked 1.0 | P->with 1.0
  (a) draw both parses (b) compute both probabilities (c) which is chosen?

A  Parse 1 VP-attachment (fork = the tool used to poke):
     1.0 x (0.3x0.4) x [0.3 x (0.7x0.3x0.3) x (1.0x0.3x0.3)]
     = 0.00020412
   Parse 2 NP-attachment (the cake has a fork in it):
     1.0 x (0.3x0.4) x [0.7 x (0.4 x (0.3x0.3) x (1.0x0.3x0.3))]
     = 0.00027216
   => PARSE 2 (NP attachment) wins, 0.000272 > 0.000204
   WHY: everything cancels except NP->NP PP (0.4) vs VP->VP PP (0.3)
```

### ⭐ p17–p19 — "Probabilistic CYK" tables (slides 66–77)

```
RECIPE  cell[i,j] = P(rule) x P(left cell) x P(right cell)
        fill the diagonal first (lexical), then work upward
        answer = the S entry in the top-right cell
        needs CNF: every RHS = 2 non-terminals OR 1 terminal

Q ASKED (from the slide itself — "The flight includes a meal")
  Grammar S->NP VP .80 | NP->Det N .30 | VP->V NP .20
          V->includes .05 | Det->the .4 | Det->a .4
          N->meal .01 | N->flight .02

A  NP[0,2] = P(Det->the) x P(N->flight) x P(NP->Det N)
           = 0.4 x 0.02 x 0.30 = 0.0024
   NP[3,5] = 0.4 x 0.01 x 0.30 = 0.0012
   VP[2,5] = P(V) x NP[3,5] x P(VP->V NP)
           = 0.05 x 0.0012 x 0.20 = 0.000012
   S[0,5]  = NP[0,2] x VP[2,5] x 0.80
           = 0.0024 x 0.000012 x 0.80 = 2.304e-8
```

### p16 — "Converting a CFG to CNF" (slides 62–65)

```
RECIPE  3 fixes:  mixed terminal + NT -> dummy NT (Det -> the)
                  unit production      -> splice it through
                  RHS longer than 2    -> chain new non-terminals
```

### p20–p21 — "Evaluating Parsers" (slides 79–83)

```
RECIPE  P  = correct constituents / constituents in MY parse
        R  = correct constituents / constituents in the GOLD parse
        F1 = 2PR / (P+R)
A eg    my parse 8 constituents, gold 10, 6 correct
        P = 6/8 = 0.75 ; R = 6/10 = 0.6
        F1 = 2(0.75)(0.6)/(0.75+0.6) = 0.9/1.35 = 0.667
```

---

# Session 10 — Dependency Parsing (handout p22–38)

*(file says "Session 10", the title slide inside says "Session 11" — same deck)*

### ⭐ p22 — title slide "Dependency Parsing" (slide 2)

```
RECIPE  3 RULES — check EVERY answer against these
  1 every word has EXACTLY ONE head
  2 no cycles
  3 everything reaches ROOT; nothing points INTO ROOT
```

### p23 — "Dependencies Also Resolve Ambiguity" (slides 5–6)

```
Q ASKED (Oct 2024 Q4a, 3m) "Compare the two parsing approaches"

A  CONSTITUENCY            vs   DEPENDENCY
   nested phrases               word -> word arrows
   words only at the leaves     no phrase nodes at all
   fixed word order (English)   FREE word order (Hindi, Czech)
   CKY / chart / PCFG           arc-eager, Chu-Liu-Edmonds
   grammar checking             relation extraction, QA, MT
```

### p24 — "Dependency graph" / "Formal conditions" (slides 10–11)

```
RECIPE  head = the boss word, dependent = hangs off it
        single head + connected + acyclic (+ projective)
Q ASKED (Oct 2024 Q4b, undated Q4b, 3m)
  "Draw the constituency AND dependency parse tree for
   'The desert became very hot'"
A  DEPENDENCY: ROOT->became ; became->desert(nsubj) ; desert->The(det)
               became->hot(xcomp) ; hot->very(advmod)
   CONSTITUENCY: (S (NP (Det The)(N desert))
                    (VP (V became) (AP (Adv very)(Adj hot))))
```

### ⭐ p26 — "Arc eager parsing (Malt parser)" (slides 18–28)

```
RECIPE  config = ( Stack , Buffer , Arcs )
  SHIFT      move the front buffer word onto the stack
  LEFT-ARC   the BUFFER word is the head of the stack top, then pop
  RIGHT-ARC  the STACK top is the head of the buffer word, then push
  REDUCE     pop the stack top — only if it ALREADY has a head
  stop when the buffer is empty

Q ASKED  "Trace arc-eager parsing for 'He likes records'"

A  Step Transition        Stack               Buffer            Arc
   0  init                [ROOT]              [He,likes,records]
   1  SHIFT               [ROOT,He]           [likes,records]
   2  LEFT-ARC(nsubj)     [ROOT]              [likes,records]   likes->He
   3  RIGHT-ARC(root)     [ROOT,likes]        [records]         ROOT->likes
   4  RIGHT-ARC(dobj)     [ROOT,likes,records][]                likes->records
   5  REDUCE              [ROOT,likes]        []
   6  REDUCE              [ROOT]              []
   TRAP: in LEFT-ARC the head is the BUFFER word, not the stack word.
```

### ⭐ p33 — "Chu-Liu-Edmonds algorithm" (slide 46)

```
RECIPE
  STEP 1  each word (not ROOT): keep only its BEST incoming arc
  STEP 2  no cycle -> that IS the answer, stop
  STEP 3  cycle -> for each arc entering the cycle from outside:
          new score = its score - (score of the arc it would replace)
  STEP 4  take the biggest; DELETE the cycle arc pointing at that node,
          KEEP the other cycle arc. Any word still headless takes its best.

Q ASKED (Feb 2026 Q3, 6m)  "He likes records", R=ROOT A=He B=likes C=records
  R->A 4 | R->B 8 | R->C 2 | A->B 3 | B->A 6 | C->A 1 | B->C 7 | C->B 9

A  STEP 1  into A: 4, 6, 1  -> B->A (6)
           into B: 8, 3, 9  -> C->B (9)
           into C: 2, 7     -> B->C (7)
   STEP 2  CYCLE  B -> C -> B
   STEP 3  enter at B: R->B  8 - 9 = -1   (would replace C->B)
           enter at C: R->C  2 - 7 = -5   (would replace B->C)
           from A:     A->B  3 - 9 = -6
           best entry = R->B
   STEP 4  break C->B (the cycle arc into B); keep B->C; A keeps B->A
   ANSWER  ROOT->likes 8 , likes->records 7 , likes->He 6   TOTAL = 21
   check: one head each, nothing into ROOT, all reach ROOT
```

---

# Session 11 — Contextual Embeddings & Attention (handout p39–54)

> **The easiest 6 marks in the paper.** Annotate this session properly.

### ⭐ p39 — session content, "Issues with recurrent models"

```
THEORY (usually 3 of the 6 marks — write these sentences)
  STATIC (Word2Vec) = ONE vector per word forever
    -> CANNOT handle polysemy; river bank and money bank share a vector
  CONTEXTUAL (BERT) = a DIFFERENT vector per sentence, computed
    from the neighbours using ATTENTION
  Why it matters: word sense disambiguation, better semantic
  relationships, better downstream task performance
```

### p40–p41 — "Encoder-Decoder architecture"

```
RECIPE  encoder x1..xn -> h1..hn ; ONE fixed context vector c
        that single c is the BOTTLENECK -> which is WHY attention exists
```

### ⭐ p42–p43 — "Attention !"

```
RECIPE  alpha = softmax(scores)  ->  ALWAYS SUMS TO 1
        output = SUM( alpha_i x v_i )   = weighted average of the values

Q ASKED (Feb 2026 Q4c, 3m)
  "The cat sat". Attention weights for 'cat' = [0.2, 0.5, 0.3] over
  (the, cat, sat). v_the=[1,0], v_cat=[1,1], v_sat=[0,1].
  Compute the contextual embedding of 'cat'.

A  = 0.2[1,0] + 0.5[1,1] + 0.3[0,1]
   = [0.2,0] + [0.5,0.5] + [0,0.3]
   = [0.7, 0.8]
   check: 0.2+0.5+0.3 = 1.0  ✓
```

### ⭐ p45 — Query / Key / Value

```
RECIPE  Q = X.Wq   K = X.Wk   V = X.Wv
        Attention = softmax( Q.K^T / sqrt(d_k) + MASK ) . V
        Q = the word asking; K = the words compared against;
        V = the content actually averaged
        sqrt(d_k) stops big scores saturating softmax
        MASK: future positions -> -infinity -> 0 after softmax
```

### ⭐ p46 — the worked attention-score slide

```
Q ASKED (Oct 2024 Q6b, 4m) — the hardest version
  "Stay Curious", both embeddings = [1 1].
  Wq=[[1,0],[0,2]]  Wk=[[0,2],[1,0]]  Wv=[[2,3],[3,2]]
  d_k = 2, given exp(3.54)=34.31. Show scaling, masking, softmax.

A  1 X = [[1,1],[1,1]]
   2 Q = [[1,2],[1,2]]   K = [[1,2],[1,2]]   V = [[5,5],[5,5]]
   3 Q.K^T = [[5,5],[5,5]]
   4 scale /sqrt2 = 5/1.414 = 3.54  -> [[3.54,3.54],[3.54,3.54]]
   5 mask row 1 -> [[3.54, -inf],[3.54, 3.54]]
   6 softmax row1 = [1.00, 0.00] ; row2 = [0.50, 0.50]
   7 x V -> row1 = [5,5] ; row2 = [5,5]     Output = [[5,5],[5,5]]
   SAY THIS: both inputs are the same vector, so every value vector
   is [5,5] and any weighted average of identical vectors is itself.
```

### p47–p48 — position encoding

```
RECIPE  self-attention is UNORDERED -> add POSITION ENCODING
        without it "dog bites man" = "man bites dog"
```

### ⭐ p49 — "Several attention layers run in parallel"

```
RECIPE  MultiHead = Concat(head_1..head_h) x W_O

Q ASKED (Mar 2026 Q4, 6m)
  head_1 = [0.7, 0.8], head_2 = [0.6, 0.9]
  W_O (4x2) = [0.5,0.3 / 0.2,0.4 / 0.1,0.6 / 0.3,0.2]
  (b) concatenate (c) project through W_O (d) what does each head do?

A  (b) Concat = [0.7, 0.8, 0.6, 0.9]
       2 heads x 2 dims = 4 numbers => W_O must have 4 ROWS (free mark)
   (c) [1x4] x [4x2] = [1x2]
       c1 = .7(.5)+.8(.2)+.6(.1)+.9(.3) = .35+.16+.06+.27 = 0.84
       c2 = .7(.3)+.8(.4)+.6(.6)+.9(.2) = .21+.32+.36+.18 = 1.07
       OUTPUT = [0.84, 1.07]
   (d) head weights [.1,.2,.7] -> peaks on the VERB   = syntactic role
       head weights [.5,.3,.2] -> peaks on 'the'      = grammatical structure
       WHY MANY HEADS: different representation subspaces, different
       relation types, diverse patterns, more capacity, cheap in parallel
```

### p50–p51 — subword tokenization / BPE

```
RECIPE  BPE: start from characters, repeatedly MERGE the most frequent
        adjacent pair, add the merged token to the vocabulary
        eg corpus hug/pug/pun/bun/hugs -> "ug" is the most frequent pair
        -> merge it first. Handles rare and unseen words.
```

### p52–p54 — pretrain / finetune, BERT

```
RECIPE  BERT = encoder-only, bidirectional
        task 1 MLM: mask 15% of tokens and predict them
        task 2 NSP: is sentence B really the next sentence?
        base = 12 layers / 768 dim / 12 heads / 110M params
        pretrain = generic + huge data ; finetune = your task, small data
```

---

# Session 12 — WordNet & WSD (handout p55–68)

### ⭐ p55 — title slide "WSD and WordNet" (slide 2)

```
RECIPE  HOMONYMY = same form, UNRELATED meanings   (bat stick / bat animal)
        POLYSEMY = same word, RELATED meanings     (bank building / company)
        test: are the two meanings historically connected? yes -> polysemy
```

### p56–p57 — "Homonymy" / "Synonyms" (slides 6–12)

```
RECIPE  synonym  same meaning              couch / sofa
        antonym  opposite on ONE feature   hot / cold
        HYPOnym  more specific   car       ("hypO = lOwer")
        HYPERnym more general    vehicle
```

### p58–p59 — "WordNet" (slides 14–19)

```
RECIPE  WordNet = hierarchical lexical database of these relations
        SYNSET = a set of synonyms = one concept / one sense
        GLOSS  = the definition text of a sense
        senses listed MOST FREQUENT FIRST -> sense 1 is the baseline
```

### p62 — "most frequent sense" (slide 31)

```
RECIPE  strongest simple WSD baseline = MOST FREQUENT SENSE
        = WordNet sense number 1
```

### p63–p65 — features / bag of words (slides 34–43)

```
RECIPE  COLLOCATIONAL = words at SPECIFIC positions (+/-2), with POS
        BAG-OF-WORDS  = counts anywhere in the window, position ignored
```

### ⭐ p66 — Naive Bayes / nearest-neighbour WSD (slides 45–48)

```
RECIPE  cos(a,b) = dot(a,b) / ( |a| x |b| )
        |[2,6,2]| = sqrt(4+36+4) = sqrt(44) = 6.633

Q ASKED (Oct 2024 Q6a, 2m)
  Target contextual embedding = [2, 6, 2]. Senses of 'bank':
  N1 financial [1,4,1] | N2 sloping land [2,8,1]
  V1 tip laterally [4,7,3] | V3 do business [3,3,3]   Which sense?

A  sense  dot            |v|            cosine
   N1     2+24+2  = 28   sqrt18 = 4.243  28/(6.633x4.243) = 0.9949  <- WINS
   N2     4+48+2  = 54   sqrt69 = 8.307  54/(6.633x8.307) = 0.9800
   V1     8+42+6  = 56   sqrt74 = 8.602  56/(6.633x8.602) = 0.9814
   V3     6+18+6  = 30   sqrt27 = 5.196  30/(6.633x5.196) = 0.8704
   ANSWER bank_N1, financial institution

   TRAP: N2 has the BIGGEST dot product (54) and is WRONG.
   The dot product favours long vectors. DIVIDE BY BOTH LENGTHS.
```

### ⭐ p67 — "Lesk Algorithm Example" (slides 50–52)

```
RECIPE  1 CONTEXT = content words of the sentence (drop target + stop words)
        2 for each sense take its GLOSS (+ usage examples if given)
        3 OVERLAP = how many words appear in BOTH
        4 highest overlap wins — and write out WHICH words matched
        knowledge-based: needs NO labelled training data

Q ASKED (Feb 2026 Q5, 3m)
  "At night, he picked up the bat to hit the ball."
  Sense 1 bat = flying mammal {animal, flying, mammal, night, wings}
  Sense 2 bat = sports equipment {sports, equipment, hit, ball, cricket}

A  Context = [night, picked, hit, ball]
   Sense 1: night              -> overlap 1
   Sense 2: hit, ball          -> overlap 2
   2 > 1 => SENSE 2, the sports equipment.

Q VARIANT (Oct 2024) "I need to fix the bug in my code." — gloss PLUS example
A  Context = [need, fix, bug, code]
   bug(1) insect + "insecticides can FIX proliferation"      -> 1 (fix)
   bug(2) flaw in a program + "FIXING defects in CODE ..."   -> 2 (fix, code)
   ANSWER bug(2). State your stemming assumption: fix = fixing.
```

---

# Session 13 — Semantic Web / Ontology (handout p69–93)

> Marked as **Application / case study** — often **no arithmetic at all**.
> Annotate definitions and answer templates, not formulas.

### ⭐ p69 — title slide "Semantic Web Ontology" (slide 2)

```
RECIPE  RDF = FACTS.   OWL = RULES.
        if the question says "must / every / at least one / constraint"
        -> the answer is OWL (restrictions + reasoning)

Q ASKED (Mar 2026 Q5B, 2m) "When would you use RDF vs OWL?"
A  RDF handles DATA REPRESENTATION; OWL handles LOGIC and CONSISTENCY
   CHECKING. Storing facts -> RDF triples. Enforcing "every book must
   have an author" -> OWL, because OWL supports restrictions and reasoning.
```

### p79–p81 — ontology definition / languages (slides 42–51)

```
RECIPE  ontology = "a formal, explicit specification of a shared
        conceptualization" (Gruber 93)
        parts: concepts, attributes, relations, axioms, instances
        LADDER: URI -> XML -> RDF -> RDFS -> OWL ; query with SPARQL
        RDFS adds Class, Property, type, subClassOf, domain, range
        OWL adds cardinality, disjointWith, inverseOf, sameAs
```

### ⭐ p82 — "The RDF Data Model" (slides 54–56)

```
RECIPE  TRIPLE = ( subject , predicate , object )
        ANSWER FORMAT: list the triples, THEN list subjects, predicates
        and objects separately — there are marks for both halves.

Q ASKED (Feb 2026 Q6) University system for students, courses, faculty.
  (a) identify entities / properties / values
  (b) write triples for: Anita is enrolled in Data Science; Data Science
      is taught by Dr. Rao; Dr. Rao is a faculty member of the CS Dept.

A  (a) Subjects: Anita, DataScience, DrRao, CSDepartment
       Predicates: enrolledIn, taughtBy, memberOf
       Objects: DataScience, DrRao, CSDepartment
   (b) ( Anita       , enrolledIn , DataScience )
       ( DataScience , taughtBy   , DrRao )
       ( DrRao       , memberOf   , CSDepartment )
   graph: Anita -enrolledIn-> DataScience -taughtBy-> DrRao -memberOf-> CSDept

Q VARIANT (Mar 2026 Q5C, 2m) "Model papers, authors, conferences"
A  RDF (facts):  (Paper1, hasAuthor, Author1) (Paper1, presentedAt, Conf1)
   OWL (schema): classes Paper/Author/Conference; object properties
                 hasAuthor, presentedAt; constraint = every Paper must
                 have AT LEAST ONE Author (owl:minCardinality)
                 -> enables reasoning and consistency checking
```

### ⭐ p83 — "RDFS Examples" (slide 58)

```
RECIPE  subClassOf is TRANSITIVE -> it produces INFERRED facts

Q ASKED (Oct 2024) Given
  LivingThing subClassOf Object | Animal subClassOf LivingThing
  Person subClassOf Animal      | Faculty type Person
  What is the derived inference?

A  Faculty -> Person -> Animal -> LivingThing -> Object
   INFERRED:  Faculty subClassOf Object   (nobody stated it)
   DRAW the chain and LABEL that last arrow "inferred" — that is the mark.
```

### p85–p88 — summary, knowledge graphs (slides 66, 79)

```
RECIPE  RDF = flexible data model | RDFS = simple inference
        OWL = expressive but hard to scale to web-size data
        ONTOLOGY + DATA = KNOWLEDGE GRAPH
        built by named entity recognition + relation extraction
        "London is the capital of England" -> (London, capitalOf, England)
```

---

# Session 14 — RAG (handout p94–105)

### ⭐ p94 — "What LLMs are great at / limitations" (slides 4–5)

```
RECIPE  3 LLM PROBLEMS: knowledge CUTOFF, HALLUCINATION, no access
        to YOUR private documents
        RAG FIX: don't retrain — retrieve documents and paste them
        into the prompt at answer time
```

### p95 — semantic search / pipeline (slides 6–7)

```
RECIPE  query -> embed -> semantic search over chunks -> retrieve top-k
        -> stuff into the prompt -> generate
        semantic search = by MEANING: "laptop repair cost" finds
        "computer hardware pricing"
```

### ⭐ p97 — "Retrieval Augmented Generation", TOP corner (slide 12)

```
RECIPE  fixed      = query tokens + system prompt tokens
        available  = context length - fixed
        chunks     = FLOOR( available / chunk size )   <- ROUND DOWN
        total sent = fixed + chunks x chunk size

Q ASKED (Feb 2026, 6m)
  query 160 | prompt 240 | context 4096 | chunk 480
  (a) max chunks? (b) if only 75% of that is retrieved, total tokens?
  (c) does retrieving fewer chunks improve or degrade quality?

A  (a) fixed = 160+240 = 400 ; available = 4096-400 = 3696
       chunks = floor(3696/480) = floor(7.7) = 7
       check 7x480 = 3360 <= 3696 ✓ , 8x480 = 3840 > 3696 ✗
   (b) 75% of 7 = 5.25 -> floor = 5 chunks
       5 x 480 = 2400 ; total = 400 + 2400 = 2800 tokens
   (c) fewer but MORE RELEVANT chunks reduce noise, improve factual
       grounding and lower hallucination -> quality likely IMPROVES
   BOTH roundings are DOWN. Write the word "floor" — it is a marked step.
```

### ⭐ p97 — same page, BOTTOM corner (slide 11)

```
RECIPE  precision = relevant retrieved / total retrieved
        recall    = relevant retrieved / all relevant that exist
        raising the threshold raises precision, lowers recall

Q ASKED (Mar 2026 Q6, 6m)
  scores 0.92, 0.86, 0.79, 0.71, 0.64, 0.58 ; threshold 0.75
  (a) how many pass? (b) precision if all are relevant?
  (c) precision if one irrelevant chunk is added, and the effect?

A  (a) >= 0.75 : 0.92, 0.86, 0.79  ->  3 chunks
   (b) 3/3 = 1.0
   (c) retrieved 4, relevant 3 -> 3/4 = 0.75
       lower precision = more irrelevant text in the context = more
       noise = higher hallucination risk = worse generation quality
```

### p98–p104 — KG vs vector DB, multimodal, agentic (slides 15–40)

```
RECIPE  vector DB = fuzzy similarity, fast, unstructured text
        KG        = multi-hop and aggregate questions, explainable
                    ("board meetings where 2+ members abstained")
        Graph RAG = retrieve over the KG instead of flat chunks
        multimodal RAG = text + images + tables + audio, one shared
                    embedding space, hybrid retrieval
        agentic RAG = LLM plans: decompose query -> several retrievals
                    -> tool calls -> iterate -> cite
                    parts: agent, memory/scratchpad, retrievers, planner
```

---

# Session 15 — Text Summarization (handout p106–118)

### ⭐ p106 — "Session Content" (slide 3)

```
RECIPE  TYPE DECISION TREE
        1 doc, headline/abstract           -> single-document, GENERIC
        many docs on the SAME event        -> MULTI-DOCUMENT (kill redundancy)
        "summarize only the parts about X" -> QUERY-FOCUSED
        copies sentences -> EXTRACTIVE ; new words -> ABSTRACTIVE

Q ASKED (Mar 2026 Q7, 6m) Classify three scenarios and justify.
  1 journalist uploads ONE climate report, wants a headline + abstract
  2 analyst gives 15 articles from different sources on the same summit
  3 researcher asks "summarize the sections on economic impact"

A  1 SINGLE-DOCUMENT, GENERIC — one document, overall content, no query
   2 MULTI-DOCUMENT — same event across sources, remove redundancy
                      and resolve overlaps
   3 QUERY-FOCUSED — tailored to a specific information need, a form
                      of complex question answering
   Why one approach can't do all three: generic ignores user intent;
   query-focused needs an explicit need; multi-document must manage
   redundancy and contradictions. Different input structure, user
   intent and output requirements.
```

### ⭐ p109 — "Summarization Three Stages" (slide 14)

```
RECIPE  1 CONTENT SELECTION    pick which sentences to use
        2 INFORMATION ORDERING what order — chronological / coherence / topical
        3 SENTENCE REALIZATION tidy the wording, fix "he", fix connectives
```

### p110–p111 — frequency, tf-idf, graph methods (slides 16–24)

```
RECIPE  word probability p(w) = count(w) / N
        sentence weight = AVERAGE p(w) over its content words
        pick the highest-weight sentence
        tf-idf = tf x log( N / n_k )
        graph method (TextRank): nodes = sentences, edges = cosine
        similarity, rank by centrality

A eg    N = 100 words. "AI improves care": p(AI)=.05 p(improves)=.01
        p(care)=.03  ->  weight = (.05+.01+.03)/3 = 0.03
```

### ⭐ p112–p113 — "MMR: Choosing informative sentences" (slides 27–28)

```
RECIPE  MMR(s) = L x sim(s,q)   -   (1-L) x sim(s,S)
                 \ relevance /       \  redundancy  /
        pick the HIGHEST, add it to S, repeat

Q ASKED (Feb 2026 Q7, 6m)
  query: government regulations on AI in healthcare
  already selected S = {"Governments are introducing regulations to
  ensure safe use of AI in medical diagnosis."}
  S1 "New AI laws focus on patient data privacy and ethical use..."
        sim(q)=0.80  sim(S)=0.30
  S2 "Several countries have passed laws regulating AI-based medical
      diagnosis systems."   sim(q)=0.88  sim(S)=0.70
  lambda = 0.6. Compute both, choose, justify.

A  MMR(S1) = 0.6(0.80) - 0.4(0.30) = 0.48 - 0.12 = 0.36   <- SELECTED
   MMR(S2) = 0.6(0.88) - 0.4(0.70) = 0.528 - 0.28 = 0.248
   JUSTIFY: although S2 is MORE RELEVANT (0.88 vs 0.80) it is highly
   similar to the already-selected sentence (0.70 vs 0.30), making it
   REDUNDANT — it repeats what the summary already says. S1 adds NEW
   COMPLEMENTARY information (ethics, data privacy), so it scores higher.

   LAMBDA: L -> 1 means care only about relevance (summary repeats itself);
   L -> 0 means care only about novelty (summary drifts off topic).
   With the same numbers, L=0.7 picks the novel one; L=0.9 flips it back
   to the relevant one. DO THE ARITHMETIC, never guess.
```

### p116–p117 — realization, neural summarization (slides 45–52)

```
RECIPE  realization fixes pronouns (he -> Pinochet) and discourse
        connectives (however, moreover, subsequently)
        extractive  = SELECT existing sentences
        abstractive = GENERATE new text, seq2seq/transformer (BART, T5, PEGASUS)
```

### ⭐ p118 — "ROUGE" / "ROUGE-2" (slides 53–55)

```
RECIPE  ROUGE-2 = reference bigrams that ALSO appear in the system summary
                  --------------------------------------------------------
                  total bigrams across ALL reference summaries
        recall-oriented -> the denominator is the HUMAN summaries
        bigrams in a sentence = (number of words) - 1
        ROUGE-1 = unigrams , ROUGE-L = longest common subsequence

Q ASKED (from the slide) Q "What is water spinach?"
  H1 "Water spinach is a green leafy vegetable grown in the tropics."
  H2 "Water spinach is a semi-aquatic tropical plant grown as a vegetable."
  H3 "Water spinach is a commonly eaten leaf vegetable of Asia."
  System X "Water spinach is a leaf vegetable commonly eaten in
            tropical areas of Asia."

A  reference   bigrams   matched
   H1          10        3   (water spinach, spinach is, is a)
   H2          10        3   (same three)
   H3           9        6   (+ commonly eaten, leaf vegetable, of asia)
   TOTAL       29        12
   ROUGE-2 = 12 / 29 = 0.4138 = 41.4%
   comment: H3 is phrased closest to the system output, so it supplies
   half the matches on its own.
```

---

# If you only have 20 minutes with a pencil

Write these six blocks and stop. They cover Q4, Q7, Q6, Q5 and half of Q3 —
about **26 of the 30 post-midsem marks**.

| p | Formula | The number to remember from the real paper |
|---|---|---|
| **p43** | `out = Σ αᵢ·vᵢ` | `[0.2,0.5,0.3]` over `[1,0],[1,1],[0,1]` → **[0.7, 0.8]** |
| **p112** | `MMR = λ·rel − (1−λ)·red` | λ=0.6: **0.36 vs 0.248 → S1**, the *less* relevant one |
| **p97** | `chunks = FLOOR(avail/chunk)` | 4096−400=3696, /480 = 7.7 → **7**; 75% of 7 → **5**, total **2800** |
| **p66** | `cos = dot/(\|a\|·\|b\|)` | `[2,6,2]` → **N1 wins at 0.9949**, though N2 has the bigger dot (54) |
| **p82** | triple = (S, P, O) | `(Anita, enrolledIn, DataScience)`; RDF facts / OWL rules |
| **p33** | CLE | cycle B↔C → `8−9`, `2−7` → enter at B → **21 total** |

---

# Reminders for the exam itself

- **Attempt order: Q4 → Q7 → Q6 → Q5 → Q3.** Q3 eats time; do it last.
- **Show every intermediate line.** Open book means the marks are for method.
- If a question says *"and/or theory"* and the numbers look nasty, the theory
  half is the safer 3 marks — write it fully before attacking the arithmetic.
- Full worked solutions: `SOLVED-NUMERICALS`. Fresh mock sets: `PRACTICE-PAPER`.
