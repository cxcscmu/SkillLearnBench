---
name: excel-statistical-and-weighted-mean-formulas
description: How to calculate statistical summaries (min, max, median, mean, percentiles) and weighted averages using SUMPRODUCT, with specific rules for rounding and avoiding double-scaling of percentages.
---

# Statistical Summaries and Weighted Means in Excel

## 1. Core Statistical Functions
To generate summary statistics across a range of cells, use the standard Excel statistical functions:
- **Minimum:** `=MIN(range)`
- **Maximum:** `=MAX(range)`
- **Median:** `=MEDIAN(range)`
- **Simple Mean:** `=AVERAGE(range)`
- **25th Percentile:** `=PERCENTILE.INC(range, 0.25)` or `=PERCENTILE.EXC(range, 0.25)`
- **75th Percentile:** `=PERCENTILE.INC(range, 0.75)` or `=PERCENTILE.EXC(range, 0.75)`

## 2. Weighted Mean (SUMPRODUCT)
A weighted mean multiplies each value by its corresponding weight and divides by the sum of the weights.
**Syntax:**
`=SUMPRODUCT(values_range, weights_range) / SUM(weights_range)`
*Note: If the weights inherently sum to exactly 1 (or 100%), dividing by the sum of the weights is mathematically optional, but including `/ SUM(weights_range)` is safer if the weights are absolute figures (like raw GDP).*

## 3. Handling Percentage Scaling (CRITICAL RULE)
If task instructions require converting decimals to standard percentage format numbers (e.g., displaying `12.3` instead of `0.123`), you achieve this by multiplying by 100. However, you must carefully control **where** this multiplication happens to avoid **double-scaling**.

*   **Scale at the Base Level:** Multiply by 100 when calculating the foundational data.
    *   *Example:* `=ROUND(((Exports - Imports) / GDP) * 100, 1)`
*   **DO NOT Double-Scale Summary Statistics:** If the base data (e.g., your Net Exports % range) is already scaled by 100, **do not** multiply your summary functions or your weighted mean function by 100 again. Functions like `AVERAGE()`, `MIN()`, and `SUMPRODUCT()` inherit the scale of the base data.
    *   *Incorrect (Double-Scaled):* `=AVERAGE(H35:H40) * 100` -> This would turn `12.3` into `1230.0`.
    *   *Correct:* `=AVERAGE(H35:H40)` -> Remains `12.3`.

## 4. Rounding Requirements
If required to round strictly to one decimal place, wrap the entire final calculation in the `ROUND` function:
`=ROUND(calculation_formula, 1)`

*Example for a scaled base calculation:*
`=ROUND(((A1 - B1) / C1) * 100, 1)`

*Example for a weighted mean on already-scaled base data:*
`=ROUND(SUMPRODUCT(H35:H40, H41:H46) / SUM(H41:H46), 1)`