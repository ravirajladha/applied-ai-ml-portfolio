# Interview preparation — journey and roadmap

A running log of what's built, what's next, and the conventions to follow, so this can be picked up months from
now without re-deciding anything.

Started: **31 July 2026** (the night before an AI/ML interview).

**Published at:** https://ravirajladha.github.io/applied-ai-ml-portfolio/interview-preparation/
(GitHub Pages, `master` branch, root path, `.nojekyll` so files serve verbatim). Any new `.html` under
`interview-preparation/` is published automatically on push — `.gitignore` has an exception for that folder.
When you add a new `.md`, also add it to the `FILES` array in `index.html` so it appears on the hub.

---

## Where things stand

| # | File | Subject | Status | Questions |
|---|------|---------|--------|-----------|
| — | `top-100-questions.md` | Broad theory across all areas | ✅ Done | 100 |
| — | `coding-questions.md` | Python, NumPy, pandas, from-scratch, sklearn, SQL, PyTorch | ✅ Done | 60 |
| — | `flashcards.html` | 100 flip cards, each with an inline SVG diagram | ✅ Done | 100 |
| — | `index.html` | Web hub — renders every `.md` in-page on mobile | ✅ Done | — |
| — | `models-explained.md` | All 14 models at four increasing depths | ✅ Done | 14 models |
| — | `quick-revision-cheatsheet.md` | Last-30-minutes revision | ✅ Done | — |
| 1 | `machine-learning.md` | Classical ML deep dive | ✅ Done | 80 |
| 2 | `deep-learning.md` | Neural nets, backprop, CNN, RNN, training | ✅ Done | 82 |
| 3 | `nlp.md` | Text processing → embeddings → Transformers → LLMs/RAG | ⬜ Not started | target ~70 |
| 4 | `deep-rl.md` | MDPs, Bellman, Q-learning, DQN, policy gradients | ⬜ Not started | target ~55 |
| 5 | `probability.md` | Distributions, Bayes, expectation, common puzzles | ⬜ Not started | target ~45 |
| 6 | `statistics.md` | Estimation, hypothesis testing, A/B tests, regression stats | ⬜ Not started | target ~45 |
| 7 | `aics.md` | Search, heuristics, CSP, logic, planning, game trees | ⬜ Not started | target ~45 |
| 8 | `seml.md` | MLOps, testing ML, CI/CD, monitoring, drift, model governance | ⬜ Not started | target ~50 |

Each subject file maps to a folder in this repo, so the coursework and the prep stay in sync:

| Prep file | Repo folder |
|---|---|
| `nlp.md` | `natural-language-processing/` |
| `deep-rl.md` | `deep-reinforcement-learning/` |
| `aics.md` | `artificial-and-computational-intelligence/` |
| `seml.md` | `software-engineering-for-machine-learning/` |
| `machine-learning.md`, `deep-learning.md`, `probability.md`, `statistics.md` | cross-cutting, no single folder |

---

## Suggested order for the remaining files

Ordered by interview value, not by syllabus order:

1. ~~**`deep-learning.md`**~~ — done 31 Jul 2026.
2. **`nlp.md`** — highest current market value; every AI/ML JD now has a Gen AI section. **Do this next.**
   Note: `deep-learning.md` Q71–Q72 covers attention and why Transformers replaced RNNs, and deliberately stops
   short of Q/K/V internals — pick those up in `nlp.md` rather than repeating them.
3. **`seml.md`** — MLOps questions appear in almost every round above fresher level, and almost nobody prepares them.
4. **`statistics.md`** + **`probability.md`** — do them together; they overlap and both show up in analytics-leaning rounds.
5. **`deep-rl.md`** — narrower in interviews, but it's coursework and it's genuinely differentiating when it comes up.
6. **`aics.md`** — mostly academic/exam value (search, logic, planning) rather than interview value.

---

## Conventions to keep (so the files stay consistent)

Established in `machine-learning.md` — match it exactly:

- **Format per question:**
  1. `**Qn. The question**` with ⭐ for high frequency, ⭐⭐ for near-guaranteed.
  2. A blockquote (`>`) containing **the spoken answer** — the sentence you'd actually say first, in plain words.
  3. The explanation: 3–8 lines, math only where it's genuinely asked, tables for comparisons.
  4. `**They'll follow up with:**` *"the chained question"* → the answer. This is the highest-value part; interviews
     are decided on the second and third question, not the first.
- **Contents table** at the top with anchor links, grouped into numbered sections.
- **A rapid-fire table** at the end — one-line answers to the quick-succession questions.
- **A closing "what to do with this file"** section with a concrete study method, not just "revise well".
- Plain English before jargon; define every term in one line before using it. Beginner-friendly, matching the
  rest of this repo.
- No filler. If a question isn't actually asked in interviews, leave it out.

---

## Ideas parked for later

- **`system-design-ml.md`** — "design a recommendation system / fraud detection / search ranking". Asked from
  mid-level upward, and completely different in shape from the theory questions.
- **`behavioural.md`** — STAR-format answers for the project narration, conflict, failure and "why this company"
  questions. Currently only a short bonus section at the end of `top-100-questions.md`.
- **`case-studies.md`** — 10 end-to-end worked problems (framing → metric → features → model → deployment),
  which is how senior rounds are actually run.
- **A per-subject flashcard export** (question on one line, answer on the next) for phone revision.
- **`mistakes-log.md`** — after each real interview, log the questions that were actually asked and the ones
  that were fumbled. Over two or three interviews this becomes more valuable than everything else here.

---

## How to resume

Pick the next file from the order above, follow the conventions section, and update the status table at the top
of this file when it's done. If a real interview happens in between, add the questions that were actually asked
to `mistakes-log.md` first — real questions beat predicted ones.
