# MLOps (AIMLC ZG523) — Study spec

> How to get ML models into production and keep them reliable: pipelines, registries, serving, monitoring, safe rollouts.
> **Status: in progress.** Topic 01 (whole lifecycle once) + codebase built; topics 02–08 planned below.

## 1. What it is and why an AI engineer should care
MLOps is DevOps adapted to systems whose behaviour depends on data and trained models, not just code. It covers
everything after the notebook: reproducible training pipelines, experiment tracking, model registries, packaging,
deployment patterns, serving, monitoring for drift and safe retraining and rollout. Almost every AI engineer job
description asks for it, and it builds directly on a full-stack background (APIs, CI/CD, containers).

**Job relevance: 5/5.** It's the most common gap between "built a model" and "shipped an AI product", and interviewers test it directly.

## 2. Sources in this folder

| Kind | File | Notes |
|------|------|-------|
| Handout (older batch, S2-25, v1.0) | `handouts/Older batch - MLOps (S2-25_AIMLCZG523) COURSE HANDOUT.docx` | 8 modules, 16 sessions, 5 labs, evaluation scheme |
| Slides (old batch) | `old-batch-slides/MLops - watermarked.pdf` | **Scanned images, no extractable text**: read visually |

**Gaps:** no past question papers, no lab notebooks. Textbooks named in the handout: T1 *Introducing MLOps* (Treveil, Dataiku),
T2 *Designing ML Systems* (Chip Huyen), T3 *Engineering MLOps*; R1 *Reliable ML* (SRE for ML), R4 *Practical MLOps*. T2 is the best single book for this course.

## 3. Running scenario
**DeliverEase**, a food-delivery app, shows "arrives in 34 min" at checkout. A gradient-boosting model predicts delivery
minutes from distance, items, kitchen prep time, rain and peak hour (synthetic data from `codebase/deliverease/data.py`).
v1 is trained in the dry season (MAE 2.6 min vs baseline 9.2). When the monsoon arrives, inputs drift (PSI 1.73 on rain)
and the relationship changes (rain costs more, roads are slower): v1 becomes 10.9 min wrong. The team must detect it,
retrain, prove the new model is better on the same fresh data and roll it out safely. Every module solves one step of this.

## 4. Module map (from the handout)

### M1 · MLOps Foundations (CS 1–3, ≈6 CH)
Topics: three levels of ML software, ML lifecycle and system architecture, AWS ML Lens, challenges, motivation, people of MLOps, AllTheOps (DataOps, ModelOps, AIOps), maturity models (Google, Microsoft).

| Concept | One-line definition | Analogy |
|---|---|---|
| MLOps | DevOps plus versioning, testing and monitoring of data and models | DevOps for programs shaped by data |
| Three levels of ML software | Data, model and code each need their own engineering | Three repos that must release together |
| Hidden technical debt | The model is a small box inside a large system of data and serving glue | Engine vs the whole car |
| Maturity levels | 0 manual → 1 automated pipeline (CT) → 2 CI/CD for pipelines | Hand release → scripted → release train |
| DataOps / ModelOps / AIOps | Ops for data pipelines / for model governance / ML applied to IT ops | Siblings with different focus |

Diagram ideas: hidden-debt box diagram · lifecycle loop · maturity ladder. **Scenario step:** decide DeliverEase needs more than a notebook.
**Notebook idea:** topic 01 cells 1–2 (data first, baseline). **Production angle:** "who owns the model in production" is the #1 org failure.

### M2 · Process and Tooling (CS 4–5, ≈4 CH)
Topics: MLOps lifecycle, process and capabilities; infrastructure (storage, compute); dev/prod environments and runtimes; ML platforms; tool landscape; Uber Michelangelo, Spotify TFX, Netflix.

| Concept | One-line definition | Analogy |
|---|---|---|
| ML platform | Shared internal tooling for data, training, registry, serving, monitoring | Internal PaaS for models |
| Dev vs prod environment | Same dependencies, different data/scale; drift between them breaks reproducibility | Works on my machine |
| Compute vs storage | Training needs bursty GPUs; data needs cheap durable storage | Build servers vs artifact store |
| Tool landscape | Best-of-breed tools per stage vs one managed platform | Microservices vs monolith |

Diagram ideas: tool-per-stage map · Michelangelo architecture redrawn simply. **Scenario step:** choose the DeliverEase stack.
**Notebook idea:** map each codebase file to the industry tool (table in `codebase/README.md`). **Production angle:** tool sprawl; buy vs build.

### M3 · Model Experimentation and Packaging (CS 6–7, ≈4 CH)
Topics: experimentation, model versioning, metadata, registry; packaging, file formats, serialization, containerization.

| Concept | One-line definition | Analogy |
|---|---|---|
| Experiment tracking | Record each run's params, data version, metrics, artifact | git log + test results for training |
| Model registry | Source of truth for versions and the Production stage | Container registry with a `production` tag |
| Metadata / lineage | Which data + code + params produced this model | Build provenance |
| Serialization formats | pickle/joblib, ONNX, TorchScript, SavedModel | Binary formats per runtime |
| Containerization | Ship the service with its dependencies as an image | Docker for any service |
| Training-serving skew | Production computes inputs differently from training | Chrome in test, old Safari in prod |

Diagram ideas: run → registry → stages · lineage graph · image vs mounted model. **Scenario step:** track runs, register v1, package the API.
**Notebook idea:** real MLflow tracking + registry replacing the stand-ins (`pip install mlflow`). **Production angle:** MLflow, W&B, DVC; breaks when models are copied by hand.

### M4 · Model Deployment & Orchestration (CS 8–9, ≈4 CH)
Topics: deployment myths, productionalization, requirements and challenges; deployment patterns (static / dynamic / streaming); orchestration with Apache Beam, Airflow, Kubeflow.

| Concept | One-line definition | Analogy |
|---|---|---|
| Static vs dynamic deployment | Model bundled with the app vs loaded/served separately and updatable | Compiled-in config vs remote config |
| Pipeline / DAG | Ordered steps with dependencies, run on a schedule or trigger | cron + dependency graph |
| Quality gate | Rules a model must pass before promotion | Branch protection |
| Champion vs challenger | Current vs candidate model, scored on the same fresh data | Same load test for both servers |

Diagram ideas: DAG of the pipeline · static vs dynamic deployment. **Scenario step:** automate DeliverEase training with a gate.
**Notebook idea:** port `pipeline.py` to an Airflow or Prefect DAG locally. **Production angle:** Airflow/Kubeflow/Prefect; breaks when the gate compares on different data.

### M5 · Model Serving (CS 10–12, ≈6 CH)
Topics: properties of a serving runtime; key questions (load, latency, location, hardware, execution, feature pipelines); serving architectures; batch vs online; model server / model-as-a-service; model API design; real-time serving; MLaaS; case studies Airbnb, Netflix, Booking.com.

| Concept | One-line definition | Analogy |
|---|---|---|
| Online serving | Answer each request live within a latency budget | REST API |
| Batch serving | Precompute predictions on a schedule, store, look up | Nightly report |
| Model API design | Validated typed inputs, versioned outputs, health endpoint | Any good API contract |
| Request-time features | Features fetched or computed at request time | DB lookups inside a request |
| MLaaS | Managed training and serving (SageMaker, Vertex, Azure ML) | PaaS |

Diagram ideas: batch vs online vs streaming · request path with latency budget. **Scenario step:** checkout ETA API + nightly batch.
**Notebook idea:** load-test `serve.py` (p50/p95 latency) and add a cache. **Production angle:** KServe, BentoML, SageMaker endpoints; breaks when feature lookup blows latency.

### M6 · Monitoring & Observability (CS 13–14, ≈4 CH)
Topics: causes of ML failures, model degradation, drift detection, feedback loops; production monitoring, observability, ML-specific metrics, monitoring toolbox.

| Concept | One-line definition | Analogy |
|---|---|---|
| Data drift | Input distributions change from training | New traffic from a new country |
| Concept drift | Input → output relationship changes | Same order, slower roads |
| PSI / KS test | Scores of how much a distribution moved | Diff between histograms |
| Feedback loop / delayed labels | True outcomes arrive late (or are shaped by the model itself) | Smoke detector before the fire report |
| Three monitoring layers | System (latency, errors), data (drift), model (accuracy) | Infra, app and business dashboards |

Diagram ideas: training vs live histograms · three-layer monitoring stack · label delay timeline. **Scenario step:** monsoon drift alert, MAE 2.6 → 10.9.
**Notebook idea:** Evidently report on dry vs monsoon data. **Production angle:** Evidently, Arize, Prometheus/Grafana; breaks when nobody owns the alert.

### M7 · Continual Learning and Testing (CS 15, ≈2 CH)
Topics: continual learning, stateless vs stateful training, stages, challenges, model upgrades; testing in production: offline vs online evaluation, shadow, A/B, canary, interleaving, bandits.

| Concept | One-line definition | Analogy |
|---|---|---|
| Stateless retraining | Retrain from scratch on a recent window | Full rebuild |
| Stateful training | Continue training on new data only | Incremental build |
| Shadow | New model logs answers on real traffic; users see the old one | Dark launch |
| Canary | Small user share gets the new model first | Staged app rollout |
| A/B test | Split users, compare a business metric statistically | Feature-flag experiment |
| Bandits | Shift traffic toward the better model automatically | Auto-scaling toward the winner |

Diagram ideas: rollout patterns grid · retrain trigger loop. **Scenario step:** retrain on monsoon data and roll out v2.
**Notebook idea:** simulate an A/B test with a significance test; an epsilon-greedy bandit (links to DRL MAB). **Production angle:** Argo Rollouts/Istio; breaks with random (non-sticky) routing.

### M8 · Trends in MLOps (CS 16, ≈2 CH)
Topics: model compression, ML in browsers and phones, ML on edge, continuous ML, federated learning.

| Concept | One-line definition | Analogy |
|---|---|---|
| Quantization / pruning / distillation | Smaller, faster models | Minify a JS bundle |
| On-device inference | Run the model in the browser/phone (ONNX Runtime Web, TFLite, Core ML) | Client-side rendering |
| Federated learning | Train across devices; only updates leave the device | Phones send diffs, not files |

Diagram ideas: cloud vs edge vs browser placement · federated round. **Scenario step:** ETA on the rider's phone offline.
**Notebook idea:** export the model to ONNX and compare size/latency. **Production angle:** overlaps ML-on-the-Edge; breaks on device fragmentation.

## 5. Codebase plan (`codebase/`, ✅ built for the first pass)

```
codebase/
├── deliverease/
│   ├── data.py        M1-M2  synthetic orders; monsoon = data + concept drift        ✅
│   ├── features.py    M3     one feature function + validation (no skew)            ✅
│   ├── tracking.py    M3     experiment tracker (MLflow stand-in)                   ✅
│   ├── registry.py    M3     model registry with stages                              ✅
│   ├── train.py       M3     train, baseline, log run                                ✅
│   ├── pipeline.py    M4     DAG + quality gate + champion vs challenger              ✅
│   ├── serve.py       M5     FastAPI /predict /health                                 ✅
│   ├── batch.py       M4-M5  batch scoring                                            ✅
│   ├── monitor.py     M6     PSI drift report + retrain trigger                       ✅
│   └── rollout.py     M7     shadow + canary router                                   ✅
├── tests/test_pipeline.py    15 tests (data, model gate, API, drift, rollout)         ✅
├── Dockerfile                M3 packaging                                             ✅
└── ci/github-actions-ci.yml  M2-M3 CI                                                 ✅
Later: mlflow_tracking.py (M3 deep), airflow_dag.py (M4 deep), loadtest.py (M5), evidently_report.py (M6), ab_test.py (M7), export_onnx.py (M8)
```

## 6. Practice topics plan
1. **01 MLOps Big Picture: notebook to monitored service** (all modules, pass 1, 4–5 h): ✅ built
2. 02 Foundations & tooling: lifecycle, roles, maturity, platform case studies (M1–M2, 3 h)
3. 03 Experiment tracking & registry with real MLflow (M3, 4 h)
4. 04 Packaging: serialization formats, containers, ONNX (M3, 3 h)
5. 05 Pipelines & orchestration: Airflow/Prefect DAG with the gate (M4, 4 h)
6. 06 Serving: API design, latency, batch vs online vs streaming (M5, 4 h)
7. 07 Monitoring & drift: PSI, KS, Evidently, delayed labels (M6, 4 h)
8. 08 Continual learning & testing in production: retraining, shadow/canary/A-B, bandits (M7, 4 h)
9. 09 Trends: compression, edge/browser, federated (M8, 2 h)

## 7. Exam signal
No past papers in this folder. Evaluation (older-batch handout): two take-home assignments 20% + 20%; mid-semester
(closed book, sessions 1–7 = M1–M4) 30%; comprehensive (open book, all sessions) 30%. The labs (MLflow pipeline,
metadata, microservice deployment, monitoring with Evidently, Azure ML) suggest assignments are hands-on.

## 8. Interview angle
1. *How do you take a model to production?* Pipeline → track → gate → registry → containerised API → monitor → retrain.
2. *Data vs concept drift?* Inputs change vs input→output rule changes; the second needs labels.
3. *How do you detect drift without labels?* Compare live vs training feature distributions (PSI, KS test).
4. *What's training-serving skew and how do you prevent it?* Different feature code paths; share one function or a feature store.
5. *Batch or online serving: how do you choose?* Is the user waiting? Are inputs known in advance? Latency/cost.
6. *Shadow vs canary vs A/B?* Log-only / small live share / split to compare a business metric.
7. *What's in a model registry and why?* Versions, lineage, stage; serving loads "Production", rollback = move the tag.
8. *How do you decide to retrain?* Schedule, drift alert, or performance drop; promote only if it beats the champion on the same fresh data.
9. *What do you monitor for an ML service?* Latency/errors, input drift, prediction distribution, accuracy once labels arrive.
10. *MLflow components?* Tracking, Projects, Models, Model Registry.

## 9. Repetition plan

| Concept | First met | Revisited in |
|---|---|---|
| Baseline | 01 (cell 2) | 03, 05 (gate), 08 |
| Training-serving skew | 01 (cell 3) | 04, 06, 07 |
| Experiment tracking | 01 (cell 4) | 03, 05 |
| Model registry & stages | 01 (cell 5) | 03, 05, 08 |
| Quality gate / champion-challenger | 01 (cells 5, 10) | 05, 08 |
| Batch vs online | 01 (cells 6–7) | 06 |
| Data vs concept drift, PSI | 01 (cells 8–9) | 07, 08 |
| Shadow / canary | 01 (cell 11) | 08 |

## 10. Overlap with my other courses
- [`../../software-engineering-for-machine-learning/materials/notes/`](../../software-engineering-for-machine-learning/materials/notes/): S2 (hidden debt), S6 (registry, batch vs real-time), S12 (testing ML), S13 (Docker/K8s), S14 (serving and deployment strategies). **Big overlap: review those first.**
- [`../../machine-learning-on-the-edge/`](../../machine-learning-on-the-edge/): M8 edge and compression.
- [`../../llm-engineering/`](../../llm-engineering/): LLMOps (serving, evaluation, cost) in the later LLM modules.
- [`../../deep-reinforcement-learning/`](../../deep-reinforcement-learning/): multi-armed bandits ↔ M7 bandit testing.

## 11. Build checklist
- [x] SPEC written
- [x] cards.json (27 cards: first pass, M1–M8)
- [x] practice/01 MLOps Big Picture (explainer, notebook, guide)
- [x] codebase/ runs + 15 tests
- [ ] practice/02 Foundations & tooling
- [ ] practice/03 Tracking & registry (MLflow)
- [ ] practice/04 Packaging
- [ ] practice/05 Pipelines & orchestration
- [ ] practice/06 Serving
- [ ] practice/07 Monitoring & drift
- [ ] practice/08 Continual learning & testing in production
- [ ] practice/09 Trends

**Total estimated study hours: ~32 h** (≈4–5 h per topic).
