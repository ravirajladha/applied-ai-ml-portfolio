#!/usr/bin/env bash
# Launch all three processes in one container: internal recommendation/event
# service (8001), API gateway (8000), and the Streamlit frontend (7860, public).
set -e

export RECO_SERVICE="http://127.0.0.1:8001"
export GATEWAY_URL="http://127.0.0.1:8000"

# Backend service 1: internal recommendation + event service (Event-Driven queue)
python -m uvicorn recommendation_api:app --host 127.0.0.1 --port 8001 &

# Backend service 2: API gateway (auth, rate-limit, routes to the internal service)
python -m uvicorn api_gateway:app --host 127.0.0.1 --port 8000 &

# Wait for the gateway to be ready before starting the UI.
python - <<'PY'
import time, urllib.request
for _ in range(60):
    try:
        urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=1)
        print("gateway is up", flush=True)
        break
    except Exception:
        time.sleep(0.5)
PY

# Frontend (public): Streamlit on the port Hugging Face exposes.
exec python -m streamlit run frontend_app.py \
    --server.port 7860 --server.address 0.0.0.0 \
    --server.headless true --browser.gatherUsageStats false
