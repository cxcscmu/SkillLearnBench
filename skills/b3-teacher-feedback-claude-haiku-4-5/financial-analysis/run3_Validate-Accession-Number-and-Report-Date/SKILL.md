---
name: Validate-Accession-Number-and-Report-Date
description: Confirm that the accession_number retrieved corresponds to the correct quarter and report date before using it for analysis. Use this to prevent analyzing data from the wrong quarter.
---

## Steps

1. **Retrieve metadata for the accession_number**
   - Look up the accession_number in the COVERPAGE or fund metadata
   - Extract the report_date or filing_date field

2. **Verify the quarter matches**
   - For Q3 2025 analysis: confirm report_date is June 30, 2025 (or close to it)
   - For Q2 2025 analysis: confirm report_date is March 31, 2025 (or close to it)
   - Do NOT proceed if the date belongs to a different quarter

3. **Check for multiple accession numbers**
   - If the same fund has multiple filings in the same folder, identify which is most recent
   - Use the filing_date to select the latest accession_number if needed

4. **Document the accession_number and date**
   - Record both the accession_number and its corresponding report_date
   - Use this in subsequent steps to ensure consistency

5. **Flag if wrong quarter**
   - If accession_number does not match the target quarter, perform fuzzy search again
   - Adjust search terms or thresholds if needed to find correct filing