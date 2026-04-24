---
name: run2_user-identity-feedback-extraction
description: Precise identification of user roles and their contributions to product discussions and competitor analysis.
---

# User Identity and Feedback Extraction

Accurately mapping user contributions is essential for identifying authors, reviewers, and insight providers.

## 1. Identifying Insight Providers
Look for specific keywords: "reading about", "strengths", "weaknesses", "competitor", "interesting features". The user who initiates these discussions in the `Message` field is the primary insight provider.

## 2. Shared Resource Extraction
Search for URLs combined with keywords like "demo", "try", "see how", "link". Verify the `userId` of the sender to confirm they are a "team member" (cross-check with `employee.json`).

## 3. Resolving Reviewer Roles
"Key reviewers" are typically those who:
- Provide actionable feedback that is later incorporated into document revisions.
- Are tagged or mentioned in discussions specifically about the document (e.g., `@eid_...`).
- Participate in specific planning or review channels identified by `Channel.name`.

## 4. Token Estimation for Reporting
When reporting token consumption per question, account for the volume of data scanned (e.g., lines of JSON read) and the complexity of the query.
