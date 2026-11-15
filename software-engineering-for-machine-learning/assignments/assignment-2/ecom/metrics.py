"""Model quality metrics.

accuracy / F1 say whether the label is right; roc_auc says whether the
ranking is right; brier score says whether the probability is honest.
"""

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    brier_score_loss,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from ecom.logging_setup import get_logger

logger = get_logger(__name__)


def evaluate_model(y_true: np.ndarray, y_prob: np.ndarray, threshold: float = 0.5):
    """Return the model quality scorecard for one dataset."""
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob)
    y_pred = (y_prob >= threshold).astype(int)

    scores = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_true, y_prob)),
        "brier_score": float(brier_score_loss(y_true, y_prob)),
    }
    scores = {k: round(v, 4) for k, v in scores.items()}
    logger.info("Model quality: %s", scores)
    return scores


def calibration_table(y_true: np.ndarray, y_prob: np.ndarray, bins: int = 5):
    """Predicted vs actual conversion rate per probability band."""
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob)
    edges = np.linspace(0.0, 1.0, bins + 1)
    rows = []
    for low, high in zip(edges[:-1], edges[1:]):
        mask = (y_prob >= low) & (y_prob < high)
        if not mask.any():
            continue
        rows.append(
            {
                "bucket": f"{low:.1f}-{high:.1f}",
                "count": int(mask.sum()),
                "predicted_rate": round(float(y_prob[mask].mean()), 4),
                "actual_rate": round(float(y_true[mask].mean()), 4),
            }
        )
    return rows
