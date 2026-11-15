# E-commerce Session Conversion Prediction

> **AIMLCZG546 · Software Engineering for Machine Learning · Assignment II · Group 049**

Predicts the probability that a live browsing session ends in a purchase, so the store can
offer help to high-intent shoppers and leave everyone else alone.

The model is small on purpose. This assignment is graded on **code quality and testing**,
so the interesting parts are the module boundaries, the logging, the API contract and the
61 tests — not the logistic regression.

---

## Start here

| If you want to… | Open |
| --- | --- |
| Understand the whole build, step by step, from scratch | **[`JOURNEY.md`](JOURNEY.md)** |
| See all 9 assignment requirements answered with live output | **[`049.ipynb`](049.ipynb)** |
| See what the code looked like *before* it was cleaned up | [`research/research_prototype.ipynb`](research/research_prototype.ipynb) |
| Answer the few things only the group can decide | [`QUESTIONS.md`](QUESTIONS.md) |
| Read the actual code | `ecom/` |

New to Python or ML? Read `JOURNEY.md` first — every term is explained.

---

## Quick start

```bash
pip install -r requirements.txt

python -m ecom.data_ingestion   # 1. build the demo dataset      -> data/
python -m ecom.train            # 2. train + evaluate + save     -> artifacts/
python -m ecom.monitor          # 3. data quality + drift check  -> reports/
python -m pytest                # 4. run all 61 tests
uvicorn ecom.api:app --reload   # 5. serve at http://127.0.0.1:8000/docs
```

---

## What it does

**Input** — what a shopper has done so far in this visit:

```json
{
  "session_id": "s000123",
  "pages_viewed": 12,
  "session_duration_min": 8.5,
  "cart_items": 2,
  "avg_item_price": 799.0,
  "is_returning_user": 1,
  "discount_applied": 0,
  "device": "mobile"
}
```

**Output** — a calibrated probability plus an actionable band:

```json
{
  "session_id": "s000123",
  "conversion_probability": 0.9025,
  "will_convert": true,
  "intent_band": "high",
  "model_version": "1.0.0"
}
```

`high` (≥ 0.60) → offer live chat · `medium` (0.25–0.60) → small nudge · `low` → leave alone.

---

## Layout

```
assignment-2/
├── 049.ipynb              the submission notebook (all 9 tasks, executed)
├── JOURNEY.md             how this was built, for a complete beginner
├── QUESTIONS.md           open decisions for the group (names, group id, upload format)
├── 049_report.html        notebook exported to HTML -> print to PDF for Taxila
├── ecom/                  PRODUCTION package
│   ├── config.py            paths, data contract, thresholds
│   ├── logging_setup.py     one logging config for everything
│   ├── exceptions.py        typed errors
│   ├── data_ingestion.py    dataset generation + CSV loading      (OOP)
│   ├── data_validation.py   schema / missing / drift checks       (OOP)
│   ├── features.py          feature engineering                   (functional)
│   ├── train.py             training pipeline + artifact          (OOP)
│   ├── metrics.py           model quality scorecard               (functional)
│   ├── predict.py           inference wrapper                     (OOP)
│   ├── monitor.py           scheduled data quality check
│   ├── schemas.py           API request/response contracts
│   └── api.py               FastAPI service
├── research/              RESEARCH code, kept as the "before" exhibit — do not fix
├── tests/                 61 pytest tests across 6 files
├── reports/               lint reports, test report, data quality report
├── artifacts/             model.joblib, metrics.json
└── data/                  generated CSVs
```

---

## The API

| Endpoint | Method | Purpose | Status codes |
| --- | --- | --- | --- |
| `/health` | GET | Liveness — reports `degraded` rather than failing | `200` always |
| `/model-info` | GET | Version and expected features | `200`, `503` |
| `/metrics` | GET | Last training scorecard | `200`, `404` |
| `/predict` | POST | Score one session | `200`, `422`, `503` |
| `/predict/batch` | POST | Score up to 100 sessions | `200`, `422`, `503` |

Interactive docs are generated from the code at `/docs`.

---

## Results

**Model quality** (1,000 held-out sessions)

| Metric | Value |
| --- | --- |
| Accuracy | 0.716 |
| F1 | 0.683 |
| ROC-AUC | 0.781 |
| Brier score (calibration) | 0.190 |

Calibration — when it says 70%, ~72% really convert:

| Predicted | Sessions | We said | Reality |
| --- | --- | --- | --- |
| 0.0 – 0.2 | 197 | 13% | 16% |
| 0.2 – 0.4 | 263 | 30% | 27% |
| 0.4 – 0.6 | 222 | 50% | 55% |
| 0.6 – 0.8 | 200 | 70% | 72% |
| 0.8 – 1.0 | 118 | 88% | 81% |

**Data quality** — schema conformance `1.0`, max missing rate `1.0%`, and drift caught on
the simulated live feed (`pages_viewed` PSI **1.69**, `session_duration_min` PSI **0.83**).

**Quality gate** — 61 tests passing; flake8, black and isort all clean on `ecom/` and
`tests/` (see `reports/`).

---

## Requirement map

| # | Requirement | Where |
| --- | --- | --- |
| 1 | OOP / functional modular design | `ecom/` — 11 modules |
| 2 | Research vs production code | `research/` vs `ecom/` |
| 3 | Error handling + logging (≥3 modules) | 5 modules, INFO/WARNING/ERROR |
| 4 | black / flake8 / isort before–after | `reports/lint_before.txt`, `lint_after.txt` |
| 5 | REST API | `ecom/api.py`, `ecom/schemas.py` |
| 6 | ≥2 test types | 3 types: data validation, unit, integration |
| 7a | Model training tests | `tests/test_training.py` |
| 7b | Model inference tests | `tests/test_inference.py` |
| 8a | ≥2 model quality metrics | 4 + calibration table |
| 8b | ≥2 data quality metrics | schema, missing rate, PSI drift |
| 9 | Production testing + security | `049.ipynb`, Task 9 |
