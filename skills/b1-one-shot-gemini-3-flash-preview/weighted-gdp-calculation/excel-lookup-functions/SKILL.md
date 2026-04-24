---
name: excel-lookup-functions
description: Covers advanced Excel lookup functions including VLOOKUP, INDEX/MATCH, and XLOOKUP for multi-dimensional data retrieval.
---

# Excel Lookup Functions

This skill covers the use of advanced Excel functions for retrieving data from structured tables based on multiple criteria.

## Key Functions

### 1. VLOOKUP with MATCH (Two-Dimensional Lookup)
When the column index needs to be dynamic (e.g., based on a year in a header row):
`=VLOOKUP(lookup_value, table_array, MATCH(header_value, header_range, 0), FALSE)`

### 2. INDEX and MATCH (Two-Way Lookup)
More flexible than VLOOKUP:
`=INDEX(data_range, MATCH(row_criteria, row_header_range, 0), MATCH(col_criteria, col_header_range, 0))`

### 3. XLOOKUP (Modern Alternative)
Allows for searching both rows and columns:
`=XLOOKUP(lookup_value, lookup_array, return_array)`

## Usage Pattern

For retrieving data based on a series code and a year:
- **Vertical criteria:** Series Code
- **Horizontal criteria:** Year
- **Formula:** `=INDEX(Data!$E$21:$Z$40, MATCH($D12, Data!$D$21:$D$40, 0), MATCH(H$10, Data!$E$10:$Z$10, 0))`

Where `Data!$E$21:$Z$40` is the data matrix, `Data!$D$21:$D$40` contains series codes, and `Data!$E$10:$Z$10` contains years.
