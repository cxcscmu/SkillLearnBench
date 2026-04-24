---
name: run2_excel-lookup
description: How to perform a two-dimensional lookup in Excel using either INDEX/MATCH or VLOOKUP/MATCH.
---

# Advanced Excel Lookups

When dealing with a matrix of data (e.g., country rows and year columns), you must look up data using both vertical and horizontal criteria.

## Option 1: INDEX & MATCH
This is the most flexible approach.
```excel
=INDEX(Data!$A$21:$Z$40, MATCH($D12, Data!$B$21:$B$40, 0), MATCH(H$9, Data!$A$4:$Z$4, 0))
```
- `Data!$A$21:$Z$40`: The full grid to return a value from.
- First `MATCH`: Finds the relative row by matching the code in column B.
- Second `MATCH`: Finds the relative column by matching the year in row 4.
