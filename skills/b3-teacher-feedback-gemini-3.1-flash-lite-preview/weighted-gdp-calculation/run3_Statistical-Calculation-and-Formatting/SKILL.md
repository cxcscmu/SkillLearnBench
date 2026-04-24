---
name: Statistical Calculation and Formatting
description: Perform descriptive statistical analysis while ensuring results are displayed as percentages rounded to one decimal place.
---
1. For Step 2, compute the statistics (min, max, median, simple mean, 25th percentile, 75th percentile) for the Net Exports as % of GDP values populated in H35:L40.
2. Apply the following functions respectively: `=MIN(range)`, `=MAX(range)`, `=MEDIAN(range)`, `=AVERAGE(range)`, `=PERCENTILE.INC(range, 0.25)`, and `=PERCENTILE.INC(range, 0.75)`.
3. To display the result as `12.3` (not `0.123`), wrap the entire statistical function in `ROUND(..., 1)`. Ensure the cell format is set to "Number" rather than "Percentage" if multiplying by 100 is not explicitly applied in the formula itself.