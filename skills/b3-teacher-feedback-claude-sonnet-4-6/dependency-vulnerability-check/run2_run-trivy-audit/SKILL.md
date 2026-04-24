---
name: run-trivy-audit
description: Use this skill to run Trivy in offline mode against /root/package-lock.json and produce the security audit CSV at /root/security_audit.csv. Use only after locating the trivy cache directory.
---

# Run Trivy Security Audit and Generate CSV

## Step 1: Run Trivy against the dependency file

```bash
# Replace CACHE_DIR with the path found by the find-trivy-and-cache skill
CACHE_DIR="/root/trivy-cache"

trivy fs /root/package-lock.json \
  --format json \
  --skip-db-update \
  --offline-scan \
  --cache-dir "$CACHE_DIR" \
  --severity HIGH,CRITICAL \
  -o /root/trivy_output.json
```

If the first cache dir doesn't work, try others found in the previous skill.

## Step 2: Parse Trivy JSON output into CSV

```python
#!/usr/bin/env python3
import json
import csv

with open("/root/trivy_output.json") as f:
    data = json.load(f)

rows = []
seen = set()

results = data.get("Results", [])

for result in results:
    vulnerabilities = result.get("Vulnerabilities", [])
    if not vulnerabilities:
        continue
    for vuln in vulnerabilities:
        pkg_name = vuln.get("PkgName", "")
        installed_version = vuln.get("InstalledVersion", "")
        cve_id = vuln.get("VulnerabilityID", "")
        severity = vuln.get("Severity", "")

        # Only HIGH and CRITICAL
        if severity not in ("HIGH", "CRITICAL"):
            continue

        # Deduplicate by (pkg, version, cve)
        key = (pkg_name, installed_version, cve_id)
        if key in seen:
            continue
        seen.add(key)

        fixed_version = vuln.get("FixedVersion", "")
        if not fixed_version:
            fixed_version = "N/A"

        # CVSS score: priority nvd > ghsa > redhat, use V3Score
        cvss_score = ""
        cvss_data = vuln.get("CVSS", {})

        for source_key in cvss_data:
            if source_key.lower() == "nvd":
                v3 = cvss_data[source_key].get("V3Score", "")
                if v3 != "" and v3 is not None:
                    cvss_score = v3
                    break

        if cvss_score == "":
            for source_key in cvss_data:
                if source_key.lower() == "ghsa":
                    v3 = cvss_data[source_key].get("V3Score", "")
                    if v3 != "" and v3 is not None:
                        cvss_score = v3
                        break

        if cvss_score == "":
            for source_key in cvss_data:
                if source_key.lower() == "redhat":
                    v3 = cvss_data[source_key].get("V3Score", "")
                    if v3 != "" and v3 is not None:
                        cvss_score = v3
                        break

        if cvss_score == "":
            # fallback: any source with V3Score
            for source_key in cvss_data:
                v3 = cvss_data[source_key].get("V3Score", "")
                if v3 != "" and v3 is not None:
                    cvss_score = v3
                    break

        # Title/description
        title = vuln.get("Title", "")
        if not title:
            title = vuln.get("Description", "")
        if not title:
            title = cve_id

        # URL: use PrimaryURL from trivy output
        url = vuln.get("PrimaryURL", "")
        if not url:
            # fallback to first reference
            refs = vuln.get("References", [])
            if refs:
                url = refs[0]

        rows.append({
            "Package": pkg_name,
            "Version": installed_version,
            "CVE_ID": cve_id,
            "Severity": severity,
            "CVSS_Score": cvss_score,
            "Fixed_Version": fixed_version,
            "Title": title,
            "Url": url,
        })

# Sort for deterministic output
rows.sort(key=lambda r: (r["Package"], r["Version"], r["CVE_ID"]))

fieldnames = ["Package", "Version", "CVE_ID", "Severity", "CVSS_Score", "Fixed_Version", "Title", "Url"]

with open("/root/security_audit.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Written {len(rows)} rows to /root/security_audit.csv")
```

Save the above as `/root/parse_trivy.py` and run:

```bash
python3 /root/parse_trivy.py
```

## Step 3: Verify output

```bash
head -5 /root/security_audit.csv
wc -l /root/security_audit.csv
```