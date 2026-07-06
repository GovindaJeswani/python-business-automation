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


LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
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

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler - INFO and above for clean terminal output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # File handler - DEBUG and above for full audit trail
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
