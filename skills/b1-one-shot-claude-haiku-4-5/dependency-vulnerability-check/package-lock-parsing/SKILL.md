---
name: package-lock-parsing
description: Parse and extract package information from npm package-lock.json files to identify dependencies and their installed versions.
---

# Package-lock.json Parsing

## Overview
The `package-lock.json` file is an npm lock file that records exact dependency versions used in a project. It enables reproducible installs and is essential for vulnerability scanning.

## File Structure

The package-lock.json follows this structure:

```json
{
  "name": "project-name",
  "version": "1.0.0",
  "lockfileVersion": 3,
  "packages": {
    "": {
      "name": "project-name",
      "version": "1.0.0",
      "dependencies": {
        "express": "^4.18.0"
      }
    },
    "node_modules/express": {
      "version": "4.18.2",
      "resolved": "https://registry.npmjs.org/express/-/express-4.18.2.tgz"
    }
  }
}
```

## Key Properties

- **packages**: Contains all packages (root + node_modules)
- **version**: The installed version of each package
- **dependencies**: Direct dependencies of a package

## Extraction Pattern

```python
import json

def parse_package_lock(file_path):
    with open(file_path, 'r') as f:
        lock_data = json.load(f)

    packages = {}
    for pkg_path, pkg_info in lock_data.get('packages', {}).items():
        # Skip root package
        if pkg_path == '':
            continue

        pkg_name = pkg_path.split('/')[-1]
        version = pkg_info.get('version')
        packages[pkg_name] = version

    return packages
```

## Usage

Use this skill when:
- Extracting dependency lists from package-lock.json
- Building vulnerability scanning pipelines
- Analyzing dependency versions for compliance
- Creating inventory reports of installed packages

## Related Skills

- `trivy-vulnerability-scanning`: Use parsed packages as input to vulnerability scanner
- `security-audit-csv-reporting`: Output results in structured CSV format
