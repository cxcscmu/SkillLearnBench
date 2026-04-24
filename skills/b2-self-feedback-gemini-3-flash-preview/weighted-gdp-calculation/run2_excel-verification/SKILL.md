---
name: run2_excel-verification
description: Verifying Excel formula results and handling errors using recalc.py and openpyxl.
---

# Verifying Excel Formulas and Results

Always verify the output of Excel modifications to ensure formula correctness and data accuracy.

### Error Checking with recalc.py
After saving the workbook, run `recalc.py` to identify formula errors (e.g., `#NAME?`, `#REF!`, `#DIV/0!`).
- `#NAME?`: Check for incorrect function names (e.g., use `PERCENTILE` instead of `PERCENTILE.INC`).
- `#REF!`: Check for invalid cell references.
- `#DIV/0!`: Check for empty or zero denominators in division.

### Value Verification with openpyxl (data_only=True)
To check the actual values calculated by Excel, reload the workbook with `data_only=True`:

```python
from openpyxl import load_workbook
wb = load_workbook('file.xlsx', data_only=True)
sheet = wb['Task']
print(f"Cell H35 Value: {sheet['H35'].value}")
```

### Manual Verification Formula
Perform a manual calculation to check a sample of cells:
- UAE 2019: `(Exports - Imports) / GDP * 100`
- Bahrain 2019: `(Exports - Imports) / GDP * 100`
- Confirm these match the values in the sheet.
