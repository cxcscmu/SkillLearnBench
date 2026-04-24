---
name: druid-patch-rebuild-procedure
description: Creating, applying, and verifying patches for Apache Druid using Maven with specific flags to bypass non-essential checks.
---

1. **Generate Patches**:
   Create `.patch` files using `git diff` or `diff -u`. Ensure the patches target the correct file paths within the `/root/druid/` directory. Save patches to `/root/patches/`.

2. **Apply Patches**:
   Navigate to the repository and apply the fixes:
   ```bash
   cd /root/druid
   git apply /root/patches/fix_javascript_vulnerability.patch
   ```

3. **Execute Optimized Build**:
   Run the Maven build command provided in the task. This command is specifically tuned to avoid Out-Of-Memory (OOM) errors by skipping the web-console and speeds up the process by skipping tests and quality checks:
   ```bash
   mvn clean package -DskipTests -Dcheckstyle.skip=true -Dpmd.skip=true -Dforbiddenapis.skip=true -Dspotbugs.skip=true -Danimal.sniffer.skip=true -Denforcer.skip=true -Djacoco.skip=true -Ddependency-check.skip=true -pl '!web-console' -pl indexing-service -am
   ```

4. **Verify Artifacts**:
   Ensure the resulting JAR files (e.g., `druid-indexing-service-0.20.0.jar`) are generated in the respective `target` folders.