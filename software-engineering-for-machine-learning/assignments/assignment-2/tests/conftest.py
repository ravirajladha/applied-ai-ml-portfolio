"""Shared fixtures for the test suite."""

import pandas as pd
import pytest

from ecom.data_ingestion import SessionDataGenerator


@pytest.fixture
def raw_df() -> pd.DataFrame:
    """A small, reproducible raw dataset."""
    return SessionDataGenerator(seed=7).generate(400)


@pytest.fixture
def tiny_df() -> pd.DataFrame:
    """A handful of rows for fast, exact assertions."""
    return pd.DataFrame(
        {
            "session_id": ["a", "b", "c"],
            "pages_viewed": [1, 10, 4],
            "session_duration_min": [0.0, 9.0, 3.0],
            "cart_items": [0, 3, 1],
            "avg_item_price": [100.0, 200.0, None],
            "is_returning_user": [0, 1, 1],
            "discount_applied": [0, 1, 0],
            "device": ["mobile", "desktop", "tablet"],
        }
    )


@pytest.fixture
def sample_session() -> dict:
    """One valid API payload."""
    return {
        "session_id": "s000123",
        "pages_viewed": 12,
        "session_duration_min": 8.5,
        "cart_items": 2,
        "avg_item_price": 799.0,
        "is_returning_user": 1,
        "discount_applied": 0,
        "device": "mobile",
    }
