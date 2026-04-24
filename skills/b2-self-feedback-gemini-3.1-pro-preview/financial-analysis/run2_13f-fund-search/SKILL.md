---
name: run2_13f-fund-search
description: How to correctly and robustly search for a fund manager's accession number in SEC 13F COVERPAGE.tsv.
---

## Overview
A critical first step in analyzing 13F data is identifying a fund manager's unique `ACCESSION_NUMBER`. Since names can be slightly misspelled or appended with corporate entities (like "LLC", "LP"), searching requires flexibility.

## Usage Patterns

### Fast Search with `grep`
The fastest and most reliable way to find the accession number is often via the command line using `grep -i` (case-insensitive search).

```bash
# Search for Renaissance Technologies in Q3 2025
grep -i "renaissance technologies" /root/2025-q3/COVERPAGE.tsv
```

### Programmatic Search with `pandas`
When writing a script, use pandas with `.str.contains` rather than exact matching.

```python
import pandas as pd

quarter = "2025-q3"
keywords = "BERKSHIRE HATHAWAY"

# Use dtype=str to avoid dropping leading zeros in IDs and to handle missing values cleanly
df = pd.read_csv(f"/root/{quarter}/COVERPAGE.tsv", sep="\t", dtype=str)

# Filter out amendments if you only want the original or final holdings report
df = df[df["REPORTTYPE"].str.contains("HOLDINGS REPORT", na=False)]

matches = df[df["FILINGMANAGER_NAME"].str.contains(keywords, case=False, na=False)]
print(matches[["ACCESSION_NUMBER", "FILINGMANAGER_NAME"]])
```
