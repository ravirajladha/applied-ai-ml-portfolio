# NumPy Arrays: coverage spec

**Ladder:** Foundations: Python & Data Tools › Python for Data   ·   **Prerequisites:** py-variables, py-lists, py-loops
**Why it matters for AI/ML:** every dataset, image, embedding and model weight is an n-dimensional array before it is anything else. PyTorch tensors copy NumPy's ideas (shape, dtype, views, strides) almost one to one, so shape and copy-vs-view mistakes here become silent bugs in training code later.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `why-arrays` | Arrays vs Python lists | one dtype per array, `*` and `+` differ from lists | upcasting on creation, memory of list vs array | why C loops over a packed buffer are fast; mixed int/str gives `<U21` | `dtype=object` arrays and why they are slow |
| 2 | `creating` | Creating arrays | `arange`, `ones`, `zeros`, `linspace` | `arange` vs `linspace`, `full`, `eye`, `empty`, `endpoint=False`, `default_rng` | float-step `arange` length surprise, `*_like` keeps dtype, explicit `dtype=` truncates, global seed vs Generator, `meshgrid` xy vs ij, `rng.random(dtype=np.float32)` | why pass a `Generator` around (no global state), `linspace(dtype=int)` truncation, int seed = `SeedSequence(seed)` |
| 3 | `attributes` | shape, ndim, size, dtype, itemsize, nbytes | `size`, `ndim`, `(5,)` shape tuple | `itemsize`/`nbytes`, `len()` = axis 0, `(5,)` vs `(5, 1)` | 0-d arrays, memory estimates, `<U` strings take 4 bytes per character | empty arrays, `nbytes` of a view vs the buffer it keeps alive |
| 4 | `dtypes` | dtypes, casting and upcasting | default `int64` / `float64` | assignment truncates, `astype(int)` truncates toward zero, bool arithmetic | NEP 50 weak Python scalars, promotion table (int8+uint8 -> int16), OverflowError for out-of-range Python ints, `astype` copies, uint8 image add/subtract wraparound, float16 integer spacing above 2048, widen before arithmetic, float16 max 65504 | integer `astype` wraps silently, float32 vs float64 equality, "safe" int64 -> float64 still loses precision, float16 rounding to inf at 65520, uint8 scalar average overflow, `uint8 + -1` raises and float32 * 1e300 stays float32 |
| 5 | `indexing` | Indexing and slicing (1D, 2D, 3D) | `a[i]`, `a[-1]`, `a[1:3]`, `a[row, col]` | `a[:, j]`, int index drops an axis, slice keeps it, negative steps | 3D indexing, `...` (Ellipsis), out-of-range slice vs index, `None` placement (`a[:, None, :]`, `a[..., None]`) | negative-step slice boundaries |
| 6 | `masks-fancy` | Boolean masks and fancy indexing | `a > 4` mask, `a[a > 4]` | `&` / `|` with brackets, `and` raises, index lists, masked assignment, counting with `.sum()` | paired index lists vs `np.ix_` (also for assignment), 2D mask returns 1D, row selection by label, repeated-index assignment (last wins), wrong-length mask raises IndexError, `nonzero` vs `argwhere`, `a[mask] += 1` is safe | buffered `a[idx] += 1` vs `np.add.at`, `bincount(weights=)` scatter-add, embedding-gradient accumulation bug, advanced-index axis placement rules |
| 7 | `views-copies` | Views vs copies | slices are views | slice writes back, fancy index copies, `=` is not a copy | `np.shares_memory`, `.base`, `+=` vs `x = x + 1`, `asarray` vs `array`, mutation through function args, reshape of a transpose copies, chained `a[[1, 2]][0] = 5` is lost, `a[...]` is a view | `ravel` vs `flatten` vs `a.T.ravel()`, `ravel(order="K")` on F arrays, which reshapes of a strided view copy, views keeping huge buffers alive, mask assignment through a copy, a reused buffer appended to a list |
| 8 | `reshaping` | Reshape, transpose, newaxis, squeeze | `reshape` fills row by row, element count must match | `-1`, `.T`, `np.newaxis`, `squeeze`, `expand_dims` | `transpose(axes)`, `moveaxis`, transpose is not reshape, two `-1`s, flattening a batch of images | `order='F'`, setting `.shape` on a non-contiguous array |
| 9 | `stack-split` | Stacking and splitting | `concatenate` of 1D arrays | `vstack`/`hstack`, `stack` adds an axis, `concatenate(axis=1)` | shape mismatch errors, `split` vs `array_split`, `column_stack` | split at indexes, why `np.append` in a loop is O(n^2) |
| 10 | `memory-layout` | Memory layout: C/F order, strides, contiguity | — | — | row-major vs column-major, `strides` (3D, int32, F order), contiguity flags, cache-friendly axis and cache lines, `as_strided` windows, `.T` is O(1), `ascontiguousarray` returns `a` when already contiguous | stride-0 broadcast views, `ascontiguousarray`, why slices can be views and index lists cannot, `sliding_window_view` (1D and 2D patches / im2col), negative strides and `torch.from_numpy`, `may_share_memory` vs `shares_memory`, why `as_strided` is unsafe |
| 11 | `special-values` | NaN, inf and structured arrays | `nan != nan` | `nansum`, `isnan`, `x == np.nan` is always False, division by zero gives inf | NaN into int arrays fails, invalid ops give NaN, `nanmax`/`nanmean`, `isfinite`, float16 overflow, `nanargmax` on all-NaN raises, `nan_to_num` defaults | `in` uses identity first, structured dtypes and their itemsize, field views with record strides, NaN in sort / argmax, `a > 0` vs `~(a <= 0)` with NaN |
| 12 | `ml-arrays` | Arrays in ML code: batches, images, sequences | `(n_samples, n_features)`, image `(H, W, C)` | row = y in `img[y, x]`, batch slicing and the short last batch, one-hot via `eye` rows and back via argmax, `np.stack` to build a batch | NHWC -> NCHW with `transpose`, batch memory in MB, uint8 / 255 gives float64, padding masks by broadcasting, `np.pad`, ragged lists raise, grayscale -> RGB with `repeat` vs `broadcast_to`, windowed (X, y) from a time series | `(time, batch)` reshape vs transpose, read-only `sliding_window_view`, in-place normalising a train view, `squeeze()` on a batch of one |

## Must-know facts
- An array has ONE dtype; mixing types on creation upcasts (int -> float -> str).
- NumPy 2 default integer is `int64` on every platform; default float is `float64`.
- `np.zeros`, `np.ones`, `np.eye` default to float64; `np.full` takes the dtype of the fill value.
- `arange(start, stop, step)` excludes stop; `linspace(start, stop, num)` includes stop by default.
- Shapes are tuples; `(5,)` is 1D and is not the same as `(5, 1)` or `(1, 5)`.
- `size` = product of shape; `nbytes` = size x itemsize; `len(a)` = `a.shape[0]`.
- Assignment into an array never changes its dtype: floats into an int array truncate; NaN into an int array raises.
- `astype` always copies by default; integer `astype` wraps modulo 2**bits without warning.
- NEP 50 (NumPy 2): Python scalars are "weak" and adopt the array's dtype; NumPy scalars and arrays are not.
- An integer index removes an axis; a slice (even of length 1) keeps it.
- Basic slicing returns a view; fancy (list) and boolean indexing return a copy. Test with `np.shares_memory`.
- Combine masks with `&`, `|`, `~` and brackets; `and`/`or` raise ValueError.
- `reshape` returns a view when it can and copies when it must; `flatten` always copies; `ravel` copies only when needed.
- Only one `-1` is allowed in a reshape.
- `stack` creates a new axis; `concatenate` joins along an existing one.
- C order = row-major (last index fastest); a transpose just swaps strides.
- `NaN != NaN`; use `np.isnan`; NaN propagates through sum / mean / max unless you use the `nan*` functions.
- Every comparison with NaN is False, so `a > 0` and `~(a <= 0)` disagree on NaN rows.
- Strides are bytes per step on each axis; slicing with a step multiplies them, a negative step negates them, `.T` swaps them. All O(1).
- `as_strided` has no bounds checks; `sliding_window_view` is the safe, read-only way to get overlapping windows.
- `a[idx] = vals` with repeated indices keeps one value (last in practice); `a[idx] += v` adds once; `np.add.at` / `np.bincount(weights=)` add every occurrence.
- uint8 arithmetic wraps mod 256 (including subtraction); widen to int16/float32 before maths on images.
- float16: integers exact only to 2048, max 65504, anything rounding past 65520 becomes inf.
- ML layout conventions: X is `(n_samples, n_features)`, images `(H, W, C)` or NCHW; change layout with `transpose`, never `reshape`.
- `squeeze()` removes every size-1 axis, including a batch of one; prefer `squeeze(axis=...)`.

## Common traps (each one must have at least one question)
- `list * 2` repeats, `array * 2` multiplies.
- `np.zeros(2, 3)` / passing the shape as separate arguments -> must be one tuple.
- `arange` with a float step can give an unexpected length -> use `linspace`.
- `np.empty` is assumed to be zeros -> it holds leftover memory.
- Assigning `9.7` into an int array -> silently truncated to 9.
- `astype(int)` on -1.7 -> -1 (toward zero, not floor).
- `astype(np.uint8)` on 300 -> 44 (silent wrap).
- int8 array + Python int 300 -> OverflowError in NumPy 2.
- `a[:, 1]` vs `a[:, 1:2]` -> shapes `(3,)` vs `(3, 1)`.
- Using `and` between masks -> ValueError (ambiguous truth value).
- Writing to a fancy-indexed or masked result -> only the copy changes.
- `b = a` -> no copy at all; both names see every change.
- `col += 1` vs `col = col + 1` on a view -> only the first changes the original.
- `a[[0, 0]] += 1` -> increments once; use `np.add.at`.
- `a[[0, 2], [1, 2]]` -> picks pairs, not a 2x2 block.
- `a.T.reshape(-1)` -> not the same order as `a.reshape(-1)`.
- `reshape(-1, 32)` on a batch -> mixes samples; keep the batch axis first.
- `np.split` with uneven sizes -> ValueError; use `array_split`.
- `np.append` in a loop -> O(n^2) copying.
- `x == np.nan` -> always False.
- `np.max` with a NaN present -> nan.
- A tiny view of a huge array -> keeps the whole buffer alive.
- `as_strided` with the wrong strides -> garbage or a crash; `sliding_window_view` is read-only, so `w -= ...` raises.
- `may_share_memory` -> True for interleaved views that share no bytes; use `shares_memory` for the exact answer.
- `torch.from_numpy(a[::-1])` -> ValueError (negative strides); copy first.
- `a[[1, 2]][0] = 5` -> writes into a temporary copy, `a` unchanged.
- `grad_E[ids] += g` with repeated token ids -> lost gradient; use `np.add.at`.
- uint8 `250 + 10` -> 4 and `10 - 20` -> 246; `(u[0] + u[1]) / 2` on uint8 scalars -> wrapped average.
- `np.float16(65520)` -> inf; `np.float16(2049)` -> 2048.
- `np.array([1], np.uint8) + -1` -> OverflowError in NumPy 2.
- `np.linspace(0, 1, 5, dtype=int)` -> `[0 0 0 0 1]`.
- `~(a <= 0)` used as "positive" -> keeps NaN rows.
- `img / 255` on uint8 -> float64, twice the memory of float32.
- `x.reshape(B, T)` on a `(T, B)` array -> scrambled sequences; use `x.T`.
- Appending a reused buffer to a list -> every entry is the last batch.
- `X_train = X[:n]; X_train -= mean` -> normalises X itself.
- `probs.squeeze().argmax(axis=1)` with a batch of one -> AxisError.
- `np.array(ragged_lists)` -> ValueError in NumPy 2; pad first.

## Interview angle
- **"Why use NumPy instead of lists?"** One contiguous typed buffer, so operations run as C loops with no per-element type checks, using far less memory. SDE analogy: a list is an array of pointers to boxed objects; an ndarray is a primitive `double[]` with shape metadata.
- **"What is a view, and how do you know if you have one?"** A view is a new array object (shape, strides, offset) over the same buffer. Slices give views; fancy and boolean indexing give copies. Check with `np.shares_memory(a, b)` or `b.base is a`. Analogy: a view is a reference, `.copy()` is a deep clone.
- **"What are strides?"** Bytes to jump per step along each axis. Transpose, slicing with steps and broadcasting just rewrite strides, which is why they are O(1). A stride of 0 repeats data without copying.
- **"What is the difference between `(n,)`, `(n, 1)` and `(1, n)`?"** A flat vector versus a column versus a row; they broadcast differently, and mixing them is the most common source of silent shape bugs.
- **"How do dtypes get promoted?"** To the smallest type that holds both inputs (int8 + uint8 -> int16, int + float -> float); in NumPy 2, Python scalars are weak and do not upcast an array.
- **"How would you build sliding windows over a long series without copying?"** `sliding_window_view(a, k)`: strides `(8, 8)` make windows overlap in the same buffer, read-only. `as_strided` does the same with no safety net. Copies only happen when you reshape the windows into a matrix (im2col).
- **"How do you accumulate gradients or counts with repeated indices?"** `np.add.at(target, idx, vals)` or `np.bincount(idx, weights, minlength)`; `target[idx] += vals` silently drops duplicates because it is read-all, add, write-all.
- **"Why does my image look wrong after brightening or differencing?"** uint8 wraps mod 256; widen first, compute, then `clip` and cast back.

## Source material
To be added.
