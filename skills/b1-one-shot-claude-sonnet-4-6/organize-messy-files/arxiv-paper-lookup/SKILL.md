---
name: arxiv-paper-lookup
description: Look up arxiv paper metadata (title, abstract, subject) from arxiv IDs to classify papers by topic without reading full PDFs.
---

# Arxiv Paper Lookup Skill

## Overview
When files are named with arxiv IDs (e.g., `2305.12773v1.pdf`), you can extract metadata via the arxiv API to classify papers by subject without downloading/reading the full PDF.

## Extracting Arxiv ID from Filename
```python
import re

def extract_arxiv_id(filename):
    # Strip path and extension
    base = os.path.basename(filename).replace('.pdf', '')
    # Remove version suffix like v1, v2, v3
    arxiv_id = re.sub(r'v\d+$', '', base)
    return arxiv_id  # e.g., "2305.12773"
```

## Fetching Metadata via Arxiv API
```python
import urllib.request
import xml.etree.ElementTree as ET

def fetch_arxiv_metadata(arxiv_id):
    url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    with urllib.request.urlopen(url) as response:
        data = response.read().decode('utf-8')

    root = ET.fromstring(data)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    entry = root.find('atom:entry', ns)
    if entry is None:
        return None

    title = entry.find('atom:title', ns).text.strip()
    summary = entry.find('atom:summary', ns).text.strip()
    categories = [c.get('term') for c in entry.findall('{http://arxiv.org/schemas/atom}primary_category', ns)]

    return {'title': title, 'summary': summary, 'categories': categories}
```

## Batch Fetching (up to 100 IDs at once)
```python
def fetch_batch(arxiv_ids):
    id_list = ','.join(arxiv_ids)
    url = f"http://export.arxiv.org/api/query?id_list={id_list}&max_results={len(arxiv_ids)}"
    # ... parse response
```

## Classification Strategy
- Use title + abstract keywords to classify
- Common arxiv categories: cs.CL, cs.AI (LLM), quant-ph (quantum), gr-qc (black hole), q-bio (DNA/biology)
- Titles are usually sufficient for classification

## Rate Limiting
- Arxiv API allows ~3 requests/second
- Add `time.sleep(0.5)` between batch requests
- Batch up to 100 IDs per request
