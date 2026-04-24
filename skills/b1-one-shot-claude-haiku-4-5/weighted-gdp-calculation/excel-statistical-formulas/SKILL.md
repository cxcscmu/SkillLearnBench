---
name: excel-statistical-formulas
description: Use Excel statistical functions for descriptive analysis including percentiles, weighted calculations, and data summaries.
---

# Excel Statistical Formulas

## Overview
Statistical functions in Excel calculate measures like mean, median, percentiles, and enable weighted calculations for economic data analysis.

## Core Statistical Functions

### Basic Descriptive Statistics

**MIN** - Returns the smallest value
```
=MIN(range)
=MIN(H35:L40)
```

**MAX** - Returns the largest value
```
=MAX(range)
=MAX(H35:L40)
```

**MEDIAN** - Returns the middle value
```
=MEDIAN(range)
=MEDIAN(H35:L40)
```

**AVERAGE** - Returns the arithmetic mean
```
=AVERAGE(range)
=AVERAGE(H35:L40)
```

### Percentile Functions

**PERCENTILE** - Returns the kth percentile of a dataset
```
=PERCENTILE(range, k)
```
Where k is a decimal (0.25 for 25th percentile, 0.75 for 75th percentile)

**Examples:**
```
25th Percentile:  =PERCENTILE(H35:L40, 0.25)
75th Percentile:  =PERCENTILE(H35:L40, 0.75)
```

**PERCENTILE.INC vs PERCENTILE.EXC:**
- PERCENTILE.INC: Inclusive method (older PERCENTILE function)
- PERCENTILE.EXC: Exclusive method (newer, statistical best practice)

## Weighted Mean Calculation

### SUMPRODUCT for Weighted Mean
The SUMPRODUCT function multiplies corresponding elements in arrays and returns the sum of products.

**Syntax:**
```
=SUMPRODUCT(array1, array2, ...)
```

**Weighted Mean Formula:**
```
=SUMPRODUCT(values_array, weights_array) / SUM(weights_array)
```

**Example: Weighted Mean of Net Exports by GDP Weight**
```
=SUMPRODUCT(G35:G40, GDP_weights) / SUM(GDP_weights)
```

**How it works:**
1. Multiply each value by its corresponding weight
2. Sum all products
3. Divide by sum of weights

### Handling Multiple Columns
For data across multiple columns (like multiple years), you may need to:
1. Flatten the data into single rows/columns, or
2. Use array formulas with SUMPRODUCT

**Example with multiple criteria:**
```
=SUMPRODUCT((range1=criteria1)*(range2=criteria2)*values) / SUMPRODUCT((range1=criteria1)*(range2=criteria2)*weights)
```

## Percentage Calculations

### Converting to Percentage Display
Excel stores percentages as decimals (0.123 = 12.3%).

**To display as percentage (12.3 instead of 0.123):**
```
=formula_result * 100
```

**To round to one decimal place:**
```
=ROUND(formula_result * 100, 1)
```

**Combined example:**
```
=ROUND(SUMPRODUCT(values, weights) / SUM(weights) * 100, 1)
```

## Practical Example: GCC Net Exports Analysis

### Step 1: Calculate Net Exports Percentage
```
=Net_Exports / GDP * 100
```

### Step 2: Calculate Statistics
```
Min:       =MIN(values) * 100
Max:       =MAX(values) * 100
Median:    =MEDIAN(values) * 100
Mean:      =AVERAGE(values) * 100
25th %ile: =PERCENTILE(values, 0.25) * 100
75th %ile: =PERCENTILE(values, 0.75) * 100
```

### Step 3: Weighted Mean
```
=SUMPRODUCT(values, weights) / SUM(weights) * 100
```
Where:
- values: Net exports as % of GDP
- weights: GDP figures (or country weights)

## Rounding Best Practices

**ROUND function:**
```
=ROUND(number, num_digits)
```
- num_digits = 1 for one decimal place
- num_digits = 0 for whole numbers
- num_digits = -1 for tens place

**Example:**
```
=ROUND(12.345 * 100, 1)  → 1234.5
=ROUND(0.12345 * 100, 1) → 12.3
```

## Performance Considerations

1. **SUMPRODUCT with conditions**: More flexible than SUMIFS, but slower on large datasets
2. **Array formulas**: Use where needed but consider calculation time
3. **Volatile functions**: MIN, MAX, PERCENTILE may recalculate frequently

## Tips for Economic Data

1. **Handling missing data**: Use IFERROR with statistical functions
   ```
   =IFERROR(PERCENTILE(range, 0.25), "N/A")
   ```

2. **Weighted by GDP**: When calculating regional averages, weight by GDP size
   ```
   =SUMPRODUCT(country_values, country_gdp) / SUM(country_gdp)
   ```

3. **Multi-year analysis**: Calculate across years while maintaining criteria
4. **Sensitivity**: Test with subsets to validate formula logic
