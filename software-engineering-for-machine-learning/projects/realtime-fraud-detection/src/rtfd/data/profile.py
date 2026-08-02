"""Profile the raw dataset before building anything on top of it.

This runs before the schema is written, before the replay producer, before any
feature work. The order matters. Writing a schema first documents what you
assumed; profiling first documents what is actually there.

One question here outranks all the others:

    **How many accounts appear more than once?**

Almost every planned feature is a per-account rolling aggregate — spend in the
last hour, transactions in the last minute, amount relative to this account's
usual. If most accounts appear exactly once in the data, none of those features
carry any signal and the entire feature plan has to be rebuilt around the
counterparty instead. Finding that out now costs an afternoon. Finding it out at
M3 costs a fortnight.

DuckDB reads the CSV directly, so nothing is loaded into memory and this runs in
seconds on a 6-million-row file.
"""

from __future__ import annotations

import argparse
import textwrap
from pathlib import Path

import duckdb

from rtfd.config import settings
from rtfd.logging_setup import configure_logging, get_logger

log = get_logger(__name__)


def _q(con: duckdb.DuckDBPyConnection, sql: str) -> list[tuple]:
    return con.execute(textwrap.dedent(sql)).fetchall()


def _md_table(headers: list[str], rows: list[tuple]) -> str:
    """Render query results as a markdown table."""
    out = ["| " + " | ".join(headers) + " |"]
    out.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        cells = [
            f"{v:,.4g}" if isinstance(v, float) else f"{v:,}" if isinstance(v, int) else str(v)
            for v in row
        ]
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def profile(csv_path: Path, out_path: Path) -> str:
    """Profile the raw CSV and write a markdown report.

    Args:
        csv_path: The raw dataset.
        out_path: Where to write the report.

    Returns:
        The report text, so callers can print or assert on it.
    """
    con = duckdb.connect()
    # Via the relational API rather than a parameterised CREATE VIEW: DuckDB
    # cannot prepare DDL statements, and interpolating a path into SQL is the
    # kind of shortcut that stops being harmless the moment the path comes from
    # somewhere else.
    con.read_csv(str(csv_path), header=True).create_view("tx")

    sections: list[str] = [
        f"# Dataset profile\n\nSource: `{csv_path.name}`\n",
    ]

    # -- Shape ---------------------------------------------------------------
    columns = _q(con, "SELECT column_name, column_type FROM (DESCRIBE tx)")
    (n_rows,) = _q(con, "SELECT count(*) FROM tx")[0]
    sections.append(f"## Shape\n\n{n_rows:,} rows, {len(columns)} columns.\n")
    sections.append(_md_table(["column", "type"], columns) + "\n")

    # -- Missing values ------------------------------------------------------
    null_sql = ", ".join(
        f'sum(CASE WHEN "{c}" IS NULL THEN 1 ELSE 0 END) AS "{c}"' for c, _ in columns
    )
    null_counts = _q(con, f"SELECT {null_sql} FROM tx")[0]
    null_rows = [(c, n, n / n_rows) for (c, _), n in zip(columns, null_counts, strict=True)]
    sections.append(
        "## Missing values\n\n" + _md_table(["column", "nulls", "fraction"], null_rows) + "\n"
    )

    # -- The label -----------------------------------------------------------
    fraud = _q(
        con,
        """
        SELECT type,
               count(*)                        AS transactions,
               sum(isFraud)                    AS frauds,
               sum(isFraud) / count(*)         AS fraud_rate,
               sum(CASE WHEN isFraud = 1 THEN amount ELSE 0 END) AS fraud_amount
        FROM tx GROUP BY type ORDER BY frauds DESC
        """,
    )
    sections.append(
        "## Fraud by transaction type\n\n"
        + _md_table(["type", "transactions", "frauds", "fraud rate", "fraud amount"], fraud)
        + "\n\nIf fraud is confined to one or two transaction types, everything "
        "else can be excluded from scoring entirely — which changes the volume "
        "the service has to handle.\n"
    )

    # -- THE question --------------------------------------------------------
    repeats = _q(
        con,
        """
        WITH per_account AS (
            SELECT nameOrig AS account, count(*) AS n FROM tx GROUP BY nameOrig
        )
        SELECT
            count(*)                                             AS accounts,
            sum(CASE WHEN n = 1 THEN 1 ELSE 0 END)               AS seen_once,
            sum(CASE WHEN n > 1 THEN 1 ELSE 0 END)               AS seen_more_than_once,
            sum(CASE WHEN n > 1 THEN 1 ELSE 0 END) / count(*)    AS repeat_account_share,
            sum(CASE WHEN n > 1 THEN n ELSE 0 END) / sum(n)      AS repeat_transaction_share,
            max(n)                                               AS max_per_account,
            avg(n)                                               AS mean_per_account
        FROM per_account
        """,
    )
    sections.append(
        "## Account repetition — the load-bearing number\n\n"
        + _md_table(
            [
                "accounts",
                "seen once",
                "seen >1",
                "share of accounts repeating",
                "share of transactions from repeat accounts",
                "max",
                "mean",
            ],
            repeats,
        )
        + "\n\n**How to read this.** `share of transactions from repeat accounts` "
        "is the number that matters. Per-account history features can only carry "
        "signal for that fraction of traffic. Below roughly 0.2, the per-account "
        "feature plan is not viable and features must be rebuilt around the "
        "counterparty (`nameDest`) instead.\n"
    )

    # Same question for the receiving side, which is the fallback if the above
    # comes back badly.
    repeats_dest = _q(
        con,
        """
        WITH per_dest AS (
            SELECT nameDest AS account, count(*) AS n FROM tx GROUP BY nameDest
        )
        SELECT count(*) AS counterparties,
               sum(CASE WHEN n > 1 THEN n ELSE 0 END) / sum(n) AS repeat_transaction_share,
               max(n) AS max_per_counterparty
        FROM per_dest
        """,
    )
    sections.append(
        "### The counterparty side (the fallback)\n\n"
        + _md_table(["counterparties", "share of transactions from repeats", "max"], repeats_dest)
        + "\n"
    )

    # -- Time ----------------------------------------------------------------
    time_span = _q(
        con,
        """
        SELECT min(step) AS first_step, max(step) AS last_step,
               count(DISTINCT step) AS distinct_steps,
               count(*) / count(DISTINCT step) AS mean_tx_per_step
        FROM tx
        """,
    )
    sections.append(
        "## Time\n\n"
        + _md_table(["first", "last", "distinct steps", "mean transactions per step"], time_span)
        + "\n\n`step` is an hour index, not a timestamp — see ADR-0002. "
        "`mean transactions per step` sets the replay rate: divided by 3600 it "
        "gives the transactions per second the service must sustain at 1x speed.\n"
    )

    # -- Amounts -------------------------------------------------------------
    amounts = _q(
        con,
        """
        SELECT isFraud,
               count(*)                              AS n,
               min(amount)                           AS min,
               quantile_cont(amount, 0.5)            AS median,
               quantile_cont(amount, 0.99)           AS p99,
               max(amount)                           AS max,
               avg(amount)                           AS mean
        FROM tx GROUP BY isFraud ORDER BY isFraud
        """,
    )
    sections.append(
        "## Amounts, fraud versus legitimate\n\n"
        + _md_table(["is_fraud", "n", "min", "median", "p99", "max", "mean"], amounts)
        + "\n\nThe gap between the two medians is the crudest possible signal. "
        "If it is large, a threshold on amount alone is a real baseline the model "
        "has to beat — and it should be reported as one.\n"
    )

    # -- The dataset's own flag ---------------------------------------------
    flagged = _q(
        con,
        """
        SELECT isFlaggedFraud, count(*) AS n, sum(isFraud) AS actually_fraud
        FROM tx GROUP BY isFlaggedFraud
        """,
    )
    sections.append(
        "## The dataset's built-in flag\n\n"
        + _md_table(["isFlaggedFraud", "n", "actually fraud"], flagged)
        + "\n\n`isFlaggedFraud` is the simulated incumbent rule-based system. It "
        "**must be excluded from the features** — it is another detector's output, "
        "not an input, and including it is leakage. It is useful as the baseline "
        "to beat.\n"
    )

    report = "\n".join(sections)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")
    log.info("profile written", path=str(out_path), rows=n_rows)
    return report


def main() -> None:
    """Entry point for ``uv run rtfd-profile``."""
    parser = argparse.ArgumentParser(description="Profile the raw dataset.")
    parser.add_argument("--csv", type=Path, default=settings.raw_dir / "paysim.csv")
    parser.add_argument("--out", type=Path, default=settings.reports_dir / "dataset-profile.md")
    args = parser.parse_args()

    configure_logging()
    if not args.csv.exists():
        log.error("dataset not found", path=str(args.csv), fix="uv run rtfd-download")
        raise SystemExit(1)

    report = profile(args.csv, args.out)
    print(report)
    print(f"\nWritten to {args.out}")


if __name__ == "__main__":
    main()
