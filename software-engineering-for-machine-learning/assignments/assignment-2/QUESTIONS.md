# Questions for you — Assignment II

Everything in the PDF is implemented, run and verified. These are the things **only you can
answer**. Read at your leisure and reply; nothing is blocked in the meantime.

---

## Q1 — What exactly is the group number? (affects the filename)

The PDF says the notebook must be named `<Group no>.ipynb`.

Assignment I's `submission_details.json` recorded the group as **`G049`**, with the `G`
prefix. I have named the notebook **`049.ipynb`**.

**Which do you want?**

- **A.** `049.ipynb` (current)
- **B.** `G049.ipynb`
- **C.** something else — tell me the exact string

Same question applies to the final upload, which the PDF says must be `<groupid>.docx`
or `<groupid>.pdf`.

---

## Q2 — Group member names and BITS IDs

The PDF requires a filled-in table inside the notebook. Right now it has placeholders in
`049.ipynb` (first markdown cell):

| Sl. No | BITS ID | Name | Contribution (Qualitative) | % |
| --- | --- | --- | --- | --- |
| 1 | `<FILL BITS ID>` | `<FILL NAME>` | Production package design — data ingestion, feature engineering, configuration and the research-vs-production refactor (Tasks 1, 2) | 25 |
| 2 | `<FILL BITS ID>` | `<FILL NAME>` | Logging, error handling, code formatting and linting setup — black / flake8 / isort reports (Tasks 3, 4) | 25 |
| 3 | `<FILL BITS ID>` | `<FILL NAME>` | REST API design and implementation with FastAPI, request/response schemas and status codes (Task 5) | 25 |
| 4 | `<FILL BITS ID>` | `<FILL NAME>` | Quality assurance — pytest suite, ML-specific tests, model & data quality metrics, production testing and security note (Tasks 6–9) | 25 |

**Send me:** the 4 BITS IDs and names, in the order you want them listed.

**Also confirm:** is 25/25/25/25 the right split, and are the four work descriptions
accurate? I invented the division of labour to match the four natural chunks of the
assignment — change it to match what actually happened in your group.

---

## Q3 — What format does the final upload need to be?

The PDF's submission guideline is:

> *"Prepare a Word/PDF document containing the project details (All tasks, screenshots of
> the application as required, along with explanation) and code. Upload the file as
> `<groupid.docx>` or `<groupid.pdf>`."*

So the graded artifact is a **document**, not the notebook itself. What I've produced so far:

- `049.ipynb` — the notebook, all cells executed with output
- `049_report.html` — the same thing exported to HTML

**Right now the easiest path is:** open `049_report.html` in a browser →
**Print → Save as PDF** → rename to `049.pdf`. That takes you about 30 seconds and needs
nothing installed.

**But tell me if you'd rather I:**

- **A.** Leave it as-is — you'll do the browser print-to-PDF *(recommended, simplest)*
- **B.** Install `pandoc` + a LaTeX distribution so I can generate the PDF directly from
  the command line (a large install, ~1 GB, and the layout is usually worse than the
  browser's)
- **C.** Generate a proper `.docx` instead (needs `pandoc`; tables and code blocks
  usually survive, but syntax highlighting is lost)

---

## Q4 — Screenshots

The PDF asks for *"screenshots of the application as required"*.

The notebook currently proves everything **textually** — real HTTP status codes, real JSON
responses, real test output, real lint output. That is arguably stronger evidence than a
screenshot, since it is reproducible.

But if the grader is expecting literal images, the one worth having is the **FastAPI
interactive docs page**. To capture it:

```bash
cd assignments/assignment-2
uvicorn ecom.api:app --reload
```

then open <http://127.0.0.1:8000/docs>, expand `POST /predict`, click **Try it out**,
**Execute**, and screenshot the response.

**Question:** do you want to take 2–3 screenshots yourself (the `/docs` page, a successful
`/predict` call, and the passing test run), or is the textual evidence enough for you?
I cannot open a browser to capture images from here.

---

## Q5 — Should I commit this to git?

Nothing is committed yet. When you're ready, say the word and I'll commit
`assignments/assignment-2/` with a clear message.

Two related things to decide:

- **Do you want `data/` and `artifacts/` committed?** They're small (288 KB and 8 KB) and
  committing them means anyone can run the notebook without regenerating anything. I'd
  say yes. `logs/` is already git-ignored.
- **Is this repo pushed anywhere public?** If yes, I'd want your confirmation before
  pushing, since the notebook will contain your names and BITS IDs once Q2 is answered.

---

## Q6 — One leftover folder

The project used to live at `projects/assignment-2/`. I moved everything to
`assignments/assignment-2/`.

The old folder is now **completely empty**, but Windows won't let me delete the directory
entry itself because it is this session's active working directory. Git doesn't track
empty directories, so it will never show up in a commit — it's harmless.

If it bothers you, delete it manually after closing this session:

```powershell
Remove-Item "C:\dev\ai-ml\software-engineering-for-machine-learning\projects\assignment-2"
```

---

## Not questions — just things worth knowing

**The model's accuracy is 0.716, and that is deliberate.** An earlier version scored 0.809
and was much worse — it had simply learned to always guess "no purchase", which was right
81% of the time. Its F1 was 0.18. If anyone asks why the accuracy isn't higher, the answer
is in `JOURNEY.md`, Step 8, with the numbers.

**`research/` is deliberately bad code.** It has hardcoded paths, no random seed, wildcard
imports and dead commented-out experiments. It is the "before" half of Task 2 and it is
excluded from linting on purpose (there's a comment in `setup.cfg` saying so). Please
don't let anyone "tidy it up" — that destroys the evidence.

**Everything currently passes.** 61 tests, flake8/black/isort all clean on `ecom/` and
`tests/`, and every notebook cell executes without error. If you change any code, re-run:

```bash
python -m pytest && python -m flake8 ecom tests && python -m black --check ecom tests
```
