---
name: maven-build-optimization
description: Optimized Maven build commands for Apache Druid to save time and resources. Use this when you need to rebuild Druid after applying patches.
---

# Maven Build Optimization for Druid

## Standard Fast Build Command
Use the following flags to skip non-essential steps during development and patching:
- `-DskipTests`: Skips unit tests.
- `-Dcheckstyle.skip=true`: Skips Checkstyle code analysis.
- `-Dpmd.skip=true`: Skips PMD analysis.
- `-Dforbiddenapis.skip=true`: Skips forbidden API checks.
- `-Dspotbugs.skip=true`: Skips SpotBugs static analysis.
- `-Danimal.sniffer.skip=true`: Skips API compatibility checks.
- `-Denforcer.skip=true`: Skips Maven Enforcer rules.
- `-Djacoco.skip=true`: Skips code coverage reporting.
- `-pl '!web-console'`: Excludes the web-console module (prevents OOM and save time).

## Building Specific Modules
To build only the necessary modules and their dependencies:
```bash
mvn clean package [skip-flags] -pl indexing-service -am
```
`-am` (also-make) ensures that all dependencies of the specified project are also built.

## Memory Management
If Maven runs out of memory, you can increase the heap size:
```bash
export MAVEN_OPTS="-Xmx2048m"
```
