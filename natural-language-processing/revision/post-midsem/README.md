# NLP Post-Midsem — Exam Pack

**AIMLCLZG525 · End-Semester Test · Open Book · 40 marks · 2.5 hours**
**Q3–Q7 are all post-midsem = 30 of 40 marks = 75% of the paper.**

## Three files, in this order

| # | File | What it is | What you do |
|---|---|---|---|
| **1** | 🧠 **`CHEATSHEET`** (16 pp) | **Learn the theory here.** One page per chapter: what it's for, the words defined, the recipe, a tiny example, the trap | **READ first** — 5 min per chapter |
| **2** | 📝 **`PRACTICE-PAPER`** (29 pp) | 3 mock sets of Q3–Q7 in exact exam format, fresh numbers | **DO this** — 45 min per set |
| **3** | 📘 **`SOLVED-NUMERICALS`** (47 pp) | Every **real past-paper** question worked in full | **LOOK UP** when stuck |

Each exists as `.pdf` (print) and `.html` (screen, dark, answers hidden until
you click) plus the `.md` source.

> **If you only have a few hours:** read the CHEATSHEET chapter → immediately do
> that question in the PRACTICE-PAPER → check. Repeat per chapter. Don't read
> SOLVED-NUMERICALS cover to cover.

## Today's loop

```
CHEATSHEET Ch 11 (5 min)  ->  PRACTICE Set A Q4  ->  mark it
CHEATSHEET Ch 15 (5 min)  ->  PRACTICE Set A Q7  ->  mark it
CHEATSHEET Ch 14 (5 min)  ->  PRACTICE Set A Q6  ->  mark it
CHEATSHEET Ch 12 (5 min)  ->  PRACTICE Set A Q5  ->  mark it
CHEATSHEET Ch 9,10        ->  PRACTICE Set A Q3  ->  mark it
then Sets B and C against a clock
```
That order is deliberate — easiest marks first.

## What's covered

| Q | Marks | Topic | Session | Numericals drilled |
|---|---|---|---|---|
| 3 | 6 | Parsing / Dependency | 9, 10 | Top-down parse table · bottom-up chart · **PCFG probability** · **arc-eager trace** · **Chu-Liu-Edmonds MST** |
| 4 | 6 | Contextual embeddings | 11 | **Weighted sum of value vectors** · **multi-head concat × W_O** · **full self-attention** |
| 5 | 6 | WordNet + WSD | 12 | **Lesk overlap** · **cosine sense selection** · homonymy/polysemy/synset |
| 6 | 6 | Semantic Web / RAG | 13, 14 | **RDF triples** · RDF-vs-OWL · **derived inference** · **token budget** · **precision** |
| 7 | 6 | Summarization | 15 | **MMR** · summarization types · **ROUGE-2** |

## Rebuilding

```bash
python build_html.py          # HTML only
python build_html.py --pdf    # HTML + PDF  (needs Chrome or Edge)
```
Edit the `.md` files — they are the source of truth. Never hand-edit the
`.html` or `.pdf`.

> **Note:** if a PDF is open in a viewer, Windows locks it and the rebuild
> silently keeps the old copy. Close it first.

## Sources and verification

Built from **your own question papers** in `../../notes/question papers/` —
Feb 2026 regular (answers), Mar 2026 makeup (answers), Oct 2024 regular
(answers), one undated regular, and the sample Q&A set — plus the Session 9–15
slide decks in `../../slides/`.

**Every numerical was recomputed independently** and agrees with the official
answer keys: both Viterbi tables, both PCFG parse probabilities, the
Chu-Liu-Edmonds MST (brute-forced against all valid spanning arborescences), the
self-attention walkthrough, the cosine sense selections, the MMR scores, the
ROUGE-2 count and the RAG arithmetic. Practice-paper and cheat-sheet numbers are
**fresh** and were verified the same way.

## Pre-midsem

Chapters 1–8 with interactive explainers live in [`../`](../README.md).
