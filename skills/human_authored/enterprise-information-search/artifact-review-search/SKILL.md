---
name: artifact-review-search
description: Multi-hop search over enterprise artifacts to find key reviewers, approvers, feedback contributors, authors, product reports, competitor insights, and demo URLs. Prevents cross-product leakage and prevents treating meeting participants as reviewers.
---

# Artifact Review Search

Use this skill when a question asks for **key reviewers**, approvers, feedback contributors, authors, product reports, competitor insights, or demo URLs across docs, Slack threads, meeting transcripts, PRs, and linked URLs.

It guides the main agent through **multi-hop artifact retrieval + structured entity extraction**. If subagents are available, use a `general-purpose` subagent; otherwise perform the steps directly in the main agent.

Critical reviewer rule:
- Never treat meeting participants as key reviewers unless they appear in explicit reviewer fields or provide substantive feedback in transcript turns, document comments, or Slack replies.
- Prefer explicit reviewers, approvers, and requested reviewers first, then evidence-backed feedback contributors.
- Treat substantive feedback contributors as key reviewers even if their suggestion was not adopted in the final revision or omitted from the author's summary.
- The author's feedback/change summary is corroborative evidence only. It is not an exhaustive reviewer list and must never be used to exclude a substantive contributor who proposed a concrete review change.

This skill is especially useful when report titles repeat across products and the wrong artifact can be selected by surface matching alone.

---

## When to Invoke This Skill

Invoke when ANY of the following is true:

1. The question asks for **key reviewers**, approvers, feedback contributors, or authors tied to a report or artifact.
2. The question requires **multi-hop** evidence gathering (artifact → references → other artifacts).
3. The answer must be **retrieved** from artifacts (IDs/names/dates/roles), not inferred.
4. Evidence is scattered across multiple artifact types (docs + slack + meetings + PRs + URLs).
5. You need **precise pointers** (doc_id/message_id/meeting_id/pr_id) to justify outputs.
6. You must keep context lean and avoid loading large files into context.

---

## Why Use This Skill?

**Without this skill:** you manually grep many files, risk cross-product leakage, and often over-count reviewers by treating attendees as reviewers.

**With this skill:** the main agent, or a `general-purpose` subagent when available:
- grounds the correct product/report before extraction
- finds explicit reviewers, approvers, and feedback contributors
- follows references across channels/meetings/docs/PRs
- extracts structured entities (employee IDs, doc IDs, URLs)
- rejects distractor artifacts
- returns a compact evidence map with artifact pointers

Typical context savings: **70–95%**.

---

## Invocation

Use this format:

```python
Task(subagent_type="general-purpose", prompt="""
Dataset root: /root/DATA
Question: <paste the question verbatim>

Output requirements:
- Return JSON-ready extracted entities (employee IDs, doc IDs, etc.).
- Provide evidence pointers: artifact_id(s) + short supporting snippets.

Constraints:
- Avoid oracle/label fields (ground_truth, gold answers).
- Prefer primary artifacts (docs/chat/meetings/PRs/URLs) over metadata-only shortcuts.
- MUST enforce product grounding: only accept artifacts proven to be about the target product.
- If subagents are unavailable, perform the same procedure directly in the main agent.
""")
```

Important:
- `artifact-review-search` is the skill name, not a runtime subagent type.
- Do not call `subagent_type="artifact-review-search"` unless that agent type is explicitly registered in the runtime.

---

## Core Procedure (Must Follow)

### Step 0 — Parse intent + target product
- Extract:
  - target product name (e.g., “CoachForce”)
  - entity types needed (e.g., author employee IDs, key reviewer employee IDs)
  - artifact types likely relevant (“Market Research Report”, docs, review threads)

If product name is missing in question, infer cautiously from nearby context ONLY if explicitly supported by artifacts; otherwise mark AMBIGUOUS.

---

### Step 1 — Build candidate set (wide recall, then filter)
Search in this order:
1) Product artifact file(s): `/root/DATA/products/<Product>.json` if exists.
2) Global sweep (if needed): other product files and docs that mention the product name.
3) Within found channels/meetings: follow doc links (e.g., `/archives/docs/<doc_id>`), referenced meeting chats, PR mentions.

Collect all candidates matching:
- type/document_type/title contains “Market Research Report” (case-insensitive)
- OR doc links/slack text contains “Market Research Report”
- OR meeting transcripts tagged document_type “Market Research Report”

---

### Step 2 — HARD Product Grounding (Anti-distractor gate)
A candidate report is **VALID** only if it passes **at least 2 independent grounding signals**:

**Grounding signals (choose any 2+):**
A) Located under the correct product artifact container (e.g., inside `products/CoachForce.json` *and* associated with that product’s planning channels/meetings).
B) Document content/title explicitly mentions the target product name (“CoachForce”) or a canonical alias list you derive from artifacts.
C) Shared in a channel whose name is clearly for the target product (e.g., `planning-CoachForce`, `#coachforce-*`) OR a product-specific meeting series (e.g., `CoachForce_planning_*`).
D) The document id/link path contains a product-specific identifier consistent with the target product (not another product).
E) A meeting transcript discussing the report includes the target product context in the meeting title/series/channel reference.

**Reject rule (very important):**
- If the report content repeatedly names a different product (e.g., “CoFoAIX”) and lacks CoachForce grounding → mark as DISTRACTOR and discard, even if it is found in the same file or near similar wording.

**Why:** Benchmarks intentionally insert same doc type across products; “first hit wins” is a common failure.

---

### Step 3 — Select the correct report version
If multiple VALID reports exist, choose the “final/latest” by this precedence:

1) Explicit “latest” marker (id/title/link contains `latest`, or most recent date field)
2) Explicit “final” marker
3) Otherwise, pick the most recent by `date` field
4) If dates missing, choose the one most frequently referenced in follow-up discussions (slack replies/meeting chats)

Keep the selected report’s doc_id and link as the anchor.

---

### Step 4 — Extract author(s)
Extract authors in this priority order:
1) Document fields: `author`, `authors`, `created_by`, `owner`
2) PR fields if the report is introduced via PR: `author`, `created_by`
3) Slack: the user who posted “Here is the report…” message (only if it clearly links to the report doc_id and is product-grounded)

Normalize into **employee IDs**:
- If already an `eid_*`, keep it.
- If only a name appears, resolve via employee directory metadata (name → employee_id) but only after you have product-grounded evidence.

---

### Step 5 — Extract key reviewers (DO NOT equate “participants” with reviewers)
Key reviewers must be **evidence-based contributors**, not simply attendees.

Use this priority order:

**Tier 1 (best): explicit reviewer fields**
- Document fields: `reviewers`, `key_reviewers`, `approvers`, `requested_reviewers`
- PR fields: `reviewers`, `approvers`, `requested_reviewers`

**Tier 2: attributable substantive feedback in Slack replies and meeting turns**
- Slack thread replies to the report-share message where the user proposes a concrete addition, clarification, comparison, restructuring, or section-level change tied to the report
- Meeting transcripts where turns are attributable to people AND those people provide concrete suggestions/edits
- Include substantive contributors even when their suggestion is not adopted later or omitted from the author's summary
- Exclude:
  - the author (unless question explicitly wants them included as reviewer too)
  - pure acknowledgements (“looks good”, “thanks”)
  - comments that only agree with or restate an earlier suggestion without adding a new actionable review point

**Tier 3: document feedback/change summaries as corroboration**
- Document `feedback` sections and author-written change summaries may confirm mappings between reviewers and accepted edits
- Do not treat these summaries as exhaustive reviewer membership lists
- Never remove a reviewer solely because their substantive suggestion is absent from the final summary

**Critical rule:**
- Meeting `participants` list alone is NOT sufficient.
  - Only count someone as a key reviewer if the transcript shows they contributed feedback
  - OR they appear in explicit reviewer fields.
- If attributable substantive feedback evidence conflicts with an author-written summary, keep the substantive contributor in the reviewer set and note that the suggestion was not adopted.

If the benchmark expects “key reviewers” to be “the people who reviewed in the review meeting”, then your evidence must cite the transcript lines/turns that contain their suggestions.

---

### Step 6 — Validate IDs & de-duplicate
- All outputs must be valid employee IDs (pattern `eid_...`) and exist in the employee directory if provided.
- Before finalizing the reviewer set, do a recall check: every person who proposed a concrete actionable change in the report-review Slack thread or transcript should be included unless their comment is only acknowledgement or restatement.
- Remove duplicates while preserving order:
  1) authors first
  2) key reviewers next

---

## Output Format (Strict, JSON-ready)

Return:

### 1) Final Answer Object
```json
{
  "target_product": "<ProductName>",
  "report_doc_id": "<doc_id>",
  "author_employee_ids": ["eid_..."],
  "key_reviewer_employee_ids": ["eid_..."],
  "all_employee_ids_union": ["eid_..."]
}
```

### 2) Evidence Map (pointers + minimal snippets)
For each extracted ID, include:
- artifact type + artifact id (doc_id / meeting_id / slack_message_id / pr_id)
- a short snippet that directly supports the mapping

Example evidence record:
```json
{
  "employee_id": "eid_xxx",
  "role": "key_reviewer",
  "evidence": [
    {
      "artifact_type": "meeting_transcript",
      "artifact_id": "CoachForce_planning_2",
      "snippet": "…Alex: We should add a section comparing CoachForce to competitor X…"
    }
  ]
}
```

---

## Recommendation Types

Return one of:
- **USE_EVIDENCE** — evidence sufficient and product-grounded
- **NEED_MORE_SEARCH** — missing reviewer signals; must expand search (PRs, slack replies, other meetings)
- **AMBIGUOUS** — conflicting product signals or multiple equally valid reports

---

## Common Failure Modes (This skill prevents them)

1) **Cross-product leakage**  
Picking “Market Research Report” for another product (e.g., CoFoAIX) because it appears first.  
→ Fixed by Step 2 (2-signal product grounding).

2) **Over-inclusive reviewers**  
Treating all meeting participants as reviewers.  
→ Fixed by Step 5 (evidence-based reviewer definition).

3) **Wrong version**  
Choosing draft over final/latest.  
→ Fixed by Step 3.

4) **Schema mismatch**  
Returning a flat list when evaluator expects split fields.  
→ Fixed by Output Format.

---

## Mini Example (Your case)

Question:  
“Find employee IDs of the authors and key reviewers of the Market Research Report for the CoachForce product?”

Correct behavior:
- Reject any report whose content/links are clearly about CoFoAIX unless it also passes 2+ CoachForce grounding signals.
- Select CoachForce’s final/latest report.
- Author from doc field `author`.
- Key reviewers from explicit `reviewers/key_reviewers` if present; else from transcript turns or slack replies showing concrete feedback.

---

## Do NOT Invoke When

- The answer is in a single small known file and location with no cross-references.
- The task is a trivial one-hop lookup and product scope is unambiguous.
