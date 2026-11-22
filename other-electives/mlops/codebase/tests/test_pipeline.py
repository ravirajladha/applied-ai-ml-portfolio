"""Tests are the CI quality bar for an ML system: code tests AND model tests AND data tests."""
import numpy as np
import pandas as pd
import pytest
from fastapi.testclient import TestClient

from deliverease.batch import score_file
from deliverease.data import FEATURES, make_orders
from deliverease.features import MODEL_INPUTS, build_features
from deliverease.monitor import drift_report, psi, should_retrain
from deliverease.pipeline import quality_gate, run_pipeline
from deliverease.registry import Registry
from deliverease.rollout import Router, bucket
from deliverease.serve import create_app


@pytest.fixture(scope="module")
def workdir(tmp_path_factory):
    wd = tmp_path_factory.mktemp("mlops")
    result = run_pipeline(wd, seed=0, n=1500)
    assert result["promoted"], result["reason"]
    return wd


# ---------- data + feature tests (M3) ----------
def test_features_have_fixed_schema():
    X = build_features(make_orders(50))
    assert list(X.columns) == MODEL_INPUTS and not X.isna().any().any()


def test_bad_input_is_rejected():
    df = make_orders(5)
    df.loc[0, "distance_km"] = -1
    with pytest.raises(ValueError):
        build_features(df)


# ---------- model tests: the quality gate (M4) ----------
def test_model_beats_baseline(workdir):
    prod = Registry(workdir / "registry").get("Production")
    assert prod["metrics"]["mae"] < prod["metrics"]["baseline_mae"] * 0.7


def test_gate_rejects_worse_model():
    ok, reason = quality_gate({"mae": 5.0, "baseline_mae": 10.0}, champion_mae=4.0)
    assert not ok and "production" in reason


def test_monsoon_hurts_old_model_and_retraining_fixes_it(tmp_path):
    first = run_pipeline(tmp_path, seed=0, n=1500)                     # dry-season model goes live
    second = run_pipeline(tmp_path, seed=3, n=1500, monsoon=True)       # retrain on monsoon data
    assert second["champion_mae"] > first["metrics"]["mae"] * 2        # old model is much worse in the monsoon
    assert second["promoted"], second["reason"]                         # challenger wins on the same fresh data


def test_registry_keeps_one_production(workdir):
    run_pipeline(workdir, seed=1, n=1500)
    stages = [v["stage"] for v in Registry(workdir / "registry").versions()]
    assert stages.count("Production") == 1


# ---------- serving (M5) ----------
def test_api_predicts(workdir):
    client = TestClient(create_app(str(workdir / "registry")))
    assert client.get("/health").json()["status"] == "ok"
    r = client.post("/predict", json={"distance_km": 3.0, "hour": 20, "items": 2, "prep_min": 10, "is_raining": 0})
    assert r.status_code == 200 and 10 < r.json()["eta_min"] < 80


def test_api_rejects_invalid(workdir):
    client = TestClient(create_app(str(workdir / "registry")))
    r = client.post("/predict", json={"distance_km": -3, "hour": 20, "items": 2, "prep_min": 10, "is_raining": 0})
    assert r.status_code == 422


def test_batch_scoring(workdir, tmp_path):
    make_orders(20, seed=5)[FEATURES].to_csv(tmp_path / "in.csv", index=False)
    assert score_file(tmp_path / "in.csv", tmp_path / "out.csv", workdir / "registry") == 20
    assert "eta_min" in pd.read_csv(tmp_path / "out.csv").columns


# ---------- monitoring (M6) ----------
def test_psi_zero_for_same_data():
    x = np.random.default_rng(0).normal(size=5000)
    assert psi(x, x) < 0.01


def test_monsoon_triggers_drift_alert():
    report = drift_report(make_orders(3000, seed=0), make_orders(3000, seed=9, monsoon=True), FEATURES)
    retrain, reason = should_retrain(report)
    assert retrain and "is_raining" in reason


def test_same_season_is_stable():
    report = drift_report(make_orders(3000, seed=0), make_orders(3000, seed=9), FEATURES)
    assert not should_retrain(report)[0]


# ---------- rollout (M7) ----------
class Const:
    def __init__(self, v): self.v = v
    def predict(self, X): return np.array([self.v])


def test_bucket_is_stable():
    assert bucket("order-42") == bucket("order-42")


def test_canary_share_is_roughly_right():
    router = Router(Const(1), Const(2), canary_percent=10)
    served = [router.predict(f"order-{i}", None)[1] for i in range(5000)]
    assert 0.07 < served.count("candidate") / len(served) < 0.13


def test_shadow_never_serves_candidate():
    router = Router(Const(1), Const(2), canary_percent=0, shadow=True)
    for i in range(100):
        y, who = router.predict(f"o{i}", None)
        assert who == "current" and y[0] == 1
    assert len(router.shadow_log) == 100
