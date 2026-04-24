---
name: fuzzy-string-matching
description: A skill for finding best string matches in datasets using fuzzy matching libraries like fuzzywuzzy or rapidfuzz.
---

# Fuzzy String Matching

This skill demonstrates how to use fuzzy string matching to find company or fund names in a dataset.

## Requirements
- `fuzzywuzzy` or `rapidfuzz`
- `python-Levenshtein` (optional but recommended for speed)

## Installation
```bash
pip install rapidfuzz
```

## Usage

```python
import pandas as pd
from rapidfuzz import process, fuzz

df = pd.read_csv('data.tsv', sep='\t')
names = df['NAME_COLUMN'].dropna().unique()

# Find the best match
query = "Renaissance Technologies"
best_match = process.extractOne(query, names, scorer=fuzz.token_sort_ratio)

print(f"Best match: {best_match[0]} with score {best_match[1]}")
```
