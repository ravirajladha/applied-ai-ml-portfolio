# Webinar 1 — ML Systems: From Notebook to Production

> **Companion:** `friend notes/2.pdf` · (webinar — no slide deck in this set)
>
> **One-line goal:** grow a 30-line notebook into a real service — the **90% that isn't ML code**.

### Contents
1. [The 90% that isn't ML code](#1-the-90-that-isnt-ml-code)
2. [What's missing from the notebook?](#2-whats-missing-from-the-notebook)
3. [Seven layers from notebook to service](#3-seven-layers-from-notebook-to-service)
4. [The pipe-and-filter prediction pipeline](#4-the-pipe-and-filter-prediction-pipeline)
5. [Recap](#-recap)

---

## 1. The 90% that isn't ML code

**Sculley et al. (2015)** again: in a real ML system the **ML code box is tiny**, surrounded by config, data collection, feature extraction, process management, serving, and monitoring. The model is the easy **10%**; the engineering around it is the **90%** that decides whether the system survives production.

> 🌍 A trained model is an **engine on a workbench**. A car also needs a chassis, fuel system, dashboard, brakes, and a way for a driver to call it. This webinar takes a 30-line notebook (the engine) and bolts on those missing parts one at a time.

---

## 2. What's missing from the notebook?

The honest starting point: read a CSV, fit a `RandomForestClassifier`, dump `model.pkl`. It works — and it's **unshippable**.

| Missing | Consequence |
|---------|-------------|
| Schema validation | Bad inputs become silent garbage predictions |
| Error handling | Crashes at 2 a.m. with no trace |
| Logging | Impossible to debug in production |
| Hardcoded paths | Breaks on any other machine |
| Model versioning | "Which `.pkl` is in production?" |
| Serving | Nobody else can actually call the model |

> ⚠️ **"It works in the notebook" ≠ "it works in production."** Every missing item is invisible until something breaks — then it breaks *expensively*. The fixes are exactly the **quality attributes** from Sessions 4–6 made concrete in code.

---

## 3. Seven layers from notebook to service

Each layer maps to a box in the Sculley diagram:

| Step | Layer (tool) | Sculley box |
|:----:|--------------|-------------|
| 1 | the notebook (model only) | ML code |
| 2 | **MLflow** experiment tracking | model versioning |
| 3 | **FastAPI** inference service | serving infrastructure |
| 4 | **Pydantic** schema validation | data validation |
| 5 | structured (JSON) logging | monitoring & logging |
| 6 | config management | configuration |
| 7 | **pytest** quality-attribute tests | testing |

> 🧪 **Four lines turn a notebook into a tracked experiment.** The training logic is *identical*; only the instrumentation changes. Wrapping `fit` in `mlflow.start_run()` and adding `log_params`, `log_metrics`, `log_model` buys a named experiment bucket, recorded hyperparameters, tracked metrics, and a **versioned model artifact**. "Which `.pkl` is live?" now has an answer.

> 🧪 **Validation + serving as a contract.** Pydantic (`schemas.py`) is the input contract: `amount: float = Field(..., gt=0)`, `hour_of_day: int = Field(..., ge=0, le=23)`. FastAPI (`main.py`) exposes `POST /predict`. Send `amount: -500, hour_of_day: 99` → Pydantic **rejects it with field-level errors before the model ever sees it** — bad inputs can no longer become silent garbage.

---

## 4. The pipe-and-filter prediction pipeline

The prediction path is a clean **pipe-and-filter** (Session 4): four *pure functions*, each testable and swappable independently.

```
validate_input → extract_features → run_model → format_response
 (robustness)      (data prep)      (prediction)   (insight)
```

> 💡 Because each stage is a pure function, you can unit-test it in isolation and replace one (a new feature extractor, a new model) without touching the others — the pipe-and-filter pattern in a dozen lines of Python.

> 🧪 **Tests grouped by quality attribute.** pytest tests organised by the quality they defend: `TestRobustness` (schema rejects `amount=-500`), `TestReliability` (all outputs well-formed), `TestPerformance` (latency < 200 ms), `TestMaintainability` (each stage isolated). Running them — **15 tests in ≈ 2.6 s** — turns abstract quality attributes into a concrete, automated gate.

---

## 🎯 Recap

> A production ML system is mostly **not the model**. Starting from a notebook, the **seven layers** — tracking (MLflow), serving (FastAPI), validation (Pydantic), logging, config, and quality-attribute tests — fill in the Sculley diagram, turning "it runs on my laptop" into a service others can **call, debug, version, and trust**.

➡️ **Next:** [Webinar 2 — CI/CD with GitHub Actions & DVC](Webinar-2-CICD-GitHub-Actions-and-DVC.md) (automate the quality gate + version the data).
