---
name: run2_enterprise-data-retrieval
description: Complete guide to retrieving structured answers from enterprise product JSON data files containing Slack, documents, meetings, and PRs
---

# Enterprise Data Retrieval

## Data File Structure
Enterprise product JSON files (`/root/DATA/products/<ProductName>.json`) contain:
- `slack`: Array of Slack messages with Channel, Message, ThreadReplies
- `documents`: Array of docs (Market Research Report, PRD, TSD, etc.)
- `meeting_transcripts`: Meeting transcripts
- `meeting_chats`: Meeting chat logs
- `urls`: URL records with link, description, id
- `prs`: GitHub pull request records

## Finding Document Authors and Reviewers

```python
import json

with open('/root/DATA/products/ContentForce.json') as f:
    data = json.load(f)

# Step 1: Get the author from the document
for doc in data['documents']:
    if doc.get('type') == 'Market Research Report':
        author = doc.get('author')  # e.g., 'eid_1e9356f5'
        # The 'feedback' field in the final document lists reviewer suggestions
        feedback = doc.get('feedback', '')
        break

# Step 2: Match Slack messages to identify key reviewers
# Find the conversation where the document was shared and reviewers gave feedback
for msg in data['slack']:
    text = msg['Message']['User']['text']
    user = msg['Message']['User']['userId']
    ts = msg['Message']['User']['timestamp']
    channel = msg['Channel']['name']

    if 'market research' in text.lower() or 'Market Research' in text:
        print(f'{ts} | {channel} | {user}: {text[:200]}')
```

Key insight: Match each bullet point in the document `feedback` field to the Slack user who suggested it.

## Channel Name Mapping
Channels may be renamed during project lifecycle:
- `planning-entAIX` → renamed to `planning-ContentForce` (the product was renamed)
- Check for `slack_admin_bot` messages like "@user renamed the channel to..."

## Finding Competitor Insights

```python
competitor_names = ['PitchPerfect AI', 'SalesMate AI', 'ConvoSuggest']

for msg in data['slack']:
    text = msg['Message']['User']['text']
    user = msg['Message']['User']['userId']
    channel = msg['Channel']['name']

    # People who initiated competitor discussions provided insights
    if any(c in text for c in competitor_names) and 'reading about' in text.lower():
        print(f'{channel} | {user}: {text[:200]}')
```

Note: "Providers of insights" = those who initiated discussions with detailed information, not just those who acknowledged insights from others.

## Finding Demo URLs

Three sources to check:
1. Slack messages containing "demo" and "http"
2. The `urls` array in the data file
3. Thread replies (sometimes URLs appear in replies)

```python
# Method 1: From Slack messages
for msg in data['slack']:
    text = msg['Message']['User']['text']
    if 'demo' in text.lower() and 'http' in text and 'ContentForce' in msg['Channel']['name']:
        # Extract the URL
        import re
        urls = re.findall(r'https?://[^\s<>\"]+', text)
        print(msg['Message']['User']['userId'], urls)

# Method 2: From urls array
for url_entry in data.get('urls', []):
    if 'demo' in url_entry['link'].lower():
        print(url_entry['link'])
```
