---
name: run2_csv_generation
description: Robust JSON-to-CSV parser for Trivy vulnerability reports.
---

# Improved CSV Generation

A Python utility to extract vulnerability data from Trivy's JSON structure.

## Processing Logic
1. Load the JSON report.
2. Iterate `Results` -> `Vulnerabilities`.
3. Extract `PkgName`, `InstalledVersion`, `VulnerabilityID`, `Severity`, `CVSS` (checking nvd, ghsa, redhat sources), `FixedVersion` (if any), `Title`, `PrimaryURL`.
4. Use `csv.DictWriter` for clean field escaping.

## Best Practice
- Always provide a fallback string (e.g., "N/A") for missing fields to avoid runtime `KeyError`.
- Ensure the CSV is opened with `newline=""` to prevent extra lines in some OS environments.
