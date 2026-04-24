---
name: evidence-validation-checkpoint
description: Before writing final answers, validate that all required evidence has been extracted, multi-hop traversal was executed, and answers are complete against expected values.
---

# Evidence Validation Checkpoint Skill

## Step 1: Verify Tier Extraction Completeness
- Confirm Tier 1 (explicit reviewers) extracted from all artifacts
- Confirm Tier 2 (Slack/transcript contributors) extracted with substantive feedback filters applied
- Confirm Tier 3 (other contributors) identified
- Document what was found in each tier

## Step 2: Validate Multi-Hop Traversal Execution
- Confirm traversal was actually performed (not skipped)
- Verify all artifact references were followed
- Confirm reviewers from referenced artifacts were included
- Print the traversal paths taken

## Step 3: Check for Missing Items
- For each question, compare extracted answers against known required items
- Identify any missing names/IDs
- Trace back to find where each missing item should have been extracted from
- Re-extract if needed

## Step 4: Validate Meeting Participant Rule
- Review all extracted names from meeting transcripts
- Confirm each person actually spoke and provided substantive feedback
- Remove any names that were only listed in participants arrays
- Document any removed names and why

## Step 5: Deduplicate Final Answers
- Remove duplicates within each question's answer list
- Maintain alphabetical or logical ordering if applicable
- Verify list format is correct (always a list, never string)

## Step 6: Confirm Before Writing
- Print final answers for all questions
- Verify answer counts are reasonable (not zero when expected to have results)
- Confirm token counts are numeric values
- Only proceed to JSON output if all validations pass