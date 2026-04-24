---
name: apply-and-rebuild
description: Applying patches to the Druid source code and performing a targeted Maven build.
---

1. Apply the patch to the local repository:
   ```bash
   cd /root/druid
   git apply /root/patches/fix-js-config.patch
   ```

2. Rebuild the project focusing on the affected modules:
   ```bash
   cd /root/druid
   mvn clean package -DskipTests \
     -Dcheckstyle.skip=true -Dpmd.skip=true -Dforbiddenapis.skip=true \
     -Dspotbugs.skip=true -Danimal.sniffer.skip=true -Denforcer.skip=true \
     -Djacoco.skip=true -Ddependency-check.skip=true \
     -pl '!web-console' -pl indexing-service -am
   ```

3. Ensure the `processing` module (where `JavaScriptConfig` resides) is included in the build and that the resulting JARs contain the patched classes.