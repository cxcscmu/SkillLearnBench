[SKILL]
---
name: patch-druid-cve-2021-25646
description: Patches Apache Druid CVE-2021-25646 by updating all usages of @JacksonInject to ignore user input via useInput = OptBoolean.FALSE, thus preventing attackers from overriding injected configurations (like JavaScriptConfig) through empty keys or property injection.
---

```bash
#!/bin/bash
set -e

# The vulnerability is caused by Jackson allowing user-provided JSON keys (like "") to override
# @JacksonInject parameters. The official patch for CVE-2021-25646 is to force useInput = OptBoolean.FALSE
# on all @JacksonInject annotations so that user