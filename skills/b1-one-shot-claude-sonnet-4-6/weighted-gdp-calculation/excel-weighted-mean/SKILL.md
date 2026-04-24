---
name: excel-weighted-mean
description: Calculating GDP-weighted means and other weighted statistics in Excel using SUMPRODUCT, including net exports as percent of GDP.
---

# Excel Weighted Mean with SUMPRODUCT

## Overview

A weighted mean assigns different weights to each observation. In economic analysis, GDP-weighted averages give more influence to larger economies.

## Formula

```excel
=SUMPRODUCT(values_range, weights_range) / SUM(weights_range)
```

## Example: GDP-Weighted Net Exports % GDP

```excel
=ROUND(SUMPRODUCT(H35:H40, H26:H31) / SUM(H26:H31), 1)
```

Where:
- `H35:H40` — net exports as % of GDP for each country (already in percentage form, e.g., 12.3 means 12.3%)
- `H26:H31` — GDP values in billions (used as weights)
- Result is automatically in the same scale as the input values (12.3 form, not 0.123)

## Scale Consistency

If values in H35:H40 are stored as 12.3 (percent form), the weighted mean formula returns the result in the same 12.3 form — no additional multiplication by 100 is needed.

## Net Exports as Percent of GDP

```excel
=ROUND((Exports - Imports) / GDP * 100, 1)
```

Example where exports are in row 12, imports in row 19, GDP in row 26:
```excel
=ROUND((H12 - H19) / H26 * 100, 1)
```

## Related Statistical Functions

All rounded to 1 decimal for consistency:

```excel
=ROUND(MIN(H35:H40), 1)                    ' Minimum
=ROUND(MAX(H35:H40), 1)                    ' Maximum
=ROUND(MEDIAN(H35:H40), 1)                 ' Median
=ROUND(AVERAGE(H35:H40), 1)               ' Simple mean
=ROUND(PERCENTILE(H35:H40, 0.25), 1)      ' 25th percentile
=ROUND(PERCENTILE(H35:H40, 0.75), 1)      ' 75th percentile
=ROUND(SUMPRODUCT(H35:H40, H26:H31) / SUM(H26:H31), 1)  ' GDP-weighted mean
```

## SUMPRODUCT for Weighted Mean vs Simple Mean

| Formula | Description |
|---------|-------------|
| `=AVERAGE(H35:H40)` | Simple mean (equal weights) |
| `=SUMPRODUCT(H35:H40, H26:H31)/SUM(H26:H31)` | GDP-weighted mean |

The weighted mean will differ from the simple mean because larger economies pull the average toward their values.

## Setting in Python (openpyxl)

```python
from openpyxl import load_workbook

wb = load_workbook('file.xlsx')
ws = wb['Task']

# Weighted mean formula
ws['H50'] = '=ROUND(SUMPRODUCT(H35:H40,H26:H31)/SUM(H26:H31),1)'

# Statistics
ws['H42'] = '=ROUND(MIN(H35:H40),1)'
ws['H43'] = '=ROUND(MAX(H35:H40),1)'
ws['H44'] = '=ROUND(MEDIAN(H35:H40),1)'
ws['H45'] = '=ROUND(AVERAGE(H35:H40),1)'
ws['H46'] = '=ROUND(PERCENTILE(H35:H40,0.25),1)'
ws['H47'] = '=ROUND(PERCENTILE(H35:H40,0.75),1)'

wb.save('file.xlsx')
```
