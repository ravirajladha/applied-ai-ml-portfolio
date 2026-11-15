# Pandas DataFrames: coverage spec

**Ladder:** Foundations › Python for Data   ·   **Prerequisites:** Python basics (lists, dicts, functions), NumPy arrays
**Why it matters for AI/ML:** almost every ML project starts by loading a table into a DataFrame, inspecting it, selecting features and filtering rows. Mistakes here (wrong rows selected, silently unchanged data, misaligned columns, wrong dtypes) flow straight into the model and are hard to spot later.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `series-vs-df` | Series vs DataFrame | what a Series and a DataFrame are, df["col"] is a Series | row access returns a Series, to_frame | rows of mixed dtypes become object | — |
| 2 | `creating` | Creating DataFrames | from a dict of lists, list of dicts, read_csv(io.StringIO) | index_col, unequal lengths, scalar broadcast | dict of Series aligns on index, dtype= for IDs, NA parsing, keep_default_na ('NA' = Namibia), thousands= | bool column with a blank becomes object, chunked inference and DtypeWarning |
| 3 | `inspecting` | head, info, describe, shape, dtypes | head, shape vs len, info | describe numeric only, dtypes, count vs len, non-null counts, size/ndim | describe(include="all"), sample std (ddof=1) | — |
| 4 | `selecting` | Selecting columns | df["a"] vs df[["a"]], list of columns, dot access | df["a","b"] KeyError, dot access clashes with methods, can't create via dot, column order | select_dtypes, df[0:2] slices rows | — |
| 5 | `loc-iloc` | loc vs iloc | label vs position, loc[row, col] | inclusive loc slicing, labels vs positions disagree, negative positions | duplicate labels change return type, scalar types, df["c"].iloc[i], loc with a missing label raises KeyError (use reindex), columns.get_loc | unsorted-index label slices, s[0] on an integer index, loc enlargement, non-unique slice bound KeyError, iloc with a boolean Series |
| 6 | `filtering` | Boolean filtering and query() | masks, df[mask], & with parentheses | `and` ValueError, `|` and `~`, isin, between, query with @var | query allows and/or, precedence trap, list mask length, backticks for names with spaces | boolean Series mask aligns by label, isin finds NaN while == doesn't, NA in a nullable mask counts as False |
| 7 | `modifying` | Adding, renaming, dropping, sorting | new column, rename returns new object, drop columns, sort_values | drop axis default, sorted index labels, multi-key sort, insert | assign with lambdas, inplace returns None, nlargest and rank | — |
| 8 | `apply-vectorise` | apply / map vs vectorised ops | vectorised arithmetic, map with dict, vectorised is faster | map leaves NaN for unknown keys, apply axis, apply axis=1 result | np.where, DataFrame.map, why apply(axis=1) is slow, np.vectorize is still a loop | result_type="expand", how many times apply calls f, row dtype upcast inside apply(axis=1) |
| 9 | `index-alignment` | Index and alignment | alignment exists, set_index | Series + Series aligns and sorts labels, reset_index | assignment aligns (sort undone), fill_value, df - df.mean(), == needs identical labels | df - row-means aligns on columns, duplicate labels in alignment, eq vs equals, int vs str labels, fill_value doesn't fill existing NaN, allows_duplicate_labels |
| 10 | `copy-view` | Copies, views, SettingWithCopyWarning, copy-on-write | .loc[mask, col] = v, .copy() | what SettingWithCopyWarning means, chained assignment loses writes | column Series is a view without CoW, CoW behaviour, df["a"][0] = v in 2.2, list selection copies, mutation side effects, iloc slice view vs CoW, filtered subset under CoW | CoW chained assignment never works, why CoW is cheap, shallow-ness of deep copy for objects, read-only to_numpy under CoW, .values view depends on dtypes, inplace on a column selection |
| 11 | `dtypes-memory` | dtypes and memory | default dtypes, object strings, astype(int) | None upcasts int to float, nullable Int64, category saves memory | category codes, memory_usage(deep=True), string dtype and pd.NA, nullable results (Float64, boolean), str.len dtype, new category TypeError, convert_dtypes, np.nan vs pd.NA | astype overflow wraps, pd.NA three-valued logic, bool(pd.NA) TypeError, nullable boolean, concat of mismatched categoricals gives object, string[python] vs pyarrow memory |
| 12 | `multiindex` | MultiIndex basics | — | — | what a MultiIndex is, loc with tuples, partial selection drops a level, agg list makes MultiIndex columns, list of labels vs list of tuples, unstack upcasts to float | xs on an inner level, unstack, lexsort for slicing, pd.IndexSlice |
| 13 | `ml-features` | DataFrames as model inputs (X, y and feature columns) | — | — | to_numpy object dtype, select_dtypes skips bool, predict with NumPy only warns, set_output(transform="pandas"), reindex(columns=train_cols), X and y from one frame | sklearn feature-name order check, reset_index on X only scrambles X/y |

## Must-know facts
- A DataFrame is a dict of Series sharing one index; df["a"] is a Series, df[["a"]] is a DataFrame.
- loc is label-based and its slices INCLUDE the end; iloc is position-based and excludes it.
- On an integer index, s[0] means label 0, not position 0. Use .iloc for positions.
- Combine masks with &, |, ~ and wrap each condition in parentheses; `and`/`or` raise ValueError (except inside query strings).
- Most methods return a new object; rename/drop/sort_values without assignment do nothing. inplace=True returns None.
- drop() defaults to rows; use drop(columns=...).
- Arithmetic and column assignment align on index labels, not positions; missing labels give NaN.
- df - series aligns the Series with the columns; for row-wise operations use df.sub(s, axis=0).
- df[mask]["col"] = v writes to a temporary copy; use df.loc[mask, "col"] = v.
- pandas 2.2: copy-on-write is opt-in; it becomes the default in 3.0, where chained assignment never works.
- Strings default to object dtype; the "string" dtype and nullable Int64/boolean use pd.NA.
- A missing value in an int column upcasts it to float64 (unless you use Int64).
- category stores each distinct value once plus small integer codes; huge savings for low-cardinality text.
- memory_usage() without deep=True undercounts object columns.
- Vectorised column math runs in C; apply(axis=1) and iterrows are Python loops.
- describe() and std() use the sample std (ddof=1).
- read_csv infers types: IDs with leading zeros need dtype=str; "NA" and blanks become NaN.
- Comparison operators (==, <) on two Series need identical labels (else ValueError); arithmetic aligns. Use .eq() to align, .equals() for strict equality.
- Under copy-on-write only the object you modify changes; to_numpy() views are read-only, and inplace methods on a column selection (df["a"].fillna(..., inplace=True)) stop updating df.
- Without CoW, iloc slices and .values on a single-dtype frame can be views; whether you get a view depends on the dtypes.
- pd.NA uses SQL three-valued logic (NA | True is True, NA & False is False); nullable ops stay nullable (Int64 / 2 is Float64, comparisons give boolean).
- Concatenating categoricals with different category lists silently gives object dtype.
- select_dtypes("number") excludes bool; to_numpy() on mixed str/number columns gives an object array.
- scikit-learn models fit on DataFrames check feature names and their order at predict; NumPy input skips the check (only a warning).

## Common traps (each one must have at least one question)
- df["a", "b"] instead of df[["a", "b"]] -> KeyError (looks for a tuple label).
- `cond1 and cond2` on Series -> ValueError: truth value is ambiguous.
- Missing parentheses with & -> wrong precedence, ValueError.
- loc slices include the end, iloc slices don't -> off-by-one row counts.
- s[0] on a non-default integer index -> label lookup, not position.
- df.rename(...) without assignment -> nothing changes.
- df = df.sort_values(..., inplace=True) -> df becomes None.
- df.drop("col") -> KeyError (default axis is rows).
- df.new_col = ... -> sets an attribute, not a column.
- df.count when a column is called "count" -> you get the method.
- Assigning a sorted Series back into df -> the sort is undone by alignment.
- df[mask]["col"] = v -> SettingWithCopyWarning and no change.
- s = df["a"]; s[0] = v -> modifies df in 2.2 without CoW, not with CoW.
- map with a dict missing some keys -> NaN and float dtype.
- One None in an int column -> float64.
- astype("int8") on large values -> silent wrap-around.
- if s[i] == x with pd.NA -> TypeError.
- read_csv on zero-padded IDs -> leading zeros lost.
- df - df.mean(axis=1) -> all-NaN frame with extra columns.
- Duplicate index labels -> loc returns a DataFrame instead of a Series.
- Label slice with a non-unique start label on an unsorted index -> KeyError.
- df.iloc[bool_series] -> NotImplementedError; pass .to_numpy().
- a == b on Series with the same labels in a different order -> ValueError.
- int labels vs string labels ('0' vs 0) -> alignment gives all NaN.
- add(fill_value=0) -> existing NaN stays NaN.
- df["a"].fillna(0, inplace=True) -> works in 2.2, does nothing under CoW / pandas 3.
- Writing into df["a"].to_numpy() under CoW -> ValueError (read-only).
- s.isin([np.nan]) finds NaN while s == np.nan never does.
- concat of two category columns with different categories -> object dtype.
- read_csv on 'NA' country codes -> NaN; one blank in a bool column -> object dtype.
- reset_index on X_train but not y_train -> X/y misaligned after concat.
- Predicting with columns in a different order -> ValueError in scikit-learn.

## Interview angle
- **"loc vs iloc?"** loc selects by label and its slices include the end; iloc selects by 0-based position like a Python list and excludes the end. With an integer index they can disagree, so be explicit. SDE analogy: lookup by primary key vs by array offset.
- **"What is SettingWithCopyWarning and how do you fix it?"** You did a two-step selection-then-assignment (df[mask]["c"] = v), so the write may land on a temporary copy. Do it in one step with df.loc[mask, "c"] = v, or take an explicit .copy() if you want a separate frame. Copy-on-write (default in pandas 3.0) makes the rule simple: only the object you modify changes, and chained assignment never works.
- **"Why is apply slow and what do you use instead?"** apply calls Python per row or element; vectorised ops (column arithmetic, np.where, .str/.dt methods, map with a dict) run one C loop over a NumPy array. Analogy: one bulk SQL UPDATE vs a loop of single-row UPDATEs.
- **"What happens when you add two Series with different indexes?"** pandas aligns on labels (like an outer join on the index); labels missing on either side give NaN. Use fill_value or reindex to control it.
- **"How do you keep training and serving features consistent?"** Save the training column list (and category lists) with the model; at serving time reindex(columns=train_cols, fill_value=0) or use pd.Categorical with the saved categories, and keep DataFrames up to predict so scikit-learn's feature-name check can catch order bugs. SDE analogy: a versioned API schema.
- **"How would you reduce a DataFrame's memory?"** Check memory_usage(deep=True), convert low-cardinality text to category, downcast numerics with pd.to_numeric(downcast=...), use nullable dtypes where needed, and only load the columns you need (usecols).

## Source material
To be added
