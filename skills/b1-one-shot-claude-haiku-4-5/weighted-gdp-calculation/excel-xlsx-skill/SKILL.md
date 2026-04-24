---
name: excel-xlsx-skill
description: Use the xlsx skill tool to create, read, modify and analyze Excel spreadsheets with formulas and formatting.
---

# Excel XLSX Skill Tool

## Overview
The `xlsx` skill is used to work with Excel spreadsheets (.xlsx, .xlsm, .csv, .tsv). It supports creating spreadsheets, reading data, modifying cells, adding formulas, and data analysis.

## When to Use
- Creating new spreadsheets from scratch
- Reading or analyzing existing spreadsheet data
- Modifying cells while preserving existing formulas and formatting
- Adding formulas and performing calculations
- Analyzing data and creating visualizations

## Setup
The xlsx skill is built-in and available through the Skill tool. No installation required.

## Usage Patterns

### Reading a Spreadsheet
```
Read the file 'data.xlsx' and understand the structure
Invoke the xlsx skill with operation: read
```

### Modifying Cells
```
To set a formula in a cell:
Use xlsx skill with operation: write_cell
Specify: file path, sheet name, cell reference, value/formula

To modify multiple cells:
Use xlsx skill with operation: batch_write
```

### Working with Formulas
When adding formulas to Excel:
- Use cell references like A1, B2:B10
- Use sheet references like Sheet1!A1
- Formulas start with `=`
- For multi-sheet references: ='SheetName'!CellRef

### Key Functions to Know
- **VLOOKUP**: Lookup values in a vertical table
  `=VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup])`

- **HLOOKUP**: Lookup values in a horizontal table
  `=HLOOKUP(lookup_value, table_array, row_index_num, [range_lookup])`

- **INDEX & MATCH**: More flexible lookup
  `=INDEX(return_array, MATCH(lookup_value, lookup_array, 0))`

- **XLOOKUP**: Modern Excel function (Excel 365+)
  `=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], [search_mode])`

### Statistical Functions
- `=MIN(range)` - Minimum value
- `=MAX(range)` - Maximum value
- `=MEDIAN(range)` - Median value
- `=AVERAGE(range)` - Mean value
- `=PERCENTILE(range, k)` - kth percentile (k as decimal, e.g., 0.25 for 25th)
- `=SUMPRODUCT(array1, array2)` - For weighted calculations

## Best Practices
1. Always preserve existing formatting and colors
2. When using two conditions for lookup, use INDEX/MATCH or XLOOKUP
3. For weighted calculations, SUMPRODUCT is ideal
4. Test formulas with sample data first
5. Round percentage results appropriately (e.g., multiply by 100 for percentage display)

## Example: Two-Condition Lookup
```
=INDEX(data_range, MATCH(1, (condition1_range=criteria1)*(condition2_range=criteria2), 0))
```
Requires array formula (Ctrl+Shift+Enter in some Excel versions).

Alternatively, use XLOOKUP if available:
```
=XLOOKUP(lookup_value, lookup_array, return_array)
```

## Example: Weighted Mean with SUMPRODUCT
```
=SUMPRODUCT(values, weights) / SUM(weights)
```
This multiplies each value by its weight, sums them, and divides by total weights.
