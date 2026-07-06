"""
Business Automation Toolkit - Main Orchestrator.

This is the entry point. It ties together all modules in the correct order:
1. Discover Excel files in the input directory.
2. Merge them into one dataset.
3. Clean the data (remove duplicates and empty rows).
4. Generate a summary report.
5. Export everything to the output directory.

Why an orchestrator?
- Each module is independent and testable on its own.
- The orchestrator defines the *workflow* — the sequence and error handling.
- A client could swap steps (skip cleaning, add email) by editing only this file.

Usage:
    python -m src.main
    python -m src.main --input ./custom_folder --output ./results
"""

import argparse
import os
import sys
import time

from src.logger import get_logger
from src.utils import discover_excel_files, ensure_directory
from src.merge import merge_excel_files
from src.cleaner import clean_data
from src.report import generate_summary, export_results

logger = get_logger(__name__)

# Project root (one level up from src/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Business Automation Toolkit - Excel Automation Module",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.main
  python -m src.main --input ./input --output ./output
  python -m src.main --input /path/to/client/files --output /path/to/results
        """,
    )
    parser.add_argument(
        "--input",
        default=os.path.join(PROJECT_ROOT, "input"),
        help="Directory containing Excel files to process (default: ./input)",
    )
    parser.add_argument(
        "--output",
        default=os.path.join(PROJECT_ROOT, "output"),
        help="Directory for output files (default: ./output)",
    )
    return parser.parse_args()


def run(input_dir: str, output_dir: str) -> dict:
    """
    Execute the full automation pipeline.

    Args:
        input_dir: Path to directory with input Excel files.
        output_dir: Path to directory for output files.

    Returns:
        Dict with output file paths and processing stats.
    """
    start_time = time.time()

    logger.info("=" * 60)
    logger.info("BUSINESS AUTOMATION TOOLKIT - Excel Processing")
    logger.info("=" * 60)
    logger.info(f"Input:  {input_dir}")
    logger.info(f"Output: {output_dir}")
    logger.info("-" * 60)

    # Step 1: Discover files
    logger.info("[1/5] Discovering Excel files...")
    file_paths = discover_excel_files(input_dir)

    # Step 2: Merge
    logger.info("[2/5] Merging files...")
    merged_df = merge_excel_files(file_paths)

    # Step 3: Clean
    logger.info("[3/5] Cleaning data...")
    cleaned_df, stats = clean_data(merged_df)

    # Step 4: Generate summary
    logger.info("[4/5] Generating summary report...")
    summary_df = generate_summary(cleaned_df, stats)

    # Step 5: Export
    logger.info("[5/5] Exporting results...")
    ensure_directory(output_dir)
    output_files = export_results(cleaned_df, summary_df, output_dir)

    elapsed = time.time() - start_time

    logger.info("-" * 60)
    logger.info(f"Processing complete in {elapsed:.2f}s")
    logger.info(f"  Files processed: {len(file_paths)}")
    logger.info(f"  Rows: {stats['rows_before']} → {stats['rows_after']}")
    logger.info(f"  Output: {output_dir}")
    logger.info("=" * 60)

    return {"files": output_files, "stats": stats, "elapsed": elapsed}


def main():
    """CLI entry point."""
    args = parse_args()

    try:
        result = run(args.input, args.output)
        print(f"\nDone. Output saved to: {args.output}")
        print(f"  Excel: {os.path.basename(result['files']['excel'])}")
        print(f"  CSV:   {os.path.basename(result['files']['csv'])}")
        print(f"  Summary: {os.path.basename(result['files']['summary'])}")
    except FileNotFoundError as e:
        logger.error(str(e))
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        logger.error(str(e))
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        print(f"\nUnexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
