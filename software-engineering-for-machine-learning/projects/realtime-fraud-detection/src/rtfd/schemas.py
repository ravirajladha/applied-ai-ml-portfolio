"""The canonical transaction contract.

Every source dataset gets adapted into *this* shape before it touches the rest
of the system. That indirection costs one small class and buys the ability to
swap PaySim for IEEE-CIS (or a real feed) without changing the feature builder,
the model, or the API.

Two representations of the same thing live here, and they are checked against
each other by a test:

* :class:`Transaction` — a single event, validated with pydantic. Used at the
  message and request boundary, where one bad record must fail loudly.
* :data:`transaction_frame_schema` — a whole table, validated with pandera.
  Used in batch, where the same rules must hold over millions of rows.

The raw, source-specific schema (PaySim's own columns) is *not* defined here.
It gets written after the dataset has actually been profiled — writing a schema
for data you have not looked at is how you end up with a schema that documents
your assumptions rather than the data.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

import pandera.pandas as pa
from pandera.typing import Series
from pydantic import BaseModel, ConfigDict, Field, field_validator


class TransactionType(StrEnum):
    """How money moved.

    Kept deliberately generic rather than mirroring one dataset's vocabulary.
    Source-specific values are mapped onto these by the adapter.
    """

    PAYMENT = "payment"
    TRANSFER = "transfer"
    CASH_OUT = "cash_out"
    CASH_IN = "cash_in"
    DEBIT = "debit"
    OTHER = "other"


class Transaction(BaseModel):
    """One transaction, in the shape the system works with.

    Validation is strict on purpose. A malformed transaction must raise, not
    quietly become a row of zeros — a zero amount scores as safe, which is the
    worst possible failure mode for this system.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    transaction_id: str = Field(min_length=1)
    #: When it happened. Always timezone-aware UTC; naive datetimes are rejected
    #: because a fraud system that is ambiguous about time is not a fraud system.
    timestamp: datetime
    #: The party being debited — the entity whose behavioural history matters.
    account_id: str = Field(min_length=1)
    #: The party being credited: merchant, payee, destination account.
    counterparty_id: str = Field(min_length=1)
    amount: float = Field(gt=0)
    transaction_type: TransactionType

    #: Balance before and after, where the source provides them. Optional
    #: because not every feed has them, and ``None`` must stay distinguishable
    #: from ``0.0`` — a zero balance and an unknown balance mean very different
    #: things.
    account_balance_before: float | None = None
    account_balance_after: float | None = None

    #: The label. ``None`` at scoring time, and ``None`` for recent history where
    #: the dispute window has not closed yet. This tri-state is load-bearing:
    #: see the delayed-label discussion in docs/01-problem.md.
    is_fraud: bool | None = None

    @field_validator("timestamp")
    @classmethod
    def _require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("timestamp must be timezone-aware (UTC)")
        return value


class TransactionFrame(pa.DataFrameModel):
    """The same contract, applied to a whole table.

    Used wherever transactions are handled in bulk: the archiver writing
    Parquet, and the training job reading it back.
    """

    transaction_id: Series[str] = pa.Field(unique=True, nullable=False)
    timestamp: Series[pa.DateTime] = pa.Field(nullable=False)
    account_id: Series[str] = pa.Field(nullable=False)
    counterparty_id: Series[str] = pa.Field(nullable=False)
    amount: Series[float] = pa.Field(gt=0, nullable=False)
    transaction_type: Series[str] = pa.Field(
        isin=[t.value for t in TransactionType], nullable=False
    )
    account_balance_before: Series[float] = pa.Field(nullable=True)
    account_balance_after: Series[float] = pa.Field(nullable=True)
    is_fraud: Series[bool] = pa.Field(nullable=True)

    class Config:
        """Reject unexpected columns rather than passing them through.

        An upstream system silently adding a column is a signal worth stopping
        for, not something to ignore.
        """

        strict = True
        coerce = True
        ordered = False


transaction_frame_schema = TransactionFrame.to_schema()

#: The canonical column order. Fixed, because feature vector column order is a
#: real source of production bugs — a model fed the right numbers in the wrong
#: order returns confident nonsense.
TRANSACTION_COLUMNS: tuple[str, ...] = tuple(Transaction.model_fields.keys())
