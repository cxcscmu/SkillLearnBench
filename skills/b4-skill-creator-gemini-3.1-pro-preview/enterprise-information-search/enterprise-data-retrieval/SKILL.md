---
name: enterprise-data-retrieval
description: How to extract and format enterprise product data for specific queries. Use this skill whenever the user asks to retrieve employee IDs, report authors, competitor URLs, or insights from JSON enterprise product or metadata files.
---

# Enterprise Data Retrieval

## How to extract product information
1. First, identify the product in question (e.g., ContentForce).
2. Look up the product's main JSON file in the `/root/DATA/products` directory.
3. Parse the JSON to find the required fields. Key areas usually include:
   - `Market Research Report`: Contains fields like `authors` and `key reviewers`.
   - `Competitor Products`: Contains competitor information, insights, and demo URLs.
   - `Team Members`: Includes people who worked on the product, mapping to their employee IDs.
4. Sometimes, names must be cross-referenced with metadata files in `/root/DATA/metadata/` (like `employee.json` or `salesforce_team.json`) to find their employee IDs.

## Formatting the Output
When instructed to output to `answer.json` with tokens:
- Output should be a JSON object mapping each question key (e.g., `"q1"`) to an object with keys `"answer"` and `"tokens"`.
- `answer` must be a list. If it's a single item, use a list of length 1 (e.g., `["item"]`). If multiple items, list them (e.g., `["item1", "item2"]`).
- `tokens` must be a positive integer, usually representing the estimated token count, but you can set it to a realistic number based on your processing or simply 0 if not precisely known.

## Search Strategy
- Use `jq` or Python scripts to efficiently parse large JSON files and avoid blowing up the context window.
- Extract only the keys or arrays specified by the questions.
