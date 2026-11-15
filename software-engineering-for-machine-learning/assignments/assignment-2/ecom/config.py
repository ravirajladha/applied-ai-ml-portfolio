"""Central place for paths, schema and constants. No logic here."""

from pathlib import Path

# --- Paths -------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
ARTIFACT_DIR = ROOT_DIR / "artifacts"
LOG_DIR = ROOT_DIR / "logs"
REPORT_DIR = ROOT_DIR / "reports"

TRAIN_DATA_PATH = DATA_DIR / "sessions_train.csv"
LIVE_DATA_PATH = DATA_DIR / "sessions_live.csv"
MODEL_PATH = ARTIFACT_DIR / "model.joblib"
METRICS_PATH = ARTIFACT_DIR / "metrics.json"

# --- Data contract -----------------------------------------------------
TARGET = "converted"

# Column -> expected pandas dtype family. Used by the schema check.
RAW_SCHEMA = {
    "session_id": "object",
    "pages_viewed": "numeric",
    "session_duration_min": "numeric",
    "cart_items": "numeric",
    "avg_item_price": "numeric",
    "is_returning_user": "numeric",
    "discount_applied": "numeric",
    "device": "object",
}

DEVICES = ["mobile", "desktop", "tablet"]

# Columns the model actually sees after feature engineering.
FEATURE_COLUMNS = [
    "pages_viewed",
    "session_duration_min",
    "cart_items",
    "avg_item_price",
    "is_returning_user",
    "discount_applied",
    "pages_per_minute",
    "cart_value",
    "has_cart",
    "device_desktop",
    "device_mobile",
    "device_tablet",
]

# --- Thresholds --------------------------------------------------------
RANDOM_SEED = 42
TEST_SIZE = 0.2
MIN_ROWS = 100  # warn if a data file is too small to train on
MAX_MISSING_RATE = 0.05  # fail data quality above 5% missing in a column
DRIFT_THRESHOLD = 0.20  # flag drift if PSI > 0.20
MIN_ACCURACY = 0.70  # release gate
MIN_F1 = 0.60  # release gate
