---
name: run2_csv-reporting
description: Generate structured CSV security audit reports from Trivy JSON vulnerability data with deduplication, proper quoting, and field mapping.
---

# Vulnerability CSV Reporting

## Target CSV Schema
```
Package,Version,CVE_ID,Severity,CVSS_Score,Fixed_Version,Title,Url
```

## Complete Python Script
```python
import csv, json

def get_cvss_score(vuln):
    cvss = vuln.get("CVSS") or {}
    for source in ["nvd", "ghsa", "redhat"]:
        entry = cvss.get(source)
        if entry:
            score = entry.get("V3Score")
            if score is not None:
                return score
    return "N/A"

with open("/root/trivy_results.json") as f:
    data = json.load(f)

rows = []
seen = set()

for result in data.get("Results", []):
    for vuln in (result.get("Vulnerabilities") or []):
        key = (vuln.get("PkgName"), vuln.get("VulnerabilityID"))
        if key in seen:
            continue
        seen.add(key)

        title = vuln.get("Title") or vuln.get("Description") or ""

        rows.append({
            "Package": vuln.get("PkgName", ""),
            "Version": vuln.get("InstalledVersion", ""),
            "CVE_ID": vuln.get("VulnerabilityID", ""),
            "Severity": vuln.get("Severity", ""),
            "CVSS_Score": get_cvss_score(vuln),
            "Fixed_Version": vuln.get("FixedVersion") or "N/A",
            "Title": title,
            "Url": vuln.get("PrimaryURL", ""),
        })

with open("/root/security_audit.csv", "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=[
        "Package", "Version", "CVE_ID", "Severity",
        "CVSS_Score", "Fixed_Version", "Title", "Url"
    ])
    writer.writeheader()
    writer.writerows(rows)

print(f"Written {len(rows)} vulnerabilities")
```

## Key considerations
- **Deduplication**: Use (PkgName, VulnerabilityID) as unique key since same package may appear multiple times
- **Null handling**: `FixedVersion` and `Vulnerabilities` can be None/null — use `or` fallbacks
- **Title fallback**: Use `Description` if `Title` is null
- **CSV quoting**: Python's `csv.DictWriter` handles quoting automatically for fields containing commas
- **Fixed version**: May contain comma-separated values for multiple branches — CSV writer handles quoting
