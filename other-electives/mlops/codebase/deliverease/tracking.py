"""M3 · Experiment tracking (a tiny stand-in for MLflow Tracking).

Every training run is recorded: what went in (params, data version), what came out (metrics, model file).
Without this, "which model is in production and how was it trained?" has no answer.

Real tools: MLflow, Weights & Biases, Neptune. Same idea: one folder/row per run.
"""
import json
import time
import uuid
from pathlib import Path


class Tracker:
    def __init__(self, root: str | Path = "runs"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def log_run(self, params: dict, metrics: dict, artifact: str | None = None, tags: dict | None = None) -> str:
        run_id = time.strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:6]
        record = {"run_id": run_id, "params": params, "metrics": metrics,
                  "artifact": artifact, "tags": tags or {}, "logged_at": time.time()}
        (self.root / f"{run_id}.json").write_text(json.dumps(record, indent=2))
        return run_id

    def runs(self) -> list[dict]:
        return sorted((json.loads(p.read_text()) for p in self.root.glob("*.json")), key=lambda r: r["logged_at"])

    def best(self, metric: str, lower_is_better: bool = True) -> dict:
        runs = [r for r in self.runs() if metric in r["metrics"]]
        return sorted(runs, key=lambda r: r["metrics"][metric], reverse=not lower_is_better)[0]
