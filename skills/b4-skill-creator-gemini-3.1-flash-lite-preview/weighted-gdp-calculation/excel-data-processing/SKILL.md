---
name: excel-data-processing
description: How to perform data lookups in Excel using INDEX and MATCH. Use this skill when needing to extract data from a source table based on two conditions (e.g., Row header and Column header).
---

# Excel Data Processing: INDEX & MATCH

Use the following pattern to perform a 2D lookup:

`=INDEX(data_range, MATCH(row_lookup, row_range, 0), MATCH(col_lookup, col_range, 0))`

- **data_range**: The grid containing the source data.
- **row_lookup**: The criteria for the row (e.g., Series Code).
- **row_range**: The column header or range containing the series codes.
- **col_lookup**: The criteria for the column (e.g., Year).
- **col_range**: The row header or range containing the years.

Ensure all ranges are locked using `$` signs (e.g., `$D$21:$Z$40`) when referencing fixed data tables.
