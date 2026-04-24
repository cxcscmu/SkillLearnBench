name: data-retrieval
description: How to search and extract information from large JSON data files. Use this skill whenever you need to process JSON files in /root/DATA to answer specific questions.

# Data Retrieval from JSON

This skill provides strategies for efficiently extracting information from JSON data files.

## Strategies

- **Large File Handling**: When dealing with large JSON files, avoid reading the entire file at once if possible. Use `grep_search` to find keywords and then read specific lines around the matches.
- **Key-Value Identification**: Identify the core keys (e.g., "Market Research Report", "Competitors", "Team Members") before diving into the content.
- **Data Filtering**: Use the structure of the JSON to filter relevant sections (e.g., look for an array of "competitors" or "team_members").
- **Multiple Files**: When a query requires data from multiple files (e.g., mapping employee names to IDs), perform the search in parallel or sequential steps to link the information.

## Patterns

- **Question to Key Mapping**:
  - "Market Research Report" -> `market_research_report` or similar keys.
  - "Competitors" -> `competitors`.
  - "Team Members" -> `team_members` or `employees`.
  - "Insights/Strengths/Weaknesses" -> Look for these keywords within competitor descriptions or feedback arrays.
  - "Demo URLs" -> Search for "http" or "url" within relevant sections.
