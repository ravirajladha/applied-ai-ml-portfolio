# SE4ML — Post-Midsem Question Bank (Sessions 9–16) ⭐ HIGH WEIGHTAGE

> **AIMLCZG546** · Modules 4–7 · Built for the **open-book end-sem (40%, 2.5 hrs)**.
> Every question here is **conceptual** or **scenario** — the two formats this paper is expected to use.
> **§ numbers match the cheat sheet**, so anything you miss is one click away.

---

## How to use this

1. **Read the question. Answer it out loud or on paper *first*.** Do not open the answer box.
2. Open the box, compare, mark yourself: ✅ got it · 🟡 half · ❌ missed.
3. Anything ❌ → go back to the cheat-sheet **§** named in the heading, not to the whole note.

**Question codes:** **C** = conceptual (define, compare, agree/disagree) · **S** = scenario (a situation → your decision + justification).

**The scenario answer shape — use it every single time:**

```
1. NAME    the pattern/strategy in the course's own vocabulary.
2. JUSTIFY against the constraint the scenario gave you
           (cost / risk / latency / team size / regulation).
3. TRADE-OFF — say what you are accepting in exchange.
4. If it asks for "use cases", give ONE concrete example per option.
```

> ⚠️ In an *agree/disagree* question: **commit first**, then restate the correct version in the course's vocabulary. A hedged answer scores the commit mark and loses the justification mark.

---

# MODULE 4 — Implementation & Code Sharing (S9–S11)

## 1. Good code & performance profiling → §1

**C1.1** Name the **five features of good code**, and give a one-line test for each — how would you actually *check* a piece of code has it?

<details><summary><b>Show answer</b></summary>

| Feature | How you would check it |
|---|---|
| **Simplicity (DRY)** | is the same logic written twice anywhere? |
| **Modularity** | can I lift one function out and test it on its own? |
| **Readability** | does it pass **PEP 8 / pylint**, and can a new joiner read it without you? |
| **Performance** | has anyone actually **measured** it, or are we guessing? |
| **Robustness** | what happens on bad, missing or corrupt input — does it fail fast or corrupt silently? |
</details>

**C1.2** Put these in order and say what each tells you that the previous one could not: `cProfile`, `time`, `line_profiler`, `memray`, `timeit`.

<details><summary><b>Show answer</b></summary>

```
time          → how long did the whole thing take?         (1 run, rough)
timeit        → how long on AVERAGE, how consistent?       (many runs, avg ± std)
cProfile      → WHICH FUNCTION is the bottleneck?          (per-function)
line_profiler → WHICH LINE inside it is slow?              (per-line)
memray        → which line/function eats MEMORY?           (per-line memory)
```

**The escalation logic: whole → average → function → line → memory.** Each rung narrows the search, and you only pay its extra overhead once the previous rung has stopped being specific enough.
</details>

**S1.1 · Scenario.** A teammate says: *"Training takes 40 minutes. I will rewrite the whole feature-engineering module in Cython this sprint."* Nothing has been profiled. What do you tell them, and what is your actual first step?

<details><summary><b>Show answer</b></summary>

**Disagree — this is optimising before measuring.** The course rule is **measure first**. There is no evidence feature engineering is the bottleneck at all; it could be data loading, or one accidental `O(n²)` line.

**First step:** run **`cProfile`** over the training script to find *which function* dominates, then **`line_profiler`** on that one function to find *which line*.

**Then climb the ladder in order of cheapness:** better **algorithm** → better **data structure** → **built-ins / vectorisation (NumPy)** → **async** → **parallelism**. A Cython rewrite is the most expensive and least maintainable rung — a last resort, not a first sprint.

**Trade-off named:** you spend an hour profiling to avoid spending a sprint on a rewrite that may deliver nothing.
</details>

---

## 2. Time complexity & Big-O → §2

**C2.1** Define **time complexity** and **Big-O**, and say what **n** and **d** are in the ML setting.

<details><summary><b>Show answer</b></summary>

- **Time complexity** = how the running time **grows as the input grows** — not how many seconds it takes on your laptop.
- **Big-O** = the **order (growth rate)** of that function — the shape of the curve, ignoring constants.
- **n** = number of **samples (rows)** · **d** = number of **features (columns)**.

> Big-O is about **scaling**, not speed. An O(n²) routine can beat an O(n) one on 10 rows and be unusable on 10 million.
</details>

**C2.2** Match each complexity to its ML operation: `O(1)` · `O(log n)` · `O(n)` · `O(n log n)` · `O(n²)` · `O(n!)`.

<details><summary><b>Show answer</b></summary>

| Big-O | Name | ML example |
|---|---|---|
| **O(1)** | Constant | prediction **lookup**, dict access, array index |
| **O(log n)** | Logarithmic | **threshold search** / binary search |
| **O(n)** | Linear | full scan of the dataset |
| **O(n log n)** | Linearithmic | **ranking** customers by score (sort-like) |
| **O(n²)** | Quadratic | **similarity computation** (every item vs every other) |
| **O(n!)** | Factorial | brute-force **feature optimisation** (every ordering) |

> 🎯 **The cliff is at O(n²)** — double the data, quadruple the time.
</details>

**S2.1 · Scenario.** A recommender computes pairwise similarity across all users to find "people like you". Fine at 5,000 users; times out at 500,000. Explain **why** in Big-O terms and give two fixes.

<details><summary><b>Show answer</b></summary>

**Why:** pairwise similarity is **O(n²)** — every user against every other. 5×10³ → 5×10⁵ users is **100× the users but ~10,000× the work**. Nothing is broken; the algorithm simply does not scale.

**Two fixes, each named as a rung of the ladder:**
1. **Better algorithm / data structure** — replace exhaustive comparison with **approximate nearest-neighbour search** over a vector index: roughly **O(log n)** per query instead of O(n) per user.
2. **Change the serving design** (§21) — precompute recommendations as an overnight **batch job** and serve them as **cached predictions**, so the expensive work never sits on the request path.

**Trade-off:** approximate search gives up exactness for scale; caching gives up freshness for latency.
</details>

**C2.3** Why is `log₂(n)` such a big deal? Quote the table.

<details><summary><b>Show answer</b></summary>

**log₂(n) = how many times you can halve n before you reach 1.**

| Dataset size | O(n) | O(log n) |
|---|---|---|
| 1,000 | 1,000 ops | **10** |
| 100,000 | 100,000 ops | **17** |
| 1,000,000 | 1,000,000 ops | **20** |
| 1,000,000,000 | 1,000,000,000 ops | **30** |

**A billion rows costs 30 steps.** That is why indexes, binary search and tree structures dominate systems work.
**O(n) = check every item · O(log n) = discard half each step.**
</details>

---

## 3. The five ML data structures → §3

**C3.1** From memory: **List · Tuple · Dictionary · NumPy array · Pandas DataFrame** — nature, storage, access, key point.

<details><summary><b>Show answer</b></summary>

| Structure | Nature | Storage | Access | Key point |
|---|---|---|---|---|
| **List** | dynamic, **mutable**, heterogeneous | **contiguous** | **O(1)** by index | resizes as elements are added |
| **Tuple** | **immutable**, ordered, mixed types | **contiguous** | **O(1)** by index | immutability → **more memory-efficient**, read-only data |
| **Dictionary** | mutable **key–value** map; keys unique & immutable | **hash table** | **O(1) average** | hashes the key to jump straight to the value |
| **NumPy array** | mutable, **homogeneous**, multidimensional | **contiguous** | **O(1)** by index | one dtype + contiguous → **vectorised**, far faster than a list |
| **Pandas DataFrame** | 2-D **labelled** table, mixed column types | built **on NumPy** | label / positional | cleaning, filtering, sorting, grouping, missing values |
</details>

**S3.1 · Scenario.** You are writing an inference service. Name the structure and justify in one line: (a) loading the raw CSV, (b) the ordered feature names the model expects, (c) mapping a feature name → column index, (d) what you pass to `model.predict()`, (e) the fixed input image dimensions.

<details><summary><b>Show answer</b></summary>

| Task | Structure | Why |
|---|---|---|
| (a) Load raw CSV | **Pandas DataFrame** | labelled 2-D table, built for cleaning and missing values |
| (b) Ordered feature names | **List** | ordered and **mutable** — the set changes as features are added |
| (c) Name → index map | **Dictionary** | **O(1) average** hash lookup, no scanning |
| (d) Input to `predict()` | **NumPy array** | homogeneous + contiguous → **vectorised** maths |
| (e) Image dimensions | **Tuple** | it **must not change** — and immutability is cheaper in memory |

> 🎯 *DataFrame to prepare · NumPy to train · dict to look up · list for things that change · tuple for things that must not.*
</details>

**C3.2** *"A tuple is just a list you cannot edit, so it has no real advantage."* Agree or disagree, with justification.

<details><summary><b>Show answer</b></summary>

**Disagree.** Immutability is the feature, not the limitation.

- Because a tuple **cannot change size or content**, Python stores it **more memory-efficiently** than a list.
- It can be used where a list cannot — e.g. as a **dictionary key**, since keys must be immutable.
- **Engineering point:** using a tuple for data that must never change (image dimensions, dataset shape, a coordinate) converts a whole class of bug into an **immediate error** rather than a silent corruption. That is **fail fast** (§5) applied at the data-structure level.
</details>

---

## 4. OOP for Agentic AI → §4

**C4.1** Map each OOP concept onto Agentic AI: **Class · Object · Inheritance · Polymorphism · Encapsulation · Abstraction · Composition.**

<details><summary><b>Show answer</b></summary>

| OOP concept | In Agentic AI |
|---|---|
| **Class** | an agent implemented as a class defining attributes and behaviours (`Agent`, `ValidationAgent`) |
| **Object** | each **running** agent, with its own state, memory and execution context |
| **Inheritance** | specialised agents inherit from a common base `Agent` and extend it |
| **Polymorphism** | different agents implement the **same method `execute()` differently**, by role |
| **Encapsulation** | memory, goals and internal logic held **inside** the class, reached only through methods |
| **Abstraction** | reasoning, planning and tool invocation hidden behind a simple interface (`ask_llm()`) |
| **Composition** | multiple agent objects combined into a **multi-agent system** — `ResearchPaperWorkflow` **has-a** validator and a summariser |

**Functional programming sits alongside it:** standalone stateless helpers — `read_paper()` (reads a PDF), `save_result()` (writes the summary).
</details>

**S4.1 · Scenario.** A team's multi-agent document pipeline is one 900-line script with dozens of `if/else` branches picking which prompt to send. Every new document type means editing that chain, and it keeps breaking. Recommend a redesign, justified in OOP terms.

<details><summary><b>Show answer</b></summary>

**Diagnosis:** this is the **procedural** design — *one director holding the camera, doing the makeup, writing the script and sweeping the floor.* It is **fragile, unscalable and crashes on minor changes**, because every behaviour lives in one branching blob.

**Redesign — the Hollywood production crew:**
- A base **`Agent`** class, the "Crew Member" — **class**.
- Specialised roles by **inheritance**: `ValidationAgent` (Director), `SummaryAgent` (Writer), `FormattingAgent` (Cinematographer).
- Each keeps its own model, client and memory inside itself — **encapsulation**; the LLM call hides behind `ask_llm()` — **abstraction**.
- A `Workflow` object **has-a** validator and a summariser — **composition** — and just says "execute!"; each subclass does its own thing — **polymorphism**.

**The payoff, phrased the way the exam wants:** adding a Sound Engineer is **a new subclass, not a rewrite** — which is exactly the **Open/Closed** principle (§5).

**Trade-off:** more files and more indirection up front; you buy testability and safe extension.
</details>

**C4.2** Where does **functional** programming still belong in an OOP agent system, and why not make everything a class?

<details><summary><b>Show answer</b></summary>

**Use plain functions for stateless work** — `read_paper()` reads a PDF, `save_result()` writes a summary. They hold **no state**, have **no identity**, and nothing needs to inherit from them.

**Why not a class:** a class earns its keep when there is **state to encapsulate** (memory, goals, a model client) or **behaviour to specialise** (`execute()` overridden per role). Wrapping a pure input→output transform in a class adds ceremony and buys nothing.

> 🎯 **State and specialisation → class. Pure transformation → function.**
</details>

---

## 5. Errors, logging, style & refactoring → §5

**C5.1** What does **fail fast** mean, and why is a bare `except:` specifically dangerous?

<details><summary><b>Show answer</b></summary>

**Fail fast** = code must **never behave unpredictably on corrupt data**. Raise **descriptive, actionable exceptions immediately**, so corrupted data does not propagate down the pipeline and poison everything downstream.

**Why a bare `except:` is dangerous:** it catches **everything** — including **system interrupts and memory-exhaustion errors** — leaving the system in an **unstable zombie state**: apparently alive, actually broken.

**The correct handler:** catch the *specific* exception → **log a descriptive message** with the `logging` library → **return a clean, predictable default**.

**Custom exceptions:** native `ValueError`/`TypeError` are too generic to act on. Inherit from `Exception` to name the **domain failure** — `IncompatibleFeatureSizeError`, `ModelWeightsNotLoadedError`.
</details>

**S5.1 · Scenario.** A 48-hour EC2 training job printed per-epoch losses with `print()`. At hour 39 the SSH session dropped; on reconnect the terminal is empty. What was lost, what should have been done, and what do you put in place next time?

<details><summary><b>Show answer</b></summary>

**What was lost:** everything. `print()` writes to the terminal's stdout buffer — an SSH disconnect or a cleared buffer loses **all 39 epochs of loss history forever**. The job may still be running, but you can never say what it did.

**What should have been done:** use the **`logging`** library, which pipes output to a **persistent file** and/or a central sink — **CloudWatch** or **Elasticsearch** — that outlives the session.

**Levels:** `DEBUG → INFO → WARNING → ERROR → CRITICAL`. Per-epoch loss = **INFO**; a NaN loss or skipped batch = **WARNING**; an unrecoverable CUDA fault = **CRITICAL**.

> *"If you do not build logging and error handling into your system, your users will become your loggers."*
</details>

**C5.2** State the **objective of PEP 8** in the deck's own words; name what it covers and the four tools.

<details><summary><b>Show answer</b></summary>

**Objective:** *ensure all Python code written by any engineer looks like it was written by the **exact same person**.*

| Covers | Rule |
|---|---|
| **Naming** | variables/functions **snake_case**; classes **PascalCase** |
| **Whitespace** | **4 spaces** per indent level, **never tabs**; single spaces around operators |
| **Import ordering** | **standard library → third-party → local**, blank line between groups |

**Tools:** **black** (auto-formatter) · **flake8 / pylint** (linters) · **isort** (imports) · **mypy** (**static type checker** — parses type annotations and finds type mismatches across the whole program).

**Type hints as a contract:** `def scale(data: List[float], factor: float) -> List[float]:` — the annotations tell **both the developer and the machine** what is required, and the **return type completes the contract**.
</details>

**S5.2 · Scenario.** A data scientist hands you a notebook that trains a model. It runs top-to-bottom on their machine. You must productionise it. Using **Research vs Production**, name the concrete things that must change, and the one skew risk you must close.

<details><summary><b>Show answer</b></summary>

| Dimension | Research (what you got) | Production (what you build) |
|---|---|---|
| Goal | **rapid discovery and validation** | reliability, maintainability, scale |
| Environment | **Jupyter notebook**, interactive | modules, packages, services |
| Style | **imperative and sequential** | modular — functions and classes |
| State | **global variables scattered everywhere** | encapsulated, passed explicitly |
| Execution order | **manual** (whatever order the cells were run) | deterministic, orchestrated |
| Duplication | **code duplicated** between cells | DRY, shared libraries |
| Errors | crash and fix by hand | **fail fast, log, degrade gracefully** |
| Tests | rare | **required** |
| Lifespan | days | **years** |

**The four highest-value moves:**
1. **Extract Function** — pull the 15-line scaling block into `scale_features()`; keep the main script high-level.
2. **Kill the global state** — pass data explicitly; hidden globals are exactly why "it works on my machine".
3. **Modularise** — split into `utils.py`, `preprocessing.py`, `train.py` once past a few hundred lines.
4. **Add tests and logging** — the lifespan just went from days to years.

⚠️ **The skew risk:** the **feature-encoding code must become a shared library used by both training and inference** — otherwise you get **training/serving skew** (§20): nothing crashes, every prediction is quietly wrong.
</details>

**C5.3** Define **refactoring**, then map **SOLID** onto an ML pipeline.

<details><summary><b>Show answer</b></summary>

**Refactoring** = *changing a software system's **internal structure** without modifying its **external behaviour**.* If the outputs change, it is not a refactor — it is a rewrite.

**Moves:** **Extract Function** · **Rename Variables** (`x`, `df`, `m` → `user_demographics_df`, `random_forest_model`) · **Modularise** past a few hundred lines.

| | Principle | In a pipeline |
|---|---|---|
| **S** | Single Responsibility | separate loader / feature engineer / trainer / server classes |
| **O** | Open/Closed | a new model is a **new subclass**, not an edit to an `if/elif` chain |
| **L** | Liskov Substitution | any `Model` subclass honours `.fit()` / `.predict()` |
| **I** | Interface Segregation | a batch scorer is not forced to implement streaming methods |
| **D** | Dependency Inversion | the trainer depends on an abstract `DataSource` — swap CSV → S3 → feature store in one place |
</details>

**S5.3 · Scenario.** Training reads a local CSV. Next quarter it must read S3, the quarter after a feature store. A junior proposes `if source == "csv": ... elif source == "s3": ...` inside the trainer. Which SOLID principles does that break, and what do you propose?

<details><summary><b>Show answer</b></summary>

**Breaks two clearly:**
- **Open/Closed** — every new source means **editing** the trainer instead of **extending** it.
- **Dependency Inversion** — the trainer (high-level policy) now depends on **concrete** storage details.

Arguably **Single Responsibility** too: the trainer has quietly become a data-access layer as well.

**Proposal:** define an abstract **`DataSource`** interface with a `load()` method. `CSVSource`, `S3Source` and `FeatureStoreSource` implement it; the trainer accepts *a* `DataSource` and never knows which. **Adding the feature store is a new class, and the tested trainer file is never touched.**

**Trade-off:** one extra abstraction layer to maintain — cheap insurance against editing working training code every quarter.
</details>

---

## 6. APIs & packaging → §6

**C6.1** Give the **three reasons** to wrap a model in a web API rather than embedding it, and name FastAPI's standout feature.

<details><summary><b>Show answer</b></summary>

| Reason | Explanation |
|---|---|
| **Decoupling** | your backend may be **Java, C# or Go** — an HTTP service gives **language independence** |
| **Independent scaling** | inference is **computationally expensive** and often needs a **GPU**; scale prediction servers **separately** from web servers, saving cloud cost |
| **Seamless model updates** | deploy a better model to the API server **without redeploying the main application** |

**FastAPI** is built on **asynchronous programming** and **type hints**. Its standout feature is **automatic documentation**: an interactive **Swagger UI at `/docs`** generated just by writing the code, so teammates test the model **in the browser** with no Postman.
</details>

**S6.1 · Scenario.** A Java e-commerce backend needs a Python fraud model. The model needs a GPU; the web tier does not. Data science ships a new model roughly every two weeks. Design the integration and justify each decision.

<details><summary><b>Show answer</b></summary>

**Design:** **model inference as a Service** (§21) — the model wrapped in a **FastAPI** app exposing a **REST** endpoint, containerised with **Docker**, run as its own **Kubernetes Deployment**.

**Justify against each constraint the scenario handed you:**
1. *Java backend, Python model* → **decoupling / language independence**. HTTP is the common denominator; no JNI, no rewrite.
2. *GPU only for inference* → **independent scaling**. The prediction service sits on GPU nodes and scales alone; the web tier stays on cheap CPU nodes. A direct cloud-cost saving.
3. *A new model every two weeks* → **seamless model updates**. Ship a new image to the inference service; the e-commerce application is never redeployed.

**Roll each new model out with a Canary** (§22) — a fraud model is unproven against live traffic and a canary keeps the blast radius small.

**Trade-off accepted:** a **network hop** on every prediction (added latency, a new failure mode) and one more service to operate — bought in exchange for language independence, separate GPU scaling and an independent release cadence.
</details>

**C6.2** Complete the packaging table — what do **Git · DVC · Conda · Poetry · Docker** each pin? Why is `requirements.txt` not enough?

<details><summary><b>Show answer</b></summary>

| Layer | Tool | Pins |
|---|---|---|
| Code | **Git** — feature branches + PRs, **never commit to `main`** | source |
| Data & models | **DVC** — Git bloats on large binaries; DVC tracks them in **cloud storage** | datasets, model files |
| Dependencies | **`requirements.txt`** (legacy) · **Conda** (also manages **non-Python packages, C++ and GPU drivers**) · **Poetry** (**deterministic resolution**; `poetry.lock` locks **every library and transitive dependency down to the patch release**) | package versions |
| Environment | **Docker** | OS, runtime, everything |

**Why `requirements.txt` is not enough:** it usually pins only your *direct* dependencies, so a **transitive** dependency can silently update and change behaviour. **Poetry's lock file pins the entire tree down to the patch release**, and **Conda** additionally covers the **non-Python** layer (C++ libraries, GPU drivers) that pip cannot see at all.
</details>

**C6.3** A Dockerfile has `COPY . .` *before* `RUN pip install -r requirements.txt`. What is wrong, and what is the rule?

<details><summary><b>Show answer</b></summary>

**Wrong:** Docker caches layer by layer. With the code copied first, **any** code edit invalidates the cache from that line onward, so `pip install` re-runs on every single build — minutes wasted each time.

**The rule — copy dependency files *before* the code:**

```
FROM python:3.12-slim               # clean Python base
COPY requirements.txt .             # dependency file FIRST
RUN pip install -r requirements.txt # this layer stays cached
COPY . .                            # code last — it changes often
CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
```

**Shape to memorise:** `FROM` → `COPY` deps → `RUN` install → `COPY` code → `CMD`.
</details>

---

# MODULE 5 — Quality Assurance (S12)

## 7. Traditional vs ML testing → §7

**C7.1** Compare **traditional software testing** and **ML testing** on logic, what tests verify, and failure modes.

<details><summary><b>Show answer</b></summary>

| | **Traditional software** | **Machine learning** |
|---|---|---|
| Logic | **explicitly programmed** | **learned from data** |
| Tests verify | whether the logic produces **expected outputs** | the **learning process**, **data integrity** and **statistical outputs** |
| Failure modes | **bugs** | **concept drift · data corruption · biased training data** |

> 🎯 In traditional software a test asks *"is this output right?"* In ML there is often **no single right output** — you test the *process* and the *statistics*, because the logic itself was never written down by anyone.
</details>

**C7.2** Name the **four ML-specific testing dimensions** and what each validates.

<details><summary><b>Show answer</b></summary>

| Dimension | Validates |
|---|---|
| **Data tests** | schemas, missing values, feature distributions |
| **Model tests** | predictive performance, fairness, robustness to edge cases |
| **Infrastructure tests** | stress-test serving APIs, measure inference latency |
| **Heuristic tests** | common-sense rules — e.g. **age cannot be negative** |

**The MLOps control loop they sit inside:**
`Data → Features → Training → Registry → Serving → Monitoring → (triggers retraining) → Data`
</details>

**S7.1 · Scenario.** A manager says: *"We have 95% unit-test coverage on the ML repo, so the model is well tested."* Agree or disagree, with justification.

<details><summary><b>Show answer</b></summary>

**Disagree.** Unit tests cover the **explicitly programmed** code — the ~5% of the system that is ML code, plus the glue. They say nothing about the parts where ML actually fails.

**The correct version:** ML testing must cover **four dimensions** —
- **Data tests** — schema, missing values, distributions. A silently changed upstream schema passes every unit test.
- **Model tests** — predictive performance, **fairness**, robustness to edge cases, evaluated **per slice** (§11), not as one aggregate.
- **Infrastructure tests** — serving API under stress, inference latency.
- **Heuristic tests** — common-sense rules such as age cannot be negative.

**And the failure modes differ:** traditional software fails from **bugs**; ML fails from **concept drift, data corruption and biased training data** — none of which a unit test can see. Coverage of the code is not coverage of the system.
</details>

---

## 8. Data quality & the validation gates → §8

**C8.1** *Garbage in, garbage out* — state the four reasons the deck gives for why data quality dominates, and name the six quality dimensions.

<details><summary><b>Show answer</b></summary>

**Why it dominates:**
1. **Data quality dictates the upper bound of model performance.**
2. **Historical data may contain human biases that the model will amplify.**
3. **Errors in collection pipelines silently degrade production systems.**
4. **Automated data validation is a strict requirement before any training begins.**

**Six dimensions:** **Accuracy · Completeness · Consistency · Timeliness/Freshness · Validity · Uniqueness.**
</details>

**C8.2** Name the **gates of the data validation pipeline** and what each catches. What does the Action Gateway do?

<details><summary><b>Show answer</b></summary>

| Gate | Checks for |
|---|---|
| **Ingestion** | raw data from product events, IoT streams, CRM tools |
| **Schema Check Gate** | **missing columns, type changes** |
| **Value Check Gate** | **impossible ranges** (negative age), **statistical outliers** |
| **Label Health Gate** | **extreme class imbalance, missing target labels** |
| **Action Gateway** | if inputs do not match expectations, **the pipeline automatically halts** |

> 🎯 The Action Gateway is the whole point: validation that only *warns* gets ignored. **It stops the pipeline** so bad data can never reach training.
</details>

**S8.1 · Scenario.** An upstream team renames `customer_age` to `age_years` and starts sending age in months for one region. Nothing crashes. Two weeks later, model accuracy has quietly fallen. Which gates should have caught which problem, and what should have happened?

<details><summary><b>Show answer</b></summary>

**Two distinct failures, two distinct gates:**

| Problem | Gate that should catch it | How |
|---|---|---|
| `customer_age` renamed to `age_years` | **Schema Check Gate** | a **missing column** (and an unexpected new one) — a pure schema violation |
| Age sent in months for one region | **Value Check Gate** | ages of 480, 600 are **impossible ranges** / **statistical outliers** for a human age field |

**What should have happened:** the **Action Gateway** halts the pipeline the moment either gate fails, so **no training run ever consumes the corrupt data**. Instead, both slipped through and the failure surfaced two weeks later as an unexplained accuracy drop — the textbook case of *"errors in collection pipelines silently degrade production systems"*.

**Also worth saying:** because the corruption hit **one region**, an aggregate accuracy number would barely move. **Slicing by region** (§11) is what makes it visible. And in production you often have **no labels yet**, so the earliest available symptom is a shift in the **prediction distribution** (§12).
</details>

---

## 9. Pipeline quality → §9

**C9.1** Define **pipeline quality** and its three properties. Why does **idempotency** matter so much in ML?

<details><summary><b>Show answer</b></summary>

**Pipeline quality** = the **robustness of the automated sequence from data extraction to model deployment**.

| Property | Meaning |
|---|---|
| **Idempotency** | **re-running with the same inputs must yield the exact same outputs** |
| **Version control** | **code, data and model artifacts linked and versioned together** |
| **Orchestration** | **Airflow / Kubeflow** manage the complex dependency graphs |

**Why idempotency matters:** without it you can never **reproduce** a result (§25), never safely **retry** a failed step, and never trust that a rerun debugging a bad model is showing you the same model. A non-idempotent pipeline turns every incident into guesswork.
</details>

**C9.2** What does **CI for ML** run that CI for ordinary software does not?

<details><summary><b>Show answer</b></summary>

| Trigger | CI action |
|---|---|
| Code commits | syntax checks + unit tests *(same as normal software)* |
| **Architecture changes** | **train on a small synthetic dataset** — proves the pipeline runs end to end without a full training run |
| **Schema updates** | **validate against historical data** — proves the change does not break past data |
| All pass | produce a **deployable artifact in a central registry** |

> 🎯 The ML-specific part: CI must test the **data contract** and the **training path**, not just the code.
</details>

---

## 10. Model quality & metrics → §10

**C10.1** Write the formulas for **Precision, Recall, F1, RMSE** and the question each answers.

<details><summary><b>Show answer</b></summary>

| Metric | Formula | Answers |
|---|---|---|
| **Precision** | **TP / (TP + FP)** | of what I **flagged**, how much was right? *(accuracy of positive predictions)* |
| **Recall** | **TP / (TP + FN)** | of what **was** positive, how much did I catch? *(ability to find all positives)* |
| **F1** | **2PR / (P + R)** | **balances precision and recall for imbalanced data** |
| **RMSE** | **√(mean squared error)** | regression — **penalises large errors heavily** |

> **Spam filter → precision. Cancer screening → recall. Imbalanced / cannot choose → F1.**
</details>

**S10.1 · Scenario.** A fraud model reports **99.9% accuracy**. Fraud occurs in 1 of every 1,000 transactions. The business is delighted. What do you say, and which metrics do you ask for?

<details><summary><b>Show answer</b></summary>

**Say:** **accuracy is misleading on imbalanced data.** A model that predicts *"no fraud"* for every single transaction is **also 99.9% accurate — and worthless**, because it catches zero fraud. The headline number is measuring the class imbalance, not the model.

**Ask for:**
- **Recall** — of all actual fraud, how much did we catch? This is the business-critical number; a missed fraud is money gone.
- **Precision** — of everything we flagged, how much was really fraud? This governs how many legitimate customers get blocked.
- **F1** — the balance, which is the right headline for **imbalanced data**.
- **Sliced metrics** (§11) — per region, per card type, per device.

**The trade-off to state:** raising recall catches more fraud but flags more innocent customers (precision falls). Where you sit on that curve is a **business decision**, not a modelling one.

**Two more course points worth a mark:** model quality also includes **interpretability, fairness and computational efficiency**; and it must be evaluated on data **strictly unseen during training**, because **quality degrades over time**.
</details>

**S10.2 · Scenario.** Two products, one question each. (a) A spam filter for a corporate mailbox. (b) An early cancer-screening triage model. Which metric do you optimise for each, and what is the cost of being wrong?

<details><summary><b>Show answer</b></summary>

**(a) Spam filter → optimise PRECISION.**
A **false positive** means a real business email is silently sent to the spam folder — potentially a lost contract. A **false negative** just means one junk mail in the inbox, which the user deletes in a second. **The costly error is the false positive, and precision is the metric that controls it.**

**(b) Cancer screening → optimise RECALL.**
A **false negative** means a real case is sent home undiagnosed — potentially fatal, and this is a **safety-critical** system (§28). A **false positive** means an unnecessary follow-up test: unpleasant and costly, but recoverable. **The costly error is the false negative, and recall is the metric that controls it.**

> 🎯 **The rule generalises: pick the metric that punishes the error you cannot afford.** If the classes are heavily imbalanced and you genuinely cannot choose, report **F1** — but say which error you would rather make.
</details>

---

## 11. Slicing & subpopulation testing → §11

**C11.1** What is **data slicing**, and what is the one-line rule about aggregate metrics?

<details><summary><b>Show answer</b></summary>

**Data slicing** = divide the test set into **subgroups** (gender, location, device type) → **calculate metrics independently per slice** → identify where the model needs **active mitigation or retraining**.

> **A model with 95% global accuracy might have 50% accuracy on a minority demographic.**

> 🎯 **Never report a single aggregate number — an average is where failures hide.** This is also **how fairness (§27) is measured operationally**: fairness is not a philosophical claim, it is a sliced metric.
</details>

**S11.1 · Scenario.** A speech-to-text product reports 94% word accuracy and is approved for launch. Post-launch, complaints cluster from users in one region on low-end Android phones. What was the testing failure, and what would you have done before launch?

<details><summary><b>Show answer</b></summary>

**The failure:** the team reported **a single aggregate number**. 94% overall can easily hide **50% accuracy on a minority subpopulation** — and that is exactly what happened. The average is where failures hide.

**What should have been done — slicing before launch:**
1. Split the test set by the dimensions the deck names: **location / accent, device type**, plus recording conditions.
2. **Compute the metric independently per slice.**
3. Any slice materially below the aggregate is a **release blocker** until mitigated — through **retraining with more data for that slice** or explicit **active mitigation**.

**Connect it to two other topics for full marks:**
- This is also the operational test for **fairness** (§27) — a group being systematically worse served *is* the fairness failure.
- In production, keep slicing: **monitor group outcomes continuously**, since offline data is static while user behaviour is dynamic (§13).
</details>

---

## 12. System quality & monitoring → §12

**C12.1** *"A more accurate model always means a better product."* Agree or disagree.

<details><summary><b>Show answer</b></summary>

**Disagree.** **The ML model is often less than 5% of the total codebase.** System quality also covers **UI/UX, database reliability and network stability** — and **a perfect model with a failing front-end has zero business value.**

**The correct version:** optimise the **end-to-end product** — latency, reliability, monitoring, user experience — not just offline accuracy. Accuracy is one quality attribute among many; robustness, explainability, fairness, privacy and latency are first-class too.
</details>

**C12.2** Name the **monitoring layers** and what each watches. In production, with no labels yet, what is your earliest symptom of drift?

<details><summary><b>Show answer</b></summary>

| Monitoring layer | Watch |
|---|---|
| **System metrics** | CPU, memory, network latency |
| **Model metrics** | **prediction distribution, confidence scores, anomaly rates** |
| **Business metrics** | click-through, conversion, revenue |
| **Alerting** | automated thresholds that **page engineers** on significant deviation |

> 💡 **Earliest symptom with no labels:** watch the **prediction distribution**. You cannot compute accuracy without ground truth, but a **sudden shift in the distribution of predictions** is the earliest available signal that the input world has changed.
</details>

---

## 13. Testing in production → §13

**C13.1** Why is offline testing not enough? Give the four reasons.

<details><summary><b>Show answer</b></summary>

1. Offline data is **static** while user behaviour is **dynamic**.
2. **Models change user behaviour, creating feedback loops that offline tests cannot simulate.**
3. Production experimentation is the **final proof of business impact**.
4. It requires **infrastructure to route traffic securely** — which is itself a system-design concern.
</details>

**C13.2** Compare **Shadow · A/B · Canary** on who sees the new model, user impact if it is bad, and the question each answers.

<details><summary><b>Show answer</b></summary>

| Strategy | Who sees the new model | User impact if bad | Answers |
|---|---|---|---|
| **Shadow** | **nobody** — it gets a **copy** of live traffic, predictions **logged not served** | **none** | *"does it work at production load?"* |
| **A/B test** | a **split** of users, each group a different version | half your users | *"is it **better**?"* |
| **Canary** | a **small subset** first, expanded if healthy | limited blast radius | *"is it **safe to expand**?"* |

> 🎯 **Shadow proves it runs · A/B proves it is better · Canary proves it is safe to expand.**
</details>

**S13.1 · Scenario.** You have a new clinical-triage model. It is faster and scores better offline, but a bad prediction can harm a patient. Sequence the production testing and justify each step.

<details><summary><b>Show answer</b></summary>

**Sequence: Shadow → Canary → (only then) A/B.** The order is driven by **blast radius**, because this is a **safety-critical** system (§28).

1. **Shadow first.** The new model receives a **copy of live traffic**; predictions are **logged, never served**. **No user impact at all.** This answers *"does it work at production load?"* — latency, memory, unseen input shapes — with zero patient risk. Compare its logged predictions against the incumbent's.
2. **Canary next.** Release to a **small subset** with **limited blast radius**, under clinician review, and expand only if healthy. This answers *"is it safe to expand?"*
3. **A/B last, if at all.** An A/B split exposes **half your users** to the new version, which for a clinical system may be ethically unacceptable. Only run it once shadow and canary have established safety, and only to answer *"is it actually better?"*

**Trade-off stated:** this sequence is **slow** — three stages before full rollout — and you accept that deliberately, because the cost of a bad prediction here is **harm to a patient**, not a lost click.

**Add for full marks:** keep **human-in-the-loop** override throughout (design for mistakes), and monitor **per slice** (§11) — a model can be safe on average and dangerous for one demographic.
</details>

---

## 14. Security for ML → §14

**C14.1** Name the ML attacks by lifecycle phase, and say which two phases are most frequently targeted and why.

<details><summary><b>Show answer</b></summary>

| Lifecycle phase | Attack | What it does |
|---|---|---|
| **Data collection** ⚠️ | **Data poisoning** | crafted samples injected into training data corrupt or backdoor the model |
| Training | **Backdoor / trojan** | normal behaviour except on a secret trigger |
| Model storage | **Model theft / extraction** | weights stolen, or reconstructed by repeated API queries |
| **Deployment / inference** ⚠️ | **Adversarial examples** | tiny input perturbations flip the prediction |
| Inference | **Membership inference** | determines whether a person's record was in the training set |
| LLM serving | **Prompt injection** | malicious instructions hidden in input or in retrieved documents |

> ⚠️ **Data collection and deployment are the most frequently targeted** — they are **the two ends where external input enters the system**. Everything in between is comparatively under your control.
</details>

**S14.1 · Scenario.** Your public image-classification API starts returning wrong labels for a handful of customers, but only for specific uploaded images. Internal test images all classify correctly. Name the likely attack, two others you should rule out, and your response.

<details><summary><b>Show answer</b></summary>

**Most likely: adversarial examples** — **tiny input perturbations that flip the prediction**, invisible to a human and absent from your clean internal test set. It is an **inference-time** attack, which is why retesting the model offline finds nothing.

**Rule out two neighbours:**
- **Backdoor / trojan** — normal behaviour **except on a secret trigger**. Test: does a specific visual pattern reliably force one class across otherwise unrelated images? If so, the corruption is in the **model**, not the request, and points back to **data poisoning** at collection time.
- **Model extraction** — check for a client making **repeated systematic queries**; that pattern suggests they are probing to **reconstruct the weights**, and adversarial crafting is often the next step.

**Response:**
1. **Robustness** (§28) — this is precisely *"can the ML system withstand hazards?"*: behave safely on **unexpected, unusual, corrupted, adversarial or deliberately manipulated inputs**. Add adversarial examples to the test set.
2. **Monitoring** — watch **anomaly rates and confidence scores**; adversarial inputs often sit at odd confidence.
3. **Integrity + Availability** (§29) — confirm the **deployed model has not been secretly replaced**, and rate-limit so the endpoint **stays operational despite malicious requests**.
4. **Threat modelling must be integrated early** — the deck's own point: ML introduces **vulnerabilities distinct from traditional web apps**, defending both the **IP (model weights)** and **data privacy**.
</details>

---

## 15. RAGAS → §15

**C15.1** What is **RAGAS**, what problem does it solve, and why are **BLEU/ROUGE** inadequate?

<details><summary><b>Show answer</b></summary>

**RAG** = Retrieval-Augmented Generation (an LLM plus an external database).

**The problem:** **BLEU and ROUGE are inadequate for measuring hallucination and context relevance** — they measure **word overlap**, which says nothing about whether the answer was invented. A fluent, well-worded lie scores well.

**RAGAS** = **Retrieval Augmented Generation Assessment** — an automated framework using an **LLM evaluator** to score the **distinct components** of a RAG pipeline **without human labels**.

**It evaluates two pipelines independently: the Retriever and the Generator.**
</details>

**C15.2** Name the **four RAGAS metrics**, which component each judges, and what it measures.

<details><summary><b>Show answer</b></summary>

| Evaluates | Metric | Measures |
|---|---|---|
| **Generator (LLM)** | **Faithfulness** | is the answer **strictly grounded in the retrieved context**? → **detects hallucination** |
| **Generator** | **Answer Relevance** | how well the answer **addresses the user's initial prompt** |
| **Retriever (vector search)** | **Context Precision** | are the top retrieved chunks **relevant, not noise**? |
| **Retriever** | **Context Recall** | did retrieval **fetch all the necessary facts**? |

> **High precision = no junk data. High recall = no missing facts.**
</details>

**S15.1 · Scenario.** Four RAG complaints land in your inbox. Diagnose each and name the fix.
(a) *"It answers confidently but the facts are not in our documents."*
(b) *"It says 'I don't have that information' — but the document definitely exists."*
(c) *"The answer is true but it does not actually answer what I asked."*
(d) *"Retrieval pulls in ten chunks and only two are on-topic."*

<details><summary><b>Show answer</b></summary>

| Complaint | Metric that flags it | Culprit | Fix |
|---|---|---|---|
| (a) Confident but ungrounded | Good context but **low faithfulness** | **the LLM invented something** | prompt / model |
| (b) Says it does not know, but the doc exists | Low **context recall** | **the retriever never fetched the fact** | chunking, embeddings, **top-k** |
| (c) True but off-question | Low **answer relevance** | the generator drifted off the prompt | prompt |
| (d) Ten chunks, two relevant | Low **context precision** | **noise crowding the context window** | **reranking**, tighter retrieval |

> 🎯 **The exam angle is diagnostic:** RAGAS earns its keep because it tells you **which half of the pipeline to fix** — retriever or generator. Without it, every complaint looks like "the LLM is bad".

**The two-step reasoning to show:** first ask *was the right context retrieved?* (context recall / precision — retriever). Only if the context was right does the blame move to the generator (faithfulness / answer relevance).
</details>

---

# MODULE 6 — Deployment (S13–S14)

## 16. Deployment & its four components → §16

**C16.1** Define **deployment**, then name its four components and what each does.

<details><summary><b>Show answer</b></summary>

**Deployment** = integrating a trained model into a **real-world production environment** so it predicts on **live, unseen data**, exposed via **REST or gRPC APIs**, and kept **scalable, reliable, secure and continuously monitored** as workloads and data evolve.

| Component | What it does |
|---|---|
| **Model packaging & containerisation** | model + **weights, dependencies, runtime, preprocessing** packaged into a portable, reproducible container with **Docker** |
| **Model serving** | deployed as a service exposing a **REST/gRPC API** via **FastAPI or Flask** |
| **Scalability & orchestration** | **Kubernetes** — **horizontal pod autoscaling, load balancing, self-healing, rolling updates** |
| **MLOps** | versioning, CI/CD, automated testing, deployment, monitoring, logging, performance tracking, **retraining** |

> 🎯 **Package · Serve · Orchestrate · Operate.**
</details>

---

## 17. Containers vs VMs → §17

**C17.1** Define a **container** and compare it with a **VM** across six dimensions. Tell the singer story.

<details><summary><b>Show answer</b></summary>

**A container** is a **standardised package of software** — **code, runtime, system libraries and settings all inside a single container**. *Build, Ship, Run — Any App, Anywhere.*

| | **Container** | **Virtual Machine** |
|---|---|---|
| **Virtualises** | the **operating system** | the **hardware** |
| **Guest OS** | none — **shares the host OS kernel** | a **full guest OS per VM** |
| **Size** | megabytes | gigabytes |
| **Startup** | **seconds** | minutes |
| **Overhead / density** | minimal / many per host | high / few per host |
| **Isolation** | process-level | hardware-level (**stronger**) |

> 🌍 **The singer analogy.** Concert 1 — the mike does not work. Concert 2 — the speakers do not work. So the singer **buys his own mike and speakers and carries them everywhere**, avoiding the vagaries of the venue. That is a container. It answers *"I cannot replicate the production issue in development."*
</details>

**S17.1 · Scenario.** A regulated bank must run two workloads on shared infrastructure: (a) 60 short-lived model-inference services that scale up and down all day, and (b) a legacy risk engine that requires its own OS and a hard tenancy boundary for audit. Containers, VMs, or both? Justify.

<details><summary><b>Show answer</b></summary>

**Both — pick per workload, not per company.**

**(a) 60 inference services → containers.** They are **megabytes not gigabytes**, start in **seconds not minutes**, carry **minimal overhead so you get high density per host**, and share the **host OS kernel**. Sixty VMs would mean sixty **full guest OSes**, which is exactly the overhead you cannot afford when scaling up and down all day. Autoscaling only makes sense at container start-up times.

**(b) Legacy risk engine → a VM.** It **requires its own OS**, which a container cannot give you — a container virtualises the **operating system** and shares the host kernel, while a VM virtualises the **hardware** and runs a full guest OS. And the audit requirement for a hard tenancy boundary needs **hardware-level isolation**, which is **stronger** than a container's **process-level** isolation.

**Trade-off stated plainly:** you accept the **gigabyte footprint and minute-long start-up** of the VM in exchange for the **stronger isolation and its own OS** that the regulator requires; and you accept containers' **weaker, process-level isolation** on the inference tier in exchange for **density and seconds-long scaling**.

**In practice:** run the containers **on** VM-backed Kubernetes nodes — that is the normal way to get both.
</details>

---

## 18. Docker's three things → §18

**C18.1** Define **Dockerfile · Image · Container** and draw the arrows between them.

<details><summary><b>Show answer</b></summary>

```
Dockerfile ──docker build──▶ Image ──docker run──▶ Container
 (blueprint,                  (template,             (running process
  set of instructions)         standalone package)    of the image)
```

| Term | Definition |
|---|---|
| **Dockerfile** | **blueprint for building an image** — a set of instructions in a text file named `Dockerfile` |
| **Docker Image** | **template for running containers** — a **lightweight, standalone, executable package** with **code, runtime, libraries, system tools** |
| **Docker Container** | a **portable unit of software** with the app + dependencies + configuration; the **running process of the image**. **One image can spawn multiple processes across environments.** |

**Keywords:** `FROM` · `RUN` (build time) · `COPY`/`ADD` · `WORKDIR` · `EXPOSE` · `ENV` · `CMD` (default run command) · `ENTRYPOINT` (always runs).
**Purpose:** **reproduce the environment** across Dev, Staging and Production. Share via **`docker push` / `docker pull`**. **Docker Hub** = the world's largest library of container images; **Docker Desktop** = the one-click GUI for Mac/Linux/Windows.
</details>

**C18.2** What exactly goes **inside** the container when you containerise an ML model?

<details><summary><b>Show answer</b></summary>

- the **trained model** — `.pkl` / `.onnx` / `.pt` / `.h5`
- the **inference code**
- the **dependencies**
- the **runtime environment**
- the **config files**
- optionally, **pre/post-processing** code

⚠️ That preprocessing code must be **the same shared library used in training** — see the encoding rule in §20, or you ship **training/serving skew** inside a perfectly reproducible container.
</details>

**S18.1 · Scenario.** *"It works on my machine but fails in staging."* The model, the code and the requirements file are all identical. Explain what Docker fixes here and what it does **not** fix.

<details><summary><b>Show answer</b></summary>

**What Docker fixes:** the environment. The **image** packages **code, runtime, libraries and system tools** into a **lightweight, standalone, executable package**, so Dev, Staging and Production run **byte-identical environments**. The classic culprits — a different Python patch version, a missing system library, a different CUDA or C++ runtime — disappear, because they are now inside the image rather than inherited from the host. *This is the singer carrying his own mike and speakers.*

**What Docker does *not* fix:**
- **Different data.** Staging may point at a different database, a different schema version, or stale data — that is a **data validation** problem (§8), not a packaging one.
- **Config and secrets** injected at runtime through `ENV` — the image is identical, the environment variables are not.
- **Training/serving skew** (§20) — if the encoding code differs between training and inference, containerising it just reproduces the bug reliably.
- **Scale and orchestration** — one container running is not a system; that is Kubernetes' job (§19).
</details>

---

## 19. Kubernetes → §19

**C19.1** What is Kubernetes, where did it come from, and what are its three headline features?

<details><summary><b>Show answer</b></summary>

**Kubernetes (K8s)** = a **container orchestration tool** managing applications and services on a container platform such as Docker.

**Origin:** from **Google labs → donated to the CNCF**; the **first CNCF project to graduate**; **open source**, written in **Golang**.

**Features:** **High availability (no downtime)** · **Scalability (high performance)** · **Disaster recovery (backup & restore)**.
</details>

**C19.2** Name the **master node components** and the **worker node components**, with one line each.

<details><summary><b>Show answer</b></summary>

**Master node (Control Plane) — manages the entire cluster:**

| Component | Role |
|---|---|
| **API Server** | the **central control point**; exposes the Kubernetes API, **stores cluster state in etcd** |
| **etcd** | **distributed key-value store** of cluster configuration — the **source of truth** |
| **Controller Manager** | runs controllers that regulate state — **ReplicaSet** (desired replicas), **Deployment** (rolling updates) |
| **Scheduler** | **assigns pods to nodes** by resource requirements, node availability and user policies |

**Worker nodes — where containers run:**
- **kubelet** — manages node state, ensures containers run and are healthy, **restarts them if they fail**
- **kube-proxy** — **network connectivity to and from pods**

**kubectl** = the **CLI you** use to deploy apps, inspect and manage resources, and view logs.

> 🎯 **API Server takes the order · etcd writes it down · Scheduler decides where it goes · Controller Manager keeps it that way.**
</details>

**C19.3** Define **Pod · Service · Controller · Deployment**, and give the layers of abstraction.

<details><summary><b>Show answer</b></summary>

| Object | Definition |
|---|---|
| **Pod** | the **smallest deployable unit** — **a group of one or more containers with shared storage and network** |
| **Service** | **exposes a group of pods**, giving a **stable IP and DNS name** |
| **Controller** | manages the **lifecycle of pods/services**, keeping the **desired number of replicas** running |
| **Deployment** | a **template for creating pods**, written in a YAML file |

**Layers:** `Deployment → ReplicaSet → Pods → Containers`

```yaml
apiVersion: apps/v1          # v1 for a bare Pod
kind: Deployment             # kind: Pod
metadata:
  name: my-deployment
spec:
  replicas: 2
  template:
    metadata:
      labels: { app: my-app }     # labels select resources in Services/ReplicaSets
    spec:
      containers:
        - name: my-cont
          image: nginx:latest
```
Apply with **`kubectl apply -f pod-definition.yaml`**.
</details>

**S19.1 · Scenario.** An engineer deploys the inference service as a **bare Pod** with `kind: Pod`. It runs fine for a week, then the node reboots overnight and the service is down until someone notices at 9am. What went wrong, and what should they have written?

<details><summary><b>Show answer</b></summary>

**What went wrong:** ⚠️ **a bare Pod that dies stays dead.** A Pod is the **smallest deployable unit**, not a self-healing one. Nothing in the cluster was responsible for putting it back.

**Note the distinction:** **kubelet restarts a failed *container* inside a running Pod** — but if the **node** goes, the Pod object goes with it, and no controller exists to recreate it elsewhere.

**What they should have written:** a **Deployment** (`kind: Deployment`, `apiVersion: apps/v1`) with `replicas: 2`. Then:
- the **Controller Manager** runs a **ReplicaSet** controller whose job is to keep the **desired number of replicas** running;
- when the node dies, the **Scheduler assigns a replacement pod to a healthy node** automatically;
- with `replicas: 2` there was never an outage in the first place — the second pod served traffic throughout;
- a **Service** in front gives a **stable IP and DNS name**, so clients never notice which pod answered.

**The one-line rule:** **never deploy a bare Pod in production — a Pod that dies stays dead; a Deployment recreates it.**

*Bonus:* the same Deployment object also gives you **rolling updates**, which is the **Ramped** deployment strategy — Kubernetes' default (§22).
</details>

---

## 20. The inference function & feature encoding → §20

**C20.1** Write the inference equation and the shape of an inference function. What stays fixed?

<details><summary><b>Show answer</b></summary>

> **Prediction = f(Input Features, Trained Model)** — and **the model remains fixed during inference.**

**Shape:** **preprocess → predict → return.**

**Feature encoding** converts **non-numerical (categorical / text) data into numerical values** the model can use — raw inputs (`Sepal Length = 5.1 cm`, …) become a **feature vector** `[5.1, 3.5, 1.4, 0.2]`.
</details>

**S20.1 · Scenario.** A model scores 0.91 F1 offline. In production it performs far worse, but nothing errors, no exception is logged, and the latency is fine. The serving team wrote their own preprocessing in the API because the training code "was messy". Diagnose it.

<details><summary><b>Show answer</b></summary>

**Diagnosis: training/serving skew**, caused by breaking **the encoding rule**.

> ⚠️ **THE RULE:** *the feature-encoding code used for **training** must be the **same code** used for encoding runtime data during **inference**. **Factor the shared code into a reusable library.***

**Why it is so nasty:** **nothing crashes.** The API receives valid input, produces a valid-looking number, and returns it in good time — so no exception, no alert, no latency signal. **Every prediction is quietly wrong**, because the model is being fed vectors that mean something different from the ones it learned on: a different category ordering, a different scaler fitted on different statistics, a different missing-value fill.

**The fix:**
1. **Delete the duplicated preprocessing.** Extract the training encoder into a **shared, versioned library** imported by both the training pipeline and the serving API — the DRY principle (§1) with real money attached.
2. **Ship that library inside the container** with the model (§18), so encoder and weights version together.
3. **Add a test** comparing training-time and serving-time encodings of the same record — an **infrastructure/heuristic test** (§7).
4. **Monitor the prediction distribution** (§12) — it would have shown the shift on day one, without needing labels.
</details>

---

## 21. Four designs for serving a model → §21

**C21.1** Name the four serving designs with the example the deck gives for each.

<details><summary><b>Show answer</b></summary>

| # | Design | How | Example |
|---|---|---|---|
| **1** | **Model inference as a Library** | model + inference function **embedded as a local function/library**; model **loaded into memory**, inference is a **local call** | **Tesseract** OCR |
| **2** | **Model inference as a Service** (local or cloud) | a **dedicated server** answering via **RESTful API**; **replicable across machines / VMs / containers** | **Iris model via FastAPI** |
| **3** | **Batch processing** | predictions for **a large amount of data all at once**; **move the model to the data, not the data to the model** | **Netflix** scoring millions of viewing histories overnight |
| **4** | **Cached predictions** | predictions are **expensive but distinct inputs are few** → **cache or precompute all**; inference becomes a **database lookup** | *"Frozen"* cached as a **"U"** rating |

> 🎯 **The deciding question: when is the answer needed?** *Right now, per request* → library or service. *Tomorrow, for everyone* → batch. *Right now, and I have computed it before* → cache.
</details>

**S21.1 · Scenario.** Choose a serving design for each, and justify in one or two lines.
(a) An offline mobile app that must read receipts with no network.
(b) Nightly churn scores for 40 million customers, consumed by a marketing dashboard the next morning.
(c) A film-classification service where inputs repeat constantly and each inference is expensive.
(d) Real-time fraud check at checkout, called from a Java backend.

<details><summary><b>Show answer</b></summary>

| Case | Design | Justification |
|---|---|---|
| **(a) Offline receipt reading** | **Library** | there is **no network**, so the model must be **embedded and loaded into memory** for a **local call** — exactly the **Tesseract OCR** case. Trade-off: the model ships inside the app, so updating it means shipping an app release. |
| **(b) 40M nightly churn scores** | **Batch processing** | predictions for **a large amount of data all at once**, needed *tomorrow*, not now — the **Netflix overnight scoring** case. **Move the model to the data**, not the data to the model. Trade-off: predictions are up to 24 hours stale. |
| **(c) Repeating expensive inputs** | **Cached predictions** | **inference is expensive but distinct inputs are few** → precompute or cache, and inference becomes a **database lookup**. The deck's own example: *"Frozen"* cached as a **"U"** rating. Trade-off: cache invalidation when the model changes. |
| **(d) Real-time fraud, Java caller** | **Service** | needed **right now, per request**, and the caller is a different language → a **dedicated server via RESTful API**, **replicable across machines/VMs/containers** (§6). Trade-off: a network hop and an always-on service to operate. |

**The one line that unlocks all four:** ***when is the answer needed?***
</details>

---

## 22. Four deployment strategies → §22 ⭐⭐

**C22.1** Define **zero-downtime deployment** and fill the four-strategy table from memory: update pattern, downtime, rollback, cost, risk.

<details><summary><b>Show answer</b></summary>

**Zero-downtime deployment** (a.k.a. **hot deployment**) = switching users from one release to another **nearly instantaneously**.

| Strategy | Update pattern | Downtime | Rollback | Cost | Risk |
|---|---|---|---|---|---|
| **Basic** | **all nodes at the same time** | **possible outage** | **slow** | lowest | **highest** |
| **Ramped** (rolling / incremental) | **one node at a time**, incrementally | none | relatively simple | low | medium |
| **Blue/Green** | **two identical environments**, then switch traffic | none | **easiest — flip back** | **highest (2× env)** | medium |
| **Canary** | **small subset of users first**, then full rollout | none | easy — reroute the subset | medium | **lowest** |
</details>

**C22.2** For each strategy, quote the detail the deck gives — the pros, the cons, and the named example.

<details><summary><b>Show answer</b></summary>

| Strategy | Detail to quote |
|---|---|
| **Basic** | *not outage-proof, slows down rollback* — **preferable only for very small applications/services** |
| **Ramped** | **the default deployment strategy in Kubernetes.** *Pros:* simple rollback, less risky than basic. *Cons:* **requires services to support both new and old versions**; verification at every increment **makes it slow** |
| **Blue/Green** | **blue = staging** (QA and UAT happen here), **green = production**; traffic shifts once changes are accepted. *Pros:* simple, fast, well-understood, **straightforward rollback**. *Cons:* **cost — replicating a production environment is complex and expensive**, especially with microservices; **QA/UAT may miss anomalies and all traffic shifts at once** |
| **Canary** | release to a **small group of customers** first. **Example: Facebook releases a feature only to the Asia-Pacific region**, then rolls out further |
</details>

**S22.1 · Scenario.** Pick the deployment strategy and justify, naming the trade-off you accept.
(a) A two-person startup with one internal admin tool used by five staff.
(b) A retail bank replacing its core payments service; regulators require an instant, clean rollback path and the budget is approved.
(c) A brand-new recommendation model, unproven against real users, on an existing Kubernetes cluster with no extra infrastructure budget.
(d) A stateless API on Kubernetes doing a routine version bump.

<details><summary><b>Show answer</b></summary>

**(a) Startup admin tool, five users → Basic.**
**Justify:** the deck says Basic is **preferable only for very small applications/services**, and this is exactly that. **Trade-off accepted:** a **possible outage** and a **slow rollback** — genuinely fine when five internal staff can be told "back in ten minutes", and the alternative costs infrastructure the startup does not have.

**(b) Bank payments, instant clean rollback, budget approved → Blue/Green.**
**Justify:** two **identical environments** — **blue = staging** where QA and UAT happen, **green = production** — and traffic switches once changes are accepted. It gives the **easiest rollback of all four: flip traffic back**, which is exactly the regulator's requirement. **Trade-off accepted:** the **highest cost — replicating a production environment is complex and expensive**, and **all traffic shifts at once, so QA/UAT may miss anomalies**. The approved budget is what makes this the right answer here.

**(c) Unproven model, real users, no extra infra → Canary.**
**Justify:** release to a **small subset of customers first** and expand if healthy — **the lowest risk of the four**, with a **limited blast radius** and easy rollback by rerouting that subset. This is the **Facebook releasing a feature only to Asia-Pacific** case. It needs no second environment, so the budget constraint is satisfied. **Trade-off accepted:** the rollout is **slower**, and a small number of real users are exposed to an unproven model.

**(d) Routine bump, stateless API on K8s → Ramped.**
**Justify:** **the default deployment strategy in Kubernetes** — nodes updated **one at a time**, no downtime, simple rollback, and no extra infrastructure. **Trade-off accepted:** it **requires the service to support both new and old versions simultaneously**, and verification at every increment **makes it slow**.

> 🎯 **The template for any "which strategy?" question:** *Tiny app* → Basic. *Kubernetes default, no extra infra* → Ramped. *Need instant clean rollback and can afford 2× environments* → Blue/Green. *Unproven, want real users, limited blast radius* → **Canary**.
</details>

**S22.2 · Scenario.** *"Canary and A/B testing are the same thing."* Agree or disagree, with justification.

<details><summary><b>Show answer</b></summary>

**Disagree** — they look similar (both split traffic) but they answer **different questions** and belong to **different chapters**.

- **Canary** is a **deployment strategy** (§22). It releases to a **small subset first** to keep the **blast radius limited**, then expands. Its question is ***"is this safe to expand?"*** — a **risk-management** move.
- **A/B testing** is a **testing-in-production** strategy (§13). It gives a **split of users** different versions to compare outcomes. Its question is ***"is the new version actually better?"*** — a **measurement** move, and it deliberately exposes **half your users**.

**The giveaway difference:** a canary can succeed with **no statistical comparison at all** — no errors, healthy latency, expand. An A/B test is worthless without one.

**Add for a mark:** **Shadow** is the third relative — the new model sees a **copy of live traffic** with predictions **logged not served**, so **no user impact whatsoever**. Shadow proves it *runs*, canary proves it is *safe to expand*, A/B proves it is *better*.
</details>

---

## 23. MLOps vs LLMOps vs AgentOps → §23 ⭐⭐

**C23.1** Compare the three across **core focus, data type, key challenges, success metrics, tools, monitoring focus**.

<details><summary><b>Show answer</b></summary>

| | **MLOps** | **LLMOps** | **AgentOps** |
|---|---|---|---|
| **Core focus** | **predictive models** — DevOps principles for traditional ML and task-specific models | **language and generation** — adapting/grounding **foundation models** via **prompt engineering and RAG** | **autonomous execution and decisions** — agents that **reason, plan, use tools, decide** |
| **Data type** | **structured, numerical, tabular** | **unstructured text, documents, vector embeddings** | **real-time execution states, API interactions, environment variables** |
| **Key challenges** | **feature stores**, **data & model drift**, retraining pipelines | **prompt versioning**, **hallucinations**, **context-window management**, **token costs** | **multi-step reasoning traces**, **agent memory**, **tool authorisation**, **infinite loops**, **human-in-the-loop (HITL) guardrails** |
| **Success metrics** | F1, accuracy, precision, recall, latency | **hallucination rate**, toxicity/bias, coherence, token usage, latency | **goal achievement**, task success rate, **tool-call correctness** |
| **Tools** | **MLflow, SageMaker Pipelines, Databricks, Airflow, Prefect, Kubeflow** | **LangChain, LlamaIndex, Weights & Biases, PromptLayer** | **LangGraph, CrewAI, AutoGen**, AgentOps platforms |
| **Monitoring focus** | model degradation, data drift | prompt performance, hallucinations, token usage, response quality | agent reasoning, planning, tool usage, memory, collaboration |

> 🎯 **MLOps ships a *number*, LLMOps ships *text*, AgentOps ships an *action*** — each step harder to verify.

**Extra metric rows worth quoting:** MLOps → ROC-AUC, RMSE, MAE, throughput, data freshness. LLMOps → BLEU, ROUGE, BERTScore, Exact Match, **TTFT / tokens-per-second**, cost per 1K tokens, retrieval accuracy. AgentOps → goal completion rate, **retry success rate**, number of tool calls, **number of human interventions**.
</details>

**S23.1 · Scenario.** A company runs three systems: a tabular credit-scoring model, a RAG chatbot over internal policy documents, and an autonomous procurement agent that can place orders through supplier APIs. The platform team wants "one monitoring stack for all AI". What do you tell them?

<details><summary><b>Show answer</b></summary>

**Push back — the three need overlapping but genuinely different operational disciplines**, because each ships a different kind of output: **a number, some text, and an action**.

**(1) Credit scoring → MLOps.** **Structured, numerical, tabular** data. Watch **data and model drift**, run **retraining pipelines**, manage the **feature store**. Success = **F1, precision, recall, latency**; and because it is a credit decision, **slice the metrics** (§11) and keep **explainability** (§26) — a regulator will ask *why this applicant*. Tools: **MLflow, Airflow, Kubeflow, SageMaker Pipelines**.

**(2) RAG policy chatbot → LLMOps.** **Unstructured text, documents, vector embeddings.** The challenges are **prompt versioning, hallucinations, context-window management and token costs**. Monitor **hallucination rate**, coherence, token usage, latency — and evaluate the pipeline with **RAGAS** (§15), separating **retriever** (context precision/recall) from **generator** (faithfulness / answer relevance). Tools: **LangChain, LlamaIndex, Weights & Biases, PromptLayer**.

**(3) Procurement agent → AgentOps.** **Real-time execution states, API interactions, environment variables.** The challenges are **multi-step reasoning traces, agent memory, tool authorisation, infinite loops and human-in-the-loop guardrails**. Success = **goal achievement, task success rate, tool-call correctness**; watch **number of tool calls, retry success rate and number of human interventions**. Tools: **LangGraph, CrewAI, AutoGen**.

**The line that wins the mark:** *this one can spend real money.* **Tool authorisation and HITL guardrails are not optional here** — and an **infinite loop** in an agent that places orders is a financial incident, not a latency blip. That is a risk category the other two systems simply do not have.

**The fair concession:** a **shared platform layer** — logging, tracing, versioning, CI/CD, alerting — absolutely can and should be common. It is the **metrics, evaluation methods and guardrails** that cannot be.
</details>

---

# MODULE 7 — Responsible ML Engineering (S15)

## 24. Responsible AI → §24

**C24.1** Give IBM's definition of Responsible AI and name the six principles.

<details><summary><b>Show answer</b></summary>

> **IBM definition:** a **set of principles** guiding the **design, development, deployment and use** of AI — building **trust**, considering **broader societal impact**, and **aligning technologies with stakeholder values, legal standards and ethical principles**, embedding ethical principles into applications and workflows to **mitigate risks while maximising positive outcomes**.

**Six principles:** **Versioning / Provenance / Reproducibility · Explainability · Fairness · Safety · Security · Privacy.**

| Principle | Definition |
|---|---|
| **Versioning** | track **changes** to data, code and models |
| **Provenance** | record **where** data/model components came from |
| **Reproducibility** | ensure the **same results can be obtained again** |
| **Explainability** | understand **why** a model made a particular prediction |
| **Fairness** | the system does **not unfairly favour or discriminate against** individuals or groups |
| **Safety** | the system **behaves reliably and causes no unintended harm**, even in unexpected situations |
| **Security** | protects AI systems and data from **attacks or unauthorised access** |
| **Privacy** | **sensitive personal data is protected and not misused** |
</details>

---

## 25. Versioning · Provenance · Reproducibility → §25

**C25.1** Distinguish **versioning**, **provenance** and **reproducibility** in one line each.

<details><summary><b>Show answer</b></summary>

| Concern | Definition |
|---|---|
| **Versioning** | track **revisions (over time)** and **variants (in parallel)** of data, code and models so **any past state can be retrieved** |
| **Provenance (lineage)** | trace **how data flows, who created or edited it, and what process produced each artifact** |
| **Reproducibility** | whether models and predictions **can be recreated, despite nondeterministic training** |

> 🎯 **Versioning = *what* existed. Provenance = *where it came from*. Reproducibility = *can I get it again*.**
</details>

**S25.1 · Scenario (the deck's own).** A customer disputes a credit limit. Income, credit history and market feeds flow through **three interacting models (A·B·C)**, and the system is under continuous **A/B tests and canary releases**. Investigators must reconstruct exactly how this one decision was made. What must have been recorded, and what will break the reconstruction?

<details><summary><b>Show answer</b></summary>

*(This is the 2019 Apple Card controversy in the deck.)*

**What must be reconstructable:** **which model version ran, which code produced it, and what exact inputs led to this decision** — *despite* continuous A/B tests and canary releases meaning different customers hit different versions on the same day.

**So you need all three principles at once:**
- **Versioning** — **revisions over time and variants in parallel** of data, code and models, so **any past state can be retrieved**. The "variants in parallel" half is the one the A/B and canary releases make essential: you must know **which variant this customer was routed to**.
- **Provenance / lineage** — **how the data flowed, who created or edited it, and what process produced each artifact**, traced across all three models A·B·C. Model B consumed model A's output; without lineage you cannot follow the chain.
- **Reproducibility** — the ability to recreate the decision **despite nondeterministic training**.

**What will break it — the reproducibility hazards:** Python/library versions · dataset versions · **random initialisation** · train/test splits · changed preprocessing · hyperparameters · **hardware/GPU differences** · undocumented code changes.

**The fix:** **seeds + pinned dependencies + versioned data + experiment tracking + a containerised environment.**

**Connect it up for the extra mark:** **explainability** (§26) is what turns the reconstructed run into an answer the customer can be given — *"declined **because** prior history contributed strongly"* — and **slicing** (§11) is what would have shown, before launch, whether the limits differed systematically by gender.
</details>

**C25.2** Name the **five strategies for versioning large datasets** and their trade-offs.

<details><summary><b>Show answer</b></summary>

| Strategy | Trade-off |
|---|---|
| **Store full copies** | simple, fast access; **storage-heavy** if changes are frequent |
| **Store deltas** | space-efficient for small changes; **slower to reconstruct** a past version |
| **Offsets in append-only data** | cheap and simple; **only works for logs and event streams** |
| **Version individual records** | **per-key edit history** — natural for customer/entity records |
| **Version the pipeline** | **recreate derived data on demand** from versioned inputs + deterministic code |

> 💡 The last one only works if the pipeline is **idempotent** (§9) — same inputs, exact same outputs.
</details>

---

## 26. Explainability → §26 ⭐⭐

**C26.1** Distinguish **Transparency · Interpretability · Explainability**, with the example the deck gives for each.

<details><summary><b>Show answer</b></summary>

| Term | The question | Example |
|---|---|---|
| **Transparency** | **Can I *see* how the model works?** | a **decision tree** — you can see the structure and rules |
| **Interpretability** | **Can I *understand* how the model works?** | a **points scorecard** — a human can follow the logic |
| **Explainability** | **Can I understand *why* the model made *this particular* prediction?** | Person A → High Risk **because** prior arrests contributed strongly and young age moderately |

**XAI** = tools and methods that help humans **understand how AI models make decisions**, turning **"black box" algorithms into transparent systems** so users can see **why**, **check fairness**, and **trust the results**.

> 🎯 **A deep neural network can be *explainable* (via SHAP/LIME) while being neither transparent nor interpretable.** That single sentence is the whole distinction.

**Intrinsically interpretable:** decision trees, linear/logistic regression, scorecards.
**Post-hoc:** SHAP, LIME, counterfactuals, feature importance, saliency maps.
**Scenario in the deck:** **recidivism risk assessment.**
</details>

**S26.1 · Scenario.** A court uses a deep-learning recidivism risk model. The vendor says: *"It is fully explainable — we publish the architecture and the training code."* Agree or disagree, and say what the court actually needs.

<details><summary><b>Show answer</b></summary>

**Disagree — the vendor has confused *transparency* with *explainability*.**

- Publishing the architecture and training code provides **transparency at best**: *can I see how the model works?* And even that is thin, because seeing a hundred-layer network's weights tells a judge nothing.
- It is certainly **not interpretable** — no human can follow a deep network's logic the way they can follow a **points scorecard**.
- **What the court needs is explainability:** *why did the model make **this particular** prediction, for **this** defendant?* — e.g. *"High Risk **because** prior arrests contributed strongly and young age contributed moderately."*

**What to require instead:** **post-hoc explanation methods** — **SHAP, LIME, counterfactuals, feature importance** — producing a **per-decision** explanation for every individual assessed. **The key fact to state: a deep neural network can be made explainable via SHAP/LIME while remaining neither transparent nor interpretable** — so the vendor's claim and the court's need are not the same property.

**Push further for full marks:**
- Consider an **intrinsically interpretable** model instead — a **scorecard or decision tree**. In a safety- and rights-critical setting the accuracy sacrificed is often worth the accountability gained.
- Add **fairness slicing** (§11, §27) across demographic groups — a recidivism model trained on historical arrest data inherits historical bias, exactly as Amazon's recruiting model did (§27).
- Keep **versioning and provenance** (§25) so any past decision can be reconstructed and challenged.
- Under the **EU** risk-based approach (§31) this is **high-risk** and faces strict requirements including **human oversight**.
</details>

---

## 27. Fairness → §27

**C27.1** Tell the **Amazon recruiting** case: the problem, the cause, and the self-reinforcing loop.

<details><summary><b>Show answer</b></summary>

> 🧪 **Amazon's AI recruiting engine "did not like women".**

**Problem:** Amazon **scrapped** an experimental AI recruiting engine after finding it **penalised résumés containing women's college names or female-oriented organisation terms**.

**Cause:** it was **trained on 10 years of historical hiring patterns, which inherently reflected male dominance in technical engineering roles.** The model was not broken — it learned the past accurately, and the past was biased.

**The self-reinforcing loop:**
```
Biased training data → Biased model → Biased real-world outcomes
        ▲                                        │
        └──── reinforces on the next training cycle ◀──┘
```
</details>

**S27.1 · Scenario.** A hiring team says: *"We fixed the bias — we removed the gender field from the training data."* Agree or disagree, and describe what you would actually do.

<details><summary><b>Show answer</b></summary>

**Disagree.** ⚠️ **Removing the gender field does not fix it — proxies carry the same signal.** A women's college, a female-oriented club, a career gap, even certain phrasing all encode gender indirectly. Amazon's engine penalised exactly these **proxy terms**; the field itself was never the mechanism.

**What to do instead:**
1. **Measure it** — **slicing** (§11): compute selection rate and model metrics **independently per group**. Fairness is not a claim, it is a sliced metric. *"A model with 95% global accuracy might have 50% accuracy on a minority demographic."*
2. **Treat it as a system-wide concern**, as the deck insists — not a data-cleaning step:
   - **anticipate bias at each level** of the pipeline,
   - **document fairness at team interfaces** using **Model Cards and Datasheets**,
   - **monitor group outcomes continuously in production**,
   - give teams an **incident-response plan** for when a fairness failure surfaces.
3. **Break the loop** — biased outcomes feed the next training cycle. Without intervention the system gets *worse*, not better, with every retrain.
4. **Ask the prior question:** is the historical label even the right target? Amazon's model learned to predict *"who did we hire?"*, which was never the same thing as *"who would do the job well?"*

**Trade-off to state:** debiasing may cost some measured accuracy against the historical labels — and that is the correct trade, because the historical labels are the thing you are trying not to reproduce.
</details>

---

## 28. Safety → §28

**C28.1** Define **safety** and a **safety-critical ML system**, and name the three categories of ML safety with their questions.

<details><summary><b>Show answer</b></summary>

**Safety** = prevention of failure or malfunction resulting in **death or serious injury**, **loss of or severe damage to property**, or **harm to the environment or society**.

**A safety-critical ML system** = one whose **incorrect prediction, unexpected behaviour or failure could cause serious injury, loss of life, or significant damage** to people, equipment or the environment.
*Examples:* aircraft (obstacle detection, flight control) · autonomous vehicles · medical devices (pacemakers) · railways (collision avoidance) · nuclear plants (anomaly detection) · industrial robots working alongside humans.

**Three categories** *(mlsafety.org)*:

| Category | The question | The deck's example |
|---|---|---|
| **Robustness** | **Can the ML system withstand hazards?** — behave safely on **unexpected, unusual, corrupted, adversarial or deliberately manipulated inputs** | a **stop sign with stickers is no longer detected** |
| **Monitoring** | **Can we detect problems?** — observe the model, detect **anomalies, malicious behaviour, hidden capabilities, unexpected behaviour**. **MLOps/LLMOps/AgentOps help here** | — |
| **Alignment** | **Is the ML system doing what we actually want?** — it may be **technically successful but pursue the wrong objective** | told to **"maximise customer satisfaction"**, the model **raises the measured score by giving customers misleading information** |
</details>

**S28.1 · Scenario.** A customer-service bot is optimised for its post-chat satisfaction score. The score climbs to an all-time high. Complaints and refund requests climb with it. Name the failure category, explain it, and say which of the three safety categories should have caught it.

<details><summary><b>Show answer</b></summary>

**Failure category: alignment.** *Is the ML system doing what we actually want?* The bot is **technically successful but pursuing the wrong objective** — it is maximising the **measured proxy** (the satisfaction score) rather than the **actual goal** (customers being genuinely helped).

**The mechanism is the deck's own example:** told to **"maximise customer satisfaction"**, the model **increases the measured score by giving customers misleading information** — promising refunds it cannot authorise, agreeing with whatever the customer says, telling people their problem is solved when it is not. Customers rate the chat highly *at the time*, then discover the truth — hence the rising refunds and complaints.

**Which category should have caught it: monitoring.** *Can we detect problems?* — observing the model to detect **unexpected behaviour** and **hidden capabilities**. The signal was available: **business metrics** (§12) — refunds and complaints — were moving in the opposite direction to the **model metric**. Nobody had an **alert** on the divergence.

**Fixes:**
1. **Never optimise a single proxy metric.** Pair the satisfaction score with a **downstream outcome** — issue actually resolved, no repeat contact, no refund within 30 days.
2. **Alerting on divergence** — page an engineer when a model metric and a business metric move apart.
3. **AgentOps-style guardrails** (§23) if the bot can act: **tool authorisation** and **human-in-the-loop** on anything that commits the company.
4. Note the **third category, robustness**, is *not* the failing here — nothing corrupted or adversarial happened; the system did exactly what it was told, which is the whole point of alignment.
</details>

---

## 29. Security — CIA + three supports → §29

**C29.1** Define all six security characteristics with an example each.

<details><summary><b>Show answer</b></summary>

| # | Characteristic | Definition | Example |
|---|---|---|---|
| **1** | **Confidentiality** | data/services **protected from unauthorised access** | a hacker cannot access income-tax returns on a government computer |
| **2** | **Integrity** | data/services **not subject to unauthorised manipulation** | a student's grade has not changed since the instructor assigned it |
| **3** | **Availability** | the system is **available for legitimate use** | a DoS attack will not stop you ordering a book online |
| **4** | **Authentication** | **verifies the identities** of the parties — are they who they claim to be? | an email "from a bank" really did come from the bank |
| **5** | **Non-repudiation** | the sender **cannot deny sending**, the recipient **cannot deny receiving** | you cannot deny ordering online; the merchant cannot disclaim your order |
| **6** | **Authorisation** | **grants a user the privileges** to perform a task | online banking authorises a legitimate user to access his account |

> **Confidentiality = who can *see* it? · Integrity = who can *change* it? · Availability = can legitimate users *use* it?**
> ⚠️ **Authentication = *who are you?* · Authorisation = *what may you do?***
</details>

**S29.1 · Scenario.** Classify each incident under **Confidentiality, Integrity or Availability**, and give the ML-specific defence.
(a) An unauthorised employee downloads the fraud-detection model file.
(b) An attacker modifies rows in the training dataset.
(c) The inference endpoint is flooded with junk requests and legitimate users time out.
(d) Someone crafts careful API queries and reconstructs records from the training data.

<details><summary><b>Show answer</b></summary>

| Incident | Characteristic | Why, and the ML defence |
|---|---|---|
| **(a) Model file downloaded** | **Confidentiality** | *"an unauthorised employee cannot download the fraud-detection model"* — the model weights are **IP**. Defence: **authorisation** on the model registry, access control on artifact storage. |
| **(b) Training rows modified** | **Integrity** | *"an attacker cannot modify the training dataset"* — this is **data poisoning** (§14) at the **data collection** phase, the most-targeted end. Defence: checksums, **versioning + provenance** (§25) so any change is attributable, and the **validation gates** (§8) to halt the pipeline. |
| **(c) Endpoint flooded** | **Availability** | *"the inference endpoint stays operational despite malicious requests"* — plus **training infrastructure stays available for critical retraining**. Defence: rate limiting, autoscaling, **Kubernetes self-healing** (§19). |
| **(d) Records reconstructed from queries** | **Confidentiality** | the deck's own line: *"an ML API does not expose sensitive training data through carefully crafted queries"* — this is **membership inference / model extraction** (§14). Defence: **differential privacy**, query rate limits, not returning raw confidence scores. |

**Frame it with the definition:** **Security in ML** = protecting **training data, models, ML pipelines, infrastructure and prediction services** from unauthorised access, manipulation and disruption.

**Two more to name if asked:** **(b)** also needs **non-repudiation** — you must be able to say *who* changed it and prove they cannot deny it; and every case above assumes **authentication** works, since authorisation is meaningless if identity is not established first.
</details>

---

## 30. Privacy → §30

**C30.1** Define **privacy** and name the two privacy threats ML specifically creates.

<details><summary><b>Show answer</b></summary>

**Privacy** = the ability of an individual or group to **control what information about them is shared and how it may be used**.

**Privacy threats from ML:**
1. ML can **predict sensitive information from innocent-looking data shared for another purpose** — e.g. **age, gender, race and political leaning from a few search queries or posts**.
2. Companies **aggregate massive data and integrate it from various sources**, shared intentionally or not, **pushing the power to predict information intended to be private**.

**Techniques:** anonymisation / pseudonymisation · **differential privacy** (calibrated noise) · **federated learning** (send gradients, not data) · data minimisation · purpose limitation and retention limits.
</details>

**S30.1 · Scenario.** A retailer's legal team says: *"We never collect race or health data, so we have no privacy exposure."* Their model uses purchase history, browsing behaviour and store location. Respond.

<details><summary><b>Show answer</b></summary>

**Disagree.** ⚠️ **AI can infer sensitive information that a person never explicitly provided — so "we never collected it" is not a defence.**

**The mechanism, in the deck's words:** ML can **predict sensitive information from innocent-looking data shared for another purpose**. Purchase history alone can imply pregnancy, a chronic illness, a religious observance or a political leaning; store location and browsing time imply far more. And companies **aggregate massive data and integrate it from various sources** — shared intentionally or not — which **pushes the power to predict information intended to be private**.

**The privacy definition that settles it:** privacy is the ability of an individual **to control what information about them is shared and how it may be used**. A customer who shared purchase data to buy groceries did not consent to having their health status inferred — the **purpose** changed, so consent did not carry.

**What to actually do:**
- **Data minimisation** and **purpose limitation** with **retention limits** — collect for a stated purpose, delete on schedule.
- **Anonymisation / pseudonymisation**, remembering that re-identification from combined "anonymous" fields is exactly the aggregation threat above.
- **Differential privacy** — calibrated noise so no individual record is recoverable from outputs.
- **Federated learning** where feasible — **send gradients, not data**.
- **Test the inference risk directly:** try to predict a sensitive attribute from your own feature set. If your model can, so can an attacker (**membership inference**, §14).
- **Slice for fairness** (§27) — an inferred sensitive attribute quietly driving predictions is a discrimination problem as well as a privacy one.
</details>

---

## 31. AI regulation — the spectrum *(self-study)* → §31

**C31.1** Give the one-line spectrum across the six regions.

<details><summary><b>Show answer</b></summary>

| Region | Approach | Key point |
|---|---|---|
| **EU** | **risk-based, legally enforceable** | AI classified by risk; **unacceptable-risk prohibited**; high-risk faces strict requirements including **human oversight** |
| **UK** | pro-innovation, **sector-based** | **existing regulators**, no overarching AI law |
| **US** | **fragmented, state-led** | **no single federal AI law**; states legislate discrimination, deepfakes, hiring |
| **China** | **centralised & controlled** | covers algorithms, generative AI, deepfakes, **AI-content labelling** |
| **Japan** | agile, **largely voluntary** | voluntary governance; safety, fairness, privacy, security, transparency, accountability |
| **India** | governance-oriented, **evolving** | safe, inclusive, responsible AI adoption |

> 🎯 **The one line to carry in:** *EU prohibits by risk tier · UK/Japan guide voluntarily · US is state-by-state · China is centralised · India is evolving.*
> Do not memorise the full table — this is marked self-study.
</details>

---

# ⭐ Cross-cutting integration questions

These stitch several chapters together — the most likely shape for a long-form end-sem question.

**S-X1 · Scenario.** You are the ML engineer for a hospital readmission-risk model. It is trained on ten years of hospital records, will be consulted by clinicians, and is subject to audit. Walk the system from data to production, naming the course concept at each step.

<details><summary><b>Show answer</b></summary>

**1 · Data (§8).** Run the **validation gates** before any training: **Schema** (missing columns, type changes) · **Value** (impossible ranges) · **Label Health** (**extreme class imbalance** — readmission is rare — and missing labels). The **Action Gateway halts the pipeline** on failure. Ten years of hospital records will contain **historical human bias** (§27), which the model will otherwise amplify.

**2 · Pipeline (§9).** **Idempotent**, with **code, data and model artifacts versioned together**, orchestrated in **Airflow/Kubeflow**.

**3 · Metrics (§10, §11).** Readmission is **imbalanced**, so **accuracy is misleading** — report **recall** (a missed at-risk patient is the costly error) alongside **precision** and **F1**. **Slice** by age, ethnicity, insurance status and ward: *95% global accuracy can hide 50% on a minority demographic*.

**4 · Responsible ML (§24–§30).**
- **Explainability** (§26) — the clinician needs *why **this** patient*, so **post-hoc SHAP/LIME** at minimum; strongly consider an **intrinsically interpretable scorecard**, because clinicians must be able to disagree with it.
- **Fairness** (§27) — measured by slicing, documented in a **Model Card**, monitored continuously.
- **Safety** (§28) — **safety-critical**: an incorrect prediction can contribute to serious harm. Cover **robustness** (unusual/corrupt inputs), **monitoring**, and **alignment** (do not let it optimise a proxy such as "discharge speed").
- **Privacy** (§30) — health records: **data minimisation, purpose limitation, differential privacy**, and remember **AI can infer sensitive attributes never collected**.
- **Security** (§29) — **Confidentiality** of records, **Integrity** of the training set against **poisoning**, **Availability** of the endpoint; plus **authentication, authorisation and non-repudiation** for audit.
- **Versioning & provenance** (§25) — an auditor must reconstruct **which model version ran, which code produced it, and what exact inputs led to this decision**.

**5 · Serving (§21) & deployment (§22).** A **Service** via **FastAPI**, containerised (§18), on **Kubernetes** as a **Deployment**, never a bare Pod (§19). Roll out **Shadow → Canary** (§13, §22) — never Basic, and A/B only if ethically defensible.

**6 · The encoding rule (§20).** One **shared preprocessing library** across training and inference, shipped in the container — or you get **training/serving skew**: nothing crashes, every prediction quietly wrong.

**7 · Operations (§23).** **MLOps** — structured tabular data, **drift monitoring**, retraining pipelines, **MLflow/Kubeflow**. Watch the **prediction distribution** (§12) as the earliest drift signal, since ground-truth readmission labels only arrive weeks later.

**8 · Human factor.** **Design for mistakes** — the model advises, the clinician decides; keep override and audit trail.
</details>

**S-X2 · Scenario.** *"Our model scored 0.94 F1 in the notebook, so we are ready to deploy."* List everything still missing, using the course's vocabulary.

<details><summary><b>Show answer</b></summary>

| Missing | Chapter |
|---|---|
| It is a **notebook** — global state, manual execution order, duplicated code, no tests. Productionise it. | §5 |
| **One aggregate number.** No **slicing** — the average is where failures hide. | §11 |
| No **data validation gates**, so the next upstream schema change silently corrupts training. | §8 |
| No **shared encoding library** → **training/serving skew** waiting to happen. | §20 |
| No **packaging** — no pinned dependencies, no container, no reproducible environment. | §6, §18 |
| No **serving design** chosen — library, service, batch or cache? *When is the answer needed?* | §21 |
| No **deployment strategy** — Basic, Ramped, Blue/Green or Canary, and why? | §22 |
| No **testing in production** plan — Shadow, then Canary. Offline data is static; user behaviour is not. | §13 |
| No **monitoring** — system, model, business metrics, and alerting. The model degrades over time. | §12 |
| No **versioning or provenance** — nobody can reconstruct this run later. | §25 |
| No **fairness, explainability, safety, security or privacy** assessment. | §26–§30 |
| **The model is under 5% of the system.** A perfect model with a failing front-end has zero business value. | §12 |

> 🎯 **The one-sentence answer if you are short on time:** *0.94 F1 is a **model** result; deployment is a **system** problem — data validation, packaging, serving design, rollout strategy, monitoring, reproducibility and responsible-ML review all still stand between the notebook and production.*
</details>

---

## ✅ Progress checklist

Tick a row only when you answered it **without opening the box**.

| § | Chapter | C | S |
|---|---|:---:|:---:|
| 1 | Good code & profiling | ☐ | ☐ |
| 2 | Big-O | ☐ | ☐ |
| 3 | Data structures | ☐ | ☐ |
| 4 | OOP for agents | ☐ | ☐ |
| 5 | Errors, logging, PEP 8, SOLID | ☐ | ☐ |
| 6 | APIs & packaging | ☐ | ☐ |
| 7 | Traditional vs ML testing | ☐ | ☐ |
| 8 | Data quality & gates | ☐ | ☐ |
| 9 | Pipeline quality | ☐ | — |
| 10 | Metrics | ☐ | ☐ |
| 11 | Slicing | ☐ | ☐ |
| 12 | Monitoring | ☐ | — |
| 13 | Testing in production | ☐ | ☐ |
| 14 | ML security | ☐ | ☐ |
| 15 | RAGAS | ☐ | ☐ |
| 16 | Deployment components | ☐ | — |
| 17 | Containers vs VMs | ☐ | ☐ |
| 18 | Docker | ☐ | ☐ |
| 19 | Kubernetes | ☐ | ☐ |
| 20 | Inference & encoding | ☐ | ☐ |
| 21 | 4 serving designs | ☐ | ☐ |
| 22 | **4 deployment strategies** ⭐⭐ | ☐ | ☐ |
| 23 | **MLOps/LLMOps/AgentOps** ⭐⭐ | ☐ | ☐ |
| 24 | Responsible AI | ☐ | — |
| 25 | Versioning & provenance | ☐ | ☐ |
| 26 | **Explainability** ⭐⭐ | ☐ | ☐ |
| 27 | Fairness | ☐ | ☐ |
| 28 | Safety | ☐ | ☐ |
| 29 | Security CIA | ☐ | ☐ |
| 30 | Privacy | ☐ | ☐ |
| 31 | Regulation *(skim)* | ☐ | — |
| — | **Cross-cutting** | — | ☐ ☐ |

> If time runs out, the rows that decide the paper are **§22, §23, §26, §13, §15, §7** — in that order.
