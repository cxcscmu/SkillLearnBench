---
name: multi-hop-evidence-extraction
description: Extract evidence from all three tiers (explicit reviewers, substantive feedback contributors from Slack and transcripts, and other identifiable contributors). Follow artifact references and traverse relationships to collect complete answer sets.
---

# Multi-Hop Evidence Extraction Skill

## Step 1: Tier 1 - Explicit Reviewer/Approver Fields
- Locate explicit "reviewers", "approvers", "assigned_to" fields in artifacts
- Extract all names/IDs listed
- Track the source field name for each person

## Step 2: Tier 2 - Substantive Feedback Contributors
- Search artifact for linked Slack conversations and meeting transcripts
- **For Slack replies**: Extract names of people who provided substantive feedback or comments
  - Do NOT include people who merely reacted or said "thanks"
  - Include people who asked questions, suggested changes, or provided critique
- **For meeting transcripts**: Extract names of people who:
  - Actually spoke in the transcript (check dialogue)
  - Provided substantive feedback, suggestions, or decisions
  - **Do NOT include people listed only in a `participants` array without speaking**

## Step 3: Multi-Hop Reference Traversal
- For each extracted person/artifact, check if they reference other artifacts or people
- Follow "related_artifacts", "depends_on", "references" links
- Recursively extract reviewers from referenced artifacts
- Traverse up to 3 hops to catch indirect relationships
- Track the traversal path for validation

## Step 4: Tier 3 - Other Identified Contributors
- Identify any other people who contributed (authors, editors, signers)
- Exclude people already captured in Tiers 1-2
- Only include if they have a substantive role

## Step 5: Deduplicate and Return
- Remove duplicates across all three tiers
- Return as a list of unique names/IDs
- Document which tier each person came from (for debugging)