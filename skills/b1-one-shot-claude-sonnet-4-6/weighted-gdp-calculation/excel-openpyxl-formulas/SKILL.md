---
name: excel-openpyxl-formulas
description: Editing Excel files with openpyxl to insert formulas while preserving all existing formatting, styles, colors, and structure.
---

# openpyxl: Insert Formulas While Preserving Formatting

## Critical Rule: Load Without data_only

```python
from openpyxl import load_workbook

# CORRECT: preserves formulas and formatting
wb = load_workbook('file.xlsx')

# WRONG: replaces formulas with cached values on save
wb = load_workbook('file.xlsx', data_only=True)
```

## Basic Formula Insertion

```python
wb = load_workbook('file.xlsx')
ws = wb['Sheet1']

ws['H12'] = '=INDEX(Data!$H$21:$M$40,MATCH($D12,Data!$B$21:$B$40,0),MATCH(H$10,Data!$H$4:$M$4,0))'

wb.save('file.xlsx')
```

## Iterating Over Cell Ranges

When applying similar formulas to a grid of cells, iterate using row/column indices:

```python
from openpyxl.utils import get_column_letter

# Fill a range (e.g., H12:L17) with formulas
start_row = 12
end_row = 17
start_col = 8   # H = column 8
end_col = 12    # L = column 12

for row in range(start_row, end_row + 1):
    for col in range(start_col, end_col + 1):
        col_letter = get_column_letter(col)
        cell = ws.cell(row=row, column=col)
        cell.value = f'=INDEX(Data!$I$21:$M$40,MATCH($D{row},Data!$B$21:$B$40,0),MATCH({col_letter}$10,Data!$I$4:$M$4,0))'
```

## Preserving Cell Formatting

openpyxl preserves existing cell styles when you only change `value`. Setting a new value does NOT erase fill color, font, borders, etc.:

```python
cell = ws['H12']
cell.value = '=SUM(A1:A10)'  # Only changes the value; style is preserved
```

## Row and Column Reference Conversion

```python
from openpyxl.utils import get_column_letter, column_index_from_string

get_column_letter(8)    # → 'H'
get_column_letter(12)   # → 'L'
column_index_from_string('H')  # → 8
column_index_from_string('L')  # → 12
```

## Recalculating Formulas After Editing

After saving, run recalc.py to update cached formula values:

```bash
python recalc.py file.xlsx
```

Check output for errors:
```json
{"status": "success", "total_errors": 0, "total_formulas": 42}
```

If errors found:
```json
{"status": "errors_found", "error_summary": {"#REF!": {"count": 2, "locations": ["Task!H12"]}}}
```

## Full Pattern for Multi-Range Formula Insertion

```python
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

wb = load_workbook('gdp.xlsx')
ws = wb['Task']

# Fill H12:L17 with INDEX&MATCH formulas
for row in range(12, 18):
    for col in range(8, 13):  # H=8 to L=12
        col_letter = get_column_letter(col)
        formula = f'=INDEX(Data!$I$21:$M$40,MATCH($D{row},Data!$B$21:$B$40,0),MATCH({col_letter}$10,Data!$I$4:$M$4,0))'
        ws.cell(row=row, column=col).value = formula

wb.save('gdp.xlsx')
```

## Verifying Column Mapping Before Writing

Always verify your column letter → index mapping:
- A=1, B=2, ..., H=8, I=9, J=10, K=11, L=12, M=13

Excel rows are 1-indexed; openpyxl uses the same 1-based indexing.
Pandas DataFrames use 0-based indexing, so Excel row N = pandas row N-1.
