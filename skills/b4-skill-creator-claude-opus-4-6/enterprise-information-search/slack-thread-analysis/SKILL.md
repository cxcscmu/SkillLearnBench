---
name: slack-thread-analysis
description: >
  Analyze Slack message threads to identify participants, extract insights, and find
  shared resources. Use this skill when tracing who contributed to discussions about
  documents, competitor products, or shared URLs/demos in enterprise Slack data.
---

# Slack Thread Analysis

## Identifying Discussion Participants

Slack messages in enterprise data are stored sequentially per channel. A "discussion thread" consists of:

1. A **starter message** (e.g., someone sharing a document or raising a topic)
2. **Follow-up messages** in the same channel that respond to or build on the starter
3. The thread ends when a new unrelated topic begins

### Finding Document Reviewers

1. Find the message where a document was first shared (contains document link)
2. Collect all messages between the share and the "updated version" share
3. Users who posted substantive feedback in this window are the reviewers
4. The document's `author` field gives the primary author

### Finding Competitor Insight Contributors

1. Search all channels for messages mentioning competitor product names
2. The person who starts the discussion ("I was reading about X...") is the primary contributor
3. Everyone who asks questions or adds observations in the follow-up is also a contributor
4. Check multiple channels — the same competitor may be discussed in different channels

### Finding Shared URLs

- Demo URLs for competitor products are shared with patterns like "try X demo here" or "see how X works"
- Internal product demos use `sf-internal.slack.com/archives/ProductName/demo_N` format
- External competitor demos use the competitor's domain (e.g., `competitor.com/demo`)
- Only include URLs for **competitor** products when asked about competitor demos, not internal product demos

## Important Distinctions

- `sf-internal.slack.com/archives/docs/...` links are document links, not demo URLs
- `sf-internal.slack.com/archives/ProductName/demo_N` links are internal product demos
- External URLs like `competitor.com/demo` are competitor demo URLs
- Blog/article URLs are informational, not demos
