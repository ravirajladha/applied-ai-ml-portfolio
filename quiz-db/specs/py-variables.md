# Variables & Types: coverage spec

**Ladder:** Python core › Basics   ·   **Prerequisites:** py-basics
**Why it matters for AI/ML:** every tensor, DataFrame and model is reached through a name. Aliasing (two names, one object) is behind many "my data changed by itself" bugs, and float precision explains why losses and metrics never compare exactly equal.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `binding` | Names and binding | `=` binds a name, rebinding doesn't affect copies of the old value, a value is stored not a formula | aliasing a list, `del` | `del` removes a name, not the object; call-by-sharing; `x = y = []` shares one list; shallow `dict.copy()` of a nested config | call-by-sharing interview answer |
| 2 | `core-types` | int, float, str, bool, None | `type()` of each literal | int + float -> float, bool is an int | `None` comparisons, `isinstance(True, int)`, `complex`, summing bools for accuracy | `1`, `True`, `1.0` as the same dict key, `hash(-1) == hash(-2)` |
| 3 | `conversion` | Type conversion | `int()`, `float()`, `str()` | `int("3.5")` fails, `bool("False")`, `bool([0])`, whitespace, `float("1e-3")` | bases, `bin`/`hex`/`oct`, `int("1e3")` fails, `int()` truncates toward zero, underscores, `json.dumps` spelling (`true`, `null`) | `int(s, 0)` reads prefixes, Unicode digits (`int("１２")`) |
| 4 | `dynamic-typing` | Dynamic vs strong typing | no type declarations, rebinding to another type | `"1" + 1` TypeError, `isinstance`, duck typing | type hints are not enforced but are stored in `__annotations__`, bools pass `isinstance(v, (int, float))` | — |
| 5 | `identity` | Mutability and identity: `is`, `==`, `id` | `==` compares values | `is` vs `==`, `is None`, mutable vs immutable | `+=` vs `+` on lists and tuples, tuple holding a list, unhashable list keys, True/False/None singletons, `id` reuse | NaN and container equality, `t[1] += [3]` both fails and mutates, `is` doesn't imply `==` |
| 6 | `caching` | Small-int caching | — | — | `-5..256` cache, `int("257") is int("257")`, why the cache exists | constants shared within one compiled unit |
| 7 | `floats` | Float precision | `0.1 + 0.2` | `round` before comparing, Decimal for money | `math.isclose`, `math.fsum`, `1e16 + 1`, NaN, inf arithmetic, `f"{0.1:.20f}"`, `round(2.675, 2)` | non-associativity, int vs float exact compare, `Decimal(0.1)`, `isclose` vs 0 needs `abs_tol`, `-0.0`, epsilon, `sum()` is compensated since 3.12 |
| 8 | `unpacking` | Multiple assignment and unpacking | `a, b = 1, 2`, `x = y = 0` | swap, starred `*rest`, count mismatch, `_` for ignored values, unpacking a str | `*mid`, empty star, unpacking a dict gives keys, `a, b = 1` TypeError, only one star | left-to-right target assignment, `i = x[i] = 1` |
| 9 | `naming` | Naming rules and conventions | valid names, no spaces, case-sensitivity, snake_case | keywords vs shadowing built-ins, UPPER_CASE constants | leading underscore convention, `Final` not enforced, soft keywords (`match`, `case`, `type`), `del` a shadowing name | `__name` mangling, NFKC-normalised identifiers |
| 10 | `scope` | Scope basics | local variables stay inside the function | assignment inside a function creates a local, no block scope for `if`/`for`, notebook globals | UnboundLocalError, `global` (even for new names), mutating a global needs no `global`, `nonlocal`, lookup at call time | nested `nonlocal`, `except ... as e` is deleted, class body isn't an enclosing scope |
| 11 | `lifetime` | Object lifetime: reference counting and garbage collection | — | — | reference counting, `sys.getrefcount`, `__del__` runs when the last reference goes, `gc` | reference cycles and `gc.collect()`, `weakref`, immortal objects (3.12+), why `del model` doesn't free GPU memory |
| 12 | `ml-precision` | Number types in ML code: float32, float16, NumPy scalars | weights are floats | Python float is float64, PyTorch defaults to float32 | float16 overflow at 65504, float32 integer limit 2**24, memory per dtype, why float32, NumPy scalars aren't JSON-serialisable | NEP 50 weak Python scalars, `isinstance(np.float32(1), float)` is False, `.item()`, bfloat16 vs float16, float16 integer limit 2048, silent int32 overflow |

## Must-know facts
- A variable is a name bound to an object; `=` never copies, it binds.
- Every value has a type (`type(x)`); names don't. Python is dynamically but strongly typed.
- `int` is unlimited precision; `float` is a 64-bit IEEE 754 double; `bool` is a subclass of `int` (`True == 1`).
- `None` is a singleton; test it with `is None`.
- `int()` on a float truncates toward zero; `int("3.5")` raises ValueError; `int()` accepts surrounding whitespace and underscores.
- `bool(x)` is False only for "empty/zero" values: `0`, `0.0`, `""`, `[]`, `{}`, `None`, `False`. `bool("False")` is True.
- `==` asks "equal value?" (calls `__eq__`); `is` asks "same object?" (compares `id`).
- Immutable: int, float, str, bool, tuple, None. Mutable: list, dict, set.
- `a += [x]` mutates a list in place; `a = a + [x]` builds a new list.
- CPython caches ints from -5 to 256; never rely on `is` for numbers or strings.
- `0.1 + 0.2 != 0.3`; compare floats with `math.isclose` or a tolerance.
- `float("nan") != float("nan")`.
- `a, b = b, a` swaps by building a tuple first; `first, *rest = seq` collects the remainder into a list.
- Assigning to a name anywhere in a function makes it local for the whole function (UnboundLocalError if read first). `global` / `nonlocal` change that.
- Lookup order is LEGB: Local, Enclosing, Global, Built-in.
- CPython frees an object when its reference count reaches 0; the `gc` module collects reference cycles.
- Python float = NumPy float64 (8 bytes); PyTorch defaults to float32 (4 bytes); float16/bfloat16 are 2 bytes.
- NumPy scalars (`np.int64`, `np.float32`) are not Python ints/floats; `.item()` converts them.

## Common traps (each one must have at least one question)
- `b = a` then mutating `a` -> `b` sees the change (same list).
- `b = a` then rebinding `a` -> `b` keeps the old value.
- `int("3.5")` -> ValueError; use `int(float("3.5"))`.
- `bool("False")` -> True (non-empty string).
- `int(3.9)` -> 3, not 4 (truncation, not rounding).
- `x is 257` style checks -> behaviour depends on caching; use `==`.
- `x == None` -> works but is wrong style; `is None` is correct and can't be fooled by `__eq__`.
- `0.1 + 0.2 == 0.3` -> False.
- `a, b = [1, 2, 3]` -> ValueError: too many values to unpack.
- Naming a variable `list`, `str` or `input` -> the built-in is shadowed; later calls fail with TypeError.
- Reading a global then assigning it in the same function -> UnboundLocalError.
- Type hints like `x: int = "hi"` -> no error at runtime.
- A tuple "can't change" -> but a list inside it can.
- `{1: "a", True: "b"}` -> one key, because `True == 1` and they hash the same.
- `x = y = []` -> one shared list, not two.
- `config.copy()` on a nested config -> inner lists/dicts are still shared; use `copy.deepcopy`.
- `int("1e3")` -> ValueError, although `float("1e3")` works.
- `isinstance(v, (int, float))` -> also accepts `True`/`False`.
- `t[1] += [3]` on a tuple holding a list -> raises TypeError AND changes the list.
- `math.isclose(x, 0.0)` -> False for any non-zero x; pass `abs_tol`.
- `except E as e:` then using `e` after the block -> NameError.
- `del model` in a notebook -> memory isn't freed while other references (optimizer, `Out`, `_`) remain.
- float16 values above 65504 -> inf; integers above 2048 aren't exact.
- `json.dumps` on NumPy scalars -> TypeError; convert with `.item()`.
- NumPy int32 arrays -> overflow wraps silently; Python ints never overflow.

## Interview angle
- **"Is Python pass-by-value or pass-by-reference?"** Neither: call by sharing (object reference passed by value). The function gets a new name for the same object: mutating it is visible to the caller, rebinding the parameter is not. Same as Java object references or JS objects.
- **"`is` vs `==`?"** `==` compares values, `is` compares identity. Use `is` only for singletons (`None`, `True`, `False`, sentinels). Small-int caching makes `is` look like it works for small numbers, which is a trap.
- **"Why is `0.1 + 0.2 != 0.3`?"** Binary floating point can't represent 0.1 exactly; the tiny errors add up. Compare with a tolerance (`math.isclose`, `np.allclose`), or use `Decimal` for money.
- **"Dynamically vs strongly typed?"** Types are checked at runtime and attached to values, not names (dynamic), but Python won't silently coerce `"1" + 1` (strong). JS is dynamic and weak.
- **"What's an UnboundLocalError?"** Python decides at compile time that a name assigned in a function is local; reading it before the assignment fails. Fix with `global`/`nonlocal` or a parameter.
- **"How does Python manage memory?"** Reference counting frees most objects the moment the last reference goes; a cycle collector (`gc`) handles reference loops. SDE analogy: like `shared_ptr` in C++ plus a backup collector, rather than a JVM-style tracing GC only.
- **"float32 vs float16 vs bfloat16?"** 4 vs 2 vs 2 bytes per value. float16 has more precision but a tiny range (max 65504); bfloat16 keeps float32's range with less precision, so large models train without loss scaling.

## Source material
To be added.
