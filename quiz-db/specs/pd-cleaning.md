# Pandas Cleaning & Grouping: coverage spec

**Ladder:** Foundations › Python for Data   ·   **Prerequisites:** pd-dataframes (selecting, loc/iloc, masks, dtypes)
**Why it matters for AI/ML:** real datasets are dirty: missing values, wrong types, duplicates, inconsistent text, several tables to join. Cleaning and feature building happen in pandas before any model sees the data, and the classic ML bugs (leakage, row blow-ups from joins, misaligned one-hot columns) are born here.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `missing` | Missing values | NaN meaning, isna().sum(), dropna, fillna, NaN != NaN, None vs NaN | == np.nan trap, how/subset/thresh, ffill/bfill, skipna, per-column fill, None in object columns | all-NaN sum is 0, interpolate, hidden missing ('', 'n/a'), Int64 keeps NA, missingness strategy | astype(int64) on NaN raises IntCastingNaNError |
| 2 | `duplicates` | Duplicates and value_counts | duplicated/drop_duplicates, value_counts, whole-row default | normalize, nunique, dropna in value_counts, subset + keep | keep=False, case/space variants, duplicates across train/test | — |
| 3 | `types` | Type conversion | astype(int), to_numeric(errors='coerce') | astype ValueError on dirty data, cleaning '$1,200', to_datetime, NaT, mixed object column, why a column is object | dayfirst, astype(bool) truthiness, float->int truncation, downcast | explicit format rejects inconsistent rows |
| 4 | `strings` | .str methods | strip/title/lower, contains/startswith | split(expand=True), str.len with NaN, slicing, whitespace breaks equality, regex=True in replace | contains is regex by default, NaN in masks (na=False), extract | why .str on object dtype is still a Python loop |
| 5 | `groupby` | groupby and aggregation | split-apply-combine, sum per group, SQL GROUP BY | Series vs DataFrame result, as_index=False, agg list, named aggregation, multi-key groups, custom agg, nunique | sum concatenates strings, mean TypeError on text (numeric_only), sort=False, filter (HAVING) | — |
| 6 | `groupby-advanced` | transform vs agg vs apply, size vs count | — | size vs count, transform vs agg, transform for new columns | share of group total, group-wise fillna, cumsum/cumcount, shift (LAG), NaN keys dropped, apply returning Series | top-n per group/idxmax, observed for categoricals, empty results, why apply is slow |
| 7 | `merge` | merge and join | merge = JOIN, inner vs left, default inner, how='outer' | duplicate keys multiply rows, suffixes, left_on/right_on, NaN after left join, join on index, merge vs join defaults | indicator, validate=, int vs str keys, diagnosing row blow-ups, many_to_one | NaN keys match each other (unlike SQL), merge_asof |
| 8 | `concat` | concat | stacking keeps old index, ignore_index, concat vs merge | union of columns, axis=1 | axis=1 aligns on index, concat in a loop is O(n^2), keys= | — |
| 9 | `reshape` | pivot, pivot_table, melt | what melt does | melt output, pivot, crosstab, wide vs long, pivot can't aggregate | pivot duplicates ValueError, pivot_table default mean, margins/fill_value | stack, pivot_table == groupby + unstack |
| 10 | `binning` | cut and qcut | cut with labels, cut vs fixed edges | cut vs qcut, qcut equal counts | right-closed bins, equal-width on skewed data, categorical result | qcut duplicate edges, bin edges as a leakage source |
| 11 | `datetime` | Dates and resampling | .dt parts, need datetime dtype, NaT | resample sum, month buckets and partial-string indexing, rolling, resample needs a DatetimeIndex | Timedelta vs DateOffset, diff, tz_convert | naive vs aware TypeError, asfreq vs resample hiding gaps |
| 12 | `ml-prep` | Preparing data for ML, performance | get_dummies, why one-hot, avoid iterrows | drop_first, mean-fill leakage, itertuples, class balance, time-based split | train/test dummy mismatch, train-only statistics, np.select, speed ranking, Pipeline in CV | time-reference leakage, target-encoding leakage, ddof differences, label vs one-hot for trees |

## Must-know facts
- NaN != NaN; test missing values with isna(), never ==.
- Aggregations skip NaN by default; an all-NaN sum is 0.0 but the mean is NaN.
- A NaN in an integer column makes it float64; use 'Int64' to keep integers.
- fillna/dropna/drop_duplicates return new objects; assign the result.
- to_numeric/to_datetime with errors='coerce' turn bad values into NaN/NaT; astype raises.
- read_csv and to_datetime default to month-first dates; pass format= or dayfirst=True.
- .str.contains and .str.replace: contains is regex by default, replace is literal by default (pandas 2).
- groupby drops NaN keys by default (dropna=True) and sorts keys (sort=True).
- size counts rows (COUNT(*)), count counts non-missing values (COUNT(col)).
- agg returns one row per group; transform returns one value per original row; apply is the flexible, slow fallback.
- In pandas 2, groupby mean/sum with text columns don't silently drop them (numeric_only=False).
- merge defaults to inner on shared column names; join defaults to left on the index.
- Duplicate keys on both sides of a merge multiply rows; use validate= to assert cardinality.
- pandas merges NaN keys with NaN keys, unlike SQL NULLs.
- concat keeps the original index (use ignore_index=True) and takes the union of columns.
- pivot fails on duplicates; pivot_table aggregates with mean by default.
- cut bins are right-closed (a, b]; qcut makes equal-count bins.
- get_dummies returns bool columns in pandas 2 and only knows the categories it sees.
- Every learned preprocessing statistic (mean, bins, categories, target means) must come from training data only.

## Common traps (each one must have at least one question)
- df[df.a == np.nan] -> always empty.
- '' / 'n/a' strings are not NaN -> isna() misses them.
- astype(int) on a column with NaN -> IntCastingNaNError.
- astype(int) on dirty text -> ValueError; use to_numeric(errors='coerce').
- astype(bool) on 'yes'/'no' -> everything True.
- Float -> int truncates toward zero.
- '05/01/2024' parsed as 1 May, not 5 Jan.
- .str.contains('.') matches everything (regex).
- NaN inside a .str.contains mask -> ValueError when indexing.
- Trailing spaces -> equality and merges silently miss.
- groupby().sum() on text -> string concatenation; mean() -> TypeError.
- NaN group keys silently dropped from groupby totals.
- Using agg where transform is needed -> misaligned new column.
- Merge row count grows unexpectedly -> duplicate keys on the right side.
- Merging int keys with string keys -> ValueError.
- Left join turns int columns into float.
- concat without ignore_index -> duplicate index labels.
- concat(axis=1) on frames with different indexes -> extra NaN rows.
- Building a DataFrame by concat in a loop -> quadratic time.
- pivot on duplicate pairs -> ValueError.
- pivot_table silently averages duplicates.
- cut: the lowest edge is excluded -> NaN for the minimum.
- qcut on many tied values -> ValueError (duplicate edges).
- resample().sum() turns missing days into 0.
- Comparing tz-naive and tz-aware timestamps -> TypeError.
- get_dummies separately on train and test -> different columns.
- fillna with the full-data mean before splitting -> leakage.
- Random split on time series -> future leakage.

## Interview angle
- **"How do you handle missing values?"** First measure (isna().sum()) and find out why they are missing. Then drop (if few and random), impute (median/mode or group-wise, fitted on train only), or add a missing-indicator feature. Never compute the fill value on the full dataset. SDE analogy: validating input at the API boundary before it reaches business logic.
- **"agg vs transform vs apply?"** agg reduces each group to one row (GROUP BY). transform returns one value per original row so you can add it as a column (a window function, PARTITION BY). apply is a flexible escape hatch that calls Python per group and is slowest.
- **"Your merge produced more rows than the left table. Why?"** The right key isn't unique: each left row matches several right rows. Check is_unique / duplicated on the key, and use validate='many_to_one' to fail fast. Also check NaN keys, which pandas matches with each other.
- **"What is data leakage in preprocessing and how do you avoid it?"** Any statistic learned from data (means, scalers, bin edges, category lists, target encodings) must be fitted on the training split only and reused on test. Use a scikit-learn Pipeline so each CV fold refits it. For time series, split by time.
- **"How do you speed up a slow pandas script?"** Replace iterrows/apply(axis=1) with vectorised column ops, np.where/np.select, .str/.dt methods, map with dicts, groupby with built-in aggregations; use category dtype for repeated strings; build frames once instead of concat in a loop.

## Source material
To be added
