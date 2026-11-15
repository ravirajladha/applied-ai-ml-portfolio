"""Data quality gate.

Three checks, each producing a measurable metric:
  1. schema conformance  - are the agreed columns present with usable types?
  2. missing value rate   - how much of each column is null?
  3. drift (PSI)          - has live traffic moved away from training data?
"""

from dataclasses import dataclass, field
from typing import Any

import numpy as np
import pandas as pd

from ecom.config import DRIFT_THRESHOLD, MAX_MISSING_RATE, RAW_SCHEMA
from ecom.exceptions import DataValidationError
from ecom.logging_setup import get_logger

logger = get_logger(__name__)


@dataclass
class ValidationReport:
    """Result of running the data quality gate."""

    passed: bool = True
    schema_conformance: float = 1.0
    missing_rates: dict[str, float] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "schema_conformance": round(self.schema_conformance, 4),
            "missing_rates": {k: round(v, 4) for k, v in self.missing_rates.items()},
            "errors": self.errors,
            "warnings": self.warnings,
        }


class DataValidator:
    """Validates a raw session dataframe against the data contract."""

    def __init__(self, schema: dict[str, str] | None = None) -> None:
        self.schema = schema or RAW_SCHEMA

    def validate(self, df: pd.DataFrame, strict: bool = True) -> ValidationReport:
        """Run all checks. strict=True raises on failure, else just reports."""
        report = ValidationReport()
        self._check_schema(df, report)
        self._check_missing(df, report)
        self._check_ranges(df, report)

        if report.errors:
            report.passed = False
            logger.error("Data validation FAILED: %s", "; ".join(report.errors))
            if strict:
                raise DataValidationError("; ".join(report.errors))
        else:
            logger.info(
                "Data validation passed (schema conformance=%.2f)",
                report.schema_conformance,
            )
        for warning in report.warnings:
            logger.warning("Data quality warning: %s", warning)
        return report

    # --- individual checks ---------------------------------------------
    def _check_schema(self, df: pd.DataFrame, report: ValidationReport) -> None:
        """Metric 1: fraction of contract columns present with the right type."""
        ok = 0
        for column, kind in self.schema.items():
            if column not in df.columns:
                report.errors.append(f"missing column '{column}'")
                continue
            is_numeric = pd.api.types.is_numeric_dtype(df[column])
            if kind == "numeric" and not is_numeric:
                report.errors.append(f"column '{column}' should be numeric")
                continue
            ok += 1
        report.schema_conformance = ok / len(self.schema)

    def _check_missing(self, df: pd.DataFrame, report: ValidationReport) -> None:
        """Metric 2: null rate per column, capped by MAX_MISSING_RATE."""
        for column in self.schema:
            if column not in df.columns:
                continue
            rate = float(df[column].isna().mean())
            report.missing_rates[column] = rate
            if rate > MAX_MISSING_RATE:
                report.errors.append(f"'{column}' has {rate:.1%} missing values")
            elif rate > 0:
                report.warnings.append(f"'{column}' has {rate:.1%} missing values")

    def _check_ranges(self, df: pd.DataFrame, report: ValidationReport) -> None:
        """Business rules: counts and prices cannot be negative."""
        for column in ("pages_viewed", "cart_items", "avg_item_price"):
            if column not in df.columns:
                continue
            # Skip non-numeric columns - the schema check already flagged them.
            if not pd.api.types.is_numeric_dtype(df[column]):
                continue
            if (df[column].dropna() < 0).any():
                report.errors.append(f"'{column}' contains negative values")


def population_stability_index(
    baseline: pd.Series, current: pd.Series, bins: int = 10
) -> float:
    """Metric 3: PSI drift score. 0 = identical, >0.2 = significant drift."""
    baseline = pd.to_numeric(baseline, errors="coerce").dropna()
    current = pd.to_numeric(current, errors="coerce").dropna()
    if baseline.empty or current.empty:
        return 0.0

    # Bin edges come from the baseline so both sides are comparable.
    edges = np.unique(np.quantile(baseline, np.linspace(0, 1, bins + 1)))
    if len(edges) < 3:
        return 0.0
    edges[0], edges[-1] = -np.inf, np.inf

    base_pct = np.histogram(baseline, bins=edges)[0] / len(baseline)
    curr_pct = np.histogram(current, bins=edges)[0] / len(current)

    # Floor at a small value to keep the log finite on empty bins.
    base_pct = np.clip(base_pct, 1e-6, None)
    curr_pct = np.clip(curr_pct, 1e-6, None)
    return float(np.sum((curr_pct - base_pct) * np.log(curr_pct / base_pct)))


def detect_drift(
    baseline: pd.DataFrame, current: pd.DataFrame, columns: list[str]
) -> dict[str, float]:
    """PSI per column; logs a warning for anything above the threshold."""
    scores: dict[str, float] = {}
    for column in columns:
        if column not in baseline.columns or column not in current.columns:
            logger.warning("Drift check skipped, column missing: %s", column)
            continue
        psi = population_stability_index(baseline[column], current[column])
        scores[column] = round(psi, 4)
        if psi > DRIFT_THRESHOLD:
            logger.warning("Drift detected in '%s' (PSI=%.3f)", column, psi)
        else:
            logger.info("No drift in '%s' (PSI=%.3f)", column, psi)
    return scores
