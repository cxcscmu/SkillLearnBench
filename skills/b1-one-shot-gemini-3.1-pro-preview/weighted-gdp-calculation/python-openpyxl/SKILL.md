---
name: python-openpyxl
description: Using openpyxl to read, write, and modify Excel files while preserving formatting and using formulas.
---

# python-openpyxl

`openpyxl` is a Python library to read/write Excel 2010 xlsx/xlsm/xltx/xltm files.

## Installation
```bash
pip install openpyxl
```

## Usage

### Loading a Workbook
```python
import openpyxl

wb = openpyxl.load_workbook("file.xlsx")
sheet = wb["Sheet1"]
```

### Writing Formulas
To write a formula, simply assign it as a string to the cell's value:
```python
sheet["A1"] = "=SUM(B1:B10)"
sheet.cell(row=2, column=1, value="=VLOOKUP(C2, Data!A:Z, 2, FALSE)")
```

### Saving
```python
wb.save("file.xlsx")
```
