"""Tests for the report module."""

import os

import pandas as pd
import pytest

from src.report import generate_summary, export_results


@pytest.fixture
def cleaned_df():
    """A sample cleaned DataFrame."""
    return pd.DataFrame({
        "Name": ["Alice", "Bob", "Carol"],
        "Amount": [100, 200, 300],
        "_source_file": ["f1.xlsx", "f1.xlsx", "f2.xlsx"],
    })


@pytest.fixture
def stats():
    """Sample cleaning stats."""
    return {
        "rows_before": 5,
        "duplicates_removed": 1,
        "empty_rows_removed": 1,
        "rows_after": 3,
    }


def test_generate_summary_returns_dataframe(cleaned_df, stats):
    """Summary should be a DataFrame with Metric and Value columns."""
    result = generate_summary(cleaned_df, stats)
    assert isinstance(result, pd.DataFrame)
    assert "Metric" in result.columns
    assert "Value" in result.columns


def test_generate_summary_contains_key_metrics(cleaned_df, stats):
    """Summary should include all important metrics."""
    result = generate_summary(cleaned_df, stats)
    metrics = result["Metric"].tolist()
    assert "Total Rows (Before Cleaning)" in metrics
    assert "Duplicates Removed" in metrics
    assert "Empty Rows Removed" in metrics
    assert "Total Rows (After Cleaning)" in metrics
    assert "Data Retention Rate" in metrics


def test_generate_summary_correct_values(cleaned_df, stats):
    """Values in summary should match the stats provided."""
    result = generate_summary(cleaned_df, stats)
    values = dict(zip(result["Metric"], result["Value"]))
    assert values["Total Rows (Before Cleaning)"] == "5"
    assert values["Duplicates Removed"] == "1"
    assert values["Total Rows (After Cleaning)"] == "3"
    assert values["Data Retention Rate"] == "60.0%"


def test_export_creates_excel(cleaned_df, stats, tmp_path):
    """Export should create an Excel file."""
    summary_df = generate_summary(cleaned_df, stats)
    output_files = export_results(cleaned_df, summary_df, str(tmp_path))

    assert "excel" in output_files
    assert os.path.exists(output_files["excel"])
    assert output_files["excel"].endswith(".xlsx")


def test_export_creates_csv(cleaned_df, stats, tmp_path):
    """Export should create a CSV file."""
    summary_df = generate_summary(cleaned_df, stats)
    output_files = export_results(cleaned_df, summary_df, str(tmp_path))

    assert "csv" in output_files
    assert os.path.exists(output_files["csv"])

    # CSV should not contain the _source_file column
    csv_df = pd.read_csv(output_files["csv"])
    assert "_source_file" not in csv_df.columns


def test_export_creates_summary(cleaned_df, stats, tmp_path):
    """Export should create a standalone summary file."""
    summary_df = generate_summary(cleaned_df, stats)
    output_files = export_results(cleaned_df, summary_df, str(tmp_path))

    assert "summary" in output_files
    assert os.path.exists(output_files["summary"])


def test_export_excel_has_two_sheets(cleaned_df, stats, tmp_path):
    """Main Excel file should have Data and Summary sheets."""
    summary_df = generate_summary(cleaned_df, stats)
    output_files = export_results(cleaned_df, summary_df, str(tmp_path))

    xl = pd.ExcelFile(output_files["excel"])
    assert "Data" in xl.sheet_names
    assert "Summary" in xl.sheet_names
