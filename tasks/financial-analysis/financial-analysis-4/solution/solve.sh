#!/bin/bash

# Use this file to solve the task.
ls /root
ls /root/2025-q2
ls /root/2025-q3

cat > /tmp/solver.py << 'PYTHON_SCRIPT'
import json

import pandas as pd

Q1_Q2_FUND = "pershing square capital management, l.p."
Q3_COMPARE_FUND = "soros fund management llc"
Q3_TOPK = 1
Q4_TARGET_CUSIP = "88160R101"  # Tesla
Q4_TOPK = 1

q3_infotable = pd.read_csv("/root/2025-q3/INFOTABLE.tsv", sep="\t")
q3_coverpage = pd.read_csv("/root/2025-q3/COVERPAGE.tsv", sep="\t")
q2_infotable = pd.read_csv("/root/2025-q2/INFOTABLE.tsv", sep="\t")
q2_coverpage = pd.read_csv("/root/2025-q2/COVERPAGE.tsv", sep="\t")

answers = {}

q1_fund_accession = q3_coverpage[q3_coverpage["FILINGMANAGER_NAME"].str.lower() == Q1_Q2_FUND].iloc[0]["ACCESSION_NUMBER"]
q1_fund_info = q3_infotable[q3_infotable["ACCESSION_NUMBER"] == q1_fund_accession]
answers["q1_answer"] = float(q1_fund_info["VALUE"].astype(float).sum())

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
answers["q2_answer"] = int(q1_fund_info["TITLEOFCLASS"].str.lower().isin(title_class_of_stocks).sum())

compare_accession_q3 = q3_coverpage[q3_coverpage["FILINGMANAGER_NAME"].str.lower() == Q3_COMPARE_FUND].iloc[0]["ACCESSION_NUMBER"]
compare_accession_q2 = q2_coverpage[q2_coverpage["FILINGMANAGER_NAME"].str.lower() == Q3_COMPARE_FUND].iloc[0]["ACCESSION_NUMBER"]
compare_q3_infotable = q3_infotable[
    (q3_infotable["ACCESSION_NUMBER"] == compare_accession_q3)
    & (q3_infotable["TITLEOFCLASS"].str.lower().isin(title_class_of_stocks))
].groupby("CUSIP").agg({
    "NAMEOFISSUER": "first",
    "TITLEOFCLASS": "first",
    "VALUE": "sum",
})
compare_q2_infotable = q2_infotable[
    (q2_infotable["ACCESSION_NUMBER"] == compare_accession_q2)
    & (q2_infotable["TITLEOFCLASS"].str.lower().isin(title_class_of_stocks))
].groupby("CUSIP").agg({
    "NAMEOFISSUER": "first",
    "TITLEOFCLASS": "first",
    "VALUE": "sum",
})
merged = pd.merge(compare_q3_infotable, compare_q2_infotable, how="outer", suffixes=("", "_base"), on="CUSIP")
merged["VALUE"] = merged["VALUE"].fillna(0)
merged["NAMEOFISSUER"] = merged["NAMEOFISSUER"].fillna(merged["NAMEOFISSUER_base"])
merged["VALUE_base"] = merged["VALUE_base"].fillna(0)
merged["ABS_CHANGE"] = merged["VALUE"] - merged["VALUE_base"]
merged["PCT_CHANGE"] = merged["ABS_CHANGE"] / merged["VALUE_base"].replace(0, 1)  # avoid division by zero
merged = merged.sort_values(by="ABS_CHANGE", ascending=False)
answers["q3_answer"] = merged[merged["ABS_CHANGE"] > 0].head(Q3_TOPK).index.tolist()

q3_target_infotable = q3_infotable[q3_infotable["CUSIP"] == Q4_TARGET_CUSIP]
top_funds = []
for accession_number, _ in (
    q3_target_infotable.groupby("ACCESSION_NUMBER").agg({"VALUE": "sum"}).sort_values("VALUE", ascending=False).head(Q4_TOPK).iterrows()
):
    filing_manager = q3_coverpage[q3_coverpage["ACCESSION_NUMBER"] == accession_number].iloc[0]["FILINGMANAGER_NAME"]
    top_funds.append(filing_manager)
answers["q4_answer"] = top_funds

json.dump(answers, open("/root/answers.json", "w"))
PYTHON_SCRIPT

python3 /tmp/solver.py
