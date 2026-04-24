---
name: sec-13f-analysis
description: Parse and analyze SEC 13-F filing TSV datasets to extract AUM, holdings count, and fund details by accession number.
---

# SEC 13-F Analysis Skill

## Overview
SEC Form 13-F datasets consist of TSV files downloaded from EDGAR. Each quarter has the same file structure.

## Key Files
| File | Purpose |
|------|---------|
| `COVERPAGE.tsv` | Fund identity: `FILINGMANAGER_NAME`, `ACCESSION_NUMBER`, `REPORTCALENDARORQUARTER` |
| `SUMMARYPAGE.tsv` | Aggregated stats: `TABLEVALUETOTAL` (AUM in thousands), `TABLEENTRYTOTAL` (number of holdings) |
| `INFOTABLE.tsv` | Individual holdings: `CUSIP`, `NAMEOFISSUER`, `VALUE` (thousands), `SSHPRNAMT` (shares) |
| `SUBMISSION.tsv` | Filer metadata |

## Common Tasks

### Load data with pandas
```python
import pandas as pd

q3_dir = "/root/2025-q3"
coverpage = pd.read_csv(f"{q3_dir}/COVERPAGE.tsv", sep="\t", dtype=str)
summarypage = pd.read_csv(f"{q3_dir}/SUMMARYPAGE.tsv", sep="\t", dtype=str)
infotable = pd.read_csv(f"{q3_dir}/INFOTABLE.tsv", sep="\t", dtype=str)
```

### Get AUM for a fund (by accession_number)
```python
row = summarypage[summarypage["ACCESSION_NUMBER"] == accession_number]
aum_thousands = int(row["TABLEVALUETOTAL"].iloc[0])
aum_dollars = aum_thousands * 1000
```

### Get holdings count
```python
holdings = infotable[infotable["ACCESSION_NUMBER"] == accession_number]
num_holdings = len(holdings)
# Or use TABLEENTRYTOTAL from SUMMARYPAGE for the reported count
```

### Get holdings detail
```python
holdings = infotable[infotable["ACCESSION_NUMBER"] == accession_number].copy()
holdings["VALUE"] = pd.to_numeric(holdings["VALUE"], errors="coerce")
holdings["SSHPRNAMT"] = pd.to_numeric(holdings["SSHPRNAMT"], errors="coerce")
```

## Notes
- `VALUE` in INFOTABLE is in thousands of USD
- `TABLEVALUETOTAL` in SUMMARYPAGE is also in thousands of USD
- `TABLEENTRYTOTAL` is the number of positions reported
