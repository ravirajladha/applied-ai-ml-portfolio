# Research paper — review summarization

A proper write-up of the experiment in the parent folder, written to understand
it deeply rather than to hand it in.

> **This is not part of the assignment.** It is deliberately excluded from the
> sync to the group repo — see `../SYNC.md`. Nothing here affects the graded
> submission.

**Start here:** [`PLAN.md`](PLAN.md). It has the session roadmap, the reading
for each session, and the one command to resume the work.

---

## The files

| File | What it is |
|---|---|
| `PLAN.md` | The roadmap and the resume command. **Read first.** |
| `EXPERIMENT_FACTS.md` | Every number the paper is allowed to quote. The single source of truth. |
| `main.tex` | The document skeleton — title, authors, and the list of sections |
| `sections/*.tex` | One file per section. Each stub says what goes in it. |
| `references.bib` | 15 bibliography entries |
| `refs/*.pdf` | The 15 papers themselves, downloaded, named to match the citation keys |
| `build.sh` | Builds `main.pdf` |
| `.vscode/settings.json` | Makes VS Code behave like Overleaf |

## Opening it locally (the Overleaf replacement)

You already have everything installed. Two ways to work:

### VS Code — the Overleaf-like way

```
File > Open Folder...  →  select this paper/ folder
```

Open `main.tex`, then **Ctrl+Alt+V** to open the PDF beside it. Now just
**save (Ctrl+S)** and the PDF rebuilds itself. That is the Overleaf loop.

Two things Overleaf cannot do that you now can:
- **Ctrl+Alt+J** — jump from where your cursor is in the source to that exact
  spot in the PDF.
- **Ctrl+click** in the PDF — jump back to the line of source that made it.

Open the folder itself, not the whole repo, or the build settings will not
apply.

### Terminal — when you just want the PDF

```bash
cd paper
./build.sh
```

It runs four passes, which looks excessive but is how LaTeX works: the first
pass discovers which sources you cited, `bibtex` formats them, and the last two
settle the page numbers that the new bibliography just shifted.

## If the build breaks

LaTeX errors are famously unhelpful. The useful line is almost never the last
one — search `main.log` for the first line starting with `!`.

| Symptom | Cause |
|---|---|
| `pdflatex not found` | MiKTeX is not on PATH. `build.sh` adds it automatically; in VS Code, restart it once after install. |
| `Citation undefined` | You added a `\cite` but have not re-run `bibtex`. Run `./build.sh`. |
| A package installs mid-build | Normal. MiKTeX fetches packages on demand the first time they are used. |
| `Undefined control sequence` | A typo in a command name — LaTeX points at the line. |
