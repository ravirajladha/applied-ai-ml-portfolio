# SE4ML — Post-Midsem Cheat Sheet (Sessions 9–16) ⭐ HIGH WEIGHTAGE

> **AIMLCZG546** · Modules 4–7: **Implementation & Code Sharing · Quality Assurance · Deployment · Responsible ML Engineering**
> Built for the **open-book end-sem (40%, 2.5 hrs)**. This is the half the exam leans on — study it first.

---

## 0. The 60-second map

```
S9–S11  IMPLEMENTATION   good code · Big-O · data structures · OOP ·
                         errors/logging · PEP 8 · SOLID · FastAPI · packaging
S12     QUALITY ASSURANCE  data/model/pipeline/system tests · slicing ·
                           shadow/canary/A-B · ML security · RAGAS
S13–S14 DEPLOYMENT       Docker · Kubernetes · 4 serving designs ·
                         4 deployment strategies · MLOps/LLMOps/AgentOps
S15     RESPONSIBLE ML   versioning/provenance/reproducibility · explainability ·
                         fairness · safety · security (CIA) · privacy
```

---

# MODULE 4 — Implementation & Code Sharing

## 1. What is good code (S9)

**Five features:** **Simplicity (DRY)** · **Modularity** · **Readability** (PEP 8 + pylint) · **Performance** · **Robustness**.

**The performance-analysis ladder — measure before you optimise:**

```
time                     → how long did the whole thing take?      (1 run, rough)
timeit / %%timeit        → how long on average, how consistent?    (many runs, avg ± std)
cProfile                 → WHICH FUNCTION is the bottleneck?       (per-function)
line_profiler            → WHICH LINE inside it is slow?           (per-line)
memray / memory_profiler → which line/function eats MEMORY?        (per-line memory)
```

**Ways to make Python faster:** better algorithm → better data structure → built-ins/vectorisation → async → parallelism. **But measure first.**

---

## 2. Time complexity & Big-O (S10)

**Time complexity** = how running time **grows as input grows**. **Big-O** = the *order* (growth rate) of that function, measured against **n** (samples) and **d** (features).

| Big-O | Name | What it does | ML example |
|---|---|---|---|
| **O(1)** | Constant | one step regardless of size | prediction **lookup**, dict access, array index |
| **O(log n)** | Logarithmic | halves the problem each step | **threshold search** / binary search |
| **O(n)** | Linear | touches every item once | full scan of the dataset |
| **O(n log n)** | Linearithmic | sort-like | **ranking** customers by score |
| **O(n²)** | Quadratic | every item vs every other | **similarity computation** |
| **O(n!)** | Factorial | every ordering | brute-force **feature optimisation** |

**log₂(n) = how many times you can divide n by 2 until you reach 1.**

| Dataset size | O(n) | O(log n) |
|---|---|---|
| 1,000 | 1,000 ops | **10** |
| 100,000 | 100,000 ops | **17** |
| 1,000,000 | 1,000,000 ops | **20** |
| 1,000,000,000 | 1,000,000,000 ops | **30** |

> 🎯 **The cliff is at O(n²)** — double the data, quadruple the time. **O(n)** = check every item; **O(log n)** = discard half each step.

---

## 3. The five ML data structures (S10) ⭐

| Structure | Nature | Storage | Access | Key point |
|---|---|---|---|---|
| **List** | dynamic, **mutable**, heterogeneous | **contiguous** | **O(1)** by index | resizes as elements are added |
| **Tuple** | **immutable**, ordered, mixed types | **contiguous** | **O(1)** by index | immutability → **more memory-efficient**, read-only data |
| **Dictionary** | mutable **key–value** map; keys unique & immutable | **hash table** | **O(1) average** | hashes the key to jump straight to the value |
| **NumPy array** | mutable, **homogeneous**, multidimensional | **contiguous** | **O(1)** by index | one dtype + contiguous → **vectorised**, far faster than a list |
| **Pandas DataFrame** | 2-D **labelled** table, mixed column types | built **on NumPy** | label/positional | cleaning, filtering, sorting, grouping, missing values |

### The selection quiz (verbatim from the deck) ⭐

| Task | Answer |
|---|---|
| Loading CSV data | **Pandas DataFrame** |
| Clean & preprocess data | **Pandas DataFrame** |
| Store feature names | **List** |
| Map feature names to indices | **Dictionary** |
| Convert data for training | **NumPy array** |
| Store dataset shape / image dimensions | **Tuple** |

> 🎯 *DataFrame to prepare · NumPy to train · dict to look up · list for things that change · tuple for things that must not.*

---

## 4. OOP for Agentic AI (S10 + S12) ⭐

| OOP concept | In Agentic AI | In the demo code |
|---|---|---|
| **Class** | an agent implemented as a class defining attributes & behaviours | `Agent`, `ValidationAgent`, `SummaryAgent`, `ResearchPaperWorkflow` |
| **Object** | each **running** agent, with its own state, memory, execution context | `workflow`, `validator`, `summarizer` |
| **Inheritance** | specialised agents inherit from a common base `Agent` and extend it | `ValidationAgent`/`SummaryAgent` inherit `Agent` |
| **Polymorphism** | different agents implement the **same method (`execute()`) differently** by role | both children **override `execute()`** |
| **Encapsulation** | memory, goals and internal logic held inside the class, reached via methods | `self.client`, `self.model`, `ask_llm()` inside `Agent` |
| **Abstraction** | reasoning, planning, tool invocation hidden behind simple interfaces | `ask_llm()` hides the API call |
| **Composition** | multiple agent objects combined into a multi-agent system | `ResearchPaperWorkflow` **has-a** validator and summariser |

**Functional programming alongside it:** standalone functions for stateless work — `read_paper()` (reads a PDF), `save_result()` (writes the summary).

> 🌍 **The Hollywood Production Crew analogy.** *Procedural* = one director holding the camera, doing makeup, writing the script and sweeping the floor — a monolithic script with dozens of `if/else` guiding an LLM: **fragile, unscalable, crashes on minor changes**. *OOP* = a crew: base "Crew Member" (`Agent`), specialised roles by **inheritance** (Director/`ValidationAgent`, Writer/`SummaryAgent`, Cinematographer/`FormattingAgent`), each in their own bubble (**encapsulation**), assembled by the producer (**composition**) who just says "Execute!" (**polymorphism**). Adding a Sound Engineer = **a new subclass**, not a rewrite.

---

## 5. Errors, logging, style & refactoring (S11)

### Fail fast
Code must **never behave unpredictably on corrupt data** — raise **descriptive, actionable exceptions immediately**, preventing corrupted data from propagating down the pipeline.

> ⚠️ **Never use a bare `except`.** It catches **everything**, including **system interrupts and memory-exhaustion errors**, leaving the system in an **unstable zombie state**. When you catch an exception: **log a descriptive message** with the `logging` library and **return a clean, predictable default**.

**Custom exceptions:** native `ValueError`/`TypeError` are too generic. Inherit from `Exception` to name **domain failures** — `IncompatibleFeatureSizeError`, `ModelWeightsNotLoadedError`.

### Logging over `print()`
> *"If you don't build logging and error handling into your system, your users will become your loggers."*

**The 48-hour EC2 training job:** with `print()`, an SSH disconnect or cleared terminal buffer loses the epoch losses **forever**. With `logging`, everything is piped to a **persistent file** or **CloudWatch / Elasticsearch**.
**Levels:** DEBUG → INFO → WARNING → ERROR → CRITICAL.

### PEP 8 & linting
**Objective of PEP 8:** *ensure all Python code written by any engineer looks like it was written by the exact same person.*

| Covers | Rule |
|---|---|
| **Naming** | variables/functions **snake_case**; classes **PascalCase** |
| **Whitespace** | **4 spaces** per indent level, **never tabs**; single spaces around operators |
| **Import ordering** | **standard library → third-party → local**, blank line between groups |

**Tools:** **black** (auto-formatter) · **flake8 / pylint** (linters) · **isort** (imports) · **mypy** (**static type checker** — parses type annotations and finds type mismatches across the whole program).

**Type hints as a contract:** `def scale(data: List[float], factor: float) -> List[float]:` — the annotations tell **both the developer and the machine** what is required; the return type **completes the contract**.

### Research vs Production ⭐

| Dimension | **Research** | **Production** |
|---|---|---|
| Goal | **rapid discovery and validation** | reliability, maintainability, scale |
| Environment | **Jupyter Notebook** (interactive: run a block, inspect instantly) | modules, packages, services |
| Style | **imperative and sequential** | modular, functions/classes |
| State | **global variables scattered everywhere** | encapsulated, passed explicitly |
| Execution order | **manual** | deterministic, orchestrated |
| Duplication | **code is duplicated** | DRY, shared libraries |
| Errors | crash and fix by hand | fail fast, log, degrade gracefully |
| Tests | rare | required |
| Lifespan | days | years |

### Refactoring
**Definition:** *changing a software system's **internal structure** without modifying its **external behaviour**.*

| Move | What to do |
|---|---|
| **Extract Function** | pull 15 lines of feature scaling into `scale_features()`; keep the main script high-level |
| **Rename Variables** | `x`, `df`, `m` → `user_demographics_df`, `random_forest_model` |
| **Modularise** | past a few hundred lines, split into `utils.py`, `preprocessing.py` |

**SOLID mapped to ML pipelines:**

| | Principle | In a pipeline |
|---|---|---|
| **S** | Single Responsibility | separate loader / feature engineer / trainer / server classes |
| **O** | Open/Closed | new model = **new subclass**, not editing an `if/elif` chain |
| **L** | Liskov Substitution | any `Model` subclass honours `.fit()`/`.predict()` |
| **I** | Interface Segregation | a batch scorer isn't forced to implement streaming methods |
| **D** | Dependency Inversion | trainer depends on abstract `DataSource` — swap CSV→S3→feature store in one place |

---

## 6. APIs & packaging (S11) ⭐

### Why wrap a model in a web API instead of embedding it?

| Reason | Explanation |
|---|---|
| **Decoupling** | your backend may be **Java, C#, Go** — an HTTP service gives **language independence** |
| **Independent scaling** | inference is **computationally expensive** and often needs **GPU**; scale prediction servers **separately** from web servers, saving cloud cost |
| **Seamless model updates** | deploy a better model to the API server **without redeploying the main application** |

**FastAPI** — built on **asynchronous programming** and **type hints**. Its standout feature is **automatic documentation**: an interactive **Swagger UI at `/docs`** generated just by writing the code, so teammates test the model **in the browser** with no Postman.

### Reproducible packaging

| Layer | Tool | Pins |
|---|---|---|
| Code | **Git** — feature branches + PRs, **never commit to `main`** | source |
| Data & models | **DVC** — Git bloats on large binaries; DVC tracks them in **cloud storage** | datasets, model files |
| Dependencies | **`requirements.txt`** (legacy) · **Conda** (also manages **non-Python packages, C++ and GPU drivers**) · **Poetry** (**deterministic resolution**, `poetry.lock` locks **every library and transitive dependency down to the patch release**) | package versions |
| Environment | **Docker** | OS, runtime, everything |

**Dockerfile shape:** `FROM` clean Python base → `COPY` dependency files → `RUN` install → `COPY` code → `CMD` startup command. *(Copy requirements **before** the code so a code edit doesn't bust the install cache.)*

---

# MODULE 5 — Quality Assurance (S12)

## 7. Traditional vs ML testing ⭐

| | **Traditional software** | **Machine learning** |
|---|---|---|
| Logic | **explicitly programmed** | **learned from data** |
| Tests verify | whether the logic produces **expected outputs** | the **learning process**, **data integrity**, **statistical outputs** |
| Failure modes | **bugs** | **concept drift · data corruption · biased training data** |

**ML-specific testing dimensions — Data · Model · Infrastructure · Heuristic:**

| Dimension | Validates |
|---|---|
| **Data tests** | schemas, missing values, feature distributions |
| **Model tests** | predictive performance, fairness, robustness to edge cases |
| **Infrastructure tests** | stress-test serving APIs, measure inference latency |
| **Heuristic tests** | common-sense rules (e.g. **age cannot be negative**) |

**The MLOps control loop:**
`Data → Features → Training → Registry → Serving → Monitoring → (triggers retraining) → Data`

---

## 8. Data quality ⭐

**Garbage in, garbage out.**
- **Data quality dictates the upper bound of model performance.**
- **Historical data may contain human biases that the model will amplify.**
- **Errors in collection pipelines silently degrade production systems.**
- **Automated data validation is a strict requirement before any training begins.**

**Dimensions:** Accuracy · Completeness · Consistency · Timeliness/Freshness · Validity · Uniqueness.

**The data validation pipeline — four gates:**

| Gate | Checks for |
|---|---|
| **Ingestion** | raw data from product events, IoT streams, CRM tools |
| **Schema Check Gate** | **missing columns, type changes** |
| **Value Check Gate** | **impossible ranges** (negative age), **statistical outliers** |
| **Label Health Gate** | **extreme class imbalance, missing target labels** |
| **Action Gateway** | if inputs don't match expectations, **the pipeline automatically halts** |

## 9. Pipeline quality

**Definition:** the **robustness of the automated sequence from data extraction to model deployment**.

| Property | Meaning |
|---|---|
| **Idempotency** | **re-running with the same inputs must yield the exact same outputs** |
| **Version control** | **code, data and model artifacts linked and versioned together** |
| **Orchestration** | **Airflow / Kubeflow** manage complex dependency graphs |

**CI for ML:** code commits → syntax + unit tests · architecture changes → **train on a small synthetic dataset** · schema updates → **validate against historical data** · all pass → **deployable artifact in a central registry**.

## 10. Model quality & metrics ⭐

- **Accuracy is misleading on imbalanced data** (1-in-1000 fraud: predicting "no fraud" always = 99.9% accurate, worthless).
- Quality also includes **interpretability, fairness, computational efficiency**.
- Evaluate on data **strictly unseen during training**; **quality degrades over time**.

| Metric | Formula | Answers |
|---|---|---|
| **Precision** | **TP / (TP + FP)** | of what I **flagged**, how much was right? *(accuracy of positive predictions)* |
| **Recall** | **TP / (TP + FN)** | of what **was** positive, how much did I catch? *(ability to find all positives)* |
| **F1** | 2PR / (P + R) | **balances precision and recall for imbalanced data** |
| **RMSE** | √(mean squared error) | regression — **penalises large errors heavily** |

> **Spam filter → precision.** **Cancer screening → recall.** **Imbalanced / can't choose → F1.**

## 11. Slicing & subpopulation testing ⭐

> **A model with 95% global accuracy might have 50% accuracy on a minority demographic.**

**Data slicing** = divide the test set into subgroups (**gender, location, device type**) → **calculate metrics independently per slice** → identify where the model needs **active mitigation or retraining**.

> 🎯 **Never report a single aggregate number** — an average is where failures hide. This is also how **fairness** (S15) is measured operationally.

## 12. System quality & monitoring

- **The ML model is often <5% of the total codebase.**
- System quality covers **UI/UX, database reliability, network stability**.
- **A perfect model with a failing front-end has zero business value.**

| Monitoring layer | Watch |
|---|---|
| **System metrics** | CPU, memory, network latency |
| **Model metrics** | **prediction distribution, confidence scores, anomaly rates** |
| **Business metrics** | click-through, conversion, revenue |
| **Alerting** | automated thresholds that **page engineers** on significant deviation |

> 💡 In production you usually have **no labels yet**, so you watch the **prediction distribution** — a sudden shift is the earliest available symptom of drift.

## 13. Testing in production ⭐

**Why offline testing isn't enough:** offline data is **static** while user behaviour is **dynamic**; **models change user behaviour, creating feedback loops offline tests cannot simulate**; production experimentation is the **final proof of business impact**; it needs **infrastructure to route traffic securely**.

| Strategy | Who sees the new model | User impact if bad | Answers |
|---|---|---|---|
| **Shadow** | **nobody** — gets a **copy** of live traffic, predictions **logged not served** | **none** | *"does it work at production load?"* |
| **A/B test** | a **split** of users, each group a different version | half your users | *"is it **better**?"* |
| **Canary** | a **small subset** first, expand if healthy | limited blast radius | *"is it **safe to expand**?"* |

## 14. Security for ML ⭐

**The new attack surface:** ML introduces **vulnerabilities distinct from traditional web apps**; attackers can manipulate **training data** or **inference requests**; you must defend both the **IP (model weights)** and **data privacy**; **threat modelling must be integrated early**.

| Lifecycle phase | Attack | What it does |
|---|---|---|
| **Data collection** ⚠️ | **Data poisoning** | crafted samples injected into training data corrupt/backdoor the model |
| Training | **Backdoor / trojan** | normal behaviour except on a secret trigger |
| Model storage | **Model theft / extraction** | weights stolen, or reconstructed by repeated API queries |
| **Deployment / inference** ⚠️ | **Adversarial examples** | tiny input perturbations flip the prediction |
| Inference | **Membership inference** | determines whether a person's record was in the training set |
| LLM serving | **Prompt injection** | malicious instructions hidden in input or retrieved documents |

> ⚠️ **Data collection and deployment are the most frequently targeted phases** — the two ends where external input enters.

## 15. RAGAS ⭐

**RAG** = Retrieval-Augmented Generation (LLM + external database).
**The problem:** **BLEU and ROUGE are inadequate for measuring hallucination and context relevance** — word overlap says nothing about whether the answer was invented.
**RAGAS** = **Retrieval Augmented Generation Assessment** — an automated framework using an **LLM evaluator** to score the **distinct components** of a RAG pipeline **without human labels**.

**Two pipelines to evaluate independently: the Retriever and the Generator.**

| Evaluates | Metric | Measures |
|---|---|---|
| **Generator (LLM)** | **Faithfulness** | is the answer **strictly grounded in the retrieved context**? → **detects hallucination** |
| **Generator** | **Answer Relevance** | how well the answer **addresses the user's initial prompt** |
| **Retriever (vector search)** | **Context Precision** | are the top retrieved chunks **relevant, not noise**? |
| **Retriever** | **Context Recall** | did retrieval **fetch all the necessary facts**? |

> **High precision = no junk data; high recall = no missing facts.**

**Diagnostic use (the likely exam angle):**

| Symptom | Culprit | Fix |
|---|---|---|
| Low **context recall** | retriever never fetched the fact | chunking, embeddings, top-k |
| Good context but low **faithfulness** | the LLM invented something | prompt / model |
| Low **context precision** | noise crowding the context window | reranking, tighter retrieval |
| Low **answer relevance** | true but doesn't answer the question | prompt |

---

# MODULE 6 — Deployment (S13–S14)

## 16. Deployment & its four components ⭐

**Deployment** = integrating a trained model into a **real-world production environment** so it predicts on **live, unseen data**, exposed via **REST or gRPC APIs**, and kept **scalable, reliable, secure and continuously monitored** as workloads and data evolve.

| Component | What it does |
|---|---|
| **Model packaging & containerisation** | model + **weights, dependencies, runtime, preprocessing** packaged into a portable, reproducible container with **Docker** |
| **Model serving** | deployed as a service exposing a **REST/gRPC API** via **FastAPI or Flask** |
| **Scalability & orchestration** | **Kubernetes**: **horizontal pod autoscaling, load balancing, self-healing, rolling updates** |
| **MLOps** | versioning, CI/CD, automated testing, deployment, monitoring, logging, performance tracking, **retraining** |

> **Package · Serve · Orchestrate · Operate.**

## 17. Containers vs VMs ⭐

> 🌍 **The singer analogy.** Concert 1 — the mike doesn't work. Concert 2 — the speakers don't work. So the singer **buys his own mike and speakers and carries them everywhere**, avoiding the vagaries of the environment. That is a container. It answers *"I can't replicate the production issue in development."*

**A container** is a **standardised package of software** — **code, runtime, system libraries and settings all inside a single container**. *Build, Ship, Run — Any App, Anywhere.*

| | **Container** | **Virtual Machine** |
|---|---|---|
| **Virtualises** | the **operating system** | the **hardware** |
| **Guest OS** | none — **shares the host OS kernel** | a **full guest OS per VM** |
| **Size** | megabytes | gigabytes |
| **Startup** | **seconds** | minutes |
| **Overhead / density** | minimal / many per host | high / few per host |
| **Isolation** | process-level | hardware-level (stronger) |

## 18. Docker's three things ⭐

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

**Purpose:** **reproduce the environment** in Dev, Staging and Production. Share images via **`docker push` / `docker pull`** to public or private repositories. **Docker Hub** = the world's largest library of container images. **Docker Desktop** = one-click GUI for Mac/Linux/Windows.

**Containerising an ML model** — inside the container: the **trained model** (`.pkl`/`.onnx`/`.pt`/`.h5`), **inference code**, **dependencies**, **runtime environment**, **config files**, optional **pre/post-processing**.

## 19. Kubernetes ⭐

**Kubernetes (K8s)** = a **container orchestration tool** managing applications/services on a container platform like Docker. From **Google labs → donated to CNCF**; the **first CNCF project to graduate**; **open source**, written in **Golang**.
**Features:** **High availability (no downtime)** · **Scalability (high performance)** · **Disaster recovery (backup & restore)**.

| Object | Definition |
|---|---|
| **Master Node** (Control Plane) | **manages the entire cluster**; holds API server, etcd, controller manager, scheduler |
| **Worker Nodes** | where **containers run**; run the workload and communicate with the master |
| **Pod** | the **smallest deployable unit** — **a group of one or more containers with shared storage and network** |
| **Service** | **exposes a group of pods**, giving a **stable IP and DNS name** |
| **Controller** | manages the **lifecycle of pods/services**, keeping the **desired number of replicas** running |

**Master node components:**

| Component | Role |
|---|---|
| **API Server** | the **central control point**, exposes the Kubernetes API, **stores cluster state in etcd** |
| **etcd** | **distributed key-value store** of cluster configuration — the **source of truth** |
| **Controller Manager** | runs controllers that regulate state — **ReplicaSet** (desired replicas), **Deployment** (rolling updates) |
| **Scheduler** | **assigns pods to nodes** by resource requirements, node availability, user policies |

**Worker node components:** **kubelet** (manages node state, ensures containers run and are healthy, **restarts them if they fail**) · **kube-proxy** (**network connectivity to and from pods**). **kubectl** = the **CLI you** use to deploy apps, inspect/manage resources, view logs.

> 🎯 **API Server takes the order · etcd writes it down · Scheduler decides where it goes · Controller Manager keeps it that way.**

**Layers of abstraction:** `Deployment → ReplicaSet → Pods → Containers`. A **Deployment** is a **template for creating pods** in a YAML file.

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

> ⚠️ **Never deploy a bare Pod in production** — a Pod that dies stays dead; a **Deployment** recreates it.

## 20. The inference function & feature encoding (S14) ⭐

> **Prediction = f(Input Features, Trained Model)** — and **the model remains fixed during inference.**

Shape: **preprocess → predict → return**.

**Feature encoding** converts **non-numerical (categorical/text) data into numerical values** the model can use — raw inputs (`Sepal Length = 5.1 cm`…) → **feature vector** `[5.1, 3.5, 1.4, 0.2]`.

> ⚠️ **THE RULE:** *the feature-encoding code used for **training** must be the **same code** used for encoding runtime data during **inference**. **Factor the shared code into a reusable library.*** (Otherwise: **training/serving skew** — nothing crashes, every prediction is quietly wrong.)

## 21. Four designs for serving a model ⭐

| # | Design | How | Example |
|---|---|---|---|
| **1** | **Model inference as a Library** | model + inference function **embedded as a local function/library**; model **loaded into memory**, inference is a **local call** | **Tesseract** OCR |
| **2** | **Model inference as a Service** (local or cloud) | a **dedicated server** answering via **RESTful API**; **replicable across machines / VMs / containers** | **Iris model via FastAPI** |
| **3** | **Batch processing** | predictions for **a large amount of data all at once**; **move the model to the data, not the data to the model** | **Netflix** scoring millions of viewing histories overnight |
| **4** | **Cached predictions** | predictions are **expensive but distinct inputs are few** → **cache or precompute all**; inference becomes a **database lookup** | *"Frozen"* cached as a **"U"** rating |

> 🎯 **The deciding question: when is the answer needed?** *Right now, per request* → library/service. *Tomorrow, for everyone* → batch. *Right now, and I've computed it before* → cache.

## 22. Four deployment strategies ⭐⭐

**Zero-downtime deployment** (a.k.a. **hot deployment**) = switching users from one release to another **nearly instantaneously**.

| Strategy | Update pattern | Downtime | Rollback | Cost | Risk |
|---|---|---|---|---|---|
| **Basic** | **all nodes at the same time** | **possible outage** | **slow** | lowest | **highest** |
| **Ramped** (rolling / incremental) | **one node at a time**, incrementally | none | relatively simple | low | medium |
| **Blue/Green** | **two identical environments**, then switch traffic | none | **easiest — flip back** | **highest (2× env)** | medium |
| **Canary** | **small subset of users first**, then full rollout | none | easy — reroute the subset | medium | **lowest** |

| Strategy | Detail to quote |
|---|---|
| **Basic** | *not outage-proof, slows down rollback* — **preferable only for very small applications/services** |
| **Ramped** | **the default deployment strategy in Kubernetes.** Pros: simple rollback, less risky than basic. Cons: **requires services to support both new and old versions**; verification at every increment **makes it slow** |
| **Blue/Green** | **blue = staging** (QA and UAT happen here), **green = production**; traffic shifts once changes are accepted. Pros: simple, fast, well-understood, **straightforward rollback**. Cons: **cost — replicating a production environment is complex and expensive**, especially with microservices; **QA/UAT may miss anomalies and all traffic shifts at once** |
| **Canary** | release to a **small group of customers** first. **Example: Facebook releases a feature only to the Asia-Pacific region**, then rolls out further |

> 🎯 **Answering "which strategy?":** name the constraint. *Tiny app* → Basic. *Kubernetes default, no extra infra* → Ramped. *Need instant clean rollback, can afford 2× environments* → Blue/Green. *Unproven model, want real users, limited blast radius* → **Canary**.

## 23. MLOps vs LLMOps vs AgentOps ⭐⭐

| | **MLOps** | **LLMOps** | **AgentOps** |
|---|---|---|---|
| **Core focus** | **predictive models** — DevOps principles for traditional ML & task-specific models | **language and generation** — adapting/grounding **foundation models** via **prompt engineering and RAG** | **autonomous execution and decisions** — agents that **reason, plan, use tools, decide** |
| **Data type** | **structured, numerical, tabular** | **unstructured text, documents, vector embeddings** | **real-time execution states, API interactions, environment variables** |
| **Key challenges** | **feature stores**, **data & model drift**, retraining pipelines | **prompt versioning**, **hallucinations**, **context-window management**, **token costs** | **multi-step reasoning traces**, **agent memory**, **tool authorisation**, **infinite loops**, **human-in-the-loop (HITL) guardrails** |
| **Success metrics** | F1, accuracy, precision, recall, latency | **hallucination rate**, toxicity/bias, coherence, token usage, latency | **goal achievement**, task success rate, **tool-call correctness** |
| **Tools** | **MLflow, SageMaker Pipelines, Databricks, Airflow, Prefect, Kubeflow** | **LangChain, LlamaIndex, Weights & Biases, PromptLayer** | **LangGraph, CrewAI, AutoGen**, AgentOps platforms |
| **Monitoring focus** | model degradation, data drift | prompt performance, hallucinations, token usage, response quality | agent reasoning, planning, tool usage, memory, collaboration |

> 🎯 **MLOps ships a *number*, LLMOps ships *text*, AgentOps ships an *action*** — each step harder to verify.

**Extra metric rows worth quoting:** MLOps → ROC-AUC, RMSE, MAE, throughput, data freshness. LLMOps → BLEU, ROUGE, BERTScore, Exact Match, **TTFT / tokens-per-sec**, cost per 1K tokens, retrieval accuracy. AgentOps → goal completion rate, **retry success rate**, number of tool calls, **number of human interventions**.

---

# MODULE 7 — Responsible ML Engineering (S15)

## 24. Responsible AI ⭐

> **IBM definition:** a **set of principles** guiding the **design, development, deployment and use** of AI — building **trust**, considering **broader societal impact**, and **aligning technologies with stakeholder values, legal standards and ethical principles**, embedding ethical principles into applications and workflows to **mitigate risks while maximising positive outcomes**.

**Six principles:** **Versioning/Provenance/Reproducibility · Explainability · Fairness · Safety · Security · Privacy.**

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

## 25. Versioning · Provenance · Reproducibility

> 🧪 **Scenario — debugging a loan decision** *(2019 Apple Card controversy).* Income, credit history and market feeds flow into **three interacting models (A·B·C)** that set a credit limit. Investigators must reconstruct **which model version ran, which code produced it, and what exact inputs led to this decision — despite continuous A/B tests and canary releases.**

| Concern | Definition |
|---|---|
| **Versioning** | track **revisions (over time)** and **variants (in parallel)** of data, code and models so **any past state can be retrieved** |
| **Provenance (lineage)** | trace **how data flows, who created or edited it, and what process produced each artifact** |
| **Reproducibility** | whether models and predictions **can be recreated, despite nondeterministic training** |

**Five strategies for versioning large datasets:**

| Strategy | Trade-off |
|---|---|
| **Store full copies** | simple, fast access; **storage-heavy** if changes are frequent |
| **Store deltas** | space-efficient for small changes; **slower to reconstruct** a past version |
| **Offsets in append-only data** | cheap and simple; **only works for logs and event streams** |
| **Version individual records** | **per-key edit history** — natural for customer/entity records |
| **Version the pipeline** | **recreate derived data on demand** from versioned inputs + deterministic code |

**Reproducibility breaks because of:** Python/library versions · dataset versions · **random initialisation** · train/test splits · changed preprocessing · hyperparameters · **hardware/GPU differences** · undocumented code changes.
**Fix:** seeds + pinned dependencies + versioned data + experiment tracking + containerised environment.

## 26. Explainability ⭐⭐

**XAI** = tools and methods that help humans **understand how AI models make decisions**, turning **"black box" algorithms into transparent systems** so users can see **why**, **check fairness**, and **trust the results**.

| Term | The question |
|---|---|
| **Transparency** | **Can I *see* how the model works?** *(e.g. a decision tree — you can see the structure & rules)* |
| **Interpretability** | **Can I *understand* how the model works?** *(e.g. a points scorecard — a human can follow the logic)* |
| **Explainability** | **Can I understand *why* the model made *this particular* prediction?** *(Person A → High Risk **because** prior arrests contributed strongly and young age moderately)* |

> 🎯 A deep neural network can be **explainable** (via SHAP/LIME) while being neither transparent nor interpretable.
> **Intrinsically interpretable:** decision trees, linear/logistic regression, scorecards. **Post-hoc:** SHAP, LIME, counterfactuals, feature importance, saliency maps.
> **Scenario in the deck:** **recidivism risk assessment**.

## 27. Fairness ⭐

> 🧪 **Amazon's AI recruiting engine "did not like women".**
> **Problem:** Amazon **scrapped** an experimental AI recruiting engine after finding it **penalised résumés containing women's college names or female-oriented organisation terms**.
> **Cause:** it was **trained on 10 years of historical hiring patterns, which inherently reflected male dominance in technical engineering roles.**

**The self-reinforcing loop:** `Biased training data → Biased model → Biased real-world outcomes → reinforces on the next training cycle.`

**Fairness is a system-wide concern:** **anticipate bias at each level** · **document fairness at team interfaces (Model Cards, Datasheets)** · **monitor group outcomes continuously in production** · give teams an **incident-response plan**.

> ⚠️ Removing the gender field does **not** fix it — **proxies** (a women's college, a club) carry the same signal. Measure with **slicing** (S12).

## 28. Safety ⭐

**Safety** = prevention of failure/malfunction resulting in **death or serious injury**, **loss of or severe damage to property**, or **harm to the environment or society**.
A **safety-critical ML system** is one whose **incorrect prediction, unexpected behaviour or failure could cause serious injury, loss of life, or significant damage** to people, equipment or the environment.

**Examples:** aircraft (obstacle detection, flight control) · autonomous vehicles (pedestrians, hazards) · medical devices (pacemakers) · railways (collision avoidance) · nuclear plants (anomaly detection) · industrial robots alongside humans.

**Three categories of ML safety** *(mlsafety.org)*:

| Category | The question |
|---|---|
| **Robustness** | **Can the ML system withstand hazards?** — behave safely on **unexpected, unusual, corrupted, adversarial or deliberately manipulated inputs**. *Example: a **Stop sign with stickers is no longer detected**.* |
| **Monitoring** | **Can we detect problems?** — observe the model, detect **anomalies, malicious behaviour, hidden capabilities, unexpected behaviour**. **MLOps/LLMOps/AgentOps help here.** |
| **Alignment** | **Is the ML system doing what we actually want?** — it may be **technically successful but pursue the wrong objective**. *Example: told to **"maximise customer satisfaction"**, the model **increases the measured score by giving customers misleading information**.* |

## 29. Security — CIA + three supports ⭐

| # | Characteristic | Definition | Example |
|---|---|---|---|
| **1** | **Confidentiality** | data/services **protected from unauthorised access** | a hacker cannot access income-tax returns on a government computer |
| **2** | **Integrity** | data/services **not subject to unauthorised manipulation** | a student's grade hasn't changed since the instructor assigned it |
| **3** | **Availability** | the system is **available for legitimate use** | a DoS attack won't stop you ordering a book online |
| **4** | **Authentication** | **verifies the identities** of the parties — are they who they claim? | an email "from a bank" really did come from the bank |
| **5** | **Non-repudiation** | the sender **cannot deny sending**, the recipient **cannot deny receiving** | you can't deny ordering online; the merchant can't disclaim your order |
| **6** | **Authorisation** | **grants a user the privileges** to perform a task | online banking authorises a legitimate user to access his account |

> **Confidentiality = who can *see* it? · Integrity = who can *change* it? · Availability = can legitimate users *use* it?**
> ⚠️ **Authentication = *who are you?* · Authorisation = *what may you do?***

**Security in ML** = protecting **training data, models, ML pipelines, infrastructure and prediction services** from unauthorised access, manipulation and disruption:

| | ML examples |
|---|---|
| **Confidentiality** | attacker can't access a dataset of income/medical records · an unauthorised employee can't download the fraud-detection model · **an ML API does not expose sensitive training data through carefully crafted queries** |
| **Integrity** | attacker can't **modify the training dataset** · a deployed model **can't be secretly replaced** with a malicious one · config and results can't be tampered with |
| **Availability** | the **inference endpoint stays operational despite malicious requests** · training infrastructure stays available for **critical retraining** |

## 30. Privacy ⭐

**Privacy** = the ability of an individual or group to **control what information about them is shared and how it may be used**.

**Privacy threats from ML:**
- ML can **predict sensitive information from innocent-looking data shared for another purpose** — e.g. **age, gender, race and political leaning from a few search queries or posts**.
- Companies **aggregate massive data and integrate it from various sources**, shared intentionally or not, **pushing the power to predict information intended to be private**.

> ⚠️ **AI can infer sensitive information that a person never explicitly provided** — so "we never collected race" is not a defence.

**Techniques:** anonymisation/pseudonymisation · **differential privacy** (calibrated noise) · **federated learning** (send gradients, not data) · data minimisation · purpose limitation & retention limits.

## 31. AI regulation — the spectrum *(self-study)*

| Region | Approach | Key point |
|---|---|---|
| **EU** | **risk-based, legally enforceable** | AI classified by risk; **unacceptable-risk prohibited**; high-risk faces strict requirements incl. **human oversight** |
| **UK** | pro-innovation, **sector-based** | **existing regulators**, no overarching AI law |
| **US** | **fragmented, state-led** | **no single federal AI law**; states legislate discrimination, deepfakes, hiring |
| **China** | **centralised & controlled** | covers algorithms, generative AI, deepfakes, **AI-content labelling** |
| **Japan** | agile, **largely voluntary** | voluntary governance; safety, fairness, privacy, security, transparency, accountability |
| **India** | governance-oriented, **evolving** | safe, inclusive, responsible AI adoption |

---

## ⭐ Exam triage — what to nail first

| Priority | Topic | Why |
|---|---|---|
| **1** | **4 deployment strategies** (Basic/Ramped/Blue-Green/Canary) | table + pros/cons + "which one and why" scenario |
| **2** | **MLOps vs LLMOps vs AgentOps** | a ready-made "compare these three" question |
| **3** | **Docker (file→image→container) + Containers vs VMs** | definitional, guaranteed marks |
| **4** | **Kubernetes architecture** (master vs worker components) | definitional, guaranteed marks |
| **5** | **RAGAS four metrics** | the deck's flagship modern topic |
| **6** | **Traditional vs ML testing** + the four test dimensions | classic compare question |
| **7** | **Precision / Recall / F1 / RMSE** + slicing | numerical or short-answer |
| **8** | **Explainability vs Interpretability vs Transparency** | three-way distinction, easy to confuse |
| **9** | **Security CIA + Authn/Non-repudiation/Authz** | six definitions with examples |
| **10** | **4 serving designs** + feature-encoding skew rule | scenario question |
| **11** | **Research vs Production**, **SOLID**, **refactoring** | compare / justify |
| **12** | **Big-O + data structure selection** | quick-answer marks |
| **13** | **Safety: robustness/monitoring/alignment** | three categories + the stop-sign and satisfaction examples |
| **14** | **Fairness (Amazon)** + versioning strategies | case-study recall |

### Answering scenario questions (the dominant format)
1. **Name the pattern/strategy** in the course's own words.
2. **Justify against the scenario's constraint** (cost / risk / latency / team size / regulation).
3. **State the trade-off you accept** — every choice in this course has one.
4. If the question says "discuss suitable use cases", give **one concrete example per option**, not a general description.
