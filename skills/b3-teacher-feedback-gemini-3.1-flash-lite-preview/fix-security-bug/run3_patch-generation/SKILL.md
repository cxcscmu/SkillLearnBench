---
name: patch-generation
description: Generating and saving git-compatible patch files for Apache Druid source code.
---

To address the vulnerability, identify the `JavaScriptConfig` class responsible for deserializing the malicious payload. Use `grep` to locate the handling of the empty string key `""`.

Create a patch file at `/root/patches/fix-js-config.patch` that removes the setter method or the logic inside `JavaScriptConfig` (or its factory/builder) that maps the empty string to the `enabled` configuration. 

Example approach:
1. Locate `src/main/java/org/apache/druid/js/JavaScriptConfig.java`.
2. Inspect the JSON deserialization logic. If there is a method like `set` or a `@JsonCreator` that accepts `""`, modify the code to ignore or explicitly throw an exception when such a key is encountered.
3. Generate the patch using:
   ```bash
   cd /root/druid
   git diff > /root/patches/fix-js-config.patch
   ```