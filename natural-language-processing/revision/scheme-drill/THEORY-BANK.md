# NLP Theory Bank — every module in the official scheme

> **How to use this.** Read the question. Say your answer **out loud, in your
> own words, before you click**. Getting it half-wrong out loud is the exercise.
> Reading a correct answer you didn't attempt teaches you nothing.
>
> Answers are written the way you should **write them in the exam**: short
> labelled points, not paragraphs. Examiners tick keywords.

---

## Contents

| § | Module | Question type in the scheme | Marks |
|---|---|---|---|
| 1 | 2 — Vector Semantics | Problem | part of Q1 (5) |
| 2 | 3 — Language Models & Neural LM | Problem | part of Q1 (5) |
| 3 | 5 — POS Tagging | Problem | part of Q2 (5) |
| 4 | 6 — Hidden Markov Models | Problem | part of Q2 (5) |
| 5 | 9 — Statistical Parsing | Problem | part of Q3 (6) |
| 6 | 10 — Dependency Parsing | **Problem / Theory / Application** | part of Q3 (6) |
| 7 | 11 — Contextual Embeddings | **Problems and/or Theory** | Q4 (6) |
| 8 | 12 — Word Sense & WordNet | **Problems and/or Theory** | part of Q5 (6) |
| 9 | 13 — Semantic Web & Ontology | **Application / Case study** | part of Q5 (6) |
| 10 | 14 — RAG | **Problem and/or Theory** | Q6 (6) |
| 11 | 15 — Text Summarization | **Problem and/or Theory** | Q7 (6) |

> **§6 to §11 are where the theory marks live.** If you are short of time,
> start at §11 and work upwards.

---
---

# 1 · Module 2 — Vector Semantics

*Scheme says **Problem**, so a sum is likely — but these definitions are what
the sum is built on, and they buy the "explain your answer" marks.*

<details>
<summary><b>Q1.1</b> What is the distributional hypothesis? [1 mark]</summary>

- Words that occur in **similar contexts** tend to have **similar meanings**.
- Firth's line: *"You shall know a word by the company it keeps."*
- Consequence: meaning can be learned **from raw text alone**, with no
  dictionary — just by counting which words appear near which.
</details>

<details>
<summary><b>Q1.2</b> Why TF-IDF instead of raw frequency counts? [2 marks]</summary>

- Raw counts are dominated by words like *the, of, is* — frequent **everywhere**,
  so they carry **no discriminating information**.
- **TF** (term frequency) rewards a word for being common **in this document**.
- **IDF** (inverse document frequency) penalises it for being common **across all
  documents**: `IDF = log(N / df)`.
- The product is high only for words **frequent here but rare elsewhere** —
  exactly the words that characterise the document.
</details>

<details>
<summary><b>Q1.3</b> Why cosine similarity rather than Euclidean distance? [2 marks]</summary>

- Cosine measures the **angle** between vectors, ignoring their **length**.
- Document length varies enormously; a long document has larger counts for
  *every* word, so Euclidean distance would call it "far" from a short document
  on the same topic.
- Cosine normalises that away: `cos(a,b) = (a·b) / (|a| × |b|)`, bounded in
  `[-1, 1]` — and in `[0, 1]` for non-negative count vectors.
- **1 = same direction = same topic. 0 = unrelated.**
</details>

<details>
<summary><b>Q1.4</b> Compare sparse and dense vector representations. [2 marks]</summary>

| | **Sparse** (TF-IDF, PPMI) | **Dense** (Word2Vec, GloVe) |
|---|---|---|
| Length | size of the vocabulary — 20,000+ | 50–300 |
| Contents | mostly zeros | all cells non-zero |
| Built by | **counting** | **predicting / learning** |
| Interpretable? | yes — each cell is a word | no — cells are latent features |
| Generalises? | no — *car* and *automobile* are unrelated dimensions | yes — similar words land near each other |
</details>

<details>
<summary><b>Q1.5</b> What is PPMI and why the "positive" part? [2 marks]</summary>

- **PMI** = `log₂( P(w,c) / (P(w) × P(c)) )` — how much more often word `w` and
  context `c` co-occur than **chance** would predict.
- **PPMI** = `max(0, PMI)` — negative values are clipped to zero.
- **Why clip:** a negative PMI claims two words co-occur *less* than chance. To
  estimate that reliably you would need a colossal corpus, so the number is
  **unreliable noise**. Better to say "no evidence of association" (0).
</details>

---
---

# 2 · Module 3 — Language Models & Neural LM

<details>
<summary><b>Q2.1</b> What is the Markov assumption in an n-gram model? [1 mark]</summary>

- The probability of the next word depends only on the **previous n−1 words**,
  not on the whole history.
- Bigram: `P(wn | w1 … wn-1) ≈ P(wn | wn-1)`.
- It is an **approximation** made for tractability — without it we would need
  counts for every possible sentence prefix, which never occur often enough to
  count reliably.
</details>

<details>
<summary><b>Q2.2</b> Why is smoothing necessary? What does Laplace smoothing do? [2 marks]</summary>

- **The zero-probability problem:** any bigram unseen in training gets
  probability 0, which makes the **whole sentence** probability 0 and perplexity
  **infinite** — even if only one word is new.
- **Laplace (add-one):** pretend every bigram was seen one extra time.
  `P(w2|w1) = (count(w1 w2) + 1) / (count(w1) + V)`
- **The trap:** the denominator adds **V**, the vocabulary size — *not* 1 —
  because you added 1 to each of V possible continuations.
- Cost: it steals a lot of probability mass from seen events. That is why
  backoff, interpolation and Kneser-Ney exist.
</details>

<details>
<summary><b>Q2.3</b> What does perplexity measure? Is high or low better? [2 marks]</summary>

- Perplexity = the **inverse probability of the test set, normalised by length**:
  `PP(W) = P(w1…wN)^(−1/N)`.
- Intuition: the **average number of equally-likely words the model is choosing
  between** at each step. Perplexity 100 means it is as confused as if guessing
  uniformly among 100 words.
- **Lower is better.** Lower perplexity = higher probability assigned to real
  text = better model.
- Only comparable between models with the **same vocabulary**.
</details>

<details>
<summary><b>Q2.4</b> Give three advantages of a neural LM over an n-gram LM. [3 marks]</summary>

1. **Generalisation via embeddings.** *dog* and *cat* have similar vectors, so a
   pattern learned for one transfers to the other. An n-gram model treats them
   as unrelated symbols.
2. **No sparsity / no zero counts.** Every word gets non-zero probability from
   the softmax — no smoothing needed.
3. **Longer, cheaper context.** N-gram tables grow as `V^n`; a neural LM's
   parameters grow roughly linearly, so it can condition on more context.
4. *(bonus)* Parameters are **shared** across contexts instead of one stored
   count per context.
</details>

<details>
<summary><b>Q2.5</b> What does the softmax layer do, and why exponentiate? [2 marks]</summary>

- Softmax turns unbounded real-valued **scores** into a **probability
  distribution**: `P(i) = e^(zi) / Σⱼ e^(zj)`.
- **Why exponentiate:** it forces every value **positive** (raw scores can be
  negative) and **amplifies the leading score**, so the model expresses
  confidence rather than a flat guess.
- The output is guaranteed to **sum to 1** — your free correctness check.
</details>

<details>
<summary><b>Q2.6</b> Why is a non-linear activation needed at all? [1 mark]</summary>

- Without it, stacking layers is just multiplying matrices, and the composition
  of linear maps is still **one linear map**. The network could never learn
  anything a single layer couldn't — the classic XOR failure.
- The non-linearity is what makes depth worth having.
</details>

---
---

# 3 · Module 5 — POS Tagging

<details>
<summary><b>Q3.1</b> What is POS tagging and why is it hard? [2 marks]</summary>

- Assigning each word in a sentence its **part of speech** (noun, verb,
  determiner …) from a fixed tagset.
- **Hard because of ambiguity:** the same word takes different tags in different
  contexts. *book* → noun in *"read a book"*, verb in *"book a flight"*.
- Around **85% of word *types*** are unambiguous — but the ambiguous ones are the
  **common** words, so a large share of *tokens* in running text are ambiguous.
- Also: **unknown words** never seen in training must still be tagged.
</details>

<details>
<summary><b>Q3.2</b> Open class vs closed class words. [2 marks]</summary>

| | **Open class** | **Closed class** |
|---|---|---|
| Members | nouns, verbs, adjectives, adverbs | determiners, prepositions, pronouns, conjunctions, auxiliaries |
| New members | **yes** — new nouns/verbs coined constantly (*to google*) | **no** — a fixed, small, stable list |
| Size | tens of thousands | a few dozen to a few hundred |
| Carry | **content** meaning | **grammatical function** |
| Unknown words | almost always land here (usually nouns) | never |
</details>

<details>
<summary><b>Q3.3</b> What is the most-frequent-tag baseline, and why does it matter? [2 marks]</summary>

- Tag every word with the tag it carried **most often in training**; tag unknown
  words as a noun (usually proper noun).
- It scores about **90%** accuracy — surprisingly high, because most tokens are
  unambiguous.
- **Why it matters:** it is the number any real tagger must beat. A model at 88%
  is *worse than doing nothing clever*. Good HMM and neural taggers reach ~97%.
</details>

<details>
<summary><b>Q3.4</b> Name three approaches to POS tagging with one strength each. [3 marks]</summary>

1. **Rule-based** — hand-written linguistic rules. Transparent and debuggable;
   needs no training data.
2. **Stochastic / HMM** — learns transition and emission probabilities from a
   tagged corpus. Fast, principled, no feature engineering.
3. **Neural (Bi-LSTM / BERT)** — learns contextual representations. Highest
   accuracy; handles unknown words through sub-word and character information.
</details>

---
---

# 4 · Module 6 — Hidden Markov Models

<details>
<summary><b>Q4.1</b> What makes an HMM "hidden"? Define its components. [2 marks]</summary>

- The **states** (the POS tags) are **not observed** — you only see the
  **emissions** (the words), and must infer the state sequence from them.
- Components:
  - **Q** — the set of hidden states (the tagset)
  - **A** — **transition** probabilities `P(tag_i | tag_i-1)`
  - **B** — **emission** probabilities `P(word | tag)`
  - **π** — initial / start probabilities
</details>

<details>
<summary><b>Q4.2</b> State the two independence assumptions an HMM makes. [2 marks]</summary>

1. **Markov assumption** — the current state depends only on the **immediately
   previous state**, not on the whole history.
2. **Output independence** — the observed word depends only on the **state that
   produced it**, not on neighbouring words or states.

Both are clearly false of real language, but they make exact inference cheap —
which is the whole point.
</details>

<details>
<summary><b>Q4.3</b> The three fundamental problems of an HMM, and the algorithm for each. [3 marks]</summary>

| # | Problem | Question it answers | Algorithm |
|---|---|---|---|
| 1 | **Likelihood** | How probable is this observation sequence? | **Forward** |
| 2 | **Decoding** | What is the most likely *hidden state sequence*? | **Viterbi** |
| 3 | **Learning** | What are A and B, given only observations? | **Forward–Backward** (Baum-Welch, an EM algorithm) |
</details>

<details>
<summary><b>Q4.4</b> Viterbi vs Forward — what is the one difference? [2 marks]</summary>

- **Identical** recursion, identical table, identical emission multiply. Only the
  combination step differs:
  - **Viterbi takes the MAX** over previous states — and stores a
    **backpointer**, so it can reconstruct the best path.
  - **Forward takes the SUM** over previous states — the total probability of
    *all* paths. No backpointer.
- **MAX = "which single path is best". SUM = "how likely overall".**
- Learn one and you have both.
</details>

<details>
<summary><b>Q4.5</b> Why dynamic programming instead of enumerating all tag sequences? [1 mark]</summary>

- With `N` states and `T` words there are `N^T` possible sequences —
  exponential, hopeless for a real sentence.
- Viterbi reuses the best path *into* each state at each step, giving `O(N²T)`.
  That reuse **is** the dynamic programming.
</details>

---
---

# 5 · Module 9 — Statistical Parsing

<details>
<summary><b>Q5.1</b> What is a PCFG and what problem does it solve? [2 marks]</summary>

- A **Probabilistic Context-Free Grammar**: a CFG in which every rule carries a
  probability, and all rules expanding the **same non-terminal sum to 1**.
- **Problem solved — structural ambiguity.** A plain CFG can tell you a sentence
  has five valid parses but not which one is meant. A PCFG **ranks** them: the
  probability of a parse is the **product of the probabilities of every rule
  used**, and the best parse is the highest product.
</details>

<details>
<summary><b>Q5.2</b> What is PP-attachment ambiguity? Give an example. [2 marks]</summary>

- A prepositional phrase can attach to **either the verb or the preceding noun**,
  giving two different meanings.
- *"I saw the man with the telescope."*
  - **VP-attachment:** *with the telescope* modifies **saw** → the telescope is
    the instrument I used.
  - **NP-attachment:** *with the telescope* modifies **the man** → the man was
    carrying it.
- A PCFG chooses whichever attachment uses higher-probability rules.
</details>

<details>
<summary><b>Q5.3</b> Compare top-down and bottom-up parsing. [3 marks]</summary>

| | **Top-down** | **Bottom-up** |
|---|---|---|
| Starts from | the start symbol **S** | the **words** |
| Direction | expands rules until it reaches the words | combines constituents until it reaches S |
| Wastes effort on | trees that **can never match the input words** | constituents that **can never fit into an S** |
| Guarantee | every tree it builds is rooted in S | every tree it builds is grounded in the input |
| Backtracking | yes, on failure | yes, on failure |
</details>

<details>
<summary><b>Q5.4</b> What is CKY and what does it require of the grammar? [2 marks]</summary>

- **CKY** is a bottom-up **dynamic programming** chart parser. It fills a
  triangular table where cell `[i,j]` holds every non-terminal that can span
  words `i…j`, building longer spans from shorter ones. Cost `O(n³ × |G|)`.
- **Requirement: Chomsky Normal Form** — every rule is either `A → B C` (exactly
  two non-terminals) or `A → w` (a single terminal).
- Any CFG can be mechanically converted to CNF, so this costs no expressive
  power.
</details>

<details>
<summary><b>Q5.5</b> Name two weaknesses of a plain PCFG. [2 marks]</summary>

1. **No lexical sensitivity.** Rule probabilities ignore the actual words, so the
   grammar cannot know that *eat* takes a food object. Fixed by
   **lexicalisation** — attaching head words to rules.
2. **Poor independence assumptions.** Each expansion is assumed independent of
   context, but real expansions depend heavily on position — subject NPs are far
   more often pronouns than object NPs. Fixed by **parent annotation / state
   splitting**.
</details>

---
---

# 6 · Module 10 — Dependency Parsing

> **The scheme explicitly allows Theory here.** Oct 2024 asked a 3-mark
> compare-and-contrast with no arithmetic at all.

<details>
<summary><b>Q6.1</b> ⭐ Constituency vs dependency parsing — compare. [3 marks]</summary>

| | **Constituency (phrase structure)** | **Dependency** |
|---|---|---|
| Represents | how words group into **nested phrases** (NP, VP, PP) | direct **head → dependent** relations between words |
| Nodes | the words **plus** invented non-terminals | **only the words** — nothing invented |
| Needs | a CFG / PCFG | a set of grammatical relations (nsubj, dobj, …) |
| Output | a tree with internal phrase nodes | labelled arcs over the sentence |
| Suits | languages with **fixed word order** (English) | languages with **free word order** (Hindi, Czech, Latin) |
| Downstream use | grammar checking, phrase extraction | relation extraction, QA, machine translation |
</details>

<details>
<summary><b>Q6.2</b> ⭐ State the well-formedness conditions of a dependency tree. [3 marks]</summary>

1. **Single head** — every word has **exactly one** incoming arc.
2. **Root** — there is a single ROOT; **nothing points into ROOT**.
3. **Connected and acyclic** — following arcs backwards from any word must reach
   ROOT. No cycles, no orphans.
4. *(optional)* **Projectivity** — no crossing arcs when drawn above the
   sentence.

**Use these as your checklist** whenever you are asked to draw a tree. They
catch essentially every mistake.
</details>

<details>
<summary><b>Q6.3</b> ⭐ Transition-based vs graph-based parsing. [3 marks]</summary>

| | **Transition-based** (arc-standard / arc-eager) | **Graph-based** (MST) |
|---|---|---|
| How | a stack + buffer; a classifier picks SHIFT / LEFT-ARC / RIGHT-ARC at each step | score **every possible arc**, then find the maximum spanning tree |
| Search | **greedy, local** — one pass, no going back | **global** — all trees considered at once |
| Speed | **linear** `O(n)` — very fast | `O(n²)` or worse |
| Errors | an early mistake **propagates** and can never be undone | no error propagation |
| Long arcs | weaker on long-distance dependencies | better on long-distance dependencies |
| Non-projective | not natively | **yes** — Chu-Liu-Edmonds handles it |
</details>

<details>
<summary><b>Q6.4</b> What is projectivity, and why does it matter? [2 marks]</summary>

- A dependency tree is **projective** if, when every arc is drawn above the
  sentence in word order, **no two arcs cross**.
- Equivalently: every word's descendants form a **contiguous block**.
- **Why it matters:** the fast standard transition systems (arc-standard,
  arc-eager) can *only* produce projective trees. Freer-word-order languages
  produce non-projective structures, which need graph-based parsing or an extra
  SWAP transition.
</details>

<details>
<summary><b>Q6.5</b> Define head and dependent. How do you tell which is which? [2 marks]</summary>

- The **head** determines the syntactic category and behaviour of the phrase;
  the **dependent** modifies or completes it.
- Tests: the head can usually **stand alone** where the whole phrase stood; the
  dependent cannot. The head controls agreement.
- *"the red car"* → head **car**, dependents *the* (det) and *red* (amod).
- In *"She ate rice"*, the verb **ate** is the head of the sentence and attaches
  to ROOT; *She* is `nsubj`, *rice* is `dobj`.
</details>

<details>
<summary><b>Q6.6</b> Why is Chu-Liu-Edmonds needed rather than "give each word its best head"? [2 marks]</summary>

- Greedily giving every word its highest-scoring head satisfies "one head each",
  but it can create a **cycle** — A's best head is B and B's best head is A —
  and a cycle is not a tree.
- **Chu-Liu-Edmonds** does exactly that greedy step, then **detects each cycle,
  contracts it to a single node, and re-solves**, repeating until nothing
  cycles. It is guaranteed to return the **maximum-scoring valid tree**.
- If the greedy step happens to produce no cycle, you are already finished.
</details>

---
---

# 7 · Module 11 — Contextual Embeddings & Attention

> Feb 2026 gave **3 of 6 marks** here to pure theory. Mar 2026 gave **2.5 of 6**.
> This section is the highest-yield reading in the file.

<details>
<summary><b>Q7.1</b> ⭐ What are contextual embeddings and why do they matter? [1.5 marks]</summary>

- Vector representations of words whose values **change with the surrounding
  context** — the same word gets a different vector in every sentence.
- Produced by transformer models such as **BERT** and **ELMo**.
- Why they matter:
  - they capture **word sense disambiguation** — *bank* in a river sentence gets
    a different vector from *bank* in a finance sentence;
  - they encode better **semantic and syntactic relationships**;
  - they substantially improve **downstream tasks** (NER, QA, sentiment,
    tagging).
</details>

<details>
<summary><b>Q7.2</b> ⭐ How do contextual embeddings differ from static ones like Word2Vec? [1.5 marks]</summary>

| | **Static** (Word2Vec, GloVe) | **Contextual** (BERT, ELMo) |
|---|---|---|
| Vectors per word | **one, fixed forever** | **one per occurrence** |
| Polysemy | **cannot handle it** — all senses collapse into one vector | handled — each sense gets its own vector |
| Computed from | a global co-occurrence/prediction objective | the **actual surrounding sentence**, via attention |
| Depends on position? | no | yes |
| Cost | cheap, a lookup table | expensive, a forward pass through the model |
</details>

<details>
<summary><b>Q7.3</b> ⭐ Why do transformers use multiple attention heads instead of one? [1.5 marks]</summary>

- Different words in a sentence relate to each other in **many ways at once** —
  a single averaging operation cannot capture all of them.
- Multiple heads let the model:
  - attend to different **representation subspaces**;
  - capture different **relationship types** — syntactic, semantic, positional;
  - learn **diverse patterns** — one head tracks adjacent words, another
    subject–verb links, another coreference;
  - **increase capacity** without a proportional increase in computation, since
    the heads run in **parallel** and each is lower-dimensional.
</details>

<details>
<summary><b>Q7.4</b> Explain the roles of Query, Key and Value. [2 marks]</summary>

Think of a **fuzzy lookup table**.

- **Query (q)** — the *current focus of attention*: the word asking "who here is
  relevant to me?"
- **Key (k)** — each other word's *advertisement*: what it offers, used to be
  compared against the query.
- **Value (v)** — each word's *actual content*, the thing that gets carried
  forward once its key matched.
- Keys and values always come in pairs. You match on the **key** but you
  propagate the **value**.
- All three come from the same input in **self**-attention: `q = Qx`, `k = Kx`,
  `v = Vx`.
</details>

<details>
<summary><b>Q7.5</b> ⭐ Why divide by √d_k in scaled dot-product attention? [1.5 marks]</summary>

- Dot products grow with dimension: with `d_k` terms in the sum, the variance of
  `q·k` scales with `d_k`, so scores become **large in magnitude**.
- Large scores push softmax into a region where one weight is ≈1 and the rest
  ≈0 — it **saturates**, and its **gradients vanish**, so the model trains badly.
- Dividing by `√d_k` keeps the scores at a sensible scale. The handout describes
  it as acting as **regularisation that improves performance of larger models**.
- Formula: `SelfAttention(Q,K,V) = softmax(QKᵀ / √d_k) V`
</details>

<details>
<summary><b>Q7.6</b> Self-attention has no notion of word order. How is that fixed? [1.5 marks]</summary>

- Self-attention is a **weighted average** — permuting the input words permutes
  the output identically. It is **order-blind**; *"dog bites man"* and
  *"man bites dog"* would produce the same set of representations.
- **Fix: positional encodings** — a position-dependent vector is **added to each
  input embedding** before the first layer, so position information is carried
  in the vectors themselves.
- Either fixed sinusoidal functions or learned position embeddings.
</details>

<details>
<summary><b>Q7.7</b> List the barriers to using self-attention as a building block, and the fix for each. [3 marks]</summary>

| Barrier | Fix |
|---|---|
| **No inherent notion of order** | add **position representations** to the inputs |
| **No non-linearity** — it is all just weighted averages | apply the same **feed-forward network** to each self-attention output |
| **Must not look at the future** when predicting a sequence | **mask** future positions by setting those attention weights to **0** (masked self-attention, used in language modelling and MT decoding) |
</details>

<details>
<summary><b>Q7.8</b> Self-attention vs cross-attention vs masked self-attention. [2 marks]</summary>

- **Self-attention** — Q, K and V all come from the **same sequence**. Every
  position may attend to every other.
- **Masked (causal) self-attention** — same, but positions **after** the current
  one are masked out, so the model cannot cheat by seeing the future. Used in
  decoders and language models.
- **Cross-attention** — the **queries come from the decoder**, while the **keys
  and values come from the encoder**. This is how the decoder reads the source
  sentence in translation.
</details>

<details>
<summary><b>Q7.9</b> How does multi-head attention combine its heads? [1 mark]</summary>

- Each head has its **own** `W^Q, W^K, W^V` matrices and produces its own output
  vector.
- The head outputs are **concatenated** and then **projected back down to
  dimension d** by a matrix `W^O`, so the output is the **same size as the
  input** and layers can be stacked.
- `MultiHeadAttention(X) = (head₁ ⊕ head₂ ⊕ … ⊕ head_h) W^O`
- **Exam check:** the number of **rows of W^O** must equal the **length of the
  concatenated vector**.
</details>

<details>
<summary><b>Q7.10</b> What problem did attention solve in the original encoder-decoder? [2 marks]</summary>

- **The bottleneck problem.** Without attention, the decoder sees a **single
  fixed context vector** — the encoder's last hidden state — which must contain
  the entire source sentence. Long sentences do not fit.
- With attention, the decoder gets a **different, dynamic context vector at each
  step**, computed from **all** the encoder hidden states.
- Extra benefits stated in the slides: it **helps with vanishing gradients** by
  giving a shortcut to faraway states, and it gives **interpretability** — the
  attention distribution shows what the decoder was looking at.
</details>

<details>
<summary><b>Q7.11</b> Given two heads with weights [0.1, 0.2, 0.7] and [0.5, 0.3, 0.2] over ("the", "cat", "sat") — what is each head specialising in? [1 mark]</summary>

*This is the Mar 2026 Q4(d) question. The method: find the largest weight, name
the word, then say what kind of relation that word represents.*

- **Head 1** puts 0.7 on **"sat"** — the verb. It appears to track the
  **action / predicate**, i.e. a **syntactic subject–verb relationship**.
- **Head 2** puts 0.5 on **"the"** — a determiner. It appears to track
  **grammatical / structural** information rather than content.
- Together they demonstrate that different heads specialise in **different
  linguistic patterns**, which is exactly why multiple heads are used.
</details>

---
---

# 8 · Module 12 — Word Sense & WordNet

<details>
<summary><b>Q8.1</b> ⭐ Define homonymy, polysemy, synonymy, antonymy — with examples. [3 marks]</summary>

| Term | Meaning | Example |
|---|---|---|
| **Homonymy** | same form, **unrelated** meanings | *bank* (river edge) vs *bank* (financial) |
| **Polysemy** | same form, **related** meanings | *bank* (the institution) vs *bank* (the building it occupies) |
| **Synonymy** | different forms, (nearly) the **same** meaning | *big / large*, *couch / sofa* |
| **Antonymy** | **opposite** meaning along one dimension | *hot / cold*, *rise / fall* |

Sub-types of homonymy: **homophones** (same sound — *write/right*),
**homographs** (same spelling — *bass* the fish / *bass* the sound).
</details>

<details>
<summary><b>Q8.2</b> Define hyponymy, hypernymy and meronymy. [2 marks]</summary>

- **Hyponym** — a **more specific** term. *dog* is a hyponym of *animal*.
- **Hypernym** — the **more general** term. *animal* is a hypernym of *dog*.
  (Mnemonic: **hyper** = above = broader.)
- **Meronym** — a **part of** something. *wheel* is a meronym of *car*.
  The reverse, *car*, is the **holonym**.
</details>

<details>
<summary><b>Q8.3</b> What is WordNet? Describe its structure. [2 marks]</summary>

- A large **lexical database** of English, organised by **meaning** rather than
  by spelling.
- The unit is the **synset** — a set of synonyms that share one sense, together
  with a **gloss** (a short definition) and usually **usage examples**.
- Synsets are linked by **semantic relations**: hypernym/hyponym (the "is-a"
  hierarchy), meronym/holonym, antonym.
- Separate hierarchies for **nouns, verbs, adjectives and adverbs**.
- Used for WSD, semantic similarity, query expansion and as a sense inventory.
</details>

<details>
<summary><b>Q8.4</b> What is Word Sense Disambiguation and why is it hard? [2 marks]</summary>

- Deciding **which sense** of an ambiguous word is intended in a given context —
  choosing one synset from the inventory.
- Hard because: senses are **fine-grained** and overlapping; the useful context
  may be **far away** in the text or absent entirely; and hand-labelled sense
  data is expensive, so there is a **knowledge-acquisition bottleneck**.
- Matters for machine translation (different senses translate differently),
  information retrieval, and text-to-speech (*bass* the fish vs the sound).
</details>

<details>
<summary><b>Q8.5</b> Explain the Lesk algorithm. What is its main weakness? [2 marks]</summary>

- **Idea:** the correct sense is the one whose **dictionary gloss shares the most
  words with the context sentence**.
- **Simplified Lesk:** for each candidate sense, count the overlap between the
  gloss (plus usage examples) and the content words of the sentence; pick the
  highest count. Ties are broken by the most frequent sense.
- **Weakness:** glosses are **very short**, so overlaps are tiny and often zero —
  the method is brittle and sensitive to exact wording. Extended Lesk adds the
  glosses of related synsets to enlarge the signature.
</details>

<details>
<summary><b>Q8.6</b> ⭐ Why does WordNet perform poorly on domain-specific text, and what is the fix? [2 marks]</summary>

*This is the Mar 2026 Q5A question, almost verbatim.*

- WordNet is a **general-purpose** lexical database. Specialised medical, legal
  and technical vocabulary is **missing or only thinly defined**.
- Domain terms also carry **domain-specific senses** that the general inventory
  does not list, so the correct sense may simply not be an option.
- **Fix:** combine WordNet with a **domain-specific ontology or lexicon** — for
  example UMLS/SNOMED in medicine — or extend it with terms mined from a domain
  corpus. This adds expert knowledge and improves accuracy.
</details>

<details>
<summary><b>Q8.7</b> Name the three families of WSD approaches. [2 marks]</summary>

1. **Knowledge-based** — use a dictionary or WordNet, no labelled data.
   Example: **Lesk**, and graph-based measures over the WordNet hierarchy.
2. **Supervised** — train a classifier on hand-labelled sense examples using
   context features. Most accurate, but limited by labelled-data scarcity.
3. **Semi-supervised / unsupervised** — bootstrapping from a few seeds
   (Yarowsky), or clustering contexts into senses (word sense induction).
</details>

---
---

# 9 · Module 13 — Semantic Web & Ontology

> **The scheme says Application / Case study — there is no numerical here.**
> Every mark in this module is prose or triples. Do not skip it because it has
> no formula.

<details>
<summary><b>Q9.1</b> What is the Semantic Web, in one idea? [2 marks]</summary>

- A vision of the Web as a **huge queryable database** rather than a pile of
  documents: data published so that **machines can understand and combine it**,
  not just display it.
- Achieved by publishing data as **RDF triples** with globally unique **URIs**,
  so that a resource named in one dataset is recognisably the *same* resource in
  another.
- That shared naming is what lets independent datasets **merge automatically** —
  the basis of **Linked Open Data** and projects like **DBpedia**.
</details>

<details>
<summary><b>Q9.2</b> ⭐ What is an RDF triple? Give the data model. [2 marks]</summary>

- RDF represents every fact as a **subject – predicate – object** triple.
  - **Subject** — the entity being described (a URI)
  - **Predicate** — the property or relation (a URI)
  - **Object** — the value: either another resource (a URI) or a literal
- A set of triples forms a **directed labelled graph**: subjects and objects are
  nodes, predicates are the edges.
- Example: `(Anita, enrolledIn, DataScience)`.
</details>

<details>
<summary><b>Q9.3</b> ⭐ RDF vs RDFS vs OWL — which does what? [2 marks]</summary>

| | **RDF** | **RDFS** | **OWL** |
|---|---|---|---|
| Purpose | **represent data** as triples | add a **simple vocabulary/schema** | add **logic and reasoning** |
| Gives you | subject–predicate–object facts | classes, subclasses, properties, domain and range | restrictions, cardinality, disjointness, equivalence, inverse and transitive properties |
| Can it infer? | no | limited (subclass inheritance) | **yes** — a reasoner derives new facts and detects inconsistency |
| Use it when | you are **storing** facts | you need a **light taxonomy** | you must **enforce constraints** or **infer** |

**The exam phrasing:** *storing book data* → **RDF**. *Checking "every book must
have an author"* → **OWL**, because that is a constraint requiring reasoning.
</details>

<details>
<summary><b>Q9.4</b> ⭐ Case study: model papers, authors and conferences using RDF and OWL. [2 marks]</summary>

*This is the Mar 2026 Q5C answer pattern. Always answer in two halves — RDF for
the facts, OWL for the rules.*

**With RDF — represent the factual data.** Entities become resources linked by
triples:
```
(Paper1, hasAuthor,   Author1)
(Paper1, presentedAt, Conference1)
(Author1, affiliatedWith, University1)
```

**With OWL — define the semantics and constraints.**
- **Classes:** `Paper`, `Author`, `Conference`
- **Object properties:** `hasAuthor` (domain Paper, range Author),
  `presentedAt` (domain Paper, range Conference)
- **Constraints:** every `Paper` must have **at least one** `hasAuthor`
  (minimum cardinality 1); `Paper` and `Author` are **disjoint** classes;
  `hasAuthor` has the **inverse** property `authorOf`.
- A reasoner can then flag a paper with no author as inconsistent, and infer
  `authorOf` links automatically.
</details>

<details>
<summary><b>Q9.5</b> Case study: identify subjects, predicates and objects for a university system. [2 marks]</summary>

*The Feb 2026 Q6 pattern. Answer in three labelled lists, then the triples.*

- **Entities (subjects):** Student (Anita), Course (Data Science),
  Faculty (Dr. Rao), Department (Computer Science)
- **Properties (predicates):** `enrolledIn`, `taughtBy`, `memberOf`,
  `hasName`, `offeredBy`
- **Values (objects):** the course resource, the faculty resource, the
  department resource, and literals such as the name string

**Triples:**
```
(Anita,        enrolledIn, DataScience)
(DataScience,  taughtBy,   Dr_Rao)
(Dr_Rao,       memberOf,   ComputerScienceDept)
```
</details>

<details>
<summary><b>Q9.6</b> Why are URIs essential to the Semantic Web? [1 mark]</summary>

- A URI is a **globally unique name** for a resource. Two datasets that both use
  `http://dbpedia.org/resource/India` are demonstrably talking about the **same
  thing**, so their graphs can be **merged without manual reconciliation**.
- Plain strings cannot do this — "India" in one database and "India" in another
  might be a country, a film or a person.
</details>

<details>
<summary><b>Q9.7</b> Name three application areas of ontologies. [1.5 marks]</summary>

- **Information retrieval and search** — query expansion using the class
  hierarchy; semantic rather than keyword matching.
- **Data integration** — merging heterogeneous databases under a shared
  vocabulary (the Linked Open Data cloud, DBpedia).
- **Knowledge-based systems and reasoning** — biomedical ontologies, e-commerce
  product taxonomies, enterprise knowledge graphs powering Graph RAG.
</details>

---
---

# 10 · Module 14 — Retrieval-Augmented Generation

<details>
<summary><b>Q10.1</b> ⭐ What is RAG and what problem does it solve? [2 marks]</summary>

- **Retrieval-Augmented Generation:** before answering, the system **retrieves
  relevant documents** from an external store and puts them into the LLM's
  prompt, so the model answers **grounded in those documents**.
- Problems it solves:
  - **Hallucination** — the model invents plausible but false facts. RAG grounds
    it in retrieved evidence.
  - **Stale knowledge** — the model's training has a cutoff. Retrieval supplies
    **up-to-date** information without retraining.
  - **No access to private data** — company documents were never in training.
  - **No citations** — RAG can point at the source it used.
</details>

<details>
<summary><b>Q10.2</b> Describe the RAG pipeline end to end. [3 marks]</summary>

1. **Ingestion** — documents are loaded and **chunked** into passages.
2. **Embedding** — each chunk is converted to a vector and stored in a **vector
   database**.
3. **Query embedding** — the user's question is embedded with the same model.
4. **Retrieval** — nearest-neighbour / similarity search returns the top-k
   chunks, usually filtered by a **similarity threshold**.
5. **Augmentation** — the retrieved chunks are inserted into the prompt
   alongside the question.
6. **Generation** — the LLM answers using that context, ideally citing it.
</details>

<details>
<summary><b>Q10.3</b> ⭐ Why is chunk overlap used? [2 marks]</summary>

- Chunk boundaries are **arbitrary**. A sentence or an idea that straddles a
  boundary gets **split in half**, and neither half retrieves well or reads
  coherently.
- **Overlap** repeats the last few tokens of one chunk at the start of the next,
  so **context is preserved across the boundary** and no idea is orphaned.
- Cost: overlap **duplicates content**, increasing storage and the risk of near
  identical chunks being retrieved together, wasting context window.
- Typical: 10–20% of the chunk size.
</details>

<details>
<summary><b>Q10.4</b> ⭐ What competes for space in the LLM context window? [2 marks]</summary>

- Every LLM has a **fixed context window** measured in tokens. Everything must
  fit inside it:
  - the **system prompt / instructions**
  - the **user query**
  - the **retrieved chunks**
  - the **conversation history**
  - and the space **reserved for the generated answer**
- This is why retrieval is thresholded and top-k limited: adding more chunks is
  not free, and eventually crowds out the answer itself.
</details>

<details>
<summary><b>Q10.5</b> ⭐ Traditional (vector) RAG vs Graph RAG. [3 marks]</summary>

| | **Traditional / Vector RAG** | **Graph RAG** |
|---|---|---|
| Store | vector database of text chunks | **knowledge graph** of entities and relations |
| Retrieval | **semantic similarity** to the query | **traversal** of typed relationships |
| Strong on | "find me passages about X" | **multi-hop** questions — "who supervised the author of X?" |
| Weak on | questions needing several linked facts; it returns similar text, not connected facts | fuzzy, unstructured, semantic queries |
| Explainability | returns a passage | returns an explicit **path** through the graph |
| Build cost | low — chunk and embed | high — entity/relation extraction and curation |

Many systems use **both**: the graph for structure, the vector store for
free text.
</details>

<details>
<summary><b>Q10.6</b> What is Agentic RAG? [2 marks]</summary>

- A framework in which the LLM acts as an **agent** that *decides* how to
  retrieve, rather than a passive generator handed a fixed set of chunks.
- Components: an **LLM agent** orchestrating reasoning; a set of **tools**
  (vector search, graph query, web search, calculators); **memory**; and a
  **planning loop**.
- The agent can **reformulate** the query, retrieve **repeatedly**, judge whether
  the evidence is sufficient, and only then answer.
- Better on complex multi-step questions; costs more calls and more latency.
</details>

<details>
<summary><b>Q10.7</b> What is Multimodal RAG? [1 mark]</summary>

- Ingestion handles more than text: documents such as PDFs are broken down with
  **text extracted, images isolated, tables parsed**, and each modality is
  embedded (often into a shared space).
- Retrieval can then return an image or a table as evidence, and a multimodal
  model reasons over text and images together.
</details>

<details>
<summary><b>Q10.8</b> How is retrieval quality measured? Define precision and recall here. [2 marks]</summary>

- **Precision** = relevant chunks retrieved ÷ **total chunks retrieved**.
  "Of what I showed the model, how much was useful?" Low precision means
  **contextual noise**, which degrades generation quality and wastes the window.
- **Recall** = relevant chunks retrieved ÷ **total relevant chunks that exist**.
  "Of what was out there, how much did I find?" Low recall means the answer may
  be missing entirely.
- Trade-off: lowering the similarity threshold raises recall and lowers
  precision. `F1 = 2PR / (P + R)` balances them.
</details>

---
---

# 11 · Module 15 — Text Summarization

> **Mar 2026 gave all 6 marks here to pure theory** — classify three scenarios
> and justify. This is the single most likely place to be asked prose.

<details>
<summary><b>Q11.1</b> ⭐ Extractive vs abstractive summarization. [2 marks]</summary>

| | **Extractive** | **Abstractive** |
|---|---|---|
| How | **selects** existing sentences from the source and concatenates them | **generates new** sentences in its own words |
| Wording | verbatim from the document | may use words not in the document |
| Grammatical? | each sentence is, but the joins can be **incoherent** and pronouns may dangle | naturally fluent |
| Factual risk | **cannot hallucinate** — every word came from the source | **can hallucinate** facts |
| Difficulty | easier — a ranking problem | harder — a generation problem |
| Typical method | sentence scoring, MMR, graph ranking | seq2seq / transformer models |
</details>

<details>
<summary><b>Q11.2</b> ⭐ Classify the types of summarization by input and by user need. [3 marks]</summary>

**By number of documents:**
- **Single-document** — one document in, one summary out. Produces a headline,
  abstract or outline.
- **Multi-document** — a set of documents on the same event. Must **remove
  redundancy** and **resolve contradictions** across sources. Used for news
  aggregation.

**By user need:**
- **Generic** — summarises the overall content, with **no particular query**.
  It ignores user intent by design.
- **Query-focused (topic-based)** — tailored to a **specific information need**;
  effectively a form of **complex question answering**. It extracts only the
  parts relevant to the query and ignores the rest.
</details>

<details>
<summary><b>Q11.3</b> ⭐ Scenario drill — name the summarization type for each. [3 marks]</summary>

*This is the exact Mar 2026 Q7 format. Read the scenario, and ask two questions:
**how many documents?** and **is there a query?***

| Scenario | Type |
|---|---|
| A journalist uploads **one long report** and wants a **headline and a short abstract** | **Single-document, generic** |
| An analyst gives **15 articles about the same summit** and wants one overview | **Multi-document** |
| A researcher asks *"summarise the sections about **economic impact**"* | **Query-focused** |

**And the follow-up you will be asked:** *why won't one approach do for all
three?* — because the scenarios differ in **input structure** (one vs many
documents), **user intent** (no query vs an explicit query), and **output
requirement** (headline vs gist vs targeted answer). Generic summarization
ignores intent; query-focused summarization requires a query to exist;
multi-document summarization must additionally manage redundancy and
contradiction across sources.
</details>

<details>
<summary><b>Q11.4</b> ⭐ What is MMR and what problem does it solve? [2 marks]</summary>

- **Maximal Marginal Relevance.** A greedy sentence-selection criterion that
  balances **relevance to the query** against **redundancy with what has already
  been selected**.
- `MMR(s) = λ · sim(s, q) − (1 − λ) · sim(s, S)`
  where `q` is the query/topic and `S` is the set already chosen.
- **Problem solved:** picking sentences purely by relevance selects the **same
  fact restated** several times. The second term **penalises** a sentence for
  resembling the summary so far.
- **λ = 1** → pure relevance, maximum redundancy. **λ = 0** → pure novelty,
  possibly off-topic. In between, a diverse *and* relevant summary.
</details>

<details>
<summary><b>Q11.5</b> How do you justify an MMR selection in words? [2 marks]</summary>

*Marks are given for the reasoning, not the arithmetic. The template:*

> Although **S2** is more relevant to the topic (higher `sim(s,q)`), it is highly
> similar to the sentence already selected, so it is **redundant** and its
> `sim(s,S)` penalty is large. **S1** contributes **new, complementary
> information** and therefore scores higher under MMR. MMR deliberately trades a
> little relevance for **coverage and diversity**, which is what makes a summary
> informative rather than repetitive.

Always name **both** halves — relevance *and* redundancy — and say which one
decided the outcome.
</details>

<details>
<summary><b>Q11.6</b> What is ROUGE and what are its limitations? [2 marks]</summary>

- **ROUGE** — Recall-Oriented Understudy for Gisting Evaluation. It measures
  **n-gram overlap between a generated summary and one or more human reference
  summaries**.
- **ROUGE-N** — overlap of n-grams (ROUGE-1 unigrams, ROUGE-2 bigrams).
  **ROUGE-L** — longest common subsequence, which rewards word order.
- Mainly **recall-oriented**: how much of the reference the summary covers.
- **Limitations:** it rewards **surface overlap**, so a correct paraphrase scores
  badly and a fluent nonsense summary made of reference words scores well. It
  ignores **factuality, coherence and readability**, and depends heavily on which
  reference summaries you happen to have.
</details>

<details>
<summary><b>Q11.7</b> Name three applications of summarization. [1.5 marks]</summary>

- **News aggregation** — one overview from many outlets covering an event.
- **Headline and snippet generation** — for publishing and search results.
- **Meeting, email and report digests**; **scientific abstract generation**;
  **legal and medical document review**, where the volume makes full reading
  impossible.
</details>

<details>
<summary><b>Q11.8</b> What are the standard stages of an extractive summarizer? [2 marks]</summary>

1. **Content selection** — score every sentence for importance (position, cue
   phrases, topic-word overlap, centrality) and choose the best ones.
2. **Information ordering** — arrange the selected sentences into a coherent
   sequence, usually by original document order for a single document.
3. **Sentence realisation** — clean up: compress the sentences, fix dangling
   pronouns and broken references so the summary reads as text rather than a
   list.

MMR sits inside **stage 1**, adding the anti-redundancy term to the score.
</details>
