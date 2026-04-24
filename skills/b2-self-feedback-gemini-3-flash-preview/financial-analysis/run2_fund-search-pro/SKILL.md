---
name: run2_fund-search-pro
description: Professional fund search with accession number verification and report type checking.
---

## Usage
When searching for a fund, always verify the `ACCESSION_NUMBER` and `REPORTCALENDARORQUARTER`.

```bash
python3 /root/.agents/skills/fuzzy-name-search/scripts/search_fund.py \
    --keywords "Fund Name" \
    --quarter 2025-q3
```

If the search returns multiple entities or unexpected results, use `grep` on `COVERPAGE.tsv` to see all related filings:
```bash
grep -i "Fund Name" /root/2025-q3/COVERPAGE.tsv
```
Pay attention to the report type (e.g., 13F-HR vs 13F-NT). Only HR reports contain the INFOTABLE.
