---
name: Weighted Mean Calculation with SUMPRODUCT
description: Calculate a weighted average using SUMPRODUCT when weights and values have a one-to-one correspondence. Use this for computing aggregate statistics where different entities have different importance (weights).
---

## When to Use
- You have values and corresponding weights in aligned rows/columns
- You need a single weighted average metric
- Weights and values must be in the same column/row order

## Formula Structure

```excel
=ROUND(SUMPRODUCT(values_range, weights_range) / SUM(weights_range), 1)
```

Where:
- `values_range`: The percentages to be weighted (already in percentage format, e.g., 12.3)
- `weights_range`: The weights (e.g., GDP values or population)
- Divide by `SUM(weights_range)` to normalize
- Multiply by 100 is **NOT needed** if values are already displayed as percentages
- `ROUND(..., 1)` rounds to one decimal place

## Step-by-Step for GCC Net Exports Weighted Mean

1. **Identify your values**: Net exports as % of GDP (from Step 2, cells H35:L40)
2. **Identify your weights**: GDP values (from Step 1 lookup, row 26 — cells H26:L26)
3. **Verify alignment**: Each column in H35:L40 corresponds to the same column in H26:L26
4. **Write the formula**:

```excel
=ROUND(SUMPRODUCT(H35:L40, H26:L26) / SUM(H26:L26), 1)
```

**Critical:** 
- Do NOT multiply by 100 in the SUMPRODUCT formula — the net export percentages are already multiplied by 100 from Step 2
- The final ROUND should happen only once, on the entire result
- Verify row numbers: H35:L40 (net exports %) and H26:L26 (GDP weights) must match your Step 1 and Step 2 placements

## Common Mistakes to Avoid
- ✗ Multiplying by 100 twice (once in Step 2, again in SUMPRODUCT)
- ✗ Using different row ranges for values and weights (e.g., H35:L40 vs. H27:L27)
- ✗ Rounding intermediate calculations before the final result
- ✗ Forgetting to divide by SUM(weights_range) to normalize