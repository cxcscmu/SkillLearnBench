---
name: excel-two-condition-lookups
description: Master two-condition lookups in Excel using INDEX&MATCH, XLOOKUP&MATCH, and HLOOKUP&MATCH. Use this skill whenever working with Excel lookups that require matching on two or more criteria (e.g., finding values based on both a row and column condition, or series code and year).
---

# Two-Condition Lookups in Excel

## Overview

When you need to retrieve data based on two conditions (e.g., matching a series code AND a year), standard VLOOKUP or HLOOKUP won't work. Advanced lookup functions provide elegant solutions.

## Methods

### Method 1: INDEX & MATCH (Most Flexible)

Best for complex scenarios with multiple conditions. Returns the value at the intersection of matched row and column.

**Syntax:**
```
=INDEX(data_range, MATCH(condition1, criteria_range1, 0), MATCH(condition2, criteria_range2, 0))
```

**Example:** Find exports for Country="USA" AND Year=2023
```
=INDEX(B:F, MATCH("USA", A:A, 0), MATCH(2023, 1:1, 0))
```

**How it works:**
- MATCH(condition1, criteria_range1, 0) returns the row number
- MATCH(condition2, criteria_range2, 0) returns the column number
- INDEX uses both numbers to find the exact cell

### Method 2: XLOOKUP & MATCH (Excel 365/2021+)

More modern and readable than INDEX/MATCH.

**Syntax:**
```
=XLOOKUP(lookup_value, lookup_array, XLOOKUP(second_condition, second_array, return_array))
```

Or use nested XLOOKUP:
```
=XLOOKUP(condition1, criteria_range1, INDEX(data_range, , MATCH(condition2, criteria_range2, 0)))
```

**Example:**
```
=XLOOKUP("USA", A:A, INDEX(B:F, , MATCH(2023, 1:1, 0)))
```

### Method 3: HLOOKUP & MATCH (When Looking Across Rows)

Use when your lookup value is in a row header and you're looking across columns.

**Syntax:**
```
=HLOOKUP(condition2, HLOOKUP(condition1, data_array, row_number, FALSE), column_index, FALSE)
```

Or better:
```
=HLOOKUP(year, INDEX(data_range, MATCH(series_code, code_column, 0)), column_in_matched_row, 0)
```

**Example for series code in rows, year in columns:**
```
=HLOOKUP(2023, INDEX(data_range, MATCH("EXP", series_codes, 0)), column_number, 0)
```

## Practical Pattern: Series Code (Row) + Year (Column)

This is common for economic data tables:

```
=INDEX($data_range$,
  MATCH($series_code_cell$, $series_codes_range$, 0),
  MATCH($year_cell$, $years_header_row$, 0))
```

**Example with cell references:**
- Series codes in column A, rows 5-10
- Years in row 3, columns B-F
- Data in B5:F10

```
=INDEX(B5:F10,
  MATCH(D12, A5:A10, 0),
  MATCH(10, B3:F3, 0))
```

Where:
- D12 contains the series code to look up
- Row 10 contains the years to look up
- B5:F10 is the data range

## Tips

1. **Use absolute references** for data ranges (e.g., $B$5:$F$10) so they don't shift when copied
2. **Use mixed references** for lookup values that change (e.g., D12, not $D$12)
3. **0 in MATCH** means exact match; use 1 for approximate match with sorted data
4. **Exact match is usually correct** for this type of lookup (use 0)
5. **Test with a known value first** to verify your ranges are correct

## Error Handling

- **#N/A** means the lookup value wasn't found — check spelling, data type, or if value exists
- **#REF!** means the range reference is invalid
- **#VALUE!** usually means a data type mismatch (text vs number)

## When to Use Each Method

| Method | Best For | Availability |
|--------|----------|--------------|
| INDEX&MATCH | Maximum flexibility, multiple conditions | All versions |
| XLOOKUP&MATCH | Clean, readable formulas | Excel 365/2021+ |
| HLOOKUP&MATCH | Horizontal lookup tables | All versions |
