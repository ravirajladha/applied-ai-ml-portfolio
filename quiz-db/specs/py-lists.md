# Lists: coverage spec

**Ladder:** Foundations: Python & Data Tools › Python Core   ·   **Prerequisites:** py-basics, py-variables, py-strings
**Why it matters for AI/ML:** Lists are the everyday container before NumPy: batches of file paths, token ids, training logs, metric histories. Aliasing and copy bugs in lists are the same bugs you later meet as view-vs-copy in NumPy and Pandas, and knowing what is O(1) vs O(n) keeps data-prep scripts fast.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `indexing-slicing` | Indexing and slicing | zero-based index, `[-1]`, `[a:b]` stop excluded, IndexError | negative slices, step, `[::-1]`, out-of-range slices don't fail | slice assignment that grows/shrinks, `del a[::2]`, extended-slice size rule | slice objects, `a[len(a):] = ...`, prepend via `a[:0]` |
| 2 | `methods` | List methods | append, len, `in`, `pop()` | extend vs append, insert, remove (first match), index, count, methods return None | `extend("hi")`, `insert` past the end, `+=` vs `+`, clear vs `= []` | `+=` on a list inside a tuple, which methods mutate in place |
| 3 | `copying` | Aliasing, shallow and deep copy | `b = a` shares the list | `a.copy()`, `a[:]`, `list(a)` make new outer lists | shallow copy shares inner lists, `copy.deepcopy` | deepcopy with shared refs/cycles, `is` vs `==` on lists |
| 4 | `nested` | Nested lists (2-D) | `m[r][c]` indexing | building a grid, iterating rows | the `[[0]*3]*3` trap vs comprehension, `zip(*m)` transpose | `[[]]*n`, modifying while iterating, `sum(lists, [])` cost |
| 5 | `tuples` | Tuples and unpacking | tuple syntax, immutability, `(1,)` | unpacking `a, b = b, a`, star unpacking `first, *rest` | tuple of lists is mutable inside, hashability | tuple vs list memory/speed, unpacking count errors |
| 6 | `stack-queue` | Lists as stack / queue, deque | stack = append + pop | `pop(0)` is slow, `collections.deque` | `deque(maxlen=n)` as sliding window | why deque is O(1) at both ends, when list still wins (random index) |
| 7 | `sorting` | Sorting | `sorted()` vs `.sort()` | `key=`, `reverse=True`, `.sort()` returns None | stable sort, sort by multiple keys with tuples, str case ordering, mixed types TypeError | key called once per element, stability with `reverse=True` |
| 8 | `complexity` | Time complexity | — | append O(1), `in` O(n) | pop(0)/insert(0) O(n), use a set for membership | amortised O(1) append, `sum(lists, [])` quadratic, `bisect.insort` still O(n) |
| 9 | `mutable-defaults` | Mutable default arguments | — | `def f(x, acc=[])` keeps growing | `None` sentinel fix | defaults are evaluated once at `def` time, live in `f.__defaults__` |
| 10 | `internals` | How lists work inside | — | — | a list stores references, not values | dynamic array over-allocation, `sys.getsizeof` excludes elements, `id` stable across growth |
| 11 | `iter-tools` | Looping helpers: enumerate, zip, reversed | `enumerate`, `min`/`max`/`sum` | `zip` pairs and silently truncates, `reversed`, loop variable is not a slot | `zip(strict=True)`, iterators are single-use | `zip(it, it)` chunking idiom |
| 12 | `ml-patterns` | Lists in ML code: batches, padding, metrics | metric history with `append` | batching with slices, `+`/`*` are not element-wise, `max(runs, key=...)` | padding token sequences, ragged lists -> NumPy ValueError, shuffle X and y together, order-keeping dedupe | NumPy dtype upcasting from mixed lists, storing loss tensors leaks the graph, float summation error |

## Must-know facts
- Indexing is zero-based; `a[-1]` is the last item; `a[i]` out of range raises IndexError but a slice out of range just returns fewer items.
- A slice `a[start:stop:step]` excludes `stop`; `a[::-1]` is a reversed copy.
- Slice assignment can change the length (`a[1:2] = [7, 8, 9]`); extended-slice assignment (`a[::2] = ...`) needs exactly the same number of items.
- `append(x)` adds one item (even a list); `extend(iterable)` adds each item.
- Mutating methods (`append`, `sort`, `reverse`, `insert`, `extend`) return `None`.
- `remove(x)` deletes the first match and raises ValueError if absent.
- `b = a` is an alias; `a.copy()`, `a[:]`, `list(a)` are shallow copies; `copy.deepcopy` copies nested objects too.
- `[[0] * 3] * 3` makes three references to the same row; build grids with a comprehension.
- `a += b` mutates `a` in place; `a = a + b` makes a new list.
- `(1)` is an int, `(1,)` is a tuple; tuples are immutable but can hold mutable items.
- `pop()` and `append()` are O(1) amortised; `pop(0)`, `insert(0, x)` and `x in a` are O(n).
- `collections.deque` gives O(1) `appendleft` / `popleft`.
- Python's sort is stable; `key` is computed once per element.
- Default argument values are evaluated once, when `def` runs.
- A list is a dynamic array of pointers that over-allocates so appends are amortised O(1).
- `zip` stops at the shortest input and is a single-use iterator; `enumerate` gives (index, item).
- Lists are not vectors: convert to NumPy for element-wise maths, and pad ragged rows first.

## Common traps (each one must have at least one question)
- `x = nums.sort()` -> `x` is None; `.sort()` sorts in place and returns None.
- `[[0]*3]*3` then `grid[0][0] = 1` -> every row changes.
- `b = a[:]` with nested lists -> inner lists are still shared.
- `a.append([3, 4])` -> nests a list instead of adding two items.
- `a.extend("hi")` -> adds `'h'` and `'i'`.
- `def f(x, acc=[])` -> the same list is reused across calls.
- Removing items while looping over the same list -> items are skipped.
- `(5)` is not a tuple -> it's the int 5.
- `a[10]` raises IndexError but `a[10:]` returns `[]`.
- `queue.pop(0)` in a loop -> quadratic time; use deque.
- `a += [4]` changes every alias, `a = a + [4]` doesn't.
- `t = ([1],); t[0] += [2]` -> raises TypeError but the inner list is still changed.
- `zip(a, b)` with different lengths -> silently drops the extras; use `strict=True`.
- `[1, 2] + [3, 4]` / `[1, 2] * 2` -> concatenation and repetition, not element-wise maths.
- `random.shuffle(X)` then `random.shuffle(y)` -> features and labels no longer line up.
- `np.array([[1, 2], [3]])` -> ValueError (ragged); pad first.
- `losses.append(loss)` with a PyTorch tensor -> keeps the autograd graph alive; append `loss.item()`.
- `sorted([3, nan, 1])` -> not sorted and no error.
- `class M: layers = []` -> one list shared by every instance.
- `sorted(["b", "A", "a"])` -> uppercase sorts before lowercase.
- `a[::2] = [1]` when the slice has 3 items -> ValueError.

## Interview angle
- **"What's the difference between a list and a tuple?"** List is mutable, tuple is immutable and hashable (if its items are), so tuples can be dict keys and signal "fixed record". SDE analogy: tuple is a `final` value object.
- **"What's the time complexity of append, insert(0), pop(0), `in`?"** Append and pop from the end are amortised O(1) because the list is a dynamic array that over-allocates; insert/pop at the front shift every element, O(n); `in` is a linear scan. Use `deque` for queues and `set` for membership.
- **"Shallow vs deep copy?"** Shallow copies the outer container and shares inner objects; deep copy recursively copies everything. Same as copying a JS array with spread vs `structuredClone`.
- **"Why is a mutable default argument a bug?"** Defaults are evaluated once at function-definition time, so the same list is shared by every call. Use `None` and create the list inside.
- **"Is Python's sort stable, and what algorithm is it?"** Yes, stable; it's Timsort, an adaptive merge sort that is O(n) on already-sorted data and O(n log n) worst case.

## Source material
To be added
