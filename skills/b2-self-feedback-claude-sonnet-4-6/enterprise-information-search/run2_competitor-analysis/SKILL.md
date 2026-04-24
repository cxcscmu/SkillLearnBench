---
name: run2_competitor-analysis
description: Finding competitor product discussions, insights, and demo URLs across all ContentForce-related Slack channels
---

# Competitor Analysis in Slack Data

## Channel Scope for ContentForce
All channels containing "ContentForce" in their name:
- `planning-ContentForce` (main planning, was `planning-entAIX`)
- `planning-ContentForce-PM` (product manager channel)
- `develop-ianjones-ContentForce` (developer channel)
- `develop-emmagarcia-ContentForce` (developer channel)
- `bug-emmagarcia-ContentForce` (bug channel)

## Competitors for ContentForce
- **PitchPerfect AI** - discussed in planning and develop channels
- **SalesMate AI** - discussed in planning channels
- **ConvoSuggest** - discussed in PM and develop channels

## Finding Insight Providers (Q2 pattern)

People who "provided insights" on competitor strengths and weaknesses are those who:
1. Initiated a discussion with "I was reading about X competitor..."
2. Provided detailed feature/weakness analysis
3. NOT just those who replied with acknowledgements ("thanks for the insights!")

```python
# Find insight providers
insight_providers = set()
for msg in data['slack']:
    text = msg['Message']['User']['text']
    user = msg['Message']['User']['userId']
    channel = msg['Channel']['name']

    if 'ContentForce' not in channel:
        continue

    # Initiated competitor insight discussions
    if 'reading about' in text.lower() and any(c in text for c in ['PitchPerfect', 'SalesMate', 'ConvoSuggest']):
        insight_providers.add(user)
```

## ContentForce Competitor Demo URLs (Q3 pattern)
```
https://www.salesmateai.com/demo     -> shared by eid_4350bf70 in planning-ContentForce
https://www.pitchperfectai.com/demo  -> shared by eid_7b85a749 in develop-ianjones-ContentForce
https://www.convosuggest.com/demo    -> shared by eid_f6ae6dd8 in develop-emmagarcia-ContentForce
```

## Market Research Report Key Reviewers (Q1 pattern)
The reviewers are identified by matching the bullet points in the document's `feedback` field
to specific Slack messages from around the same time the document was shared.

| Feedback Item | Reviewer |
|---|---|
| Add key metrics to Executive Summary | eid_06cddbb3 |
| Include integration details in Product Overview | eid_99835861 |
| Enhance Competitive Analysis with comparison chart | eid_2d72674d |
| Expand on analytics capabilities in Customer Needs | eid_c3f3eff2 |
| Specify emerging markets in Growth Opportunities | eid_4350bf70 |
| Elaborate on data privacy measures in Challenges | eid_24dbff62 |
