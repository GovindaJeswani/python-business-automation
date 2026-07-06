# Screenshots

## Terminal Output

The toolkit produces rich, colored terminal output:

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

  Output Files:
    • excel: cleaned_data_20260706_204459.xlsx
    • csv: cleaned_data_20260706_204459.csv
    • summary: summary_report_20260706_204459.xlsx
```

## How to take your own screenshots

1. **Terminal**: Run `python3 -m src.main` and screenshot your terminal
2. **Excel Output**: Open `output/cleaned_data_*.xlsx` → screenshot the Data sheet
3. **Summary**: Open `output/summary_report_*.xlsx` → screenshot
4. **Folder Structure**: Screenshot VS Code / Finder showing the project tree

Place `.png` or `.jpg` files in this directory and reference them in the README.
