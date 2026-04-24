---
name: SetupStockVisualizerWorkspace
description: Initializes the directory structure and populates the environment with necessary data and libraries for the D3.js visualization. This skill should be executed before generating any code files to ensure the target paths exist and the D3 library is available locally.
---

```bash
# 1. Create directory structure
mkdir -p /root/output/js
mkdir -p /root/output/css
mkdir -p /root/output/data

# 2. Copy source data to the output directory for relative path accessibility
cp -r /root/data/* /root/output/data/

# 3. Vendor D3.js v6 library directly using curl
curl -L https://cdn.jsdelivr.net/npm/d3@6.7.8/dist/d3.min.js -o /root/output/js/d3.v6.min.js
```