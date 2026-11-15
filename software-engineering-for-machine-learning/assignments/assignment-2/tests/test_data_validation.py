"""Test type 1: DATA VALIDATION tests.

These guard the input contract, not the model.
"""

import pandas as pd
import pytest

from ecom.data_validation import (
    DataValidator,
    detect_drift,
    population_stability_index,
)
from ecom.exceptions import DataValidationError


def test_clean_data_passes(raw_df):
    report = DataValidator().validate(raw_df)
    assert report.passed
    assert report.schema_conformance == 1.0


def test_missing_column_is_rejected(raw_df):
    broken = raw_df.drop(columns=["cart_items"])
    with pytest.raises(DataValidationError, match="cart_items"):
        DataValidator().validate(broken)


def test_wrong_dtype_is_rejected(raw_df):
    broken = raw_df.copy()
    broken["pages_viewed"] = "not-a-number"
    with pytest.raises(DataValidationError, match="numeric"):
        DataValidator().validate(broken)


def test_too_many_missing_values_is_rejected(raw_df):
    broken = raw_df.copy()
    broken.loc[: len(broken) // 2, "avg_item_price"] = None
    with pytest.raises(DataValidationError, match="missing"):
        DataValidator().validate(broken)


def test_negative_values_are_rejected(raw_df):
    broken = raw_df.copy()
    broken.loc[0, "pages_viewed"] = -5
    with pytest.raises(DataValidationError, match="negative"):
        DataValidator().validate(broken)


def test_non_strict_mode_reports_instead_of_raising(raw_df):
    broken = raw_df.drop(columns=["device"])
    report = DataValidator().validate(broken, strict=False)
    assert not report.passed
    assert report.schema_conformance < 1.0


def test_schema_conformance_is_a_measurable_fraction(raw_df):
    broken = raw_df.drop(columns=["device", "cart_items"])
    report = DataValidator().validate(broken, strict=False)
    assert report.schema_conformance == pytest.approx(6 / 8)


# --- drift detection ---------------------------------------------------
def test_psi_is_zero_for_identical_distributions():
    series = pd.Series(range(1000))
    assert population_stability_index(series, series) < 0.01


def test_psi_flags_a_shifted_distribution():
    baseline = pd.Series(range(1000))
    shifted = pd.Series(range(2000, 3000))
    assert population_stability_index(baseline, shifted) > 0.2


def test_detect_drift_catches_the_drifted_live_feed(raw_df):
    from ecom.data_ingestion import SessionDataGenerator

    live = SessionDataGenerator(seed=99).generate(300, drifted=True)
    scores = detect_drift(raw_df, live, ["pages_viewed"])
    assert scores["pages_viewed"] > 0.2
