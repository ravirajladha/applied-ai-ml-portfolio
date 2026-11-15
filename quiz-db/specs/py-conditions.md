# Conditions & Booleans: coverage spec

**Ladder:** Foundations: Python & Data Tools › Python Core   ·   **Prerequisites:** py-basics, py-variables
**Why it matters for AI/ML:** Every data-cleaning filter, early-stopping check, config validation and LLM-response router is a condition. Python's truthiness rules differ from JS and Java in ways that bite (`0` and `""` vs `None`, `x or default`), NumPy arrays refuse to be used in `if`, and `match/case` is now the clean way to dispatch on parsed JSON and tool-call payloads.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `comparisons` | Comparison operators and chaining | `==`, `!=`, `<`, `>=` give True/False | chaining `1 < x < 5`, comparing strings | `int` vs `str` ordering TypeError, `0.1 + 0.2 == 0.3`, sequence comparison | chaining with `==`/`in` (`False == False in [False]`), each operand evaluated once |
| 2 | `truthiness` | Truthy and falsy values | `0`, `""`, `[]`, `None` are falsy | `"0"`, `"False"`, `[0]` are truthy, `if items:` idiom | NumPy array in `if` raises ValueError, `x or default` swallows 0 | `__bool__` / `__len__` protocol |
| 3 | `logic-ops` | and / or / not, short-circuit | truth tables | `and`/`or` return an operand, not a bool | short-circuit skips function calls, `x and x.attr` guard | chains like `[] or {} or 0`, `or` vs `??` |
| 4 | `identity` | `is` vs `==`, None checks | `x is None` | `[] == []` vs `[] is []` | why `is` with numbers/strings is unreliable, SyntaxWarning | custom `__eq__` makes `== None` lie, NaN and `in` identity shortcut |
| 5 | `ternary` | Conditional expressions | `a if cond else b` | ternary inside f-strings / comprehensions | ternary has the lowest precedence | nested ternaries, laziness of the unused branch |
| 6 | `match-case` | Structural pattern matching | — | literal cases, `_` wildcard, `\|` alternatives | sequence and mapping patterns, guards, capture variables | bare-name capture trap, mapping patterns match subsets, str is not a sequence pattern, class patterns |
| 7 | `precedence` | Operator precedence | — | `not` binds looser than `==` | `and` binds tighter than `or`, `x == 1 or 2` trap | `not` with `in`/`is`, comparison vs bitwise `&` (Pandas masks) |
| 8 | `any-all` | any() and all() | — | `any`/`all` with a generator | `all([])` is True, `any([])` is False | short-circuit on generators, returning bool not the item |
| 9 | `if-structure` | if / elif / else and guard clauses | `if`/`elif`/`else` order, indentation | first True branch wins, elif vs separate ifs | unreachable elif order bugs, guard clauses / early return | walrus in conditions, empty block needs `pass` |
| 10 | `type-checks` | isinstance and type checks | `isinstance(x, int)` | tuple of types, convert after `isdigit()` | `isinstance(True, int)` is True, isinstance vs `type() ==`, `list \| tuple` unions | `np.int64` is not an `int`, `collections.abc.Mapping`, rejecting bools in validators |
| 11 | `ml-patterns` | Conditions in ML code: thresholds, masks, early stopping | save-best-checkpoint check | accuracy from summed comparisons | early stopping with patience and `min_delta`, `np.where` thresholds, tensor in `if` -> RuntimeError, `df.empty`, `in` vs truthiness for config keys | NaN is truthy and fails every comparison, `if a == b` on arrays, `np.array_equal` |

## Must-know facts
- Comparisons return `True` or `False`; `=` assigns, `==` compares.
- `a < b < c` means `a < b and b < c`, with `b` evaluated once.
- Falsy values: `False`, `None`, `0`, `0.0`, `""`, `[]`, `{}`, `set()`, `()`, `range(0)`. Almost everything else is truthy, including `"0"`, `"False"` and `[0]`.
- `and` returns the first falsy operand or the last operand; `or` returns the first truthy operand or the last operand.
- `and`/`or` short-circuit: the right side isn't evaluated if the left decides the result.
- Precedence, high to low: comparisons, `not`, `and`, `or`, then the conditional expression `a if c else b`.
- Use `is` only for singletons (`None`, `True`, `False`, sentinels); use `==` for values.
- `x is None` is the correct None check; `== None` can be overridden by `__eq__`.
- `0.1 + 0.2 == 0.3` is False; use `math.isclose`.
- Python 3 refuses to order unrelated types (`3 < "4"` raises TypeError), but `==` between them just gives False.
- `all([])` is True and `any([])` is False.
- `if np_array:` raises ValueError for arrays with more than one element; use `.any()` / `.all()`.
- `match` checks cases top to bottom, runs only the first match, and never falls through.
- A bare name in a `case` is a capture pattern that matches anything; constants must be dotted (`Color.RED`) or literals.
- Mapping patterns match if the listed keys are present (extra keys are fine); sequence patterns never match `str`.
- `isinstance` accepts subclasses (and `bool` is a subclass of `int`); `type(x) == T` is an exact match.
- In Python `&`/`|` bind tighter than comparisons (the opposite of C/JS), so mask conditions need brackets.
- NaN is truthy and never compares True with `<`, `>` or `==`; test it with `math.isnan`.

## Common traps (each one must have at least one question)
- `if x == 1 or 2:` -> always true, because `2` is truthy on its own.
- `count = user_count or 10` -> a real count of 0 becomes 10.
- `bool("False")` -> True; any non-empty string is truthy.
- `x is 1000` / `s is "abc"` -> unreliable; use `==`.
- `not x == y` -> means `not (x == y)`, not `(not x) == y`.
- `if arr:` on a NumPy array -> ValueError: truth value is ambiguous.
- `case RED:` with a bare name -> captures everything (SyntaxError if it isn't the last case).
- `print("big" if x > 5 else "small" + "!")` -> the `+` only applies to the else branch.
- `all([])` -> True (vacuous truth), which can silently pass validation of an empty list.
- `0.1 + 0.2 == 0.3` -> False.
- `elif` order: `if score >= 50: ... elif score >= 90:` -> the second branch can never run.
- `True + True` -> 2; bool is a subclass of int.
- `df[(a > 1) and (b < 2)]` in Pandas -> ValueError; use `&` with brackets.
- `df[df.a > 1 & df.b < 2]` without brackets -> `&` binds first, ValueError.
- `bucket = bucket or []` -> a caller's empty list is replaced, so their list never changes.
- `if loss > 10: stop()` -> never fires for NaN; NaN is truthy and every comparison with it is False.
- `isinstance(True, int)` -> True; validators accept booleans as ints.
- `isinstance(np.int64(5), int)` -> False.
- `if tensor > 1:` on a multi-element PyTorch tensor -> RuntimeError.
- `"10" < "9"` -> True; strings compare character by character.
- `x > 3 == True` -> a chained comparison, `(x > 3) and (3 == True)`.
- `[n for n in xs if c else 0]` -> SyntaxError; a mapping conditional goes before `for`.

## Interview angle
- **"What does `a or b` return?"** Not necessarily a bool: it returns `a` if `a` is truthy, else `b`. That's why `name or "anonymous"` works as a default, and why it's wrong when `0` or `""` is a valid value. Similar to JS `||`; Python has no `??`, so for "only if None" write `b if a is None else a`.
- **"`is` vs `==`?"** `==` asks "same value?" (calls `__eq__`); `is` asks "same object?" (compares identity). Use `is` for `None` and sentinels only. SDE analogy: `equals()` vs `==` on references in Java.
- **"What's falsy in Python?"** Zero numbers, empty containers and strings, `None` and `False`. Objects can define `__bool__` or `__len__`.
- **"When would you use match/case over if/elif?"** When you're dispatching on the shape of data (parsed JSON, AST nodes, commands, tool-call payloads): it destructures and checks shape in one step. For simple value comparisons if/elif is fine.
- **"What's a guard clause and why use it?"** Handle the invalid or edge cases first and return early, so the main logic isn't nested five levels deep. Same advice as in any codebase review.

## Source material
To be added
