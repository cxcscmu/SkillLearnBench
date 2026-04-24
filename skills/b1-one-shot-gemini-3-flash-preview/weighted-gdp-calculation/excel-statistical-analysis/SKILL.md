---
name: excel-statistical-analysis
description: Covers descriptive statistics (mean, median, percentiles) and weighted averages using Excel formulas.
---

# Excel Statistical Analysis

This skill covers the calculation of descriptive statistics and advanced metrics like weighted means.

## Core Functions

### 1. Descriptive Statistics
- **Mean (Average):** `=AVERAGE(range)`
- **Median:** `=MEDIAN(range)`
- **Min/Max:** `=MIN(range)`, `=MAX(range)`
- **Percentiles:** `=PERCENTILE.INC(range, 0.25)` for 25th percentile, `=PERCENTILE.INC(range, 0.75)` for 75th percentile.

### 2. Weighted Mean
The weighted mean uses the `SUMPRODUCT` and `SUM` functions:
`=SUMPRODUCT(values_range, weights_range) / SUM(weights_range)`

### 3. Data Transformation and Rounding
To represent decimals as percentages (e.g., 0.123 as 12.3):
`=ROUND(value * 100, 1)` or `=value * 100` if formatting handles the rest.

## Usage Pattern

**For Net Exports as % of GDP:**
If Net Exports are in range `NX_Range` and GDP is in `GDP_Range`:
`=ROUND((NX_Value / GDP_Value) * 100, 1)`

**For Weighted Mean of Percentages:**
To weight net export percentages by GDP:
`=ROUND(SUMPRODUCT(percentages_range, weights_range) / SUM(weights_range), 1)`
