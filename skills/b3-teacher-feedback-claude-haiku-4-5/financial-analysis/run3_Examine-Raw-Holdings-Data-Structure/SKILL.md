---
name: Examine-Raw-Holdings-Data-Structure
description: Inspect the actual holdings dataset to understand its schema, field names, and data patterns before applying filters. Use this to identify the correct field name that distinguishes equity securities from bonds, options, warrants, and other non-stock instruments.
---

## Steps

1. **Load holdings data** for the target fund and quarter
   - Use the accession_number to locate the correct holdings file
   - Load a sample (e.g., first 50 rows) into memory

2. **Inspect the schema**
   - Print all column names and their data types
   - Look for fields related to security type, asset class, or instrument classification

3. **Examine sample records** from different security categories
   - Manually inspect 10-20 records to understand how stocks, bonds, options, and warrants are represented
   - Note the exact values in the security classification field(s)
   - Check for patterns in CUSIP format by security type

4. **Identify the authoritative classification field**
   - Determine the primary field name used to filter equity vs. non-equity
   - Document acceptable values for stocks (e.g., "STOCK", "EQUITY", "COMMON STOCK")
   - Document values to exclude (e.g., "BOND", "OPTION", "WARRANT", "PREFERRED", "FUND")

5. **Test filtering logic on samples**
   - Apply the filter to your 10-20 sample records
   - Verify that non-stocks are removed and stocks are retained
   - Adjust filter logic if needed before running on full dataset