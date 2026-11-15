from helpers import mcq, tf, out, fill

SUBJECT = "pd-cleaning"

TOPICS = [
    ("missing", "Missing values"),
    ("duplicates", "Duplicates and value_counts"),
    ("types", "Type conversion"),
    ("strings", "String methods (.str)"),
    ("groupby", "groupby and aggregation"),
    ("groupby-advanced", "transform vs agg vs apply, size vs count"),
    ("merge", "merge and join"),
    ("concat", "concat"),
    ("reshape", "pivot, pivot_table and melt"),
    ("binning", "Binning with cut and qcut"),
    ("datetime", "Dates, times and resampling"),
    ("ml-prep", "Preparing data for ML and performance"),
    ("windows", "Rolling, expanding and ewm windows"),
    ("ml-features", "Leak-free feature engineering (lags, windows, target encoding)"),
]

QUESTIONS = [
    # ------------------------------------------------------------------ missing
    mcq("What does NaN stand for in pandas?",
        ["Not a Number: the marker pandas uses for a missing numeric value",
         "Null and Nothing: an empty string",
         "A zero that has not been calculated yet",
         "A row that has been deleted"], 0,
        "It's a special float value.",
        "NaN (Not a Number) is a special floating-point value that pandas uses to mark missing data. It is not 0 and not an empty string.",
        analogy="Like NULL in a SQL table: 'we don't know this value'.",
        topic="missing", level=1),
    out("""import pandas as pd
import numpy as np
df = pd.DataFrame({"a": [1, np.nan, 3], "b": [None, "x", "y"]})
print(df.isna().sum().tolist())""",
        ["[1, 1]", "[0, 0]", "[1, 0]", "[2]"], 0,
        "isna() marks each missing cell True; sum() counts the Trues per column.",
        "Column a has one NaN, column b has one None; isna() treats both as missing, so each column counts 1.",
        topic="missing", level=1),
    out("""import pandas as pd
import numpy as np
df = pd.DataFrame({"a": [1, np.nan, 3], "b": [4, 5, np.nan]})
print(df.dropna().shape)""",
        ["(1, 2)", "(3, 2)", "(2, 2)", "(0, 2)"], 0,
        "dropna() removes a row if ANY of its values is missing.",
        "Row 1 has NaN in a, row 2 has NaN in b. Only row 0 is complete, so 1 row is left.",
        diagram="""
     a     b     any NaN?   dropna()
0    1     4     no         kept
1   NaN    5     yes        dropped
2    3    NaN    yes        dropped""",
        topic="missing", level=1),
    out("""import pandas as pd
import numpy as np
s = pd.Series([1, np.nan, 3])
print(s.fillna(0).tolist())""",
        ["[1.0, 0.0, 3.0]", "[1, 0, 3]", "[1.0, nan, 3.0]", "[1.0, 3.0]"], 0,
        "fillna replaces missing values; the dtype stays float.",
        "fillna(0) puts 0 where NaN was. The Series was float64 because of the NaN, and it stays float64 after filling.",
        topic="missing", level=1),
    out("""import numpy as np
print(np.nan == np.nan, None == None)""",
        ["False True", "True True", "False False", "True False"], 0,
        "NaN is defined as not equal to anything, even itself.",
        "By the IEEE float rules NaN != NaN, so == can never find missing values. None == None is True in Python. Always use isna() to test for missing.",
        topic="missing", level=1),
    tf("`df[df['a'] == np.nan]` returns the rows where column a is missing.", False,
        "What is NaN == NaN?",
        "Every comparison with NaN is False, so the mask is all False and you get an empty frame. Use df[df['a'].isna()].",
        topic="missing", level=2),
    out("""import pandas as pd
import numpy as np
df = pd.DataFrame({"a": [1, np.nan, np.nan], "b": [4, 5, np.nan]})
print(df.dropna(how="all").shape, df.dropna(subset=["b"]).shape, df.dropna(thresh=1).shape)""",
        ["(2, 2) (2, 2) (2, 2)", "(1, 2) (2, 2) (2, 2)", "(2, 2) (1, 2) (3, 2)", "(3, 2) (2, 2) (1, 2)"], 0,
        "how='all' needs every value missing; subset limits which columns are checked; thresh = minimum non-missing values to keep.",
        "Only row 2 is all-NaN, so how='all' keeps 2 rows. subset=['b'] drops row 2 only. thresh=1 keeps rows with at least 1 value: rows 0 and 1.",
        topic="missing", level=2),
    out("""import pandas as pd
import numpy as np
s = pd.Series([1, np.nan, np.nan, 4])
print(s.ffill().tolist(), s.bfill().tolist())""",
        ["[1.0, 1.0, 1.0, 4.0] [1.0, 4.0, 4.0, 4.0]", "[1.0, 4.0, 4.0, 4.0] [1.0, 1.0, 1.0, 4.0]", "[1.0, 1.0, nan, 4.0] [1.0, nan, 4.0, 4.0]", "[1.0, 2.5, 2.5, 4.0] [1.0, 2.5, 2.5, 4.0]"], 0,
        "ffill carries the last seen value forward; bfill pulls the next value backward.",
        "ffill copies 1 down into the gaps; bfill copies 4 up. Both are typical for time series (e.g. last known price).",
        diagram="""
value   ffill   bfill
  1       1       1
 NaN      1 v     4 ^
 NaN      1 v     4 ^
  4       4       4""",
        topic="missing", level=2),
    out("""import pandas as pd
import numpy as np
s = pd.Series([1, np.nan, 3])
print(s.sum(), s.mean(), s.sum(skipna=False))""",
        ["4.0 2.0 nan", "nan nan nan", "4.0 1.3333333333333333 nan", "4.0 2.0 4.0"], 0,
        "Aggregations skip NaN unless you tell them not to.",
        "skipna=True is the default: sum is 1+3 and mean divides by the 2 present values. With skipna=False a single NaN poisons the result.",
        topic="missing", level=2),
    out("""import pandas as pd
import numpy as np
print(pd.Series([np.nan, np.nan]).sum(), pd.Series([np.nan, np.nan]).mean())""",
        ["0.0 nan", "nan nan", "0.0 0.0", "nan 0.0"], 0,
        "The sum of nothing is the 'empty' value for addition.",
        "With all values skipped, sum returns 0.0 (sum of an empty set), but mean returns NaN (0/0). Use sum(min_count=1) to get NaN for an all-missing group.",
        topic="missing", level=3),
    out("""import pandas as pd
import numpy as np
df = pd.DataFrame({"a": [1, np.nan], "b": [np.nan, 2]})
print(df.fillna({"a": 0, "b": -1}).values.tolist())""",
        ["[[1.0, -1.0], [0.0, 2.0]]", "[[1.0, 0.0], [-1.0, 2.0]]", "[[1, -1], [0, 2]]", "TypeError"], 0,
        "A dict lets you give each column its own fill value.",
        "fillna({'a': 0, 'b': -1}) fills a's NaN with 0 and b's NaN with -1.",
        topic="missing", level=2),
    out("""import pandas as pd
s = pd.Series(["x", None, "y"])
print(s.dtype, s.isna().tolist(), s.fillna("missing").tolist())""",
        ["object [False, True, False] ['x', 'missing', 'y']", "object [False, False, False] ['x', None, 'y']", "string [False, True, False] ['x', 'missing', 'y']", "float64 [False, True, False] ['x', 'missing', 'y']"], 0,
        "None in a text column stays None, but isna() still recognises it.",
        "In an object column None is kept as None, and pandas treats both None and NaN as missing for isna/fillna/dropna.",
        topic="missing", level=2),
    out("""import pandas as pd
import numpy as np
s = pd.Series([1.0, np.nan, 3.0])
print(s.interpolate().tolist())""",
        ["[1.0, 2.0, 3.0]", "[1.0, 1.0, 3.0]", "[1.0, 3.0, 3.0]", "[1.0, nan, 3.0]"], 0,
        "interpolate draws a straight line between the neighbours.",
        "Linear interpolation fills the gap with the midpoint of 1 and 3, which is 2.",
        topic="missing", level=3),
    out("""import pandas as pd
s = pd.Series(["", " ", "n/a", "ok"])
print(s.isna().sum(), s.replace({"": None, " ": None, "n/a": None}).isna().sum())""",
        ["0 3", "3 3", "1 3", "0 0"], 0,
        "To pandas, an empty string is a perfectly valid value.",
        "'', ' ' and 'n/a' are strings, not missing. Real data often hides missing values like this; replace them (or use na_values= in read_csv) before counting NaN.",
        topic="missing", level=3),
    mcq("A sensor column has 40% missing values. Which first step is most sensible before training a model?",
        ["Check WHY values are missing (and add a 'was_missing' flag if missingness may carry information) before choosing to drop or impute",
         "Always drop every row with a missing value",
         "Always replace missing values with 0",
         "Ignore it: models handle NaN automatically"], 0,
        "Missingness itself can be a signal.",
        "Dropping 40% of rows loses data and may bias it; filling with 0 invents values. Understand the cause, consider a missing-indicator column, and impute using training-set statistics only. Many scikit-learn models reject NaN.",
        topic="missing", level=3),
    out("""import pandas as pd
import numpy as np
s = pd.Series([1, np.nan, 3], dtype="float64")
print(s.isna().sum(), (s.astype("Int64")).isna().sum(), s.astype("Int64").dtype)""",
        ["1 1 Int64", "1 0 Int64", "1 1 int64", "IntCastingNaNError"], 0,
        "The nullable Int64 type has its own missing marker.",
        "astype('Int64') converts NaN to pd.NA and keeps it missing. astype('int64') on the same Series would raise IntCastingNaNError.",
        topic="missing", level=3),
    out("""import pandas as pd
import numpy as np
s = pd.Series([1, np.nan, 3])
print(s.astype("int64"))""",
        ["IntCastingNaNError", "ValueError", "0    1\n1    0\n2    3\ndtype: int64", "TypeError"], 0,
        "Where would the NaN go in a plain int64 array?",
        "A NumPy int64 array has no way to store NaN, so pandas raises IntCastingNaNError ('Cannot convert non-finite values (NA or inf) to integer'). Fill first, or use 'Int64'.",
        topic="missing", level=4),

    # ------------------------------------------------------------------ duplicates
    out("""import pandas as pd
df = pd.DataFrame({"id": [1, 1, 2], "v": ["a", "a", "b"]})
print(df.duplicated().tolist(), len(df.drop_duplicates()))""",
        ["[False, True, False] 2", "[True, True, False] 2", "[False, True, False] 3", "[False, False, False] 3"], 0,
        "By default the FIRST occurrence is not counted as a duplicate.",
        "duplicated() marks repeats after the first (keep='first'). drop_duplicates removes them, leaving 2 rows.",
        analogy="SQL: SELECT DISTINCT * FROM df.",
        topic="duplicates", level=1),
    out("""import pandas as pd
s = pd.Series(["cat", "dog", "cat", "cat"])
print(s.value_counts().to_dict())""",
        ["{'cat': 3, 'dog': 1}", "{'dog': 1, 'cat': 3}", "{'cat': 1, 'dog': 1}", "[3, 1]"], 0,
        "value_counts counts each distinct value, most frequent first.",
        "cat appears 3 times, dog once. The result is sorted by count, descending.",
        analogy="SQL: SELECT v, COUNT(*) FROM t GROUP BY v ORDER BY 2 DESC.",
        topic="duplicates", level=1),
    out("""import pandas as pd
s = pd.Series(["cat", "dog", "cat", "cat"])
print(s.value_counts(normalize=True).tolist(), s.nunique())""",
        ["[0.75, 0.25] 2", "[3, 1] 2", "[0.75, 0.25] 4", "[0.5, 0.5] 2"], 0,
        "normalize turns counts into fractions.",
        "normalize=True divides by the total (3/4, 1/4). nunique counts distinct values: 2. Handy for checking class balance.",
        topic="duplicates", level=2),
    out("""import pandas as pd
s = pd.Series(["a", "b", "a", None])
print(s.value_counts().sum(), s.value_counts(dropna=False).sum())""",
        ["3 4", "4 4", "3 3", "4 3"], 0,
        "value_counts hides missing values unless asked.",
        "dropna=True is the default, so None isn't counted (3). dropna=False adds a row for the missing value (4).",
        topic="duplicates", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"email": ["a@x", "b@x", "a@x"], "ts": [1, 2, 3]})
print(df.drop_duplicates(subset="email", keep="last")["ts"].tolist())""",
        ["[2, 3]", "[1, 2]", "[3]", "[1, 2, 3]"], 0,
        "subset picks which columns define 'same'; keep picks which copy survives.",
        "Rows are duplicates if email matches. keep='last' keeps the later a@x (ts 3); b@x is unique. Survivors keep their original order: ts 2, then 3.",
        topic="duplicates", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"id": [1, 1, 2]})
print(df.duplicated(keep=False).tolist())""",
        ["[True, True, False]", "[False, True, False]", "[True, False, False]", "[False, False, False]"], 0,
        "keep=False means no copy is treated as the original.",
        "keep=False marks every row that has a twin, useful for inspecting ALL conflicting records.",
        topic="duplicates", level=3),
    tf("`df.duplicated()` with no arguments compares only the first column.", False,
        "What does 'duplicate row' mean by default?",
        "With no subset, a row is a duplicate only if ALL its columns match an earlier row.",
        topic="duplicates", level=1),
    out("""import pandas as pd
s = pd.Series(["Pune", "pune ", "PUNE"])
print(s.nunique(), s.str.strip().str.lower().nunique())""",
        ["3 1", "1 1", "3 3", "2 1"], 0,
        "Exact string matching is case- and space-sensitive.",
        "The three strings differ by case and a trailing space, so they count as 3 distinct values. Normalising with strip + lower makes them one.",
        topic="duplicates", level=3),
    mcq("Why can duplicate rows between your train and test sets make a model look better than it is?",
        ["The model is tested on rows it has already memorised, so test accuracy overstates real-world accuracy",
         "Duplicates make training slower but don't affect scores",
         "Duplicates are automatically removed by scikit-learn",
         "Duplicates only matter for regression, not classification"], 0,
        "Think of exam questions you've already seen the answers to.",
        "If the same record sits in both sets, the test is no longer 'unseen data'. Deduplicate (or split by entity, e.g. user_id) before splitting.",
        topic="duplicates", level=3),

    # ------------------------------------------------------------------ types
    out("""import pandas as pd
s = pd.Series(["10", "20", "30"])
print(s.astype(int).sum())""",
        ["60", "102030", "TypeError", "'102030'"], 0,
        "Convert the text to numbers first.",
        "astype(int) turns '10', '20', '30' into integers, so sum is 60. Without it, summing strings concatenates them.",
        topic="types", level=1),
    out("""import pandas as pd
s = pd.Series(["1", "two", "3"])
print(pd.to_numeric(s, errors="coerce").tolist())""",
        ["[1.0, nan, 3.0]", "[1, 'two', 3]", "ValueError", "[1, 0, 3]"], 0,
        "errors='coerce' turns anything unparseable into missing.",
        "'two' can't be parsed, so it becomes NaN, and NaN makes the column float64.",
        topic="types", level=1),
    out("""import pandas as pd
s = pd.Series(["1", "two", "3"])
print(s.astype(int))""",
        ["ValueError", "TypeError", "0    1\n1    0\n2    3\ndtype: int64", "KeyError"], 0,
        "astype has no 'skip bad values' option.",
        "int('two') fails, so astype raises ValueError. Use pd.to_numeric(errors='coerce') when the data may be dirty.",
        topic="types", level=2),
    fill("Complete to parse dirty numbers, turning bad ones into NaN: `pd.to_numeric(s, errors=\"____\")`",
        "coerce",
        "Force them, and give up gracefully.",
        "errors='coerce' converts unparseable entries to NaN instead of raising.",
        topic="types", level=1),
    out("""import pandas as pd
s = pd.Series(["$1,200", "$350"])
print(s.str.replace("[$,]", "", regex=True).astype(int).tolist())""",
        ["[1200, 350]", "ValueError", "['1200', '350']", "[1.2, 350]"], 0,
        "Remove the characters that aren't digits first.",
        "The regex [$,] removes dollar signs and commas, leaving '1200' and '350', which astype(int) converts.",
        topic="types", level=2),
    out("""import pandas as pd
s = pd.Series(["2024-01-05", "2024-03-20"])
d = pd.to_datetime(s)
print(d.dtype, (d[1] - d[0]).days)""",
        ["datetime64[ns] 75", "object 75", "datetime64[ns] 74", "TypeError"], 0,
        "Once parsed, subtracting dates gives a Timedelta.",
        "to_datetime gives datetime64[ns]. Jan 5 -> Mar 20 in the leap year 2024: 26 (rest of Jan) + 29 (Feb) + 20 = 75 days.",
        topic="types", level=2),
    out("""import pandas as pd
s = pd.Series(["05/01/2024", "06/01/2024"])
print(pd.to_datetime(s).dt.month.tolist(), pd.to_datetime(s, dayfirst=True).dt.month.tolist())""",
        ["[5, 6] [1, 1]", "[1, 1] [5, 6]", "[5, 6] [5, 6]", "[1, 1] [1, 1]"], 0,
        "By default pandas reads 05/01 as month/day (US style).",
        "Default parsing is month-first, giving May and June. dayfirst=True reads them as 5 Jan and 6 Jan. Always pass format= or dayfirst for non-US data.",
        topic="types", level=3),
    out("""import pandas as pd
s = pd.Series(["2024-01-05", "not a date"])
print(pd.to_datetime(s, errors="coerce").isna().tolist())""",
        ["[False, True]", "[False, False]", "ValueError", "[True, True]"], 0,
        "Same errors='coerce' idea as to_numeric.",
        "Unparseable dates become NaT (Not a Time), the datetime version of NaN.",
        topic="types", level=2),
    out("""import pandas as pd
s = pd.Series(["yes", "no", "yes"])
print(s.astype(bool).tolist(), s.map({"yes": True, "no": False}).tolist())""",
        ["[True, True, True] [True, False, True]", "[True, False, True] [True, False, True]", "ValueError", "[False, False, False] [True, False, True]"], 0,
        "bool('no') in Python is...?",
        "astype(bool) uses Python truthiness: every non-empty string is True, including 'no'. Map explicitly instead.",
        topic="types", level=3),
    out("""import pandas as pd
s = pd.Series([1.9, -1.9])
print(s.astype(int).tolist(), s.round().astype(int).tolist())""",
        ["[1, -1] [2, -2]", "[2, -2] [2, -2]", "[1, -2] [2, -2]", "[1, -1] [1, -1]"], 0,
        "Casting float to int truncates toward zero.",
        "astype(int) chops off the decimals (1.9 -> 1, -1.9 -> -1). Round first if you want nearest.",
        topic="types", level=3),
    out("""import pandas as pd
s = pd.Series([1, 2, 300])
print(pd.to_numeric(s, downcast="integer").dtype)""",
        ["int16", "int8", "int64", "uint8"], 0,
        "It picks the smallest signed type that can hold every value.",
        "300 doesn't fit in int8 (max 127), so downcast picks int16. Unlike astype('int8'), downcasting never overflows.",
        topic="types", level=3),
    out("""import pandas as pd
s = pd.Series([1, 2.5, "3"])
print(s.dtype, pd.to_numeric(s).dtype)""",
        ["object float64", "float64 float64", "object object", "ValueError"], 0,
        "One string makes the whole column object.",
        "A mix of int, float and str can only be object. to_numeric parses '3' and returns float64.",
        topic="types", level=2),
    out("""import pandas as pd
s = pd.Series(["2024-01-05 10:00", "2024-01-05"])
print(pd.to_datetime(s, format="%Y-%m-%d %H:%M", errors="coerce").isna().tolist())""",
        ["[False, True]", "[False, False]", "ValueError", "[True, True]"], 0,
        "With an explicit format, a value must match it exactly.",
        "The second string has no time part, so it fails the format and is coerced to NaT. An explicit format is faster and catches inconsistent data; format='mixed' would parse both.",
        topic="types", level=4),

    # ------------------------------------------------------------------ strings
    out("""import pandas as pd
s = pd.Series([" ann ", "BOB"])
print(s.str.strip().str.title().tolist())""",
        ["['Ann', 'Bob']", "[' Ann ', 'Bob']", "['ann', 'bob']", "AttributeError"], 0,
        ".str methods work on every element, and can be chained.",
        "strip removes surrounding spaces; title capitalises each word.",
        topic="strings", level=1),
    tf("To call a string method like `.lower()` on every value of a Series, you write `s.str.lower()`.", True,
        "A Series isn't a string, so the string methods live under an accessor.",
        "The .str accessor applies the string method to each element and skips missing values. s.lower() would raise AttributeError.",
        topic="strings", level=1),
    out("""import pandas as pd
s = pd.Series(["apple pie", "banana", "apple tart"])
print(s.str.contains("apple").sum(), s.str.startswith("ban").tolist())""",
        ["2 [False, True, False]", "1 [False, True, False]", "2 [True, False, True]", "3 [False, True, False]"], 0,
        "contains gives a boolean per row; summing Trues counts them.",
        "Two strings contain 'apple'. startswith('ban') is True only for banana.",
        analogy="SQL: WHERE name LIKE '%apple%'.",
        topic="strings", level=1),
    out("""import pandas as pd
s = pd.Series(["Ann Lee", "Bob Ray"])
parts = s.str.split(" ", expand=True)
print(parts.shape, parts[1].tolist())""",
        ["(2, 2) ['Lee', 'Ray']", "(2,) ['Lee', 'Ray']", "(2, 1) ['Ann Lee', 'Bob Ray']", "KeyError"], 0,
        "expand=True turns the pieces into columns.",
        "split with expand=True returns a DataFrame with one column per piece (labelled 0, 1). Without expand you get a Series of lists.",
        topic="strings", level=2),
    out("""import pandas as pd
s = pd.Series(["a.b", "axb"])
print(s.str.contains(".", regex=False).tolist(), s.str.contains(".").tolist())""",
        ["[True, False] [True, True]", "[True, False] [True, False]", "[True, True] [True, True]", "[True, True] [True, False]"], 0,
        "contains treats the pattern as a regular expression by default.",
        "In regex '.' means 'any character', so both strings match. regex=False searches for a literal dot.",
        topic="strings", level=3),
    out("""import pandas as pd
s = pd.Series(["apple", None, "kiwi"])
print(s.str.len().tolist())""",
        ["[5.0, nan, 4.0]", "[5, 0, 4]", "TypeError", "[5, None, 4]"], 0,
        ".str methods pass missing values through.",
        "The None stays missing (NaN), and NaN makes the result float64.",
        topic="strings", level=2),
    out("""import pandas as pd
s = pd.Series(["apple", None, "kiwi"])
print(s[s.str.contains("a")])""",
        ["ValueError", "0    apple\ndtype: object", "TypeError", "KeyError"], 0,
        "What does contains return for the None row, and can a mask contain that?",
        "contains gives [True, NaN, False]; the mask has a missing value, so boolean indexing raises ValueError ('Cannot mask with non-boolean array containing NA / NaN values'). Pass na=False.",
        topic="strings", level=3),
    out("""import pandas as pd
s = pd.Series(["order-17", "order-305"])
print(s.str.extract(r"(\\d+)")[0].astype(int).tolist())""",
        ["[17, 305]", "['17', '305']", "[1, 3]", "ValueError"], 0,
        "extract returns the regex capture group as a column.",
        "str.extract with one group returns a DataFrame whose column 0 holds '17' and '305'; astype(int) makes them numbers.",
        topic="strings", level=3),
    out("""import pandas as pd
s = pd.Series(["Hello"])
print(s.str[1:3].tolist(), s.str[0].tolist())""",
        ["['el'] ['H']", "['ell'] ['H']", "TypeError", "['He'] ['e']"], 0,
        ".str also supports slicing each string.",
        "s.str[1:3] slices every string like Python ('el'); s.str[0] takes the first character.",
        topic="strings", level=2),
    out("""import pandas as pd
s = pd.Series([" a", "b "])
print((s == "a").sum(), (s.str.strip() == "a").sum())""",
        ["0 1", "1 1", "0 0", "2 1"], 0,
        "Invisible whitespace breaks equality.",
        "' a' is not equal to 'a'. Stray spaces from CSVs and forms are the #1 reason filters or merges silently miss rows.",
        topic="strings", level=2),
    mcq("Why is `s.str.lower()` not truly vectorised the way `s * 2` is for numbers?",
        ["For object dtype, it still loops over Python str objects in Python; there is no fixed-width C array of strings",
         "Because .str methods run on the GPU",
         "Because lower() has to sort the strings first",
         "It is exactly as fast as numeric operations"], 0,
        "How are strings stored in an object column?",
        "An object column holds pointers to Python strings, so .str methods are a convenient Python-level loop (they handle NaN for you). The pyarrow-backed 'string[pyarrow]' dtype can run many string ops in compiled code.",
        topic="strings", level=4),

    # ------------------------------------------------------------------ groupby
    mcq("What does `df.groupby('city')['sales'].sum()` do?",
        ["Splits rows by city, sums sales within each city, and returns one total per city",
         "Sorts the DataFrame by city and then by sales",
         "Adds a running total of sales to each row",
         "Returns the total of all sales in the table"], 0,
        "Split, apply, combine.",
        "groupby splits rows into one group per city, applies sum to each group's sales, and combines the results into a Series indexed by city.",
        analogy="SQL: SELECT city, SUM(sales) FROM df GROUP BY city.",
        diagram="""
split          apply         combine
Pune  5 \\
Pune  7 / ->  sum = 12  \\
Goa   3   ->  sum =  3  +->  Goa 3, Pune 12""",
        topic="groupby", level=1),
    out("""import pandas as pd
df = pd.DataFrame({"city": ["Pune", "Goa", "Pune"], "sales": [5, 3, 7]})
print(df.groupby("city")["sales"].sum().to_dict())""",
        ["{'Goa': 3, 'Pune': 12}", "{'Pune': 12, 'Goa': 3}", "{'Pune': 5, 'Goa': 3}", "15"], 0,
        "Group keys come back sorted.",
        "Pune 5 + 7 = 12, Goa 3. groupby sorts keys by default (sort=True), so Goa comes first.",
        topic="groupby", level=1),
    out("""import pandas as pd
df = pd.DataFrame({"city": ["Pune", "Goa", "Pune"], "sales": [5, 3, 7]})
r = df.groupby("city")["sales"].mean()
print(type(r).__name__, r.index.name)""",
        ["Series city", "DataFrame city", "Series None", "DataFrame None"], 0,
        "One column selected, one value per group.",
        "Selecting a single column before aggregating gives a Series, indexed by the group key, whose index name is 'city'.",
        topic="groupby", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"city": ["Pune", "Goa", "Pune"], "sales": [5, 3, 7]})
r = df.groupby("city", as_index=False)["sales"].sum()
print(r.columns.tolist(), r.shape)""",
        ["['city', 'sales'] (2, 2)", "['sales'] (2, 1)", "['city', 'sales'] (3, 2)", "['sales'] (2,)"], 0,
        "as_index=False keeps the key as a normal column.",
        "With as_index=False the result is a DataFrame with city as a column (like SQL output), not as the index. Same as .sum().reset_index().",
        topic="groupby", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"city": ["Pune", "Goa", "Pune"], "sales": [5, 3, 7]})
r = df.groupby("city")["sales"].agg(["sum", "mean", "max"])
print(r.loc["Pune"].tolist())""",
        ["[12.0, 6.0, 7.0]", "[12, 6, 7]", "[5, 7, 12]", "KeyError"], 0,
        "A row of a DataFrame is a Series with one dtype.",
        "agg with a list gives one column per function. The Pune row holds 12, 6.0 and 7; since the mean is a float, the row Series is float64.",
        topic="groupby", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"city": ["Pune", "Goa", "Pune"], "sales": [5, 3, 7], "qty": [1, 2, 3]})
r = df.groupby("city").agg(total=("sales", "sum"), orders=("qty", "count"))
print(r.columns.tolist(), r.loc["Pune", "total"])""",
        ["['total', 'orders'] 12", "[('sales', 'sum'), ('qty', 'count')] 12", "['sales', 'qty'] 12", "TypeError"], 0,
        "Named aggregation: new_name=(column, function).",
        "Named aggregation gives flat, readable column names (like SQL's SUM(sales) AS total) instead of a MultiIndex.",
        topic="groupby", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"city": ["P", "P", "G", "G"], "year": [1, 2, 1, 1], "s": [1, 2, 3, 4]})
r = df.groupby(["city", "year"])["s"].sum()
print(r.index.nlevels, r.to_dict())""",
        ["2 {('G', 1): 7, ('P', 1): 1, ('P', 2): 2}", "1 {'G': 7, 'P': 3}", "2 {('P', 1): 1, ('P', 2): 2, ('G', 1): 7}", "2 {'G1': 7, 'P1': 1, 'P2': 2}"], 0,
        "Grouping by two columns gives a two-level key.",
        "The result is indexed by a MultiIndex of (city, year) tuples, sorted. G/1 has 3 + 4 = 7.",
        topic="groupby", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"g": ["a", "a", "b"], "txt": ["x", "y", "z"], "v": [1, 2, 3]})
r = df.groupby("g").sum()
print(r.loc["a", "txt"], r.loc["a", "v"])""",
        ["xy 3", "nan 3", "TypeError", "x 3"], 0,
        "What does + mean for strings?",
        "sum on an object column concatenates the strings, so 'x' + 'y' = 'xy'. Select the numeric columns first, or pass numeric_only=True, to avoid surprises.",
        topic="groupby", level=3),
    out("""import pandas as pd
df = pd.DataFrame({"g": ["a", "a", "b"], "txt": ["x", "y", "z"], "v": [1, 2, 3]})
print(df.groupby("g").mean())""",
        ["TypeError", "   v\ng   \na  1.5\nb  3.0", "ValueError", "     txt    v\ng          \na    NaN  1.5\nb    NaN  3.0"], 0,
        "pandas 2.x no longer silently drops columns it can't average.",
        "Since pandas 2.0, numeric_only defaults to False, so mean() tries to average the text column and raises TypeError. Use numeric_only=True or select ['v'] first.",
        topic="groupby", level=3),
    fill("To get per-group totals with the key as a normal column (like SQL output), pass `as_index=____` to groupby.",
        "False",
        "The opposite of the default.",
        "groupby(..., as_index=False) returns the keys as columns instead of the index.",
        topic="groupby", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"g": ["b", "a", "b"], "v": [1, 2, 3]})
print(list(df.groupby("g", sort=False).groups.keys()))""",
        ["['b', 'a']", "['a', 'b']", "['b', 'a', 'b']", "[0, 1, 2]"], 0,
        "sort=False keeps keys in order of first appearance.",
        "With sort=False, keys follow first appearance (b, then a). It can also speed up large groupbys.",
        topic="groupby", level=3),
    out("""import pandas as pd
df = pd.DataFrame({"g": ["a", "a", "b"], "v": [1, 5, 3]})
print(df.groupby("g")["v"].agg(lambda s: s.max() - s.min()).to_dict())""",
        ["{'a': 4, 'b': 0}", "{'a': 5, 'b': 3}", "{'a': 1, 'b': 3}", "TypeError"], 0,
        "agg can take any function that reduces a Series to one value.",
        "The custom function computes the range per group: a 5-1 = 4, b 3-3 = 0.",
        topic="groupby", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"g": ["a", "a", "b"], "v": [1, 5, 3]})
print(df.groupby("g").filter(lambda grp: grp["v"].sum() > 4)["v"].tolist())""",
        ["[1, 5]", "[3]", "[6]", "[1, 5, 3]"], 0,
        "filter keeps or drops whole groups.",
        "Group a sums to 6 (> 4) and is kept with all its rows; group b sums to 3 and is dropped.",
        analogy="SQL: HAVING SUM(v) > 4, but returning the original rows.",
        topic="groupby", level=3),

    # ------------------------------------------------------------------ groupby-advanced
    out("""import pandas as pd
import numpy as np
df = pd.DataFrame({"g": ["a", "a", "b"], "v": [1, np.nan, 3]})
print(df.groupby("g").size().to_dict(), df.groupby("g")["v"].count().to_dict())""",
        ["{'a': 2, 'b': 1} {'a': 1, 'b': 1}", "{'a': 2, 'b': 1} {'a': 2, 'b': 1}", "{'a': 1, 'b': 1} {'a': 2, 'b': 1}", "{'a': 1, 'b': 1} {'a': 1, 'b': 1}"], 0,
        "One counts rows, the other counts non-missing values.",
        "size() counts rows in each group (COUNT(*)); count() counts non-NaN values in the column (COUNT(v)). Group a has 2 rows but only 1 non-missing v.",
        diagram="""
g   v       size()  count()
a   1   \\
a   NaN /    2        1
b   3        1        1""",
        analogy="SQL: COUNT(*) vs COUNT(v).",
        topic="groupby-advanced", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"g": ["a", "a", "b"], "v": [1, 3, 5]})
print(df.groupby("g")["v"].transform("mean").tolist(), df.groupby("g")["v"].agg("mean").tolist())""",
        ["[2.0, 2.0, 5.0] [2.0, 5.0]", "[2.0, 5.0] [2.0, 2.0, 5.0]", "[2.0, 2.0, 5.0] [2.0, 2.0, 5.0]", "[2.0, 5.0] [2.0, 5.0]"], 0,
        "One returns a value per group, the other a value per original row.",
        "agg reduces each group to one row (2 results). transform broadcasts the group's result back onto every original row (3 results), aligned with df.",
        diagram="""
g  v     agg('mean')   transform('mean')
a  1  \\                     2.0
a  3  /  a -> 2.0           2.0
b  5     b -> 5.0           5.0""",
        topic="groupby-advanced", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"g": ["a", "a", "b"], "v": [1, 3, 5]})
df["share"] = df["v"] / df.groupby("g")["v"].transform("sum")
print(df["share"].tolist())""",
        ["[0.25, 0.75, 1.0]", "[0.1111111111111111, 0.3333333333333333, 0.5555555555555556]", "ValueError", "[nan, nan, nan]"], 0,
        "transform keeps the original shape, so you can divide row by row.",
        "transform('sum') gives each row its group's total (4, 4, 5), so share = 1/4, 3/4, 5/5. Using agg here would misalign.",
        topic="groupby-advanced", level=3),
    out("""import pandas as pd
import numpy as np
df = pd.DataFrame({"g": ["a", "a", "b", "b"], "v": [1, np.nan, np.nan, 7]})
df["v"] = df["v"].fillna(df.groupby("g")["v"].transform("mean"))
print(df["v"].tolist())""",
        ["[1.0, 1.0, 7.0, 7.0]", "[1.0, 4.0, 4.0, 7.0]", "[1.0, nan, nan, 7.0]", "[1.0, 0.0, 0.0, 7.0]"], 0,
        "Fill each missing value with the mean of its own group.",
        "transform('mean') gives a per-row group mean (a: 1, b: 7), and fillna uses it aligned by index. Group-wise imputation is common for features like 'price by category'.",
        topic="groupby-advanced", level=3),
    out("""import pandas as pd
df = pd.DataFrame({"g": ["a", "a", "b"], "v": [1, 3, 5]})
print(df.groupby("g")["v"].cumsum().tolist(), df.groupby("g").cumcount().tolist())""",
        ["[1, 4, 5] [0, 1, 0]", "[1, 4, 9] [0, 1, 2]", "[4, 4, 5] [1, 2, 1]", "[1, 4, 5] [1, 2, 1]"], 0,
        "Cumulative functions restart in each group.",
        "cumsum runs within each group (1, 1+3, then 5 for b). cumcount numbers rows within the group starting at 0.",
        analogy="SQL window functions: SUM(v) OVER (PARTITION BY g ORDER BY ...), ROW_NUMBER() - 1.",
        topic="groupby-advanced", level=3),
    out("""import pandas as pd
df = pd.DataFrame({"g": ["a", "a", "b"], "v": [1, 3, 5]})
print(df.groupby("g")["v"].shift(1).tolist())""",
        ["[nan, 1.0, nan]", "[nan, 1.0, 3.0]", "[3.0, nan, nan]", "[1.0, 3.0, 5.0]"], 0,
        "shift moves values down by one, but not across group borders.",
        "Within group a, 3's previous value is 1; the first row of each group has nothing before it, so NaN. This is the safe way to build 'previous value' features (SQL LAG).",
        topic="groupby-advanced", level=3),
    out("""import pandas as pd
df = pd.DataFrame({"g": ["a", None, "a"], "v": [1, 2, 3]})
print(df.groupby("g")["v"].sum().to_dict(), df.groupby("g", dropna=False)["v"].sum().sum())""",
        ["{'a': 4} 6", "{'a': 4, None: 2} 6", "{'a': 4} 4", "{'a': 6} 6"], 0,
        "By default rows with a missing group key are dropped.",
        "groupby drops rows whose key is NaN/None (dropna=True), silently losing value 2. dropna=False keeps a NaN group, so the total is 6 again.",
        topic="groupby-advanced", level=3),
    out("""import pandas as pd
df = pd.DataFrame({"g": ["a", "a", "b"], "v": [1, 3, 5]})
r = df.groupby("g")["v"].apply(lambda s: s - s.mean())
print(r.tolist())""",
        ["[-1.0, 1.0, 0.0]", "[2.0, 5.0]", "[-1.0, 1.0]", "TypeError"], 0,
        "apply can return a whole Series per group, not just one value.",
        "Here each group returns a same-length Series (centred values), so apply behaves like transform. apply is the flexible but slowest option; prefer transform when the output is row-shaped.",
        topic="groupby-advanced", level=3),
    mcq("Which groupby method should you use to add a column 'customer_total' to every order row?",
        ["transform", "agg", "size", "filter"], 0,
        "The result must have one value per ORIGINAL row.",
        "transform returns an object indexed like the original rows, so it can be assigned straight back as a column. agg returns one row per customer.",
        topic="groupby-advanced", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"g": ["a", "a", "b", "b", "b"], "v": [5, 9, 1, 8, 4]})
top = df.sort_values("v", ascending=False).groupby("g").head(1)
print(top["v"].tolist(), df.loc[df.groupby("g")["v"].idxmax(), "v"].tolist())""",
        ["[9, 8] [9, 8]", "[9, 8] [5, 1]", "[8, 9] [9, 8]", "[9] [9, 8]"], 0,
        "Two ways to get the top row of each group.",
        "Sorting then head(1) per group keeps the largest v of each group in sorted order (9 then 8). idxmax returns the index label of each group's max, which loc then fetches.",
        topic="groupby-advanced", level=4),
    out("""import pandas as pd
df = pd.DataFrame({"g": pd.Categorical(["a", "a"], categories=["a", "b"]), "v": [1, 2]})
print(df.groupby("g", observed=False)["v"].sum().to_dict(), df.groupby("g", observed=True)["v"].sum().to_dict())""",
        ["{'a': 3, 'b': 0} {'a': 3}", "{'a': 3} {'a': 3}", "{'a': 3} {'a': 3, 'b': 0}", "{'a': 3, 'b': nan} {'a': 3}"], 0,
        "With a categorical key, unused categories can still appear as groups.",
        "observed=False includes every declared category, even empty ones (sum of nothing = 0). observed=True shows only groups that actually occur; it will become the default in a future pandas release.",
        topic="groupby-advanced", level=4),
    out("""import pandas as pd
df = pd.DataFrame({"g": ["a", "b"], "v": [1, 2]})
print(df.groupby("g")["v"].sum(min_count=1).tolist(), df[df.v > 5].groupby("g")["v"].sum().tolist())""",
        ["[1, 2] []", "[1, 2] [0]", "[1.0, 2.0] []", "[1, 2] [0, 0]"], 0,
        "An empty frame has no groups at all.",
        "Each group has one value, so min_count=1 is satisfied. After filtering out every row there are no keys left, so the result is empty, not zeros.",
        topic="groupby-advanced", level=4),
    mcq("Why is `df.groupby('g').apply(f)` often much slower than `agg`/`transform` with built-in names like 'sum'?",
        ["Built-in names dispatch to optimised Cython group kernels; apply calls a Python function per group and must then infer how to stitch the results",
         "apply sorts the whole DataFrame twice",
         "agg runs on multiple threads by default",
         "apply copies the DataFrame to disk"], 0,
        "Strings like 'sum' vs a Python callable.",
        "String aggregations ('sum', 'mean', 'size') run in one compiled pass over all groups. apply builds a sub-DataFrame per group, calls Python, then guesses whether to concat, broadcast or reduce. With millions of small groups the per-group overhead dominates.",
        topic="groupby-advanced", level=4),

    # ------------------------------------------------------------------ merge
    mcq("Which pandas function is the closest match to a SQL JOIN?",
        ["pd.merge (or df.merge)", "pd.concat", "df.groupby", "df.pivot"], 0,
        "Combine two tables on a matching key.",
        "merge matches rows on key columns, with how='inner'/'left'/'right'/'outer' like the SQL join types. concat just stacks tables.",
        topic="merge", level=1),
    out("""import pandas as pd
users = pd.DataFrame({"uid": [1, 2, 3], "name": ["Ann", "Bob", "Cy"]})
orders = pd.DataFrame({"uid": [1, 1, 3], "amt": [10, 20, 5]})
print(len(users.merge(orders, on="uid")), len(users.merge(orders, on="uid", how="left")))""",
        ["3 4", "3 3", "4 4", "2 3"], 0,
        "Inner keeps only matches; left keeps every user.",
        "Inner: Ann matches 2 orders, Cy 1, Bob none -> 3 rows. Left join also keeps Bob with NaN amt -> 4 rows.",
        diagram="""
users  orders     inner        left
1 Ann  1 10       Ann 10       Ann 10
2 Bob  1 20       Ann 20       Ann 20
3 Cy   3  5       Cy   5       Bob NaN
                               Cy   5""",
        topic="merge", level=1),
    tf("The default `how` for `pd.merge` is 'inner'.", True,
        "Same default as a plain SQL JOIN.",
        "merge defaults to an inner join: only keys present in both tables survive. Pass how='left' to keep every row of the left table.",
        topic="merge", level=1),
    out("""import pandas as pd
a = pd.DataFrame({"k": [1, 1, 2], "x": ["a", "b", "c"]})
b = pd.DataFrame({"k": [1, 1, 3], "y": ["p", "q", "r"]})
print(len(a.merge(b, on="k")), len(a.merge(b, on="k", how="outer")))""",
        ["4 6", "2 4", "4 4", "2 5"], 0,
        "Duplicate keys on BOTH sides multiply: every match pairs with every match.",
        "Key 1 appears twice on each side -> 2 x 2 = 4 rows. Outer adds the unmatched k=2 and k=3 rows -> 6. This is how merges 'blow up' row counts.",
        diagram="""
left k=1: a, b      right k=1: p, q
              a-p   a-q
              b-p   b-q     -> 4 rows for one key
duplicate keys on both sides multiply rows""",
        topic="merge", level=2),
    out("""import pandas as pd
a = pd.DataFrame({"id": [1, 2], "v": [10, 20]})
b = pd.DataFrame({"id": [1, 2], "v": [30, 40]})
print(a.merge(b, on="id").columns.tolist())""",
        ["['id', 'v_x', 'v_y']", "['id', 'v', 'v']", "['id', 'v']", "ValueError"], 0,
        "Two non-key columns share a name.",
        "Overlapping non-key columns get suffixes _x (left) and _y (right). Use suffixes=('_old', '_new') for clearer names.",
        topic="merge", level=2),
    out("""import pandas as pd
a = pd.DataFrame({"user_id": [1, 2], "v": [10, 20]})
b = pd.DataFrame({"uid": [2, 3], "w": [5, 6]})
r = a.merge(b, left_on="user_id", right_on="uid")
print(r.columns.tolist(), len(r))""",
        ["['user_id', 'v', 'uid', 'w'] 1", "['user_id', 'v', 'w'] 1", "['uid', 'v', 'w'] 2", "KeyError"], 0,
        "Different key names on each side keep both key columns.",
        "left_on/right_on join columns with different names; both columns stay in the result. Only id 2 matches.",
        topic="merge", level=2),
    out("""import pandas as pd
a = pd.DataFrame({"k": [1, 2]})
b = pd.DataFrame({"k": [2, 3]})
r = a.merge(b, on="k", how="outer", indicator=True)
print(r["_merge"].astype(str).tolist())""",
        ["['left_only', 'both', 'right_only']", "['both', 'left_only', 'right_only']", "[True, True, True]", "['left', 'both', 'right']"], 0,
        "indicator adds a column saying where each row came from.",
        "Key 1 only exists on the left, 2 in both, 3 only on the right. indicator=True is great for auditing joins.",
        topic="merge", level=3),
    out("""import pandas as pd
a = pd.DataFrame({"k": [1, 2], "x": [1, 2]})
b = pd.DataFrame({"k": [1, 1], "y": [3, 4]})
try:
    a.merge(b, on="k", validate="one_to_one")
except Exception as e:
    print(type(e).__name__)""",
        ["MergeError", "ValueError", "KeyError", "(nothing is printed)"], 0,
        "validate checks your assumption about key uniqueness.",
        "validate='one_to_one' requires unique keys on both sides; b has k=1 twice, so merge raises MergeError instead of silently duplicating rows.",
        topic="merge", level=3),
    out("""import pandas as pd
a = pd.DataFrame({"k": [1, 2]})
b = pd.DataFrame({"k": ["1", "2"]})
print(a.merge(b, on="k"))""",
        ["ValueError", "   k\n0  1\n1  2", "Empty DataFrame\nColumns: [k]\nIndex: []", "TypeError"], 0,
        "int keys vs string keys.",
        "pandas refuses to merge an int64 key with an object (string) key and raises ValueError ('You are trying to merge on int64 and object columns'). Convert types first.",
        topic="merge", level=3),
    out("""import pandas as pd
users = pd.DataFrame({"uid": [1, 2], "name": ["Ann", "Bob"]})
orders = pd.DataFrame({"uid": [1], "amt": [10]})
r = users.merge(orders, on="uid", how="left")
print(r["amt"].dtype, r["amt"].isna().sum())""",
        ["float64 1", "int64 0", "int64 1", "object 1"], 0,
        "Bob has no order. What fills his amt?",
        "Unmatched left rows get NaN in the right table's columns, which upcasts an int column to float64. Count NaNs after a left join to see how many rows found no match.",
        topic="merge", level=2),
    out("""import pandas as pd
left = pd.DataFrame({"v": [1, 2]}, index=["a", "b"])
right = pd.DataFrame({"w": [3]}, index=["b"])
print(left.join(right)["w"].tolist())""",
        ["[nan, 3.0]", "[3]", "[3.0, nan]", "KeyError"], 0,
        "join matches on the index, and is a left join by default.",
        "df.join aligns on the index with how='left', so row a has no w (NaN) and b gets 3.",
        topic="merge", level=2),
    mcq("You merge 1,000 orders with a products table on product_id and get 1,350 rows. What is the most likely cause?",
        ["product_id is not unique in the products table, so some orders matched several product rows",
         "merge always adds the right table's rows to the end",
         "Orders with missing product_id were duplicated",
         "The merge used how='inner' instead of how='left'"], 0,
        "A lookup table should have one row per key.",
        "When the right-hand key is duplicated, each matching order is repeated once per duplicate. Check products['product_id'].is_unique, or pass validate='many_to_one' to fail fast.",
        topic="merge", level=3),
    out("""import pandas as pd
a = pd.DataFrame({"k": [1, None], "x": [1, 2]})
b = pd.DataFrame({"k": [None, 1], "y": [3, 4]})
print(len(a.merge(b, on="k")))""",
        ["2", "1", "0", "4"], 0,
        "Unlike SQL, pandas treats missing keys as equal to each other.",
        "In SQL, NULL never equals NULL in a join, so you'd get 1 row. pandas matches NaN keys with NaN keys, giving 2 rows. Drop missing keys before merging if you want SQL behaviour.",
        topic="merge", level=4),
    out("""import pandas as pd
trades = pd.DataFrame({"t": [2, 5, 9], "qty": [1, 2, 3]})
quotes = pd.DataFrame({"t": [1, 4, 8], "px": [10, 11, 12]})
print(pd.merge_asof(trades, quotes, on="t")["px"].tolist())""",
        ["[10, 11, 12]", "[11, 12, 12]", "[10, 10, 11]", "[nan, 11.0, nan]"], 0,
        "merge_asof matches each row to the most recent earlier key.",
        "For each trade time it takes the last quote at or before it: t=2 -> 1 (10), t=5 -> 4 (11), t=9 -> 8 (12). Both sides must be sorted on the key. Used for point-in-time features without future leakage.",
        diagram="""
quotes: t=1 (10)    t=4 (11)        t=8 (12)
trades:    t=2 -/      t=5 -/          t=9 -/
           -> 10       -> 11           -> 12
(always look backward, never forward)""",
        topic="merge", level=4),

    # ------------------------------------------------------------------ concat
    out("""import pandas as pd
a = pd.DataFrame({"x": [1, 2]})
b = pd.DataFrame({"x": [3]})
r = pd.concat([a, b])
print(r["x"].tolist(), r.index.tolist())""",
        ["[1, 2, 3] [0, 1, 0]", "[1, 2, 3] [0, 1, 2]", "[4, 2] [0, 1]", "[1, 2, 3] [1, 2, 3]"], 0,
        "concat stacks rows and keeps each piece's original index.",
        "Rows are stacked a then b; the index labels are kept as they were, so 0 appears twice. Use ignore_index=True for a fresh 0..n-1.",
        analogy="SQL: UNION ALL.",
        topic="concat", level=1),
    out("""import pandas as pd
a = pd.DataFrame({"x": [1, 2]})
b = pd.DataFrame({"x": [3]})
print(pd.concat([a, b], ignore_index=True).index.tolist())""",
        ["[0, 1, 2]", "[0, 1, 0]", "[1, 2, 3]", "[0, 0, 1]"], 0,
        "ignore_index throws away the old labels.",
        "ignore_index=True renumbers the stacked rows 0, 1, 2.",
        topic="concat", level=1),
    out("""import pandas as pd
a = pd.DataFrame({"x": [1], "y": [2]})
b = pd.DataFrame({"x": [3], "z": [4]})
r = pd.concat([a, b], ignore_index=True)
print(r.columns.tolist(), r.isna().sum().sum())""",
        ["['x', 'y', 'z'] 2", "['x'] 0", "ValueError", "['x', 'y', 'x', 'z'] 0"], 0,
        "Columns are matched by name; missing ones are filled.",
        "concat takes the union of columns (outer join on columns). a has no z and b has no y, so 2 cells are NaN. join='inner' would keep only x.",
        topic="concat", level=2),
    out("""import pandas as pd
a = pd.DataFrame({"x": [1, 2]})
b = pd.DataFrame({"y": [3, 4]})
print(pd.concat([a, b], axis=1).shape)""",
        ["(2, 2)", "(4, 2)", "(4, 1)", "(2, 1)"], 0,
        "axis=1 places frames side by side.",
        "axis=1 aligns rows on the index and puts the columns next to each other: 2 rows, 2 columns.",
        diagram="""
axis=0 (default)        axis=1
  x    y                x  y
  1   NaN               1  3
  2   NaN               2  4
 NaN   3
 NaN   4""",
        topic="concat", level=2),
    out("""import pandas as pd
a = pd.DataFrame({"x": [1, 2]}, index=[0, 1])
b = pd.DataFrame({"y": [3, 4]}, index=[1, 2])
print(pd.concat([a, b], axis=1).shape)""",
        ["(3, 2)", "(2, 2)", "(4, 2)", "ValueError"], 0,
        "Side-by-side concat aligns on index labels, not positions.",
        "The union of the indexes is 0, 1, 2, so the result has 3 rows with NaNs where a frame has no row. A common bug when the two parts were filtered differently.",
        topic="concat", level=3),
    tf("Appending rows one at a time with `df = pd.concat([df, new_row])` inside a loop is an efficient way to build a large DataFrame.", False,
        "Each concat copies everything so far.",
        "Every concat builds a brand-new frame, so a loop of n appends costs O(n^2). Collect rows in a Python list (of dicts) and build one DataFrame at the end.",
        analogy="Like rebuilding a whole array every time you push one element.",
        topic="concat", level=3),
    out("""import pandas as pd
a = pd.DataFrame({"v": [1]})
b = pd.DataFrame({"v": [2]})
r = pd.concat([a, b], keys=["jan", "feb"])
print(r.index.tolist())""",
        ["[('jan', 0), ('feb', 0)]", "['jan', 'feb']", "[0, 0]", "[0, 1]"], 0,
        "keys adds an outer index level saying which piece each row came from.",
        "keys=['jan', 'feb'] builds a MultiIndex (source, original label), handy for tracking which file a row came from.",
        topic="concat", level=3),
    fill("To stack two DataFrames vertically and renumber the rows 0..n-1, call `pd.concat([a, b], ____=True)`.",
        "ignore_index",
        "Ignore the old labels.",
        "ignore_index=True discards the original index labels and creates a new RangeIndex.",
        topic="concat", level=2),

    # ------------------------------------------------------------------ reshape
    mcq("What does `melt` do?",
        ["Turns wide data (one column per measurement) into long data (one row per measurement)",
         "Merges two DataFrames on a key",
         "Converts strings to numbers",
         "Removes duplicate rows"], 0,
        "Many columns become two: variable and value.",
        "melt unpivots: columns like q1, q2, q3 become rows, with a 'variable' column holding the old column name and a 'value' column holding the number.",
        topic="reshape", level=1),
    out("""import pandas as pd
w = pd.DataFrame({"id": [1, 2], "q1": [5, 6], "q2": [7, 8]})
print(w.melt(id_vars="id"))""",
        ["   id variable  value\n0   1       q1      5\n1   2       q1      6\n2   1       q2      7\n3   2       q2      8",
         "   id variable  value\n0   1       q1      5\n1   1       q2      7\n2   2       q1      6\n3   2       q2      8",
         "   id  q1  q2\n0   1   5   7\n1   2   6   8",
         "   variable  value\n0       q1      5\n1       q1      6\n2       q2      7\n3       q2      8"], 0,
        "melt goes column by column: all of q1, then all of q2.",
        "id_vars stays as an identifier; every other column is unpivoted into (variable, value) rows, in column order.",
        diagram="""
wide:  id q1 q2        long:  id variable value
        1  5  7   ->           1   q1      5
        2  6  8                2   q1      6
                               1   q2      7
                               2   q2      8""",
        topic="reshape", level=2),
    out("""import pandas as pd
long = pd.DataFrame({"day": ["mon", "mon", "tue"], "city": ["P", "G", "P"], "t": [30, 28, 31]})
w = long.pivot(index="day", columns="city", values="t")
print(w.shape, w.loc["tue", "G"])""",
        ["(2, 2) nan", "(3, 3) nan", "(2, 2) 0", "KeyError"], 0,
        "pivot spreads one column's values into new columns.",
        "pivot makes one row per day and one column per city. Tuesday has no G reading, so that cell is NaN.",
        topic="reshape", level=2),
    out("""import pandas as pd
p = pd.DataFrame({"d": ["x", "x", "y"], "c": ["m", "m", "n"], "v": [1, 2, 3]})
p.pivot(index="d", columns="c", values="v")""",
        ["ValueError", "KeyError", "TypeError", "(nothing is printed)"], 0,
        "Two rows land in the same (x, m) cell.",
        "pivot can only reshape, not aggregate. Duplicate (index, column) pairs raise ValueError ('Index contains duplicate entries'). Use pivot_table with an aggfunc.",
        topic="reshape", level=3),
    out("""import pandas as pd
p = pd.DataFrame({"d": ["x", "x", "y"], "c": ["m", "m", "n"], "v": [1, 2, 3]})
print(p.pivot_table(index="d", columns="c", values="v").loc["x", "m"])""",
        ["1.5", "3", "1", "ValueError"], 0,
        "pivot_table aggregates duplicates, and its default aggfunc is...?",
        "pivot_table's default aggfunc is 'mean', so the two values 1 and 2 in (x, m) become 1.5. Pass aggfunc='sum' for 3.",
        topic="reshape", level=3),
    out("""import pandas as pd
p = pd.DataFrame({"d": ["x", "x", "y"], "c": ["m", "n", "n"], "v": [1, 2, 3]})
t = p.pivot_table(index="d", columns="c", values="v", aggfunc="sum", fill_value=0, margins=True)
print(t.loc["All", "All"], t.loc["y", "m"])""",
        ["6 0", "6 nan", "3 0", "KeyError"], 0,
        "margins adds totals; fill_value replaces empty cells.",
        "margins=True adds an 'All' row and column with grand totals (1 + 2 + 3 = 6). The empty (y, m) cell is filled with 0.",
        topic="reshape", level=3),
    out("""import pandas as pd
df = pd.DataFrame({"sex": ["M", "F", "F", "M"], "smoker": ["y", "n", "y", "y"]})
print(pd.crosstab(df["sex"], df["smoker"]).loc["M", "y"])""",
        ["2", "1", "0", "4"], 0,
        "crosstab counts how often each pair of values occurs.",
        "crosstab builds a frequency table: M and y occurs twice.",
        topic="reshape", level=2),
    mcq("A plotting library or model needs 'long' (tidy) data: one row per observation. You have columns jan, feb, mar of sales per store. Which call fixes it?",
        ['df.melt(id_vars="store", var_name="month", value_name="sales")',
         'df.pivot(index="store", columns="month")',
         'df.groupby("store").sum()',
         'pd.concat([df["jan"], df["feb"], df["mar"]], axis=1)'], 0,
        "Wide -> long.",
        "melt turns the month columns into (month, sales) rows; var_name/value_name set the new column names. pivot goes the other way (long -> wide).",
        topic="reshape", level=2),
    out("""import pandas as pd
s = pd.DataFrame({"d": ["x", "y"], "m": [1, 2], "n": [3, 4]}).set_index("d").stack()
print(s.index.tolist(), s.tolist())""",
        ["[('x', 'm'), ('x', 'n'), ('y', 'm'), ('y', 'n')] [1, 3, 2, 4]", "[('x', 'm'), ('y', 'm'), ('x', 'n'), ('y', 'n')] [1, 2, 3, 4]", "['x', 'y'] [1, 2]", "['m', 'n'] [1, 3]"], 0,
        "stack moves the columns into the innermost index level, row by row.",
        "stack walks each row and pushes its columns into the index, giving (row, column) tuples: x-m, x-n, y-m, y-n. unstack is the inverse.",
        topic="reshape", level=4),
    tf("`pivot_table(..., aggfunc='sum')` and `groupby([a, b])[v].sum().unstack()` produce the same table.", True,
        "pivot_table is built on groupby.",
        "pivot_table groups by the index and columns keys, aggregates, then unstacks the column key. Both give the same numbers (pivot_table can add fill_value and margins conveniently).",
        topic="reshape", level=4),

    # ------------------------------------------------------------------ binning
    out("""import pandas as pd
ages = pd.Series([5, 25, 70])
print(pd.cut(ages, bins=[0, 18, 60, 100], labels=["kid", "adult", "senior"]).tolist())""",
        ["['kid', 'adult', 'senior']", "[0, 1, 2]", "['kid', 'kid', 'adult']", "[18, 60, 100]"], 0,
        "cut puts each value into the bin whose edges surround it.",
        "5 falls in (0, 18] -> kid, 25 in (18, 60] -> adult, 70 in (60, 100] -> senior.",
        topic="binning", level=1),
    mcq("What is the difference between `pd.cut` and `pd.qcut`?",
        ["cut uses fixed bin edges (equal-width or given); qcut uses quantiles so each bin has about the same number of rows",
         "cut works on strings, qcut on numbers",
         "qcut is the faster version of cut",
         "cut drops outliers, qcut keeps them"], 0,
        "The q stands for quantile.",
        "cut splits the value RANGE; qcut splits the sorted DATA into equal-count groups (e.g. quartiles).",
        topic="binning", level=2),
    out("""import pandas as pd
c = pd.cut(pd.Series([0, 5, 10]), bins=[0, 5, 10])
print(c.isna().tolist(), c.cat.codes.tolist())""",
        ["[True, False, False] [-1, 0, 1]", "[False, False, False] [0, 0, 1]", "[False, False, True] [0, 1, -1]", "[False, False, False] [0, 1, 1]"], 0,
        "Bins are (left, right]: the left edge is excluded.",
        "By default bins are right-closed, so 0 is not inside (0, 5] and becomes NaN. 5 falls in (0, 5]. Use include_lowest=True or right=False to change it.",
        diagram="""
bins=[0, 5, 10]  ->  (0, 5]   (5, 10]
                     ^ open    ^ closed
value 0  -> outside every bin -> NaN (code -1)
value 5  -> (0, 5]   value 10 -> (5, 10]""",
        topic="binning", level=3),
    out("""import pandas as pd
s = pd.Series([1, 2, 3, 4, 5, 6, 7, 100])
print(pd.qcut(s, 4, labels=False).tolist())""",
        ["[0, 0, 1, 1, 2, 2, 3, 3]", "[0, 0, 0, 0, 0, 0, 0, 3]", "[0, 1, 2, 3, 0, 1, 2, 3]", "[1, 1, 2, 2, 3, 3, 4, 4]"], 0,
        "Quantile bins have equal counts no matter how extreme a value is.",
        "qcut(4) puts 2 of the 8 values in each quartile, so the outlier 100 only affects the last bin. Equal-width cut(4) would put 7 values in the first bin.",
        diagram="""
values: 1 2 | 3 4 | 5 6 | 7 100
qcut:   q0    q1    q2    q3     (equal counts)
cut:    |1..25|25..50|50..75|75..100|
         7 vals  0      0     1     (equal widths)""",
        topic="binning", level=2),
    out("""import pandas as pd
s = pd.Series([1, 2, 3, 4, 5, 6, 7, 100])
print(pd.cut(s, 4, labels=False).value_counts().sort_index().tolist())""",
        ["[7, 1]", "[2, 2, 2, 2]", "[7, 0, 0, 1]", "[4, 4]"], 0,
        "Equal-width bins over 1..100: where do most values fall?",
        "cut(4) makes 4 bins of width ~25. Seven values land in the first bin and one in the last; value_counts omits the two empty bins.",
        topic="binning", level=3),
    out("""import pandas as pd
s = pd.Series([1, 1, 1, 1, 2])
print(pd.qcut(s, 4))""",
        ["ValueError", "TypeError", "0    (0.999, 1.0]\n1    (0.999, 1.0]\n2    (0.999, 1.0]\n3    (0.999, 1.0]\n4    (1.0, 2.0]\ndtype: category", "IndexError"], 0,
        "Several quartile edges are the same number.",
        "The quartiles are 1, 1, 1, 1, 2, so bin edges repeat and qcut raises ValueError ('Bin edges must be unique'). Pass duplicates='drop' or use rank first.",
        topic="binning", level=4),
    out("""import pandas as pd
c = pd.cut(pd.Series([5, 25]), bins=[0, 18, 60], labels=["kid", "adult"])
print(c.dtype, c.cat.codes.tolist())""",
        ["category [0, 1]", "object [0, 1]", "category ['kid', 'adult']", "int64 [0, 1]"], 0,
        "cut returns an ordered categorical.",
        "The result has category dtype with ordered categories kid < adult; the codes are the bin numbers.",
        topic="binning", level=3),
    mcq("You bin 'income' into quartiles with `pd.qcut` on the full dataset, then split into train and test. What is wrong?",
        ["The quartile edges were computed using test rows, leaking test information into the features",
         "qcut can't be used on income",
         "Quartiles must always be computed on the test set",
         "Nothing; binning can never leak"], 0,
        "Where did the edges come from?",
        "Bin edges are learned statistics. Compute them on the training set (pd.qcut(train, 4, retbins=True)) and apply the same edges to the test set with pd.cut(test, bins=edges).",
        topic="binning", level=4),

    # ------------------------------------------------------------------ datetime
    out("""import pandas as pd
d = pd.to_datetime(pd.Series(["2024-03-15", "2024-12-01"]))
print(d.dt.year.tolist(), d.dt.month.tolist(), d.dt.day_name().tolist())""",
        ["[2024, 2024] [3, 12] ['Friday', 'Sunday']", "[2024, 2024] [3, 12] ['Fri', 'Sun']", "[2024, 2024] [15, 1] ['Friday', 'Sunday']", "AttributeError"], 0,
        "The .dt accessor exposes date parts.",
        ".dt.year, .dt.month and .dt.day_name() pull parts out of each date. 15 March 2024 was a Friday; 1 December 2024 was a Sunday.",
        topic="datetime", level=1),
    tf("You can only use `.dt.year` on a column after it has been converted to a datetime dtype.", True,
        "A string '2024-03-15' has no year attribute.",
        "On an object (string) column, .dt raises AttributeError ('Can only use .dt accessor with datetimelike values'). Convert with pd.to_datetime first.",
        topic="datetime", level=1),
    out("""import pandas as pd
d = pd.to_datetime(pd.Series(["2024-01-31"]))
print((d + pd.Timedelta(days=1)).dt.strftime("%Y-%m-%d").tolist(), (d + pd.DateOffset(months=1)).dt.strftime("%Y-%m-%d").tolist())""",
        ["['2024-02-01'] ['2024-02-29']", "['2024-02-01'] ['2024-03-02']", "['2024-02-01'] ['2024-02-31']", "['2024-01-32'] ['2024-02-29']"], 0,
        "Timedelta is a fixed length of time; DateOffset follows calendar rules.",
        "Adding 1 day gives 1 Feb. Adding one calendar month to 31 Jan clips to the last day of February 2024 (a leap year): 29 Feb.",
        topic="datetime", level=3),
    out("""import pandas as pd
s = pd.Series(range(6), index=pd.date_range("2024-01-01", periods=6, freq="D"))
print(s.resample("2D").sum().tolist())""",
        ["[1, 5, 9]", "[0, 1, 2, 3, 4, 5]", "[3, 12]", "[1, 9]"], 0,
        "resample groups consecutive time windows, like groupby on time.",
        "2-day buckets: (0+1), (2+3), (4+5) = 1, 5, 9.",
        analogy="Like GROUP BY date_trunc('day', ts) in SQL, but for any window size.",
        topic="datetime", level=2),
    out("""import pandas as pd
idx = pd.to_datetime(["2024-01-10", "2024-01-20", "2024-02-05"])
s = pd.Series([1, 2, 3], index=idx)
print(s.resample("MS").sum().tolist(), s["2024-01"].tolist())""",
        ["[3, 3] [1, 2]", "[1, 2, 3] [1, 2]", "[3, 3] [1]", "KeyError"], 0,
        "'MS' = month start buckets; a partial date string selects a whole month.",
        "January totals 1 + 2 = 3, February 3. On a DatetimeIndex, s['2024-01'] selects every row in January (partial string indexing).",
        topic="datetime", level=2),
    out("""import pandas as pd
s = pd.Series([1, 2, 3, 4, 5])
print(s.rolling(3).mean().tolist())""",
        ["[nan, nan, 2.0, 3.0, 4.0]", "[1.0, 1.5, 2.0, 3.0, 4.0]", "[2.0, 3.0, 4.0]", "[nan, 2.0, 3.0, 4.0, nan]"], 0,
        "A window of 3 needs 3 values before it can produce a result.",
        "rolling(3).mean() averages each value with the two before it; the first two positions have incomplete windows, so NaN (unless min_periods is lowered).",
        diagram="""
values:   1   2   3   4   5
window:  [1   2   3]           -> 2.0
             [2   3   4]       -> 3.0
                 [3   4   5]   -> 4.0
result:  NaN NaN 2.0 3.0 4.0""",
        topic="datetime", level=2),
    out("""import pandas as pd
d = pd.Series(pd.to_datetime(["2024-01-01", "2024-01-03"]))
print(d.diff().dt.days.tolist())""",
        ["[nan, 2.0]", "[0, 2]", "[2.0, nan]", "[nan, 3.0]"], 0,
        "diff subtracts the previous row; the first row has none.",
        "diff gives Timedeltas [NaT, 2 days]; .dt.days turns them into numbers, with NaN for the missing first value.",
        topic="datetime", level=3),
    out("""import pandas as pd
t = pd.Timestamp("2024-03-10 12:00", tz="UTC")
print(t.tz_convert("Asia/Kolkata").strftime("%H:%M"))""",
        ["17:30", "12:00", "06:30", "18:00"], 0,
        "India is UTC+5:30.",
        "tz_convert changes the wall-clock representation of the same instant: 12:00 UTC is 17:30 IST. tz_localize, by contrast, attaches a zone without shifting.",
        topic="datetime", level=3),
    out("""import pandas as pd
a = pd.Timestamp("2024-01-01")
b = pd.Timestamp("2024-01-01", tz="UTC")
print(a < b)""",
        ["TypeError", "True", "False", "ValueError"], 0,
        "Can you compare a time with no zone to a time with a zone?",
        "Comparing tz-naive and tz-aware timestamps raises TypeError: pandas won't guess what zone the naive one is in. Localise or convert everything to UTC first.",
        topic="datetime", level=4),
    out("""import pandas as pd
s = pd.Series([10, 20, 30], index=pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-05"]))
print(s.asfreq("D").isna().sum(), s.resample("D").sum().tolist()[-2:])""",
        ["2 [0, 30]", "0 [20, 30]", "2 [nan, 30]", "3 [0, 30]"], 0,
        "asfreq inserts missing days as NaN; resample-sum of an empty bucket is...?",
        "asfreq('D') adds rows for 3 and 4 Jan with NaN. resample('D').sum() also creates those days, but the sum of an empty bucket is 0, which can hide gaps in time series.",
        topic="datetime", level=4),
    fill("To bucket a time-indexed Series by calendar month and sum each bucket, call `s.____(\"MS\").sum()`.",
        "resample",
        "groupby, but for time windows.",
        "resample('MS') groups rows into month-start buckets.",
        topic="datetime", level=2),

    # ------------------------------------------------------------------ ml-prep
    out("""import pandas as pd
df = pd.DataFrame({"color": ["red", "green", "red"]})
d = pd.get_dummies(df)
print(d.columns.tolist(), d.dtypes.iloc[0])""",
        ["['color_green', 'color_red'] bool", "['color_red', 'color_green'] int64", "['green', 'red'] uint8", "['color'] object"], 0,
        "One column per category, sorted; pandas 2 uses booleans.",
        "get_dummies one-hot encodes: one column per distinct value (sorted), prefixed with the column name. Since pandas 2.0 the columns are bool, not uint8; pass dtype=int if you want 0/1.",
        diagram="""
color      color_green  color_red
red    ->     False        True
green  ->     True         False
red    ->     False        True""",
        topic="ml-prep", level=1),
    mcq("Why do we one-hot encode a categorical column like `city` before giving it to most ML models?",
        ["Models need numbers, and coding cities as 0, 1, 2 would invent an order and distance that don't exist",
         "One-hot encoding makes the data smaller",
         "Models can read strings, but one-hot is faster",
         "It removes missing values"], 0,
        "Is Pune 'twice' Goa?",
        "Label codes like Goa=0, Pune=1, Delhi=2 imply Delhi > Pune > Goa. One-hot gives each city its own 0/1 column, so no fake order is created.",
        topic="ml-prep", level=1),
    out("""import pandas as pd
df = pd.DataFrame({"color": ["red", "green", "blue"]})
print(pd.get_dummies(df, drop_first=True).columns.tolist())""",
        ["['color_green', 'color_red']", "['color_blue', 'color_green']", "['color_red', 'color_green']", "['color_blue', 'color_green', 'color_red']"], 0,
        "Categories are sorted; drop_first removes the first one.",
        "Sorted categories are blue, green, red; drop_first drops blue (it's implied when both others are 0). Useful for linear models to avoid perfectly correlated columns.",
        topic="ml-prep", level=2),
    out("""import pandas as pd
train = pd.DataFrame({"c": ["a", "b"]})
test = pd.DataFrame({"c": ["a", "z"]})
print(pd.get_dummies(train).columns.tolist(), pd.get_dummies(test).columns.tolist())""",
        ["['c_a', 'c_b'] ['c_a', 'c_z']", "['c_a', 'c_b'] ['c_a', 'c_b']", "['c_a', 'c_b'] ['c_a', 'c_b', 'c_z']", "ValueError"], 0,
        "get_dummies only knows the values it sees.",
        "Encoding train and test separately gives different columns, so the model's inputs don't line up. Fit an encoder on train (OneHotEncoder(handle_unknown='ignore')) or reindex test columns to train's.",
        topic="ml-prep", level=3),
    mcq("You fill missing ages with `df['age'].fillna(df['age'].mean())` on the FULL dataset and then split into train and test. What's the problem?",
        ["Data leakage: the mean includes test rows, so information from the test set leaks into training",
         "fillna can't take a mean",
         "The mean should be computed on the test set only",
         "There is no problem as long as you shuffle"], 0,
        "Would you know the test set's mean in production?",
        "Any statistic used for preprocessing (mean, std, bin edges, vocabularies) must be learned from training data only, then applied to test. Split first, or use a scikit-learn Pipeline so this happens automatically.",
        diagram="""
WRONG                         RIGHT
full data -> fit mean         split -> train / test
          -> fill             train -> fit mean
          -> split            mean  -> fill train AND test
(test rows shaped the mean)   (test never seen while fitting)""",
        analogy="Like letting a test suite peek at the expected outputs while the code is being written.",
        topic="ml-prep", level=2),
    out("""import pandas as pd
import numpy as np
df = pd.DataFrame({"age": [20, np.nan, 40, 100]})
train, test = df.iloc[:3].copy(), df.iloc[3:].copy()
m = train["age"].mean()
train["age"] = train["age"].fillna(m)
print(m, df["age"].mean())""",
        ["30.0 53.333333333333336", "53.333333333333336 30.0", "30.0 30.0", "20.0 53.333333333333336"], 0,
        "Which rows contribute to each mean?",
        "The training mean (20, 40) is 30.0. The full-data mean includes the test row 100, giving 53.3: a different value, learned from data the model must not see.",
        topic="ml-prep", level=3),
    tf("`df.iterrows()` is the recommended way to compute a new column from two existing columns.", False,
        "How fast is a Python loop over a million rows?",
        "iterrows creates a Series for every row and loops in Python. Write df['c'] = df['a'] + df['b'] (vectorised), or use np.where / np.select for conditions.",
        topic="ml-prep", level=1),
    out("""import pandas as pd
import numpy as np
df = pd.DataFrame({"score": [35, 65, 90]})
cond = [df["score"] >= 80, df["score"] >= 50]
df["grade"] = np.select(cond, ["A", "B"], default="C")
print(df["grade"].tolist())""",
        ["['C', 'B', 'A']", "['C', 'A', 'A']", "['A', 'B', 'C']", "['C', 'B', 'B']"], 0,
        "np.select picks the FIRST condition that is True for each row.",
        "90 meets >= 80 first -> A; 65 meets only >= 50 -> B; 35 meets none -> default C. It replaces a row-wise if/elif chain with one vectorised call.",
        topic="ml-prep", level=3),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
for row in df.itertuples():
    print(row.Index, row.a + row.b)""",
        ["0 4\n1 6", "0 (1, 3)\n1 (2, 4)", "4\n6", "AttributeError"], 0,
        "itertuples yields namedtuples with an Index field plus one field per column.",
        "itertuples gives lightweight namedtuples (much faster than iterrows and dtype-preserving). row.Index is the index label.",
        topic="ml-prep", level=2),
    mcq("A feature `days_since_signup` is built as `(df['signup'].max() - df['signup']).dt.days` on the full dataset before a time-based split. Why is that a leak?",
        ["The reference date (max) comes from the latest rows, which belong to the future/test period",
         "Timedeltas can't be used as features",
         "dt.days rounds the values",
         "It's not a leak; max is a harmless statistic"], 0,
        "What date is 'today' for a training row?",
        "Using the global max lets training rows know how far the data extends into the test period. Use a fixed reference date known at training time, or compute relative to each row's own timestamp.",
        topic="ml-prep", level=4),
    out("""import pandas as pd
df = pd.DataFrame({"y": [0, 0, 0, 1]})
print(df["y"].value_counts(normalize=True)[1], df["y"].mean())""",
        ["0.25 0.25", "1 0.25", "0.25 1", "0.75 0.25"], 0,
        "For a 0/1 column, the mean IS the share of ones.",
        "Only 1 in 4 labels is positive: 25%. A model that always predicts 0 scores 75% accuracy, so check class balance before trusting accuracy.",
        topic="ml-prep", level=2),
    mcq("You need features for a 50-million-row DataFrame. Which ordering is fastest, from fastest to slowest?",
        ["vectorised column ops  >  list comprehension over zip(...)  >  apply(axis=1)  >  iterrows",
         "iterrows  >  apply(axis=1)  >  vectorised column ops  >  list comprehension",
         "apply(axis=1)  >  vectorised column ops  >  iterrows  >  list comprehension",
         "They are all about the same speed"], 0,
        "Less Python per row = faster.",
        "Vectorised ops run one C loop. A comprehension over zip touches plain Python values. apply(axis=1) and especially iterrows box every row into a Series, adding large per-row overhead.",
        topic="ml-prep", level=3),
    mcq("A colleague's training data has a column `target_mean_by_city` computed with `df.groupby('city')['target'].transform('mean')` on all rows. Validation accuracy is excellent; production accuracy is poor. What happened?",
        ["Target leakage: each row's feature includes its own label (and test labels), so the model learned a shortcut it won't have in production",
         "groupby transform returns values in the wrong order",
         "Mean encoding can't be used with categorical data",
         "The model overfit because the column is float"], 0,
        "The feature was computed from the very thing you're predicting.",
        "Target (mean) encoding must be fitted out-of-fold on training data only, excluding the row itself; otherwise the feature leaks the label. This is a classic reason for 'too good to be true' validation scores.",
        topic="ml-prep", level=4),
    out("""import pandas as pd
import numpy as np
df = pd.DataFrame({"x": [1.0, 2.0, 3.0, 4.0]})
z = (df["x"] - df["x"].mean()) / df["x"].std()
print(round(z.std(), 3), round(((df["x"] - df["x"].mean()) / df["x"].std(ddof=0)).std(ddof=0), 3))""",
        ["1.0 1.0", "0.866 1.0", "1.0 1.155", "1.155 1.0"], 0,
        "Standardising with a given ddof gives std 1 under that same ddof.",
        "pandas std uses ddof=1; scikit-learn's StandardScaler uses ddof=0. Each version gives std 1 under its own definition, but the z-values themselves differ slightly between the two, which matters when reproducing a pipeline.",
        topic="ml-prep", level=4),

    # ------------------------------------------------------------------ concept round-up (mixed topics)
    fill("To count the missing values in every column, write `df.____().sum()`.",
        "isna",
        "'Is it NA?' for every cell.",
        "df.isna() gives True for each missing cell; .sum() counts the Trues per column. isnull is an alias.",
        topic="missing", level=1),
    tf("In pandas, `None` and `np.nan` are both treated as missing by `isna()`, `dropna()` and `fillna()`.", True,
        "pandas has several missing markers but one way to detect them.",
        "isna/dropna/fillna recognise None, np.nan, pd.NaT and pd.NA. In a numeric column None is converted to NaN on creation.",
        topic="missing", level=1),
    mcq("Which statement about `df.fillna(0)` is true?",
        ["It returns a new DataFrame with missing values replaced; df itself is unchanged unless you assign the result",
         "It permanently changes df in place",
         "It deletes rows that contain NaN",
         "It only works on the first column"], 0,
        "Most pandas methods return a new object.",
        "fillna returns a filled copy. Write df = df.fillna(0) (or assign one column: df['a'] = df['a'].fillna(0)).",
        topic="missing", level=1),
    mcq("A 'price' column was read as object dtype. What is the most likely cause?",
        ["Some entries are not plain numbers, e.g. '$12', '1,200', 'N/A' or blanks with spaces",
         "The prices are too large for int64",
         "read_csv always reads money as object",
         "The column has missing values"], 0,
        "A single bad value is enough.",
        "If any value can't be parsed as a number, read_csv keeps the whole column as text. Missing values alone give float64, not object. Find them with pd.to_numeric(s, errors='coerce').isna().",
        topic="types", level=2),
    tf("`pd.to_numeric(s, errors='coerce')` raises an error if any value can't be parsed.", False,
        "What does 'coerce' mean?",
        "coerce turns unparseable values into NaN silently. errors='raise' (the default) is the one that raises.",
        topic="types", level=1),
    mcq("You want every value in a 'name' column trimmed and lower-cased. Which is idiomatic pandas?",
        ['df["name"] = df["name"].str.strip().str.lower()',
         'df["name"] = df["name"].strip().lower()',
         'for i in range(len(df)): df["name"][i] = df["name"][i].strip().lower()',
         'df["name"].str.lower(strip=True)'], 0,
        "Series string methods live under an accessor and can be chained.",
        "The .str accessor applies each method element-wise and skips missing values. The loop version is slow and is also chained assignment.",
        topic="strings", level=1),
    fill("To replace every match of a regular expression in a text column, write `s.str.replace(pattern, '', ____=True)`.",
        "regex",
        "Since pandas 2.0 the default treats the pattern literally.",
        "str.replace(..., regex=True) treats the pattern as a regex; the default regex=False replaces the literal text.",
        topic="strings", level=2),
    mcq("In SQL terms, what is `df.groupby('dept').agg(avg_salary=('salary', 'mean'))`?",
        ["SELECT dept, AVG(salary) AS avg_salary FROM df GROUP BY dept",
         "SELECT AVG(salary) FROM df",
         "SELECT dept, salary FROM df ORDER BY dept",
         "SELECT dept, AVG(salary) OVER (PARTITION BY dept) FROM df"], 0,
        "agg reduces each group to one row.",
        "groupby + agg is GROUP BY with aggregate functions; named aggregation is the AS alias. The window-function version (one value per original row) is transform.",
        topic="groupby", level=1),
    tf("`groupby(...).transform('sum')` returns one row per group.", False,
        "transform keeps the original shape.",
        "transform returns one value per ORIGINAL row (the group's result broadcast back). agg is the one that returns one row per group.",
        topic="groupby-advanced", level=2),
    mcq("What does `df.groupby('g')['v'].nunique()` return?",
        ["The number of distinct v values in each group",
         "The number of rows in each group",
         "The number of groups",
         "The unique v values as a list per group"], 0,
        "n + unique.",
        "nunique counts distinct values per group (SQL COUNT(DISTINCT v)). .unique() would return the arrays of values instead.",
        analogy="SQL: COUNT(DISTINCT v) ... GROUP BY g.",
        topic="groupby", level=2),
    mcq("Which `how` keeps every row from BOTH tables, matched where possible?",
        ['"outer"', '"inner"', '"left"', '"cross"'], 0,
        "FULL OUTER JOIN.",
        "how='outer' keeps all keys from both sides and fills NaN where one side has no match. 'cross' is the Cartesian product.",
        topic="merge", level=1),
    tf("`df1.join(df2)` joins on the index by default, while `pd.merge(df1, df2)` joins on common column names by default.", True,
        "Two APIs, two defaults.",
        "join is index-based (left join by default); merge uses columns with the same name (inner join by default), unless you pass on=/left_on=/left_index= etc.",
        topic="merge", level=2),
    mcq("Before merging a fact table with a dimension (lookup) table, which `validate=` value encodes 'each fact row must match at most one dimension row'?",
        ['"many_to_one"', '"one_to_many"', '"one_to_one"', '"many_to_many"'], 0,
        "Left side is many (facts), right side is one (lookup).",
        "validate='many_to_one' checks that the right-hand keys are unique and raises MergeError otherwise, stopping silent row duplication.",
        topic="merge", level=3),
    mcq("What is the difference between `pd.concat` and `pd.merge`?",
        ["concat stacks or glues frames along an axis by index/column labels; merge matches rows by key values",
         "concat is for strings, merge is for numbers",
         "They are the same function with different names",
         "merge stacks rows, concat joins on keys"], 0,
        "UNION ALL vs JOIN.",
        "concat(axis=0) is like UNION ALL; concat(axis=1) aligns on the index. merge is a SQL JOIN on column values.",
        topic="concat", level=1),
    tf("`pivot` can handle duplicate (index, column) pairs by averaging them.", False,
        "Which of pivot / pivot_table takes an aggfunc?",
        "pivot only reshapes and raises ValueError on duplicates. pivot_table aggregates them (mean by default).",
        topic="reshape", level=2),
    fill("The function that turns wide columns (q1, q2, q3) into long rows (variable, value) is `df.____(id_vars='id')`.",
        "melt",
        "The opposite of pivot.",
        "melt unpivots wide data into long format.",
        topic="reshape", level=1),
    mcq("You want to turn ages into groups 0-18, 18-60, 60+ for a dashboard. Which function fits?",
        ["pd.cut with explicit bin edges", "pd.qcut with 3 quantiles", "df.groupby('age')", "pd.get_dummies('age')"], 0,
        "The edges are fixed by meaning, not by the data's distribution.",
        "cut takes the edges you choose. qcut would choose edges so each group has the same number of people, which wouldn't match 18 and 60.",
        topic="binning", level=1),
    mcq("What is NaT?",
        ["The datetime version of NaN: a missing timestamp",
         "A timezone name",
         "A Timedelta of zero",
         "The first valid date pandas supports"], 0,
        "Not a ...",
        "NaT (Not a Time) marks a missing datetime or timedelta. isna() detects it, and it propagates through arithmetic like NaN.",
        topic="datetime", level=1),
    tf("`df.resample('W')` works on any DataFrame, even one with a plain RangeIndex and no date column.", False,
        "What would it group by?",
        "resample needs a DatetimeIndex (or on='date_col' pointing to a datetime column). Otherwise it raises TypeError.",
        topic="datetime", level=2),
    mcq("For a time-series model (predict tomorrow's sales), how should you split train and test?",
        ["By time: train on earlier dates, test on later dates",
         "Randomly shuffle rows and take 20% as test",
         "Put every weekend in the test set",
         "Use the same rows for train and test"], 0,
        "In production you never know the future.",
        "A random split lets the model train on days after the ones it is tested on, leaking the future. Split chronologically (or use TimeSeriesSplit).",
        topic="ml-prep", level=2),
    tf("For a tree-based model like a random forest, label-encoding a high-cardinality category (one integer per value) can be acceptable, while for linear models one-hot encoding is usually safer.", True,
        "Trees split on thresholds; linear models multiply by a weight.",
        "A linear model would treat code 7 as '7 times' code 1. Trees can carve any integer ranges and are less hurt by arbitrary codes, and one-hot on thousands of values can bloat the feature matrix.",
        topic="ml-prep", level=4),
    mcq("Why does scikit-learn recommend putting imputation and encoding inside a `Pipeline` with cross-validation?",
        ["So each fold fits the imputer/encoder on that fold's training part only, preventing leakage",
         "Pipelines make the model more accurate by default",
         "Because pandas can't do imputation",
         "To avoid converting DataFrames to arrays"], 0,
        "What would happen if you imputed once before cross-validation?",
        "Preprocessing done once on all data leaks validation statistics into every fold. A Pipeline refits the preprocessing inside each training fold.",
        topic="ml-prep", level=3),

    # ================================================================== round 2: depth (L3/L4)
    # ------------------------------------------------------------------ groupby-advanced
    out("import pandas as pd\ndf = pd.DataFrame({\"g\": [\"a\", \"b\", \"a\", \"c\", \"b\"], \"v\": [1, 2, 3, 4, 5]})\nprint(df.groupby(\"g\").filter(lambda d: len(d) > 1).index.tolist())",
        ["[0, 1, 2, 4]", "['a', 'b']", "[0, 2, 1, 4]", "[0, 1]"], 0,
        "filter returns original rows, not one row per group.",
        "filter keeps or drops whole groups, and the surviving rows come back as they were: original index, original order. Groups a (rows 0, 2) and b (rows 1, 4) have more than one row, c (row 3) is dropped. "
        "['a', 'b'] is what an agg-then-filter would give. [0, 2, 1, 4] assumes the rows get regrouped. "
        "It's SQL's HAVING, but returning the detail rows: 'all orders from customers with 2+ orders'.",
        topic="groupby-advanced", level=3,
        analogy="SELECT * FROM orders WHERE cust IN (SELECT cust FROM orders GROUP BY cust HAVING COUNT(*) > 1)."),
    mcq("You want a new column `spread` on every row: that row's group max minus group min. Which line does it?",
        ["df['spread'] = df.groupby('g')['v'].transform(lambda x: x.max() - x.min())",
         "df['spread'] = df.groupby('g')['v'].agg(lambda x: x.max() - x.min())",
         "df['spread'] = df.groupby('g')['v'].max() - df['v'].min()",
         "df['spread'] = df.groupby('g').apply(len)"], 0,
        "The result must have one value per ORIGINAL row.",
        "transform calls the function once per group and broadcasts the scalar result back to every row of that group, keeping df's index, so the assignment lines up. "
        "agg returns one row per group, indexed by group key. Assigning that to df aligns group labels ('a', 'b') against row labels (0, 1, ...) and gives all-NaN. "
        "In SQL terms, transform is MAX(v) OVER (PARTITION BY g) - MIN(v) OVER (PARTITION BY g).",
        code="import pandas as pd\ndf = pd.DataFrame({\"g\": [\"a\", \"b\", \"a\", \"b\"], \"v\": [1, 10, 4, 30]})\ndf[\"spread\"] = df.groupby(\"g\")[\"v\"].transform(lambda x: x.max() - x.min())\nprint(df[\"spread\"].tolist())",
        topic="groupby-advanced", level=3),
    out("import pandas as pd\ndf = pd.DataFrame({\"a\": pd.Categorical([\"x\", \"y\"]), \"b\": pd.Categorical([\"p\", \"q\"]), \"v\": [1, 2]})\nprint(df.groupby([\"a\", \"b\"], observed=False).size().tolist(), df.groupby([\"a\", \"b\"], observed=True).size().tolist())",
        ["[1, 0, 0, 1] [1, 1]", "[1, 1] [1, 1]", "[1, 1] [1, 0, 0, 1]", "[1, 0, 0, 1] [1, 0, 0, 1]"], 0,
        "With observed=False, the result has one row per combination of categories, seen or not.",
        "With categorical keys and observed=False (still the 2.2 default, with a FutureWarning), pandas builds the cartesian product of all categories: 2 x 2 = 4 groups, two of them empty. observed=True keeps only combinations that occur. "
        "With five categorical keys of 100 categories each, observed=False asks for 10^10 groups and can exhaust memory. "
        "Pass observed=True explicitly. pandas 3.0 makes it the default.",
        topic="groupby-advanced", level=4,
        diagram="""a: {x, y}   b: {p, q}
observed=False -> x,p  x,q  y,p  y,q   (all 4)
                   1    0    0    1
observed=True  -> x,p  y,q             (only seen)"""),
    mcq("You want each order's rank within its customer by amount, highest = 1, with ties broken by row order. Which line?",
        ["df.groupby('cust')['amount'].rank(ascending=False, method='first')",
         "df['amount'].rank(ascending=False)",
         "df.groupby('cust')['amount'].agg('rank')",
         "df.sort_values('amount').groupby('cust').cumcount()"], 0,
        "Rank restarts inside each group, and the result must align with the original rows.",
        "groupby(...).rank is a transform-like method: one rank per original row, computed within each customer. ascending=False makes the largest 1, and method='first' breaks ties by order of appearance (the default 'average' gives 1.5). "
        "Plain df['amount'].rank() ranks across all customers. The cumcount version ranks ascending, starting at 0. "
        "SQL equivalent: ROW_NUMBER() OVER (PARTITION BY cust ORDER BY amount DESC).",
        code="import pandas as pd\ndf = pd.DataFrame({\"cust\": [\"a\", \"a\", \"b\", \"a\"], \"amount\": [5, 9, 1, 7]})\nprint(df.groupby(\"cust\")[\"amount\"].rank(ascending=False, method=\"first\").tolist())",
        topic="groupby-advanced", level=3),
    mcq("`clicked` is a bool column. What does `df.groupby('ad')['clicked'].mean()` give you?",
        ["The click-through rate per ad: the share of rows where clicked is True",
         "TypeError, because you can't average booleans",
         "The number of clicks per ad",
         "1.0 for every ad that has at least one click"], 0,
        "True counts as 1 and False as 0.",
        "The mean of a 0/1 column is the proportion of 1s, so this is the CTR (or conversion rate, churn rate...) per group in one line. sum() would give the click count, and mean() divides by the number of rows. "
        "It's the pandas version of AVG(CASE WHEN clicked THEN 1 ELSE 0 END), and a common way to build rate features or check label balance per segment.",
        code="import pandas as pd\ndf = pd.DataFrame({\"ad\": [\"A\", \"A\", \"B\", \"B\", \"B\"], \"clicked\": [True, False, True, True, False]})\nprint(df.groupby(\"ad\")[\"clicked\"].mean().round(2).tolist())",
        topic="groupby-advanced", level=3),
    out("import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({\"g\": [\"a\", \"a\"], \"v\": [np.nan, 2.0]})\nprint(df.groupby(\"g\")[\"v\"].first().tolist(), df.groupby(\"g\")[\"v\"].nth(0).tolist())",
        ["[2.0] [nan]", "[nan] [nan]", "[2.0] [2.0]", "[nan] [2.0]"], 0,
        "One of them skips missing values, the other is purely positional.",
        "groupby().first() returns the first NON-NULL value in each column of the group, so it skips the NaN and gives 2.0. nth(0) returns the literal first row, NaN included. "
        "With several columns, first() can stitch together values from different rows into a row that never existed. "
        "For 'the earliest record per user', sort and use nth(0), head(1) or drop_duplicates(keep='first'), not first().",
        topic="groupby-advanced", level=4),
    tf("`df.groupby('g').last()` returns, for each group, exactly the group's last row, the same values as `df.groupby('g').tail(1)`.", False,
        "Check how last() treats NaN.",
        "last() takes the last non-null value per column, so with v = [1.0, NaN] it returns 1.0, while tail(1) returns the real last row with NaN. With several columns, last() can mix values from different rows. "
        "In an event log that matters: 'the user's latest status' via last() can report a status from an older event because the newest row had a blank.",
        code="import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({\"g\": [\"a\", \"a\"], \"v\": [1.0, np.nan]})\nprint(df.groupby(\"g\")[\"v\"].last().tolist(), df.groupby(\"g\").tail(1)[\"v\"].tolist())",
        topic="groupby-advanced", level=4),
    mcq("Which groupby method returns a result with exactly one row per ORIGINAL row (same index as df), and only allows a function that returns either a scalar per group or a same-length result?",
        ["transform", "agg", "apply", "filter"], 0,
        "Think about the output shape of each method.",
        "agg reduces each group to one row. filter returns a subset of the original rows. apply can return anything (scalar, Series, frame) and pandas guesses how to glue it together. transform is the only one that guarantees the original shape and index, so its output can be assigned straight back as a column. "
        "Picking the method by output shape is the quickest way to answer this in an interview.",
        topic="groupby-advanced", level=4,
        diagram="""df (6 rows, 2 groups)
agg        -> 2 rows    (one per group)
transform  -> 6 rows    (same index as df)
filter     -> <=6 rows  (whole groups kept/dropped)
apply      -> any shape (flexible, slow)"""),
    fill("To group by a categorical column and get only the categories that actually appear (no empty groups), pass `observed=____`.",
        "True",
        "It's a boolean, and pandas 3.0 makes it the default.",
        "observed=True limits the result to category values (or combinations) present in the data. In pandas 2.2 the default is still False for categoricals, which adds empty groups and warns. "
        "Being explicit keeps results identical across versions and avoids the cartesian-product blow-up with several categorical keys.",
        topic="groupby-advanced", level=3),
    # ------------------------------------------------------------------ merge / reshape (round 2)
    out("import pandas as pd\na = pd.DataFrame({\"k\": [1, 1, 1, 2]})\nb = pd.DataFrame({\"k\": [1, 1, 2, 2, 3]})\nprint(len(a.merge(b, on=\"k\")), len(a.merge(b, on=\"k\", how=\"left\")), len(a.merge(b, on=\"k\", how=\"outer\")))",
        ["8 8 9", "4 4 5", "6 6 7", "8 4 9"], 0,
        "For each key, rows = (left count) x (right count).",
        "Key 1: 3 x 2 = 6 rows. Key 2: 1 x 2 = 2. Inner = 8. Every left key has a match, so left is also 8, not 4: a left join keeps all left rows but still multiplies them. Outer adds the unmatched right key 3: 9. "
        "The tempting '4' assumes a left join can't grow the left table. It can whenever the right key is duplicated. "
        "Before any join, check value_counts() of the key on both sides. That's the cardinality check a DBA does before writing the JOIN.",
        topic="merge", level=3,
        diagram="""key   left  right   rows
 1      3  x  2   =  6
 2      1  x  2   =  2
 3      0     1   (outer only) 1
inner/left = 8, outer = 9"""),
    tf("`a.merge(b, on='k')` keeps the row index of `a`, so you can still look up merged rows by their old labels.", False,
        "Check m.index after a merge on columns.",
        "A merge on columns builds a brand-new frame with a fresh RangeIndex 0..n-1. a's labels (say 'r1', 'r2') are gone. Rows can be duplicated or dropped, so there's no single 'old label' to keep. "
        "If you need the original id, keep it as a column (a.reset_index()) before merging, or join on the index explicitly with left_index=True / DataFrame.join.",
        code="import pandas as pd\na = pd.DataFrame({\"k\": [1, 2], \"x\": [5, 6]}, index=[\"r1\", \"r2\"])\nb = pd.DataFrame({\"k\": [2, 1], \"y\": [7, 8]})\nm = a.merge(b, on=\"k\", how=\"left\")\nprint(m.index.tolist(), m[\"y\"].tolist())",
        topic="merge", level=3),
    out("import pandas as pd\na = pd.DataFrame({\"k\": [1, 2]})\nb = pd.DataFrame({\"k\": [2]})\nm = a.merge(b, on=\"k\", how=\"left\", indicator=True)\nprint(m[\"_merge\"].value_counts().to_dict())",
        ["{'left_only': 1, 'both': 1, 'right_only': 0}", "{'left_only': 1, 'both': 1}", "{'both': 1, 'left_only': 1}", "{1: 1, 2: 1}"], 0,
        "What dtype is the _merge column?",
        "_merge is a categorical with three fixed categories: left_only, right_only and both. value_counts on a categorical reports every category, including ones with zero rows, so right_only: 0 shows up even though a left join can't produce it. "
        "It's harmless here, but the same behaviour gives zero-count rows in groupby and value_counts reports on any category column. Filter with m['_merge'] == 'left_only' to find unmatched rows.",
        topic="merge", level=4),
    mcq("Which pandas expression is the equivalent of the SQL anti-join `SELECT * FROM a WHERE NOT EXISTS (SELECT 1 FROM b WHERE b.k = a.k)`?",
        ["a[~a['k'].isin(b['k'])]",
         "a.merge(b, on='k', how='left')",
         "a.merge(b, on='k', how='inner')",
         "a.drop(b.index)"], 0,
        "You want rows of a whose key never appears in b.",
        "isin builds a membership mask and ~ negates it, so you keep a's rows with no partner in b, without duplicating anything. "
        "A plain left join keeps every row of a (and can multiply them). drop(b.index) removes by row label, which has nothing to do with key values. "
        "For multi-column keys, use merge(how='left', indicator=True) and keep _merge == 'left_only'. Use it to find orders with no customer record before training.",
        code="import pandas as pd\na = pd.DataFrame({\"k\": [1, 2, 3]})\nb = pd.DataFrame({\"k\": [2]})\nprint(a[~a[\"k\"].isin(b[\"k\"])][\"k\"].tolist())",
        topic="merge", level=3),
    mcq("You enrich 1M click events with a `user_daily_stats` table (one row per user PER DAY) using `events.merge(stats, on='user_id', how='left')`. Training data grows to 30M rows. What's wrong, and what's the right join?",
        ["The key isn't unique on the right (30 days per user), so each event matches every day; join on (user_id, date), or merge_asof on time so each event gets the latest stats before it",
         "how='left' always multiplies rows; use how='inner'",
         "merge can't handle 1M rows; use concat",
         "Nothing is wrong: more rows mean more training data"], 0,
        "What is the grain of each table?",
        "The stats table's grain is (user, day), but you joined on user only, which is a many-to-many explosion. Each event now also carries stats from days AFTER it happened, so this is leakage as well as duplication. "
        "Join on the full grain (user_id, date) with validate='many_to_one', or use merge_asof(by='user_id', direction='backward') so each event only sees stats computed before its timestamp. "
        "This is the most expensive kind of join bug: the job runs fine and the offline metrics look great.",
        topic="merge", level=4,
        analogy="Joining an orders table to a price-history table on product_id alone: every order picks up every price the product ever had."),
    mcq("What are the columns of `df.pivot_table(index='d', values='v', aggfunc=['sum', 'count'])`?",
        ["A 2-level MultiIndex: ('sum', 'v') and ('count', 'v')",
         "Two plain columns named 'sum' and 'count'",
         "Two plain columns named 'v_sum' and 'v_count'",
         "One column 'v' holding (sum, count) tuples"], 0,
        "A list of aggfuncs adds a level on top of the value names.",
        "With a list of functions, pandas puts the function name on the outer column level and the value column underneath, giving MultiIndex columns. Most downstream tools (CSV, scikit-learn, parquet with some engines) want flat names. "
        "Flatten with p.columns = ['_'.join(c) for c in p.columns] to get 'sum_v', 'count_v'. Or use groupby().agg(v_sum=('v', 'sum'), ...) named aggregation, which gives flat names directly.",
        code="import pandas as pd\ndf = pd.DataFrame({\"d\": [\"x\", \"x\", \"y\"], \"v\": [1, 2, 3]})\np = df.pivot_table(index=\"d\", values=\"v\", aggfunc=[\"sum\", \"count\"])\nprint(p.columns.tolist())",
        topic="reshape", level=3),
    out("import pandas as pd\na = pd.Series([\"M\", \"M\", \"F\", \"F\", \"F\"], name=\"sex\")\nb = pd.Series([\"y\", \"n\", \"y\", \"y\", \"n\"], name=\"smoker\")\nprint(pd.crosstab(a, b, normalize=\"index\").round(2).values.tolist())",
        ["[[0.33, 0.67], [0.5, 0.5]]", "[[0.5, 0.5], [0.33, 0.67]]", "[[0.2, 0.4], [0.2, 0.2]]", "[[0.5, 0.67], [0.5, 0.33]]"], 0,
        "Rows and columns are sorted (F before M, n before y); normalize='index' makes each row sum to 1.",
        "Row F has n=1 and y=2 out of 3, so [0.33, 0.67]. Row M has n=1 and y=1, so [0.5, 0.5]. normalize='index' gives conditional rates P(smoker | sex). The third option is normalize='all' (share of the grand total), a different question. "
        "Rates per segment are what you compare when checking whether a feature separates the target. Raw counts mislead when groups have different sizes.",
        topic="reshape", level=3),
    tf("`pivot_table` (like `groupby`) silently drops rows whose index key is NaN.", True,
        "pivot_table is built on groupby.",
        "pivot_table groups by its index/columns keys and inherits groupby's default of dropping NaN keys, so the NaN row's values vanish from every cell and from the totals (margins=True). "
        "Totals that don't match df['v'].sum() are the symptom. Fill the key first (df['d'].fillna('unknown')) if missing categories should be reported.",
        code="import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({\"d\": [\"x\", np.nan, \"y\"], \"c\": [\"m\", \"m\", \"m\"], \"v\": [1, 2, 3]})\nprint(df.pivot_table(index=\"d\", columns=\"c\", values=\"v\", aggfunc=\"sum\")[\"m\"].tolist())",
        topic="reshape", level=4),
    out("import pandas as pd\nimport numpy as np\nw = pd.DataFrame({\"m\": [1.0, np.nan], \"n\": [3.0, 4.0]}, index=[\"x\", \"y\"])\nprint(len(w.stack()), len(w.stack(future_stack=True)))",
        ["3 4", "4 4", "3 3", "4 3"], 0,
        "The legacy stack has a dropna default; the new implementation doesn't.",
        "In pandas 2.2 the legacy stack() drops cells that are NaN (here ('y', 'm')), giving 3 values. future_stack=True opts into the pandas 3.0 behaviour, which keeps every cell, NaN included: 4. "
        "If you reshape wide to long and then count observations per id, the legacy version quietly loses rows, and the count changes when you upgrade. Pass future_stack=True and drop NaN explicitly when you mean it.",
        topic="reshape", level=4),
    fill("To add a `_merge` column that says whether each row came from the left table, the right table or both, call `a.merge(b, on='k', how='outer', ____=True)`.",
        "indicator",
        "It indicates where each row came from.",
        "indicator=True adds a categorical _merge column with values left_only, right_only and both. value_counts() on it is a one-line join audit, and filtering on 'left_only' gives an anti-join. "
        "Run it after every important merge in a data pipeline, the way you'd check row counts after a SQL JOIN.",
        topic="merge", level=3),
    # ------------------------------------------------------------------ windows
    out("import pandas as pd\ns = pd.Series([2, 4, 6, 8])\nprint(s.rolling(3, min_periods=1).mean().tolist())",
        ["[2.0, 3.0, 4.0, 6.0]", "[nan, nan, 4.0, 6.0]", "[2.0, 3.0, 4.0, 5.0]", "[4.0, 6.0]"], 0,
        "min_periods=1 lets the window produce a value as soon as it has one observation.",
        "rolling(3) normally needs 3 values, so the first two outputs are NaN. With min_periods=1 the early windows use what they have: [2] gives 2, [2, 4] gives 3, then [2, 4, 6] gives 4 and [4, 6, 8] gives 6. "
        "[2.0, 3.0, 4.0, 5.0] is the expanding mean, which never forgets old values. "
        "Be aware that the first rows' features are computed from fewer points and are noisier. Some teams add a 'window_count' feature so the model knows.",
        topic="windows", level=3),
    fill("To compute a running mean over ALL rows so far (a window that only grows), call `s.____().mean()`.",
        "expanding",
        "The window expands instead of rolling.",
        "expanding() includes every row from the start up to the current one, so s.expanding().mean() is the cumulative average: [2, 4, 6, 8] gives [2.0, 3.0, 4.0, 5.0]. cumsum/cummax are special cases. "
        "In SQL that's AVG(x) OVER (ORDER BY t ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW).",
        code="import pandas as pd\ns = pd.Series([2, 4, 6, 8])\nprint(s.expanding().mean().tolist(), s.cummax().tolist())",
        topic="windows", level=3),
    out("import pandas as pd\nidx = pd.to_datetime([\"2024-01-01\", \"2024-01-02\", \"2024-01-05\", \"2024-01-06\"])\ns = pd.Series([1, 2, 3, 4], index=idx)\nprint(s.rolling(\"2D\").sum().tolist(), s.rolling(2).sum().tolist())",
        ["[1.0, 3.0, 3.0, 7.0] [nan, 3.0, 5.0, 7.0]", "[nan, 3.0, 5.0, 7.0] [nan, 3.0, 5.0, 7.0]", "[1.0, 3.0, 5.0, 7.0] [nan, 3.0, 5.0, 7.0]", "[1.0, 3.0, 3.0, 7.0] [1.0, 3.0, 3.0, 7.0]"], 0,
        "'2D' means 'the last 2 days of time', not 'the last 2 rows'.",
        "A time-based window looks back over (t - 2 days, t]. On 5 Jan the previous row is 3 days old, so only 3 itself is in the window. The row-count window rolling(2) blindly pairs 5 Jan with 2 Jan and gives 5. Time windows also default to min_periods=1, so the first value is 1.0, not NaN. "
        "For irregular event data (sessions, transactions), time windows are what you mean by 'spend in the last 7 days'. Row windows quietly reach back months for inactive users.",
        topic="windows", level=4,
        diagram="""date : 01   02   .    .   05   06
value: 1    2              3    4
'2D' : 1   1+2            3   3+4   <- by time
 2   : nan 1+2           2+3  3+4   <- by rows"""),
    out("import pandas as pd\ns = pd.Series([0.0, 10.0, 10.0])\nprint(s.ewm(alpha=0.5, adjust=False).mean().tolist())",
        ["[0.0, 5.0, 7.5]", "[0.0, 6.667, 8.571]", "[0.0, 10.0, 10.0]", "[nan, 5.0, 7.5]"], 0,
        "With adjust=False: y_t = alpha * x_t + (1 - alpha) * y_(t-1).",
        "The recursive form starts at y0 = 0. Then y1 = 0.5*10 + 0.5*0 = 5, and y2 = 0.5*10 + 0.5*5 = 7.5. Recent values weigh more, and old ones fade geometrically without ever fully dropping out. "
        "[0.0, 6.667, 8.571] is the default adjust=True result, which normalises the weights over the finite history. "
        "EWMs are popular trend features because they react faster than a long rolling mean and need no window length.",
        topic="windows", level=3),
    mcq("`s = [0, 10, 10]`. Why does `s.ewm(alpha=0.5).mean()` (default `adjust=True`) give [0.0, 6.667, 8.571] instead of the recursive [0.0, 5.0, 7.5]?",
        ["adjust=True divides by the sum of the weights actually used (1, 0.5, 0.25, ...), so the start isn't dragged towards the first value",
         "adjust=True ignores the first value",
         "adjust=True uses alpha = 2/(span+1) instead of 0.5",
         "The defaults add a bias correction of 1/(1 - alpha)"], 0,
        "Write y_1 as a weighted average of x_1 and x_0 with weights 1 and 0.5.",
        "With adjust=True, y_t = sum(w_i * x_(t-i)) / sum(w_i) with w_i = (1 - alpha)^i. y1 = (1*10 + 0.5*0) / 1.5 = 6.667, and y2 = (10 + 5 + 0) / 1.75 = 8.571. The recursive form instead treats y0 = x0 as if it summarised an infinite past, which biases early values towards x0. "
        "The two converge after a few dozen steps. Make sure training and serving use the SAME setting, or the features will drift for new users with short histories.",
        code="import pandas as pd\ns = pd.Series([0.0, 10.0, 10.0])\nprint(s.ewm(alpha=0.5).mean().round(3).tolist())",
        topic="windows", level=4),
    mcq("A teammate builds a feature with `df['smooth'] = df['sales'].rolling(7, center=True).mean()` for a model that forecasts tomorrow's sales. What's the problem?",
        ["center=True uses the 3 days AFTER each row, so the feature contains future information that won't exist at prediction time",
         "center=True is slower than the default",
         "center=True needs an odd window, and 7 is odd, so nothing is wrong",
         "It drops the first 7 rows"], 0,
        "Where does a centred window reach?",
        "A centred 7-row window spans t-3..t+3. It's fine for plotting a smoothed history, but as a feature each row sees its own future, so offline accuracy looks great and production accuracy collapses. "
        "For features, use trailing windows that end before the prediction point: df['sales'].shift(1).rolling(7).mean().",
        code="import pandas as pd\ns = pd.Series([1, 2, 3, 4, 5])\nprint(s.rolling(3, center=True).mean().tolist())",
        topic="windows", level=3),
    tf("A time-based window like `s.rolling('3D')` raises ValueError if the DatetimeIndex is not sorted.", True,
        "A time window needs to know which rows are 'the last 3 days'.",
        "Time windows walk forward through the index and need it to be monotonic, so pandas raises ValueError: index values must be monotonic. Row-count windows don't check, and on unsorted data they silently compute nonsense. "
        "Always sort_index() (or sort_values('ts')) before any window or shift feature. Data from parallel jobs or UNION queries is rarely in time order.",
        code="import pandas as pd\nidx = pd.to_datetime([\"2024-01-02\", \"2024-01-01\", \"2024-01-03\"])\ns = pd.Series([1, 2, 3], index=idx)\nprint(s.sort_index().rolling(\"3D\").sum().tolist())",
        topic="windows", level=3),
    out("import pandas as pd\nimport numpy as np\ns = pd.Series([1, np.nan, 3, 4])\nprint(s.rolling(2).sum().tolist(), s.rolling(2, min_periods=1).sum().tolist())",
        ["[nan, nan, nan, 7.0] [1.0, 1.0, 3.0, 7.0]", "[nan, 1.0, 3.0, 7.0] [1.0, 1.0, 3.0, 7.0]", "[nan, nan, nan, 7.0] [nan, nan, nan, 7.0]", "[1.0, 1.0, 3.0, 7.0] [1.0, 1.0, 3.0, 7.0]"], 0,
        "min_periods counts non-NaN observations, not rows.",
        "With the default min_periods equal to the window (2), a window holding a NaN has only 1 valid value and returns NaN. A single NaN therefore wipes out two outputs (positions 1 and 2). With min_periods=1 the NaN is skipped: [1], [1, NaN] gives 1, [NaN, 3] gives 3, [3, 4] gives 7. "
        "Sensor gaps can spread NaN through a rolling feature this way, so decide on min_periods deliberately and log the share of NaN features.",
        topic="windows", level=4),
    mcq("A daily sales Series has missing days (no rows when the store was closed). What is the difference between `rolling(7)` and `rolling('7D')`?",
        ["rolling(7) uses the last 7 ROWS, which can span weeks across gaps; rolling('7D') uses the last 7 calendar days, however many rows that is",
         "They are identical for daily data",
         "rolling('7D') needs exactly 7 rows in every window",
         "rolling(7) is time-aware when the index is a DatetimeIndex"], 0,
        "One counts rows, the other measures time.",
        "Integer windows count observations and know nothing about time. If the store was closed for a week, rolling(7) averages over two weeks of real time. Offset strings like '7D' define the window by timestamp, so the window size varies with the data density. "
        "Pick the one that matches the business definition ('last 7 trading days' vs 'last 7 days'), and remember that '7D' windows need a sorted DatetimeIndex (or on='ts').",
        topic="windows", level=3,
        analogy="ROWS BETWEEN 6 PRECEDING AND CURRENT ROW vs RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW in SQL."),
    # ------------------------------------------------------------------ ml-features
    out("import pandas as pd\ndf = pd.DataFrame({\"user\": [\"A\", \"A\", \"B\", \"B\"], \"amt\": [10, 20, 30, 40]})\nprint(df[\"amt\"].shift(1).tolist(), df.groupby(\"user\")[\"amt\"].shift(1).tolist())",
        ["[nan, 10.0, 20.0, 30.0] [nan, 10.0, nan, 30.0]", "[nan, 10.0, 20.0, 30.0] [nan, 10.0, 20.0, 30.0]", "[nan, 10.0, nan, 30.0] [nan, 10.0, nan, 30.0]", "[10.0, 20.0, 30.0, nan] [10.0, nan, 30.0, nan]"], 0,
        "Where does user B's first 'previous amount' come from in each version?",
        "A plain shift(1) on a stacked table lets user B's first row inherit user A's last amount (20), which mixes one customer's history into another's features. groupby('user').shift(1) restarts at each user, so B's first lag is NaN. "
        "This is the classic lag-feature bug. It doesn't crash, it just makes the model a little worse in a way that's hard to find.",
        topic="ml-features", level=3,
        analogy="LAG(amt) OVER (ORDER BY ...) vs LAG(amt) OVER (PARTITION BY user ORDER BY ...) in SQL.",
        diagram="""user amt  shift(1)  groupby.shift(1)
A    10    nan        nan
A    20    10         10
B    30    20 <- A!   nan
B    40    30         30"""),
    out("import pandas as pd\ndf = pd.DataFrame({\"u\": [\"A\", \"A\", \"A\", \"B\", \"B\"], \"y\": [1, 3, 5, 10, 20]})\nf = df.groupby(\"u\")[\"y\"].transform(lambda s: s.shift(1).rolling(2, min_periods=1).mean())\nprint(f.tolist())",
        ["[nan, 1.0, 2.0, nan, 10.0]", "[1.0, 2.0, 4.0, 10.0, 15.0]", "[nan, 2.0, 4.0, nan, 15.0]", "[nan, 1.0, 2.0, 5.0, 10.0]"], 0,
        "Shift first (exclude today), then roll, and do both inside each user.",
        "For A: the shifted values are [nan, 1, 3], and a 2-window mean with min_periods=1 gives [nan, 1, 2]. For B: [nan, 10] gives [nan, 10]. Each row only sees that user's strictly earlier targets. "
        "[1.0, 2.0, 4.0, ...] is the leaky version without shift: every row's feature includes its own label. [.., 5.0, ..] lets A's history bleed into B. "
        "This 'groupby, shift, then roll' recipe is the standard leak-free 'average of last k outcomes' feature.",
        topic="ml-features", level=4),
    out("import pandas as pd\ndf = pd.DataFrame({\"u\": [\"A\", \"A\", \"A\"], \"day\": [3, 1, 2], \"y\": [30, 10, 20]})\nprint(df.groupby(\"u\")[\"y\"].shift(1).tolist(), df.sort_values(\"day\").groupby(\"u\")[\"y\"].shift(1).tolist())",
        ["[nan, 30.0, 10.0] [nan, 10.0, 20.0]", "[nan, 10.0, 20.0] [nan, 10.0, 20.0]", "[20.0, nan, 10.0] [nan, 10.0, 20.0]", "[nan, 30.0, 10.0] [nan, 30.0, 10.0]"], 0,
        "shift works on row order, not on the day column.",
        "groupby().shift(1) takes 'the previous row in the group', whatever order the rows are in. Unsorted, day 1 gets day 3's value (30) as its 'previous' value, so the past is filled from the future. After sort_values('day') the lags are correct: [nan, 10, 20] in day order. "
        "Sort by (entity, time) before every lag, diff, cumsum or rolling feature, and assert df['day'].is_monotonic_increasing inside each group if you can.",
        topic="ml-features", level=4),
    mcq("For target-encoding `city`, you replace each row's value with the mean target of the OTHER rows in its city (leave-one-out). For city P with targets [1, 0, 1], what are the encodings?",
        ["[0.5, 1.0, 0.5]: each row averages the other two",
         "[0.67, 0.67, 0.67]: the plain city mean",
         "[1.0, 0.0, 1.0]: each row's own target",
         "[0.5, 0.5, 0.5]"], 0,
        "Row 1 excludes itself: (0 + 1) / 2.",
        "Leave-one-out = (group sum - own y) / (group count - 1). Rows with y=1 get (2 - 1)/2 = 0.5, and the row with y=0 gets (2 - 0)/2 = 1.0. The plain mean 0.67 includes each row's own label, which is direct target leakage, and it's strongest for small categories. "
        "LOO itself can still leak, because the encoding is anti-correlated with the row's own label (y=1 rows get lower values), and flexible models exploit that. K-fold (out-of-fold) encoding plus smoothing towards the global mean is the safer default.",
        code="import pandas as pd\ndf = pd.DataFrame({\"city\": [\"P\", \"P\", \"P\", \"G\", \"G\"], \"y\": [1, 0, 1, 1, 1]})\ng = df.groupby(\"city\")[\"y\"]\nloo = (g.transform(\"sum\") - df[\"y\"]) / (g.transform(\"count\") - 1)\nprint(loo.round(2).tolist())",
        topic="ml-features", level=4),
    mcq("Your features use 30-day trailing windows and the label is 'did the user churn in the NEXT 30 days'. You split by time at 1 June. Why do careful teams leave a 30-day gap between the last training label and the first test row?",
        ["Training labels for late-May rows look into June, the test period, so without a gap train and test overlap in time",
         "To make the test set smaller",
         "Because rolling windows need 30 NaN rows to warm up",
         "A gap is only needed for random splits"], 0,
        "Over which dates is the label of a 31-May row computed?",
        "A 31-May row's label is built from 1-30 June, the same days the test rows are evaluated on. A time split alone still leaks the near future through the labels. Leaving a gap the size of the label horizon ('purging' or 'embargo') removes that overlap. "
        "In scikit-learn, TimeSeriesSplit(gap=...) does this. Without it, offline metrics can look better than what you'll see in production.",
        topic="ml-features", level=4,
        diagram="""train rows ....... May31 | gap 30d | test rows June...
May31 label window: [Jun1 ---- Jun30]
                     ^ overlaps test without the gap"""),
    mcq("At serving time a request has city 'z', which training never saw. You encode with `pd.get_dummies(pd.Categorical(req['city'], categories=train_cats))`. What does the encoded row look like?",
        ["All dummy columns are 0: the unseen value becomes NaN and gets no column, while the columns still match training",
         "A new column city_z is added",
         "It raises KeyError",
         "The row is dropped"], 0,
        "The categories list is fixed. What happens to a value outside it?",
        "pd.Categorical with explicit categories turns unknown values into NaN (code -1). get_dummies then emits exactly one column per training category, and the unseen row is all zeros. The schema stays identical to training, which is what the model needs. "
        "That's the pandas equivalent of OneHotEncoder(handle_unknown='ignore'). Save train_cats with the model and use them at both training and serving time.",
        code="import pandas as pd\ncats = [\"a\", \"b\", \"c\"]\nreq = pd.Series(pd.Categorical([\"b\", \"z\"], categories=cats))\nd = pd.get_dummies(req)\nprint(d.columns.tolist(), d.sum(axis=1).tolist())",
        topic="ml-features", level=3),
    mcq("What's wrong with `df['avg3'] = df.groupby('store')['sales'].transform(lambda s: s.rolling(3).mean())` as a feature for predicting `sales`?",
        ["Each row's window includes that row's own sales, the label, so the feature leaks the target; shift(1) before rolling",
         "transform can't be used with rolling",
         "rolling(3) across stores mixes their data",
         "Nothing; it's the standard approach"], 0,
        "Does the window end before or at the current row?",
        "Trailing windows include the current row by default, so 'average of the last 3 days' contains today's sales, the very value you're predicting. The model learns to read the answer off the feature. "
        "The fix is s.shift(1).rolling(3).mean() inside the group. Rolling across stores isn't the problem here, since groupby already separates them. "
        "A feature that correlates suspiciously well with the label is the usual sign of this bug.",
        topic="ml-features", level=3),
    tf("Out-of-fold target encoding (each fold's rows are encoded with category means computed on the OTHER folds) stops a row's own label from leaking into its feature.", True,
        "Is the row's own target ever part of the statistic it receives?",
        "With K-fold encoding, the statistic for a row comes only from rows in other folds, so its own label never enters its feature. That's what makes it safe to train on. At test time you encode with means from the full training set. "
        "Adding smoothing (blending with the global mean, weighted by category size) protects rare categories, whose means are mostly noise.",
        topic="ml-features", level=4,
        analogy="Like grading each student's essay with a rubric calibrated on the other classes' essays, never on their own."),
    fill("To make a rolling feature use only PAST rows (excluding the current one), write `s.____(1).rolling(3).mean()`.",
        "shift",
        "Move the data down one row first.",
        "shift(1) moves every value down a row, so the window ending at row t only contains t-1, t-2 and t-3. Without it, the current row (often the label) is inside its own feature. "
        "In SQL it's ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING instead of ... AND CURRENT ROW.",
        topic="ml-features", level=3),
    # ------------------------------------------------------------------ datetime / missing / duplicates (round 2)
    out("import pandas as pd\nidx = pd.date_range(\"2024-03-30\", periods=3, freq=\"D\", tz=\"Europe/Berlin\")\nprint(idx[2] - idx[0], (idx[2] - idx[0]) / pd.Timedelta(hours=1))",
        ["1 days 23:00:00 47.0", "2 days 00:00:00 48.0", "2 days 01:00:00 49.0", "TypeError"], 0,
        "Europe switches to summer time on the last Sunday of March.",
        "freq='D' on a tz-aware range means 'same wall-clock time each calendar day'. On 31 March 2024 Berlin clocks jumped from 02:00 to 03:00, so that day has only 23 hours, and the elapsed time from 30 March to 1 April midnight is 47 hours. "
        "A feature like 'hours since signup' or a model of hourly load is off by one around every DST change if you mix calendar and absolute time. Store timestamps in UTC, and convert to local time only for calendar features (hour of day, weekday).",
        topic="datetime", level=4,
        analogy="The same rule backend teams use: store UTC in the database and localise only in the UI."),
    mcq("You parse `['2024-01-01 10:00+05:30', '2024-01-01 10:00+00:00']` with `pd.to_datetime(...)` in pandas 2.2 and get an object Index, not a DatetimeIndex. Why, and what's the fix?",
        ["A single datetime64 column can hold only one timezone, so mixed offsets fall back to objects (with a FutureWarning); pass utc=True to convert both to UTC",
         "The strings are invalid; add errors='coerce'",
         "to_datetime only accepts dates without times",
         "You must call tz_localize first"], 0,
        "What dtype would hold +05:30 and +00:00 at the same time?",
        "datetime64[ns, tz] has one timezone per column. With two different fixed offsets pandas 2.2 can't pick one, so it returns plain Python datetime objects in an object Index and warns. pandas 3 raises instead. "
        "utc=True converts each value to the same instant in UTC (04:30 and 10:00 here), giving a proper DatetimeIndex you can sort, resample and subtract. "
        "Logs collected from servers in different regions hit this constantly.",
        code="import pandas as pd\nt = pd.to_datetime([\"2024-01-01 10:00+05:30\", \"2024-01-01 10:00+00:00\"], utc=True)\nprint(type(t).__name__, t.hour.tolist())",
        topic="datetime", level=4),
    out("import pandas as pd\ns = pd.Series(range(10), index=pd.date_range(\"2024-01-01\", periods=10, freq=\"D\"))\nr = s.resample(\"W\").sum()\nprint(str(r.index[0].date()), r.tolist())",
        ["2024-01-07 [21, 24]", "2024-01-01 [21, 24]", "2024-01-07 [28, 17]", "2024-01-01 [0, 45]"], 0,
        "'W' is an alias for 'W-SUN'. Which edge labels a weekly bin?",
        "Weekly bins end on Sunday and are labelled by that end date. 1 Jan 2024 was a Monday, so the first bin covers 1-7 Jan (0+...+6 = 21) and is labelled 2024-01-07. 8-10 Jan sum to 24. "
        "If you join these weekly aggregates back to daily rows by the label date, every day lines up with the FOLLOWING Sunday's total, which includes days after it. Use 'W-MON' with label='left', or be explicit about the edge.",
        topic="datetime", level=3),
    out("import pandas as pd\ns = pd.Series([1, 2, 3, 4], index=pd.date_range(\"2024-01-01 00:00\", periods=4, freq=\"30min\"))\nprint(s.resample(\"h\").mean().tolist(), s.resample(\"h\", closed=\"right\", label=\"right\").mean().tolist())",
        ["[1.5, 3.5] [1.0, 2.5, 4.0]", "[1.5, 3.5] [1.5, 3.5]", "[1.0, 2.5, 4.0] [1.5, 3.5]", "[1.5, 3.5] [2.5, 4.0]"], 0,
        "Default hourly bins are [00:00, 01:00): left-closed, left-labelled.",
        "Default: [00:00, 01:00) holds 1 and 2 (mean 1.5), and [01:00, 02:00) holds 3 and 4 (mean 3.5). With closed='right' the bins become (23:00, 00:00], (00:00, 01:00] and (01:00, 02:00], holding [1], [2, 3] and [4]: three bins with means 1.0, 2.5 and 4.0. "
        "Data vendors disagree on this (a bar labelled 10:00 can mean 09:00-10:00 or 10:00-11:00). Getting it wrong shifts every feature by one bucket, which is a subtle leak.",
        topic="datetime", level=4),
    out("import pandas as pd\ns = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 100])\nlo, hi = s.quantile(0.1), s.quantile(0.9)\nprint(round(lo, 2), round(hi, 2), round(s.clip(lo, hi).max(), 2))",
        ["1.9 18.1 18.1", "1 9 9", "1.0 100.0 100.0", "2 9 9"], 0,
        "quantile interpolates linearly between sorted values by default.",
        "With 10 values, the 0.1 quantile sits at position 0.9 between 1 and 2, giving 1.9. The 0.9 quantile sits at position 8.1 between 9 and 100, giving 9 + 0.1*91 = 18.1. clip caps the 100 at 18.1. "
        "Note how far one outlier pulls the upper cap. Winsorising by quantiles is common, but on small groups the cap can be far from 'typical' data. Compute the caps on the training split and reuse them on test.",
        topic="missing", level=3),
    mcq("You cap outliers with `s.clip(s.quantile(0.01), s.quantile(0.99))` on the whole dataset, then split into train and test. What's the issue?",
        ["The caps are statistics of the test rows too, so test information leaks into training; fit the caps on train and apply the same numbers to test and serving",
         "clip can't take quantiles",
         "It removes outlier rows, shrinking the dataset",
         "There is no issue, because clipping isn't learning"], 0,
        "Is a quantile something learned from data?",
        "Any number computed from data (mean, std, quantile caps, bin edges) is a fitted parameter. Computing it on all rows lets the test distribution shape the training features. The leak is small on big i.i.d. data, but it's still wrong and can be large for time series, where the future's extremes set today's caps. "
        "Treat caps like a scaler: fit on train, save lo/hi, and apply them unchanged at serving time.",
        topic="ml-prep", level=4,
        analogy="Like setting an API's rate-limit thresholds from last month's traffic, not from the traffic you're about to test against."),
    tf("`s.value_counts(normalize=True)` divides by the number of non-missing values, so with `dropna=False` the same categories get smaller shares.", True,
        "What's the denominator when NaN is excluded?",
        "On ['a', 'a', None, 'b'] the default excludes the None: a = 2/3 and b = 1/3. With dropna=False, NaN becomes its own row and the denominator becomes 4: a = 0.5, NaN = 0.25, b = 0.25. "
        "Class-balance or 'percentage of users per plan' reports can differ just because of this flag. State which denominator you used.",
        code="import pandas as pd\ns = pd.Series([\"a\", \"a\", None, \"b\"])\nprint(s.value_counts(normalize=True).round(2).tolist(), s.value_counts(normalize=True, dropna=False).round(2).tolist())",
        topic="duplicates", level=3),
    mcq("A sensor table stacks several devices. Missing readings are filled with `df['v'].ffill()`. Why is `df.groupby('device')['v'].ffill()` usually what you want?",
        ["A plain ffill carries device A's last reading into device B's first missing rows; groupby restarts the fill at each device",
         "groupby().ffill() is faster but gives the same result",
         "A plain ffill also fills backwards",
         "groupby().ffill() fills with the group mean"], 0,
        "Picture device B's first reading missing, right after device A's rows.",
        "ffill copies the previous ROW's value, whatever entity it belongs to. On a stacked table that leaks one device's (or user's, or patient's) data into another's. groupby('device').ffill() keeps fills within each device, and a device whose first reading is missing stays NaN, which is honest. "
        "Sort by (device, time) first, and consider limit= so a device that went offline for a week isn't 'filled' with stale values.",
        code="import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({\"device\": [\"A\", \"A\", \"B\", \"B\"], \"v\": [1.0, np.nan, np.nan, 4.0]})\nprint(df[\"v\"].ffill().tolist(), df.groupby(\"device\")[\"v\"].ffill().tolist())",
        topic="missing", level=3),
]
