---
name: excel-statistics-formulas
description: Excel statistical functions (MIN, MAX, MEDIAN, AVERAGE, PERCENTILE, SUMPRODUCT) with ROUND.
---

# Excel Statistical Formulas

## Common Statistical Functions
```
=MIN(range)
=MAX(range)
=MEDIAN(range)
=AVERAGE(range)
=PERCENTILE(range, k)    -- k is 0 to 1 (e.g., 0.25 for 25th percentile)
```

## ROUND Function
```
=ROUND(value, num_digits)   -- e.g., ROUND(12.345, 1) = 12.3
```

## SUMPRODUCT for Weighted Mean
GDP-weighted mean of net exports as % of GDP:
```
=ROUND(SUMPRODUCT(Exports - Imports) / SUM(GDP) * 100, 1)
```

This works because:
- weighted_mean = Σ(gdp_i × (exp_i - imp_i)/gdp_i) / Σ(gdp_i) × 100
- Simplifies to: Σ(exp_i - imp_i) / Σ(gdp_i) × 100
- SUMPRODUCT handles the element-wise subtraction and summation
