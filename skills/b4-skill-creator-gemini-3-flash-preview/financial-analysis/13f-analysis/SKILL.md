name: 13f-analysis
description: How to extract AUM, count holdings, and compare quarterly changes in 13F filings. Use this skill when calculating fund metrics or analyzing investment shifts between quarters.

# 13F Analysis Skill

This skill covers data extraction and comparison logic for SEC 13F filings.

## Extracting AUM (Assets Under Management)

The total value of reported holdings can be found in `SUMMARYPAGE.tsv` or by summing the `VALUE` column in `INFOTABLE.tsv`.
1. Join `COVERPAGE.tsv` with `SUMMARYPAGE.tsv` using `ACCESSION_NUMBER`.
2. The `TABLEVALUETOTAL` column in `SUMMARYPAGE.tsv` represents the total value in thousands of dollars.
3. To get the dollar amount, multiply `TABLEVALUETOTAL` by 1000.

## Counting Held Stocks

1. The `TABLEENTRYTOTAL` column in `SUMMARYPAGE.tsv` often provides the count of line items.
2. For unique stocks, count the number of unique `CUSIP`s associated with an `ACCESSION_NUMBER` in `INFOTABLE.tsv`.

## Comparing Quarterly Changes

To compare changes between Q2 and Q3 for a fund:
1. Identify the `ACCESSION_NUMBER` for the fund in both quarters.
2. Extract the `CUSIP` and `VALUE` (or `SSHPRNAMT` for shares) from `INFOTABLE.tsv` for both quarters.
3. Join the datasets on `CUSIP`.
4. Calculate the difference: `Change = Value_Q3 - Value_Q2`.
5. Rank by the absolute or relative change as requested.

## Finding Top Holders of a Stock

To find which funds hold the most of a specific stock:
1. Identify the `CUSIP` for the stock.
2. Filter `INFOTABLE.tsv` by that `CUSIP`.
3. Join with `COVERPAGE.tsv` on `ACCESSION_NUMBER` to get the `FILINGMANAGER_NAME`.
4. Sort by `VALUE` or `SSHPRNAMT` in descending order.
