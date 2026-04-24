---
name: run2_excel-index-match
description: Use INDEX&MATCH with two conditions (series code + year) to populate data tables in Excel from a source sheet, with proper anchoring for copyable formulas.
---

# Excel INDEX & MATCH: Two-Condition Lookup (Series Code + Year)

## Formula Pattern for This Task
```excel
=INDEX(Data!$H$21:$M$40, MATCH($D12, Data!$B$21:$B$40, 0), MATCH(H$9, Data!$H$4:$M$4, 0))
```

### Breakdown
| Part | Purpose |
|------|---------|
| `Data!$H$21:$M$40` | Source data range (fully anchored — never moves) |
| `MATCH($D12, Data!$B$21:$B$40, 0)` | Find row by series code; `$D` anchors column D, row 12 moves |
| `MATCH(H$9, Data!$H$4:$M$4, 0)` | Find column by year; `H` moves across years, `$9` anchors row 9 |

### Dollar Sign Rules (Critical for Copy-Down/Copy-Across)
- `$D12` — lock column D (series codes), let row vary as you copy down
- `H$9` — let column vary as you copy right (year moves), lock row 9 (year header)
- `Data!$H$21:$M$40` — fully lock the data range

## Key Observations About the Data Structure
- **Data sheet rows 21-40**: Contains all 3 data types (Exports rows 21-26, gap at 27, Imports rows 28-33, gap at 34, GDP rows 35-40)
- **Using the FULL range** (`$B$21:$B$40` and `$H$21:$M$40`) works for all three sections since series codes are unique across the entire range
- **No need to specify sub-ranges** per data type — one formula works for all of H12:L17, H19:L24, H26:L31

## Data Sheet Key Coordinates
- Series codes: `Data!$B$21:$B$40` (column B)
- Year headers: `Data!$H$4:$M$4` (row 4, years 2018–2023)
- Data values: `Data!$H$21:$M$40` (the intersection)

## Task Sheet Key Coordinates
- Series codes (lookup keys): Column D (D12, D19, D26, etc.)
- Year headers (lookup keys): Row 9 (H9=2019, I9=2020, ..., L9=2023)
- Yellow cells to fill:
  - `H12:L17` — Exports
  - `H19:L24` — Imports
  - `H26:L31` — GDP

## openpyxl Implementation
```python
cols = ['H', 'I', 'J', 'K', 'L']

for row in range(12, 18):  # also 19-24 and 26-31
    for col in cols:
        task[f'{col}{row}'] = (
            f'=INDEX(Data!$H$21:$M$40,'
            f'MATCH($D{row},Data!$B$21:$B$40,0),'
            f'MATCH({col}$9,Data!$H$4:$M$4,0))'
        )
```

## Validation
Verify formula results:
- UAE Exports 2019 should be ≈ 404.05 billion (matches Data!I26)
- Bahrain GDP 2023 should be ≈ 44.67 billion (matches Data!M35)
