---
name: enterprise-data-retrieval
description: Retrieve information from enterprise JSON datasets in /root/DATA.
---

## Overview
This skill provides methods for searching and extracting data from JSON files located in `/root/DATA`.

## Search Strategy
1. Use `grep_search` to find relevant keys or patterns across JSON files.
2. Read the identified files using `read_file` to understand the structure.
3. If necessary, use `run_shell_command` with `jq` to query complex JSON structures if files are large or deeply nested.

## Dataset Structure
- `/root/DATA/metadata/`: Contains `customers_data.json`, `employee.json`, etc.
- `/root/DATA/products/`: Contains individual product metadata files (e.g., `ActionGenie.json`).
