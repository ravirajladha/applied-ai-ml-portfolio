"""fastapi-ml-crud

A minimal FastAPI application for learning ML/AI back-end workflows. It exposes
a full CRUD (Create, Read, Update, Delete) REST API over a table of ML
"experiments" and demonstrates the two things FastAPI is loved for:

  * **Pydantic models** for request/response validation and typing
  * **Automatic interactive API docs** (Swagger UI at /docs, ReDoc at /redoc)

Run it with:

    uvicorn main:app --reload

then open:

    http://127.0.0.1:8000/docs      <- Swagger UI (try the endpoints here)
    http://127.0.0.1:8000/redoc     <- ReDoc
    http://127.0.0.1:8000/openapi.json  <- raw OpenAPI schema
"""

from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Pydantic models
#
# We keep three models so the API surface is explicit:
#   * ExperimentCreate  -> what the client sends to create a record
#   * ExperimentUpdate  -> what the client sends to update a record
#   * Experiment        -> what the API sends back (includes server fields)
# Pydantic validates every incoming request against these automatically and
# turns validation failures into clean 422 responses.
# ---------------------------------------------------------------------------


class ExperimentBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Human-readable name of the experiment.",
        examples=["Iris baseline"],
    )
    algorithm: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Algorithm or model family used.",
        examples=["RandomForest"],
    )
    accuracy: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Validation accuracy, between 0 and 1.",
        examples=[0.947],
    )
    notes: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Free-form notes: hyperparameters, dataset, observations.",
        examples=["50 trees, max_depth=8"],
    )


class ExperimentCreate(ExperimentBase):
    """Payload for creating an experiment."""


class ExperimentUpdate(BaseModel):
    """Payload for updating an experiment. Every field is optional so a client
    can send a partial update (PATCH-style)."""

    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    algorithm: Optional[str] = Field(default=None, max_length=100)
    accuracy: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    notes: Optional[str] = Field(default=None, max_length=1000)


class Experiment(ExperimentBase):
    """Full experiment as returned by the API."""

    id: int = Field(..., description="Server-assigned unique id.")
    created_at: datetime = Field(..., description="Creation timestamp (UTC).")


# ---------------------------------------------------------------------------
# In-memory "database"
#
# A real project would use a database (SQLAlchemy, Tortoise, etc.). To keep the
# focus on FastAPI + Pydantic + Swagger, we store records in a plain dict.
# ---------------------------------------------------------------------------

_experiments: dict[int, Experiment] = {}
_next_id = 1


def _create(payload: ExperimentCreate) -> Experiment:
    global _next_id
    experiment = Experiment(
        id=_next_id,
        created_at=datetime.now(timezone.utc),
        **payload.model_dump(),
    )
    _experiments[_next_id] = experiment
    _next_id += 1
    return experiment


# Seed one row so the docs and list endpoint show something on first launch.
_create(
    ExperimentCreate(
        name="Iris baseline",
        algorithm="RandomForest",
        accuracy=0.947,
        notes="50 trees, max_depth=8",
    )
)


# ---------------------------------------------------------------------------
# FastAPI app
#
# The title/description/version below show up at the top of the Swagger UI.
# ---------------------------------------------------------------------------

app = FastAPI(
    title="ML Experiment Tracker API",
    description=(
        "A tiny FastAPI CRUD service for tracking machine-learning "
        "experiments. Built for learning ML/AI back-end workflows — explore "
        "and try every endpoint live in the Swagger UI below."
    ),
    version="1.0.0",
)


@app.get("/", tags=["meta"], summary="API root / quick links")
def root():
    return {
        "message": "ML Experiment Tracker API",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
    }


@app.get(
    "/experiments",
    response_model=list[Experiment],
    tags=["experiments"],
    summary="List all experiments",
)
def list_experiments():
    return list(_experiments.values())


@app.post(
    "/experiments",
    response_model=Experiment,
    status_code=status.HTTP_201_CREATED,
    tags=["experiments"],
    summary="Create an experiment",
)
def create_experiment(payload: ExperimentCreate):
    return _create(payload)


@app.get(
    "/experiments/{experiment_id}",
    response_model=Experiment,
    tags=["experiments"],
    summary="Get one experiment by id",
)
def get_experiment(experiment_id: int):
    experiment = _experiments.get(experiment_id)
    if experiment is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return experiment


@app.put(
    "/experiments/{experiment_id}",
    response_model=Experiment,
    tags=["experiments"],
    summary="Update an experiment",
)
def update_experiment(experiment_id: int, payload: ExperimentUpdate):
    existing = _experiments.get(experiment_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Experiment not found")

    # Only overwrite the fields the client actually sent.
    updates = payload.model_dump(exclude_unset=True)
    updated = existing.model_copy(update=updates)
    _experiments[experiment_id] = updated
    return updated


@app.delete(
    "/experiments/{experiment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["experiments"],
    summary="Delete an experiment",
)
def delete_experiment(experiment_id: int):
    if experiment_id not in _experiments:
        raise HTTPException(status_code=404, detail="Experiment not found")
    del _experiments[experiment_id]
    return None
