# excel-statistical-analysis

Calculating descriptive statistics (min, max, median, mean, percentiles) and weighted means using `SUMPRODUCT`. Use this skill whenever the user asks for aggregate calculations or weighted averages in Excel.

## Basic Descriptive Statistics
- **Minimum:** `=MIN(Range)`
- **Maximum:** `=MAX(Range)`
- **Median:** `=MEDIAN(Range)`
- **Simple Mean (Average):** `=AVERAGE(Range)`
- **Percentiles:** `=PERCENTILE.INC(Range, k)` (where `k` is a value from 0 to 1, e.g., 0.25 for 25th percentile)

## Weighted Mean with SUMPRODUCT
The weighted mean is calculated by taking the sum of the products of each value and its weight, and then dividing by the sum of the weights.

**Formula Template:**
`=SUMPRODUCT(Values_Range, Weights_Range) / SUM(Weights_Range)`

- `Values_Range`: The data values you want to average (e.g., Net Exports as % of GDP).
- `Weights_Range`: The weights for each value (e.g., GDP).

**Note:** Ensure both ranges are the same size and shape.

## Rounding Results
When the user requests a specific number of decimal places, wrap the formula in `ROUND()`.

**Formula Template:**
`=ROUND(Calculation_Formula, 1)`

- `1`: Rounds to one decimal place.
- If the result is a percentage (e.g., 0.123 for 12.3%) and the user wants it displayed as 12.3:
  - `=ROUND((Calculation_Formula) * 100, 1)`
