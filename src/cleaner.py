"""
Data cleaning module.

Why a separate cleaner?
- Cleaning rules change per client. Isolating them makes customization easy.
- Each cleaning step is a pure function: DataFrame in, DataFrame out.
- Easy to add new steps (trim whitespace, fix dates, etc.) without touching merge or report.

Design decision: each function returns a new DataFrame and a count of what changed.
This lets the report module show exactly what was cleaned.
"""

import pandas as pd
from typing import Tuple

from src.logger import get_logger

logger = get_logger(__name__)


def remove_duplicates(df: pd.DataFrame) -> Tuple[pd.DataFrame, int]:
    """
    Remove exact duplicate rows.

    Ignores the _source_file tracking column when checking for duplicates,
    so the same row from two different files counts as a duplicate.

    Args:
        df: Input DataFrame.

    Returns:
        Tuple of (cleaned DataFrame, number of duplicates removed).
    """
    # Exclude our internal tracking column from duplicate detection
    subset_cols = [col for col in df.columns if col != "_source_file"]

    before = len(df)
    df_clean = df.drop_duplicates(subset=subset_cols, keep="first").reset_index(drop=True)
    removed = before - len(df_clean)

    logger.info(f"Removed {removed} duplicate row(s)")
    return df_clean, removed


def remove_empty_rows(df: pd.DataFrame) -> Tuple[pd.DataFrame, int]:
    """
    Remove rows where all business columns are NaN/empty.

    A row is considered empty if every column (except _source_file) is null.

    Args:
        df: Input DataFrame.

    Returns:
        Tuple of (cleaned DataFrame, number of empty rows removed).
    """
    subset_cols = [col for col in df.columns if col != "_source_file"]

    before = len(df)
    df_clean = df.dropna(subset=subset_cols, how="all").reset_index(drop=True)
    removed = before - len(df_clean)

    logger.info(f"Removed {removed} empty row(s)")
    return df_clean, removed


def clean_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
    """
    Run the full cleaning pipeline.

    Args:
        df: Raw merged DataFrame.

    Returns:
        Tuple of (cleaned DataFrame, stats dict with counts of what was removed).
    """
    stats = {"rows_before": len(df)}

    df, duplicates_removed = remove_duplicates(df)
    stats["duplicates_removed"] = duplicates_removed

    df, empty_removed = remove_empty_rows(df)
    stats["empty_rows_removed"] = empty_removed

    stats["rows_after"] = len(df)

    logger.info(
        f"Cleaning complete: {stats['rows_before']} → {stats['rows_after']} rows "
        f"({stats['rows_before'] - stats['rows_after']} removed)"
    )

    return df, stats
