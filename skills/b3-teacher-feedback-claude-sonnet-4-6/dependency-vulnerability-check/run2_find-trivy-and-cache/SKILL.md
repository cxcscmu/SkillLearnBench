---
name: find-trivy-and-cache
description: Use this skill first to locate the trivy binary and its pre-downloaded vulnerability database cache on the system before running any security audit.
---

# Find Trivy Binary and Cache Directory

## Step 1: Check if Trivy is available

```bash
which trivy
trivy --version
```

## Step 2: Locate trivy database cache

```bash
# Check common cache locations
ls /root/trivy-cache/ 2>/dev/null
ls /home/trivy-cache/ 2>/dev/null
ls ~/.cache/trivy/ 2>/dev/null

# Find trivy.db anywhere on the system
find / -name "trivy.db" 2>/dev/null
find / -name "metadata.json" -path "*/trivy/*" 2>/dev/null

# Also check for fanal db
find / -name "fanal.db" 2>/dev/null
```

## Step 3: Record the cache directory path

Note the directory that contains `trivy.db`. This will be passed as `--cache-dir` to trivy commands. Common paths:
- `/root/trivy-cache`
- `/root/.cache/trivy`
- `/home/trivy-cache`