---
name: holdings-comparison
description: Compare fund holdings between two quarters (Q2 vs Q3) to identify increased/decreased positions by dollar value or share count.
---

# Holdings Comparison Skill

## Overview
To compare holdings across quarters, load INFOTABLE for both quarters, filter by accession number, then compute the difference in VALUE or SSHPRNAMT.

## Step-by-step

### 1. Get accession numbers for both quarters
```python
import pandas as pd

q2_cover = pd.read_csv("/root/2025-q2/COVERPAGE.tsv", sep="\t", dtype=str)
q3_cover = pd.read_csv("/root/2025-q3/COVERPAGE.tsv", sep="\t", dtype=str)

q2_acc = q2_cover[q2_cover["FILINGMANAGER_NAME"].str.contains("berkshire", case=False, na=False)]["ACCESSION_NUMBER"].iloc[0]
q3_acc = q3_cover[q3_cover["FILINGMANAGER_NAME"].str.contains("berkshire", case=False, na=False)]["ACCESSION_NUMBER"].iloc[0]
```

### 2. Load holdings for both quarters
```python
q2_info = pd.read_csv("/root/2025-q2/INFOTABLE.tsv", sep="\t", dtype=str)
q3_info = pd.read_csv("/root/2025-q3/INFOTABLE.tsv", sep="\t", dtype=str)

q2_holdings = q2_info[q2_info["ACCESSION_NUMBER"] == q2_acc].copy()
q3_holdings = q3_info[q3_info["ACCESSION_NUMBER"] == q3_acc].copy()

q2_holdings["VALUE"] = pd.to_numeric(q2_holdings["VALUE"], errors="coerce").fillna(0)
q3_holdings["VALUE"] = pd.to_numeric(q3_holdings["VALUE"], errors="coerce").fillna(0)
```

### 3. Merge and compute changes
```python
# Aggregate by CUSIP (a fund may have multiple entries per stock for different share types)
q2_agg = q2_holdings.groupby("CUSIP")["VALUE"].sum().reset_index().rename(columns={"VALUE": "VALUE_Q2"})
q3_agg = q3_holdings.groupby("CUSIP")["VALUE"].sum().reset_index().rename(columns={"VALUE": "VALUE_Q3"})

merged = pd.merge(q2_agg, q3_agg, on="CUSIP", how="outer").fillna(0)
merged["CHANGE"] = merged["VALUE_Q3"] - merged["VALUE_Q2"]

# Top 5 increased positions
top5 = merged.sort_values("CHANGE", ascending=False).head(5)
print(top5[["CUSIP", "VALUE_Q2", "VALUE_Q3", "CHANGE"]])
```

### 4. Find top investors in a specific stock
```python
# Find all funds holding a specific CUSIP in Q3
palantir_cusip = "69608A108"  # example
holders = q3_info[q3_info["CUSIP"] == palantir_cusip].copy()
holders["VALUE"] = pd.to_numeric(holders["VALUE"], errors="coerce").fillna(0)

# Aggregate by accession number and merge with fund names
holders_agg = holders.groupby("ACCESSION_NUMBER")["VALUE"].sum().reset_index()
holders_with_names = holders_agg.merge(q3_cover[["ACCESSION_NUMBER", "FILINGMANAGER_NAME"]], on="ACCESSION_NUMBER")
top3 = holders_with_names.sort_values("VALUE", ascending=False).head(3)
print(top3[["FILINGMANAGER_NAME", "VALUE"]])
```

## Notes
- Always aggregate by CUSIP before comparing (avoid double-counting from multiple lot entries)
- VALUE is in thousands USD in all TSV files
- New positions (not in Q2) will have VALUE_Q2 = 0
- Closed positions will have VALUE_Q3 = 0; exclude from "increased" analysis
