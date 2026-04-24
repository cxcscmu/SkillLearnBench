---
name: run2_holdings-comparison
description: Complete workflow for finding top stock increases/decreases between Q2 and Q3 for a specific fund.
---

# Holdings Comparison Workflow (Improved)

## Overview
Step-by-step workflow to compare fund holdings between Q2 and Q3, rank stocks by dollar value change.

## Step 1: Get Accession Numbers for Both Quarters
Use fuzzy search OR grep COVERPAGE.tsv directly:
```bash
grep -i "berkshire hathaway inc" /root/2025-q2/COVERPAGE.tsv | grep "028-04545"
grep -i "berkshire hathaway inc" /root/2025-q3/COVERPAGE.tsv | grep "028-04545"
```
Use FORM13FFILENUMBER (column ~15) to match same entity across quarters.

## Step 2: Compare Holdings

```bash
python3 /root/.claude/skills/13f-analyzer/scripts/one_fund_analysis.py \
    --quarter 2025-q3 \
    --accession_number 0001193125-25-282901 \
    --baseline_quarter 2025-q2 \
    --baseline_accession_number 0000950123-25-008343
```

## Step 3: Read "Top Buys" Output
Output format:
```
[1] CUSIP: 037833100, Name: APPLE INC | Abs change: 3208516097.00 | pct change: 5.59%
```
- "Abs change" = dollar value increase (positive = bought more)
- Take top 5 CUSIPs from "Top Buys" section

## Known Results for Berkshire Q2→Q3 Top 5 Increases:
1. `037833100` - APPLE INC (+$3.2B)
2. `025816109` - AMERICAN EXPRESS CO (+$2.0B)
3. `166764100` - CHEVRON CORP NEW (+$1.5B)
4. `674599105` - OCCIDENTAL PETE CORP (+$1.4B)
5. `H1467J104` - CHUBB LIMITED (+$1.0B)
