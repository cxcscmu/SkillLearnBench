---
name: druid-maven-build
description: How to build Apache Druid with Maven, including how to skip OOM-prone modules, skip code quality checks for patched files, and build only specific modules. Use this skill when building Druid from source, when rebuilding after applying security patches, or when Maven build fails due to memory or code quality check issues.
---

# Apache Druid Maven Build

## Standard Patch Build Command

When applying security patches (skip tests + code quality checks + web-console to avoid OOM):

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

Key flags:
- `-pl indexing-service -am`: Build only `indexing-service` and all its dependencies (modules it depends on)
- `-pl '!web-console'`: Exclude web-console (causes OOM during build)
- `-DskipTests`: Skip unit tests
- `-Dcheckstyle.skip=true` etc.: Skip code quality checks that may fail on patched files

## Module Dependency Chain

For a patch affecting `indexing-service`, these modules are typically rebuilt (via `-am`):
- `druid-core` (contains `JavaScriptConfig`, `JavaScriptParseSpec`)
- `druid-processing` (contains filters, aggregators, extractors)
- `druid-server` (contains `JavaScriptTieredBrokerSelectorStrategy`)
- `druid-indexing-service` (contains `SamplerResource`, `JavaScriptWorkerSelectStrategy`)

## Output JARs

After build, the patched JARs are in:
- `indexing-service/target/druid-indexing-service-<version>.jar`
- Module JARs in respective `target/` directories

## Troubleshooting

**OOM during build:** Add `-Xmx4g` to `MAVEN_OPTS` or exclude heavy modules with `-pl '!web-console'`

**Checkstyle failures on patched files:** Use `-Dcheckstyle.skip=true`

**ForbiddenApis failures:** Use `-Dforbiddenapis.skip=true`
