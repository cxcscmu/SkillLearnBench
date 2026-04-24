---
name: run2_csv-report-generation-advanced
description: Advanced CSV security report generation with validation, normalization, and comprehensive error handling
---

# Advanced CSV Security Report Generation

## Purpose
Generate production-ready CSV vulnerability reports with data validation, field normalization, and comprehensive error handling.

## CSV Schema with Validation

### Columns
```
Package,Version,CVE_ID,Severity,CVSS_Score,Fixed_Version,Title,Url
```

### Field Validation Rules

| Field | Validation | Example | Invalid Example |
|-------|-----------|---------|-----------------|
| Package | Non-empty, valid npm name | `lodash`, `@babel/core` | Empty, special chars only |
| Version | Semantic versioning | `4.17.20`, `1.0.0` | `latest`, `@latest` |
| CVE_ID | Format: CVE-YYYY-XXXXX | `CVE-2021-23337` | `CVE2021-23337`, `GHSA-...` |
| Severity | Exactly "HIGH" or "CRITICAL" | `HIGH`, `CRITICAL` | `High`, `MEDIUM`, `"HIGH"` |
| CVSS_Score | Numeric 0-10 or "N/A" | `7.5`, `9.8`, `N/A` | `10.1`, `HIGH`, empty |
| Fixed_Version | Version string or "N/A" | `4.17.21`, `N/A` | Empty, `fixed` |
| Title | Non-empty string, max 256 chars | `Prototype Pollution` | Empty |
| Url | Valid HTTP/HTTPS URL | `https://nvd.nist.gov/...` | `http://`, relative path |

## Data Normalization

### Package Name Normalization
```python
def normalize_package_name(pkg_name):
    """Normalize package name"""
    if not pkg_name or not isinstance(pkg_name, str):
        return ""
    return pkg_name.strip()
```

### Version Normalization
```python
def normalize_version(version):
    """Normalize version string"""
    if not version or not isinstance(version, str):
        return ""

    version = version.strip()

    # Remove common prefixes
    if version.startswith('v'):
        version = version[1:]

    # Return only the first version if multiple are listed
    if ',' in version:
        version = version.split(',')[0].strip()

    return version
```

### CVE ID Normalization
```python
def normalize_cve_id(cve_id):
    """Normalize and validate CVE ID"""
    if not cve_id or not isinstance(cve_id, str):
        return ""

    cve_id = cve_id.strip().upper()

    # Handle multiple CVEs
    if ',' in cve_id:
        cve_id = cve_id.split(',')[0].strip()

    # Validate format: CVE-YYYY-XXXXX
    import re
    if re.match(r'^CVE-\d{4}-\d+$', cve_id):
        return cve_id

    return ""  # Invalid format
```

### Severity Normalization
```python
def normalize_severity(severity):
    """Normalize severity to uppercase"""
    if not severity or not isinstance(severity, str):
        return ""

    severity = severity.strip().upper()

    if severity in ["HIGH", "CRITICAL"]:
        return severity

    return ""  # Invalid severity
```

### CVSS Score Normalization
```python
def normalize_cvss_score(score):
    """Normalize CVSS score to valid format"""
    if score is None or score == "" or str(score).upper() == "N/A":
        return "N/A"

    try:
        f_score = float(str(score).strip())

        # Validate CVSS range (0.0-10.0)
        if 0.0 <= f_score <= 10.0:
            # Format to 1 decimal place
            return f"{f_score:.1f}"
        else:
            return "N/A"  # Out of range

    except (ValueError, TypeError):
        return "N/A"  # Non-numeric
```

### Fixed Version Normalization
```python
def normalize_fixed_version(version):
    """Normalize fixed version"""
    if not version or not isinstance(version, str):
        return "N/A"

    version = version.strip()

    if not version or version.lower() == "n/a":
        return "N/A"

    # Extract first version if multiple
    if ',' in version:
        version = version.split(',')[0].strip()

    # Remove version prefix if present
    if version.startswith('v'):
        version = version[1:]

    return version if version else "N/A"
```

### Title Normalization
```python
def normalize_title(title):
    """Normalize vulnerability title"""
    if not title or not isinstance(title, str):
        return ""

    title = title.strip()

    # Truncate if too long (max 256 chars for CSV readability)
    if len(title) > 256:
        title = title[:253] + "..."

    # Remove newlines and extra whitespace
    title = " ".join(title.split())

    return title
```

### URL Normalization
```python
def normalize_url(url):
    """Normalize and validate URL"""
    if not url or not isinstance(url, str):
        return ""

    url = url.strip()

    # Must be HTTP or HTTPS
    if not url.startswith(('http://', 'https://')):
        return ""

    # Basic URL validation
    if len(url) > 2048:  # URLs shouldn't be this long
        return ""

    return url
```

## CSV Writing with Validation

### Complete Implementation
```python
import csv
from typing import List, Dict

class VulnerabilityReportWriter:
    """Write validated vulnerability data to CSV"""

    FIELDNAMES = ["Package", "Version", "CVE_ID", "Severity", "CVSS_Score",
                  "Fixed_Version", "Title", "Url"]

    def __init__(self, output_path: str):
        self.output_path = output_path
        self.valid_count = 0
        self.invalid_count = 0

    def write_report(self, vulnerabilities: List[Dict]) -> bool:
        """Write vulnerabilities with validation"""

        try:
            with open(self.output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.FIELDNAMES)
                writer.writeheader()

                for vuln in vulnerabilities:
                    row = self._validate_and_normalize(vuln)

                    if row:
                        writer.writerow(row)
                        self.valid_count += 1
                    else:
                        self.invalid_count += 1

            return self.valid_count > 0

        except Exception as e:
            print(f"[!] Error writing CSV: {e}")
            return False

    def _validate_and_normalize(self, vuln: Dict) -> Dict:
        """Validate and normalize a single vulnerability record"""

        # Normalize all fields
        normalized = {
            "Package": normalize_package_name(vuln.get("package")),
            "Version": normalize_version(vuln.get("version")),
            "CVE_ID": normalize_cve_id(vuln.get("cve_id")),
            "Severity": normalize_severity(vuln.get("severity")),
            "CVSS_Score": normalize_cvss_score(vuln.get("cvss_score")),
            "Fixed_Version": normalize_fixed_version(vuln.get("fixed_version")),
            "Title": normalize_title(vuln.get("title")),
            "Url": normalize_url(vuln.get("url"))
        }

        # Validate critical fields
        if not normalized["Package"]:
            print(f"[!] Invalid package name: {vuln.get('package')}")
            return None

        if not normalized["CVE_ID"]:
            print(f"[!] Invalid CVE ID: {vuln.get('cve_id')}")
            return None

        if not normalized["Severity"]:
            print(f"[!] Invalid severity: {vuln.get('severity')}")
            return None

        if not normalized["Version"]:
            print(f"[!] Invalid version: {vuln.get('version')}")
            return None

        return normalized

    def get_report_stats(self) -> Dict:
        """Get report generation statistics"""
        return {
            "valid_records": self.valid_count,
            "invalid_records": self.invalid_count,
            "total_processed": self.valid_count + self.invalid_count
        }
```

## Data Quality Checks

### Pre-Write Validation
```python
def validate_vulnerabilities(vulns: List[Dict]) -> List[str]:
    """Validate entire vulnerability dataset"""
    issues = []

    if not vulns:
        return ["No vulnerabilities to process"]

    # Check for duplicates
    seen = set()
    for vuln in vulns:
        key = (vuln.get("cve_id"), vuln.get("package"), vuln.get("version"))
        if key in seen:
            issues.append(f"Duplicate: {key}")
        seen.add(key)

    # Check for missing critical fields
    for i, vuln in enumerate(vulns):
        if not vuln.get("package"):
            issues.append(f"Row {i}: Missing package name")
        if not vuln.get("cve_id"):
            issues.append(f"Row {i}: Missing CVE ID")
        if not vuln.get("severity"):
            issues.append(f"Row {i}: Missing severity")

    return issues
```

## Output Verification

### Post-Write Validation
```python
def verify_csv_output(csv_path: str) -> bool:
    """Verify CSV file integrity after writing"""
    import os

    # Check file exists
    if not os.path.exists(csv_path):
        print(f"[!] CSV file not created: {csv_path}")
        return False

    # Check file size
    if os.path.getsize(csv_path) == 0:
        print(f"[!] CSV file is empty")
        return False

    # Verify readability
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

            if not rows:
                print("[!] CSV has no data rows (only header)")
                return False

            # Verify all columns present
            expected_cols = {"Package", "Version", "CVE_ID", "Severity",
                           "CVSS_Score", "Fixed_Version", "Title", "Url"}
            if not expected_cols.issubset(set(reader.fieldnames or [])):
                print("[!] CSV missing required columns")
                return False

            print(f"[*] CSV verified: {len(rows)} records")
            return True

    except Exception as e:
        print(f"[!] Error reading CSV: {e}")
        return False
```

## Example Output

```csv
Package,Version,CVE_ID,Severity,CVSS_Score,Fixed_Version,Title,Url
ip,2.0.0,CVE-2024-29415,HIGH,8.1,N/A,node-ip: Incomplete fix for CVE-2023-42282,https://nvd.nist.gov/vuln/detail/CVE-2024-29415
semver,7.3.7,CVE-2022-25883,HIGH,7.5,7.5.2,nodejs-semver: Regular expression denial of service,https://nvd.nist.gov/vuln/detail/CVE-2022-25883
tar,6.1.11,CVE-2026-23745,HIGH,8.2,7.5.3,node-tar: Arbitrary file overwrite and symlink poisoning,https://nvd.nist.gov/vuln/detail/CVE-2026-23745
```

## CSV Best Practices

1. **Always validate before writing**: Use field-level validation
2. **Handle special characters**: CSV library handles quotes and commas
3. **Use UTF-8 encoding**: Ensures compatibility with all systems
4. **Include BOM only if needed**: Standard CSV doesn't need BOM
5. **One record per vulnerability**: Avoid multi-line cells where possible
6. **Sort by severity then package**: Makes review easier
7. **Include metadata row**: Consider adding timestamp and version info
