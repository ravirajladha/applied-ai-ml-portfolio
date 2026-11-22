"""M3 · One feature pipeline, used by BOTH training and serving.

If training computes "is it peak hour?" one way and the API computes it another way, the model silently gets
different inputs in production. That bug has a name: **training-serving skew**. The fix is boring and powerful:
one function, imported by both sides.
"""
import pandas as pd

from .data import FEATURES

PEAK_HOURS = (13, 14, 20, 21)
MODEL_INPUTS = ["distance_km", "items", "prep_min", "is_raining", "is_peak"]


def validate(df: pd.DataFrame) -> None:
    """Fail fast on bad input, like request validation in any API."""
    missing = [c for c in FEATURES if c not in df.columns]
    if missing:
        raise ValueError(f"missing columns: {missing}")
    if (df["distance_km"] <= 0).any():
        raise ValueError("distance_km must be positive")
    if not df["hour"].between(0, 23).all():
        raise ValueError("hour must be 0-23")


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    validate(df)
    out = df[["distance_km", "items", "prep_min", "is_raining"]].astype(float).copy()
    out["is_peak"] = df["hour"].isin(PEAK_HOURS).astype(float)
    return out[MODEL_INPUTS]
