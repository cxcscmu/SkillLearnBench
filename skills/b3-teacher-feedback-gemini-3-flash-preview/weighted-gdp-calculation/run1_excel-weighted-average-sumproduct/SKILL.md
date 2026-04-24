---
name: excel-weighted-average-sumproduct
description: Calculate a weighted mean using the SUMPRODUCT and SUM functions.
---

A weighted average is calculated by multiplying each value by its corresponding weight, summing those products, and dividing by the total sum of the weights.

**Formula structure:**
`=SUMPRODUCT(values_range, weights_range) / SUM(weights_range)`

*   **values_range**: The data points (e.g., Net Exports as % of GDP for each country).
*   **weights_range**: The values used for weighting (typically GDP or Population).

**Example Application:**
If you need the weighted mean of net exports (column A) weighted by GDP (column B):
`=SUMPRODUCT(A1:A6, B1:B6) / SUM(B1:B6)`