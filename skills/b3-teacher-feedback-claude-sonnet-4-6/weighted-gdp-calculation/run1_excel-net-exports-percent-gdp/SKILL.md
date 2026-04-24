---
name: excel-net-exports-percent-gdp
description: Use when calculating net exports as a percentage of GDP in Excel, including computing summary statistics (min, max, median, mean, percentiles) and a GDP-weighted mean using SUMPRODUCT. Covers formula structure, rounding conventions, and display formatting.
---

## Net Exports as % of GDP Calculations in Excel

### Definition

**Net Exports (NX)** = Exports of Goods & Services − Imports of Goods & Services

**Net Exports as % of GDP** = (NX / GDP) × 100

Where all values are in the same currency and time period.

### Formula Pattern

Assuming:
- Exports values are in range H12:L17 (rows = countries, columns = years)
- Imports values are in range H19:L24
- GDP values are in range H26:L31
- Net exports % of GDP output goes in H35:L40

For cell H35 (country 1, first year):
```excel
=((H12 - H19) / H26) * 100
```

- Subtract imports from exports to get net exports
- Divide by GDP
- Multiply by 100 to express as percentage points (e.g., display 12.3 not 0.123)
- Wrap in ROUND(..., 1) if rounding is required at formula level:
  ```excel
  =ROUND(((H12 - H19) / H26) * 100, 1)
  ```

### Summary Statistics (applied to the % of GDP results)

Assuming results are in H35:L40 (5 years × 6 countries = 30 values, or arranged by context):

```excel
=ROUND(MIN(H35:L40), 1)      ' Minimum
=ROUND(MAX(H35:L40), 1)      ' Maximum
=ROUND(MEDIAN(H35:L40), 1)   ' Median
=ROUND(AVERAGE(H35:L40), 1)  ' Simple mean
=ROUND(PERCENTILE(H35:L40, 0.25), 1)  ' 25th percentile
=ROUND(PERCENTILE(H35:L40, 0.75), 1)  ' 75th percentile
```

Or use `PERCENTILE.INC` for inclusive percentile (default behavior, same as PERCENTILE):
```excel
=ROUND(PERCENTILE.INC(H35:L40, 0.25), 1)
```

### GDP-Weighted Mean Using SUMPRODUCT

The weighted mean weights each country's net exports % by that country's GDP share.

**Formula concept:**
```
Weighted Mean = Σ(NX%_i × GDP_i) / Σ(GDP_i)
```

**In Excel (for a single year, e.g., column H, 6 countries in rows 35-40 and GDP in rows 26-31):**
```excel
=ROUND(SUMPRODUCT(H35:H40, H26:H31) / SUM(H26:H31), 1)
```

**For multiple years across a 2D range (all years combined):**
```excel
=ROUND(SUMPRODUCT(H35:L40, H26:L31) / SUM(H26:L31), 1)
```

- `SUMPRODUCT(nx_pct_range, gdp_range)` — multiplies each country's NX% by its GDP and sums the products
- `SUM(gdp_range)` — total GDP (the denominator / sum of weights)
- Since NX% is already multiplied by 100, the result is already in percentage-point form

**Important:** Make sure the NX% values fed into SUMPRODUCT are already in ×100 form (e.g., 12.3), not decimal form (0.123), so the weighted mean is also in the same scale.

Alternatively, compute from raw values directly:
```excel
=ROUND(SUMPRODUCT(H12:L17 - H19:L24, H26:L31) / SUMPRODUCT(H26:L31, H26:L31) * 100, 1)
```
*(Only use this pattern if the denominator logic matches — typically simpler to use the already-computed % cells.)*

### Display vs. Calculation

- The task requires displaying `12.3` not `0.123`
- Achieve this by multiplying by 100 **inside the formula** (not just via cell formatting)
- Do NOT use percentage cell format (which would show `1230%` if value is already 12.3)
- Use **Number** format with 1 decimal place, or **General** format