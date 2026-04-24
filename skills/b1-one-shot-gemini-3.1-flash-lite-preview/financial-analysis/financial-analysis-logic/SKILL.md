---
name: financial-analysis-logic
description: Logical patterns for comparing 13F holdings across quarters to determine net change.
---

# Financial Analysis Logic

When comparing quarterly 13F holdings (Q2 vs Q3), follow these steps:

1. **Accession Number Retrieval**: Locate the submission metadata for the target firm in both quarterly folders. The `COVERPAGE.tsv` or `SUBMISSION.tsv` usually links the manager name to an accession number.
2. **Holdings Data Loading**:
   - `INFOTABLE.tsv` contains the granular list of stocks held by the manager for that specific submission/accession.
   - Merge these tables using 'CUSIP' as the primary key.
3. **Change Calculation**:
   - Calculate value change: `delta_value = (Q3_value_held - Q2_value_held)`.
   - Sort by `delta_value` to identify increased/decreased investments.
4. **CUSIP Identification**: Always normalize CUSIP strings before comparison.
