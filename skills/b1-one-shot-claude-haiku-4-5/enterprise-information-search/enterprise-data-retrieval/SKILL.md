---
name: enterprise-data-retrieval
description: Retrieve and aggregate information across multiple enterprise data sources
---

# Enterprise Data Retrieval

## Overview
Techniques for finding specific information across multiple enterprise data files (employee records, product files, team information) and aggregating results.

## Use Cases
- Finding team members involved in specific projects/products
- Identifying authors and reviewers of documents
- Extracting URLs and resources shared in team communications
- Cross-referencing employee IDs with their information
- Building answer sets from multiple data sources

## Directory Structure
```
/root/DATA/
├── metadata/
│   ├── employee.json          # Employee records with IDs and names
│   ├── customers_data.json    # Customer information
│   └── salesforce_team.json   # Sales team information
└── products/
    ├── ContentForce.json      # Product-specific data (Slack, docs, etc.)
    ├── SecurityForce.json     # Other products...
    └── ...
```

## Code Examples

### Load All Metadata
```python
import json
import os

def load_metadata():
    """Load all metadata files"""
    metadata_path = '/root/DATA/metadata'
    metadata = {}

    for file in os.listdir(metadata_path):
        if file.endswith('.json') and not file.endswith(':Zone.Identifier'):
            with open(os.path.join(metadata_path, file), 'r') as f:
                metadata[file.replace('.json', '')] = json.load(f)

    return metadata

# Usage
metadata = load_metadata()
employees = metadata['employee']
```

### Find Product Data
```python
import json

def load_product_data(product_name):
    """Load product JSON data"""
    path = f'/root/DATA/products/{product_name}.json'
    with open(path, 'r') as f:
        return json.load(f)

# Usage
contentforce_data = load_product_data('ContentForce')
```

### Identify Competitors and Resources
```python
import json
import re

def find_competitor_mentions(product_data):
    """Find all mentions of competitor products"""
    competitors = {}

    messages = product_data.get('slack', [])
    for msg in messages:
        text = msg.get('Message', {}).get('text', '')

        # Look for competitor product mentions (heuristic: Force/Genie products)
        if 'demo' in text.lower() or 'url' in text.lower():
            # Extract URLs
            urls = re.findall(r'https?://[^\s\)]+', text)
            if urls:
                user_id = msg.get('Message', {}).get('User', {}).get('userId')
                competitors[user_id] = urls

    return competitors
```

### Map Employee IDs to Names
```python
def get_employee_info(employee_id, employee_data):
    """Get employee info by ID"""
    return employee_data.get(employee_id, {})

def get_employee_name(employee_id, employee_data):
    """Get employee name by ID"""
    info = get_employee_info(employee_id, employee_data)
    return info.get('name', 'Unknown')
```

## Retrieval Workflow

### Step 1: Load Data
```python
import json

# Load product data
with open('/root/DATA/products/ContentForce.json', 'r') as f:
    product = json.load(f)

# Load employee reference
with open('/root/DATA/metadata/employee.json', 'r') as f:
    employees = json.load(f)
```

### Step 2: Extract Information
```python
# For reports: find who authored/reviewed
# For competitors: find who mentioned them
# For URLs: extract all shared links
```

### Step 3: Deduplicate and Format
```python
# Convert to lists, deduplicate with sets
results = list(set(collected_ids))
```

### Step 4: Validate Against Employee Data
```python
# Verify IDs exist in employee database
valid_ids = [eid for eid in results if eid in employees]
```

## Key Patterns

### Pattern: Report Tracking
- Author: First person to share report link
- Key Reviewers: People providing feedback in thread replies

### Pattern: Competitor Analysis
- Look for messages about "competitor products"
- Extract product names and user IDs from these discussions

### Pattern: Resource Sharing
- Extract URLs from message text
- Associate with user IDs and product context
- Look for explicit "demo URL" mentions

## Error Handling
```python
# Safe nested access
def safe_get(obj, *keys, default=None):
    """Safely navigate nested dicts"""
    for key in keys:
        obj = obj.get(key) if isinstance(obj, dict) else None
        if obj is None:
            return default
    return obj

# Usage
user_id = safe_get(msg, 'Message', 'User', 'userId')
```

## Output Format
Results should be formatted as lists for consistency:
- Single item: `["eid_xxx"]`
- Multiple items: `["eid_xxx", "eid_yyy", "eid_zzz"]`
- Empty result: `[]`
