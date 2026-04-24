---
name: openpyxl-formula-editing
description: Editing existing Excel files with openpyxl while preserving formatting and adding formulas.
---

# Editing Excel Files with openpyxl (Preserve Formatting)

## Load and Edit
```python
from openpyxl import load_workbook

wb = load_workbook('file.xlsx')
ws = wb['SheetName']

# Write formula to a cell (preserves existing formatting)
ws['H12'] = '=SOME_FORMULA()'

# Iterate over a range
for row in range(12, 18):
    for col_letter in ['H', 'I', 'J', 'K', 'L']:
        ws[f'{col_letter}{row}'] = f'=FORMULA({col_letter}...)'

wb.save('file.xlsx')
```

## Important Notes
- Assigning a value to a cell preserves its existing formatting (fill, font, borders)
- Formulas are stored as strings starting with '='
- Use `recalc.py` after saving to compute formula values
- Never open with `data_only=True` if you plan to save (destroys formulas)
