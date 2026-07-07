# Session 9 — Implementation & Code Sharing ⭐

> **Module 4 · Lecture 9** · Slides: `Session 09 - Implementation & Code Sharing (Good Code & Performance).pptx` · Companion: *(none — this note is built directly from the slides, in full detail)*
>
> **One-line goal:** *what is good code* in ML, its **five features**, and how to **measure and profile** code performance.
>
> ⭐ This is the session I'm currently studying — the most detailed note in the set.

### Contents
1. [SE coding vs ML coding — the mindset shift](#1-se-coding-vs-ml-coding--the-mindset-shift)
2. [What is "good code"?](#2-what-is-good-code)
3. [The five features of good ML code](#3-the-five-features-of-good-ml-code)
   - [Feature 1 · Simplicity (DRY)](#feature-1--simplicity-dry)
   - [Feature 2 · Modularity](#feature-2--modularity)
   - [Feature 3 · Readability (PEP 8 + pylint)](#feature-3--readability-pep-8--pylint)
   - [Feature 4 · Performance](#feature-4--performance)
   - [Feature 5 · Robustness](#feature-5--robustness)
4. [Analysing code performance](#4-analysing-code-performance)
   - [Ways to make Python faster](#ways-to-make-python-faster)
   - [Timing: `time` module](#timing-the-time-module)
   - [Benchmarking: `timeit` / `%%timeit`](#benchmarking-timeit--timeit)
   - [`time` vs `timeit`](#time-vs-timeit)
   - [Profiling: `cProfile`](#profiling-cprofile)
   - [`line_profiler`](#line_profiler)
   - [Memory: `memray` / `memory_profiler`](#memory-memray--memory_profiler)
5. [The performance-analysis ladder](#5-the-performance-analysis-ladder)
6. [Recap](#-recap)

---

## 1. SE coding vs ML coding — the mindset shift

The key difference: **who writes the decision rules.**

```python
# Traditional Software Engineering — the DEVELOPER writes the rule
def approve_loan(income):
    if income > 50000:
        return "Approved"
    else:
        return "Rejected"

# Machine Learning — the developer writes code to TRAIN a model;
# the algorithm learns the rules from data
model.fit(X_train, y_train)          # X_train = customer details, y_train = correct answers
prediction = model.predict(new_customer)
```

After training on thousands of examples, the model might *internally* learn something like:
> *If income is high AND age < 60 AND credit score > 700 AND existing loans are few → probability of approval = 92%.*
…but nobody wrote that rule — the algorithm discovered it.

| | Software Engineering | Machine Learning |
|---|---|---|
| Who writes the rules | **Developers** write the decision rules | Developers build systems that **learn** the rules from data |
| Where logic lives | Encoded in **code** | Encoded in the trained model's **parameters** |
| Focus | Implementing functionality correctly | Enabling the model to **generalize** to unseen data |
| Fixing bugs | Change the **code** | May require improving the **data, features, or training** — not the app logic |
| Inspecting rules | Easy to read & modify | Embedded in learned parameters; hard to interpret (esp. deep learning) |
| Example | `if income > 60000: approve` | `model.predict(customer_data)` uses learned patterns |

---

## 2. What is "good code"?

The slide poses it as a question — is good code the code that…
- runs fastest? · is easy to read? · is easy to maintain? · follows all project standards?

**Answer: all of these together.** Good ML code is defined by **five features** ↓.

---

## 3. The five features of good ML code

| # | Feature | In one line |
|---|---------|-------------|
| 1 | **Simplicity** | Avoid repetition, unnecessary complexity, unneeded lines (**DRY**). |
| 2 | **Modularity** | Break code into logical functions with well-defined inputs/outputs. |
| 3 | **Readability** | Follow **PEP 8**, choose good names, document well. |
| 4 | **Performance** | Don't take unnecessarily long or use more resources than available. |
| 5 | **Robustness** | Reproducible; useful error messages; handles unexpected inputs without failing. |

### Feature 1 · Simplicity (DRY)

**DRY = Don't Repeat Yourself.** Every piece of knowledge or logic should exist in **only one place**. Duplication → more bugs, longer code, more time to read.

```python
# ❌ Repetitive — the same 3 lines copied for every file (3 places to update)
df  = pd.read_csv("sdg_literacy_rate.csv")
df  = df.drop(["Series Name", "Series Code", "Country Code"], axis=1)
df  = df.set_index("Country Name").transpose()
df2 = pd.read_csv("sdg_electricity_data.csv")
df2 = df2.drop([...], axis=1)
df2 = df2.set_index("Country Name").transpose()
df3 = pd.read_csv("sdg_urban_population.csv")
# ...same again

# ✅ DRY — one reusable function, called wherever needed
def process_sdg_data(csv_file, columns_to_drop):
    df = pd.read_csv(csv_file)
    df = df.drop(columns_to_drop, axis=1)
    df = df.set_index("Country Name").transpose()
    return df
```

**Where duplication sneaks into ML projects:** data preprocessing (cleaning, missing values, scaling) · feature engineering across models · model training & evaluation · repeating the *same preprocessing + prediction* code in training, testing, **and** deployment scripts. → Extract reusable functions/classes/pipelines.

### Feature 2 · Modularity

Writing modular code = **the art of breaking a big system into smaller components.**

Advantages:
- Easier to **read**.
- Easier to **locate** where a problem comes from.
- Easier to **reuse** in the next project.
- Easier to **test** smaller components.

> 💡 The **Pipe-and-Filter** pattern (Session 4) and the **Microservices** style (Session 5) both advocate modularity — the same principle, at the architecture level.

### Feature 3 · Readability (PEP 8 + pylint)

Most ML apps are Python. **Coding standards** keep everyone's code consistent:
- **PEP 8** (Python Enhancement Proposal 8, 2001) — the main Python standard. → <https://peps.python.org/pep-0008/>
- **Google Python Style Guide** — another standard.
- **pylint** — checks code quality / readability automatically.

**pylint** = a *static* code-analysis tool (checks code **without running it**). It detects errors, checks PEP 8 style, suggests better names, finds unused code, warns about duplicate/complex code, reports missing docstrings, and gives a **quality score**.

```python
# ❌ Before pylint
from sklearn.linear_model import LogisticRegression
X = [[22, 50000], [35, 80000], [28, 60000]]
y = [0, 1, 1]
m = LogisticRegression()
m.fit(X, y)
p = m.predict([[30, 70000]])
print(p)
```
```
pylint warnings:
C0103: Variable name "X" doesn't conform to snake_case naming style
C0103: Variable name "y" ...
C0103: Variable name "m" ...
C0103: Variable name "p" ...
```
```python
# ✅ After applying pylint suggestions (snake_case, meaningful names)
from sklearn.linear_model import LogisticRegression
training_data   = [[22, 50000], [35, 80000], [28, 60000]]
training_labels = [0, 1, 1]
model = LogisticRegression()
model.fit(training_data, training_labels)
prediction = model.predict([[30, 70000]])
print(prediction)
```
> **snake_case** = words in lowercase separated by underscores (`training_data`).

### Feature 4 · Performance

- Use **efficient data structures & algorithms**; choose faster alternatives.
- **Identify** the parts that take the most time; optimize both **execution time** and **memory**.
- Performance is critical for production apps used by many users — small improvements matter when code runs **millions of times**, and prevent bottlenecks in large applications.

### Feature 5 · Robustness

- Code must be **reproducible**.
- Runs from start to finish **without failures**.
- Handles unexpected inputs & errors **gracefully** (not crashing).
- Uses proper **error handling + logging** to track issues.
- Has **tests** verifying it works under different conditions.

---

## 4. Analysing code performance

### Ways to make Python faster

| Lever | Idea |
|-------|------|
| **Choice of algorithm** | Pick an efficient ML algorithm for the problem & dataset |
| **Choice of data structure** | Use the right one: List, Tuple, Dictionary, NumPy arrays, Pandas DataFrames |
| **Built-in functions** | Prefer optimized libraries (NumPy, Pandas, Scikit-learn) over custom loops |
| **Asynchronous code** | Run data loading, preprocessing & I/O concurrently to cut waiting time |
| **Parallel & distributed computing** | Train across multiple CPU cores, GPUs, or distributed frameworks |

> 💡 The golden rule of optimization: **measure first.** "Measure → change → measure again" — never guess where the slow part is.

### Timing: the `time` module

Simplest approach — wrap code and subtract timestamps. **Runs the code once.**

```python
import time
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

X, y = load_iris(return_X_y=True)

start = time.time()                       # record start
model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)                           # the code being timed
end = time.time()                         # record end

print(f"Training Time: {end - start:.6f} seconds")
# → Training Time: 0.002007 seconds
```

> 📎 **Iris dataset** (used throughout): `load_iris()` from scikit-learn. 150 samples, 4 features (sepal length/width, petal length/width), 3 classes (Setosa, Versicolor, Virginica). The go-to tiny classification dataset.

### Benchmarking: `timeit` / `%%timeit`

`time` runs once, so background noise skews it. **`timeit` runs the code many times and averages** — far more reliable.

```python
import timeit, statistics
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

def train_model():
    X, y = load_iris(return_X_y=True)
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X, y)

# repeat=10 → run the whole benchmark 10 separate times
# number=100 → each benchmark runs the function 100 times
times = timeit.repeat(train_model, repeat=10, number=100)
avg_times = [t / 100 for t in times]      # total → average per run

print(f"Average Training Time : {statistics.mean(avg_times):.6f} seconds")
print(f"Standard Deviation    : {statistics.stdev(avg_times):.6f} seconds")
# → Average Training Time : 1.812 ms
# → Standard Deviation    : 0.041 ms
```

**Reading the result:** `1.812 ± 0.041 ms` → most runs fell between **1.771 and 1.853 ms** → very consistent.
- **Small std dev** → stable, consistent performance.
- **Large std dev** → performance varies (CPU load, background processes, caching).

In Colab / Jupyter you can use the cell magic instead:

```python
%%timeit
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
X, y = load_iris(return_X_y=True)
model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)
# → 3.43 ms ± 160 µs per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

### `time` vs `timeit`

| Feature | `time` module | `timeit` / `%%timeit` |
|---------|---------------|------------------------|
| Purpose | Measure elapsed time of a block/program | **Benchmark** a code snippet |
| Execution | Runs the code **once** | Runs it **many times** automatically |
| Accuracy | Lower (affected by background processes) | Higher (averages runs to reduce noise) |
| Output | Total time for one run | **Average time + standard deviation** |
| Best use | Timing a whole ML workflow (load → train → predict) | Comparing algorithms/functions/implementations |

### Profiling: `cProfile`

**Why a profiler?** `%%timeit` is ideal for a *single line or small snippet*. For **long functions or full scripts**, timing each line by hand is impractical. A **profiler analyses the whole program and finds which parts eat the most time** — so you optimize the slowest sections.

**cProfile** = Python's **built-in** profiler. Written as a C extension (low overhead), suitable for long-running programs. It tracks **execution time + call count of every function**, pinpointing where efficiency is lost.

```
Accuracy: 0.90
   12156 function calls (11932 primitive calls) in 0.036 seconds
   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.036    0.036 train_model
        1    0.001    0.001    0.027    0.027 sklearn/ensemble/_forest.py:319(fit)
        5    0.002    0.000    0.024    0.005 .../_forest.py:167(_parallel_build_trees)
        1    0.000    0.000    0.003    0.003 .../_forest.py:824(score)
        1    0.000    0.000    0.002    0.002 model_selection/_split.py(train_test_split)
        1    0.000    0.000    0.001    0.001 datasets/_base.py:30(load_iris)
```

**How to read each column:**

| Column | Meaning |
|--------|---------|
| **ncalls** | How many times the function was called |
| **tottime** | Time spent **only in this function** (excludes children) |
| **percall** (after tottime) | Average self-time per call = tottime ÷ ncalls |
| **cumtime** | Time in this function **+ all functions it called** |
| **percall** (after cumtime) | Average cumulative time per call = cumtime ÷ ncalls |

**Interpreting this run:** accuracy 0.90 = 90% of test samples predicted correctly · 12,156 calls in 0.036 s · sorted by cumulative time · `fit` (RandomForest) consumes the **most** time · `_parallel_build_trees` builds the 5 trees · `score` evaluates · `train_test_split` splits data · `load_iris` loads it.

**Minimal example:**
```python
def square(x):
    return x * x
def calculate():
    total = 0
    for i in range(5):
        total += square(i)
    return total
calculate()
```
```
ncalls  tottime  percall  cumtime  percall  function
1        0.001    0.001    0.006    0.006    calculate
5        0.002    0.0004   0.002    0.0004   square      ← called 5 times
```

### `line_profiler`

cProfile is detailed but **hard to read** and dives deep into Python internals. **`line_profiler`** gives a much more readable, **line-by-line** breakdown.

```bash
pip install line_profiler
```

**Sample run (a RandomForest script), % of total execution time:**

| Line | Time | % of total |
|------|------|-----------|
| `load_iris()` | 26.104 ms | 19.5% |
| `train_test_split()` | 6.940 ms | 5.2% |
| `RandomForestClassifier()` (create) | 0.328 ms | 0.2% |
| **`model.fit()`** | **83.812 ms** | **62.7% ← bottleneck** |
| `model.score()` | 14.713 ms | 11.0% |
| `print(accuracy)` | 1.717 ms | 1.3% |

→ `model.fit()` is clearly the bottleneck (it trains the model). That's where to optimize.

| cProfile | line_profiler |
|----------|---------------|
| Profiles **functions** | Profiles **individual lines** |
| Shows *which function* is slow | Shows *which specific line inside a function* is slow |
| Best for identifying slow functions | Best for optimizing code within a function |
| Answers: *"Which function is the bottleneck?"* | Answers: *"Which line inside that function is the bottleneck?"* |

### Memory: `memray` / `memory_profiler`

Unlike cProfile (time) and line_profiler (line-by-line time), these measure **memory usage**.
- **memray** — memory profiler by Bloomberg; **Mac & Linux only** (not Windows).
- **memory_profiler** — used on **Windows**.

They answer: which function allocates the most memory? how much? where are leaks? which lines consume the most?

```
Line #   Mem usage   Increment  Occurrences  Line Contents
=========================================================
   11   118.0 MiB   118.0 MiB       1   @profile
   12                                   def train_model():
   15   118.1 MiB     0.1 MiB       1       iris = load_iris()
   20   118.2 MiB     0.1 MiB       1       X_train, X_test, y_train, y_test = train_test_split(...)
   23   118.2 MiB     0.0 MiB       1       model = RandomForestClassifier(n_estimators=5, max_depth=2)
   26   118.6 MiB     0.4 MiB       1       model.fit(X_train, y_train)   ← biggest memory bump
   29   118.6 MiB     0.0 MiB       1       accuracy = model.score(X_test, y_test)
```

| Column | Meaning |
|--------|---------|
| **Mem usage** | How much memory the program is using *now* |
| **Increment** | How much *extra* memory this line added |
| **Occurrences** | How many times the line executed |

> 📎 **MiB** = Mebibyte = 1,048,576 bytes. 1 MiB ≈ 1.05 MB.

---

## 5. The performance-analysis ladder

Climb from coarse to fine — each rung answers a sharper question:

```
time            → "how long did the whole thing take?"          (1 run, rough)
   ↓
timeit / %%timeit → "how long on average, how consistent?"      (many runs, avg ± std)
   ↓
cProfile        → "WHICH FUNCTION is the bottleneck?"           (per-function time)
   ↓
line_profiler   → "WHICH LINE inside it is slow?"               (per-line time)
   ↓
memray / memory_profiler → "which line/function eats MEMORY?"   (per-line memory)
```

> 🎯 **Measure before you optimize.** Start coarse (`time`), confirm with a benchmark (`timeit`), locate the slow *function* (`cProfile`), zoom to the slow *line* (`line_profiler`), and check *memory* separately (`memray`/`memory_profiler`).

---

## 🎯 Recap

- **SE vs ML coding:** SE devs write the rules in code; ML devs write code that **learns** the rules — so ML bugs are often fixed in **data/features/training**, not app logic.
- **Good code = 5 features:** **Simplicity (DRY) · Modularity · Readability (PEP 8 + pylint) · Performance · Robustness.**
- **Analysing performance:** make Python faster via algorithm / data-structure / built-ins / async / parallelism — but **measure first**.
- **Tool ladder:** `time` → `timeit`/`%%timeit` → `cProfile` (function) → `line_profiler` (line) → `memray`/`memory_profiler` (memory).

⬅️ **Prev:** [Session 7 — Agentic AI & coordination patterns](Session-07-Agentic-AI-and-Coordination-Patterns.md) · 🏠 [Back to index](README.md)
