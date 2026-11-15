# NLP Comprehensive Exam — Official Scheme Drill

**AIMLCLZG525 · Open Book · 40 marks · 2.5 hours**

Built from the **official question-paper structure** the course shared
(`Comprehensive Examination — Question Paper Structure`), cross-checked against
all four past papers in `../../notes/question papers/`.

---

## The official scheme, as issued

| Q | Module | Topic / question type | Marks |
|---|---|---|---|
| 1 | **2 & 3** | M2 Vector Semantics — **Problem** · M3 Language Models — **Problem** · Neural Language Models — **Problem** | 5 |
| 2 | **5 & 6** | M5 POS Tagging — **Problem** · M6 Hidden Markov Models — **Problem** | 5 |
| 3 | **9 & 10** | M9 Statistical Parsing — **Problem** · M10 Dependency Parsing — **Problem / Theory / Application** (e.g. building a dependency tree) | 6 |
| 4 | **11** | Contextual Embeddings — **Problems and/or Theory** | 6 |
| 5 | **12 & 13** | M12 Word Sense & WordNet — **Problems and/or Theory** · M13 Semantic Web & Ontology — **Application / Case Study** | 6 |
| 6 | **14** | Retrieval-Augmented Generation — **Problem and/or Theory** | 6 |
| 7 | **15** | Text Summarization — **Problem and/or Theory** | 6 |
| | | **TOTAL** | **40** |

---

## ⚠️ The finding: "only numericals are asked" is **not true**

The word **Theory** appears in the official scheme for **five of the seven
questions**. Read the marks column carefully:

| Question type in the scheme | Modules | Marks |
|---|---|---|
| 🔢 **Problem only** — numerical guaranteed | 2, 3, 5, 6, 9 | **10 marks + part of Q3** |
| ⚖️ **Problem *and/or* Theory** — either, or both | 10, 11, 12, 14, 15 | **~21 marks** |
| 📝 **Application / Case study** — *no numerical exists* | 13 | **~2–3 marks** |

**So roughly 24 of 40 marks can legally be pure prose.** Our existing packs
(`../post-midsem/`, `../pre-midsem/`) drill the *numericals* to death. This
folder closes the theory half.

### The past papers confirm it

| Paper | Question | What it actually was |
|---|---|---|
| Feb 2026 | Q4 Contextual embeddings | (a) 1.5 **theory** + (b) 1.5 **theory** + (c) 3 numerical |
| Feb 2026 | Q7 Summarization | 3 numerical (MMR) + 1 + **2 marks pure justification** |
| Mar 2026 | Q5 WordNet + Semantic Web | **6 of 6 marks pure theory** — no arithmetic at all |
| Mar 2026 | Q7 Summarization | **6 of 6 marks pure theory** — classify 3 scenarios and justify |
| Mar 2026 | Q4 Multi-head | (a) 1.5 theory + (d) 1 theory + 3.5 numerical |
| Oct 2024 | Q4a Dependency | **3 marks** compare-and-contrast table, no numbers |

A whole 6-mark question has already been answered with **zero calculation**,
twice. If you walk in with formulas only, those are the marks you lose.

### ⚠️ Second finding: Q1 may contain Vector Semantics

`../pre-midsem/README.md` says chapters 2 and 3 "have never appeared in Q1 or
Q2" — that was inferred from four past papers, and it was true of those papers.
**The official scheme overrides it:** it explicitly lists *Module 2: Vector
Semantics — Problem* inside the 5-mark Q1. TF-IDF, cosine similarity and PPMI
are now live. They are in `SIMPLE-NUMERICALS` §1. They are five minutes of work
each — do not skip them.

---

## The two files

| # | File | What it is |
|---|---|---|
| **1** | 📝 **`THEORY-BANK`** | **The gap-filler.** ~60 theory questions in exam wording, module by module, answers hidden until you click. This is the new material. |
| **2** | 🔢 **`SIMPLE-NUMERICALS`** | Deliberately *easy* warm-up sums — one clean pass per module before you attempt the real past-paper ones |

Each exists as `.md` (source), `.html` (dark, click to reveal) and `.pdf`.

## How to use it, given the clock

```
Per module:  SIMPLE-NUMERICALS  (10 min, builds confidence)
             THEORY-BANK        (10 min, say the answer OUT LOUD first)
             then the real past-paper question in ../post-midsem/
```

Answer **out loud, in your own words, before clicking**. A wrong answer in your
own words is worth more than a correct one you read. That is the whole point of
the hidden `<details>` blocks.

### Order, by marks-per-minute

```
1. Module 15  Summarization      6 marks   pure recall, has been 100% theory
2. Module 11  Contextual embed   6 marks   half theory, half one weighted sum
3. Module 14  RAG                6 marks   theory + division
4. Module 12  WordNet + 13 SW    6 marks   definitions + RDF triples
5. Module 9/10 Parsing           6 marks   hardest numericals — do last
6. Module 2/3 + 5/6              10 marks  drilled already in ../pre-midsem/
```

## Rebuilding

```bash
python build_html.py          # HTML only
python build_html.py --pdf    # HTML + PDF  (needs Chrome or Edge)
```
The `.md` files are the source of truth. Close any open PDF first — Windows
locks it and the rebuild silently keeps the old copy.

## Related

- [`../pre-midsem/`](../pre-midsem/README.md) — Q1 & Q2 numericals, every past paper solved
- [`../post-midsem/`](../post-midsem/README.md) — Q3–Q7 numericals + practice paper
- [`../`](../README.md) — full chapter notes and interactive explainers

## Verification

Every numerical in `SIMPLE-NUMERICALS` was computed independently before being
written down. The theory answers are drawn from the Session 9–15 slide decks in
`../../slides/`, the handout `../../notes/NLP_Handout_Part2_Sessions_9-end (3).pdf`,
and the official answer keys in `../../notes/question papers/`.

> **Open-book note:** the equations inside the handout PDFs are *images*, not
> text — `Ctrl-F` will never find them. The self-attention formulas
> `SelfAttention(Q,K,V) = softmax(QKᵀ/√d_k)V` and the multi-head projection are
> on **page 45–46 of Part 2**. Tab those pages before you go in.
