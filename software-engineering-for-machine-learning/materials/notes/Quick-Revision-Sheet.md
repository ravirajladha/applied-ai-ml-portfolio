# Quick Revision Sheet — SE4ML on one page

> Source: `SE4ML-One-Sheet.pdf` companion, expanded slightly. For the night before the exam.

## SE vs ML (the fault line)

| | Software Engineering | Machine Learning |
|---|---|---|
| Logic comes from | a programmer writing **rules** | **data** teaching the rules |
| Nature | **deterministic**, spec-driven | **inductive / probabilistic**, data-driven |
| Correctness | **binary** (right / bug) | **statistical** (metrics) that **decays** with data drift |
| Moving parts | code | **data + model + code** (3×) |

Roles ML adds on top of SE: **data engineer, data scientist, ML engineer, MLOps**.

## Hidden technical debt (Sculley et al.)

> The ML model is a **small box**; most of a real system is data collection & verification, feature extraction, configuration, serving, and **monitoring**. Optimise the **end-to-end product** (latency, reliability, monitoring) — not just offline accuracy.

## Requirements & quality

- **When to use ML** (Hulten): logic is complex / changing, patterns are learnable, and **mistakes are tolerable**.
- **Goal hierarchy:** organisational → product → user → model.
- **Quality attributes:** robustness, explainability, fairness, privacy, security, scalability, latency, reproducibility, drift-adaptability.

## Architecture patterns

- **Pipe-and-filter** — independent, testable stages.
- **Microservices** — scale & deploy independently.
- **Event-driven** — loose coupling via events / queues.
- **CQRS** — split writes (commands) from reads (queries).
- **RAG** — retrieve relevant docs, then generate grounded answers.
- **ML design patterns:** feature store, **model registry**, **batch vs online serving**, shadow / canary deploys.

## MLOps & CI/CD

- **CI:** build + test on every change (build server + runners).
- **Git** versions *code*; **DVC** versions *data & models* (md5 `.dvc` pointer + remote store); **MLflow** tracks *experiments, params, metrics* + a model registry.
- **Git + DVC + MLflow = full reproducibility.**

## Metrics (memorise)

$$\text{Precision}=\frac{TP}{TP+FP}\qquad \text{Recall}=\frac{TP}{TP+FN}\qquad F1=\frac{2PR}{P+R}$$

- **Precision** — of what I *flagged*, how much was right? (cost of false alarms)
- **Recall** — of what I *should have caught*, how much did I? (cost of misses)
- **F1** — harmonic mean, balances the two.

## Agentic AI

Agentic AI = **plan + tool-use + memory**; a reasoning loop that calls specialised models/tools.
Equation: **Generative AI + Reasoning + Tools + Feedback loops → Agentic AI**.
Coordinate many agents with **SAGA** (compensating transactions) and **Blackboard** (shared state + controller).

## Good code (Session 9)

**5 features:** Simplicity (DRY) · Modularity · Readability (PEP 8 + pylint) · Performance · Robustness.
**Profiling ladder:** `time` → `timeit`/`%%timeit` → `cProfile` (which *function*) → `line_profiler` (which *line*) → `memory_profiler`/`memray` (memory).

---

### ⭐ High-weightage exam topics
SE vs ML · hidden technical debt · quality attributes · architecture patterns · CI/CD, DVC, MLflow · precision / recall / F1.
