---
name: maven-build-skip
description: Guide on how to rebuild Druid using Maven while skipping unnecessary checks. Use this skill when asked to compile or build Druid.
---

# Druid Maven Rebuild

When patching Druid, you typically need to recompile the project without running slow test suites, code quality checks, and web console builds (which can cause OOM errors).

## Build Command

To quickly build the indexing-service (and its dependencies) while skipping the web-console, use:
```bash
cd /root/druid
mvn clean package \
  -DskipTests \
  -Dcheckstyle.skip=true \
  -Dpmd.skip=true \
  -Dforbiddenapis.skip=true \
  -Dspotbugs.skip=true \
  -Danimal.sniffer.skip=true \
  -Denforcer.skip=true \
  -Djacoco.skip=true \
  -Ddependency-check.skip=true \
  -pl '!web-console' \
  -pl indexing-service \
  -am
```

This compiles the required artifacts while avoiding heavy QA plugins and frontend compilation steps.
