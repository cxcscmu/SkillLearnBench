---
name: run2_13f-fund-analysis
description: Analyze fund AUM, holdings count, and cross-quarter investment changes from SEC 13F filings.
---

# 13F Fund Analysis (Improved)

## Overview
Analyze individual fund holdings and compare changes between quarters.

## Setup
- Scripts: `/root/.claude/skills/13f-analyzer/scripts/`
- Data format: `/root/{quarter}/INFOTABLE.tsv`, `/root/{quarter}/COVERPAGE.tsv`

## Analyze Single Fund (AUM, holdings count)

```bash
python3 /root/.claude/skills/13f-analyzer/scripts/one_fund_analysis.py \
    --accession_number 0001037389-25-000064 \
    --quarter 2025-q3
```

Output fields:
- `Total number of holdings`: all asset classes
- `Total AUM`: in USD dollars (float)
- `Number of stock holdings`: equities only
- `Total stock AUM`: equity AUM only

## Compare Fund Between Two Quarters

```bash
python3 /root/.claude/skills/13f-analyzer/scripts/one_fund_analysis.py \
    --quarter 2025-q3 \
    --accession_number 0001193125-25-282901 \
    --baseline_quarter 2025-q2 \
    --baseline_accession_number 0000950123-25-008343
```

Output: "Top 10 Buys" and "Top 10 Sells" ranked by `Abs change` (dollar value change).

## IMPORTANT: holding_analysis.py Has a Bug
The script uses hardcoded `/root/INFOTABLE.tsv` (missing quarter subdirectory). Use this Python workaround instead:

```python
import pandas as pd

quarter = '2025-q3'
cusip = '69608A108'
topk = 3

infotable = pd.read_csv(f'/root/{quarter}/INFOTABLE.tsv', sep='\t', dtype=str)
infotable['VALUE'] = infotable['VALUE'].astype(float)
holding_details = infotable[infotable['CUSIP'] == cusip]

top = (
    holding_details.groupby('ACCESSION_NUMBER')
    .agg(TOTAL_VALUE=('VALUE', 'sum'))
    .sort_values('TOTAL_VALUE', ascending=False)
    .head(topk)
)

coverpage = pd.read_csv(f'/root/{quarter}/COVERPAGE.tsv', sep='\t', dtype=str)

for idx, (accession_number, row) in enumerate(top.iterrows()):
    fund_info = coverpage[coverpage['ACCESSION_NUMBER'] == accession_number]
    fund_name = fund_info['FILINGMANAGER_NAME'].values[0] if not fund_info.empty else 'Unknown'
    print(f'Rank {idx+1}: {fund_name} | Value = {row["TOTAL_VALUE"]:.2f}')
```
