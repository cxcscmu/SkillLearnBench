---
name: run2_stock-analysis-pro
description: Robust stock analysis and holder identification, bypassing file path issues in default scripts.
---

## Usage
### Search CUSIP
```bash
python3 /root/.agents/skills/fuzzy-name-search/scripts/search_stock_cusip.py --keywords "Palantir"
```

### Top Holders Analysis
The `holding_analysis.py` script may have incorrect paths. Use `awk` for a direct and reliable analysis of `INFOTABLE.tsv`:

```bash
# Sum VALUE (col 7) by ACCESSION_NUMBER (col 1) for a specific CUSIP (col 5)
awk -F'\t' '$5 == "CUSIP_HERE" {sum[$1] += $7} END {for (a in sum) print a, sum[a]}' /root/2025-q3/INFOTABLE.tsv | sort -k2 -nr | head -n 3
```

Then look up the names in `COVERPAGE.tsv`:
```bash
grep "ACCESSION_NUMBER" /root/2025-q3/COVERPAGE.tsv
```
