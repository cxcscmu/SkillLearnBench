---
name: Net Exports Percentage Calculation and Statistical Analysis
description: Calculate net exports as a percentage of GDP for multiple countries, then compute descriptive statistics (min, max, median, mean, percentiles) on the percentage values. Use this when analyzing trade performance across multiple entities.
---

## When to Use
- You have net exports and GDP values in separate rows/ranges
- You need to convert to percentages and analyze the distribution
- Results must be displayed as percentages (e.g., 12.3, not 0.123)

## Calculation Steps

### Step 1: Calculate Net Exports as Percentage of GDP
In cells H35:L40, use:
```excel
=ROUND((net_exports / gdp) * 100, 1)
```

Where:
- `net_exports` is the row containing net export values (from Step 1 lookup)
- `gdp` is the row containing GDP values (from Step 1 lookup)
- Multiply by 100 to convert to percentage display format
- `ROUND(..., 1)` rounds to one decimal place

**Example for cell H35:**
```excel
=ROUND((H12 / H26) * 100, 1)
```

### Step 2: Calculate Statistics

Use these formulas for the six countries' net export percentages (range H35:L40):

- **Minimum**: `=ROUND(MIN(H35:L40), 1)`
- **Maximum**: `=ROUND(MAX(H35:L40), 1)`
- **Median**: `=ROUND(MEDIAN(H35:L40), 1)`
- **Simple Mean**: `=ROUND(AVERAGE(H35:L40), 1)`
- **25th Percentile**: `=ROUND(PERCENTILE(H35:L40, 0.25), 1)`
- **75th Percentile**: `=ROUND(PERCENTILE(H35:L40, 0.75), 1)`

## Key Points
- Values in H35:L40 are already percentages (multiplied by 100)
- Do NOT multiply by 100 again in these statistics formulas
- Always round the final result, not intermediate steps
- Each statistic should display as a decimal (e.g., 12.3, not 0.123)