# Business Automation Toolkit

> Merge, clean, and report on hundreds of Excel files in seconds. Built for businesses that waste hours on manual data consolidation.

[![Tests](https://github.com/GovindaJeswani/python-business-automation/actions/workflows/tests.yml/badge.svg)](https://github.com/GovindaJeswani/python-business-automation/actions/workflows/tests.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## The Problem

Companies receive hundreds of Excel files every month — from branches, vendors, or internal systems. Consolidating them manually means:

- Hours of copy-paste work
- Missed duplicates that corrupt reports
- Empty rows that break dashboards
- No audit trail of what was processed

**One mistake costs more than the software to prevent it.**

---

## The Solution

Drop your files in a folder. Run one command. Get clean, merged output in seconds.

```bash
python3 -m src.main --input ./client_files --output ./results
```

```
╭────────────────────────────────────╮
│                                    │
│    Business Automation Toolkit     │
│    Excel Processing Module v1.0    │
│                                    │
╰────────────────────────────────────╯

  ✓ [1/5] Found 5 file(s)
  ✓ [2/5] Merged → 110 rows
  ✓ [3/5] Cleaned → 100 rows
  ✓ [4/5] Summary report generated
  ✓ [5/5] Export complete

      Processing Summary
╭────────────────────┬───────╮
│ Metric             │ Value │
├────────────────────┼───────┤
│ Rows Before        │   110 │
│ Duplicates Removed │   -10 │
│ Empty Rows Removed │    -0 │
│ Rows After         │   100 │
│ Data Retention     │ 90.9% │
│ Time Elapsed       │ 0.17s │
╰────────────────────┴───────╯
```

---

## Architecture

```
input/*.xlsx
     │
     ▼
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  merge   │ ──▶ │ cleaner  │ ──▶ │  report  │ ──▶ │  export  │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
                                                         │
                                              ┌──────────┼──────────┐
                                              ▼          ▼          ▼
                                          .xlsx       .csv      summary
```

**Design principles:**
- Each module does one thing (single responsibility)
- Modules are independent — use merge without cleaning, or cleaning without reporting
- One bad file doesn't crash the batch (graceful error handling)
- Every row is traceable back to its source file

---

## Features

| Feature | Description |
|---------|-------------|
| Multi-file merge | Reads all `.xlsx`/`.xls` files from input directory |
| Duplicate removal | Detects and removes exact duplicate rows across files |
| Empty row cleanup | Removes rows where all business columns are null |
| Source tracking | `_source_file` column traces every row to its origin |
| Summary report | Statistics on what was processed and cleaned |
| Dual export | Output as Excel (multi-sheet) and CSV |
| Progress bar | Visual feedback with tqdm during processing |
| Rich terminal | Colored, formatted output using Rich |
| Full logging | Timestamped audit trail in `logs/` |
| Configurable | All settings in one `config.py` file |
| CI/CD | Automated tests on every push via GitHub Actions |

---

## Demo

```bash
# Generate sample data (5 files with duplicates + empty rows)
python3 sample_data/generate_samples.py

# Copy to input folder
cp sample_data/*.xlsx input/

# Run the toolkit
python3 -m src.main
```

---

## Installation

```bash
git clone https://github.com/GovindaJeswani/python-business-automation.git
cd python-business-automation
pip install -r requirements.txt
```

### Requirements
- Python 3.9+
- pandas, openpyxl, tqdm, rich

---

## Usage

### Basic (default paths)
```bash
python3 -m src.main
```

### Custom input/output
```bash
python3 -m src.main --input /path/to/client/files --output /path/to/results
```

### Output Files

| Output File | Description |
|-------------|-------------|
| `cleaned_data_TIMESTAMP.xlsx` | Cleaned data (Sheet: Data) + Summary (Sheet: Summary) |
| `cleaned_data_TIMESTAMP.csv` | Same data in CSV for downstream systems |
| `summary_report_TIMESTAMP.xlsx` | Standalone summary for clients |

---

## Project Structure

```
python-business-automation/
├── .github/workflows/    ← CI: runs tests on every push
├── input/                ← Drop Excel files here
├── output/               ← Results appear here
├── logs/                 ← Timestamped audit logs
├── sample_data/          ← Demo files + generator
├── screenshots/          ← Terminal + output screenshots
├── src/
│   ├── config.py         ← All settings in one place
│   ├── main.py           ← Orchestrator (entry point)
│   ├── merge.py          ← File merging + progress bar
│   ├── cleaner.py        ← Dedup + empty row removal
│   ├── report.py         ← Summary generation + export
│   ├── logger.py         ← Centralized logging
│   └── utils.py          ← File discovery utilities
└── tests/
    ├── test_merge.py     ← 6 tests
    ├── test_cleaner.py   ← 7 tests
    └── test_report.py    ← 7 tests
```

---

## Configuration

All settings live in `src/config.py`:

```python
# Paths
INPUT_DIR = "input"
OUTPUT_DIR = "output"

# File types to process
EXCEL_EXTENSIONS = (".xlsx", ".xls")

# Export options
EXPORT_EXCEL = True
EXPORT_CSV = True
EXPORT_SUMMARY = True

# Display
SHOW_PROGRESS_BAR = True
USE_RICH_OUTPUT = True
```

---

## Running Tests

```bash
pytest tests/ -v
```

```
tests/test_cleaner.py   7 passed
tests/test_merge.py     6 passed
tests/test_report.py    7 passed
======================== 20 passed in 0.64s ========================
```

---

## Technologies

| Tool | Purpose |
|------|---------|
| Python 3.9+ | Core language |
| Pandas | Data manipulation |
| OpenPyXL | Excel read/write |
| tqdm | Progress bars |
| Rich | Terminal formatting |
| pytest | Unit testing |
| GitHub Actions | CI/CD |

---

## Roadmap

- [x] v1: Merge + Clean + Report + Export
- [ ] v2: Email report delivery (SMTP)
- [ ] v3: GUI dashboard (Streamlit)
- [ ] v4: Scheduled automation (cron integration)
- [ ] Invoice processing module
- [ ] CSV cleaner module

---

## License

[MIT](LICENSE)
