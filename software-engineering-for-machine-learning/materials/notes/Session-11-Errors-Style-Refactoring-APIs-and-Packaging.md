# Session 11 — Errors, Logging, Style, Refactoring, APIs & Packaging

> **Module 4 · Lecture 11** ("Implementation and Code Sharing" — Part 2) · Slides: `Session 11.pptx`
>
> **One-line goal:** the six habits that turn a notebook into a shippable service — **fail fast · log · lint · refactor · wrap in an API · package it**.

### Contents
1. [Errors & debugging — fail fast](#1-errors--debugging--fail-fast)
2. [Logging](#2-logging--print-is-not-logging)
3. [Debugging strategies](#3-debugging-strategies)
4. [Style & linting](#4-style--linting--pep-8-and-friends)
5. [Type hints & static checking](#5-type-hints--static-checking)
6. [Research vs Production code](#6-research-vs-production-code-exam-favourite)
7. [Design & refactoring (SOLID)](#7-design--refactoring-solid)
8. [Designing APIs for ML services](#8-designing-apis-for-ml-services)
9. [Sharing code & packaging](#9-sharing-code--packaging)
10. [Recap](#-recap)

---

## 1. Errors & debugging — fail fast

> 🌍 **Famous saying from the deck:** *"If you don't build logging and error handling into your system, your users will become your loggers."*

**Failing fast** = your code must **never behave unpredictably when fed corrupt data**. It should raise a **descriptive, actionable exception immediately**, preventing corrupted data from propagating further down the pipeline.

> 💡 **Why "immediately"?** A bad value that slips through silently doesn't disappear — it becomes a wrong feature, then a wrong model, then a wrong decision that nobody can trace back. Cheap to catch at the door, expensive to catch at the exit.

### ⚠️ Never use a bare `except`

```python
# ❌ catches everything
try:
    result = risky_step(data)
except:
    pass
```

**A bare `except` will catch everything** — including system interrupts (Ctrl-C) and memory-exhaustion errors — **leaving your system in an unstable "zombie" state**.

```python
# ✅ specific exception, descriptive log, predictable default
try:
    result = risky_step(data)
except ValueError as exc:
    logger.error("risky_step failed for batch %s: %s", batch_id, exc)
    return DEFAULT_RESULT
```

The rule: **when an exception is caught, don't just ignore it** — write a descriptive log message using the `logging` library and return a **clean, predictable default value**.

### Custom exceptions

As pipelines grow, native Python exceptions like `ValueError` or `TypeError` become **too generic**. To make code maintainable and self-documenting, write **custom exceptions** — a simple class inheriting from Python's base `Exception` that represents a **specific domain failure**:

```python
class IncompatibleFeatureSizeError(Exception):
    """Raised when an inference request's feature vector length != the model's."""

class ModelWeightsNotLoadedError(Exception):
    """Raised when predict() is called before the weights are loaded."""
```

> 🎯 A named exception tells the on-call engineer *what broke in ML terms* — not just "a value was wrong somewhere".

---

## 2. Logging — `print()` is not logging

> 🧪 **The 48-hour training job.** You launch an ML training job on an AWS EC2 instance that runs for 48 hours. If you track epoch losses and accuracy with **`print()`** and your SSH session disconnects or the terminal buffer clears, **that information is lost forever**. With a configured **logging** system, every statement is safely piped to a **persistent file** or an observability platform such as **CloudWatch** or **Elasticsearch**.

| | `print()` | `logging` |
|---|---|---|
| Destination | stdout only | file, stream, CloudWatch, Elasticsearch… |
| Severity levels | none | DEBUG / INFO / WARNING / ERROR / CRITICAL |
| Survives disconnect | ❌ | ✅ |
| Timestamps, module name | manual | automatic |
| Switchable per environment | ❌ | ✅ (verbose in dev, quiet in prod) |

**The five levels, in order:**

| Level | Use it for |
|---|---|
| **DEBUG** | detailed diagnostic detail while developing |
| **INFO** | normal progress: "epoch 3 complete, loss 0.21" |
| **WARNING** | something unexpected but survivable: "3% of rows had missing values" |
| **ERROR** | an operation failed: "model file not found, using fallback" |
| **CRITICAL** | the system cannot continue |

*(code: `error_handling_logging.py`)*

---

## 3. Debugging strategies

| Strategy | What it means |
|---|---|
| **Reproduce first** | pin down a minimal input that reliably triggers the bug — you cannot fix what you cannot repeat |
| **Read the traceback bottom-up** | the last line is the actual error; the lines above are the call chain that led there |
| **Log-based debugging** | add structured log statements around the suspect region; works in production where a debugger cannot go |
| **Interactive debugger** | `pdb` / IDE breakpoints — step through, inspect variables live |
| **Bisect** | comment out or `git bisect` halves of the change until the culprit is isolated |
| **Rubber-duck** | explain the code line by line out loud; the explanation usually exposes the assumption that is wrong |

> ⚠️ **ML-specific twist:** in ML, "the code ran without error" is not success. A silent bug shows up as **a metric that quietly got worse**, not as a stack trace. Which is why data validation (Session 12) and monitoring exist.

---

## 4. Style & linting — PEP 8 and friends

**PEP 8** is the official *Python Enhancement Proposal* that defines the language's style guidelines.

> 🎯 **Its objective, stated exactly:** *to ensure that all Python code written by any engineer looks like it was written by the exact same person.*

| PEP 8 covers | Rule |
|---|---|
| **Naming conventions** | variables and functions use **snake_case**; classes use **PascalCase** |
| **Whitespace usage** | always **4 spaces** per indentation level, **never tabs**; single spaces around mathematical operators |
| **Import ordering** | **standard library** first, then **third-party** packages, then **local project** imports — each group separated by a blank line |

```python
# standard library
import os
import logging

# third party
import numpy as np
import pandas as pd

# local
from src.preprocessing import scale_features
```

**Linting** moves style from *subjective argument* to *programmatic validation* — a tool decides, so code review can be about logic instead of formatting.

| Tool | Role |
|---|---|
| **`black`** | **auto-formatter** — rewrites your file into canonical style. No options to argue about. |
| **`flake8` / `pylint`** | **linters** — flag style violations, unused imports/variables, suspicious constructs |
| **`isort`** | sorts and groups imports per PEP 8 |
| **`mypy`** | **static type checker** (see next section) |

> 💡 These plug into **pre-commit hooks** and **CI**, so unstyled code simply cannot be merged.

---

## 5. Type hints & static checking

**Type hints** annotate what goes in and what comes out — a machine-checkable **contract**.

```python
from typing import List

def scale(data: List[float], factor: float) -> List[float]:
    return [x * factor for x in data]
```

- `data: List[float]` and `factor: float` tell **both the developer and the machine** exactly what types are required.
- The return annotation `-> List[float]` **completes the contract**.
- Then run **`mypy`**, a **static type checker**: it parses these annotations and checks for **type mismatches across your entire program** — before the code ever runs.

> 🎯 A type hint is documentation that **cannot go stale**, because a tool verifies it.

---

## 6. Research vs Production code (exam favourite)

> 💡 These are two different *mindsets*, not two levels of skill. Trouble starts when research-style code is shipped as production code.

### The Research mindset

When exploring a brand-new dataset, **you don't know which features will be predictive or which architecture will fit**. Your goal is **rapid discovery and validation**.

- Primary environment: the **Jupyter Notebook** — highly interactive; write a block, execute instantly, inspect the visualisation or data table.
- Coding style is heavily **imperative and sequential**.
- **But this freedom has significant drawbacks:** global variables scattered everywhere, duplicated code, and **manual execution order**.

### Side by side

| Dimension | **Research code** | **Production code** |
|---|---|---|
| **Goal** | rapid discovery & validation | reliability, maintainability, scale |
| **Environment** | Jupyter Notebook | modules, packages, services |
| **Style** | imperative, sequential, exploratory | modular, functions/classes, tested |
| **State** | global variables everywhere | encapsulated, passed explicitly |
| **Execution order** | manual (run cells in some order) | deterministic, orchestrated |
| **Duplication** | copy-paste is fine | DRY, shared libraries |
| **Errors** | crash and fix by hand | fail fast, log, degrade gracefully |
| **Tests** | rare | required (unit, data, model, integration) |
| **Lifespan** | days | years |
| **Audience** | you, this week | your team, on-call, future you |

> 🎯 **The transition is the job.** Session 11 in one sentence: *take the notebook that proved the idea, and give it error handling, logging, style, structure, an API and a package — so somebody else's system can rely on it.*

---

## 7. Design & refactoring (SOLID)

**Refactoring** = *changing a software system's internal structure **without modifying its external behaviour**.*

> ⚠️ Both halves matter. Change behaviour *and* structure at once and you can no longer tell which change broke it.

### The three everyday refactorings from the deck

| Refactoring | What to do |
|---|---|
| **Extract Function** | if 15 lines inside a main script handle feature scaling, move them into a dedicated function `scale_features()`. This keeps the main script **high-level and easy to read**. |
| **Rename Variables** | move away from generic single-letter names like `x`, `df`, `m` → use explicit names like `user_demographics_df`, `random_forest_model`. |
| **Modularise** | once a script grows past a few hundred lines, extract helpers into separate files — `utils.py` for shared helpers, `preprocessing.py` for feature engineering. |

### SOLID mapped onto ML pipelines

| Letter | Principle | In an ML pipeline |
|---|---|---|
| **S** | **Single Responsibility** — a class has one reason to change | one class loads data, another engineers features, another trains, another serves. Not one `Pipeline` god-class. |
| **O** | **Open/Closed** — open for extension, closed for modification | adding a new model type means **adding a subclass**, not editing the trainer's `if/elif` chain. |
| **L** | **Liskov Substitution** — a subclass must be usable wherever the parent is | any `Model` subclass must honour `.fit()`/`.predict()` so the pipeline never needs to know which one it has. |
| **I** | **Interface Segregation** — many small interfaces beat one fat one | a batch scorer shouldn't be forced to implement streaming methods it never uses. |
| **D** | **Dependency Inversion** — depend on abstractions, not concretions | the trainer depends on an abstract `DataSource`, so swapping CSV → S3 → feature store touches one class. |

*(code: `design_refactoring_solid.py`)*

---

## 8. Designing APIs for ML services

**Why wrap models in web APIs instead of embedding them directly into application code?** Three reasons, straight from the deck:

| Reason | Explanation |
|---|---|
| **Decoupling** | your core application backend might be written in **Java, C# or Go**. Exposing the model as an independent HTTP service gives you **language independence**. |
| **Independent scaling** | model inference is **computationally expensive** and often needs **GPU acceleration**. Isolating it into its own API service lets you scale prediction servers **independently of the main web servers**, saving cloud cost. |
| **Seamless model updates** | when you train a better version, deploy it to the API server **without updating or redeploying the main application**. This clean isolation simplifies release cycles. |

### FastAPI

**FastAPI** is built on modern Python features — specifically **asynchronous programming** and **type hints**.

Its most powerful feature is **automatic documentation**: simply by writing your code, FastAPI generates an interactive **Swagger UI** at **`/docs`**. Frontend developers and teammates can test your model **directly in the browser**, with no Postman and no command-line scripts.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class IrisRequest(BaseModel):        # type hints define + validate the contract
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.post("/predict")
def predict(req: IrisRequest):
    features = [[req.sepal_length, req.sepal_width,
                 req.petal_length, req.petal_width]]
    return {"species": model.predict(features)[0]}
```

Run it, then open **`http://127.0.0.1:8000/docs`**. *(code: `fastapi_ml_service.py`)*

> 🎯 **The type hints do triple duty:** they document the contract, **validate incoming requests automatically** (via Pydantic), and generate the Swagger page.

---

## 9. Sharing code & packaging

> 💡 **Sharing is about reproducibility.** The goal is not "you can read my code" — it is "your machine produces my result".

### Version control

| Rule | Why |
|---|---|
| **Never commit directly to `main`** | use **feature branches** for active development and **pull requests** for peer review |
| **Never commit large datasets or heavy model files to Git** | Git is designed to track **lightweight text code**. Large binaries **bloat the repository and slow down development.** |
| **Use DVC instead** | **Data Version Control** tracks large files in **cloud storage** while keeping Git focused strictly on **code** |

> 🌍 **Mental model of DVC:** Git stores a small text *pointer* (a hash) to your 8 GB dataset; the dataset itself lives in S3/GCS. `git checkout` an old commit and `dvc pull` brings back exactly the data that commit used.

### Dependencies & virtual environments

Python packages are **constantly updated, and even minor version upgrades can introduce breaking changes.** The fix: run **every project in an isolated virtual environment**.

| Tool | Where it fits |
|---|---|
| **`requirements.txt`** | the **legacy** approach — a flat list of packages |
| **Conda** | excellent for data science because it manages **non-Python packages too**, like C++ libraries and **GPU drivers** |
| **Poetry** | highly popular for **pure Python** projects. Gives **deterministic dependency resolution**, generating a **`poetry.lock`** that locks the exact version of every library **and every transitive dependency, down to the patch release** |

> ⚠️ `requirements.txt` pins what *you* asked for; a **lock file** pins what actually got installed, including dependencies-of-dependencies. That difference is the usual cause of "works on my machine".

### Docker — the final reproducibility layer

The standard Dockerfile shape for an ML service:

```dockerfile
FROM python:3.11-slim          # 1. clean Python base image
WORKDIR /app
COPY requirements.txt .        # 2. copy dependency files FIRST (layer caching)
RUN pip install --no-cache-dir -r requirements.txt   # 3. install
COPY . .                       # 4. copy the code
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]   # 5. startup command
```

> 💡 **Why copy `requirements.txt` before the code?** Docker caches each layer. Code changes far more often than dependencies — copying requirements first means a code edit doesn't trigger a full reinstall.

> 🎯 **The reproducibility stack, bottom to top:** Git (code) → DVC (data & models) → lock file (exact package versions) → Docker (OS, drivers, runtime). Each layer pins what the layer below cannot.

---

## 🎯 Recap

- **Fail fast:** raise descriptive, actionable exceptions immediately so corrupt data never propagates. **Never bare-`except`** — it swallows interrupts and memory errors, leaving a zombie system. Catch specific, **log**, return a predictable default. Write **custom exceptions** for domain failures.
- **Logging over `print()`:** `print` dies with your SSH session; `logging` persists to files/CloudWatch/Elasticsearch, with levels DEBUG→CRITICAL.
- **PEP 8** exists so all code "looks like it was written by the same person" — snake_case/PascalCase, 4 spaces never tabs, stdlib→third-party→local imports. Enforce with **black · flake8/pylint · isort**; check types with **mypy**.
- **Research vs Production:** notebook, imperative, globals, manual order, rapid discovery **vs** modular, tested, deterministic, long-lived.
- **Refactoring** = change internal structure, **not** external behaviour. Three moves: **Extract Function · Rename Variables · Modularise**. **SOLID** maps directly onto pipeline stages.
- **APIs:** wrap models in HTTP for **decoupling · independent scaling · seamless model updates**. **FastAPI** = async + type hints + free Swagger UI at `/docs`.
- **Packaging:** feature branches + PRs; **never** commit big data to Git (use **DVC**); isolate with venv/**Conda** (handles GPU drivers) or **Poetry** (`poetry.lock` = exact versions); ship in **Docker**.

⬅️ **Prev:** [Session 10 — Time Complexity, Data Structures & OOP](Session-10-Time-Complexity-Data-Structures-and-OOP.md) · ➡️ **Next:** [Session 12 — Quality Assurance](Session-12-Quality-Assurance-Testing-and-RAGAS.md) · 🏠 [Back to index](README.md)
