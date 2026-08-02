"""Tests for configuration.

The path derivation test exists because of a real bug: `raw_dir` and
`offline_dir` originally had their own independent defaults, so pointing
`RTFD_DATA_DIR` at a different volume silently moved nothing and the data kept
landing next to the code. On a machine that was nearly out of disk, that is not
a cosmetic problem.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from rtfd.config import Settings


@pytest.fixture(autouse=True)
def _isolate_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Stop a developer's real ``.env`` or shell from leaking into these tests."""
    for name in ("RTFD_DATA_DIR", "RTFD_RAW_DIR", "RTFD_OFFLINE_DIR", "RTFD_REPORTS_DIR"):
        monkeypatch.delenv(name, raising=False)


def _settings(monkeypatch: pytest.MonkeyPatch, **env: str) -> Settings:
    """Build Settings from environment variables.

    Deliberately goes through the environment rather than constructor keywords:
    the environment is how these are actually set, and an earlier version of
    this helper passed kwargs and therefore tested nothing real.
    """
    for name, value in env.items():
        monkeypatch.setenv(name, value)
    # _env_file=None so the repository's own .env cannot affect the result.
    return Settings(_env_file=None)


class TestDataPaths:
    def test_subdirs_default_under_data_dir(self, monkeypatch: pytest.MonkeyPatch) -> None:
        s = _settings(monkeypatch)
        assert s.raw_dir == s.data_dir / "raw"
        assert s.offline_dir == s.data_dir / "offline"

    def test_moving_data_dir_moves_the_subdirs(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # The actual bug. Setting only data_dir must relocate everything under
        # it, or bulk data quietly lands on the wrong volume.
        s = _settings(monkeypatch, RTFD_DATA_DIR=str(tmp_path / "elsewhere"))
        assert s.raw_dir == tmp_path / "elsewhere" / "raw"
        assert s.offline_dir == tmp_path / "elsewhere" / "offline"

    def test_explicit_subdir_still_wins(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # Deriving from data_dir must not take away the ability to place one
        # directory somewhere else on purpose.
        s = _settings(
            monkeypatch,
            RTFD_DATA_DIR=str(tmp_path / "bulk"),
            RTFD_OFFLINE_DIR=str(tmp_path / "fast-disk" / "offline"),
        )
        assert s.raw_dir == tmp_path / "bulk" / "raw"
        assert s.offline_dir == tmp_path / "fast-disk" / "offline"

    def test_ensure_dirs_creates_everything(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        s = _settings(
            monkeypatch,
            RTFD_DATA_DIR=str(tmp_path / "bulk"),
            RTFD_REPORTS_DIR=str(tmp_path / "reports"),
        )
        s.ensure_dirs()
        assert s.raw_dir.is_dir()
        assert s.offline_dir.is_dir()
        assert s.reports_dir.is_dir()


class TestCostModel:
    def test_missed_fraud_is_far_more_expensive_than_a_false_alarm(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Guards the assumption the decision threshold is derived from.

        If these two ever end up comparable, the cost-based threshold collapses
        towards the naive 0.5 cutoff and ADR-0004 stops meaning anything. This
        test does not assert a specific ratio — it asserts the asymmetry that
        the whole design depends on.
        """
        s = _settings(monkeypatch)
        typical_fraud_amount = 8000.0
        missed = (
            s.cost_missed_fraud_fixed + typical_fraud_amount * s.cost_missed_fraud_amount_multiplier
        )
        assert missed > 5 * s.cost_false_alarm
