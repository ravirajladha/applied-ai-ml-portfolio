# Monitoring & Drift: coverage spec

**Ladder:** L5 · Shipping It › Production ML   ·   **Prerequisites:** ops-serving, ml-basics (train/test, accuracy), basic statistics (mean, distribution, p-value)
**Why it matters for AI/ML:** A broken model rarely crashes; it just gets quietly worse. Monitoring is how you notice: classic observability (latency, errors) plus ML-only signals (input drift, prediction shifts, delayed labels, feedback loops) and, for LLM apps, traces, cost and sampled quality checks.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `why-ml` | Why ML monitoring is different | silent failure: 200 OK but wrong | what to monitor in layers (system, data, model, business) | monitoring without labels | designing a monitoring plan for a new model |
| 2 | `system-metrics` | System metrics, SLOs and dashboards | latency percentiles, error rate, throughput | SLI vs SLO, error budgets; GPU utilisation | burn-rate alerts; percentiles don't average | SLOs for ML quality, not just uptime |
| 3 | `drift-types` | Data, concept and label drift | the world changes; data drift | data vs concept vs label (prior) drift | which drift input monitors can't see | drift that doesn't hurt; covariate shift vs real degradation; precision collapse under prior shift |
| 4 | `drift-detection` | Detecting drift (PSI, KS, KL/JS, chi-square) | compare live vs reference distribution; KS name | PSI on bins and thresholds; KS for numeric | KL asymmetry and zero bins; JS distance vs divergence; chi-square for categories; PSI with quantile bins by hand; KS statistic by hand; PSI depends on binning | large-n significance trap; multiple testing; PSI is symmetric; KS is weak in the tails; JS bound; multivariate drift via a domain classifier |
| 5 | `ground-truth` | Delayed labels, proxies and prediction monitoring | labels arrive late; ground truth; prediction mean shift | proxy metrics; prediction distribution needs no labels | label-shift effect on accuracy; join keys for late labels; share of matured labels | estimating performance without labels; biased label samples; early labels are not random (vintage analysis) |
| 6 | `data-quality` | Data quality checks and training-serving skew | nulls, ranges, schema | validation as a pipeline gate (Great Expectations expectations); unseen category rate | training-serving skew detection by logging features; skew vs drift; point-in-time logged features; handle_unknown='ignore' all-zero rows | silent upstream changes (units, encodings, defaults); row-level skew with identical aggregates |
| 7 | `feedback-loops` | Feedback loops | the model affects its own future data | recommender / fraud examples | exploration and holdout to break loops (and their cost); position bias in click logs | selection bias in logged data; counterfactual evaluation; propensities (IPS) |
| 8 | `retraining` | Retraining triggers and continuous training | why retrain | schedule vs drift-triggered | champion/challenger gate before promote; newest is not always better; hysteresis and cool-down for triggers | retraining pitfalls: on drifted junk, on feedback-biased data, label lag |
| 9 | `online-eval` | A/B testing and online metrics | what an A/B test is | online vs offline metrics; guardrail metrics; SRM name | randomisation unit; sample ratio mismatch | peeking, novelty effect, interference (switchback/cluster); sample size per arm |
| 10 | `llm-monitoring` | LLM-specific monitoring | traces, tokens, cost, thumbs up/down; why log tokens per request | TTFT, per-feature cost (token arithmetic); sampling for quality; output-length creep | groundedness checks with a judge; judge sampling cost; thumbs-down is a biased sample; eval sets in CI | prompt-injection monitoring; judge drift; regression on model upgrades; confidence intervals on sampled rates; heavy-tailed agent cost |
| 11 | `alerting` | Alerting, alert fatigue, logging and privacy | why too many alerts is bad; false positive vs false negative alerts | moving-average and threshold alerts; alert-on-everything is not safe | multiple-testing false alarms; Bonferroni; N-consecutive-window rules; actionable alerts | family-wise false-alarm maths; multi-window burn-rate alerts; PII in logs; hashing is not anonymisation; retention |
| 12 | `windows` | Monitoring windows, baselines and sample size | — | what a reference/baseline dataset is | rolling windows and detection delay; short vs long windows; seasonality-aware references | sliding baselines hide slow drift; window size from event counts (rare positives) |

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
- PSI is symmetric (it equals KL(a||e) + KL(e||a)) and depends on the binning; store the reference bin edges.
- KS is most sensitive near the middle of the distribution, weak in the tails.
- 100 tests at 0.05 with no drift: P(at least one alarm) = 1 - 0.95^100 = 99.4%; Bonferroni uses alpha / tests.
- Burn rate = observed error rate / allowed error rate; 14.4x for 1 hour burns 2% of a 30-day budget.
- Under label shift, precision falls with prevalence even when TPR and FPR are unchanged.
- Rolling windows smooth noise but delay detection; short windows are fast but noisy. Size label-based windows by event counts.
- A sampled rate needs an interval: 16/200 = 8% has a 95% range of about 4-12%.
- A/B sample size rule of thumb: n per arm = 16 p(1-p) / delta^2.

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
- Thinking PSI depends on which sample is the reference -> PSI is symmetric (KL is not).
- Trusting KS to catch tail changes -> it reacts mostly near the median.
- Univariate tests all green -> joint (correlation) drift can still break the model.
- Day-over-day drift checks on weekly-seasonal traffic -> false alarms every weekend.
- Only a sliding baseline -> slow drift is never flagged.
- Daily precision on a rare-positive model -> noise from a handful of events.
- Treating early labels as a random sample -> fast outcomes arrive first; compare cohorts at the same label age.
- `handle_unknown='ignore'` for new categories -> silent all-zero inputs.
- Recomputing features from current tables for training -> not what the model saw; leaks the future.
- Clicks = relevance -> position bias from the old ranking.
- Retrain on every threshold crossing -> trigger thrash; add hysteresis and a cool-down.
- Estimating hallucination rate from thumbs-down conversations -> self-selected sample.
- Reading an 8% -> 10% change from 200 judged samples as real -> within the confidence interval.
- A/B test in a two-sided marketplace randomised by user -> interference inflates the win.

## Interview angle
- **"How do you monitor a model in production?"** Four layers: system (p50/p95/p99 latency, error rate, throughput, GPU), data (schema, nulls, ranges, drift via PSI/KS/chi-square against a training reference), model (prediction distribution, accuracy when labels arrive, proxies before), business (conversion, complaints). Alert on a few actionable signals; dashboard the rest. SDE analogy: it's observability, but "correctness" needs its own probes because a wrong answer doesn't throw.
- **"Data drift vs concept drift?"** Data drift: inputs look different (new users, new devices). Concept drift: the same input now means a different answer (fraudsters change tactics). Input monitors catch the first; only labels or proxies catch the second.
- **"Labels arrive 60 days later. What do you do?"** Monitor input drift and the prediction distribution now, use proxies (early chargebacks, user corrections), join labels back by prediction ID when they arrive, and report delayed accuracy by cohort.
- **"When do you retrain?"** On a schedule as a baseline, plus triggers (drift past threshold, performance drop). Every retrain goes through the same eval gate as a deploy: challenger must beat champion on a held-out recent set, then canary.
- **"How do you monitor an LLM feature?"** Traces per request (retrieval, prompt, model call, tools), tokens and cost, TTFT and total latency, user feedback, sampled groundedness checks by a judge model, flagged injection attempts, and a regression eval set in CI for every prompt or model change.

- **"Your drift dashboard is always red. What do you change?"** Fix the statistics before the thresholds: effect sizes instead of p-values on huge samples, a multiple-testing correction, seasonality-aware references, N-consecutive-window or burn-rate style rules, and alert only on features that matter to the model (importance-weighted). Keep a fixed training reference plus a rolling one.
- **"Your LLM bill tripled with flat traffic."** Look at per-request token and tool-call distributions (p99, max) by feature and prompt version: a few looping agents or huge contexts dominate. Add caps per request and session, and alert on tail growth, not averages.

## Source material
To be added.
