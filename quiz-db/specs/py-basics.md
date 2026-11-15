# Running Python & print: coverage spec

**Ladder:** Python core › Basics   ·   **Prerequisites:** none (first subject)
**Why it matters for AI/ML:** every notebook, training script and data pipeline starts here. Knowing how a script runs versus a notebook cell, how print buffers inside long training loops, and how integer vs float division behaves saves hours of confused debugging later.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `running` | Running Python: script, REPL, notebook | `python file.py`, what a REPL is, notebook shows last expression | `__name__ == "__main__"` | notebook hidden state, module import runs once, REPL `_` | — |
| 2 | `print` | print(): sep, end, file, flush | multiple args, `end`, empty `print()` | `sep=""`, `print(*list)`, print returns None | `file=sys.stderr`, `flush=True` and buffering, implicit literal concatenation | `sep=None` / `end=None` mean "default" |
| 3 | `comments` | Comments and docstrings | `#` comments, no `/* */` | docstrings, `__doc__` | shebang line | — |
| 4 | `indentation` | Indentation and blocks | 4 spaces, what is inside an `if` | IndentationError, TabError | — | INDENT/DEDENT tokens |
| 5 | `arithmetic` | Arithmetic operators | `/`, `%`, result types | `//` and `%` with negatives, `**` with negatives/fractions | `round()` banker's rounding, `divmod`, float floor division, big ints, `0 ** 0` | why floor division floors, `%` sign rule, big-int true division |
| 6 | `precedence` | Operator precedence | `*` before `+`, parentheses | `**` right-associative, `-2 ** 2`, `not` vs `==` | chained comparisons, bool arithmetic, conditional expression | `2 ** -1 ** 2` grammar |
| 7 | `input` | Reading input with input() | input() returns str | converting with int(), `"30" + 1` TypeError | EOFError when stdin closes | — |
| 8 | `introspection` | help(), dir(), type() | help() | dir(), type(print) | callable(), filtering dir() | `__code__` |
| 9 | `execution` | How Python executes code | interpreted, no build step | — | whole file is compiled first (SyntaxError before anything runs), NameError only at runtime | bytecode, `.pyc` caching, constant folding, `-O`, import steps |

## Must-know facts
- `python file.py` runs a script top to bottom; the REPL runs one statement at a time; a notebook keeps one live process (kernel) across cells.
- In a notebook (and the REPL) the value of the last expression is displayed automatically; in a script nothing is shown unless you `print`.
- `print(*args, sep=" ", end="\n", file=sys.stdout, flush=False)`; it returns `None`.
- `#` starts a comment; Python has no block-comment syntax. A string as the first statement of a module/function/class is a docstring (`__doc__`).
- Indentation defines blocks. PEP 8 says 4 spaces. Mixing tabs and spaces can raise `TabError`.
- `/` always returns a float; `//` floors (toward minus infinity); `%` takes the sign of the divisor; `a == (a // b) * b + a % b`.
- `**` binds tighter than unary minus on its left and is right-associative: `-2 ** 2 == -4`, `2 ** 3 ** 2 == 512`.
- `round()` uses banker's rounding: `round(2.5) == 2`.
- Python ints have unlimited size.
- `input()` always returns a `str` (without the trailing newline).
- `help(x)` shows docs, `dir(x)` lists attribute names, `type(x)` gives the class.
- CPython compiles the whole file to bytecode first, then runs it on a virtual machine; a SyntaxError anywhere stops everything, a NameError only fires when that line runs.
- `__pycache__/*.pyc` caches bytecode to speed up imports, not execution.
- A module's top-level code runs once per process; later imports hit the `sys.modules` cache.

## Common traps (each one must have at least one question)
- Expecting `print` to return the printed text -> it returns `None`.
- `-7 // 2` is `-4`, not `-3` -> floor division rounds toward minus infinity.
- `-7 % 3` is `2`, not `-1` -> result takes the sign of the divisor.
- `-2 ** 2` is `-4` -> `**` binds before unary minus.
- `2 ** 3 ** 2` is `512`, not `64` -> `**` is right-associative.
- `round(2.5)` is `2` -> banker's rounding to the even neighbour.
- `input()` result used as a number -> `TypeError` until you convert it with `int()`.
- Thinking `/` on two ints gives an int -> always a float (`10 / 5 == 2.0`).
- Thinking earlier lines run before a later SyntaxError -> the whole file fails to compile.
- Expecting a typo inside a function body to fail at definition -> NameError only when the function is called.
- Mixing tabs and spaces -> TabError / IndentationError.
- Printing from a long job redirected to a log file shows nothing for a while -> stdout is buffered; use `flush=True` or `python -u`.
- Notebook hidden state: deleting a cell doesn't delete its variables from the kernel.
- `1 < 3 > 2` is a chained comparison (`1 < 3 and 3 > 2`), not `(1 < 3) > 2`.

## Interview angle
- **"Is Python compiled or interpreted?"** Both: CPython compiles source to bytecode (cached in `.pyc`), then a virtual machine interprets that bytecode. There's no separate build step, but syntax errors are caught for the whole file before anything runs. SDE analogy: like Java compiling to bytecode for the JVM, except the compile is automatic and happens every run.
- **"Why is `-7 // 2 == -4`?"** `//` is floor division, rounding toward minus infinity, so the identity `a == (a // b) * b + a % b` holds with `%` taking the divisor's sign. Java and C truncate toward zero instead.
- **"Why doesn't my training log show up until the end?"** stdout is block-buffered when it isn't a terminal. Use `print(..., flush=True)`, `python -u`, or proper logging.
- **"What does `if __name__ == "__main__":` do?"** It runs code only when the file is executed directly, not when imported, like a `main()` entry point.
- **"Notebook vs script for ML work?"** Notebooks for exploration (live state, plots); scripts for anything repeatable (training jobs, pipelines) because hidden state and out-of-order cells make notebooks hard to reproduce.

## Source material
To be added.
