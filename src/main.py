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

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from src.config import PROJECT_ROOT, INPUT_DIR, OUTPUT_DIR, USE_RICH_OUTPUT
from src.logger import get_logger
from src.utils import discover_excel_files, ensure_directory
from src.merge import merge_excel_files
from src.cleaner import clean_data
from src.report import generate_summary, export_results

logger = get_logger(__name__)
console = Console()


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
        default=INPUT_DIR,
        help="Directory containing Excel files to process (default: ./input)",
    )
    parser.add_argument(
        "--output",
        default=OUTPUT_DIR,
        help="Directory for output files (default: ./output)",
    )
    return parser.parse_args()


def print_header():
    """Display a styled header banner."""
    if USE_RICH_OUTPUT:
        console.print()
        console.print(
            Panel.fit(
                "[bold cyan]Business Automation Toolkit[/bold cyan]\n"
                "[dim]Excel Processing Module v1.0[/dim]",
                border_style="cyan",
                padding=(1, 4),
            )
        )
        console.print()
    else:
        print("=" * 60)
        print("BUSINESS AUTOMATION TOOLKIT - Excel Processing")
        print("=" * 60)


def print_step(step: int, total: int, message: str, status: str = "running"):
    """Display a step with status indicator."""
    if USE_RICH_OUTPUT:
        icons = {"running": "⏳", "done": "✓", "error": "✗"}
        colors = {"running": "yellow", "done": "green", "error": "red"}
        icon = icons.get(status, "•")
        color = colors.get(status, "white")
        console.print(f"  [{color}]{icon}[/{color}] [{color}][{step}/{total}][/{color}] {message}")
    else:
        print(f"  [{step}/{total}] {message}")


def print_summary_table(stats: dict, output_files: dict, elapsed: float):
    """Display a rich summary table."""
    if USE_RICH_OUTPUT:
        console.print()

        table = Table(
            title="Processing Summary",
            box=box.ROUNDED,
            title_style="bold green",
            show_header=True,
            header_style="bold",
        )
        table.add_column("Metric", style="cyan")
        table.add_column("Value", justify="right")

        table.add_row("Rows Before", str(stats["rows_before"]))
        table.add_row("Duplicates Removed", f"[red]-{stats['duplicates_removed']}[/red]")
        table.add_row("Empty Rows Removed", f"[red]-{stats['empty_rows_removed']}[/red]")
        table.add_row("Rows After", f"[green]{stats['rows_after']}[/green]")
        retention = (stats["rows_after"] / max(stats["rows_before"], 1)) * 100
        table.add_row("Data Retention", f"[green]{retention:.1f}%[/green]")
        table.add_row("Time Elapsed", f"{elapsed:.2f}s")

        console.print(table)
        console.print()

        # Output files
        console.print("  [bold]Output Files:[/bold]")
        for key, path in output_files.items():
            console.print(f"    [dim]•[/dim] {key}: [cyan]{os.path.basename(path)}[/cyan]")
        console.print()
    else:
        print(f"\n  Rows: {stats['rows_before']} → {stats['rows_after']}")
        print(f"  Time: {elapsed:.2f}s")
        for key, path in output_files.items():
            print(f"  {key}: {os.path.basename(path)}")


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
    total_steps = 5

    print_header()

    logger.info("=" * 60)
    logger.info("BUSINESS AUTOMATION TOOLKIT - Excel Processing")
    logger.info("=" * 60)
    logger.info(f"Input:  {input_dir}")
    logger.info(f"Output: {output_dir}")

    if USE_RICH_OUTPUT:
        console.print(f"  [dim]Input:[/dim]  {input_dir}")
        console.print(f"  [dim]Output:[/dim] {output_dir}")
        console.print()

    # Step 1: Discover files
    print_step(1, total_steps, "Discovering Excel files...")
    file_paths = discover_excel_files(input_dir)
    print_step(1, total_steps, f"Found {len(file_paths)} file(s)", "done")

    # Step 2: Merge
    print_step(2, total_steps, "Merging files...")
    merged_df = merge_excel_files(file_paths)
    print_step(2, total_steps, f"Merged → {len(merged_df)} rows", "done")

    # Step 3: Clean
    print_step(3, total_steps, "Cleaning data...")
    cleaned_df, stats = clean_data(merged_df)
    print_step(3, total_steps, f"Cleaned → {stats['rows_after']} rows", "done")

    # Step 4: Generate summary
    print_step(4, total_steps, "Generating summary report...")
    summary_df = generate_summary(cleaned_df, stats)
    print_step(4, total_steps, "Summary report generated", "done")

    # Step 5: Export
    print_step(5, total_steps, "Exporting results...")
    ensure_directory(output_dir)
    output_files = export_results(cleaned_df, summary_df, output_dir)
    print_step(5, total_steps, "Export complete", "done")

    elapsed = time.time() - start_time

    logger.info(f"Processing complete in {elapsed:.2f}s")
    logger.info(f"  Files processed: {len(file_paths)}")
    logger.info(f"  Rows: {stats['rows_before']} → {stats['rows_after']}")

    print_summary_table(stats, output_files, elapsed)

    return {"files": output_files, "stats": stats, "elapsed": elapsed}


def main():
    """CLI entry point."""
    args = parse_args()

    try:
        run(args.input, args.output)
    except FileNotFoundError as e:
        logger.error(str(e))
        if USE_RICH_OUTPUT:
            console.print(f"\n  [red]✗ Error:[/red] {e}")
        else:
            print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        logger.error(str(e))
        if USE_RICH_OUTPUT:
            console.print(f"\n  [red]✗ Error:[/red] {e}")
        else:
            print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        if USE_RICH_OUTPUT:
            console.print(f"\n  [red]✗ Unexpected error:[/red] {e}")
        else:
            print(f"\nUnexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
