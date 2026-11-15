"""One logging config for the whole package.

Every module calls get_logger(__name__) instead of print().
"""

import logging
import sys

from ecom.config import LOG_DIR

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_configured = False


def _configure() -> None:
    """Attach console + file handlers once."""
    global _configured
    if _configured:
        return

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger("ecom")
    root.setLevel(logging.INFO)

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(logging.Formatter(LOG_FORMAT))

    file_handler = logging.FileHandler(LOG_DIR / "app.log", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    root.addHandler(console)
    root.addHandler(file_handler)
    root.propagate = False
    _configured = True


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger."""
    _configure()
    return logging.getLogger(name)
