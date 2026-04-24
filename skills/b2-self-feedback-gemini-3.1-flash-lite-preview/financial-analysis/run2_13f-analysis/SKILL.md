---
name: run2_13f-analysis
description: Improved 13F dataset analysis functions (includes better handling of TSVs).
---
## Usage Patterns

### Search Fund Accession Number
`grep -i "FUND_NAME" COVERPAGE.tsv | awk -F'\t' '{print $1}'`

### Calculate Holdings Change
1. `awk -F'\t' '$1=="ACCESSION_Q2" {print $5, $7}' INFOTABLE.tsv > q2_h.tsv`
2. `awk -F'\t' '$1=="ACCESSION_Q3" {print $5, $7}' INFOTABLE.tsv > q3_h.tsv`
3. Use Python `pandas` to merge on `CUSIP` and calculate difference.
