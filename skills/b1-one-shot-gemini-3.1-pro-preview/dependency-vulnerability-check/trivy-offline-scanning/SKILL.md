---
name: trivy-offline-scanning
description: Use Trivy for offline vulnerability scanning of dependency files like package-lock.json.
---

# Trivy Offline Vulnerability Scanning

Trivy can be used to scan dependency files (e.g. `package-lock.json`) offline without updating its database or querying the network for dependency analysis.

## Prerequisites
- Trivy installed.
- Vulnerability DB present in the Trivy cache directory.

## Usage

To scan a file like `package-lock.json` and output the results as a JSON file, use the following command:

```bash
trivy fs --skip-db-update --offline-scan --format json --output trivy-report.json <path-to-file>
```

### Options Explained:
- `fs`: Scan a filesystem path or a specific file.
- `--skip-db-update`: Prevents Trivy from attempting to update the vulnerability database, crucial for offline scanning.
- `--offline-scan`: Prevents Trivy from issuing API requests to identify dependencies.
- `--format json`: Formats the output as JSON for easier programmatic parsing.
- `--output trivy-report.json`: Saves the output to the specified file.

This approach ensures zero network calls during the analysis of dependency manifests.
