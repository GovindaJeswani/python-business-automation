"""
Summary report generation module.

Why a report module?
- Clients want proof that automation worked. A summary gives them confidence.
- Separating reporting from processing means we can change report format
  (add charts, change layout) without touching data logic.
- The report doubles as documentation of what happened during each run.
"""

import os
from datetime import datetime

import pandas as pd

from src.config import TIMESTAMP_FORMAT, EXPORT_EXCEL, EXPORT_CSV, EXPORT_SUMMARY
from src.logger import get_logger

logger = get_logger(__name__)


def generate_summary(df: pd.DataFrame, stats: dict) -> pd.DataFrame:
    """
    Create a summary DataFrame with key statistics about the processed data.

    Args:
        df: The cleaned DataFrame.
        stats: Cleaning statistics from the cleaner module.

    Returns:
        A DataFrame containing the summary report.
    """
    summary_data = {
        "Metric": [
            "Run Timestamp",
            "Total Rows (Before Cleaning)",
            "Duplicates Removed",
            "Empty Rows Removed",
            "Total Rows (After Cleaning)",
            "Total Columns",
            "Data Retention Rate",
        ],
        "Value": [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            str(stats["rows_before"]),
            str(stats["duplicates_removed"]),
            str(stats["empty_rows_removed"]),
            str(stats["rows_after"]),
            str(len([col for col in df.columns if col != "_source_file"])),
            f"{(stats['rows_after'] / max(stats['rows_before'], 1)) * 100:.1f}%",
        ],
    }

    summary_df = pd.DataFrame(summary_data)
    logger.info("Summary report generated")
    return summary_df


def export_results(
    df: pd.DataFrame,
    summary_df: pd.DataFrame,
    output_dir: str,
) -> dict:
    """
    Export cleaned data and summary to Excel and CSV files.

    Produces:
    - cleaned_data.xlsx (with two sheets: Data and Summary)
    - cleaned_data.csv (data only, for systems that prefer CSV)
    - summary_report.xlsx (standalone summary)

    Args:
        df: Cleaned DataFrame to export.
        summary_df: Summary report DataFrame.
        output_dir: Directory to write output files.

    Returns:
        Dict with paths to all generated files.
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)

    # Remove internal tracking column before export
    export_df = df.drop(columns=["_source_file"], errors="ignore")

    output_files = {}

    # Main Excel output with two sheets
    if EXPORT_EXCEL:
        excel_path = os.path.join(output_dir, f"cleaned_data_{timestamp}.xlsx")
        with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
            export_df.to_excel(writer, sheet_name="Data", index=False)
            summary_df.to_excel(writer, sheet_name="Summary", index=False)
        output_files["excel"] = excel_path

    # CSV export for interoperability
    if EXPORT_CSV:
        csv_path = os.path.join(output_dir, f"cleaned_data_{timestamp}.csv")
        export_df.to_csv(csv_path, index=False)
        output_files["csv"] = csv_path

    # Standalone summary
    if EXPORT_SUMMARY:
        summary_path = os.path.join(output_dir, f"summary_report_{timestamp}.xlsx")
        summary_df.to_excel(summary_path, index=False)
        output_files["summary"] = summary_path

    logger.info(f"Exported results to {output_dir}/")
    for key, path in output_files.items():
        logger.debug(f"  {key}: {os.path.basename(path)}")

    return output_files
