# DeliverEase ETA — a small end-to-end MLOps codebase

**The scenario:** DeliverEase is a food-delivery app. When a customer orders, the app shows "arrives in 34 min".
That number comes from a model. This codebase is everything *around* the model that keeps that number trustworthy
every day: a reproducible pipeline, a registry, an API, monitoring and safe rollouts.

```
 make_orders ──► build_features ──► train ──► Tracker (runs/) ──► quality_gate ──► Registry (registry/)
  data.py          features.py       train.py   tracking.py        pipeline.py       registry.py
                       ▲                                                                  │ Production model
                       │ same function = no training-serving skew                          ▼
                       └──────────────────────────────── serve.py (FastAPI /predict) · batch.py (nightly CSV)
                                                                  │ prediction log
                                                                  ▼
                                    monitor.py (PSI drift, live MAE) ──► should_retrain? ──► pipeline again
                                    rollout.py (shadow / canary) for the new version
```

## Run it

```bash
cd other-electives/mlops/codebase
pip install -r requirements.txt            # all of these are already in the local Anaconda install
pytest -q                                   # 14 tests: data, features, quality gate, API, drift, rollout
python -m deliverease.pipeline              # trains, gates, registers -> creates mlops_workdir/
uvicorn deliverease.serve:create_app --factory --reload   # then open http://127.0.0.1:8000/docs
```

## Which module added which file

| File | Module | Concept it makes real |
|------|--------|----------------------|
| `deliverease/data.py` | M1–M2 | Data source; `monsoon=True` creates real-world change (drift) |
| `deliverease/features.py` | M3 | One feature function for training *and* serving; input validation |
| `deliverease/tracking.py` | M3 | Experiment tracking (MLflow stand-in) |
| `deliverease/registry.py` | M3 | Model registry with stages (MLflow Registry stand-in) |
| `deliverease/train.py` | M3 | Train + evaluate against a baseline + log the run |
| `Dockerfile` | M3 | Packaging the service as a container |
| `deliverease/pipeline.py` | M4 | The pipeline (DAG) and the **quality gate** |
| `deliverease/batch.py` | M4–M5 | Batch (offline) prediction |
| `deliverease/serve.py` | M5 | Online serving: REST API, validation, model version in every response |
| `deliverease/monitor.py` | M6 | Data drift (PSI), retrain trigger |
| `deliverease/rollout.py` | M7 | Shadow and canary deployment |
| `ci/github-actions-ci.yml` | M2–M3 | CI: tests incl. the model quality gate on every push |
| `tests/test_pipeline.py` | all | Code tests + data tests + model tests |

## Stand-ins vs. the real tools

| Here | In industry |
|------|-------------|
| `Tracker` (JSON files) | MLflow Tracking, Weights & Biases, Neptune |
| `Registry` (folder + index.json) | MLflow Model Registry, SageMaker / Azure ML registries |
| `run_pipeline()` | Airflow, Kubeflow Pipelines, Prefect, Dagster |
| `serve.py` (FastAPI) | FastAPI / BentoML / KServe / SageMaker endpoints |
| `monitor.py` (PSI) | Evidently, Arize, WhyLabs; Prometheus + Grafana for latency/errors |
| `rollout.py` | Istio / Argo Rollouts / SageMaker shadow & canary |
| local folders | S3 / GCS / Azure Blob, a feature store (Feast) |
