---
name: enterprise-data-retrieval
description: Techniques for retrieving structured information from enterprise Slack/document JSON data files.
---

# Enterprise Data Retrieval from JSON Files

## Overview
Enterprise data files often contain Slack messages, documents, meeting transcripts, and metadata in nested JSON format. This skill covers patterns for efficiently searching and extracting information from these large files.

## Data Structure Pattern
```json
{
  "slack": [
    {
      "Channel": {"name": "...", "channelID": "..."},
      "Message": {
        "User": {"userId": "eid_xxx", "timestamp": "...", "text": "..."}
      },
      "ThreadReplies": []
    }
  ],
  "documents": [
    {
      "content": "...",
      "author": "eid_xxx",
      "type": "Market Research Report",
      "feedback": "...",
      "id": "..."
    }
  ],
  "meeting_transcripts": [...]
}
```

## Key Retrieval Strategies

### 1. Finding Document Authors and Reviewers
- Check `documents` array for `author` field
- Search Slack messages for discussion threads around document sharing
- Match feedback items in final documents to reviewer suggestions in Slack
- The `feedback` field on updated documents lists what changes were incorporated

### 2. Finding Competitor Insights
- Search for messages containing competitor product names
- Look for discussions about "strengths", "weaknesses", "competitor"
- The person who initiates the discussion and provides detailed answers is the primary insight provider

### 3. Finding URLs
- Use grep for URL patterns (https://, demo, etc.)
- Distinguish between internal URLs (sf-internal.slack.com) and external competitor URLs
- Demo URLs for competitor products are external domains

## Tips
- Large JSON files (800KB+) require offset/limit reading or grep-based searching
- Employee IDs follow pattern `eid_[hex]`
- Cross-reference employee IDs with metadata/employee.json for names
