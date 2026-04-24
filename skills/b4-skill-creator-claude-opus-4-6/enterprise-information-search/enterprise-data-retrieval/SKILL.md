---
name: enterprise-data-retrieval
description: >
  Retrieve structured answers from enterprise product JSON data files.
  Use this skill when querying product data stored in JSON format under /root/DATA/,
  including product documents, slack messages, meeting transcripts, PRs, and URLs.
  Triggers on questions about employee IDs, authors, reviewers, competitor products,
  or any structured enterprise data lookup.
---

# Enterprise Data Retrieval

## Data Structure

Enterprise data lives under `/root/DATA/` with two subdirectories:

- `metadata/` — employee.json, customers_data.json, salesforce_team.json
- `products/` — One JSON file per product (e.g., ContentForce.json)

### Product JSON Schema

Each product file contains:
- `slack` — List of Slack messages with Channel, Message (User, text, timestamp), ThreadReplies, Reactions
- `documents` — List of docs with content, date, author (employee ID), type, feedback, document_link
- `meeting_transcripts` — List with transcript text, date, participants, document_type
- `meeting_chats` — List of meeting chat messages
- `urls` — List of links with description
- `prs` — List of pull requests with title, summary, reviews, user

### Slack Message Schema

```json
{
  "Channel": {"name": "channel-name", "channelID": "ch-xxx"},
  "Message": {
    "User": {"userId": "eid_xxx", "timestamp": "...", "text": "...", "utterranceID": "..."},
    "Reactions": []
  },
  "ThreadReplies": [
    {"User": {"userId": "eid_xxx", "text": "..."}}
  ]
}
```

## Retrieval Strategy

1. **Parse the question** to identify: product name, entity type (document, slack, PR), and target info (employee IDs, URLs, names).
2. **Load the product JSON** and search relevant sections.
3. **For document queries**: Check `author` field and `feedback` field. Search slack for discussion threads about the document.
4. **For competitor queries**: Search slack messages for competitor product names. Track all participants in those discussion threads.
5. **For URL queries**: Search slack messages and the `urls` section for links matching the criteria.

## Key Patterns

- Document authors are stored as employee IDs (e.g., `eid_xxx`) in the `author` field.
- Document reviewers are found in Slack discussions — look for messages between the initial document share and the updated version share.
- Competitor discussions happen across multiple channels. Search all channels for competitor product names.
- Slack conversations are sequential — messages following a topic-starter in the same channel are part of that discussion until the topic changes.

## Output Format

Return answers as lists of strings (employee IDs, URLs, etc.) even for single items.
