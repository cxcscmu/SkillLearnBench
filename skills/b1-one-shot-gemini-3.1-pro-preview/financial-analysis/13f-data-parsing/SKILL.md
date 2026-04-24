---
name: 13f-data-parsing
description: A skill for parsing and analyzing SEC Form 13F TSV files, including COVERPAGE, INFOTABLE, and SUMMARYPAGE, using pandas.
---

# 13F Data Parsing

This skill outlines how to process SEC Form 13F data structured as TSV files (COVERPAGE, INFOTABLE, SUMMARYPAGE, etc.).

## Requirements
- pandas
- dask (optional for large files)

## Common Operations

### 1. Loading the Data
Use `pd.read_csv` with `sep='\t'` to read the files. For large files like `INFOTABLE.tsv`, you might want to specify `dtype` or use `low_memory=False`.

```python
import pandas as pd

coverpage_df = pd.read_csv('COVERPAGE.tsv', sep='\t', low_memory=False)
infotable_df = pd.read_csv('INFOTABLE.tsv', sep='\t', low_memory=False)
summary_df = pd.read_csv('SUMMARYPAGE.tsv', sep='\t', low_memory=False)
```

### 2. Finding Fund Accession Number
The COVERPAGE contains the name of the institutional investment manager.
```python
# Assuming 'FILINGMANAGER_NAME' or similar column exists.
# We will use fuzzy matching to find the exact name.
```

### 3. Extracting Fund Details (AUM, Number of Holdings)
Once you have the `ACCESSION_NUMBER`, you can look it up in SUMMARYPAGE or INFOTABLE.
AUM can be calculated as the sum of `VALUEDOLLAR` (or similar column) in INFOTABLE for the specific accession number, or sometimes it's reported in SUMMARYPAGE. Number of holdings can be the count of rows in INFOTABLE for that accession number.

### 4. Analyzing Changes between Quarters
You can join INFOTABLEs from two quarters on `CUSIP` for a specific fund to find differences in share count or value.
