"""M6 · Monitoring: has the world changed since training?

Two kinds of signal:
1. **Data drift** (no labels needed): compare each input feature's distribution today vs. at training time.
   We use PSI (Population Stability Index). Rule of thumb: < 0.1 stable, 0.1-0.25 watch, > 0.25 alert.
2. **Performance** (needs labels, which arrive later): once real delivery times come in, compute MAE.

Real tools: Evidently, Arize, WhyLabs, Prometheus + Grafana for the system metrics.
"""
import numpy as np
import pandas as pd

PSI_WATCH, PSI_ALERT = 0.10, 0.25


def psi(expected: np.ndarray, actual: np.ndarray, bins: int = 10) -> float:
    """PSI = sum over bins of (a% - e%) * ln(a% / e%). Bins come from the training (expected) data."""
    expected, actual = np.asarray(expected, float), np.asarray(actual, float)
    edges = np.unique(np.quantile(expected, np.linspace(0, 1, bins + 1)))
    if len(edges) < 3:                                   # (almost) constant or binary feature: use its values
        values = np.unique(np.concatenate([expected, actual]))
        e = np.array([(expected == v).mean() for v in values])
        a = np.array([(actual == v).mean() for v in values])
    else:
        edges[0], edges[-1] = -np.inf, np.inf
        e = np.histogram(expected, edges)[0] / len(expected)
        a = np.histogram(actual, edges)[0] / len(actual)
    e, a = np.clip(e, 1e-4, None), np.clip(a, 1e-4, None)
    return float(np.sum((a - e) * np.log(a / e)))


def drift_report(train_df: pd.DataFrame, live_df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    rows = []
    for c in columns:
        value = psi(train_df[c], live_df[c])
        status = "ALERT" if value > PSI_ALERT else "watch" if value > PSI_WATCH else "ok"
        rows.append({"feature": c, "psi": round(value, 3), "status": status})
    return pd.DataFrame(rows).sort_values("psi", ascending=False).reset_index(drop=True)


def should_retrain(report: pd.DataFrame, live_mae: float | None = None, max_mae: float = 6.0) -> tuple[bool, str]:
    alerts = report.loc[report["status"] == "ALERT", "feature"].tolist()
    if live_mae is not None and live_mae > max_mae:
        return True, f"live MAE {live_mae:.2f} above {max_mae}"
    if alerts:
        return True, f"drift alert on {alerts}"
    return False, "stable"
