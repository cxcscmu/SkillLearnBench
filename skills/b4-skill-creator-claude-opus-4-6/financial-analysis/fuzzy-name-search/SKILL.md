---
name: fuzzy-name-search
description: Fuzzy search fund names in SEC 13F COVERPAGE data or stock names in INFOTABLE data. Use this skill whenever searching for a fund or stock by name when the exact spelling or format is uncertain, or when performing case-insensitive partial matching on SEC filing data.
---

# Fuzzy Name Search for 13F Data

## Fund Name Search

Search `COVERPAGE.tsv` column `FILINGMANAGER_NAME` using case-insensitive substring or fuzzy matching.

```python
import pandas as pd

cover = pd.read_csv('/root/2025-q3/COVERPAGE.tsv', sep='\t')
# Case-insensitive substring match
matches = cover[cover['FILINGMANAGER_NAME'].str.contains('renaissance', case=False, na=False)]
# Returns ACCESSION_NUMBER, FILINGMANAGER_NAME, etc.
```

### Handling Multiple Matches
- If multiple rows match, prefer non-amendment filings (`ISAMENDMENT` column is empty or 'N')
- If still ambiguous, pick the best name match

## Stock CUSIP Search

Search `INFOTABLE.tsv` column `NAMEOFISSUER` for a stock name, then extract the unique CUSIP.

```python
info = pd.read_csv('/root/2025-q3/INFOTABLE.tsv', sep='\t')
matches = info[info['NAMEOFISSUER'].str.contains('palantir', case=False, na=False)]
cusip = matches['CUSIP'].unique()
```

### Notes
- CUSIP is 9 characters and uniquely identifies a security
- A stock may have multiple entries in INFOTABLE (one per fund holding it)
- Use `.unique()` on CUSIP to deduplicate
