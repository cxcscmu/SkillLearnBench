---
name: report-generator
description: How to process GitHub API JSON output into a structured report.json for monthly analytics. Use this whenever you have raw JSON data from the gh CLI.
---

## Overview
This skill outlines how to process raw JSON output from `gh` into the required `report.json` format.

## Required Fields
- **PRs**:
  - `total`: Count of created PRs.
  - `merged`: Count of merged PRs.
  - `closed`: Count of closed (not merged) PRs.
  - `avg_merge_days`: Average days from creation to merge.
  - `top_contributor`: Person with the most opened PRs.
- **Issues**:
  - `total`: Count of created issues.
  - `bug`: Count of issues labeled with 'bug' (substring match).
  - `resolved_bugs`: Count of bug issues closed within the month.

## Process
1. Save raw data to temporary files (e.g., `prs.json`, `issues.json`).
2. Use Python (or jq) to aggregate the metrics.
3. Output the JSON in the exact schema provided in the request.
