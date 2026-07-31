# Interview preparation

Prep material for AI/ML interviews — theory-first, written so each answer can be *spoken*, not just read.

| File | What it is |
|------|------------|
| [JOURNEY.md](JOURNEY.md) | Roadmap and progress tracker — which subject files exist, which are next, and the conventions they follow |
| [top-100-questions.md](top-100-questions.md) | The 100 theory questions that repeat most often, each with a one-line answer plus short theory for the follow-up |
| [coding-questions.md](coding-questions.md) | 60 coding problems with runnable solutions — Python, NumPy, pandas, algorithms from scratch, scikit-learn, SQL, PyTorch |
| [quick-revision-cheatsheet.md](quick-revision-cheatsheet.md) | Formulas, decision tables, Python/pandas and SQL snippets — for the last 30 minutes |

### Subject deep dives

One file per subject, at interview depth: spoken answer → explanation → the follow-up question they chain onto it.

| File | Subject | Status |
|------|---------|--------|
| [machine-learning.md](machine-learning.md) | Classical ML — 80 questions | ✅ Done |
| `deep-learning.md` | Neural nets, backprop, CNN/RNN, training | ⬜ Planned |
| `nlp.md` | Text → embeddings → Transformers → LLMs/RAG | ⬜ Planned |
| `deep-rl.md` | MDPs, Q-learning, DQN, policy gradients | ⬜ Planned |
| `probability.md` / `statistics.md` | Distributions, Bayes, inference, A/B testing | ⬜ Planned |
| `aics.md` | Search, logic, CSP, planning | ⬜ Planned |
| `seml.md` | MLOps, testing ML, CI/CD, drift, governance | ⬜ Planned |

See [JOURNEY.md](JOURNEY.md) for the build order and the conventions each file follows.

## How the 100 are organised

| # | Section |
|---|---------|
| 1–12 | AI/ML fundamentals |
| 13–20 | Statistics & probability |
| 21–31 | Data preprocessing & feature engineering |
| 32–45 | Supervised learning algorithms |
| 46–57 | Model evaluation & tuning |
| 58–64 | Unsupervised learning & dimensionality reduction |
| 65–76 | Deep learning |
| 77–83 | Natural Language Processing |
| 84–91 | Transformers, LLMs & Generative AI |
| 92–94 | Reinforcement learning |
| 95–100 | MLOps, deployment & responsible AI |

⭐ marks the very high-frequency questions.

## How the coding questions are organised

| # | Section |
|---|---------|
| 1–12 | Python fundamentals & logic |
| 13–21 | NumPy |
| 22–33 | Pandas |
| 34–44 | ML algorithms from scratch (NumPy) |
| 45–50 | scikit-learn / practical ML |
| 51–55 | SQL |
| 56–60 | PyTorch / deep learning |

Plus a debugging table ("training loss won't go down", "loss is NaN", …) which is a favourite live question.

## Suggested plan for one evening

1. **Hour 1** — Q1–Q12, Q46–Q57 (fundamentals + overfitting/metrics). These come up in almost every interview and
   every follow-up chains back to them.
2. **Hour 2** — Q21–Q45 (data prep + algorithms). Be able to explain *when* you'd pick each algorithm, not just
   what it is.
3. **Hour 3** — Q65–Q76 and Q84–Q91 (deep learning + Transformers/GenAI). Q90 (RAG vs fine-tuning) is currently
   the most-asked generative AI question, so rehearse that one aloud.
4. **Hour 4 — coding.** Hand-write these five from a blank file, no copying: linear regression with gradient
   descent, logistic regression, K-Means, precision/recall/F1 from the confusion matrix, and a scikit-learn
   pipeline + PyTorch training loop. Skim the rest of `coding-questions.md`.
5. **Last 30 min** — the cheat sheet only, plus one rehearsal of your own project story.
6. Skim Q13–Q20 and Q92–Q100 for coverage; don't over-invest.

## Two things that matter more than the list

- **Say it in plain words first, then add the technical layer.** "It memorised the training data instead of
  learning the pattern" beats reciting a definition of overfitting.
- **Have one project you can narrate end to end** — problem, data, what you tried, what failed, the final metric,
  what you'd improve. Most interviews are decided there.
