# The plan — writing this paper across ~10 sessions

## The one command to start every session

Paste exactly this, nothing more:

```
Continue the review-summarization paper. Read paper/PLAN.md, then
paper/EXPERIMENT_FACTS.md. Tell me which session we are on and quiz me
before we write anything.
```

That is deliberately short. Two files, ~600 lines total, is all the context a
new session needs. Do **not** paste the notebook, the code, or old chat
history — that is what burns tokens for no gain. Everything a session needs to
know is in those two files, and we update them as we go.

---

## The deal (read this part twice)

You said you want to be made to study. Here is what that means in practice, and
I will hold to it:

**I will not write a section until you have answered its questions.**

Not as a punishment — because it does not work otherwise. If I write the
Related Work section for you, you will have a nice paragraph and no idea why
those papers are in it. If you answer three questions first, badly, in your own
words, then we write it together, you will still know it in a year. The first
version being wrong is not a problem. Not having a version is the problem.

Rules I am holding myself to:
- **Small reading.** Never more than ~6 pages of a paper per session, and I
  will tell you exactly which pages. You do not read papers front to back.
- **Answer in your own words, badly.** "I think ROUGE counts word overlap and
  that is bad when summaries are short?" is a *good* answer. It shows me where
  the gap is. Copy-pasted correctness teaches nothing.
- **You may say "I do not know."** Then I explain it in plain language with an
  analogy, and we move on. That is a legitimate answer and costs you nothing.
- **No session without the gate.** If you skip the reading, tell me and we do a
  10-minute version of it together. We do not skip it silently.

Why this paper is worth the effort: you have a genuinely interesting result.
"A pretrained model scored worse than returning the first sentence" is the kind
of finding people remember, and you found it by accident and then explained it.
That is what research is. Most people never get that far.

---

## Where things stand

| | |
|---|---|
| Branch | `paper/review-summarization` (local only, nothing pushed) |
| Location | `natural-language-processing/assignments/assignment-2/paper/` |
| Build | `cd paper && ./build.sh` → `main.pdf` |
| Editor | VS Code, open the `paper/` folder, save to rebuild |
| Scope decision | **Write up existing results only.** No new training runs. |
| Team repo | This folder is **excluded** from the sync to Sumanth's repo |

---

## Session log

- [x] **Session 1 — scaffolding** *(2026-08-09)*
      Branch, folder, IEEE skeleton, 10 section files, 15 reference PDFs
      downloaded, `references.bib` written, MiKTeX installed, VS Code
      configured, `EXPERIMENT_FACTS.md` extracted from the notebook,
      abstract drafted. Builds to 2 pages.

- [x] **Session 2 — Data + Experimental Setup** *(2026-08-09)*
      Both sections written. Quiz answered: ROUGE-2 counts bigrams, a 4-word
      reference has 3 of them. Settled both open questions — `TEAM_UPDATE.md`
      now carries the notebook's ROUGE numbers, and the training wall-clock is
      **unrecoverable** (no `trainer_state.json`, empty `_checkpoints/`), so
      the paper reports none. Build hardened: intermediates go to `.build/`
      after a stale `main.aux` silently broke every `\ref`. Paper is 3 pages.

      *Carried forward into the paper:* a 4-word reference has 3 bigrams, so
      ROUGE-2 on one example can only be 0, 0.333, 0.667 or 1.0. The metric is
      four steps, not a smooth ruler. That is the seed of Section 7.2 — it is
      why our 0.0448 must never be printed beside a news benchmark's 0.20.

- [x] **Session 3 — Introduction** *(2026-08-09)*
      Written, with the three contributions stated explicitly and a Scope
      paragraph that declares the study's limits up front rather than hiding
      them in Limitations.
      *The framing to keep hold of:* fine-tuning did not teach the model about
      food. It taught it **the shape of the answer**. Pretraining gives fluent
      sentence-shaped summaries; our references are four-word headlines, so a
      fluent model in the wrong shape scores below a one-line heuristic. Form,
      not knowledge. This is the same insight as the 3-bigram observation from
      Session 2, pointed at the model instead of at the metric.

- [x] **Session 4 — Related Work** *(2026-08-09)*
      Four themed paragraphs rather than a list: the encoder--decoder lineage,
      pretraining and its benchmarks, opinion summarization, and evaluation.
      *Two load-bearing points placed here deliberately:*
      (a) prior systems are reported on news corpora whose references are
      paragraphs or at least full sentences — ours are four-word headlines, so
      absolute ROUGE is not comparable. Stated here so Section 7.2 can lean on
      it without re-arguing.
      (b) MeanSum and Bražinskas both emit **one fluent paragraph** per
      product. We emit per-review summaries plus a structured aspect list,
      because a fluent paragraph is exactly the format in which a minority
      complaint disappears. That is the difference our arsenic finding depends
      on.

- [x] **Session 5 — Method** *(2026-08-09)*
      Written from a close read of `aggregate.py` and `aspects.py`, which
      turned up **two facts nobody had written down** (now in
      `EXPERIMENT_FACTS.md` §7b):
      1. **The map--reduce ceiling is raised, not removed.** The reduce step
         re-enters the same 256-token encoder, so it saturates at ~40--50
         reviews. The demo uses 60. Declared in the paper as an implementation
         limitation, with hierarchical reduce named as the fix.
      2. **The displayed verdict is a template**, not end-to-end generation —
         mood phrase by threshold, plus top-5 aspect lists, plus the reduce
         step's sentence quoted. The paper says so explicitly.
      Both were found only by reading the code rather than trusting the docs.

- [ ] **Session 6 — Results + the main figure**
      *File:* `sections/06-results.tex`, plus a plot into `figures/`
      *Read first:* nothing. This is a making session.
      *Task:* build the ROUGE comparison table and one clean figure. Also
      **resolve the training-time discrepancy** (README says ~50 min,
      TEAM_UPDATE says ~112 min — we cannot print both).
      *Also:* delete the `\nocite{*}` line from `main.tex` once real `\cite`
      commands are live.

- [ ] **Session 7 — Analysis** ← *the important one*
      *File:* `sections/07-analysis.tex`
      *Read first:* `refs/faithfulness-maynez-2020.pdf`, **abstract + section
      1**, and `refs/summeval-fabbri-2021.pdf`, **abstract only**.
      *Answer before we write:*
      1. Our model turned "offensive gas producer!!!" into "a great treat!".
         Is that a *hallucination*, or a different kind of error? Name it.
      2. SummEval found ROUGE agrees poorly with human judgement. Does that
         destroy our result, or not? Defend your answer.
      3. The baby formula case: why did the star average hide the arsenic
         complaints?
      *Budget two sessions if it needs them.* This section is the paper.

- [ ] **Session 8 — Limitations + Conclusion**
      *Files:* `sections/08-limitations.tex`, `sections/09-conclusion.tex`
      *Answer before we write:*
      1. Name the single biggest weakness of this paper without looking at
         `EXPERIMENT_FACTS.md`.
      2. If a reviewer had one objection, what would it be?

- [ ] **Session 9 — Revision pass**
      Read the whole thing top to bottom out loud. Rewrite the abstract last,
      once you know what the paper actually says. Check every number against
      `EXPERIMENT_FACTS.md`. Kill repetition between Results and Analysis.

- [ ] **Session 10 — Polish and decide**
      Figures, spacing, column balance, final build. Then decide together:
      does this stay a personal artefact, go on your GitHub, or get cleaned up
      for a student workshop?

---

## Rules for keeping sessions cheap

1. **`EXPERIMENT_FACTS.md` is the only source of numbers.** If a number is not
   in it, do not put it in the paper — add it to the facts file first, with
   where it came from.
2. **One section per session.** Sections live in separate files precisely so a
   session only ever opens one small file.
3. **Update this file at the end of every session** — tick the box, note
   anything that changed. This file *is* the memory between sessions.
4. **Never re-read `assignment2.ipynb`.** It is 200 KB. It has already been
   distilled into the facts file.
5. **Commit at the end of each session** so progress is never lost.

---

## Open questions to settle as we go

- ~~Training time: ~50 min or ~112 min?~~ **Closed, Session 2.** Neither is
  recoverable; the paper reports no wall-clock. See `EXPERIMENT_FACTS.md`.
- ~~ROUGE numbers: `TEAM_UPDATE.md` quotes an older run.~~ **Closed, Session
  2.** `TEAM_UPDATE.md` now carries the notebook's numbers, with a note.
- Do we want a BERTScore run to complement ROUGE? It would strengthen the
  evaluation, but it is a new experiment and we said no new experiments.
  *(Decide at Session 7)*
