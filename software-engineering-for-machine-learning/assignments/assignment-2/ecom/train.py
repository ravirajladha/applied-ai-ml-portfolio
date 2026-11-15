"""Model training: raw CSV -> validated data -> features -> saved artifact."""

import json
import warnings

import joblib
import numpy as np
import pandas as pd
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from ecom import __version__
from ecom.config import (
    ARTIFACT_DIR,
    FEATURE_COLUMNS,
    METRICS_PATH,
    MIN_ACCURACY,
    MIN_F1,
    MODEL_PATH,
    RANDOM_SEED,
    TARGET,
    TEST_SIZE,
    TRAIN_DATA_PATH,
)
from ecom.data_ingestion import DataIngestor
from ecom.data_validation import DataValidator
from ecom.features import build_features
from ecom.logging_setup import get_logger
from ecom.metrics import calibration_table, evaluate_model

logger = get_logger(__name__)


class ModelTrainer:
    """Trains and saves the conversion model."""

    def __init__(self, seed: int = RANDOM_SEED, max_iter: int = 500) -> None:
        self.seed = seed
        self.max_iter = max_iter
        self.pipeline: Pipeline | None = None

    def _new_pipeline(self, max_iter: int | None = None) -> Pipeline:
        """Scaler + logistic regression. Scaling lives inside the pipeline so
        serving cannot forget it."""
        return Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "model",
                    LogisticRegression(
                        max_iter=max_iter or self.max_iter,
                        random_state=self.seed,
                    ),
                ),
            ]
        )

    def fit(self, X: pd.DataFrame, y: pd.Series) -> Pipeline:
        """Fit the pipeline on the given features."""
        logger.info("Training on %d rows, %d features", len(X), X.shape[1])
        self.pipeline = self._new_pipeline()
        self.pipeline.fit(X, y)
        return self.pipeline

    def loss_curve(self, X: pd.DataFrame, y: pd.Series, steps=(1, 2, 5, 10, 50, 200)):
        """Training log-loss at increasing optimiser budgets.

        Used by the QA suite to assert that the loss actually goes down.
        """
        losses = []
        for step in steps:
            pipe = self._new_pipeline(max_iter=step)
            with warnings.catch_warnings():
                # Low budgets are meant to stop early - that is the point.
                warnings.simplefilter("ignore", ConvergenceWarning)
                pipe.fit(X, y)
            losses.append(round(float(log_loss(y, pipe.predict_proba(X)[:, 1])), 6))
        logger.info("Loss curve %s -> %s", list(steps), losses)
        return losses

    def save(self, path=MODEL_PATH) -> None:
        """Persist the fitted pipeline plus the feature order it expects."""
        if self.pipeline is None:
            raise RuntimeError("Nothing to save - call fit() first")
        ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
        joblib.dump(
            {
                "pipeline": self.pipeline,
                "features": FEATURE_COLUMNS,
                "version": __version__,
            },
            path,
        )
        logger.info("Model saved to %s", path)


def run_training(data_path=TRAIN_DATA_PATH) -> dict:
    """End-to-end training run. Returns the metrics report."""
    raw = DataIngestor(data_path).load()
    DataValidator().validate(raw)

    X = build_features(raw)
    y = raw[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_SEED, stratify=y
    )

    trainer = ModelTrainer()
    pipeline = trainer.fit(X_train, y_train)

    y_prob = pipeline.predict_proba(X_test)[:, 1]
    scores = evaluate_model(y_test, y_prob)

    # Release gate: a model below these numbers is not worth shipping.
    if scores["accuracy"] < MIN_ACCURACY or scores["f1"] < MIN_F1:
        logger.warning(
            "Model below release gate (accuracy=%.3f, f1=%.3f)",
            scores["accuracy"],
            scores["f1"],
        )
    else:
        logger.info("Model passed the release gate")

    trainer.save()

    report = {
        "version": __version__,
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "model_quality": scores,
        "calibration": calibration_table(np.asarray(y_test), y_prob),
        "loss_curve": trainer.loss_curve(X_train, y_train),
        "release_gate": {
            "min_accuracy": MIN_ACCURACY,
            "min_f1": MIN_F1,
            "passed": scores["accuracy"] >= MIN_ACCURACY and scores["f1"] >= MIN_F1,
        },
    }
    METRICS_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logger.info("Metrics written to %s", METRICS_PATH)
    return report


if __name__ == "__main__":
    run_training()
