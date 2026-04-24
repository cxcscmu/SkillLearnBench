---
name: security-audit-csv-report
description: Generate structured CSV security audit reports from vulnerability data with proper formatting and schema validation. Use this skill whenever you need to export vulnerability records to CSV format with consistent field ordering, proper escaping, and RFC 4180 compliance.
---

# Security Audit CSV Report Generation

## Overview

This skill handles exporting vulnerability records to a properly formatted CSV file suitable for security audits and compliance reporting.

## CSV Schema

The report uses 8 columns in this exact order:

```
Package,Version,CVE_ID,Severity,CVSS_Score,Fixed_Version,Title,Url
```

### Column Definitions

| Column | Type | Example | Notes |
|--------|------|---------|-------|
| Package | String | express | Package name from npm |
| Version | String | 4.17.1 | Installed version |
| CVE_ID | String | CVE-2022-12345 | Standard CVE format |
| Severity | String | HIGH or CRITICAL | Only these two values in audit |
| CVSS_Score | Float/String | 7.5 or N/A | CVSS v3 score or "N/A" |
| Fixed_Version | String | 4.17.2 or N/A | Earliest patched version or "N/A" |
| Title | String | Description of vulnerability | Vulnerability title/summary |
| Url | String | https://... or N/A | Primary reference URL |

## CSV Format Requirements

### RFC 4180 Compliance

- Fields containing commas, quotes, or newlines must be quoted
- Double quotes inside quoted fields must be escaped: `"` → `""`
- Line endings: LF (`\n`)
- Character encoding: UTF-8
- No BOM (Byte Order Mark)

### Field-Specific Rules

**CVSS_Score:**
- Numeric values: `7.5` (not quoted)
- Missing scores: `N/A` (literal string)

**Url:**
- Full HTTPS URL or `N/A`
- If URL contains special characters, quote the entire field

**Title:**
- Max 500 characters recommended (quote if exceeds)
- Escape internal quotes: `Vulnerability in "package"` → `"Vulnerability in ""package"""`

**Package, Version, CVE_ID:**
- Should not require quoting in typical cases
- Always validate and quote if contains special chars

## Python Implementation

```python
import csv
from pathlib import Path

def write_audit_report(records, output_file):
    """
    Write vulnerability records to CSV file.

    Args:
        records: List of dicts with keys:
                 Package, Version, CVE_ID, Severity, CVSS_Score,
                 Fixed_Version, Title, Url
        output_file: Path to write CSV (str or Path)
    """
    fieldnames = [
        "Package",
        "Version",
        "CVE_ID",
        "Severity",
        "CVSS_Score",
        "Fixed_Version",
        "Title",
        "Url"
    ]

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames,
            quoting=csv.QUOTE_MINIMAL,
            lineterminator='\n'
        )

        # Write header
        writer.writeheader()

        # Write records
        for record in records:
            # Ensure all fields present (use N/A for missing)
            clean_record = {
                field: record.get(field, "N/A")
                for field in fieldnames
            }
            writer.writerow(clean_record)
```

## Data Validation Before Export

Before writing CSV, validate records:

```python
def validate_record(record):
    """Validate a vulnerability record."""
    required_fields = [
        "Package", "Version", "CVE_ID", "Severity",
        "CVSS_Score", "Fixed_Version", "Title", "Url"
    ]

    # Check all required fields present
    for field in required_fields:
        if field not in record:
            raise ValueError(f"Missing field: {field}")

    # Validate severity
    if record["Severity"] not in ["HIGH", "CRITICAL"]:
        raise ValueError(f"Invalid severity: {record['Severity']}")

    # Validate CVSS_Score (numeric or N/A)
    cvss = record["CVSS_Score"]
    if cvss != "N/A":
        try:
            float(cvss)
        except ValueError:
            raise ValueError(f"Invalid CVSS_Score: {cvss}")

    return True
```

## Sorting (Optional)

Consider sorting records by severity (CRITICAL first) then by CVSS score descending:

```python
def sort_records(records):
    """Sort by severity then CVSS score."""
    severity_order = {"CRITICAL": 0, "HIGH": 1}

    def sort_key(record):
        severity = severity_order.get(record["Severity"], 2)
        cvss = record.get("CVSS_Score", "N/A")
        cvss_numeric = float(cvss) if cvss != "N/A" else 0
        return (severity, -cvss_numeric)

    return sorted(records, key=sort_key)
```

## Complete Workflow Example

```python
def generate_audit_report(json_input, csv_output):
    """End-to-end: parse Trivy JSON → validate → write CSV."""

    # 1. Parse and process (using vulnerability-data-processing skill)
    records = process_vulnerabilities(json_input)

    # 2. Validate each record
    for record in records:
        validate_record(record)

    # 3. Sort for readability
    records = sort_records(records)

    # 4. Write CSV
    write_audit_report(records, csv_output)

    print(f"✓ Audit report written to {csv_output}")
    print(f"✓ Total vulnerabilities: {len(records)}")
    critical_count = sum(1 for r in records if r["Severity"] == "CRITICAL")
    high_count = sum(1 for r in records if r["Severity"] == "HIGH")
    print(f"  - CRITICAL: {critical_count}")
    print(f"  - HIGH: {high_count}")
```

## Verification

After generating CSV, verify:

1. **File exists and readable**: `ls -l security_audit.csv`
2. **Valid CSV**: `head -5 security_audit.csv` shows proper columns
3. **Record count**: `wc -l security_audit.csv` (includes header)
4. **Character encoding**: `file security_audit.csv` shows UTF-8
5. **No BOM**: `od -c security_audit.csv | head -1` should not show BOM

## Common Issues

| Issue | Solution |
|-------|----------|
| Commas in Title field | csv.DictWriter automatically quotes |
| Quotes in Title | Escape as `""` (csv module handles this) |
| Non-ASCII characters | Ensure UTF-8 encoding (default in Python 3) |
| Mixed line endings | Use `newline=''` and `lineterminator='\n'` |
| Empty records list | Still generates valid CSV with headers only |

## Output Example

```csv
Package,Version,CVE_ID,Severity,CVSS_Score,Fixed_Version,Title,Url
express,4.17.1,CVE-2022-12345,HIGH,7.5,4.17.2,Vulnerability in express body parser,https://nvd.nist.gov/vuln/detail/CVE-2022-12345
lodash,4.17.20,CVE-2021-23337,CRITICAL,9.8,4.17.21,Prototype pollution in lodash,https://nvd.nist.gov/vuln/detail/CVE-2021-23337
```

## Next Steps

Generated CSV is ready for:
- Import into security dashboards
- Email distribution to security teams
- Compliance reporting
- Tracking and remediation workflows
