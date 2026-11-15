# Loops: coverage spec

**Ladder:** Foundations: Python & Data Tools › Python Core   ·   **Prerequisites:** py-variables, py-lists, py-dicts, py-conditions
**Why it matters for AI/ML:** Every training loop, data loader and evaluation pass is a loop over an iterable. Knowing iterators and generators lets you stream datasets that don't fit in memory; knowing when *not* to loop (vectorise with NumPy) is the difference between a 2-second and a 2-hour job.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `for-basics` | for over lists, strings, dicts | for item in list / str, indentation, accumulator | dict keys vs .items(), rebinding the loop variable doesn't change the list | for i in range(len(x)) anti-pattern, unpacking targets | the loop target is any assignment target (`for a[0] in ...`) |
| 2 | `range` | range() | range(n), start/stop, stop is excluded | negative step, empty ranges, len(range) | range is a lazy sequence (indexable, O(1) `in`), not an iterator | — |
| 3 | `while` | while loops | condition, counter, stopping | while True + break, falsy conditions | float-equality infinite loops, do-while emulation | — |
| 4 | `break-continue` | break and continue | break exits, continue skips | combining break/continue with counters | break only exits the innermost loop | — |
| 5 | `loop-else` | for-else / while-else | — | else runs when no break happened | search pattern with for-else; else on empty loops | while-else semantics, else is "no break", not "if empty" |
| 6 | `enumerate-zip` | enumerate and zip | enumerate gives (index, item) | enumerate(start=), zip pairs, shortest wins | zip(strict=True), zip(*pairs) transposes | zip(it, it) chunking with a shared iterator |
| 7 | `nested` | Nested loops | inner loop runs fully per outer step | counting iterations, building pairs | breaking out of two loops (flag / function / for-else) | — |
| 8 | `mutating` | Modifying while iterating | — | removing from a list skips items | iterate over a copy or build a new list; dict size change raises | dict key changes raise even at same size; why the list version silently skips |
| 9 | `iterators` | Iterables vs iterators | — | iter() / next(), single-use iterators (map, zip) | StopIteration, next(it, default), `in` consumes | for-loop desugaring, `__iter__`/`__next__`, `__getitem__` legacy protocol, shared-iterator loops |
| 10 | `generators` | Generators and yield | — | yield produces values lazily, a generator function returns a generator | body runs only on next(), memory benefit, single use | PEP 479 (StopIteration -> RuntimeError), return value via StopIteration / yield from |
| 11 | `itertools` | itertools basics | — | chain, islice, count | product, accumulate, groupby needs sorted input | groupby groups go stale once the outer iterator advances |
| 12 | `scope-perf` | Loop variable leakage and performance | loop variable still exists after the loop | empty loop leaves variable undefined | Python loop vs NumPy vectorisation, str += vs join, built-in sum | why the interpreter loop is slow (boxing, dispatch), when a loop is still the right tool |

## Must-know facts
- `for x in thing` works on any **iterable**; it calls `iter(thing)` then `next()` until `StopIteration`.
- `range(start, stop, step)` excludes `stop`; `range(5, 0)` is empty; a negative step counts down.
- `range` is a lazy, re-usable sequence: `len`, indexing and `in` work without building a list.
- Rebinding the loop variable (`x = x * 2`) never changes the list being looped over.
- Looping over a dict gives keys; use `.items()` for (key, value), `.values()` for values. Order is insertion order.
- `break` leaves only the innermost loop; `continue` jumps to the next iteration.
- The `else` on a loop runs when the loop finished **without `break`** (including zero iterations).
- `enumerate(x, start=1)` changes the counter, not which items you get.
- `zip` stops at the shortest input; `zip(..., strict=True)` raises `ValueError` on unequal lengths.
- Iterators (map, zip, filter, generators, file objects) are single-use; a list or range can be looped again.
- `x in iterator` consumes items up to and including the match.
- A generator function's body does not run until the first `next()`.
- Raising `StopIteration` inside a generator turns into `RuntimeError` (PEP 479).
- Removing items from a list while looping over it skips elements; changing a dict's size while looping raises `RuntimeError`.
- The loop variable leaks: after `for i in range(3)`, `i == 2`. If the loop never ran, it is undefined.
- `itertools.groupby` only groups *consecutive* equal keys: sort first.
- Pure-Python loops over numbers are ~10-100x slower than the equivalent NumPy operation.

## Common traps (each one must have at least one question)
- `range(1, 5)` includes 5 -> it stops at 4.
- Changing the loop variable changes the list -> it doesn't; the list is untouched.
- Looping over a dict gives pairs -> it gives keys only.
- `break` in the inner loop exits both loops -> only the inner one.
- Loop `else` means "if the loop was empty" -> it means "if no break happened".
- `zip` raises on unequal lengths -> it silently truncates (unless `strict=True`).
- Removing from a list while iterating removes all matches -> it skips the item after each removal.
- Looping over a `map`/`zip`/generator twice -> the second pass is empty.
- Calling a generator function runs its body -> it only creates a generator object.
- `groupby` on unsorted data groups all equal keys -> only consecutive runs.
- `while x != 1.0: x += 0.1` stops -> floating-point error makes it loop forever.
- The loop variable is gone after the loop -> it keeps its last value (NameError only if the loop never ran).
- `next()` on a list or range works -> TypeError; they are iterables, not iterators.
- `enumerate(x, start=1)` skips the first item -> it only shifts the counter.

## Interview angle
- **"What's the difference between an iterable and an iterator?"** An iterable can hand you an iterator (`__iter__`); an iterator hands out items one at a time (`__next__`) and is exhausted after one pass. A list is iterable, `iter(list)` is an iterator. SDE analogy: an iterable is the database table, an iterator is the cursor.
- **"Why use a generator?"** It produces items lazily, so memory is O(1) instead of O(n). Ideal for streaming a large file or dataset batch by batch, like a paginated API you fetch page by page.
- **"What does for-else do?"** The else block runs only if the loop didn't `break`. It replaces a "found" flag in search loops.
- **"Why is this Python loop slow, and how do you fix it?"** Each iteration goes through the interpreter: boxed integers, type checks, bytecode dispatch. Push the loop into C with NumPy vectorisation or built-ins like `sum`.
- **"What happens if you modify a list while looping over it?"** The internal index keeps moving while items shift, so elements get skipped. Loop over a copy or build a new list with a comprehension.

## Source material
To be added
