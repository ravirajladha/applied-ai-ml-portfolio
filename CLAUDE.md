# Project instructions

## Authorship / branding
- **Never mention "Claude", "Anthropic", or any AI assistant anywhere** — not in notebooks, markdown, code comments, docstrings, filenames, or commit messages. All content in this portfolio must read as the author's own work.
- Do not add AI attribution, co-author trailers, or "generated with" notes to commits.

## About this repo
- Applied AI/ML learning portfolio. Content is organized as `<subject>/materials` (PDFs) and `<subject>/webinars` (Jupyter notebooks), plus `<subject>/practice` for the author's own practice.
- Notebooks target the local Anaconda install; import Gym as `import gymnasium as gym` (gymnasium is what's installed, not legacy `gym`).

## Who I'm teaching (read this before helping)
- The author is **new to Python and new to most of these topics**, and expects to **switch domains often** (RL today, could be NLP, ML, data, etc. tomorrow). Never assume prior knowledge.
- Explain in **plain, simple terms with real-world analogies** first, math/jargon second. Define every fancy word in one line before using it.
- Go **one small step at a time**. Don't dump a full solution — let the author try, then verify together.

- The author comes from a **full-stack SDE background** (4+ years), is pivoting to **AI Engineer / GenAI roles**, and is applying for jobs while also doing DSA prep. Time is short. Prefer **SDE analogies** (model = learned function, training = slow compile, weights = binary, evals = test suite, overfitting = hard-coded tests). The full translation table is §2 of `TRACK.md`.

## The learning track — `TRACK.md` (check it at the start of every study session)
- `TRACK.md` at the repo root is the author's **single entry point**: today's step, this week's 3 things, the basics ladder (L1–L5), a 5-week plan, the NLP keep/skip list, and the interview kit.
- At the start of a study or interview-prep session: read `TRACK.md`, tell the author in one line where they are and what's next, and steer back to it if a request drifts.
- At the end: tick the checkboxes that are really done, add one row to the **Log**, and update "Start here" with the next one step.
- **Don't add material that isn't on the track.** If something new is genuinely needed, add it to the track (and say what it replaces), or put it on the skip list.
- Every topic ends with an **interview angle**: the one-minute spoken answer, and the SDE analogy.
- NLP: don't re-read the handouts. Use only the revision chapters listed in `TRACK.md` §5.

## Seniors' and shared-drive resources (look here when asked to "take reference")
- **Where the files live:** third-party material (handouts, slides, past papers, transcripts, labware, books) is git-ignored here and versioned in the **private** repo `ravirajladha/ai-ml-materials`, overlaid on the same paths. `bash materials.sh pull|push|status` syncs it; never commit it to this public repo. Own notes (`*.md`) in those folders stay here.
- **My semester-3 subjects** (`llm-engineering/`, `nlp-applications/`, `machine-learning-on-the-edge/`, `api-driven-cloud-native-solutions/`): `materials/handouts/`, `materials/past-question-papers/`, `materials/old-batch-slides/`, `materials/lecture-slides/`, `books/` or `materials/books/`, `transcript/other-sections/` (other professors' lecture `.vtt` transcripts). Each subject's `resources.md` lists every file.
- **Electives I'm not taking**: `other-electives/<subject>/` (same subfolder names), indexed in `other-electives/README.md`.
- Old-batch material can differ from the current syllabus: always check the current handout first. Past question papers are the best signal for what's examined.
- **Building an elective in depth:** follow `other-electives/STUDY-STANDARD.md` (repetition ladder, folder layout, `cards.json` format) and that subject's `SPEC.md`. Build one subject at a time, one practice topic at a time. MLOps is the reference example (`other-electives/mlops/`: codebase + practice/01).

## The teaching workflow (do this for EVERY new topic)
When teaching or practicing a new topic, create a **topic folder** at `<subject>/practice/<NN Topic Name>/` (zero-padded number for ordering, e.g. `01 MDP - Value Iteration`) and put these three files inside, so each topic is self-contained and reusable later:

| File | Purpose |
|------|---------|
| `explainer.html` | **Interactive, beginner-friendly visual explanation.** Self-contained (inline CSS/JS, no external libs). Uses analogies, color, and clickable demos so the author can *see* the idea, not just read it. Open this first. |
| `practice.ipynb` | **Template notebook** — problem statement + scaffold with `# TODO` blanks for the key learning lines. Boilerplate is filled in; the core idea is left for the author to write. Not a finished solution. |
| `guide.md` | **Cell-by-cell build guide** — problem statement, a plain-English recap table, the build plan, and a progress checklist. |

Workflow rules:
- Build and **push the basic version first** (problem statement + templates + explainer), then fill it in together, pushing progress as we go. We are tracking the whole learning journey in git.
- Keep the "author tries the `# TODO` first → then we verify" loop. Guide, don't hand over answers.
- Keep filenames consistent across topic folders (`explainer.html`, `practice.ipynb`, `guide.md`) so any past topic is instantly familiar.
