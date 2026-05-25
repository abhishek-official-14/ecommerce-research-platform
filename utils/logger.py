"""Centralized logging setup."""

import sys
from loguru import logger
from utils.constants import LOG_DIR


def setup_logger() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger.remove()
    logger.add(sys.stdout, level="INFO", colorize=True, enqueue=True)
    logger.add(
        LOG_DIR / "platform.log",
        level="DEBUG",
        rotation="10 MB",
        retention="14 days",
        compression="zip",
        enqueue=True,
        backtrace=True,
        diagnose=False,
    )
