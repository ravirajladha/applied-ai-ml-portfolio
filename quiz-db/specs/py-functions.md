# Functions: coverage spec

**Ladder:** Foundations: Python & Data Tools › Python Core   ·   **Prerequisites:** py-variables, py-lists, py-dicts, py-loops
**Why it matters for AI/ML:** Every ML codebase is functions passed to other functions: `key=` in sorted, `transform=` in a dataset, a loss function handed to a trainer, `@torch.no_grad()` and `@lru_cache` decorators. Scope and closure bugs (and the mutable default trap) are among the most common Python interview questions.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `def-return` | def and return | def syntax, calling, return vs print, None | returning several values (a tuple), early return | functions are objects with attributes | — |
| 2 | `arguments` | Positional, keyword and default arguments | positional vs keyword call, defaults | mixing positional and keyword, order rules | defaults evaluated once at def time | — |
| 3 | `args-kwargs` | *args and **kwargs | *args collects extras | **kwargs as a dict, unpacking at the call site | forwarding *args/**kwargs, duplicate-keyword TypeError | — |
| 4 | `param-kinds` | Keyword-only and positional-only parameters | — | bare * makes keyword-only params | / makes positional-only params | positional-only names can reappear in **kwargs; full signature order |
| 5 | `mutable-default` | The mutable default argument trap | — | `def f(x=[])` shares one list | the `None` sentinel fix, `__defaults__` | when a shared default is used on purpose (memo) |
| 6 | `scope` | Scope: LEGB, global, nonlocal | local vs global names | reading a global, `global` keyword | UnboundLocalError, `+=` on a global | nonlocal rules, compile-time scope decisions |
| 7 | `closures` | Closures and late binding | — | inner function remembers outer variables | late binding of loop variables, `i=i` fix | `__closure__` cells, mutation vs rebinding in a closure |
| 8 | `first-class` | First-class functions, lambda, higher-order | lambda basics, passing a function | map, filter, sorted(key=), max(key=) | map/filter are lazy iterators, filter(None, ...) | lambda restrictions, key functions and stable sorting |
| 9 | `decorators` | Decorators | — | `@deco` means `f = deco(f)` | decorators with arguments, wrapper needs *args/**kwargs | stacking order, runs at definition time |
| 10 | `functools` | functools: partial, lru_cache, wraps, reduce | — | partial, reduce | lru_cache speedups, cache_info, wraps preserves `__name__` | lru_cache needs hashable args, method-cache memory leak, `__wrapped__` |
| 11 | `hints-docs` | Type hints and docstrings | what a docstring is | type hint syntax, `int \| None` | hints are not enforced at runtime, `__annotations__` | `from __future__ import annotations` stores hints as strings |
| 12 | `recursion` | Recursion | a function calling itself, base case | tracing a small recursion | RecursionError, default limit ~1000, exponential naive fib, recursive flatten | no tail-call optimisation, memoised recursion still hits the depth limit, raising the limit can crash |
| 13 | `passing` | Argument passing: object references | the function gets the same object, not a copy | mutating a passed list is visible; rebinding the parameter isn't | call by object reference (sharing), defensive copies, a tuple holding a list | `+=` on a list vs a tuple parameter, in-place ops on NumPy arrays |
| 14 | `callbacks` | Callbacks and callable objects in ML code | pass `f`, not `f()` | callback hooks (on_epoch_end), dicts of functions chosen by config | `__call__` objects, bound methods as callbacks, `callable()` | why `model(x)` not `model.forward(x)`, lambdas can't be pickled for DataLoader workers |

## Must-know facts
- A function with no `return` (or a bare `return`) returns `None`. Printing is not returning.
- `return a, b` returns one tuple `(a, b)`.
- Positional arguments must come before keyword arguments in a call.
- Default values are evaluated **once**, when `def` runs, not on every call.
- `*args` collects extra positional args into a tuple; `**kwargs` collects extra keyword args into a dict.
- At a call site, `*seq` and `**mapping` unpack into separate arguments.
- Parameters after `*` (or after `*args`) are keyword-only; parameters before `/` are positional-only.
- Name lookup order is LEGB: Local, Enclosing, Global, Built-in.
- Assigning to a name anywhere in a function makes it local for the whole function -> `UnboundLocalError` if read first.
- `global` rebinds a module name; `nonlocal` rebinds a name in the nearest enclosing function.
- Closures capture variables, not values: lambdas made in a loop all see the loop variable's final value.
- `@deco` above `def f` is exactly `f = deco(f)`; it runs at definition (import) time.
- Stacked decorators apply bottom-up: `@a @b def f` is `f = a(b(f))`.
- `functools.wraps` copies `__name__`, `__doc__` and sets `__wrapped__` on the wrapper.
- `lru_cache` keys on the arguments, so they must be hashable; default `maxsize` is 128.
- Type hints are documentation for tools (mypy, IDEs); Python does not enforce them.
- CPython's default recursion limit is about 1000 and there is no tail-call optimisation.
- Arguments are passed by object reference: mutation is visible to the caller, rebinding the parameter is not.
- `x += ...` mutates a list or NumPy array in place but rebinds an int, str or tuple.
- A callback is the function object (`f`), not its result (`f()`); any object with `__call__` can be one.
- `lru_cache`/`cache` return the same object every time, so mutating a cached result corrupts the cache.
- Pickle stores functions by importable name, so lambdas and nested functions can't be sent to worker processes.

## Common traps (each one must have at least one question)
- A function that prints its result can be used as a value -> it returns `None`.
- `def f(items=[])` gives a fresh list each call -> one list is shared by all calls.
- Defaults are re-evaluated at each call -> evaluated once at def time.
- Reading a global then assigning it in the same function works -> `UnboundLocalError`.
- `[lambda: i for i in range(3)]` gives 0, 1, 2 -> all return 2 (late binding).
- `map()` / `filter()` return lists -> they return single-use iterators.
- Type hints raise an error on a wrong type -> they are not checked at runtime.
- A decorator without `wraps` keeps the function's name -> `__name__` becomes `wrapper`.
- Stacked decorators apply top-down -> the one closest to `def` wraps first.
- `lru_cache` works with any arguments -> list or dict arguments raise `TypeError`.
- `f(1, a=1)` where `a` is the first parameter -> `TypeError: multiple values for argument`.
- Recursion is fine for any depth -> `RecursionError` around depth 1000.
- `lambda x: return x` -> `SyntaxError`; a lambda body is a single expression.
- `tags = []` inside a function empties the caller's list -> it only rebinds the local name; use `tags.clear()`.
- Passing a tuple protects its contents -> a list inside the tuple can still be changed.
- `key=len()` -> TypeError; pass the function, `key=len`.
- A decorator that forgets `return wrapper` (or `return f(...)`) still works -> the name becomes `None`, or every call returns `None`.
- `partial(power, 3)` fixes the exponent -> it fixes the first parameter (base).
- A cached function's result is a fresh object -> it's the same object every call.
- `lru_cache` treats `f(1)`, `f(x=1)` and `f(1.0)` as one call -> they can be three separate cache entries.
- `lru_cache` with a recursive function avoids RecursionError -> the first deep call still recurses fully.
- Methods can read class-level names directly -> use `self.name`; the class body isn't an enclosing scope.
- `x = x * 2` on an array parameter changes the caller's array -> only `x *= 2` does.

## Interview angle
- **"Explain the mutable default argument bug."** Defaults are evaluated once when the function is defined, so a list default is one shared object that keeps growing. Fix: `def f(x=None): if x is None: x = []`. SDE analogy: a static field shared by every instance.
- **"What is a closure?"** An inner function that remembers variables from the enclosing function after it returns. It captures the variable, not its value, which is why lambdas in a loop all see the last value.
- **"How do decorators work?"** A decorator is a function that takes a function and returns a new one, usually a wrapper that adds behaviour before/after. `@deco` is sugar for `f = deco(f)`. Use `functools.wraps` to keep metadata. Same idea as Express middleware or Spring AOP.
- **"What are *args and **kwargs?"** Variadic positional args as a tuple and keyword args as a dict; used to forward arguments through wrappers.
- **"Is Python pass-by-value or pass-by-reference?"** Neither: call by object reference. The parameter is a new name for the same object, so mutating it is visible to the caller and rebinding it isn't. SDE analogy: passing an object reference in Java or JavaScript.
- **"What does LEGB mean?"** The order Python searches for a name: Local, Enclosing, Global, Built-in. Assigning makes a name local unless declared `global`/`nonlocal`.

## Source material
To be added
