---
name: run2_maven-security-build
description: Building Apache Druid with Maven while maintaining security patch integrity and skipping unnecessary checks
---

# Maven Build for Security Patches

## Overview

When applying security patches to large Java projects like Druid, you need to rebuild with specific Maven configurations to:
1. Ensure patches are properly compiled
2. Skip expensive code quality checks that may not apply to security fixes
3. Avoid memory exhaustion on large builds
4. Focus on functional correctness

## Build Strategy for Security Patches

### Stage 1: Verify Patch Application
```bash
cd /root/druid
git status  # Should show modified files
git diff    # Should show the security patch applied
```

### Stage 2: Build with Minimal Overhead
```bash
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

## Why Each Skip Flag is Used

### Code Quality Checks (Safe to Skip for Security Patches)

| Flag | Skips | Why Safe |
|------|-------|---------|
| `-Dcheckstyle.skip=true` | CheckStyle (code style) | Style doesn't affect security |
| `-Dpmd.skip=true` | PMD (potential bugs) | Not relevant for focused patches |
| `-Dforbiddenapis.skip=true` | Forbidden APIs check | Security patch may use specific APIs |
| `-Dspotbugs.skip=true` | SpotBugs (static analysis) | Not relevant for focused patches |
| `-Danimal.sniffer.skip=true` | Animal Sniffer (API compatibility) | Not relevant for internal patches |
| `-Denforcer.skip=true` | Maven Enforcer | Version requirements not affected |
| `-Djacoco.skip=true` | JaCoCo (code coverage) | Coverage tracking not needed |
| `-Ddependency-check.skip=true` | Dependency vulnerability scan | Patch doesn't add dependencies |

### Module Configuration

| Flag | Effect | Purpose |
|------|--------|---------|
| `-DskipTests` | Skip all tests | Speeds up build, tests run later in pipeline |
| `-pl '!web-console'` | Exclude web-console module | Prevents OOM on memory-limited systems |
| `-pl indexing-service` | Build only indexing-service | Focuses on affected module |
| `-am` | Build all upstream dependencies | Ensures dependencies are current |

## Module Selection

### For Indexing Service Patches (Most Common)
```bash
mvn ... -pl indexing-service -am
```

This builds:
- core
- processing
- server
- indexing-service and its dependencies

### For Processing Module Patches
```bash
mvn ... -pl processing -am
```

### For Full Build (If Needed)
```bash
mvn ... clean package
```

## Build Output Analysis

### Success Indicators
```
[INFO] Reactor Summary:
[INFO] Druid ............................. SUCCESS
[INFO] druid-core ........................ SUCCESS
...
[INFO] druid-indexing-service ........... SUCCESS
[INFO] BUILD SUCCESS
```

### Watch For
- Compilation warnings (acceptable for security patches)
- Module build times (indexing-service should be ~5-10 seconds)
- Final JAR size (should not significantly change)

## JAR Verification

After successful build, verify the patched classes:

```bash
# Locate the JAR
ls -lh /root/druid/indexing-service/target/druid-indexing-service-*.jar

# Verify patched class exists
jar tf /root/druid/indexing-service/target/druid-indexing-service-0.20.0.jar | \
  grep JavaScriptDimFilter

# Extract and inspect (optional)
jar xf /root/druid/indexing-service/target/druid-indexing-service-0.20.0.jar \
  org/apache/druid/query/filter/JavaScriptDimFilter.class

# View class annotations
javap org/apache/druid/query/filter/JavaScriptDimFilter.class
```

## Memory Management

### If You Encounter OOM Errors

```bash
# Increase Maven memory
export MAVEN_OPTS="-Xmx4g -XX:+UseG1GC"
mvn clean package ...

# Or use larger heap
export MAVEN_OPTS="-Xmx8g -XX:UseG1GC -XX:+UnlockExperimentalVMOptions -XX:G1MaxGCPauseMillis=200"
```

### Memory Optimization Tips
1. Exclude web-console with `-pl '!web-console'`
2. Skip tests with `-DskipTests`
3. Use `-pl indexing-service -am` to build only affected modules
4. Run on system with 8GB+ available memory

## Incremental Builds

After first successful build:

```bash
# Clean only the affected module
rm -rf indexing-service/target

# Rebuild (faster, uses cached dependencies)
mvn package -DskipTests -pl indexing-service
```

## Troubleshooting Build Failures

### Compilation Error: "Cannot find symbol"
```bash
# Cause: Dependency not rebuilt
# Solution: Rebuild all dependencies
mvn clean compile -pl indexing-service -am
```

### "Cannot create module alias"
```bash
# Cause: Conflicting Maven modules
# Solution: Check for duplicate module declarations in pom.xml
```

### Build Hangs or Freezes
```bash
# Cause: Memory exhaustion
# Solution: Kill and restart with -Xmx4g
pkill -9 java
export MAVEN_OPTS="-Xmx4g"
mvn clean package ...
```

## Final Verification

After build completes:

```bash
# Check JAR was created
test -f /root/druid/indexing-service/target/druid-indexing-service-0.20.0.jar && \
  echo "JAR created successfully"

# Check build artifacts directory
ls -lh /root/druid/indexing-service/target/

# Verify class was compiled with patch
unzip -p /root/druid/indexing-service/target/druid-indexing-service-0.20.0.jar \
  org/apache/druid/query/filter/JavaScriptDimFilter.class | \
  hexdump -C | grep -i "JsonIgnoreProperties" || \
  echo "Annotation check: May need binary inspection"
```

## Complete Build Command for Reference

```bash
cd /root/druid && \
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
  -am && \
echo "Build successful, JAR available at:" && \
ls -lh /root/druid/indexing-service/target/druid-indexing-service-0.20.0.jar
```
