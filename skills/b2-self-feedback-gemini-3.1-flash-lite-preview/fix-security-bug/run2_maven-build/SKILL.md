---
name: run2_maven-build
description: Improved skill for building Apache Druid with Maven, focusing on skipping non-essential tasks efficiently.
---

# Maven Build Skill

## Build command
Build the necessary modules while excluding non-essential tasks to save time and resources:
```bash
cd /root/druid
# Build with skip flags
mvn clean package -DskipTests \
  -Dcheckstyle.skip=true \
  -Dpmd.skip=true \
  -Dforbiddenapis.skip=true \
  -Dspotbugs.skip=true \
  -Danimal.sniffer.skip=true \
  -Denforcer.skip=true \
  -Djacoco.skip=true \
  -Ddependency-check.skip=true \
  -pl '!web-console' -pl indexing-service -am
```
