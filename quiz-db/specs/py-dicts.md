# Dictionaries: coverage spec

**Ladder:** Foundations: Python & Data Tools › Python Core   ·   **Prerequisites:** py-variables, py-strings, py-lists
**Why it matters for AI/ML:** Dicts are everywhere in ML code: config files and hyperparameters, JSON from APIs and LLM responses, vocabularies (token -> id), label maps, metric logs, and the `state_dict` of a PyTorch model. Sets are the go-to tool for de-duplication and fast "have I seen this?" checks in data cleaning.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `crud` | Create, read, update, delete | `{}` literal, `d[k]`, `d[k] = v`, `len`, `in` checks keys | `del`, `pop(k, default)`, `dict(zip(...))`, `update` | `popitem()` is LIFO, `in` never checks values | `fromkeys` with a mutable value shares it |
| 2 | `get-setdefault` | Safe lookup: get and setdefault | `get(k)` returns None, `get(k, default)` | `setdefault(k, []).append(x)` grouping | default argument is evaluated eagerly | `get` vs `setdefault` vs `defaultdict` vs `__missing__` |
| 3 | `iteration` | Iterating keys, values, items | `for k in d` gives keys | `.items()` unpacking, `.values()`, `list(d)` | views are live, `max(d, key=d.get)`, sort by value | changing size during iteration -> RuntimeError, keys views support set ops |
| 4 | `ordering` | Insertion order | dicts keep insertion order | overwriting a key keeps its position | delete + re-insert moves to the end, `==` ignores order | OrderedDict equality and `move_to_end` |
| 5 | `hashability` | What can be a key | strings and numbers as keys | tuples ok, lists raise TypeError | tuple containing a list is unhashable, `1`/`1.0`/`True` are the same key | `__eq__` without `__hash__`, mutating a key after insert, NaN keys |
| 6 | `comprehensions` | Dict comprehensions | — | `{k: v for ...}`, filtering with `if` | inverting a dict, duplicate keys -> last wins | inversion loses data on duplicate values |
| 7 | `merging` | Merging dicts | — | `d1 \| d2`, `{**d1, **d2}`, right side wins | `\|=` / `update` mutate, merge is shallow | merging nested configs needs recursion |
| 8 | `collections` | defaultdict and Counter | — | `defaultdict(list)`, `Counter(words).most_common(n)` | defaultdict inserts on read, Counter returns 0 without inserting | Counter arithmetic drops non-positive counts |
| 9 | `sets` | Sets | `set()` vs `{}`, de-duplicate with `set(list)` | `&`, `\|`, `-`, `^`, `add`, `discard` vs `remove` | `{1, 1.0, True}` has one item, frozenset, sets are unordered | set-of-strings order varies between runs (hash randomisation) |
| 10 | `complexity` | Time complexity | — | lookup/insert/delete O(1) average | set membership vs list membership | worst case O(n) with collisions, memory cost of hashing |
| 11 | `internals` | How dicts work inside | — | — | keys are found by hash, then `==` | compact dict layout, open addressing, `hash(-1) == -2`, identity check before `==` |
| 12 | `json-nested` | JSON and nested data | `json.loads` gives nested dicts, `d[a][b]` | `json.dumps` spelling (true/null), chained `.get(k, {})`, API response shapes | int keys become str, tuples become lists, sets aren't serialisable, single quotes -> JSONDecodeError, duplicate keys, validating LLM JSON | `NaN` is written as invalid JSON, `1` and `'1'` collide, autovivifying `defaultdict` trees |
| 13 | `ml-patterns` | Dicts in ML code: vocabularies, label maps, configs | label map id -> name, vocab token -> id | `id2label` inversion, `**cfg` into a function | state_dict prefix filtering, `**kw` duplicate-argument TypeError, union of metric keys, dict vs `list.index` for vocab | `module.` prefix from DataParallel, hashable cache keys from configs, `np.float32` not JSON serialisable |

## Must-know facts
- `d[k]` raises KeyError for a missing key; `d.get(k)` returns None (or a default you pass).
- `k in d` checks keys only, never values.
- Since Python 3.7 dicts keep insertion order; overwriting a key keeps its original position.
- Keys must be hashable: str, int, float, tuple of hashables, frozenset. Lists, dicts and sets are not.
- Equal keys collapse: `1`, `1.0` and `True` are the same key (equal and same hash); the first key object is kept, the last value wins.
- `d1 | d2` (3.9+) and `{**d1, **d2}` make a new dict; the right-hand side wins on conflicts. `update` and `|=` mutate.
- Merges and `.copy()` are shallow.
- `setdefault(k, v)` inserts v only if k is missing and returns the value stored.
- `defaultdict(factory)` creates and inserts a value on any `d[k]` read of a missing key; `get` and `in` do not insert.
- `Counter` returns 0 for missing keys without inserting; `most_common(n)` gives the top n.
- `{}` is an empty dict; an empty set is `set()`.
- Dict and set lookup, insert and delete are O(1) on average; list membership is O(n).
- Adding or removing keys while iterating a dict raises RuntimeError.
- `keys()`, `values()`, `items()` are live views, not copies.
- JSON object keys are always strings; tuples come back as lists; sets, NumPy float32 and custom objects aren't serialisable by default.
- `f(**cfg)` spreads a dict into keyword arguments; this is how configs reach model constructors.
- CPython dicts use a hash table with open addressing and a separate compact entries array (which is why order is preserved).

## Common traps (each one must have at least one question)
- `d["missing"]` -> KeyError; use `get` or `in` first.
- `"Ravi" in {"name": "Ravi"}` -> False, because `in` checks keys.
- `x = {}` -> that's a dict, not a set.
- `d[[1, 2]] = ...` -> TypeError: unhashable type 'list'.
- `{1: "a", True: "b"}` -> one key; `True == 1`.
- `dict.fromkeys(keys, [])` -> every key shares the same list.
- `d.get("k", expensive())` -> `expensive()` runs even when the key exists.
- `dd = defaultdict(list); if dd["x"]: ...` -> the read inserts `"x"`.
- Deleting keys inside `for k in d:` -> RuntimeError.
- `{**a, **b}` with nested dicts -> nested dicts are shared, not merged.
- Inverting `{v: k for k, v in d.items()}` when values repeat -> data silently lost.
- `s.remove(x)` on a missing item -> KeyError; `discard` doesn't raise.
- `Counter(a=3) - Counter(a=5)` -> empty Counter, not -2.
- Printing a set of strings -> order can change between runs.
- `json.loads(json.dumps({1: 'a'}))` -> `{'1': 'a'}`; int keys come back as strings.
- `json.loads("{'a': 1}")` -> JSONDecodeError; JSON needs double quotes (common in LLM output).
- `d.get('k', default)` when the key exists with value None -> returns None, not the default.
- `Counter.update` adds counts; `dict.update` replaces values.
- `json.dumps(np.float32(0.5))` -> TypeError; convert with `float()`.
- `json.dumps(float('nan'))` -> writes `NaN`, which is not valid JSON.
- `f(0.5, **{'lr': 0.1})` where lr is the first parameter -> TypeError (multiple values).

## Interview angle
- **"How does a dict lookup work and why is it O(1)?"** Python hashes the key to pick a slot in a table, then confirms with `==`. With a good hash and the table kept under about 2/3 full, a lookup touches a constant number of slots on average. Collisions are resolved by probing other slots; the worst case is O(n). SDE analogy: a Java HashMap, but with open addressing instead of buckets.
- **"Why can't a list be a dict key?"** Keys must be hashable and their hash must never change. A list is mutable, so its hash could change after insertion and the key would be lost. Use a tuple.
- **"Are dicts ordered?"** Yes, insertion order is guaranteed since 3.7 (a side effect of the compact layout that became a language guarantee). Equality still ignores order.
- **"defaultdict vs Counter vs setdefault?"** setdefault is the plain-dict one-liner; defaultdict auto-creates values for grouping; Counter is a dict specialised for counting with `most_common` and arithmetic.
- **"When would you use a set?"** De-duplication and fast membership checks, plus set algebra (intersection of vocabularies, users in A but not B).

## Source material
To be added
