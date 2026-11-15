# What I Need From You

Read this, study the topic, come back with answers. Nothing here is urgent —
the code works and is fully tested. These are the calls only you can make.

---

## Part A — Decisions I can't make for you

### A1. Two Prolog files exist. Which one ships? ⬅ **most important**

The zip must contain **one** `.pl` file ("Do not fragment your code into
multiple files"). Right now the folder has two.

| | `PS05.pl` (mine) | `diagnosePS05.pl` (appeared mid-session — not written by me) |
|---|---|---|
| Entry point | `main.` | `diagnose.` |
| Handles `101.9.` as a fever | **yes** | **no — fails the required edge case** |
| Writes `outputPS05.txt` itself | **yes** | no, relies on shell `> outputPS05.txt`, which dumps prompts into the file too |
| Multiple patients per input file | yes | no, one only |
| Capital-letter answer (`High_sudden.`) | rejected cleanly | reports the wrong error ("input ended") |
| Lines | 232 | 216 |

**I recommend `PS05.pl`** — `diagnosePS05.pl` fails edge case 2 outright. Here's
the proof, run on your machine:

```
$ printf '101.9.\npersistent_dry.\nsevere.\nabsent.\n' | swipl -q -g diagnose -t halt diagnosePS05.pl
Is the Fever Intensity (high_sudden/high/mild/none)? 101.9.
Error: "101.9" is not a valid value. Expected one of [high_sudden,high,mild,none].
Is the Fever Intensity (high_sudden/high/mild/none)? persistent_dry.
Error: "persistent_dry" is not a valid value...
...
Result: no diagnosis - incomplete symptom data.
```

It rejects the temperature, then eats the *next three answers* as retries for
the fever question, and ends with no diagnosis.

`diagnosePS05.pl` does have one nice idea worth stealing: its commented-out
`show_tree/0` prints every symptom combination and its predicted disease. I can
port that into `PS05.pl` if you want it.

**→ Tell me: keep `PS05.pl` and delete the other? Keep both for now? Merge
anything across?** I have not deleted anything.

### A2. What goes in `inputPS05.txt`?

You trimmed it to the single sample case (4 lines). That's valid.

But the PDF says *"Mention the results for the below mentioned edge case
scenarios."* Right now those live in `tests/input_all_cases.txt` — **outside the
zip**. They're written up in the design doc, so you're covered on paper, but the
grader can't re-run them from your submission.

**→ Tell me: leave it as the one sample case, or promote the 6-case file to be
`inputPS05.txt`?** (My lean: 6 cases. Costs nothing, proves every edge case.)

### A3. Group details

I've left placeholders everywhere. I need:

- **Group number** (e.g. 26 → `G026`)
- **4 × BITS registration number + name**
- **Percentage contribution per person** (0–100 each)

Goes into: `PS05.pl` header, `designPS05.md` header, `Gxxx_Contribution.csv`,
and every `Gxxx` filename.

### A4. The `.xlsx` file

The PDF demands `.xlsx`. I made `Gxxx_Contribution.csv` because `openpyxl` isn't
installed here.

**→ Either** open the CSV in Excel and "Save As .xlsx" (30 seconds), **or** say
the word and I'll `pip install openpyxl` and generate the real `.xlsx`.

### A5. The design PDF

`designPS05.md` needs to become `designPS05_Gxxx.pdf`, **max 4 pages**. It's
currently sized for about that, but the real page count depends on your
converter.

**→ How do you want to make the PDF?** Paste into Word, use a markdown-to-PDF
tool, or have me generate one?

---

## Part B — What to study (so my explanations land)

Everything below is explained from zero in **[JOURNEY.md](JOURNEY.md)**. Read
that first — this is just the list of concepts, so you know what you're looking
at.

### B1. Prolog basics — the only three things (30 min)

- **Fact** — `high_fever(high).` A statement you assert. No computation.
- **Rule** — `a :- b, c.` Read `:-` as **"if"** and `,` as **"and"**.
- **Query** — `?- diagnose(high, ...).` The question you ask.

Try in `swipl`: load `PS05.pl`, then type `high_fever(high).` and
`high_fever(mild).` and see `true` / `false`.

### B2. Atoms vs Variables — the one that bites (15 min)

**Lowercase = atom (a value). Uppercase = variable (a blank).**

`high_sudden` is a value. `High_sudden` is a *variable* — Prolog will happily
fill it with anything. This is exactly the bug I found and fixed today (see
Part C). If you understand only one thing from this list, make it this one.

### B3. The cut `!` (30 min)

Prolog normally backtracks and finds *every* answer. `!` says "stop, I've
committed." A decision tree needs exactly one answer, so every `diagnose/5` rule
ends in a cut.

Key detail: the cut goes at the **end** of the rule body. Conditions are checked
first; only if they all pass do we commit.

### B4. Rule order = the algorithm (15 min)

In Python you'd write `if / elif / else`. In Prolog you just *arrange the rules*
in tree order and let Prolog pick the first match. Look at Section 2 of
`PS05.pl` — the seven rules are literally a top-down walk of the diagram.

### B5. The tree/prompt conflict (10 min) — **be ready to defend this**

The diagram has **5** decision points. The samples only ask **4** questions.
There is no taste/smell prompt.

I kept the 4 prompts and derived taste/smell from `persistent_dry` cough, which
the severity matrix names as the COVID-19 signature. A grader will notice the
same gap. JOURNEY.md Step 3 and design doc §2.1 have the full reasoning — read
it before any viva.

### B6. Optional, if you're curious

- `read/1`, `catch/3`, `setup_call_cleanup/3` — the I/O and error handling
- Backward chaining vs forward chaining — design doc §5.2
- Tree-as-rules vs tree-as-data — design doc §5.1, the required "alternate
  modelling approach"

### Quick self-test

If you can answer these, you understand the submission:

1. Why is `High_sudden.` dangerous but `high_sudden.` fine?
2. Why does every `diagnose/5` rule end in `!`?
3. Why does the last rule have no conditions at all?
4. Why do we ask 4 questions when the tree has 5 decision points?
5. Why does `101.9.` produce a *high* fever path?

(Answers: B2 / B3 / totality — a failing predicate would crash the caller /
B5 / `101.9 >= 100.4`, via the `fever_threshold` fact.)

---

## Part C — What I found and fixed in this review

For your awareness. No action needed.

**A real bug: unbound variables were silently accepted.**

If someone typed `High_sudden.` (capital H), Prolog reads a *variable*. Then
`memberchk(Variable, [high_sudden, high, mild, none])` **succeeds and binds it to
the first item** — so garbage input would have been silently accepted as
`high_sudden`. Proof:

```
?- X = _Unbound, memberchk(X, [high_sudden, high, mild, none]).
X = high_sudden.        % it just made one up
```

It happened to be masked by an unrelated accident in `echo_answer/1`. Masked is
not fixed. `safe_read/1` now explicitly rejects unbound answers with `var/1`.

**The same bug is live in `diagnosePS05.pl`** and is *not* masked there — it
produces the misleading message "input ended before all four symptoms were
given."

**Exhaustive check.** All **128** symptom combinations (4 fever × 4 cough ×
4 pain × 2 rash) produce **exactly one** diagnosis — no gaps, no ambiguity. All
six leaves are reachable:

```
allergies-56, dengue-32, other_virus-20, common_cold-8, covid19-8, influenza-4
```

**Also verified this round:** integer fever (`102.`), quoted atoms (`'high'.`),
compound terms (`foo(bar).`), sub-threshold temperatures (`98.6.`), malformed
syntax, truncated cases, and empty input. Loads with zero warnings.

---

## Where everything is

| File | What it's for |
|---|---|
| **`JOURNEY.md`** | **Start here.** Prolog from zero + every decision, in order |
| `README.md` | How to run it, answer format, submission checklist |
| `designPS05.md` | The design doc → becomes your PDF |
| `PS05.pl` | The program |
| `tests/` | 6 test inputs + saved transcripts |

## Run it yourself

```
swipl -q -g main -t halt PS05.pl < inputPS05.txt
```

All six cases at once:

```
swipl -q -g main -t halt PS05.pl < tests/input_all_cases.txt
```

Interactively, to feel how it works:

```
swipl PS05.pl
?- main.
```

Deadline: **17 Aug 2026, 23:55 IST**.
