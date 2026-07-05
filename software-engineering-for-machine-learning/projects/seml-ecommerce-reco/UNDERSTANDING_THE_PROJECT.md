# Understanding this project (plain-English guide)

This is a **product recommendation system for an online store** — the "Customers who
viewed this also liked…" feature. This guide explains *what* it does, *how* it works, and
*where* everything lives, assuming no prior background.

---

## 1. The problem we're solving

An online store has lots of products and lots of shoppers. Showing everyone the same
"best sellers" is lazy — different people want different things. We want to show **each user
a personalized short list of products they haven't seen yet but are likely to want.**

We only have **implicit signals** — we can't ask users what they like, but we can watch what
they do: they *view*, *click*, *add to cart*, and *purchase*. Stronger actions mean stronger
interest.

**Goal:** turn a stream of these actions into a personalized **Top-5** list per user.

---

## 2. The idea behind the ML (item-based collaborative filtering)

The core intuition: **products that get interacted with by the same people are "similar."**
If many users who bought product A also bought product B, then A and B are related — so if
*you* liked A, we should suggest B.

Here's the whole method in four steps:

### Step 1 — Weight the actions
Each action becomes a number (how much interest it shows):

| Action | Weight |
|--------|--------|
| view | 1 |
| click | 2 |
| cart | 3 |
| purchase | 5 |

### Step 2 — Build a user–item matrix
A big grid: **rows = users, columns = products**. Each cell = the total weight that user has
put on that product. Most cells are 0 (nobody interacts with everything).

```
          P01  P02  P03  ...  P40
   u1  [   5    0    2   ...   0 ]
   u2  [   0    3    0   ...   1 ]
   ...
```

### Step 3 — Compute item-to-item similarity
For every pair of products, measure how similarly they're treated across all users, using
**cosine similarity** (a standard "how aligned are these two columns?" score from 0 to 1).
Result: a **product × product similarity table**.

### Step 4 — Score and rank for one user
To recommend for user *u*:
1. Take *u*'s row (what they've interacted with).
2. Multiply it by the similarity table → a **score for every product** ("how related is this
   product to the things u already likes?").
3. **Remove products u already interacted with** (no point re-recommending them).
4. Return the **top 5** highest-scoring remaining products.

That's it. No deep learning, no training a neural network — just weighting, a matrix, and
cosine similarity. It's fast, explainable, and good enough to demonstrate the engineering.

**Example (real output from this project):** for user `u7`, the top 5 are
`P28, P25, P21, P16, P40`. Offline accuracy **Precision@5 = 0.323** (explained in §6).

---

## 3. The software architecture (this is the "engineering" part)

The assignment isn't really about the ML — it's about **software engineering for ML**. So we
wrap that simple model in a realistic, well-structured system using **two architectural
patterns**:

### Pattern 1 — Event-Driven Architecture
When a shopper does something (say, adds P12 to cart), we don't stop everything to update the
model right then. Instead:
1. The action is dropped onto a **queue** (like a to-do inbox) and we instantly reply "got it."
2. A **background worker** quietly picks items off the queue and updates the model **later**.

Why? So the website stays fast even during a rush. Writes (events pouring in) never block
reads (shoppers asking for recommendations). This is called being **asynchronous**.

### Pattern 2 — API Gateway
Instead of letting the outside world talk directly to our internal machinery, **everything
goes through one front door** — the "gateway." The gateway:
- checks a security **token** (is this caller allowed?),
- applies **rate limiting** (don't let one caller spam us),
- **routes** the request to the right internal service.

Why? Security and control live in one place; the internal service stays simple and hidden.

### How they fit together
```
   Shopper / UI
        │
        ▼
   ┌─────────────┐   "give me recommendations" or "here's an event"
   │ API Gateway │  (checks token, rate-limits, routes)   ← Pattern 2
   └─────────────┘
        │
        ▼
   ┌───────────────────────┐
   │ Recommendation service│
   │  • /rank  → get top-5 │
   │  • /track → queue event ──▶ [queue] ──▶ background worker ──▶ updates model  ← Pattern 1
   └───────────────────────┘
```

There are **three running pieces**: the **gateway**, the **recommendation service** (with its
queue + worker + the ML), and a **web frontend** (the Streamlit page you see).

---

## 4. What each part is built with

| Piece | Technology | What it is |
|-------|-----------|------------|
| Gateway & recommendation service | **FastAPI** (Python web framework) | Two small web servers exposing URLs like `/recommend`, `/track` |
| The queue + background worker | Python's built-in `queue` + a thread | The "event-driven" mechanism |
| The ML | **NumPy** + **scikit-learn** (`cosine_similarity`) | The matrix math from §2 |
| Frontend | **Streamlit** | A simple interactive web page |
| Packaging for the internet | **Docker** + **Hugging Face Spaces** | Runs all three together, free, at a public URL |

---

## 5. Codebase structure — the full map

### ⚠️ First, the one thing that explains all your confusion

**This repository contains TWO complete versions of the same assignment.** That's why you
saw "backend", "frontend", "hugging face" and got lost — some of those belong to a version we
**do not use**.

| | **Version A — what we submitted & deployed** | **Version B — an older, alternate design (ignore)** |
|---|---|---|
| Design | Event-Driven Architecture + API Gateway | Microservices + CQRS |
| Lives in | **`event_driven_prototype/` only** | everything else at the top level |
| Used by the report? | ✅ Yes | ❌ No |
| Deployed to Hugging Face? | ✅ Yes | ❌ No |

👉 **If you only open ONE folder, open `event_driven_prototype/`.** That single folder is the
entire project — the ML, both backend services, the frontend, and the deployment. Everything
else can be ignored for understanding the submission.

---

### Every top-level folder, and whether you need it

| Path | Version | What it is | Do you need it? |
|------|---------|-----------|-----------------|
| **`event_driven_prototype/`** | **A ✅** | **The whole submitted project (code + frontend + deployment)** | **YES — go here** |
| `final_submission/` | A | The files you upload to the college portal (notebook + report) | Yes, to submit |
| `UNDERSTANDING_THE_PROJECT.md` | A | This guide | Yes |
| `SUBMISSION_G49.md` | A | Submission checklist | Optional |
| `backend/` | B | Version B's backend (CQRS command/query services) | No — ignore |
| `frontend/` | B | Version B's frontend (`app.py`, a different Streamlit UI) | No — ignore |
| `scripts/`, `tools/` | B | Version B's helper scripts (seed data, build report/notebook) | No — ignore |
| `data/`, `artifacts/`, `evidence/` | B | Version B's sample data, saved model, screenshots | No — ignore |
| `Dockerfile`, `docker-compose.yml`, `Makefile`, `pyproject.toml`, root `requirements.txt` | B | Version B's build/config files | No — ignore |
| `Assignment Iseml.pdf` | — | The original assignment question | Reference only |
| `Vivek_..._Final_Report.docx` (+ `.BACKUP`) | A | Loose copies of the report (the real one lives in `final_submission/`) | Reference only |

> Why do both versions exist? The repo was originally cloned from a teammate whose code had
> been rewritten into Version B (CQRS). Our report describes Version A (Event-Driven), so we
> restored Version A into `event_driven_prototype/`. Both were kept so nothing was lost.

---

### Inside `event_driven_prototype/` — the folder you actually go through

```
event_driven_prototype/
│
│   ── THE BACKEND (two services) ──
├── recommender_engine.py     ← the ML brain: matrix, similarity, ranking, Precision@5
├── recommendation_api.py     ← internal service: /rank + /track + the queue & worker  (Pattern 1)
├── api_gateway.py            ← the front door: token, rate-limit, routing              (Pattern 2)
│
│   ── THE FRONTEND ──
├── frontend_app.py           ← the Streamlit web page (what you see in the browser)
│
│   ── THE HUGGING FACE DEPLOYMENT ──
├── Dockerfile                ← recipe that packages all 3 processes into one container
├── start.sh                  ← the container's startup: launches all 3 processes
├── requirements-hf.txt       ← Python packages installed on Hugging Face
├── README.md                 ← its top has the HF "sdk: docker" config that makes it a Space
├── .gitattributes            ← keeps files uncorrupted when deployed (binary/line-ending rules)
│
│   ── HELPERS & PROOF ──
├── demo_requests.py          ← a script that fires test events + fetches recommendations
├── report_evidence.py        ← regenerates the metrics JSON + the evidence chart
├── requirements.txt          ← packages for running locally (not the HF one)
├── run_local.ps1             ← one-click local runner (auto-picks free ports)
└── evidence/                 ← captured proof: metrics JSON, sample output, PNG charts
```

### Answering your three words directly

- **"backend"** — the backend is the **two FastAPI files** in `event_driven_prototype/`:
  `api_gateway.py` (front door) and `recommendation_api.py` (does the work, holds the queue),
  with `recommender_engine.py` as the ML underneath.
  *(The top-level `backend/` folder is Version B's backend — not used.)*

- **"frontend"** — the frontend is **`event_driven_prototype/frontend_app.py`** (Streamlit).
  *(The top-level `frontend/` folder is Version B's frontend — not used.)*

- **"hugging face"** — that's not a separate folder; it's **how we deploy**. The deployment is
  the three files inside `event_driven_prototype/`: `Dockerfile` + `start.sh` +
  `requirements-hf.txt` (plus the config at the top of `README.md`). Hugging Face reads these,
  builds the container, and runs `start.sh` — which starts backend + frontend together.

---

### The 3 files that matter most, in reading order
1. **`recommender_engine.py`** — read this first. It's the ML in ~200 lines: build the matrix,
   compute similarity, `rank_items()` (the recommendation), `evaluate_precision_at_k()` (scoring).
2. **`recommendation_api.py`** — wraps the engine in a web service and adds the **queue +
   background worker** (Pattern 1). Look at `/track` (queue an event) and `consumer_loop`.
3. **`api_gateway.py`** — the **front door** (Pattern 2). Look at `require_token`,
   `enforce_rate_limit`, and how `/recommend` forwards to the internal `/rank`.

---

## 6. How we measure if it's any good (Precision@5)

We can't know the "right" answer, so we test offline like this:
1. For each user, **hide 3 products** they actually interacted with.
2. Ask the model for its top-5, pretending it never saw those 3.
3. Check: **how many of the hidden 3 show up in the top-5?**

**Precision@5 = 0.323** means, on average, about 1.6 of every 5 recommended products are ones
the user genuinely engaged with — solidly above our target of 0.30. (This is the
"leave-three-out" test in `evaluate_precision_at_k`.)

---

## 7. How to see it working

- **Live online (easiest):** open the hosted app —
  <https://huggingface.co/spaces/ravirajladha/seml-ecommerce-reco>. Pick a user, click
  *Recommend*, send an event, watch the numbers update.
- **The notebook:** `final_submission/G49.ipynb` runs the whole thing top-to-bottom with
  explanations and outputs.
- **Locally (full 3-service demo):** run `event_driven_prototype/run_local.ps1`, then open the
  gateway docs it prints.

---

## 8. One-paragraph summary (for when someone asks "what is this?")

> "It's a personalized product recommender for an e-commerce store. It learns from shopper
> behavior (views, clicks, carts, purchases) using item-based collaborative filtering, and
> returns each user a Top-5 list of products. The interesting part is the software
> engineering: it's built with two architectural patterns — an **Event-Driven** pipeline
> (events go on a queue and a background worker updates the model asynchronously) behind an
> **API Gateway** (a single secured entry point that handles auth, rate-limiting, and
> routing). It's implemented in Python with FastAPI + scikit-learn, has a Streamlit UI, and is
> deployed for free on Hugging Face as a Docker container running all three services."
