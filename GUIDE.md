# Repo Guide & Conventions

This is a personal portfolio repo for M.Tech coursework, mirroring the
subject/session structure used on the Taxila LMS so that notes, notebooks,
and slides accumulate in one trackable, public place over the semesters.

## Folder & naming conventions

- Subject folders: lowercase, hyphenated, no spaces
  (e.g. `natural-language-processing/`).
- Each subject contains:
  - `notes.md` — running notes / session log for that subject
  - `resources.md` — links to slides, readings, and PDFs hosted on Drive
    (heavy PDFs are never committed — see below)
  - `materials/` — slide decks and other course material (`.pptx`)
  - `webinars/` — webinar notebooks (`.ipynb`) and their accompanying data
    (`.xlsx`)
- `natural-language-processing/` is the working example — copy its layout
  when adding a new subject.

## What gets committed vs. linked

- `.pptx` and `.xlsx` are large/binary — they're tracked via **Git LFS**
  (`.gitattributes`). Run `git lfs install` once per machine before cloning
  or pushing such files.
- `.pdf`, `.html`, `.ipynb_checkpoints/`, `__pycache__/`, and `.DS_Store` are
  git-ignored — heavy PDFs (textbook chapters, scans, papers) live on Google
  Drive and get linked from the relevant subject's `resources.md` instead.

## Secrets

- Copy `.env.example` to `.env` and fill in your own API keys/tokens
  (e.g. for notebooks that call OpenAI, Hugging Face, or Kaggle APIs).
- `.env` is git-ignored — never commit real credentials. Only `.env.example`
  (with empty placeholder values) is tracked.

## Adding a new subject or session

1. Create `<subject-name>/` following the naming convention above.
2. Copy `notes.md`, `resources.md`, `materials/`, and `webinars/` from
   `natural-language-processing/` as a starting point.
3. Add the subject to the index table in the top-level `README.md`.
4. Link any heavy PDFs/slides hosted on Drive from that subject's
   `resources.md` rather than committing them.
