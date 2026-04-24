---
name: run2_slack-analysis
description: Advanced patterns for analyzing Slack conversations to extract reviewers, competitor insights, and shared resources from enterprise product channels.
---

# Slack Analysis for Enterprise Data

## Channel Naming Conventions
- `planning-<Product>` - early planning discussions, document reviews
- `planning-<Product>-PM` - product management planning
- `develop-<person>-<Product>` - development phase per contributor
- `bug-<person>-<Product>` - bug tracking discussions

## Document Review Workflow
1. Author shares draft: message contains document link
2. Team provides feedback as sequential messages (not thread replies)
3. Author summarizes changes
4. Author shares final version with "final_" prefix in link
5. Key reviewers = all who gave substantive feedback between draft and final

## Competitor Analysis Identification
Primary insight providers are those who:
- Initiate discussions about competitor products ("I was reading about X...")
- Provide detailed descriptions of features, strengths, or weaknesses
- Answer follow-up questions with substantive information

Secondary participants (not insight providers):
- Those who only ask questions
- Those who say "thanks", "agreed", "interesting"
- Those who suggest leveraging insights without adding new information

## Common Pitfalls
- Messages may appear in multiple search results due to overlapping windows
- Same competitor may be discussed in multiple channels by different people
- Distinguish internal product demos from competitor demos by URL domain
- "entAIX" was the original name for ContentForce (renamed during development)
