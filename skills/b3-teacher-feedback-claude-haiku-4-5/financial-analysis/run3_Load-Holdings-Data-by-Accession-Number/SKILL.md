---
name: Load-Holdings-Data-by-Accession-Number
description: Retrieve and load the complete holdings dataset for a specific fund using its accession_number. Use this to access position-level details needed for AUM, stock count, and comparative analysis.
---

## Steps

1. **Construct the file path**
   - Use the accession_number to locate the holdings file in the data folder
   - Typical path structure: `/root/[quarter]/[accession_number]_holdings.txt` or similar
   - Check folder structure if path is unclear

2. **Load the holdings data**
   - Read the file into a DataFrame with appropriate delimiters
   - Preserve data types (especially numeric fields for share counts and values)

3. **Inspect loaded data**
   - Confirm number of rows matches expected holdings count
   - Verify all required columns are present: security identifiers, share count, market value, security type
   - Check for null values that might affect calculations

4. **Validate data integrity**
   - Spot-check a few rows for reasonable values (positive shares, positive values)
   - Confirm security identifiers (CUSIP, ticker) are properly formatted
   - Flag any data quality issues before proceeding

5. **Cache or store for reuse**
   - If the same accession_number is needed multiple times, store the DataFrame
   - Avoid reloading the same data multiple times in subsequent steps