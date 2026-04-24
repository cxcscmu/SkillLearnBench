---
name: run2_json-data-extraction
description: Deep parsing and structural querying of nested JSON documents, resolving implicit relations across multi-modal corporate datasets like Slack messages and PRs.
---

# Advanced JSON Data Extraction Skill

This skill provides refined techniques for extracting, associating, and validating relational data in complex JSON environments, typically found in corporate data exports containing interwoven schemas (e.g., Slack messages, Git PRs, meeting transcripts).

## Usage
1. **Schema Discovery:** Use `jq` or Python's `json` module to map the root keys (e.g., `['slack', 'documents', 'meeting_transcripts', 'meeting_chats', 'urls', 'prs']`).
2. **Text Search Automation:** Automate keyword hunting across deeply nested fields (e.g., recursive search for 'strengths and weaknesses' or 'reviewer').
3. **Cross-Referencing IDs:** Trace Employee IDs (`eid_*`) discovered in unstructured text (like feedback summaries) or Slack message metadata to resolve entity roles accurately.
4. **URL Validation:** Programmatically filter metadata objects (like demo link objects inside a `urls` array) matching specific competitor names and extract the exact shared properties.

## Code Example
```python
import json

def find_competitor_demos(filepath, competitors):
    with open(filepath, 'r') as f:
        data = json.load(f)
    urls = data.get('urls', [])
    return [u['link'] for u in urls if any(comp.lower() in u['link'].lower() for comp in competitors)]
```