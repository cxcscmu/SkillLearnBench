---
name: cli-file-writing
description: How to write multi-line text files using command line interfaces.
---

# CLI File Writing

When creating files with specific formatting or multiple lines in a command-line environment, it is best to use tools that preserve line breaks and exact structure.

## Using the `write_file` Tool
If your agent environment supports a direct `write_file` API, use it by providing the exact path and the complete text content, making sure to include necessary newline characters (`\n`).

## Alternative Shell Commands
If no direct API is available, you can use `cat` with a Heredoc to write multi-line strings:

```bash
cat << 'EOF' > /path/to/file.txt
Line 1
Line 2
EOF
```
