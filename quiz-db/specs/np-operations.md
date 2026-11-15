# NumPy Operations: coverage spec

**Ladder:** Foundations: Python & Data Tools › Python for Data   ·   **Prerequisites:** np-arrays, py-loops, py-functions
**Why it matters for AI/ML:** a model's forward pass is just ufuncs, broadcasting, reductions and matrix multiplies. Softmax, normalisation, distances, attention scores and loss functions are all one-liners in NumPy, and the same shape rules and numerical traps carry straight over to PyTorch.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `ufuncs` | Element-wise arithmetic and ufuncs | scalar + array, `*` is element-wise, `np.sqrt`, `np.exp`, `np.abs`, `np.round(a, 1)` | `/` vs `//`, floor division of negatives, `**` vs `^`, `np.maximum` vs `np.max`, maths ufuncs return float | `ufunc.outer`, `.reduce` / `.accumulate`, `np.add.at` | `where=` with `out=` for safe division |
| 2 | `broadcasting` | Broadcasting rules | scalar broadcasting | the right-aligned rule, column + row table, compatible vs incompatible shapes, total size is irrelevant | 4D shape arithmetic, centring with `axis=1` fails, `np.broadcast_shapes`, in-place output can't grow, inputs not copied (but the output is allocated), per-channel mean on NCHW needs keepdims, batch norm by hand | memory blow-up of pairwise broadcasting, read-only `broadcast_to`, `(n,)` vs `(n, 1)` accuracy bug |
| 3 | `aggregation` | Aggregation and the axis argument | `sum`/`mean`/`max`, axis=0 collapses rows, mean of ints is float, `min` vs `argmin`, `np.mean` on a list, `np.sum(a)` = `a.sum()` | `axis=0` vs `axis=1`, flat `argmax`, `keepdims` | `cumsum` flattening, `ddof` (NumPy vs pandas std), multi-axis reductions, empty `sum` vs `max`, `np.average(weights=)`, `argmax(keepdims=True)` | small-int sums accumulate in int64 while `+` wraps, `keepdims` in broadcasting + evaluation order, float16 `cumsum` stalls at 2048 while `sum` is pairwise |
| 4 | `compare-where` | Comparisons, np.where and np.clip | `np.clip`, `np.where(cond, a, b)` as ReLU, `==` is element-wise | one-argument `np.where`, `any`/`all`, `array_equal` vs `==`, one-sided clip | both branches are evaluated, `np.select` (first true condition wins), branch dtype promotion | array bounds in clip, swapped clip bounds give a constant, no short-circuit |
| 5 | `sorting` | Sorting, argsort and unique | `np.sort` | `argsort`, `a.sort()` returns None, `unique` + counts, descending order | default axis=-1, sort rows by a column, ranks via double argsort, `return_inverse` label encoding, `argpartition` top-k (unordered), `take_along_axis` vs `s[idx]` | stable sorts and ties, `argsort(-a)` vs `argsort(a)[::-1]` tie order, `lexsort` key priority, top-k at scale, NaN in `unique`, `searchsorted` |
| 6 | `linalg` | Linear algebra: dot, @, solve, norm | `*` vs `@`, 1D dot product | matmul shape rule, inner-dim mismatch, `A * I` vs `A @ I`, L2 norm, `@` is `matmul` | `solve`, why not `inv`, 1D operands of `@`, `.T` on 1D is a no-op, singular matrix error, batched `@`, `(B, T, d) @ (d, h)`, `*` vs `@` on 3D, einsum attention scores / trace / transpose / row-wise dots, `'bij,bjk->bik'` | `np.dot` vs `matmul` on N-d, matrix norms (`ord`, axis), `einsum` (and why plain einsum skips BLAS), condition numbers |
| 7 | `vectorisation` | Vectorisation vs Python loops | what vectorising means | rewrite loops as `a * b + 1` / `np.dot`, element loops over arrays are slow | why loops are 50-100x slower, `np.vectorize` is not compiled, recurrences, row-wise reductions, `maximum.accumulate` and `diff` | `np.vectorize` output dtype trap, chunking to bound memory (chunked k-NN with argpartition) |
| 8 | `inplace` | In-place operations and out= | — | `a += 1` vs `a = a + 1` with aliases, casting error on `int += float`, `out=` reuses memory | overlapping in-place ops are buffered, `x[1:] = x[:-1]` shifts cleanly, why in-place saves memory, `out=` allocates no temporary, `casting='unsafe'`, `int_array *= 0.5` raises | `where=` without `out=` leaves garbage, writing through `out=` into a view, `a += a.T` overlap detection |
| 9 | `precision` | Integer overflow and float precision | `0.1 + 0.2 != 0.3` | `isclose` / `allclose`, int8 wraps silently, never `==` on floats | float grids from `arange`, int64 wrap and float32 mantissa, `1e8 + 1` in float32, float32 `+=` loop drift vs `np.sum`, default `atol` on tiny numbers, scalar overflow warns | `isclose` is asymmetric, non-associative addition, machine epsilon, `np.prod` silently wraps (even positive), BLAS results differ in the last bits across machines |
| 10 | `random` | Random numbers with seeds | why seed, `integers` high is exclusive | `random`, `normal(loc, scale)`, `choice(replace=False)`, `shuffle` vs `permutation` | shuffle X and y together, a stream is consumed the same way in batches or singly, re-seeding inside a loop, save/restore `bit_generator.state`, `choice(p=...)` | `SeedSequence.spawn` / `rng.spawn` for workers, `permuted` vs `permutation` with axis, `endpoint=True`, cross-machine reproducibility |
| 11 | `ml-idioms` | ML idioms: scaling, one-hot, softmax, distances | accuracy as the mean of a mask, `argmax` of scores is the predicted class | min-max scaling, standardisation per column, one-hot via `eye`, unit-norm rows | one-hot via broadcasting, softmax with keepdims (and the silent square-batch bug), cosine similarity, pairwise distances, top-k classes, fit statistics on train only | batched attention scores, expanded-distance cancellation, argmax of softmax = argmax of logits |
| 12 | `stability` | Numerical stability | — | — | softmax overflow and the max trick (why it is exact), logsumexp, `log(0)` in losses, cross-entropy from logits via log-softmax | `log1p`/`expm1`, catastrophic cancellation in variance, float32 running sums vs pairwise sum, stable log-sigmoid / BCE with logits, float16 softmax overflow, logsumexp of an all `-inf` (fully masked) row, scaled norms |
| 13 | `ml-numpy` | ML from scratch in NumPy: linear models, k-NN, mini-batches | `w @ x` prediction, MSE in one line | `X @ w + b` for a batch, bias column trick | one gradient-descent step by hand, k-NN vote with `argsort` + `bincount`, vectorised 1-NN with a distance table, `lstsq` closed form, shuffled mini-batches from one permutation, squared distance is enough for ranking | `(n, 1)` vs `(n,)` gradient shape bug, central-difference gradient check, softmax-CE gradient `(P - Y) / n`, normal equations square the condition number |

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
- einsum: letters missing from the output are summed; `'bqd,bkd->bqk'` is batched `Q @ K^T`. Plain einsum doesn't use BLAS; `@` does.
- `argpartition` top-k is unordered; sort the k winners afterwards. Use `take_along_axis` to apply per-row indexes.
- `lexsort` sorts by its LAST key first.
- `np.select` and `np.where` chains pick the first true condition.
- Overlapping in-place ops (`x[1:] = x[:-1]`, `a += a.T`) are detected and buffered, so they give the mathematically correct answer.
- `np.sum` uses pairwise summation; running totals (`+=` loops, `cumsum`) in low precision drift or stall.
- Cross-entropy from logits: `logits - logsumexp(logits)`, then pick `log_p[np.arange(n), y]`; its gradient is `(P - Y) / n`.
- Save `rng.bit_generator.state` in checkpoints to resume the same random stream; use `rng.spawn` for workers.
- Linear models from scratch: prediction `X @ w + b`, MSE gradient `(2/n) X.T @ (X @ w - y)`, closed form via `lstsq`, never `inv(X.T @ X)`.

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
- `x - x.mean(axis=(0, 2, 3))` on NCHW -> lines up with width, not channels; use keepdims.
- `np.argpartition(a, -k)[-k:]` treated as ranked -> wrong order.
- `s[argsort_idx]` for per-row results -> whole rows (or IndexError); use `take_along_axis`.
- `argsort(a)[::-1]` as "stable descending" -> ties reversed; use `argsort(-a, kind="stable")`.
- `np.lexsort((primary, secondary))` -> sorts by secondary first.
- `np.select([x > 10, x > 20], ...)` -> the broader condition shadows the narrower one.
- `np.clip(p, hi, lo)` with swapped bounds -> every value becomes the second bound, no error.
- `int_array *= 0.5` -> UFuncTypeError.
- float32 `+=` loop over 100k values -> visible drift; float16 `cumsum` stalls at 2048.
- `np.prod` of 1..25 in int64 -> wraps to a plausible positive number.
- float32 `1e8 + 1` -> `1e8`.
- logsumexp of an all `-inf` row -> nan (fully masked attention row).
- Naive `log(sigmoid(z))` BCE -> inf for confident wrong predictions; use the logits form.
- float16 softmax with logits around 11 -> sum overflows, probabilities all 0.
- `rng.permuted(M, axis=1)` used to shuffle features -> rows shuffled independently, columns misaligned.
- `(X @ w - y)` with `w` (d, 1) and `y` (n,) -> (n, n) residuals, gradient of the wrong shape.
- `inv(X.T @ X) @ X.T @ y` -> condition number squared, garbage weights for collinear features.

## Interview angle
- **"Explain broadcasting."** Shapes are compared from the right; sizes must match or be 1, and size-1 axes are stretched with stride 0, so nothing is copied. Example: `(n, d) - (d,)` centres every row. SDE analogy: like a `map` that reuses one config object for every element instead of cloning it.
- **"Why is vectorised code faster than a loop?"** The loop moves from the interpreter (bytecode, boxing, dynamic dispatch per element) into one typed C loop over contiguous memory, often SIMD. Analogy: one bulk SQL statement versus N round-trips.
- **"Implement softmax in NumPy. What can go wrong?"** `e = np.exp(x - x.max(axis=-1, keepdims=True)); e / e.sum(axis=-1, keepdims=True)`. Without the max shift it overflows to nan; without keepdims it divides by the wrong sums.
- **"How do you compute pairwise distances efficiently?"** Broadcasting `A[:, None] - B[None]` is clear but uses O(n*m*d) memory; the `|a|^2 + |b|^2 - 2 A @ B.T` form is one matmul but needs clipping at 0 and loses precision for far-from-origin data; chunk for big inputs.
- **"Implement k-NN / linear regression in NumPy."** k-NN: distance table by broadcasting (squared is enough), `argpartition` for the k nearest, `bincount(...).argmax()` for the vote, chunk the test set to bound memory. Linear regression: `lstsq` on `[X, 1]`, or gradient descent with `(2/n) X.T @ (X @ w - y)`; assert `grad.shape == w.shape` and check the gradient with central differences.
- **"Write attention scores with einsum, and is it fast?"** `np.einsum('bqd,bkd->bqk', Q, K) / sqrt(d)`. It documents shapes nicely, but `Q @ K.transpose(0, 2, 1)` goes through BLAS and is usually faster unless you pass `optimize=True`.
- **"Why do floats break `==`, and how do you test numeric code?"** Binary rounding means equal maths gives different bits; use `np.allclose` with sensible `rtol`/`atol`, set `atol=0` for tiny magnitudes. Analogy: `assertEquals(expected, actual, delta)`.

## Source material
To be added.
