---
name: Calculate-AUM-from-Holdings
description: Sum the market values of all holdings to derive the Assets Under Management (AUM) for a fund as of a specific report date. Use this to answer questions about fund size in a given quarter.
---

## Steps

1. **Verify the value field exists**
   - Confirm the holdings data has a market value or position value column
   - Check field name (e.g., "market_value", "value", "position_value")
   - Ensure values are in consistent currency (typically USD)

2. **Handle missing or null values**
   - Identify rows with null market values
   - Decide whether to exclude them or impute (usually exclude)
   - Document how many rows are excluded

3. **Sum all position values**
   - Calculate total: `AUM = sum(market_value)` across all holdings
   - Ensure calculation uses correct numeric type (avoid string concatenation)

4. **Verify AUM reasonableness**
   - Compare against any AUM figures in fund metadata if available
   - Check if AUM aligns with fund size expectations (e.g., Renaissance should be large)
   - Flag if AUM seems unusually high or low

5. **Format and report**
   - Return AUM as a numeric value (e.g., in millions or billions as appropriate)
   - Document the report date and accession_number alongside the AUM