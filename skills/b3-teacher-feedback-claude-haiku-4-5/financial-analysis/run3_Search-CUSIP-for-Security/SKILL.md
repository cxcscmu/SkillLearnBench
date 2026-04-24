---
name: Search-CUSIP-for-Security
description: Find the CUSIP identifier for a specific security (e.g., Palantir) by searching across all holdings data or a security master file. Use this when you need to locate a specific stock across multiple fund positions.
---

## Steps

1. **Determine search scope**
   - Decide whether to search within a specific fund's holdings or across all available data
   - For broader searches, load a security master file or aggregate holdings across funds

2. **Prepare search terms**
   - Identify the security name or ticker to search for (e.g., "Palantir", "PLTR")
   - Decide if search should be exact, fuzzy, or case-insensitive

3. **Perform the search**
   - Search the security name or ticker field in holdings data
   - Use exact match for ticker symbols (case-insensitive)
   - Use fuzzy match for company names if needed

4. **Handle multiple matches**
   - If multiple securities match, identify the correct one by additional criteria
   - For stocks, prefer exact ticker matches over partial name matches
   - Verify against public market data if necessary

5. **Extract and validate CUSIP**
   - Retrieve the CUSIP from the matched record
   - Confirm CUSIP format (typically 9 alphanumeric characters for equities)
   - Document the security name and ticker alongside the CUSIP for reference

6. **Store for reuse**
   - Cache the CUSIP for use in subsequent steps (e.g., finding all funds holding this security)