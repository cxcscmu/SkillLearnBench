---
name: run2_excel-weighted-mean
description: Understanding scaling and execution of weighted means using SUMPRODUCT.
---

# Weighted Means

A weighted mean accounts for the varying importance of data points using a secondary vector of weights (e.g., GDP).

## The SUMPRODUCT Formula
```excel
=SUMPRODUCT(values, weights) / SUM(weights)
```
- **Values**: e.g., Net Exports as % of GDP (`H35:H40`).
- **Weights**: e.g., Total GDP (`H26:H31`).

## Scaling Preservation
If your input `values` are already scaled by `100` (e.g., `12.3` representing `12.3%`), the result of the weighted mean will automatically preserve this scale. No secondary multiplication by `100` is needed.
```excel
=ROUND(SUMPRODUCT(H35:H40, H26:H31) / SUM(H26:H31), 1)
```
This calculates the aggregated weighted mean percentage directly and rounds it to the nearest single decimal.
