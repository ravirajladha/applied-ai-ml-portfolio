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
