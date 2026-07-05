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

---

## 9. Line-by-line code walkthrough (deep dive)

This section explains the three core files in `event_driven_prototype/`, block by block.
Read them in this order: **engine → recommendation service → gateway.**

### 9a. `recommender_engine.py` — the ML brain

This file holds the data and does all the math. It has **no web code** — it's pure Python
functions that other files call.

**The setup (module top):**
```python
USERS = [f"u{i}" for i in range(1, 61)]      # 60 users: u1 … u60
ITEMS = [f"P{i:02d}" for i in range(1, 41)]  # 40 products: P01 … P40
USER_INDEX = {user_id: index for index, user_id in enumerate(USERS)}   # "u7" -> row 6
ITEM_INDEX = {item_id: index for index, item_id in enumerate(ITEMS)}   # "P12" -> col 11
ACTION_WEIGHT = {"view": 1.0, "click": 2.0, "cart": 3.0, "purchase": 5.0}
```
- `USERS`/`ITEMS` are the fixed IDs. `USER_INDEX`/`ITEM_INDEX` translate an ID → a
  row/column number, because NumPy works with numbers, not names.

```python
_LOCK = threading.RLock()
_MATRIX = np.zeros((len(USERS), len(ITEMS)))       # the 60×40 user–item grid, all zeros
_ITEM_SIMILARITY = np.zeros((len(ITEMS), len(ITEMS)))  # the 40×40 product-similarity table
_EVENT_COUNT = 0
_SEEDED = False
```
- These are the **shared memory** of the app. `_MATRIX` is the grid from §2. `_LOCK` prevents
  two threads (the web request and the background worker) from writing at the same time and
  corrupting it. The `_` prefix just means "internal, don't touch from outside."

**`seed_demo_data()` — invent realistic starter data**
```python
rng = np.random.default_rng(546)          # fixed seed => same data every run (reproducible)
for user_index, _user_id in enumerate(USERS):
    cluster = user_index % 4              # put each user in one of 4 "taste groups"
    core_items = np.arange(cluster*10, cluster*10 + 10)          # their group's products
    neighbour_items = np.arange(((cluster+1)%4)*10, ...+10)      # a neighbouring group
    selected_core = rng.choice(core_items, size=7, replace=False)      # 7 from their group
    selected_neighbour = rng.choice(neighbour_items, size=2, ...)      # 2 from the neighbour
    for item_index in selected:
        _MATRIX[user_index, item_index] += rng.choice([1,2,3,5], p=[...])  # a weighted action
```
- Real stores have real logs; for the demo we **fabricate believable behavior**. Users cluster
  into taste groups so there's an actual pattern to learn. `seed=546` makes it identical every
  time, which is why your results always match the report.

**`_refresh_similarity_locked()` — turn the grid into a similarity table**
```python
_ITEM_SIMILARITY = cosine_similarity(_MATRIX.T)   # .T = transpose, so we compare COLUMNS (items)
np.fill_diagonal(_ITEM_SIMILARITY, 0.0)           # a product is not "similar to itself" for recos
```
- This is the heart of collaborative filtering: how alike is every product to every other
  product, based on who interacted with them. The diagonal is zeroed so an item never
  recommends itself.

**`track_event()` — the WRITE path (record one action)**
```python
_MATRIX[USER_INDEX[user_id], ITEM_INDEX[item_id]] += ACTION_WEIGHT[action]  # add the weight
_EVENT_COUNT += 1
_refresh_similarity_locked()          # the model just changed, so recompute similarity
return {..., "event_count": _EVENT_COUNT}   # a receipt
```
- Convert IDs to row/col, add the action's weight to that cell, and recompute similarity.
  This is what the background worker calls for every queued event.

**`rank_items()` — the READ path (the actual recommendation)** — the most important function:
```python
user_row = _MATRIX[USER_INDEX[user_id]].copy()   # this user's row (what they like)
scores   = user_row @ _ITEM_SIMILARITY           # (1×40)·(40×40) = a score for every product
scores[user_row > 0] = -np.inf                   # never recommend already-seen products
ordered  = np.argsort(...scores...)[::-1]         # sort products best-first
# then walk down 'ordered', skip seen ones, collect the first k
return recommendations                            # e.g. [{"item_id":"P28","score":10.027}, ...]
```
- Line 2 (`user_row @ _ITEM_SIMILARITY`) is the whole idea in one line: "for every product,
  add up how similar it is to the things this user already likes." Line 3 masks seen items by
  setting their score to minus-infinity so they sink to the bottom. Then take the top `k`.

**`evaluate_precision_at_k()` — how we grade it (§6)**
```python
holdout_items = rng.choice(positives, size=3, ...)   # secretly hide 3 items this user liked
train_matrix[user_index, holdout_items] = 0.0        # pretend they never happened
similarity = cosine_similarity(train_matrix.T)       # rebuild similarity WITHOUT the hidden ones
top = np.argsort(...)[:k]                             # ask for top-k
hits = len(set(top) & holdout_items)                 # how many hidden items came back?
precision_values.append(hits / k)                    # score for this user
# final answer = average across all users  => 0.323
```
- A fair "did it actually work?" test: hide some real interactions, then see if the model can
  rediscover them. Averaged over all users, that's **Precision@5 = 0.323**.

---

### 9b. `recommendation_api.py` — the internal service + the queue (Pattern 1)

This wraps the engine in a **web service** and adds the **Event-Driven** machinery.

```python
EVENT_QUEUE: Queue[dict] = Queue()   # the "inbox" that events land in
STOP_WORKER = Event()                # a flag to tell the worker to stop
```
- `EVENT_QUEUE` is the queue at the center of Pattern 1. `STOP_WORKER` lets us shut the worker
  down cleanly.

**`consumer_loop()` — the background worker (runs forever on its own thread)**
```python
while not STOP_WORKER.is_set():
    event = EVENT_QUEUE.get(timeout=0.2)          # take the next event off the queue (wait if empty)
    result = recommender_engine.track_event(event["user_id"], event["item_id"], event["action"])
    print("processed event:", result)             # update the model, then log it
    EVENT_QUEUE.task_done()
```
- This is the "asynchronous" part: it quietly drains the queue and updates the model **in the
  background**, separately from anyone asking for recommendations.

**`lifespan()` — startup/shutdown wiring**
```python
recommender_engine.seed_demo_data()               # load starter data
worker = Thread(target=consumer_loop, daemon=True) # create the background worker
worker.start()                                     # start it when the server boots
yield                                              # (server runs here)
STOP_WORKER.set(); worker.join(timeout=1)          # stop the worker when the server shuts down
```

**The endpoints (URLs this service exposes):**
```python
@app.post("/track", status_code=202)              # 202 = "Accepted", i.e. "I'll handle it later"
def track(event):
    recommender_engine.validate_event(...)         # reject bad events immediately
    EVENT_QUEUE.put(event.model_dump())            # drop it on the queue and RETURN RIGHT AWAY
    return {"status": "accepted", "pattern": "event-driven", ...}

@app.get("/rank")                                  # the read path
def rank(user_id, k=5):
    return {"recommendations": recommender_engine.rank_items(user_id, k), ...}
```
- **`/track` is the key line for Pattern 1:** it *queues* the event and replies instantly (202),
  instead of processing it on the spot. The worker handles it moments later. `/rank` just calls
  the engine's `rank_items()`.

---

### 9c. `api_gateway.py` — the single front door (Pattern 2)

The outside world talks **only** to this service. It never touches the engine directly.

```python
RECO_SERVICE = "http://127.0.0.1:8001"             # where the internal service lives
VALID_TOKEN  = "Bearer seml-demo-token"            # the password callers must send
REQUEST_LOG  = {}                                  # remembers when each caller last called
MIN_SECONDS_BETWEEN_REQUESTS = 0.25
```

**The two "guard" helpers:**
```python
def require_token(authorization):
    if authorization != VALID_TOKEN:
        raise HTTPException(status_code=401, ...)   # 401 = "not allowed"

def enforce_rate_limit(key):
    if now - REQUEST_LOG.get(key, 0) < 0.25:
        raise HTTPException(status_code=429, ...)   # 429 = "slow down"
    REQUEST_LOG[key] = now
```
- These are Pattern 2's whole point: **security and throttling live in one place**, so the
  internal service can stay simple.

**The public endpoints — they check, then forward:**
```python
@app.get("/recommend")
async def recommend(user_id, k=5, authorization=Header(...)):
    require_token(authorization)                    # 1. is the caller allowed?
    enforce_rate_limit(f"recommend:{user_id}")      # 2. are they calling too fast?
    async with httpx.AsyncClient() as client:       # 3. forward to the internal service…
        response = await client.get(f"{RECO_SERVICE}/rank", params={"user_id": user_id, "k": k})
    payload = await forward_response(response)
    payload["served_by"] = "api-gateway"            # 4. tag it so you can see it went through here
    return payload
```
- `/recommend` checks the token, checks the rate limit, then calls the internal service's
  `/rank` and returns the result. `/activity` does the same but forwards to `/track`. The
  gateway itself contains **no ML** — it only guards and routes.

---

### 9d. Follow ONE request through all three files

**"Recommend 5 products for u7"** (what the Streamlit button does):
1. **Frontend** (`frontend_app.py`) → `GET /recommend?user_id=u7&k=5` to the **gateway**, with
   the token header.
2. **Gateway** (`api_gateway.py`) → `require_token` ✔ → `enforce_rate_limit` ✔ → forwards to the
   internal service's `GET /rank`.
3. **Service** (`recommendation_api.py`) → calls `recommender_engine.rank_items("u7", 5)`.
4. **Engine** (`recommender_engine.py`) → `user_row @ _ITEM_SIMILARITY`, mask seen, take top-5 →
   `[P28, P25, P21, P16, P40]`.
5. The list travels back up the same chain to the browser. Done.

**"u7 just purchased P12"** (the event path):
1. Frontend → `POST /activity` to the **gateway**.
2. Gateway → checks token/rate-limit → forwards to the service's `POST /track`.
3. Service → drops the event on `EVENT_QUEUE` and **immediately** returns "accepted" (202).
4. Moments later, `consumer_loop` (the background worker) pulls it off the queue and calls
   `track_event`, which updates `_MATRIX` and recomputes similarity.
5. The **next** `/recommend` call for u7 reflects the change. (This delay is the deliberate
   "asynchronous / eventually-updated" behavior of Event-Driven Architecture.)
