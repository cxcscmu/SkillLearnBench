---
name: enterprise-data-parsing
description: Strategies for reading and indexing diverse enterprise data formats located in a flat directory or specific path.
---

When retrieving information from enterprise data (like `/root/DATA`), first identify the file structure. Enterprise data often consists of mixed formats (PDF, CSV, JSON, TXT, or Markdown).

1. **Inventory**: List all files in the directory to determine the scope.
   ```python
   import os
   data_path = "/root/DATA"
   files = os.listdir(data_path)
   ```
2. **Reading Techniques**:
   - **Text/Markdown**: Use standard `open().read()`.
   - **JSON**: Use `json.load()`.
   - **CSV**: Use `pandas.read_csv()` for structured queries.
3. **Indexing**: If the dataset is large, create a simple keyword index or use a search function to map keywords from the questions to specific filenames to narrow the search space.