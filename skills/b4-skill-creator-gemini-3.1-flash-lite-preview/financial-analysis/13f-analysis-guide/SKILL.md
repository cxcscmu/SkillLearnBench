---
name: 13f-analysis-guide
description: How to analyze 13F filings. Use this skill to process COVERPAGE.tsv, INFOTABLE.tsv, and metadata for hedge fund holdings and AUM.
---

# 13F Analysis Guide

Use this guide when tasked with analyzing hedge fund activity from SEC 13F filings stored in quarterly folders (e.g., /root/2025-q2).

## Data Sources
- `COVERPAGE.tsv`: Contains the `accession_number` and filer information.
- `INFOTABLE.tsv`: Contains the actual holdings (CUSIP, value, shares).
- `FORM13F_metadata.json`: Provides extra context.

## Workflow

### 1. Identify the Filer
Search for the fund name in `COVERPAGE.tsv` to get the `accession_number`.
```bash
grep -i "Fund Name" /root/2025-qX/COVERPAGE.tsv
```

### 2. Extract AUM
AUM is typically found in the `SUMMARYPAGE.tsv` or the `COVERPAGE` itself, depending on the structure. If absent, sum the value of all entries in `INFOTABLE.tsv` for that `accession_number`.

### 3. Analyze Holdings
Use `INFOTABLE.tsv` to count holdings (unique CUSIPs) or track changes between quarters.

## Common Tasks
- **Count Holdings**: Count the number of unique CUSIPs in `INFOTABLE.tsv`.
- **Compare Quarters**: Compare CUSIP-to-value mappings between two quarters to find increased investments.
- **Find CUSIP**: Search for stock names by CUSIP if a mapping file exists, or search across `INFOTABLE.tsv`.
