"""Feature engineering - written as pure functions.

Same input always gives the same output, no hidden state, so training and
serving cannot drift apart and every step is trivial to unit test.
"""

import pandas as pd

from ecom.config import DEVICES, FEATURE_COLUMNS
from ecom.logging_setup import get_logger

logger = get_logger(__name__)


def fill_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Replace null prices with 0 - a session with no price has no cart value."""
    out = df.copy()
    missing = int(out["avg_item_price"].isna().sum())
    if missing:
        logger.warning("Imputing %d missing avg_item_price values with 0", missing)
    out["avg_item_price"] = out["avg_item_price"].fillna(0.0)
    return out


def add_behaviour_features(df: pd.DataFrame) -> pd.DataFrame:
    """Derived signals: browsing speed, cart value, and whether a cart exists."""
    out = df.copy()
    # +1 avoids divide-by-zero on instant bounces.
    out["pages_per_minute"] = out["pages_viewed"] / (out["session_duration_min"] + 1.0)
    out["cart_value"] = out["cart_items"] * out["avg_item_price"]
    out["has_cart"] = (out["cart_items"] > 0).astype(int)
    return out


def encode_device(df: pd.DataFrame) -> pd.DataFrame:
    """One-hot the device column, always producing the same three columns."""
    out = df.copy()
    device = out["device"].astype(str).str.lower()
    for name in DEVICES:
        out[f"device_{name}"] = (device == name).astype(int)

    unknown = int((~device.isin(DEVICES)).sum())
    if unknown:
        logger.warning("%d rows have an unknown device, encoded as all-zero", unknown)
    return out.drop(columns=["device"])


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Full pipeline: raw sessions -> model-ready feature matrix."""
    out = fill_missing(df)
    out = add_behaviour_features(out)
    out = encode_device(out)
    logger.info("Built %d features for %d rows", len(FEATURE_COLUMNS), len(out))
    return out[FEATURE_COLUMNS]
