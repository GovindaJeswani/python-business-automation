"""
Utility functions shared across the toolkit.

Why a utils module?
- Keeps file-discovery logic out of business logic modules.
- Makes it easy to extend (e.g., add CSV discovery later) without touching merge/cleaner.
- Single place to validate paths, so errors surface early with clear messages.
"""

import os
from typing import List

from src.config import EXCEL_EXTENSIONS, IGNORE_TEMP_FILES
from src.logger import get_logger

logger = get_logger(__name__)


def discover_excel_files(directory: str) -> List[str]:
    """
    Find all .xlsx and .xls files in a directory (non-recursive).

    Args:
        directory: Path to scan for Excel files.

    Returns:
        Sorted list of absolute paths to Excel files found.

    Raises:
        FileNotFoundError: If the directory does not exist.
        ValueError: If no Excel files are found.
    """
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Input directory not found: {directory}")

    files = []
    for f in sorted(os.listdir(directory)):
        if not f.lower().endswith(EXCEL_EXTENSIONS):
            continue
        if IGNORE_TEMP_FILES and f.startswith("~$"):
            continue
        files.append(os.path.join(directory, f))

    if not files:
        raise ValueError(f"No Excel files found in: {directory}")

    logger.info(f"Discovered {len(files)} Excel file(s) in {directory}")
    logger.debug(f"Files: {[os.path.basename(f) for f in files]}")

    return files


def ensure_directory(path: str) -> str:
    """
    Create a directory if it doesn't exist.

    Args:
        path: Directory path to create.

    Returns:
        The same path (for chaining convenience).
    """
    os.makedirs(path, exist_ok=True)
    return path
