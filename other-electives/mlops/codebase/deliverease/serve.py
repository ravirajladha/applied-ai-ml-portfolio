"""M5 · Online serving: the model behind a REST API (model-as-a-service).

The app asks the registry for the Production model at start-up, validates each request, builds features with
the SAME function used in training, and returns a prediction plus the model version (so every prediction is
traceable). Run it with:  uvicorn deliverease.serve:create_app --factory --reload
"""
import os
import time

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .features import build_features
from .registry import Registry


class Order(BaseModel):
    distance_km: float = Field(gt=0, le=50)
    hour: int = Field(ge=0, le=23)
    items: int = Field(ge=1, le=50)
    prep_min: float = Field(ge=0, le=120)
    is_raining: int = Field(ge=0, le=1)


def create_app(registry_dir: str | None = None) -> FastAPI:
    registry = Registry(registry_dir or os.environ.get("REGISTRY_DIR", "mlops_workdir/registry"))
    prod = registry.get("Production")
    model = joblib.load(prod["path"]) if prod else None
    app = FastAPI(title="DeliverEase ETA")
    app.state.prediction_log = []          # in real life: a log stream / table that monitoring reads

    @app.get("/health")
    def health():
        return {"status": "ok" if model else "no-model", "model_version": prod and prod["version"]}

    @app.post("/predict")
    def predict(order: Order):
        if model is None:
            raise HTTPException(503, "no production model in registry")
        started = time.perf_counter()
        X = build_features(pd.DataFrame([order.model_dump()]))
        eta = float(model.predict(X)[0])
        latency_ms = (time.perf_counter() - started) * 1000
        app.state.prediction_log.append({**order.model_dump(), "eta_min": eta, "version": prod["version"]})
        return {"eta_min": round(eta, 1), "model_version": prod["version"], "latency_ms": round(latency_ms, 2)}

    return app

