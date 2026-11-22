"""M3 · Model registry (a tiny stand-in for the MLflow Model Registry).

The registry is the single source of truth for "which model version is live".
Each version has a stage: None -> Staging -> Production -> Archived.
Serving code never loads "model.pkl from someone's laptop"; it asks the registry for the Production version.

SDE analogy: a container registry with tags, where `production` is a movable tag.
"""
import json
import shutil
import time
from pathlib import Path

STAGES = ("None", "Staging", "Production", "Archived")


class Registry:
    def __init__(self, root: str | Path = "registry"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.index = self.root / "index.json"
        if not self.index.exists():
            self.index.write_text("[]")

    def _load(self) -> list[dict]:
        return json.loads(self.index.read_text())

    def _save(self, versions: list[dict]) -> None:
        self.index.write_text(json.dumps(versions, indent=2))

    def register(self, model_path: str | Path, run_id: str, metrics: dict) -> int:
        versions = self._load()
        version = len(versions) + 1
        dest = self.root / f"v{version}.joblib"
        shutil.copy(model_path, dest)
        versions.append({"version": version, "path": str(dest), "run_id": run_id,
                         "metrics": metrics, "stage": "None", "registered_at": time.time()})
        self._save(versions)
        return version

    def promote(self, version: int, stage: str) -> None:
        if stage not in STAGES:
            raise ValueError(f"stage must be one of {STAGES}")
        versions = self._load()
        for v in versions:
            if stage == "Production" and v["stage"] == "Production":
                v["stage"] = "Archived"            # only one Production version at a time
            if v["version"] == version:
                v["stage"] = stage
        self._save(versions)

    def get(self, stage: str = "Production") -> dict | None:
        matches = [v for v in self._load() if v["stage"] == stage]
        return matches[-1] if matches else None

    def versions(self) -> list[dict]:
        return self._load()
