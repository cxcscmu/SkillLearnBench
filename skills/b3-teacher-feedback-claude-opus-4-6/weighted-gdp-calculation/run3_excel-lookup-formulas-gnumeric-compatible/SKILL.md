---
name: excel-lookup-formulas-gnumeric-compatible
description: How to write lookup formulas (INDEX/MATCH, VLOOKUP, SUMPRODUCT-based lookups) that work in both Excel and Gnumeric/LibreOffice for multi-condition lookups. Use this when filling cells with formulas that reference data based on multiple criteria.
---

# Writing Lookup Formulas Compatible with Gnumeric/LibreOffice

## Problem: Array formulas may not work in Gnumeric

Gnumeric and LibreOffice Calc may not properly evaluate array-entered formulas like:
```
{=INDEX(range, MATCH(1, (cond1)*(cond2), 0))}
```

## Solution 1: SUMPRODUCT-based lookup (most compatible)

When you need to look up a value using two or more conditions, use SUMPRODUCT which naturally handles arrays without Ctrl+Shift+Enter:

```
=SUMPRODUCT((condition1_range=value1)*(condition2_range=value2)*data_range)
```

This works because SUMPRODUCT inherently iterates over arrays. It returns the sum of products, and when only one row matches both conditions, it effectively returns just that value.

### Example: Look up a value by country AND series code
```
=SUMPRODUCT((Data.A$21:A$40="Bahrain")*(Data.B$21:B$40="NE.EXP.GNFS.CD")*(Data.F$21:F$40))
```

Where:
- Column A has country names
- Column B has series codes  
- Column F has the numeric data for a specific year

## Solution 2: INDEX with SUMPRODUCT for column matching

If the year column is also dynamic:
```
=INDEX(Data.$F$21:$J$40, SUMPRODUCT((Data.$A$21:$A$40=country_ref)*(Data.$B$21:$B$40=series_ref)*ROW(Data.$A$21:$A$40))-ROW(Data.$A$21)+1, MATCH(year_ref, Data.$F$1:$J$1, 0))
```

But this is complex. A simpler approach:

## Solution 3: SUMPRODUCT with column selection via nested approach

```
=SUMPRODUCT((country_range=country_val)*(series_range=series_val)*
  IF(year=2019, year2019_col, IF(year=2020, year2020_col, ...)))
```

Actually, the cleanest compatible approach:

## Solution 4: INDEX + MATCH + MATCH (two-dimensional lookup)

If the data can be filtered to a specific block (e.g., one country's data is in a known row range), use:

```
=INDEX(data_block, MATCH(series_code, series_column, 0), MATCH(year, year_header_row, 0))
```

This is a standard two-axis lookup that works everywhere. The key is that `data_block` must be a rectangular range of just the numeric data, `series_column` is the column of series codes aligned with the rows, and `year_header_row` is the row of years aligned with the columns.

## Solution 5: Three-condition SUMPRODUCT lookup

For a true three-condition lookup (country + series + year), where data is in a flat table:

If each year is in a separate column (wide format), you need to match the year to find the right column first, then use that. SUMPRODUCT can't easily select a column dynamically.

Best approach for wide-format data with 3 conditions:
```
=INDEX(data_range, MATCH(country&series, country_col&series_col, 0), MATCH(year, year_header, 0))
```

But concatenation inside MATCH needs array evaluation. For Gnumeric compatibility, use:

```
=SUMPRODUCT((country_range=country_val)*(series_range=series_val)*INDEX(data_range,,MATCH(year_val,year_header,0)))
```

The `INDEX(data_range,,MATCH(...))` extracts the entire column for the matching year, then SUMPRODUCT filters by country and series.

## Writing formulas with openpyxl

```python
import openpyxl
wb = openpyxl.load_workbook('gdp.xlsx')
ts = wb['Task']

# Always use sheet name prefix for cross-sheet references: Data.A1
# Use $ for absolute references where needed
# Use 0 (not FALSE) for exact match in MATCH

ts['H12'] = '=SUMPRODUCT((Data.$A$21:$A$40="Bahrain")*(Data.$C$21:$C$40=$D12)*INDEX(Data.$E$21:$I$40,,MATCH(H$10,Data.$E$20:$I$20,0)))'

wb.save('gdp.xlsx')
```

## Critical: Verify before writing

1. Print the actual cell values from the Data sheet to know exact column letters
2. Confirm where country names, series codes, and year headers are
3. Confirm data type matching (numbers vs text) for MATCH conditions
4. Test one formula first, open in Gnumeric/LibreOffice to verify it calculates