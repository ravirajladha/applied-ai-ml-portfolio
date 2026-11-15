"""Test type 3: INTEGRATION tests.

These drive the real FastAPI app end to end - schema, model and status codes
together - using FastAPI's TestClient (no server needs to be running).
"""

import pytest
from fastapi.testclient import TestClient

from ecom.api import app


@pytest.fixture(scope="module")
def client():
    # The `with` block runs startup, which loads the model.
    with TestClient(app) as test_client:
        yield test_client


# --- ops endpoints -----------------------------------------------------
def test_health_is_always_200(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] in {"ok", "degraded"}


def test_model_info(client):
    response = client.get("/model-info")
    if response.status_code == 503:
        pytest.skip("No trained model available")
    assert response.status_code == 200
    assert response.json()["n_features"] == 12


def test_metrics_endpoint(client):
    response = client.get("/metrics")
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        assert "model_quality" in response.json()


# --- happy path --------------------------------------------------------
def test_predict_returns_200_and_a_valid_body(client, sample_session):
    response = client.post("/predict", json=sample_session)
    if response.status_code == 503:
        pytest.skip("No trained model available")

    assert response.status_code == 200
    body = response.json()
    assert body["session_id"] == sample_session["session_id"]
    assert 0.0 <= body["conversion_probability"] <= 1.0
    assert body["intent_band"] in {"low", "medium", "high"}
    assert isinstance(body["will_convert"], bool)


def test_batch_predict(client, sample_session):
    payload = {"sessions": [sample_session, {**sample_session, "cart_items": 0}]}
    response = client.post("/predict/batch", json=payload)
    if response.status_code == 503:
        pytest.skip("No trained model available")

    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 2
    assert len(body["predictions"]) == 2


# --- input validation (422) --------------------------------------------
@pytest.mark.parametrize(
    "field, bad_value",
    [
        ("pages_viewed", -1),
        ("pages_viewed", "twelve"),
        ("cart_items", 10_000),
        ("device", "smart-fridge"),
        ("avg_item_price", -50),
        ("session_id", ""),
    ],
)
def test_invalid_input_returns_422(client, sample_session, field, bad_value):
    response = client.post("/predict", json={**sample_session, field: bad_value})
    assert response.status_code == 422


def test_missing_required_field_returns_422(client, sample_session):
    payload = {k: v for k, v in sample_session.items() if k != "device"}
    assert client.post("/predict", json=payload).status_code == 422


def test_unknown_field_is_rejected(client, sample_session):
    payload = {**sample_session, "sql_injection": "DROP TABLE users"}
    assert client.post("/predict", json=payload).status_code == 422


def test_oversized_batch_is_rejected(client, sample_session):
    payload = {"sessions": [sample_session] * 101}
    assert client.post("/predict/batch", json=payload).status_code == 422


def test_empty_batch_is_rejected(client):
    assert client.post("/predict/batch", json={"sessions": []}).status_code == 422


def test_unknown_route_returns_404(client):
    assert client.get("/does-not-exist").status_code == 404
