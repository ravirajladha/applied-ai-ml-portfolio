# Strings: coverage spec

**Ladder:** Python core › Basics   ·   **Prerequisites:** py-basics, py-variables
**Why it matters for AI/ML:** NLP, prompt building for LLMs, log parsing, file paths and CSV/JSON cleaning are all string work. Encoding bugs (mojibake, UnicodeDecodeError) and slow string building in loops show up the moment you process a real dataset.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `indexing` | Indexing and slicing | `s[i]`, `s[-i]`, `s[a:]` | `[::-1]`, out-of-range slice vs index, `s[:5]` / `s[-6:]` | negative steps, step slices, empty slices, no `char` type, named `slice()` objects | bool used as an index |
| 2 | `immutability` | Immutability | methods return new strings | method result must be reassigned, rebuild with slices | why immutability (hashing, safe sharing), dict lookup by content, edit via `list(s)` + join | `replace` returning the same object, mutable `bytearray` |
| 3 | `methods` | Common string methods | upper/title/strip/replace/count, chaining | find vs index, startswith/endswith, lstrip | `strip(chars)` is a character set, `removeprefix`, `center`/`ljust`/`zfill`, non-overlapping `count`, tuple of prefixes | `replace("", x)` inserts everywhere |
| 4 | `operators` | Operators and comparison | `+`, `*`, `in` | lexicographic order, uppercase before lowercase, `"10" < "9"`, `s * 0` and `s * -1` give `''` | `is` vs `==` for strings, prefix rule (`"ab" < "abc"`), `key=str.lower` sorting, `'' in s` is always True | — |
| 5 | `fstrings` | f-strings and format specs | `{expr}`, `:.2f`, forgetting the `f` | alignment, `,`, `%`, `{x=}`, `:03d` for file names | zero padding, bases, fill chars, `{{ }}`, `str.format`, significant digits / `e` / `g`, `!r`, nested width, date format specs, `%`-formatting | banker's rounding in `.0f`, `-0.00`, `:c`, why logging uses `%s` arguments instead of f-strings |
| 6 | `escapes` | Quotes, escapes, raw strings | quote styles, `\n` | `len("a\nb")`, raw strings, `\'` | `len(r"\n")`, `\t` / `\x41` / `\u00e9`, newlines inside triple quotes | raw string can't end in `\`, invalid escapes like `"\d"`, `\N{NAME}` escapes |
| 7 | `unicode` | Unicode, encoding, bytes | str is Unicode text | `ord`, `chr` | UTF-8 byte length (1-4 bytes, emoji vs UTF-16), encode/decode round trip, bytes indexing, UnicodeEncodeError, `errors="replace"`, `str != bytes` | combining characters, mojibake, `ß` case rules, BOM / `utf-8-sig`, code-point sorting, PEP 393 storage, O(1) indexing |
| 8 | `split-join` | split and join | `sep.join(list)` | `split()` vs `split(" ")`, empty fields, join needs strings, `rsplit(".", 1)` | maxsplit, partition (also when the separator is missing), splitlines, `"".split(",")` is `['']` | splitlines' extra line boundaries (`\x0b`, `\x1c`) |
| 9 | `performance` | Performance of building strings | — | — | `+=` in a loop vs `join`, `io.StringIO` as a builder | CPython's in-place `+=` trick, memory per character, join with a generator isn't faster, slicing copies (recursive `s[1:-1]` is O(n²)) |
| 10 | `interning` | String interning | — | — | don't compare with `is` | interned literals vs runtime strings, constant-folded `"da" + "ta"`, `sys.intern`, why interning exists |
| 11 | `char-tests` | Character tests: isdigit, isalpha, isspace... | `isdigit()` | `isalpha`/`isalnum`/`isspace`, all False on `''` | validate numbers with `int()` not `isdigit()`, `islower` needs a letter, `istitle` | `isdecimal` ⊂ `isdigit` ⊂ `isnumeric`, `"²".isdigit()` but `int("²")` fails |
| 12 | `text-cleaning` | Text cleaning and prompt templates | — | collapse whitespace with `" ".join(s.split())` | `str.maketrans`/`translate`, `re.sub`/`re.findall` basics, `str.format` KeyError on JSON braces, `string.Template`, `textwrap.dedent` | NFKC normalisation, stripping accents with NFD |

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
- `isdecimal()` ⊂ `isdigit()` ⊂ `isnumeric()`; only `isdecimal()` characters are safe for `int()`, and every `is...` test is False on `''`.
- For text cleaning: `" ".join(s.split())` collapses whitespace, `str.translate` deletes or maps characters in one pass, `unicodedata.normalize("NFKC", s)` folds look-alike characters.
- `str.format` treats every `{...}` as a field; `string.Template` uses `$name`, which is safer for prompts containing JSON.

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
- `"-5".isdigit()` is False and `"²".isdigit()` is True -> validate with `int()` in a try/except.
- `"".isspace()` (and every `is...` test on `''`) -> False.
- `"aaaa".count("aa")` -> 2; matches don't overlap.
- `"".split(",")` -> `['']`, but `"".split()` -> `[]`.
- A prompt template with JSON braces passed to `.format()` -> KeyError; double the braces or use `string.Template`.
- `re.findall(r"\d+", ...)` -> returns strings, not ints.
- CSV saved by Excel with a BOM -> first header is `'\ufeffid'`; read with `encoding="utf-8-sig"`.
- `sorted(["éclair", "egg"])` -> code-point order, not dictionary order.
- `f"{-0.0001:.2f}"` -> `-0.00`.
- `logger.debug(f"...{big}")` -> formats even when DEBUG is off; pass `%s` arguments.
- Recursion on `s[1:-1]` -> O(n²) copying; pass indexes.

## Interview angle
- **"Why are Python strings immutable?"** So they can be hashed (dict keys, set members), safely shared between names and threads, and interned. Same as Java's `String`.
- **"How would you build a large string efficiently?"** Collect pieces in a list and `"".join(parts)` once; repeated `+=` copies the string each time (O(n²)), like using `String +` instead of `StringBuilder` in Java.
- **"str vs bytes?"** `str` is text (Unicode code points), `bytes` is raw data. Encode at the boundary when writing (`s.encode("utf-8")`), decode when reading. Most encoding bugs come from guessing the wrong encoding.
- **"Why is `len("👨‍👩‍👧")` 5?"** `len` counts code points; that emoji is three people joined by two zero-width joiners. User-visible characters (grapheme clusters) need a library.
- **"`is` vs `==` for strings?"** `==` compares content. `is` compares identity and only "works" because CPython interns some strings; runtime-built strings usually aren't interned.
- **"How do you clean text before feeding it to a model or an index?"** Normalise Unicode (NFC/NFKC), fix the encoding at the boundary, collapse whitespace, optionally lowercase/casefold and strip punctuation with `translate`. Do the same steps at training and inference time. SDE analogy: input sanitising in a web form, applied identically on every path.

## Source material
To be added.
