---
name: run2_13f-fund-summary
description: How to calculate a fund's actual AUM and total unique stock count for modern SEC 13F data.
---

## Overview
Starting in 2023, the SEC began requiring funds to report exact dollar amounts in the `SUMMARYPAGE.tsv` and `INFOTABLE.tsv` `VALUE` columns, replacing the old system where values were reported in thousands.

## Usage Patterns

### Calculating True AUM
The total value is now precisely reported in exact dollars.

```python
import pandas as pd

accession_number = "0001037389-25-000064"
quarter = "2025-q3"

summary = pd.read_csv(f"/root/{quarter}/SUMMARYPAGE.tsv", sep="\t", dtype=str)
match = summary[summary["ACCESSION_NUMBER"] == accession_number]

if not match.empty:
    # 13F forms currently report VALUES in EXACT dollars (no longer in thousands)
    aum = float(match["TABLEVALUETOTAL"].iloc[0])
    print(f"Total AUM: ${aum:,.2f}")
```

### Counting Unique Stock Holdings
Since one CUSIP can have multiple rows (for different investment discretion types or voting authority), use `nunique()` on the `CUSIP` column.

```python
import pandas as pd

infotable = pd.read_csv(f"/root/2025-q3/INFOTABLE.tsv", sep="\t", dtype=str)
holdings = infotable[infotable["ACCESSION_NUMBER"] == "0001037389-25-000064"]

# Number of unique CUSIPs represents the total number of stocks held
unique_stocks = holdings["CUSIP"].nunique()
print(f"Number of Unique Stocks Held: {unique_stocks}")
```
