"""Tests for the merge module."""

import os
import tempfile

import pandas as pd
import pytest

from src.merge import merge_excel_files


@pytest.fixture
def sample_files(tmp_path):
    """Create temporary Excel files for testing."""
    data1 = pd.DataFrame({
        "Name": ["Alice", "Bob"],
        "Amount": [100, 200],
    })
    data2 = pd.DataFrame({
        "Name": ["Carol", "Dan"],
        "Amount": [300, 400],
    })

    path1 = tmp_path / "file1.xlsx"
    path2 = tmp_path / "file2.xlsx"
    data1.to_excel(path1, index=False)
    data2.to_excel(path2, index=False)

    return [str(path1), str(path2)]


def test_merge_combines_rows(sample_files):
    """Merging two files with 2 rows each should produce 4 rows."""
    result = merge_excel_files(sample_files)
    assert len(result) == 4


def test_merge_preserves_columns(sample_files):
    """Merged result should contain original columns plus _source_file."""
    result = merge_excel_files(sample_files)
    assert "Name" in result.columns
    assert "Amount" in result.columns
    assert "_source_file" in result.columns


def test_merge_tracks_source_file(sample_files):
    """Each row should know which file it came from."""
    result = merge_excel_files(sample_files)
    sources = result["_source_file"].unique().tolist()
    assert "file1.xlsx" in sources
    assert "file2.xlsx" in sources


def test_merge_skips_corrupt_file(sample_files, tmp_path):
    """A corrupt file should be skipped without crashing."""
    corrupt_path = tmp_path / "corrupt.xlsx"
    corrupt_path.write_text("this is not an excel file")

    all_files = sample_files + [str(corrupt_path)]
    result = merge_excel_files(all_files)

    # Should still have the 4 rows from the 2 valid files
    assert len(result) == 4


def test_merge_raises_on_all_failures(tmp_path):
    """If all files fail to read, should raise ValueError."""
    bad_path = tmp_path / "bad.xlsx"
    bad_path.write_text("not excel")

    with pytest.raises(ValueError, match="No files could be read"):
        merge_excel_files([str(bad_path)])


def test_merge_handles_different_columns(tmp_path):
    """Files with different column sets should merge with NaN fill."""
    df1 = pd.DataFrame({"A": [1], "B": [2]})
    df2 = pd.DataFrame({"B": [3], "C": [4]})

    path1 = tmp_path / "diff1.xlsx"
    path2 = tmp_path / "diff2.xlsx"
    df1.to_excel(path1, index=False)
    df2.to_excel(path2, index=False)

    result = merge_excel_files([str(path1), str(path2)])
    assert "A" in result.columns
    assert "B" in result.columns
    assert "C" in result.columns
    assert len(result) == 2
