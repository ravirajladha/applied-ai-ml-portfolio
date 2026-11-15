"""Data ingestion: create the demo dataset and load it from disk.

Real systems read from a warehouse; here we generate a reproducible
synthetic clickstream so the whole assignment runs offline.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from ecom.config import (
    DATA_DIR,
    DEVICES,
    LIVE_DATA_PATH,
    MIN_ROWS,
    RANDOM_SEED,
    TARGET,
    TRAIN_DATA_PATH,
)
from ecom.exceptions import DataIngestionError
from ecom.logging_setup import get_logger

logger = get_logger(__name__)


class SessionDataGenerator:
    """Builds a synthetic e-commerce session dataset."""

    def __init__(self, seed: int = RANDOM_SEED) -> None:
        self.rng = np.random.default_rng(seed)

    def generate(self, n_rows: int = 5000, drifted: bool = False) -> pd.DataFrame:
        """Return n_rows sessions. drifted=True shifts the traffic mix."""
        rng = self.rng

        # Drifted traffic = shorter, more mobile-heavy sessions.
        page_mean = 4.0 if drifted else 7.0
        device_p = [0.75, 0.15, 0.10] if drifted else [0.45, 0.40, 0.15]

        pages = np.clip(rng.poisson(page_mean, n_rows), 1, None)
        duration = np.round(pages * rng.uniform(0.3, 1.5, n_rows), 2)
        cart_items = rng.binomial(3, 0.35, n_rows)
        price = np.round(rng.gamma(shape=3.0, scale=250.0, size=n_rows), 2)
        returning = rng.binomial(1, 0.4, n_rows)
        discount = rng.binomial(1, 0.3, n_rows)
        device = rng.choice(DEVICES, size=n_rows, p=device_p)

        # Latent conversion score -> probability -> label.
        score = (
            -3.0
            + 0.18 * pages
            + 1.30 * cart_items
            + 0.80 * returning
            + 0.70 * discount
            - 0.0004 * price
        )
        prob = 1.0 / (1.0 + np.exp(-score))
        converted = rng.binomial(1, prob)

        df = pd.DataFrame(
            {
                "session_id": [f"s{i:06d}" for i in range(n_rows)],
                "pages_viewed": pages,
                "session_duration_min": duration,
                "cart_items": cart_items,
                "avg_item_price": price,
                "is_returning_user": returning,
                "discount_applied": discount,
                "device": device,
                TARGET: converted,
            }
        )

        # Sprinkle a few missing prices - real feeds are never perfect.
        holes = rng.choice(n_rows, size=max(1, n_rows // 100), replace=False)
        df.loc[holes, "avg_item_price"] = np.nan

        logger.info(
            "Generated %d sessions (drifted=%s, conversion rate=%.3f)",
            n_rows,
            drifted,
            df[TARGET].mean(),
        )
        return df


class DataIngestor:
    """Reads session data from a CSV file."""

    def __init__(self, path: Path = TRAIN_DATA_PATH) -> None:
        self.path = Path(path)

    def load(self) -> pd.DataFrame:
        """Load the CSV, or raise a clear error if it is unusable."""
        logger.info("Loading data from %s", self.path)
        if not self.path.exists():
            logger.error("Data file not found: %s", self.path)
            raise DataIngestionError(f"Data file not found: {self.path}")

        try:
            df = pd.read_csv(self.path)
        except Exception as exc:  # unreadable / corrupt file
            logger.error("Failed to read %s: %s", self.path, exc)
            raise DataIngestionError(f"Could not read {self.path}") from exc

        if df.empty:
            logger.error("Data file is empty: %s", self.path)
            raise DataIngestionError(f"Data file is empty: {self.path}")

        # Too few rows is not fatal, but a model trained on them is worthless.
        if len(df) < MIN_ROWS:
            logger.warning(
                "Only %d rows in %s - below the %d row minimum for training",
                len(df),
                self.path,
                MIN_ROWS,
            )

        logger.info("Loaded %d rows, %d columns", len(df), df.shape[1])
        return df


def build_demo_datasets(n_rows: int = 5000) -> None:
    """Write a training file and a drifted 'live traffic' file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SessionDataGenerator(RANDOM_SEED).generate(n_rows).to_csv(
        TRAIN_DATA_PATH, index=False
    )
    SessionDataGenerator(RANDOM_SEED + 1).generate(n_rows // 2, drifted=True).to_csv(
        LIVE_DATA_PATH, index=False
    )
    logger.info("Datasets written to %s", DATA_DIR)


if __name__ == "__main__":
    build_demo_datasets()
