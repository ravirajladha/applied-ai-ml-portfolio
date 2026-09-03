# Natural Language Processing — Notes & Reading Index

Your single starting point for every NLP topic. Open the **explainer** first (visual,
no maths), then the **notes**, then run the **notebook**.

## How this is organized
- **`notes/<topic>/`** — the stuff you *read*: `explainer.html` (visual first-look) + `README.md` (written notes).
- **`webinars/<topic>/`** — the stuff you *run*: the Jupyter `.ipynb` notebook.
- **`materials/`** — the original slide decks / PDFs.
- **`practice/<NN Topic>/`** — your own from-scratch practice (explainer + template notebook + guide).

> Convention for future topics: same three filenames every time — `explainer.html`,
> `README.md`, and one notebook — so any past topic is instantly familiar.

## Exam revision pack — PRE-MIDSEM (Sessions 1–8)

Built the same way as the ACI pack: chapter notes with a formula box, one fully
worked numerical per pattern, and "You try" problems whose answers are hidden at
the bottom of each file. **Start at [`revision/README.md`](revision/README.md).**

| # | S | Topic | 👀 Explainer (open first) | 📖 Notes |
|---|---|-------|---|---|
| 1 | S1 | Intro to NLP — levels of language, ambiguity, evaluation | [levels & ambiguity](revision/explainers/ch01-levels-and-ambiguity.html) | [ch01](revision/ch01-intro-nlp.md) |
| 2 | S2 | **Vector semantics — sparse vs dense, cosine, TF-IDF** | [sparse vs dense](revision/explainers/ch02-sparse-vs-dense-vectors.html) | [ch02](revision/ch02-vector-semantics-tfidf.md) |
| 3 | S3 | Word embeddings — word2vec, skip-gram/SGNS, CBOW, GloVe | [word2vec & GloVe](revision/explainers/ch03-word2vec-skipgram-glove.html) | [ch03](revision/ch03-word-embeddings-word2vec-glove.md) |
| 4 | S4 | N-gram language models — MLE, smoothing, backoff, perplexity | [n-grams & perplexity](revision/explainers/ch04-ngrams-smoothing-perplexity.html) | [ch04](revision/ch04-ngram-language-models.md) |
| 5 | S5 | Neural networks & neural LMs — the unit, XOR, softmax | [neural nets & XOR](revision/explainers/ch05-neural-nets-xor.html) | [ch05](revision/ch05-neural-networks-neural-lm.md) |
| 6 | S6 | POS tagging — HMM, **Viterbi**, MEMM | [**the Viterbi drill**](revision/explainers/ch06-viterbi-drill.html) | [ch06](revision/ch06-pos-tagging-hmm-viterbi.md) |
| 7 | S7 | Neural/LLM/agentic POS tagging — Bi-LSTM-CRF, BERT | [modern POS tagging](revision/explainers/ch07-modern-pos-tagging.html) | [ch07](revision/ch07-neural-llm-pos-tagging.md) |
| 8 | S8 | LLM & prompt engineering, transfer learning | [prompt / transfer / fine-tune](revision/explainers/ch08-prompting-transfer-finetuning.html) | [ch08](revision/ch08-llm-prompt-engineering.md) |
| — | — | Everything on one page | — | [formula-sheet](revision/formula-sheet.md) |

Explainers are self-contained HTML — double-click to open, no server or internet
needed. Each one ends with a self-marking quiz.

## Endsem quick packs ⭐ start here

| Pack | Marks | Files |
|---|---|---|
| 🔴 **[POST-midsem](revision/post-midsem/README.md)** | **30 of 40** | [cheatsheet](revision/post-midsem/CHEATSHEET.pdf) · [practice paper](revision/post-midsem/PRACTICE-PAPER.pdf) · [solved](revision/post-midsem/SOLVED-NUMERICALS.pdf) |
| 🟡 [PRE-midsem (Q1 & Q2 only)](revision/pre-midsem/README.md) | 10 of 40 | [cheatsheet](revision/pre-midsem/CHEATSHEET.pdf) · [solved](revision/pre-midsem/SOLVED-NUMERICALS.pdf) |

Endsem Q1/Q2 are pre-midsem; **Q3–Q7 are all post-midsem**. Weight your time
accordingly. Pre-mid only ever tests **Laplace smoothing, a neural-LM forward
pass, and HMM Viterbi/Forward** — chapters 1, 2, 3, 7, 8 have never appeared.

## Exam revision pack — POST-MIDSEM (Sessions 9–15) ⭐ 30 of 40 marks

Q3–Q7 of the endsem are **all post-midsem — 75% of the paper**, and every one has
a numerical core. Little notes + **every past-paper numerical solved**, built
from the six question papers in `notes/question papers/`.

| Open this | What it is |
|---|---|
| 🧠 **[CHEATSHEET.pdf](revision/post-midsem/CHEATSHEET.pdf)** | **Read this first.** One page per chapter — the theory you actually need, in plain English |
| 📝 **[PRACTICE-PAPER.pdf](revision/post-midsem/PRACTICE-PAPER.pdf)** | **Then do this.** 3 full mock sets of Q3–Q7, exact exam format, fresh numbers |
| 📝 [PRACTICE-PAPER.html](revision/post-midsem/PRACTICE-PAPER.html) | Same on screen — answers hidden until you click |
| 📘 **[SOLVED-NUMERICALS.pdf](revision/post-midsem/SOLVED-NUMERICALS.pdf)** | The reference — every past-paper numerical worked in full (47 pp) |
| 📘 [SOLVED-NUMERICALS.html](revision/post-midsem/SOLVED-NUMERICALS.html) | Same on screen, dark, sticky contents sidebar |
| 🗺 [README](revision/post-midsem/README.md) | Exam map, today's plan, how to rebuild |

Covers: Parsing (top-down, chart, **PCFG probability**) · Dependency
(**arc-eager**, **Chu-Liu-Edmonds MST**) · **Self-attention & multi-head** ·
**Lesk WSD & cosine sense selection** · **RDF/OWL** · **RAG token budget &
precision** · **MMR & ROUGE**.

## Topics — post-midsem (with notebooks)

| # | Topic | 👀 Explainer (open first) | 📖 Notes | ▶ Notebook |
|---|-------|---------------------------|----------|------------|
| 9 | **Parsing** — Constituency, CFG, Chart & Probabilistic CKY | [explainer.html](notes/parsing/explainer.html) | [README](notes/parsing/README.md) | [constituency_parsing.ipynb](webinars/parsing/constituency_parsing.ipynb) |
| 10 | **Dependency Parsing** — Transition-Based (Arc-Eager) | [explainer.html](notes/dependency-parsing/explainer.html) | [README](notes/dependency-parsing/README.md) | [flow (basic)](webinars/dependency-parsing/dependency_parsing_flow.ipynb) · [arc_eager_parser.ipynb](webinars/dependency-parsing/arc_eager_parser.ipynb) |

## Session log

- _Date_ — Lab Session 1: intro to tokenization & embeddings
