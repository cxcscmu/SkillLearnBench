---
name: run2_xlsx-analysis
description: Improved Excel data analysis and formula manipulation using openpyxl.
---

### Usage
- Use openpyxl.load_workbook('file.xlsx') to work with formulas.
- Use sheet.cell(row=R, column=C).number_format to set format.
- Use sheet.cell(row=R, column=C).value = '=Formula' for calculations.
- Use recalc.py to evaluate formulas after changes.
- Handle potential compatibility issues (e.g. PERCENTILE vs PERCENTILE.INC).
