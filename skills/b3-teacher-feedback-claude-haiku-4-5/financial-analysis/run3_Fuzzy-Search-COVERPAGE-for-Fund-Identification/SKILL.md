---
name: Fuzzy-Search-COVERPAGE-for-Fund-Identification
description: Search the COVERPAGE dataset using fuzzy matching to locate a specific fund by name and extract its accession_number for subsequent analysis. Use this when you need to identify a fund's filing by partial or approximate name matching.
---

## Steps

1. **Load COVERPAGE data** from the appropriate quarter folder (`/root/2025-q2` or `/root/2025-q3`)
   - Read the COVERPAGE.txt file containing fund registration information

2. **Perform fuzzy matching** on the fund name field
   - Use fuzzy string matching library (e.g., `fuzzywuzzy`) to find best match against search term
   - Set a reasonable similarity threshold (e.g., 80+) to filter candidates
   - Return top match with highest similarity score

3. **Validate the match**
   - Confirm the matched fund name aligns with expected fund characteristics
   - If multiple high-confidence matches exist, manually verify which is correct

4. **Extract accession_number**
   - Retrieve the accession_number field from the matched record
   - This accession_number is required for all subsequent fund detail lookups

5. **Document the match quality**
   - Record the similarity score and matched fund name for audit purposes
   - Note if manual verification was required