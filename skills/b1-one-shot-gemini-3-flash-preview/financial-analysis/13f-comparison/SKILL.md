---
name: 13f-comparison
description: Compare holdings between two quarters or find top holders of a specific stock.
---

## Overview

Analyze changes in investment strategy across quarters or identify major institutional holders of a stock.

## Usage

### Compare Holdings Between Quarters
```bash
python3 /root/.agents/skills/13f-analyzer/scripts/one_fund_analysis.py \
    --quarter 2025-q3 --accession_number <Q3_ACCESSION> \
    --baseline_quarter 2025-q2 --baseline_accession_number <Q2_ACCESSION>
```

### Find Top Holders of a Stock
```bash
python3 /root/.agents/skills/13f-analyzer/scripts/holding_analysis.py --cusip <CUSIP> --quarter 2025-q3 --topk 3
```
