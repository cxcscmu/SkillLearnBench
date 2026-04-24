---
name: run2_13f-stock-search
description: How to find top fund managers heavily invested in a particular stock across all data quality issues.
---

## Overview
When searching for funds heavily invested in a single stock, be aware that `CUSIP` codes might be entered in varying cases (e.g. `69608A108` vs `69608a108`), so normalizations like `.str.upper()` are critical.

## Usage Patterns

### Finding Top Funds by Value
This strategy avoids issues with case sensitivity and missing commas when parsing `TITLEOFCLASS`.

```python
import pandas as pd

cusip = "69608A108"
quarter = "2025-q3"

infotable = pd.read_csv(f"/root/{quarter}/INFOTABLE.tsv", sep="\t", dtype=str)
coverpage = pd.read_csv(f"/root/{quarter}/COVERPAGE.tsv", sep="\t", dtype=str)

# Filter by CUSIP defensively
infotable["CUSIP_UPPER"] = infotable["CUSIP"].str.upper()
stock_holders = infotable[infotable["CUSIP_UPPER"] == cusip].copy()

# Sum the VALUE by ACCESSION_NUMBER
stock_holders["VALUE"] = stock_holders["VALUE"].astype(float)
fund_sums = stock_holders.groupby("ACCESSION_NUMBER")["VALUE"].sum().reset_index()

# Sort to get top 3
top_funds = fund_sums.sort_values(by="VALUE", ascending=False).head(3)

# Merge back to COVERPAGE to obtain FILINGMANAGER_NAME
merged = pd.merge(top_funds, coverpage[["ACCESSION_NUMBER", "FILINGMANAGER_NAME"]], on="ACCESSION_NUMBER", how="left")

print(merged[["FILINGMANAGER_NAME", "VALUE"]])
```
