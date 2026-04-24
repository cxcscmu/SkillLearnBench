---
name: json-data-extraction
description: Extract, parse, and query JSON data from large enterprise files efficiently
---

# JSON Data Extraction from Enterprise Data

## Overview
This skill covers parsing and extracting information from large JSON files containing enterprise data like employee records, Slack messages, and product metadata.

## Use Cases
- Extracting specific fields from employee databases
- Searching through Slack message histories for mentions or keywords
- Finding relationships between employees and documents/reports
- Aggregating data across multiple JSON sources

## Installation & Setup
```bash
# Python has built-in json module, no installation needed
python3 -c "import json; print('JSON module available')"
```

## Code Examples

### Basic JSON Loading
```python
import json

with open('/root/DATA/metadata/employee.json', 'r') as f:
    employee_data = json.load(f)

# Access specific employee
employee = employee_data.get('eid_1e9356f5', {})
```

### Extracting Data with Filters
```python
import json

with open('/root/DATA/products/ContentForce.json', 'r') as f:
    product_data = json.load(f)

# Extract Slack messages mentioning specific employee
messages = product_data.get('slack', [])
for msg in messages:
    if 'Market Research Report' in msg.get('Message', {}).get('text', ''):
        print(msg)
```

### Extracting IDs from Text
```python
import re

def extract_employee_ids(text):
    """Extract employee IDs (format: eid_xxxxxxxx) from text"""
    pattern = r'eid_[a-f0-9]{8}'
    return re.findall(pattern, text)

# Usage
text = "@eid_1e9356f5 created this channel. @eid_06cddbb3 joined."
ids = extract_employee_ids(text)  # Returns ['eid_1e9356f5', 'eid_06cddbb3']
```

### Finding Report Authors and Reviewers
```python
import json
import re

def find_report_authors_and_reviewers(product_json_path, report_name):
    """Find employees who authored/reviewed a report"""
    with open(product_json_path, 'r') as f:
        data = json.load(f)

    authors = set()
    reviewers = set()

    messages = data.get('slack', [])
    for msg in messages:
        text = msg.get('Message', {}).get('text', '')
        if report_name.lower() in text.lower():
            # Author: person sharing the report
            author_id = msg.get('Message', {}).get('User', {}).get('userId')
            if author_id and author_id.startswith('eid_'):
                authors.add(author_id)

            # Reviewers: people responding in thread
            for reply in msg.get('ThreadReplies', []):
                reviewer_id = reply.get('User', {}).get('userId')
                if reviewer_id and reviewer_id.startswith('eid_'):
                    reviewers.add(reviewer_id)

    return list(authors), list(reviewers)
```

## Best Practices
1. **Memory Efficiency**: For large files, process in chunks rather than loading entire file
2. **Error Handling**: Always check if keys exist before accessing nested values
3. **ID Pattern Matching**: Employee IDs follow format `eid_` followed by 8 hex characters
4. **Text Search**: Use case-insensitive matching for report/document names
5. **Deduplication**: Use sets to avoid duplicate IDs before converting to lists

## Common Patterns

### Pattern 1: Search for Document Mentions
Look for link syntax in Slack: `<https://...|Report Name>`

### Pattern 2: Extract User IDs from Messages
- Author: `Message.User.userId`
- Reviewers: `Message.ThreadReplies[].User.userId`
- Mentions: Look for `@eid_` patterns in message text

### Pattern 3: Cross-Reference Data
Load employee.json to map IDs to names if needed for verification

## Token Tracking
When using this with APIs, track token consumption:
```python
# After API calls
tokens_used = response.usage.input_tokens + response.usage.output_tokens
```
