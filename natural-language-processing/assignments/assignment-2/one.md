# Open questions for you

Answer whenever you get a chance — I've marked which ones actually block
submission and which are just preferences.

**Status: everything buildable is built and verified.** The model is trained,
the app runs, ROUGE is measured, screenshots are captured, and the notebook is
exported to both `Group140.pdf` (23 pages) and `Group140.html`. The only
things left are the ones below that need information I don't have.

---

## 🔴 Blocking — I cannot finish the submission without these

### Q1. Member details  *(group number now settled — we are Group 140)*

The PDF requires:
- the exported file to be named **`Group<no>.pdf`** — done, it is `Group140.pdf`
- a table of **member names, BITS IDs, and contribution percentages** — still needed

The table at the top of `assignment2.ipynb` now carries the group number, but
the name and BITS ID fields are still `<Name N>` / `2023XXXXXXX` placeholders.
I need:

| | |
|---|---|
| Group number | **140** ✅ |
| Member 1 — name, BITS ID, contribution % | ? |
| Member 2 — name, BITS ID, contribution % | ? |
| Member 3 — name, BITS ID, contribution % | ? |
| Member 4 — name, BITS ID, contribution % | ? |
| Member 5 — name, BITS ID, contribution % | ? |

### Q2. BITS OSHA Virtual Lab (worth 1 mark)

Instruction 1 says implementation on the OSHA Virtual Lab is **compulsory**. I
cannot reach that environment from here. I need to know:

- Do you have working access to it?
- Does it have **internet access**? This matters a lot — the app currently
  downloads the `t5-small` checkpoint and the NLTK VADER lexicon on first run.
  If OSHA is offline, I need to change the code to load everything from bundled
  local files instead.
- Is there a **GPU**, or CPU only?
- Can you `pip install` there, or is the package list fixed? If fixed, tell me
  what's available and I'll target it.

Answering this may change the code, so it's the most important question here.

---

## 🟡 Preferences — I've picked a sensible default, tell me if you disagree

### Q3. Dataset choice

The PDF says "if the dataset link is not working, download a similar dataset and
note this in your submission." **No dataset link was actually given** in the PDF,
so I chose:

> **Amazon Fine Food Reviews** (568,454 reviews), via the Hugging Face Hub as
> `jhan21/amazon-food-reviews-dataset`

It fits well because each row has a long review *and* a short human-written
headline (a free reference summary), plus a `ProductId` so we can group many
reviews of one product — exactly the scenario in the problem statement.

**Confirm this is acceptable**, or tell me if your course gave you a specific
dataset link I should use instead.

### Q4. Should I also build the LSTM Seq2Seq version?

You chose **fine-tuned t5-small**, which is what's built and it works well. The
PDF allows "Seq2Seq/LSTM **or** Transformer", so this fully satisfies Task 3.

However — some evaluators like to see the model built from scratch. I could add
an LSTM encoder–decoder as a *second* model and put both in the ROUGE comparison
table. It would strengthen Task 3 and Task 5 at the cost of extra runtime.

- [ ] No, t5-small alone is fine (current state)
- [ ] Yes, add the from-scratch LSTM as a comparison

### Q5. How hard should I train?

Actual run: **4,000 reviews, 1 epoch, 112 minutes on CPU.** I originally planned
20,000 but measured the real speed at ~6 seconds per training step — 20,000
would have taken about 4 hours. (It also stalled for 24 minutes mid-run when the
laptop ran low on RAM; see `JOURNEY.md` §7.)

**It still works well.** Measured on 300 held-out reviews:

| Model | ROUGE-1 | ROUGE-2 | ROUGE-L |
|---|---|---|---|
| Lead-1 baseline | 0.1245 | 0.0342 | 0.1144 |
| t5-small, not fine-tuned | 0.1080 | 0.0261 | 0.0977 |
| **ours, fine-tuned** | **0.1744** | **0.0445** | **0.1726** |

A longer run (20,000 reviews, ~4 hours) would likely improve this. It just needs
the laptop left alone, ideally with browser tabs closed.

- [ ] Keep the current 4k / 1 epoch run (already done, fully working)
- [ ] Do a longer overnight run — I can leave it going

### Q6. Submission format

The PDF says submit code "in .pdf/html format along with output".

My plan: run `assignment2.ipynb` top to bottom so every output and chart is
embedded, then export to **PDF**. The `.py` files (`summarizer.py`, `train.py`,
`app.py`) are referenced but their full source is *not* currently pasted into the
notebook.

- [ ] PDF export, with a code appendix containing the full `.py` sources (safest —
      the evaluator sees all the code in one file)
- [ ] PDF export without the appendix (cleaner, but the `.py` code isn't visible
      in the submitted document)
- [ ] HTML instead of PDF

I'd recommend the **first option** — evaluators generally mark only what's in the
submitted file.

---

## 🟢 Housekeeping — just say yes/no

### Q7. Screenshots of the web app — done

I went ahead and captured three (input screen, aspect charts, per-review
summaries) into `screenshots/`, and they are embedded in the notebook. Replace
them if you would rather use your own.

### Q8. The accidental Prolog work

I initially built a complete Prolog solution for **PS-05 (COVID/flu/dengue
decision tree)** because that PDF was in this folder when I started. I moved it
to `artificial-and-computational-intelligence/assignments/assignment-2/`.

That folder **already had** its own `PS05.pl` and a `tests/` directory. So there
are now two Prolog solutions sitting side by side:

- `PS05.pl` — yours, pre-existing
- `diagnosePS05.pl` + `inputPS05.txt` + `outputPS05.txt` — mine

Mine is tested and working (both sample cases from that PDF match exactly, all
128 symptom combinations covered). But I don't know which you want to keep.

- [ ] Keep both, I'll compare them myself
- [ ] Delete mine
- [ ] Look at both and merge the best of each

### Q9. Git commits

Your `CLAUDE.md` says the learning journey is tracked in git. I have **not
committed anything** yet. Want me to?

Note: `models/` (~240 MB) and `.venv/` should not go into git — I'd add a
`.gitignore` for those and commit only the code, notebook and docs.

- [ ] Yes, commit the work
- [ ] No, I'll handle git myself

---

## Things I already decided (no action needed, just so you know)

| Decision | Why |
|---|---|
| **PyTorch, not TensorFlow** | Your laptop is ARM64; TensorFlow has no Windows-ARM64 build at all |
| **x64 Anaconda Python, not native ARM64** | PyTorch has no ARM64 wheel either — this was forced, not a preference |
| **Isolated `.venv`** | So installs can't break your existing Anaconda setup |
| **Streamlit over Flask** | Your choice; also far less code and easier to screenshot |
| **Aspects ranked by distinctiveness, not raw frequency** | Ranking by frequency made both lists identical (for a cat toy, "cat" and "toy" topped praise *and* complaints). Now a term is only listed on a side if it's disproportionately common there |
| **Kept `. ! ?` during cleaning** | Most tutorials strip all punctuation; the aspect step needs sentence boundaries |

Full reasoning for all of these is in **`JOURNEY.md`**.
