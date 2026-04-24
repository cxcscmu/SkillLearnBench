---
name: enterprise-search
description: Search and query enterprise JSON data to find specific information like employee IDs, document references, URLs, and insights. Use this skill when you need to locate answers to business questions such as finding authors of reports, team members with specific insights, or shared URLs. Handles multi-step queries, filtering, and deduplication of results.
---

## Enterprise Data Search Strategies

### Finding Document Authors and Reviewers
**Pattern**: Search for document name + extract userId from messages mentioning it

```bash
# Find all messages mentioning a specific report
grep -i "market research report\|market research" /root/DATA/products/ContentForce.json

# Extract from those messages: the userId (author/reviewer)
grep -i "market research" /root/DATA/products/ContentForce.json | grep -o '"userId":"[^"]*"' | cut -d'"' -f4
```

### Finding Team Members with Specific Insights
**Pattern**: Search for keywords related to competitor products or strengths/weaknesses

```bash
# Search for competitor mentions
grep -i "competitor\|strengths\|weaknesses\|advantages\|disadvantages" /root/DATA/products/ContentForce.json

# Extract userIds from those messages
grep -i "competitor\|strengths\|weaknesses" /root/DATA/products/ContentForce.json | grep -o '"userId":"[^"]*"' | cut -d'"' -f4
```

### Finding Shared URLs/Demo URLs
**Pattern**: Search for URLs, links, and demo references

```bash
# Find all URLs in messages
grep -o 'https*://[^" |<]*' /root/DATA/products/ContentForce.json | sort -u

# Find demo-related URLs specifically
grep -i "demo\|url\|link" /root/DATA/products/ContentForce.json | grep -o 'https*://[^" |<]*'
```

### Deduplication and Formatting
```bash
# Remove duplicates and sort
grep -o 'eid_[a-f0-9]*' file.json | sort -u

# Count results
grep -o 'eid_[a-f0-9]*' file.json | sort -u | wc -l
```

## Question Answering Workflow

1. **Parse the question** - Identify key terms (report names, keywords, types)
2. **Search the product JSON** - Use grep to find relevant messages
3. **Extract entities** - Get userIds, URLs, or other requested information
4. **Deduplicate** - Ensure unique results using `sort -u`
5. **Format** - Convert to the required output format (list of IDs/URLs)

## Product Files Location
- Main data: `/root/DATA/products/`
- Each product has a `.json` file (e.g., `ContentForce.json`)
- Look for both primary product and competitor product files
