---
name: run2_enterprise-product-data-analysis
description: Advanced techniques for analyzing complex enterprise product JSON files containing messages, documents, and transcripts.
---

# Enterprise Product Data Analysis

Enterprise product data often combines unstructured communication (Slack messages) with structured documents and meeting transcripts.

## 1. Document-Centric Retrieval
Documents are usually stored in a `documents` array. Each entry has metadata like `author`, `type`, `feedback`, and `document_link`. To find reviewers, trace the `feedback` comments back to the `Message` objects in the same file.

## 2. Transcript and Message Correlation
When a task asks for "key reviewers", correlate the `feedback` field in `documents` with the `User` IDs who made similar suggestions in the `Message` history.

## 3. Handling Large Files Surgicaly
For files over 500KB, use `grep_search` to find line numbers and `read_file` with narrow ranges (±10 lines) to understand the context of mentions.

## 4. Entity Mapping
Consolidate mappings between `userId` and names early by sampling `employee.json`. Note that some IDs might not be present in all metadata files, requiring a search across the entire `/root/DATA` directory.
