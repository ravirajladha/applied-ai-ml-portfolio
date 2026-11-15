# Strings: coverage spec

**Ladder:** Python core › Basics   ·   **Prerequisites:** py-basics, py-variables
**Why it matters for AI/ML:** NLP, prompt building for LLMs, log parsing, file paths and CSV/JSON cleaning are all string work. Encoding bugs (mojibake, UnicodeDecodeError) and slow string building in loops show up the moment you process a real dataset.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `indexing` | Indexing and slicing | `s[i]`, `s[-i]`, `s[a:]` | `[::-1]`, out-of-range slice vs index | negative steps, step slices, empty slices | — |
| 2 | `immutability` | Immutability | methods return new strings | method result must be reassigned, rebuild with slices | why immutability (hashing, safe sharing) | `replace` returning the same object |
| 3 | `methods` | Common string methods | upper/title/strip/replace/count | find vs index, startswith/endswith, lstrip | `strip(chars)` is a character set, `removeprefix` | — |
| 4 | `operators` | Operators and comparison | `+`, `*`, `in` | lexicographic order, uppercase before lowercase, `"10" < "9"` | `is` vs `==` for strings | — |
| 5 | `fstrings` | f-strings and format specs | `{expr}`, `:.2f` | alignment, `,`, `%`, `{x=}` | zero padding, bases, fill chars, `{{ }}`, `str.format` | banker's rounding in `.0f` |
| 6 | `escapes` | Quotes, escapes, raw strings | quote styles, `\n` | `len("a\nb")`, raw strings, `\'` | `len(r"\n")` | raw string can't end in `\`, invalid escapes like `"\d"` |
| 7 | `unicode` | Unicode, encoding, bytes | str is Unicode text | `ord`, `chr` | UTF-8 byte length, bytes indexing, UnicodeEncodeError | combining characters, mojibake, `ß` case rules, PEP 393 storage, O(1) indexing |
| 8 | `split-join` | split and join | `sep.join(list)` | `split()` vs `split(" ")`, empty fields, join needs strings | maxsplit, partition, splitlines | — |
| 9 | `performance` | Performance of building strings | — | — | `+=` in a loop vs `join` | CPython's in-place `+=` trick, memory per character |
| 10 | `interning` | String interning | — | — | don't compare with `is` | interned literals vs runtime strings, `sys.intern`, why interning exists |

## Must-know facts
- A `str` is an immutable sequence of Unicode code points; `len` counts code points, not bytes or visible characters.
- Indexing out of range raises IndexError; slicing out of range just clips.
- `s[::-1]` reverses; `s[start:stop:step]` excludes `stop`.
- Every method (`upper`, `replace`, `strip`...) returns a new string; the original never changes.
- `find` returns -1 when missing, `index` raises ValueError.
- `strip("abc")` removes any of those characters from the ends, not the substring "abc"; use `removeprefix`/`removesuffix` for substrings.
- `split()` with no argument splits on runs of whitespace and drops empty strings; `split(" ")` keeps empty strings.
- `sep.join(iterable)` needs every item to be a `str`.
- Comparison is lexicographic by code point: `"Z" < "a"`, `"10" < "9"`.
- f-string format spec: `{value:[fill][align][width][,][.precision][type]}`; `{x=}` prints `x=<value>`; `{{` gives a literal brace.
- `r"..."` turns off escape processing; a raw string still cannot end in an odd number of backslashes.
- `str.encode()` -> `bytes`; `bytes.decode()` -> `str`. UTF-8 uses 1-4 bytes per character. Indexing `bytes` gives an int.
- Building a string with `+=` in a loop can be quadratic; `"".join(parts)` is linear.
- CPython interns some strings (identifier-like literals, `sys.intern`); `is` on strings is an implementation detail. Always use `==`.

## Common traps (each one must have at least one question)
- `s.upper()` without assignment -> `s` is unchanged.
- `s[0] = "X"` -> TypeError; build a new string.
- `s[10]` on a short string -> IndexError, but `s[1:10]` is fine.
- `"".join([1, 2, 3])` -> TypeError; convert with `map(str, ...)`.
- `"a  b".split(" ")` -> contains an empty string.
- `"Hello".strip("Ho")` -> strips characters, giving `"ell"`.
- `"10" < "9"` -> True (string, not numeric, comparison).
- `find` returning -1 used as an index -> silently picks the last character.
- `len("café".encode())` -> 5, not 4.
- Decoding UTF-8 bytes as latin-1 -> mojibake like `hÃ©llo`.
- Windows paths like `"C:\new"` -> `\n` becomes a newline; use a raw string or forward slashes.
- `r"C:\folder\"` -> SyntaxError.
- `"\d"` in a regex without `r` -> SyntaxWarning (works by luck today).
- Comparing strings with `is` -> works for some literals, fails for runtime-built strings.
- `f"{2.5:.0f}"` -> `2` (round half to even).

## Interview angle
- **"Why are Python strings immutable?"** So they can be hashed (dict keys, set members), safely shared between names and threads, and interned. Same as Java's `String`.
- **"How would you build a large string efficiently?"** Collect pieces in a list and `"".join(parts)` once; repeated `+=` copies the string each time (O(n²)), like using `String +` instead of `StringBuilder` in Java.
- **"str vs bytes?"** `str` is text (Unicode code points), `bytes` is raw data. Encode at the boundary when writing (`s.encode("utf-8")`), decode when reading. Most encoding bugs come from guessing the wrong encoding.
- **"Why is `len("👨‍👩‍👧")` 5?"** `len` counts code points; that emoji is three people joined by two zero-width joiners. User-visible characters (grapheme clusters) need a library.
- **"`is` vs `==` for strings?"** `==` compares content. `is` compares identity and only "works" because CPython interns some strings; runtime-built strings usually aren't interned.

## Source material
To be added.
