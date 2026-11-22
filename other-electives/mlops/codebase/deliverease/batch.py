"""M4/M5 · Batch (offline) prediction.

Not every prediction needs an API. If the business needs "tomorrow's expected delivery times for all
scheduled orders" once a night, a batch job is simpler and cheaper: read a file, score every row, write a file.
"""
from pathlib import Path

import joblib
import pandas as pd

from .features import build_features
from .registry import Registry


def score_file(in_csv: str | Path, out_csv: str | Path, registry_dir: str | Path) -> int:
    prod = Registry(registry_dir).get("Production")
    if prod is None:
        raise RuntimeError("no production model")
    model = joblib.load(prod["path"])
    df = pd.read_csv(in_csv)
    df["eta_min"] = model.predict(build_features(df)).round(1)
    df["model_version"] = prod["version"]
    df.to_csv(out_csv, index=False)
    return len(df)
