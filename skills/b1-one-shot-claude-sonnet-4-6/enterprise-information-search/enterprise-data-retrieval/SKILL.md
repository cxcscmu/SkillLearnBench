---
name: enterprise-data-retrieval
description: Techniques for retrieving and querying structured enterprise data from JSON files containing slack messages, documents, meeting transcripts, and URLs.
---

# Enterprise Data Retrieval

## Data Structure
Enterprise data is typically organized by product in `/root/DATA/products/<ProductName>.json` with the following top-level keys:
- `slack`: list of slack messages with `Channel`, `Message`, `ThreadReplies`, `id`
- `documents`: list of docs with `content`, `date`, `document_link`, `author`, `type`, `id`
- `meeting_transcripts`: list of transcripts with `transcript`, `date`, `document_type`, `participants`, `id`
- `meeting_chats`: list of chat messages
- `urls`: list of URLs with `link`, `description`, `id`
- `prs`: list of PRs with `title`, `summary`, `link`, `mergeable`, `merged`, `number`, `state`, `user`, `created_at`, `reviews`, `id`

## Finding Documents by Type
```python
import json

with open('/root/DATA/products/ContentForce.json') as f:
    data = json.load(f)

# Find documents by type (e.g., "Market Research Report")
docs = [d for d in data['documents'] if 'market research' in d['type'].lower() or 'market research' in d['content'].lower()]
```

## Finding Authors and Reviewers
```python
# Documents have an 'author' field; PRs have 'user' and 'reviews'
for doc in docs:
    print(doc['author'])  # author employee ID or name

# For PRs
for pr in data['prs']:
    print(pr['user'])  # PR author
    for review in pr['reviews']:
        print(review)  # reviewer info
```

## Searching Slack for Keywords
```python
keyword = 'competitor'
results = []
for msg in data['slack']:
    if keyword.lower() in msg['Message'].lower():
        results.append(msg)
    for reply in msg.get('ThreadReplies', []):
        if keyword.lower() in reply.lower():
            results.append({'parent': msg, 'reply': reply})
```

## Metadata Files
- `/root/DATA/metadata/employee.json`: employee records mapping IDs to names
- `/root/DATA/metadata/customers_data.json`: customer records
- `/root/DATA/metadata/salesforce_team.json`: sales team info
