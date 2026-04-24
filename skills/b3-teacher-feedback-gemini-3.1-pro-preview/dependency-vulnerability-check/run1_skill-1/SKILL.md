[SKILL]
---
name: package-lock-json-parser
description: Parse package-lock.json (v2/v3) to extract all installed third-party dependencies and their exact versions. This is a critical first step for performing offline vulnerability scanning when standard network-based tools are unavailable.
---

When network access is restricted or strictly offline scanning is required, `npm audit` may fail. To perform a vulnerability audit against a local database, you first need to extract the installed packages and their versions directly from the `package-lock.json` file. 

Modern `package-lock.json` files (lockfileVersion 2 and 3) store dependency information in the `packages` object.

### Python Example: Extracting Dependencies

```python