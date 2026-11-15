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
]
