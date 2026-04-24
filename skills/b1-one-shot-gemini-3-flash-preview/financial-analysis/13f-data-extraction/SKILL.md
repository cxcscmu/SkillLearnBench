---
name: 13f-data-extraction
description: Extract AUM, holdings count, and detailed holding information for a specific fund.
---

## Overview

Extract summary and detailed information about a fund's holdings using its accession number.

## Usage

### Extract Fund Summary (AUM and Total Holdings)
```bash
python3 /root/.agents/skills/13f-analyzer/scripts/one_fund_analysis.py --accession_number <ACCESSION_NUMBER> --quarter 2025-q3
```

### Manual Extraction (Alternative)
- **AUM**: Found in `SUMMARYPAGE.tsv` under `TABLEVALUETOTAL` for a given `ACCESSION_NUMBER`.
- **Holdings Count**: Found in `SUMMARYPAGE.tsv` under `TABLEENTRYTOTAL`.
- **Detailed Holdings**: Found in `INFOTABLE.tsv` by filtering for `ACCESSION_NUMBER`.
