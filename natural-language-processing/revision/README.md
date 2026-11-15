# NLP (AIMLCZG530) — Exam Revision Pack

Session-wise notes built directly from **my own slide decks and handouts**
(`slides/NLP Session *.pptx`, `notes/NLP_Handout_Part1_Sessions_1-8.pdf`),
not from a generic textbook. Every worked number here is traceable to a slide.

Same shape as my ACI revision pack, so the habits carry over.

> ### ▶ Start here for the endsem
> **[`scheme-drill/`](scheme-drill/README.md)** — built from the **official
> question-paper structure**. It maps every module to its marks, shows that
> **~24 of 40 marks can be pure theory**, and holds the theory bank plus easy
> warm-up numericals the other two packs don't cover.
> Then: [`pre-midsem/`](pre-midsem/README.md) (Q1–Q2) ·
> [`post-midsem/`](post-midsem/README.md) (Q3–Q7).

## How to use this pack

| File | What it is | When to open it |
|---|---|---|
| `chNN-*.md` | The notes: concepts + **formula box** + **worked numericals** + "You try" | Main revision file |
| `explainers/chNN-*.html` | Click-around visual explainer, no maths wall | **Open this FIRST** for a topic I haven't touched |
| `formula-sheet.md` | Everything on one page | Final 30 minutes before the exam |

**Rule for numericals:** each pattern has ONE fully worked example, then 2–3
"You try" problems with the answer hidden at the bottom of the file. Attempt
first, check after. Reading a solved sum feels like learning and isn't.

## Chapter map — PRE-MIDSEM (Sessions 1–8)

| # | S | Topic | Numericals | 📖 Notes | 👀 Explainer |
|---|---|---|---|---|---|
| 1 | S1 | Intro to NLP — levels of language, ambiguity, applications, evaluation | Light | [ch01](ch01-intro-nlp.md) | [levels & ambiguity](explainers/ch01-levels-and-ambiguity.html) |
| 2 | S2 | **Vector semantics** — term-document & term-term matrices, **sparse vs dense**, dot product, cosine, TF-IDF | **Heavy** | [ch02](ch02-vector-semantics-tfidf.md) | [sparse vs dense](explainers/ch02-sparse-vs-dense-vectors.html) |
| 3 | S3 | Word embeddings — word2vec, skip-gram w/ negative sampling, CBOW, GloVe, analogies, bias | Medium | [ch03](ch03-word-embeddings-word2vec-glove.md) | [word2vec & GloVe](explainers/ch03-word2vec-skipgram-glove.html) |
| 4 | S4 | N-gram LMs — chain rule, Markov, MLE, add-1 smoothing, backoff, interpolation, perplexity | **Heavy** | [ch04](ch04-ngram-language-models.md) | [n-grams & perplexity](explainers/ch04-ngrams-smoothing-perplexity.html) |
| 5 | S5 | Neural networks & neural LMs — the unit, XOR, feedforward nets, softmax, neural LM | Medium | [ch05](ch05-neural-networks-neural-lm.md) | [neural nets & XOR](explainers/ch05-neural-nets-xor.html) |
| 6 | S6 | POS tagging — word classes, Penn Treebank, HMM tagging, **Viterbi**, MEMM | **Heavy** | [ch06](ch06-pos-tagging-hmm-viterbi.md) | [**the Viterbi drill**](explainers/ch06-viterbi-drill.html) |
| 7 | S7 | Neural / LLM / agentic POS tagging — Bi-LSTM-CRF, Transformer, BERT, prompting, agents | Theory | [ch07](ch07-neural-llm-pos-tagging.md) | [modern POS tagging](explainers/ch07-modern-pos-tagging.html) |
| 8 | S8 | LLM & prompt engineering — zero/few-shot, generative AI, transfer learning, fine-tuning | Theory | [ch08](ch08-llm-prompt-engineering.md) | [prompt / transfer / fine-tune](explainers/ch08-prompting-transfer-finetuning.html) |

**All 8 chapters and all 8 explainers are built.** Every explainer is a
self-contained HTML file — double-click it, no server and no internet needed.
Each one ends with a multiple-choice quiz that marks itself and explains why.

### The four explainers that do real work for you

| Explainer | What it actually does |
|---|---|
| [**Viterbi drill**](explainers/ch06-viterbi-drill.html) | Steps through **every cell** of the table one at a time — showing the candidates, then the max, then the emission. Five sentences to practise on, with backtrace. **Drill this one until it is automatic.** |
| [n-grams & perplexity](explainers/ch04-ngrams-smoothing-perplexity.html) | Live bigram count & probability tables from an editable corpus, an MLE ↔ add-1 toggle with a `V` slider, sentence scorer, perplexity calculator |
| [sparse vs dense](explainers/ch02-sparse-vs-dense-vectors.html) | Cosine playground with a live angle diagram, TF-IDF calculator, side-by-side sparse/dense vector strips |
| [word2vec & GloVe](explainers/ch03-word2vec-skipgram-glove.html) | One full SGNS training step (the "Ned Stark" numbers) with a learning-rate slider, stage by stage |

Every worked number in the explainers was checked against the slide values —
the Viterbi table reproduces `.21 / .0756 / .027216 / .005443` and the path
`Det Noun Verb Prep` exactly.

Post-midsem (Sessions 9–16) already has written notes in a different place —
see `../notes/parsing/` and `../notes/dependency-parsing/`. Those get folded into
this pack later as `ch09`+.

## Where the numericals actually live

If exam time is short, the three chapters that can *cost you marks by hand* are:

1. **Ch 6 — Viterbi.** Fill a tag × word table, backtrace. Always asked.
2. **Ch 4 — N-grams.** Bigram MLE table, add-1 smoothing, perplexity.
3. **Ch 2 — Cosine and TF-IDF.** Small, cheap, and very easy to lose to arithmetic.

Everything else is definitions, which are the cheapest marks in any paper.

## Source decks

| Session | Deck |
|---|---|
| 1 | `NLP Session 1 Natural Language Understanding and Generation.pptx` |
| 2–3 | `NLP Session 2 and 3 Vector semantics and Embedding [Autosaved].pptx` |
| 3 | `NLP Session 3- Word Embedding.pptx` |
| 4 | `NLP Session 4-Language modelling.pptx` |
| 5 | `NLP Session 5_Neural networks and Neural language Models.pptx` |
| 6 | `NLP Session 6- POS Tagging and its applications.pptx` |
| 7 | `NLP Session 7-Neural LLM Agentic approaches to POS tagging.pptx` |

Textbook throughout: **Jurafsky & Martin, *Speech and Language Processing*** —
Ch 6 (vector semantics), Ch 3 (n-grams), Ch 7 (neural nets), Ch 8 (POS/HMM).
