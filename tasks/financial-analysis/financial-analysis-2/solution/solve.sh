#!/bin/bash

# Use this file to solve the task.
ls /root
ls /root/2025-q2
ls /root/2025-q3

cat > /tmp/solver.py << 'PYTHON_SCRIPT'
import pandas as pd
import json


q3_infotable = pd.read_csv("/root/2025-q3/INFOTABLE.tsv", sep="\t")
q3_coverpage = pd.read_csv("/root/2025-q3/COVERPAGE.tsv", sep="\t")
q2_infotable = pd.read_csv("/root/2025-q2/INFOTABLE.tsv", sep="\t")
q2_coverpage = pd.read_csv("/root/2025-q2/COVERPAGE.tsv", sep="\t")

answers = {}

bridgewater_accession = q3_coverpage[q3_coverpage["FILINGMANAGER_NAME"].str.lower() == "bridgewater associates, lp"].iloc[0]["ACCESSION_NUMBER"]
bridgewater_info = q3_infotable[q3_infotable["ACCESSION_NUMBER"] == bridgewater_accession]
answers["q1_answer"] = float(bridgewater_info["VALUE"].astype(float).sum())

title_class_of_stocks = [
    "com",
    "common stock",
    "cl a",
    "com new",
    "class a",
    "stock",
    "common",
    "com cl a",
    "com shs",
    "sponsored adr"
    "sponsored ads"
    "adr"
    "equity"
    "cmn"
    "cl b"
    "ord shs"
    "cl a com"
    "class a com"
    "cap stk cl a"
    "comm stk"
    "cl b new"
    "cap stk cl c"
    "cl a new"
    "foreign stock"
    "shs cl a",
]
answers["q2_answer"] = int(bridgewater_info["TITLEOFCLASS"].str.lower().isin(title_class_of_stocks).sum())

soros_accession_q3 = q3_coverpage[q3_coverpage["FILINGMANAGER_NAME"].str.lower() == "soros fund management llc"].iloc[0]["ACCESSION_NUMBER"]
soros_accession_q2 = q2_coverpage[q2_coverpage["FILINGMANAGER_NAME"].str.lower() == "soros fund management llc"].iloc[0]["ACCESSION_NUMBER"]
soros_q3_infotable = q3_infotable[(q3_infotable["ACCESSION_NUMBER"] == soros_accession_q3) & (q3_infotable["TITLEOFCLASS"].str.lower().isin(title_class_of_stocks))].groupby("CUSIP").agg({
    "NAMEOFISSUER": "first",
    "TITLEOFCLASS": "first",
    "VALUE": "sum",
})
soros_q2_infotable = q2_infotable[(q2_infotable["ACCESSION_NUMBER"] == soros_accession_q2) & (q2_infotable["TITLEOFCLASS"].str.lower().isin(title_class_of_stocks))].groupby("CUSIP").agg({
    "NAMEOFISSUER": "first",
    "TITLEOFCLASS": "first",
    "VALUE": "sum",
})
merged = pd.merge(soros_q3_infotable, soros_q2_infotable, how="outer", suffixes=("", "_base"), on="CUSIP")
merged["VALUE"] = merged["VALUE"].fillna(0)
merged["NAMEOFISSUER"] = merged["NAMEOFISSUER"].fillna(merged["NAMEOFISSUER_base"])
merged["VALUE_base"] = merged["VALUE_base"].fillna(0)
merged["ABS_CHANGE"] = merged["VALUE"] - merged["VALUE_base"]
merged["PCT_CHANGE"] = merged["ABS_CHANGE"] / merged["VALUE_base"].replace(0, 1)  # avoid division by zero
merged = merged.sort_values(by="ABS_CHANGE", ascending=False)
top_buys = merged[merged["ABS_CHANGE"] > 0].head(5)
answers["q3_answer"] = top_buys.index.tolist()

palantir_cusip = "69608A108"
q3_infotable_palantir = q3_infotable[q3_infotable["CUSIP"] == palantir_cusip]
q3_infotable_palantir.groupby("ACCESSION_NUMBER").agg({"VALUE": "sum"}).sort_values("VALUE", ascending=False).head(3)
top3_funds = []
for accession_number, row in q3_infotable_palantir.groupby("ACCESSION_NUMBER").agg({"VALUE": "sum"}).sort_values("VALUE", ascending=False).head(3).iterrows():
    filing_manager = q3_coverpage[q3_coverpage["ACCESSION_NUMBER"] == accession_number].iloc[0]["FILINGMANAGER_NAME"]
    top3_funds.append(filing_manager)
answers["q4_answer"] = top3_funds

json.dump(answers, open("/root/answers.json", "w"))
PYTHON_SCRIPT

python3 /tmp/solver.py
