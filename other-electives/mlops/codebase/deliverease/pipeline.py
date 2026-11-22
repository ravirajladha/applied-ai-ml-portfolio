"""M4 · The pipeline: data -> train -> quality gate -> register -> promote.

This is what Airflow / Kubeflow / Prefect run on a schedule as a DAG (a graph of steps).
Here it's plain Python so you can read every step. The important part is the **quality gate**:
a new model is only promoted if it is good enough. Same idea as "CI must be green before deploy".
"""
from pathlib import Path

import joblib
from sklearn.metrics import mean_absolute_error

from .data import TARGET, make_orders
from .features import build_features
from .registry import Registry
from .tracking import Tracker
from .train import train

MAX_MAE = 6.0              # business rule: average error must stay under 6 minutes
MUST_BEAT_BASELINE_BY = 0.30   # and be at least 30% better than "predict the average"


def quality_gate(metrics: dict, champion_mae: float | None) -> tuple[bool, str]:
    """`metrics` = the new model (challenger). `champion_mae` = the production model scored on the SAME fresh data."""
    if metrics["mae"] > MAX_MAE:
        return False, f"MAE {metrics['mae']} above limit {MAX_MAE}"
    if metrics["mae"] > metrics["baseline_mae"] * (1 - MUST_BEAT_BASELINE_BY):
        return False, "not clearly better than the baseline"
    if champion_mae is not None and metrics["mae"] >= champion_mae:
        return False, f"not better than production (champion MAE {champion_mae:.2f})"
    return True, "passed"


def mae_on(model_path: str, df) -> float:
    model = joblib.load(model_path)
    return round(mean_absolute_error(df[TARGET], model.predict(build_features(df))), 3)


def run_pipeline(workdir: str | Path, seed: int = 0, monsoon: bool = False, n: int = 2000) -> dict:
    workdir = Path(workdir)
    tracker, registry = Tracker(workdir / "runs"), Registry(workdir / "registry")

    df = make_orders(n=n, seed=seed, monsoon=monsoon)                       # step 1: get data
    result = train(df, workdir / "artifacts", tracker,                      # step 2: train + track
                   data_version="monsoon-v1" if monsoon else "dry-season-v1")
    # step 3: champion vs challenger, both scored on the same fresh, recent data
    fresh = make_orders(n=600, seed=seed + 100, monsoon=monsoon)
    challenger_mae = mae_on(result["model_path"], fresh)
    champion = registry.get("Production")
    champion_mae = mae_on(champion["path"], fresh) if champion else None
    ok, reason = quality_gate({**result["metrics"], "mae": challenger_mae}, champion_mae)
    version = registry.register(result["model_path"], result["run_id"], result["metrics"])  # step 4
    if ok:
        registry.promote(version, "Production")                             # step 5: go live
    else:
        registry.promote(version, "Staging")
    return {**result, "version": version, "promoted": ok, "reason": reason,
            "challenger_mae": challenger_mae, "champion_mae": champion_mae}


if __name__ == "__main__":
    print(run_pipeline("mlops_workdir"))
