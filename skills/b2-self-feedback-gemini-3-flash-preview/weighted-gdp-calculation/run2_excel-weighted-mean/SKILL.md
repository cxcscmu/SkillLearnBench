---
name: run2_excel-weighted-mean
description: Weighted mean calculations in Excel using SUMPRODUCT and SUM in openpyxl.
---

# Weighted Mean Formula (SUMPRODUCT)

Weighted means account for the relative importance of each data point, such as weighting country percentages by their respective GDPs.

### Formula Structure
`=ROUND(SUMPRODUCT(values_range, weights_range) / SUM(weights_range), 1)`

- `values_range`: The cell range containing the numbers to average (e.g., `H35:H40`).
- `weights_range`: The cell range containing the weights (e.g., `H26:H31`).
- `ROUND(..., 1)`: Ensures the final result is rounded to one decimal place.

### Alignment Requirements
- Ensure both the `values_range` and `weights_range` have the exact same dimensions and orientation.
- Confirm both ranges contain the corresponding data for the same entities (e.g., the same list of countries).
- If the values are already percentages multiplied by 100, the weighted mean will automatically be on the same scale.
