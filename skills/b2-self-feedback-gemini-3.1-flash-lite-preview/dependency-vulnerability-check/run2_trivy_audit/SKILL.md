---
name: run2_trivy_audit
description: Run Trivy in offline mode to identify high and critical vulnerabilities in package-lock.json with specific flag usage.
---

# Trivy Offline Audit (Improved)

Use this skill to scan `package-lock.json` for HIGH/CRITICAL vulnerabilities.

## Usage

1. **Database:** Trivy uses its own local DB. Ensure the DB is updated (`trivy --download-db-only`).
2. **Execution:** Use `trivy fs` to scan the lock file. 
   ```bash
   trivy fs --cache-dir /root/.cache/trivy --severity HIGH,CRITICAL --format json --output report.json .
   ```
3. **Important:** Do *not* use `--offline` as it prevents the scanner from accessing local database paths correctly in some versions. Rely on the cached DB.
