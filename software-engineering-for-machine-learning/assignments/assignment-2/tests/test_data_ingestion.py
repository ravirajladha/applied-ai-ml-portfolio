"""Unit tests for ingestion - the error handling and logging of Task 3."""

import logging

import pandas as pd
import pytest

from ecom.config import MIN_ROWS
from ecom.data_ingestion import DataIngestor, SessionDataGenerator
from ecom.exceptions import DataIngestionError


def test_missing_file_raises(tmp_path):
    with pytest.raises(DataIngestionError, match="not found"):
        DataIngestor(tmp_path / "nope.csv").load()


def test_empty_file_raises(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("session_id,pages_viewed\n", encoding="utf-8")
    with pytest.raises(DataIngestionError, match="empty"):
        DataIngestor(path).load()


def test_corrupt_file_raises(tmp_path):
    path = tmp_path / "corrupt.csv"
    path.write_text('a,b\n"unclosed,1\n2', encoding="utf-8")
    with pytest.raises(DataIngestionError):
        DataIngestor(path).load()


def test_small_file_warns_but_still_loads(tmp_path, caplog):
    path = tmp_path / "tiny.csv"
    pd.DataFrame({"session_id": ["a", "b"]}).to_csv(path, index=False)

    with caplog.at_level(logging.WARNING, logger="ecom.data_ingestion"):
        df = DataIngestor(path).load()

    assert len(df) == 2  # a warning, not an error
    assert str(MIN_ROWS) in caplog.text


def test_generator_is_reproducible():
    a = SessionDataGenerator(seed=3).generate(50)
    b = SessionDataGenerator(seed=3).generate(50)
    assert a.equals(b)


def test_drifted_traffic_really_is_different():
    normal = SessionDataGenerator(seed=3).generate(2000)
    drifted = SessionDataGenerator(seed=4).generate(2000, drifted=True)
    assert drifted["pages_viewed"].mean() < normal["pages_viewed"].mean()
