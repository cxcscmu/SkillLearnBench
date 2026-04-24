---
name: excel-index-match
description: Using INDEX/MATCH formulas in Excel for two-condition lookups across sheets.
---

# INDEX & MATCH for Two-Condition Lookups in Excel

## Pattern: Cross-Sheet Lookup with Two Criteria

When you need to look up a value using both a row identifier and a column identifier (e.g., series code + year), use INDEX/MATCH:

```
=INDEX(DataRange, MATCH(RowCriteria, RowLookupRange, 0), MATCH(ColCriteria, ColLookupRange, 0))
```

### Example
Given a Data sheet with series codes in column B and years in row 4:
```
=INDEX(Data!$H$21:$M$40, MATCH($D12, Data!$B$21:$B$40, 0), MATCH(H$9, Data!$H$4:$M$4, 0))
```

### Key Points
- Use `$` to lock ranges that shouldn't shift when copying formulas
- Lock row criteria column with `$D12` (column locked, row relative)
- Lock year row with `H$9` (column relative, row locked)
- The third argument `0` means exact match
- INDEX range and MATCH ranges must align (same rows/columns)

### Openpyxl Implementation
```python
# When writing INDEX/MATCH formulas via openpyxl, use string assignment:
ws['H12'] = '=INDEX(Data!$H$21:$M$40,MATCH($D12,Data!$B$21:$B$40,0),MATCH(H$9,Data!$H$4:$M$4,0))'
```
