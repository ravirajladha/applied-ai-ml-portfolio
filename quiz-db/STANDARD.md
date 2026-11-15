# Question bank standard

Every subject gets two files:

| File | What it is |
|------|-----------|
| `specs/<subject-slug>.md` | **The coverage spec.** What someone must know at each level, broken into topics, plus the traps to test. Written first, before any questions. |
| `content/subjects/<subject-slug>.py` | **The question bank.** Questions that cover every topic in the spec at every level they apply to. |

`<subject-slug>` is the slug from `content/structure.py` (e.g. `np-arrays`).

## 1. The four levels

| Level | Name | The learner can... | Typical question |
|-------|------|--------------------|------------------|
| 1 | Amateur | say what it is, read and run simple code, recognise the basic syntax | "What does `arr.shape` give you?" |
| 2 | Intermediate | use it daily, combine two ideas, predict output of everyday code, avoid the common traps | "What does this slice + reshape print?" |
| 3 | Advanced | explain edge cases, performance, copy-vs-view, dtype and memory behaviour, choose between approaches | "Why does this loop run 100x slower than the vectorised version?" |
| 4 | Expert | reason about internals and design trade-offs, debug subtle bugs, answer senior-interview questions | "Why is `a[::2]` a view but `a[[0, 2]]` a copy, and what does that mean for strides?" |

The learner is a beginner who climbs. **Level 1 must be truly gentle** (no jargon without a one-line definition). Level 4 must be truly hard: a strong practitioner should get some wrong.

**Minimum per subject:** 15 amateur, 15 intermediate, 12 advanced, 8 expert = **50**. Aim for **60–80**. `check_subject.py` fails below the minimum.

## 2. The spec: `specs/<slug>.md`

```markdown
# <Subject name>: coverage spec

**Ladder:** <category> › <section>   ·   **Prerequisites:** <subjects to know first>
**Why it matters for AI/ML:** 2-3 lines.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `creating` | Creating arrays | np.array, zeros, ones | arange vs linspace, dtype arg | ... | ... |

(6-12 topics. Each cell says what is tested at that level, or "—" if that level doesn't apply.)

## Must-know facts
Bullet list of the 10-20 facts a master of this subject never gets wrong.

## Common traps (each one must have at least one question)
- Trap -> what actually happens.

## Interview angle
The 3-5 questions an interviewer would ask, and the one-minute answers.

## Source material
Notes from the author's course material go here when added. (Leave "To be added" for now.)
```

The `Topic slug` column must match `TOPICS` in the question bank exactly.

## 3. The question bank: `content/subjects/<slug>.py`

```python
from helpers import mcq, tf, out, fill

SUBJECT = "np-arrays"

TOPICS = [
    ("creating", "Creating arrays"),
    ("shape-dtype", "Shape, ndim and dtype"),
]

QUESTIONS = [
    mcq("Which call makes a 2x3 array of zeros?",
        ["np.zeros((2, 3))", "np.zeros(2, 3)", "np.zero([2, 3])", "np.empty(2, 3)"], 0,
        "The shape goes in as ONE argument.",
        "np.zeros takes the shape as a tuple: np.zeros((2, 3)). np.zeros(2, 3) passes 3 as dtype and fails.",
        topic="creating", level=1),
    out("import numpy as np\na = np.arange(6).reshape(2, 3)\nprint(a.shape, a.ndim)",
        ["(2, 3) 2", "(3, 2) 2", "(2, 3) 6", "6 2"], 0,
        "shape is (rows, cols); ndim counts the axes.",
        "reshape(2, 3) gives 2 rows x 3 columns: shape (2, 3), 2 dimensions.",
        topic="shape-dtype", level=1),
]
```

### Builders (from `content/helpers.py`)
- `mcq(question, [4 options], correct_index, hint, explanation, ...)`
- `tf(statement, True/False, hint, explanation, ...)`
- `out(code, [4 options], correct_index, hint, explanation, question="What does this print?", ...)`
- `fill(question_with_____, answer, hint, explanation, ...)`: answer is short exact text (≤ 40 chars), e.g. a function name.

Every call **must** pass `topic="<slug>"` and `level=1..4`. Optional: `code="..."` (shown with an mcq/tf/fill), `diagram="""..."""`, `analogy="..."`, `lang="text"` for non-Python code.

### Writing rules
1. **Put the correct option at index 0.** The build shuffles options deterministically.
2. **Four options for mcq/out,** all plausible. Wrong options should be the mistakes people actually make (off-by-one, view vs copy, wrong axis), not jokes.
3. **The hint nudges, it doesn't give away the answer.** One line.
4. **The explanation is the quick answer:** 1-3 lines that say why the right one is right and, where it helps, why the tempting wrong one is wrong.
5. **Diagrams:** ASCII only (shown in `<pre>`). Max ~10 lines, max ~60 chars wide. Use them where a picture actually helps: shapes, axes, memory, flows, curves. Aim for about 1 in 5 questions.
6. **Analogies:** real-world or SDE (the learner is a full-stack developer). Optional, about 1 in 6 questions.
7. **Code snippets:** small (≤ 12 lines), self-contained (do the imports), deterministic (seed any randomness: `np.random.default_rng(0)`, `torch.manual_seed(0)`; never print a `set` of strings). They run on **Python 3.13, NumPy 2.1, Pandas 2.2, scikit-learn 1.6, PyTorch 2.6, matplotlib 3.10**.
   - For `out(...)`, the answer must be the **exact** stdout. If the code raises, the answer is the exception class name, e.g. `"ValueError"`.
   - NumPy 2 prints scalars as `np.float64(3.0)` with `repr` but `3.0` with `print`, so **always use `print(...)`**. Inside a printed list/tuple/dict, NumPy scalars still show as `np.int64(0)`: convert with `.tolist()`, `int(...)` or `float(...)` first.
   - Every snippet is executed by `check_subject.py`; if it doesn't match, fix the answer, not the checker.
8. **Mix question types:** roughly 40% mcq, 35% out (code questions), 15% tf, 10% fill. Conceptual subjects (ML theory) can use fewer `out` questions, but still include small numeric or code ones.
9. **No duplicates** of the starter questions already in `content/q_python.py` / `content/q_ml.py`.
10. Plain English. No mention of any AI assistant or tool that wrote the content.
11. Accuracy beats volume. If you're not sure a statement is true for the library versions above, check it by running code.

## 4. Check before you call it done

```
C:/ProgramData/anaconda3/python.exe check_subject.py <slug>
C:/ProgramData/anaconda3/python.exe build_seed.py
```

`check_subject.py` validates the structure, the topic coverage and the level minimums, and runs every snippet twice. Done means it prints no problems.
