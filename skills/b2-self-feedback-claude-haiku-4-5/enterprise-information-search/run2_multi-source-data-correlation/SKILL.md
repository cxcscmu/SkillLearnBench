---
name: multi-source-data-correlation
description: Correlate and merge data from multiple sources (documents, Slack, meetings, URLs) to answer enterprise questions.
---

# Multi-Source Data Correlation

## Overview
This skill covers strategies for correlating data across multiple sources (structured documents, chat platforms, meeting transcripts, external URLs) to extract comprehensive answers to business questions.

## Understanding Multi-Source Data Structures

### ContentForce Example Structure
```
├── documents/      - Structured reports with metadata (author, feedback, date)
├── slack/          - Message threads with authors and reactions
├── meeting_transcripts/ - Attendee lists and discussion content
├── meeting_chats/  - Real-time chat during meetings
└── urls/           - Referenced links with descriptions
```

## Key Patterns for Multi-Source Queries

### Pattern 1: Document Authors and Reviewers
```python
def extract_document_contributors(docs, slack_data, meetings):
    """Extract authors and reviewers from documents"""
    contributors = {'authors': set(), 'reviewers': set()}

    # 1. Extract explicit authors from document metadata
    for doc in docs:
        if 'author' in doc:
            contributors['authors'].add(doc['author'])

    # 2. Find Slack discussions about the documents
    # Look for messages mentioning the document ID or title
    doc_ids = [doc.get('id') for doc in docs]
    doc_titles = [doc.get('type') for doc in docs]

    for msg in slack_data:
        text = msg.get('Message', {}).get('User', {}).get('text', '')
        user = msg.get('Message', {}).get('User', {}).get('userId', '')

        # Check if this message discusses the document
        if any(doc_id in text for doc_id in doc_ids) or \
           any(title.lower() in text.lower() for title in doc_titles):

            # The original author shares it
            if 'shared' in text.lower():
                # This is the author confirming they shared it
                pass
            else:
                # Others commenting are potential reviewers
                if user not in contributors['authors']:
                    contributors['reviewers'].add(user)

        # Check thread replies
        for reply in msg.get('ThreadReplies', []):
            reply_text = reply.get('text', '')
            reply_user = reply.get('userId', '')

            if any(doc_id in reply_text for doc_id in doc_ids) or \
               any(title.lower() in reply_text.lower() for title in doc_titles):
                if reply_user not in contributors['authors']:
                    contributors['reviewers'].add(reply_user)

    # 3. Meeting participants who reviewed
    for meeting in meetings:
        # Participants in meetings about the documents are reviewers
        if 'contentforce' in meeting.get('id', '').lower():
            participants = meeting.get('participants', [])
            # Remove known authors from reviewers
            reviewers = [p for p in participants if p not in contributors['authors']]
            contributors['reviewers'].update(reviewers)

    return contributors
```

### Pattern 2: Extracting Competitive Intelligence
```python
def extract_competitor_insights(slack_data):
    """Find team members discussing specific competitors"""
    competitors = {}

    # Known competitor keywords
    competitor_keywords = {
        'PitchPerfect': ['pitchperfect'],
        'ConvoSuggest': ['convosuggest'],
        'SalesMate': ['salesmate'],
    }

    insights = {competitor: {'discussers': set(), 'topics': []}
               for competitor in competitor_keywords}

    for msg in slack_data:
        text = msg.get('Message', {}).get('User', {}).get('text', '')
        user = msg.get('Message', {}).get('User', {}).get('userId', '')

        for competitor, keywords in competitor_keywords.items():
            if any(kw in text.lower() for kw in keywords):
                insights[competitor]['discussers'].add(user)

                # Extract topics discussed
                if 'strength' in text.lower() or 'advantage' in text.lower():
                    insights[competitor]['topics'].append('strengths')
                if 'weakness' in text.lower() or 'drawback' in text.lower():
                    insights[competitor]['topics'].append('weaknesses')

        # Also check thread replies
        for reply in msg.get('ThreadReplies', []):
            reply_text = reply.get('text', '')
            reply_user = reply.get('userId', '')

            for competitor, keywords in competitor_keywords.items():
                if any(kw in reply_text.lower() for kw in keywords):
                    insights[competitor]['discussers'].add(reply_user)

    return insights
```

### Pattern 3: URL Correlation by Type
```python
def extract_urls_by_category(urls, category_keywords):
    """Extract and categorize URLs from data"""
    categorized = {cat: [] for cat in category_keywords}

    for url_obj in urls:
        link = url_obj.get('link', '')
        description = url_obj.get('description', '')

        for category, keywords in category_keywords.items():
            # Check if link or description matches category
            full_text = f"{link} {description}".lower()
            if any(kw.lower() in full_text for kw in keywords):
                categorized[category].append(link)
                break

    return categorized
```

### Pattern 4: Deduplication and Validation
```python
def validate_employee_ids(employee_ids, employee_db):
    """Validate extracted employee IDs against employee database"""
    valid_ids = []
    invalid_ids = []

    for eid in employee_ids:
        if eid in employee_db:
            valid_ids.append(eid)
        else:
            invalid_ids.append(eid)

    return valid_ids, invalid_ids
```

## Query Strategy

1. **Start with explicit data** - Documents with author fields
2. **Expand through Slack discussions** - Find who commented/reviewed
3. **Cross-reference with meetings** - Validate with meeting attendance
4. **Extract URLs and metadata** - Links embedded in messages/documents
5. **Deduplicate and validate** - Remove duplicates, verify against employee DB
6. **Correlate themes** - Link competitor discussions to specific products

## Common Challenges and Solutions

| Challenge | Solution |
|-----------|----------|
| Multiple data sources have different IDs | Map all ID formats early, create lookup tables |
| Implicit vs explicit reviewers | Consider both: explicit (marked as reviewer) and implicit (participated in discussions) |
| Duplicate data across sources | Use sets for deduplication, track source |
| Missing structured reviewer info | Fall back to Slack engagement, meeting participation |
| Nested URLs in message text | Use regex to extract all URLs from text fields |

## Performance Tips

- Load all data sources once at the beginning
- Use sets for IDs/URLs to auto-deduplicate
- Create lookup dicts for O(1) reference lookups
- Process Slack messages in batches for large datasets
- Cache mapping results between data sources

