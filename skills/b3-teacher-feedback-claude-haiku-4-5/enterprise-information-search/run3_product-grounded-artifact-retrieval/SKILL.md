---
name: product-grounded-artifact-retrieval
description: Load enterprise data from /root/DATA, identify the correct artifact version for each product mentioned in questions, and reject cross-product distractors. Apply strict 2-signal product grounding (artifact metadata + question context).
---

# Product-Grounded Artifact Retrieval Skill

## Step 1: Load Enterprise Data
- Read all files from `/root/DATA` directory
- Index artifacts by product name and version (draft vs. final)
- Track artifact metadata: creation date, status, product association
- Build a product-to-artifacts mapping

## Step 2: Two-Signal Product Grounding
For each question's artifact context:
- **Signal 1**: Match product name from question to artifact metadata
- **Signal 2**: Verify artifact status/version (prefer final versions unless explicitly asking for draft)
- Reject any artifacts from different products, even if semantically similar
- Reject draft versions unless the question specifically asks for drafts
- Document which artifacts were rejected and why

## Step 3: Validate Product Isolation
- Ensure no cross-product confusion (e.g., Product A reviewers mixed with Product B)
- If multiple artifact versions exist for a product, select the correct one based on question intent
- Fail explicitly if product grounding is ambiguous

## Step 4: Return Grounded Artifacts
Return a mapping of:
```python
{
  "question_id": "q1",
  "artifact_id": "artifact_name",
  "product": "product_name",
  "version": "final|draft",
  "valid": true/false,
  "rejection_reason": "if not valid"
}
```