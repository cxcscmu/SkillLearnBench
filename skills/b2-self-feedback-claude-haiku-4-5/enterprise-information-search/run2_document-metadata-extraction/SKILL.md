---
name: document-metadata-extraction
description: Extract author, reviewer, and feedback information from structured documents and their associated discussions.
---

# Document Metadata Extraction

## Overview
This skill covers extracting metadata (author, date, type, reviewers, feedback) from documents and correlating them with discussion threads and review feedback.

## Document Structure Analysis

### Identifying Document Metadata
```python
def analyze_document_structure(doc):
    """Extract all metadata from a document"""
    metadata = {
        'type': doc.get('type'),           # e.g., 'Technical Specifications'
        'id': doc.get('id'),              # e.g., 'contentforce_tech_spec'
        'author': doc.get('author'),      # e.g., 'eid_8efef28a'
        'date': doc.get('date'),          # Document creation date
        'feedback': doc.get('feedback'),  # Review feedback (often text)
        'document_link': doc.get('document_link'),  # URL to document
        'content_preview': doc.get('content', '')[:200],  # First 200 chars
    }
    return metadata
```

### Understanding Document Feedback Format
```python
def extract_feedback_insights(feedback):
    """Parse feedback string for reviewer comments"""
    if isinstance(feedback, str):
        # Feedback is often a bulleted list of suggestions
        lines = feedback.split('\n')
        suggestions = [line.strip('- ').strip() for line in lines if line.strip()]
        return suggestions
    elif isinstance(feedback, dict):
        # Sometimes structured as dict with reviewers
        return feedback.get('comments', [])
    elif isinstance(feedback, list):
        return feedback
    return []
```

## Identifying Reviewers

### Strategy 1: Slack Document Share Discussions
```python
def find_reviewers_in_slack(slack_msgs, doc_id, doc_type):
    """Find who reviewed/commented on a document in Slack"""
    reviewers = set()

    for msg in slack_msgs:
        msg_text = msg.get('Message', {}).get('User', {}).get('text', '')
        msg_user = msg.get('Message', {}).get('User', {}).get('userId', '')

        # Find the message where document was shared
        if doc_id in msg_text or doc_type.lower() in msg_text.lower():
            if 'shared' in msg_text.lower() or 'shared the' in msg_text.lower():
                # This is the author sharing the document
                author = msg_user

                # Now look for thread replies - these are the reviewers
                for reply in msg.get('ThreadReplies', []):
                    reply_user = reply.get('userId', '')
                    if reply_user and reply_user != 'slack_admin_bot' and reply_user != author:
                        reviewers.add(reply_user)

    return list(reviewers)
```

### Strategy 2: Updated Document Notifications
```python
def extract_reviewers_from_updates(slack_msgs, doc_id):
    """When document is updated with "thank you everyone", find recent participants"""
    reviewers = set()
    thank_you_msgs = []

    # Find "thank you everyone" messages
    for i, msg in enumerate(slack_msgs):
        msg_text = msg.get('Message', {}).get('User', {}).get('text', '')
        if 'thank you everyone' in msg_text.lower() and doc_id in msg_text:
            thank_you_msgs.append(i)

    # Look back from these messages to find earlier discussions
    for thank_you_idx in thank_you_msgs:
        # Scan backwards to find the original share message
        for j in range(thank_you_idx - 1, max(0, thank_you_idx - 50), -1):
            msg = slack_msgs[j]
            msg_text = msg.get('Message', {}).get('User', {}).get('text', '')
            msg_user = msg.get('Message', {}).get('User', {}).get('userId', '')

            if doc_id in msg_text and 'shared' in msg_text.lower():
                # Found the original share, extract thread participants
                for reply in msg.get('ThreadReplies', []):
                    reply_user = reply.get('userId', '')
                    if reply_user and reply_user != 'slack_admin_bot':
                        reviewers.add(reply_user)
                break

    return list(reviewers)
```

### Strategy 3: Meeting Participation
```python
def find_reviewers_in_meetings(meetings, document_type):
    """Find reviewers from meeting attendance on document-related meetings"""
    reviewers = set()

    for meeting in meetings:
        meeting_id = meeting.get('id', '').lower()

        # Check if meeting relates to the document type
        # e.g., 'product_dev_ContentForce' meeting for ContentForce documents
        if 'contentforce' in meeting_id and 'product_dev' in meeting_id:
            participants = meeting.get('participants', [])
            reviewers.update(participants)

    return list(reviewers)
```

## Document Type Handling

### Distinguishing Document Versions
```python
def identify_document_versions(docs):
    """Find original and updated versions of documents"""
    documents = {}

    for doc in docs:
        doc_id = doc.get('id', '')

        # Separate original from final versions
        if 'final_' in doc_id:
            base_id = doc_id.replace('final_', '')
            if base_id not in documents:
                documents[base_id] = {}
            documents[base_id]['final'] = doc
        else:
            if doc_id not in documents:
                documents[doc_id] = {}
            documents[doc_id]['original'] = doc

    return documents
```

### Correlating Versions
```python
def correlate_document_versions(docs, slack_msgs):
    """Find both original and updated versions, track reviewers"""
    result = {}

    versioned = identify_document_versions(docs)

    for base_id, versions in versioned.items():
        if 'original' in versions:
            author = versions['original'].get('author')

            # Find reviewers from Slack discussion about original
            reviewers = find_reviewers_in_slack(slack_msgs, base_id, '')

            result[base_id] = {
                'author': author,
                'original_version': versions.get('original'),
                'final_version': versions.get('final'),
                'reviewers': reviewers
            }

    return result
```

## Practical Workflow

```python
def analyze_documents_completely(docs, slack_data, meetings):
    """Complete analysis pipeline"""
    results = {}

    # Step 1: Get all document metadata
    for doc in docs:
        doc_id = doc.get('id')
        if 'final_' not in doc_id:  # Skip final versions initially
            results[doc_id] = {
                'metadata': analyze_document_structure(doc),
                'author': doc.get('author'),
            }

    # Step 2: Find reviewers through multiple strategies
    for doc_id, data in results.items():
        # Try Slack discussions
        slack_reviewers = find_reviewers_in_slack(slack_data, doc_id, data['metadata']['type'])

        # Try meeting participation
        meeting_reviewers = find_reviewers_in_meetings(meetings, data['metadata']['type'])

        # Combine, remove author from reviewers
        all_reviewers = list(set(slack_reviewers + meeting_reviewers))
        author = data['author']
        data['reviewers'] = [r for r in all_reviewers if r != author]

    return results
```

## Tips

- **Document IDs are key** - Use them to correlate across Slack and other sources
- **Multiple versions** - Always check for both original and "final_" versions
- **Feedback is metadata** - The feedback field often contains reviewer suggestions
- **Slack share dates** - Look for the specific share message to find review threads
- **Meeting attendance** - Cross-check with meeting participants for validation
- **Remove duplicates** - Use sets to deduplicate across different discovery methods

