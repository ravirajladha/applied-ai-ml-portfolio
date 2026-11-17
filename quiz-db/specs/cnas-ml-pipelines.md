# ML Pipelines & MLOps (S6-S7): coverage spec

**Ladder:** API-driven Cloud Native Solutions (AIMLCZG549) › ML Pipelines & MLOps (S6-S7)   ·   **Prerequisites:** cnas-data-pipelines (data pipelines, SEMMA, Prefect, CI); ml-what and ml-metrics for general ML; ops-monitoring for production monitoring in depth
**Why it matters for AI/ML:** Sessions 6-7 take a model from notebook to an API-driven pipeline: why ML is harder than software (data, model and code all change), the model workflow and ML life cycle, MLOps as the practice that makes it repeatable, MLflow for tracking, registry and serving (the course's Covid demo), and SageMaker (Canvas vs Studio) as the managed option. The handout frames it as API-driven ML pipelines for development/training, deployment, monitoring and scalability; the lab is an API-based ML pipeline with MLOps.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `ml-basics` | ML, ML complexity, the model and the model workflow | ML and 'model' in one line | data, model and code all change; the five workflow steps | why a code-only CI misses a data change | reproducing a model needs all three versions |
| 2 | `ml-generations` | Three generations of ML and transfer learning | the three generations | algorithms per generation; what transfer learning reuses | choosing a generation for a dataset; trainable parameters when fine-tuning a head | the slide's transformer table read critically |
| 3 | `ml-process-metrics` | ML types, the ML process and evaluation metrics | regression vs classification metrics | the process (primary and secondary models, more predictors, best model) | MAE, RMSE, R², adjusted R² and F1 by hand | lower-is-better vs higher-is-better selection traps |
| 4 | `ml-lifecycle` | The ML life cycle and SEMMA in ML | life-cycle stages | SEMMA mapped to the ML life cycle; Assess -> deploy the best model | what SEMMA does not cover (deployment, monitoring, retraining) | where the lifecycle loops back |
| 5 | `mlops` | MLOps: definition, why, lifecycle, components, tools landscape | MLOps in one line | why productionising ML is hard; the components | DevOps vs MLOps (CD4ML); tool-landscape categories | designing the minimum MLOps setup for a small team |
| 6 | `mlflow-tracking` | MLflow experiment tracking: experiments, runs, params, metrics, artifacts, system metrics | what MLflow is | params vs metrics vs artifacts; runs and experiments | metric history with steps; comparing runs; system metrics | immutable params, picking the best run, what system metrics really measure |
| 7 | `mlflow-registry` | MLflow models, artifacts, model registry and serving | the registry's purpose | MLmodel, conda.yaml, model.pkl, python_env.yaml, requirements.txt | stages vs aliases; models:/ URIs; REST serving | promotion and rollback design with aliases |
| 8 | `covid-demo` | The MLflow Covid demo and its metrics summary | the demo's four functions | reading the metrics summary | recomputing metrics from the confusion matrix | why the summary's equal P/R/F1 hides a 4% recall |
| 9 | `sagemaker` | Amazon SageMaker: Canvas vs Studio, Data Wrangler, AutoML, registry, endpoints | SageMaker as a managed MLOps platform | Canvas (no-code) vs Studio (IDE) | the Canvas flow select -> build -> analyze -> predict -> deploy; endpoints | MLflow vs SageMaker for a given team |
| 10 | `api-ml-pipelines` | API-driven ML pipelines: training, deployment, monitoring, scalability | serving a model behind a REST API | request/response payloads; training via API | autoscaling arithmetic, ₹ endpoint cost, monitoring hooks | retraining triggers and safe promotion through APIs |

## Must-know facts
- ML has three changing variables, data, model and code; plain software has only code (Fowler's CD4ML).
- A model is the trained algorithm that makes predictions; it is developed, deployed, monitored and maintained in an operational pipeline.
- Model workflow: development -> versioning -> deployment -> monitoring -> retraining.
- Three generations: Gen 1 basic ML (hand-engineered features, structured data: Naive Bayes, decision tree, random forest, SVM, KNN, logistic regression); Gen 2 deep learning (CNN for images/video, RNN and LSTM for sequences); Gen 3 transfer learning / transformers (pre-train on a data-rich task, fine-tune on a downstream task).
- Regression metrics: MAE, RMSE, R² / adjusted R². Classification metrics: confusion matrix, accuracy, precision, recall, F1.
- SEMMA in ML: Sample, Explore, Modify, Model (basic ML, deep learning, transfer learning), Assess (evaluate, then deploy the selected best model). It suits data analyst / data scientist roles and stops at deployment; MLOps covers what comes after.
- MLOps standardises and streamlines developing and deploying ML models across the whole workflow: data collection, development, training, deployment, model management.
- MLflow (open source, from Databricks): tracking, visualization, evaluation, models, model registry, serving, observability, generative AI support.
- Params are inputs set before training (logged once per run); metrics are numeric results that can be logged many times with a step; artifacts are files (model, plots, environment files).
- An MLflow model directory holds MLmodel (flavors and loading metadata), conda.yaml, python_env.yaml, requirements.txt and the serialized model (model.pkl for scikit-learn).
- The registry gives versioned models with stage transitions (None, Staging, Production, Archived); newer MLflow versions deprecate stages in favour of aliases such as @champion, loaded as models:/name@alias.
- `mlflow models serve` exposes a model as a REST API (POST /invocations with a JSON body such as dataframe_split).
- System metrics (CPU, memory, GPU, network, disk) describe the machine during the run, not the model's quality, and system memory % is for the whole machine.
- SageMaker Canvas is low-code/no-code for analysts; SageMaker Studio is a full ML IDE (notebooks, experiments, debugging, automatic tuning). Canvas flow: select dataset -> build -> analyze -> predict -> deploy to an endpoint; SageMaker Model Registry catalogs versions.

## Common traps (each one must have at least one question)
- Thinking CI on code alone catches every ML regression -> new data can break a model with no code change.
- Logging accuracy per epoch as a param -> metrics are numeric and have history; params are inputs.
- Treating the model file as the only artifact needed -> without the environment files you cannot reload it reliably.
- Reading the Covid summary's P = R = F1 = 0.785 as good positive-class performance -> with TP=2, FN=48, recall for the positive class is 4%.
- Assuming 'memory usage 94.3%' means the model used 94% of memory -> it is system-wide usage sampled during the run.
- Picking the model with the highest RMSE -> lower is better for error metrics.
- Expecting R² to always rise in a fair comparison when predictors are added -> adjusted R² penalises useless predictors.
- Believing SEMMA ends with a monitored production model -> SEMMA stops at assess/deploy; monitoring and retraining are MLOps.
- Hard-coding 'version 7' in the serving app -> use an alias or stage so promotion and rollback need no redeploy.
- Canvas vs Studio swapped -> Canvas is no-code; Studio is the IDE.
- Scaling an endpoint on average traffic -> size for peak with headroom.

## Interview angle
1. **"Why is MLOps harder than DevOps?"** Three things change, data, model and code; a model can degrade with no code change, so you version data and models, track experiments and monitor predictions, not just uptime.
2. **"Params vs metrics vs artifacts in MLflow?"** Params: inputs such as n_estimators. Metrics: numeric outcomes such as accuracy, can have a history. Artifacts: files such as the pickled model, plots, conda.yaml.
3. **"How do you promote a model safely?"** Register a new version, validate it, move the champion alias (or Production stage) to it; serving loads models:/name@champion, so rollback is moving the alias back.
4. **"Canvas or Studio?"** Canvas for analysts who need no-code AutoML predictions; Studio for engineers who need notebooks, experiments, tuning and pipelines.
5. **"What does an API-driven ML pipeline look like?"** Training jobs started through an API, models registered and served behind a REST endpoint, predictions and system metrics monitored, autoscaling on load, retraining triggered by monitoring.

## Source material
- Slides (old batch, p147-189): ML definition; ML complexity (data, model, code vs code only, from Fowler's CD4ML); model definition; the five-step model workflow (development, versioning, deployment, monitoring, retraining).
- Slides: three generations of ML with algorithm lists; transfer learning definition; a table of transformer models (encoder sizes, pre-training corpora, tasks). Questions describe these models generically rather than by name.
- Slides: ML types (image), the ML process (primary and secondary models, more predictors, best model), regression and classification evaluation metrics; the ML life cycle (image); SEMMA for ML (Model covers basic ML, deep learning and transfer learning; Assess ends with deploying the best model; ideal for data analyst and data scientist roles) and the Covid discharge case. SEMMA is tested here only as it maps to the ML life cycle; cnas-data-pipelines covers it as a data-science process.
- Slides: MLOps definition, why MLOps is important (Databricks; Hidden Technical Debt), the MLOps lifecycle, components and tools landscape (images).
- Slides: MLflow components (experiment tracking, visualization, generative AI, observability, evaluation, models, model registry, serving); the Covid demo (main -> preprocess_data -> train_model -> evaluate_model -> log_to_mlflow); the metrics summary; the model artifacts; the system-metric names.
- Slides: SageMaker as an MLOps platform; Canvas vs Studio; the demo with Data Wrangler, the Pima Indians diabetes dataset, AutoML, select -> build -> analyze -> predict -> deploy, and SageMaker Model Registry.
- Handout (S6-S7): API-driven ML pipelines for model development and training, deployment, monitoring and scalability; MLOps practices; lab: API-based ML pipeline with MLOps.
- No past papers; scenario style modelled on BITS WILP papers (Bengaluru food delivery, Pune smart city, agritech cooperative, ₹ costs, by-hand computations).
- **Standard practice (slides thin or image-only):** the MLOps lifecycle and component list (Databricks glossary: EDA, data prep and feature engineering, training and tuning, review and governance, inference and serving, monitoring, automated retraining), tool-landscape categories, MLflow param immutability, metric steps, experiment/run structure, registry aliases vs deprecated stages, models:/ URIs and the /invocations REST payload (MLflow documentation), SageMaker endpoints, and the whole api-ml-pipelines topic (autoscaling, payloads, retraining triggers). Snippets simulate the tracker and registry with dicts; nothing imports mlflow.
- **Course-material notes:** (1) the Covid metrics summary is internally inconsistent: TP=2, TN=192, FP=1, FN=48 gives accuracy 194/243 = 0.798, not 0.785, and positive-class precision 0.667, recall 0.04, F1 about 0.08; precision = recall = F1 = accuracy only happens with micro-averaging, so the summary hides that the model finds almost no positives. (2) The summary's "the model used 94.3% of the system's memory" and "22.4% CPU" are system-wide readings sampled during the run, not the model's own usage. (3) The transformer table's base-encoder row, "12 encoder & 768 hidden layers", means 12 encoder layers with a hidden size of 768 (and 24 layers / 1024 for Large), not 768 layers. (4) MLflow model-registry stages are deprecated since MLflow 2.9 in favour of aliases and tags; questions teach both.
