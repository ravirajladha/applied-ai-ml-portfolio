"""Tests for the canonical transaction contract.

These are not ceremony. Each one pins down a failure mode that would otherwise
be silent and expensive:

* a naive timestamp makes every time-window feature ambiguous
* a zero or negative amount scores as safe
* an unknown label and a "not fraud" label mean different things, and conflating
  them teaches the model that recent traffic is clean
* feature column order decides what the model actually sees
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta, timezone

import pandas as pd
import pandera.errors
import pytest
from pydantic import ValidationError

from rtfd.schemas import (
    TRANSACTION_COLUMNS,
    Transaction,
    TransactionType,
    transaction_frame_schema,
)

#: pandera raises ``SchemaError`` for a single failed check but ``SchemaErrors``
#: (plural) when the container-level validation collects several — which is what
#: a ``strict=True`` unexpected-column violation produces. The two do not share a
#: useful base class, so assertions accept either.
SCHEMA_FAILURE = (pandera.errors.SchemaError, pandera.errors.SchemaErrors)


def _valid_kwargs(**overrides: object) -> dict:
    base = {
        "transaction_id": "t-1",
        "timestamp": datetime(2026, 8, 2, 12, 0, tzinfo=UTC),
        "account_id": "C1000001",
        "counterparty_id": "M2000001",
        "amount": 1500.0,
        "transaction_type": TransactionType.TRANSFER,
    }
    base.update(overrides)
    return base


class TestTransaction:
    def test_accepts_a_valid_transaction(self) -> None:
        tx = Transaction(**_valid_kwargs())
        assert tx.amount == 1500.0
        assert tx.is_fraud is None, "label must default to unknown, not to False"

    def test_rejects_naive_timestamp(self) -> None:
        # A fraud system that is ambiguous about time cannot compute a
        # "last 60 seconds" feature it can defend.
        with pytest.raises(ValidationError, match="timezone-aware"):
            Transaction(**_valid_kwargs(timestamp=datetime(2026, 8, 2, 12, 0)))

    def test_accepts_non_utc_timezone(self) -> None:
        ist = timezone(timedelta(hours=5, minutes=30))
        tx = Transaction(**_valid_kwargs(timestamp=datetime(2026, 8, 2, 17, 30, tzinfo=ist)))
        assert tx.timestamp.utcoffset() is not None

    @pytest.mark.parametrize("amount", [0.0, -1.0, -0.01])
    def test_rejects_non_positive_amount(self, amount: float) -> None:
        # The dangerous case: a malformed record defaulting to 0.0 would look
        # like the safest transaction the model has ever seen.
        with pytest.raises(ValidationError):
            Transaction(**_valid_kwargs(amount=amount))

    def test_rejects_unknown_fields(self) -> None:
        # An upstream system adding a field is a signal to stop, not to ignore.
        with pytest.raises(ValidationError):
            Transaction(**_valid_kwargs(device_fingerprint="abc"))

    def test_is_immutable(self) -> None:
        tx = Transaction(**_valid_kwargs())
        with pytest.raises(ValidationError):
            tx.amount = 99.0  # type: ignore[misc]

    def test_unknown_label_is_distinct_from_not_fraud(self) -> None:
        unknown = Transaction(**_valid_kwargs())
        settled = Transaction(**_valid_kwargs(is_fraud=False))
        assert unknown.is_fraud is None
        assert settled.is_fraud is False
        assert unknown.is_fraud is not settled.is_fraud

    def test_balances_distinguish_zero_from_unknown(self) -> None:
        unknown = Transaction(**_valid_kwargs())
        zero = Transaction(**_valid_kwargs(account_balance_before=0.0))
        assert unknown.account_balance_before is None
        assert zero.account_balance_before == 0.0


class TestTransactionFrame:
    @staticmethod
    def _valid_frame() -> pd.DataFrame:
        return pd.DataFrame(
            {
                "transaction_id": ["t-1", "t-2"],
                "timestamp": pd.to_datetime(["2026-08-02T12:00:00Z", "2026-08-02T12:00:05Z"]),
                "account_id": ["C1", "C1"],
                "counterparty_id": ["M1", "M2"],
                "amount": [100.0, 250.0],
                "transaction_type": ["transfer", "payment"],
                "account_balance_before": [1000.0, 900.0],
                "account_balance_after": [900.0, 650.0],
                "is_fraud": [False, True],
            }
        )

    def test_accepts_a_valid_frame(self) -> None:
        transaction_frame_schema.validate(self._valid_frame())

    def test_rejects_duplicate_transaction_ids(self) -> None:
        # Duplicates mean the archiver double-wrote, which would double-count
        # every rolling aggregate built from it.
        frame = self._valid_frame()
        frame.loc[1, "transaction_id"] = "t-1"
        with pytest.raises(SCHEMA_FAILURE):
            transaction_frame_schema.validate(frame)

    def test_rejects_unknown_transaction_type(self) -> None:
        frame = self._valid_frame()
        frame.loc[0, "transaction_type"] = "CRYPTO_YOLO"
        with pytest.raises(SCHEMA_FAILURE):
            transaction_frame_schema.validate(frame)

    def test_rejects_extra_columns(self) -> None:
        frame = self._valid_frame()
        frame["surprise"] = 1
        with pytest.raises(SCHEMA_FAILURE):
            transaction_frame_schema.validate(frame)

    def test_rejects_non_positive_amount(self) -> None:
        frame = self._valid_frame()
        frame.loc[0, "amount"] = 0.0
        with pytest.raises(SCHEMA_FAILURE):
            transaction_frame_schema.validate(frame)


def test_the_two_schemas_describe_the_same_columns() -> None:
    """The row-level and table-level contracts must not drift apart.

    They are maintained by hand in two places, so this test is the thing that
    stops one being updated without the other.
    """
    assert set(TRANSACTION_COLUMNS) == set(transaction_frame_schema.columns)


def test_column_order_is_fixed() -> None:
    """Feature vector order is load-bearing.

    A model handed the right numbers in the wrong order returns confident
    nonsense and never errors. Pinning the order here means a reordering shows
    up as a failing test rather than as a quiet accuracy drop in production.
    """
    assert TRANSACTION_COLUMNS == (
        "transaction_id",
        "timestamp",
        "account_id",
        "counterparty_id",
        "amount",
        "transaction_type",
        "account_balance_before",
        "account_balance_after",
        "is_fraud",
    )
