---
name: Compare-Holdings-Between-Quarters
description: Load holdings for the same fund in two different quarters, match positions by security identifier, and calculate the change in shares and market values. Use this to identify which securities received increased investment between reporting periods.
---

## Steps

1. **Obtain accession numbers for both quarters**
   - Retrieve accession_number for Q2 2025 and Q3 2025 using fuzzy search
   - Validate that each accession_number corresponds to correct report date
   - Document both accession numbers

2. **Load holdings for both quarters**
   - Load Q2 holdings data using Q2 accession_number
   - Load Q3 holdings data using Q3 accession_number
   - Apply stock-only filter to both datasets

3. **Match positions by security identifier**
   - Use CUSIP or ticker as the join key between Q2 and Q3 holdings
   - Create a merged DataFrame with both quarters' data side-by-side
   - Handle securities that appear in only one quarter

4. **Calculate changes**
   - For securities in both quarters: calculate change in share count
   - Calculate change in market value (Q3 value - Q2 value)
   - For securities only in Q3: treat Q2 as zero (new positions)
   - For securities only in Q2: treat as fully exited (divestment)

5. **Filter for increased investments**
   - Keep only securities where market value increased (positive change)
   - Rank by absolute dollar value increase (largest first)
   - Select top 5

6. **Validate results**
   - Spot-check a few positions to confirm calculations are correct
   - Verify that CUSIPs are properly formatted
   - Confirm that top increases align with expected holdings patterns