"""Structured Logging Utility for AI Remote Desktop."""

import logging
import sys


def setup_logger(name: str = "antigravity_desk", level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "\033[90m%(asctime)s\033[0m [\033[96m%(levelname)s\033[0m] \033[94m%(name)s\033[0m: %(message)s",
            datefmt="%H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


logger = setup_logger()
