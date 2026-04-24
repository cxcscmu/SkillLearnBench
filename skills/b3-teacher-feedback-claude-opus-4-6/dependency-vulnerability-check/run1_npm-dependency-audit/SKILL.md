---
name: npm-dependency-audit
description: How to perform security audits on Node.js package-lock.json files using npm audit and other offline tools to identify vulnerabilities in third-party dependencies.
---

## npm audit

`npm audit` analyzes the dependency tree described in `package-lock.json` and checks for known vulnerabilities.

### Basic Usage

```bash
# Run audit in the directory containing package-lock.json
cd /root
npm audit

# JSON output for programmatic parsing
npm audit --json

# Filter by severity
npm audit --audit-level=high

# Production only
npm audit --production
```

### JSON Output Structure

```json
{
  "vulnerabilities": {
    "package-name": {
      "name": "package-name",
      "severity": "high",
      "via": [
        {
          "source": 1234,
          "name": "package-name",
          "dependency": "package-name",
          "title": "Vulnerability title",
          "url": "https://github.com/advisories/GHSA-xxxx-xxxx-xxxx",
          "severity": "high",
          "cwe": ["CWE-xxx"],
          "cvss": {
            "score": 7.5,
            "vectorString": "CVSS:3.1/..."
          },
          "range": ">=1.0.0 <1.2.3"
        }
      ],
      "effects": [],
      "range": ">=1.0.0 <1.2.3",
      "nodes": ["node_modules/package-name"],
      "fixAvailable": {
        "name": "parent-package",
        "version": "2.0.0"
      }
    }
  }
}
```

### npm audit with Older npm Versions (v6)

Older npm versions produce a different JSON structure:

```json
{
  "advisories": {
    "1234": {
      "findings": [{"version": "1.0.0", "paths": ["..."]}],
      "id": 1234,
      "title": "Vulnerability Title",
      "module_name": "package-name",
      "severity": "high",
      "url": "https://npmjs.com/advisories/1234",
      "cves": ["CVE-2021-XXXXX"],
      "cvss": {"score": 7.5},
      "patched_versions": ">=1.2.3",
      "vulnerable_versions": "<1.2.3"
    }
  }
}
```

### Offline Considerations

If `npm audit` requires network access and you're offline, alternatives include:
- Using a local advisory database
- Using `grype` or `trivy` with offline databases
- Manually parsing against a cached vulnerability DB