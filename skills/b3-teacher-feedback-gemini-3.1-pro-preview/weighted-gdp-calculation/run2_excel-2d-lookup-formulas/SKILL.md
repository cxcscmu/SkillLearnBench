---
name: excel-2d-lookup-formulas
description: How to perform two-dimensional data lookups in Excel using functions like INDEX & MATCH or VLOOKUP & MATCH based on both row and column criteria.
---

# Two-Dimensional Lookups in Excel

When extracting data based on two conditions (e.g., a series code in a row and a year in a column), you must use a combination of lookup formulas.

## 1. INDEX and MATCH (Recommended)
This approach is highly flexible and robust against structural changes in your workbook.

**Syntax:**
`=INDEX(data_range, MATCH(row_criterion, row_lookup_range, 0), MATCH(column_criterion, column_lookup_range, 0))`

**Example Usage:**
If finding a value where the Series Code is in D12 and Year is in H10, from a data sheet:
`=INDEX(Data!$A$1:$Z$100, MATCH($D12, Data!$A$1:$A$100, 0), MATCH(H$10, Data!$A$1:$Z$1, 0))`

## 2. VLOOKUP and MATCH
You can replace the hardcoded column index in VLOOKUP with a MATCH function to find the right column dynamically.

**Syntax:**
`=VLOOKUP(row_criterion, table_range, MATCH(column_criterion, header_range, 0), FALSE)`

**Example Usage:**
`=VLOOKUP($D12, Data!$A$21:$Z$40, MATCH(H$10, Data!$A$20:$Z$20, 0), FALSE)`

## Referencing Best Practices
- **Row Criteria:** Lock the column (e.g., `$D12`) so you can drag the formula across columns.
- **Column Criteria:** Lock the row (e.g., `H$10`) so you can drag the formula down rows.
- **Lookup Ranges:** Use absolute references (e.g., `$A$21:$Z$40`) so the range does not shift when dragging formulas.