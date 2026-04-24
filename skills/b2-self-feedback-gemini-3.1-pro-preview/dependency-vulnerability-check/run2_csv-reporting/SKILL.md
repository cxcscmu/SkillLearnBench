---
name: run2_csv-reporting
description: An advanced guide on generating a fully-featured CSV vulnerability report, featuring explicit filtering, missing data fallbacks, and strict header schemas.
---

# Vulnerability CSV Report Generation

Compiling a structured, comma-separated values (CSV) file from vulnerability JSON output is a crucial reporting step. Doing so robustly requires explicitly defining schemas and applying default fallback values to missing keys to prevent schema deviations and Python runtime errors.

## CSV Schema Design

A rigorous CSV security report must use explicitly defined columns. Common columns include:
- `Package`: Affected package name.
- `Version`: Installed version.
- `CVE_ID`: Vulnerability identifier.
- `Severity`: Impact level.
- `CVSS_Score`: The CVSS numeric score (or N/A).
- `Fixed_Version`: Version containing the patch (or N/A).
- `Title`: Short description.
- `Url`: Reference URL.

### Severity Filtering
Only process vulnerabilities that cross a specific severity threshold (e.g., `HIGH` or `CRITICAL`) to eliminate noise in executive reporting.

## Advanced Implementation (Python)

Using `csv.DictWriter` ensures data correctly matches column headers. When data fields like `Title` or `FixedVersion` are occasionally omitted by the scanner, using Python's `.get('Key', 'Fallback_Value')` pattern prevents empty columns from appearing blank.

```python
import csv

def generate_csv_report(json_data, output_file, severity_filter=['HIGH', 'CRITICAL']):
    """
    Generate a filtered CSV from parsed Trivy JSON data.
    
    Args:
        json_data (dict): The parsed Trivy output dictionary.
        output_file (str): The destination path for the CSV.
        severity_filter (list): Severity levels to include.
    """
    headers = ["Package", "Version", "CVE_ID", "Severity", 
               "CVSS_Score", "Fixed_Version", "Title", "Url"]
    
    vulnerabilities = []
    
    if 'Results' in json_data:
        for result in json_data['Results']:
            for vuln in result.get('Vulnerabilities', []):
                severity = vuln.get('Severity', 'UNKNOWN')
                
                # Filter noise by only recording severe vulnerabilities
                if severity in severity_filter:
                    # Construct record using safe fallbacks
                    record = {
                        "Package": vuln.get('PkgName', 'N/A'),
                        "Version": vuln.get('InstalledVersion', 'N/A'),
                        "CVE_ID": vuln.get('VulnerabilityID', 'N/A'),
                        "Severity": severity,
                        "CVSS_Score": extract_cvss_score_with_fallback(vuln),
                        "Fixed_Version": vuln.get('FixedVersion', 'N/A'),
                        "Title": vuln.get('Title', 'No description provided'),
                        "Url": vuln.get('PrimaryURL', 'N/A')
                    }
                    vulnerabilities.append(record)
                    
    # Write output reliably
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        if vulnerabilities:
            writer.writerows(vulnerabilities)
            
    print(f"[+] Report generated with {len(vulnerabilities)} severe issues.")

# Helper CVSS extraction function referenced above
def extract_cvss_score_with_fallback(vuln):
    cvss = vuln.get('CVSS', {})
    for source in ['nvd', 'ghsa', 'redhat']:
        if source in cvss:
            score = cvss[source].get('V3Score')
            if score is not None:
                return score
            score = cvss[source].get('V2Score')
            if score is not None:
                return score
    return 'N/A'
```

### Safety and Cross-Platform Consistency
- **`newline=''`**: Required to avoid blank line spacing on Windows.
- **`encoding='utf-8'`**: Mandatory to process potential unicode characters inside vulnerability titles or descriptions properly.
