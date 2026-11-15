from helpers import mcq, tf, out, fill

SUBJECT = "ops-monitoring"

TOPICS = [
    ("why-ml", "Why ML monitoring is different"),
    ("system-metrics", "System metrics, SLOs and dashboards"),
    ("drift-types", "Data, concept and label drift"),
    ("drift-detection", "Detecting drift (PSI, KS, KL/JS, chi-square)"),
    ("ground-truth", "Delayed labels, proxies and prediction monitoring"),
    ("data-quality", "Data quality checks and training-serving skew"),
    ("feedback-loops", "Feedback loops"),
    ("retraining", "Retraining triggers and continuous training"),
    ("online-eval", "A/B testing and online metrics"),
    ("llm-monitoring", "LLM-specific monitoring"),
    ("alerting", "Alerting, alert fatigue, logging and privacy"),
    ("windows", "Monitoring windows, baselines and sample size"),
]

QUESTIONS = [
    # ------------------------------------------------------------------ why-ml
    tf("If a model server returns HTTP 200 for every request and has no errors in its logs, the model's predictions must be good.", False,
       "A wrong prediction is still a valid response.",
       "ML fails silently: the code works perfectly while the answers get worse. You need data and model checks on top of normal uptime monitoring.",
       topic="why-ml", level=1),
    mcq("Which of these is an ML-specific thing to monitor that a normal web app wouldn't have?",
        ["The distribution of the model's input features and predictions over time",
         "HTTP error rate",
         "CPU usage",
         "Number of requests per second"], 0,
        "The other three apply to any web service.",
        "Error rate, CPU and traffic are standard app metrics. ML adds: are the inputs still like the training data, and are the predictions still sensible?",
        topic="why-ml", level=1),
    mcq("A useful way to organise ML monitoring is in layers. Which list is complete?",
        ["System (latency, errors) -> data (input quality, drift) -> model (predictions, accuracy) -> business (KPIs like conversions)",
         "CPU -> memory -> disk",
         "Training loss -> validation loss",
         "Unit tests -> integration tests"], 0,
        "From 'is it up' to 'is it helping the business'.",
        "Each layer catches different failures: a crash, a broken input pipeline, a degraded model, or a model that is accurate but no longer moves the KPI.",
        diagram="""
 business  : conversions, complaints
 model     : prediction mix, accuracy (late)
 data      : schema, nulls, drift
 system    : latency, errors, GPU""",
        topic="why-ml", level=2),
    mcq("You launch a churn model whose true labels (did the customer leave?) arrive 90 days later. What can you monitor in week 1?",
        ["Input data quality and drift, the prediction distribution, and early proxy signals; accuracy waits for labels",
         "Nothing until labels arrive",
         "Only training accuracy",
         "Only CPU usage"], 0,
        "What do you have right now, without labels?",
        "Inputs and outputs are available immediately. Drift on inputs and shifts in predicted churn rate are early warnings; label-based metrics come later.",
        topic="why-ml", level=3),
    mcq("You are designing monitoring for a new credit-risk model. Which plan is strongest?",
        ["Keep training data as a reference; log features, prediction, model version and a prediction ID per request; run daily drift and quality checks; join late labels by ID; alert on a few actionable thresholds",
         "Log only errors and CPU",
         "Recompute training accuracy every day",
         "Alert on every feature whenever any test gives p < 0.05"], 0,
        "You need a reference, the served data, a join key for labels, and few good alerts.",
        "Without a reference you can't measure drift; without logged features you can't debug skew; without a prediction ID you can't attach labels later; without restraint you drown in alerts.",
        topic="why-ml", level=4),

    # ------------------------------------------------------------------ system-metrics
    mcq("Which three are the basic 'golden signal' style metrics for any model API?",
        ["Latency, error rate and throughput (requests per second)",
         "Accuracy, recall and F1",
         "Training loss, epochs and batch size",
         "Lines of code, commits and tests"], 0,
        "How fast, how often broken, how much traffic.",
        "These system metrics tell you whether the service is up and responsive. Model-quality metrics are a separate layer.",
        topic="system-metrics", level=1),
    out("""import numpy as np

rng = np.random.default_rng(0)
lat = rng.exponential(scale=100, size=10_000)   # ms, long right tail
p50, p95, p99 = np.percentile(lat, [50, 95, 99])
print(round(p50), round(p95), round(p99))""",
        ["68 301 456", "100 100 100", "50 95 99", "100 301 456"], 0,
        "Exponential latencies: most are fast, a few are very slow.",
        "The median is around 68 ms but p99 is about 6-7x higher. Users who hit the tail feel the p99, which is why SLOs are written on p95/p99.",
        topic="system-metrics", level=1),
    mcq("In SRE terms, what is the difference between an SLI and an SLO?",
        ["SLI is the measured indicator (e.g. % of requests under 300 ms); SLO is the target for it (e.g. 99% over 30 days)",
         "They are the same",
         "SLO is a legal contract with refunds; SLI is a target",
         "SLI is for ML only"], 0,
        "Indicator vs objective.",
        "SLI = what you measure, SLO = the goal, SLA = the external contract with penalties.",
        topic="system-metrics", level=2),
    out("""slo = 0.999
minutes_in_30_days = 30 * 24 * 60
budget = (1 - slo) * minutes_in_30_days
print(round(budget, 1))""",
        ["43.2", "4.3", "432.0", "1.4"], 0,
        "0.1% of 43,200 minutes.",
        "A 99.9% SLO allows about 43 minutes of bad time per 30 days. That's the error budget: spend it on risky deploys, or freeze when it's gone.",
        topic="system-metrics", level=2),
    mcq("A GPU-backed model server shows 98% 'GPU utilisation' in nvidia-smi, yet throughput is low. Why might that metric mislead?",
        ["That 'utilisation' only means a kernel was running during the sample window, not that the GPU's compute units are busy; check throughput, batch size and memory bandwidth too",
         "The GPU is definitely at maximum efficiency",
         "nvidia-smi reports CPU usage",
         "98% means the model is overfitting"], 0,
        "Busy doesn't mean efficient.",
        "A single small kernel running all the time can show ~100%. Pair it with tokens/s or requests/s, batch size and memory use to judge real efficiency.",
        topic="system-metrics", level=3),
    mcq("Your SLO is 99.9% of requests succeed over 30 days. Which alert is best practice?",
        ["Alert when the error budget is burning fast (e.g. 14x the allowed rate over 1 hour) AND still burning over a shorter window, so you page only for real, ongoing problems",
         "Alert on every single failed request",
         "Alert once the whole month's budget is gone",
         "Alert when CPU is over 50%"], 0,
        "Page on things that threaten the SLO.",
        "Burn-rate alerts measure how fast you're spending the budget. Multi-window checks cut flapping and catch both sudden and slow burns.",
        topic="system-metrics", level=3),
    mcq("Your team only has uptime and latency SLOs. The model's precision drops from 0.9 to 0.6 and nothing alerts. What should be added?",
        ["Model-quality SLOs, e.g. 'weekly precision on labelled samples >= 0.85' or 'proxy metric within band', with owners and alerting, like any other SLO",
         "A tighter latency SLO",
         "More CPU",
         "Nothing; quality is not an operational concern"], 0,
        "What does the user actually care about?",
        "A fast, available, wrong model breaks the product. Quality can be an SLI too, measured on labelled or judged samples, with the caveat that it lags.",
        topic="system-metrics", level=4),

    tf("To get a fleet-wide p99 latency for the dashboard, it is fine to average the p99 values reported by each server.", False,
       "Would one slow server's tail be weighted correctly?",
       "Percentiles don't compose: the average of per-host p99s can be far from the true p99 over all requests. Export latency histograms (buckets) and compute the percentile over the merged histogram.",
       topic="system-metrics", level=3),
    fill("Fill in the blank: a dashboard that shows how many requests per second the model serves is showing ____ (one word).",
         "throughput",
         "A rate, not a duration.",
         "Throughput = requests (or tokens) completed per second; latency = how long each one takes.",
         topic="system-metrics", level=1),

    # ------------------------------------------------------------------ drift-types
    mcq("A spam model was trained on emails from 2022. In 2026, spammers use new tricks, so emails that look like the old 'normal' emails are now often spam. Which drift is this?",
        ["Concept drift: the relationship between the email and the label changed",
         "Label drift only",
         "No drift; the model is fine",
         "A server error"], 0,
        "Same-looking inputs, different correct answer.",
        "Concept drift means P(label | input) changed. The model's learned rule is now wrong even for inputs that look familiar.",
        topic="drift-types", level=1),
    mcq("Match the definitions. Data drift, concept drift and label (prior) shift are changes in, respectively:",
        ["P(x); P(y | x); P(y) while P(x | y) stays the same",
         "P(y); P(x); P(y | x)",
         "P(y | x); P(x); P(x | y)",
         "Model weights; code; labels"], 0,
        "x = inputs, y = target.",
        "Data (covariate) drift: input mix changes. Concept drift: the mapping changes. Label shift: the class balance changes, but each class still looks the same.",
        topic="drift-types", level=2),
    tf("If every input feature's distribution is exactly the same as in training, the model's accuracy cannot have dropped.", False,
       "Think of a fraudster who keeps the same transaction pattern but the meaning changes.",
       "Concept drift changes P(y | x) without touching P(x). Input-drift monitors stay green; only labels or proxies reveal the drop.",
       topic="drift-types", level=2),
    mcq("During a flu outbreak, the share of flu patients at a clinic rises from 5% to 30%, but flu patients' symptoms look the same as before. Which drift is this?",
        ["Label (prior) shift", "Concept drift", "Training-serving skew", "No drift"], 0,
        "The class balance changed; what each class looks like didn't.",
        "Label shift: P(y) changes, P(x | y) is stable. Calibrated probabilities and thresholds tuned for 5% prevalence become off.",
        topic="drift-types", level=2),
    mcq("A house-price model trained mostly on 2-3 bedroom homes starts seeing many more 3-bedroom homes (still within training range). Drift alerts fire. Accuracy is unchanged. Why?",
        ["Covariate shift within a region the model learned well doesn't necessarily hurt; drift is a warning, not proof of degradation",
         "The drift test must be broken",
         "Accuracy always drops with drift; it will drop later",
         "The model is overfitting"], 0,
        "Did the inputs move outside what the model knows?",
        "Shifts towards well-covered regions are often harmless. Shifts into regions with little training data, or concept changes, are the dangerous ones. Confirm with performance or proxies before retraining.",
        topic="drift-types", level=3),
    mcq("An e-commerce model's input monitors are all green, yet weekly conversion from recommendations fell 20% after a competitor launched free shipping. What is the best diagnosis?",
        ["Concept drift: user behaviour given the same features changed; input monitors cannot see it, so you need outcome metrics (conversion) and fresh labels",
         "Data drift in the product catalogue",
         "A latency regression",
         "Training-serving skew"], 0,
        "The world changed how people respond, not what they look like.",
        "External events change P(y | x). Business-outcome monitoring and A/B holdouts catch it; feature-drift tests alone never will.",
        topic="drift-types", level=4),

    # ------------------------------------------------------------------ drift-detection
    mcq("To detect data drift, what do you compare?",
        ["The distribution of a feature in recent live data with its distribution in a reference set (usually the training data)",
         "Today's model weights with yesterday's",
         "The code in production with the code in git",
         "Training loss with validation loss"], 0,
        "Drift = 'live looks different from what the model learned on'.",
        "Pick a reference window (training data or a known-good period) and compare each feature's live distribution to it with a statistic like PSI or KS.",
        topic="drift-detection", level=1),
    fill("Fill in the blank: PSI, a popular drift score, stands for Population ____ Index.",
         "Stability",
         "It asks: is the population still stable?",
         "Population Stability Index: compares the share of data in each bin between a reference and a live sample. 0 means identical.",
         topic="drift-detection", level=1),
    out("""import numpy as np

expected = np.array([0.25, 0.25, 0.25, 0.25])   # training share per bin
actual   = np.array([0.10, 0.20, 0.30, 0.40])   # live share per bin
psi = np.sum((actual - expected) * np.log(actual / expected))
print(round(psi, 3))""",
        ["0.228", "0.0", "0.6", "-0.228"], 0,
        "Each bin contributes (a - e) x ln(a / e), which is never negative.",
        "PSI = 0.228: in the 0.1-0.25 'moderate shift' band. Each term is >= 0 because (a - e) and ln(a / e) always have the same sign.",
        topic="drift-detection", level=2),
    fill("Fill in the blank: a common rule of thumb says PSI above ____ means a significant shift that needs investigation.",
         "0.25",
         "The bands are < 0.1, 0.1 to ?, above ?.",
         "Typical reading: < 0.1 stable, 0.1-0.25 moderate, > 0.25 significant. These are conventions from credit scoring, not laws.",
         topic="drift-detection", level=2),
    out("""from scipy.stats import ks_2samp
import numpy as np

rng = np.random.default_rng(0)
train = rng.normal(0.0, 1.0, 500)
live  = rng.normal(0.5, 1.0, 500)
res = ks_2samp(train, live)
print(round(res.statistic, 2), res.pvalue < 0.05)""",
        ["0.21 True", "0.21 False", "0.5 True", "0.02 False"], 0,
        "The live mean moved by half a standard deviation with 500 samples each.",
        "The KS statistic is the largest vertical gap between the two empirical CDFs (about 0.2 here), and with 500 points each that gap is clearly significant.",
        diagram="""
 CDF 1 |        ____----
       |    _--/  __----   <- gap = KS statistic
       |  _/   _-/
     0 |_/__--/____________ x
         train  live""",
        topic="drift-detection", level=2),
    out("""from scipy.stats import ks_2samp
import numpy as np

rng = np.random.default_rng(1)
train = rng.normal(0.00, 1.0, 1_000_000)
live  = rng.normal(0.01, 1.0, 1_000_000)
res = ks_2samp(train, live)
print(round(res.statistic, 3), res.pvalue < 0.05)""",
        ["0.005 True", "0.005 False", "0.5 True", "0.0 False"], 0,
        "A shift of 0.01 standard deviations, but a million rows each.",
        "The statistic is tiny (about 0.005) yet p < 0.05: with huge samples every negligible difference is 'significant'. Alert on effect size (KS statistic, PSI), not on p-values alone.",
        topic="drift-detection", level=3),
    out("""import numpy as np

expected = np.array([0.5, 0.3, 0.2, 0.0])   # bin never seen in training
actual   = np.array([0.4, 0.3, 0.2, 0.1])
with np.errstate(divide="ignore"):
    psi = np.sum((actual - expected) * np.log(actual / expected))
print(psi)
eps = 1e-4
e, a = np.clip(expected, eps, None), np.clip(actual, eps, None)
print(round(np.sum((a - e) * np.log(a / e)), 2))""",
        ["inf\n0.71", "0.0\n0.71", "nan\n0.0", "inf\ninf"], 0,
        "ln(0.1 / 0) is infinite.",
        "One empty reference bin makes PSI infinite. Clipping to a small epsilon gives a finite (but epsilon-dependent) value; better binning (quantile bins on training data, an 'other' bin) avoids the problem.",
        topic="drift-detection", level=3),
    out("""from scipy.stats import entropy
import numpy as np

p = np.array([0.9, 0.1])
q = np.array([0.5, 0.5])
print(round(entropy(p, q), 3), round(entropy(q, p), 3))""",
        ["0.368 0.511", "0.368 0.368", "0.511 0.511", "0.511 0.368"], 0,
        "scipy.stats.entropy(p, q) is KL(p || q).",
        "KL divergence is not symmetric: KL(p || q) = 0.368 but KL(q || p) = 0.511. Always state which direction you computed, or use a symmetric measure (PSI, JS).",
        topic="drift-detection", level=3),
    out("""from scipy.spatial.distance import jensenshannon
import numpy as np

p = np.array([1.0, 0.0])
q = np.array([0.0, 1.0])
d = jensenshannon(p, q, base=2)
print(round(d, 3), round(d ** 2, 3))""",
        ["1.0 1.0", "0.5 0.25", "inf inf", "0.693 0.48"], 0,
        "Completely non-overlapping distributions hit the maximum.",
        "With base 2, both the JS distance and divergence top out at 1. For partial overlap they differ: scipy returns the distance, which is the square root of the divergence.",
        topic="drift-detection", level=3),
    out("""from scipy.spatial.distance import jensenshannon
import numpy as np

p = np.array([0.5, 0.5])
q = np.array([0.9, 0.1])
d = jensenshannon(p, q, base=2)
print(round(d, 3), round(d ** 2, 3))""",
        ["0.383 0.147", "0.147 0.383", "0.383 0.383", "0.147 0.022"], 0,
        "scipy returns the square root of the JS divergence.",
        "jensenshannon gives the JS distance (0.383); the divergence is its square (0.147). Mixing the two up changes your alert thresholds a lot.",
        topic="drift-detection", level=4),
    out("""from scipy.stats import chi2_contingency
import numpy as np

#                 mobile  desktop  tablet
counts = np.array([[600,    350,     50],    # training
                   [750,    200,     50]])   # live
chi2, p, dof, _ = chi2_contingency(counts)
print(dof, p < 0.05)""",
        ["2 True", "2 False", "6 True", "1 True"], 0,
        "dof = (rows - 1) x (cols - 1).",
        "Device type is categorical, so use a chi-square test on counts (not KS, which needs ordered numbers). dof = 1 x 2 = 2, and the mobile/desktop swing is clearly significant.",
        topic="drift-detection", level=2),
    tf("A two-sample KS test is a good choice for detecting drift in a categorical feature like 'country'.", False,
       "KS works on cumulative distributions of ordered values.",
       "Categories have no natural order, so a CDF is meaningless. Use chi-square on counts, or PSI / JS over category shares.",
       topic="drift-detection", level=2),
    mcq("You check drift daily by comparing each day's live data to the training set. Every day since launch shows 'drift' on a seasonal feature. What is the better reference design?",
        ["Compare against a matching window (e.g. same weekday / same season last year, or a recent known-good window) and/or a rolling reference, so normal seasonality doesn't count as drift",
         "Stop monitoring that feature forever",
         "Retrain the model every day",
         "Lower the threshold"], 0,
        "What's 'normal' changes with the calendar.",
        "Reference choice is a design decision: training data catches distance from what the model learned; a rolling or seasonal reference catches sudden changes. Many teams track both.",
        topic="drift-detection", level=4),

    # ------------------------------------------------------------------ ground-truth
    mcq("Why can't a fraud team measure their model's real accuracy on today's transactions?",
        ["The true label (was it fraud?) often only arrives weeks later via chargebacks",
         "Fraud models don't have labels",
         "Accuracy can only be computed during training",
         "The database is too slow"], 0,
        "When does the bank learn the truth?",
        "Ground truth is delayed. Until labels arrive, teams watch inputs, predictions and proxy signals.",
        topic="ground-truth", level=1),
    mcq("Which is a reasonable proxy metric for a search-ranking model while true relevance labels are unavailable?",
        ["Click-through rate on top results and how often users reformulate the query",
         "CPU usage",
         "Number of model parameters",
         "Training loss"], 0,
        "Proxies are cheap signals that move with quality.",
        "Proxies correlate with quality but are not quality: clicks can be fooled by clickbait titles. Validate proxies against labels when you get them.",
        topic="ground-truth", level=2),
    out("""import numpy as np

last_week = np.array([0]*95 + [1]*5)        # 5% flagged as fraud
today     = np.array([0]*80 + [1]*20)       # 20% flagged
print(last_week.mean(), today.mean(), today.mean() / last_week.mean())""",
        ["0.05 0.2 4.0", "5 20 4", "0.05 0.2 0.25", "0.2 0.05 4.0"], 0,
        "The mean of 0/1 predictions is the positive rate.",
        "The model's flag rate jumped 4x with no labels needed. Either fraud really spiked or something upstream broke: prediction-distribution monitoring catches both early.",
        topic="ground-truth", level=2),
    out("""# per-class accuracy stays the same; only the class mix changes
acc_pos, acc_neg = 0.70, 0.95
for share_pos in (0.10, 0.50):
    overall = share_pos * acc_pos + (1 - share_pos) * acc_neg
    print(share_pos, round(overall, 3))""",
        ["0.1 0.925\n0.5 0.825", "0.1 0.825\n0.5 0.925", "0.1 0.95\n0.5 0.95", "0.1 0.7\n0.5 0.7"], 0,
        "Overall accuracy is a weighted average of per-class accuracy.",
        "The model hasn't changed, yet overall accuracy falls from 0.925 to 0.825 because positives (the harder class) became more common. That's label shift: report per-class metrics, not just overall accuracy.",
        topic="ground-truth", level=3),
    mcq("Labels for a loan model arrive 60 days later in a separate system. What must you log at prediction time so you can compute accuracy later?",
        ["A unique prediction ID (or entity ID + timestamp), the model version, the features and the prediction, so labels can be joined back exactly",
         "Only the prediction",
         "Only the model version",
         "Nothing; recompute predictions when labels arrive"], 0,
        "You need a join key and the exact state at decision time.",
        "Recomputing later uses today's features and model, not what was actually served. Log the decision and join the label to it.",
        topic="ground-truth", level=3),
    mcq("A fraud model blocks transactions it scores as risky. Labels only exist for transactions that went through. What's wrong with measuring precision/recall on those labels?",
        ["Blocked transactions never get a label, so the labelled set is biased by the model itself; you can't see its false positives. Keep a small random sample that is let through or reviewed manually",
         "Nothing; labelled data is always unbiased",
         "Precision can't be computed for fraud",
         "You should use training accuracy instead"], 0,
        "Which outcomes can you never observe?",
        "The model decides which labels exist (selection bias). A randomised review/holdout slice gives an unbiased estimate, at a controlled cost.",
        topic="ground-truth", level=4),
    mcq("Without any labels, which approach can estimate a classifier's accuracy on new data, and what does it assume?",
        ["Average the model's predicted confidence (or methods like confidence-based performance estimation) - assumes the model stays calibrated and there's no concept drift",
         "Use training accuracy - assumes nothing",
         "Count requests - assumes accuracy equals traffic",
         "It is mathematically impossible under any assumptions"], 0,
        "If a calibrated model says 0.8 on average, about 80% should be right.",
        "Confidence-based estimation works under covariate shift if calibration holds; under concept drift the model is confidently wrong and the estimate is too optimistic.",
        topic="ground-truth", level=4),

    # ------------------------------------------------------------------ data-quality
    mcq("Which is a basic data-quality check to run on every batch of inputs before scoring?",
        ["Columns and types match the expected schema, null rates are within limits, values are in valid ranges",
         "The model's accuracy is above 90%",
         "The batch is bigger than 1 GB",
         "The file name contains today's date"], 0,
        "Garbage in, garbage out.",
        "Schema, nulls and ranges catch most broken pipelines before they turn into silent bad predictions.",
        topic="data-quality", level=1),
    out("""import pandas as pd
import numpy as np

df = pd.DataFrame({"age": [25, 41, np.nan, 230, 37],
                   "income": [50, 80, 62, None, 71]})
print(df.isna().sum().tolist(), int(((df["age"] < 0) | (df["age"] > 120)).sum()))""",
        ["[1, 1] 1", "[1, 1] 0", "[2, 0] 1", "[0, 0] 1"], 0,
        "None in a float column also becomes NaN; NaN comparisons are False.",
        "Each column has one missing value, and one age (230) is out of range. NaN is not counted as out of range because NaN > 120 is False, so null checks and range checks are both needed.",
        topic="data-quality", level=1),
    out("""import pandas as pd

expected = {"user_id": "int64", "amount": "float64", "country": "object"}
batch = pd.DataFrame({"user_id": [1, 2], "amount": ["10.5", "7"], "country": ["IN", "US"]})
problems = [c for c, t in expected.items() if str(batch[c].dtype) != t]
print(problems)""",
        ["['amount']", "[]", "['amount', 'country']", "['user_id', 'amount']"], 0,
        "Strings in a column are stored with dtype object.",
        "amount arrived as strings (object), not float64. A schema check catches this before the model receives text where it expects numbers.",
        topic="data-quality", level=2),
    mcq("What is the core idea of a tool like Great Expectations (or pandera) in an ML pipeline?",
        ["Declare expectations about data (not null, in range, unique, allowed values) and run them as a gate that fails the pipeline when data breaks them",
         "Train models automatically",
         "Visualise model weights",
         "Store model versions"], 0,
        "Unit tests, but for data.",
        "Expectations are assertions on data, run in CI or before training/scoring. A failing check stops bad data from silently reaching the model.",
        analogy="Like contract tests on an API payload, but for every batch of data.",
        topic="data-quality", level=2),
    mcq("How do you detect training-serving skew in practice?",
        ["Log the exact feature values the model received at serving time and compare them with the offline/training features computed for the same entities and timestamps",
         "Compare training loss with validation loss",
         "Check the Docker image size",
         "Watch CPU usage"], 0,
        "You need both versions of the same feature row.",
        "Skew means the same entity got different feature values online vs offline. Logging served features and recomputing offline for the same keys makes mismatches visible.",
        topic="data-quality", level=3),
    out("""import numpy as np

train_amount = np.array([12.0, 30.5, 8.2, 45.0])         # in dollars
served_amount = np.array([1200.0, 3050.0, 820.0, 4500.0])  # upstream switched to cents
ratio = np.median(served_amount) / np.median(train_amount)
print(round(ratio), ratio > 10)""",
        ["100 True", "1 False", "10 False", "100 False"], 0,
        "Medians of the same values in different units.",
        "A 100x jump in the median screams unit change (dollars -> cents). The schema still passes (float), nulls are fine; only a distribution check catches it.",
        topic="data-quality", level=3),
    mcq("An upstream team changes a missing-value default for 'last_login_days' from NULL to 0. No schema check fails. What happens and what would catch it?",
        ["The model reads 'missing' as 'logged in today' and predictions shift; a distribution check (sudden spike at 0, changed mean, null rate dropping to 0%) catches it",
         "Nothing changes because 0 and NULL mean the same",
         "The schema check catches it",
         "The model throws an error"], 0,
        "A valid-looking value with a different meaning.",
        "Silent semantic changes pass type checks. Monitor value distributions and null rates, and treat data contracts with upstream teams like API contracts.",
        topic="data-quality", level=4),

    # ------------------------------------------------------------------ feedback-loops
    mcq("A video app's recommender only shows cooking videos to a user, the user only clicks cooking videos (because that's all they see), and the model learns 'this user only likes cooking'. What is this?",
        ["A feedback loop: the model's own outputs shape the data it learns from next",
         "Data drift",
         "A server bug",
         "Overfitting to the test set"], 0,
        "Where did the training data come from?",
        "The model creates its own evidence. Over time recommendations narrow and the data can no longer show what the user would have liked.",
        topic="feedback-loops", level=1),
    tf("Feedback loops can make a model look better and better on its own logged data while real-world quality gets worse.", True,
       "The model chooses what gets observed.",
       "If the model only sees outcomes for actions it chose, its logged metrics confirm its own choices. Unbiased evaluation needs data it didn't select.",
       topic="feedback-loops", level=2),
    mcq("What is a standard way to keep a recommender's feedback loop in check?",
        ["Reserve a small share of traffic for exploration (random or diverse items) and keep a holdout group, so you collect data the model didn't choose",
         "Retrain more often on the same logged clicks",
         "Remove the model",
         "Show users only their top item"], 0,
        "You need some data that isn't biased by the model.",
        "Exploration (e.g. epsilon-greedy, bandits) and randomised holdouts give unbiased signal for training and evaluation, at a small short-term cost.",
        topic="feedback-loops", level=3),
    out("""import numpy as np

rng = np.random.default_rng(0)
true_like = np.array([0.30, 0.25, 0.20])   # real chance a user clicks each item
shown = np.zeros(3); clicks = np.zeros(3)
for _ in range(3000):
    item = 0                                  # always show the current 'best' item
    shown[item] += 1
    clicks[item] += rng.random() < true_like[item]
print(shown.astype(int).tolist(), int(clicks[1]))""",
        ["[3000, 0, 0] 0", "[1000, 1000, 1000] 250", "[3000, 0, 0] 750", "[0, 3000, 0] 0"], 0,
        "Which items ever get a chance to be clicked?",
        "Items 1 and 2 are never shown, so they have zero clicks and the logs 'prove' item 0 is best. Without exploration the model can never learn whether its other options are good.",
        topic="feedback-loops", level=3),
    mcq("You want to evaluate a new ranking policy offline using logs from the old policy. Why do teams log the old policy's probability of showing each item (propensity)?",
        ["So they can reweight logged outcomes (inverse propensity scoring) to estimate how the new policy would have done, correcting for the old policy's selection bias",
         "To make the logs smaller",
         "To speed up training",
         "Propensities are only needed for images"], 0,
        "Rarely shown items need a higher weight.",
        "Counterfactual evaluation divides each outcome by how likely the old policy was to show it. It only works if the old policy gave every relevant item non-zero probability (exploration again).",
        topic="feedback-loops", level=4),

    # ------------------------------------------------------------------ retraining
    mcq("Why do production models usually need retraining?",
        ["The world changes after training (new users, products, behaviour), so a model trained on old data slowly goes stale",
         "Model files expire after 30 days",
         "Retraining fixes server errors",
         "Retraining makes the code faster"], 0,
        "What happened since the training data was collected?",
        "Models encode a snapshot of the past. As the present drifts away from it, performance decays and fresh data is needed.",
        topic="retraining", level=1),
    mcq("What are the two common ways to decide WHEN to retrain?",
        ["On a fixed schedule (e.g. weekly), or triggered by monitoring (drift past a threshold, performance drop)",
         "Only when the server restarts",
         "Every request",
         "When the code is refactored"], 0,
        "Calendar vs signal.",
        "Schedules are simple and predictable; triggers react to real change but need trustworthy monitors. Many teams do both: a scheduled baseline plus triggers.",
        topic="retraining", level=2),
    mcq("A continuous-training pipeline retrains weekly. What must happen between 'new model trained' and 'new model serves 100% of traffic'?",
        ["Automated eval: the challenger must beat (or match) the current champion on a recent held-out set and pass data/fairness checks, then roll out via shadow or canary",
         "Nothing; newer is always better",
         "A manual check of the training loss curve only",
         "Delete the old model to save space"], 0,
        "Treat a retrain like a deploy.",
        "Champion/challenger gating stops a bad training run (broken data, bug) from replacing a good model. Keep the champion available for rollback.",
        diagram="""
 new data -> train -> eval vs champion --pass--> canary -> 100%
                            |
                          fail -> keep champion, alert""",
        topic="retraining", level=3),
    tf("If a drift alert fires, the right automatic response is always to retrain immediately on the latest data and deploy.", False,
       "What if the 'drift' is a broken upstream pipeline?",
       "Drift can be a data bug (unit change, nulls) rather than a real-world change. Retraining on broken data bakes the bug into the model. Investigate or gate, then retrain.",
       topic="retraining", level=3),
    mcq("A fraud model retrains weekly on 'last 4 weeks of labelled data', but chargeback labels take 8 weeks to settle. What subtle problem results?",
        ["Recent fraud that hasn't been charged back yet is labelled as legitimate, so each retrain learns that new fraud patterns are 'safe'",
         "No problem; more recent data is always better",
         "The model will overfit to old data",
         "Training will be too slow"], 0,
        "What label does a not-yet-reported fraud have today?",
        "Label lag makes the newest data look cleaner than it is. Train only on matured labels (older than the settlement window) or model label maturity explicitly.",
        topic="retraining", level=4),
    mcq("Which retraining risk comes from feedback loops specifically?",
        ["Training on data the current model filtered (approved loans, shown items) reinforces its own past decisions and hides groups it rejected",
         "The model file becomes too big",
         "Retraining takes too long",
         "GPU memory runs out"], 0,
        "Who decided what data you collected?",
        "Without exploration or reject-inference, each retrain narrows the model further. The fix is unbiased data slices, not more frequent retraining.",
        topic="retraining", level=4),

    # ------------------------------------------------------------------ online-eval
    mcq("What is an A/B test for a model?",
        ["Randomly split users into groups, give each group a different model, and compare a chosen metric between the groups",
         "Testing the model twice on the same data",
         "Training two models and keeping the bigger one",
         "Testing in alphabetical order"], 0,
        "Random groups, one difference.",
        "Randomisation makes the groups comparable, so a difference in the metric can be attributed to the model.",
        topic="online-eval", level=1),
    mcq("A new model has better offline AUC but loses the A/B test on revenue. What is the most likely explanation?",
        ["Offline metrics on historical data don't capture everything real users respond to (and may not align with the business goal); the online metric is the ground truth for impact",
         "The A/B test is always wrong",
         "AUC and revenue are the same thing",
         "The new model must have a bug in its weights"], 0,
        "Offline is a proxy for online.",
        "Offline evaluation can miss skew, feedback effects, latency and misalignment between the training objective and the business metric.",
        topic="online-eval", level=2),
    mcq("In an A/B test of a new recommender, which is a 'guardrail metric'?",
        ["Page latency and unsubscribe rate: metrics that must not get worse, even if the main metric improves",
         "The main metric you hope to improve",
         "The number of users in the test",
         "The training loss"], 0,
        "Guardrails stop you shipping a win that breaks something else.",
        "You optimise one primary metric but block launches that hurt guardrails (latency, errors, complaints, retention).",
        topic="online-eval", level=2),
    mcq("Why should an A/B test of a chatbot model randomise by user rather than by request?",
        ["Per-request randomisation shows the same user both models, contaminating their experience and the measured effect; users are the independent unit",
         "Per-request randomisation is illegal",
         "Per-user randomisation needs fewer servers",
         "There is no difference"], 0,
        "A conversation has many requests.",
        "The randomisation unit should match the unit of analysis and avoid carry-over. Sticky user assignment (stable hash) keeps each user in one arm.",
        topic="online-eval", level=3),
    out("""from scipy.stats import chisquare

observed = [5_210, 4_790]            # users in A and B; planned 50/50
res = chisquare(observed, f_exp=[5_000, 5_000])
print(round(res.statistic, 2), res.pvalue < 0.001)""",
        ["17.64 True", "17.64 False", "0.42 False", "420.0 True"], 0,
        "Chi-square = sum((obs - exp)^2 / exp).",
        "(210^2 + 210^2) / 5000 = 17.64, p far below 0.001: a sample ratio mismatch. The split itself is broken (bucketing bug, bots, crashes in one arm), so the test's results can't be trusted.",
        topic="online-eval", level=3),
    out("""import numpy as np

rng = np.random.default_rng(0)
false_wins = 0
for _ in range(2000):                      # A and B are IDENTICAL
    a = rng.normal(0, 1, 1000); b = rng.normal(0, 1, 1000)
    for n in range(100, 1001, 100):        # peek after every 100 users
        diff = b[:n].mean() - a[:n].mean()
        if abs(diff) / np.sqrt(2 / n) > 1.96:
            false_wins += 1
            break
print(round(false_wins / 2000, 2) > 0.05)""",
        ["True", "False", "ValueError", "None"], 0,
        "Each peek is another chance to see a fluke.",
        "With 10 peeks the false-positive rate is about 0.2, far above the nominal 0.05. Fix the sample size up front, or use sequential testing methods designed for peeking.",
        topic="online-eval", level=4),
    mcq("A new recommender's A/B lift is +8% in week 1, +3% in week 2 and +0.5% in week 4. What is the most likely effect, and the lesson?",
        ["Novelty effect: users react to anything new at first; run tests long enough (and look at the trend) before trusting the lift",
         "Data drift in the model",
         "The test is broken and must be restarted",
         "The model is getting better over time"], 0,
        "New things get clicked because they're new.",
        "Novelty (or its opposite, change aversion) distorts short tests. Look at effect over time and by cohort (new vs returning users).",
        topic="online-eval", level=4),

    # ------------------------------------------------------------------ llm-monitoring
    mcq("Which set of signals is most useful to log for every request of an LLM chatbot?",
        ["A trace of each step (retrieval, prompt, model call, tools) with latency, token counts, cost, model version and user feedback",
         "Only whether the HTTP call returned 200",
         "Only the GPU temperature",
         "Only the final answer text"], 0,
        "You need to debug a bad answer AND explain the bill.",
        "Traces show where time and tokens went; feedback and sampled reviews show quality. Status codes alone miss wrong answers.",
        topic="llm-monitoring", level=1),
    tf("A thumbs-up / thumbs-down button gives an LLM app a cheap, if noisy and biased, quality signal.", True,
       "Who bothers to click, and when?",
       "Feedback is valuable but skewed (unhappy users click more, most don't click). Use it as one signal alongside sampled evaluations.",
       topic="llm-monitoring", level=1),
    out("""import pandas as pd

logs = pd.DataFrame({
    "feature": ["chat", "chat", "summarise", "summarise", "chat"],
    "in_tok":  [800, 1200, 6000, 5000, 1000],
    "out_tok": [200, 300, 400, 300, 100],
})
logs["cost"] = logs.in_tok * 3e-6 + logs.out_tok * 15e-6
print(logs.groupby("feature")["cost"].sum().round(4).to_dict())""",
        ["{'chat': 0.018, 'summarise': 0.0435}", "{'chat': 0.0435, 'summarise': 0.018}",
         "{'chat': 0.009, 'summarise': 0.033}", "{'chat': 3000, 'summarise': 11700}"], 0,
        "Price: $3 per million input tokens, $15 per million output tokens.",
        "chat: 3000 input x $3/M + 600 output x $15/M = $0.018. summarise: 11000 x $3/M + 700 x $15/M = $0.0435. Two summaries cost more than twice the three chats: per-feature cost dashboards show where to optimise.",
        topic="llm-monitoring", level=2),
    mcq("For a streaming chat endpoint, which latency metric best matches 'how long until the user sees something'?",
        ["Time to first token (TTFT)", "Total response time", "Model load time", "Database query time"], 0,
        "Streaming changes what 'slow' feels like.",
        "Track TTFT (perceived responsiveness) and tokens/s or total time (throughput) separately; they have different causes (prompt length vs generation).",
        topic="llm-monitoring", level=2),
    mcq("You can't afford human review of every RAG answer. What is a common way to monitor groundedness (answers supported by the retrieved documents)?",
        ["Sample a small percentage of traffic and have a judge model (or humans for a smaller slice) check each claim against the retrieved context, tracking the score over time",
         "Assume answers are grounded if the response is long",
         "Check that the HTTP status is 200",
         "Measure token count only"], 0,
        "Sampling + automated grading.",
        "LLM-as-judge on a sample gives a trend line for hallucination rate. Calibrate the judge against human labels periodically.",
        topic="llm-monitoring", level=3),
    mcq("Why keep a fixed evaluation set (questions + expected behaviour) and run it in CI on every prompt or model change?",
        ["It's a regression test suite: a prompt tweak that fixes one case can silently break others, and the eval set catches that before deploy",
         "It trains the model",
         "It reduces token cost in production",
         "It replaces production monitoring"], 0,
        "Prompts are code.",
        "Evals are the test suite of LLM apps. They complement, not replace, production monitoring, which sees real-world inputs the eval set lacks.",
        analogy="Evals = the test suite; a prompt change without evals is a deploy without tests.",
        topic="llm-monitoring", level=3),
    mcq("The provider silently updates the model behind the alias `model-latest`. What monitoring practice helps most?",
        ["Pin dated model versions, log the exact model version per request, and rerun the eval set on any version change; watch for shifts in output length, refusal rate and judge scores",
         "Nothing; providers guarantee identical behaviour",
         "Only watch latency",
         "Retrain your own model"], 0,
        "A dependency upgrade you didn't ship.",
        "Behaviour changes from upstream model updates are a real source of drift in LLM apps. Version pinning plus per-version metrics make them visible.",
        topic="llm-monitoring", level=4),
    mcq("How should you monitor for prompt-injection attempts in a production LLM app?",
        ["Flag and log inputs and retrieved content matching injection patterns or classifier hits, alert on spikes and on unexpected tool calls, and review samples; detection is imperfect, so it complements least-privilege design",
         "It can't be monitored at all",
         "Count tokens only",
         "Rely on the system prompt to block everything"], 0,
        "Watch both the inputs and what the model tries to do.",
        "Injection shows up in inputs (patterns, classifiers) and in behaviour (unusual tool calls, data exfiltration attempts). Alerts on behaviour are often more reliable than on text.",
        topic="llm-monitoring", level=4),
    mcq("Your LLM-as-judge groundedness score jumped from 0.82 to 0.91 overnight with no change to your app. What should you suspect first?",
        ["The judge itself changed (its model version or prompt), so the metric moved, not the app; pin and version the judge and recalibrate on a human-labelled set",
         "Your app got 10% better on its own",
         "Users asked easier questions; celebrate",
         "Latency improved"], 0,
        "Who watches the watcher?",
        "A judge is a model too and can drift. Version it, keep a fixed human-labelled calibration set, and treat judge changes like metric definition changes.",
        topic="llm-monitoring", level=4),

    # ------------------------------------------------------------------ alerting
    mcq("Why is getting 200 alerts a day a problem, even if some are real?",
        ["Alert fatigue: people start ignoring alerts, so real incidents get missed",
         "Alerts cost a lot of money each",
         "Too many alerts make the model less accurate",
         "It's not a problem"], 0,
        "Think of the boy who cried wolf.",
        "Every alert should be actionable. Noisy alerts train the team to ignore the pager.",
        topic="alerting", level=1),
    out("""import numpy as np

error_rate = np.array([1, 1, 2, 1, 9, 1, 1, 8, 9, 10])   # % per minute
window = 3
moving = np.convolve(error_rate, np.ones(window) / window, mode="valid")
alerts = np.where(moving > 5)[0] + window - 1
print(alerts.tolist())""",
        ["[8, 9]", "[4, 7, 8, 9]", "[4, 8, 9]", "[]"], 0,
        "A 3-minute average smooths out a single spike.",
        "The lone spike at minute 4 averages to 4.0 and doesn't alert; the sustained rise at minutes 7-9 does (averages 6.0 and 9.0). Smoothing trades a little delay for far fewer false alarms.",
        topic="alerting", level=2),
    out("""p_false_alarm = 0.05      # per feature per day, when nothing has drifted
features = 100
print(round(features * p_false_alarm, 1), round(1 - (1 - p_false_alarm) ** features, 3))""",
        ["5.0 0.994", "0.05 0.05", "5.0 0.5", "100 1.0"], 0,
        "Each test independently has a 5% chance of a fluke.",
        "Expect ~5 false drift alerts every day and a 99.4% chance of at least one, with zero real drift. Use effect-size thresholds, corrections (Bonferroni), or alert only on important features.",
        topic="alerting", level=3),
    mcq("Which alert is the most actionable?",
        ["'PSI > 0.25 on top-5 features for 2 consecutive days, AND predicted positive rate outside its band': linked to a runbook",
         "'Any feature's KS p-value < 0.05'",
         "'CPU above 40%'",
         "'A user clicked thumbs down'"], 0,
        "Important features, effect size, persistence, a runbook.",
        "Good alerts are tied to impact, use effect sizes, require persistence, and say what to do next. The others fire constantly or on noise.",
        topic="alerting", level=3),
    tf("Replacing user emails with their SHA-256 hash in logs makes the logs fully anonymous.", False,
       "Could someone hash a list of known emails and compare?",
       "Hashes of guessable values (emails, phone numbers) can be reversed by hashing candidates and matching. That's pseudonymisation at best; use keyed hashing, tokenisation, or don't log them, with access control and retention limits.",
       topic="alerting", level=4),
    out("""import re

log = "user rahul.k@example.com asked to call +91 98765 43210 about order 5512"
log = re.sub(r"[\\w.]+@[\\w.]+", "<EMAIL>", log)
log = re.sub(r"\\+?\\d[\\d ]{8,}\\d", "<PHONE>", log)
print(log)""",
        ["user <EMAIL> asked to call <PHONE> about order 5512",
         "user <EMAIL> asked to call +91 98765 43210 about order 5512",
         "user <EMAIL> asked to call <PHONE> about order <PHONE>",
         "user rahul.k@example.com asked to call <PHONE> about order 5512"], 0,
        "The phone pattern needs at least 10 characters of digits/spaces.",
        "Both PII values are masked before the line is stored; the short order number survives. Redact at write time: logs get copied to many systems and are hard to clean later.",
        topic="alerting", level=4),

    # ---------------- round 2 additions ----------------
    tf("A deployed model can get worse even though nobody changed its code, its weights or its server.",
        True,
        "The model stays the same; what else can change?",
        "The world the model sees keeps changing: new users, new products, new fraud tactics, an upstream team editing a feature. A frozen model on moving data slowly decays. That is the core reason ML needs monitoring beyond 'is the service up?'.",
        analogy="Like a street map printed in 2020: the paper hasn't changed, but the city has.",
        topic="why-ml", level=1),
    mcq("Which of these is a 'silent failure' of an ML service?",
        ["The API keeps returning 200 OK with confident predictions, but a renamed upstream column means one feature is now always zero",
         "The server crashes and returns HTTP 500",
         "The container fails its health check and restarts",
         "Requests time out after 30 seconds"], 0,
        "Which one would no ordinary uptime alert catch?",
        "Crashes, 500s and timeouts trip normal alerts. A broken feature still produces numbers, so the service looks healthy while predictions are wrong. Catching it needs data checks (null/zero rates, ranges) and prediction-distribution monitors.",
        topic="why-ml", level=1),
    fill("Fill in the blank: a model that keeps returning HTTP 200 with wrong answers is said to fail ____ (one word).",
        "silently",
        "No error, no crash, no log line.",
        "Silent failure is the defining problem of ML monitoring: nothing throws, so you need probes for correctness (data checks, prediction drift, labels, proxies), not just for availability.",
        topic="why-ml", level=2),
    tf("Data drift means the distribution of the model's inputs has changed compared with the data it was trained on.",
        True,
        "Drift of what, exactly?",
        "Data drift (covariate shift) = P(x) changes: new age groups, new devices, a new country. It is the easiest drift to see because inputs are available right away, with no labels needed. Whether it hurts accuracy is a separate question.",
        topic="drift-types", level=1),
    fill("Fill in the blank: when the same input now deserves a different answer, so P(y | x) has changed, it is called ____ drift.",
        "concept",
        "The meaning of the pattern changed, not the pattern.",
        "Concept drift: fraudsters change tactics, so a transaction that looked safe last year is now fraud. Input monitors cannot see it, because the inputs look the same; you need labels or proxies.",
        topic="drift-types", level=2),
    fill("Fill in the blank: KS, the two-sample drift test for numeric features, stands for Kolmogorov-____.",
        "Smirnov",
        "Two Russian mathematicians.",
        "The Kolmogorov-Smirnov test compares two samples by the largest gap between their cumulative distribution curves. In SciPy it is scipy.stats.ks_2samp. It is for continuous numbers; use chi-square for categories.",
        topic="drift-detection", level=1),
    fill("Fill in the blank: the real outcome you compare predictions against (did the customer actually churn?) is called the ground ____.",
        "truth",
        "Two words, the second one means 'what really happened'.",
        "Ground truth = the true labels. In production it often arrives late (chargebacks, loan defaults) or only for some cases, which is why monitoring leans on proxies and prediction distributions in the meantime.",
        topic="ground-truth", level=1),
    out("""import numpy as np

yesterday = np.array([0.1, 0.2, 0.15, 0.1, 0.2])   # predicted churn probabilities
today     = np.array([0.6, 0.7, 0.65, 0.5, 0.8])
print(round(float(yesterday.mean()), 2), round(float(today.mean()), 2))""",
        ["0.15 0.65", "0.15 0.15", "0.75 0.65", "0.65 0.15"], 0,
        "Average each day's predictions.",
        "The average predicted churn jumped from 0.15 to 0.65 overnight. You need no labels to see that: something changed (inputs, a pipeline bug, a new model). Monitoring the prediction distribution is the cheapest early warning you have.",
        topic="ground-truth", level=1),
    tf("Monitoring the distribution of a model's predictions requires waiting until the true labels arrive.",
        False,
        "Predictions exist the moment you make them.",
        "Prediction distributions (mean score, % positive, class mix) are available instantly. A sudden shift is a strong hint that inputs or the pipeline changed. Labels are needed to measure accuracy, not to notice that the model's behaviour moved.",
        topic="ground-truth", level=2),
    fill("Fill in the blank: an alert that fires when nothing is wrong is a false positive; staying silent during a real incident is a false ____.",
        "negative",
        "The opposite kind of mistake.",
        "Alert design trades the two: tight thresholds give false positives (fatigue, ignored pages), loose ones give false negatives (missed incidents). Same confusion-matrix thinking you use for the model itself, applied to the monitor.",
        topic="alerting", level=1),
    mcq("Which statement about the 'reference' (baseline) dataset in drift monitoring is right?",
        ["It is the data you compare live traffic against, usually the training set or a known-good recent production window, and the choice changes what 'drift' means",
         "It must always be the most recent hour of live traffic",
         "It is the test set used once to report accuracy, and it is never used again",
         "Drift monitoring does not need a reference"], 0,
        "Drift is always 'different from WHAT?'.",
        "Against the training set you ask 'is this still the world the model learned?'. Against last month's traffic you ask 'did something change recently?'. Teams often keep both: a fixed training reference to catch slow drift and a rolling one to catch sudden breaks.",
        topic="windows", level=2),
    fill("Fill in the blank: the fixed dataset you compare live data against in a drift check is called the ____ dataset (also 'baseline').",
        "reference",
        "Tools like Evidently call it 'reference_data'.",
        "Reference vs current is the standard framing: drift tools take a reference dataset and a current window and compare them feature by feature. Version the reference like code, so a drift score is reproducible.",
        topic="windows", level=2),
    tf("Alerting on every metric that moves is the safest monitoring setup, because it guarantees nothing is missed.",
        False,
        "What do people do with a pager that rings 200 times a day?",
        "Too many alerts train people to ignore them, so real incidents get missed: alert fatigue. Page only on a few actionable, user-impacting signals; put the rest on dashboards or in daily reports.",
        topic="alerting", level=2),
    out("""import pandas as pd

train_devices = {"android", "ios", "web"}
live = pd.Series(["ios", "android", "web", "smart_tv", "ios", "smart_tv", "car", "web"])
unseen = ~live.isin(train_devices)
print(unseen.sum(), round(unseen.mean(), 2))""",
        ["3 0.38", "2 0.25", "5 0.62", "3 0.03"], 0,
        "isin checks membership; ~ flips it.",
        "smart_tv twice and car once are new categories: 3 of 8 rows, 0.38 (37.5% rounded). A one-hot encoder fitted on training data maps unseen categories to all-zeros (or errors), so a rising 'unseen category' rate is a data-quality alarm, not something drift tests on known categories will show.",
        topic="data-quality", level=2),
    fill("Fill in the blank: in Great Expectations a single rule about data, like 'column age is between 0 and 120', is called an ____.",
        "expectation",
        "The tool is named after it.",
        "Expectations are unit tests for data: run them as a pipeline gate before training or scoring, and fail the batch (or quarantine it) when they break, the same way a failing test blocks a deploy.",
        topic="data-quality", level=2),
    fill("Fill in the blank: when an A/B test planned 50/50 actually gets 52/48 users, far beyond chance, it is called a sample ratio ____.",
        "mismatch",
        "Abbreviated SRM.",
        "A sample ratio mismatch means assignment or logging is broken (bots filtered on one side, a redirect that drops users). Results from an SRM test cannot be trusted, so check the split with a chi-square test before reading any metric.",
        topic="online-eval", level=2),
    tf("Monitoring average output tokens per request can catch a prompt change that quietly makes answers longer and more expensive.",
        True,
        "Output tokens are the pricier ones.",
        "A prompt edit like 'explain your reasoning' can double output length, so cost and latency jump while answers still look fine. Track tokens in and out per feature and per prompt version, and alert on a step change.",
        topic="llm-monitoring", level=2),
    out("""requests_per_day = 20_000
avg_in, avg_out = 1_500, 400          # tokens
price_in, price_out = 0.40, 1.60      # USD per 1M tokens
daily = requests_per_day * (avg_in * price_in + avg_out * price_out) / 1e6
print(round(daily, 2), round(daily * 30))""",
        ["24.8 744", "12.0 360", "24.8 248", "2480.0 74400"], 0,
        "Per request: 1,500 x 0.40 + 400 x 1.60 micro-dollars.",
        "Per request (1500 x 0.40 + 400 x 1.60) / 1e6 = $0.00124; x 20,000 = $24.80/day, about $744/month. Output is 21% of the tokens but more than half the cost. A cost dashboard per feature turns 'the bill doubled' into 'summarise started sending 3x more context on Tuesday'.",
        topic="llm-monitoring", level=2),
    mcq("Why should an LLM app record token counts for every request, not only total monthly spend?",
        ["Cost and latency scale with tokens, so per-request counts show WHICH feature, prompt version or user drives the bill and catch runaway requests early",
         "Providers require it by law",
         "Token counts measure answer quality directly",
         "Monthly totals are always accurate enough"], 0,
        "A monthly invoice says 'how much', not 'why'.",
        "Per-request tokens (in and out), tagged with feature, prompt version and model, let you slice cost like any other metric, spot a single agent stuck in a loop, and set per-request caps. It is like per-endpoint latency metrics versus one server-wide average.",
        topic="llm-monitoring", level=1),
    out("""import numpy as np

rng = np.random.default_rng(0)
ref = rng.normal(0, 1, 10_000)
live = rng.normal(0.5, 1, 10_000)
edges = np.quantile(ref, np.linspace(0, 1, 11))   # 10 equal-count bins
edges[0], edges[-1] = -np.inf, np.inf
e = np.histogram(ref, edges)[0] / len(ref)
a = np.histogram(live, edges)[0] / len(live)
psi = np.sum((a - e) * np.log(a / e))
print(round(float(e[0]), 2), round(float(psi), 2))""",
        ["0.1 0.24", "0.1 0.0", "0.5 0.24", "0.1 2.4"], 0,
        "Quantile edges put 10% of the reference in each bin.",
        "Bins from reference deciles give expected shares of 0.1 each; a half-standard-deviation shift moves mass into the upper bins and PSI comes out about 0.24, the top of the 'moderate' band. The open-ended outer edges (-inf, inf) catch live values outside the training range, which fixed edges would silently drop.",
        diagram="""
 ref bins   |10%|10%|10%|10%|10%|10%|10%|10%|10%|10%|
 live share | 4 | 5 | 6 | 8 | 8 |11 |11 |12 |14 |22 |
 PSI = sum (a - e) * ln(a / e)  ~ 0.24
""",
        topic="drift-detection", level=3),
    out("""import numpy as np
from scipy.stats import ks_2samp

ref = np.array([1, 2, 3, 4, 5, 6, 7, 8])
live = np.array([3, 4, 5, 6, 7, 8, 9, 10])
grid = np.union1d(ref, live)
cdf = lambda s: np.searchsorted(np.sort(s), grid, side="right") / len(s)
by_hand = np.abs(cdf(ref) - cdf(live)).max()
print(float(by_hand), float(ks_2samp(ref, live).statistic))""",
        ["0.25 0.25", "0.25 0.5", "2.0 0.25", "0.125 0.125"], 0,
        "At x = 2 the reference has 2/8 below or equal, the live sample has 0/8.",
        "The KS statistic is the biggest vertical gap between the two empirical CDFs. Here live is the reference shifted by 2, and the gap peaks at 2/8 = 0.25 (e.g. at x = 2 and x = 8). Computing it by hand once makes the scipy number meaningful: 0.25 means 'at some threshold, 25% of one sample is on a different side than the other'.",
        topic="drift-detection", level=3),
    tf("The PSI value you get for the same two samples depends on how you choose the bins.",
        True,
        "Try 3 bins versus 30 bins in your head.",
        "PSI sums over bins, so more or narrower bins usually give a larger value, and empty bins blow it up. The 0.1/0.25 thresholds assume roughly 10 equal-population bins from the reference. Fix the binning (store the edges with the reference) or your drift scores are not comparable over time.",
        topic="drift-detection", level=3),
    fill("Fill in the blank (one word): by the usual rule of thumb, a PSI of 0.18 means a ____ shift.",
        "moderate",
        "Below 0.1 stable, above 0.25 significant.",
        "0.1-0.25 is the 'moderate, investigate' band: look at which bins moved and whether performance proxies moved, before deciding to retrain. Treat the thresholds as conventions, not laws; they depend on binning and sample size.",
        topic="drift-detection", level=3),
    out("""import pandas as pd

ref_mean = 50.0
daily = pd.Series([49, 51, 50, 52, 58, 61, 63, 64],
                  index=pd.date_range("2026-01-01", periods=8))
rolling = daily.rolling(3).mean()
flag = (rolling - ref_mean).abs() > 5
print(flag.idxmax().day, round(float(rolling.iloc[-1]), 1))""",
        ["6 62.7", "5 62.7", "3 64.0", "6 64.0"], 0,
        "The first two rolling values are NaN; NaN > 5 is False.",
        "3-day means: 50, 51, 53.3, 57, ... The first one more than 5 away from 50 is 57 on Jan 6, though the raw value jumped on Jan 5. A rolling window smooths noise but adds detection delay of about half the window; idxmax on a boolean Series returns the first True.",
        topic="windows", level=3),
    tf("A smaller monitoring window (say 1 hour instead of 1 day) detects sudden changes faster but raises more false alarms.",
        True,
        "Fewer samples per window means noisier statistics.",
        "Short windows react quickly but have few samples, so drift scores and error rates bounce around. Long windows are stable but slow. Common practice: a short window with a high threshold for big breaks plus a long window with a low threshold for slow drift, like multi-window SLO alerts.",
        topic="windows", level=3),
    mcq("A food-delivery model's drift monitor compares each day's inputs with the previous day. It alerts every Saturday and Monday. Nothing is broken. What is the best fix?",
        ["Account for seasonality: compare each day with the same weekday in past weeks (or a reference covering full weeks) so normal weekly patterns don't count as drift",
         "Raise the threshold until the weekend alerts stop",
         "Turn off drift monitoring on weekends",
         "Retrain the model every Saturday"], 0,
        "What is different about Saturday compared with Friday, every week?",
        "Weekend traffic looks different every week, so day-over-day comparison flags a normal cycle. Choose references that contain the same seasonality (same weekday last week, a 4-week rolling baseline). Raising the threshold would also hide real drift.",
        diagram="""
 orders  Mon Tue Wed Thu Fri Sat Sun Mon
         ##  ##  ##  ##  ### #### ### ##
 day-over-day:            !    !       !   <- false alarms
 same-weekday ref: no alarm unless the pattern itself moves
""",
        topic="windows", level=3),
    tf("Using a sliding baseline (always comparing this week with last week) can hide slow, gradual drift.",
        True,
        "Each week differs only a little from the one before.",
        "If a feature creeps 2% a week, every week-over-week check looks fine, while after six months it is far from the training data. Keep a fixed training reference alongside the sliding one, the way you track both day-over-day and year-over-year in business metrics.",
        analogy="Like the boiling frog: each degree feels the same as the last one.",
        topic="windows", level=4),
    out("""import numpy as np

pred_day = np.arange(1, 61)          # one batch of predictions per day, days 1..60
label_delay = 30                     # labels arrive 30 days after the prediction
today = 45
matured = pred_day + label_delay <= today
print(int(matured.sum()), round(float(matured.mean()), 2))""",
        ["15 0.25", "45 0.75", "30 0.5", "60 1.0"], 0,
        "A day-d batch is labelled on day d + 30.",
        "Only batches from days 1-15 have labels by day 45: 15 of 60, 25%. Your 'current accuracy' is really accuracy from 30+ days ago, so anything that broke last week is invisible to it. Always report labelled metrics by prediction date (cohort) and pair them with label-free monitors for recent days.",
        topic="ground-truth", level=3),
    out("""slo = 0.999
error_rate_last_hour = 0.0144
burn_rate = error_rate_last_hour / (1 - slo)
budget_used_pct = burn_rate * 1 / (30 * 24) * 100     # 1 hour out of 30 days
print(round(burn_rate, 1), round(budget_used_pct, 1))""",
        ["14.4 2.0", "1.4 0.2", "14.4 14.4", "0.0 0.0"], 0,
        "Burn rate = observed error rate / allowed error rate.",
        "The SLO allows 0.1% errors; 1.44% is 14.4x that. Burning at 14.4x for one hour uses 14.4 / 720 hours = 2% of the 30-day budget. That is the classic 'page now' threshold from SRE practice: at this pace the whole month's budget is gone in about 2 days.",
        topic="system-metrics", level=3),
    out("""import numpy as np

psi = np.array([0.05, 0.31, 0.04, 0.06, 0.27, 0.29, 0.33, 0.08])   # per hour
breach = psi > 0.25
single = int(breach.sum())
# alert only when 3 consecutive hours breach
three_in_row = int(sum(breach[i:i+3].all() for i in range(len(breach) - 2)))
print(single, three_in_row)""",
        ["4 1", "4 2", "1 1", "4 0"], 0,
        "Hours 5, 6 and 7 (0-based 4, 5, 6) breach together.",
        "A single-hour rule fires 4 times, including the lone spike at hour 2. Requiring 3 consecutive breaches fires once, for the sustained shift. 'N of M windows' rules are a cheap way to cut false alarms at the cost of a little detection delay.",
        topic="alerting", level=3),
    fill("Fill in the blank (decimal): you test 50 features for drift each day and want an overall false-alarm rate of about 5%. With a Bonferroni correction, each feature's p-value threshold is ____.",
        "0.001",
        "Divide alpha by the number of tests.",
        "0.05 / 50 = 0.001. Bonferroni is conservative (it can miss real but small drift), but it turns 'about 2.5 false alarms per day' into 'about one every 20 days'. Alternatives: Benjamini-Hochberg (controls false discovery rate) or alerting on effect size plus importance-weighted features.",
        topic="alerting", level=3),
    out("""requests_per_day = 50_000
sample_rate = 0.02
judge_tokens = 2_500                 # prompt + answer + context sent to the judge
price_per_m = 1.00                   # USD per 1M judge tokens
judged = int(requests_per_day * sample_rate)
monthly = judged * judge_tokens * price_per_m / 1e6 * 30
print(judged, round(monthly, 2))""",
        ["1000 75.0", "1000 2.5", "50000 3750.0", "100 7.5"], 0,
        "1,000 judged x 2,500 tokens = 2.5M tokens a day.",
        "2% of 50,000 = 1,000 judged answers a day; 2.5M tokens/day at $1/M = $2.50/day, $75/month. Sampling makes LLM-as-judge quality monitoring affordable; judging 100% would cost $3,750/month and add latency if done inline. Run judges asynchronously, off the request path.",
        topic="llm-monitoring", level=3),
    fill("Fill in the blank (whole dollars): 1,000 requests/day, you judge a 5% sample, and each judge call costs $0.002. Over 30 days the judge costs about $____.",
        "3",
        "50 calls a day.",
        "1,000 x 0.05 = 50 judged per day x $0.002 = $0.10/day, $3 per 30 days. At low traffic you can afford a much higher sample rate; at high traffic a fixed number of judged answers per day (stratified by feature) keeps cost flat.",
        topic="llm-monitoring", level=3),
    tf("Reviewing only the conversations that got a thumbs-down gives an unbiased estimate of the app's overall hallucination rate.",
        False,
        "Who presses thumbs-down, and on which answers?",
        "Thumbs-down answers are a self-selected, very biased sample: most users never vote, and wrong answers that sound right get no downvote. Use them to find failure examples, but estimate rates from a RANDOM sample of all traffic judged the same way.",
        topic="llm-monitoring", level=3),
    tf("Keeping a small random-exploration slice (say 2% of traffic gets a non-personalised ranking) usually costs a little short-term engagement.",
        True,
        "Random choices are, on average, worse than the model's choices.",
        "Exploration is a deliberate cost: those users get slightly worse recommendations. In return you get unbiased data to evaluate and retrain on, and a way to discover items the model never shows. Teams size it as small as possible and treat it like an insurance premium.",
        topic="feedback-loops", level=3),
    tf("A model retrained on the latest data is always better than the model currently in production, so it can be deployed without comparison.",
        False,
        "What if the latest data is broken, or too small?",
        "Recent data can hold pipeline bugs, a holiday spike, or labels that are not settled yet. Every retrained challenger must beat the champion on a held-out recent set (plus slice checks) before promotion, then go through canary like any deploy.",
        topic="retraining", level=3),
    mcq("A team says 'the model drifted' because the served values of feature `amount` differ from what the training pipeline computes for the SAME transactions. What is this, and how do you tell it apart from drift?",
        ["Training-serving skew: the two code paths compute the feature differently; compare logged served features with the training pipeline's output for the same IDs (row by row), whereas drift compares different time periods",
         "Concept drift; retrain the model",
         "Label shift; reweight the classes",
         "Normal noise; nothing to do"], 0,
        "Same rows, different values, so time is not the cause.",
        "Drift is the world changing between periods; skew is your two pipelines disagreeing about the same event. The test for skew is a join: served features (logged at request time) vs offline-computed features keyed by request ID. Retraining does not fix skew, because the next model will be served through the same broken path.",
        topic="data-quality", level=3),
    mcq("Why do teams log the exact feature vector at prediction time instead of recomputing features later from the raw tables when labels arrive?",
        ["Raw tables change (late updates, backfills, corrected values), so recomputing later leaks future information and does not reproduce what the model actually saw; logged features give point-in-time correct training and debugging data",
         "Logging is cheaper than computing",
         "Recomputed features are always identical, so it makes no difference",
         "Regulations forbid recomputing features"], 0,
        "Is 'the customer's balance' the same value today as at 10:03 last Tuesday?",
        "Recomputing a feature after the fact gives its CURRENT value, not the value at decision time, which leaks future information into training and hides skew. Logging served features (or using a feature store with point-in-time joins) is like event sourcing: keep the facts as they were, not a later snapshot.",
        topic="data-quality", level=3),
    mcq("A categorical feature `device` is one-hot encoded with `handle_unknown='ignore'`. A new app version sends 'android_tv', which the encoder never saw. What happens and what should monitoring catch?",
        ["The row is encoded as all zeros for device, so the model silently treats it like no device at all; monitor the unseen-category rate per feature",
         "sklearn raises an error for every such request",
         "The encoder adds a new column automatically",
         "The value is mapped to the most frequent device"], 0,
        "'ignore' means no error, not 'handled well'.",
        "With handle_unknown='ignore', unknown categories become an all-zero block: no exception, just a quietly odd input. If 30% of traffic moves to a new device name, predictions shift with no alert. Track the share of unseen categories as a data-quality metric next to null rates.",
        topic="data-quality", level=3),
    mcq("A news recommender is retrained on click logs. Items in slot 1 get 10x the clicks of slot 5. Why is 'clicked = relevant' a biased training label here?",
        ["Position bias: users click top slots partly because they are on top, so the logs reward whatever the old model ranked first; correct with position-aware models, randomised slots, or inverse-propensity weighting",
         "Clicks are always a perfect relevance label",
         "Slot 5 items are always worse, so the labels are fine",
         "Click logs have no bias if the dataset is large enough"], 0,
        "Would the same article get the same clicks in slot 5?",
        "The model's own ranking decides exposure, and exposure drives clicks: a feedback loop. Without correction the retrained model learns 'what the old model liked' more than 'what users like'. More data does not remove a systematic bias.",
        topic="feedback-loops", level=3),
    mcq("A drift-triggered retraining job fires on PSI > 0.2. During a two-week promotion, PSI bounces around 0.2 and the pipeline retrains and redeploys 9 times. What is the best design fix?",
        ["Add hysteresis and gates: require the breach to persist, use a cool-down between retrains, and promote only if the challenger beats the champion on recent labelled data",
         "Lower the threshold to 0.1 so it is more sensitive",
         "Retrain every hour instead",
         "Remove the champion/challenger gate to deploy faster"], 0,
        "A thermostat with no dead band switches on and off constantly.",
        "Triggers on a noisy signal flap. Persistence (N windows in a row), a cool-down and a dead band (trigger at 0.25, reset below 0.15) stop the thrash. A temporary promotion may not even need a new model, and each churned deploy adds risk and cost for no gain.",
        analogy="Like a thermostat without a dead band: it clicks the heater on and off every few seconds.",
        topic="retraining", level=3),
    out("""import numpy as np

def psi(e, a):
    return float(np.sum((a - e) * np.log(a / e)))

e = np.array([0.6, 0.3, 0.1])
a = np.array([0.3, 0.3, 0.4])
print(round(psi(e, a), 3), round(psi(a, e), 3))""",
        ["0.624 0.624", "0.624 0.347", "0.347 0.624", "0.624 -0.624"], 0,
        "Swap e and a: both factors (a - e) and ln(a / e) flip sign.",
        "PSI is symmetric: swapping the samples flips the sign of both (a - e) and ln(a/e), so each term is unchanged. In fact PSI = KL(a||e) + KL(e||a), the symmetrised KL divergence. So, unlike KL, it does not matter which side you call 'reference', but it is still infinite on empty bins.",
        topic="drift-detection", level=4),
    tf("The two-sample KS test is most sensitive to differences in the tails of a distribution and least sensitive near the median.",
        False,
        "Where can two CDFs be furthest apart?",
        "It is the reverse. Both CDFs are pinned to 0 and 1 at the extremes, so gaps there are small and the KS statistic mostly reacts to shifts near the middle. For tail changes (e.g. more very large transactions) use Anderson-Darling, quantile checks (p99 of the feature) or tail-focused bins in PSI.",
        topic="drift-detection", level=4),
    fill("Fill in the blank (whole number): with log base 2, the Jensen-Shannon divergence between two distributions is at most ____.",
        "1",
        "It is bounded, unlike KL.",
        "JS divergence lies in [0, 1] with base-2 logs (and [0, ln 2] with natural logs); it hits the maximum when the two distributions do not overlap at all. Bounded, symmetric scores are easy to threshold and compare across features, unlike KL, which can be infinite.",
        topic="drift-detection", level=4),
    mcq("Every feature passes its univariate drift test, but the model's error rate doubles. Investigation shows that 'age' and 'income' used to be strongly correlated and now are not. Which monitor would have caught this?",
        ["A multivariate check, e.g. a domain classifier trained to tell reference rows from live rows (AUC well above 0.5 means the joint distribution moved), or monitoring the model's own score distribution",
         "Running the same KS tests with a lower p-value threshold",
         "Checking each feature's mean and standard deviation more often",
         "A chi-square test on each feature separately"], 0,
        "Each marginal is unchanged; the relationship between features changed.",
        "Univariate tests look at one column at a time and cannot see a change in how columns move together. A 'reference vs live' classifier sees all features jointly, and its feature importances show what changed. PCA reconstruction error is another multivariate option.",
        diagram="""
 reference          live
 income             income
  |      . .         | .    .  .
  |   . .            |    .  .
  | . .              |  .  .   .
  +------- age       +------- age
 same marginals, different joint
""",
        topic="drift-detection", level=4),
    out("""tpr, fpr = 0.90, 0.05      # the model itself does not change

def precision(prevalence):
    tp = tpr * prevalence
    fp = fpr * (1 - prevalence)
    return round(tp / (tp + fp), 2)

print(precision(0.10), precision(0.01))""",
        ["0.67 0.15", "0.67 0.67", "0.9 0.9", "0.15 0.67"], 0,
        "False positives come from the big negative class.",
        "Same TPR and FPR, but when positives fall from 10% to 1%, precision drops from 0.67 to 0.15, because false positives now outnumber true ones. That is label (prior) shift: the model is unchanged, yet the alert queue fills with false alarms. Monitor the predicted-positive rate and, when labels arrive, precision by cohort.",
        topic="drift-types", level=4),
    mcq("A loan model's 'early accuracy' is computed from labels that have arrived so far. In the first month it looks great, then steadily worsens as more labels arrive. No real change happened. Why?",
        ["Early labels are not a random sample: defaults that happen fast (and the loans that pay off early) arrive first, so early metrics come from a biased subset; compare cohorts at the same label age",
         "The model is overfitting to new labels",
         "Accuracy always gets worse over time by definition",
         "The label pipeline randomly drops rows"], 0,
        "Which outcomes can be known after 30 days?",
        "With delayed labels, the label you can observe depends on time. Comparing a 1-month-old cohort with a 12-month-old one mixes label maturity with model quality. Use 'accuracy at 90 days of label age' curves (vintage analysis), the same idea credit teams use for default rates.",
        topic="ground-truth", level=4),
    out("""import math

p, delta = 0.10, 0.01           # baseline conversion, smallest lift worth detecting
n_per_arm = 16 * p * (1 - p) / delta ** 2   # rule of thumb: 80% power, alpha 0.05
print(round(n_per_arm))""",
        ["14400", "1440", "144", "900"], 0,
        "16 x 0.09 / 0.0001.",
        "About 14,400 users per arm to detect a 1-point lift on 10% conversion. Halving the detectable lift quadruples the sample (delta is squared). Running 'for a week and seeing' without this arithmetic is how teams declare noise a win, or kill a good model that never had enough traffic.",
        topic="online-eval", level=4),
    out("""import math

n, flagged = 200, 16            # judged answers, unsupported ones
p = flagged / n
half = 1.96 * math.sqrt(p * (1 - p) / n)
print(p, round(p - half, 3), round(p + half, 3))""",
        ["0.08 0.042 0.118", "0.08 0.08 0.08", "0.08 0.079 0.081", "16 14 18"], 0,
        "Standard error of a proportion = sqrt(p(1-p)/n).",
        "8% unsupported answers, but with only 200 judged samples the 95% interval is about 4% to 12%. A dashboard showing '8% -> 10% hallucination' week over week is well within noise. Report rates with intervals, and size the judged sample for the change you need to see.",
        topic="llm-monitoring", level=4),
    out("""alpha, features = 0.05, 100
p_any = 1 - (1 - alpha) ** features
bonf = alpha / features
p_any_bonf = 1 - (1 - bonf) ** features
print(round(p_any, 3), bonf, round(p_any_bonf, 3))""",
        ["0.994 0.0005 0.049", "0.05 0.0005 0.05", "0.994 0.05 0.994", "5.0 0.0005 0.05"], 0,
        "P(at least one false alarm) = 1 - P(no false alarm on any feature).",
        "With 100 independent tests at 0.05, a drift-free day still fires at least one alert 99.4% of the time. A Bonferroni threshold of 0.0005 brings the family-wise rate back to about 4.9%. That is why 'test every feature at p < 0.05' dashboards are always red, and why people stop looking at them.",
        topic="alerting", level=4),
    fill("Fill in the blank (whole number, percent): an SLO-based page fires when the 1-hour burn rate is 14.4. Burning at that rate for 1 hour uses about ____% of a 30-day error budget.",
        "2",
        "A 30-day month has 720 hours.",
        "14.4 x 1 / 720 = 0.02, so 2% of the budget per hour; at that pace the month's budget is gone in about 50 hours. That is why the classic multi-window SLO alert pages on 14.4x over 1 hour (with a 5-minute check that it is still happening) and opens a ticket on slower burns like 1x over 3 days.",
        topic="system-metrics", level=4),
    mcq("You replace 'alert if error rate > 1% for 5 minutes' with multi-window burn-rate alerts on a 99.9% SLO. What problem does the pair of windows (e.g. 1 hour AND 5 minutes both above 14.4x) solve?",
        ["The long window makes sure enough budget was burned to matter (no paging on a 30-second blip); the short window makes the alert stop soon after the problem is fixed",
         "It doubles the number of alerts so nothing is missed",
         "It removes the need for an SLO",
         "It averages p99 latency correctly across hosts"], 0,
        "One window controls significance, the other controls reset time.",
        "A long window alone keeps firing for an hour after recovery; a short window alone pages on every spike. Requiring both gives precision (it mattered) and fast reset (it is still happening). The same idea transfers to ML signals: 'drift high over a day AND still high in the last hour'.",
        topic="alerting", level=4),
    fill("Fill in the blank: to evaluate a new policy offline from old logs, you weight each logged outcome by 1 / (probability the old policy chose that action). That probability is called the ____.",
        "propensity",
        "As in inverse ____ scoring (IPS).",
        "Inverse propensity scoring re-weights logged data as if the new policy had chosen the actions. It only works if the old policy logged its probabilities AND gave every action some non-zero chance; a purely greedy old policy leaves actions with propensity 0 that you can never evaluate. That is why exploration and logging propensities go together.",
        topic="feedback-loops", level=4),
    mcq("An agentic LLM feature's daily cost triples overnight while request count is flat and average latency barely moves. Which monitoring would find the cause fastest?",
        ["Per-request token and tool-call counts with their p99 and max, broken down by feature and prompt version: a few requests stuck in a tool loop or with huge context dominate cost but hardly move the average latency",
         "The overall average tokens per request only",
         "Server CPU utilisation",
         "The HTTP error rate"], 0,
        "A cost spike with flat traffic means some requests got much bigger.",
        "Cost is heavy-tailed: one agent looping 200 tool calls costs as much as thousands of normal requests. Track distributions (p99, max) per request, set hard caps (max steps, max tokens, budget per session) and alert on tail growth. It is like finding the N+1 query that blows up your DB bill: averages hide it.",
        topic="llm-monitoring", level=4),
    mcq("A ride-hailing company A/B tests a new pricing model by randomising riders. Treatment riders book more, and the test shows a big win. After full launch, total bookings barely change. What most likely went wrong?",
        ["Interference: both groups competed for the same drivers, so treatment gained partly by taking supply from control; use cluster or switchback randomisation (by city or time slot)",
         "The test had a sample ratio mismatch",
         "The novelty effect always reverses at launch",
         "The model overfitted to the treatment group"], 0,
        "Do treatment and control share a limited resource?",
        "A/B tests assume one user's treatment doesn't affect another's outcome (SUTVA). In two-sided markets that fails: a 'win' can be a transfer from control. Randomise whole markets or alternate treatment by time slot (switchback), accepting more variance for an unbiased answer.",
        topic="online-eval", level=4),
    tf("Training-serving skew can exist even when the served and training distributions of a feature look identical in aggregate.",
        True,
        "Distributions compare groups; skew is about individual rows.",
        "If serving computes 'hour of day' in UTC and training in local time, values are shuffled per row while the overall histogram looks similar. Aggregate drift tests pass, yet each prediction gets the wrong input. Only a row-level comparison of logged served features against offline features for the same IDs catches it.",
        topic="data-quality", level=4),
    mcq("You design monitoring windows for a fraud model that scores 2,000 transactions a day with a fraud rate of 0.2%. Which choice is most defensible for monitoring precision once labels arrive?",
        ["Aggregate labelled outcomes over weeks (about 4 frauds a day is far too few for a daily precision), report intervals, and use daily label-free monitors (score distribution, flag rate) for fast detection",
         "Compute precision every hour so problems show up quickly",
         "Daily precision is fine because 2,000 rows is a large sample",
         "Skip precision entirely; only accuracy matters"], 0,
        "How many positive cases does a day contain?",
        "A metric's sample size is the number of relevant events, not rows: 0.2% of 2,000 is about 4 frauds a day, so daily precision jumps between 0% and 100% by chance. Use longer windows (or pooled cohorts) for label-based metrics and keep fast windows for high-volume, label-free signals.",
        topic="windows", level=4),
]
