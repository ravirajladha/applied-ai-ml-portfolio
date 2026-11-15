# Variables & Types: coverage spec

**Ladder:** Python core › Basics   ·   **Prerequisites:** py-basics
**Why it matters for AI/ML:** every tensor, DataFrame and model is reached through a name. Aliasing (two names, one object) is behind many "my data changed by itself" bugs, and float precision explains why losses and metrics never compare exactly equal.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `binding` | Names and binding | `=` binds a name, rebinding doesn't affect copies of the old value | aliasing a list | `del` removes a name, not the object; call-by-sharing | — |
| 2 | `core-types` | int, float, str, bool, None | `type()` of each literal | int + float -> float, bool is an int | `None` comparisons | `1`, `True`, `1.0` as the same dict key |
| 3 | `conversion` | Type conversion | `int()`, `float()`, `str()` | `int("3.5")` fails, `bool("False")`, whitespace | bases, `int()` truncates toward zero, underscores | — |
| 4 | `dynamic-typing` | Dynamic vs strong typing | no type declarations, rebinding to another type | `"1" + 1` TypeError, `isinstance` | type hints are not enforced | — |
| 5 | `identity` | Mutability and identity: `is`, `==`, `id` | `==` compares values | `is` vs `==`, `is None`, mutable vs immutable | `+=` vs `+` on lists, tuple holding a list, `id` reuse | NaN and container equality |
| 6 | `caching` | Small-int caching | — | — | `-5..256` cache, `int("257") is int("257")` | constants shared within one compiled unit |
| 7 | `floats` | Float precision | `0.1 + 0.2` | `round` before comparing | `math.isclose`, `1e16 + 1`, NaN, `round(2.675, 2)` | non-associativity, int vs float exact compare, `Decimal(0.1)` |
| 8 | `unpacking` | Multiple assignment and unpacking | `a, b = 1, 2`, `x = y = 0` | swap, starred `*rest`, count mismatch | — | left-to-right target assignment |
| 9 | `naming` | Naming rules and conventions | valid names, case-sensitivity, snake_case | keywords vs shadowing built-ins | leading underscore convention | — |
| 10 | `scope` | Scope basics | local variables stay inside the function | assignment inside a function creates a local | UnboundLocalError, `global`, `nonlocal`, lookup at call time | nested `nonlocal` |

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

## Interview angle
- **"Is Python pass-by-value or pass-by-reference?"** Neither: call by sharing (object reference passed by value). The function gets a new name for the same object: mutating it is visible to the caller, rebinding the parameter is not. Same as Java object references or JS objects.
- **"`is` vs `==`?"** `==` compares values, `is` compares identity. Use `is` only for singletons (`None`, `True`, `False`, sentinels). Small-int caching makes `is` look like it works for small numbers, which is a trap.
- **"Why is `0.1 + 0.2 != 0.3`?"** Binary floating point can't represent 0.1 exactly; the tiny errors add up. Compare with a tolerance (`math.isclose`, `np.allclose`), or use `Decimal` for money.
- **"Dynamically vs strongly typed?"** Types are checked at runtime and attached to values, not names (dynamic), but Python won't silently coerce `"1" + 1` (strong). JS is dynamic and weak.
- **"What's an UnboundLocalError?"** Python decides at compile time that a name assigned in a function is local; reading it before the assignment fails. Fix with `global`/`nonlocal` or a parameter.

## Source material
To be added.
