# Resume point — updated 2026-09-05 (exam is TOMORROW, 2026-09-06)

## ▶ START HERE TONIGHT

| Order | File | What to do |
|---|---|---|
| **1** | `MOCK-PAPERS.pdf` | **Sit Paper A blind, 150 min, clock running.** Two full 40-mark papers in the exact Apr-2025 shape, fresh numbers, solutions held back. This is the highest-value thing left. |
| **2** | `MOCK-PAPERS.pdf` → Rapid Drill | 18 short numericals covering everything the papers don't. Do the ones matching what you dropped. |
| **3** | `CHAPTER-HOMEWORK.pdf` | Every **Exercise / Try it & Test** slide from both decks, solved. HW8 first — its query is the same shape as the real Q3(c). |
| **4** | `formula-sheet.md` + Part B of `ACI-EC3-PostMidsem-Practice` | Print and tab. You are open book. |

**Audit done 2026-09-05:** the EC-2 sheet, the Module-3 supplement and the EC-3
post-midsem sheet were checked against the Apr 2025 paper and its marking
scheme. **Every figure re-computed independently and matched** — Bayes-net
(0.2268 / 0.7079 / 0.6471 / 0.5758), Forward & Viterbi trellises, Shapley
(30, 40, 50), the Core violation at {2,3}, Borda 2/1/0, the Vickrey and voting
blocks. Coverage matches the real paper question for question. **Nothing needed
correcting.** The only gap was that all three sheets print their solutions
inline, so none of them can test you — hence `MOCK-PAPERS`.

---

## Previous resume point — 2026-08-31

## THE PACK IS COMPLETE. Ch 1–14, the whole syllabus.

| File | Covers |
|---|---|
| `README.md` | plan, re-weighted from the past papers |
| `exam-analysis.md` | breakdown of all 3 past papers, mark weighting, priorities |
| `formula-sheet.md` | the official CS-1..CS-12 sheet + CS-13/14/15 blocks I added |
| `ch01-intro-agents.md` | Agents, PEAS, environments |
| `ch02-problem-solving-uninformed-search.md` | BFS/DFS/UCS/DLS/IDS |
| `ch03-informed-search-astar.md` | Greedy, A*, admissibility, consistency |
| `ch04-local-search.md` | Hill climbing, SA, beam |
| `ch05-genetic-aco-neuroevolution.md` | GA, ACO, CoDeepNEAT |
| `ch06-07-minimax-alphabeta-mcts.md` | Minimax, alpha-beta, MCTS + **past paper Q1 worked** |
| `ch08-09-logic-cnf-dpll-fol.md` | Prop logic, CNF, DPLL, FOL + **past paper Q2 and makeup Q1B worked** |
| `ch10-probabilistic-reasoning.md` | Bayes nets, D-separation, sampling |
| `ch11-markov-hmm-viterbi.md` | Markov, HMM, Forward, Viterbi + **past paper Q4 and Q5c worked** |
| `ch12-game-theory-noncooperative.md` | Maximin, mixed strategies, repeated games, backward induction, SPNE |
| `ch13-cooperative-gt-shapley-auctions-voting.md` | Core, Shapley, mechanism design, auctions, bargaining, voting |
| `ch14-responsible-ai-ethics.md` | Ethics, bias, FAT, Three Layers of Safety + **makeup Q3B worked** |

**Explainers exist for every chapter**, in `explainers/`. Fourteen chapters,
eleven explainer files (06/07 and 08/09 are merged).

**Five past-paper questions are now worked in full against their marking
schemes:** Q1 Connect-Three · Q2 CNF/DPLL · Q4 Viterbi · Q5c Tata Sky ·
the makeup FOL resolution · plus the makeup's 2.5-mark ethics question Q3B.

---

## What was built on 2026-08-31

**Ch 12 (CS#14) — non-cooperative game theory.**
Five elements · action vs strategy · game types · four representations ·
pure vs mixed strategies · **maximin/minimax and the saddle-point test** ·
**the Morra numerical worked to p = 7/12, V = −1/12** · the graphical
interpretation · repeated games and the five strategies (Hawk, Dove, **Grim**,
**Tit-for-Tat**, Tat-for-Tit) · FSM strategies · sequential games ·
**backward induction and SPNE with a worked non-credible-threat tree** ·
imperfect information and poker · assistance games.

> **⚠ Found and documented a typo in the deck.** Slide 35 prints the Morra leaf
> as `3p + 4(1−p)`; the leading minus is missing and it must be `−3p + 4(1−p)`.
> Proof is on the deck's own graph (slide 38): that line hits −3 at p = 1.

**Ch 13 (CS#15) — cooperative game theory.**
Coalitions, characteristic function, superadditivity · imputations ·
**the Core, with the empty-core proof** · **the Shapley value with all six taxi
permutations → (2, 5, 35)** · the four axioms · **the 45/45/10 board → 33.3 each,
solved both by symmetry and by pivotal counting** · mechanism design's three
pillars · strategy-proof vs truth-revealing vs the Revelation Principle ·
**Contract Net (Recognise → Announce → Bid → Award)** · auctions and the full
**Vickrey payoff matrix** · **Nash bargaining with the split-the-surplus
shortcut** · Rubinstein · **voting counted four ways on one election** ·
Condorcet paradox · Arrow vs Gibbard–Satterthwaite.

**Ch 14 (CS#16) — Responsible AI.** Nearly all image slides, so this was read
off the slide images directly. The CV-screener and healthcare case studies ·
bias and the proxy problem · FAT · the devil's-advocate section · who owns AI ·
the climate numbers · high-risk applications · **the Three Layers of AI Safety
(Alignment / Robustness / Corrigibility)** · ethics-by-design vs pro-ethical
design · explainability a priori vs a posteriori.

**Every Shapley figure in Ch 13 was recomputed independently and matched.**

---

## NEXT — there is no reading left. The remaining work is SPEED.

The exam is **open book**, 40 marks, 2.5 hours. You are not graded on recall.
You are graded on **executing a procedure fast** with your notes in front of you.

**In priority order:**

1. **Sit a timed mock of the Apr 2025 paper.** 150 minutes, notes open, phone
   away. It is in `materials/old question papers/`. That paper's answer key is
   included — mark it yourself afterwards. This is the single highest-value
   thing left to do, by a distance.
2. **Do the "You try" sections you have not attempted.** Each chapter has one,
   with answers hidden at the bottom. Attempt before opening. Priority order by
   mark weight: **ch11 → ch10 → ch08-09 → ch06-07 → ch13 → ch12**.
3. **Print `formula-sheet.md`.** It is the one page to have physically open.

**Ch 10 and Ch 11 have been self-checked and stuck** (Viterbi = max not sum;
v-structure dependent when the collider is observed). Those two are ~46% of the
marks and they are solid.

---

## The trap list — the things most likely to cost whole questions

- **Ch 11:** which way the transition matrix sums to 1 (the paper uses
  **columns = previous state**), and **normalise at t = 1 only**.
- **Ch 13:** the **cost-game sign flip** — `x(C) ≤ v(C)`, not `≥`.
- **Ch 13:** **Borda points are `m−1` down to 0** — for 3 candidates that is
  **2 / 1 / 0**, not 3/2/1.
- **Ch 12:** in backward induction, **read THAT player's own number** in the
  payoff tuple, not the first one.
- **Ch 12:** the deck's Morra sign typo (above).
- **Ch 10:** always write the **symbolic chain-rule expansion first** — the
  marking scheme gives 0.5 marks each for "query extraction" and "linearise the
  sequence" **before any arithmetic**.
- **Everywhere:** *"Assumptions made, if any, should be stated clearly at the
  beginning."* Free marks, and it protects ambiguous work.
