# NumPy Operations: coverage spec

**Ladder:** Foundations: Python & Data Tools › Python for Data   ·   **Prerequisites:** np-arrays, py-loops, py-functions
**Why it matters for AI/ML:** a model's forward pass is just ufuncs, broadcasting, reductions and matrix multiplies. Softmax, normalisation, distances, attention scores and loss functions are all one-liners in NumPy, and the same shape rules and numerical traps carry straight over to PyTorch.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `ufuncs` | Element-wise arithmetic and ufuncs | scalar + array, `*` is element-wise, `np.sqrt`, `np.exp` | `/` vs `//`, floor division of negatives, `**` vs `^`, `np.maximum` vs `np.max`, maths ufuncs return float | `ufunc.outer`, `.reduce` / `.accumulate` | `where=` with `out=` for safe division |
| 2 | `broadcasting` | Broadcasting rules | scalar broadcasting | the right-aligned rule, column + row table, compatible vs incompatible shapes, total size is irrelevant | 4D shape arithmetic, centring with `axis=1` fails, `np.broadcast_shapes`, in-place output can't grow, inputs not copied | memory blow-up of pairwise broadcasting, read-only `broadcast_to`, `(n,)` vs `(n, 1)` accuracy bug |
| 3 | `aggregation` | Aggregation and the axis argument | `sum`/`mean`/`max`, axis=0 collapses rows, mean of ints is float | `axis=0` vs `axis=1`, flat `argmax`, `keepdims` | `cumsum` flattening, `ddof` (NumPy vs pandas std), multi-axis reductions, empty `sum` vs `max` | small-int sums accumulate in int64 while `+` wraps, `keepdims` in broadcasting + evaluation order |
| 4 | `compare-where` | Comparisons, np.where and np.clip | `np.clip`, `np.where(cond, a, b)` as ReLU, `==` is element-wise | one-argument `np.where`, `any`/`all`, `array_equal` vs `==`, one-sided clip | both branches are evaluated, `np.select`, branch dtype promotion | array bounds in clip, no short-circuit |
| 5 | `sorting` | Sorting, argsort and unique | `np.sort` | `argsort`, `a.sort()` returns None, `unique` + counts, descending order | default axis=-1, sort rows by a column, ranks via double argsort, `return_inverse` label encoding, `argpartition` top-k | stable sorts and ties, top-k at scale, NaN in `unique`, `searchsorted` |
| 6 | `linalg` | Linear algebra: dot, @, solve, norm | `*` vs `@`, 1D dot product | matmul shape rule, inner-dim mismatch, `A * I` vs `A @ I`, L2 norm, `@` is `matmul` | `solve`, why not `inv`, 1D operands of `@`, `.T` on 1D is a no-op, singular matrix error, batched `@` | `np.dot` vs `matmul` on N-d, matrix norms (`ord`, axis), `einsum`, condition numbers |
| 7 | `vectorisation` | Vectorisation vs Python loops | what vectorising means | rewrite loops as `a * b + 1` / `np.dot`, element loops over arrays are slow | why loops are 50-100x slower, `np.vectorize` is not compiled, recurrences, row-wise reductions | `np.vectorize` output dtype trap, chunking to bound memory |
| 8 | `inplace` | In-place operations and out= | — | `a += 1` vs `a = a + 1` with aliases, casting error on `int += float`, `out=` reuses memory | overlapping in-place ops are buffered, why in-place saves memory, `casting='unsafe'` | `where=` without `out=` leaves garbage, writing through `out=` into a view |
| 9 | `precision` | Integer overflow and float precision | `0.1 + 0.2 != 0.3` | `isclose` / `allclose`, int8 wraps silently, never `==` on floats | float grids from `arange`, int64 wrap and float32 mantissa, default `atol` on tiny numbers, scalar overflow warns | `isclose` is asymmetric, non-associative addition, machine epsilon |
| 10 | `random` | Random numbers with seeds | why seed, `integers` high is exclusive | `random`, `normal(loc, scale)`, `choice(replace=False)`, `shuffle` vs `permutation` | shuffle X and y together, a stream is consumed the same way in batches or singly, re-seeding inside a loop | `SeedSequence.spawn` for workers, `endpoint=True`, cross-machine reproducibility |
| 11 | `ml-idioms` | ML idioms: scaling, one-hot, softmax, distances | accuracy as the mean of a mask | min-max scaling, standardisation per column, one-hot via `eye`, unit-norm rows | one-hot via broadcasting, softmax with keepdims (and the silent square-batch bug), cosine similarity, pairwise distances, top-k classes, fit statistics on train only | batched attention scores, expanded-distance cancellation, argmax of softmax = argmax of logits |
| 12 | `stability` | Numerical stability | — | — | softmax overflow and the max trick (why it is exact), logsumexp, `log(0)` in losses | `log1p`/`expm1`, catastrophic cancellation in variance, float32 running sums vs pairwise sum, stable log-sigmoid, float16 NaNs, scaled norms |

## Must-know facts
- Arithmetic operators and ufuncs are element-wise; `*` is never matrix multiplication; use `@`.
- Broadcasting: align shapes from the right; each pair must be equal or contain a 1; missing axes count as 1.
- Broadcasting never copies the inputs, but the result is fully allocated.
- `axis=k` means "this axis disappears"; `keepdims=True` keeps it as size 1 so the result broadcasts back.
- `argmax` without an axis returns an index into the flattened array.
- `np.std` defaults to `ddof=0`; pandas defaults to `ddof=1`.
- `np.where(cond, a, b)` evaluates both `a` and `b` everywhere; one-argument `np.where` returns a tuple of index arrays.
- `a.sort()` sorts in place and returns None; `np.sort` returns a copy; `np.unique` returns sorted values.
- `argpartition` gives top-k in O(n); a full sort is O(n log n).
- `(m, k) @ (k, n) -> (m, n)`; `@` broadcasts leading batch axes; `np.dot` does not batch.
- Use `np.linalg.solve`, not `inv(A) @ b`.
- Python loops cost tens of nanoseconds per element; `np.vectorize` is still a Python loop.
- `a += b` writes into `a` (aliases see it) and cannot change `a`'s dtype or shape; `a = a + b` allocates a new array.
- Integer arrays wrap on overflow silently; never compare floats with `==`; `np.isclose` default `atol=1e-8` dominates for tiny values.
- Seed with `rng = np.random.default_rng(seed)`, create it once, and pass it around.
- Softmax: subtract the row max, sum with `keepdims=True`; logsumexp: `m + log(sum(exp(x - m)))`.
- float16 overflows above 65504; float32 integers are exact only up to 2**24.

## Common traps (each one must have at least one question)
- `a ^ 2` -> XOR, not power.
- `-5 // 2` -> -3 (floor), unlike C/Java/JS.
- `np.max(a, b)` vs `np.maximum(a, b)` -> reduction vs pairwise.
- `(2, 3) + (2,)` -> ValueError; compare from the right.
- `X - X.mean(axis=1)` -> ValueError (or silently wrong for square X); use `keepdims=True`.
- `y_true (n,) == y_pred (n, 1)` -> a broadcast (n, n) table, wrong accuracy.
- `a += b` where the result would be bigger than `a` -> ValueError.
- Pairwise broadcasting on big inputs -> a huge allocation.
- `argmax()` without axis on 2D -> flat index.
- `np.std` vs pandas `.std()` -> different answers (ddof).
- `np.array([]).max()` -> ValueError.
- int8 `+` wraps while int8 `.sum()` does not.
- `np.where(x != 0, 1 / x, 0)` -> still computes 1/0.
- `a.sort()` -> returns None.
- `np.sort` has no descending flag -> use `[::-1]`.
- `A * B` used where `A @ B` was meant.
- `v.T` on a 1D vector -> unchanged.
- `np.dot` on 3D arrays -> not a batch matmul.
- `np.vectorize` -> no speed-up, and output dtype taken from the first result.
- `int_array += 0.5` -> casting error.
- `np.divide(..., where=...)` without `out=` -> garbage values.
- `0.1 + 0.2 == 0.3` -> False; `arange` grid value `== 0.3` -> False.
- `np.isclose(1e-10, 2e-10)` -> True by default.
- Re-creating `default_rng(0)` per batch -> identical "random" numbers every batch.
- Shuffling X and y separately -> scrambled labels.
- `rng.integers(0, 10)` never returns 10.
- Softmax without `keepdims` -> wrong probabilities with no error on square batches.
- Naive softmax / logsumexp on large logits -> nan / inf.
- `E[x^2] - E[x]^2` -> catastrophic cancellation.
- Expanded distance `|a|^2 + |b|^2 - 2a.b` -> lost precision, even negative values.
- Standardising with statistics from the full dataset -> data leakage.

## Interview angle
- **"Explain broadcasting."** Shapes are compared from the right; sizes must match or be 1, and size-1 axes are stretched with stride 0, so nothing is copied. Example: `(n, d) - (d,)` centres every row. SDE analogy: like a `map` that reuses one config object for every element instead of cloning it.
- **"Why is vectorised code faster than a loop?"** The loop moves from the interpreter (bytecode, boxing, dynamic dispatch per element) into one typed C loop over contiguous memory, often SIMD. Analogy: one bulk SQL statement versus N round-trips.
- **"Implement softmax in NumPy. What can go wrong?"** `e = np.exp(x - x.max(axis=-1, keepdims=True)); e / e.sum(axis=-1, keepdims=True)`. Without the max shift it overflows to nan; without keepdims it divides by the wrong sums.
- **"How do you compute pairwise distances efficiently?"** Broadcasting `A[:, None] - B[None]` is clear but uses O(n*m*d) memory; the `|a|^2 + |b|^2 - 2 A @ B.T` form is one matmul but needs clipping at 0 and loses precision for far-from-origin data; chunk for big inputs.
- **"Why do floats break `==`, and how do you test numeric code?"** Binary rounding means equal maths gives different bits; use `np.allclose` with sensible `rtol`/`atol`, set `atol=0` for tiny magnitudes. Analogy: `assertEquals(expected, actual, delta)`.

## Source material
To be added.
