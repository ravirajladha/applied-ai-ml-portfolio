# fastapi-ml-crud

A minimal **FastAPI** REST API for learning ML/AI back-end workflows. It's an
**ML Experiment Tracker API** with full CRUD (Create, Read, Update, Delete) and
demonstrates the two headline FastAPI features:

- **Pydantic models** — request/response validation, typing, and automatic
  `422` errors on bad input (see the `Experiment*` models in `main.py`)
- **Automatic interactive docs** — **Swagger UI** and ReDoc generated from your
  code with zero extra work

## Run it

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open:

| URL                                   | What it is                          |
|---------------------------------------|-------------------------------------|
| <http://127.0.0.1:8000/docs>          | **Swagger UI** — try endpoints live |
| <http://127.0.0.1:8000/redoc>         | ReDoc documentation                 |
| <http://127.0.0.1:8000/openapi.json>  | Raw OpenAPI schema                   |

## Endpoints

| Method   | Path                        | Description            |
|----------|-----------------------------|------------------------|
| `GET`    | `/experiments`              | List all experiments   |
| `POST`   | `/experiments`              | Create an experiment   |
| `GET`    | `/experiments/{id}`         | Get one experiment     |
| `PUT`    | `/experiments/{id}`         | Update an experiment   |
| `DELETE` | `/experiments/{id}`         | Delete an experiment   |

## Pydantic in this project

`main.py` defines several models to make the API surface explicit:

- `ExperimentCreate` — the create payload; `name` is required, `accuracy` must
  be between `0` and `1` (enforced by `Field(ge=0.0, le=1.0)`)
- `ExperimentUpdate` — all fields optional, for partial updates
- `Experiment` — the response model, adding server-set `id` and `created_at`

Because these are Pydantic models, FastAPI validates every request against them
automatically and documents them in the Swagger schema.

## Data storage

To keep the focus on FastAPI, Pydantic, and Swagger, records are kept in an
in-memory dict (they reset when the server restarts). Swap in a database when
you're ready — the sibling `flask-ml-crud` project shows a SQLite approach.
```
