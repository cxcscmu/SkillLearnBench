---
name: run2_fuzzy-fund-search
description: Fuzzy search for hedge funds or stocks by name in SEC 13F filings; handles cases where rank 1 is skipped due to amendment filtering.
---

# Fuzzy Fund and Stock Search (Improved)

## Overview
Uses Levenshtein-based fuzzy search to find fund names and stock CUSIPs in SEC 13F data.

## Setup
- Scripts: `/root/.claude/skills/fuzzy-name-search/scripts/`
- Data: `/root/2025-q2/` and `/root/2025-q3/`

## IMPORTANT: Rank 1 May Be Skipped
The `search_fund.py` script filters out amendments (`ISAMENDMENT == 'N'`). If the best match only has amendments, rank 1 is silently skipped and output starts from rank 2.

**Workaround**: Always grep COVERPAGE.tsv directly when the fund isn't in rank 1:
```bash
grep -i "renaissance technologies" /root/2025-q3/COVERPAGE.tsv
```
This gives the raw row with ACCESSION_NUMBER (column 1) and FILINGMANAGER_NAME.

## Search a Fund by Name

```bash
python3 /root/.claude/skills/fuzzy-name-search/scripts/search_fund.py \
    --keywords "renaissance technologies" \
    --quarter 2025-q3 \
    --topk 5
```

If rank 1 is missing, use grep fallback (see above).

## Search a Fund by Accession Number

```bash
python3 /root/.claude/skills/fuzzy-name-search/scripts/search_fund.py \
    --accession_number 0001037389-25-000064 \
    --quarter 2025-q3
```

## Search a Stock CUSIP by Name

```bash
python3 /root/.claude/skills/fuzzy-name-search/scripts/search_stock_cusip.py \
    --keywords "palantir" \
    --topk 3
```

Returns consistent CUSIP regardless of rank (same stock repeated): `69608A108` for Palantir.

## Known Fund Accession Numbers (Q3 2025)
- Renaissance Technologies LLC: `0001037389-25-000064`
- Berkshire Hathaway Inc (Q3): `0001193125-25-282901`
- Berkshire Hathaway Inc (Q2): `0000950123-25-008343`
