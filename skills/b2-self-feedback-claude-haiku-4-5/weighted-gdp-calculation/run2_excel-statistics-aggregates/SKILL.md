---
name: run2_excel-statistics-aggregates
description: Excel statistical functions for datasets including MIN, MAX, MEDIAN, AVERAGE, QUARTILE, and SUMPRODUCT
---

# Excel Statistical and Aggregate Functions

## Central Tendency Functions

### AVERAGE (Arithmetic Mean)
Returns the arithmetic mean of a range.
```
=AVERAGE(H35:H40)
```
- Simple mean across all values
- Treats all values equally
- Returns single decimal value

### MEDIAN
Returns the middle value in a sorted range.
```
=MEDIAN(H35:H40)
```
- Middle value when data is sorted
- For 6 values: average of 3rd and 4th values
- Robust to outliers

## Extreme Values

### MIN
Returns the minimum value in a range.
```
=MIN(H35:H40)
```

### MAX
Returns the maximum value in a range.
```
=MAX(H35:H40)
```

## Percentile Functions

### QUARTILE (Excel 2007+) - Recommended
Returns quartile values for a dataset.

**Syntax:** `=QUARTILE(range, quart)`

**Parameters:**
- **range**: Data range to analyze (e.g., H35:H40)
- **quart**: Quartile number (0-4)
  - 0: Minimum value
  - 1: 25th percentile (Q1)
  - 2: Median/50th percentile
  - 3: 75th percentile (Q3)
  - 4: Maximum value

**Examples:**
```
=QUARTILE(H35:H40, 1)   # 25th percentile
=QUARTILE(H35:H40, 3)   # 75th percentile
```

### PERCENTILE (Alternative Syntax)
Returns percentile value with flexible precision.

**Syntax:** `=PERCENTILE(range, k)`

**Parameters:**
- **range**: Data range
- **k**: Percentile value (0 to 1)
  - 0.25 for 25th percentile
  - 0.5 for 50th percentile (median)
  - 0.75 for 75th percentile

**Examples:**
```
=PERCENTILE(H35:H40, 0.25)   # 25th percentile
=PERCENTILE(H35:H40, 0.75)   # 75th percentile
```

## Weighted Aggregates

### SUMPRODUCT (Weighted Sum and Weighted Mean)

**For weighted sum:**
```
=SUMPRODUCT(values_range, weights_range)
```
Multiplies each value by its weight, then sums results.

**For weighted mean:**
```
=SUMPRODUCT(values_range, weights_range) / SUM(weights_range)
```

**Example - Weighted mean of GDP by country:**
```
=SUMPRODUCT(H35:H40, H26:H31) / SUM(H26:H31)
```

**Example - Aggregate net exports as % of GDP for region:**
```
=(SUM(Exports) - SUM(Imports)) / SUM(GDP) * 100
```

## Rounding Statistical Results

Always round when displaying statistics as percentages or to specific decimal places:

```
=ROUND(MIN(H35:H40), 1)
=ROUND(MAX(H35:H40), 1)
=ROUND(MEDIAN(H35:H40), 1)
=ROUND(AVERAGE(H35:H40), 1)
=ROUND(QUARTILE(H35:H40, 1), 1)
=ROUND(QUARTILE(H35:H40, 3), 1)
```

## Statistical Function Selection Guide

| Need | Function | Example |
|------|----------|---------|
| Middle value | MEDIAN | `=MEDIAN(range)` |
| Average | AVERAGE | `=AVERAGE(range)` |
| Smallest | MIN | `=MIN(range)` |
| Largest | MAX | `=MAX(range)` |
| 25th percentile | QUARTILE(...,1) | `=QUARTILE(range,1)` |
| 75th percentile | QUARTILE(...,3) | `=QUARTILE(range,3)` |
| Weighted average | SUMPRODUCT | `=SUMPRODUCT(vals,wts)/SUM(wts)` |
| Aggregate %* | SUM ratio | `=(SUM(E)-SUM(I))/SUM(G)*100` |

*For aggregate metrics like GCC-wide net exports %

## Performance Considerations

- **SUMPRODUCT vs. array formulas**: SUMPRODUCT is simpler and more compatible across Excel versions
- **Data range size**: All functions handle large ranges efficiently (tested up to millions of rows)
- **Empty cells**: Most functions ignore empty cells; verify if zeros should be included

## Common Patterns for Data Analysis

### Compare Individual vs. Aggregate
```
Individual (per country): =ROUND(AVERAGE(H35:H40), 1)
Aggregate (for region): =ROUND((SUM(H12:H17)-SUM(H19:H24))/SUM(H26:H31)*100, 1)
```

### Detect Outliers Using Quartiles
```
Q1: =QUARTILE(range, 1)
Q3: =QUARTILE(range, 3)
IQR: =Q3 - Q1
Outlier threshold: Values > Q3 + 1.5*IQR or < Q1 - 1.5*IQR
```

### Multi-Dimensional Aggregation
```
=SUMPRODUCT(criteria_range=criteria_value, aggregate_range) / SUMPRODUCT(criteria_range=criteria_value, weight_range)
```
