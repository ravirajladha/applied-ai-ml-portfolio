"""Request/response contracts for the REST API.

Pydantic enforces these at the edge, so bad or hostile input is rejected
with a 422 before it can ever reach the model.
"""

from typing import Literal

from pydantic import BaseModel, Field


class SessionRequest(BaseModel):
    """One browsing session to score."""

    session_id: str = Field(..., min_length=1, max_length=64, examples=["s000123"])
    pages_viewed: int = Field(..., ge=0, le=500)
    session_duration_min: float = Field(..., ge=0, le=600)
    cart_items: int = Field(..., ge=0, le=100)
    avg_item_price: float = Field(0.0, ge=0, le=1_000_000)
    is_returning_user: int = Field(..., ge=0, le=1)
    discount_applied: int = Field(0, ge=0, le=1)
    device: Literal["mobile", "desktop", "tablet"]

    model_config = {
        "extra": "forbid",  # unknown fields are rejected, not silently ignored
        "json_schema_extra": {
            "example": {
                "session_id": "s000123",
                "pages_viewed": 12,
                "session_duration_min": 8.5,
                "cart_items": 2,
                "avg_item_price": 799.0,
                "is_returning_user": 1,
                "discount_applied": 0,
                "device": "mobile",
            }
        },
    }


class BatchRequest(BaseModel):
    """Up to 100 sessions at a time - a bounded payload is a safer payload."""

    sessions: list[SessionRequest] = Field(..., min_length=1, max_length=100)


class PredictionResponse(BaseModel):
    """What the caller gets back."""

    session_id: str
    conversion_probability: float = Field(..., ge=0.0, le=1.0)
    will_convert: bool
    intent_band: Literal["low", "medium", "high"]
    model_version: str


class BatchResponse(BaseModel):
    count: int
    predictions: list[PredictionResponse]


class HealthResponse(BaseModel):
    status: Literal["ok", "degraded"]
    model_loaded: bool
    api_version: str


class ModelInfoResponse(BaseModel):
    model_version: str
    features: list[str]
    n_features: int
