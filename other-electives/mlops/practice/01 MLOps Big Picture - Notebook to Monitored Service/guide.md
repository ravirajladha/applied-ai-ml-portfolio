# MLOps 01 — The big picture: notebook model → monitored service

**MLOps · Topic 01 · first pass through all 8 modules** · ⏱️ about 4–5 hours (explainer 1 h · notebook 2 h · codebase tour 1 h · recall 30 min)

| File | What it is |
|------|------------|
| `explainer.html` | **Open first.** Clickable lifecycle (the 8 modules), the three things that change, the skew demo, a registry stepper, a batch-vs-online chooser, a **live drift slider with PSI**, shadow/canary/A-B visual, and an 8-question quiz. |
| `practice.ipynb` | 12 cells, 13 short `# TODO` lines, each with `assert` checks. Walks the DeliverEase story end to end. |
| `guide.md` | This file. |
| `../../codebase/` | The real project. Each notebook cell names the file where its idea lives. Run `pytest -q` there: 15 tests. |
| `../../cards.json` | Flashcards for this topic (and later topics). |

---

## The story (rung ② · scenario)

**DeliverEase** shows "arrives in 34 min" at checkout. A gradient-boosting model predicts it from distance, items,
kitchen prep time, rain and peak hour.

| Day | What happens | Module | Numbers |
|-----|--------------|--------|---------|
| Mon | Look at 2,000 past orders; baseline "predict the average" | M1, M3 | baseline MAE **9.2 min** |
| Tue | Train two runs, track them, register the best, pass the gate, go live as v1 | M3, M4 | MAE **2.6 min** (72% better) |
| Wed | API answers checkout requests; nightly batch scores tomorrow's orders | M5 | ~2 ms per prediction |
| Jul 1 | Monsoon: drift alert on `is_raining` (PSI 1.73) and `prep_min` (PSI 1.36), no labels needed | M6 | PSI > 0.25 = alert |
| Jul 2 | Real delivery times arrive: v1 is now **10.9 min** wrong (concept drift) | M6 | 4× worse |
| Jul 2 | Pipeline retrains on monsoon data; challenger 2.6 vs champion 11.0 on the same fresh data → v2 promoted | M4, M7 | v1 archived |
| Jul 3 | Canary: 10% of orders get v2, then ramp up | M7 | ~10% routed |

---

## Warm-up (rung ⑤ · recall from earlier courses)

Answer out loud before starting. These come from courses you've already done:
1. *(SE4ML S2)* Why is the ML code only a small box in a real ML system?
2. *(SE4ML S12)* Name one data test and one model test.
3. *(SE4ML S14)* Batch vs real-time serving: one example of each.

---

## Plain-English recap (rung ① words, same as `cards.json`)

| Term | One line |
|------|----------|
| **MLOps** | DevOps practices plus versioning, testing and monitoring of data and models, so ML stays reliable in production. |
| **Baseline** | The simplest possible predictor (e.g. always the average); a real model must clearly beat it. |
| **Training-serving skew** | Production computes inputs differently from training, so the model sees data it never learned from. |
| **Experiment tracking** | Recording every training run's params, data version, metrics and model file. |
| **Model registry** | Single source of truth for model versions and which one is in Production. |
| **Quality gate** | Automatic rules a new model must pass before promotion, like CI that must be green. |
| **Champion / challenger** | Current production model vs new candidate, compared on the same fresh data. |
| **Batch / online / streaming serving** | Score a file on a schedule / answer each request live / score events as they flow. |
| **Data drift** | Input distributions change from what the model was trained on. |
| **Concept drift** | The relationship between inputs and the right answer changes. |
| **PSI** | Score of how much a feature's distribution moved; > 0.25 means alert. |
| **Shadow deployment** | New model runs on real traffic but only logs answers; users see the old model. |
| **Canary release** | A small share of users get the new model first; ramp up if metrics hold. |
| **Continuous training (CT)** | Retraining automatically on a schedule or a trigger such as a drift alert. |

---

## The build plan, cell by cell (rung ③ · hands)

| Cell | You write | Module | Codebase file (rung ④) |
|------|-----------|--------|------------------------|
| 0 | nothing: setup | — | — |
| 1 | `avg` | M1 | `data.py` |
| 2 | `baseline_pred`, `baseline_mae` | M3 | `train.py` |
| 3 | `X = build_features(df)` | M3 | `features.py` |
| 4 | `best = tracker.best("mae")` | M3 | `tracking.py` |
| 5 | gate + promote | M3/M4 | `registry.py`, `pipeline.py` |
| 6 | the request payload | M5 | `serve.py` |
| 7 | count late orders | M4/M5 | `batch.py` |
| 8 | the PSI formula line | M6 | `monitor.py` |
| 9 | live MAE | M6 | `monitor.py` |
| 10 | read champion/challenger MAE | M4/M7 | `pipeline.py` |
| 11 | canary 10% | M7 | `rollout.py` |
| 12 | 5 answers in your own words | all | — |

### Where people get stuck
- **Cell 0** fails to import `deliverease`: run the notebook from its own folder, so `../../codebase` resolves.
- **Cell 5:** `quality_gate` returns *two* values: `ok, reason = …`.
- **Cell 6:** keys must match the API exactly: `distance_km, hour, items, prep_min, is_raining`.
- **Cell 8:** `a` and `e` are already percentages per bin; the formula is one line.
- **Cell 10:** if `promoted` is False, re-run from cell 0 (the scratch registry is rebuilt each run).

---

## Production boxes

| Module | How industry does it | What breaks in production | How you'd monitor it |
|--------|---------------------|---------------------------|----------------------|
| M3 | MLflow / W&B, feature store | Two copies of feature code → skew | Compare live feature stats to training stats |
| M4 | Airflow / Kubeflow DAG + gate | Gate compares on different data (this codebase's first bug) | Log champion & challenger on the same eval set |
| M5 | FastAPI / BentoML / KServe | Slow feature lookup breaks latency budget | p95 latency, error rate (Prometheus/Grafana) |
| M6 | Evidently / Arize | Labels arrive late → accuracy drop unseen for hours | Drift (PSI) as early warning; MAE once labels land |
| M7 | Argo Rollouts / Istio | Random routing flips a user between models | Hash-based routing; per-variant dashboards |

## Interview box (60-second answers)

- **"How would you deploy and maintain an ML model?"** Version code, data and model. A pipeline trains and logs every run,
  a quality gate checks it beats the baseline and the current model on the same fresh data, and it's registered and
  served behind an API that returns the model version. Monitor latency, input drift (PSI) and accuracy once labels
  arrive. A drift alert triggers retraining, and the new model goes out via shadow or canary.
- **"Data drift vs concept drift?"** Data drift = inputs changed (detect without labels by comparing distributions).
  Concept drift = the input→output relationship changed (needs real outcomes; shows up as rising error).

## Exam box
No MLOps past papers in this folder yet. The handout (older batch, `handouts/`) says: midsem = sessions 1–7
(M1–M4, closed book), comprehensive = all sessions (open book), 2 take-home assignments (40%).

---

## Progress checklist
- [ ] Warm-up questions answered out loud
- [ ] Explainer §1–8 + quiz ≥ 6/8
- [ ] Notebook cells 1–11 ✅
- [ ] `cd codebase && pytest -q`: 15 passed
- [ ] Opened each codebase file named in the table above (5 min each)
- [ ] Cell 12: five answers in my own words
- [ ] Reviewed this topic's cards in `cards.json` (day 1, then day 3, 7, 21)
