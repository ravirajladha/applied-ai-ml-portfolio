# NumPy Arrays: coverage spec

**Ladder:** Foundations: Python & Data Tools › Python for Data   ·   **Prerequisites:** py-variables, py-lists, py-loops
**Why it matters for AI/ML:** every dataset, image, embedding and model weight is an n-dimensional array before it is anything else. PyTorch tensors copy NumPy's ideas (shape, dtype, views, strides) almost one to one, so shape and copy-vs-view mistakes here become silent bugs in training code later.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `why-arrays` | Arrays vs Python lists | one dtype per array, `*` and `+` differ from lists | upcasting on creation, memory of list vs array | why C loops over a packed buffer are fast; mixed int/str gives `<U21` | `dtype=object` arrays and why they are slow |
| 2 | `creating` | Creating arrays | `arange`, `ones`, `zeros`, `linspace` | `arange` vs `linspace`, `full`, `eye`, `empty`, `endpoint=False`, `default_rng` | float-step `arange` length surprise, `*_like` keeps dtype, explicit `dtype=` truncates, global seed vs Generator | why pass a `Generator` around (no global state) |
| 3 | `attributes` | shape, ndim, size, dtype, itemsize, nbytes | `size`, `ndim`, `(5,)` shape tuple | `itemsize`/`nbytes`, `len()` = axis 0, `(5,)` vs `(5, 1)` | 0-d arrays, memory estimates | empty arrays, `nbytes` of a view vs the buffer it keeps alive |
| 4 | `dtypes` | dtypes, casting and upcasting | default `int64` / `float64` | assignment truncates, `astype(int)` truncates toward zero, bool arithmetic | NEP 50 weak Python scalars, promotion table (int8+uint8 -> int16), OverflowError for out-of-range Python ints, `astype` copies | integer `astype` wraps silently, float32 vs float64 equality, "safe" int64 -> float64 still loses precision |
| 5 | `indexing` | Indexing and slicing (1D, 2D, 3D) | `a[i]`, `a[-1]`, `a[1:3]`, `a[row, col]` | `a[:, j]`, int index drops an axis, slice keeps it, negative steps | 3D indexing, `...` (Ellipsis), out-of-range slice vs index | negative-step slice boundaries |
| 6 | `masks-fancy` | Boolean masks and fancy indexing | `a > 4` mask, `a[a > 4]` | `&` / `|` with brackets, `and` raises, index lists, masked assignment, counting with `.sum()` | paired index lists vs `np.ix_`, 2D mask returns 1D, row selection by label | buffered `a[idx] += 1` vs `np.add.at`, advanced-index axis placement rules |
| 7 | `views-copies` | Views vs copies | slices are views | slice writes back, fancy index copies, `=` is not a copy | `np.shares_memory`, `.base`, `+=` vs `x = x + 1`, `asarray` vs `array`, mutation through function args | `ravel` vs `flatten` vs `a.T.ravel()`, views keeping huge buffers alive, mask assignment through a copy |
| 8 | `reshaping` | Reshape, transpose, newaxis, squeeze | `reshape` fills row by row, element count must match | `-1`, `.T`, `np.newaxis`, `squeeze`, `expand_dims` | `transpose(axes)`, `moveaxis`, transpose is not reshape, two `-1`s, flattening a batch of images | `order='F'`, setting `.shape` on a non-contiguous array |
| 9 | `stack-split` | Stacking and splitting | `concatenate` of 1D arrays | `vstack`/`hstack`, `stack` adds an axis, `concatenate(axis=1)` | shape mismatch errors, `split` vs `array_split`, `column_stack` | split at indexes, why `np.append` in a loop is O(n^2) |
| 10 | `memory-layout` | Memory layout: C/F order, strides, contiguity | — | — | row-major vs column-major, `strides`, contiguity flags, cache-friendly axis | stride-0 broadcast views, `ascontiguousarray`, why slices can be views and index lists cannot, `sliding_window_view` |
| 11 | `special-values` | NaN, inf and structured arrays | `nan != nan` | `nansum`, `isnan`, `x == np.nan` is always False, division by zero gives inf | NaN into int arrays fails, invalid ops give NaN, `nanmax`/`nanmean`, `isfinite`, float16 overflow | `in` uses identity first, structured dtypes and their itemsize, NaN in sort / argmax |

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

## Interview angle
- **"Why use NumPy instead of lists?"** One contiguous typed buffer, so operations run as C loops with no per-element type checks, using far less memory. SDE analogy: a list is an array of pointers to boxed objects; an ndarray is a primitive `double[]` with shape metadata.
- **"What is a view, and how do you know if you have one?"** A view is a new array object (shape, strides, offset) over the same buffer. Slices give views; fancy and boolean indexing give copies. Check with `np.shares_memory(a, b)` or `b.base is a`. Analogy: a view is a reference, `.copy()` is a deep clone.
- **"What are strides?"** Bytes to jump per step along each axis. Transpose, slicing with steps and broadcasting just rewrite strides, which is why they are O(1). A stride of 0 repeats data without copying.
- **"What is the difference between `(n,)`, `(n, 1)` and `(1, n)`?"** A flat vector versus a column versus a row; they broadcast differently, and mixing them is the most common source of silent shape bugs.
- **"How do dtypes get promoted?"** To the smallest type that holds both inputs (int8 + uint8 -> int16, int + float -> float); in NumPy 2, Python scalars are weak and do not upcast an array.

## Source material
To be added.
