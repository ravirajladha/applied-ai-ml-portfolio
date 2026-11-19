from helpers import mcq, tf, out, fill

SUBJECT = "pd-dataframes"

TOPICS = [
    ("series-vs-df", "Series vs DataFrame"),
    ("creating", "Creating DataFrames"),
    ("inspecting", "Inspecting: head, info, describe, shape, dtypes"),
    ("selecting", "Selecting columns"),
    ("loc-iloc", "loc vs iloc"),
    ("filtering", "Boolean filtering and query()"),
    ("modifying", "Adding, renaming, dropping and sorting"),
    ("apply-vectorise", "apply / map vs vectorised operations"),
    ("index-alignment", "The index and alignment in arithmetic"),
    ("copy-view", "Copies, views, SettingWithCopyWarning and copy-on-write"),
    ("dtypes-memory", "dtypes and memory"),
    ("multiindex", "MultiIndex basics"),
    ("ml-features", "DataFrames as model inputs (X, y and feature columns)"),
]

QUESTIONS = [
    # ------------------------------------------------------------------ series-vs-df
    mcq("In pandas, what is a Series?",
        ["A single labelled column of values (values + an index)",
         "A whole table with rows and columns",
         "A Python list with extra methods but no labels",
         "A database connection to a CSV file"], 0,
        "Think of one column of a spreadsheet, together with its row labels.",
        "A Series is one-dimensional: an array of values plus an index (the row labels). A DataFrame is a table made of several Series that share the same index.",
        diagram="""
Series "age"          DataFrame
index  value          index  name  age
  0     30              0    Ann   30
  1     25              1    Bob   25
(labels) (data)         (shared index, many columns)""",
        analogy="A Series is one column in an Excel sheet; a DataFrame is the whole sheet.",
        topic="series-vs-df", level=1),
    out("""import pandas as pd
df = pd.DataFrame({"name": ["Ann", "Bob"], "age": [30, 25]})
print(type(df).__name__, type(df["age"]).__name__)""",
        ["DataFrame Series", "DataFrame DataFrame", "DataFrame list", "Series Series"], 0,
        "One pair of square brackets with one column name gives you a single column.",
        "df is a DataFrame; df[\"age\"] picks one column, which is a Series.",
        topic="series-vs-df", level=1),
    tf("Every column of a DataFrame shares the same index (row labels).", True,
        "How else would row 3 of one column line up with row 3 of another?",
        "A DataFrame is a dict of Series that all share one index. That shared index is what keeps each row's values together.",
        topic="series-vs-df", level=1),
    out("""import pandas as pd
s = pd.Series([10, 20, 30], index=["a", "b", "c"])
print(s["b"], s.index.tolist())""",
        ["20 ['a', 'b', 'c']", "10 ['a', 'b', 'c']", "20 [0, 1, 2]", "KeyError"], 0,
        "With a custom index, s[\"b\"] looks up the label \"b\".",
        "The index holds the labels a, b, c. s[\"b\"] returns the value stored under label b, which is 20.",
        topic="series-vs-df", level=1),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1, 2], "b": [3.5, 4.5]})
row = df.iloc[0]
print(type(row).__name__, row.dtype)""",
        ["Series float64", "DataFrame int64", "Series int64", "Series object"], 0,
        "One row must hold both an int and a float in a single 1-D container.",
        "A single row comes back as a Series. Its values must share one dtype, so int 1 is upcast to float64 to live next to 3.5.",
        topic="series-vs-df", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1, 2], "c": ["x", "y"]})
print(df.iloc[0].dtype)""",
        ["object", "int64", "string", "mixed"], 0,
        "A Series has exactly one dtype. What can hold both 1 and 'x'?",
        "The row holds an int and a str, so pandas falls back to object dtype (generic Python objects). Row access on mixed tables silently loses the column dtypes.",
        topic="series-vs-df", level=3),
    mcq("You run `s = df['price']` and then `s.to_frame()`. What is the result?",
        ["A one-column DataFrame whose column is named 'price'",
         "A Series with the same values",
         "A list of prices",
         "A DataFrame with the prices as its column names"], 0,
        "to_frame turns 1-D into 2-D.",
        "Series.to_frame() wraps the Series into a DataFrame with one column; the column name is the Series name ('price').",
        topic="series-vs-df", level=2),

    # ------------------------------------------------------------------ creating
    mcq("Which call builds a DataFrame with columns `name` and `age`?",
        ['pd.DataFrame({"name": ["Ann", "Bob"], "age": [30, 25]})',
         'pd.DataFrame(["name", "age"], ["Ann", "Bob"], [30, 25])',
         'pd.Series({"name": ["Ann", "Bob"], "age": [30, 25]})',
         'pd.DataFrame.columns("name", "age")'], 0,
        "A dict maps column name -> list of values.",
        "Passing a dict gives one column per key; each list becomes that column's values. This is the most common way to build a small DataFrame.",
        analogy="Like a JSON object where each key holds an array: {\"name\": [...], \"age\": [...]}.",
        topic="creating", level=1),
    out("""import pandas as pd
rows = [{"name": "Ann", "age": 30}, {"name": "Bob", "age": 25}]
df = pd.DataFrame(rows)
print(df.shape)""",
        ["(2, 2)", "(2,)", "(1, 2)", "(4,)"], 0,
        "A list of dicts: each dict is one row.",
        "A list of records (like rows from a JSON API) gives one row per dict and one column per key: 2 rows x 2 columns.",
        analogy="Exactly the shape of `res.json()` from a REST API returning an array of objects.",
        topic="creating", level=1),
    out("""import pandas as pd
df = pd.DataFrame({"name": ["Ann", "Bob", "Cy"], "age": [30, 25, 35]})
print(df)""",
        ["  name  age\n0  Ann   30\n1  Bob   25\n2   Cy   35",
         "name  age\nAnn   30\nBob   25\nCy    35",
         "  name  age\n1  Ann   30\n2  Bob   25\n3   Cy   35",
         "   0    1    2\nname  Ann  Bob  Cy\nage    30   25  35"], 0,
        "If you don't give an index, pandas numbers the rows for you, starting at 0.",
        "The default index is a RangeIndex 0, 1, 2 printed on the left. Text is right-aligned by default when printed.",
        topic="creating", level=1),
    out("""import io
import pandas as pd
csv = "id,score\\n1,90\\n2,85\\n3,70"
df = pd.read_csv(io.StringIO(csv))
print(df["score"].sum(), df.shape)""",
        ["245 (3, 2)", "245 (4, 2)", "908570 (3, 2)", "245 (3, 1)"], 0,
        "The first line is the header, not a data row.",
        "read_csv uses the first line as column names, so there are 3 data rows and 2 columns. The scores are parsed as integers, so sum is 245.",
        topic="creating", level=1),
    fill("To parse CSV text held in a Python string, wrap it in `io.____(text)` and pass that to pd.read_csv.",
        "StringIO",
        "It makes a string behave like an open file.",
        "io.StringIO turns a string into an in-memory file object; read_csv accepts any file-like object.",
        topic="creating", level=1),
    out("""import io
import pandas as pd
csv = "id,score\\n1,90\\n2,85"
df = pd.read_csv(io.StringIO(csv), index_col="id")
print(df.columns.tolist(), df.index.tolist())""",
        ["['score'] [1, 2]", "['id', 'score'] [0, 1]", "['score'] [0, 1]", "['id', 'score'] [1, 2]"], 0,
        "index_col moves a column into the row labels.",
        "index_col='id' makes the id column the index, so only 'score' remains as a column and the index is [1, 2].",
        topic="creating", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5]})
print(df.shape)""",
        ["ValueError", "(3, 2)", "(2, 2)", "KeyError"], 0,
        "From a dict of lists, every list must be the same length.",
        "Lists of different lengths cannot form a rectangular table, so pandas raises ValueError: All arrays must be of the same length.",
        topic="creating", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"x": 0, "y": [1, 2, 3]})
print(df["x"].tolist())""",
        ["[0, 0, 0]", "ValueError", "[0]", "[0, nan, nan]"], 0,
        "A scalar can be stretched to fit.",
        "A scalar value in the dict is broadcast to the length of the other columns, so x becomes [0, 0, 0].",
        topic="creating", level=2),
    out("""import pandas as pd
a = pd.Series([1, 2], index=["r1", "r2"])
b = pd.Series([3, 4], index=["r2", "r3"])
df = pd.DataFrame({"a": a, "b": b})
print(df.shape, df.isna().sum().sum())""",
        ["(3, 2) 2", "(2, 2) 0", "ValueError", "(4, 2) 4"], 0,
        "Series in a dict are lined up by their index labels, not by position.",
        "The index becomes the union r1, r2, r3. a has no r3 and b has no r1, so 2 cells are NaN.",
        topic="creating", level=3),
    out("""import io
import pandas as pd
csv = "id,code\\n1,007\\n2,042"
df = pd.read_csv(io.StringIO(csv))
df2 = pd.read_csv(io.StringIO(csv), dtype={"code": str})
print(df["code"].tolist(), df2["code"].tolist())""",
        ["[7, 42] ['007', '042']", "['007', '042'] ['007', '042']", "[7, 42] [7, 42]", "[7.0, 42.0] ['007', '042']"], 0,
        "read_csv guesses types, and numbers lose leading zeros.",
        "Type inference turns 007 into the integer 7. Pass dtype={'code': str} for IDs, zip codes or phone numbers to keep the leading zeros.",
        topic="creating", level=3),
    out("""import io
import pandas as pd
csv = "a,b\\n1,x\\nNA,y\\n3,"
df = pd.read_csv(io.StringIO(csv))
print(df["a"].dtype, df["b"].isna().sum())""",
        ["float64 1", "int64 1", "object 0", "float64 0"], 0,
        "'NA' and an empty field are both read as missing by default.",
        "read_csv treats 'NA' and empty fields as NaN. A NaN in column a forces float64 (NumPy ints can't hold NaN); b has one missing value.",
        topic="creating", level=3),

    # ------------------------------------------------------------------ inspecting
    mcq("What does `df.head()` return when you give it no argument?",
        ["The first 5 rows", "The first row only", "The column names", "The first 10 rows"], 0,
        "It's a quick peek at the top of the table.",
        "head() defaults to n=5. Use head(10) for more, and tail() for the last rows.",
        topic="inspecting", level=1),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1, 2, 3, 4], "b": [5, 6, 7, 8], "c": [9, 10, 11, 12]})
print(df.shape, len(df))""",
        ["(4, 3) 4", "(3, 4) 3", "(4, 3) 12", "(4, 3) 3"], 0,
        "shape is (rows, columns); len counts rows.",
        "There are 4 rows and 3 columns, so shape is (4, 3). len(df) is the number of rows, 4. df.size would be 12.",
        topic="inspecting", level=1),
    mcq("Which method prints the column names, non-null counts and dtypes of a DataFrame?",
        ["df.info()", "df.describe()", "df.head()", "df.columns()"], 0,
        "It gives information about the structure, not statistics.",
        "info() prints the index range, each column's non-null count and dtype, and memory usage. describe() gives summary statistics instead.",
        analogy="info() is like `DESCRIBE table` in SQL: the schema, not the data.",
        topic="inspecting", level=1),
    out("""import pandas as pd
df = pd.DataFrame({"name": ["Ann", "Bob", "Cy"], "age": [30, 25, 35]})
print(df.describe().loc["mean", "age"], df.describe().columns.tolist())""",
        ["30.0 ['age']", "30.0 ['name', 'age']", "30 ['age']", "KeyError"], 0,
        "By default describe() only summarises numeric columns.",
        "describe() skips the text column, so only 'age' appears; its mean is 30.0 (always a float in describe).",
        topic="inspecting", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"name": ["Ann", "Bob"], "age": [30, 25], "score": [9.5, 8.0]})
print(df.dtypes.tolist())""",
        ["[dtype('O'), dtype('int64'), dtype('float64')]",
         "[str, int, float]",
         "['object', 'int64', 'float64']",
         "[dtype('<U3'), dtype('int64'), dtype('float64')]"], 0,
        "dtypes is a Series of NumPy dtype objects; text is stored as Python objects.",
        "Text columns default to object dtype (shown as dtype('O')), whole numbers to int64, decimals to float64.",
        topic="inspecting", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"name": ["Ann", "Bob", "Cy"], "age": [30, 25, 35]})
print(df.describe())""",
        ["        age\ncount   3.0\nmean   30.0\nstd     5.0\nmin    25.0\n25%    27.5\n50%    30.0\n75%    32.5\nmax    35.0",
         "        age\ncount   3.0\nmean   30.0\nstd     4.1\nmin    25.0\n25%    27.5\n50%    30.0\n75%    32.5\nmax    35.0",
         "       name   age\ncount     3   3.0\nmean    NaN  30.0\nstd     NaN   5.0\nmin     Ann  25.0\nmax      Cy  35.0",
         "        age\ncount     3\nmean     30\nstd       5\nmin      25\nmax      35"], 0,
        "pandas uses the sample standard deviation (divide by n-1).",
        "describe() shows count, mean, std, min, quartiles and max for numeric columns. std is the sample std: sqrt(((-0)^2+5^2+5^2)/2) = 5.0, not the population value 4.08.",
        topic="inspecting", level=2),
    tf("`df.describe()` uses the population standard deviation (dividing by n).", False,
        "Compare with NumPy's default ddof.",
        "pandas' std() and describe() use ddof=1 (sample std, divide by n-1). NumPy's np.std defaults to ddof=0. The two disagree on the same data.",
        topic="inspecting", level=3),
    out("""import pandas as pd
import numpy as np
s = pd.Series([1, np.nan, 3])
print(len(s), s.count(), s.mean())""",
        ["3 2 2.0", "3 3 1.333", "2 2 2.0", "3 2 nan"], 0,
        "count() counts non-missing values; mean() skips NaN by default.",
        "len counts every slot (3); count() ignores NaN (2); mean skips NaN, so (1 + 3) / 2 = 2.0.",
        topic="inspecting", level=2),
    mcq("`df.info()` shows a column with `998 non-null` while the RangeIndex says 1000 entries. What does that tell you?",
        ["That column has 2 missing values", "The column has 2 duplicate values", "2 rows failed to parse and were dropped", "The column uses 998 bytes"], 0,
        "Non-null count vs total rows.",
        "Non-null count lower than the row count means missing values (NaN/None). df['col'].isna().sum() would print 2.",
        topic="inspecting", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
print(df.size, df.ndim, df.columns.tolist())""",
        ["4 2 ['a', 'b']", "2 2 ['a', 'b']", "4 1 ['a', 'b']", "(2, 2) 2 ['a', 'b']"], 0,
        "size counts cells; ndim counts axes.",
        "size = rows x columns = 4; a DataFrame has 2 axes (rows and columns); columns is an Index converted to a list.",
        topic="inspecting", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"g": ["a", "b", "a"], "v": [1, 2, 3]})
print(df.describe(include="all").loc["unique", "g"], df.describe(include="all").loc["top", "g"])""",
        ["2 a", "3 a", "2 b", "nan nan"], 0,
        "include='all' adds count/unique/top/freq rows for text columns.",
        "For object columns describe reports unique (2 distinct values), top (most frequent, 'a') and freq. Numeric-only rows like mean are NaN for that column.",
        topic="inspecting", level=3),

    # ------------------------------------------------------------------ selecting
    out("""import pandas as pd
df = pd.DataFrame({"name": ["Ann", "Bob"], "age": [30, 25]})
print(type(df["age"]).__name__, type(df[["age"]]).__name__)""",
        ["Series DataFrame", "Series Series", "DataFrame DataFrame", "DataFrame Series"], 0,
        "A string inside [] vs a list inside [].",
        "df['age'] gives a Series (1-D). df[['age']] passes a list of column names, so you get a DataFrame with one column (2-D).",
        topic="selecting", level=1),
    mcq("How do you select the two columns `name` and `age` from df?",
        ['df[["name", "age"]]', 'df["name", "age"]', 'df.select("name", "age")', 'df[name, age]'], 0,
        "You pass ONE thing inside the brackets: a list.",
        "df[['name', 'age']] passes a Python list of names. df['name', 'age'] looks for a single column whose label is the tuple ('name', 'age') and raises KeyError.",
        topic="selecting", level=1),
    out("""import pandas as pd
df = pd.DataFrame({"name": ["Ann", "Bob"], "age": [30, 25]})
print(df["name", "age"])""",
        ["KeyError", "  name  age\n0  Ann   30\n1  Bob   25", "TypeError", "IndexError"], 0,
        "Python turns `a, b` inside [] into a tuple.",
        "df['name', 'age'] is df[('name', 'age')]: pandas looks for one column labelled by that tuple and raises KeyError. Use double brackets.",
        topic="selecting", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"name": ["Ann", "Bob"], "age": [30, 25]})
print(df.age.tolist(), df["age"].tolist())""",
        ["[30, 25] [30, 25]", "AttributeError", "[30, 25] KeyError", "None [30, 25]"], 0,
        "Columns with simple names are also reachable as attributes.",
        "df.age is a shortcut for df['age'] when the name is a valid Python identifier and doesn't clash with a method.",
        topic="selecting", level=1),
    out("""import pandas as pd
df = pd.DataFrame({"count": [1, 2], "first name": ["A", "B"]})
print(type(df.count).__name__)""",
        ["method", "Series", "int", "AttributeError"], 0,
        "DataFrame already has a method with this name.",
        "df.count is the DataFrame.count method, not your column. Attribute access loses to built-in methods; columns with spaces can't be reached by dot at all. Prefer df['count'].",
        topic="selecting", level=2),
    tf("`df.new_col = [1, 2, 3]` creates a new column named new_col.", False,
        "Attribute *reading* works for existing columns. What about attribute *writing*?",
        "Assigning to a new attribute just sets a Python attribute on the object (pandas warns about it). New columns must be created with df['new_col'] = ...",
        topic="selecting", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1], "b": [2], "c": [3]})
print(df[["c", "a"]].columns.tolist())""",
        ["['c', 'a']", "['a', 'c']", "['a', 'b', 'c']", "KeyError"], 0,
        "The list decides the order.",
        "Selecting with a list returns the columns in the order you listed them, which is also an easy way to reorder columns.",
        topic="selecting", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1, 2], "b": [3.0, 4.0], "c": ["x", "y"]})
print(df.select_dtypes("number").columns.tolist())""",
        ["['a', 'b']", "['a']", "['b']", "['a', 'b', 'c']"], 0,
        "'number' covers both integer and float dtypes.",
        "select_dtypes('number') keeps every numeric column (int and float), handy before scaling features for a model.",
        topic="selecting", level=3),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
print(df[0:2].shape, df[["a"]].shape)""",
        ["(2, 2) (3, 1)", "KeyError", "(2, 2) (3,)", "(3, 2) (3, 1)"], 0,
        "A slice inside df[] is treated differently from a label.",
        "df[0:2] slices ROWS by position (a historical shortcut), giving 2 rows. df['a'] or df[['a']] select columns. Mixing these is confusing, so prefer .iloc for rows.",
        topic="selecting", level=3),

    # ------------------------------------------------------------------ loc-iloc
    mcq("What is the difference between `df.loc` and `df.iloc`?",
        ["loc selects by label (index names); iloc selects by integer position",
         "loc selects rows; iloc selects columns",
         "loc is faster; iloc is safer",
         "loc returns a copy; iloc returns a view"], 0,
        "The 'i' stands for integer.",
        "loc uses index labels and column names. iloc uses 0-based positions like a list, regardless of what the labels are.",
        analogy="loc is looking someone up by name; iloc is 'the 3rd person in the queue'.",
        topic="loc-iloc", level=1),
    out("""import pandas as pd
df = pd.DataFrame({"v": [10, 20, 30, 40]})
print(df.loc[1:2, "v"].tolist(), df.iloc[1:2, 0].tolist())""",
        ["[20, 30] [20]", "[20] [20]", "[20, 30] [20, 30]", "[10, 20] [20]"], 0,
        "One of them includes the end of the slice.",
        "loc slices by label and INCLUDES the end label (1 and 2). iloc slices by position like Python, EXCLUDING the end (just position 1).",
        diagram="""
labels:   0   1   2   3
values:  10  20  30  40
loc[1:2]     [------]     -> 20, 30  (end included)
iloc[1:2]    [--]         -> 20      (end excluded)""",
        topic="loc-iloc", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"name": ["Ann", "Bob", "Cy"], "age": [30, 25, 35]})
print(df.loc[2, "name"], df.iloc[0, 1])""",
        ["Cy 30", "Bob 30", "Cy Ann", "Bob Ann"], 0,
        "loc[row label, column name]; iloc[row position, column position].",
        "loc[2, 'name'] is the row labelled 2 in column name: Cy. iloc[0, 1] is row 0, column 1 (age): 30.",
        topic="loc-iloc", level=1),
    out("""import pandas as pd
df = pd.DataFrame({"v": [10, 20, 30]}, index=[2, 0, 1])
print(df.loc[0, "v"], df.iloc[0, 0])""",
        ["20 10", "10 10", "10 20", "20 20"], 0,
        "When the index isn't 0,1,2 in order, labels and positions disagree.",
        "loc[0] finds the row whose LABEL is 0 (value 20). iloc[0] takes the FIRST row by position (label 2, value 10).",
        diagram="""
position:  0    1    2
label:     2    0    1
value:    10   20   30
iloc[0] -> position 0 -> 10
loc[0]  -> label 0    -> 20""",
        topic="loc-iloc", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"v": [10, 20, 30]}, index=["a", "b", "c"])
print(df.iloc[-1, 0])
print(df.loc[-1, "v"])""",
        ["30\nKeyError", "30\n30", "KeyError", "30\nIndexError"], 0,
        "Negative positions work like Python lists; negative labels must actually exist.",
        "iloc[-1] is the last row (30). loc[-1] looks for a row labelled -1, which doesn't exist, so it raises KeyError after the first print.",
        topic="loc-iloc", level=2),
    fill("Complete to select the `age` column for rows labelled 'r1' through 'r3' inclusive: `df.____['r1':'r3', 'age']`",
        "loc",
        "Label-based, and the end is included.",
        "df.loc['r1':'r3', 'age'] slices by labels and includes 'r3'.",
        topic="loc-iloc", level=1),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1, 2], "b": [3, 4], "c": [5, 6]})
print(df.loc[:, "a":"b"].columns.tolist(), df.iloc[:, 0:1].columns.tolist())""",
        ["['a', 'b'] ['a']", "['a'] ['a']", "['a', 'b'] ['a', 'b']", "['a', 'b', 'c'] ['a']"], 0,
        "The same inclusive/exclusive rule applies to column slices.",
        "loc 'a':'b' includes b; iloc 0:1 excludes position 1, so only column a.",
        topic="loc-iloc", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"v": [10, 20, 30]}, index=[0, 1, 2])
print(df.loc[[0, 2], "v"].tolist(), type(df.loc[1, "v"]).__name__)""",
        ["[10, 30] int64", "[10, 30] Series", "[10, 20, 30] int64", "[10, 30] int"], 0,
        "A list of labels returns several rows; a single label plus single column returns one cell.",
        "loc with a list of labels returns those rows. A single row label with a single column returns a scalar, which is a NumPy int64 here.",
        topic="loc-iloc", level=3),
    out("""import pandas as pd
df = pd.DataFrame({"v": [10, 20, 30]}, index=[1, 1, 2])
print(type(df.loc[1]).__name__, type(df.loc[2]).__name__)""",
        ["DataFrame Series", "Series Series", "DataFrame DataFrame", "KeyError"], 0,
        "Index labels don't have to be unique.",
        "Label 1 appears twice, so loc[1] returns both rows as a DataFrame; label 2 is unique, so loc[2] is one row (a Series). Code that assumes one type breaks on duplicate labels.",
        diagram="""
index  v
  1   10  \\ loc[1] -> 2 rows -> DataFrame
  1   20  /
  2   30    loc[2] -> 1 row  -> Series""",
        topic="loc-iloc", level=3),
    out("""import pandas as pd
df = pd.DataFrame({"v": [10, 20, 30]}, index=[3, 1, 2])
print(df.loc[1:3, "v"].tolist())""",
        ["[]", "[10, 20, 30]", "[20, 30]", "KeyError"], 0,
        "Label slices follow the order of the index, not sorted order.",
        "On a non-sorted index, loc[1:3] goes from wherever label 1 is to wherever label 3 is, in the index's current order. Label 1 is at position 1 and 3 is at 0, so the slice is empty.",
        topic="loc-iloc", level=4),
    mcq("You want the value in the 3rd row of column `price`, regardless of the index labels. Which is correct and clear?",
        ['df["price"].iloc[2]', 'df["price"][2]', 'df.loc[2, "price"]', 'df.iloc[2, "price"]'], 0,
        "Mix 'position for rows' with 'name for columns' safely.",
        "df['price'].iloc[2] is position-based for the row. df['price'][2] and df.loc[2] look for the LABEL 2. df.iloc[2, 'price'] fails because iloc only takes integers.",
        topic="loc-iloc", level=3),
    out("""import pandas as pd
s = pd.Series([10, 20, 30], index=[2, 1, 0])
print(s[0], s.iloc[0])""",
        ["30 10", "10 10", "10 30", "30 30"], 0,
        "With an integer index, plain [] on a Series means label.",
        "s[0] on an integer index looks up LABEL 0 (value 30). s.iloc[0] is position 0 (value 10). This ambiguity is exactly why .loc/.iloc exist.",
        topic="loc-iloc", level=4),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1, 2, 3]})
df.loc[5, "a"] = 9
print(df.index.tolist(), df["a"].dtype)""",
        ["[0, 1, 2, 5] float64", "KeyError", "[0, 1, 2, 5] int64", "IndexError"], 0,
        "loc assignment to a missing label behaves like an upsert.",
        "Setting with loc on a label that doesn't exist appends a new row (enlargement). The column is temporarily NaN-filled during the insert, so it ends up float64. iloc would raise IndexError instead.",
        topic="loc-iloc", level=4),

    # ------------------------------------------------------------------ filtering
    out("""import pandas as pd
df = pd.DataFrame({"name": ["Ann", "Bob", "Cy"], "age": [30, 25, 35]})
print(df[df["age"] > 28]["name"].tolist())""",
        ["['Ann', 'Cy']", "['Cy']", "['Bob']", "[True, False, True]"], 0,
        "The condition makes a True/False per row; df[...] keeps the True rows.",
        "df['age'] > 28 gives a boolean mask [True, False, True]. df[mask] keeps rows Ann and Cy.",
        diagram="""
name  age   age > 28   keep?
Ann    30     True      yes
Bob    25     False     no
Cy     35     True      yes""",
        analogy="SQL: SELECT name FROM df WHERE age > 28.",
        topic="filtering", level=1),
    out("""import pandas as pd
df = pd.DataFrame({"age": [30, 25, 35]})
print((df["age"] > 28).tolist())""",
        ["[True, False, True]", "[30, 35]", "[0, 2]", "True"], 0,
        "A comparison on a column compares every element.",
        "Comparing a Series to a number gives a boolean Series of the same length: the mask.",
        topic="filtering", level=1),
    mcq("Which line correctly keeps rows where age > 20 AND city == 'Pune'?",
        ['df[(df["age"] > 20) & (df["city"] == "Pune")]',
         'df[df["age"] > 20 and df["city"] == "Pune"]',
         'df[df["age"] > 20 & df["city"] == "Pune"]',
         'df[(df["age"] > 20) && (df["city"] == "Pune")]'], 0,
        "Element-wise AND is a different symbol, and it binds tighter than >.",
        "Use & (element-wise AND) with each condition in parentheses. `and` tries to turn a whole Series into one True/False and fails; without parentheses, & is evaluated before > and ==.",
        topic="filtering", level=1),
    out("""import pandas as pd
df = pd.DataFrame({"age": [30, 25, 35]})
print(df[df["age"] > 26 and df["age"] < 34])""",
        ["ValueError", "TypeError", "   age\n0   30", "KeyError"], 0,
        "`and` needs ONE True or False.",
        "Python's `and` calls bool() on a Series, and pandas refuses: 'The truth value of a Series is ambiguous'. That is a ValueError. Use & with parentheses.",
        topic="filtering", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"age": [30, 25, 35]})
print(df[(df["age"] < 26) | (df["age"] > 34)].index.tolist(), df[~(df["age"] > 26)].index.tolist())""",
        ["[1, 2] [1]", "[1, 2] [0, 2]", "[0] [1]", "[1, 2] [0, 1, 2]"], 0,
        "| is OR, ~ is NOT.",
        "Ages under 26 or over 34 are rows 1 and 2. ~ flips the mask age > 26 ([T, F, T]) to [F, T, F], leaving row 1.",
        topic="filtering", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"city": ["Pune", "Goa", "Delhi", "Pune"]})
print(df[df["city"].isin(["Pune", "Goa"])].index.tolist())""",
        ["[0, 1, 3]", "[0, 3]", "[0, 1]", "[1, 2]"], 0,
        "isin is SQL's IN (...).",
        "isin checks membership in a list for each row: Pune, Goa and Pune match at positions 0, 1, 3.",
        analogy="SQL: WHERE city IN ('Pune', 'Goa').",
        topic="filtering", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"name": ["Ann", "Bob", "Cy"], "age": [30, 25, 35]})
limit = 28
print(df.query("age > @limit")["name"].tolist())""",
        ["['Ann', 'Cy']", "['Bob']", "NameError", "UndefinedVariableError"], 0,
        "@ refers to a Python variable inside a query string.",
        "query() takes a string expression; @limit pulls in the local variable. It is the same filter as df[df['age'] > limit], just easier to read.",
        topic="filtering", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"age": [30, 25, 35], "city": ["Pune", "Goa", "Pune"]})
print(df.query("age > 26 and city == 'Pune'").shape)""",
        ["(2, 2)", "ValueError", "(1, 2)", "(3, 2)"], 0,
        "Inside a query string the rules differ from plain Python.",
        "query() parses its own expression language, where `and`/`or` are allowed and mean element-wise &/|. Rows 0 and 2 match.",
        topic="filtering", level=3),
    out("""import pandas as pd
df = pd.DataFrame({"age": [30, 25, 35]})
print(df[df["age"] > 26 & df["age"] < 34])""",
        ["ValueError", "   age\n0   30", "TypeError", "Empty DataFrame\nColumns: [age]\nIndex: []"], 0,
        "& is evaluated first: 26 & df['age']. Then Python sees a chained comparison a > b < c.",
        "Without parentheses, Python computes 26 & df['age'], then expands `x > y < z` into `(x > y) and (y < z)`, and `and` calls bool() on a Series: ValueError. Always parenthesise each condition.",
        diagram="""
written:   df.age > 26 & df.age < 34
Python:    df.age > (26 & df.age) < 34
becomes:   (df.age > X) and (X < 34)   <- `and` on Series
fix:       (df.age > 26) & (df.age < 34)""",
        topic="filtering", level=3),
    out("""import pandas as pd
df = pd.DataFrame({"v": [5, 10, 15, 20]})
print(df[df["v"].between(10, 15)]["v"].tolist())""",
        ["[10, 15]", "[15]", "[10]", "[5, 10, 15, 20]"], 0,
        "Like SQL's BETWEEN.",
        "between(left, right) is inclusive on both ends by default (inclusive='both'), so 10 and 15 are kept.",
        topic="filtering", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"v": [1, 2, 3]})
mask = pd.Series([True, False, True], index=[2, 1, 0])
print(df[mask]["v"].tolist())""",
        ["[1, 3]", "[3, 1]", "[1, 2]", "IndexingError"], 0,
        "A boolean Series mask is matched to rows by index label, not position.",
        "The mask is aligned to df's index first: label 0 -> True, 1 -> False, 2 -> True. Rows 0 and 2 are kept in df's order: [1, 3].",
        topic="filtering", level=4),
    out("""import pandas as pd
df = pd.DataFrame({"v": [1, 2, 3]})
print(df[[True, False]])""",
        ["ValueError", "   v\n0  1", "IndexError", "KeyError"], 0,
        "A plain list mask has no index to align with.",
        "A boolean list must be exactly as long as the DataFrame; length 2 vs 3 raises ValueError ('Item wrong length 2 instead of 3').",
        topic="filtering", level=3),

    # ------------------------------------------------------------------ modifying
    out("""import pandas as pd
df = pd.DataFrame({"price": [100, 200], "qty": [2, 3]})
df["total"] = df["price"] * df["qty"]
print(df["total"].tolist(), df.columns.tolist())""",
        ["[200, 600] ['price', 'qty', 'total']", "[200, 600] ['total', 'price', 'qty']", "[300, 500] ['price', 'qty', 'total']", "KeyError"], 0,
        "Assigning to a new column name creates it at the end.",
        "df['total'] = ... computes row by row (100*2, 200*3) and appends a new column on the right.",
        topic="modifying", level=1),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1], "b": [2]})
df.rename(columns={"a": "x"})
print(df.columns.tolist())""",
        ["['a', 'b']", "['x', 'b']", "['x']", "KeyError"], 0,
        "Most pandas methods return a NEW object.",
        "rename returns a new DataFrame; the result was thrown away, so df is unchanged. Write df = df.rename(columns={'a': 'x'}).",
        topic="modifying", level=1),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1], "b": [2], "c": [3]})
df = df.drop(columns=["b"])
print(df.columns.tolist())""",
        ["['a', 'c']", "['a', 'b', 'c']", "['b']", "KeyError"], 0,
        "drop removes the listed columns and returns the rest.",
        "drop(columns=[...]) removes those columns. Assigning back to df keeps the result.",
        topic="modifying", level=1),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1, 2]})
print(df.drop("a").shape)""",
        ["KeyError", "(2, 0)", "(1, 1)", "(2, 1)"], 0,
        "drop's default axis is rows (axis=0).",
        "Without columns= or axis=1, drop looks for a ROW label 'a' and raises KeyError. Use df.drop(columns='a').",
        topic="modifying", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"name": ["Ann", "Bob", "Cy"], "age": [30, 25, 35]})
print(df.sort_values("age", ascending=False)["name"].tolist())""",
        ["['Cy', 'Ann', 'Bob']", "['Bob', 'Ann', 'Cy']", "['Ann', 'Bob', 'Cy']", "['Cy', 'Bob', 'Ann']"], 0,
        "ascending=False puts the largest first.",
        "Sorted by age descending: 35 (Cy), 30 (Ann), 25 (Bob).",
        analogy="SQL: ORDER BY age DESC.",
        topic="modifying", level=1),
    out("""import pandas as pd
df = pd.DataFrame({"name": ["Ann", "Bob", "Cy"], "age": [30, 25, 35]})
print(df.sort_values("age").index.tolist())""",
        ["[1, 0, 2]", "[0, 1, 2]", "[2, 0, 1]", "[25, 30, 35]"], 0,
        "Sorting moves rows, and each row keeps its label.",
        "Rows carry their original index labels when sorted, so the index reads 1, 0, 2. Use reset_index(drop=True) for 0..n-1 again.",
        topic="modifying", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"team": ["b", "a", "b", "a"], "pts": [1, 5, 3, 2]})
s = df.sort_values(["team", "pts"], ascending=[True, False])
print(s["pts"].tolist())""",
        ["[5, 2, 3, 1]", "[2, 5, 1, 3]", "[5, 3, 2, 1]", "[1, 3, 2, 5]"], 0,
        "Sort by team A-Z first, then within each team by pts high-to-low.",
        "Team a rows (5, 2) come first sorted descending, then team b (3, 1).",
        topic="modifying", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1, 2]})
df2 = df.assign(b=df["a"] * 10, c=lambda d: d["b"] + 1)
print(df2["c"].tolist(), df.columns.tolist())""",
        ["[11, 21] ['a']", "[11, 21] ['a', 'b', 'c']", "KeyError", "[2, 3] ['a']"], 0,
        "assign returns a new frame; later keywords can see earlier ones via a lambda.",
        "assign builds b first, then the lambda receives the frame that already has b, so c = b + 1. The original df is untouched.",
        topic="modifying", level=3),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1, 2]})
r = df.sort_values("a", inplace=True)
print(r)""",
        ["None", "   a\n0  1\n1  2", "True", "   a\n1  2\n0  1"], 0,
        "inplace methods change the object and hand back nothing.",
        "With inplace=True the method returns None. Writing df = df.sort_values(..., inplace=True) sets df to None, a classic bug. inplace also rarely saves memory, so pandas recommends the return-a-new-object style.",
        topic="modifying", level=3),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1], "b": [2]})
df.insert(0, "id", [99])
print(df.columns.tolist())""",
        ["['id', 'a', 'b']", "['a', 'b', 'id']", "['a', 'id', 'b']", "None"], 0,
        "insert takes a position.",
        "insert(loc, name, values) puts the column at that position, in place. Plain df['id'] = ... would append it at the end.",
        topic="modifying", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"v": [3, 1, 4, 1, 5]})
print(df.nlargest(2, "v")["v"].tolist(), df["v"].rank(method="min").tolist())""",
        ["[5, 4] [3.0, 1.0, 4.0, 1.0, 5.0]", "[5, 4] [3.0, 1.5, 4.0, 1.5, 5.0]", "[4, 5] [3.0, 1.0, 4.0, 1.0, 5.0]", "[5, 4] [3, 1, 4, 1, 5]"], 0,
        "rank with method='min' gives tied values the lowest rank of the tie.",
        "nlargest(2) is 'ORDER BY v DESC LIMIT 2'. The two 1s tie for ranks 1-2; method='min' gives both 1.0 (the default 'average' would give 1.5). rank always returns floats.",
        topic="modifying", level=3),

    # ------------------------------------------------------------------ apply-vectorise
    out("""import pandas as pd
s = pd.Series([1, 2, 3])
print((s * 2).tolist())""",
        ["[2, 4, 6]", "[1, 2, 3, 1, 2, 3]", "TypeError", "[1, 2, 3]"], 0,
        "Unlike a Python list, a Series does math on every element.",
        "s * 2 multiplies each value (vectorised). With a plain Python list, [1, 2, 3] * 2 would repeat the list instead.",
        topic="apply-vectorise", level=1),
    out("""import pandas as pd
s = pd.Series(["lo", "hi", "lo"])
print(s.map({"lo": 0, "hi": 1}).tolist())""",
        ["[0, 1, 0]", "['lo', 'hi', 'lo']", "[0, 1]", "KeyError"], 0,
        "map with a dict looks up each value.",
        "Series.map(dict) replaces each value with its dict value, a common way to encode labels.",
        topic="apply-vectorise", level=1),
    tf("A vectorised operation like `df['a'] * 2` is usually much faster than `df['a'].apply(lambda x: x * 2)`.", True,
        "Where does the loop run: in C or in Python?",
        "Vectorised ops loop in compiled C over a NumPy array. apply calls a Python function once per element, which is often 10-100x slower.",
        analogy="Like one bulk SQL UPDATE versus a for-loop issuing one UPDATE per row.",
        topic="apply-vectorise", level=1),
    out("""import pandas as pd
s = pd.Series(["lo", "hi", "mid"])
print(s.map({"lo": 0, "hi": 1}).tolist())""",
        ["[0.0, 1.0, nan]", "[0, 1, 'mid']", "KeyError", "[0, 1, None]"], 0,
        "What does map do with a value that is not in the dict?",
        "Values missing from the dict become NaN, and NaN forces the result to float64. Use .replace() if unmatched values should stay as they are.",
        topic="apply-vectorise", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1, 2], "b": [10, 20]})
print(df.apply(sum).tolist(), df.apply(sum, axis=1).tolist())""",
        ["[3, 30] [11, 22]", "[11, 22] [3, 30]", "[3, 30] [3, 30]", "[33] [33]"], 0,
        "axis=0 (default) hands each COLUMN to the function.",
        "Default axis=0 calls sum on each column (1+2, 10+20). axis=1 calls it on each row (1+10, 2+20).",
        diagram="""
            a    b
row 0       1   10   -> axis=1 sums along a row: 11
row 1       2   20   ->                          22
            |    |
axis=0:     3   30   (sum down each column)""",
        topic="apply-vectorise", level=2),
    mcq("You need `df['bmi'] = weight / height**2` for a million rows. Which is the best approach?",
        ['df["bmi"] = df["weight"] / df["height"] ** 2',
         'df["bmi"] = df.apply(lambda r: r["weight"] / r["height"] ** 2, axis=1)',
         'A for loop with df.iterrows() appending to a list',
         'df["bmi"] = [w / h ** 2 for w, h in zip(df["weight"], df["height"])]'], 0,
        "Column-level arithmetic beats row-by-row Python.",
        "Plain column arithmetic is vectorised and runs in C. apply(axis=1) builds a Series per row, which is the slowest of all; the list comprehension is better but still Python-level.",
        topic="apply-vectorise", level=2),
    out("""import pandas as pd
import numpy as np
df = pd.DataFrame({"t": [5, 15, 25]})
df["band"] = np.where(df["t"] > 10, "warm", "cold")
print(df["band"].tolist())""",
        ["['cold', 'warm', 'warm']", "['warm', 'warm', 'warm']", "[False, True, True]", "ValueError"], 0,
        "np.where(condition, value_if_true, value_if_false).",
        "np.where is the vectorised if/else: 5 is cold, 15 and 25 are warm. It replaces apply with an if inside.",
        analogy="SQL: CASE WHEN t > 10 THEN 'warm' ELSE 'cold' END.",
        topic="apply-vectorise", level=3),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
r = df.apply(lambda row: row["a"] + row["b"], axis=1)
print(type(r).__name__, r.tolist())""",
        ["Series [4, 6]", "DataFrame [4, 6]", "list [4, 6]", "Series [3, 7]"], 0,
        "When the function returns a scalar per row, what shape is the result?",
        "apply(axis=1) with a scalar-returning function gives one value per row: a Series indexed like df.",
        topic="apply-vectorise", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1, 2]})
r = df.apply(lambda row: [row["a"], row["a"] * 10], axis=1, result_type="expand")
print(r.shape, r.columns.tolist())""",
        ["(2, 2) [0, 1]", "(2, 1) [0]", "(2,) []", "(2, 2) ['a', 'b']"], 0,
        "result_type='expand' turns list results into columns.",
        "Each returned list is spread over new columns labelled 0 and 1, giving a 2x2 DataFrame.",
        topic="apply-vectorise", level=4),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
print(df.map(lambda x: x * 10).values.tolist())""",
        ["[[10, 30], [20, 40]]", "AttributeError", "[[10, 20], [30, 40]]", "[40, 60]"], 0,
        "DataFrame.map (pandas 2.1+) is the element-wise version, formerly applymap.",
        "DataFrame.map applies a function to every cell; it replaced the deprecated applymap. .values.tolist() lists the rows.",
        topic="apply-vectorise", level=3),
    out("""import pandas as pd
calls = []
def f(col):
    calls.append(col.name)
    return col.sum()
df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
df.apply(f)
print(calls)""",
        ["['a', 'b']", "['a', 'a', 'b']", "[0, 1]", "['a', 'b', 'a', 'b']"], 0,
        "Each column is passed once; col.name is the column label.",
        "apply on a DataFrame calls f once per column with a Series whose .name is the column label. (Older pandas versions called the first column twice to infer the result shape.)",
        topic="apply-vectorise", level=4),
    mcq("Why is `df.apply(func, axis=1)` so slow compared with column-wise vectorised code?",
        ["It builds a new Series object for every row and calls a Python function on it",
         "It always copies the whole DataFrame to disk first",
         "It runs on one CPU core while vectorised code uses all cores",
         "It converts every value to a string before calling func"], 0,
        "Think about the per-row overhead.",
        "Each row is boxed into a Series (with an index, dtype resolution and possibly upcasting) and passed to Python code, so the per-row overhead dwarfs the actual math. Vectorised code runs one C loop over a contiguous array.",
        topic="apply-vectorise", level=3),

    # ------------------------------------------------------------------ index-alignment
    out("""import pandas as pd
a = pd.Series([1, 2, 3], index=["x", "y", "z"])
b = pd.Series([10, 20, 30], index=["y", "z", "w"])
print((a + b).tolist())""",
        ["[nan, nan, 12.0, 23.0]", "[11, 22, 33]", "[12.0, 23.0]", "[nan, 12.0, 23.0, nan]"], 0,
        "pandas matches labels, not positions, and sorts the union of labels.",
        "Arithmetic aligns on the index. The union of labels is sorted: w, x, y, z. Only y (2+10) and z (3+20) exist in both; w and x become NaN.",
        diagram="""
label   a     b     a+b
w      --    30     NaN
x       1    --     NaN
y       2    10    12.0
z       3    20    23.0""",
        analogy="Like a FULL OUTER JOIN on the index, then adding the matched columns.",
        topic="index-alignment", level=2),
    tf("Adding two Series always adds them element by element in position order, like NumPy arrays.", False,
        "What does pandas use to pair values up?",
        "pandas aligns on index labels first. With identical indexes this looks positional, but with different labels you get NaN for labels missing on either side.",
        topic="index-alignment", level=1),
    out("""import pandas as pd
df = pd.DataFrame({"name": ["Ann", "Bob"], "age": [30, 25]})
df = df.set_index("name")
print(df.loc["Bob", "age"], df.columns.tolist())""",
        ["25 ['age']", "25 ['name', 'age']", "KeyError", "30 ['age']"], 0,
        "set_index moves a column into the row labels.",
        "After set_index('name') the names are the index, so loc['Bob'] works and 'name' is no longer a column.",
        analogy="Like making 'name' the primary key so you can look rows up by it.",
        topic="index-alignment", level=1),
    out("""import pandas as pd
df = pd.DataFrame({"v": [3, 1, 2]}).sort_values("v")
print(df.reset_index().columns.tolist(), df.reset_index(drop=True).columns.tolist())""",
        ["['index', 'v'] ['v']", "['v'] ['v']", "['index', 'v'] ['index', 'v']", "['v', 'index'] ['v']"], 0,
        "reset_index by default keeps the old index as a column.",
        "reset_index() moves the old index into a column called 'index' and gives 0..n-1. drop=True throws the old index away.",
        topic="index-alignment", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"v": [10, 20, 30]})
s = df["v"].sort_values(ascending=False).reset_index(drop=True)
df["rank_val"] = s
print(df["rank_val"].tolist())""",
        ["[30, 20, 10]", "[10, 20, 30]", "[nan, nan, nan]", "ValueError"], 0,
        "Column assignment aligns on the index. What is s's index after reset?",
        "After reset_index(drop=True), s has labels 0, 1, 2 holding 30, 20, 10, so it is assigned by label: row 0 gets 30.",
        topic="index-alignment", level=3),
    out("""import pandas as pd
df = pd.DataFrame({"v": [10, 20, 30]})
df["sorted"] = df["v"].sort_values(ascending=False)
print(df["sorted"].tolist())""",
        ["[10, 20, 30]", "[30, 20, 10]", "[nan, nan, nan]", "ValueError"], 0,
        "The sorted Series still carries its original labels.",
        "Assigning a Series aligns by index, so each value goes back to its own row and the sort is undone. Use .to_numpy() or reset_index(drop=True) if you want positional assignment.",
        diagram="""
df["v"]     sorted s       assigned by label
0  10       2  30          0 <- 10
1  20       1  20          1 <- 20
2  30       0  10          2 <- 30   (sort undone)""",
        topic="index-alignment", level=3),
    out("""import pandas as pd
a = pd.Series([1, 2], index=["x", "y"])
b = pd.Series([10], index=["x"])
print(a.add(b, fill_value=0).tolist())""",
        ["[11.0, 2.0]", "[11.0, nan]", "[11, 2]", "[11.0]"], 0,
        "fill_value stands in for the side that's missing.",
        "a.add(b, fill_value=0) treats b's missing y as 0, so y = 2 + 0. The intermediate NaN makes the result float64.",
        topic="index-alignment", level=3),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1, 2], "b": [10, 20]})
print((df - df.mean()).values.tolist())""",
        ["[[-0.5, -5.0], [0.5, 5.0]]", "[[-4.5, 4.5], [-9.0, 9.0]]", "ValueError", "[[nan, nan], [nan, nan]]"], 0,
        "df.mean() is a Series indexed by column names.",
        "DataFrame minus Series aligns the Series index with the COLUMNS and broadcasts down the rows: column a subtracts 1.5, column b subtracts 15.",
        topic="index-alignment", level=3),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1, 2], "b": [10, 20]})
print((df - df.mean(axis=1)).shape, (df - df.mean(axis=1)).isna().all().all())""",
        ["(2, 4) True", "(2, 2) False", "ValueError", "(2, 2) True"], 0,
        "The row means are indexed by 0 and 1; which axis do they get matched against?",
        "df - Series matches the Series index to the column labels. Labels 0, 1 don't match 'a', 'b', so the union gives 4 columns, all NaN. Use df.sub(df.mean(axis=1), axis=0).",
        topic="index-alignment", level=4),
    out("""import pandas as pd
a = pd.Series([1, 2, 3], index=["x", "x", "y"])
b = pd.Series([10, 20], index=["x", "y"])
print((a + b).tolist())""",
        ["[11, 12, 23]", "[11, 22, 3]", "ValueError", "[nan, nan, nan]"], 0,
        "Each x on the left finds the single x on the right.",
        "Alignment matches labels; both x rows in a pair with b's x (10) and y pairs with 20. With duplicates on BOTH sides, alignment does a many-to-many match and can multiply rows.",
        topic="index-alignment", level=4),

    # ------------------------------------------------------------------ copy-view
    tf("In pandas 2.2, copy-on-write is turned on by default.", False,
        "It becomes the default in a later major version.",
        "In 2.2 copy-on-write is opt-in (pd.options.mode.copy_on_write = True, or 'warn'). It becomes the only behaviour in pandas 3.0.",
        topic="copy-view", level=3),
    mcq("What does SettingWithCopyWarning mean?",
        ["You may be modifying a temporary copy, so the original DataFrame might not change",
         "You made too many copies and memory is low",
         "The column you set has the wrong dtype",
         "Your DataFrame has duplicate column names"], 0,
        "It's about whether your write actually reaches the original data.",
        "pandas can't tell if the object you're writing to is a view of the original or a copy, so it warns that your change may be lost. Fix by doing the selection and assignment in ONE .loc call, or by calling .copy() explicitly.",
        topic="copy-view", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1, 2, 3], "b": [10, 20, 30]})
df[df["a"] > 1]["b"] = 0
print(df["b"].tolist())""",
        ["[10, 20, 30]", "[10, 0, 0]", "[0, 0, 0]", "KeyError"], 0,
        "Two separate [] steps: the first one makes a NEW frame.",
        "df[mask] creates a new DataFrame (a copy). Setting ['b'] on that temporary copy is lost; pandas emits SettingWithCopyWarning. df is unchanged.",
        diagram="""
df --df[mask]--> temp copy --["b"] = 0--> temp changed
 |                                          (then discarded)
 +-- unchanged

df.loc[mask, "b"] = 0  --> writes straight into df""",
        topic="copy-view", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1, 2, 3], "b": [10, 20, 30]})
df.loc[df["a"] > 1, "b"] = 0
print(df["b"].tolist())""",
        ["[10, 0, 0]", "[10, 20, 30]", "[0, 0, 0]", "[10, 20, 0]"], 0,
        "One .loc call with both the row filter and the column.",
        "loc[row_mask, column] = value writes directly into df, with no intermediate copy. This is the fix for SettingWithCopyWarning.",
        analogy="SQL: UPDATE df SET b = 0 WHERE a > 1, one statement.",
        topic="copy-view", level=1),
    fill("To get an independent DataFrame that you can change without touching the original, call `sub = df[df.a > 1].____()`.",
        "copy",
        "Make it explicit.",
        ".copy() returns a deep copy by default. Changing sub afterwards can never affect df, and no SettingWithCopyWarning is raised.",
        topic="copy-view", level=1),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1, 2, 3]})
s = df["a"]
s[0] = 100
print(df["a"].tolist())""",
        ["[100, 2, 3]", "[1, 2, 3]", "KeyError", "[100, 100, 100]"], 0,
        "In pandas 2.2 without copy-on-write, df['a'] can share memory with df.",
        "With copy-on-write off (the 2.2 default), the column Series is a view of df's data, so writing to it changes df. With copy-on-write on, df would stay [1, 2, 3].",
        topic="copy-view", level=3),
    out("""import pandas as pd
with pd.option_context("mode.copy_on_write", True):
    df = pd.DataFrame({"a": [1, 2, 3]})
    s = df["a"]
    s[0] = 100
    print(df["a"].tolist(), s.tolist())""",
        ["[1, 2, 3] [100, 2, 3]", "[100, 2, 3] [100, 2, 3]", "[1, 2, 3] [1, 2, 3]", "ValueError"], 0,
        "Under copy-on-write, every derived object behaves like a copy.",
        "With copy-on-write, s shares memory only until it is written to; the write triggers a real copy, so df is protected. Behaviour is predictable: only the object you modify changes.",
        diagram="""
s = df["a"]      df --\\
                      +--> [1, 2, 3]   (shared)
                 s ---/
s[0] = 100       df --> [1, 2, 3]
                 s  --> [100, 2, 3]  (copied on write)""",
        topic="copy-view", level=3),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1, 2, 3]})
df["a"][0] = 99
print(df["a"].tolist())""",
        ["[99, 2, 3]", "[1, 2, 3]", "KeyError", "ValueError"], 0,
        "In 2.2 with default settings, df['a'] is a cached view of the column.",
        "Chained assignment through a column still writes through in pandas 2.2 (with a FutureWarning saying it will stop working). Under copy-on-write / pandas 3.0 it never updates df. Use df.loc[0, 'a'] = 99.",
        topic="copy-view", level=3),
    out("""import pandas as pd
with pd.option_context("mode.copy_on_write", True):
    df = pd.DataFrame({"a": [1, 2, 3]})
    df["a"][0] = 99
    print(df["a"].tolist())""",
        ["[1, 2, 3]", "[99, 2, 3]", "ChainedAssignmentError", "KeyError"], 0,
        "Under copy-on-write, df['a'] is always a new object as far as writes are concerned.",
        "With copy-on-write, chained assignment never reaches df; pandas only emits a ChainedAssignmentError *warning*, so the code runs and df is unchanged. This is how pandas 3.0 behaves.",
        topic="copy-view", level=4),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
sub = df[["a"]]
sub.loc[0, "a"] = 100
print(df["a"].tolist())""",
        ["[1, 2, 3]", "[100, 2, 3]", "KeyError", "[100, 100, 100]"], 0,
        "Selecting columns with a list builds a new frame.",
        "df[['a']] (list indexing) always returns a copy, so changing sub never affects df; pandas still warns because it cannot be sure. Under copy-on-write the warning disappears and the result is the same.",
        topic="copy-view", level=3),
    mcq("A teammate's function does `def clean(df): df['x'] = df['x'].fillna(0); return df`. What's the design risk?",
        ["It mutates the caller's DataFrame as a side effect",
         "fillna cannot be used inside a function",
         "It returns a copy, so the changes are lost",
         "It raises SettingWithCopyWarning every time"], 0,
        "DataFrames are passed by reference, like objects in JS or Java.",
        "The function receives a reference to the same object, so assigning a column modifies the caller's frame too. Start with df = df.copy() (or use assign) to keep functions pure.",
        analogy="Same as mutating an object argument in a JS function: the caller sees the change.",
        topic="copy-view", level=3),
    mcq("Under pandas copy-on-write, why can `df2 = df.reset_index(drop=True)` be cheap even for a huge df?",
        ["The new object shares the underlying data until one of them is written to",
         "reset_index is always done lazily on disk",
         "copy-on-write skips creating df2 entirely",
         "It deletes df's data and moves it into df2"], 0,
        "Copying is deferred until it is actually needed.",
        "Copy-on-write lets methods return new objects that share memory with the original; a real copy happens only when one side is modified. You get copy semantics at near-view cost.",
        analogy="Like fork() in Unix or immutable data structures: pages are shared until someone writes.",
        topic="copy-view", level=4),
    tf("`df.copy()` with the default `deep=True` also deep-copies Python objects stored inside object-dtype cells (e.g. lists in a cell).", False,
        "The 'deep' refers to the data arrays, not to Python objects within them.",
        "deep=True copies the arrays, but for object dtype it copies the references, not the Python objects themselves. Mutating a list stored in a cell affects both copies. Use copy.deepcopy if you truly need it.",
        topic="copy-view", level=4),

    # ------------------------------------------------------------------ dtypes-memory
    out("""import pandas as pd
s = pd.Series([1, None, 3])
print(s.dtype)""",
        ["float64", "int64", "object", "Int64"], 0,
        "NumPy integer arrays cannot store a missing value.",
        "None becomes NaN, and NaN is a float, so pandas upcasts the whole column to float64. The ints are now 1.0 and 3.0.",
        topic="dtypes-memory", level=2),
    out("""import pandas as pd
s = pd.Series([1, None, 3], dtype="Int64")
print(s.dtype, s.tolist())""",
        ["Int64 [1, <NA>, 3]", "int64 [1, nan, 3]", "float64 [1.0, nan, 3.0]", "TypeError"], 0,
        "Capital-I Int64 is pandas' nullable integer type.",
        "Int64 (capital I) stores integers plus a mask of missing values, shown as <NA>. The ints stay ints.",
        topic="dtypes-memory", level=2),
    mcq("What dtype does pandas 2.2 give a column of Python strings by default?",
        ["object", "string", "str", "category"], 0,
        "The dedicated text type exists but isn't the default yet.",
        "Strings default to object dtype (an array of pointers to Python str objects). The 'string' dtype exists and must be requested with dtype='string' or astype('string').",
        topic="dtypes-memory", level=1),
    out("""import pandas as pd
s = pd.Series(["1", "2", "3"])
print(s.astype(int).sum(), s.sum())""",
        ["6 123", "6 6", "123 123", "TypeError"], 0,
        "Adding strings joins them.",
        "astype(int) converts text to numbers, so the sum is 6. Summing the object column concatenates the strings: '123'.",
        topic="dtypes-memory", level=1),
    out("""import pandas as pd
df = pd.DataFrame({"a": [1, 2], "b": [1.5, 2.5], "c": ["x", "y"], "d": [True, False]})
print(df.dtypes.astype(str).tolist())""",
        ["['int64', 'float64', 'object', 'bool']", "['int64', 'float64', 'string', 'bool']", "['int', 'float', 'str', 'bool']", "['int64', 'float64', 'object', 'object']"], 0,
        "Default NumPy-backed dtypes for each Python type.",
        "ints -> int64, floats -> float64, str -> object, bools -> bool.",
        topic="dtypes-memory", level=1),
    tf("Converting a column with few distinct values (e.g. 'lo'/'hi' over a million rows) to `category` usually saves a lot of memory.", True,
        "Store each distinct string once.",
        "category stores the unique values once plus a small integer code per row, instead of a Python string object per row.",
        diagram="""
object column           category column
"lo" -> str obj         categories: ["hi", "lo"]
"hi" -> str obj         codes (int8): 1 0 1 1 ...
"lo" -> str obj
...  one object per row  one byte per row""",
        analogy="Like normalising a table: a lookup table of values plus a foreign-key integer column.",
        topic="dtypes-memory", level=2),
    out("""import pandas as pd
s = pd.Series(["lo", "hi", "lo", "lo"] * 1000)
c = s.astype("category")
print(c.cat.categories.tolist(), c.cat.codes.dtype, c.memory_usage(deep=True) < s.memory_usage(deep=True) / 10)""",
        ["['hi', 'lo'] int8 True", "['lo', 'hi'] int8 True", "['hi', 'lo'] int64 True", "['hi', 'lo'] int8 False"], 0,
        "Categories are sorted; with 2 categories the codes need only 1 byte.",
        "Categories are stored sorted (hi, lo); the codes use the smallest integer type that fits (int8). Memory drops by over 10x.",
        topic="dtypes-memory", level=3),
    mcq("Why does `df.memory_usage()` report much less than `df.memory_usage(deep=True)` for a text column?",
        ["Without deep, object columns count only the 8-byte pointers, not the Python strings they point to",
         "deep=True also counts the memory of the index twice",
         "deep=True includes the memory of the CSV file it came from",
         "Without deep, pandas compresses the strings first"], 0,
        "An object column is an array of references.",
        "An object array stores pointers (8 bytes each). Only deep=True follows the pointers and adds the size of each Python str object, which is the real cost.",
        topic="dtypes-memory", level=3),
    out("""import pandas as pd
s = pd.Series([1, 2, 300])
print(s.astype("int8").tolist())""",
        ["[1, 2, 44]", "OverflowError", "[1, 2, 300]", "[1, 2, 127]"], 0,
        "int8 holds -128..127, and astype doesn't check range.",
        "astype('int8') wraps around silently on overflow: 300 - 256 = 44. pd.to_numeric(s, downcast='integer') picks a safe size instead.",
        topic="dtypes-memory", level=4),
    out("""import pandas as pd
s = pd.Series(["a", None], dtype="string")
o = pd.Series(["a", None])
print(s.isna().tolist(), repr(s[1]), repr(o[1]))""",
        ["[False, True] <NA> None", "[False, True] nan None", "[False, False] None None", "[False, True] <NA> nan"], 0,
        "The string dtype uses pandas' own missing marker.",
        "The 'string' dtype stores missing as pd.NA (printed <NA>). An object Series keeps the actual None object, though isna() treats both as missing.",
        topic="dtypes-memory", level=3),
    out("""import pandas as pd
s = pd.Series([1, None], dtype="Int64")
print(s[1] == 1, s.sum())""",
        ["<NA> 1", "False 1", "False 1.0", "TypeError"], 0,
        "pd.NA propagates through comparisons (three-valued logic, like SQL NULL).",
        "pd.NA == 1 is pd.NA, not False, mirroring SQL where NULL = 1 is NULL. Aggregations skip NA, so the sum is 1 and stays an integer.",
        topic="dtypes-memory", level=4),
    out("""import pandas as pd
s = pd.Series([1, None], dtype="Int64")
if s[1] == 1:
    print("yes")""",
        ["TypeError", "yes", "", "ValueError"], 0,
        "What is bool(pd.NA)?",
        "s[1] == 1 is pd.NA, and pd.NA refuses to be converted to True/False: TypeError ('boolean value of NA is ambiguous'). Check with pd.isna() first.",
        topic="dtypes-memory", level=4),
    out("""import pandas as pd
s = pd.Series([True, False, None])
print(s.dtype, s.astype("boolean").sum())""",
        ["object 1", "bool 1", "boolean 1", "object TypeError"], 0,
        "A NumPy bool array has no slot for missing.",
        "With a None present, the column can't be bool, so it falls back to object. The nullable 'boolean' dtype holds True/False/<NA>; its sum skips NA and counts 1 True.",
        topic="dtypes-memory", level=4),

    # ------------------------------------------------------------------ multiindex
    mcq("What is a MultiIndex?",
        ["An index with more than one level, so each row label is a tuple like ('Pune', 2024)",
         "Several DataFrames stored inside one",
         "An index that allows duplicate labels",
         "An index of multiple dtypes at once"], 0,
        "Think of a composite key.",
        "A MultiIndex (hierarchical index) has several levels; each label is a tuple. groupby on several columns and pivot results often produce one.",
        analogy="A composite primary key (city, year) in SQL.",
        topic="multiindex", level=3),
    out("""import pandas as pd
df = pd.DataFrame({"city": ["Pune", "Pune", "Goa"], "year": [2023, 2024, 2024], "sales": [5, 7, 3]})
m = df.set_index(["city", "year"])
print(m.loc[("Pune", 2024), "sales"], m.index.nlevels)""",
        ["7 2", "5 2", "7 1", "KeyError"], 0,
        "Each row label is now a (city, year) tuple.",
        "set_index with two columns builds a 2-level MultiIndex; loc[('Pune', 2024)] selects that exact row.",
        diagram="""
         level 0  level 1
index:   (Pune,   2023)  -> sales 5
         (Pune,   2024)  -> sales 7
         (Goa,    2024)  -> sales 3""",
        topic="multiindex", level=3),
    out("""import pandas as pd
df = pd.DataFrame({"city": ["Pune", "Pune", "Goa"], "year": [2023, 2024, 2024], "sales": [5, 7, 3]})
m = df.set_index(["city", "year"])
print(m.loc["Pune"]["sales"].tolist(), m.loc["Pune"].index.tolist())""",
        ["[5, 7] [2023, 2024]", "[5] [2023]", "KeyError", "[5, 7] [('Pune', 2023), ('Pune', 2024)]"], 0,
        "Selecting by the first level only drops that level.",
        "loc['Pune'] returns all rows for Pune, and the city level is dropped, leaving year as the index.",
        topic="multiindex", level=3),
    out("""import pandas as pd
df = pd.DataFrame({"city": ["Pune", "Pune", "Goa"], "year": [2023, 2024, 2024], "sales": [5, 7, 3]})
s = df.set_index(["city", "year"])["sales"]
print(s.xs(2024, level="year").to_dict())""",
        ["{'Pune': 7, 'Goa': 3}", "{'Goa': 3, 'Pune': 7}", "{('Pune', 2024): 7, ('Goa', 2024): 3}", "KeyError"], 0,
        "xs takes a cross-section on an inner level.",
        "xs(2024, level='year') picks every row whose year is 2024 and drops the year level, keeping the original row order.",
        topic="multiindex", level=4),
    out("""import pandas as pd
df = pd.DataFrame({"city": ["Pune", "Pune", "Goa"], "year": [2023, 2024, 2024], "sales": [5, 7, 3]})
w = df.set_index(["city", "year"])["sales"].unstack()
print(w.shape, w.columns.tolist(), w.isna().sum().sum())""",
        ["(2, 2) [2023, 2024] 1", "(3, 1) [2024] 0", "(2, 2) ['Goa', 'Pune'] 1", "(2, 2) [2023, 2024] 0"], 0,
        "unstack moves the innermost index level into the columns.",
        "unstack pivots year into columns: rows Goa and Pune, columns 2023 and 2024. Goa has no 2023 row, so one cell is NaN.",
        diagram="""
(city, year) sales        year  2023  2024
(Pune, 2023)   5    ->   city
(Pune, 2024)   7         Goa    NaN   3.0
(Goa,  2024)   3         Pune   5.0   7.0""",
        topic="multiindex", level=4),
    out("""import pandas as pd
df = pd.DataFrame({"g": ["a", "a", "b"], "v": [1, 2, 3]})
r = df.groupby("g").agg(["sum", "max"])
print(r.columns.tolist())""",
        ["[('v', 'sum'), ('v', 'max')]", "['sum', 'max']", "['v_sum', 'v_max']", "['v', 'sum', 'max']"], 0,
        "Several aggregations per column produce two levels of column labels.",
        "agg with a list gives MultiIndex COLUMNS: (column, function). Flatten with ['_'.join(c) for c in r.columns] or use named aggregation.",
        topic="multiindex", level=3),
    tf("Slicing a MultiIndex with `loc` by ranges (e.g. `m.loc['A':'C']`) works reliably only when the index is lexsorted (call `sort_index()` first).", True,
        "Range lookups need sorted keys.",
        "On an unsorted MultiIndex, range slicing can raise UnsortedIndexError or be slow. sort_index() makes slicing work and lookups fast (binary search).",
        topic="multiindex", level=4),

    # ------------------------------------------------------------------ concept round-up (mixed topics)
    mcq("In SQL terms, what does a DataFrame's index most resemble?",
        ["A row key used to look up and align rows (like a primary key, though it may repeat)",
         "A database index that only speeds up queries and is never visible",
         "The list of column names",
         "An auto-increment column that can't be changed"], 0,
        "It's what loc looks things up by.",
        "The index labels the rows: loc uses it for lookups and arithmetic aligns on it. Unlike a primary key, pandas allows duplicate labels.",
        topic="index-alignment", level=2),
    tf("`df.loc[:, 'a':'c']` and `df.iloc[:, 0:3]` select the same columns when the columns are a, b, c, d.", True,
        "loc includes the end label; iloc excludes the end position.",
        "loc 'a':'c' gives a, b, c. iloc 0:3 gives positions 0, 1, 2, which are also a, b, c.",
        topic="loc-iloc", level=2),
    mcq("You have a DataFrame `df` indexed by user_id. Which gives the row for user_id 42?",
        ["df.loc[42]", "df.iloc[42]", "df[42]", "df.get_row(42)"], 0,
        "user_id is a label, not a position.",
        "loc[42] looks up the label 42. iloc[42] would be the 43rd row, whatever its id. df[42] looks for a COLUMN named 42.",
        topic="loc-iloc", level=1),
    fill("To keep only rows where column `city` is in a list, write `df[df['city'].____(['Pune', 'Goa'])]`.",
        "isin",
        "SQL's IN.",
        "Series.isin(values) returns a boolean mask that is True where the value is in the list.",
        topic="filtering", level=1),
    mcq("Which is the readable equivalent of `df[(df['age'] > 30) & (df['city'] == 'Pune')]`?",
        ["df.query(\"age > 30 and city == 'Pune'\")",
         "df.where(\"age > 30 and city == 'Pune'\")",
         "df.filter(\"age > 30 and city == 'Pune'\")",
         "df.select(\"age > 30 & city == Pune\")"], 0,
        "One method takes a whole boolean expression as a string.",
        "query() evaluates a string expression against the columns. df.filter selects columns/rows by LABEL name, not by value, and df.where keeps the shape and puts NaN where the condition is False.",
        topic="filtering", level=2),
    out("""import pandas as pd
df = pd.DataFrame({"v": [1, 5, 3]})
print(df.where(df["v"] > 2)["v"].tolist())""",
        ["[nan, 5.0, 3.0]", "[5, 3]", "[False, True, True]", "[1, 5, 3]"], 0,
        "where keeps the shape and blanks out the rest.",
        "df.where(cond) returns the same shape, with NaN where cond is False (so ints become float). Filtering with df[cond] drops rows instead.",
        topic="filtering", level=3),
    tf("`df.filter(like='price')` keeps the rows whose price column matches a condition.", False,
        "filter is about labels, not values.",
        "DataFrame.filter selects columns (or rows) whose LABELS match items/like/regex, e.g. every column with 'price' in its name. Value filtering is df[mask] or query().",
        topic="selecting", level=3),
    mcq("You want to rename every column to lower case. Which works?",
        ["df.columns = df.columns.str.lower()", "df.rename(str.lower)", "df.lower(columns=True)", "df.columns.lower()"], 0,
        "df.columns is an Index, and it has a .str accessor.",
        "Assigning a new Index to df.columns renames everything. df.rename(columns=str.lower) also works; df.rename(str.lower) would rename the row labels.",
        topic="modifying", level=2),
    fill("To sort a DataFrame by its row labels rather than by a column, call `df.____()`.",
        "sort_index",
        "Sorting by the index.",
        "sort_index() orders rows by the index labels; sort_values(col) orders by a column's values.",
        topic="modifying", level=2),
    tf("`df.sort_values('a')` sorts df itself and returns None.", False,
        "Which methods return a new object by default?",
        "sort_values returns a new sorted DataFrame and leaves df as it was. Only inplace=True mutates df (and then returns None).",
        topic="modifying", level=1),
    mcq("Which statement about `Series.map` vs `Series.apply` is true?",
        ["map accepts a dict or Series as a lookup table; apply takes a function",
         "map is always vectorised C code; apply is always Python",
         "apply works only on DataFrames",
         "map changes the Series in place"], 0,
        "Think about what you can pass as the argument.",
        "map(dict) does a lookup (missing keys -> NaN); both map and apply also accept a function, which runs in Python per element. Neither mutates the Series.",
        topic="apply-vectorise", level=2),
    mcq("A senior reviewer says 'never use iterrows to compute a new column'. What is the best reason?",
        ["It is a Python loop that builds a Series per row, and it also upcasts mixed row dtypes",
         "It skips the first row",
         "It only works on numeric columns",
         "It modifies the DataFrame while iterating"], 0,
        "Two problems: speed and dtypes.",
        "iterrows yields (index, Series) pairs: one Python object per row, which is slow, and each row Series has a single dtype, so ints can become floats. Use vectorised ops, or itertuples if you truly must loop.",
        topic="apply-vectorise", level=3),
    tf("`df['a'].mean()` skips NaN values by default.", True,
        "Look for the skipna parameter.",
        "Reductions like mean, sum, max use skipna=True by default. NumPy's np.mean on an array with NaN returns nan instead.",
        topic="inspecting", level=1),
    mcq("What does `pd.options.mode.copy_on_write = 'warn'` do in pandas 2.2?",
        ["Keeps the old behaviour but warns wherever the result would change under copy-on-write",
         "Turns copy-on-write on and raises an error on chained assignment",
         "Disables SettingWithCopyWarning permanently",
         "Copies every DataFrame on creation"], 0,
        "It's a migration aid for pandas 3.0.",
        "'warn' mode runs with today's semantics but warns at every spot whose behaviour would change once copy-on-write is the default, so you can fix code before upgrading.",
        topic="copy-view", level=4),
    mcq("Under copy-on-write, which line is the correct way to set `b` to 0 for rows where `a > 1`?",
        ['df.loc[df["a"] > 1, "b"] = 0', 'df[df["a"] > 1]["b"] = 0', 'df["b"][df["a"] > 1] = 0', 'df.b[df.a > 1] = 0'], 0,
        "One indexing operation, not two.",
        "Only a single __setitem__ on df itself (via loc) modifies df. The other three are chained assignment: under copy-on-write they never update df.",
        topic="copy-view", level=2),
    mcq("A column of 10 million user_id strings with ~10 million distinct values is using lots of memory. Is `category` a good fit?",
        ["No: with almost all values unique, category stores every value anyway plus codes, so it saves little or nothing",
         "Yes: category always halves memory",
         "Yes: category compresses strings with gzip",
         "No: category can't store strings"], 0,
        "When does category help?",
        "category wins when the number of distinct values is small relative to rows. With near-unique values, the categories array is as big as the original plus a code array. Consider the 'string[pyarrow]' dtype or an integer key instead.",
        topic="dtypes-memory", level=3),
    fill("The nullable integer dtype that can hold missing values without becoming float is written `\"____\"` (capital letter matters).",
        "Int64",
        "Capital I.",
        "'Int64' (capital I) is the pandas extension dtype with a mask; 'int64' is the NumPy dtype that can't hold NaN.",
        topic="dtypes-memory", level=2),
    tf("In pandas, `df.shape` is a method, so you call it as `df.shape()`.", False,
        "Is it an attribute or a function?",
        "shape is an attribute holding a tuple (rows, cols). df.shape() raises TypeError: 'tuple' object is not callable.",
        topic="inspecting", level=1),
    mcq("What does `df.set_index(['city', 'year'])` produce?",
        ["A DataFrame whose index is a 2-level MultiIndex of (city, year) tuples",
         "Two separate DataFrames, one per column",
         "A DataFrame with an index named 'city_year'",
         "An error, because set_index takes one column"], 0,
        "A list of keys builds a composite key.",
        "Passing a list to set_index creates a MultiIndex; each row label becomes a (city, year) tuple and both columns leave the data.",
        topic="multiindex", level=3),
    mcq("You have a MultiIndex DataFrame and want plain columns again (e.g. before saving to CSV or feeding scikit-learn). What do you call?",
        ["reset_index()", "unstack()", "flatten()", "drop_index()"], 0,
        "Undo set_index.",
        "reset_index() moves every index level back into ordinary columns and gives a fresh 0..n-1 RangeIndex.",
        topic="multiindex", level=3),
    mcq("Why does pandas insist that `bool(series)` raises instead of returning True/False?",
        ["It's ambiguous: should it mean 'any element is True', 'all are True' or 'not empty'?",
         "Series objects are always truthy, so it would be useless",
         "Because Series can contain strings",
         "For performance: computing truthiness is too slow"], 0,
        "There are several reasonable meanings.",
        "Unlike a list (truthy if non-empty), a Series could reasonably mean .any(), .all() or not .empty, so pandas refuses to guess. That is why `and`, `or` and `if series:` raise ValueError.",
        topic="filtering", level=4),
    mcq("A pipeline does `X = df.drop(columns='target')` then `X['age'] = X['age'].fillna(0)`. Does this change `df`?",
        ["No: drop returns a new DataFrame, so writing to X doesn't touch df",
         "Yes: X is a view of df",
         "Yes, but only the age column",
         "It raises SettingWithCopyWarning and changes df"], 0,
        "drop builds a new object.",
        "drop returns a new frame that owns its data (or, under copy-on-write, shares it until written). Either way, assigning a column on X leaves df unchanged.",
        topic="copy-view", level=3),

    # ================================================================== round 2: depth (L3/L4)
    out("import pandas as pd\ndf = pd.DataFrame({\"a\": [1, 2, 3]})\ntop = df.iloc[:2]\ntop.iloc[0, 0] = 100\nprint(df[\"a\"].tolist())",
        ["[100, 2, 3]", "[1, 2, 3]", "SettingWithCopyError", "[100, 100, 3]"], 0,
        "Copy-on-write is off by default in pandas 2.2. Is a positional slice a view?",
        "A basic iloc slice of a single-dtype frame is a NumPy view, so without copy-on-write writing into `top` writes into df's memory too. "
        "People guess [1, 2, 3] because they think every selection copies. It's the same aliasing bug as two variables pointing at one mutable list. "
        "In a real pipeline, 'preview' code like this can quietly corrupt the source frame. Call .copy() when you mean a separate frame.",
        topic="copy-view", level=3,
        diagram="""df   ->  [ 1 | 2 | 3 ]   one buffer
top  ->  [ 1 | 2 ]       same memory (view)
top.iloc[0,0] = 100  ->  df sees 100 too""",
        analogy="Two JavaScript variables holding the same array: push through one and the other sees it."),
    tf("With copy-on-write turned on, `top = df.iloc[:2]` followed by `top.iloc[0, 0] = 100` also changes `df`.", False,
        "Under copy-on-write, which object does a write affect?",
        "Copy-on-write keeps the slice as a lazy view and copies the shared block the moment you write to `top`. So `top` becomes [100, 2] and df stays [1, 2, 3]. "
        "The rule is 'only the object you modify changes', and pandas 3.0 makes this the default. Code that relied on writing through a slice to edit the parent will silently stop doing so after the upgrade.",
        topic="copy-view", level=3),
    out("import pandas as pd\nwith pd.option_context(\"mode.copy_on_write\", True):\n    df = pd.DataFrame({\"a\": [1, 2, 3]})\n    arr = df[\"a\"].to_numpy()\n    arr[0] = 5\n    print(df[\"a\"].tolist())",
        ["ValueError", "[5, 2, 3]", "[1, 2, 3]", "ChainedAssignmentError"], 0,
        "Under copy-on-write, pandas can't let you write into its buffer behind its back.",
        "With copy-on-write, to_numpy() returns a zero-copy view of the column, and pandas marks it read-only. "
        "Otherwise you could change df through the array without pandas knowing, which breaks the CoW promise. NumPy raises ValueError: assignment destination is read-only. "
        "Use to_numpy(copy=True) (or np.array(...)) when an algorithm needs to mutate the array, e.g. an in-place shuffle before training.",
        topic="copy-view", level=4),
    out("import pandas as pd\ndf = pd.DataFrame({\"a\": [1, 2], \"b\": [3, 4]})\nv = df.values\nv[0, 0] = 99\nm = pd.DataFrame({\"a\": [1, 2], \"b\": [\"x\", \"y\"]})\nw = m.values\nw[0, 0] = 99\nprint(df.loc[0, \"a\"], m.loc[0, \"a\"])",
        ["99 1", "1 1", "99 99", "1 99"], 0,
        "One frame has a single dtype block; the other has to build an object array.",
        "With copy-on-write off (the 2.2 default), `.values` on an all-int64 frame can return a view of the single 2-D block, so the write reaches df. "
        "The mixed int/str frame has no single block to view, so pandas builds a fresh object array and the write goes nowhere. "
        "Whether you get a view depends on the dtypes, not the method name. That's why 'modify the result of .values' is never a safe way to edit a DataFrame.",
        topic="copy-view", level=4),
    mcq("Under copy-on-write, what happens here?\n\n`sub = df[df['a'] > 1]` then `sub['a'] = 0`",
        ["sub's column becomes 0, df is unchanged, and no warning is raised",
         "Both sub and df change, because sub is a view",
         "SettingWithCopyWarning is raised and df may or may not change",
         "ChainedAssignmentError is raised and nothing changes"], 0,
        "There is only one assignment, and it targets sub.",
        "With copy-on-write, `sub` behaves as its own object, so writing to it changes only `sub`. The old SettingWithCopyWarning (\"is this a view or a copy?\") goes away because the answer is always 'a copy, as far as you can tell'. "
        "The tempting answer is the warning, but that's pre-CoW behaviour. In practice this removes the need for defensive .copy() calls after filtering, while df[mask]['a'] = 0 (chained) still never updates df.",
        topic="copy-view", level=3),
    mcq("This line works in pandas 2.2 with default settings and fills df['a']. What happens with copy-on-write on (the pandas 3.0 default)?",
        ["df is unchanged: the inplace call fills a temporary Series; write df['a'] = df['a'].fillna(0) instead",
         "It still fills df['a'], because inplace=True always edits the parent",
         "It raises TypeError because inplace is removed",
         "It fills df['a'] and also every other column"], 0,
        "`df['a']` is a selection. What does copy-on-write say about modifying a selection?",
        "`df['a'].fillna(0, inplace=True)` is chained assignment in disguise: the first step selects a column and the second mutates that object. "
        "Without CoW the column Series happens to share memory with df, so the fill shows up. With CoW the Series is its own object, so df keeps its NaN. pandas 2.2 already warns (FutureWarning) about this pattern. "
        "This is one of the most common silent breakages when upgrading notebooks to pandas 3, so search your code for `inplace=True` on column selections.",
        code="import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({\"a\": [1.0, np.nan]})\ndf[\"a\"].fillna(0, inplace=True)",
        topic="copy-view", level=4),
    out("import pandas as pd\ns = pd.Series([1, 2, 3], index=[\"a\", \"b\", \"a\"])\nprint(s.loc[\"a\":\"b\"].tolist())",
        ["KeyError", "[1, 2]", "[1, 2, 3]", "[2, 3]"], 0,
        "Where does a label slice start when the start label appears twice and the index isn't sorted?",
        "A label slice needs one start position and one end position. With 'a' at positions 0 and 2 in an unsorted index there is no single start, so pandas raises KeyError: cannot get left slice bound for non-unique label. "
        "[1, 2] is what you'd guess if pandas used the first 'a'. It refuses to guess instead. "
        "Duplicate labels often sneak in after concat without ignore_index. Check df.index.is_unique, or sort_index() (a sorted index with duplicates can be sliced).",
        topic="loc-iloc", level=4,
        diagram="""pos:    0    1    2
label: 'a'  'b'  'a'
         ^         ^
   left bound for 'a' = 0 or 2?  -> KeyError"""),
    mcq("`df` has index [0, 1]. What does `df.loc[[0, 5], 'v']` do?",
        ["Raises KeyError, because label 5 is not in the index",
         "Returns the value for 0 and NaN for 5",
         "Returns only the row for label 0",
         "Treats 5 as a position and raises IndexError"], 0,
        "Older pandas filled missing labels with NaN. What changed in pandas 1.0?",
        "Since pandas 1.0, loc with a list that contains any missing label raises KeyError instead of quietly inserting NaN rows. "
        "If you really want 'NaN where missing' (like a LEFT JOIN against a list of ids), say so with df.reindex([0, 5]). "
        "Being explicit matters in feature lookups: a typo'd id should fail loudly rather than add an all-NaN row to your training data.",
        code="import pandas as pd\ndf = pd.DataFrame({\"v\": [10, 20]})\nprint(df.reindex([0, 5])[\"v\"].tolist())",
        topic="loc-iloc", level=3),
    tf("`df.iloc[df['v'] > 1]` works exactly like `df.loc[df['v'] > 1]`.", False,
        "iloc is position-based. A boolean Series carries labels.",
        "iloc refuses a boolean Series, because a Series brings an index that iloc can't use. You get NotImplementedError (\"iLocation based boolean indexing on an integer type is not available\"). "
        "Pass a plain array instead: df.iloc[(df['v'] > 1).to_numpy()]. Or use loc, which aligns the mask by label. "
        "The tempting belief is that 'a mask is a mask'. The difference is a reminder that loc aligns and iloc doesn't.",
        topic="loc-iloc", level=4),
    mcq("You need column 'b' for every row from the 2nd one onward, by position, on a frame with string row labels. Which line is correct?",
        ["df.iloc[1:, df.columns.get_loc('b')]",
         "df.iloc[1:, 'b']",
         "df.loc[1:, 'b']",
         "df.ix[1:, 'b']"], 0,
        "iloc wants positions on BOTH axes.",
        "iloc accepts only integers, slices and boolean arrays, so turn the column name into its position with df.columns.get_loc('b'). df['b'].iloc[1:] works too. "
        "df.iloc[1:, 'b'] raises because 'b' isn't a position, and df.loc[1:, 'b'] fails because 1 isn't a label in a string index. .ix was removed in pandas 1.0. "
        "Mixing label and position lookups explicitly like this avoids bugs when the index later changes from RangeIndex to ids.",
        topic="loc-iloc", level=3),
    out("import pandas as pd\na = pd.Series([1, 2], index=[\"x\", \"y\"])\nb = pd.Series([1, 2], index=[\"y\", \"x\"])\nprint((a == b).tolist())",
        ["ValueError", "[True, True]", "[False, False]", "[True, False]"], 0,
        "Arithmetic aligns. Do comparison operators?",
        "`+` and `-` align on labels, but `==`, `<` and friends on two Series require identically-labelled Series (same labels in the same order), otherwise ValueError: Can only compare identically-labeled Series objects. "
        "pandas refuses to silently reorder a comparison you'll probably use as a mask. "
        "Use a.eq(b), which aligns first, or compare a.sort_index() with b.sort_index() when you mean 'same values per label'.",
        topic="index-alignment", level=3),
    out("import pandas as pd\na = pd.Series([1, 2], index=[\"x\", \"y\"])\nb = pd.Series([2, 1], index=[\"y\", \"x\"])\nprint(a.eq(b).tolist(), a.equals(b), (a + b).tolist())",
        ["[True, True] False [2, 4]", "[False, False] False [3, 3]", "[True, True] True [2, 4]", "ValueError"], 0,
        "eq and + align by label; equals is stricter.",
        "a.eq(b) aligns first: x is 1 vs 1 and y is 2 vs 2, so both are True. `+` aligns the same way: [2, 4]. "
        "equals() compares the objects as stored, element by element in position order with the index included, so the reordered b is not 'equal'. "
        "In tests, use pd.testing.assert_series_equal(a, b.reindex(a.index)) when order shouldn't matter. Otherwise a reordered but correct result fails the test.",
        topic="index-alignment", level=4),
    mcq("`a` has integer labels 0, 1. `b` came from a JSON payload and has string labels '0', '1'. What is `a + b`?",
        ["4 rows, all NaN: 0 and '0' are different labels, so nothing aligns",
         "2 rows with the element-wise sums, since the labels look the same",
         "TypeError, because the index types differ",
         "2 rows, all NaN"], 0,
        "Alignment compares labels with ==. Is 0 == '0' in Python?",
        "Alignment is an outer join on the index, and the int 0 never equals the string '0'. The result has the union of the labels (four of them) and every value is NaN. "
        "There's no error, so the bug shows up later as a column of NaN. It's the same as joining an INT key to a VARCHAR key in a database that doesn't cast. "
        "Normalise index dtypes at the boundary (b.index = b.index.astype(int)) whenever data arrives from JSON, CSV or an API.",
        code="import pandas as pd\na = pd.Series([1, 2], index=[0, 1])\nb = pd.Series([10, 20], index=[\"0\", \"1\"])\nr = a + b\nprint(len(r), int(r.isna().sum()))",
        topic="index-alignment", level=4,
        analogy="Like a SQL join on user_id where one table stores it as INT and the other as VARCHAR: no rows match."),
    out("import pandas as pd\nimport numpy as np\na = pd.Series([1.0, np.nan], index=[\"x\", \"y\"])\nb = pd.Series([10.0], index=[\"x\"])\nprint(a.add(b, fill_value=0).tolist())",
        ["[11.0, nan]", "[11.0, 0.0]", "[11.0, 10.0]", "[11.0, 1.0]"], 0,
        "fill_value fills a label that is missing on ONE side. What about a NaN that is already there?",
        "For y, b has no label, so fill_value=0 stands in for b. But a's own value at y is NaN, and NaN + 0 is still NaN. "
        "fill_value only patches holes created by alignment, not existing missing values. The tempting [11.0, 0.0] assumes it fills NaN everywhere. "
        "When summing per-user totals from two sources, fillna(0) both sides first if a missing value really means zero.",
        topic="index-alignment", level=4),
    mcq("How can you make pandas fail fast when a step in your pipeline introduces duplicate row labels?",
        ["df = df.set_flags(allows_duplicate_labels=False): operations that would create duplicates raise DuplicateLabelError",
         "pd.options.mode.unique_index = True",
         "df.index.is_unique = True",
         "There's no way; you must call df.index.duplicated().any() after every step"], 0,
        "It's a per-object flag, not a global option.",
        "set_flags(allows_duplicate_labels=False) marks the frame, and pandas raises DuplicateLabelError if the frame has, or would get, duplicate labels (for example via a concat or loc enlargement that propagates the flag). "
        "is_unique is a read-only property, and the option doesn't exist. "
        "It works like a UNIQUE constraint on a primary key, and it's handy at the top of a feature pipeline where duplicate ids would silently double-count rows.",
        code="import pandas as pd\ns = pd.Series([1, 2], index=[\"a\", \"b\"]).set_flags(allows_duplicate_labels=False)\nprint(s.flags.allows_duplicate_labels)",
        topic="index-alignment", level=4,
        analogy="A UNIQUE constraint on the primary key column, enforced at write time."),
    # ------------------------------------------------------------------ ml-features
    mcq("A feature frame has two numeric columns and one forgotten text column. What does `X = df.to_numpy()` give you?",
        ["A single array of dtype object, so every number becomes a Python object and most models fail or crawl",
         "An array with the text column dropped automatically",
         "A float64 array with NaN in place of the text",
         "One NumPy array per column, each with its own dtype"], 0,
        "A NumPy array has exactly one dtype.",
        "to_numpy() must find one dtype that fits every column. int + float gives float64, but adding any str column forces object. "
        "scikit-learn then either raises 'could not convert string to float' or runs slowly on boxed Python objects. "
        "Check X.dtypes, or build X with select_dtypes / an explicit column list, before converting. That one-line check catches a surprising number of 'my model won't train' bugs.",
        code="import pandas as pd\ndf = pd.DataFrame({\"a\": [1, 2], \"b\": [0.5, 1.5]})\nprint(df.to_numpy().dtype, df.assign(c=[\"x\", \"y\"]).to_numpy().dtype)",
        topic="ml-features", level=3),
    out("import pandas as pd\ndf = pd.DataFrame({\"a\": [1], \"b\": [True], \"c\": [1.5], \"d\": [\"x\"]})\nprint(df.select_dtypes(\"number\").columns.tolist())",
        ["['a', 'c']", "['a', 'b', 'c']", "['a', 'b', 'c', 'd']", "['c']"], 0,
        "Is bool a 'number' in pandas' dtype hierarchy?",
        "select_dtypes('number') matches integer and float dtypes, but bool is a separate kind and is excluded. Python says True + 1 == 2, which tempts people towards ['a', 'b', 'c']. "
        "If your numeric-feature list is built this way, boolean flags like is_premium silently drop out of the model. "
        "Use select_dtypes(include=['number', 'bool']) or list the features explicitly.",
        topic="ml-features", level=3),
    out("import pandas as pd\nfrom sklearn.model_selection import train_test_split\ndf = pd.DataFrame({\"x\": range(10), \"y\": range(10)})\nXtr, Xte, ytr, yte = train_test_split(df[[\"x\"]], df[\"y\"], test_size=0.3, random_state=0)\nXtr = Xtr.reset_index(drop=True)\nboth = pd.concat([Xtr, ytr], axis=1)\nprint(both.shape, int(both[\"y\"].isna().sum()))",
        ["(9, 2) 2", "(7, 2) 0", "(14, 2) 7", "ValueError"], 0,
        "train_test_split keeps the original row labels. Which of the two did you renumber?",
        "Xtr now has labels 0..6, while ytr keeps the shuffled original labels (a subset of 0..9). concat(axis=1) aligns on labels: the union has 9 labels, and the two labels only Xtr has get NaN in y. "
        "Worse, the rows that do line up pair x with the wrong y. "
        "Reset both or neither. Mixing them is a classic way to train on scrambled labels and get a mysteriously useless model.",
        topic="ml-features", level=4,
        diagram="""Xtr (reset): 0 1 2 3 4 5 6
ytr (orig) : 9 1 6 7 3 0 5      <- labels, not positions
concat aligns labels -> 0..6 plus 9, 7 = 9 rows
x and y now paired by label, not by sample"""),
    mcq("A model was fit on a DataFrame with columns ['a', 'b']. At serving time the request builds a frame with columns ['b', 'a']. What does scikit-learn 1.6 do on predict?",
        ["Raises ValueError: the feature names must be in the same order as during fit",
         "Reorders the columns automatically by name",
         "Silently predicts using the columns by position (b as a)",
         "Warns and drops the extra ordering information"], 0,
        "The estimator stored feature_names_in_. Does it reorder or check?",
        "Since scikit-learn 1.2, an estimator fitted on a DataFrame records feature_names_in_, and predict raises ValueError if the names, or their order, differ. It checks but doesn't fix. "
        "That's lucky: silently using positions would apply a's weight to b. "
        "In a service, align explicitly with X = X[model.feature_names_in_] (or reindex) before predict, like a typed API contract.",
        code="import pandas as pd\nfrom sklearn.linear_model import LinearRegression\nX = pd.DataFrame({\"a\": [1.0, 2.0, 3.0], \"b\": [0.0, 1.0, 0.0]})\nm = LinearRegression().fit(X, [1.0, 2.0, 3.0])\nprint(m.feature_names_in_.tolist())",
        topic="ml-features", level=4),
    tf("If a scikit-learn model was fit on a DataFrame, calling `predict` with a plain NumPy array of the same shape raises an error.", False,
        "A NumPy array has no column names to check.",
        "It only warns ('X does not have valid feature names') and then uses the columns by position. That's exactly the dangerous case: the names check can't protect you, so a column-order bug goes straight into predictions. "
        "Keep DataFrames all the way to predict, or keep the column order in one place (a saved feature list) and enforce it.",
        topic="ml-features", level=3),
    mcq("What does `StandardScaler().set_output(transform='pandas').fit_transform(X)` return when X is a DataFrame with index [10, 20]?",
        ["A DataFrame with the same column names and the same index [10, 20]",
         "A NumPy array, because scalers always return arrays",
         "A DataFrame with columns 0, 1 and a fresh RangeIndex",
         "A dict of column name -> scaled array"], 0,
        "set_output was added so pipelines can stay in pandas.",
        "By default transformers return NumPy arrays and lose the column names. set_output(transform='pandas') (scikit-learn 1.2+) makes them return a DataFrame that keeps the names and the original index. "
        "Feature importances and debugging stay readable, and later pandas steps can still select by name. "
        "Because the index is kept, concatenating the output with other frames aligns correctly.",
        code="import pandas as pd\nfrom sklearn.preprocessing import StandardScaler\nX = pd.DataFrame({\"a\": [1.0, 3.0], \"b\": [2.0, 2.0]}, index=[10, 20])\nout = StandardScaler().set_output(transform=\"pandas\").fit_transform(X)\nprint(type(out).__name__, out.index.tolist(), out[\"a\"].tolist())",
        topic="ml-features", level=3),
    fill("At serving time, force a request frame to the training columns (same order, missing ones as 0, extra ones dropped): `X = X.____(columns=train_cols, fill_value=0)`",
        "reindex",
        "It conforms an axis to a given list of labels.",
        "reindex(columns=train_cols, fill_value=0) puts the columns in training order, adds any missing one-hot columns as 0 and drops unknown extras. "
        "That's the standard fix for 'test has a category train never saw' and 'test lacks a category train had'. Save train_cols with the model artifact so training and serving share one source of truth.",
        code="import pandas as pd\ntrain_cols = [\"age\", \"city_Goa\", \"city_Pune\"]\nreq = pd.DataFrame({\"city_Pune\": [1], \"age\": [30], \"city_Delhi\": [1]})\nprint(req.reindex(columns=train_cols, fill_value=0).values.tolist())",
        topic="ml-features", level=3,
        diagram="""request: city_Pune age city_Delhi
            \\       |      x  (unknown, dropped)
train  : age  city_Goa  city_Pune
         30     0 (new)     1"""),
    mcq("Why is `X, y = df.drop(columns='target'), df['target']` safer than building X and y from separate queries or separate CSV files?",
        ["They come from one frame with one index, so row i of X and row i of y describe the same sample",
         "drop is faster than selecting columns",
         "scikit-learn requires y to be named 'target'",
         "It automatically removes leakage columns"], 0,
        "What keeps a feature row and its label together?",
        "X and y split from the same frame share the index, so every later filter, sort or split can be applied to both consistently. Two separate queries can return rows in different orders (SQL without ORDER BY guarantees nothing), and the model then learns from mismatched pairs without any error. "
        "If you must load them separately, join them on an id first and assert the ids match.",
        topic="ml-features", level=3,
        analogy="Like selecting both columns in one SQL query instead of running two queries without ORDER BY and zipping the results."),
    # ------------------------------------------------------------------ dtypes-memory (round 2)
    out("import pandas as pd\nprint(pd.NA ** 0, pd.NA | True, pd.NA & False, pd.NA & True)",
        ["1 True False <NA>", "<NA> <NA> <NA> <NA>", "1 True False True", "TypeError"], 0,
        "pd.NA means 'unknown'. Is the result the same whatever the unknown value is?",
        "pd.NA follows three-valued (SQL-style) logic: when the answer is the same whatever the unknown value is, you get that answer. x**0 is always 1, unknown OR True is always True, and unknown AND False is always False. "
        "unknown AND True depends on the unknown, so it stays <NA>. "
        "That's exactly SQL's NULL truth table. If you expect NA to swallow everything you'll mispredict filters built from nullable boolean columns.",
        topic="dtypes-memory", level=4,
        diagram="""  AND  | True   False  NA
 ------+-------------------
  NA   |  NA    False   NA
  OR   | True   False  NA
 ------+-------------------
  NA   | True    NA     NA"""),
    out("import pandas as pd\ns = pd.Series([1, 2, None], dtype=\"Int64\")\nprint((s / 2).dtype, (s // 2).dtype, (s > 1).dtype)",
        ["Float64 Int64 boolean", "float64 int64 bool", "Float64 Float64 bool", "object Int64 boolean"], 0,
        "Nullable dtypes stay nullable through operations.",
        "True division can produce fractions, so Int64 / 2 becomes the nullable Float64 (capital F), floor division stays Int64, and a comparison gives the nullable boolean dtype with <NA> where the input was missing. "
        "The NumPy-flavoured answers (float64, bool) are what you'd get from int64 data. "
        "Once you opt into nullable dtypes the whole chain stays nullable, which is good for correctness. Some older libraries choke on Float64 and boolean, though, so convert at the model boundary.",
        topic="dtypes-memory", level=3),
    tf("On an object column with a None in it, `s.str.len()` returns float64, but on a `'string'` dtype column it returns the nullable `Int64`.", True,
        "Lengths are integers. What does each dtype family use for 'missing'?",
        "Object columns mark missing as NaN, and NaN can only live in a float column, so the lengths become float64 (1.0, 2.0, nan). The 'string' dtype uses pd.NA and returns Int64 lengths (1, 2, <NA>). "
        "It's a small difference until you use the lengths as dictionary keys or compare them to ints from another table.",
        code="import pandas as pd\no = pd.Series([\"a\", \"bb\", None])\nprint(o.str.len().dtype, o.astype(\"string\").str.len().dtype)",
        topic="dtypes-memory", level=3),
    mcq("What happens here, and what's the fix?",
        ["TypeError: 'z' is not one of the categories; call s.cat.add_categories('z') first (or work in object/string dtype)",
         "The value becomes 'z' and the category list grows automatically",
         "The value silently becomes NaN",
         "ValueError: categoricals are read-only"], 0,
        "A categorical's set of allowed values is part of its dtype.",
        "A category column is an integer code per row plus a fixed list of categories, and there is no code for 'z'. pandas raises TypeError: Cannot setitem on a Categorical with a new category. "
        "That strictness is a feature: it's how a category dtype behaves like a CHECK constraint or an enum column. "
        "In ML data prep, decide deliberately what to do with unseen values (map them to an 'other' category) rather than letting them sneak in.",
        code="import pandas as pd\ns = pd.Series([\"a\", \"b\"], dtype=\"category\")\ntry:\n    s[0] = \"z\"\nexcept TypeError:\n    print(\"TypeError\")",
        topic="dtypes-memory", level=3,
        analogy="Like inserting a value into a Postgres ENUM column that the enum type doesn't list."),
    out("import pandas as pd\na = pd.Series([\"x\", \"y\"], dtype=\"category\")\nb = pd.Series([\"y\", \"z\"], dtype=\"category\")\nc = pd.Series([\"x\", \"y\"], dtype=\"category\")\nprint(pd.concat([a, b]).dtype, pd.concat([a, c]).dtype)",
        ["object category", "category category", "object object", "category object"], 0,
        "concat keeps the category dtype only when the dtypes are identical.",
        "a and b have different category lists, so concat can't keep one categorical dtype and falls back to object. All the memory savings vanish without a warning. a and c have identical categories, so the result stays category. "
        "This bites when monthly files each get astype('category') separately. Fix it with a shared pd.CategoricalDtype(all_values), or pandas.api.types.union_categoricals.",
        topic="dtypes-memory", level=4),
    fill("To convert every column of a DataFrame to the best nullable dtype (Int64, string, boolean, Float64) in one call, use `df.____()`.",
        "convert_dtypes",
        "It's a single method that 'converts dtypes'.",
        "convert_dtypes() inspects each column and picks the nullable extension dtype that fits it: ints with missing values become Int64 instead of float64, text becomes string, and True/False/None becomes boolean. "
        "It's a quick way to stop None from upcasting ints after loading messy data.",
        code="import pandas as pd\ndf = pd.DataFrame({\"a\": [1, None], \"b\": [\"x\", None], \"c\": [True, None]})\nprint(df.convert_dtypes().dtypes.astype(str).tolist())",
        topic="dtypes-memory", level=3),
    mcq("You switch a 10-million-row text column from object to `dtype='string'` (the default python storage) to save memory. What happens?",
        ["Little or no saving: 'string[python]' still stores one Python str object per row; pyarrow-backed strings ('string[pyarrow]') are the compact option",
         "Memory drops about 8x because string dtype packs characters into one buffer",
         "Memory doubles because every value is stored twice",
         "It raises because string dtype needs a fixed width"], 0,
        "What does the 'python' in 'string[python]' refer to?",
        "The 'string' dtype gives you clear semantics: only strings or pd.NA, and Int64/boolean results from .str methods. With python storage it still holds an array of Python str objects, so memory_usage(deep=True) barely changes. "
        "pyarrow storage keeps all the characters in one contiguous buffer plus offsets, which is often several times smaller and faster. pandas 3.0 makes the pyarrow-backed str the default when pyarrow is installed. "
        "For low-cardinality text, category is still the biggest win.",
        topic="dtypes-memory", level=4),
    mcq("Which statement about `np.nan` vs `pd.NA` is correct?",
        ["np.nan is a float that is unequal to everything; pd.NA is a dtype-independent 'unknown' that propagates through comparisons (pd.NA == 1 is <NA>)",
         "They are the same object with two names",
         "pd.NA is just None, so pd.NA == None is True",
         "np.nan works in Int64 columns, pd.NA only in float columns"], 0,
        "Think of IEEE floats on one side and SQL NULL on the other.",
        "np.nan comes from IEEE floating point: it's a float, so ints with NaN become float64, and nan == nan is False. pd.NA is pandas' own missing marker for nullable dtypes (Int64, boolean, string). Comparisons with it give <NA>, like SQL NULL, and bool(pd.NA) raises TypeError. "
        "Code that checks `x == x` to detect missing values breaks with pd.NA. Use pd.isna(x) everywhere.",
        topic="dtypes-memory", level=3),
    # ------------------------------------------------------------------ apply / filtering / multiindex / creating (round 2)
    out("import pandas as pd\ndf = pd.DataFrame({\"a\": [1, 2], \"b\": [0.5, 1.5]})\nprint(df.apply(lambda r: r[\"a\"], axis=1).tolist())\ndf[\"c\"] = [\"x\", \"y\"]\nprint(df.apply(lambda r: r[\"a\"], axis=1).tolist())",
        ["[1.0, 2.0]\n[1, 2]", "[1, 2]\n[1, 2]", "[1.0, 2.0]\n[1.0, 2.0]", "[1, 2]\n['1', '2']"], 0,
        "apply(axis=1) hands your function each row as a Series. What dtype must that Series have?",
        "Each row is packed into one Series, which needs one dtype. With int and float columns the row is float64, so r['a'] is 1.0. Once a str column joins, the row has to be object, and the original int survives as 1. "
        "So the same lambda returns different types depending on unrelated columns. "
        "It's one more reason (besides speed) to use column-wise vectorised code. An ID column read through apply(axis=1) can quietly become 1.0 and then fail a dictionary lookup.",
        topic="apply-vectorise", level=4),
    mcq("A teammate wraps a Python function with `np.vectorize(f)` and applies it to a 5-million-row column, saying it is now vectorised. Is it as fast as `df['a'] * 2`?",
        ["No: np.vectorize is a convenience loop that still calls f once per element in Python",
         "Yes: np.vectorize compiles f to C",
         "Yes, as long as f only uses arithmetic",
         "No, it's slower because it runs on the GPU"], 0,
        "Read the NumPy docs' note on np.vectorize performance.",
        "np.vectorize only gives f broadcasting semantics. Under the hood it's essentially a for loop, so it runs at Series.apply speed, about 100x slower than real array ops. "
        "True vectorisation means expressing the logic with whole-array operations: arithmetic, np.where/np.select, .str/.dt methods, map with a dict. "
        "Interviewers like this one because the name misleads so many people.",
        topic="apply-vectorise", level=3,
        analogy="Like calling a stored procedure once per row from your app versus one set-based UPDATE: the wrapper's name doesn't change the round-trips."),
    fill("Inside `df.query(...)`, a column name that contains a space (like unit price) must be wrapped in ____.",
        "backticks",
        "It's the same character Markdown uses for inline code.",
        "query parses its string as an expression, so `unit price` must be quoted with backticks: df.query('`unit price` > 5'). Plain quotes would make it a string literal. "
        "It's similar to quoting an identifier with spaces in SQL (\"unit price\" in Postgres, `unit price` in MySQL). Renaming columns to snake_case at load time avoids the issue.",
        code="import pandas as pd\ndf = pd.DataFrame({\"unit price\": [4, 8, 12]})\nprint(df.query(\"`unit price` > 5\").shape)",
        topic="filtering", level=3),
    out("import pandas as pd\nimport numpy as np\ns = pd.Series([1.0, np.nan])\nprint(s.isin([np.nan]).tolist(), (s == np.nan).tolist())",
        ["[False, True] [False, False]", "[False, False] [False, False]", "[False, True] [False, True]", "TypeError"], 0,
        "isin uses hashing, not ==.",
        "`== np.nan` is always False, because NaN is unequal to itself under IEEE rules. isin works like a hash-set lookup, and pandas' hash table treats all NaNs as the same key, so NaN is found. "
        "The inconsistency is real: a filter written with isin([..., np.nan]) keeps missing rows, while the equivalent == chain drops them. "
        "When you mean missing, say so: s.isna() | s.isin(values).",
        topic="filtering", level=4),
    tf("Indexing an `Int64` Series with a boolean mask that contains `<NA>` (e.g. `s[s > 1]` where s has a missing value) raises ValueError.", False,
        "Object-dtype masks with NaN raise. Nullable boolean masks follow a different rule.",
        "Since pandas 1.0.2, a nullable boolean mask treats <NA> as False when indexing, so s[s > 1] on [1, <NA>, 3] returns [3]. "
        "An object-dtype mask holding NaN (say, from .str.contains on an object column) still raises ValueError. "
        "So the same filter code can work or crash depending on the column's dtype. Write .fillna(False) on masks when you can't control the dtype.",
        code="import pandas as pd\ns = pd.Series([1, None, 3], dtype=\"Int64\")\nprint(s[s > 1].tolist())",
        topic="filtering", level=4),
    mcq("`m` has a sorted (city, year) MultiIndex. Which expression selects the 'v' values for every city in 2024?",
        ["m.loc[pd.IndexSlice[:, 2024], 'v']",
         "m.loc[(:, 2024), 'v']",
         "m.loc[2024, 'v']",
         "m.loc[('*', 2024), 'v']"], 0,
        "You need a slice object for the outer level, and Python syntax doesn't allow a bare colon inside a tuple.",
        "pd.IndexSlice lets you write slices per level: idx[:, 2024] means 'all cities, year 2024'. `(:, 2024)` is a SyntaxError. m.loc[2024] looks 2024 up in the OUTER level (city) and raises KeyError, and '*' is just a literal label. "
        "m.xs(2024, level='year') is the other idiom. Slicing like this needs a lexsorted index, so call sort_index() first or pandas raises UnsortedIndexError.",
        code="import pandas as pd\ndf = pd.DataFrame({\"city\": [\"Goa\", \"Goa\", \"Pune\", \"Pune\"], \"year\": [2023, 2024, 2023, 2024], \"v\": [1, 2, 3, 4]})\nm = df.set_index([\"city\", \"year\"]).sort_index()\nprint(m.loc[pd.IndexSlice[:, 2024], \"v\"].tolist())",
        topic="multiindex", level=4,
        diagram="""city  year | v
Goa   2023 | 1
Goa   2024 | 2   <- idx[:, 2024]
Pune  2023 | 3
Pune  2024 | 4   <-"""),
    out("import pandas as pd\ndf = pd.DataFrame({\"city\": [\"Goa\", \"Goa\", \"Pune\"], \"year\": [2023, 2024, 2023], \"v\": [1, 2, 3]})\nm = df.set_index([\"city\", \"year\"])\nprint(m.loc[[\"Goa\", \"Pune\"]].shape, m.loc[[(\"Goa\", 2024), (\"Pune\", 2023)]].shape)",
        ["(3, 1) (2, 1)", "(2, 1) (2, 1)", "(3, 1) (3, 1)", "KeyError"], 0,
        "A list of plain labels matches the outer level; a list of tuples matches full keys.",
        "m.loc[['Goa', 'Pune']] picks every row whose OUTER label is Goa or Pune: all 3 rows. A list of tuples is a list of complete (city, year) keys, so exactly those 2 rows come back. "
        "A single tuple, m.loc[('Goa', 2024)], is one full key, which is why list-vs-tuple matters so much with a MultiIndex. "
        "It's like WHERE city IN (...) versus WHERE (city, year) IN (...).",
        topic="multiindex", level=3),
    tf("`unstack()` on an int64 Series whose (row, col) combinations are not all present keeps the int64 dtype.", False,
        "What goes in the missing cells?",
        "The missing combinations become NaN, and NaN forces float64, so the whole table turns float. Pass fill_value=0 (s.unstack(fill_value=0)) to keep integers when 'missing' really means zero, e.g. counts. "
        "Otherwise a count matrix used as model features quietly becomes floats with NaN, and many estimators reject the NaN.",
        code="import pandas as pd\ns = pd.Series([1, 2, 3], index=pd.MultiIndex.from_tuples([(\"a\", \"x\"), (\"a\", \"y\"), (\"b\", \"x\")]))\nprint(s.unstack().dtypes.astype(str).tolist(), s.unstack(fill_value=0)[\"y\"].tolist())",
        topic="multiindex", level=3),
    out("import io\nimport pandas as pd\ncsv = \"country\\nNA\\nIN\"\na = pd.read_csv(io.StringIO(csv))\nb = pd.read_csv(io.StringIO(csv), keep_default_na=False)\nprint(int(a[\"country\"].isna().sum()), int(b[\"country\"].isna().sum()))",
        ["1 0", "0 0", "1 1", "0 1"], 0,
        "'NA' is on read_csv's default list of missing-value markers.",
        "By default read_csv treats strings like 'NA', 'N/A', 'null', 'NaN' and '' as missing, so Namibia's ISO code 'NA' becomes NaN. keep_default_na=False turns that list off. You can then pass your own na_values=[''] if blanks should still be missing. "
        "The same trap hits a 'NULL' surname or an 'NA' (not applicable) answer that is a real category. Always check value_counts(dropna=False) on text columns after loading.",
        topic="creating", level=3),
    fill("A CSV has amounts written like \"1,234\". To parse them as integers, call `pd.read_csv(f, ____=\",\")`.",
        "thousands",
        "The parameter names the separator used between groups of digits.",
        "thousands=',' tells the parser to strip the grouping separator, so \"1,234\" becomes 1234 (int64) instead of the column staying object. For European files, combine thousands='.' with decimal=','. "
        "The alternative, cleaning the strings afterwards with .str.replace, is slower and easy to forget.",
        code="import io\nimport pandas as pd\ncsv = 'amount\\n\"1,234\"\\n5'\nprint(pd.read_csv(io.StringIO(csv), thousands=\",\")[\"amount\"].tolist())",
        topic="creating", level=3),
    mcq("A CSV column `flag` holds True/False, but one row is blank. What dtype does read_csv give it?",
        ["object: True, False and NaN mixed, because NumPy bool has no missing value",
         "bool, with the blank read as False",
         "boolean (nullable), with <NA> for the blank",
         "float64, with 1.0/0.0 and NaN"], 0,
        "Without the blank it would be bool. What can hold a NaN?",
        "A clean True/False column parses as bool. One blank means a missing value, NumPy bool can't hold NaN, and read_csv's default (NumPy-backed) parser falls back to object. "
        "The nullable 'boolean' answer is what you'd get with dtype={'flag': 'boolean'} or dtype_backend='numpy_nullable'. "
        "On an object column, df[df['flag']] raises ValueError because the mask contains NaN. That's how a single blank cell in a nightly file can break the training job.",
        code="import io\nimport pandas as pd\nclean = \"flag\\nTrue\\nFalse\"\ndirty = \"flag,x\\nTrue,1\\n,2\\nFalse,3\"\nprint(pd.read_csv(io.StringIO(clean))[\"flag\"].dtype, pd.read_csv(io.StringIO(dirty))[\"flag\"].dtype)",
        topic="creating", level=4),
    mcq("Loading a 5 GB CSV prints `DtypeWarning: Columns (7) have mixed types`. What is going on, and what is the proper fix?",
        ["The parser infers types chunk by chunk; column 7 looked numeric in some chunks and text in others, so it became object with mixed int/str values. Pass dtype={...} for that column",
         "Column 7 has too many rows; pass nrows=",
         "The file encoding is wrong; pass encoding='latin-1'",
         "It's harmless; pandas converts the whole column to float at the end"], 0,
        "With low_memory=True (the default) the C parser works in chunks.",
        "Type inference happens per chunk. If early chunks are all digits (zip codes 41001) and a later one has '41001-A', the column ends up object holding a mix of int and str. Then '41001' and 41001 never compare equal, and groupby splits one value into two keys. "
        "low_memory=False only hides the symptom by inferring once over the whole column. Declaring dtype={'zip': 'string'} states the contract, much like a schema in a database.",
        topic="creating", level=4,
        diagram="""chunk 1: 41001, 41002  -> int
chunk 2: 41003         -> int
chunk 3: '41001-A'     -> str
column = object [41001, 41002, 41003, '41001-A']
         41001 != '41001'  -> groupby splits keys"""),
    # ------------------------------------------------------------------ round 3: conceptual mix
    mcq("`s` is a Series of ages indexed by name (Ann, Bob). What does `'Ann' in s` check?",
        ["Whether 'Ann' is one of the index labels",
         "Whether 'Ann' is one of the values",
         "Whether 'Ann' appears in either the labels or the values",
         "Nothing: `in` raises ValueError on a Series"], 0,
        "A Series behaves a lot like a dict.",
        "Like a Python dict, `in` on a Series tests the keys (the index), not the values: 'Ann' in s is True but 30 in s is False even if 30 is an age. "
        "To test values, use `30 in s.values` or `s.isin([30]).any()`. A wrong membership check silently returns False and skips a branch you thought ran.",
        code="import pandas as pd\ns = pd.Series([30, 25], index=['Ann', 'Bob'])\nprint('Ann' in s, 30 in s, 30 in s.values)",
        analogy="dict membership: `'Ann' in {'Ann': 30}` is True, `30 in {'Ann': 30}` is False.",
        topic="series-vs-df", level=2),
    tf("`df.loc['r1']` on a DataFrame returns a Series whose index is the DataFrame's column names.", True,
        "One row, turned on its side.",
        "Selecting one row gives a 1-D Series: the column names become its index and the cells become its values. "
        "That is why row['age'] works on a row from loc or iterrows. It is the same idea as one record from a JSON array: keys are field names.",
        topic="series-vs-df", level=1),
    fill("The pandas function that loads a CSV file into a DataFrame is `pd.____('data.csv')`.",
        "read_csv",
        "read_... followed by the file format.",
        "pd.read_csv parses the file, uses the first line as column names and guesses a dtype for each column. "
        "Its siblings follow the same pattern: read_json, read_parquet, read_excel, read_sql.",
        topic="creating", level=1),
    mcq("You build `pd.DataFrame(records)` from API JSON where some records have no `email` key. What happens?",
        ["You get an email column with NaN in the rows whose record lacked the key",
         "pandas raises KeyError because the records have different keys",
         "The email column is dropped because not every record has it",
         "The missing emails are filled with empty strings"], 0,
        "pandas takes the union of all keys.",
        "From a list of dicts, the columns are the union of the keys; a record missing a key gets NaN in that cell. "
        "This is like a LEFT JOIN that leaves NULLs, not an error. Check df['email'].isna().sum() before you trust the column, because downstream code that expects strings will meet floats (NaN).",
        code="import pandas as pd\nrecords = [{'id': 1, 'email': 'a@x.io'}, {'id': 2}]\nprint(pd.DataFrame(records))",
        topic="creating", level=2),
    fill("A 3 GB CSV has 200 columns but your model needs 5. To parse only those, pass `pd.read_csv(path, ____=['a', 'b', 'c', 'd', 'e'])`.",
        "usecols",
        "Which columns to use.",
        "usecols skips the other columns during parsing, so they never take up memory or parse time. "
        "Loading everything and then doing df[cols] still pays the full cost first.",
        analogy="SELECT a, b FROM t instead of SELECT * FROM t and throwing columns away in the app.",
        topic="creating", level=2),
    mcq("pandas 2.2, copy-on-write OFF (the default). You do `df = pd.DataFrame(arr)` with a 2-D float NumPy array, then `arr[0, 0] = 9`. What happens to df?",
        ["df changes too: the constructor wrapped the array without copying it",
         "df is unchanged: DataFrame() always copies its input",
         "NumPy raises because the array is now owned by pandas",
         "df changes only if you passed copy=True"], 0,
        "A single-dtype 2-D array can be used as the frame's data block as it is.",
        "Without CoW, DataFrame(ndarray) defaults to copy=False and the frame shares the array's memory, so writes to arr show up in df (this prints 9.0). "
        "With pd.options.mode.copy_on_write = True (the pandas 3.0 default) the constructor copies NumPy input by default and df stays 0. "
        "If you need isolation in 2.2, pass copy=True or build from arr.copy().",
        code="import numpy as np\nimport pandas as pd\narr = np.zeros((2, 2))\ndf = pd.DataFrame(arr)\narr[0, 0] = 9\nprint(df.iloc[0, 0])",
        diagram="""no CoW:  arr --+--> [ 9. 0. | 0. 0. ]
         df  --+     (one shared buffer)

CoW:     arr ----> [ 9. 0. | 0. 0. ]
         df  ----> [ 0. 0. | 0. 0. ]  (own copy)""",
        topic="creating", level=4),
    mcq("You run `df['city'].value_counts()` on a column with 40 missing values. Where are those 40 rows in the result?",
        ["Not shown: value_counts drops NaN unless you pass dropna=False",
         "In a row labelled NaN at the top",
         "Counted under the most common city",
         "In a row labelled 'None'"], 0,
        "Many pandas counting methods skip missing values by default.",
        "value_counts() has dropna=True, so the counts add up to the non-missing rows only. Pass dropna=False to see a NaN row. "
        "It's easy to report 'Pune is 60% of users' when you actually divided by the non-null count, so check how many rows are missing before you trust the percentages.",
        topic="inspecting", level=2),
    tf("For `s = pd.Series(['a', 'b', None, 'a'])`, `s.nunique()` is 2 but `len(s.unique())` is 3.", True,
        "One of them has a dropna default.",
        "nunique() defaults to dropna=True and ignores the missing value; unique() returns every distinct value including None. "
        "Use nunique(dropna=False) when a missing value should count as its own category, for example when sizing a one-hot encoding.",
        topic="inspecting", level=3),
    mcq("`df.info()` ends with `memory usage: 164.0+ bytes`. What does the `+` mean?",
        ["Object columns were counted only as 8-byte pointers, so the real size is larger; use memory_usage='deep'",
         "The frame is still growing and info() could not finish measuring",
         "The index is excluded from the total",
         "pandas rounded the number up to the nearest kilobyte"], 0,
        "What does a column of Python strings actually store in its array?",
        "An object column stores pointers to Python objects. By default info() counts only the pointers and marks the total with + to say it is a lower bound. "
        "df.info(memory_usage='deep') or df.memory_usage(deep=True) also measures the string objects, often several times more. Use the deep number when you size a container or a batch job.",
        code="import pandas as pd\ndf = pd.DataFrame({'t': ['a', 'bb'], 'n': [1, 2]})\ndf.info()",
        topic="inspecting", level=3),
    mcq("A column is named `unit price` (with a space). Which line selects it?",
        ["df['unit price']",
         "df.unit price",
         "df.unit_price",
         "df.loc['unit price']"], 0,
        "Dot access only works for names that are valid Python identifiers.",
        "Square brackets accept any column label. Dot access needs a valid identifier (no spaces, no leading digit, not a method name like count). "
        "df.unit_price is a different name and raises AttributeError, and df.loc['unit price'] looks for a row label. Use brackets in production code; dot access is a notebook shortcut.",
        topic="selecting", level=2),
    fill("To keep every column EXCEPT the numeric ones (e.g. to list the text columns you still have to encode), write `df.select_dtypes(____='number')`.",
        "exclude",
        "select_dtypes takes two keyword arguments: one to keep, one to drop.",
        "select_dtypes(include=...) keeps the matching dtypes and select_dtypes(exclude=...) drops them. "
        "A quick `df.select_dtypes(exclude='number').columns` before training lists the object/category/bool columns a model can't take raw. "
        "Remember bool is not 'number' here, so bool columns show up in the exclude list.",
        topic="selecting", level=3),
    tf("`df.iloc[0, 'price']` reads the price of the first row.", False,
        "iloc wants positions on BOTH axes.",
        "iloc is position-only, so a column name raises ValueError. Write df['price'].iloc[0], df.loc[df.index[0], 'price'], or df.iloc[0, df.columns.get_loc('price')]. "
        "Mixing a label and a position in one call is a very common first-week bug; pick one system per call.",
        topic="loc-iloc", level=2),
    tf("`df.at['r1', 'price']` reads one cell faster than `df.loc['r1', 'price']`, but it cannot take slices or lists.", True,
        "at and iat exist for exactly one cell.",
        "at (labels) and iat (positions) skip the general indexing machinery that loc/iloc need for slices, lists and masks, so a single read or write is cheaper. "
        "Passing a slice to at raises. If you're calling at in a hot loop, though, the real fix is usually to vectorise the loop.",
        topic="loc-iloc", level=3),
    mcq("A script builds a frame row by row: `for r in rows: df.loc[len(df)] = r`. With 3,000 rows it takes about 2 seconds; with 100,000 it seems to hang. Why, and what is the fix?",
        ["Each enlargement reallocates and copies the whole frame, so the loop is O(n^2); collect rows in a list and call pd.DataFrame(rows) once",
         "len(df) is slow on big frames; keep a counter instead",
         "loc is slower than iloc; use df.iloc[len(df)] = r",
         "The index isn't sorted; call sort_index() inside the loop"], 0,
        "A DataFrame's columns are fixed-size NumPy arrays.",
        "NumPy arrays can't grow in place, so every new row means new arrays plus a copy of all existing rows: quadratic time. "
        "Appending dicts to a Python list is O(1) each, and one DataFrame(rows) call builds the arrays once; in a quick test that was about 500x faster for 3,000 rows. "
        "iloc can't enlarge at all (IndexError).",
        analogy="Like running one INSERT per row with a full table rewrite each time, instead of a single bulk insert.",
        topic="loc-iloc", level=3),
    tf("`df[df['age'] > 30]` removes the younger rows from df.", False,
        "Did you assign the result anywhere?",
        "Boolean filtering returns a NEW DataFrame with the matching rows; df itself keeps every row. "
        "Write adults = df[df['age'] > 30] (or reassign df = ...) to keep the result. Like a SQL SELECT ... WHERE, a filter reads, it doesn't DELETE.",
        topic="filtering", level=1),
    mcq("`df[df['name'].str.contains('a')]` raises `ValueError: Cannot mask with non-boolean array containing NA / NaN values`. What's the clean fix?",
        ["Pass na=False: df[df['name'].str.contains('a', na=False)]",
         "Wrap the mask in bool(): df[bool(df['name'].str.contains('a'))]",
         "Use `and` instead of the mask",
         "Call df.dropna() on the whole frame first"], 0,
        "What does str.contains return for a missing name?",
        "On an object column, str.contains gives NaN for missing values, and a mask with NaN in it isn't a valid boolean mask. "
        "na=False says 'treat missing as not matching'. dropna() on the whole frame would also throw away rows that are missing in other, unrelated columns.",
        code="import numpy as np\nimport pandas as pd\ndf = pd.DataFrame({'name': ['apple', np.nan, 'kiwi']})\nprint(df['name'].str.contains('a').tolist())\nprint(df[df['name'].str.contains('a', na=False)])",
        topic="filtering", level=3),
    mcq("After `f = df[df['v'] > 2]`, the index of f is [0, 2]. Your next line is `f.loc[1]`, meaning 'the second row'. What happens?",
        ["KeyError: label 1 was filtered out; use f.iloc[1] or f.reset_index(drop=True) first",
         "It returns the second row (label 2)",
         "It returns row 1 from the original df",
         "It returns an empty DataFrame"], 0,
        "Filtering keeps the original row labels.",
        "A filter keeps the surviving rows' labels, leaving gaps (0, 2). loc looks up label 1, which is gone, so it raises KeyError. "
        "For 'the nth row' use iloc; if you want 0..n-1 labels again (for example before concatenating with a NumPy result) call reset_index(drop=True).",
        diagram="""df            f = df[df.v > 2]
label  v      label  v
  0    5        0    5    <- iloc[0]
  1    1        2    7    <- iloc[1]
  2    7      (label 1 no longer exists)""",
        topic="filtering", level=2),
    mcq("Your API passes a user-supplied city into a filter. Which version should you ship?",
        ["df.query('city == @city')",
         "df.query(f\"city == '{city}'\")",
         "df.query('city == ' + city)",
         "eval(f\"df[df.city == '{city}']\")"], 0,
        "What happens when city is \"O'Brien Nagar\"?",
        "@city passes the Python variable as a value, so quotes or odd characters in it can't break the expression. "
        "Pasting the value into the string with an f-string fails on an apostrophe (a tokenizer error) and, like SQL built by string concatenation, lets input change the expression itself. "
        "For a plain equality, df[df['city'] == city] is just as safe.",
        analogy="@var is a bound parameter in a prepared SQL statement; the f-string is string-concatenated SQL.",
        code="import pandas as pd\ndf = pd.DataFrame({'city': [\"O'Brien Nagar\", 'Pune']})\ncity = \"O'Brien Nagar\"\nprint(df.query('city == @city').shape)",
        topic="filtering", level=3),
    mcq("Which line removes the column `tmp` from df and keeps the result?",
        ["df = df.drop(columns='tmp')",
         "df.drop('tmp')",
         "df = df.drop('tmp')",
         "del df.tmp"], 0,
        "Two things to get right: which axis, and keeping the result.",
        "drop(columns=...) says you mean a column, and the assignment keeps the new frame. "
        "df.drop('tmp') looks for a ROW labelled 'tmp' (KeyError) and throws the result away anyway; del df.tmp tries to delete an attribute (del df['tmp'] would work).",
        topic="modifying", level=1),
    tf("`sort_values` puts NaN at the end both when ascending and when `ascending=False`.", True,
        "Missing values don't take part in the comparison.",
        "na_position defaults to 'last' for both directions, so a descending sort does not bring NaN to the top. "
        "Pass na_position='first' to change it. This matters for 'top 10' reports: missing scores never appear in df.sort_values('score', ascending=False).head(10), so you may not notice how many there are.",
        topic="modifying", level=2),
    mcq("Events are already in time order. You run `df.sort_values('user_id')` and expect each user's events to stay in time order. Is that guaranteed?",
        ["No: the default kind='quicksort' isn't stable, so ties can be reordered; pass kind='stable' (or sort by ['user_id', 'ts'])",
         "Yes: pandas sorts are always stable",
         "Yes, but only if the index is a RangeIndex",
         "No, and there is no way to get a stable sort in pandas"], 0,
        "What does 'stable' mean for rows with equal keys?",
        "A stable sort keeps rows with equal keys in their original order. A single-column sort_values uses NumPy quicksort (an introsort), which doesn't promise that: in a 40-row test with two key values, the tied rows came out shuffled. "
        "kind='stable' (or 'mergesort') fixes it; sorting by both keys says what you mean even more clearly. Multi-column sorts are stable already. "
        "This bug looks like 'events out of order' in session features, and it only shows up on larger data.",
        diagram="""before:  (u1,t1) (u2,t1) (u1,t2) (u1,t3)
stable:  (u1,t1) (u1,t2) (u1,t3) (u2,t1)
quick:   (u1,t3) (u1,t1) (u1,t2) (u2,t1)  <- ties shuffled""",
        topic="modifying", level=4),
    fill("To remove rows that are exact repeats of an earlier row, call `df.____()`.",
        "drop_duplicates",
        "drop_... the repeats.",
        "drop_duplicates() keeps the first copy of each identical row by default (keep='first') and returns a new frame. "
        "Pass subset=['email'] to dedupe on a key instead of on the whole row, like SELECT DISTINCT vs a unique constraint on one column.",
        topic="modifying", level=2),
    mcq("`s` holds 'a', 'b', 'c'. You want 'a' turned into 1 and every other value left alone. Which call does that?",
        ["s.replace({'a': 1})",
         "s.map({'a': 1})",
         "s.map({'a': 1}, na_action='ignore')",
         "s.astype({'a': 1})"], 0,
        "One of these treats the dict as the complete lookup table.",
        "replace only changes the values it finds in the dict and keeps the rest, giving [1, 'b', 'c']. "
        "map treats the dict as the full mapping: any value not in it becomes NaN, so you'd get [1.0, NaN, NaN]. na_action='ignore' only skips values that were already missing. "
        "Use map for full lookups like encoding labels, and replace for patching a few values.",
        code="import pandas as pd\ns = pd.Series(['a', 'b', 'c'])\nprint(s.replace({'a': 1}).tolist(), s.map({'a': 1}).tolist())",
        topic="apply-vectorise", level=2),
    tf("On a default object-dtype column of strings, `s.str.lower()` runs about as fast as numeric vectorised math like `n * 2`, because .str methods are compiled C loops.", False,
        "What is stored in an object column?",
        "On object dtype, .str methods still call a Python string method once per element; they're tidier and NaN-safe, but in a 1M-row test str.lower took about 0.16 s, apply took 0.25 s and n * 2 took 0.007 s. "
        "Converting to 'string[pyarrow]' moved str.lower to about 0.035 s, because Arrow strings have real compiled kernels. "
        "So 'use .str instead of apply' is about clarity first; for big text columns the speed comes from the dtype.",
        topic="apply-vectorise", level=3),
    mcq("You must use `df.apply(f)` column-wise with a custom NumPy-only function. What does `df.apply(f, raw=True)` change?",
        ["f receives each column as a plain ndarray instead of a Series, skipping Series construction and index handling, which is often faster",
         "f runs in compiled C instead of Python",
         "f receives the whole frame at once as a 2-D array",
         "Nothing; raw only affects how the result is printed"], 0,
        "What object does f get with and without it?",
        "By default apply builds a Series (values + index + name) for every column or row it hands to f. raw=True passes the bare ndarray, which removes that cost and lets f use NumPy directly. "
        "f still runs once per column/row in Python, so it is not vectorisation; and f loses access to labels (no row['age']). "
        "It helps most with axis=1 on many rows, where building one Series per row dominates.",
        code="import pandas as pd\ndf = pd.DataFrame({'a': [1, 2, 3]})\nprint(df.apply(lambda c: type(c).__name__).tolist(), df.apply(lambda c: type(c).__name__, raw=True).tolist())",
        topic="apply-vectorise", level=4),
    mcq("What does `df.set_index('user_id')` do?",
        ["Returns a new frame where the user_id column becomes the row labels (and is no longer a regular column)",
         "Sorts df by user_id",
         "Adds a user_id column filled with 0, 1, 2, ...",
         "Changes df itself and returns None"], 0,
        "Think 'primary key'.",
        "set_index moves the column into the index, so you can then look rows up with df.loc[42] and arithmetic aligns on user_id. "
        "Like most pandas methods it returns a new frame, so write df = df.set_index('user_id'). It doesn't sort; call sort_index() if you need that.",
        analogy="Declaring user_id as the table's primary key: rows are now addressed by it.",
        topic="index-alignment", level=1),
    mcq("df has index [2, 0, 1]. Which statement about these two assignments is correct?\n`df['l'] = [10, 20, 30]` and `df['s'] = pd.Series([10, 20, 30])`",
        ["The list is placed by position; the Series is matched by label, so df['s'] becomes [30, 10, 20]",
         "Both are placed by position, giving [10, 20, 30] each",
         "Both are matched by label",
         "The Series assignment raises because the index order differs"], 0,
        "Only one of the two has labels.",
        "A list or ndarray has no index, so it is written top to bottom. A Series brings labels 0, 1, 2, and pandas aligns them with df's labels 2, 0, 1, so label 2 gets 30. "
        "This bites after a sort or a filter: assign model.predict(X) (an ndarray) and it lands by position; assign a Series built elsewhere and it lands by label, with NaN for labels it lacks.",
        code="import pandas as pd\ndf = pd.DataFrame({'a': [1, 2, 3]}, index=[2, 0, 1])\ndf['l'] = [10, 20, 30]\ndf['s'] = pd.Series([10, 20, 30])\nprint(df)",
        diagram="""label | list (by position) | Series (by label)
  2   |        10          |   s[2] = 30
  0   |        20          |   s[0] = 10
  1   |        30          |   s[1] = 20""",
        topic="index-alignment", level=3),
    mcq("You want to centre each ROW of a numeric df (subtract that row's mean from every cell). Which line is correct?",
        ["df.sub(df.mean(axis=1), axis=0)",
         "df - df.mean(axis=1)",
         "df - df.mean()",
         "df.sub(df.mean(axis=1))"], 0,
        "By default, a Series is lined up with the columns.",
        "df - series matches the Series' labels against the COLUMN names. Row means are labelled by row (0, 1, ...), so df - df.mean(axis=1) gives an all-NaN frame with extra columns. "
        "axis=0 tells sub to match the Series against the index instead. df - df.mean() is valid but centres each column, which is a different thing.",
        topic="index-alignment", level=3),
    fill("To get both Series reindexed to their shared labels only (an inner join on the index) in one call, write `a2, b2 = a.____(b, join='inner')`.",
        "align",
        "The verb for what pandas does silently before arithmetic.",
        "align returns both objects reindexed to a common index: join='outer' (union, what + uses), 'inner', 'left' or 'right'. "
        "Making it explicit lets you check len(a2) and catch a key mismatch before it turns into NaNs, the same way you'd check row counts after a SQL join.",
        topic="index-alignment", level=4),
    tf("`df2 = df` makes a copy, so changing df2 leaves df unchanged.", False,
        "Python assignment never copies objects.",
        "Assignment only binds a second name to the same object, just like `b = a` with a JS object or a Python list. Any change through df2 is a change to df. "
        "Use df2 = df.copy() when you need an independent frame.",
        analogy="Two variables holding the same object reference, like `const b = a` for a JS object.",
        topic="copy-view", level=1),
    mcq("pandas 2.2 with `pd.options.mode.copy_on_write = True`. You run `df['a'][0] = 5`. What happens?",
        ["df is unchanged, and pandas emits a ChainedAssignmentError warning telling you to use df.loc[0, 'a'] = 5",
         "df['a'][0] becomes 5, exactly as with CoW off",
         "It raises SettingWithCopyError and stops the script",
         "df['a'] becomes 5 in every row"], 0,
        "Under CoW, df['a'] behaves as a brand-new object.",
        "With CoW, df['a'] acts like a separate Series; writing into it can never reach df, so chained assignment never works. pandas 2.2 detects the pattern and warns with ChainedAssignmentError (a Warning, not an exception). "
        "With CoW off, 2.2 still updates df but warns with a FutureWarning that this changes in 3.0. Either way the fix is one indexing call: df.loc[0, 'a'] = 5.",
        diagram="""df['a'][0] = 5
 \\_____/ \\___/
  step 1  step 2: writes into step 1's result
CoW: step 1 is a new object -> df never changes
fix: df.loc[0, 'a'] = 5   (one call, writes to df)""",
        topic="copy-view", level=4),
    mcq("A `price` column read from a scraped file holds strings like '12.5', '7' and 'N/A'. `astype(float)` raises. Which call turns the good values into numbers and the junk into NaN?",
        ["pd.to_numeric(df['price'], errors='coerce')",
         "df['price'].astype(float, errors='ignore')",
         "pd.to_numeric(df['price'], errors='raise')",
         "df['price'].astype('Int64')"], 0,
        "One option means 'force it, and mark failures as missing'.",
        "errors='coerce' converts what it can and makes unparseable values NaN, giving a float64 column. errors='raise' (the default) fails like astype; astype(errors='ignore') returns the original strings unchanged. "
        "Afterwards, count the new NaNs (and look at a few raw values) so a format change in the source doesn't quietly turn half the column into NaN.",
        code="import pandas as pd\ns = pd.Series(['12.5', '7', 'N/A'])\nprint(pd.to_numeric(s, errors='coerce').tolist())",
        topic="dtypes-memory", level=2),
    fill("To shrink an int64 column of small numbers to the smallest integer dtype that fits (e.g. int8), call `pd.to_numeric(s, ____='integer')`.",
        "downcast",
        "The opposite of upcasting.",
        "downcast='integer' picks the smallest of int8/int16/int32/int64 that holds every value, so [1, 2, 3] becomes int8: 1 byte per value instead of 8. "
        "Unlike astype('int8'), it checks the range first, so it never wraps large values around. 'float' and 'unsigned' work the same way.",
        topic="dtypes-memory", level=3),
    mcq("`size` is a plain (unordered) category column with values 'S', 'M', 'L'. What does `df[df['size'] > 'M']` do?",
        ["Raises TypeError: unordered categoricals only support == and !=",
         "Keeps 'L' rows, because pandas knows S < M < L",
         "Keeps rows that sort after 'M' alphabetically ('S')",
         "Returns an empty frame"], 0,
        "Does pandas know that S < M < L just from the strings?",
        "An unordered categorical has no ranking, so <, > and sorting by meaning aren't defined and pandas raises TypeError. "
        "Declare the order: pd.CategoricalDtype(['S', 'M', 'L'], ordered=True). Then > 'M' keeps L, and sort_values sorts S, M, L instead of alphabetically (L, M, S). "
        "The same idea is useful for ordinal features like education level.",
        code="import pandas as pd\nt = pd.CategoricalDtype(['S', 'M', 'L'], ordered=True)\ns = pd.Series(['S', 'L', 'M']).astype(t)\nprint((s > 'M').tolist(), s.sort_values().tolist())",
        topic="dtypes-memory", level=4),
    tf("`df.groupby(['city', 'year'])['sales'].sum()` returns a Series whose index is a MultiIndex of (city, year) pairs.", True,
        "Each result row needs both keys to identify it.",
        "Grouping by two keys gives one result per (city, year) combination, so pandas labels the result with a two-level index. "
        "That's why m.loc['Pune'] works on it afterwards. If you want flat columns (for a CSV, a chart or a model), call .reset_index() or pass as_index=False to groupby.",
        diagram="""groupby(['city','year']).sum()
city  year    sales
Goa   2023      3
      2024      1
Pune  2024      2
(city, year) = 2-level row labels""",
        topic="multiindex", level=3),
    mcq("Training used `pd.get_dummies(train)` on a `city` column with Goa, Pune and Delhi. At serving time a request batch contains only Pune. What goes wrong?",
        ["The batch gets only a city_Pune column, so the columns don't match the model; reindex to the saved training columns with fill_value=0",
         "Nothing; get_dummies remembers the training categories",
         "get_dummies raises because Goa and Delhi are missing",
         "The batch gets all three columns but filled with NaN"], 0,
        "get_dummies only sees the data you pass it right now.",
        "get_dummies makes one column per value present in THIS frame, so a small batch produces fewer (and differently ordered) columns, and scikit-learn rejects it (or, with NumPy input, silently misreads it). "
        "Save train_cols = X_train.columns and do X.reindex(columns=train_cols, fill_value=0), or use a fitted OneHotEncoder(handle_unknown='ignore'), which keeps the training categories.",
        analogy="Like an API whose response schema changes depending on which rows the query happened to return.",
        topic="ml-features", level=3),
    mcq("Before splitting, a notebook runs `df['age'] = df['age'].fillna(df['age'].mean())`, then `train_test_split`. What is the problem?",
        ["Leakage: the mean includes the test rows, so test data influences training; compute the mean on the training split only and reuse it for test",
         "None; the mean is the same either way",
         "fillna doesn't work before a split",
         "It changes the dtype of age to object"], 0,
        "Which rows went into that mean?",
        "Any statistic you learn from the data (means, scaler parameters, category lists) must be fitted on the training split only and then applied to the test split, or your test score is optimistic. "
        "Here the effect is small, but the same pattern with target encoding or scaling can inflate metrics a lot. "
        "In practice, put SimpleImputer in a Pipeline so fit only ever sees training data.",
        diagram="""wrong:  mean(all rows) -> fill -> split
                  ^ test rows leak in
right:  split -> m = mean(train)
               -> train.fillna(m), test.fillna(m)""",
        topic="ml-features", level=4),
    tf("`X = df[['b', 'a']]` gives X with columns in the order b, a, even if df stores them as a, b.", True,
        "The list you pass is a request, in order.",
        "Selecting with a list returns the columns in the list's order. That makes df[train_cols] a simple way to force serving data into the training column order. "
        "It also means a hand-typed list in a different order quietly gives a different X.",
        topic="ml-features", level=2),
    mcq("A team encodes city as `X['city'] = X['city'].astype('category').cat.codes`, separately on the training data (Goa, Pune) and on each serving batch. Why do predictions go wrong?",
        ["Codes depend on which values are in each frame: in a batch of only Pune, Pune gets code 0, which meant Goa in training",
         "cat.codes returns strings, which models can't use",
         "Codes are random on every run",
         "astype('category') drops rows that are new"], 0,
        "Codes come from the sorted list of categories found in that frame.",
        "astype('category') builds its category list from the values present, so the same city can get different codes in different frames. Nothing raises; the model just reads the wrong city. "
        "Save the training categories and reuse them: astype(pd.CategoricalDtype(train_cats)). An unseen city then gets code -1, which you can handle on purpose.",
        code="import pandas as pd\ntrain = pd.Series(['Goa', 'Pune']).astype('category').cat.codes.tolist()\nbatch = pd.Series(['Pune']).astype('category').cat.codes.tolist()\nprint(train, batch)",
        diagram="""train:  Goa -> 0   Pune -> 1
batch:  Pune -> 0          (only Pune present)
model reads 0 as Goa  -> wrong feature, no error
fix:    astype(CategoricalDtype(['Goa', 'Pune']))""",
        topic="ml-features", level=4),
    mcq("pandas 2.2: `s = pd.Series([1, None], dtype='Int64')`. What does `s.to_numpy()` return?",
        ["A float64 array [1.0, nan]",
         "An object array [1, <NA>]",
         "An int64 array, with the missing value as 0",
         "It raises because pd.NA can't go into NumPy"], 0,
        "This changed in pandas 2.2.",
        "Since 2.2, to_numpy() on nullable numeric dtypes picks a matching NumPy dtype: int64 when nothing is missing, float64 with NaN when something is. Before 2.2 it gave an object array of pd.NA, which broke NumPy and scikit-learn code. "
        "Nullable boolean with a missing value still gives object. In shared code, be explicit: s.to_numpy(dtype='float64', na_value=np.nan).",
        code="import pandas as pd\ns = pd.Series([1, None], dtype='Int64')\nprint(s.to_numpy(), s.to_numpy().dtype)",
        topic="dtypes-memory", level=4),
    # ---- round 3 pass 2: conceptual mcq/tf/fill
    mcq("Which call shows the LAST 3 rows of a DataFrame?",
        ["df.tail(3)",
         "df.head(-3)",
         "df[-3]",
         "df.iloc[3]"], 0,
        "head looks at the top; what looks at the bottom?",
        "tail(n) returns the last n rows, the mirror of head(n). head(-3) means 'everything EXCEPT the last 3 rows', the opposite of what you want. df[-3] looks for a COLUMN labelled -3 and raises KeyError, and iloc[3] is the single row at position 3. "
        "Checking the tail of a freshly loaded file catches footer junk like 'Total' rows or a truncated last line.",
        topic="inspecting", level=1),
    tf("`df['price'].mean()` returns a single number, not a Series.", True,
        "One column in, one summary out.",
        "df['price'] is a Series, and reducing a Series with mean(), sum() or max() gives one scalar (a NumPy float64). Calling df.mean(numeric_only=True) on the whole DataFrame instead returns a Series: one mean per column, indexed by column name. "
        "Knowing which one you have tells you whether you can format it with f'{x:.2f}' or need to pick a column first.",
        topic="series-vs-df", level=1),
    fill("To see the column names of a DataFrame, look at `df.____` (no parentheses).",
        "columns",
        "It's an attribute, the column counterpart of df.index.",
        "df.columns is an Index object holding the column labels; df.columns.tolist() gives a plain list. It's also assignable: df.columns = ['a', 'b'] renames every column at once (the list must have the right length). "
        "Printing it right after loading catches stray spaces like 'price ' that make df['price'] raise KeyError.",
        topic="selecting", level=1),
    mcq("How do you rename the column `amt` to `amount` and keep the result?",
        ["df = df.rename(columns={'amt': 'amount'})",
         "df.rename('amt', 'amount')",
         "df['amount'] = df.rename('amt')",
         "df = df.rename({'amount': 'amt'})"], 0,
        "A dict maps OLD name to NEW name, and the method returns a new frame.",
        "rename takes a mapping {old: new} passed as columns=, and returns a new DataFrame that you assign back. The second option raises TypeError (rename takes a mapping, not two names), and even a valid call there would throw its result away. The last option has the mapping backwards and, without columns=, tries to rename ROW labels, so nothing visible happens. "
        "Like ALTER TABLE ... RENAME COLUMN, except pandas gives you a new table instead of changing the old one.",
        topic="modifying", level=1),
    mcq("Which line keeps every row whose city is NOT 'Pune'?",
        ["df[df['city'] != 'Pune']",
         "df[df['city'] is not 'Pune']",
         "df[not df['city'] == 'Pune']",
         "df.drop('Pune')"], 0,
        "Comparison operators work element-wise on a column.",
        "!= compares every value and returns a True/False mask; df[mask] keeps the True rows. 'is not' checks whether the whole Series is the same object as the string (always True), so it's not a mask at all. 'not' tries to turn the whole Series into one bool and raises ValueError. drop('Pune') looks for a row LABEL 'Pune'. "
        "SQL: WHERE city <> 'Pune' (careful: rows where city is NaN are kept by != but dropped by SQL's <>).",
        topic="filtering", level=1),
    mcq("You save a cleaned DataFrame with `df.to_csv('clean.csv')` and load it back. There's a new column `Unnamed: 0`. How do you avoid it?",
        ["Save with df.to_csv('clean.csv', index=False), since the 0..n-1 index isn't real data",
         "Load with pd.read_csv('clean.csv', header=None)",
         "Rename the column after loading every time",
         "It's a bug in read_csv; upgrade pandas"], 0,
        "to_csv writes one extra thing by default.",
        "to_csv writes the index as the first column by default, with an empty header, and read_csv names that column 'Unnamed: 0'. index=False skips it. If the index IS meaningful (user ids), keep it and load with index_col=0 instead. "
        "header=None would treat the header row as data. Many 'mystery feature' columns in ML datasets are just a saved RangeIndex.",
        topic="creating", level=1),
    tf("`df.iloc[0]` returns the first row of the table even when the index labels are something like [105, 7, 42].", True,
        "iloc never looks at labels.",
        "iloc is purely positional: position 0 is whatever row is physically first, here the one labelled 105. df.loc[0] would look for the LABEL 0 and raise KeyError on this index. "
        "After sorting or filtering, labels and positions no longer agree, so choose deliberately: loc for 'the row with id 42', iloc for 'the first row'.",
        diagram="""
position:   0     1    2
label:     105    7   42
iloc[0] -> position 0 -> row 105
loc[0]  -> label 0    -> KeyError""",
        topic="loc-iloc", level=1),
    mcq("You need a `price_with_tax` column equal to price x 1.18 for 2 million rows. Which is the idiomatic pandas way?",
        ["df['price_with_tax'] = df['price'] * 1.18",
         "df['price_with_tax'] = [p * 1.18 for p in df['price']]",
         "for i in range(len(df)): df.loc[i, 'price_with_tax'] = df.loc[i, 'price'] * 1.18",
         "df['price_with_tax'] = df['price'].apply(lambda p: p * 1.18)"], 0,
        "Let the whole column do the math at once.",
        "Arithmetic on a Series is vectorised: one compiled loop over the whole array, typically 50-100x faster than Python-level loops. The list comprehension and apply call Python once per value, and the loc loop is the slowest of all, since every assignment goes through indexing machinery. "
        "Like one UPDATE t SET price_with_tax = price * 1.18 instead of 2 million single-row updates.",
        topic="apply-vectorise", level=1),
    mcq("You build `pd.DataFrame({'a': [5, 6, 7]})` without giving an index. What are the row labels?",
        ["0, 1, 2: a RangeIndex",
         "1, 2, 3",
         "5, 6, 7, taken from the first column",
         "There are no row labels"], 0,
        "pandas numbers rows the way Python numbers list items.",
        "Without index=, pandas creates a RangeIndex starting at 0. It's cheap (stored as start/stop/step, not as an array) and it's what df.reset_index(drop=True) gives you back. "
        "Every row always has a label. That label, not the position, is what pandas uses to line up rows in arithmetic and assignment, which is the source of many surprises later.",
        topic="index-alignment", level=1),
    fill("To see the dtype of every column at once (int64, float64, object...), look at `df.____`.",
        "dtypes",
        "Plural of dtype.",
        "df.dtypes is a Series mapping each column name to its dtype; s.dtype (singular) is for one Series. df.info() shows the same plus non-null counts and memory. "
        "Check it right after loading: a numeric column that shows object usually hides a stray string like 'N/A' or '1,200'.",
        topic="dtypes-memory", level=1),
    mcq("A CSV export is sorted by signup date. Why is `df.sample(10, random_state=0)` a better first look than `df.head(10)`?",
        ["head only shows the oldest rows, which can hide problems that appear later in the file; sample draws rows from everywhere, and random_state makes it repeatable",
         "sample is faster than head",
         "head modifies the DataFrame",
         "sample returns the 10 most typical rows"], 0,
        "What do the first 10 rows of a sorted file have in common?",
        "In a file sorted by date, id or region, the top rows are not representative: a format change in 2024, a new category or a column that only fills in later won't show in head(). sample picks random rows, and random_state=0 gives the same rows on every run, so a notebook stays reproducible. "
        "It's like checking a few random log lines from across the day instead of only the first minute after a deploy.",
        topic="inspecting", level=2),
    mcq("A config lists optional columns. What does `df.get('discount')` return when df has no 'discount' column?",
        ["None (or the default you pass as the second argument), instead of raising KeyError",
         "KeyError, like df['discount']",
         "An empty Series",
         "A column of NaN"], 0,
        "DataFrame behaves like a dict of columns here.",
        "DataFrame.get works like dict.get: it returns the column if it exists, otherwise None or the default you pass (df.get('discount', 0)). df['discount'] raises KeyError. "
        "Handy for optional fields in loosely structured data, but in a training pipeline a missing feature column should usually fail loudly rather than silently become None.",
        topic="selecting", level=2),
    mcq("Which line selects columns `b` and `c` only for the rows where `a > 1`?",
        ["df.loc[df['a'] > 1, ['b', 'c']]",
         "df.iloc[df['a'] > 1, ['b', 'c']]",
         "df[df['a'] > 1, ['b', 'c']]",
         "df.loc[['b', 'c'], df['a'] > 1]"], 0,
        "loc takes [rows, columns], and the row part can be a mask.",
        "loc accepts a boolean mask for rows and a list of labels for columns in one call. That's one clean selection, and the same form (df.loc[mask, 'b'] = 0) is the safe way to ASSIGN. iloc takes positions, not names. Plain df[...] with a tuple looks for a column called (mask, list). The last option has rows and columns swapped. "
        "SQL: SELECT b, c FROM df WHERE a > 1.",
        topic="loc-iloc", level=2),
    tf("`df[df['email'] != None]` keeps only the rows that have an email.", False,
        "How does pandas compare values to None?",
        "pandas treats None in a comparison like a missing value, so every element compares as 'not equal' and the mask is all True: you keep every row, including the missing ones. (== None gives all False.) Use df[df['email'].notna()]. "
        "The same goes for == np.nan. Missing values are tested with isna/notna, just as SQL needs IS NULL instead of = NULL.",
        code="import pandas as pd\ne = pd.Series(['a@x', None, 'b@x'])\nprint((e != None).tolist(), e.notna().tolist())",
        topic="filtering", level=2),
    mcq("A city column mixes old and new names. Which line turns every 'Bombay' into 'Mumbai' and leaves other values alone?",
        ["df['city'] = df['city'].replace({'Bombay': 'Mumbai'})",
         "df['city'] = df['city'].map({'Bombay': 'Mumbai'})",
         "df['city'] = df['city'].rename({'Bombay': 'Mumbai'})",
         "df['city'].str.replace('Bombay', 'Mumbai')"], 0,
        "One of these turns every unmapped value into NaN.",
        "replace swaps only the values found in the dict and keeps everything else. map with a dict looks up EVERY value, so all cities not in the dict become NaN, a classic data-loss bug. rename changes index labels, not values. The last line computes a result but never assigns it (and it would also change 'Bombay Central' inside longer strings). "
        "Use map when the dict covers every value (encoding), replace when it's a partial fix-up.",
        topic="modifying", level=2),
    fill("To label each temperature in one vectorised call, write `df['band'] = np.____(df['t'] > 30, 'hot', 'ok')`.",
        "where",
        "NumPy's element-wise if/else.",
        "np.where(condition, value_if_true, value_if_false) evaluates the condition for every row at once and picks one of the two values, replacing an apply with an if/else inside. For more than two outcomes, use np.select with a list of conditions. "
        "It's the CASE WHEN t > 30 THEN 'hot' ELSE 'ok' END of pandas.",
        topic="apply-vectorise", level=2),
    tf("After `df = df.set_index('user_id')`, `user_id` is still available as a normal column too.", False,
        "Check the drop= default of set_index.",
        "set_index moves the column into the index (drop=True by default), so df['user_id'] now raises KeyError. You reach it as df.index or with df.loc[42]. Pass drop=False to keep a copy as a column, or reset_index() to move it back. "
        "Code that later does df['user_id'] or merge(on='user_id') breaks after this, so many teams keep ids as columns and only set an index where they need fast label lookups.",
        topic="index-alignment", level=2),
    mcq("A 50-million-row feature frame has 40 float64 columns. Roughly how much memory do you save by converting them all to float32?",
        ["About half: each value goes from 8 bytes to 4, so roughly 16 GB becomes 8 GB",
         "Nothing, because pandas stores floats compressed",
         "About 90%",
         "It doubles memory because of the conversion"], 0,
        "float64 = 64 bits; float32 = 32 bits.",
        "Numeric columns are plain arrays: 50M rows x 40 columns x 8 bytes is about 16 GB, and float32 halves that. You lose precision (about 7 significant digits instead of 15-16), which is usually fine for model features (many GPU frameworks train in float32 anyway) but not for money or ids. "
        "The conversion briefly needs both copies in memory, so convert column by column or set dtype= at load time.",
        topic="dtypes-memory", level=2),
    mcq("Why do you usually drop a `user_id` column from X before training, even though it's numeric?",
        ["An id is an arbitrary label: the model may learn spurious patterns (for example, later signups have bigger ids), which won't generalise to new users",
         "scikit-learn refuses integer columns",
         "ids always contain missing values",
         "Dropping columns makes training more accurate in general"], 0,
        "Does user 50,001 have '1 more' of anything than user 50,000?",
        "The numeric value of an id carries no meaning, but it often correlates with time (auto-increment) or source system, so a tree model can split on it and look good offline. New users at serving time have ids outside the training range. "
        "Keep the id in the DataFrame for joining and debugging, but build X with df.drop(columns=['user_id', 'target']) or an explicit feature list.",
        topic="ml-features", level=2),
    tf("`pd.read_csv` turns a column of ISO dates like '2024-01-15' into datetime64 automatically.", False,
        "Check df.dtypes after loading.",
        "By default read_csv leaves date strings as object; you have to ask: pd.read_csv(path, parse_dates=['signup']) (plus date_format= when you know the format), or convert afterwards with pd.to_datetime. "
        "Until then, .dt raises AttributeError and comparisons like df['signup'] > '2024-01-01' compare strings, which only works by luck for ISO formats.",
        code="import io\nimport pandas as pd\ncsv = 'signup\\n2024-01-15'\nprint(pd.read_csv(io.StringIO(csv)).dtypes.iloc[0], pd.read_csv(io.StringIO(csv), parse_dates=['signup']).dtypes.iloc[0])",
        topic="creating", level=2),
    mcq("With copy-on-write on (opt-in in pandas 2.2, the default in 3.0), a helper receives `df`. Which change inside the helper is STILL visible to the caller?",
        ["df['x'] = 1 on the df argument itself, because the caller holds the very same object",
         "sub = df[['a']]; sub.loc[0, 'a'] = 99",
         "d2 = df.reset_index(drop=True); d2.loc[0, 'a'] = 99",
         "None of them; CoW makes every function argument a private copy"], 0,
        "CoW is about objects DERIVED from df, not about df itself.",
        "Copy-on-write guarantees that any object you derive from df (a selection, a method result) behaves as an independent copy, so writing to sub or d2 never touches df. But the argument df is the caller's object, not a derived one, so adding or changing a column on it mutates the caller's frame, exactly like a list passed into a function. "
        "So under CoW the defensive df = df.copy() at the top of every helper is mostly unnecessary, and costs memory. The clean style is to not mutate inputs at all: return df.assign(x=1).",
        analogy="Like passing a JavaScript object into a function: reassigning or spreading it is safe, but setting obj.x = 1 changes the caller's object.",
        code="import pandas as pd\nwith pd.option_context('mode.copy_on_write', True):\n    df = pd.DataFrame({'a': [1, 2]})\n    sub = df[['a']]\n    sub.loc[0, 'a'] = 99\n    df['x'] = 1\n    print(df['a'].tolist(), df.columns.tolist())",
        topic="copy-view", level=3),
    tf("`df.loc[df['a'] > 1, 'flag'] = 1` on a frame without a `flag` column creates it, with NaN in the rows where the mask is False.", True,
        "Only some rows get a value. What do the others hold?",
        "Assigning through loc to a new column label creates the column; rows outside the mask have no value, so they get NaN, and the NaN makes the column float64 (1.0 rather than 1). "
        "If you want 0/1 flags, initialise first (df['flag'] = 0, then the loc assignment) or write it in one go: df['flag'] = (df['a'] > 1).astype(int).",
        code="import pandas as pd\ndf = pd.DataFrame({'a': [1, 2, 3]})\ndf.loc[df['a'] > 1, 'flag'] = 1\nprint(df['flag'].tolist(), df['flag'].dtype)",
        topic="loc-iloc", level=3),
    mcq("You compute `m = f['v'] > 2` on a FILTERED frame `f = df[df['v'] > 1]` and then run `df[m]` on the original. What happens in pandas 2.2?",
        ["It raises IndexingError ('Unalignable boolean Series'), because the mask has no entry for some of df's labels",
         "It keeps the first len(m) rows of df",
         "It fills the missing mask labels with False and works silently",
         "It works because masks are applied by position"], 0,
        "A boolean Series mask is matched to rows by LABEL.",
        "pandas aligns a boolean Series to the frame's index. m has labels only for the rows that survived the first filter, so labels in df that are missing from m can't be decided, and pandas raises IndexingError (after a UserWarning about reindexing). It never silently treats missing labels as False. "
        "Fix it by building the mask on the same frame you filter, or combine conditions up front: df[(df['v'] > 1) & (df['v'] > 2)].",
        topic="filtering", level=3),
    mcq("`codes` is a Series of 'P', 'G'. `lookup = pd.Series({'P': 'Pune', 'G': 'Goa'})`. What does `codes.map(lookup)` do?",
        ["Uses lookup's INDEX as the keys and its values as results, like a dict, giving 'Pune'/'Goa', and NaN for codes not in the index",
         "Pairs codes and lookup by position",
         "Raises TypeError, because map only accepts dicts and functions",
         "Returns lookup unchanged"], 0,
        "A Series is a labelled mapping, just like a dict.",
        "map accepts a dict, a function or a Series. With a Series it matches each value against lookup's index and returns the matching value, so a dimension table stored as a Series (indexed by code) works as a fast lookup. Unknown codes become NaN, as with a dict. "
        "It's a one-column LEFT JOIN: df['city'] = df['code'].map(cities.set_index('code')['name']). If the lookup index has duplicates, map raises (InvalidIndexError), unlike merge, which would duplicate rows.",
        code="import pandas as pd\nlookup = pd.Series({'P': 'Pune', 'G': 'Goa'})\nprint(pd.Series(['G', 'P', 'X']).map(lookup).tolist())",
        topic="apply-vectorise", level=3),
    tf("Adding two DataFrames with columns ['x', 'y'] and ['y', 'z'] gives a result with columns x, y and z, where x and z are all NaN.", True,
        "Alignment happens on BOTH axes.",
        "DataFrame arithmetic aligns rows by index and columns by name, taking the union of both. Only y exists in both frames, so only y gets numbers; x and z have a partner missing and become NaN. "
        "Use a.add(b, fill_value=0) to treat the missing side as 0, or select the shared columns first. In a feature pipeline this silently turns typos in column names into NaN columns.",
        code="import pandas as pd\na = pd.DataFrame({'x': [1], 'y': [2]})\nb = pd.DataFrame({'y': [10], 'z': [20]})\nprint((a + b).columns.tolist(), (a + b).values.tolist())",
        topic="index-alignment", level=3),
    fill("To get Arrow-backed result dtypes like int64[pyarrow] and string[pyarrow] straight from read_csv (not just the Arrow parser), pass `pd.read_csv(path, ____='pyarrow')`.",
        "dtype_backend",
        "It chooses the backend of the dtypes, not the engine.",
        "dtype_backend='pyarrow' makes every column an Arrow-backed dtype: integers with missing values stay integers, and strings are stored compactly. dtype_backend='numpy_nullable' gives Int64/string/boolean instead. engine='pyarrow' is a different option: it only swaps in a faster multithreaded parser, and by default still returns NumPy dtypes. "
        "You can combine both for large files.",
        topic="dtypes-memory", level=3),
    mcq("`s` is a sales Series with a (city, year) MultiIndex. Which line gives total sales per year across all cities?",
        ["s.groupby(level='year').sum()",
         "s.sum(axis='year')",
         "s.loc['year'].sum()",
         "s.unstack().sum()"], 0,
        "Group by an index level instead of a column.",
        "groupby(level=...) groups by one level of the index, here year, and sums over the other level. sum(axis=...) on a Series has only one axis. s.loc['year'] looks for a CITY called 'year'. s.unstack().sum() puts years in columns and sums each column, so it gives the same numbers but takes a detour and builds a wide table first. "
        "SQL: SELECT year, SUM(sales) FROM t GROUP BY year.",
        code="import pandas as pd\ns = pd.DataFrame({'city': ['P', 'P', 'G'], 'year': [2023, 2024, 2024], 'v': [1, 2, 3]}).set_index(['city', 'year'])['v']\nprint(s.groupby(level='year').sum().to_dict())",
        topic="multiindex", level=3),
    mcq("A new dataset has 300 columns. Why is `df.nunique().sort_values()` a useful early check?",
        ["Columns with 1 distinct value carry no information, and columns with about as many distinct values as rows are ids or free text; both usually need dropping or special handling",
         "It counts the missing values per column",
         "It finds duplicate rows",
         "It shows which columns are numeric"], 0,
        "Think about both ends of the sorted list.",
        "nunique per column (NaN excluded by default) shows the cardinality profile at a glance. 1 means a constant column, useless to a model. Close to len(df) means an id, timestamp or free text, which leaks or overfits if used as a category. Low counts are candidates for category dtype or one-hot encoding. "
        "It's the pandas version of SELECT COUNT(DISTINCT col) for every column of a new table.",
        diagram="""
col          nunique
country           1   <- constant: drop
plan              4   <- category / one-hot
age              70   <- numeric feature
user_id     100000    <- id: not a feature (rows = 100000)""",
        topic="inspecting", level=3),
    mcq("`pd.DataFrame({'a': 1, 'b': 2})` raises ValueError: 'If using all scalar values, you must pass an index'. Why, and what's the fix?",
        ["With only scalars pandas can't tell how many rows to make; pass index=[0], or wrap it as a list of one record: pd.DataFrame([{'a': 1, 'b': 2}])",
         "Column values must always be strings",
         "Dicts can't be used to build DataFrames",
         "The column names must be integers"], 0,
        "A scalar can be broadcast, but to what length?",
        "Scalars are broadcast to the length of the other columns. When EVERY value is a scalar, there's no length to broadcast to, so pandas asks for an index. A list of dicts (one per row) is the natural shape for a single JSON record, for example a serving request. "
        "pd.DataFrame([payload]) is the usual one-liner for turning one API request into a one-row feature frame.",
        topic="creating", level=3),
    fill("To keep only the columns whose names start with 'feat_', write `df.filter(____='^feat_')`.",
        "regex",
        "filter can match names by substring, by exact list or by pattern.",
        "DataFrame.filter selects COLUMNS (or rows with axis=0) by label: items= for an exact list, like= for a substring, regex= for a pattern. It never looks at the values, despite the name. "
        "A naming convention like feat_* plus filter(regex=...) is a cheap way to keep the feature list in sync with the frame, though an explicit saved list of training columns is safer for serving.",
        topic="selecting", level=3),
    mcq("You take `s = df['a']`, then write `df.loc[0, 'a'] = 9`. What is `s` afterwards in pandas 2.2 with default settings, and with copy-on-write on?",
        ["[9, 2, 3] by default (s is a view on df's memory), [1, 2, 3] with CoW (the write to df makes df copy first, so s keeps the old data)",
         "[1, 2, 3] in both cases",
         "[9, 2, 3] in both cases",
         "[1, 2, 3] by default, [9, 2, 3] with CoW"], 0,
        "CoW protects in BOTH directions: parent to child and child to parent.",
        "Without CoW, selecting a column returns a Series that shares memory with df, so an in-place write to df shows through s (and vice versa). With CoW, df and s share memory only until one of them is written to. The write to df first copies the data, so s keeps the snapshot it was created with. "
        "Code that keeps a reference to a column and relies on it 'updating itself' silently breaks when you upgrade to pandas 3.0. Re-select the column after changes instead of caching it.",
        diagram="""
before write:   df['a'] --\\
                           >--  [1, 2, 3]   (shared buffer)
                s ---------/
default 2.2:    df.loc[0,'a']=9 writes the shared buffer -> s sees 9
CoW:            df copies first -> df [9,2,3], s still [1,2,3]""",
        analogy="Like a git branch: both point at the same commit until one side commits a change.",
        code="import pandas as pd\ndf = pd.DataFrame({'a': [1, 2, 3]})\ns = df['a']\ndf.loc[0, 'a'] = 9\nwith pd.option_context('mode.copy_on_write', True):\n    df2 = pd.DataFrame({'a': [1, 2, 3]})\n    s2 = df2['a']\n    df2.loc[0, 'a'] = 9\n    print(s.tolist(), s2.tolist())",
        topic="copy-view", level=4),
    mcq("A `country` column with 200 distinct values over 10 million rows is converted to `category`. What dtype are the codes, and why does that matter?",
        ["int16: pandas picks the smallest signed integer that fits (int8 only for fewer than 127 categories, since -1 is kept for NaN), so 10M rows cost about 20 MB of codes",
         "int8, because there are fewer than 256 categories",
         "int64, like every pandas integer",
         "object, because the categories are strings"], 0,
        "Signed int8 tops out at 127, and one code is reserved.",
        "Codes are signed so that -1 can mean missing. int8 is used only up to 126 categories, int16 up to 32,766, then int32. 200 categories therefore cost 2 bytes per row plus one small array of the 200 strings, compared with roughly 50-60 bytes per row for object strings. "
        "Past a few hundred thousand distinct values the codes reach int32 and the categories array itself gets big, so the savings shrink. Categoricals pay off for low-cardinality columns, not for ids.",
        code="import pandas as pd\nprint(pd.Categorical([str(i) for i in range(126)]).codes.dtype, pd.Categorical([str(i) for i in range(200)]).codes.dtype)",
        topic="dtypes-memory", level=4),
    mcq("`df['qty']` is int64. In pandas 2.2 you run `df.loc[:, 'qty'] = [1.5, 2.5]`. What happens, and how does it differ from `df['qty'] = [1.5, 2.5]`?",
        ["loc tries to write into the existing int64 column: 2.2 upcasts it to float64 with a FutureWarning ('Setting an item of incompatible dtype is deprecated'), and pandas 3.0 raises; df['qty'] = ... simply replaces the column with a new float64 one",
         "Both silently truncate the values to 1 and 2",
         "Both raise TypeError in 2.2",
         "loc replaces the column; df['qty'] = ... writes in place"], 0,
        "One form means 'set these values in the existing array', the other 'swap in a new column'.",
        "df.loc[:, col] = values is an in-place setitem that has to respect the existing dtype. Silently changing the dtype is being phased out (PDEP-6): 2.2 still upcasts but warns, and 3.0 raises instead. df[col] = values replaces the whole column, so the new dtype is simply float64 with no warning. "
        "When you mean to change the type, say so: df['qty'] = df['qty'].astype(float) before the partial write, or assign the whole column.",
        topic="modifying", level=4),
    mcq("A team moves a pipeline from pandas to Polars. What is the key DESIGN difference around the row index that changes how arithmetic and assignment behave?",
        ["Polars has no row index: operations line up rows by position (lengths must match) and any matching by key is an explicit join, while pandas silently aligns on index labels",
         "Polars aligns on labels too, but sorts them first",
         "Polars always copies data, pandas never does",
         "There is no difference; both align by index"], 0,
        "What would a + b mean if there were no labels?",
        "pandas' implicit alignment is powerful (rows stay matched after a sort or filter) but it surprises people: reordered or differently filtered frames produce NaN instead of an error, and assignment aligns instead of pasting. Polars, like SQL, has no index. Columns combine positionally inside one frame, and combining data from two frames means an explicit join on named keys. "
        "That makes Polars code more predictable and easier to parallelise. The price is that you must carry keys as ordinary columns. A port fails when the pandas code silently relied on index alignment.",
        diagram="""
pandas:  a[x=1, y=2] + b[y=10, z=20] -> x NaN, y 12, z NaN
         (matched by label)
Polars:  a [1, 2] + b [10, 20]       -> [11, 22]
         (matched by position; keyed match = explicit join)""",
        analogy="SQL tables have no implicit row index either: to combine two tables you write a JOIN ON key.",
        topic="index-alignment", level=4),
    fill("In scikit-learn 1.6, `HistGradientBoostingClassifier` treats pandas `category` columns as categorical features automatically, because its `categorical_features` default is `'____'`.",
        "from_dtype",
        "The categorical columns are detected from the column dtype.",
        "With categorical_features='from_dtype' (the default in 1.6), every column of category dtype in the input DataFrame is handled with native categorical splits, with no one-hot encoding needed. This only works if the training and serving frames use the same categories, so fix them with pd.Categorical(..., categories=train_cats). "
        "If you pass a NumPy array, there are no dtypes to read, so nothing is treated as categorical: the int codes become plain numbers.",
        topic="ml-features", level=4),
    mcq("On a 50-million-row frame, why can `df.eval('a + b * c')` be faster and lighter on memory than `df['a'] + df['b'] * df['c']`?",
        ["With numexpr installed, eval computes the expression in cache-sized chunks on several threads, without materialising the full-size temporary b * c array",
         "eval compiles the expression to GPU code",
         "eval skips NaN values",
         "eval is always faster, even on 100-row frames"], 0,
        "How many full-length arrays does the plain version create?",
        "The plain expression first builds a full 50M-element array for b * c (400 MB for float64) and then another for the sum. numexpr streams through the data in blocks and fuses the operations, so temporaries stay small and work is spread over cores. "
        "On small frames, parsing the string costs more than it saves. Use eval for big, arithmetic-heavy expressions and keep plain vectorised code elsewhere.",
        analogy="Like a database pipelining a computed column row block by row block instead of writing intermediate tables to disk.",
        code="import pandas as pd\ndf = pd.DataFrame({'a': [1, 2], 'b': [3, 4], 'c': [5, 6]})\nprint(df.eval('a + b * c').tolist())",
        topic="apply-vectorise", level=4),
    tf("`df.loc[mask]` with a boolean NumPy array selects rows by POSITION, while `df.loc[mask_series]` with a boolean Series matches rows by index LABEL.", True,
        "A NumPy array has no labels to align.",
        "A plain array (or list) of booleans is taken position by position, so it must have exactly len(df) entries. A boolean Series is first aligned to df's index. On an index like [2, 0, 1], the same True/False values pick different rows depending on whether they come in as an array or as a Series with its own labels. "
        "Masks created with .values or .to_numpy() quietly switch from label to position semantics. That's harmless when the order matches and a silent bug when it doesn't.",
        diagram="""
df index:     2    0    1        values: 10 20 30
array mask:   T    F    T   -> positions 0, 2 -> [10, 30]
Series mask:  {0: T, 1: F, 2: T} aligned to labels
              label 2 -> T, 0 -> T, 1 -> F    -> [10, 20]""",
        code="import numpy as np\nimport pandas as pd\ndf = pd.DataFrame({'v': [10, 20, 30]}, index=[2, 0, 1])\nm = pd.Series([True, False, True], index=[0, 1, 2])\nprint(df.loc[np.array([True, False, True])]['v'].tolist(), df.loc[m]['v'].tolist())",
        topic="filtering", level=4),
    tf("On a sorted index ['a', 'b', 'd'], `s.loc['b':'c']` works even though 'c' is not a label, but on an unsorted index the same kind of slice raises KeyError.", True,
        "With a monotonic index, pandas can binary-search where 'c' WOULD go.",
        "For a monotonic index, label slicing uses searchsorted, so slice bounds don't have to exist: 'b':'c' means 'every label from b up to c', giving just b here. On a non-monotonic index there's no 'where it would be', so a missing bound raises KeyError. "
        "Date slices like df.loc['2024-01-01':'2024-01-31'] rely on this: sort_index() first, and missing days at the edges don't matter.",
        code="import pandas as pd\ns = pd.Series([1, 2, 3], index=['a', 'b', 'd'])\nprint(s.loc['b':'c'].tolist(), s.loc['a':'c'].tolist())",
        topic="loc-iloc", level=4),
    mcq("You need ONE row of a mixed-type feature frame to pass to `model.predict`. Why is `df.iloc[[0]]` better than `df.iloc[0]`?",
        ["iloc[[0]] returns a 1-row DataFrame that keeps each column's dtype and the column names; iloc[0] returns a Series, which forces one common dtype (often object) and is 1-D",
         "iloc[0] is slower to compute",
         "iloc[[0]] returns a copy, iloc[0] a view",
         "There is no difference for predict"], 0,
        "A list inside iloc keeps the result 2-D.",
        "A single position collapses the row into a Series: the columns become its index and the values must share one dtype, so int, float and str together become object. scikit-learn then gets a 1-D object array, which fails or gets misread. A list of positions keeps the DataFrame shape (1, n_features), the dtypes and the feature names that the model checks. "
        "The same rule applies to loc: df.loc[[label]] vs df.loc[label].",
        diagram="""
df.iloc[0]    -> Series, dtype object      (1-D, dtypes lost)
                 a  1 | b  1.5 | c  'x'
df.iloc[[0]]  -> DataFrame shape (1, 3)    (2-D, dtypes kept)
                 a:int64  b:float64  c:object""",
        code="import pandas as pd\ndf = pd.DataFrame({'a': [1], 'b': [1.5], 'c': ['x']})\nprint(df.iloc[0].dtype, df.iloc[[0]].dtypes.astype(str).tolist())",
        topic="series-vs-df", level=4),
    tf("Converting an int64 id column to float64 (which happens silently when one id is missing) keeps every id exactly.", False,
        "float64 has 53 bits of mantissa.",
        "float64 represents every integer exactly only up to 2**53 (about 9 x 10^15). Larger ids, such as 64-bit snowflake ids or some order numbers, get rounded to a neighbouring value, so two different ids can collide and joins match the wrong rows. "
        "Keep ids as strings or as the nullable 'Int64' dtype (read_csv(dtype={'id': 'Int64'})), so a missing value doesn't force a float conversion.",
        analogy="The same reason JavaScript's Number can't hold a 64-bit id from a backend, and why APIs send big ids as strings.",
        code="import pandas as pd\nprint(int(pd.Series([2**53 + 1]).astype(float)[0]) == 2**53 + 1)",
        topic="dtypes-memory", level=4),
]
