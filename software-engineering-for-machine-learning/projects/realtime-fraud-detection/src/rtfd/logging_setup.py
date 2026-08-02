"""Structured logging.

Logs are JSON in production and human-readable in a terminal. The reason for
structured logs here is not tidiness: every scoring decision is logged with the
features that produced it, and those records need to be queryable months later
when someone asks why a particular transaction was blocked.
"""

from __future__ import annotations

import logging
import sys
from typing import cast

import structlog

from rtfd.config import settings


def _force_utf8_streams() -> None:
    """Make stdout and stderr UTF-8.

    A Windows console still defaults to a legacy code page, which turns any
    non-ASCII character in a report or log line into a replacement character.
    JSON logs would be corrupted the same way. Reconfiguring once at startup
    costs nothing and removes an entire class of "why is my output mojibake"
    confusion.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")


def configure_logging(json_output: bool | None = None) -> None:
    """Set up structlog once, at process start.

    Args:
        json_output: Force JSON output. When ``None``, output is
            human-readable if stderr is a terminal and JSON otherwise, which is
            the behaviour you want both locally and in a container.
    """
    _force_utf8_streams()

    if json_output is None:
        json_output = not sys.stderr.isatty()

    renderer: structlog.types.Processor = (
        structlog.processors.JSONRenderer() if json_output else structlog.dev.ConsoleRenderer()
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.getLevelName(settings.log_level.upper())
        ),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Return a bound logger for a module."""
    # structlog.get_logger is typed as returning Any because the concrete class
    # depends on runtime configuration. Narrowing it here means callers get real
    # type checking instead of Any leaking through the whole codebase.
    return cast(structlog.stdlib.BoundLogger, structlog.get_logger(name))
