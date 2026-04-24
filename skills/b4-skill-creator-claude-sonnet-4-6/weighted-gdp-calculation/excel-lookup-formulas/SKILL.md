---
name: excel-lookup-formulas
description: How to write INDEX&MATCH, VLOOKUP&MATCH, XLOOKUP, and similar two-condition lookup formulas in Excel using openpyxl. Use this skill whenever the user needs to populate data cells using lookup functions that match on two criteria (e.g., series code AND year), especially when pulling cross-sheet data with dynamic row/column matching.
---

# Excel Two-Condition Lookup Formulas

## Overview

When populating a data table from a source sheet using two lookup conditions (e.g., a row identifier like series code AND a column identifier like year), use INDEX&MATCH with two MATCH calls.

## Standard Pattern: INDEX&MATCH with Two Conditions

```excel
=INDEX(Data!$H$21:$M$40, MATCH($D12, Data!$B$21:$B$40, 0), MATCH(H$9, Data!$H$4:$M$4, 0))
```

**How it works:**
- `INDEX(range, row_num, col_num)` — returns value at intersection
- First `MATCH` finds the row: matches series code from Task column D against Data column B
- Second `MATCH` finds the column: matches year from Task row 9 against Data row 4 headers
- `$D12` — dollar-locks the column (D), leaves row relative so it moves down when copied
- `H$9` — dollar-locks the row (9), leaves column relative so it moves right when copied

## Absolute vs Relative References

| Reference | Behavior when copied |
|-----------|---------------------|
| `$D$12` | Never moves |
| `$D12` | Column locked, row moves down |
| `H$9` | Row locked, column moves right |
| `H12` | Both move |

- Use `$D12` for the row lookup key (series code in column D) — column stays, row varies
- Use `H$9` for the column lookup key (year in row 9) — row stays, column varies
- Use `$` on both dimensions for the lookup arrays (source ranges)

## Data Sheet References

When the source data has:
- **Row headers** (series codes) in column B, rows 21–40 → `Data!$B$21:$B$40`
- **Column headers** (years) in row 4, columns H–M → `Data!$H$4:$M$4`
- **Data values** in the body → `Data!$H$21:$M$40`

The year headers in the source (Data sheet row 4) may include one extra year (e.g., 2018) not present in the Task sheet, so MATCH correctly selects the right column.

## Writing Formulas with openpyxl

```python
from openpyxl import load_workbook

wb = load_workbook('file.xlsx')
task = wb['Task']

# Fill a block of cells with the same formula pattern
for row in range(12, 18):   # rows 12–17
    for col in range(8, 13):  # columns H–L (8–12)
        col_letter = task.cell(row=row, column=col).column_letter
        formula = f'=INDEX(Data!$H$21:$M$40,MATCH($D{row},Data!$B$21:$B$40,0),MATCH({col_letter}$9,Data!$H$4:$M$4,0))'
        task.cell(row=row, column=col).value = formula

wb.save('file.xlsx')
```

## Key Rules

1. Always verify which row/column has the lookup keys before writing formulas
2. Use `load_workbook` without `data_only=True` to preserve existing formulas
3. Use `keep_vba=False` (default) unless macros must be preserved
4. After saving, run `recalc.py` to evaluate formulas and check for errors
5. Never hardcode computed values — always write Excel formulas
