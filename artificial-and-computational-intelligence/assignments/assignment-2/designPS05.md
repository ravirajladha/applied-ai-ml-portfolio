# Design Document — PS5 (COVID-19 Diagnosis using a Decision Tree in Prolog)

**Course:** AIMLCZG557 / AECLZG557 — Assignment 2
**Group Id:** Gxxx
**Deliverable file:** `PS05.pl` (single Prolog source file)

| Sl. No | Registration Number | Name | Contribution |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |

---

## 1. Problem

Given a decision tree and a symptom severity matrix, build a Prolog expert
system that asks a patient for four symptom values, walks the tree, and reports
the likely disease — Influenza, COVID-19, Dengue, or Common Cold — on screen and
in `outputPS05.txt`.

## 2. Design decisions

### 2.1 Four questions, not five

The tree contains five decision points; the fifth is *"Is taste/smell lost?"*.
The sample runs and the severity matrix, however, use only four attributes:
fever intensity, cough type, body pain severity, skin rash type.

We follow the **sample prompt format exactly**, because the evaluation input
file is built to that format. A fifth prompt would desynchronise the reads and
corrupt every subsequent case.

The taste/smell node is preserved by *derivation* rather than by asking. The
severity matrix identifies **"Persistent, Dry"** as the COVID-19 cough, which is
the same population the taste/smell question isolates. The knowledge base
therefore contains one explicit, commented fact:

```prolog
taste_smell_lost(persistent_dry).
```

All five levels of the tree are represented; only the source of the fifth
value differs.

### 2.2 Numeric fever accepted

One required edge case states the fever as `101.9`. The program accepts either a
category word or a raw temperature and converts the latter using the single
threshold fact `fever_threshold(100.4)`. This keeps the 100.4 F boundary in one
place and satisfies the "do not hard code values" instruction.

### 2.3 One extra rule beyond the diagram

The tree tests for a skin rash only on the high-fever branch, which would
classify "mild fever with a patchy rash" as Common Cold. A rash is not a cold
symptom, so a rash on the low-fever path is routed to
*Allergies / Other Infection*. This is the only place the implementation extends
the given diagram, and it is marked as such in the source.

## 3. Structure of `PS05.pl`

The file is a single module divided into six commented sections.

| Section | Contents | Key predicates |
|---|---|---|
| 1. Knowledge base | Threshold, prompts, valid answers, tree nodes, display names | `fever_threshold/1`, `question/2`, `allowed/2`, `high_fever/1`, `rash_present/1`, `severe_pain/1`, `hacking_cough/1`, `taste_smell_lost/1`, `mild_symptom/1`, `disease_name/2` |
| 2. Decision tree | Seven rules, one per leaf, in top-down tree order | `diagnose/5` |
| 3. Input | Prompting, exception-safe reading, conversion, validation, retry | `ask/2`, `ask_all/2`, `safe_read/1`, `normalise_fever/2`, `convert/3`, `validate/3` |
| 4. Output | Result sentence, screen and file writing | `result_line/2`, `reset_output/0`, `append_output/1`, `report/1` |
| 5. Driver | Recursive case loop and entry point | `run_cases/0`, `main/0` |
| 6. Test helpers | Commented out for submission, as instructed | `test/4`, `test_all/0` |

Separating facts from rules means the tree can be re-tuned (a new threshold, a
renamed disease, an extra accepted answer) by editing Section 1 alone.

### 3.1 The tree as rules

`diagnose(+Fever, +Cough, +Pain, +Rash, -Disease)` is backward-chained. Clauses
appear in the same order as a top-down walk of the tree, and each ends in a cut
so that the first matching branch commits — the deterministic behaviour a
decision tree requires.

| # | Guard | Leaf |
|---|---|---|
| 1 | `high_fever` ∧ `rash_present` | Dengue |
| 2 | `high_fever` ∧ `hacking_cough` ∧ `severe_pain` | Influenza |
| 3 | `high_fever` ∧ `taste_smell_lost` | COVID-19 |
| 4 | `high_fever` | Other Viral Infection |
| 5 | `rash_present` | Allergies / Other Infection |
| 6 | `mild_symptom(Cough)` ∧ `mild_symptom(Pain)` | Common Cold |
| 7 | — (catch-all) | Allergies / Other Infection |

The cut is placed at the **end** of each body, so guards are fully evaluated
before committing; a failed guard falls through to the next clause, mirroring
descent to the next node. Clause 7 has no guard, so `diagnose/5` is total — it
can never fail and bring down the caller.

### 3.2 Error handling

| Failure | Handling |
|---|---|
| Unreadable term (syntax error) | `catch/3` around `read/1` yields `malformed_answer`; one clear message; re-prompt |
| Answer beginning with a capital letter | Prolog reads it as a *variable*, which `memberchk/2` would bind to the first allowed value and accept silently. `safe_read/1` rejects any unbound answer via `var/1` |
| Value outside the allowed list | Message naming the valid options; re-prompt |
| Input exhausted mid-case | `ask/2` fails, the case is abandoned with no diagnosis, `main` still succeeds |
| Empty input | `main` succeeds, output file created empty |
| Output file cannot be opened or written | Message printed, error propagated to the user rather than swallowed |

`setup_call_cleanup/3` guarantees the output stream is closed even if a write
raises. The retry loop is bounded by end-of-input, so it cannot spin forever on
a file.

### 3.3 Input / output behaviour

Answers are Prolog terms ending in a full stop, read with `read/1`. When input
is redirected from a file the program echoes each answer, so the transcript
reproduces the sample layout (prompt and answer on one line). It also looks
ahead for end-of-input before printing a prompt, so no dangling prompt is
emitted after the last case. Both behaviours are disabled on an interactive
terminal, where echoing would duplicate keystrokes and look-ahead would block.

`run_cases/0` recurses, so a single input file may contain any number of
four-line cases; each produces one result line in `outputPS05.txt`. On an
interactive terminal the loop stops after one patient, matching the sample run.

## 4. Results

### 4.1 Samples from the problem statement

| Input | Expected | Obtained |
|---|---|---|
| `high_sudden. severe_dry. severe. absent.` | Influenza | Influenza |
| `high. none. excruciating. patchy.` | Dengue | Dengue |

### 4.2 Required edge cases

| Scenario | Input used | Result | Path taken |
|---|---|---|---|
| High fever 102 F, severe cough, sore throat, severe body pain, no rash | `102.0. severe_dry. severe. absent.` | **Influenza** | 102.0 ≥ 100.4 → high fever → no rash → severe pain + hacking cough → taste/smell intact |
| Fever 101.9, with a persistent dry cough | `101.9. persistent_dry. severe. absent.` | **COVID-19** | 101.9 ≥ 100.4 → high fever → no rash → persistent dry cough → taste/smell lost |
| Fever 101.9, body pain and sore throat only | `101.9. mild. severe. absent.` | **Other Viral Infection** | high fever, no rash, no distinguishing cough → `OTHER VIRUS` leaf |
| Mild body pain, mild sore throat, no fever | `none. mild. mild. absent.` | **Common Cold** | not high fever → mild cough and mild aches |

The second scenario is stated without a full symptom set, so both variants are
reported. The decisive point is that **101.9 ≥ 100.4 classifies as a high
fever**; the remaining symptoms then select the leaf.

### 4.3 Error-handling verification

| Test input | Behaviour observed |
|---|---|
| `burning_hot.` for fever | `[error] "burning_hot" is not a valid answer. Expected one of [high_sudden,high,mild,none].` then re-prompt, next answer accepted |
| `severe_dry ) bad.` for cough | `[error] that answer could not be read. Expected one of [...]` then re-prompt |
| Case truncated after three answers | Run ends cleanly, no diagnosis emitted for the partial case |
| `High_sudden.` (capital letter) | Rejected as unreadable and re-prompted, instead of being silently bound to `high_sudden` |

### 4.4 Exhaustive coverage

All 4 × 4 × 4 × 2 = **128** symptom combinations were run through
`diagnose/5`. Every one yields **exactly one** diagnosis — no combination falls
through and none matches two clauses — and all six leaves are reachable, so no
rule is dead:

```
allergies-56  dengue-32  other_virus-20  common_cold-8  covid19-8  influenza-4
```

## 5. Alternate way of modelling the problem, and its performance implications

### 5.1 Alternative: the tree as data, walked by a generic interpreter

Instead of encoding each path as a clause of `diagnose/5`, the tree can be
stored as a **single nested term** and traversed by a small interpreter:

```prolog
tree(node(fever,
      [ high_sudden - node(rash, [ patchy - leaf(dengue),
                                   absent - node(cough, [...]) ]),
        mild        - node(cough, [...]) ])).

walk(leaf(D), _, D).
walk(node(Attr, Branches), Answers, D) :-
    memberchk(Attr-Value, Answers),
    memberchk(Value-Sub, Branches),
    walk(Sub, Answers, D).
```

**Advantages.** The tree becomes data, so it can be read from a file, generated
by a learning algorithm (ID3/C4.5), swapped at runtime, or printed and validated
programmatically — none of which is possible when the tree is compiled into
clause heads. One interpreter serves any number of trees, and adding a level
costs a data edit rather than a code edit.

**Performance implications.** This is the real trade-off:

| | Rules (implemented) | Tree-as-data (alternative) |
|---|---|---|
| Cost per diagnosis | ≤ 7 compiled head unifications, each with ≤ 3 small guard calls | One `walk/3` recursion per level (4 levels), each doing two linear `memberchk/2` scans over the branch list |
| Where the work happens | Resolved by the WAM at compile time; guards are indexed fact lookups | Interpreted at run time; every node costs list traversal and term decomposition |
| Measured shape | O(1) for a fixed tree — constant, small | O(d · b) where d = depth, b = branching factor; also O(1) for a fixed tree but with a noticeably larger constant, typically 2–4× slower per query |
| Memory | Clauses only; no runtime term to build | Whole tree held as a term and re-traversed on every query |
| Failure mode | A missing branch is a missing clause — caught by the catch-all rule | A missing branch makes `memberchk/2` fail silently; needs its own guard |

For this assignment — a fixed four-level tree, one query per patient — both are
effectively instantaneous, and the rule form is preferable because it is faster,
more readable, and lets Prolog's own clause selection *be* the tree walk.

The data-driven form becomes the better choice when the tree is **large or not
fixed**: a tree induced from a dataset, a tree with hundreds of nodes, or a
system that must load a new tree without recompiling. At that scale the
interpretation overhead is dwarfed by the maintenance cost of generating and
compiling thousands of clauses.

### 5.2 Other options considered

- **Forward chaining** (assert observed symptoms, let rules fire until a
  diagnosis is derived). Handles *partial* symptom sets gracefully, which is
  attractive given edge case 2. Rejected because it repeatedly re-scans the rule
  base and needs conflict resolution when several diseases match — significant
  overhead for a problem whose input is always exactly four attributes.
- **Probabilistic scoring** over the severity matrix (score each disease, pick
  the highest). Degrades more gracefully on unusual symptom combinations, but
  the problem statement requires traversal of the *given* decision tree, and a
  scoring model would not be auditable against that diagram.

## 6. How to run

```
swipl -q -g main -t halt PS05.pl < inputPS05.txt
```

Or interactively:

```
swipl PS05.pl
?- main.
```

Results appear on screen and in `outputPS05.txt`.
