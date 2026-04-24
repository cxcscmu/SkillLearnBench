---
name: fuzzy-search
description: Fuzzy string matching for fund names and stock CUSIPs using thefuzz library.
---

# Fuzzy Search for 13-F Data

## Setup
```bash
pip install thefuzz python-Levenshtein
```

## Fund Name Search
```python
from thefuzz import fuzz, process

# Search in COVERPAGE for fund name
results = process.extract(search_term, cover['FILINGMANAGER_NAME'].tolist(), scorer=fuzz.token_sort_ratio, limit=5)
# Returns list of (match, score, index)
```

## Stock CUSIP Search by Issuer Name
```python
# Get unique issuers with CUSIPs
issuers = info[['NAMEOFISSUER','CUSIP']].drop_duplicates()
results = process.extract(stock_name, issuers['NAMEOFISSUER'].tolist(), scorer=fuzz.token_sort_ratio, limit=5)
```
