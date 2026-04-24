---
name: java-patch-workflow
description: Workflow for creating and applying patches to Java projects - diff format, patch application, and Maven rebuilds for security fixes.
---

# Java Patch Workflow

## Creating Unified Diff Patches

```bash
# Create a patch from changes to a specific file
diff -u original_file.java modified_file.java > my_fix.patch

# Create patch with context lines
diff -u -p original.java modified.java > fix.patch

# Apply a patch
patch -p1 < fix.patch           # Strip 1 prefix component
patch -p0 < fix.patch           # Don't strip (exact path match)
patch --dry-run -p1 < fix.patch # Test without applying
```

## Git-Based Patching

```bash
# Create patch from staged changes
git diff HEAD > my_fix.patch

# Create patch from specific commit
git format-patch HEAD~1

# Apply git format-patch
git am patch_file.patch

# Apply unified diff
git apply patch_file.patch
git apply --check patch_file.patch  # Dry run
```

## Apache Druid Build

### Full Build (skip web-console for OOM prevention)
```bash
cd /root/druid
mvn clean package -DskipTests \
  -Dcheckstyle.skip=true -Dpmd.skip=true \
  -Dforbiddenapis.skip=true -Dspotbugs.skip=true \
  -Danimal.sniffer.skip=true -Denforcer.skip=true \
  -Djacoco.skip=true -Ddependency-check.skip=true \
  -pl '!web-console' -pl indexing-service -am
```

### Module-Specific Build
```bash
# Build only the indexing-service and dependencies
mvn package -DskipTests -pl indexing-service -am

# Build specific module with quality checks skipped
mvn package -DskipTests -Dcheckstyle.skip=true -pl processing
```

## Patch File Organization

```
/root/patches/
├── 01-fix-javascript-injection.patch     # Primary root cause fix
├── 02-fix-sampler-validation.patch       # Defense in depth
└── README.md                            # Fix description
```

## Common Issues

### Patch Offset Errors
If `patch` reports "offset" or "fuzz", the patch may be for a different file version.
Use `patch --fuzz=3` to allow more context flexibility.

### Build Failures After Patch
- Check for compilation errors: `mvn compile` first
- Verify imports are added for new classes used
- Check Guice injection: ensure `@Inject` annotation is present for DI

### Finding the Right JAR After Build
```bash
find /root/druid -name "druid-indexing-service-*.jar" -not -path "*/test*"
# Typically at: druid/indexing-service/target/druid-indexing-service-*.jar
```
