"""Inference: load the saved artifact and score sessions."""

import joblib
import pandas as pd

from ecom.config import MODEL_PATH
from ecom.exceptions import ModelNotReadyError
from ecom.features import build_features
from ecom.logging_setup import get_logger

logger = get_logger(__name__)

# Business labels for the probability bands.
HIGH_INTENT = 0.60
LOW_INTENT = 0.25


def intent_band(probability: float) -> str:
    """Turn a raw probability into something a marketer can act on."""
    if probability >= HIGH_INTENT:
        return "high"
    if probability >= LOW_INTENT:
        return "medium"
    return "low"


class ConversionPredictor:
    """Wraps the trained pipeline behind a small, safe interface."""

    def __init__(self, model_path=MODEL_PATH) -> None:
        self.model_path = model_path
        self.pipeline = None
        self.features: list[str] = []
        self.version = "unknown"

    def load(self) -> "ConversionPredictor":
        """Load the artifact. Raises ModelNotReadyError if it is unusable."""
        if not self.model_path.exists():
            logger.error("Model artifact not found at %s", self.model_path)
            raise ModelNotReadyError(f"No model at {self.model_path}. Train first.")
        try:
            bundle = joblib.load(self.model_path)
            self.pipeline = bundle["pipeline"]
            self.features = bundle["features"]
            self.version = bundle.get("version", "unknown")
        except Exception as exc:  # corrupt or incompatible artifact
            logger.error("Failed to load model: %s", exc)
            raise ModelNotReadyError("Model artifact could not be loaded") from exc

        logger.info("Model v%s loaded from %s", self.version, self.model_path)
        return self

    @property
    def is_ready(self) -> bool:
        return self.pipeline is not None

    def predict(self, sessions: list[dict] | pd.DataFrame) -> list[dict]:
        """Score one or more sessions. Returns probability + label + band."""
        if not self.is_ready:
            raise ModelNotReadyError("Model is not loaded - call load() first")

        df = (
            pd.DataFrame(sessions)
            if not isinstance(sessions, pd.DataFrame)
            else sessions
        )
        if df.empty:
            logger.warning("predict() called with no sessions")
            return []

        X = build_features(df)[self.features]
        probs = self.pipeline.predict_proba(X)[:, 1]

        results = [
            {
                "conversion_probability": round(float(p), 4),
                "will_convert": bool(p >= 0.5),
                "intent_band": intent_band(float(p)),
                "model_version": self.version,
            }
            for p in probs
        ]
        logger.info("Scored %d session(s)", len(results))
        return results
