# ACI (AIMLCZG557) — Exam Revision Pack

Chapter-wise notes built directly from **my own slide decks**
(`materials/ACI Pre midsem.pdf`, `materials/ACI Post midsem and formula.pdf`),
not from a generic textbook. Every worked number here is traceable to a slide.

## Sit a paper before you read anything else

| File | What it is |
|---|---|
| **`MOCK-PAPERS.md`** / `.pdf` | **Two full 40-mark EC-3 papers you can sit blind**, exact Apr-2025 shape, fresh numbers, solutions held back — plus an 18-item rapid numerical drill. The other sheets print their answers inline and so cannot test you. |
| **`CHAPTER-HOMEWORK.md`** / `.pdf` | Every **Exercise / Try it & Test** slide from both decks, question as printed + full worked solution. |

Rebuild either with `python build_html.py --pdf` (the `.md` is the source of
truth; never hand-edit the `.html`/`.pdf`).

## How to use this pack

Each chapter has up to three files:

| File | What it is | When to open it |
|---|---|---|
| `chNN-*.md` | The notes: concepts + **formula box** + **worked numericals** + "You try" | Main revision file |
| `explainers/chNN-*.html` | Click-around visual explainer, no maths wall | **Open this FIRST** for a topic I haven't touched |
| `practice/` | Only where code genuinely helps | Optional |

**Rule for numericals:** each pattern has ONE fully worked example, then 2–3
"You try" problems with the answer hidden at the bottom of the file. Attempt
first, check after. Reading a solved sum feels like learning and isn't.

## Chapter map

Pre-midsem (CS#1–CS#8):

| # | Chapter | Numerical weight | Status |
|---|---|---|---|
| 1 | Intro to AI, Agents, PEAS, Environment types | Light | **BUILT** |
| 2 | Problem solving as search, Uninformed search (BFS/DFS/UCS/DLS/IDS) | Heavy | **BUILT** |
| 3 | Informed search — Greedy Best-First, A*, admissibility, consistency | Heavy | **BUILT** |
| 4 | Local search — Hill Climbing, Simulated Annealing, Beam | Medium | **BUILT** |
| 5 | Genetic Algorithms, ACO, Neuroevolution (DeepNEAT / CoDeepNEAT) | Heavy | **BUILT** (was untouched) |
| 6 | Adversarial search — game trees, Minimax | Heavy | **BUILT** |
| 7 | Alpha-Beta pruning, Monte Carlo Tree Search (UCB1) | Heavy | **BUILT** |

Post-midsem (CS#9–CS#16):

| # | Chapter | Numerical weight | Status |
|---|---|---|---|
| 8 | Logical agents — Wumpus, propositional logic, TT-entailment, resolution | Heavy | **BUILT** |
| 9 | First-Order Logic — quantifiers, unification, forward/backward chaining | Medium | **BUILT** |
| 10 | Probabilistic reasoning — Bayes, Bayesian Nets, D-separation, sampling | Heavy | **BUILT** (was untouched) |
| 11 | Markov models, MDP, HMM, Forward algorithm, Viterbi | Heavy | **BUILT** (was untouched) |
| 12 | Game theory — payoff matrix, maximin, mixed strategies, repeated games, SPNE | Heavy | **BUILT** (was untouched) |
| 13 | Cooperative GT — Core, Shapley value, auctions, bargaining, voting | Heavy | **BUILT** (was untouched) |
| 14 | Responsible AI — ethics, bias, FAT, Three Layers of AI Safety | Theory only | **BUILT** + **makeup Q3B worked** |

## PLAN v2 — re-weighted from the past papers

**Read `exam-analysis.md` first.** Three past papers are now in
`materials/old question papers/`, and they change the priorities significantly.

Two facts that matter most:
- The exam is **OPEN BOOK**, 40 marks, 2.5 hours. You are graded on *executing
  procedures fast*, not on recall. These notes are your exam resource.
- **Ch 10 + Ch 11 are ~46% of the marks.** Both were on your untouched list.

**Priority order for what is left:**

| Priority | Chapter | Share of marks | Why |
|---|---|---|---|
| **1** | **Ch 11 — Markov / HMM / Forward / Viterbi** | **~22%** | Biggest gap. Appeared on BOTH papers. Never studied. |
| **2** | **Ch 8/9 — Logic, CNF, DPLL, Resolution, FOL** | ~14% | Whole 7-mark question every time |
| **3** | **Ch 6/7 — Minimax, Alpha-Beta, MCTS** | ~11% | The 9-mark Q1 on the real paper |
| 4 | Ch 12/13 — Game theory, Shapley, auctions | 0% historically | BUT likely new syllabus content — do not skip. **BUILT** |
| 5 | Ch 14 — Responsible AI | ~3% | Cheap marks, one hour. **BUILT** |
| 6 | Ch 5 — GA / ACO / Neuroevolution | **0%** | **BUILT** |

**Ch 1–14 are all built and verified — the whole syllabus.** What is left is not
reading, it is **speed**: a timed mock of the Apr 2025 paper, and the "You try"
sections you have not attempted yet.

## Formula sheet

`formula-sheet.md` — everything on one page, matching the "Quick Revision –
Formulas / Notations" appendix in the post-midsem deck (slide pages 92–98).

## Past papers

`materials/old question papers/` holds all three papers, and `exam-analysis.md`
is already re-weighted around them:

- `ACI - Apr 2025 - Endsem regular with answers.pdf` — the real thing, with its
  own marking scheme
- `EC3_Sample1.pdf` — the EC3 makeup sample
- `EC3_SolvedSamples.pdf` — the faculty's previous-year solved problems deck

Four of those questions are worked in full inside the chapter notes: **Q1
Connect-Three** (ch06-07), **Q2 CNF/DPLL** and the **makeup FOL resolution**
(ch08-09), **Q4 Viterbi** and **Q5c Tata Sky** (ch11).
