---
name: sec-13f-search-fund-coverpage
description: How to fuzzy search for a fund in COVERPAGE.tsv to find its accession_number, using either built-in scripts or manual search
---

## Searching for a Fund in COVERPAGE

### Method 1: Use Built-in Scripts (Preferred)
```bash
# Check if search script exists
cat /root/2025-q3/scripts/search_fund.py 2>/dev/null
# Run it if available
python /root/2025-q3/scripts/search_fund.py "renaissance technologies" 2>/dev/null
python /root/2025-q3/scripts/search_fund.py "berkshire hathaway" 2>/dev/null
```

### Method 2: Manual Fuzzy Search in COVERPAGE.tsv
```python
import pandas as pd

cover = pd.read_csv('/root/2025-q3/COVERPAGE.tsv', sep='\t', low_memory=False)

# Print columns to understand structure
print(cover.columns.tolist())

# Fuzzy search by fund name - check various possible column names
# Common column names: FILINGMANAGER_NAME, COMPANY_NAME, etc.
search_term = "renaissance technologies"
for col in cover.columns:
    if 'name' in col.lower() or 'manager' in col.lower() or 'company' in col.lower():
        print(f"Column: {col}")
        matches = cover[cover[col].astype(str).str.lower().str.contains(search_term, na=False)]
        if len(matches) > 0:
            print(matches[[col, 'ACCESSION_NUMBER']].head(10))
```

### Getting the Accession Number
The accession_number from COVERPAGE links to INFOTABLE for holdings data.

```python
# Example: find Renaissance Technologies
search = "renaissance"
name_col = 'FILINGMANAGER_NAME'  # adjust based on actual column name
matches = cover[cover[name_col].astype(str).str.lower().str.contains(search, na=False)]
print(matches[['ACCESSION_NUMBER', name_col]].drop_duplicates())
# Pick the best matching accession_number
accession = matches['ACCESSION_NUMBER'].iloc[0]
```