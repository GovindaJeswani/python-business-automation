"""
Centralized configuration for the Business Automation Toolkit.

Why a config module?
- All tunables live in one place. No hunting through code to change a path.
- Clients can adjust behavior (extensions, thresholds) without reading business logic.
- Makes the toolkit feel like configurable software, not a hardcoded script.
"""

import os

# ─── Paths ──────────────────────────────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_DIR = os.path.join(PROJECT_ROOT, "input")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
SAMPLE_DIR = os.path.join(PROJECT_ROOT, "sample_data")

# ─── File Discovery ─────────────────────────────────────────────────────────────
EXCEL_EXTENSIONS = (".xlsx", ".xls")
IGNORE_TEMP_FILES = True  # Skip files starting with ~$ (Excel lock files)

# ─── Cleaning ───────────────────────────────────────────────────────────────────
DUPLICATE_CHECK_IGNORE_COLUMNS = ["_source_file"]  # Columns excluded from dedup
EMPTY_ROW_CHECK_IGNORE_COLUMNS = ["_source_file"]  # Columns excluded from empty check

# ─── Export ─────────────────────────────────────────────────────────────────────
EXPORT_EXCEL = True
EXPORT_CSV = True
EXPORT_SUMMARY = True
TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"

# ─── Logging ────────────────────────────────────────────────────────────────────
LOG_LEVEL_CONSOLE = "INFO"
LOG_LEVEL_FILE = "DEBUG"
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ─── Display ────────────────────────────────────────────────────────────────────
SHOW_PROGRESS_BAR = True
USE_RICH_OUTPUT = True
