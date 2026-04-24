---
name: run2_enterprise-data-retrieval
description: Comprehensive guide for retrieving structured information from enterprise JSON data files containing Slack messages, documents, meetings, and metadata.
---

# Enterprise Data Retrieval

## Data Layout
- `/root/DATA/metadata/` - employee.json (eid -> name, role, location, org), customers_data.json, salesforce_team.json
- `/root/DATA/products/<ProductName>.json` - per-product data with keys: slack, documents, meeting_transcripts, meeting_chats, urls, prs

## Product JSON Keys

### slack (list)
```json
{
  "Channel": {"name": "planning-ProductName", "channelID": "ch-xxx"},
  "Message": {"User": {"userId": "eid_xxx", "timestamp": "ISO", "text": "..."}, "Reactions": []},
  "ThreadReplies": [{"User": {...}}],
  "id": "utteranceID"
}
```
Note: ThreadReplies are often empty; sequential messages in a channel represent the conversation flow.

### documents (list)
```json
{"content": "...", "date": "ISO", "document_link": "URL", "author": "eid_xxx", "type": "Market Research Report|Product Vision Document|...", "id": "..."}
```
Documents typically have draft and final versions. The final version link contains "final_" prefix.

### urls (list)
```json
{"link": "URL", "description": "...", "id": "..."}
```

## Retrieval Patterns

### Finding Document Authors + Key Reviewers
1. Filter `documents` by `type` matching the document name
2. `author` field gives the document author (employee ID)
3. Search Slack for messages containing the document link
4. Find messages between the draft post and final post timestamps
5. All users who provided feedback (not just "thanks") are key reviewers
6. The author who posted both draft and final is also included

### Finding Competitor Insight Providers
1. Search all Slack messages for competitor product names
2. Identify messages where users share specific features, strengths, or weaknesses
3. "Insight providers" = those who shared substantive information (described features, compared, analyzed)
4. Differentiate from those who just asked questions or said "thanks"

### Finding Competitor Demo URLs
1. Search Slack messages for URL patterns containing competitor names + "demo"
2. Filter out internal product demos (sf-internal URLs)
3. Only include external competitor product demo URLs
