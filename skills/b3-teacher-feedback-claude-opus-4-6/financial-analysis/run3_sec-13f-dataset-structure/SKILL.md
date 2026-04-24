---
name: sec-13f-dataset-structure
description: Understanding the structure of SEC 13F filing datasets stored in /root/2025-q2 and /root/2025-q3 folders, including available scripts and data files
---

## SEC 13F Dataset Structure

The datasets are stored in `/root/2025-q2` and `/root/2025-q3` folders.

### Check for Scripts Directory
The dataset likely comes with pre-built Python scripts. Check:
- `/root/2025-q3/scripts/` or `/root/2025-q2/scripts/`
- Common scripts: `search_fund.py`, `one_fund_analysis.py`, `holding_analysis.py`, `search_stock_cusip.py`

```bash
# First, explore the directory structure
find /root/2025-q2 -type f | head -40
find /root/2025-q3 -type f | head -40
ls -la /root/2025-q2/scripts/ 2>/dev/null
ls -la /root/2025-q3/scripts/ 2>/dev/null
ls -la /root/2025-q2/*.py 2>/dev/null
ls -la /root/2025-q3/*.py 2>/dev/null
```

**Always check the scripts first** and read their source code to understand how they handle data parsing, filtering, and deduplication. These scripts handle edge cases correctly.

### Data Files (TSV format)
Key TSV files typically found:
- `COVERPAGE.tsv` — Fund cover page info (filing metadata, accession numbers)
- `INFOTABLE.tsv` — Holdings data (stocks, CUSIPs, values, shares)
- `SUMMARYPAGE.tsv` — Summary info
- Other supporting files

### Key Columns in INFOTABLE.tsv
- `ACCESSION_NUMBER` — Links to COVERPAGE
- `NAMEOFISSUER` — Company name
- `CUSIP` — Stock identifier (9-character)
- `VALUE` — Value in thousands of dollars
- `SSHPRNAMT` — Number of shares/principal amount
- `SSHPRNAMTTYPE` — Type: "SH" for shares, "PRN" for principal
- `PUTCALL` — If populated with "PUT" or "CALL", it's an option, not a stock
- `INVESTMENTDISCRETION` — Type of discretion

### Critical: PUTCALL Column Values
The PUTCALL column may contain unexpected values. Always inspect:
```python
import pandas as pd
info = pd.read_csv('/root/2025-q3/INFOTABLE.tsv', sep='\t')
print(info['PUTCALL'].unique())
print(info['PUTCALL'].value_counts(dropna=False))
```