---
name: run2_13f-holdings-comparison
description: How to accurately identify stocks that "received increased investment" by checking both share count and dollar value change.
---

## Overview
To determine if a fund truly invested more in a stock (rather than the stock simply going up in price), you must check if their total share count (`SSHPRNAMT`) increased.

## Usage Patterns

### Identifying True Buys
This script compares Q2 and Q3 data to find stocks where the manager actively purchased more shares (`SHARE_CHANGE > 0`), and ranks them by the total change in reported dollar value (`VALUE_CHANGE`).

```python
import pandas as pd

q2_acc = "0000950123-25-008343"
q3_acc = "0001193125-25-282901"

q2_info = pd.read_csv("/root/2025-q2/INFOTABLE.tsv", sep="\t", dtype=str)
q3_info = pd.read_csv("/root/2025-q3/INFOTABLE.tsv", sep="\t", dtype=str)

holdings_q2 = q2_info[q2_info["ACCESSION_NUMBER"] == q2_acc].copy()
holdings_q3 = q3_info[q3_info["ACCESSION_NUMBER"] == q3_acc].copy()

# Ensure numeric types
holdings_q2["SSHPRNAMT"] = holdings_q2["SSHPRNAMT"].astype(float)
holdings_q3["SSHPRNAMT"] = holdings_q3["SSHPRNAMT"].astype(float)
holdings_q2["VALUE"] = holdings_q2["VALUE"].astype(float)
holdings_q3["VALUE"] = holdings_q3["VALUE"].astype(float)

# Group by CUSIP to handle multiple lines per stock
sum_q2 = holdings_q2.groupby("CUSIP")[["SSHPRNAMT", "VALUE"]].sum().reset_index()
sum_q3 = holdings_q3.groupby("CUSIP")[["SSHPRNAMT", "VALUE"]].sum().reset_index()

# Merge and calculate changes
merged = pd.merge(sum_q2, sum_q3, on="CUSIP", how="outer", suffixes=("_q2", "_q3")).fillna(0)
merged["SHARE_CHANGE"] = merged["SSHPRNAMT_q3"] - merged["SSHPRNAMT_q2"]
merged["VALUE_CHANGE"] = merged["VALUE_q3"] - merged["VALUE_q2"]

# Filter for stocks where the manager actually purchased more shares
increased_shares = merged[merged["SHARE_CHANGE"] > 0]

# Rank by Dollar Value Increase
top_5 = increased_shares.sort_values(by="VALUE_CHANGE", ascending=False).head(5)
print(top_5[["CUSIP", "SHARE_CHANGE", "VALUE_CHANGE"]])
```
