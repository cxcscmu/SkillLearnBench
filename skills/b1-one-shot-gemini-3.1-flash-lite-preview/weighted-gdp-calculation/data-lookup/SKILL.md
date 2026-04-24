---
name: data-lookup
description: Advanced data retrieval in Excel using INDEX and MATCH.
---

### INDEX & MATCH
For a two-dimensional look-up, use `INDEX` combined with two `MATCH` functions.
Syntax: `=INDEX(data_array, MATCH(row_value, row_range, 0), MATCH(column_value, column_range, 0))`

- `data_array`: The range containing the data.
- `row_range`: The range containing the row headers.
- `column_range`: The range containing the column headers.
- The `0` argument ensures an exact match.
