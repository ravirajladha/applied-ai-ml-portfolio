"""Fetch the source dataset.

The dataset is never committed to git (see ``.gitignore``). Anyone cloning this
repository runs this once, and it is the only manual setup step in the project.

Why the dataset is PaySim, and what is wrong with it, is recorded in ADR-0002.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from rtfd.config import settings
from rtfd.logging_setup import configure_logging, get_logger

log = get_logger(__name__)

KAGGLE_DATASET = "ealaxi/paysim1"
EXPECTED_CSV = "PS_20174392719_1491204439457_log.csv"
LOCAL_NAME = "paysim.csv"

MANUAL_INSTRUCTIONS = f"""
Automatic download needs Kaggle credentials, which are not configured.

Either set them up once (recommended — it makes this repeatable):

  1. Sign in at https://www.kaggle.com and open Settings
  2. Under 'API', click 'Create New Token'. A kaggle.json file downloads.
  3. Move it to:  {Path.home() / ".kaggle" / "kaggle.json"}
  4. Re-run:  uv run rtfd-download

Or download it by hand:

  1. Open https://www.kaggle.com/datasets/{KAGGLE_DATASET}
  2. Download and unzip it
  3. Put the CSV at:  {settings.raw_dir / LOCAL_NAME}
"""


def _target_path() -> Path:
    return settings.raw_dir / LOCAL_NAME


def _already_present() -> bool:
    target = _target_path()
    if not target.exists():
        return False
    size_mb = target.stat().st_size / 1_000_000
    # The real file is ~470 MB. A tiny file here usually means an interrupted
    # download or an HTML error page saved with a .csv extension.
    if size_mb < 100:
        log.warning(
            "existing file looks too small, re-downloading",
            path=str(target),
            size_mb=round(size_mb, 1),
        )
        return False
    log.info("dataset already present", path=str(target), size_mb=round(size_mb, 1))
    return True


def download(force: bool = False) -> Path:
    """Download PaySim into ``data/raw/``.

    Args:
        force: Download again even if the file is already there.

    Returns:
        Path to the CSV.

    Raises:
        SystemExit: If credentials are missing. The message explains what to do;
            a stack trace would not.
    """
    settings.ensure_dirs()
    target = _target_path()

    if not force and _already_present():
        return target

    try:
        import kagglehub
    except ImportError:
        log.error("kagglehub is not installed", fix="uv add kagglehub")
        raise SystemExit(1) from None

    log.info("downloading from kaggle", dataset=KAGGLE_DATASET)
    try:
        cache_dir = Path(kagglehub.dataset_download(KAGGLE_DATASET))
    except Exception as exc:
        # Catching broadly on purpose: kagglehub raises a different type for
        # missing credentials, an expired token, a network failure and a
        # renamed dataset, and the advice below is the same for all of them.
        log.error("kaggle download failed", error=str(exc))
        print(MANUAL_INSTRUCTIONS, file=sys.stderr)
        raise SystemExit(1) from exc

    candidates = list(cache_dir.glob("*.csv"))
    if not candidates:
        log.error("no csv found in the download", cache_dir=str(cache_dir))
        raise SystemExit(1)
    source = max(candidates, key=lambda p: p.stat().st_size)

    log.info("copying into the project", source=str(source), target=str(target))
    shutil.copy2(source, target)

    size_mb = target.stat().st_size / 1_000_000
    log.info("done", path=str(target), size_mb=round(size_mb, 1))
    return target


def main() -> None:
    """Entry point for ``uv run rtfd-download``."""
    parser = argparse.ArgumentParser(description="Download the source dataset.")
    parser.add_argument("--force", action="store_true", help="re-download even if already present")
    args = parser.parse_args()

    configure_logging()
    path = download(force=args.force)
    print(f"\nDataset ready: {path}")
    print("Next:  uv run rtfd-profile")


if __name__ == "__main__":
    main()
