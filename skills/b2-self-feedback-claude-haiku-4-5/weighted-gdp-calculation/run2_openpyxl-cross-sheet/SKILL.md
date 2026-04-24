---
name: run2_openpyxl-cross-sheet
description: Using openpyxl to edit Excel workbooks with cross-sheet formulas while preserving all formatting
---

# Editing Excel Workbooks with openpyxl: Cross-Sheet References

## Workflow Overview

1. Load existing workbook with `load_workbook()`
2. Access sheets by name: `wb['SheetName']`
3. Modify specific cells
4. Save the file
5. Recalculate formulas with external tool (e.g., LibreOffice)

## Loading Workbooks

```python
from openpyxl import load_workbook

# Load workbook (preserves ALL formatting, colors, fonts)
wb = load_workbook('file.xlsx')

# Access sheets
task_sheet = wb['Task']
data_sheet = wb['Data']

# List all sheets
sheet_names = wb.sheetnames  # ['Task', 'Data']
```

## Cross-Sheet References in Formulas

### Critical: Use ! Syntax, Not .

When writing cross-sheet references in openpyxl formulas:
- **Use:** `=INDEX(Data!$H$21:$M$40, ...)`  ← Excel/LibreOffice compatible
- **Not:** `=INDEX(Data.$H$21:$M$40, ...)`  ← Causes #NAME? errors

### Correct Sheet Reference Patterns

```python
# Two-condition lookup with cross-sheet reference
formula = "=INDEX(Data!$H$21:$M$40, MATCH($D12, Data!$B$21:$B$40, 0), MATCH(H$9, Data!$H$4:$M$4, 0))"

# Aggregate calculation
formula = "=(SUM(Data!$H$12:$H$17) - SUM(Data!$H$19:$H$24)) / SUM(Data!$H$26:$H$31) * 100"

# Statistical function
formula = "=ROUND(MIN(Data!$H$35:$H$40), 1)"
```

## Cell Reference Anchoring

### Copying Formulas with Mixed References
Use `$` selectively so references adjust correctly when copying:

```python
# Row absolute, column relative - changes column when copying right
formula = f"=INDEX(Data!$H$21:$M$40, MATCH($D{row}, Data!$B$21:$B$40, 0), MATCH({col_letter}$9, Data!$H$4:$M$4, 0))"
```

When copied:
- Right (H → I): `H$9` becomes `I$9` ✓
- Down (12 → 13): `$D12` becomes `$D13` ✓

## Setting Formulas in openpyxl

```python
# Direct cell assignment
sheet['H12'] = "=INDEX(Data!$H$21:$M$40, MATCH($D12, Data!$B$21:$B$40, 0), MATCH(H$9, Data!$H$4:$M$4, 0))"

# Using cell object (equivalent)
sheet.cell(row=12, column=8).value = "=INDEX(...)"

# Multi-cell loop
for row in range(12, 18):
    for col in range(8, 13):  # H-L
        col_letter = chr(64 + col)
        formula = f"=SUM({col_letter}12:{col_letter}17)"
        sheet[f'{col_letter}{row}'] = formula
```

## Formatting Preservation

### Automatic Preservation
openpyxl automatically preserves when loading and saving:
- Cell colors and fill patterns (including yellow background)
- Font styles and colors (including blue text)
- Cell borders and alignment
- Number formatting
- Merged cells

```python
# Formatting is preserved automatically
sheet['H12'] = formula  # Yellow background stays yellow
sheet['D9'] = value    # Blue font stays blue
```

### Checking Cell Properties

```python
cell = sheet['H12']
print(cell.fill.start_color.rgb)    # 'FFFFFF00' for yellow
print(cell.font.color.rgb)          # 'FF0000FF' for blue
print(cell.number_format)           # e.g., '0.0' for 1 decimal
```

## Saving and Recalculating

### Save Changes
```python
wb.save('file.xlsx')
```

### Recalculate Formulas
openpyxl stores formulas as strings but doesn't calculate them. Use external tool:

```bash
# Use LibreOffice to recalculate
python3 recalc.py file.xlsx

# Expected output:
# {
#   "status": "success",
#   "total_formulas": 150,
#   "total_errors": 0
# }
```

## Handling Errors After Recalculation

### Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| #NAME? | Sheet reference wrong (using `.` instead of `!`) | Change `Data.$H$21` to `Data!$H$21` |
| #REF! | Invalid cell reference | Verify range exists and sheet name is correct |
| #N/A | Value not found in MATCH | Check criteria matches data exactly |
| #DIV/0! | Division by zero | Add error handling: `=IFERROR(formula, 0)` |

## Python Script Pattern

```python
from openpyxl import load_workbook

wb = load_workbook('gdp.xlsx')
task = wb['Task']

# Fill lookup formulas
for row in range(12, 18):
    for col in range(8, 13):  # H-L
        col_letter = chr(64 + col)
        formula = f"=INDEX(Data!$H$21:$M$40, MATCH($D{row}, Data!$B$21:$B$40, 0), MATCH({col_letter}$9, Data!$H$4:$M$4, 0))"
        task[f'{col_letter}{row}'] = formula

# Fill calculation formulas
for col in range(8, 13):
    col_letter = chr(64 + col)
    task[f'{col_letter}42'] = f"=ROUND(MIN({col_letter}35:{col_letter}40), 1)"
    task[f'{col_letter}50'] = f"=ROUND((SUM({col_letter}12:{col_letter}17)-SUM({col_letter}19:{col_letter}24))/SUM({col_letter}26:{col_letter}31)*100, 1)"

wb.save('gdp.xlsx')
```

## Performance Tips

- **Batch operations**: Loop through ranges instead of individual cells
- **Avoid data_only=True during edit**: It replaces formulas with values permanently
- **Use cell coordinates**: A1, H12, L40 notation is clearer than row/column numbers
- **Verify before save**: Print a few cells to confirm formulas are correct
