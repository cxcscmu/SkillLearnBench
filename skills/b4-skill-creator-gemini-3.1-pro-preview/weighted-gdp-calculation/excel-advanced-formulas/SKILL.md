---
name: excel-advanced-formulas
description: How to write advanced Excel formulas (INDEX/MATCH, XLOOKUP, VLOOKUP, SUMPRODUCT, Percentiles, and other statistical functions). Use this skill whenever you need to populate Excel cells with advanced lookup or statistical formulas, or when calculating weighted averages in Excel.
---

# Excel Advanced Formulas Guide

This skill provides correct syntax and usage for common advanced Excel formulas, specifically for two-way lookups, statistical functions, and weighted means.

## Lookups with Two Criteria
When you need to look up a value based on two criteria (e.g., matching a row and a column), use INDEX/MATCH, VLOOKUP/MATCH, or HLOOKUP/MATCH.

### VLOOKUP with MATCH (2D Lookup)
`=VLOOKUP(row_lookup_value, table_array, MATCH(col_lookup_value, header_range, 0), FALSE)`
Where `header_range` starts from the same column as `table_array` and spans across.

### INDEX / MATCH (2D Lookup)
`=INDEX(data_range, MATCH(row_lookup_value, row_labels_range, 0), MATCH(col_lookup_value, col_labels_range, 0))`

### XLOOKUP (Nested for 2D Lookup)
`=XLOOKUP(row_lookup_value, row_labels_range, XLOOKUP(col_lookup_value, col_labels_range, data_range))`

## Statistical Functions
Use these formulas for basic descriptive statistics over a `range`:
- **Min**: `=MIN(range)`
- **Max**: `=MAX(range)`
- **Median**: `=MEDIAN(range)`
- **Simple Mean**: `=AVERAGE(range)`
- **25th Percentile**: `=PERCENTILE.INC(range, 0.25)`
- **75th Percentile**: `=PERCENTILE.INC(range, 0.75)`

## Weighted Mean using SUMPRODUCT
To calculate a weighted mean (e.g., a metric weighted by GDP):
`=SUMPRODUCT(values_range, weights_range) / SUM(weights_range)`

*Note on Percentages:* If requirements state percentages should be rounded to one decimal place as whole numbers (e.g., 12.3 instead of 0.123), multiply the final calculation by 100:
`=(SUMPRODUCT(values, weights) / SUM(weights)) * 100`
Or for regular formulas: `= (value / total) * 100`