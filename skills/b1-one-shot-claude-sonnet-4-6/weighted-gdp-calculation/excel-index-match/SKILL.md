---
name: excel-index-match
description: Using INDEX&MATCH (single and dual condition) for dynamic lookups across rows and columns in Excel, including cross-sheet references.
---

# INDEX & MATCH for Two-Condition Lookups

## Overview
INDEX&MATCH is preferred over VLOOKUP/HLOOKUP because it allows:
- Lookups by both row AND column simultaneously
- Lookups in any direction (not just left-to-right)
- Cross-sheet references with ease

## Basic Syntax

```excel
=INDEX(data_range, MATCH(row_key, row_lookup_range, 0), MATCH(col_key, col_lookup_range, 0))
```

## Two-Dimensional Lookup Pattern

When you need to find a value based on BOTH a row label (e.g., series code) and a column label (e.g., year):

```excel
=INDEX(Data!$H$21:$M$40,
       MATCH($D12, Data!$B$21:$B$40, 0),
       MATCH(H$10, Data!$H$4:$M$4, 0))
```

**Explanation:**
- `Data!$H$21:$M$40` — the value table (rows = series, cols = years)
- `MATCH($D12, Data!$B$21:$B$40, 0)` — find the ROW where D12's series code appears in column B
- `MATCH(H$10, Data!$H$4:$M$4, 0)` — find the COLUMN where H10's year appears in row 4
- `0` = exact match

## Dollar Sign Anchoring for Drag-Copying

Use mixed references so formulas can be dragged across rows and columns:

```excel
=INDEX(Data!$H$21:$M$40, MATCH($D12, Data!$B$21:$B$40, 0), MATCH(H$10, Data!$H$4:$M$4, 0))
```

- `$D12` — column D is fixed (series code column), row shifts when dragged down
- `H$10` — column H shifts when dragged right, row 10 is fixed (year header row)
- `Data!$B$21:$B$40` — fully fixed (lookup range never changes)
- `Data!$H$4:$M$4` — fully fixed (header row never changes)

## Cross-Sheet Reference Format

```excel
=INDEX(SheetName!$A$1:$Z$100, ...)
```

Use `!` to reference another sheet. Wrap sheet names with spaces in single quotes:
```excel
=INDEX('Sheet Name'!$A$1:$Z$100, ...)
```

## XLOOKUP Alternative (Excel 365+)

```excel
=XLOOKUP(row_key, row_lookup_range, XLOOKUP(col_key, col_header_range, data_range))
```

For two-dimensional lookup with XLOOKUP (nested):
```excel
=XLOOKUP($D12, Data!$B$21:$B$40, XLOOKUP(H$10, Data!$H$4:$M$4, Data!$H$21:$M$40))
```

## Common Pitfalls

- Always use `0` (exact match) as third argument unless intentional approximate match
- Ensure row lookup range has same length as first dimension of data_range
- Ensure col lookup range has same length as second dimension of data_range
- The `data_range` rows must align with `row_lookup_range`, and cols with `col_lookup_range`

## Setting in Python (openpyxl)

```python
from openpyxl import load_workbook

wb = load_workbook('file.xlsx')
ws = wb['Task']

# Set formula string directly
ws['H12'] = '=INDEX(Data!$H$21:$M$40,MATCH($D12,Data!$B$21:$B$40,0),MATCH(H$10,Data!$H$4:$M$4,0))'
wb.save('file.xlsx')
```
