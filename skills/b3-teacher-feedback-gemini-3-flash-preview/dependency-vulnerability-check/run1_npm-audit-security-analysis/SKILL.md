---
name: npm-audit-security-analysis
description: Identifying vulnerabilities in Node.js dependencies using the npm audit tool to filter for high and critical severities.
---

### Overview
`npm audit` is a built-in tool in the Node.js ecosystem that checks projects for known vulnerabilities in dependencies. It compares the versions listed in `package-lock.json` against the GitHub Advisory Database.

### Key Commands
To perform a security audit and obtain detailed information in a machine-readable format, use the following flags:

*   **Audit with JSON output:** `npm audit --json`
    Provides a detailed JSON report containing dependency paths, CVE IDs, CVSS scores, and fix versions.
*   **Filtering by Severity:** While `npm audit` can filter exit codes by severity, the full JSON output contains all levels. You must post-process the JSON to filter for `high` and `critical` severities as requested.

### Analyzing the Output
The JSON output typically contains:
- `vulnerabilities`: A map of package names to vulnerability details.
- `via`: Sources of the vulnerability (e.g., specific advisories).
- `effects`: Other packages affected by this dependency.
- `range`: The semver range of affected versions.
- `fixAvailable`: Information on whether a fix exists and what version resolves it.