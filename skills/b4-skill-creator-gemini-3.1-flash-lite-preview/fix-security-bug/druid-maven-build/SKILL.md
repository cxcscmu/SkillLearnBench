---
name: druid-maven-build
description: How to rebuild Apache Druid after applying patches. Use this whenever the codebase has been modified and needs a partial or full rebuild.
---

# Druid Build Procedure

## Overview
Rebuilding the patched Druid component requires using Maven, ensuring specific modules and skips are handled correctly to avoid OOM or code quality failures on patched code.

## Build Command
Execute the following to build the relevant module:

```bash
cd /root/druid
mvn clean package -DskipTests -Dcheckstyle.skip=true -Dpmd.skip=true -Dforbiddenapis.skip=true -Dspotbugs.skip=true -Danimal.sniffer.skip=true -Denforcer.skip=true -Djacoco.skip=true -Ddependency-check.skip=true -pl '!web-console' -pl indexing-service -am
```

## Important Notes
- `-pl '!web-console'`: Skips the web-console to avoid OOM errors.
- `-D*.skip=true`: Skips various quality checks which may fail on custom patches.
- Ensure you are in the `/root/druid` directory before running the command.
