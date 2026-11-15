"""ML-specific tests: MODEL INFERENCE behaviour.

Covers output shape/range, directional expectations and invariance.
"""

import pytest

from ecom.exceptions import ModelNotReadyError
from ecom.predict import ConversionPredictor, intent_band


@pytest.fixture(scope="module")
def predictor():
    """Uses the artifact produced by `python -m ecom.train`."""
    try:
        return ConversionPredictor().load()
    except ModelNotReadyError:
        pytest.skip("No trained model - run `python -m ecom.train` first")


def _session(**overrides) -> dict:
    base = {
        "session_id": "test",
        "pages_viewed": 8,
        "session_duration_min": 5.0,
        "cart_items": 1,
        "avg_item_price": 500.0,
        "is_returning_user": 0,
        "discount_applied": 0,
        "device": "mobile",
    }
    base.update(overrides)
    return base


# --- shape and range ---------------------------------------------------
def test_output_shape_matches_input(predictor):
    results = predictor.predict([_session(), _session(), _session()])
    assert len(results) == 3


def test_probability_is_in_range(predictor):
    for result in predictor.predict([_session(cart_items=i) for i in range(4)]):
        assert 0.0 <= result["conversion_probability"] <= 1.0


def test_response_has_the_expected_keys(predictor):
    result = predictor.predict([_session()])[0]
    assert set(result) == {
        "conversion_probability",
        "will_convert",
        "intent_band",
        "model_version",
    }


def test_empty_input_returns_empty_list(predictor):
    assert predictor.predict([]) == []


# --- directional tests -------------------------------------------------
def test_more_cart_items_increases_conversion_probability(predictor):
    low, high = predictor.predict([_session(cart_items=0), _session(cart_items=3)])
    assert high["conversion_probability"] > low["conversion_probability"]


def test_returning_user_is_more_likely_to_convert(predictor):
    new, returning = predictor.predict(
        [_session(is_returning_user=0), _session(is_returning_user=1)]
    )
    assert returning["conversion_probability"] > new["conversion_probability"]


def test_discount_increases_conversion_probability(predictor):
    without, with_discount = predictor.predict(
        [_session(discount_applied=0), _session(discount_applied=1)]
    )
    assert with_discount["conversion_probability"] > without["conversion_probability"]


# --- invariance tests --------------------------------------------------
def test_session_id_does_not_change_the_prediction(predictor):
    a, b = predictor.predict([_session(session_id="x"), _session(session_id="y")])
    assert a["conversion_probability"] == b["conversion_probability"]


def test_device_casing_does_not_change_the_prediction(predictor):
    a, b = predictor.predict([_session(device="mobile"), _session(device="MOBILE")])
    assert a["conversion_probability"] == b["conversion_probability"]


def test_row_order_does_not_change_predictions(predictor):
    one, two = _session(cart_items=0), _session(cart_items=3)
    forward = predictor.predict([one, two])
    backward = predictor.predict([two, one])
    assert forward[0]["conversion_probability"] == backward[1]["conversion_probability"]


# --- guard rails -------------------------------------------------------
def test_predicting_without_loading_raises():
    with pytest.raises(ModelNotReadyError):
        ConversionPredictor().predict([_session()])


def test_missing_artifact_raises(tmp_path):
    with pytest.raises(ModelNotReadyError, match="Train first"):
        ConversionPredictor(tmp_path / "nope.joblib").load()


@pytest.mark.parametrize(
    "probability, expected",
    [(0.05, "low"), (0.30, "medium"), (0.90, "high")],
)
def test_intent_band(probability, expected):
    assert intent_band(probability) == expected
