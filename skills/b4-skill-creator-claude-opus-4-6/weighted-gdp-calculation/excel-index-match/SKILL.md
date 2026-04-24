---
name: excel-index-match
description: >
  How to use INDEX&MATCH for two-dimensional lookups in Excel via openpyxl.
  Use this skill whenever building Excel formulas that look up values by matching
  both a row criterion and a column criterion from a data table — e.g., matching
  a series code (row) and a year (column). Trigger when the user mentions
  VLOOKUP&MATCH, HLOOKUP&MATCH, XLOOKUP&MATCH, INDEX&MATCH, or two-condition lookups.
---

# INDEX & MATCH Two-Dimensional Lookup in Excel

## When to Use
Use INDEX(range, MATCH(...), MATCH(...)) when you need to retrieve a value from
a rectangular data range using two criteria — one to identify the row and one to
identify the column.

## Formula Pattern

```
=INDEX(data_range, MATCH(row_criterion, row_lookup_range, 0), MATCH(col_criterion, col_lookup_range, 0))
```

### Components
| Part | Purpose |
|------|---------|
| `data_range` | The rectangular block of values (e.g., `Data!H21:M40`) |
| `row_criterion` | The value to match in the row dimension (e.g., a series code in `$D12`) |
| `row_lookup_range` | A single column containing the row keys (e.g., `Data!$B$21:$B$40`) |
| `col_criterion` | The value to match in the column dimension (e.g., a year in `H$9`) |
| `col_lookup_range` | A single row containing the column keys (e.g., `Data!$H$4:$M$4`) |
| `0` | Exact match |

### Locking References
- Lock the **row criterion column** with `$D12` (absolute column, relative row) so it adjusts when copied down but not across.
- Lock the **col criterion row** with `H$9` (relative column, absolute row) so it adjusts when copied across but not down.
- Lock lookup ranges with `$` on both dimensions since they never move.

## Example in openpyxl

```python
from openpyxl import load_workbook

wb = load_workbook('file.xlsx')
ws = wb['Task']

# Fill a grid of lookup cells
for row in range(12, 18):          # rows 12-17
    for col_idx, col_letter in enumerate(['H','I','J','K','L']):
        formula = (
            f"=INDEX(Data!$H$21:$M$40,"
            f"MATCH($D{row},Data!$B$21:$B$40,0),"
            f"MATCH({col_letter}$9,Data!$H$4:$M$4,0))"
        )
        ws[f'{col_letter}{row}'] = formula

wb.save('file.xlsx')
```

## Common Pitfalls
- Ensure the data_range, row_lookup_range, and col_lookup_range all span the same rows/columns of the source data.
- Use absolute references (`$`) on ranges that should not shift when the formula is copied.
- The third argument `0` in MATCH means exact match — omitting it defaults to approximate match, which requires sorted data.
