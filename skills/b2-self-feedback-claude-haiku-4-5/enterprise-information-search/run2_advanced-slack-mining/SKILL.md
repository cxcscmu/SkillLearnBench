---
name: advanced-slack-mining
description: Mine Slack data for embedded URLs, mentioned products, competitive intelligence, and cross-referencing with external data sources.
---

# Advanced Slack Data Mining

## Overview
This skill covers sophisticated techniques for extracting data from Slack messages including embedded URLs, product mentions, competitive intelligence, and correlating with external data sources.

## URL Extraction from Messages

### Basic URL Pattern Matching
```python
import re

def extract_all_urls(text):
    """Extract all URLs from text using regex"""
    url_pattern = r'https?://[^\s\)\"\']+|<(https?://[^\|>]+)[^\>]*>'

    matches = re.findall(url_pattern, text)
    urls = []

    for match in matches:
        if isinstance(match, tuple):
            urls.append(match[1] if match[1] else match[0])
        else:
            urls.append(match)

    return urls

# Slack-formatted URLs are often like: <https://example.com|Text>
def extract_slack_formatted_urls(text):
    """Extract URLs from Slack format"""
    pattern = r'<(https?://[^\|>]+)\|([^>]+)>'
    matches = re.findall(pattern, text)
    return [url for url, _ in matches]
```

### Categorizing URLs by Type
```python
def categorize_urls(urls):
    """Categorize URLs by domain/type"""
    categories = {
        'demo': [],
        'documentation': [],
        'blog': [],
        'github': [],
        'slack_internal': [],
        'other': []
    }

    for url in urls:
        url_lower = url.lower()

        if 'demo' in url_lower:
            categories['demo'].append(url)
        elif 'docs' in url_lower or 'documentation' in url_lower:
            categories['documentation'].append(url)
        elif 'blog' in url_lower or 'medium' in url_lower or 'towards' in url_lower:
            categories['blog'].append(url)
        elif 'github' in url_lower:
            categories['github'].append(url)
        elif 'slack.com/archives' in url_lower:
            categories['slack_internal'].append(url)
        else:
            categories['other'].append(url)

    return categories
```

## Competitive Product Intelligence

### Identifying Competitor Mentions
```python
def extract_competitor_mentions(slack_data, competitors_dict):
    """
    competitors_dict: {
        'CompetitorName': {
            'keywords': ['keyword1', 'keyword2'],
            'discussers': set(),
            'topics': [],
            'quotes': []
        }
    }
    """
    results = {name: dict(comp) for name, comp in competitors_dict.items()}

    for msg in slack_data:
        msg_text = msg.get('Message', {}).get('User', {}).get('text', '')
        msg_user = msg.get('Message', {}).get('User', {}).get('userId', '')
        timestamp = msg.get('Message', {}).get('User', {}).get('timestamp', '')

        for competitor, info in results.items():
            keywords = info['keywords']

            if any(kw.lower() in msg_text.lower() for kw in keywords):
                # Record the discusser
                info['discussers'].add(msg_user)

                # Extract topics
                if 'strength' in msg_text.lower() or 'advantage' in msg_text.lower():
                    info['topics'].append({'topic': 'strengths', 'timestamp': timestamp})

                if 'weakness' in msg_text.lower() or 'limitation' in msg_text.lower():
                    info['topics'].append({'topic': 'weaknesses', 'timestamp': timestamp})

                if 'feature' in msg_text.lower():
                    info['topics'].append({'topic': 'features', 'timestamp': timestamp})

                # Store quote snippet
                if len(msg_text) < 300:
                    info['quotes'].append(msg_text)

    return results
```

### Finding Product Insights in Context
```python
def extract_product_insights(slack_data, product_names):
    """Find detailed insights about specific products"""
    insights = {product: {'discussed_in': [], 'contexts': []} for product in product_names}

    for i, msg in enumerate(slack_data):
        msg_text = msg.get('Message', {}).get('User', {}).get('text', '')
        msg_user = msg.get('Message', {}).get('User', {}).get('userId', '')

        for product in product_names:
            if product.lower() in msg_text.lower():
                insights[product]['discussed_in'].append({
                    'message_index': i,
                    'user': msg_user,
                    'text': msg_text[:200]
                })

                # Extract context - what was being discussed
                if 'demo' in msg_text.lower():
                    insights[product]['contexts'].append('demo')
                if 'api' in msg_text.lower():
                    insights[product]['contexts'].append('api')
                if 'integration' in msg_text.lower():
                    insights[product]['contexts'].append('integration')

    return insights
```

## Cross-Referencing Slack with External Data

### Linking Slack Mentions to Document References
```python
def correlate_slack_mentions_with_documents(slack_data, documents):
    """Find Slack discussion of documents and extract reviewer info"""
    correlations = {}

    # Extract document identifiers
    doc_map = {doc.get('id'): doc for doc in documents}

    for msg in slack_data:
        msg_text = msg.get('Message', {}).get('User', {}).get('text', '')
        msg_user = msg.get('Message', {}).get('User', {}).get('userId', '')

        # Check if any document is mentioned
        for doc_id in doc_map.keys():
            if doc_id in msg_text:
                if doc_id not in correlations:
                    correlations[doc_id] = {
                        'document': doc_map[doc_id],
                        'slack_discussions': []
                    }

                correlations[doc_id]['slack_discussions'].append({
                    'user': msg_user,
                    'message': msg_text[:150],
                    'thread_replies': len(msg.get('ThreadReplies', []))
                })

    return correlations
```

### Linking Slack URLs to URL Database
```python
def match_slack_urls_to_database(slack_data, url_database):
    """Find which URLs are mentioned in Slack and by whom"""
    url_mentions = {}

    for msg in slack_data:
        msg_text = msg.get('Message', {}).get('User', {}).get('text', '')
        msg_user = msg.get('Message', {}).get('User', {}).get('userId', '')
        timestamp = msg.get('Message', {}).get('User', {}).get('timestamp', '')

        # Extract URLs from this message
        urls_found = extract_all_urls(msg_text)

        for url in urls_found:
            # Normalize URL
            url_clean = url.rstrip('/')

            # Check if it's in our database
            for db_url_obj in url_database:
                db_url = db_url_obj.get('link', '').rstrip('/')
                if db_url == url_clean or db_url in url_clean or url_clean in db_url:
                    if db_url not in url_mentions:
                        url_mentions[db_url] = {
                            'mentioned_by': set(),
                            'mentions': []
                        }

                    url_mentions[db_url]['mentioned_by'].add(msg_user)
                    url_mentions[db_url]['mentions'].append({
                        'user': msg_user,
                        'timestamp': timestamp,
                        'context': msg_text[:100]
                    })

    return url_mentions
```

## Advanced Patterns

### Finding Discussion Chains
```python
def trace_discussion_chain(slack_data, starting_msg_idx):
    """Trace a discussion thread and participants"""
    chain = {
        'main_message': slack_data[starting_msg_idx],
        'thread_participants': set(),
        'topics': [],
        'evolution': []
    }

    main_msg = slack_data[starting_msg_idx]
    main_user = main_msg.get('Message', {}).get('User', {}).get('userId', '')

    for reply in main_msg.get('ThreadReplies', []):
        reply_user = reply.get('userId', '')
        if reply_user and reply_user != main_user:
            chain['thread_participants'].add(reply_user)
            chain['evolution'].append({
                'user': reply_user,
                'text': reply.get('text', '')[:150]
            })

    return chain
```

### Sentiment Analysis for Review Comments
```python
def analyze_review_sentiment(thread_replies):
    """Analyze feedback tone from thread replies"""
    positive_words = ['good', 'great', 'excellent', 'agree', 'looks good', 'nice']
    negative_words = ['issue', 'problem', 'concern', 'need', 'should']

    sentiment = {'positive': [], 'negative': [], 'neutral': []}

    for reply in thread_replies:
        text = reply.get('text', '').lower()

        has_positive = any(word in text for word in positive_words)
        has_negative = any(word in text for word in negative_words)

        if has_positive and not has_negative:
            sentiment['positive'].append(reply)
        elif has_negative and not has_positive:
            sentiment['negative'].append(reply)
        else:
            sentiment['neutral'].append(reply)

    return sentiment
```

## Complete Workflow Example

```python
def comprehensive_slack_analysis(slack_data, external_data):
    """Complete analysis of Slack for intelligence gathering"""

    analysis = {
        'urls_extracted': [],
        'competitors_discussed': {},
        'documents_mentioned': {},
        'key_contributors': set()
    }

    # 1. Extract all URLs
    all_urls = set()
    for msg in slack_data:
        text = msg.get('Message', {}).get('User', {}).get('text', '')
        urls = extract_all_urls(text)
        all_urls.update(urls)

    analysis['urls_extracted'] = list(all_urls)

    # 2. Find competitor discussions
    competitors = {
        'PitchPerfect': {'keywords': ['pitchperfect', 'pitch perfect']},
        'ConvoSuggest': {'keywords': ['convosuggest', 'convo suggest']},
        'SalesMate': {'keywords': ['salesmate', 'sales mate']},
    }

    analysis['competitors_discussed'] = extract_competitor_mentions(slack_data, competitors)

    # 3. Link documents to discussions
    analysis['documents_mentioned'] = correlate_slack_mentions_with_documents(
        slack_data,
        external_data.get('documents', [])
    )

    # 4. Extract all participants
    for msg in slack_data:
        user = msg.get('Message', {}).get('User', {}).get('userId', '')
        if user:
            analysis['key_contributors'].add(user)

    return analysis
```

## Performance Considerations

- **Regex compilation** - Compile patterns once if used repeatedly
- **Set operations** - Use sets for deduplication to avoid O(n²) comparisons
- **Early filtering** - Filter data before detailed analysis to reduce processing
- **Caching** - Cache extracted URLs and compiled patterns
- **Batch processing** - Process messages in batches for large datasets

