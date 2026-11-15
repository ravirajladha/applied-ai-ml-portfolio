# SE4ML — End-Sem Revision

> **AIMLCZG546 · End Semester Exam — OPEN BOOK · 40% · 2.5 hours**
> The packs below were built **straight from the slides**, weighted the way the syllabus is weighted. The **Sep 2026 regular paper** has since been added, along with full model answers and two mock papers in its exact shape.

---

## 📝 The actual paper — [`endsem/`](endsem/)

| File | What it is |
|---|---|
| **[endsem/QUESTION-PAPER.pdf](endsem/QUESTION-PAPER.pdf)** | The **Sep 2026 End-Sem Regular** paper — 7 questions, 40 marks, 2.5 hours |
| **[endsem/SOLVED-PAPER.pdf](endsem/SOLVED-PAPER.pdf)** ⭐ | **Full model answers to all 7**, in the course's own vocabulary, each cross-referenced to a cheat-sheet **§** |
| **[endsem/PRACTICE-PAPER.pdf](endsem/PRACTICE-PAPER.pdf)** ⭐ | **Two complete mock papers (Sets A & B)** built from the slide notes, using the **same seven question archetypes** the real paper used — answers in collapsible boxes |

**What that paper turned out to be:** not one bare definition in it. Every question was *"here is a situation, apply the course vocabulary."* **12 of 40 marks were Kubernetes** (sequence-of-events + write the YAML), **12 more were architecture patterns** (microservices decomposition + Blackboard), and the remaining marks were Big-O, agree/disagree, and a six-lens Responsible-AI analysis.

**The seven archetypes — practise the format, not just the topic:**

| # | Archetype | Sep 2026 used it for |
|---|---|---|
| 1 | **Pick-and-justify** [4] | Big-O for four hospital tasks |
| 2 | **Trace the mechanism** [6] | what K8s does on `replicas: 1 → 5` |
| 3 | **Design the system** [6] | microservices + communication mechanisms |
| 4 | **Write the artefact** [6] | multi-container Pod YAML + kubectl commands |
| 5 | **Challenge the statement** [6] | agree/disagree ×3 |
| 6 | **Evolve the state** [6] | Blackboard contents at five events |
| 7 | **Six-lens analysis** [6] | Responsible AI over an agentic system |

---

## 📄 The packs

**Two kinds of pack.** The **cheat sheets** are what you *answer from* in the hall. The **question banks** are what you *practise on* beforehand — the paper is expected to be conceptual and scenario-based, so those are the only two formats in there.

| Pack | Covers | Weight |
|---|---|---|
| **[post-midsem/CHEATSHEET.pdf](post-midsem/CHEATSHEET.pdf)** ⭐ | **Sessions 9–16** — Implementation · Quality Assurance · Deployment · Responsible ML | **HIGH — study this first** |
| **[post-midsem/QUESTION-BANK.pdf](post-midsem/QUESTION-BANK.pdf)** ⭐ | **83 conceptual + scenario questions**, chapter by chapter, § numbers matching the cheat sheet | **HIGH — practise on this** |
| [pre-midsem/CHEATSHEET.pdf](pre-midsem/CHEATSHEET.pdf) | Sessions 1–7 — Foundations · Requirements · Architecture | lower |
| [pre-midsem/QUESTION-BANK.pdf](pre-midsem/QUESTION-BANK.pdf) | 31 conceptual + scenario questions on the same seven sessions | lower |

**How to use a question bank:** every answer is hidden inside a collapsed box. **Answer out loud or on paper first**, then open the box and mark yourself ✅ / 🟡 / ❌. Only revisit the **§** you missed — not the whole note. In the `.html` there is a **"Show all answers"** button; in the printed PDF every box is already open.

Each file has a matching `.html` (dark, searchable, with a jump-to sidebar) and a `.md` source.
**The `.md` is the single source of truth — never hand-edit the `.html` or `.pdf`.** Rebuild with:

```bash
python build_html.py --pdf
```

---

## 📚 The full notes (one file per slide deck)

Sitting in [`../materials/notes/`](../materials/notes/README.md) — one `.md` per session, written to be read on its own:

| Pre-midsem | Post-midsem ⭐ |
|---|---|
| S1 Foundations of ML Systems Engineering | S9 Implementation & Code Sharing |
| S2 From Models to Systems | S10 Time Complexity, Data Structures & OOP |
| S3 Requirements Engineering (GR4ML) | S11 Errors, Style, Refactoring, APIs & Packaging |
| S4 Quality Attributes & Architecture | S12 Quality Assurance, Testing & RAGAS |
| S5 Architectural Patterns (CQRS, RAG, Mono/Micro) | S13 Deployment — Docker & Kubernetes |
| S6 Event-Driven Architecture & ML Patterns | S14 Inference, Serving & Deployment Strategies |
| S7 Agentic AI & Coordination Patterns | S15 Responsible ML Engineering |
| *(S8 — no slides; the mid-term fell here)* | S16 Course Review |

**Use the notes to *understand*, use the PDFs to *answer*.** In an open-book exam you don't have time to read a note — you need the table.

---

## 🗓️ Five-day plan (today → Sunday)

The whole point is **post-midsem first**, because that is where the marks are.

| Day | Do this | Then |
|---|---|---|
| **Tue** | **Deployment** — Session 13 + 14 notes. The 4 deployment strategies and the Docker/K8s definitions are the highest-return pages in the course. | Cheat sheet §16–23 → then **question bank §16–23** |
| **Wed** | **Quality Assurance** — Session 12 notes: testing types, data validation gates, precision/recall, slicing, shadow/canary/A-B, RAGAS. | Cheat sheet §7–15 → then **question bank §7–15** |
| **Thu** | **Responsible ML** — Session 15: the six principles, explainability three-way split, safety categories, CIA. | Cheat sheet §24–31 → then **question bank §24–31** |
| **Fri** | **Implementation** — Sessions 9, 10, 11: Big-O, data structures, OOP-for-agents, PEP 8, SOLID, FastAPI, packaging. | Cheat sheet §1–6 → then **question bank §1–6** |
| **Sat** | **Pre-midsem sweep** — read the 10-page pre-midsem PDF **once**, properly. Then the **pre-midsem question bank** (31 questions, ~1 hr). | Finish with the **two cross-cutting scenarios** at the end of the post-midsem bank — answered out loud |
| **Sun** | **Exam.** Take **both PDFs printed**, plus the notes folder on a laptop if allowed. | — |

> If a day slips, **drop Friday, not Tuesday.** Implementation is the cheapest module to recover in the hall from an open book; deployment scenarios are not.

---

## ✂️ Explicit skip list — do NOT spend time on these

You cannot cover everything by Sunday, and you don't need to. **Skip:**

- **Instructor profile / consultancy slides** (S1 slides 3–5) — not examinable.
- **All the demo code files** (`bigonotation.py`, `travelagentapp.py`, `RAGAS_demo.py`, the PIMA simulator, the minikube demo). Know **what each demonstrates**, never the code itself.
- **The DevOps end-to-end video** (S13, marked *self-study*) — read the CI/CD lifecycle box in the S13 note instead.
- **Memorising the AI-regulations table** (S15, marked *self-study*) — learn the **one-line spectrum** only: *EU prohibits by risk tier · UK/Japan guide voluntarily · US is state-by-state · China is centralised · India is evolving.*
- **The full MLOps/LLMOps/AgentOps metrics grid** — learn the **three rows that differ most** (core focus, data type, key challenges) and the tool names. Don't memorise all 8 rows.
- **Deep Big-O maths.** You need the ladder and the log table, not proofs.
- **Writing Dockerfiles or K8s YAML from memory.** Recognise the keywords and what each does; the YAML is in the PDF if you need it.
- **Session 8** — there are no slides for it.

---

## 🎯 The three things most likely to decide the paper

1. **"Which deployment strategy would you use and why?"** — Basic / Ramped / Blue-Green / Canary, with the trade-off named.
2. **"Compare X and Y"** — traditional vs ML testing · containers vs VMs · monolith vs microservices · research vs production · MLOps vs LLMOps vs AgentOps · explainability vs interpretability vs transparency.
3. **"Agree or disagree, with justification"** — the mid-term used this format heavily. Answer plainly, then **restate the correct version in the course's own vocabulary**. Do not hedge; a hedged answer loses the justification mark.
