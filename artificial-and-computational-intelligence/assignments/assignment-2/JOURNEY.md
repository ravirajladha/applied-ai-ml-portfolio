# The Journey — How This Assignment Was Built

This file is the story of the project, written for someone who has **never used
Prolog before**. Read it top to bottom and you will understand not just *what*
the code does, but *why* each piece exists.

---

## Step 0 — What were we actually asked to do?

The PDF (`Assignment 2 PS 05.pdf`) gives us:

- A **decision tree** drawn in ASCII art. It diagnoses a patient as Influenza,
  COVID-19, Dengue, or Common Cold based on their symptoms.
- A **symptom severity matrix** — a small table saying which symptoms belong to
  which disease.
- Two **sample runs**, showing the exact questions to ask and the exact answer
  sentence to print.

And it asks us to write **Prolog** rules that:

1. store the tree as facts and rules,
2. ask the user for symptom values,
3. walk the tree using those values,
4. print the predicted disease,
5. handle three tricky "edge case" scenarios.

Deliverables: **one** Prolog file, an input file, an output file, a design PDF,
and a contribution sheet — all zipped.

---

## Step 1 — What even is Prolog? (the 2-minute version)

Most languages you have seen (Python, Java) are **imperative**: you write a list
of steps and the computer follows them.

Prolog is **declarative**: you write down *facts* and *rules*, and then ask a
*question*. Prolog figures out the steps itself.

**Real-world analogy.** Imagine a family tree written on paper:

- **Fact** — "Ravi is Meena's parent." You just state it. No computation.
- **Rule** — "X is a grandparent of Z **if** X is a parent of Y **and** Y is a
  parent of Z." A rule is an *if-then* sentence.
- **Query** — "Who is Meena's grandparent?" Prolog searches the facts and rules
  and answers.

That is the entire language. Three things: facts, rules, queries.

**Syntax you need for this file:**

| You see | It means |
|---|---|
| `high_fever(high).` | A **fact**: "high is a high fever." Ends in a full stop. |
| `:-` | Read it as **"if"**. |
| `,` | Read it as **"and"**. |
| `dengue :- a, b.` | Rule: "dengue is true **if** a **and** b are true." |
| lowercase `high_sudden` | An **atom** — a fixed value, like a string constant. |
| Uppercase `F`, `Cough` | A **variable** — a blank Prolog will fill in. |
| `_` | "I don't care what goes here." |
| `!` | The **cut** — "stop looking for other answers." More on this below. |

Why Prolog is a good fit here: a decision tree *is* a pile of if-then rules.
In Python we would write nested `if/elif`. In Prolog each branch of the tree
becomes one rule, and the rules read almost like the diagram.

---

## Step 2 — Reading the decision tree carefully

Here is the tree from the PDF, cleaned up:

```
                    Patient shows symptoms
                              |
                  Is fever >= 100.4 F (high)?
                     /                    \
                  YES                      NO
                   |                        |
           Is there a skin rash?    Cough/sore throat mild
              /          \           AND body aches mild?
        patchy            no             /        \
           |               |          YES          NO
       [ DENGUE ]          |           |            |
                           |     [ COMMON     [ ALLERGIES /
                           |        COLD ]     OTHER INF. ]
                           |
              How bad is body pain & cough?
                /                          \
   Severe pain + hacking cough      Moderate pain + dry cough
              |                                |
     Is taste/smell lost?             Is taste/smell lost?
        /          \                     /          \
      YES          NO                  YES          NO
       |            |                   |            |
 [ COVID-19 ]  [ INFLUENZA ]      [ COVID-19 ]  [ OTHER VIRUS ]
```

And the severity matrix:

| Disease | Fever | Cough | Body pain | Rash |
|---|---|---|---|---|
| Influenza | High & sudden | Severe, dry / hacking | Severe & debilitating | Absent |
| COVID-19 | High | **Persistent, dry** | Moderate to severe | Absent / variable |
| Dengue | High & sharp | Rare / mild | Excruciating | **Flat, red, patchy** |
| Common Cold | Mild or none | Tickly, productive | Mild & tiring | Absent |

---

## Step 3 — The problem we had to solve first

Look closely and you will spot a **conflict**:

- The **tree** has *five* decision points. The fifth one asks *"Is taste/smell
  lost?"*
- The **sample runs** only ask *four* questions: fever, cough, body pain, rash.
  There is no taste/smell prompt.
- The **matrix** also has only those four columns.

So: do we ask five questions or four?

**Decision: four.** The PDF says *"Ensure that the input, prompt and output file
guidelines are adhered to. Deviations from the mentioned formats will not be
entertained."* The evaluator will feed our program a file containing four
answers per patient. If we printed a fifth prompt and waited for a fifth
answer, every case after the first would be misaligned and the program would
produce garbage. Matching the sample format is non-negotiable.

**So how do we still honour the taste/smell node?** We *derive* it. Look at the
matrix again: the one cough type unique to COVID-19 is **"Persistent, Dry"**.
That is exactly the population the taste/smell question is there to catch. So
in our knowledge base:

```prolog
taste_smell_lost(persistent_dry).
```

Read as: *"if the patient reports a persistent dry cough, treat that as the
'taste/smell lost = yes' branch."* One fact, clearly commented, and the tree
still has all five levels. This reasoning goes in the design document, because a
grader will notice the same conflict and will want to see that we noticed it
too.

---

## Step 4 — Writing the knowledge base (facts)

Facts come first because rules are built out of them. We wrote five kinds:

**(a) The threshold.** The tree's root is a number, so it gets its own fact:

```prolog
fever_threshold(100.4).
```

Never hard-code `100.4` inside a rule. If the definition of "high fever"
changes, you edit one line.

**(b) The questions**, kept word-for-word from the PDF:

```prolog
question(fever, 'Is the Fever Intensity (high_sudden/high/mild/none)? ').
```

**(c) The allowed answers**, so we can reject nonsense:

```prolog
allowed(fever, [high_sudden, high, mild, none]).
```

**(d) The tree's decision points**, one predicate per node:

```prolog
high_fever(high_sudden).     % root node: yes-branch
high_fever(high).
rash_present(patchy).        % skin rash node
severe_pain(severe).         % "severe body pain" group
severe_pain(excruciating).
hacking_cough(severe_dry).   % "hacking cough"
taste_smell_lost(persistent_dry).
mild_symptom(mild).          % low-fever path
mild_symptom(none).
```

Notice `high_fever` has **two** facts. In Prolog, multiple facts for the same
name mean **OR**: a fever is high if it is `high_sudden` *or* `high`.

**(e) The display names**, separating the internal tag from the printed text:

```prolog
disease_name(covid19, 'COVID-19').
```

Why bother? Because `covid19` is easy to type in rules and impossible to
mistype in a string, while `'COVID-19'` is what the human must see. Keeping
them apart means we can change the wording without touching any logic.

---

## Step 5 — Turning the tree into rules

This is the heart of the assignment. One predicate does the whole tree:

```prolog
diagnose(+Fever, +Cough, +Pain, +Rash, -Disease)
```

The `+` means "you give me this", the `-` means "I give you this back". That is
just a comment convention, but every Prolog programmer uses it.

Then we wrote **one rule per leaf of the tree, in top-down order**:

```prolog
% Node 2 : high fever + patchy rash -> Dengue.
diagnose(F, _, _, R, dengue) :-
    high_fever(F),
    rash_present(R),
    !.
```

Read it out loud: *"The diagnosis is dengue **if** the fever counts as high
**and** the rash is present. Then stop."*

The `_` in the cough and pain slots means those symptoms are irrelevant on this
branch — which is exactly what the tree says. Dengue is decided by rash alone
once you are on the high-fever path.

### What the cut (`!`) is for

Without a cut, Prolog is stubbornly thorough: after finding one answer, it
backtracks and tries every remaining rule looking for more. For a diagnosis we
want **exactly one** answer — the first branch that matches, just like a real
tree walk.

The cut says *"I have committed to this branch, do not reconsider."* Putting it
at the **end** of the body matters: the conditions get checked first, and only
once they all pass do we commit. If `rash_present(R)` fails, there is no cut yet,
so Prolog falls through to the next rule. That is precisely the behaviour of
walking down to the next node.

This ordering also gives us a free safety property: the **last** rule is a
catch-all with no conditions, so `diagnose` can *never* fail. There is always an
answer.

### The final rule order

| # | Condition | Result |
|---|---|---|
| 1 | high fever **and** patchy rash | Dengue |
| 2 | high fever **and** hacking cough **and** severe pain | Influenza |
| 3 | high fever **and** persistent dry cough | COVID-19 |
| 4 | high fever (anything else) | Other Viral Infection |
| 5 | not high fever **and** patchy rash | Allergies / Other Infection |
| 6 | not high fever **and** mild cough **and** mild pain | Common Cold |
| 7 | anything else | Allergies / Other Infection |

Rule 5 is our own small addition. The tree only checks for a rash on the
high-fever side, which would leave "mild fever with a patchy rash" being called
a Common Cold — clearly wrong, since a rash is not a cold symptom. We route it
to the "other infection" leaf and say so in the design document.

---

## Step 6 — Asking the questions (and surviving bad input)

Prolog's `read/1` reads **one term ending in a full stop**. That is why the
sample answers look like `high_sudden.` with a dot — the dot is not decoration,
it is the terminator. This is convenient: our input file is literally a list of
Prolog terms.

We wrapped reading in three layers, each solving one real problem:

**Problem 1 — the answer is not readable at all** (someone typed `severe_dry )`).
Plain `read/1` throws an exception and the program dies. So:

```prolog
safe_read(Term) :-
    catch(read(Term), _Error, Term = malformed_answer).
```

`catch/3` is Prolog's try/except. On failure we hand back a marker atom instead
of crashing.

**Problem 2 — the answer is readable but wrong** (`burning_hot`). We check it
against the `allowed/2` list, print a helpful message listing the valid options,
and ask again:

```
Is the Fever Intensity (high_sudden/high/mild/none)? burning_hot.
  [error] "burning_hot" is not a valid answer. Expected one of [high_sudden,high,mild,none].
Is the Fever Intensity (high_sudden/high/mild/none)? high_sudden.
```

This retry loop cannot spin forever: if the input runs out while retrying, the
read returns `end_of_file`, `ask/2` fails, and the run ends cleanly.

**Problem 3 — the answer is a number.** One of the required edge cases is
*"Fever is 101.9 — what will be the decision?"*. So we accept a raw temperature
and convert it using the threshold fact:

```prolog
normalise_fever(Raw, high) :- number(Raw), fever_threshold(T), Raw >= T, !.
normalise_fever(Raw, mild) :- number(Raw), !.
normalise_fever(Value, Value).          % already a word, pass through
```

`101.9 >= 100.4`, so it becomes `high` and takes the high-fever path. The third
clause is the pass-through for when the user typed a word as normal.

---

## Step 7 — Two cosmetic bugs we found by running it

The first working version produced this when fed a file:

```
Is the Fever Intensity...? Is the Cough Type...? Is the Body Pain...? Result: ...
```

Everything on one line, unreadable.

**Why?** When you type at a keyboard, the *terminal* echoes your keystrokes and
your Enter key supplies the newline. When input is redirected from a file,
nobody echoes anything and there is no newline. The prompts simply ran together.

**Fix.** Detect whether we are reading from a keyboard or a file, and if it is a
file, echo the answer ourselves:

```prolog
from_file :- \+ stream_property(user_input, tty(true)).
```

`\+` means "not". Now the file transcript looks exactly like the sample in the
PDF — prompt and answer on the same line.

The second bug: after the last patient, the program printed one more `Is the
Fever Intensity...?` before exiting. It had to print the prompt *before* it
could discover the input was finished.

**Fix.** Peek ahead. `input_left/0` skips blank space and looks at the next
character without consuming it; if that is end-of-file, we stop before printing
anything. On a keyboard we skip this check, because peeking would block waiting
for the user to type — and they would be staring at a blank screen with no
prompt.

Neither bug affected correctness. Both would have made a grader wince.

---

## Step 8 — Handling more than one patient per file

`run_cases/0` diagnoses one patient and then **calls itself**:

```prolog
run_cases :-
    input_left,
    attribute_order(Attrs),
    ask_all(Attrs, Values),
    !,
    Values = [F, C, P, R],
    diagnose(F, C, P, R, Disease),
    report(Disease),
    continue_cases.
run_cases.        % base case: nothing left, succeed quietly
```

That is **recursion** — the same idea as a loop. The second clause with no body
is the stopping condition.

Why bother? The evaluator's file will probably hold one case, and this handles
that fine. But it also lets a single file hold six test cases, which is how we
demonstrate all the edge cases in one run. Costs three lines; no downside.

### The third bug this exposed

The first version of the loop called `run_cases` directly. From a file that is
correct. From a keyboard it was wrong: after answering four questions and seeing
a result, the user was immediately asked about a *second* patient, forever. The
PDF's sample run clearly ends after one diagnosis (`true.`).

**Fix.** Split the decision to continue into its own predicate:

```prolog
continue_cases :- from_file, !, run_cases.
continue_cases.
```

From a file, keep going. From a keyboard, stop after one patient. Both usages
now match what the PDF shows. This kind of thing is only findable by running the
program *both* ways.

---

## Step 9 — Output

The result goes to two places:

- the **screen**, in the exact sentence from the PDF, and
- **`outputPS05.txt`**, which is a required deliverable.

`main/0` truncates the file at the start of a run and each result is appended,
so the file always reflects exactly one run. Both file operations are wrapped in
`catch/3` — if the file cannot be opened (read-only folder, missing directory)
we print a clear message rather than dying halfway through a diagnosis.

`setup_call_cleanup/3` is Prolog's "with open(...) as f" — it guarantees the
file handle is closed even if the write fails.

---

## Step 10 — Checking the required edge cases

The PDF names three scenarios. Here is what our program actually produced:

**Scenario 1 — High fever (102 F), severe cough, sore throat, severe body pain, no skin rash.**

Input `102.0. severe_dry. severe. absent.` → **Influenza**

Walk: 102.0 >= 100.4 so high fever → rash absent, not dengue → hacking cough +
severe pain → taste/smell not lost → Influenza. This matches Sample Output 1.

**Scenario 2 — Fever is 101.9.**

101.9 >= 100.4, so it is a **high** fever and we take the high-fever path. The
final answer then depends on the other three symptoms, which the scenario leaves
open, so we ran two variants:

- `101.9. persistent_dry. severe. absent.` → **COVID-19**
- `101.9. mild. severe. absent.` → **Other Viral Infection**

The second is the honest answer for "body pain and sore throat" with no
distinctive cough: high fever, no rash, nothing that identifies flu or COVID.
The tree's `OTHER VIRUS` leaf exists for exactly this.

**Scenario 3 — Mild body pain, mild sore throat, no fever.**

Input `none. mild. mild. absent.` → **Common Cold**

Walk: not a high fever → low/mild path → cough mild and aches mild → Common Cold.

And the two samples from the PDF, to prove we match:

| Input | Expected | We got |
|---|---|---|
| `high_sudden. severe_dry. severe. absent.` | Influenza | **Influenza** |
| `high. none. excruciating. patchy.` | Dengue | **Dengue** |

All six cases live in `tests/input_all_cases.txt`; the transcript is in
`tests/transcript_all_cases.txt`.

---

## Step 11 — Deliberately breaking it

Requirement: *"ensure basic error handling is implemented."* We tested three
failure modes rather than assuming they work:

| Test file | What we fed it | What happened |
|---|---|---|
| `tests/input_errors.txt` | `burning_hot.` then a case cut short | Rejected with the valid options listed, re-prompted, accepted the next answer; the truncated case ended without a crash |
| `tests/input_malformed.txt` | `severe_dry ) bad.` | Caught the syntax error, printed one clean message, re-prompted |
| (empty input) | nothing | `main` succeeds silently, empty output file |

The truncated-case behaviour is worth noting: an incomplete patient produces
**no** diagnosis rather than a guess. Inventing an answer from partial symptoms
would be worse than saying nothing.

### The bug that only a review caught

Testing found something the samples never would have. What happens if the user
types a **capital letter** — `High_sudden.` instead of `high_sudden.`?

Remember from Step 1: lowercase is an atom (a value), **uppercase is a
variable** (a blank). So Prolog does not read the word "High_sudden" at all — it
reads an empty variable. And then this happens:

```prolog
?- X = _Unbound, memberchk(X, [high_sudden, high, mild, none]).
X = high_sudden.
```

`memberchk/2` does not *check membership* of a blank — it **fills the blank in**
with the first item on the list. Our validator would have silently accepted
nonsense as `high_sudden` and produced a confident, wrong diagnosis.

The fix is to refuse anything that came back unbound:

```prolog
safe_read(Term) :-
    catch(read(Raw), _Error, Raw = malformed_answer),
    (   var(Raw)                       % var/1 = "is this still a blank?"
    ->  Term = malformed_answer
    ;   Term = Raw
    ).
```

Two lessons. First, in Prolog a "check" against an unbound variable is often
secretly an *assignment* — this is the single most common beginner trap. Second,
the bug had been accidentally hidden by an unrelated clause elsewhere, so the
program *behaved* correctly for the wrong reason. Working by accident is not
working; the moment either piece of code changed, it would have broken silently.

### Proving the tree is complete

Last check: does every possible patient get exactly one answer? There are
4 fever × 4 cough × 4 pain × 2 rash = **128** combinations, so we simply ran all
of them:

```
combinations diagnosed: 128 of 128
every combination gives exactly one answer: OK
leaf coverage: allergies-56, dengue-32, other_virus-20,
               common_cold-8, covid19-8, influenza-4
```

No gaps (nothing falls through) and no ambiguity (nothing matches twice). Every
one of the six leaves is reachable, so no rule is dead code. Influenza is the
narrowest leaf at 4 combinations, which is right — it needs a high fever, a
hacking cough, severe pain *and* no rash, all at once.

---

## Step 12 — Tidying up for submission

- Test helpers (`test/4`, `test_all/0`) are **commented out** at the bottom of
  the file — the PDF explicitly asks for this.
- Everything is in **one** `.pl` file, as required.
- Section banners split the file into: facts → tree rules → input → output →
  driver → test helpers. A reader can follow it top to bottom.
- No magic numbers. `100.4`, the question text, the valid answers, and the
  output filename are all facts near the top.

---

## The short version

| Step | What we did |
|---|---|
| 1 | Learned enough Prolog: facts, rules, queries |
| 2 | Redrew the decision tree and the severity matrix |
| 3 | Found the tree/prompt conflict and resolved it (4 questions, derive taste/smell) |
| 4 | Wrote facts — threshold, questions, valid answers, tree nodes, disease names |
| 5 | Wrote 7 `diagnose/5` rules, one per leaf, ordered top-down, each ending in a cut |
| 6 | Wrote input handling: catch bad syntax, reject bad values, accept numeric fever |
| 7 | Fixed two output-formatting bugs found by actually running it |
| 8 | Added recursion so one file can hold many cases, and stopped the loop after one patient when run interactively |
| 9 | Wrote results to screen and to `outputPS05.txt` |
| 10 | Verified both PDF samples and all three edge scenarios |
| 11 | Deliberately fed it broken input to prove the error handling works |
| 12 | Commented out test helpers, tidied, documented |

## Things worth remembering from this project

1. **Read the samples before the diagram.** The diagram had five decision
   points; the samples had four prompts. The samples win, because that is what
   the grader's input file looks like.
2. **Rule order is the algorithm.** In Prolog you do not write "check this
   first" — you *arrange* the rules so the right one is found first.
3. **A cut at the end of the body, not the start.** Conditions first, commit
   after.
4. **Always end with a catch-all rule.** A predicate that can fail will take
   your whole program down with it.
5. **Run it against a file, not just the keyboard.** Both formatting bugs were
   invisible in interactive mode and obvious the moment we piped a file in —
   which is exactly how it will be graded.
