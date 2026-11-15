# Comprehensions: coverage spec

**Ladder:** Foundations: Python & Data Tools › Python Core   ·   **Prerequisites:** py-loops, py-lists, py-dicts, py-conditions
**Why it matters for AI/ML:** Comprehensions are how Python code builds vocabularies (`{w: i for i, w in enumerate(vocab)}`), cleans token lists, batches data and maps labels. Generator expressions stream large datasets without loading them into memory. Reading them fluently is non-negotiable for working with real ML code.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `list-comp` | List comprehension basics | [expr for x in xs], reading it left to right | calling functions/methods in the expression, string iteration | equivalence to a loop with append, nested data | — |
| 2 | `filters` | Filtering with if | trailing if keeps matching items | multiple conditions, multiple ifs | filter + transform together, order of evaluation | — |
| 3 | `conditional-expr` | if-else inside the expression | — | `a if cond else b` goes in front, filter goes at the end | SyntaxError for if-else at the end, combining both | — |
| 4 | `dict-set` | Dict and set comprehensions | {k: v ...} and {x ...} syntax | inverting a dict, filtering a dict, `set()` vs `{}` | duplicate keys: last wins but first position kept, unhashable items | key evaluated before value (3.8+); 1, 1.0 and True are one key |
| 5 | `nested` | Nested comprehensions | — | flatten a 2D list | clause order mirrors nested loops, matrix of lists, transpose | wrong clause order NameError, cross product size |
| 6 | `genexp` | Generator expressions | round brackets make a generator | single use, sum(x for x in ...) without extra brackets | laziness and memory, any()/all() short-circuit | outermost iterable evaluated immediately, the rest lazily; late-bound names |
| 7 | `scope` | Comprehension scope | — | the loop variable does not leak (Python 3) | loop var vs outer variable of the same name | class-body scope NameError, lambdas inside comprehensions, PEP 709 inlining |
| 8 | `walrus` | Walrus operator in comprehensions | — | `:=` assigns inside an expression | avoid computing twice, the name leaks to the outer scope | can't rebind the iteration variable |
| 9 | `readability-perf` | Readability and performance | — | comprehensions vs map/filter | side-effect comprehensions are an anti-pattern; faster than append loops; no try/except inside; dict.fromkeys dedupe | when a loop is clearer; map(builtin) vs comprehension vs map(lambda); hidden side effects (seen.add); vectorising beats both |
| 10 | `grid-aliasing` | Building nested lists safely | `[0] * 3` repeats an item | `[[0] * n] * m` shares one row; a comprehension builds separate rows | `[[]] * n`, `dict.fromkeys(keys, [])`, shallow copies | deepcopy keeps shared rows shared; half-fixed grids |
| 11 | `ml-patterns` | Comprehensions in ML and data code | label -> id mapping, word -> index vocab, cleaning tokens | id -> word decoding, one-hot rows, filter + clean in one pass | padding and attention masks, chunking into batches, Counter + min-frequency filter, top-k, duplicate words in a vocab | ragged lists vs NumPy, lazy genexp over a closed file, streaming big files |

## Must-know facts
- `[expr for x in iterable]` equals a loop that appends `expr` for each `x`.
- A trailing `if cond` **filters** (drops items); `a if cond else b` in front **transforms** (keeps every item).
- `[x for x in xs if c else d]` is a `SyntaxError`; the if-else form must come before `for`.
- Multiple `for` clauses read left to right, exactly as nested loops written top to bottom.
- `{k: v for ...}` is a dict comprehension, `{x for ...}` is a set comprehension, `{}` alone is an empty dict.
- Duplicate keys in a dict comprehension: the last value wins.
- `(x for x in xs)` is a generator expression: lazy, single use, constant memory.
- A genexp that is the only argument doesn't need its own brackets: `sum(x * x for x in xs)`.
- `any()` / `all()` with a generator stop as soon as the answer is known.
- In a generator expression the outermost iterable is evaluated immediately; everything else runs lazily when consumed.
- In Python 3, the comprehension variable does not leak into the surrounding scope.
- A name bound with `:=` inside a comprehension **does** leak into the containing scope.
- `:=` cannot rebind a comprehension iteration variable (SyntaxError).
- In a class body, comprehensions can't see class-level names (except in the outermost iterable).
- A list comprehension is usually faster than an equivalent for-loop with `.append`; a NumPy vectorised op is faster than both.
- If you need side effects (print, write) use a loop, not a comprehension.
- `[[0] * n] * m` repeats one row object m times; build grids with `[[0] * n for _ in range(m)]`.
- Only the first `for` clause's iterable is evaluated once; later clauses re-run for every outer item.
- A generator that raised is finished; the remaining items are lost.
- Ragged nested lists can't become a NumPy array (ValueError in NumPy 2), so batches are padded first.

## Common traps (each one must have at least one question)
- `[x if x > 0 for x in xs]` or `if-else` at the end -> SyntaxError; position matters.
- Trailing `if` keeps the list length -> it drops items; only if-else in front keeps the length.
- `{}` is an empty set -> it's an empty dict; use `set()`.
- Nested comprehension clauses read inside-out -> they read in the same order as nested loops.
- Generator expressions can be reused -> the second pass is empty.
- `(x for x in xs)` is a tuple comprehension -> it's a generator; use `tuple(...)` for a tuple.
- The comprehension variable overwrites a variable of the same name outside -> not in Python 3.
- A walrus variable stays inside the comprehension -> it leaks to the enclosing scope.
- A generator expression captures variable values when created -> later names are read when consumed.
- `[print(x) for x in xs]` is a neat loop -> it builds a useless list of `None`.
- Dict comprehension with duplicate keys raises -> last value silently wins.
- Long nested comprehensions with three conditions are "Pythonic" -> beyond ~2 clauses, a loop is clearer.
- `[[0] * 2] * 2` makes two independent rows -> both slots are the same row.
- `dict.fromkeys(keys, [])` gives each key its own list -> they all share one list.
- `copy.deepcopy` separates shared rows -> it keeps them shared.
- `[x, -x for x in xs]` builds pairs -> SyntaxError; write `(x, -x)`.
- `all(...)` over empty data is False -> it's True.
- A genexp over an open file can be consumed after the `with` block -> ValueError: the file is closed.
- `{w: tokens.count(w) for w in set(tokens)}` is fine for counting -> it's quadratic; use `Counter`.
- `{k: ... for k in [1, 1.0, True]}` has three keys -> they collapse into one.

## Interview angle
- **"List comprehension vs generator expression?"** Square brackets build the whole list now (fast to re-read, O(n) memory); round brackets yield items on demand (O(1) memory, single use). For `sum`, `any`, `max` over big data, prefer the generator. SDE analogy: an array vs a stream.
- **"Where does the if go?"** At the end to filter, in front as `a if c else b` to transform every item.
- **"Why is a comprehension faster than a loop with append?"** It avoids looking up and calling `.append` each iteration and uses a dedicated bytecode to add items; the overall loop is still interpreted, so NumPy is faster for numeric work.
- **"Does the comprehension variable leak?"** Not in Python 3; it has its own scope. A walrus target does leak, by design.
- **"Why is `[[0] * 3] * 3` a bug?"** `*` copies references, so all three rows are one list; writing to one row writes to all. Use a comprehension so each row is built separately. SDE analogy: three pointers to one buffer.
- **"When would you not use a comprehension?"** When it has side effects, needs try/except, or becomes so nested that a reader has to untangle it.

## Source material
To be added
