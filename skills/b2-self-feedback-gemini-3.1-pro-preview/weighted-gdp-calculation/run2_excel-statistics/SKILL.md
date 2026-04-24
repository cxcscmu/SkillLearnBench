---
name: run2_excel-statistics
description: Calculating and rounding summary statistics like percentiles in Excel.
---

# Statistical Metrics in Excel

Excel provides built-in functions for summarizing data sets. When formatting is restricted, or exact value representation is required, use `ROUND`.

## Key Functions
- **Min / Max / Median**: `=MIN(range)`, `=MAX(range)`, `=MEDIAN(range)`
- **Mean**: `=AVERAGE(range)`
- **Percentiles**: The safest function across all Excel versions and LibreOffice is `=PERCENTILE(range, k)` where `k` is the fraction (e.g., `0.25` or `0.75`).

## Applying Hard Rounding
To force a calculation to a specific decimal place explicitly (not just visually formatted), wrap the entire calculation in `ROUND`:
```excel
=ROUND(PERCENTILE(H35:H40, 0.25), 1)
```
This ensures the stored value is accurately rounded to one decimal place, e.g., `12.3`.
