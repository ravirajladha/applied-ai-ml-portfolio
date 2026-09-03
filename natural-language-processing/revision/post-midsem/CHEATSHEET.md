# NLP Post-Midsem — Chapter-wise Cheat Sheet
**Only what you need to answer the exam questions. Nothing else.**

You have not done the theory. That is fine — there is far less of it than the
slides suggest. Each chapter below is **one page**: what it's for, the words you
must know, the recipe, one tiny worked example, and the trap.

Read a chapter (5 min) → do that question in `PRACTICE-PAPER` → come back if stuck.

| Ch | Session | Exam Q | Page |
|---|---|---|---|
| 9 | Parsing | Q3 | [↓](#ch-9--parsing) |
| 10 | Dependency Parsing | Q3 | [↓](#ch-10--dependency-parsing) |
| 11 | Contextual Embeddings & Attention | Q4 | [↓](#ch-11--contextual-embeddings--attention) |
| 12 | WordNet & Word Sense Disambiguation | Q5 | [↓](#ch-12--wordnet--word-sense-disambiguation) |
| 13 | Semantic Web (RDF / OWL) | Q6 | [↓](#ch-13--semantic-web-rdf--owl) |
| 14 | RAG | Q6 | [↓](#ch-14--rag) |
| 15 | Text Summarization | Q7 | [↓](#ch-15--text-summarization) |

---

# Ch 9 — Parsing

### What it's for
**Parsing = working out the grammatical structure of a sentence.** Like the
sentence diagrams from school: which words group together, and what role each
group plays.

### Words you must know
| Word | Means |
|---|---|
| **Grammar (CFG)** | A list of rules like `S → NP VP` — "a Sentence is a Noun Phrase followed by a Verb Phrase" |
| **Non-terminal** | A category: `S`, `NP`, `VP`, `PP`, `Det`, `N`, `V` |
| **Terminal** | An actual word: *the*, *dog* |
| **NP / VP / PP** | Noun Phrase (*the dog*) / Verb Phrase (*chased the cat*) / Prepositional Phrase (*with a fork*) |
| **Det** | Determiner — *the*, *a* |
| **Top-down** | Start at `S`, expand rules downward until you hit the words |
| **Backtracking** | You guessed the wrong rule, so you go back and try the other one |
| **PCFG** | A grammar where every rule carries a **probability** |
| **Ambiguity** | The same sentence has **two valid structures** — the thing PCFGs resolve |

### The exam asks one of two things

---

**(A) Top-down parse table.** *"Parse until 'The small dog' using depth-first top-down parsing."*

A **state** is `((symbols still to find) position)`. Position = which word you're up to.

```
1. Leftmost symbol is a CATEGORY  -> replace it with a rule's right-hand side.
                                     Two rules fit? Take one, PUT THE OTHER IN "BACKUP".
2. Leftmost symbol MATCHES the current word -> delete it, position + 1.
3. It does NOT match -> THROW AWAY this state, POP the backup.   <- the marks are here
4. Nothing left to find -> done.
```

Mini example — grammar `NP → Det AP N` (try first), `NP → Det N`; *"The small dog"*:

| Step | State | Backup | Why |
|---|---|---|---|
| 1 | `((NP VP) 1)` | | start |
| 2 | `((Det AP N VP) 1)` | `((Det N VP) 1)` | took rule 1, saved rule 2 |
| 3 | `((AP N VP) 2)` | `((Det N VP) 1)` | *The* is a Det ✓ |
| 4 | `((Adv Adj N VP) 2)` | +`((Adj N VP) 2)` | expanded AP |
| 5 | **FAIL** | | *small* is not an Adv ✗ |
| 6 | `((Adj N VP) 2)` | | **popped the backup** |
| 7 | `((N VP) 3)` | | *small* is an Adj ✓ |
| 8 | `((VP) 4)` | | *dog* is an N ✓ — parsed |

---

**(B) PCFG probability.** *"Two parses — compute both probabilities, which wins?"*

```
P(tree) = MULTIPLY the probability of EVERY rule used in that tree.
Higher probability wins.
```

The classic case: *"saw the girl **with the telescope**"* — did he *use* the
telescope (PP attaches to the **verb**) or did *she have* it (PP attaches to the
**noun**)?

```
VP attachment: uses rule  VP -> VP PP   [0.4]
NP attachment: uses rule  NP -> NP PP   [0.3]

Everything else in the two trees is IDENTICAL, so 0.4 beats 0.3
-> VP attachment wins.
```

> **Shortcut:** the two parses differ in **exactly one rule**. Find it, compare
> those two numbers, and you know the answer before multiplying. Then multiply
> anyway to show working.

### Trap
In (A), **you must show the failure and the pop.** A clean table with no
backtracking hasn't demonstrated the algorithm and loses most of the marks.

---
---

# Ch 10 — Dependency Parsing

### What it's for
The *other* way to show sentence structure. Instead of grouping words into
phrases, you **draw an arrow from each word to the word it depends on**.

```
     ROOT ──► chase ──► Dogs      "Dogs" depends on "chase"
                └────► cats       "cats" depends on "chase"
```

### Words you must know
| Word | Means |
|---|---|
| **Head** | The boss word (*chase*) |
| **Dependent** | The word that hangs off it (*Dogs*) |
| **ROOT** | An imaginary word at the top; the main verb hangs off it |
| **The 3 rules** | Every word has **exactly one head** · **no cycles** · **everything reaches ROOT** |
| **Transition-based** | Build the tree left-to-right, greedily. Fast. Algorithm: **arc-eager / MaltParser** |
| **Graph-based** | Score every possible arrow, then pick the best overall tree. Algorithm: **Chu-Liu-Edmonds** |
| **MST** | Maximum Spanning Tree — the highest-scoring set of arrows that obeys the 3 rules |

### The exam asks: Chu-Liu-Edmonds

You get a table of arrow scores. Find the best tree.

```
STEP 1  For EVERY word, keep only its single BEST incoming arrow.
STEP 2  No cycle?  ->  that's your answer, done.
STEP 3  Cycle?     ->  for each arrow coming INTO the cycle from outside:
                          new score = its score - (score of the arrow it replaces)
                       pick the biggest.
STEP 4  Enter the cycle there; DELETE the cycle arrow pointing at that node;
        KEEP the other cycle arrow.
```

Mini example — R=ROOT, A, B. Scores: `R→A 3`, `R→B 9`, `A→B 5`, `B→A 8`.

```
Step 1   Best into A:  R->A 3 vs B->A 8   ->  B->A (8)
         Best into B:  R->B 9 vs A->B 5   ->  R->B (9)

Step 2   A's head is B, B's head is R.  No cycle!  DONE.

ANSWER:  R->B (9),  B->A (8).   Total = 17
```

If instead `A→B` had been 12, you'd get a cycle `A↔B` and would need steps 3–4.

### Also asked: Constituency vs Dependency (a table)
| | Constituency | Dependency |
|---|---|---|
| **Structure** | Nested **phrases**; words only at the leaves | **Word-to-word** arrows, no phrase nodes |
| **Good for** | Fixed word order (English) | **Free word order** (Hindi, Czech) |
| **Used in** | Grammar checking | **Relation extraction, QA, machine translation** |
| **Algorithms** | CKY, chart, PCFG | Arc-eager (transition), Chu-Liu-Edmonds (graph) |

### Trap
Check your final answer against the **3 rules**: one head per word, nothing
points *into* ROOT, and following arrows backwards from any word must reach ROOT.

---
---

# Ch 11 — Contextual Embeddings & Attention

> **This is the easiest 6 marks in the paper.** It is one weighted average.
> If you learn one chapter today, learn this one.

### What it's for
An **embedding** is a word turned into a list of numbers, so a computer can do
maths on it.

- **Static embedding** (Word2Vec): *bank* gets **one** list of numbers forever —
  river bank and money bank share it. Bad.
- **Contextual embedding** (BERT): *bank* gets a **different** list of numbers in
  every sentence, worked out from its neighbours. Good.

**Attention** is how it does that: to represent a word, **take a weighted average
of the words around it**, giving more weight to the ones that matter.

### Words you must know
| Word | Means |
|---|---|
| **Embedding** | A word represented as a list of numbers, e.g. `[0.7, 0.8]` |
| **Attention weights (α)** | How much to listen to each word. **They always add up to 1** |
| **Value vectors (v)** | The numbers being averaged |
| **Head** | One attention calculation. Models run several in parallel |
| **Multi-head** | Several heads, results glued together and squashed back down by a matrix `W_O` |

### The exam asks: compute the contextual embedding

```
Output = α₁ × v₁  +  α₂ × v₂  +  α₃ × v₃

That's it. Multiply each vector by its weight, add them up.
```

Mini example — `α = [0.5, 0.5]`, `v₁ = [2, 0]`, `v₂ = [0, 4]`:
```
= 0.5 × [2,0]  +  0.5 × [0,4]
= [1, 0]       +  [0, 2]
= [1, 2]
```
**Free check: the weights must sum to 1.** `0.5 + 0.5 = 1` ✓

### Then it may ask: multi-head
Glue the head outputs into one long list, then multiply by `W_O`.
```
head₁ = [1.1, 2.2] ,  head₂ = [0.5, 0.8]

Concatenate  ->  [1.1, 2.2, 0.5, 0.8]      (4 numbers, so W_O has 4 rows)

Multiply by W_O: for each COLUMN of W_O, multiply down and add.
    column 1: 1.1×0.2 + 2.2×0.4 + 0.5×0.6 + 0.8×0.1 = 1.48
```

### The theory half (3 of the 6 marks — memorise these)
**What are contextual embeddings?** Vector representations of words that
**change based on the surrounding context**. Important because they capture
**word sense disambiguation**, better **semantic relationships**, and improve
**downstream tasks**.

**Static vs contextual?** Static = one fixed vector per word, **cannot handle
polysemy** (words with several meanings). Contextual = dynamic, different vector
per sentence, **computed using attention**.

**Why multiple heads?** Different **representation subspaces** · different
**relationship types** (syntactic, semantic, positional) · **diverse patterns**
· more capacity for little extra compute.

### Trap
None, really — just don't forget to check that α sums to 1.

---
---

# Ch 12 — WordNet & Word Sense Disambiguation

### What it's for
Many words have several meanings. **WSD = deciding which meaning is being used.**
*"I went to the bank"* — money, or river?

### Words you must know
| Word | Means |
|---|---|
| **Sense** | One meaning of a word |
| **Homonymy** | Same spelling, **unrelated** meanings. *bat* (stick) vs *bat* (animal) |
| **Polysemy** | Same word, **related** meanings. *bank* the building vs *bank* the company |
| **Synonym** | Same meaning. *couch / sofa* |
| **Antonym** | Opposite. *hot / cold* |
| **Hyponym** | More specific. *car* is a hyponym of *vehicle* |
| **Hypernym** | More general. *vehicle* is a hypernym of *car* |
| **WordNet** | A big dictionary/thesaurus database of all these relations |
| **Synset** | WordNet's word for a **set of synonyms** = one concept |
| **Gloss** | The dictionary definition text of a sense |

### The exam asks one of two things

---

**(A) Lesk algorithm.** *"Which sense fits? Compute the overlap."*

```
1. Write down the words in the SENTENCE (drop the target word and the/a/is...).
2. Write down the words in EACH sense's definition.
3. COUNT how many words appear in BOTH.
4. Highest count wins.
```

Mini example — *"The crane at the construction site lifted a heavy load."*
```
Context: [ construction, site, lifted, heavy, load ]

Sense 1 (bird)    : tall, bird, long, neck, wetland      -> overlap 0
Sense 2 (machine) : machine, lifting, heavy, construction, site, load
                     matches: construction, site, heavy, load  -> overlap 4

4 > 0  =>  SENSE 2, the machine.
```

---

**(B) Cosine similarity.** *"Here are vectors for each sense and the target. Which sense?"*

**Cosine** measures whether two lists of numbers **point the same way**.
1.0 = identical direction. 0 = unrelated.

```
              (multiply matching numbers and add them up)
cosine  =  ---------------------------------------------------
            (length of a)  ×  (length of b)

length of [1,3,2] = √(1² + 3² + 2²) = √14 = 3.742
```

Mini example — target `[1,3,2]`, sense S1 `[2,6,4]`:
```
top    = 1×2 + 3×6 + 2×4 = 2 + 18 + 8 = 28
|S1|   = √(4+36+16) = √56 = 7.483
cosine = 28 / (3.742 × 7.483) = 1.0     <- perfect match, pick S1
```

### Trap ⚠️ — this one costs marks every year
**Do not just pick the biggest "top" number.** A sense with big numbers wins the
multiplication without being the right meaning. **You must divide by both
lengths.** In the real 2024 paper, the wrong sense had the larger top number.

---
---

# Ch 13 — Semantic Web (RDF / OWL)

### What it's for
Web pages are written for humans. A computer sees *"Anita studies Data Science"*
as a meaningless string. **The semantic web writes facts in a form computers can
reason about.**

### Words you must know
| Word | Means |
|---|---|
| **Triple** | A fact in three parts: **subject – predicate – object**. *(Anita, enrolledIn, DataScience)* |
| **RDF** | Resource Description Framework — the language for writing **facts** as triples |
| **RDFS** | RDF Schema — adds `Class`, `subClassOf`, `domain`, `range` |
| **OWL** | Web Ontology Language — adds **rules and logic**, so a computer can **reason** |
| **Ontology** | A formal description of the concepts in a domain and how they relate |
| **SPARQL** | The query language for RDF (like SQL for databases) |
| **Inference** | A fact **nobody wrote down** but which follows logically |

### The exam asks: write triples, and RDF vs OWL

**Writing triples** — just split each English sentence into three parts:
```
"Anita is enrolled in Data Science"        -> ( Anita , enrolledIn , DataScience )
"Data Science is taught by Dr. Rao"        -> ( DataScience , taughtBy , DrRao )
"Dr. Rao is a member of the CS Department" -> ( DrRao , memberOf , CSDepartment )
```
And name the parts: **Subjects** = Anita, DataScience, DrRao. **Predicates** =
enrolledIn, taughtBy, memberOf. **Objects** = DataScience, DrRao, CSDepartment.

**⭐ RDF vs OWL — learn this sentence:**
> **RDF handles data representation; OWL handles logic and consistency checking.**
> Storing facts → **RDF** (simple subject–predicate–object triples).
> Checking a constraint like *"every book must have an author"* → **OWL**,
> because OWL supports **restrictions and reasoning**.

**Derived inference** — if asked to spot one:
```
Given:  Tesla is a  ElectricCar
        ElectricCar is a  Car
        Car is a  Vehicle

INFERRED (nobody wrote it):   Tesla is a  Vehicle
because "is a / subClassOf" is TRANSITIVE.
```
Label that arrow **"inferred"** on your diagram — that's what the marks are for.

### Trap
Don't mix them up. **RDF = facts. OWL = rules.** If the question says
*"must", "every", "at least one", "constraint"* → the answer is OWL.

---
---

# Ch 14 — RAG

### What it's for
An LLM like ChatGPT has three problems: its knowledge **stops at its training
date**, it **makes things up** (hallucinates), and it **doesn't know your private
documents**.

**RAG's fix:** don't retrain it. Before answering, **go and fetch the relevant
documents and paste them into the prompt.**

### Words you must know
| Word | Means |
|---|---|
| **Retriever** | The part that **finds** relevant documents |
| **Generator** | The LLM that **writes** the answer using them |
| **Chunk** | A document sliced into a bite-sized piece |
| **Token** | Roughly a word — how LLM input is measured |
| **Context length** | The **maximum tokens** the LLM can accept at once |
| **Semantic search** | Finds by **meaning**, not exact words — so *"laptop repair cost"* finds *"computer hardware pricing"* |
| **Hallucination** | The LLM confidently making something up |

### The exam asks: two bits of arithmetic

---

**(A) How many chunks fit?**
```
1. fixed     = query tokens + system prompt tokens
2. available = context length - fixed
3. chunks    = available ÷ chunk size , ROUNDED DOWN   ("floor")
4. total sent = fixed + (chunks used × chunk size)
```
Mini example — query 160, prompt 240, context 4096, chunk 480:
```
fixed     = 160 + 240 = 400
available = 4096 - 400 = 3696
chunks    = 3696 ÷ 480 = 7.7  ->  7        (a part-chunk doesn't fit)
total     = 400 + 7×480 = 400 + 3360 = 3760
```

---

**(B) Precision.**
```
              how many retrieved chunks were RELEVANT
precision = ------------------------------------------
                 how many chunks you retrieved
```
Mini example — you keep everything scoring ≥ 0.75 from
`0.92, 0.86, 0.79, 0.71` → **3 chunks kept**. All relevant → `3/3 = 1.0`.
If one turns out irrelevant → `2/3 = 0.67`.

**The comment they always want:**
> Lower precision means **more irrelevant text in the context**, which
> **increases noise** and **raises the risk of hallucination**, degrading
> generation quality. Fewer but more relevant chunks generally **improves**
> factual grounding.

### Trap
**Always round DOWN.** 7.7 chunks → 7, never 8. Write the word *"floor"* — it's
a marked step.

---
---

# Ch 15 — Text Summarization

### What it's for
Turning long text into short text. The exam cares about **which kind** of
summarization, and one **formula** for picking sentences.

### Words you must know
| Word | Means |
|---|---|
| **Extractive** | Summary is built from **sentences copied out of** the original |
| **Abstractive** | Summary is written in **new words** |
| **Single-document** | Summarises **one** document |
| **Multi-document** | Summarises **many documents about the same event** — must remove repetition |
| **Generic** | A general summary, no particular question in mind |
| **Query-focused** | Summarises only the parts answering **a specific question** |
| **Redundancy** | Repeating what the summary already says |
| **MMR** | Maximal Marginal Relevance — the formula for picking the next sentence |
| **ROUGE** | The score for grading a summary against human-written ones |

### The exam asks one of two things

---

**(A) MMR.** *"Which sentence gets picked next?"*

The idea: a good next sentence must be **about the topic** AND **not repeat what
you already have**.

```
MMR = λ × sim(s,q)   −   (1−λ) × sim(s,S)
      \___________/       \______________/
       relevance           redundancy
      (to the query)      (to what's already picked)

Pick the HIGHEST. That's it.
```

Mini example — λ = 0.5. S1: relevance 0.8, redundancy 0.6. S2: relevance 0.7, redundancy 0.2.
```
MMR(S1) = 0.5 × 0.8 − 0.5 × 0.6 = 0.40 − 0.30 = 0.10
MMR(S2) = 0.5 × 0.7 − 0.5 × 0.2 = 0.35 − 0.10 = 0.25

S2 wins — even though S1 is MORE relevant, it repeats the summary too much.
```
**The justification they want (2 marks):** *although S1 is more relevant, it is
highly similar to the already-selected sentence, making it redundant; S2 adds
new complementary information, giving a higher MMR score.*

---

**(B) Identify the summarization type.** Just match the scenario:
```
ONE document, wants a headline/abstract   ->  Single-document, GENERIC
MANY documents on the same event          ->  MULTI-DOCUMENT
"Summarize only the parts about X"        ->  QUERY-FOCUSED
```

**Also learn: the 3 stages of summarization**
```
1. Content selection    — pick which sentences to use
2. Information ordering — decide what order to put them in
3. Sentence realization — tidy up the wording
```

**ROUGE-2**, if asked: *what fraction of the bigrams (word pairs) in the human
reference summaries also appear in the system summary?*
```
                bigrams matched
ROUGE-2  =  ------------------------
             total reference bigrams
```

### Trap
In MMR, the **more relevant sentence often loses**. That's the whole point of
the formula — don't just pick the biggest `sim(s,q)`. But it isn't a rule: if
**λ is large** (0.8+), relevance dominates and the more relevant one *does* win.
**Do the arithmetic, don't guess.**

---
---

# The whole exam on one page

| Q | Chapter | The one formula / recipe |
|---|---|---|
| **3** | 9 Parsing | `P(tree) = multiply all rule probabilities` · or the top-down table **with a backtrack** |
| **3** | 10 Dependency | Best incoming arc per word → cycle? → contract → `score − replaced score` |
| **4** | 11 Attention | `Output = Σ αᵢ × vᵢ` — **weights sum to 1** |
| **5** | 12 WSD | Lesk: **count shared words**. Cosine: **divide by both lengths** |
| **6** | 13 Semantic Web | Triples = subject–predicate–object. **RDF = facts, OWL = rules** |
| **6** | 14 RAG | `floor((context − query − prompt) ÷ chunk)` · `precision = relevant/retrieved` |
| **7** | 15 Summarization | `MMR = λ·relevance − (1−λ)·redundancy` |

### The 5 things that cost marks
1. **Cosine — divide by the lengths.** Biggest dot product is often the wrong sense.
2. **RAG — round DOWN.** Always.
3. **MMR — do the arithmetic.** The more relevant sentence frequently loses.
4. **Top-down parsing — show the failure and the pop.**
5. **Dependency — one head per word, nothing into ROOT, everything reaches ROOT.**

### Do them in this order (not paper order)
```
Q4  Attention      ~5 min   easiest marks in the paper
Q7  MMR            ~7 min   two multiplications
Q6  RAG            ~10 min  arithmetic + recall
Q5  Lesk/cosine    ~10 min  counting
Q3  Parsing        longest — leave it the remaining time
```

---

**Next:** open `PRACTICE-PAPER` and do **Set A**. Come back here when stuck.
Full worked past-paper solutions are in `SOLVED-NUMERICALS`.
