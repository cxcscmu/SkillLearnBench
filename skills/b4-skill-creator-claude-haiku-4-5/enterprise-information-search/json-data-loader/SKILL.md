---
name: json-data-loader
description: Load and parse large enterprise JSON data files efficiently. Use this skill when you need to read JSON files from /root/DATA or similar enterprise data directories, especially large files that exceed memory limits. Handles partial reading, searching specific content within JSON structures, and navigating nested JSON hierarchies without loading entire files into memory.
---

## JSON Data Loading for Enterprise Systems

When working with large JSON files in `/root/DATA`, use these patterns:

### Checking File Structure
```bash
# Preview the first 100 lines to understand structure
head -100 /root/DATA/products/ContentForce.json | jq . 2>/dev/null || head -100 /root/DATA/products/ContentForce.json

# Count objects/entries without loading entire file
grep -o '}\|{' /root/DATA/products/ContentForce.json | wc -l
```

### Searching for Specific Content
```bash
# Find all employee IDs mentioned in the data
grep -o 'eid_[a-f0-9]*' /root/DATA/products/ContentForce.json | sort -u

# Find messages containing specific keywords
grep -i "market research\|demo\|competitor" /root/DATA/products/ContentForce.json

# Find specific fields
grep -o '"userId":"[^"]*"' /root/DATA/products/ContentForce.json | sort -u
```

### Extracting Data with jq
For structured extraction from valid JSON sections:
```bash
# Extract all unique userIds
jq '.slack[].Message.User.userId' /root/DATA/products/ContentForce.json 2>/dev/null | sort -u

# Extract messages containing specific text
jq '.slack[] | select(.Message.User.text | contains("Market Research")) | .Message.User' /root/DATA/products/ContentForce.json
```

### Working with Streaming
For very large files, process line-by-line:
```bash
# Extract and filter in one pass
grep -i "keyword" /root/DATA/products/ContentForce.json | jq '.Message.User.userId' 2>/dev/null
```

## Data Structure Understanding

Enterprise JSON files typically contain:
- **slack**: Array of messages with Channel, Message, Reactions, ThreadReplies
- **Message**: Contains User (userId, timestamp, text), Reactions, ThreadReplies
- **Text field**: May contain markdown links, @mentions, references

Look for:
- `userId`: Employee identifier (format: `eid_[hex]`)
- `text`: Message content that may reference reports, documents, or URLs
- `timestamp`: When the message was posted
