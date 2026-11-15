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
]
