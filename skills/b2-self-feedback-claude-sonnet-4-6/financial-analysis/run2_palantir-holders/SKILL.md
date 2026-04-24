---
name: run2_palantir-holders
description: Find top fund managers holding a specific stock (by CUSIP) using a fixed version of the holding_analysis workflow.
---

# Stock Holders Analysis (Fixed Workflow)

## Overview
Find top-k fund managers holding a specific stock in a given quarter, with fund names resolved.

## Step 1: Find CUSIP
```bash
python3 /root/.claude/skills/fuzzy-name-search/scripts/search_stock_cusip.py --keywords "palantir" --topk 3
# Palantir CUSIP: 69608A108
```

## Step 2: Find Top Holders (Manual Python - avoids holding_analysis.py bug)

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

## Known Results for Palantir (Q3 2025):
1. VANGUARD GROUP INC - $39,017,133,374
2. BlackRock, Inc. - $34,409,511,965
3. STATE STREET CORP - $18,471,648,356

## Notes
- `holding_analysis.py` from the 13f-analyzer skill has a bug (hardcoded path missing quarter)
- VALUE in INFOTABLE is in thousands of dollars (multiply by 1000 for actual USD)
- Always resolve accession_number → fund name using COVERPAGE.tsv
