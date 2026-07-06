"""
Centralized logging configuration for the Business Automation Toolkit.

Why a separate logger module?
- Every module gets consistent formatting without repeating setup code.
- Logs go to both console (for immediate feedback) and a rotating file (for audit trails).
- Clients can review logs/automation.log to verify what was processed.
"""

import logging
import os
from datetime import datetime

from src.config import LOG_DIR, LOG_LEVEL_CONSOLE, LOG_LEVEL_FILE, LOG_FORMAT, LOG_DATE_FORMAT

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, f"automation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")


def get_logger(name: str) -> logging.Logger:
    """
    Create and return a configured logger instance.

    Args:
        name: Module name (typically __name__) for log attribution.

    Returns:
        A Logger with console and file handlers attached.
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if get_logger is called multiple times
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL_CONSOLE))
    console_handler.setFormatter(formatter)

    # File handler
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(getattr(logging, LOG_LEVEL_FILE))
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
