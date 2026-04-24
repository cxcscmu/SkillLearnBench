---
name: weighted-mean-calculation
description: How to calculate weighted means in Excel using SUMPRODUCT. Use this skill when calculating the weighted average for a group (e.g., GCC Countries) by multiplying values by their corresponding weights (e.g., GDP).
---

# Weighted Mean Calculation: SUMPRODUCT

To calculate the weighted mean:

`=SUMPRODUCT(values_range, weights_range) / SUM(weights_range)`

- **values_range**: The data points to be weighted (e.g., Net Exports as % of GDP).
- **weights_range**: The values used as weights (e.g., GDP in current prices).

Ensure both ranges are of the same size. If the desired result is a percentage, format the cell appropriately or multiply the final formula by 100 to meet reporting requirements.
