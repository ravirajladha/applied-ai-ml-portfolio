"""REST API exposing the conversion model.

Endpoints
    GET  /health       liveness + whether a model is loaded
    GET  /model-info   version and expected features
    GET  /metrics      last training scorecard
    POST /predict      score one session
    POST /predict/batch  score up to 100 sessions
"""

import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status

from ecom import __version__
from ecom.config import METRICS_PATH
from ecom.exceptions import ModelNotReadyError
from ecom.logging_setup import get_logger
from ecom.predict import ConversionPredictor
from ecom.schemas import (
    BatchRequest,
    BatchResponse,
    HealthResponse,
    ModelInfoResponse,
    PredictionResponse,
    SessionRequest,
)

logger = get_logger(__name__)

predictor = ConversionPredictor()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the model once at startup instead of on every request."""
    try:
        predictor.load()
    except ModelNotReadyError as exc:
        # Start anyway so /health can report the problem honestly.
        logger.error("Starting without a model: %s", exc)
    yield
    logger.info("API shutting down")


app = FastAPI(
    title="E-commerce Conversion Prediction API",
    description="Predicts whether a browsing session will end in a purchase.",
    version=__version__,
    lifespan=lifespan,
)


def _require_model() -> ConversionPredictor:
    """503 is the honest answer when the model is missing - not 500."""
    if not predictor.is_ready:
        logger.error("Request rejected: model not loaded")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded. Train the model and restart the service.",
        )
    return predictor


@app.get("/health", response_model=HealthResponse, tags=["ops"])
def health() -> HealthResponse:
    """Liveness probe - always 200 so the pod is not killed for a missing model."""
    return HealthResponse(
        status="ok" if predictor.is_ready else "degraded",
        model_loaded=predictor.is_ready,
        api_version=__version__,
    )


@app.get("/model-info", response_model=ModelInfoResponse, tags=["ops"])
def model_info() -> ModelInfoResponse:
    """What model is actually serving traffic right now."""
    model = _require_model()
    return ModelInfoResponse(
        model_version=model.version,
        features=model.features,
        n_features=len(model.features),
    )


@app.get("/metrics", tags=["ops"])
def metrics() -> dict:
    """Last training scorecard, straight from the artifact folder."""
    if not METRICS_PATH.exists():
        logger.warning("Metrics requested but %s is missing", METRICS_PATH)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No metrics available. Run training first.",
        )
    return json.loads(METRICS_PATH.read_text(encoding="utf-8"))


@app.post(
    "/predict",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    tags=["inference"],
)
def predict(request: SessionRequest) -> PredictionResponse:
    """Score a single session."""
    model = _require_model()
    try:
        result = model.predict([request.model_dump()])[0]
    except Exception as exc:  # unexpected scoring failure
        logger.error("Prediction failed for %s: %s", request.session_id, exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Prediction failed",
        ) from exc

    logger.info(
        "session=%s prob=%.4f band=%s",
        request.session_id,
        result["conversion_probability"],
        result["intent_band"],
    )
    return PredictionResponse(session_id=request.session_id, **result)


@app.post(
    "/predict/batch",
    response_model=BatchResponse,
    status_code=status.HTTP_200_OK,
    tags=["inference"],
)
def predict_batch(request: BatchRequest) -> BatchResponse:
    """Score many sessions in one call."""
    model = _require_model()
    rows = [s.model_dump() for s in request.sessions]
    try:
        results = model.predict(rows)
    except Exception as exc:
        logger.error("Batch prediction failed for %d rows: %s", len(rows), exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Batch prediction failed",
        ) from exc

    predictions = [
        PredictionResponse(session_id=row["session_id"], **result)
        for row, result in zip(rows, results)
    ]
    logger.info("Batch scored %d sessions", len(predictions))
    return BatchResponse(count=len(predictions), predictions=predictions)
