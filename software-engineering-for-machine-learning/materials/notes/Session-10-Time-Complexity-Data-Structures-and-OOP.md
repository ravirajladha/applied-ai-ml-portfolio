# Session 10 — Time Complexity, Data Structures, OOP & Functional Programming

> **Module 4 · Lecture 10** · Slides: `Session 10.pptx`
>
> **One-line goal:** the three practical skills that make ML code *fast* and *maintainable* — reading **Big-O**, picking the **right data structure**, and structuring code with **OOP**.

### Contents
1. [Time complexity & Big-O](#1-time-complexity--big-o)
2. [Reading the log](#2-reading-the-log--why-log-n-is-magic)
3. [The five ML data structures](#3-the-five-ml-data-structures)
4. [Which structure for which job](#4-which-structure-for-which-job-exam-favourite)
5. [OOP — the pillars](#5-oop--the-pillars)
6. [OOP applied to Agentic AI](#6-oop-applied-to-agentic-ai-exam-favourite)
7. [Functional programming alongside OOP](#7-functional-programming-alongside-oop)
8. [Recap](#-recap)

---

## 1. Time complexity & Big-O

**Time complexity** describes *how the running time of an algorithm grows as the input grows*. It is not "how many seconds" — it is "what shape is the curve".

> 🌍 **Everyday picture.** Finding a name in a phone book. Reading every page start-to-finish is **O(n)**. Opening the middle, deciding "before or after", and throwing away half is **O(log n)**. Same book, wildly different effort.

**Big-O** is the notation for that growth rate — the "**O**" stands for *order* of the function, i.e. its growth rate. In ML it is measured against two things that both get big:

| Symbol | Means |
|---|---|
| **n** | number of data samples (rows) |
| **d** | number of features (columns) |

> 💡 **Why it matters in ML.** ML systems process millions of records, billions of parameters, thousands of concurrent interactions. **An algorithm that works well on a small dataset may become impractical at scale.** Complexity tells you that *in advance*, without waiting for the job to crash.

### The ladder, fastest to worst

| Big-O | Name | What it does | ML example (from the deck) |
|---|---|---|---|
| **O(1)** | Constant | one step, regardless of size | prediction **lookup** |
| **O(log n)** | Logarithmic | halves the problem each step | **threshold search** |
| **O(n)** | Linear | touches every item once | one pass over the dataset |
| **O(n log n)** | Linearithmic | sort-like | **ranking** customers by churn score |
| **O(n²)** | Quadratic | every item against every other | **similarity computation** |
| **O(n!)** | Factorial | tries every ordering | brute-force **feature optimisation** |

> ⚠️ **The cliff sits between O(n log n) and O(n²).** Below it you scale by adding data. Above it, doubling the data **quadruples** the time — 10× data is 100× time. O(n!) is unusable past ~10 items.

> 🧪 **Slide case study — telecom churn.** A company wants to identify customers likely to churn. As the dataset grows, efficient processing becomes critical. The simulation runs one churn pipeline that exercises the whole ladder: prediction lookup **O(1)** → threshold search **O(log n)** → full scan **O(n)** → ranking **O(n log n)** → similarity **O(n²)** → feature optimisation **O(n!)**. *(code: `bigonotation.py`)*

---

## 2. Reading the log — why `log n` is magic

**Logarithm (base 2), in one line:** *how many times can I divide n by 2 until I reach 1?*

| n | log₂(n) |
|---|---|
| 8 | 3 |
| 16 | 4 |
| 64 | 6 |
| 1,024 | 10 |
| 1,048,576 (≈1 M) | 20 |
| 1,073,741,824 (≈1 B) | 30 |

Put side by side, the point becomes obvious:

| Dataset size | O(n) — check every item | O(log n) — discard half each step |
|---|---|---|
| 1,000 | 1,000 operations | **10** |
| 10,000 | 10,000 operations | **14** |
| 100,000 | 100,000 operations | **17** |
| 1,000,000 | 1,000,000 operations | **20** |
| 1,000,000,000 | 1,000,000,000 operations | **30** |

- **O(n)** = check every item.
- **O(log n)** = discard half the remaining items after each step.

> 🎯 Going from a thousand rows to a **billion** rows costs an O(log n) algorithm just **20 extra operations**. That is why sorted structures, indexes and binary search are everywhere in production systems.

---

## 3. The five ML data structures

> 💡 Data is the foundation of ML models, and **the data structure used can significantly impact performance and accuracy.** The five that matter: **List · Tuple · Dictionary · NumPy array · Pandas DataFrame.**

### List — dynamic, mutable array
- A **dynamic mutable array** — it resizes as elements are added.
- **Heterogeneous** — one list can hold both strings and integers.
- Stored in **contiguous memory**. Since the starting address is known, Python computes any element's location directly from its index.
- → **Fast random access, O(1)**, so lists are efficient for retrieving by position. *(code: `listds.py`)*

### Tuple — immutable ordered collection
- An **immutable ordered collection**: elements cannot be modified, added or removed after creation.
- Can hold mixed types (ints, strings, floats, even other tuples).
- Also stored **contiguously**, so also **O(1)** index access.
- Immutability makes it **more memory-efficient** and suited to **read-only** data. *(code: `tupleds.py`)*

### Dictionary — hash-table key→value map
- A **mutable mapping** storing **key–value pairs**. Values can be any type; **keys must be unique and immutable** (str, int, tuple).
- Implemented as a **hash table**: given a key, Python computes its **hash** to locate the value directly instead of searching every entry.
- → **Lookup, insertion and deletion are O(1) *average*.** *(code: `dictionaryds.py`)*

> ⚠️ Note the word **average**. Hash collisions can degrade a dictionary, which is why the deck says *O(1) average* for dict but plain *O(1)* for list/tuple/array indexing.

### NumPy array (`ndarray`) — the numerical workhorse
- NumPy's core structure: a **mutable, homogeneous, multidimensional** array.
- **Homogeneous** = all elements share one dtype → compact storage and faster computation.
- Stored in **contiguous memory** → efficient traversal and **vectorised** operations (one instruction applied across a whole block).
- **O(1)** index access, and **significantly faster than a Python list** for numerical work — a list stores pointers to boxed Python objects; an array stores raw numbers back to back. *(code: `numpyds.py`, `numpyvslist.py`)*

### Pandas DataFrame — labelled table
- Built **on top of NumPy arrays**, so NumPy's principles largely carry over.
- A **two-dimensional, labelled, tabular** structure: rows × named columns.
- Can store **multiple data types across columns** (int, float, str, date) — which is what real-world datasets look like.
- Provides powerful built-ins for **cleaning, filtering, sorting, grouping, and handling missing values**.

```python
import pandas as pd

# basic syntax
pd.DataFrame(data, index=None, columns=None, dtype=None)

# from a dictionary
data = {"Name": ["Alice", "Bob", "Charlie"],
        "Age":  [20, 21, 22],
        "Marks":[85, 90, 88]}
df = pd.DataFrame(data)

# from a NumPy array
import numpy as np
df = pd.DataFrame(np.array([[1, 2], [3, 4], [5, 6]]), columns=["A", "B"])

# the Iris dataset
from sklearn.datasets import load_iris
iris = load_iris()
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
```

---

## 4. Which structure for which job (exam favourite)

The deck asks this as a quiz, then answers it. Learn this table cold:

| Task | Best structure |
|---|---|
| Loading CSV data | **Pandas DataFrame** |
| Clean & preprocess data | **Pandas DataFrame** |
| Store feature names | **List** |
| Map feature names to indices | **Dictionary** |
| Convert data for training | **NumPy array** |
| Store dataset shape or image dimensions | **Tuple** |

And the general-purpose "when to use what":

| Structure | Purpose in ML | Example |
|---|---|---|
| **Python list** | store dynamic collections that may change during preprocessing | feature names, labels, file paths |
| **Dictionary** | store key–value mappings for fast lookup | feature-to-index mapping, hyperparameters, label encoding |
| **Tuple** | store fixed, immutable information | dataset shape `(rows, columns)`, image size `(224, 224, 3)` |
| **NumPy array** | store numerical data, perform fast vectorised computation | feature matrix `X`, target vector `y`, model weights |
| **Pandas DataFrame** | store, manipulate, clean and analyse tabular datasets before training | customer records, sales data, CSV datasets |

> 🎯 **The one-line rule:** *DataFrame to prepare it · NumPy array to train on it · dict to look things up · list for things that change · tuple for things that must not.* *(code: `allds.py`)*

---

## 5. OOP — the pillars

**Object-Oriented Programming** organises code around **objects** that bundle *data* (attributes) with *behaviour* (methods). A **class** is the blueprint; an **object** is one built instance.

| Concept | One-line definition |
|---|---|
| **Class** | the blueprint: what attributes and behaviours this kind of thing has |
| **Object** | one live instance of the class, with its own state |
| **Inheritance** (Pillar 1) | deriving a class from another class, forming a **hierarchy** — gives **code reuse, better organisation, faster development time** |
| **Polymorphism** (Pillar 2) | the ability of an object or method to **take on multiple forms** — the same interface or function executes differently depending on the data type or the object calling it, making code flexible and reusable |
| **Encapsulation** | internal state and logic kept inside the class, reached only through its methods |
| **Abstraction** | complex operations hidden behind a simple interface |
| **Composition** | building a bigger object by *containing* other objects |

> 🌍 **Inheritance vs composition in one breath.** A `ValidationAgent` **is-a** `Agent` → *inheritance*. A `Workflow` **has-a** `ValidationAgent` → *composition*.

---

## 6. OOP applied to Agentic AI (exam favourite)

This is the deck's flagship example — mapping each OOP concept onto an agent system.

| OOP concept | Application in Agentic AI |
|---|---|
| **Class** | an AI agent implemented as a class defining its attributes and behaviours |
| **Object** | each *running* agent is an object with its own state, memory and execution context |
| **Inheritance** | specialised agents inherit from a common base `Agent` class and extend its functionality |
| **Polymorphism** | different agents implement the same method (e.g. `execute()`) in different ways based on their roles |
| **Encapsulation** | an agent's memory, goals and internal logic are encapsulated in the class and accessed through methods |
| **Abstraction** | complex operations — reasoning, planning, tool invocation — hidden behind simple method interfaces |
| **Composition** | multiple agent objects combined to build a complete multi-agent system with coordinated interactions |

And how that lands in the demo code (`demo-class-object-function.py`):

| OOP concept | Demonstration in the code |
|---|---|
| Class | `Agent`, `ValidationAgent`, `SummaryAgent`, `ResearchPaperWorkflow` |
| Object | `workflow`, `validator`, `summarizer` |
| Inheritance | `ValidationAgent` and `SummaryAgent` inherit from the `Agent` base class |
| Polymorphism | both child classes **override `execute()`** with different implementations for validation and summarisation |
| Encapsulation | the LLM client (`self.client`), the model (`self.model`) and `ask_llm()` are encapsulated within `Agent` |
| Abstraction | `ask_llm()` hides the complexity of making the API call from the derived classes |
| Composition | `ResearchPaperWorkflow` **has-a** `ValidationAgent` and a `SummaryAgent` to coordinate the workflow |

> 🧪 **Second worked example — travel planner.** Design an AI-powered travel-planning workflow automating two tasks: one specialised agent provides **live flight details**, another independently creates a **structured sightseeing itinerary** from the user's travel request. Same skeleton — base `Agent`, two subclasses overriding `execute()`, a coordinator composing them. *(code: `travelagentapp.py`)*

> 🎯 **Why OOP for agents:** to add a new capability you **write a new subclass and plug it in** — you never reopen and re-risk the coordinator.

---

## 7. Functional programming alongside OOP

Not everything deserves to be a class. **Standalone functions** are right for stateless, input→output work:

| Functional programming concept | Demonstration in the code |
|---|---|
| Standalone function | `read_paper()` — reads text from a PDF research paper |
| Standalone function | `save_result()` — writes the generated summary to a text file |

> 🎯 **The dividing line:** if it *has state and a role*, make it a **class**; if it just **transforms input into output**, make it a **function**.

---

## 🎯 Recap

- **Time complexity** = the shape of the growth curve, not the seconds. **Big-O** ("order of the function") measures it against **n** (samples) and **d** (features).
- **Ladder:** O(1) → O(log n) → O(n) → O(n log n) → **O(n²)** → O(n!). The scalability cliff is **O(n²)**.
- **log₂(n)** = how many halvings to reach 1. A **billion** rows costs an O(log n) algorithm only **30** operations.
- **Five structures:** list (mutable, O(1) index) · tuple (immutable, O(1) index, memory-efficient) · dict (hash table, **O(1) average**) · NumPy array (homogeneous, contiguous, vectorised) · DataFrame (labelled table built on NumPy).
- **Selection rule:** *DataFrame to prepare · NumPy to train · dict to look up · list for changing · tuple for fixed.*
- **OOP for agents:** class = agent definition · object = running agent · inheritance = specialised agents · polymorphism = each overrides `execute()` · encapsulation = private memory · abstraction = hidden LLM call · composition = the multi-agent workflow.

⬅️ **Prev:** [Session 9 — Implementation & Code Sharing](Session-09-Implementation-and-Code-Sharing.md) · ➡️ **Next:** [Session 11 — Errors, Style, Refactoring, APIs & Packaging](Session-11-Errors-Style-Refactoring-APIs-and-Packaging.md) · 🏠 [Back to index](README.md)
