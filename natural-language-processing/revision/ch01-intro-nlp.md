# Ch 1 — Introduction to NLP: Levels of Language, Ambiguity, Applications
**Session 1** (deck: *NLP Session 1 — Natural Language Understanding and Generation*)

This chapter is **light on maths and heavy on cheap marks**. It is almost all
definitions, and definitions are the cheapest marks in any paper. The two things
that actually get *asked* are: **the six levels of language analysis** and
**the types of ambiguity, with an example of each**. Learn those two cold.

---

## 1. What is NLP?

> **NLP = analyse, understand and generate human languages just like humans do.**

- Explains linguistic theories, and uses those theories to build systems of
  social use.
- Started off as a branch of **Artificial Intelligence**.
- Borrows from **Linguistics, Psycholinguistics, Cognitive Science & Statistics**.
- The slogan on the slide: **make computers learn our language rather than we
  learn theirs.**

### Where it sits in the CS taxonomy
```
Computers
  └── Artificial Intelligence
        └── Natural Language Processing
              ├── Information Retrieval
              ├── Machine Translation
              └── Language Analysis
                    ├── Parsing
                    └── Semantics
```

### Why study NLP
- A **hallmark of human intelligence**.
- **Text is the largest repository of human knowledge**, and growing fast —
  emails, news, web pages, scientific articles, insurance claims, complaint
  letters, call transcripts, patents, court decisions, contracts.
- Market size: **USD 15.7 bn (2022) → USD 49.4 bn (2027)**, CAGR **25.7%**.

---

## 2. ⭐ The six levels of language analysis

Bottom-up. **This is the most-asked question in the chapter** — you must be able
to name all six *in order* and give the slide's own example for each.

```
        Pragmatic       <- how sentences are USED in a situation
        Discourse       <- how preceding sentences affect the next one
        Semantic        <- what words MEAN, combined into sentence meaning
        Syntactic       <- how words combine into correct sentences
        Lexical         <- listing and categorising words
        Morphological   <- how words are built from morphemes
```

| Level | Concerns | Slide's example |
|---|---|---|
| **Morphological** | How words are constructed from basic meaning units called **morphemes**. A **morpheme** is the primitive unit of meaning in a language. | *"friendly"* = noun *friend* + suffix *-ly*, which turns a noun into an adjective |
| **Lexical** | Listing words and categorising them | *friendful*, *beautyship* are **lexically incorrect**; *friendship*, *beautiful* are correct |
| **Syntactic** | How words are put together to form correct sentences; what structural role each word plays and which phrases are subparts of others | *"Large have green ideas nose"* — lexically correct, **syntactically incorrect** |
| **Semantic** | What words mean, and how those meanings combine into sentence meaning. **Context-independent** meaning. | *"Green ideas have large noses"* — syntactically correct, **semantically incorrect** |
| **Pragmatic** | How sentences are used in different situations, and how that use affects interpretation | *"She cuts banana with a pen"* — semantically correct, **pragmatically incorrect** (no useful meaning) |
| **Discourse** | How the immediately preceding sentences affect interpretation of the next | *"Chetana completed PhD at IIT Bombay. **She** is a Professor at BITS Pilani."* — resolving *she* needs the previous sentence |

> **Exam pattern to notice.** The examples form a **ladder**: each one is correct
> at the level below and broken at the level above. If a question hands you a
> weird sentence and asks "what is wrong with it?", walk up the ladder.

---

## 3. ⭐ Why is NLP hard? Ambiguity

The slide's summary of the difficulty:
```
L = Words + rules + exceptions
```
- **Ambiguity at all levels.**
- We speak **different languages**, and language is a **cultural entity** — so
  languages are not equivalent.
- **Highly systematic but also complex.**
- **Keeps changing** — new words, new rules, new exceptions.
- Sources (electronic text / printed text / acoustic speech signal) are **noisy**.

### The three types of ambiguity (with the slide's examples)

| Type | What varies | Example |
|---|---|---|
| **Structural** | Which words attach to which — the parse tree | *"Namrata thinks she understands me."* → *she* = Namrata, or someone else? <br> *"Visiting relatives can be a nuisance."* → the relatives who visit, or the act of visiting them? |
| **Grammatical** | The grammatical category / inflection | *"I go"* — *I* could be feminine or masculine in many languages. <br> *can* = Noun (container) / Modal auxiliary verb / Verb (*to can* = to pack) |
| **Lexical** | Which **word sense** is meant | **Polysemy**: *"understand"* (I get it) — related senses. <br> **Homonymy**: *bank* = river bank vs financial bank — unrelated senses |

> **Exam trap — polysemy vs homonymy.**
> **Polysemy** = one word, several **related** senses.
> **Homonymy** = same form, **unrelated** senses that just collided.
> Both are *lexical* ambiguity. This distinction comes back in Session 12
> (Word senses and WordNet).

Also mentioned: **situational ambiguity** (the HAL / *2001* examples) — the same
utterance means different things depending on the situation.

---

## 4. Applications and application areas

### NLP applications named on the slides
Question answering · Text categorisation / routing (e.g. customer emails) ·
Text mining · Machine (assisted) translation · Language teaching & learning ·
Usage checking · Spelling correction ("is that just dictionary lookup?" — no).

### Broader application areas
Text-to-speech & speech recognition · Healthcare · Natural-language dialogue
interfaces to databases · Information retrieval · **Information extraction** ·
Document classification · Document image analysis · **Automatic summarization** ·
Text proof-reading (spelling & grammar) · **Machine translation** · Fake news and
cyberbullying detection · Social media monitoring · **Plagiarism detection** ·
Look-ahead typing / word prediction · **Question answering** ·
**Sentiment analysis**.

### The HAL example — what full understanding would require
The *2001: A Space Odyssey* dialogue is used to list what a truly
language-understanding system needs:
- General speech and language **understanding and generation**
- **Politeness** — emotional intelligence
- **Self-awareness** — a model of self, including goals and plans
- **Belief ascription** — modelling others, reasoning about *their* goals and plans
- **Recognition of emotion** from speech, and **visual recognition** of emotions
  and faces

To reach that level we must be able to define, model, acquire and manipulate:
**knowledge of the world and of the agents in it**, **text meaning**, and
**intention**.

---

## 5. Who studies language, and how

| Discipline | Typical problems | Tools |
|---|---|---|
| **Linguists** | How do words form phrases and sentences? What constrains possible meanings? | Intuitions about well-formedness and meaning; mathematical models of structure and meaning |
| **Psycholinguists** | How do people identify sentence structure? How are word and text meanings identified? | Experiments measuring human performance; statistical analysis of observations |
| **Philosophers** | What *is* meaning? How do words acquire it and identify objects in the world? | Natural-language argumentation using intuitions about counter-examples; logic and model theory |
| **Computational linguists** | How is sentence structure identified? How can knowledge and reasoning be modelled? How can language accomplish tasks? | Algorithms, data structures; formal models of representation and reasoning; AI search and representation methods |

---

## 6. Representation: a first look at CFGs

A tiny preview of Session 9 (Parsing). The slide's grammar:

```
CFG Rules                Lexicon
  S  -> NP VP              Rice  : N
  NP -> N N                Flies : N, V
  NP -> N                  Like  : V, P
  VP -> V NP               Sand  : N
  VP -> V PP
  PP -> P NP

  NP = Noun Phrase,  VP = Verb Phrase,  PP = Prepositional Phrase
```
The classic sentence this grammar is built for: **"Rice flies like sand"** — which
is structurally ambiguous (is *flies* a noun or a verb?). Exactly the point of §3.

---

## 7. The organisation of an NLP system

Two halves, and every course topic sits in one of them:

| Half | What it does | Course topics that live here |
|---|---|---|
| **Natural Language Understanding (NLU)** | Text → meaning | POS tagging, parsing, word sense disambiguation, semantic web |
| **Natural Language Generation (NLG)** | Meaning → text | Language modelling, summarization, LLM generation |

---

## 8. Evaluating language understanding systems

The questions the slide says you must ask:
- What **metrics** to use?
- How to deal with **complex outputs** like translations?
- Are the **human judgments** measuring something real? Are they reliable?
- Is the sample of texts **sufficiently representative**?
- How **reliable or certain** are the results?

### The contingency table and the standard metrics

```
                      ACTUAL: yes        ACTUAL: no
    PREDICTED: yes    TP                 FP
    PREDICTED: no     FN                 TN

    Precision =  TP / (TP + FP)      of what I flagged, how much was right
    Recall    =  TP / (TP + FN)      of what was there, how much did I find
    Accuracy  = (TP + TN) / (TP + FP + FN + TN)
    F1        =  2 · P · R / (P + R)     harmonic mean of P and R
```

> **Why the harmonic mean and not the average?** Because it punishes imbalance.
> A system with P = 1.0 and R = 0.0 has arithmetic mean 0.5 but **F1 = 0**.

---

## 9. Tools and pre-processing

### Commercial
IBM Watson · Google Cloud NLP API · Amazon Comprehend.

### Open source
| Tool | Note |
|---|---|
| **NLTK** | The most popular Python library; what this course uses |
| **Stanford CoreNLP** | Java library from Stanford |
| **spaCy** | One of the newer open-source Python NLP libraries |
| **Gensim** | Specialised in topic modelling (e.g. LDA) |
| **GPT** | Autoregressive LM from OpenAI; an autocompleting program used mainly for predicting text |
| **AllenNLP** | Prototyping; provides modules like `Seq2VecEncoder`, `Seq2SeqEncoder` |
| **Berkeley Neural Parser** | High-accuracy parser, models for 11 languages |

Install: `pip install nltk` from the Anaconda terminal, or `!pip install nltk`
inside a Jupyter cell (the `!` runs a console command from a notebook cell).

### ⭐ The four pre-processing steps
```
1. Remove punctuation
2. Tokenization
3. Remove stop words
4. Lemmatize / Stem
```
> **Stemming vs lemmatization** (asked often): stemming chops affixes with rules
> and can produce a non-word (*studies → studi*); lemmatization uses a dictionary
> and returns a real dictionary form (*studies → study*).

---

## 10. Quick recall table (cover the right column)

| Question | Answer |
|---|---|
| The six levels of language analysis, bottom-up? | Morphological, Lexical, Syntactic, Semantic, Pragmatic, Discourse |
| What is a morpheme? | The primitive unit of meaning in a language |
| *"Green ideas have large noses"* is wrong at which level? | **Semantic** (it is syntactically fine) |
| *"Large have green ideas nose"* is wrong at which level? | **Syntactic** (it is lexically fine) |
| *"She cuts banana with a pen"* is wrong at which level? | **Pragmatic** (semantically fine, no useful meaning) |
| The three types of ambiguity? | Structural, Grammatical, Lexical |
| Polysemy vs homonymy? | Related senses of one word vs unrelated senses that share a form |
| Two halves of an NLP system? | NLU (text → meaning) and NLG (meaning → text) |
| The four pre-processing steps? | Remove punctuation, tokenize, remove stop words, lemmatize/stem |
| F1 formula? | 2PR / (P + R) |
| Most popular Python NLP library? | NLTK |

---

## 11. You try
*Attempt on paper before scrolling. Answers at the very bottom.*

**Q1.** For each sentence, name the **lowest level at which it is broken**, and
justify in one line:
(a) *"Colourless green ideas sleep furiously."*
(b) *"The beautyship of the sunset."*
(c) *"Boy the ran quickly."*
(d) *"I microwaved the constitution for eleven minutes."*

**Q2.** Classify the ambiguity in each, and name the sub-type where relevant:
(a) *"I saw the man with the telescope."*
(b) *"He went to the bank."*
(c) *"Book that flight."* (*book* = verb or noun?)

**Q3.** A named-entity recogniser is run on a document containing **40** true
entity mentions. It outputs **50** mentions, of which **30** are correct.
Compute precision, recall and F1.

**Q4.** In one sentence each, define **morpheme**, **discourse knowledge**, and
**pragmatic knowledge**.

---

## Next
**Chapter 2 — Vector Semantics.** The first real machinery of the course: turning
words into vectors, and the sparse-vs-dense distinction everything else rests on.
→ [`ch02-vector-semantics-tfidf.md`](ch02-vector-semantics-tfidf.md)

---
---
---

<!-- ANSWERS BELOW - stop scrolling until you have attempted -->

## Answers

**A1.**
(a) **Semantic.** Morphologically, lexically and syntactically well formed
(Adj Adj N V Adv), but the meanings cannot combine — ideas are not coloured and
do not sleep.
(b) **Lexical.** *beauty* + *-ship* is a morphologically plausible construction,
but *beautyship* is not a word of English — exactly the slide's own example.
(c) **Syntactic.** Every word is a real word (lexically fine), but the
determiner *the* cannot follow its noun in English word order.
(d) **Pragmatic.** Semantically interpretable — you can picture it — but the
utterance serves no sensible purpose in any situation.

**A2.**
(a) **Structural** ambiguity — does *with the telescope* attach to *saw* (the
instrument) or to *the man* (he was holding it)? Two different parse trees.
(b) **Lexical** ambiguity, sub-type **homonymy** — *bank* (riverside) and *bank*
(financial) are unrelated senses that happen to share a form.
(c) **Grammatical** ambiguity — the ambiguity is over the word's grammatical
category (verb vs noun), which is precisely what POS tagging in Session 6 exists
to resolve.

**A3.**
```
TP = 30            (correct outputs)
FP = 50 − 30 = 20  (output but wrong)
FN = 40 − 30 = 10  (true mentions missed)

Precision = 30 / 50 = 0.60
Recall    = 30 / 40 = 0.75
F1        = 2(0.60)(0.75) / (0.60 + 0.75) = 0.90 / 1.35 = 0.667
```
Note F1 = 0.667 sits **below** the arithmetic mean of 0.675 — the harmonic mean
always leans toward the weaker of the two scores.

**A4.**
**Morpheme** — the primitive unit of meaning in a language, from which words are
constructed (*friend* + *-ly* → *friendly*).
**Discourse knowledge** — knowledge of how the immediately preceding sentences
affect the interpretation of the next one, e.g. resolving *she* to a person named
in the prior sentence.
**Pragmatic knowledge** — knowledge of how sentences are used in different
situations and how that use affects their interpretation, e.g. recognising that
*"She cuts banana with a pen"* conveys nothing useful even though it parses and
means something.
