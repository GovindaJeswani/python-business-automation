# Case Study: Excel Report Automation

## Problem

Small and mid-size businesses receive dozens to hundreds of Excel files every month — sales reports from regional branches, vendor invoices, system exports, employee timesheets. Consolidating them manually means:

- 2–4 hours of repetitive copy-paste work per reporting cycle
- Duplicate rows that silently corrupt downstream dashboards
- Empty rows that break pivot tables and formulas
- No way to verify what was processed or trace errors back to source files

The cost isn't just time — it's the mistakes that go unnoticed until a quarterly review.

## Solution

The Business Automation Toolkit replaces manual consolidation with a single command:

```bash
python3 -m src.main --input ./monthly_reports --output ./results
```

It reads every Excel file in the input folder, merges them into one dataset, removes duplicates and empty rows, generates a summary report, and exports clean output as both Excel and CSV — with full logging of every step.

The toolkit is designed to be handed to a non-technical user: drop files in a folder, run the command, pick up results.

## Technical Decisions

| Decision | Reasoning |
|----------|-----------|
| Modular architecture (merge → clean → report) | Each step can be used independently. A client who only needs merging doesn't pay for (or break) cleaning logic. |
| Source file tracking (`_source_file` column) | Traceability. When a client asks "where did this row come from?" — there's an answer. |
| Graceful error handling | One corrupted file out of 100 shouldn't block the entire batch. Log it, skip it, keep going. |
| Config module | All tunables in one file. When a client says "we also have .csv files" — it's a one-line change. |
| Timestamped outputs | Never overwrites previous runs. Enables comparison between processing cycles. |
| Rich CLI + progress bar | Gives non-technical users confidence that something is happening. Silence creates anxiety. |

## Results

Processing 5 regional sales reports (120 total rows with intentional data quality issues):

| Metric | Value |
|--------|-------|
| Files processed | 5 |
| Rows merged | 110 |
| Duplicates removed | 10 |
| Empty rows removed | 0 |
| Final clean rows | 100 |
| Data retention rate | 90.9% |
| Processing time | 0.19 seconds |
| Output formats | Excel (multi-sheet) + CSV + Summary |

## Business Value

A task that previously took 2–4 hours of manual work per month now completes in under 1 second with zero human error.

For a business processing this monthly:
- **Time saved:** ~30 hours/year of analyst time
- **Error reduction:** Duplicates caught automatically instead of discovered weeks later
- **Audit trail:** Full logs prove exactly what was processed, when, and what was removed
- **Scalability:** Works the same whether the input is 5 files or 500

The toolkit pays for itself after a single use.
