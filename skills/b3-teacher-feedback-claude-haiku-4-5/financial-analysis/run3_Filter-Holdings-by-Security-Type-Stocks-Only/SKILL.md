---
name: Filter-Holdings-by-Security-Type-Stocks-Only
description: Remove non-equity securities (bonds, options, warrants, preferred shares, funds) from holdings data, keeping only common stock positions. Use the correct security type field identified from the raw data structure inspection.
---

## Steps

1. **Verify the security type field name**
   - Confirm from raw data inspection which field distinguishes equity from other instruments
   - Do NOT assume field names like "security_type" or "asset_class" without validation

2. **Define inclusion criteria for stocks**
   - Create a list of acceptable values that represent common equity shares
   - Examples: "STOCK", "EQUITY", "COMMON STOCK" (exact values depend on actual data)
   - Ensure logic is case-insensitive if needed

3. **Apply filtering logic**
   - Filter the holdings DataFrame to keep ONLY rows where security type matches stock criteria
   - Use `.isin()` or `.str.contains()` with the correct field name
   - Verify that rows are actually removed (not just flagged)

4. **Validate filter results**
   - Count retained records after filtering
   - Spot-check several remaining records to confirm they are actual stocks
   - Compare count against expected result to detect over/under-filtering

5. **Log excluded items**
   - Count how many non-stock items were removed by category
   - If count is significantly different from expected, review sample excluded records
   - Adjust filter criteria if needed (e.g., if ~1000 extra records remain, inspect what they are)

6. **Proceed only if counts match expected range**
   - Do not proceed to answer question until filtering produces correct count
   - If discrepancy remains, return to raw data inspection step