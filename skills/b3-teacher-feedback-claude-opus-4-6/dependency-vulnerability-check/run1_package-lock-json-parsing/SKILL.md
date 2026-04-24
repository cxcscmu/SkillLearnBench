---
name: package-lock-json-parsing
description: How to parse package-lock.json to extract all dependency names and versions for vulnerability lookups, covering both lockfile v1, v2, and v3 formats.
---

## package-lock.json Format

### Lockfile Version 2/3 (npm 7+)

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "lockfileVersion": 3,
  "packages": {
    "": {
      "name": "my-app",
      "dependencies": { "express": "^4.17.1" }
    },
    "node_modules/express": {
      "version": "4.17.1",
      "resolved": "https://registry.npmjs.org/express/-/express-4.17.1.tgz",
      "dependencies": { "accepts": "~1.3.7" }
    },
    "node_modules/accepts": {
      "version": "1.3.7"
    }
  }
}
```

### Lockfile Version 1 (npm 5-6)

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "lockfileVersion": 1,
  "dependencies": {
    "express": {
      "version": "4.17.1",
      "resolved": "...",
      "requires": { "accepts": "~1.3.7" },
      "dependencies": {
        "accepts": { "version": "1.3.7" }
      }
    }
  }
}
```

### Extracting Dependencies with Python

```python
import json

def extract_deps_v2v3(lockfile_path):
    """Extract from lockfileVersion 2 or 3."""
    with open(lockfile_path) as f:
        data = json.load(f)
    deps = {}
    for path, info in data.get("packages", {}).items():
        if path == "":
            continue  # skip root
        name = path.split("node_modules/")[-1]
        version = info.get("version", "unknown")
        deps[name] = version
    return deps

def extract_deps_v1(lockfile_path):
    """Extract from lockfileVersion 1 (recursive)."""
    with open(lockfile_path) as f:
        data = json.load(f)
    deps = {}
    def recurse(dep_dict):
        for name, info in dep_dict.items():
            version = info.get("version", "unknown")
            # Keep highest-level version or first found
            if name not in deps:
                deps[name] = version
            if "dependencies" in info:
                recurse(info["dependencies"])
    recurse(data.get("dependencies", {}))
    return deps

def extract_all_deps(lockfile_path):
    with open(lockfile_path) as f:
        data = json.load(f)
    version = data.get("lockfileVersion", 1)
    if version >= 2:
        return extract_deps_v2v3(lockfile_path)
    else:
        return extract_deps_v1(lockfile_path)
```

### Extracting with jq

```bash
# Lockfile v2/v3
jq -r '.packages | to_entries[] | select(.key != "") | "\(.key | split("node_modules/") | last)\t\(.value.version)"' package-lock.json

# Lockfile v1
jq -r '.dependencies | to_entries[] | "\(.key)\t\(.value.version)"' package-lock.json
```