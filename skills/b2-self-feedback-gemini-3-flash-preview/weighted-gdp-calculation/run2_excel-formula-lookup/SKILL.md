---
name: run2_excel-formula-lookup
description: Advanced two-condition lookups in Excel using INDEX and MATCH with sheet-specific references in openpyxl.
---

# Excel Cross-Sheet Two-Condition Lookup (INDEX-MATCH-MATCH)

When looking up values from a different sheet (e.g., `Data`) based on a unique identifier (e.g., Series Code) and a secondary criterion (e.g., Year), use the `INDEX-MATCH-MATCH` pattern for maximum flexibility.

### Formula Pattern
`=INDEX(Data!$A:$Z, MATCH($IdentifierCol, Data!$IdentifierRange, 0), MATCH(HeaderRow, Data!$HeaderRange, 0))`

- `Data!$A:$Z`: The entire data range on the source sheet.
- `MATCH($IdentifierCol, Data!$IdentifierRange, 0)`: Finds the row by matching a unique code (e.g., `$D12`) in the source's identifier column (e.g., `Data!$B:$B`).
- `MATCH(HeaderRow, Data!$HeaderRange, 0)`: Finds the column by matching a header (e.g., `H$9`) in the source's header row (e.g., `Data!$4:$4`).

### openpyxl Implementation Details
- Always use absolute references (`$`) for source ranges in formulas that will be copied across many cells.
- Use mixed references for inputs: `$D12` (locked column, relative row) and `H$9` (relative column, locked row).
- Verify the header row on both sheets to ensure the criteria match (e.g., strings vs. numbers).

```python
# H12 in Task sheet
task['H12'] = '=INDEX(Data!$A:$Z, MATCH($D12, Data!$B:$B, 0), MATCH(H$9, Data!$4:$4, 0))'
```
