"""M3 · Train, evaluate against a baseline, and record the run.

Rule: a model only counts if it beats the simplest possible baseline on data it never saw.
Baseline here: "always predict the average delivery time from training data".
"""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

from .data import TARGET
from .features import build_features
from .tracking import Tracker


def train(df: pd.DataFrame, out_dir: str | Path, tracker: Tracker, params: dict | None = None,
          data_version: str = "dry-season-v1") -> dict:
    params = {"n_estimators": 200, "max_depth": 3, "learning_rate": 0.05, **(params or {})}
    X, y = build_features(df), df[TARGET]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

    baseline_mae = mean_absolute_error(y_te, np.full(len(y_te), y_tr.mean()))
    model = GradientBoostingRegressor(random_state=42, **params).fit(X_tr, y_tr)
    mae = mean_absolute_error(y_te, model.predict(X_te))

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "model.joblib"
    joblib.dump(model, path)

    metrics = {"mae": round(mae, 3), "baseline_mae": round(baseline_mae, 3)}
    run_id = tracker.log_run(params={**params, "data_version": data_version, "rows": len(df)},
                             metrics=metrics, artifact=str(path))
    return {"run_id": run_id, "model_path": str(path), "metrics": metrics}
