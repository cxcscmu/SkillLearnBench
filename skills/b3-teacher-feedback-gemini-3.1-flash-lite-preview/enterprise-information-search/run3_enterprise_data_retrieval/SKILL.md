---
name: enterprise_data_retrieval
description: Use this to search, filter, and navigate enterprise artifacts (/root/DATA) to answer specific questions, ensuring cross-product isolation and multi-hop link traversal.
---
To retrieve accurate information:
1. **Identify Product Scope**: Parse the question to determine the product context. Navigate specifically to `/root/DATA/products/<Product>/` to ensure data isolation.
2. **Contextual Search**: Scan relevant sub-directories (e.g., `meetings/`, `slack/`, `docs/`) using keyword extraction from the question.
3. **Multi-hop Traversal**: If an artifact references an external entity (e.g., "see PR #123" or "discussed by Alice"), perform a secondary lookup in the corresponding `/root/DATA/` sub-directories to resolve the link.
4. **Validation**: Verify that the extracted entity matches the intent of the question before finalizing the list.