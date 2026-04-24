---
name: run2_excel-stats
description: Using Excel's statistical functions with rounding and percentage scaling in openpyxl.
---

# Statistical Calculations with Rounding

Common Excel statistical functions used for data analysis:
- **Min/Max**: `=MIN(range)`, `=MAX(range)`
- **Median/Mean**: `=MEDIAN(range)`, `=AVERAGE(range)`
- **Percentiles**: Use `=PERCENTILE(range, alpha)` for broad compatibility (where alpha is 0.25 for 25th, etc.).

### Rounding and Scaling to Percentages
If the requirement is to display percentages as whole numbers with one decimal place (e.g., 12.3 rather than 0.123):

1.  Calculate the ratio: `(Numerator / Denominator)`.
2.  Multiply by 100: `ratio * 100`.
3.  Round the result: `ROUND(result, 1)`.

`=ROUND((Exports - Imports) / GDP * 100, 1)`

### Consistent Formula Application
- Ensure statistics are computed over the correct data range (e.g., `H35:H40` for each year).
- If statistics themselves are percentages, ensure they are also rounded as per user instructions.

`=ROUND(AVERAGE(H35:H40), 1)`
