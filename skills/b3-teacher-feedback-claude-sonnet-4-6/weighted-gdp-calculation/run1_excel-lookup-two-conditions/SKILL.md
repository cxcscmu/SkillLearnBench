---
name: excel-lookup-two-conditions
description: Use when you need to retrieve data from a table using two simultaneous conditions (e.g., row label + column header). Covers INDEX&MATCH, XLOOKUP&MATCH, VLOOKUP&MATCH, and HLOOKUP&MATCH patterns in Excel.
---

## Two-Condition Lookups in Excel

When data is organized in a 2D table (rows = one dimension, columns = another), you need to match both a row key and a column key to extract a value.

### INDEX & MATCH (most flexible, works in all Excel versions)

```excel
=INDEX(data_range, MATCH(row_key, row_headers, 0), MATCH(col_key, col_headers, 0))
```

**Example:** Retrieve value where Series Code = D12 and Year = 2020:
```excel
=INDEX(Data!$E$21:$I$40, MATCH($D12, Data!$D$21:$D$40, 0), MATCH(H$10, Data!$E$20:$I$20, 0))
```

- `MATCH(row_key, ..., 0)` — finds the row position of the series code
- `MATCH(col_key, ..., 0)` — finds the column position of the year
- `INDEX(array, row, col)` — returns the value at that intersection

**Key tips:**
- Lock the data array with `$` on both row and column (`$E$21:$I$40`)
- Lock the row-key column reference (`$D12`) so it doesn't shift horizontally when copying across columns
- Lock the col-key row reference (`H$10`) so it doesn't shift vertically when copying down rows
- Use `0` as the third argument to MATCH for exact matching

### XLOOKUP & MATCH (Excel 365 / 2021+)

```excel
=XLOOKUP(row_key, row_key_range, XLOOKUP(col_key, col_key_range, data_array))
```

Or with MATCH:
```excel
=XLOOKUP(row_key, row_key_range, INDEX(data_array, 0, MATCH(col_key, col_headers, 0)))
```

### VLOOKUP & MATCH

```excel
=VLOOKUP(row_key, lookup_table, MATCH(col_key, col_headers, 0), 0)
```

- `MATCH` dynamically returns the column number for VLOOKUP
- `lookup_table` must start from the row_key column
- Less flexible than INDEX&MATCH because it can only look right

### HLOOKUP & MATCH

```excel
=HLOOKUP(col_key, lookup_table, MATCH(row_key, row_keys, 0), 0)
```

- `lookup_table` must start from the col_key row
- `MATCH` returns the row number dynamically

### Copying Formulas Across Ranges

When filling a rectangular range like H12:L17:
- The **row condition** (series code) is in a column (e.g., D12) → lock the column: `$D12`
- The **column condition** (year) is in a row (e.g., H10) → lock the row: `H$10`
- This allows the formula to be dragged both right and down correctly