name: enterprise-data-analysis
description: Analyzing relationships between enterprise data entities (employees, products, reports, teams). Use this skill when a question requires connecting different types of information.

# Enterprise Data Analysis

This skill provides a framework for understanding and navigating complex relationships in enterprise datasets.

## Relational Mapping

- **Product to Team**: Look for a "team" or "team_members" field in the product JSON. If it's just names, you'll need to look up their IDs in the `employee.json` file.
- **Product to Competitor**: Products usually have a `competitors` array. This array may contain objects with details like names, strengths, weaknesses, and URLs.
- **Report to Author/Reviewer**: Reports often have `authors` and `reviewers` fields. These are usually lists of names or IDs.
- **Insights to Employee**: Insights about competitors or products may be linked to specific team members who provided them. Check for "provided_by", "member", or "author" fields within feedback or insight arrays.

## Linking Data

1.  **Identify the Source**: Determine which product file contains the core information (e.g., `ContentForce.json`).
2.  **Extract Primary Keys**: Get names or IDs of the relevant people/competitors from the product file.
3.  **Cross-Reference**: If only names are found, look up the `employee.json` to find corresponding IDs.
4.  **Consolidate**: Bring the findings together to form a complete answer (e.g., a list of IDs).
