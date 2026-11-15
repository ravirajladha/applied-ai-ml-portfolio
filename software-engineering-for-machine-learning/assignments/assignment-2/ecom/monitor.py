"""Data quality monitor.

Compares today's live traffic against the training data and writes a
report. This is what you would run on a schedule in production.
"""

import json

from ecom.config import LIVE_DATA_PATH, REPORT_DIR, TRAIN_DATA_PATH
from ecom.data_ingestion import DataIngestor
from ecom.data_validation import DataValidator, detect_drift
from ecom.logging_setup import get_logger

logger = get_logger(__name__)

# Numeric columns worth watching for drift.
MONITORED_COLUMNS = [
    "pages_viewed",
    "session_duration_min",
    "cart_items",
    "avg_item_price",
]


def run_data_quality_check(baseline_path=TRAIN_DATA_PATH, live_path=LIVE_DATA_PATH):
    """Validate live data and compare its distribution to the baseline."""
    baseline = DataIngestor(baseline_path).load()
    live = DataIngestor(live_path).load()

    # strict=False: a monitor reports, it does not crash the pipeline.
    validation = DataValidator().validate(live, strict=False)
    drift = detect_drift(baseline, live, MONITORED_COLUMNS)

    report = {
        "baseline_rows": len(baseline),
        "live_rows": len(live),
        "validation": validation.as_dict(),
        "drift_psi": drift,
        "drifted_columns": [c for c, psi in drift.items() if psi > 0.20],
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORT_DIR / "data_quality.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logger.info("Data quality report written to %s", path)

    if report["drifted_columns"]:
        logger.warning("Retraining suggested - drifted: %s", report["drifted_columns"])
    return report


if __name__ == "__main__":
    run_data_quality_check()
