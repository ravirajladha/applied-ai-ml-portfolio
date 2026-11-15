# Errors & Exceptions: coverage spec

**Ladder:** Python core › Errors & Exceptions   ·   **Prerequisites:** py-basics, py-functions (calling functions, return values)
**Why it matters for AI/ML:** Training scripts crash hours in, data loaders hit bad rows, and notebooks throw long tracebacks from deep inside PyTorch or pandas. Reading the traceback, catching the right error, and cleaning up resources (files, GPU memory, database handles) with `with` is daily work. Good error handling is what turns a notebook into a pipeline that can run unattended.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `tracebacks` | Reading tracebacks | read bottom-up, last line = type + message | find your own frame among library frames, line numbers | traceback module, `format_exc`, chained tracebacks ("During handling...") | — |
| 2 | `builtin-errors` | Common built-in exceptions | ValueError vs TypeError, KeyError, IndexError, NameError, ZeroDivisionError | AttributeError, FileNotFoundError, StopIteration, which line raises what | ImportError vs ModuleNotFoundError, RecursionError, UnboundLocalError, LookupError family | OSError subclasses / errno, KeyError repr quirk |
| 3 | `try-except` | try / except / else / finally | basic try/except, catching one named error | `else` and `finally` order, multiple except clauses, tuple of types, `as e` | first matching clause wins, `e` is deleted after except, return inside try with finally | `finally` overriding return / swallowing exceptions, `break`/`continue` in finally |
| 4 | `catching` | Catching well: specific vs bare, hierarchy | why bare `except:` is risky | Exception vs BaseException, KeyboardInterrupt, order of clauses (subclass first) | `except Exception` vs bare except, SystemExit/GeneratorExit, LBYL vs EAFP | designing what to catch at which layer |
| 5 | `raising` | raise, re-raise and chaining | `raise ValueError("msg")` | bare `raise` to re-raise, raising inside a function | `raise X from e`, `__cause__`, `__context__`, `from None` | `__suppress_context__`, `raise e` vs `raise`, `add_note` |
| 6 | `custom-exceptions` | Custom exception classes | `class MyError(Exception): pass` | subclass hierarchy for a library, catching the base | storing extra fields, `str(e)`, `e.args` | why inherit from Exception not BaseException, pickling / args pitfalls |
| 7 | `context-managers` | `with` and context managers | `with open(...)` closes the file | `__enter__` / `__exit__` protocol, what `as` binds | `__exit__` returning True suppresses, `contextlib.contextmanager`, `suppress` | generator-based CM cleanup with try/finally, `ExitStack` |
| 8 | `assert-warnings` | assert and warnings | what `assert` does | AssertionError message, assert is not validation | `python -O` strips asserts, `warnings.warn`, categories | warnings filters, turning warnings into errors |
| 9 | `debugging` | Debugging: print, logging, pdb | print vs breakpoint idea | `logging` levels, `logger.exception` | `pdb` commands (n, s, c, p, q), post-mortem `%debug` | logger hierarchy / propagation, lazy `%s` formatting |
| 10 | `exception-groups` | ExceptionGroup and except* | — | — | what an ExceptionGroup is (many errors at once) | `except*` matching, splitting groups, asyncio TaskGroup |
| 11 | `ml-patterns` | Error handling in real ML code | skip bad rows per item, log what was skipped | retry loops for flaky I/O, NaN loss never raises | PyTorch RuntimeError for shapes, `torch.cuda.OutOfMemoryError`, DataLoader worker tracebacks, checkpoint on Ctrl+C, silent-skip data loss | what to retry vs fail fast, stored exceptions pinning GPU memory via `__traceback__`, adding sample context with `add_note` / `from e` |

## Must-know facts
- Read a traceback from the bottom: last line is `ErrorType: message`; the frame just above it is where it was raised.
- `int("abc")` is ValueError (right type, bad value); `"a" + 1` is TypeError (wrong type).
- `d["missing"]` is KeyError, `lst[99]` is IndexError, an unknown name is NameError, `obj.missing` is AttributeError.
- Order: `try` -> (`except` if it raised | `else` if it didn't) -> `finally` always.
- Only the first matching `except` clause runs; put subclasses before base classes.
- `except (A, B) as e:` catches either; the name `e` is deleted when the block ends.
- Bare `except:` also catches KeyboardInterrupt and SystemExit; prefer `except Exception:` or something narrower.
- `KeyboardInterrupt`, `SystemExit`, `GeneratorExit` inherit from BaseException, not Exception.
- A bare `raise` inside `except` re-raises the current exception with its original traceback.
- `raise New from old` sets `__cause__`; raising inside an except sets `__context__` automatically; `from None` hides the context.
- Custom exceptions subclass `Exception` (or a more specific built-in).
- `with` calls `__enter__` on entry and `__exit__` on exit, even when an exception happens; `__exit__` returning a truthy value swallows the exception.
- `assert` is removed under `python -O`; never use it to validate user input.
- A `return` in `finally` overrides the try's return and silently discards an in-flight exception.
- `logging` has levels (DEBUG < INFO < WARNING < ERROR < CRITICAL); the default level is WARNING.
- `breakpoint()` drops into pdb at that line.
- `except*` handles parts of an ExceptionGroup; each matching clause can run.
- The expression after `except` is evaluated only when an exception arrives, so a typo there (or a list instead of a tuple) fails late.
- If `__enter__` raises, `__exit__` never runs; an error raised in `finally` replaces the in-flight one (the original becomes `__context__`).
- PyTorch reports shape mismatches as RuntimeError; `torch.cuda.OutOfMemoryError` is a RuntimeError subclass.
- NaN and inf are valid floats: a NaN loss never raises on its own.

## Common traps (each one must have at least one question)
- Thinking the first traceback line is the error -> the last line is.
- `int("3.5")` -> ValueError, not 3.
- Catching `Exception` before `ValueError` -> the ValueError clause is unreachable.
- Bare `except:` swallowing Ctrl+C -> the loop cannot be interrupted.
- Using `e` after the except block -> NameError, Python deleted it.
- Expecting `else` to run when an exception was caught -> it only runs when try finished cleanly.
- `raise e` vs bare `raise` -> both re-raise, but `raise e` adds the current line to the traceback.
- Inheriting custom errors from BaseException -> `except Exception` will not catch them.
- `__exit__` accidentally returning True -> exceptions vanish silently.
- `@contextmanager` without try/finally around `yield` -> cleanup skipped when the body raises.
- `assert (x > 0, "msg")` -> a non-empty tuple is always truthy, never fails.
- Relying on assert for input checks -> disappears under `-O`.
- `return` in `finally` -> swallows the exception and overrides the return value.
- `logging.debug` printing nothing -> default level is WARNING.
- `dict.get` vs `[]` -> `.get` returns None instead of raising KeyError.
- UnboundLocalError when assigning to a global name inside a function.
- `except Exception: continue` over every row -> silent data loss; count skips and fail past a threshold.
- Saving a checkpoint with `except Exception` on Ctrl+C -> never runs; catch KeyboardInterrupt, save, re-raise.
- Storing caught exceptions in a list -> their tracebacks keep frames and GPU tensors alive.
- Retrying every error -> bad requests and auth failures retried forever; retry only transient errors.
- `raise StopIteration` inside a generator -> RuntimeError (PEP 479).
- `@contextmanager` that doesn't yield on some path -> RuntimeError: generator didn't yield.
- Plain `except ValueError` around code that raises an ExceptionGroup -> no match; use except*.

## Interview angle
1. **"try/except/else/finally: when does each run?"** try always; except only on a matching error; else only if try raised nothing; finally always, even on return. Use else for code that should only run on success, so its own errors are not caught by the except. SDE analogy: Java try/catch/finally plus a "success" hook.
2. **"Why is bare except bad?"** It catches everything including KeyboardInterrupt and SystemExit, so it hides bugs and blocks shutdown. Catch the narrowest exception you can handle; log and re-raise the rest.
3. **"What is exception chaining?"** When you raise inside an except, Python keeps the original as `__context__`. `raise X from e` makes it explicit (`__cause__`) and the traceback says "The above exception was the direct cause". Use it to wrap low-level errors in domain errors without losing the root cause.
4. **"What's a context manager and why use it?"** An object with `__enter__`/`__exit__` that guarantees cleanup (files, locks, DB sessions, `torch.no_grad()`). It is try/finally packaged as reusable code, like Java try-with-resources or C# `using`.
5. **"assert vs raise?"** assert documents internal invariants and can be turned off with -O; raise is for errors that must always be checked (bad input, missing files).

## Source material
To be added
