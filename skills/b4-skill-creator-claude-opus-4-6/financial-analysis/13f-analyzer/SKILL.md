---
name: 13f-analyzer
description: Perform data analysis on SEC 13-F filing datasets (TSV format) to obtain insights about fund activities such as number of holdings, AUM, and change of holdings between two quarters. Use this skill whenever analyzing hedge fund portfolios, comparing quarterly holdings, or working with SEC EDGAR 13F data files.
---

# 13F Filing Analyzer

## Dataset Structure

SEC 13F data comes as TSV files in quarterly folders (e.g., `/root/2025-q2/`, `/root/2025-q3/`):

| File | Purpose | Key Columns |
|------|---------|-------------|
| `COVERPAGE.tsv` | Filer metadata | `ACCESSION_NUMBER`, `FILINGMANAGER_NAME`, `REPORTCALENDARORQUARTER` |
| `INFOTABLE.tsv` | Individual holdings | `ACCESSION_NUMBER`, `NAMEOFISSUER`, `CUSIP`, `VALUE` (in thousands USD), `SSHPRNAMT` (shares) |
| `SUMMARYPAGE.tsv` | Filing summary | `ACCESSION_NUMBER`, `TABLEENTRYTOTAL` (count of holdings), `TABLEVALUETOTAL` (AUM in thousands) |

## Common Analysis Patterns

### Get Fund's Accession Number
Search `COVERPAGE.tsv` by `FILINGMANAGER_NAME` to get the fund's `ACCESSION_NUMBER` for a given quarter.

### Get AUM
Use the accession number to look up `TABLEVALUETOTAL` in `SUMMARYPAGE.tsv`. The value is in **thousands of USD**.

### Get Number of Holdings
Use `TABLEENTRYTOTAL` from `SUMMARYPAGE.tsv`.

### Compare Holdings Between Quarters
1. Get accession numbers for both quarters from COVERPAGE
2. Filter INFOTABLE by each accession number
3. Join on CUSIP and compute differences in VALUE or SSHPRNAMT
4. Rank by dollar value change (VALUE column, in thousands)

### Find Top Holders of a Stock
1. Find the stock's CUSIP from INFOTABLE (search by NAMEOFISSUER)
2. Filter all INFOTABLE rows matching that CUSIP
3. Join with COVERPAGE on ACCESSION_NUMBER to get fund names
4. Rank by VALUE (in thousands)

## Implementation Notes

- Use Python with pandas for efficient TSV processing
- TSV files use tab separator, read with `pd.read_csv(path, sep='\t')`
- INFOTABLE is large (~3M rows); filter early to reduce memory usage
- VALUE column is in thousands of USD
- ACCESSION_NUMBER is the join key across all tables
- When comparing quarters, some funds may have multiple filings (amendments); prefer non-amendment filings (`ISAMENDMENT` is empty or 'N')
