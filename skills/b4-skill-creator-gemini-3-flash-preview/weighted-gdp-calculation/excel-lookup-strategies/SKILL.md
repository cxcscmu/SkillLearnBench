# excel-lookup-strategies

How to use VLOOKUP, INDEX/MATCH, and XLOOKUP for two-way lookups. Use this skill whenever the user asks to populate data from one sheet to another based on multiple conditions like row headers and column headers.

## Two-Way Lookup with INDEX/MATCH
This is the most flexible way to perform a lookup when you need to match both a row and a column.

**Formula Template:**
`=INDEX(Data_Range, MATCH(Row_Criteria, Row_Header_Range, 0), MATCH(Column_Criteria, Column_Header_Range, 0))`

- `Data_Range`: The block of cells containing the values you want to retrieve.
- `Row_Criteria`: The value to look for in the rows (e.g., a Series Code).
- `Row_Header_Range`: The single column in the source sheet containing the row identifiers.
- `Column_Criteria`: The value to look for in the columns (e.g., a Year).
- `Column_Header_Range`: The single row in the source sheet containing the column identifiers.

## Two-Way Lookup with XLOOKUP
Available in modern Excel, XLOOKUP is more intuitive.

**Formula Template:**
`=XLOOKUP(Row_Criteria, Row_Header_Range, XLOOKUP(Column_Criteria, Column_Header_Range, Data_Range))`

## Two-Way Lookup with VLOOKUP/MATCH
Useful when the data is structured with the lookup key in the leftmost column.

**Formula Template:**
`=VLOOKUP(Row_Criteria, Full_Table_Range, MATCH(Column_Criteria, Column_Header_Range, 0), FALSE)`

- Note: `Column_Header_Range` must start from the same column as `Full_Table_Range`.

## Handling Absolute References
When dragging formulas across a range:
- Use `$` to lock references.
- Lock the criteria's column for row matching: `$D12`.
- Lock the criteria's row for column matching: `H$10`.
- Always lock the source data ranges: `Data!$B$5:$M$40`.
