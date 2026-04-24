---
name: run2_excel-sumproduct
description: Calculate GDP-weighted mean of net exports as % of GDP using SUMPRODUCT in Excel, including all supporting statistics (min, max, median, percentiles).
---

# Excel SUMPRODUCT: GDP-Weighted Mean and Statistics

## Net Exports % of GDP (Step 2 Formula)
```excel
=ROUND((H12 - H19) / H26 * 100, 1)
```
- `H12` = Exports; `H19` = Imports; `H26` = GDP
- Multiply by 100 to express as percentage points (e.g., 19.7 not 0.197)
- ROUND to 1 decimal place per task requirements

## Row Mapping in Task Sheet
| Step 2 Row | Country | Exports Row | Imports Row | GDP Row |
|-----------|---------|-------------|-------------|---------|
| 35 | UAE | 12 | 19 | 26 |
| 36 | Bahrain | 13 | 20 | 27 |
| 37 | Kuwait | 14 | 21 | 28 |
| 38 | Qatar | 15 | 22 | 29 |
| 39 | Oman | 16 | 23 | 30 |
| 40 | Saudi Arabia | 17 | 24 | 31 |

## Statistics Formulas (H42:L47)
All statistics use the net exports % range for that year column:
```excel
Row 42 (min):     =ROUND(MIN(H35:H40), 1)
Row 43 (max):     =ROUND(MAX(H35:H40), 1)
Row 44 (median):  =ROUND(MEDIAN(H35:H40), 1)
Row 45 (mean):    =ROUND(AVERAGE(H35:H40), 1)
Row 46 (P25):     =ROUND(PERCENTILE(H35:H40, 0.25), 1)
Row 47 (P75):     =ROUND(PERCENTILE(H35:H40, 0.75), 1)
```

## GDP-Weighted Mean (Step 3)
```excel
=ROUND(SUMPRODUCT(H35:H40, H26:H31) / SUM(H26:H31), 1)
```

### Why This Works
- `H35:H40` = net exports % (already × 100)
- `H26:H31` = GDP weights
- `SUMPRODUCT(pct, GDP) / SUM(GDP)` = weighted average
- Since pct is already ×100, result is in percentage points

### Mathematical Equivalence
```
Weighted Mean = Σ(pct_i × GDP_i) / Σ(GDP_i)
              = Σ((Exports_i - Imports_i) / GDP_i × 100 × GDP_i) / Σ(GDP_i)
              = Σ(Exports_i - Imports_i) × 100 / Σ(GDP_i)
```

### Sample Values (2019)
- UAE: 19.7%, weight 418.0B
- Bahrain: 11.3%, weight 38.7B
- Kuwait: 12.6%, weight 138.7B
- Qatar: 14.3%, weight 176.4B
- Oman: 12.5%, weight 88.1B
- Saudi Arabia: 8.0%, weight 838.6B
- **Weighted Mean ≈ 12.2%**

## openpyxl Implementation
```python
cols = ['H', 'I', 'J', 'K', 'L']

# Net exports % per country
for i in range(6):
    row = 35 + i
    for col in cols:
        task[f'{col}{row}'] = f'=ROUND(({col}{12+i}-{col}{19+i})/{col}{26+i}*100,1)'

# Statistics
for col in cols:
    task[f'{col}42'] = f'=ROUND(MIN({col}35:{col}40),1)'
    task[f'{col}43'] = f'=ROUND(MAX({col}35:{col}40),1)'
    task[f'{col}44'] = f'=ROUND(MEDIAN({col}35:{col}40),1)'
    task[f'{col}45'] = f'=ROUND(AVERAGE({col}35:{col}40),1)'
    task[f'{col}46'] = f'=ROUND(PERCENTILE({col}35:{col}40,0.25),1)'
    task[f'{col}47'] = f'=ROUND(PERCENTILE({col}35:{col}40,0.75),1)'

# Weighted mean
for col in cols:
    task[f'{col}50'] = f'=ROUND(SUMPRODUCT({col}35:{col}40,{col}26:{col}31)/SUM({col}26:{col}31),1)'
```
