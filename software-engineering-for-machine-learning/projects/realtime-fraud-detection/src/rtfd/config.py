"""Central configuration.

Everything that could differ between a laptop and a server lives here, is read
from the environment, and has a sensible local default. Nothing anywhere else in
the codebase reads ``os.environ`` directly.

The cost constants are deliberately in this file rather than buried in the
training code, because they are the most important numbers in the system: they
determine the decision threshold. See ``docs/01-problem.md``.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Runtime configuration, overridable by environment variables.

    Every field can be set with an ``RTFD_`` prefixed environment variable, or
    in a ``.env`` file at the repository root. See ``.env.example``.
    """

    model_config = SettingsConfigDict(
        env_prefix="RTFD_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # -- Paths ---------------------------------------------------------------
    #: Where bulk data lives. The dataset and the offline store are large enough
    #: that they often cannot sit on the same volume as the code, so this is
    #: overridable on its own, and the sub-directories follow it unless they are
    #: set explicitly too.
    data_dir: Path = REPO_ROOT / "data"
    reports_dir: Path = REPO_ROOT / "reports"

    # The sub-directories are stored as optional overrides and exposed through
    # properties below. The alternative — plain fields with their own defaults —
    # was tried and is a trap: setting RTFD_DATA_DIR alone then moves nothing,
    # silently, and the data still lands beside the code. On a machine short of
    # disk that is discovered the hard way.
    raw_dir_override: Path | None = Field(default=None, validation_alias="RTFD_RAW_DIR")
    offline_dir_override: Path | None = Field(default=None, validation_alias="RTFD_OFFLINE_DIR")

    @property
    def raw_dir(self) -> Path:
        """Where the source dataset lives. Follows ``data_dir`` unless overridden."""
        return self.raw_dir_override or self.data_dir / "raw"

    @property
    def offline_dir(self) -> Path:
        """The offline store. Follows ``data_dir`` unless overridden."""
        return self.offline_dir_override or self.data_dir / "offline"

    # -- Streaming -----------------------------------------------------------
    kafka_bootstrap: str = "localhost:19092"
    topic_transactions: str = "transactions"
    topic_decisions: str = "decisions"

    # -- Online feature store ------------------------------------------------
    redis_url: str = "redis://localhost:6379/0"
    #: How long an account's rolling history is kept in Redis before expiring.
    #: Must be at least as long as the widest feature window, with headroom.
    feature_ttl_seconds: int = 60 * 60 * 48

    # -- Replay --------------------------------------------------------------
    #: 1.0 replays at true wall-clock speed; 60.0 compresses an hour into a
    #: minute. Used for development, never for latency measurement.
    replay_speed: float = 1.0
    #: Seed for the deterministic sub-hour timestamp spreading described in
    #: ADR-0002. Fixed so that replays are reproducible.
    replay_seed: int = 20260802

    # -- The cost model (see docs/01-problem.md) -----------------------------
    #: What it costs when fraud is approved: the transaction amount is lost, plus
    #: a fixed handling and investigation cost.
    cost_missed_fraud_fixed: float = 500.0
    cost_missed_fraud_amount_multiplier: float = 1.0
    #: What it costs when a legitimate transaction is blocked: lost margin, a
    #: support contact, and some probability of losing the customer.
    cost_false_alarm: float = 300.0

    # -- Model ---------------------------------------------------------------
    mlflow_tracking_uri: str = "http://localhost:5000"
    model_name: str = "fraud-detector"
    model_stage: str = "Production"

    # -- Service -------------------------------------------------------------
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    log_level: str = Field(default="INFO")

    def ensure_dirs(self) -> None:
        """Create the working directories if they do not exist."""
        for directory in (self.data_dir, self.raw_dir, self.offline_dir, self.reports_dir):
            directory.mkdir(parents=True, exist_ok=True)


settings = Settings()
