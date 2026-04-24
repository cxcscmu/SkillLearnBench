---
name: run2_trivy-offline-scanning
description: Use Trivy vulnerability scanner in offline mode to scan dependency lock files and produce JSON vulnerability reports without internet access.
---

# Trivy Offline Vulnerability Scanning (Round 2)

## Environment Details
- Trivy binary: `/usr/bin/trivy` (version 0.69.3)
- Database cache: `/root/trivy-cache/` (contains `db/trivy.db` and `db/metadata.json`)
- DB updated: 2026-01-21 (may be outdated — scan results reflect DB date)

## Key Command

```bash
trivy fs /root/package-lock.json \
  --format json \
  --output /root/trivy_report.json \
  --scanners vuln \
  --skip-db-update \
  --offline-scan \
  --cache-dir /root/trivy-cache
```

## Important Flags
| Flag | Purpose |
|------|---------|
| `fs <file>` | Scan a dependency lock file directly |
| `--skip-db-update` | Don't fetch updated DB (offline requirement) |
| `--offline-scan` | Disable all network calls |
| `--cache-dir` | Point to offline DB location |
| `--scanners vuln` | Only vulnerability scanning (skip misconfig) |

## Behavior Notes
- Trivy by default **suppresses dev dependencies** — use `--include-dev-deps` if needed
- Output goes to the file specified by `--output`; stdout shows only progress logs
- Non-zero exit code indicates scan failure (not just vulnerability presence)

## Python Wrapper

```python
import subprocess, sys, os

def run_trivy_scan(target='/root/package-lock.json',
                   output='/root/trivy_report.json',
                   cache_dir='/root/trivy-cache'):
    db_path = os.path.join(cache_dir, 'db', 'trivy.db')
    if not os.path.exists(db_path):
        print(f"[!] DB not found at {db_path}")
        sys.exit(1)

    cmd = [
        'trivy', 'fs', target,
        '--format', 'json',
        '--output', output,
        '--scanners', 'vuln',
        '--skip-db-update',
        '--offline-scan',
        '--cache-dir', cache_dir
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr)
        sys.exit(1)
    print(f"[+] Scan complete: {output}")
    return output
```

## JSON Output Structure

```json
{
  "Results": [
    {
      "Target": "package-lock.json",
      "Class": "lang-pkgs",
      "Type": "npm",
      "Vulnerabilities": [
        {
          "VulnerabilityID": "CVE-2024-29415",
          "PkgName": "ip",
          "InstalledVersion": "2.0.0",
          "FixedVersion": "",        // Empty string = no fix; use 'N/A'
          "Severity": "HIGH",
          "Title": "node-ip: Incomplete fix for CVE-2023-42282",
          "PrimaryURL": "https://avd.aquasec.com/nvd/cve-2024-29415",
          "CVSS": {
            "ghsa": { "V3Score": 8.1 },
            "redhat": { "V3Score": 9.8 }
          }
        }
      ]
    }
  ]
}
```

## Gotchas
- `FixedVersion` can be `None` OR an empty string `""` — handle both as 'N/A'
- `Vulnerabilities` key may be `null` (not just missing) — use `or []` not just `.get()`
- Multiple fix versions are comma-separated in a single string: `"7.5.2, 6.3.1, 5.7.2"`
