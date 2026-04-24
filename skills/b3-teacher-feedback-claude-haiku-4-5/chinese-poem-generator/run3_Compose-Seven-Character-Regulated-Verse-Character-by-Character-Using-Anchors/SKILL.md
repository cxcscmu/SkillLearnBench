---
name: Compose Seven-Character Regulated Verse Character-by-Character Using Anchors
description: Fill in your poem position-by-position, starting with the 4 rhyme characters (lines 2, 4, 6, 8). For each remaining position, select a character, verify its pinyin and tone in your reference table, confirm it matches the required 平/仄 classification, then move to the next position. Never move to a new line until all 7 positions of the current line pass verification.
---

## Process

1. **Anchor Phase — Place all 4 rhyme characters first:**
   - Position: Line 2, character 7
   - Position: Line 4, character 7
   - Position: Line 6, character 7
   - Position: Line 8, character 7
   - All must share the same final and tone classification
   - Verify each against your reference table

2. **Fill remaining positions in order (left to right, top to bottom):**
   - Current position: Line 1, character 1
   - Candidate character: ?
   - Check reference table → Pinyin → Tone → 平/仄?
   - Does it match the pattern requirement at position [Line, Char]?
   - If YES → place it, move to next position
   - If NO → reject and try another character

3. **For each character placed:**
   - Write: `[Position] | Candidate | Pinyin | Tone | Pattern Match? [✓/✗]`
   - Verbally confirm: "Position L1C1: 古 (gǔ, 3rd tone, 仄) ✓ matches 仄"

4. **Complete one full line before moving to the next** — do not skip ahead.

5. **After all 8 lines are filled, run a final line-by-line verification:**
   - Line 1: 古 仄 今 平 悲 仄 声 仄 → Expected 仄平仄仄平平仄 → [✓ PASS / ✗ FAIL]
   - (repeat for lines 2–8)

6. **Only after final verification passes:** Write the poem to `\root\poem.txt` with title on line 1 and poem lines 2–9.