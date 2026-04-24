---
name: trivy-audit
description: Performing offline security audits on package-lock.json files using Trivy.
---

### Purpose
Identify vulnerabilities in node.js projects by scanning `package-lock.json` with Trivy.

### Workflow
1. Ensure the Trivy database is available (e.g., at `~/.cache/trivy/db/trivy.db`).
2. Run scan in offline mode:
   `trivy fs --offline --db-repository /root/.cache/trivy/db package-lock.json --format json --output report.json`
3. Parse the output for HIGH/CRITICAL vulnerabilities.
