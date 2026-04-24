---
name: gdp-weighted-mean-net-exports-gcc
description: How to calculate net exports as % of GDP, descriptive statistics, and weighted mean for GCC countries in the gdp.xlsx workbook. Use this for the specific task of filling in the Task sheet with lookup formulas, percentage calculations, and SUMPRODUCT weighted mean.
---

# Calculating Weighted Mean of Net Exports (% of GDP) for GCC Countries

## Overview

The workbook `gdp.xlsx` has two sheets:
- **Data**: Source data in rows 21-40 with country names, series codes, and yearly values
- **Task**: Where formulas go. Has blue condition cells and yellow target cells.

## CRITICAL: Inspect first, then write formulas

You MUST run inspection code to determine the exact layout before writing any formula.

```python
import openpyxl

wb = openpyxl.load_workbook('gdp.xlsx', data_only=True)
ds = wb['Data']
ts = wb['Task']

# Print EVERYTHING in both sheets
for sheet_name in ['Data', 'Task']:
    s = wb[sheet_name]
    print(f"\n{'='*60}")
    print(f"SHEET: {sheet_name} (rows {s.min_row}-{s.max_row}, cols {s.min_column}-{s.max_column})")
    print(f"{'='*60}")
    for row in s.iter_rows(min_row=1, max_row=s.max_row, min_col=1, max_col=s.max_column, values_only=False):
        row_num = row[0].row
        vals = {cell.column_letter: cell.value for cell in row if cell.value is not None}
        if vals:
            print(f"  Row {row_num}: {vals}")
```

## Step 1: Fill lookup ranges (H12:L17, H19:L24, H26:L31)

After inspection, you'll know:
- Which column in Data has country names
- Which column has series codes
- Which row has year headers
- Which columns have the numeric year data

### Formula pattern (adapt column letters based on inspection)

The lookup must match THREE things: country name (from Task sheet), series code (from Task column D), and year (from Task row 10).

Use SUMPRODUCT for Gnumeric compatibility:

```
=SUMPRODUCT((Data.$A$21:$A$40=countryRef)*(Data.$B$21:$B$40=$D12)*INDEX(Data.$E$21:$I$40,,MATCH(H$10,Data.$E$20:$I$20,0)))
```

**Adapt all column letters** based on what the inspection reveals.

### Where does the country name come from?

Check the Task sheet layout. The country name for rows 12-17 might be in column C, column B, or somewhere else. Or it might be that each block (H12:L17, H19:L24, H26:L31) corresponds to a different data series and the rows within each block are different countries. Inspect carefully!

### Data type matching for years

If Task row 10 has years as numbers (e.g., 2019) but Data header has them as text (e.g., "2019"), use:
```
MATCH(H$10*1, ...)   or   MATCH(TEXT(H$10,"0"), ...)
```

Or if Data has numbers and Task has text:
```
MATCH(H$10+0, ...)   or   MATCH(VALUE(H$10), ...)
```

## Step 2: Net exports as % of GDP

Net exports = Exports - Imports

The formula in H35:L40 should calculate:
```
= (Exports - Imports) / GDP * 100
```

Using cell references from the three blocks filled in Step 1. For example if:
- H12:L17 = Exports (or GDP, etc.)
- H19:L24 = Imports
- H26:L31 = GDP

Then: `=(H12 - H19) / H26 * 100` (adjust based on what each block actually represents)

**Multiply by 100** to display as percentage number (12.3 not 0.123).

### Descriptive statistics

Use Excel functions in the designated cells:
- MIN: `=MIN(H35:H40)`
- MAX: `=MAX(H35:H40)`
- MEDIAN: `=MEDIAN(H35:H40)`
- Simple mean: `=AVERAGE(H35:H40)`
- 25th percentile: `=PERCENTILE(H35:H40, 0.25)`
- 75th percentile: `=PERCENTILE(H35:H40, 0.75)`

**Round to 1 decimal**: Wrap with `=ROUND(..., 1)` or ensure the formula inherently produces the right precision.

## Step 3: Weighted mean using SUMPRODUCT

The weighted mean of net exports (% of GDP) weighted by GDP:

```
=ROUND(SUMPRODUCT(net_exports_pct_range, gdp_range) / SUM(gdp_range), 1)
```

Or equivalently, since net exports % = (Exp-Imp)/GDP*100:

```
=ROUND(SUMPRODUCT((exports_range - imports_range) / gdp_range * 100, gdp_range) / SUM(gdp_range), 1)
```

Which simplifies to:
```
=ROUND(SUMPRODUCT(exports_range - imports_range) / SUM(gdp_range) * 100, 1)
```

But it's safer to use the already-calculated percentages with GDP weights:
```
=ROUND(SUMPRODUCT(H35:H40, gdp_column_for_that_year) / SUM(gdp_column_for_that_year), 1)
```

## Step 4: Rounding

All percentage results in Steps 2 and 3 must display as numbers rounded to 1 decimal place (e.g., 12.3 not 0.123).

Use `=ROUND(formula * 100, 1)` if the base calculation returns a decimal, or `=ROUND(formula, 1)` if already multiplied by 100.

## Writing formulas with openpyxl

```python
wb = openpyxl.load_workbook('gdp.xlsx')  # NOT data_only
ts = wb['Task']

# Set formula (string starting with =)
ts['H12'] = '=SUMPRODUCT(...)'

# Do NOT change formatting, colors, fonts
# Do NOT add macros or VBA

wb.save('gdp.xlsx')
```

## Common pitfalls

1. **Wrong column letters**: The #1 cause of failure. Always inspect first.
2. **Country name mismatch**: "Bahrain" vs "Bahrain, Kingdom of" — check exact strings.
3. **Series code mismatch**: Must match exactly including case.
4. **Year type mismatch**: Numbers vs text causes MATCH to fail silently.
5. **Gnumeric compatibility**: Avoid Ctrl+Shift+Enter array formulas. Use SUMPRODUCT.
6. **Cross-sheet reference syntax**: Use `Data.A1` (with period) for references to the Data sheet.
7. **Forgetting *100**: Results must be in percentage points (12.3), not decimals (0.123).