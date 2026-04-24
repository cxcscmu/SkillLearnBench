---
name: 13f-search
description: Search for fund accession numbers and stock CUSIPs using fuzzy matching.
---

## Overview

Use the provided scripts to find the unique identifier (ACCESSION_NUMBER) for a fund or the CUSIP for a stock.

## Usage

### Finding a Fund's Accession Number
To find the accession number for a fund in a specific quarter:
```bash
python3 /root/.agents/skills/fuzzy-name-search/scripts/search_fund.py --keywords "Fund Name" --quarter 2025-q3
```

### Finding a Stock's CUSIP
To find the CUSIP for a company:
```bash
python3 /root/.agents/skills/fuzzy-name-search/scripts/search_stock_cusip.py --keywords "Company Name"
```
