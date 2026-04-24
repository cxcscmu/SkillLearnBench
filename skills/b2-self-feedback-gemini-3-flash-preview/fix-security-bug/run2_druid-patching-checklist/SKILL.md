---
name: run2_druid-patching-checklist
description: A checklist for ensuring thorough patching of Apache Druid security vulnerabilities.
---

# Druid Patching Checklist

When applying security patches to Druid, ensure you cover all affected areas:

1. **Grep for Patterns**: Search for all instances of the vulnerable pattern (e.g., `@JacksonInject JavaScriptConfig`).
2. **Apply Consistent Fixes**: Use the same robust fix across all occurrences.
3. **Import Management**:
    - Ensure all required classes (like `OptBoolean`) are imported.
    - Be careful not to accidentally remove existing imports (like `com.google.common.base.Function`).
4. **Parameter Name Accuracy**: Verify the parameter names in the `@JsonCreator` constructors. Some use `fn` while others use `function`.
5. **Verify Project Structure**: Ensure patches are applied to the correct modules (core, processing, server, indexing-service).
6. **Build Verification**: Run a full build of the affected modules to catch compilation errors.
7. **Patch Generation**: Generate a clean `git diff` and save it to the `patches/` directory.
