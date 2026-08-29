"""Shared logging for the harness and session loops.

Operator-facing answers stay on stdout (streamed model text, --tool JSON).
Noise (thinking, stop reason, tool dumps, audit) is logger.debug.
Set HARNESS_LOG_LEVEL=DEBUG or pass --debug on a harness launcher.
"""

from __future__ import annotations

import logging
import os
import sys

_CONFIGURED = False
ROOT_NAME = "harness"


def configure_logging(level: int | None = None) -> None:
    global _CONFIGURED
    if level is None:
        level_name = os.environ.get("HARNESS_LOG_LEVEL", "WARNING").upper()
        level = getattr(logging, level_name, logging.INFO)
    else:
        os.environ["HARNESS_LOG_LEVEL"] = logging.getLevelName(level)

    logger = logging.getLogger(ROOT_NAME)
    logger.setLevel(level)
    logger.handlers.clear()
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
    logger.addHandler(handler)
    logger.propagate = False
    _CONFIGURED = True


def get_logger(name: str = ROOT_NAME) -> logging.Logger:
    if not _CONFIGURED:
        configure_logging()
    if name == ROOT_NAME:
        return logging.getLogger(ROOT_NAME)
    return logging.getLogger(f"{ROOT_NAME}.{name}")


def enable_debug() -> None:
    configure_logging(logging.DEBUG)
