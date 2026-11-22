# Study standard — how every subject in this library is built

> One standard for every subject, so any subject feels familiar the moment it's opened.
> Aim: **production-level understanding, explained simply**, written for a software engineer moving into AI/ML.
> Each subject first gets a `SPEC.md` (the plan). Then subjects are built in depth **one at a time**, module by module.

---

## 1. The repetition ladder — every concept is met 5 times

Reading something once doesn't make it stick. Every concept in every subject goes through the same five rungs, in five
different forms, so the repetition never feels like re-reading:

```
 ① PICTURE        ② STORY             ③ HANDS             ④ SYSTEM             ⑤ RECALL
 diagram +        the subject's       notebook TODO:      where it lives in    flashcard + quiz +
 one-line         running scenario    you write the       the subject's        "say it in an interview";
 definition +     uses it to solve    1–3 key lines       codebase (real       revisited on day 1, 3, 7, 21
 analogy          a real problem                          files, real tests)   and in later modules' warm-ups
 explainer.html   SPEC + guide.md     practice.ipynb      codebase/            cards.json
```

Rules that make the repetition work:
- **Warm-up first.** Every module's `guide.md` starts with 3–5 cards from *earlier* modules. Old concepts keep coming back.
- **Same scenario all the way.** One company story per subject. Module 7 reuses the data, names and problem from module 1.
- **Same definition, same words.** A concept's one-line definition is written once (in `cards.json`) and reused word for word everywhere.

---

## 2. Folder layout per subject

```
other-electives/<subject>/
├── README.md            resource index (handouts, past papers, slides, labware, books): already exists
├── SPEC.md              the study spec: modules, scenario, codebase plan, exam + interview angle
├── cards.json           all flashcards for the subject (app-ready, see §5)
├── codebase/            one small real project that grows module by module (runs locally)
│   ├── README.md        how to run it + which module added which file
│   ├── src/  tests/  ...
└── practice/
    └── <NN Topic>/      one folder per module or topic: same three files as every practice topic in this repo
        ├── explainer.html   ① picture: interactive, self-contained, diagrams, analogies, a quiz at the end
        ├── practice.ipynb   ③ hands: problem statement + scaffold with # TODO lines, assert checks
        └── guide.md         ② story + warm-up + build plan + ⑤ recap checklist
```

---

## 3. What every module must contain

| Element | Where | Rule |
|---|---|---|
| One-line definition per concept | explainer + cards.json | ≤ 20 words, no undefined jargon |
| Real-world analogy | explainer | Prefer software-engineering analogies (cache, CI, load balancer, API contract) |
| ≥ 1 diagram per concept | explainer (inline SVG/HTML), guide (ASCII or mermaid) | If it has moving parts, draw it |
| Scenario step | guide.md | "In our company, this is the problem it solves on Tuesday morning" |
| Production box | explainer + guide | **How industry does it** (tools) · **What breaks in production** · **How you'd monitor it** |
| Interview box | guide | 1 question + the 60-second spoken answer |
| Exam box | guide | Which past-paper questions hit this topic (if papers exist) |
| Notebook TODOs | practice.ipynb | 1–3 short lines per concept; every cell ends with `assert` checks |
| Codebase change | codebase/ | Module adds or changes real files, with a test |
| Cards | cards.json | 5–12 cards per module |

**Depth levels** (go as far as the topic needs): **L1** picture & analogy → **L2** mechanics (how it works) → **L3** maths (only where the exam or the job needs it) → **L4** production (tools, failure modes, monitoring, cost).

---

## 4. Writing style

- Plain English first, jargon second. Define every term in one line before using it.
- Short sentences. Tables and diagrams over paragraphs.
- Every number traceable: either from the course material (cite the file in this folder) or worked out on the page.
- No walls of code: small cells, each paired with a plain-English explanation and visible output.

---

## 5. `cards.json` format (so a study app can read every subject the same way)

```json
[
  {
    "id": "mlops-01-003",
    "subject": "mlops",
    "module": 1,
    "concept": "Training-serving skew",
    "q": "What is training-serving skew?",
    "a": "When the data or code path used in production differs from the one used in training, so the model sees inputs it never learned from.",
    "analogy": "Testing your app on Chrome but users run it on an old Safari.",
    "kind": "definition | why | how | compare | numerical | interview",
    "tags": ["interview", "exam"],
    "source": "handouts/Older batch - MLOps ... HANDOUT.docx"
  }
]
```

- `id` = `<subject>-<module two digits>-<card three digits>`, stable forever (the app tracks progress by id).
- `a` holds the canonical one-line definition, reused word for word in explainers and guides.
- Spaced-repetition schedule the app should use: day 1 → 3 → 7 → 21 → 60.

---

## 6. Priority order for building in depth

Ranked by **usefulness for an AI engineer job + overlap with my own courses**:

| # | Subject | Why this rank |
|---|---|---|
| 1 | **MLOps** | Every production AI job needs it; builds on my SE4ML course. **Built first.** |
| 2 | ML System Optimisation | Inference speed and cost: overlaps LLM modules 4–5 |
| 3 | Conversational AI | Chatbots, dialogue, RAG: overlaps the LLM and NLP Applications courses |
| 4 | Multimodal Information Retrieval | Search, embeddings, RAG over images, audio and text |
| 5 | Speech Processing / Audio Analytics | Voice products (ASR, TTS); Audio Analytics has full labware |
| 6 | Graph Neural Networks | Recommendations, fraud detection |
| 7 | Social Media Analytics | Applied NLP, graph mining |
| 8 | FAccT ML (fairness, accountability, transparency) | Responsible AI: bias audits and explainability come up in interviews |
| 9 | AI and ML for Robotics | Strong labware, but ROS2 setup is heavy |
| 10 | 3D Computer Vision · Computational Photography · Computational Imaging | Vision specialisations |
| 11 | Computational Learning Theory | Mostly theory |
| 12 | Quantum Machine Learning | Niche |

Status of every subject: see the table in [`README.md`](README.md).
