name: 13f-search
description: How to search for fund managers and stock CUSIPs in SEC 13F data. Use this skill whenever you need to find an accession number for a fund name or a CUSIP for a company name in the 13F datasets.

# 13F Search Skill

This skill provides workflows for identifying specific entities within the SEC 13F datasets (found in directories like `2025-q2` and `2025-q3`).

## Finding a Fund's Accession Number

To find the `ACCESSION_NUMBER` for a specific fund manager:
1. Use `grep` or `awk` to search the `COVERPAGE.tsv` file in the relevant quarter's directory.
2. The `FILINGMANAGER_NAME` column contains the fund name.
3. Perform a case-insensitive search for the fund name.
4. Note that some funds may have multiple filings; usually, the one with `ISAMENDMENT` as 'N' or the latest amendment is preferred unless specified.

Example:
```bash
grep -i "Renaissance Technologies" /root/2025-q3/COVERPAGE.tsv | cut -f1,10
```

## Finding a Stock's CUSIP

To find the `CUSIP` for a company:
1. Search the `INFOTABLE.tsv` file for the company name in the `NAMEOFISSUER` column.
2. Stock names in 13F filings are often abbreviated or formatted in all caps (e.g., "PALANTIR TECHNOLOGIES INC").
3. Use `grep -i` to find potential matches and extract the unique CUSIP.

Example:
```bash
grep -i "PALANTIR" /root/2025-q3/INFOTABLE.tsv | cut -f3,5 | sort -u
```

## Tips for Fuzzy Matching
- If a direct grep fails, try searching for unique parts of the name.
- Be aware of common suffixes like "LLC", "INC", "LP".
- For major funds like "Berkshire Hathaway", search for "BERKSHIRE HATHAWAY".
