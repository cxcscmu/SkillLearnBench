---
name: excel-weighted-stats
description: >
  How to calculate weighted means and descriptive statistics (min, max, median,
  percentiles, simple mean) in Excel formulas via openpyxl. Use this skill
  whenever the user asks for SUMPRODUCT-based weighted averages, GDP-weighted
  means, percentile calculations, or descriptive statistics in Excel.
---

# Weighted Mean and Descriptive Statistics in Excel

## Weighted Mean with SUMPRODUCT

The GDP-weighted mean of a percentage series:

```
=ROUND(SUMPRODUCT(value_range, weight_range) / SUM(weight_range), 1)
```

- `value_range`: the calculated percentages (e.g., `H35:H40`)
- `weight_range`: the GDP values used as weights (e.g., `H26:H31`)

Both ranges must be the same size. SUMPRODUCT multiplies element-wise and sums.

### Why This Works
If `pct_i = (exports_i - imports_i) / gdp_i * 100`, then:
```
SUMPRODUCT(pct, gdp) / SUM(gdp)
= SUM(pct_i * gdp_i) / SUM(gdp_i)
= 100 * SUM(net_exports_i) / SUM(gdp_i)
```
This is the aggregate net-exports-to-GDP ratio for the group.

## Descriptive Statistics Formulas

| Statistic | Excel Formula |
|-----------|---------------|
| Min | `=MIN(range)` |
| Max | `=MAX(range)` |
| Median | `=MEDIAN(range)` |
| Simple mean | `=AVERAGE(range)` |
| 25th percentile | `=PERCENTILE(range, 0.25)` |
| 75th percentile | `=PERCENTILE(range, 0.75)` |

### Rounding to 1 Decimal (percentage display)
Wrap in ROUND: `=ROUND(MIN(H35:H40), 1)`

## Net Exports as Percent of GDP

```
=ROUND((Exports - Imports) / GDP * 100, 1)
```

Example cell formula:
```
=ROUND((H12-H19)/H26*100,1)
```

This yields a value like `12.3` (not `0.123`), matching the requirement to display
percentages as whole-number-scale values.

## openpyxl Example

```python
ws = wb['Task']

# Net exports % of GDP (row 35, columns H-L)
for col in ['H','I','J','K','L']:
    ws[f'{col}35'] = f'=ROUND(({col}12-{col}19)/{col}26*100,1)'

# Descriptive stats (rows 42-47)
for col in ['H','I','J','K','L']:
    ws[f'{col}42'] = f'=ROUND(MIN({col}35:{col}40),1)'
    ws[f'{col}43'] = f'=ROUND(MAX({col}35:{col}40),1)'
    ws[f'{col}44'] = f'=ROUND(MEDIAN({col}35:{col}40),1)'
    ws[f'{col}45'] = f'=ROUND(AVERAGE({col}35:{col}40),1)'
    ws[f'{col}46'] = f'=ROUND(PERCENTILE({col}35:{col}40,0.25),1)'
    ws[f'{col}47'] = f'=ROUND(PERCENTILE({col}35:{col}40,0.75),1)'

# Weighted mean (row 50)
for col in ['H','I','J','K','L']:
    ws[f'{col}50'] = f'=ROUND(SUMPRODUCT({col}35:{col}40,{col}26:{col}31)/SUM({col}26:{col}31),1)'
```
