---
name: run2_trivy-offline
description: A complete guide to executing Trivy in offline mode via Python `subprocess` to scan dependency files for vulnerabilities.
---

# Offline Dependency Scanning with Trivy

Trivy is an essential security tool that can scan for vulnerabilities in various artifacts, including source code repositories, container images, and dependency files like `package-lock.json`. Offline scanning is an excellent approach for air-gapped systems or reproducible CI/CD pipelines since it relies on a local vulnerability database instead of continuously fetching updates from the internet.

## Database Prerequisites
The offline database typically exists in a `.cache` directory (e.g., `~/.cache/trivy/db/trivy.db`). Trivy needs this cache path explicitly if it is not in the default location.

## Python Integration via Subprocess
To automate the scanning process, you can call Trivy using Python's `subprocess` module. Ensure that you instruct Trivy to skip database updates (`--skip-db-update`) and run exclusively in offline mode (`--offline-scan`).

### Code Example

```python
import subprocess
import sys
import json
import os

def run_trivy_scan(target_file, output_file, cache_dir):
    """
    Executes an offline Trivy scan on the target dependency file.
    
    Args:
        target_file (str): Path to the dependency file (e.g., 'package-lock.json')
        output_file (str): Desired output file path (e.g., 'trivy_report.json')
        cache_dir (str): Path to the Trivy cache directory
    """
    if not os.path.exists(cache_dir):
        print(f"[!] Warning: Cache directory {cache_dir} not found.")

    command = [
        "trivy", "fs", target_file,
        "--format", "json",
        "--output", output_file,
        "--scanners", "vuln",
        "--skip-db-update",
        "--offline-scan",
        "--cache-dir", cache_dir
    ]
    
    try:
        # We set check=False because Trivy may exit with a non-zero code if vulnerabilities are found
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        
        if "ERROR" in result.stderr:
            print(f"[!] Trivy Scan Error:\n{result.stderr}")
            sys.exit(1)
            
        print(f"[*] Trivy scan completed successfully. Report saved to {output_file}")
    except FileNotFoundError:
        print("[!] Error: Trivy is not installed or not in the PATH.")
        sys.exit(1)

# Example usage
if __name__ == "__main__":
    run_trivy_scan(
        target_file="/root/package-lock.json",
        output_file="/root/trivy_report.json",
        cache_dir="/root/.cache/trivy"
    )
```

## Parsing the Output
The JSON generated has the following structure:
```json
{
  "Results": [
    {
      "Target": "package-lock.json",
      "Vulnerabilities": [
        {
          "VulnerabilityID": "CVE-XXXX-YYYY",
          "PkgName": "example-pkg",
          "InstalledVersion": "1.0.0",
          "FixedVersion": "1.0.1",
          "Severity": "HIGH",
          "Title": "Example Vulnerability",
          "PrimaryURL": "https://nvd.nist.gov/vuln/detail/CVE-XXXX-YYYY",
          "CVSS": { ... }
        }
      ]
    }
  ]
}
```
You can use `json.load()` to parse this structure programmatically and extract only the relevant severity levels.
