---
name: run2_excel-weighted-mean
description: GDP-weighted mean and descriptive statistics for net exports as % of GDP in Excel
---

# Weighted Mean and Statistics for Net Exports % of GDP

## Step 2: Net Exports as % of GDP
Formula: `=ROUND((Exports - Imports) / GDP * 100, 1)`

Where:
- Exports = row from H12:L17
- Imports = corresponding row from H19:L24
- GDP = corresponding row from H26:L31
- Multiply by 100 to get percentage as number (e.g., 12.3 not 0.123)
- ROUND to 1 decimal place

```python
for i in range(6):
    export_row = 12 + i
    import_row = 19 + i
    gdp_row = 26 + i
    dest_row = 35 + i
    for col in ['H', 'I', 'J', 'K', 'L']:
        ws[f'{col}{dest_row}'] = f'=ROUND(({col}{export_row}-{col}{import_row})/{col}{gdp_row}*100,1)'
```

## Descriptive Statistics
All wrapped in ROUND(..., 1):
- MIN, MAX, MEDIAN, AVERAGE
- PERCENTILE(range, 0.25) and PERCENTILE(range, 0.75)

## Step 3: GDP-Weighted Mean using SUMPRODUCT
The weighted mean weights each country's net export % by its GDP:

```
=ROUND(SUMPRODUCT(H35:H40, H26:H31) / SUM(H26:H31), 1)
```

Mathematical equivalence:
- weighted_mean = Σ(NX%_i × GDP_i) / Σ(GDP_i)
- This equals: Σ(NX_i) / Σ(GDP_i) × 100
- Both give the same result since NX%_i = NX_i/GDP_i × 100

## Verification
Always verify with manual Python calculation:
```python
pcts = [cell_values_from_H35_to_H40]
gdps = [cell_values_from_H26_to_H31]
weighted_mean = sum(p*g for p,g in zip(pcts, gdps)) / sum(gdps)
```
