---
name: run2_druid-build-maven
description: Optimized Maven build command for Apache Druid to verify security patches.
---

# Building Apache Druid for Patch Validation

Use the following optimized command to verify your changes:

```bash
mvn clean package -DskipTests \
  -Dcheckstyle.skip=true \
  -Dpmd.skip=true \
  -Dforbiddenapis.skip=true \
  -Dspotbugs.skip=true \
  -Danimal.sniffer.skip=true \
  -Denforcer.skip=true \
  -Djacoco.skip=true \
  -Ddependency-check.skip=true \
  -pl '!web-console' \
  -pl indexing-service -am
```

## Troubleshooting Build Failures:
- **Compilation Error (cannot find symbol)**: Check imports. Common missing imports when patching Jackson are `com.fasterxml.jackson.annotation.OptBoolean`.
- **Duplicate Imports**: Check if you accidentally added an import that already exists with a different package or same package.
- **OOM Error**: Ensure `-pl '!web-console'` is included to skip the memory-intensive web console build.
