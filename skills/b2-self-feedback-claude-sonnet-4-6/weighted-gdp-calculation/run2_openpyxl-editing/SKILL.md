---
name: run2_openpyxl-editing
description: Safely insert Excel formulas into specific cells using openpyxl without altering formatting, colors, or structure of existing workbooks.
---

# openpyxl: Safe Formula Insertion into Existing Excel Files

## Critical Rules
1. **NEVER use `data_only=True` when loading to modify** — it strips formulas; re-saving destroys them permanently
2. **NEVER overwrite with a fresh Workbook** — always load and modify in place
3. **Only set `.value`** — don't touch `.font`, `.fill`, `.border`, `.number_format` unless explicitly required

## Load and Save Pattern
```python
from openpyxl import load_workbook

wb = load_workbook('/path/to/file.xlsx')  # NO data_only=True
task = wb['Task']
data = wb['Data']

# Write formulas
task['H12'] = '=INDEX(Data!$H$21:$M$40,MATCH($D12,Data!$B$21:$B$40,0),MATCH(H$9,Data!$H$4:$M$4,0))'

wb.save('/path/to/file.xlsx')
```

## Verify After Saving (using data_only=True read-back)
```python
wb_check = load_workbook('/path/to/file.xlsx', data_only=True)
task_check = wb_check['Task']
print(task_check['H12'].value)  # Shows cached value (only valid after recalc.py)
```

## Recalculation (Mandatory)
openpyxl writes formula strings but does NOT compute values. Use recalc.py:
```bash
python3 /path/to/recalc.py /path/to/file.xlsx 60
```
Returns JSON:
```json
{"status": "success", "total_errors": 0, "total_formulas": 213}
```
If `status` is `"errors_found"`, check `error_summary` for locations and types.

## Cross-Sheet References in Formulas
```python
# Correct format for cross-sheet formula
task['H12'] = '=INDEX(Data!$H$21:$M$40, ...)'

# For sheet names with spaces, use single quotes
task['A1'] = "=INDEX('Sheet Name'!$A$1:$B$10, 1, 1)"
```

## Iterating Columns A-Z
```python
cols = ['H', 'I', 'J', 'K', 'L']  # Named columns (preferred for clarity)
# OR
from openpyxl.utils import get_column_letter
cols = [get_column_letter(i) for i in range(8, 13)]  # H through L
```

## Pre-flight Checks (Before Writing)
```python
# Check what's already there before overwriting
for row in task.iter_rows(min_row=12, max_row=17, min_col=8, max_col=12):
    for cell in row:
        print(f'{cell.coordinate}: {cell.value}')
```

## Common Mistakes
| Mistake | Fix |
|---------|-----|
| Using `=` prefix but wrong sheet name | Check `wb.sheetnames` |
| Formula works but value shows `None` | Run recalc.py first |
| Number shows as `0.123` not `12.3` | Multiply by 100 inside formula |
| `#N/A` error | Series code mismatch — check exact string values |
| `#REF!` error | Row/column references out of range |
