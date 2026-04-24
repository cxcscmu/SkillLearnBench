---
name: security-audit-csv-reporting
description: Generate structured CSV security audit reports from vulnerability data with proper filtering, formatting, and field mapping.
---

# Security Audit CSV Reporting

## Overview
Converting vulnerability data into CSV format for audit trails, compliance reporting, and stakeholder communication.

## CSV Schema

Standard security audit CSV columns:

```
Package,Version,CVE_ID,Severity,CVSS_Score,Fixed_Version,Title,Url
```

### Field Definitions

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| Package | String | Package/library name | lodash |
| Version | String | Installed version | 4.17.20 |
| CVE_ID | String | CVE identifier | CVE-2021-23337 |
| Severity | String | HIGH or CRITICAL | HIGH |
| CVSS_Score | Float/String | CVSS v3 score (0-10) | 7.5 or N/A |
| Fixed_Version | String | Version with fix or N/A | 4.17.21 |
| Title | String | Vulnerability title/description | Prototype Pollution |
| Url | String | Reference URL | https://nvd.nist.gov/vuln/detail/CVE-2021-23337 |

## Implementation Pattern

```python
import csv
import json
from typing import List, Dict

def generate_security_audit_csv(vulnerabilities: List[Dict], output_file: str):
    """
    Generate security audit CSV from vulnerability data.

    vulnerabilities: List of vulnerability dictionaries
    output_file: Path to output CSV file
    """

    fieldnames = ['Package', 'Version', 'CVE_ID', 'Severity',
                  'CVSS_Score', 'Fixed_Version', 'Title', 'Url']

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for vuln in vulnerabilities:
            row = {
                'Package': vuln.get('package', 'N/A'),
                'Version': vuln.get('version', 'N/A'),
                'CVE_ID': vuln.get('cve_id', 'N/A'),
                'Severity': vuln.get('severity', 'N/A'),
                'CVSS_Score': vuln.get('cvss_score', 'N/A'),
                'Fixed_Version': vuln.get('fixed_version', 'N/A'),
                'Title': vuln.get('title', 'N/A'),
                'Url': vuln.get('url', 'N/A')
            }
            writer.writerow(row)
```

## Filtering and Sorting

### Filter by Severity

```python
def filter_by_severity(vulnerabilities, severity_levels=['HIGH', 'CRITICAL']):
    """Filter vulnerabilities to only specified severity levels"""
    return [v for v in vulnerabilities if v.get('severity') in severity_levels]
```

### Sort by Severity and CVSS

```python
def sort_vulnerabilities(vulnerabilities):
    """Sort by severity (CRITICAL first) then by CVSS score (descending)"""

    severity_order = {'CRITICAL': 0, 'HIGH': 1}

    def sort_key(vuln):
        severity = severity_order.get(vuln.get('severity'), 2)
        # Handle N/A CVSS scores
        cvss = float(vuln.get('cvss_score', 0)) if vuln.get('cvss_score') != 'N/A' else 0
        return (severity, -cvss)

    return sorted(vulnerabilities, key=sort_key)
```

## Data Cleaning

### Sanitize CSV Fields

```python
def sanitize_field(value):
    """Sanitize field for CSV output"""
    if value is None:
        return 'N/A'
    if isinstance(value, list):
        return '; '.join(str(v) for v in value)
    return str(value).strip()

def prepare_row(vuln_data):
    """Prepare vulnerability record for CSV output"""
    return {k: sanitize_field(v) for k, v in vuln_data.items()}
```

## Usage

Use this skill when:
- Converting vulnerability scan results to audit format
- Creating compliance reports
- Sharing findings with stakeholders
- Building automated security audit pipelines
- Archiving vulnerability data for historical tracking

## Related Skills

- `trivy-vulnerability-scanning`: Source of vulnerability data
- `cvss-score-extraction`: Enriching data with CVSS scores
