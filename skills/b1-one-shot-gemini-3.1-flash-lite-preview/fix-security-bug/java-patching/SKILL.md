---
name: java-patching
description: Techniques for applying security fixes to Java projects using git, diffs, and Maven.
---

# Java Security Patching Workflow

1. **Locate code**: Identify the affected classes (e.g., `*JavaScript*`).
2. **Develop the fix**:
   - Create a reproduction test first.
   - Modify the source code to add validation (e.g., checking for restricted keywords or verifying configuration).
3. **Generate Patch**:
   ```bash
   git diff > ../patches/security-fix.patch
   ```
4. **Build & Test**:
   - Apply using `git apply ../patches/security-fix.patch` if necessary.
   - Run the build with `-DskipTests=false` initially to verify the fix before running the production-like build.
5. **Rebuild**:
   Use standard Apache Maven commands, skipping quality checks as requested for production stability.
