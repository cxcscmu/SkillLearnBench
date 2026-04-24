---
name: run2_multi-condition-lookups
description: Implementing two-condition lookups in Excel using INDEX/MATCH with proper sheet references
---

# Multi-Condition Lookups: INDEX/MATCH in Excel

## When to Use

Use INDEX/MATCH when you need to:
- Look up data based on TWO OR MORE criteria (e.g., series code AND year)
- Work with data in any row/column order (unlike VLOOKUP/HLOOKUP which require specific ordering)
- Reference cells/ranges from other sheets in the same workbook

## Cross-Sheet Reference Syntax

### Critical: Use ! for Sheet References (Not .)
Excel and LibreOffice Calc require different syntax for cross-sheet references:
- **Excel syntax**: `Sheet!Cell` or `Sheet!Range`
- **LibreOffice Calc**: Also supports `Sheet!Range` (Excel compatible)
- **DO NOT use**: `Sheet.Cell` or `Sheet.$H$21` (these cause #NAME? errors in LibreOffice)

**Correct:** `=INDEX(Data!$H$21:$M$40, MATCH(...), MATCH(...))`
**Wrong:** `=INDEX(Data.$H$21:$M$40, MATCH(...), MATCH(...))`

## Two-Condition INDEX/MATCH Formula

### Structure
```
=INDEX(data_range,
  MATCH(row_criteria, row_lookup_range, 0),
  MATCH(col_criteria, col_lookup_range, 0)
)
```

### Parameters
- **data_range**: The 2D range containing the values to return (e.g., `Data!$H$21:$M$40`)
- **row_criteria**: The value to match in rows (e.g., `$D12` for series code)
- **row_lookup_range**: Column containing row criteria (e.g., `Data!$B$21:$B$40`)
- **col_criteria**: The value to match in columns (e.g., `H$9` for year)
- **col_lookup_range**: Row containing column criteria (e.g., `Data!$H$4:$M$4`)
- **0**: Exact match (required for lookups)

### Example: Lookup Exports by Series Code and Year
```
=INDEX(Data!$H$21:$M$40,
  MATCH($D12, Data!$B$21:$B$40, 0),
  MATCH(H$9, Data!$H$4:$M$4, 0)
)
```

## Cell Reference Anchoring

### Absolute vs. Mixed References
- **$column$row**: Absolute - never changes when copying
- **column$row**: Column relative, row absolute - column changes when copying right
- **$columnrow**: Column absolute, row relative - row changes when copying down
- **columnrow**: Both relative - both change when copying

### Pattern for 2D Data Lookups
```
=INDEX(Data!$H$21:$M$40,        # Absolute data range
  MATCH($D12, Data!$B$21:$B$40, 0),   # Row criteria absolute, lookup range absolute
  MATCH(H$9, Data!$H$4:$M$4, 0)      # Column criteria absolute, lookup range absolute
)
```

When copying:
- Down: Row number in criteria changes ($D12 → $D13)
- Right: Column letter in criteria changes (H$9 → I$9)

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| #NAME? | Wrong sheet reference syntax (using .) | Change `Sheet.Cell` to `Sheet!Cell` |
| #REF! | Invalid range reference | Verify sheet name and ranges exist |
| #N/A | Criteria not found in lookup range | Check criteria value matches exactly |
| #VALUE! | Wrong data type in criteria | Ensure criteria matches lookup data type |

## Alternative Functions

- **XLOOKUP** (Excel 365+): Simpler syntax, more flexible
- **VLOOKUP/HLOOKUP**: Simpler but requires data in specific order
- **LOOKUP**: Less flexible but works across both rows and columns
