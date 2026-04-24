---
name: apache-druid-security
description: Security practices and vulnerability patching for Apache Druid, focusing on JavaScript sandbox configuration.
---

# Apache Druid Security Patching

When patching vulnerabilities related to arbitrary code execution in Druid via JavaScript filters or samplers:

1. **Identify the vulnerability point**: Look for where JavaScript is evaluated (e.g., `JavaScriptFilter`, `JavaScriptFunction`).
2. **Review sandbox settings**: Check how `JavascriptConfig` is initialized and enforced. Ensure that enabling JavaScript (`enabled: true`) is not allowing bypasses via unexpected configurations or null keys.
3. **Impose Restrictions**: Modify the logic to strictly require explicit approval for dangerous operations, or block them entirely by default.
4. **Testing**: Create a regression test that mimics the exploit payload to ensure the fix is effective.
