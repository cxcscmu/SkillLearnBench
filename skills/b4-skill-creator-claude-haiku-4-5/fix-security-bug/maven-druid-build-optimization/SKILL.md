---
name: maven-druid-build-optimization
description: How to build Apache Druid efficiently with Maven while skipping unnecessary checks and OOM-prone modules. Use this skill when building patched Druid versions, when rebuilding after security fixes, or when the web-console module causes out-of-memory errors.
---

# Maven Druid Build Optimization

## Overview

Apache Druid is a large project with extensive code quality checks and a heavy web-console module. When building a patched version or in memory-constrained environments, selective skipping of modules and checks optimizes build time and resource usage.

## Build Command Structure

The standard optimized build for patched Druid skips:
- **Web-console module** (`-pl '!web-console'`) - Frontend build with Node.js dependencies, causes OOM
- **Unit tests** (`-DskipTests`) - Can be skipped when applying security patches
- **Code quality checks** - Multiple style, security, and analysis tools

## Full Build Command for Patched Druid

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

## Understanding the Flags

### Module Selection
- `-pl '!web-console'` - Exclude web-console from build (prevents OOM)
- `-pl indexing-service` - Include only indexing-service module
- `-am` (--also-make) - Build dependencies of selected modules

### Test Skipping
- `-DskipTests` - Skip test compilation and execution

### Quality Check Skips
These skip code quality tools that can be safely bypassed for patched code:
- `-Dcheckstyle.skip=true` - Checkstyle code style checks
- `-Dpmd.skip=true` - PMD static analysis
- `-Dforbiddenapis.skip=true` - Forbidden APIs checks
- `-Dspotbugs.skip=true` - SpotBugs security analysis
- `-Danimal.sniffer.skip=true` - Animal Sniffer API compatibility
- `-Denforcer.skip=true` - Maven Enforcer rules
- `-Djacoco.skip=true` - Code coverage
- `-Ddependency-check.skip=true` - Dependency vulnerability checking

### Build Phases
- `clean` - Remove previous build artifacts
- `package` - Compile and create JAR files

## Build Output Location

Built artifacts (JAR files) are located at:
```
druid-indexing-service/target/druid-indexing-service-<version>-<classifier>.jar
```

## Memory Management

If you still encounter OOM errors:

1. **Increase Maven heap:**
   ```bash
   export MAVEN_OPTS="-Xmx2g"
   ```

2. **Build specific modules sequentially:**
   ```bash
   mvn clean package -pl 'druid-core' -DskipTests -Dcheckstyle.skip=true ...
   mvn package -pl 'druid-indexing-service' -am -DskipTests -Dcheckstyle.skip=true ...
   ```

## Verification After Build

After a successful build, verify the JAR was created:

```bash
ls -lh druid-indexing-service/target/*.jar
```

The verifier will deploy the JAR to `/opt/druid/lib/` and restart the Druid service before running tests.

## Build Troubleshooting

- **Timeout issues:** Increase Maven timeout: `mvn -DmultiModuleProjectDirectory=. ...`
- **Out of memory:** Use `-Xmx4g` or higher in MAVEN_OPTS
- **Module not found:** Verify module names with `mvn -pl help:describe`
- **Dependency issues:** Run `mvn dependency:tree` to verify dependency resolution
