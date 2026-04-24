---
name: excel-weighted-statistics
description: How to calculate weighted means, net export percentages, and statistical summaries (min, max, median, mean, percentiles) in Excel using SUMPRODUCT, ROUND, PERCENTILE, and other functions. Use this skill whenever the user needs GDP-weighted averages, trade statistics as percent of GDP, or descriptive statistics across a cross-section of countries or entities.
---

# Excel Weighted Statistics and Economic Calculations

## Net Exports as Percent of GDP

Net exports = Exports − Imports. As a percent of GDP, multiply by 100 to show in percentage-point form (e.g., 12.3 not 0.123):

```excel
=ROUND((Exports - Imports) / GDP * 100, 1)
```

**Example for one country (row 35, year column H):**
```excel
=ROUND((H12-H19)/H26*100, 1)
```

When copying this formula across rows and columns, use purely relative references so both dimensions adjust automatically.

## Statistical Summary Formulas (per column/year)

Given net export percentages in H35:H40 (six countries for one year):

| Statistic | Formula |
|-----------|---------|
| Min | `=ROUND(MIN(H35:H40), 1)` |
| Max | `=ROUND(MAX(H35:H40), 1)` |
| Median | `=ROUND(MEDIAN(H35:H40), 1)` |
| Simple mean | `=ROUND(AVERAGE(H35:H40), 1)` |
| 25th percentile | `=ROUND(PERCENTILE(H35:H40, 0.25), 1)` |
| 75th percentile | `=ROUND(PERCENTILE(H35:H40, 0.75), 1)` |

Lock the row of the data range with `$` when copying across columns: `H$35:H$40`.

## GDP-Weighted Mean with SUMPRODUCT

The GDP-weighted average of net export percentages equals the ratio of total net exports to total GDP (times 100). Using SUMPRODUCT:

```excel
=ROUND(SUMPRODUCT(H35:H40, H26:H31) / SUM(H26:H31), 1)
```

**Why this works:**
- `SUMPRODUCT(pct_i, GDP_i)` = Σ (NX_i/GDP_i × 100 × GDP_i) = 100 × Σ NX_i
- Dividing by `SUM(GDP_i)` gives 100 × Σ NX_i / Σ GDP_i = weighted mean %

**Equivalent interpretation:** total net exports of GCC / total GCC GDP × 100.

When copying across year columns, use relative column references so GDP and NX ranges shift together.

## Rounding Convention

Per the task instructions, all percentage results must display as numbers like `12.3` (not `0.123`):
- Multiply raw ratio by 100 inside the formula
- Wrap with `ROUND(..., 1)` for exactly one decimal place
- This ensures the stored value is rounded, not just display-formatted

## Writing These Formulas with openpyxl

```python
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

wb = load_workbook('file.xlsx')
ws = wb['Task']

# Net exports % for 6 countries (rows 35–40), 5 years (cols H–L = 8–12)
exports_start_row = 12
imports_start_row = 19
gdp_start_row = 26

for i, data_row in enumerate(range(35, 41)):  # rows 35–40
    exp_row = exports_start_row + i
    imp_row = imports_start_row + i
    gdp_row = gdp_start_row + i
    for col in range(8, 13):  # columns H–L
        c = get_column_letter(col)
        ws.cell(row=data_row, column=col).value = (
            f'=ROUND(({c}{exp_row}-{c}{imp_row})/{c}{gdp_row}*100,1)'
        )

# Summary stats (rows 42–47), same columns
stat_formulas = [
    'ROUND(MIN({r}),1)',
    'ROUND(MAX({r}),1)',
    'ROUND(MEDIAN({r}),1)',
    'ROUND(AVERAGE({r}),1)',
    'ROUND(PERCENTILE({r},0.25),1)',
    'ROUND(PERCENTILE({r},0.75),1)',
]
for i, fmt in enumerate(stat_formulas):
    for col in range(8, 13):
        c = get_column_letter(col)
        rng = f'{c}35:{c}40'
        ws.cell(row=42 + i, column=col).value = '=' + fmt.format(r=rng)

# Weighted mean (row 50)
for col in range(8, 13):
    c = get_column_letter(col)
    ws.cell(row=50, column=col).value = (
        f'=ROUND(SUMPRODUCT({c}35:{c}40,{c}26:{c}31)/SUM({c}26:{c}31),1)'
    )

wb.save('file.xlsx')
```
