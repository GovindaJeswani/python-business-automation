"""
Excel file merging module.

Why split merging into its own module?
- Merging is a distinct operation from cleaning or reporting.
- A client might want to merge without cleaning (or vice versa).
- Easier to test in isolation.
- Clear responsibility: this module reads N files and produces one DataFrame.
"""

import pandas as pd
from typing import List

from src.logger import get_logger

logger = get_logger(__name__)


def merge_excel_files(file_paths: List[str]) -> pd.DataFrame:
    """
    Read and concatenate multiple Excel files into a single DataFrame.

    Handles files with different column orders by aligning on column names.
    Skips files that fail to read (logs a warning) rather than aborting the
    entire batch - because in production, one corrupt file shouldn't block
    processing of the other 99.

    Args:
        file_paths: List of paths to Excel files.

    Returns:
        A single DataFrame containing all rows from all successfully read files.

    Raises:
        ValueError: If no files could be read successfully.
    """
    dataframes = []
    failed_files = []

    for path in file_paths:
        try:
            df = pd.read_excel(path, engine="openpyxl")
            df["_source_file"] = path.split("/")[-1].split("\\")[-1]
            dataframes.append(df)
            logger.debug(f"Read {len(df)} rows from {path}")
        except Exception as e:
            logger.warning(f"Failed to read {path}: {e}")
            failed_files.append(path)

    if not dataframes:
        raise ValueError("No files could be read successfully.")

    merged = pd.concat(dataframes, ignore_index=True)

    logger.info(
        f"Merged {len(dataframes)} file(s) → {len(merged)} total rows, "
        f"{len(merged.columns)} columns"
    )

    if failed_files:
        logger.warning(f"Skipped {len(failed_files)} unreadable file(s): {failed_files}")

    return merged
