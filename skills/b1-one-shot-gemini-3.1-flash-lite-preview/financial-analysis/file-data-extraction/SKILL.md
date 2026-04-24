---
name: file-data-extraction
description: Techniques for parsing TSV/JSON files for financial reporting data (13F).
---

# File Data Extraction

When dealing with 13F financial data, the primary data formats encountered are TSV (Tab Separated Values) and JSON.

## Parsing TSV
TSV files (like COVERPAGE.tsv and INFOTABLE.tsv) should be treated as structured datasets. Use `pandas` in Python to quickly aggregate, filter, and compare data.

Example snippet:
```python
import pandas as pd

# Load TSV
df = pd.read_csv('COVERPAGE.tsv', sep='\t')
# Filter for specific fund
fund_data = df[df['name'].str.contains('RENAISSANCE TECHNOLOGIES', case=False)]
```

## Parsing JSON
Metadata files often use JSON. Use the standard `json` library or `pandas.read_json` for consistency with TSV processing.
