"""Tests for the dataset profiler.

The profiler's output is what the whole feature plan gets decided from, so the
queries behind it need to be right. These run against a small synthetic CSV with
PaySim's column layout — see ``conftest.py``.
"""

from __future__ import annotations

from pathlib import Path

import duckdb
import pytest

from rtfd.data.profile import profile


@pytest.fixture
def report(fake_paysim_csv: Path, tmp_path: Path) -> str:
    return profile(fake_paysim_csv, tmp_path / "profile.md")


def test_report_is_written_to_disk(fake_paysim_csv: Path, tmp_path: Path) -> None:
    out = tmp_path / "nested" / "profile.md"
    profile(fake_paysim_csv, out)
    assert out.exists()
    assert out.read_text(encoding="utf-8").startswith("# Dataset profile")


def test_report_covers_every_section(report: str) -> None:
    for heading in (
        "## Shape",
        "## Missing values",
        "## Fraud by transaction type",
        "## Account repetition",
        "## Time",
        "## Amounts",
        "## The dataset's built-in flag",
    ):
        assert heading in report, f"missing section: {heading}"


def test_row_count_is_correct(report: str) -> None:
    assert "200 rows, 11 columns" in report


def test_account_repetition_query_is_arithmetically_right(fake_paysim_csv: Path) -> None:
    """Verify the load-bearing number independently of the report text.

    This is the query the entire feature plan hangs on, so it is checked
    against a separately written calculation rather than trusted.
    """
    con = duckdb.connect()
    con.read_csv(str(fake_paysim_csv), header=True).create_view("tx")

    counts = con.execute("SELECT count(*) AS n FROM tx GROUP BY nameOrig").fetchall()
    per_account = [row[0] for row in counts]

    total_transactions = sum(per_account)
    from_repeat_accounts = sum(n for n in per_account if n > 1)
    expected_share = from_repeat_accounts / total_transactions

    actual = con.execute(
        """
        WITH per_account AS (
            SELECT nameOrig AS account, count(*) AS n FROM tx GROUP BY nameOrig
        )
        SELECT sum(CASE WHEN n > 1 THEN n ELSE 0 END) / sum(n) FROM per_account
        """
    ).fetchone()
    assert actual is not None
    assert actual[0] == pytest.approx(expected_share)
    assert total_transactions == 200


def test_fixture_actually_contains_repeat_accounts(fake_paysim_csv: Path) -> None:
    """Guard the fixture itself.

    If the fixture stopped producing repeat accounts, the test above would
    still pass while checking nothing meaningful.
    """
    con = duckdb.connect()
    con.read_csv(str(fake_paysim_csv), header=True).create_view("tx")
    result = con.execute(
        "SELECT count(*) FROM (SELECT nameOrig FROM tx GROUP BY nameOrig HAVING count(*) > 1)"
    ).fetchone()
    assert result is not None
    assert result[0] > 0
