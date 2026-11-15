"""Test type 2: UNIT tests for the feature functions."""

import pandas as pd

from ecom.config import FEATURE_COLUMNS
from ecom.features import (
    add_behaviour_features,
    build_features,
    encode_device,
    fill_missing,
)


def test_fill_missing_removes_nulls(tiny_df):
    out = fill_missing(tiny_df)
    assert out["avg_item_price"].isna().sum() == 0
    assert out.loc[2, "avg_item_price"] == 0.0


def test_fill_missing_does_not_mutate_input(tiny_df):
    before = tiny_df["avg_item_price"].isna().sum()
    fill_missing(tiny_df)
    assert tiny_df["avg_item_price"].isna().sum() == before


def test_pages_per_minute_handles_zero_duration(tiny_df):
    out = add_behaviour_features(fill_missing(tiny_df))
    assert out.loc[0, "pages_per_minute"] == 1.0  # 1 page / (0 + 1) min
    assert out["pages_per_minute"].notna().all()


def test_cart_value_and_has_cart(tiny_df):
    out = add_behaviour_features(fill_missing(tiny_df))
    assert out.loc[1, "cart_value"] == 600.0  # 3 items x 200
    assert list(out["has_cart"]) == [0, 1, 1]


def test_encode_device_is_one_hot(tiny_df):
    out = encode_device(tiny_df)
    assert "device" not in out.columns
    assert out.loc[0, "device_mobile"] == 1
    assert out.loc[0, "device_desktop"] == 0
    assert out[["device_mobile", "device_desktop", "device_tablet"]].sum().sum() == 3


def test_unknown_device_encodes_as_all_zero():
    df = pd.DataFrame({"device": ["smart-fridge"]})
    out = encode_device(df)
    assert out[["device_mobile", "device_desktop", "device_tablet"]].sum().sum() == 0


def test_build_features_returns_the_agreed_columns_in_order(tiny_df):
    out = build_features(tiny_df)
    assert list(out.columns) == FEATURE_COLUMNS
    assert len(out) == len(tiny_df)
    assert out.isna().sum().sum() == 0


def test_build_features_is_deterministic(raw_df):
    assert build_features(raw_df).equals(build_features(raw_df))
