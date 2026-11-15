# Monitoring & Drift: coverage spec

**Ladder:** L5 · Shipping It › Production ML   ·   **Prerequisites:** ops-serving, ml-basics (train/test, accuracy), basic statistics (mean, distribution, p-value)
**Why it matters for AI/ML:** A broken model rarely crashes; it just gets quietly worse. Monitoring is how you notice: classic observability (latency, errors) plus ML-only signals (input drift, prediction shifts, delayed labels, feedback loops) and, for LLM apps, traces, cost and sampled quality checks.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `why-ml` | Why ML monitoring is different | silent failure: 200 OK but wrong | what to monitor in layers (system, data, model, business) | monitoring without labels | designing a monitoring plan for a new model |
| 2 | `system-metrics` | System metrics, SLOs and dashboards | latency percentiles, error rate, throughput | SLI vs SLO, error budgets; GPU utilisation | burn-rate alerts; percentiles don't average | SLOs for ML quality, not just uptime |
| 3 | `drift-types` | Data, concept and label drift | the world changes; data drift | data vs concept vs label (prior) drift | which drift input monitors can't see | drift that doesn't hurt; covariate shift vs real degradation |
| 4 | `drift-detection` | Detecting drift (PSI, KS, KL/JS, chi-square) | compare live vs reference distribution | PSI on bins and thresholds; KS for numeric | KL asymmetry and zero bins; JS distance vs divergence; chi-square for categories | large-n significance trap; multiple testing; choosing windows and references |
| 5 | `ground-truth` | Delayed labels, proxies and prediction monitoring | labels arrive late | proxy metrics; prediction distribution | label-shift effect on accuracy; join keys for late labels | estimating performance without labels; biased label samples |
| 6 | `data-quality` | Data quality checks and training-serving skew | nulls, ranges, schema | validation as a pipeline gate (Great Expectations idea) | training-serving skew detection by logging features | silent upstream changes (units, encodings, defaults) |
| 7 | `feedback-loops` | Feedback loops | the model affects its own future data | recommender / fraud examples | exploration and holdout to break loops | selection bias in logged data; counterfactual evaluation |
| 8 | `retraining` | Retraining triggers and continuous training | why retrain | schedule vs drift-triggered | champion/challenger gate before promote | retraining pitfalls: on drifted junk, on feedback-biased data, label lag |
| 9 | `online-eval` | A/B testing and online metrics | what an A/B test is | online vs offline metrics; guardrail metrics | randomisation unit; sample ratio mismatch | peeking, novelty effect, interference |
| 10 | `llm-monitoring` | LLM-specific monitoring | traces, tokens, cost, thumbs up/down | TTFT, per-feature cost; sampling for quality | groundedness checks with a judge; eval sets in CI | prompt-injection monitoring; judge drift; regression on model upgrades |
| 11 | `alerting` | Alerting, alert fatigue, logging and privacy | why too many alerts is bad | moving-average and threshold alerts | multiple-testing false alarms; actionable alerts | PII in logs; hashing is not anonymisation; retention |

## Must-know facts
- ML failures are usually silent: the service returns 200 OK with a wrong answer.
- Monitor in layers: system (latency, errors), data (inputs), model (predictions, accuracy), business (KPIs).
- Data drift (covariate shift) = P(x) changes. Concept drift = P(y | x) changes. Label / prior shift = P(y) changes while P(x | y) stays.
- Concept drift can happen with no change in inputs, so input-drift monitors can't see it; you need labels or proxies.
- PSI = sum((actual - expected) x ln(actual / expected)) over bins. Rule of thumb: < 0.1 stable, 0.1-0.25 moderate, > 0.25 big shift. Empty bins need a small epsilon.
- KS test compares two numeric samples using the maximum gap between their cumulative distributions.
- With huge samples, any tiny difference is "significant": look at effect size (KS statistic, PSI), not just p < 0.05.
- KL divergence is asymmetric and infinite when the reference has zero where live data doesn't; JS divergence is symmetric and bounded.
- `scipy.spatial.distance.jensenshannon` returns the JS *distance* (square root of the divergence).
- Chi-square tests compare category counts (e.g. device type, country).
- Testing 100 features at p < 0.05 gives about 5 false alarms per run even with no drift.
- Ground truth is often delayed (fraud chargebacks, loan defaults); use proxies and prediction-distribution monitoring meanwhile.
- Feedback loops: the model's decisions shape the data it will be retrained on; keep a small random / exploration holdout.
- Training-serving skew is detected by logging the exact features served and comparing to the training features.
- Retrain on schedule or on triggers, but always evaluate the challenger against the champion before promoting.
- Error budget: a 99.9% monthly SLO allows about 43 minutes of failure in 30 days.
- Percentiles cannot be averaged across hosts or time windows; aggregate histograms.
- LLM monitoring: traces of every step, tokens and cost per request, TTFT, sampled quality (groundedness, judge scores), user feedback, injection attempts, and a fixed eval set run in CI on every prompt/model change.
- Logs with prompts often contain PII: redact at write time and set retention.

## Common traps (each one must have at least one question)
- "No errors in the logs, so the model is fine" -> ML fails silently.
- "Input distributions look stable, so accuracy is stable" -> concept drift changes P(y | x) with the same inputs.
- "Drift detected means the model got worse" -> some covariate shift doesn't hurt; check performance or proxies.
- Treating a tiny p-value on millions of rows as a real problem -> statistical vs practical significance.
- PSI or KL with an empty bin -> division by zero / infinity; add epsilon.
- Thinking KL(P || Q) = KL(Q || P) -> KL is asymmetric.
- Reading `jensenshannon(p, q)` as the divergence -> it's the distance (sqrt).
- Using a KS test on a categorical feature -> use chi-square on counts.
- Alerting on every feature at p < 0.05 -> alert fatigue from false alarms.
- Averaging p99 latency across hosts -> wrong tail.
- Waiting for labels before monitoring anything -> weeks of blindness; monitor predictions and proxies.
- Accuracy dropping with no model or input-pipeline change because class balance changed -> label shift.
- Retraining on data the model itself filtered -> reinforces its own bias (feedback loop).
- Auto-promoting every retrained model -> may ship a worse model; need a champion/challenger gate.
- Randomising A/B by request instead of by user -> the same user sees both variants; contaminated results.
- Stopping an A/B test the first time p < 0.05 ("peeking") -> inflated false positives.
- Monitoring an LLM app only by latency and errors -> hallucinations and bad answers are invisible.
- "Hashing emails makes logs anonymous" -> hashes of low-entropy values can be reversed by lookup.

## Interview angle
- **"How do you monitor a model in production?"** Four layers: system (p50/p95/p99 latency, error rate, throughput, GPU), data (schema, nulls, ranges, drift via PSI/KS/chi-square against a training reference), model (prediction distribution, accuracy when labels arrive, proxies before), business (conversion, complaints). Alert on a few actionable signals; dashboard the rest. SDE analogy: it's observability, but "correctness" needs its own probes because a wrong answer doesn't throw.
- **"Data drift vs concept drift?"** Data drift: inputs look different (new users, new devices). Concept drift: the same input now means a different answer (fraudsters change tactics). Input monitors catch the first; only labels or proxies catch the second.
- **"Labels arrive 60 days later. What do you do?"** Monitor input drift and the prediction distribution now, use proxies (early chargebacks, user corrections), join labels back by prediction ID when they arrive, and report delayed accuracy by cohort.
- **"When do you retrain?"** On a schedule as a baseline, plus triggers (drift past threshold, performance drop). Every retrain goes through the same eval gate as a deploy: challenger must beat champion on a held-out recent set, then canary.
- **"How do you monitor an LLM feature?"** Traces per request (retrieval, prompt, model call, tools), tokens and cost, TTFT and total latency, user feedback, sampled groundedness checks by a judge model, flagged injection attempts, and a regression eval set in CI for every prompt or model change.

## Source material
To be added.
