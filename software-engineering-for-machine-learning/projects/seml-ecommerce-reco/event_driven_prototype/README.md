---
title: SEML E-commerce Recommendation
emoji: 🛒
colorFrom: indigo
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

# Event-Driven + API Gateway prototype (Group G49 submission)

> **Deployed as a Hugging Face Docker Space:** one container runs the internal
> recommendation/event service (`:8001`), the API gateway (`:8000`), and the Streamlit
> frontend (`:7860`, public). See `Dockerfile`, `start.sh`, and `frontend_app.py`.

Runnable code for the SEML Assignment I report
*"Real-Time Product Recommendation for an E-commerce Platform"*.

Two architectural patterns:
- **Event-Driven Architecture** — `recommendation_api.py` accepts activity events on
  `POST /track` (202), queues them, and a background consumer updates features
  asynchronously.
- **API Gateway** — `api_gateway.py` is the single public entry point (`/recommend`,
  `/activity`) that validates a bearer token, rate-limits, and routes to the internal
  service.

ML core: `recommender_engine.py` (item-based collaborative filtering, cosine similarity,
offline Precision@5).

## Run

```bash
python -m pip install -r requirements.txt

# Terminal 1 — internal recommendation/event service (port 8001)
python -m uvicorn recommendation_api:app --host 127.0.0.1 --port 8001

# Terminal 2 — public API gateway (port 8000)
python -m uvicorn api_gateway:app --host 127.0.0.1 --port 8000

# Terminal 3 — send events through the gateway and fetch recommendations
python demo_requests.py

# Regenerate metric JSON / plot evidence
python report_evidence.py
```

Public docs: Gateway <http://127.0.0.1:8000/docs> · Internal service <http://127.0.0.1:8001/docs>

## Recorded results (deterministic, seed=546 / eval seed=1546)

- Dataset: 60 users × 40 items, matrix density 22.63%, 543 events after the demo
- Offline **Precision@5 = 0.323** (leave-three-out, 60 users, 53 with ≥1 hit)
- Top-5 for `u7`: P28 (10.027), P25 (9.243), P21 (8.805), P16 (6.136), P40 (5.802)

The executable notebook `../final_submission/G49.ipynb` reproduces the ML core and the
event-driven flow in-process. The `evidence/` folder holds the captured run outputs used
in the report.
