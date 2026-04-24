---
name: fuzzy-fund-search
description: Fuzzy search SEC 13-F COVERPAGE.tsv to find fund names and accession numbers by approximate name matching.
---

# Fuzzy Fund Search Skill

## Overview
Fund names in SEC filings may differ slightly from common names. Use fuzzy matching to find the best match.

## Method: Simple substring / case-insensitive search
```python
import pandas as pd

coverpage = pd.read_csv("/root/2025-q3/COVERPAGE.tsv", sep="\t", dtype=str)

# Case-insensitive substring search
results = coverpage[coverpage["FILINGMANAGER_NAME"].str.contains("renaissance", case=False, na=False)]
print(results[["ACCESSION_NUMBER", "FILINGMANAGER_NAME"]].to_string())
```

## Method: Using rapidfuzz for fuzzy matching
```python
from rapidfuzz import process, fuzz

coverpage = pd.read_csv("/root/2025-q3/COVERPAGE.tsv", sep="\t", dtype=str)
names = coverpage["FILINGMANAGER_NAME"].fillna("").tolist()

query = "renaissance technologies"
matches = process.extract(query, names, scorer=fuzz.token_sort_ratio, limit=5)
for match_name, score, idx in matches:
    print(f"Score: {score}, Name: {match_name}, Accession: {coverpage.iloc[idx]['ACCESSION_NUMBER']}")
```

## Method: Search CUSIP for a stock by name
```python
infotable = pd.read_csv("/root/2025-q3/INFOTABLE.tsv", sep="\t", dtype=str)

# Search by issuer name
results = infotable[infotable["NAMEOFISSUER"].str.contains("palantir", case=False, na=False)]
# Get unique CUSIPs
print(results[["CUSIP", "NAMEOFISSUER"]].drop_duplicates())
```

## Tips
- Fund names are often uppercase in filings (e.g., "RENAISSANCE TECHNOLOGIES LLC")
- Search both Q2 and Q3 data since accession numbers change per quarter
- Always verify with multiple search terms if first attempt returns no results
