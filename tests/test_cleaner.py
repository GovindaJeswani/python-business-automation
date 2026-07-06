"""Tests for the cleaner module."""

import pandas as pd
import pytest

from src.cleaner import remove_duplicates, remove_empty_rows, clean_data


@pytest.fixture
def df_with_duplicates():
    """DataFrame with intentional duplicate rows."""
    return pd.DataFrame({
        "Name": ["Alice", "Bob", "Alice", "Carol"],
        "Amount": [100, 200, 100, 300],
        "_source_file": ["f1.xlsx", "f1.xlsx", "f2.xlsx", "f2.xlsx"],
    })


@pytest.fixture
def df_with_empty_rows():
    """DataFrame with completely empty rows."""
    return pd.DataFrame({
        "Name": ["Alice", None, "Bob", None],
        "Amount": [100, None, 200, None],
        "_source_file": ["f1.xlsx", "f1.xlsx", "f1.xlsx", "f1.xlsx"],
    })


def test_remove_duplicates_count(df_with_duplicates):
    """Should remove 1 duplicate (Alice/100 appears twice)."""
    result, removed = remove_duplicates(df_with_duplicates)
    assert removed == 1
    assert len(result) == 3


def test_remove_duplicates_ignores_source_file(df_with_duplicates):
    """Same data from different files should still be considered duplicate."""
    result, removed = remove_duplicates(df_with_duplicates)
    # Alice/100 from f1 and f2 are duplicates (ignoring _source_file)
    assert removed == 1


def test_remove_duplicates_no_duplicates():
    """No duplicates means no rows removed."""
    df = pd.DataFrame({
        "Name": ["Alice", "Bob", "Carol"],
        "Amount": [100, 200, 300],
        "_source_file": ["f1.xlsx", "f1.xlsx", "f1.xlsx"],
    })
    result, removed = remove_duplicates(df)
    assert removed == 0
    assert len(result) == 3


def test_remove_empty_rows_count(df_with_empty_rows):
    """Should remove 2 completely empty rows."""
    result, removed = remove_empty_rows(df_with_empty_rows)
    assert removed == 2
    assert len(result) == 2


def test_remove_empty_rows_keeps_partial():
    """Rows with at least one non-null business column should stay."""
    df = pd.DataFrame({
        "Name": ["Alice", None, None],
        "Amount": [None, 200, None],
        "_source_file": ["f1.xlsx", "f1.xlsx", "f1.xlsx"],
    })
    result, removed = remove_empty_rows(df)
    # Only the last row (both Name and Amount are None) should be removed
    assert removed == 1
    assert len(result) == 2


def test_clean_data_returns_stats(df_with_duplicates):
    """clean_data should return a stats dict with expected keys."""
    _, stats = clean_data(df_with_duplicates)
    assert "rows_before" in stats
    assert "rows_after" in stats
    assert "duplicates_removed" in stats
    assert "empty_rows_removed" in stats


def test_clean_data_pipeline():
    """Full pipeline: duplicates + empty rows removed in one pass."""
    df = pd.DataFrame({
        "Name": ["Alice", "Alice", None, "Bob"],
        "Amount": [100, 100, None, 200],
        "_source_file": ["f1.xlsx", "f2.xlsx", "f1.xlsx", "f1.xlsx"],
    })
    result, stats = clean_data(df)
    assert stats["duplicates_removed"] == 1
    assert stats["empty_rows_removed"] == 1
    assert stats["rows_after"] == 2
