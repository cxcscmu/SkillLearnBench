---
name: Multi-Condition Lookup with INDEX-MATCH for Financial Data
description: Use INDEX-MATCH with two conditions (series code and year) to retrieve values from a source data table. Apply this when you need to pull specific data points based on multiple criteria from an unstructured data range.
---

## When to Use
- You have data organized by multiple dimensions (e.g., country/series code and year)
- You need to match on two or more criteria simultaneously
- VLOOKUP or HLOOKUP alone cannot handle your lookup structure

## Formula Structure

Use **nested INDEX-MATCH** to handle two conditions:

```excel
=INDEX(data_array, MATCH(criteria1, lookup_array1, 0), MATCH(criteria2, lookup_array2, 0))
```

## Step-by-Step Approach

1. **Identify your criteria**: Series code (column D in Task sheet) and Year (row 10 in Task sheet)
2. **Locate source data**: Data sheet, rows 21–40
3. **Set up the formula**:
   - `data_array`: The values you want to retrieve (e.g., columns with actual data in Data sheet)
   - `lookup_array1`: Series code column in Data sheet (find match for column D)
   - `lookup_array2`: Year row in Task sheet (find match for row 10)
4. **Apply absolute references** where needed so the formula can be copied across multiple cells

## Example
```excel
=INDEX(Data.$A$21:$Z$40, MATCH($D12, Data.$A$21:$A$40, 0), MATCH(H$10, Data.$A$20:$Z$20, 0))
```

## Key Points
- Use `MATCH(..., 0)` for exact matches
- Lock criteria references with `$` appropriately (e.g., `$D12` to keep column D fixed, `H$10` to keep row 10 fixed)
- Ensure the lookup arrays span the correct range in the source sheet
- Test with one cell, then copy to all yellow ranges (H12:L17, H19:L24, H26:L31)