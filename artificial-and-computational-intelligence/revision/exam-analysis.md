# Past Paper Analysis — what actually gets asked

Based on the three papers in `materials/old question papers/`:

1. **ACI – Apr 2025 – Endsem regular (with answers)** — the real thing, 40 marks
2. **EC3_Sample1** — EC3 Makeup sample paper, 40 marks
3. **EC3_SolvedSamples** — faculty's "previous year sample problems" deck

---

## THE HEADLINE: it is an OPEN BOOK exam

Both papers state it explicitly:

> *Nature of Exam: **Open Book*** · Weightage: **40%** · Duration: **2.5 Hours**

**This changes the whole strategy.** You are not being tested on recall — you are
being tested on whether you can **execute a procedure under time pressure** with
your notes in front of you.

What that means concretely:
- **Stop trying to memorise formulas.** Print `formula-sheet.md`.
- **What you cannot look up is speed.** A Viterbi trellis takes 15 minutes if
  you have done it three times, and 45 if you haven't. With 40 marks in 150
  minutes, that gap is the whole exam.
- **The worked examples in these notes ARE your exam resource.** Every chapter's
  "You try" section exists to buy you that speed.

---

## Structure of the real paper (Apr 2025)

**5 questions · 40 marks · answer all.**

| Q | Topic | Chapter | Marks |
|---|---|---|---|
| Q1 | Connect-Three game tree, static evaluation, **Minimax** | **Ch 6/7** | **9** |
| Q2 | Propositional logic → **CNF** → **DPLL** | **Ch 8** | **7** |
| Q3 | **Bayesian net** + CPTs + **D-separation** + joint query | **Ch 10** | **9** |
| Q4 | **HMM** — transition & emission matrices + **Viterbi** | **Ch 11** | **8** |
| Q5a | Admissible but **not** consistent — with example | Ch 3 | 2 |
| Q5b | **BFS** evaluation (time, space, optimality, completeness) | Ch 2 | 2 |
| Q5c | Markov model — missing probabilities + sequence likelihood | **Ch 11** | **3** |

Note the shape: **four big applied questions (7–9 marks each) plus one
short-answer question**. There is no essay. Almost everything is a calculation.

---

## Combined mark weighting across both papers (80 marks total)

| Chapter | Marks | Share | Status |
|---|---|---|---|
| **Ch 10 — Bayesian Networks** | **19** | **~24%** | ✅ built |
| **Ch 11 — Markov / HMM / Viterbi** | **~18** | **~22%** | ✅ built |
| **Ch 8/9 — Logic, CNF, DPLL, Resolution** | **11** | ~14% | ✅ built |
| **Ch 6/7 — Minimax / Alpha-Beta** | **9** | ~11% | ✅ built |
| Ch 1 — Agents, PEAS, AI concepts | 7 | ~9% | ✅ built |
| Ch 3 — A*, admissibility/consistency | 6 | ~8% | ✅ built |
| Ch 2 — Search, BFS, forward/backward | 4.5 | ~6% | ✅ built |
| Ch 14 — Responsible AI / ethics | 2.5 | ~3% | ✅ built |
| Ch 4 — Local search | 2 | ~3% | ✅ built |
| **Ch 5 — GA / ACO / Neuroevolution** | **0** | **0%** | ✅ built |
| **Ch 12/13 — Game theory / Shapley / auctions** | **0** | **0%** | ✅ built |

### **Ch 10 + Ch 11 together are ~46% of the marks.**

Both were on the "never touched" list. **Both are now built and self-checked.**

> **Status as of 2026-08-31: every chapter in this table is built.** Nothing in
> this file is a to-do list any more — it is now a *weighting* guide. Use it to
> decide **which "You try" sections to drill first** and **how many minutes to
> budget per question in the mock**, not what to read next.

---

## Two honest caveats about the zero-mark chapters

**Ch 5 (GA / ACO / Neuroevolution) scored 0 across all three papers.** I built it
before seeing the papers. It is not wasted — it is examinable content and the
ACO numerical is very mechanical — but **it is the last thing you should revise**,
not the first.

**Ch 12/13 (game theory, Nash, Shapley, auctions, voting) also scored 0 — but do
not skip these.** The papers are from **2024-25**, and your slide deck was
generated **16-Aug-2026** and contains CS#14, CS#15 on exactly this material.
If that content is **new to the syllabus this session**, it has never had a
chance to appear on a past paper — and new content is *more* likely to be
examined, not less. Treat the zero as "no evidence", not "evidence of absence".

---

## Recurring question formats — learn the phrasing

These exact instructions appear repeatedly. They tell you what the marker wants.

| Phrase | What it means for you |
|---|---|
| *"Strictly follow the approach as discussed in class only"* (Viterbi) | Use the **slide method**, not a textbook variant. Show the trellis. |
| *"Assume all events... are equally likely to occur except those explicitly specified"* | Any CPT the question doesn't give you gets **0.5**. Don't invent numbers. |
| *"Depict them with neat diagrams **in addition to** tabular representation"* | **Draw the diagram AND the table.** Marks are allocated to both. |
| *"If there are any ties, assume alphabetical tiebreaking"* | State your tiebreak rule in A*/search traces. |
| *"Assumptions made if any, should be stated clearly at the beginning"* | Write your assumptions first. Free marks, and it protects ambiguous work. |
| *"Vague answers will not be awarded marks"* | Give **numbers and named rules**, not prose. |
| *"with a relatable real world case study"* | Every concept answer needs a **concrete example**, not just a definition. |

---

## The marking schemes give away the structure

The Apr 2025 paper includes its own marking scheme. Copy this structure in your
answers:

**Q1 (game tree, 9 marks)**
```
Level 1 expansion              1 mark
Level 2 expansion              2 marks
Static evaluation values       3 marks    <- the single biggest sub-chunk
Minimax on the tree            2 marks
Best path highlighted          1 mark
```

**Q3 (Bayes net, 9 marks)**
```
Network structure              2 marks
CPTs (crop yield 0.5, rest 1.5) 2 marks
D-separation: diagram 1.5, removal of evidence 0.5, result+justification 1  = 3
Query extraction 0.5, linearise the sequence 0.5, chain rule + computation 1 = 2
```

> **Read that Q3 breakdown again.** *"Query extraction"* and *"linearise the
> sequence"* are worth **0.5 marks each — just for writing down the query
> symbolically and expanding the chain rule before you compute anything.**
> Always write the symbolic expansion first. It is free marks even if the
> arithmetic goes wrong.

**Q5 (short answers)** — the scheme literally lists the bullet points expected.
For BFS: *time complexity · space complexity · optimality · completeness*. Four
items, 2 marks. **Answer in a list, not a paragraph.**

---

## Specific things the papers ask that these notes already cover

| Question | Where it is answered |
|---|---|
| "Admissible but not consistent — numerical example" (Q5a, 2 marks) | **`ch03` §5** — your slides' own Exercise 2 has `h(S)` admissible but the `S→A` arc inconsistent. That IS the answer. |
| "BFS evaluation" (Q5b, 2 marks) | **`ch02` §7** — the four-row complexity table |
| "Hill climbing p = 0.2, expected runs for random restart?" (makeup Q1c) | **`ch04` §5(a)** — expected restarts = **1/p = 5** |
| "PEAS of a voice assistant" (makeup, 3 marks) | **`ch01` §4** — the 4-move method for an unseen task |
| Prior / rejection / likelihood weighting on the Flu network | **`ch10` §10** — the solved-samples deck uses **the identical network** |
| "Joint distribution as it factorizes" (makeup Q4a) | **`ch10` §5** — BN chain rule |
| D-separation proof with justification | **`ch10` §8** — the three patterns |
| "How can learning agents adapt to new environments without compromising safety and ethical standards in high-stakes applications?" (makeup Q3B, 2.5 marks) | **`ch14` §11** — worked in full. It is the **Three Layers of AI Safety** slide: *adapt to new environments* = **Robustness**, *without compromising safety* = **Alignment**, plus **Corrigibility** and the high-risk applications list. |

The solved-samples deck's Bayesian question is **literally the Flu / Fever /
FoodPoison / Viral network** with the same CPTs already worked in `ch10`.

---

## Revised priority order

All fourteen chapters are built. This is now the order to **drill the
"You try" sections** in, and roughly how to budget time in a timed mock:

**1. Ch 11 — Markov, HMM, Forward, Viterbi** ← *~22% of marks*
**2. Ch 10 — Bayesian networks, D-separation, sampling* ← *~24%*
**3. Ch 8/9 — Propositional logic, CNF, DPLL, Resolution, FOL** ← *~14%*
**4. Ch 6/7 — Minimax, Alpha-Beta, MCTS** ← *~11%*
**5. Ch 12/13 — Game theory** ← *0% historically, but new syllabus content*
**6. Ch 14 — Responsible AI** ← *~3%, cheap marks*
**7. Ch 1–5** ← revise from the "two-minute recall cards" only.

**The highest-value single action left is a timed mock of the Apr 2025 paper**,
150 minutes with notes open. Reading is no longer the bottleneck; speed is.
