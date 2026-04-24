---
name: excel-two-way-lookup
description: Perform a two-dimensional lookup in Excel to retrieve data based on both a row criteria (e.g., series code) and a column criteria (e.g., year).
---

To retrieve data from a table based on two variables, you can use the `INDEX` and `MATCH` combination or nested `XLOOKUP`.

### INDEX and MATCH (Two-Way)
This is the most robust method for older and newer versions of Excel.
`=INDEX(data_range, MATCH(row_criteria, row_header_range, 0), MATCH(column_criteria, column_header_range, 0))`

*   **data_range**: The grid containing the values you want to extract.
*   **row_criteria**: The specific value to look for in the first column (e.g., Series Code).
*   **MATCH(..., 0)**: Finds the exact position of the criteria.

### XLOOKUP (Nested)
If using modern Excel, you can nest XLOOKUPs:
`=XLOOKUP(row_criteria, row_header_range, XLOOKUP(column_criteria, column_header_range, data_range))`

### Absolute Referencing
When dragging formulas across a range, ensure you use `$` to lock the source data ranges (e.g., `$D$21:$D$40`) while allowing the criteria references (like year or country) to shift appropriately.