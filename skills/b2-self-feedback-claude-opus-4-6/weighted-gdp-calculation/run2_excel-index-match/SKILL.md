---
name: run2_excel-index-match
description: INDEX&MATCH for two-condition lookups in Excel, with correct absolute/mixed references for fill-down/fill-right
---

# INDEX & MATCH Two-Condition Lookup

## Formula Pattern
```
=INDEX(data_range, MATCH(row_criteria, row_lookup_range, 0), MATCH(col_criteria, col_lookup_range, 0))
```

## Two-Condition Lookup (series code + year)
Given:
- Data range: `Data!$H$21:$M$40` (all values, absolute)
- Row lookup: `Data!$B$21:$B$40` (series codes, absolute)
- Col lookup: `Data!$H$4:$M$4` (years, absolute)
- Row criteria: `$D12` (series code in Task sheet - lock column, allow row to change)
- Col criteria: `H$9` (year in Task sheet - lock row, allow column to change)

```
=INDEX(Data!$H$21:$M$40, MATCH($D12, Data!$B$21:$B$40, 0), MATCH(H$9, Data!$H$4:$M$4, 0))
```

## Reference Locking Strategy
| Reference | Lock | Why |
|-----------|------|-----|
| `$D12` | Column locked | Series code always in col D; row changes per country |
| `H$9` | Row locked | Year always in row 9; column changes per year |
| Data ranges | Fully absolute | Never changes |

## openpyxl Implementation
```python
from openpyxl import load_workbook
wb = load_workbook('file.xlsx')
ws = wb['Task']

# Fill H12:L17 (and similar ranges) with lookup formulas
for row in range(12, 18):
    for col in ['H', 'I', 'J', 'K', 'L']:
        ws[f'{col}{row}'] = f'=INDEX(Data!$H$21:$M$40,MATCH($D{row},Data!$B$21:$B$40,0),MATCH({col}$9,Data!$H$4:$M$4,0))'
```

## Important Notes
- Skip gap rows between sections (e.g., row 18, 25 if ranges are 12-17, 19-24, 26-31)
- MATCH with 0 = exact match; returns #N/A if not found
- Verify series codes in Task!D column exactly match Data!B column
