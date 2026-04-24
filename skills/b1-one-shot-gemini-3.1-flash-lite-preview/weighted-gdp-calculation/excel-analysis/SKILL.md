---
name: excel-analysis
description: Techniques for statistical analysis in Excel including weighted means, percentiles, and rounding.
---

### Weighted Mean
Use `SUMPRODUCT` to calculate the weighted mean.
Formula: `=SUMPRODUCT(values_array, weights_array) / SUM(weights_array)`
Ensure the result is multiplied by 100 if the values are proportions.

### Percentiles
Use the `PERCENTILE.INC` function.
Formula: `=PERCENTILE.INC(array, k)` where `k` is 0.25 for 25th percentile and 0.75 for 75th.

### Rounding
Use the `ROUND` function to limit decimal places.
Formula: `=ROUND(value, 1)`
If the value is a percentage in proportion format (e.g., 0.123), use `=ROUND(value * 100, 1)`.
