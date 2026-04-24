---
name: maven-druid-build
description: Building Apache Druid with Maven, managing memory constraints, and skipping verification checks.
---

# Maven Build for Apache Druid

## Build Command Reference

### Full Build (from instructions)
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

## Flag Explanations

| Flag | Purpose |
|------|---------|
| `clean` | Remove previous build artifacts |
| `package` | Compile and package into JAR/WAR |
| `-DskipTests` | Skip unit test execution |
| `-Dcheckstyle.skip=true` | Skip code style checking |
| `-Dpmd.skip=true` | Skip PMD analysis |
| `-Dforbiddenapis.skip=true` | Skip forbidden API checking |
| `-Dspotbugs.skip=true` | Skip SpotBugs (FindBugs) analysis |
| `-Danimal.sniffer.skip=true` | Skip JDK version compatibility checks |
| `-Denforcer.skip=true` | Skip Maven Enforcer rules |
| `-Djacoco.skip=true` | Skip code coverage analysis |
| `-Ddependency-check.skip=true` | Skip OWASP dependency checking |
| `-pl '!web-console'` | Exclude web-console module (memory constraint) |
| `-pl indexing-service` | Include indexing-service module |
| `-am` | Also make dependencies of selected projects |

## Memory Management

### Memory Issues
If you encounter OOM (Out of Memory) errors:
```bash
# Increase heap size
export MAVEN_OPTS="-Xmx2g -Xms1g"

# Very aggressive heap limit
export MAVEN_OPTS="-Xmx1g -Xms512m"
```

### Parallel Builds
To speed up builds with multiple cores:
```bash
mvn clean package -T 1C  # 1 thread per core
```

## Output Artifacts

After successful build:
```
druid/indexing-service/target/druid-indexing-service-0.20.0-SNAPSHOT.jar
druid/distribution/target/apache-druid-0.20.0-SNAPSHOT/lib/
```

## Verifying Build

```bash
# Check if JAR was created
ls -la indexing-service/target/*.jar

# Check build log for errors
tail -100 build.log

# Verify specific file was included
jar tf indexing-service/target/*.jar | grep "JavaScriptFilter"
```

## Maven Troubleshooting

### Module Not Found
```bash
# Verify module exists
ls -la indexing-service/pom.xml

# Rebuild parent projects
mvn clean install -pl '!web-console'
```

### Compilation Errors
```bash
# Detailed error output
mvn clean package -X 2>&1 | tail -50

# Compile only (no packaging)
mvn clean compile
```

## Selective Compilation

```bash
# Build specific module and dependencies
mvn clean package -pl indexing-service -am

# Build without tests but with other checks
mvn clean package -DskipTests

# Minimal build for testing
mvn clean package -DskipTests -Denforcer.skip=true
```
