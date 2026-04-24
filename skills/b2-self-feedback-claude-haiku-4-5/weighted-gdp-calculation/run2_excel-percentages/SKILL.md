---
name: run2_excel-percentages
description: Calculating and formatting percentages in Excel with proper rounding and display
---

# Excel Percentages: Calculation, Rounding, and Display

## Key Concept: Percentage Storage vs. Display

Excel stores percentages as decimals:
- **Internal storage**: 0.123 (decimal)
- **Display as percentage**: 12.3% (with % format)
- **Display as number**: 12.3 (multiply by 100, format as number)

## Percentage Calculation Patterns

### Simple Percentage
```
=Value / Total * 100
```
Result: 12.3 (displays as "12.3" when formatted as number)

### Percentage of Change
```
=(New - Old) / Old * 100
```
Example: `=(105 - 100) / 100 * 100` = 5

### Weighted Percentage (Average with Weights)
```
=SUM(Values * Weights) / SUM(Weights) * 100
```

### Percentage of Total (where Total = SUM of Components)
```
=(E - I) / G * 100
```
Example: Net exports as % of GDP = (Exports - Imports) / GDP * 100

## Rounding Percentages to 1 Decimal Place

### Method 1: ROUND Function (Recommended)
```
=ROUND((Numerator / Denominator * 100), 1)
=ROUND(Formula_Result, 1)
```

**Example:**
```
=ROUND((Exports - Imports) / GDP * 100, 1)
```
Result: 12.3 (always displayed with up to 1 decimal place)

### Method 2: Cell Number Formatting
1. Calculate without ROUND: `=(E-I)/G*100`
2. Format cell as: Number with 1 decimal place
3. Result displays: 12.3

**Recommended:** Use ROUND in the formula for portability and clarity.

## Common Percentage Calculations in Finance

### Net Exports as % of GDP
```
=ROUND(((Exports - Imports) / GDP * 100), 1)
```

### Profitability Ratios
```
=ROUND((Income / Revenue * 100), 1)      # Margin %
=ROUND((Profit / Investment * 100), 1)   # ROI %
```

### Growth Rate
```
=ROUND(((Current - Previous) / Previous * 100), 1)
```

### Weighted Average Percentage
```
=ROUND((SUM(H35:H40 * H26:H31) / SUM(H26:H31)), 1)
```

## Statistical Functions with Percentages

### MIN, MAX, MEDIAN of Percentages
```
=ROUND(MIN(H35:H40), 1)     # Already in % form
=ROUND(MAX(H35:H40), 1)
=ROUND(MEDIAN(H35:H40), 1)
```

### AVERAGE of Percentages
```
=ROUND(AVERAGE(H35:H40), 1)
```

### QUARTILE (Percentiles) of Percentages
```
=ROUND(QUARTILE(H35:H40, 1), 1)   # 25th percentile
=ROUND(QUARTILE(H35:H40, 3), 1)   # 75th percentile
```

## Important Notes

- **Apply *100 when needed**: Only when converting decimals to percentage representation
- **Apply ROUND when required**: Especially when displaying to specific decimal places
- **Order matters**: ROUND should be the outermost function when combining with *100
- **Verify units**: Ensure the result matches the intended unit (% vs. 0-1 scale)

## Examples

### Wrong (Missing *100)
```
=ROUND((Exports - Imports) / GDP, 1)    # Result: 0.1 instead of 12.3
```

### Correct
```
=ROUND((Exports - Imports) / GDP * 100, 1)   # Result: 12.3
```

### Wrong (Incorrect ROUND placement)
```
=ROUND((E-I)/G, 1) * 100    # Rounds 0.123 to 0.1, then multiplies by 100 = 10
```

### Correct
```
=ROUND((E-I)/G * 100, 1)    # Multiplies to 12.3, then rounds to 12.3
```
