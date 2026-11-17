# Data Science & DataOps Pipelines (S4-S5): coverage spec

**Ladder:** API-driven Cloud Native Solutions (AIMLCZG549) › Data Science & DataOps Pipelines (S4-S5)   ·   **Prerequisites:** cnas-apis (REST, JSON), cnas-cloudnative (DevOps, CI/CD); ml-data for general data preparation
**Why it matters for AI/ML:** Every model sits on a data pipeline. Sessions 4-5 build an API-driven, cloud-native data pipeline: the big data Vs that make it hard, the data science process that structures the work (Big Data Analytics Life Cycle, SEMMA, CRISP-DM), DataOps as DevOps applied to data, Prefect as the orchestrator (flows, tasks, retries, caching, deployments, Prefect Cloud REST API) and GitHub Actions as the CI that triggers it. Lab: an API-based data pipeline with DataOps.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `big-data-vs` | Characteristics of big data (the 5 Vs) | name the five Vs | match a scenario to the V; velocity drives volume | size a sensor stream by hand; veracity and provenance | value vs aggregation trade-off (raw vs aggregated IoT readings) |
| 2 | `ds-foundations` | Data science definitions, supporting technologies, hierarchy of needs | data science as the study of data, storytelling | the four supporting technologies; DS/AI/ML convergence | hierarchy of needs: why AI sits on top of collect/store/clean | hidden technical debt: ML code is a small box |
| 3 | `ds-process` | Data science methodologies (CRISP-DM, DASC-PM, BDA life cycle, SEMMA) | the four methodologies the slides list | CRISP-DM's six phases | SEMMA vs CRISP-DM: what SEMMA leaves out | picking a methodology for a project |
| 4 | `bda-lifecycle` | Big Data Analytics Life Cycle and the cardiac-surgery case study | the nine stages in order | what each stage does in the case study | which role owns a stage; acquisition vs extraction vs cleansing | spotting a stage done in the wrong order (leakage, utilisation before validation) |
| 5 | `semma` | SEMMA as a data-science process and the Covid discharge case | expand the acronym | what happens in each step | classify activities (PCA, partitioning, correlation) into steps | the slide's Covid mapping vs the standard SEMMA mapping |
| 6 | `dataops` | DataOps: need, challenges, definition, architecture, automation, tools | DataOps in one line | DataKitchen's formula; DevOps concepts reused | why data is harder than code; canonical and functional architecture; automated data tests | designing DataOps checks for a pipeline; tool choice |
| 7 | `pipeline-stages` | Pipeline stages: ingestion, (pre)processing, storage, integration, monitoring and alerting, scalability and reliability | name the stages | batch vs streaming ingestion; storage choices | idempotent ingestion, freshness alerts, chunking | reliability design: retries plus idempotency, backfills |
| 8 | `prefect-core` | Prefect: flows, tasks, architecture, folder structure | @flow and @task | flow vs task vs run; local server vs Prefect Cloud | the architecture (account, workspace, API key, deployment, schedule, runs); hybrid model | one deployment and one main flow for the DS project |
| 9 | `prefect-ops` | Prefect retries, caching, deployments, REST API | what a retry is | retries and retry_delay_seconds; caching by inputs | retry timing and cache expiry by hand; deployment run naming | retry vs non-idempotent side effects; reading run states from the REST API |
| 10 | `github-actions` | CI with GitHub Actions | what GitHub Actions is | workflow, event, job, runner, step, action | the main.yaml triggers, secrets, job ordering with needs | flaws in a workflow (secrets in plain text, wrong trigger, jobs not sharing files) |

## Must-know facts
- The five Vs: Volume (too big for one machine), Velocity (how fast it is generated), Variety (structured, semi-structured, unstructured), Veracity (accuracy, provenance, noise), Value (usefulness, tied to veracity and sometimes to speed of processing).
- High velocity makes volume pile up in a short time.
- Supporting technologies for data science: powerful algorithms (transformers), open-source tools (Python), cloud computing (speed, accuracy, cost) and cheap storage.
- The data science hierarchy of needs: collect -> move/store -> explore/transform -> aggregate/label -> learn/optimize. AI is the top of a pyramid that needs reliable data plumbing first.
- The slides list four methodologies: CRISP-DM, DASC-PM, the Big Data Analytics Life Cycle and SEMMA (for ML projects).
- Big Data Analytics Life Cycle: business case evaluation -> data identification -> data acquisition and filtering -> data extraction -> data validation and cleansing -> data aggregation and representation -> data analysis -> data visualization -> utilization of analysis results.
- SEMMA (SAS): Sample, Explore, Modify, Model, Assess. It covers model development only; it has no business-understanding or deployment phase (CRISP-DM has both).
- DataOps = Agile practices + Lean thinking + Data analytics + DevOps (DataKitchen). It reuses Git, CI, CD, monitoring/logging and a culture of collaboration.
- DataOps automation orchestrates, tests and monitors the pipeline: check data for anomalies, notify on test failures, show metrics on a dashboard.
- Tools: Apache Airflow, Prefect (+ Prefect Cloud), Dagster (open source); DataKitchen, Unravel (commercial).
- Prefect turns Python functions into a flow (@flow) made of tasks (@task). Each execution is a flow run / task run. A deployment adds a schedule or trigger to a flow and is run as 'flow-name/deployment-name'.
- Prefect Cloud keeps the metadata (runs, states, logs, schedules) in an account and workspace reached with an API key; your code and data run on your own infrastructure. `prefect server start` runs the same API locally.
- Retries: `@task(retries=3, retry_delay_seconds=10)` re-runs a failed task; a list of delays gives a custom backoff. Retrying is only safe if the task is idempotent.
- Caching: a cache key (for example from the task inputs) lets a later call reuse the stored result instead of running again, until the cache expires.
- GitHub Actions: a workflow (.github/workflows/*.yml) is triggered by events (push, pull_request, schedule, webhook); it has jobs; each job runs on a runner (a fresh GitHub-hosted VM) and has steps; a step is a shell command (run) or an action (uses).
- Jobs run in parallel by default and do not share a file system; `needs:` orders them. Secrets go in `${{ secrets.NAME }}`, never in the YAML.

## Common traps (each one must have at least one question)
- Veracity confused with variety -> veracity is accuracy and trust, variety is the forms of data.
- Treating volume and velocity as unrelated -> high velocity is what makes volume explode.
- Thinking SEMMA covers the whole project -> it has no business understanding and no deployment phase.
- Doing feature selection or scaling on the whole dataset before Sample's train/test partition -> leakage.
- Data acquisition vs extraction mixed up -> acquisition gathers and filters records, extraction pulls the needed fields.
- Assuming data can be CI/CD'd exactly like code -> data changes without a commit, environments are hard to reproduce, exploration is iterative.
- Believing a retry is always safe -> a non-idempotent task (send SMS, insert row) repeats its side effect.
- Expecting a cached task to see new source data -> the cache key ignores what it does not hash.
- Thinking Prefect Cloud runs your code -> it orchestrates and stores metadata; your worker or process runs the code.
- Assuming two jobs in a workflow share files -> each job gets a fresh runner; use artifacts or put steps in one job.
- Hard-coding the Prefect API key in main.yaml -> use repository secrets.
- Believing `on: push` with `branches: [main]` runs for a push to a feature branch -> it does not.

## Interview angle
1. **"What is DataOps and how is it different from DevOps?"** DevOps applied to data pipelines, plus Agile, Lean and analytics. The extra difficulty is that data changes on its own: you test the data at every stage, not only the code.
2. **"Why use an orchestrator like Prefect instead of cron + scripts?"** Retries, caching, logging, state tracking, schedules, a UI and an API for runs; a failing step is visible and re-runnable instead of a silent cron failure.
3. **"How do you make a pipeline reliable?"** Idempotent tasks (upserts, dedupe keys), retries with backoff, data tests between stages, freshness and volume alerts, and the ability to backfill.
4. **"SEMMA vs CRISP-DM?"** SEMMA is the model-building core (sample, explore, modify, model, assess); CRISP-DM wraps it with business understanding and deployment.
5. **"How would CI trigger a data pipeline?"** A GitHub Actions workflow on push to main installs dependencies, logs in to Prefect Cloud with a secret API key and runs the deployment.

## Source material
- Slides (old batch, p98-146): the five Vs with the IoT air-pollution aggregation example; data science definitions (study of data, storytelling, all aspects from collection to insight); supporting technologies; the DS/AI/ML convergence and key-takeaway slides including "Hidden Technical Debt in ML Systems"; the data science hierarchy of needs (image only).
- Slides: the four methodologies (CRISP-DM, DASC-PM, Big Data Analytics Life Cycle, SEMMA); the nine-stage Big Data Analytics Life Cycle and the case study "Predicting Patient Survival After Cardiac Surgery" with each stage's objective, activities and role.
- Slides: SEMMA steps and the Covid patient discharge case (1,233 patients, 2nd wave Apr-Jun 2021; univariate/bivariate exploration with Pearson and chi-square; PCA; seven X variables; seven classifiers; Random Forest best at 92%).
- Slides: need for DataOps, data teams' challenges and bottlenecks, the DataKitchen definition, the DevOps concepts reused, the canonical and functional architectures (images), automation, tools.
- Slides: Prefect (Python-only orchestration, local server vs Prefect Cloud, architecture: account ID, workspace ID, API key, deployment, schedule/trigger, flow, tasks, runs), the DS project as one deployment with one main flow and tasks (ingestion, pre-processing, EDA, analysis, visualization), the folder structure, the Prefect Cloud REST API (deployment and flow details); GitHub Actions concepts and the course's main.yaml.
- Handout (S4-S5): API-driven cloud-native data pipeline with ingestion, (pre)processing, storage, integration, monitoring and alerting, scalability and reliability; lab: API-based data pipeline with DataOps.
- No past papers; scenario style modelled on BITS WILP papers (Bengaluru food delivery, Pune smart-city, agritech cooperative, ₹ costs, by-hand computations).
- **Standard practice (slides thin or image-only):** the hierarchy of needs levels (Rogati), CRISP-DM phases, the canonical/functional DataOps architecture (DataKitchen: production and development pipelines, automated tests at each stage), the pipeline-stage questions (batch vs streaming, idempotent ingestion, freshness alerts, backfills), Prefect retries/caching/deployments/states/hybrid model and GitHub Actions job isolation, `needs`, secrets and triggers (Prefect and GitHub documentation). Snippets simulate Prefect behaviour in plain Python; nothing imports prefect.
- **Course-material notes:** the Covid SEMMA slide puts "Feature Engineering, Subset selection" under Model; in standard SEMMA, creating and selecting variables is Modify (the slide's own Modify definition says so). The GitHub Actions slide says "each job runs inside a container"; on GitHub-hosted runners a job runs directly on a fresh VM unless the job sets `container:`. The main.yaml's `prefect deployment run ... --workspace-key` flag is not a documented Prefect CLI option; the workspace is selected at `prefect cloud login`. The YAML also uses old action versions (checkout@v2, setup-python@v2).
