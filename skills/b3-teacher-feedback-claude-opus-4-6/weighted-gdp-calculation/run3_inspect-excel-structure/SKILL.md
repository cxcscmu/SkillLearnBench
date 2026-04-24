---
name: inspect-excel-structure
description: How to inspect the structure of an Excel workbook before writing formulas, including checking sheet names, cell values, data types, and layout. Use this whenever you need to understand the actual content of an Excel file before modifying it.
---

# Inspecting Excel Workbook Structure

Before writing any formulas into an Excel file, you MUST inspect the actual structure of both sheets. Never assume row/column positions.

## Step-by-step inspection with openpyxl

```python
import openpyxl

wb = openpyxl.load_workbook('gdp.xlsx', data_only=True)
print("Sheet names:", wb.sheetnames)

# Inspect the Data sheet thoroughly
ds = wb['Data']
print(f"Data sheet dimensions: {ds.min_row}-{ds.max_row} rows, {ds.min_column}-{ds.max_column} cols")

# Print ALL rows in the Data sheet (rows 1 through max), showing first 20 columns
print("\n=== DATA SHEET FULL DUMP ===")
for row in ds.iter_rows(min_row=1, max_row=ds.max_row, min_col=1, max_col=min(20, ds.max_column), values_only=False):
    row_num = row[0].row
    vals = [(cell.column_letter, cell.value) for cell in row]
    print(f"Row {row_num}: {vals}")

# Inspect the Task sheet thoroughly
ts = wb['Task']
print(f"\nTask sheet dimensions: {ts.min_row}-{ts.max_row} rows, {ts.min_column}-{ts.max_column} cols")

print("\n=== TASK SHEET FULL DUMP ===")
for row in ts.iter_rows(min_row=1, max_row=ts.max_row, min_col=1, max_col=min(20, ts.max_column), values_only=False):
    row_num = row[0].row
    vals = [(cell.column_letter, cell.value) for cell in row]
    print(f"Row {row_num}: {vals}")
```

## Key things to check

1. **Header row in Data sheet**: Which row contains year headers? What column do they start in? Are years stored as numbers (2019) or text ("2019")?
2. **Data rows 21-40 in Data sheet**: What columns contain country names, series codes, and numeric values?
3. **Task sheet row 10**: What are the year values? Are they numbers or text?
4. **Task sheet column D**: What series codes are listed? Do they exactly match the Data sheet?
5. **Task sheet yellow cell ranges**: What rows/columns correspond to H12:L17, H19:L24, H26:L31, H35:L40?
6. **Country names/identifiers**: Where do country names appear in the Task sheet vs the Data sheet? Are they identical strings?

## Check data types explicitly

```python
# Check type of year values in both sheets
for cell in ts[10]:  # Task sheet row 10
    if cell.value is not None:
        print(f"Task row 10 col {cell.column_letter}: value={cell.value!r}, type={type(cell.value).__name__}")

# Check years in Data sheet header row (find it first)
for row_num in range(1, 5):
    for cell in ds[row_num]:
        if cell.value is not None:
            print(f"Data row {row_num} col {cell.column_letter}: value={cell.value!r}, type={type(cell.value).__name__}")
```

## Important: Run inspection BEFORE writing any formulas
Never skip this step. The actual file structure determines everything about formula construction.