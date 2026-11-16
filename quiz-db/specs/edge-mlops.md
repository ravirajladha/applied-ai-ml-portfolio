# Edge MLOps & Management (M5, S9-S10): coverage spec

**Ladder:** Machine Learning on the Edge (AIMLCZG535) › Module 5 Edge MLOps & Management   ·   **Prerequisites:** edge-deployment (runtimes, containers, Greengrass / Azure IoT Edge), ops-monitoring (general drift statistics), ops-serving (general shadow / canary serving)
**Why it matters for AI/ML:** A model on 5,000 devices you cannot SSH into is a fleet-management problem, not a notebook. Module 5 covers how edge models are built, registered, shipped over the air, watched for drift on the device and improved from field feedback. The end-sem papers test it with a by-hand PSI on a gateway's confidence distribution, its classification against the 0.1 / 0.25 thresholds, and what the month-to-month trend says.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `edge-mlops-arch` | Edge MLOps pipeline and architecture | what edge MLOps adds to MLOps, the loop | cloud control plane vs device data plane, heterogeneous fleet | why the loop is slower and partial at the edge (connectivity, no labels) | designing the loop for an offline-first fleet |
| 2 | `orchestration` | Lightweight deployment orchestration | fleet, device group, desired state | device twin / shadow, pull vs push, K3s / KubeEdge | rollout waves by device group, reconciling offline devices | footprint vs control trade-offs for MCU vs gateway tiers |
| 3 | `cicd` | CI/CD workflows for edge models | what CI and CD mean for a model | pipeline stages: train, convert, quantize, test, package | per-target build matrix, accuracy and size/latency gates, hardware-in-the-loop | gate design, what blocks a release, reproducibility |
| 4 | `registry-versioning` | Model registry and model versioning | what a registry stores | versions, stages, metadata (target, precision, runtime) | model-preprocessing-runtime compatibility, semantic versioning | lineage and audit for a fleet running mixed versions |
| 5 | `monitoring-logging` | On-device monitoring and logging | what to log on a device | latency, confidence, input stats; summaries not raw data | confidence-distribution monitoring without labels, log budgets | silent failures, what a gateway can and cannot detect |
| 6 | `drift-psi` | Drift detection with PSI | what drift is, PSI name | PSI formula and the 0.1 / 0.25 bands | the papers' four-bin by-hand PSI, the dominant term | trend across months, binning and zero bins, what PSI cannot say |
| 7 | `ota-updates` | Over-the-air (OTA) updates | what OTA is | A/B partitions, rollback, signed images | delta updates and bandwidth/cost sums, staged rollouts | bricking risks, health checks, atomicity, anti-rollback |
| 8 | `shadow-ab` | Shadow deployment and A/B / canary testing | shadow vs A/B in one line | what each measures, risk to users | on-device shadow cost (2x compute), canary sizing | choosing a strategy for a constrained device, labels for A/B |
| 9 | `feedback-retraining` | Feedback loops and continuous retraining | what a feedback loop is | label sources at the edge, retrain triggers | selecting which samples to upload, budget sums | feedback-loop bias, retrain-on-schedule vs on-drift |

## Must-know facts
- Edge MLOps = MLOps for a heterogeneous, intermittently connected fleet: the cloud is the control plane (train, register, decide), devices are the data plane (infer, log, report).
- Course loop: data → train → optimize → deploy → monitor → update/retrain, then back to data.
- CI for models tests code AND model: convert/quantize for each target, then gate on accuracy drop, size, latency on the real (or emulated) device. CD ships the signed artefact to device groups in waves.
- A model registry stores versioned artefacts with metadata: version, training data snapshot, metrics, target hardware, precision (FP32/INT8), runtime version, stage (staging/production/archived).
- A model version only makes sense with its preprocessing and runtime: version the three together.
- Device twin / shadow (AWS IoT shadow, Azure device twin): the cloud writes the desired model version, the device reports the actual one; the device reconciles when it reconnects.
- PSI = Σ (actual − expected) · ln(actual / expected). Course bands: < 0.1 stable (no action), 0.1-0.25 moderate (investigate), > 0.25 significant (retrain).
- Every PSI term is ≥ 0 because (a − e) and ln(a/e) have the same sign; an empty bin makes PSI infinite.
- Confidence-distribution monitoring needs no labels: a model that grows less sure (mass moving from the 0.9-1.0 bin into lower bins) is a proxy for drift.
- A trend across months (rising PSI) tells you drift is progressive and lets you act before the significant threshold; a single reading cannot separate a one-off event from a trend.
- OTA with A/B partitions: write the new image to the inactive slot, switch the boot flag atomically, run health checks, and fall back to the old slot if they fail. Nothing is overwritten in place.
- Images are signed; the device verifies the signature before installing. Delta updates send only the changed bytes.
- Staged rollout: canary group first (1-5%), then waves; halt automatically on error or KPI regression.
- Shadow: the new model sees real inputs but its outputs are only logged; zero user risk, but on-device shadow doubles compute. A/B: a share of devices/users is served by the new model, so outcomes can be compared.
- Feedback loops: field labels (operator corrections, downstream outcomes), low-confidence samples uploaded for labelling, retrain in the cloud, redeploy through the same CI/CD.

## Common traps (each one must have at least one question)
- "PSI 0.06 means retrain now" -> below 0.1 is stable; no action.
- Using the 0.2 threshold some blogs quote -> the course uses 0.1 / 0.25.
- Swapping actual and expected and expecting a different value -> PSI is symmetric.
- Thinking a label-free confidence monitor proves accuracy dropped -> it signals change; you still need labels to confirm.
- Judging only the latest month -> the trend is the early warning.
- Overwriting the only model partition during OTA -> a power cut bricks the device; use A/B slots.
- Shipping one INT8 file without its preprocessing version -> silent accuracy loss (normalisation mismatch).
- Shadow on a tiny MCU at full rate -> doubles latency and energy; sample or shadow on the gateway.
- Treating A/B results without labels as conclusive -> without outcome labels you compare only proxies.
- Retraining only on uploaded low-confidence or operator-flagged samples -> biased feedback loop.
- Pushing an update to the whole fleet at once -> no blast-radius control.
- Assuming offline devices got the update -> desired state is applied only when they reconnect; track reported version.

## Interview angle
1. **"How do you know an edge model is degrading when no labels come back?"** Monitor input statistics and the confidence distribution on the device or gateway; compute PSI against the training reference each period; alert at 0.1, retrain at 0.25; confirm with a small labelled sample.
2. **"How do you update a model on 10,000 devices safely?"** Signed image, A/B partitions with health check and automatic rollback, delta updates for bandwidth, staged rollout by device group with halt criteria, desired/reported state in a device twin.
3. **"Shadow or A/B for a new edge model?"** Shadow first (no user risk, compare outputs), then canary/A-B on a small device group to measure outcomes, then waves.
4. **"What goes into the model registry for an edge model?"** Artefact per target and precision, metrics, data snapshot, preprocessing version, runtime version, stage and lineage.

## Source material
- Handout (`edge-src/handout.txt`), Session 9 (Instructor Supplied Material): lightweight deployment orchestration; edge MLOps pipeline and architecture; CI/CD workflows and model registry management.
- Handout Session 10 (T1 Ch 9, 10): model monitoring, logging and drift detection; over-the-air (OTA) updates and model versioning; shadow deployment and A/B testing; feedback loops for continuous improvement and retraining.
- Handout lab 5: simulate OTA model deployment using an MLOps workflow and monitor model drift through logs. LO5: lightweight MLOps workflows for managing, updating and monitoring edge models.
- Sep 2026 end-sem Set 1 Q5: confidence bins [0.9-1.0, 0.8-0.9, 0.7-0.8, < 0.7]; reference [45, 30, 15, 10]%, April [35, 30, 20, 15] (PSI ≈ 0.060, stable), May [20, 25, 30, 25] (PSI ≈ 0.453, significant); "what does the progression tell you".
- Sep 2026 end-sem Set 2 Q5: reference [40, 30, 20, 10]%, January [42, 29, 19, 10] (PSI ≈ 0.002), February [18, 25, 30, 27] (PSI ≈ 0.394). Note the contrast with Set 1: there the first month is already drifting, here it is flat and the jump is sudden.
- Exam patterns: four-term PSI shown term by term, classified against < 0.1 / 0.1-0.25 / > 0.25 with the action (none / investigate / retrain), and an interpretation of the two-month trend (progressive vs sudden drift, early warning). L3/L4 questions here use new reference distributions, months and Indian deployments (dairy cooperatives, textile mills, metro turnstiles).
- **Standard practice (no slides exist):** Session 9 is "Instructor Supplied Material" with no slides in the source set. Edge MLOps architecture, lightweight orchestration (K3s, KubeEdge, device twins / shadows), CI/CD gates, registry metadata, OTA mechanics (A/B partitions, signed images, delta updates, staged rollouts, anti-rollback), shadow/canary practice and feedback-loop design are written from T1 Ch 9-10 and general industry practice (Mender/SWUpdate/RAUC style OTA, AWS IoT Greengrass and Azure IoT Edge deployments).
- **Convention stated:** PSI uses natural log and the course's 0.1 / 0.25 bands; some sources use 0.2 as the single alert threshold. Questions name the course convention.
- **Gap flagged:** the handout gives no definition of the course's "edge MLOps pipeline" stages; questions test the reasoning (control plane vs data plane, the closed loop) rather than one exact list.
