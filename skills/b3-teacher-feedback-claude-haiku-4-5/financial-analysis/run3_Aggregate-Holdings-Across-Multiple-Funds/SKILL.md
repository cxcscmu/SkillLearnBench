---
name: Aggregate-Holdings-Across-Multiple-Funds
description: Search multiple funds' holdings data for a specific security (by CUSIP) and aggregate the total share values held by each fund manager. Use this to rank fund managers by their investment in a particular security.
---

## Steps

1. **Prepare the CUSIP to search**
   - Confirm you have the correct CUSIP for the target security
   - Document the security name for reference

2. **Iterate through all available funds**
   - Determine which fund data files exist in the data folder
   - For each fund, load its holdings data for the target quarter

3. **Search for the CUSIP in each fund's holdings**
   - Filter holdings to rows matching the target CUSIP
   - If found, extract the market value and fund manager name
   - If not found, record that this fund does not hold the security

4. **Aggregate results**
   - Create a summary table with fund manager name and total market value invested in the security
   - Sort by market value in descending order

5. **Select top results**
   - Rank funds by market value invested (largest first)
   - Extract the top 3 fund manager names

6. **Validate the results**
   - Confirm that the top funds are known large investors (e.g., Berkshire Hathaway, Renaissance)
   - Spot-check a few holdings to verify CUSIP matches are correct
   - Flag if results seem unusual or incomplete