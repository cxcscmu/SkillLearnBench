---
name: run2_trivy-offline
description: Use Trivy vulnerability scanner in offline mode to discover security vulnerabilities in dependency files, covering setup, execution, and JSON output parsing.
---

# Trivy Offline Vulnerability Scanning

## Prerequisites
- Trivy installed (`trivy --version` to check)
- Local vulnerability DB already downloaded (check `trivy --version` for DB info)

## Command for npm package-lock.json
```bash
trivy fs \
  --skip-db-update \
  --skip-java-db-update \
  --offline-scan \
  --scanners vuln \
  --severity HIGH,CRITICAL \
  --format json \
  /path/to/package-lock.json > results.json
```

### Flag reference
| Flag | Purpose |
|------|---------|
| `--skip-db-update` | Don't update vulnerability DB (required for offline) |
| `--skip-java-db-update` | Don't update Java DB (required for offline) |
| `--offline-scan` | No network access |
| `--scanners vuln` | Only vulnerability scanning (not misconfig/secret) |
| `--severity HIGH,CRITICAL` | Filter severity at scan time |
| `--format json` | Machine-readable JSON output |

## JSON Output Structure
```json
{
  "SchemaVersion": 2,
  "Results": [
    {
      "Target": "package-lock.json",
      "Type": "npm",
      "Vulnerabilities": [
        {
          "VulnerabilityID": "CVE-YYYY-NNNNN",
          "PkgName": "package-name",
          "InstalledVersion": "1.2.3",
          "FixedVersion": "1.2.4",       // may be null/missing if no fix
          "Severity": "HIGH",
          "Title": "Short description",
          "Description": "Longer description",
          "PrimaryURL": "https://avd.aquasec.com/nvd/cve-...",
          "CVSS": {
            "nvd": {"V3Score": 7.5},
            "ghsa": {"V3Score": 7.5},
            "redhat": {"V3Score": 7.2}
          }
        }
      ]
    }
  ]
}
```

### Important notes
- `FixedVersion` can be null/None (not just missing) when no fix is available
- `FixedVersion` may contain comma-separated values for multiple fix branches (e.g., "7.5.2, 6.3.1, 5.7.2")
- `CVSS` dict keys vary per vulnerability — not all sources are present for every CVE
- `Title` may be null; fall back to `Description` if so
- `Vulnerabilities` key may be null (not just empty list) if no vulns found for a target
