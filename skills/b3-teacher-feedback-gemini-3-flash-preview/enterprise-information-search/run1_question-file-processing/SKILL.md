---
name: question-file-processing
description: How to parse key-value pairs from a text file where keys and question values are stored together.
---

To process `/root/question.txt`, which contains keys and values, you must accurately extract the identifier (e.g., "q1") and the query string.

1. **Parsing Pattern**: Use regular expressions or string splitting if the format is consistent (e.g., `key: value` or `key=value`).
   ```python
   questions = {}
   with open('/root/question.txt', 'r') as f:
       for line in f:
           if ':' in line:
               key, val = line.split(':', 1)
               questions[key.strip()] = val.strip()
   ```
2. **Iteration**: Loop through the resulting dictionary to perform retrieval for each unique ID.