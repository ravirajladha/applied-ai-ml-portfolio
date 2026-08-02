"""Shared test fixtures.

The synthetic PaySim fixture here exists so the data pipeline can be tested
without a 470 MB download in CI. It mimics PaySim's *column layout*, not its
statistical properties — it is for exercising code paths, never for drawing
conclusions about the data.
"""

from __future__ import annotations

import csv
import random
from pathlib import Path

import pytest

PAYSIM_COLUMNS = [
    "step",
    "type",
    "amount",
    "nameOrig",
    "oldbalanceOrg",
    "newbalanceOrig",
    "nameDest",
    "oldbalanceDest",
    "newbalanceDest",
    "isFraud",
    "isFlaggedFraud",
]

TYPES = ["PAYMENT", "TRANSFER", "CASH_OUT", "CASH_IN", "DEBIT"]


@pytest.fixture
def fake_paysim_csv(tmp_path: Path) -> Path:
    """A small CSV with PaySim's exact column layout.

    Deliberately includes accounts that appear several times, so the account
    repetition query in the profiler has something non-trivial to count.
    """
    rng = random.Random(42)
    path = tmp_path / "paysim_sample.csv"

    # 40 accounts over 200 transactions guarantees repeats.
    accounts = [f"C{1000000 + i}" for i in range(40)]
    merchants = [f"M{2000000 + i}" for i in range(15)]

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=PAYSIM_COLUMNS)
        writer.writeheader()
        for i in range(200):
            tx_type = rng.choice(TYPES)
            # Fraud only on TRANSFER and CASH_OUT, matching PaySim's real
            # behaviour, so tests exercise the grouped query meaningfully.
            is_fraud = int(tx_type in ("TRANSFER", "CASH_OUT") and rng.random() < 0.05)
            amount = round(
                rng.uniform(500_000, 2_000_000) if is_fraud else rng.uniform(10, 50_000), 2
            )
            old_balance = round(rng.uniform(0, 100_000), 2)
            writer.writerow(
                {
                    "step": 1 + i // 20,
                    "type": tx_type,
                    "amount": amount,
                    "nameOrig": rng.choice(accounts),
                    "oldbalanceOrg": old_balance,
                    "newbalanceOrig": round(max(0.0, old_balance - amount), 2),
                    "nameDest": rng.choice(merchants),
                    "oldbalanceDest": 0.0,
                    "newbalanceDest": amount,
                    "isFraud": is_fraud,
                    "isFlaggedFraud": int(is_fraud and amount > 1_500_000),
                }
            )
    return path
