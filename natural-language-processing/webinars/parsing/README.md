# Session 9 — Parsing (Constituency, CFG, Chart & Probabilistic CKY)

Interactive study notes for **NLP Session 9 – Parsing**. Everything is pure Python
(no installs needed); an optional NLTK demo sits at the end.

**👉 Open first:** [`explainer.html`](explainer.html) — a visual, click-around
introduction (no maths). Best for a first-time look at the topic. Just double-click it
to open in your browser. Includes a step-through CKY chart, an ambiguity toggle, a
probability build-up, and a "how to not drown in the Python" guide.

**Then run:** [`constituency_parsing.ipynb`](constituency_parsing.ipynb) — the hands-on notebook.

## What's inside
1. Why parse? — applications (sentiment, relation extraction, QA, MT, speech)
2. Constituency vs. Dependency — the two views of structure
3. Context-Free Grammars (CFG) + phrase categories (NP, VP, PP, …)
4. Top-down vs. Bottom-up parsing — a bottom-up recogniser you can watch run
5. Chart parsing — caching partial results, the `•` dot / active-arc idea
6. **CKY recogniser** from scratch (triangular chart)
7. **PCFG** — rule probabilities, `P(tree) = ∏ P(rule)`, consistency
8. **Probabilistic CKY** — the *"The flight includes a meal"* slide example, coded
   with back-pointers (reproduces the slide's `P ≈ 2.304e-08` and best tree)
9. **Chomsky Normal Form** — why CKY needs it + a binariser
10. Problems with PCFGs — no lexicalisation / no context
11. Parser evaluation — precision / recall / F1 (PARSEVAL) on constituent brackets

## Run it
```bash
jupyter notebook webinars/parsing/constituency_parsing.ipynb
```
Then run cells top to bottom. Every code cell is self-contained.

Next session (10) is **Dependency Parsing** — the other view of structure:
[`../dependency-parsing/arc_eager_parser.ipynb`](../dependency-parsing/arc_eager_parser.ipynb).
