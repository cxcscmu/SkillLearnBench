---
name: enterprise-data-retrieval
description: Retrieve and analyze information from enterprise JSON data files (Slack messages, employee records, product data). Use this skill whenever the user asks to find employee IDs, URLs, or other structured information from enterprise data directories containing JSON files. Handles large files by using grep/search to locate relevant content before reading.
---

# Enterprise Data Retrieval

## Overview

Enterprise data is stored under `/root/DATA/` with two subdirectories:
- `metadata/` — employee records, customer data, salesforce team info
- `products/` — per-product JSON files containing Slack channel messages, threads, and reactions

## Data Structure

Each product JSON file has the structure:
```json
{
  "slack": [
    {
      "Channel": { "name": "...", "channelID": "..." },
      "Message": {
        "User": { "userId": "eid_XXXX", "timestamp": "...", "text": "...", "utterranceID": "..." },
        "Reactions": []
      },
      "ThreadReplies": [ ... ],
      "id": "..."
    }
  ]
}
```

## Key Patterns

### Finding employee IDs
- Employee IDs follow the pattern `eid_XXXXXXXX`
- Use grep to find relevant messages: `grep -i "keyword" /root/DATA/products/ProductName.json`
- Authors of documents are typically mentioned with phrasing like "I've shared the [Document]" or "I've created..."
- Reviewers are those who reply with feedback/suggestions

### Finding URLs
- URLs in Slack messages are formatted as `<URL|display text>` or just plain URLs
- Use grep to extract: `grep -oP '<https?://[^|>]+' file.json`

### Large file handling
- Product JSON files can be large (>256KB); use grep instead of reading the full file
- Use offset/limit parameters when reading specific sections

## Workflow

1. Identify which product file to search: `/root/DATA/products/<ProductName>.json`
2. Use grep with relevant keywords to locate messages
3. Extract employee IDs and URLs from matching context
4. Cross-reference with `metadata/employee.json` if needed for name-to-ID mapping
