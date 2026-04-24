---
name: json-extraction
description: Skill to extract information from the structured JSON data, including Slack messages and document metadata.
---

# JSON Extraction Skill

This skill covers how to efficiently navigate and extract information from the enterprise data JSON files.

## Data Structure
The product data files (e.g., `/root/DATA/products/Product.json`) typically have the following structure:
- `slack`: A list of channel messages. Each message has a `User`, `text`, and `timestamp`.
- `documents`: A list of document metadata, including `author`, `date`, `type`, and `content`.
- `meeting_transcripts`: Transcripts of meetings.
- `urls`: Shared URLs and their descriptions.

## Techniques
### Extracting Document Authors and Reviewers
1. Search the `documents` list for a specific `type` (e.g., "Market Research Report").
2. Identify the `author` field.
3. Search `slack` messages around the document's `date` to find discussions and feedback.
4. Users who provide specific suggestions or critiques in the Slack threads are considered reviewers.

### Identifying Competitor Insights
1. Search `slack` messages and `meeting_transcripts` for keywords like "competitor", "strengths", "weaknesses", or specific competitor names (e.g., "Salesforce", "HubSpot").
2. Map the `userId` from those messages to identify the team members.

### Finding Shared URLs
1. Search the `slack` messages for "http" or "demo".
2. Cross-reference with the `urls` list in the JSON if available.
