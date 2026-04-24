---
name: seven-character-regulated-verse-structure-and-rhyme
description: Use this skill when composing a seven-character regulated verse (七言律诗) to ensure correct structural requirements including rhyme scheme, parallelism (对仗), thematic progression, and formatting rules.
---

# Seven-Character Regulated Verse Structure and Rhyme (七言律诗结构与韵律)

## Basic Structure

A 七言律诗 consists of exactly **8 lines**, each with exactly **7 characters**. The 8 lines form 4 couplets:

1. **首联 (Opening Couplet):** Lines 1-2 — Introduce the theme/setting
2. **颔联 (Chin Couplet):** Lines 3-4 — Develop the theme (MUST use antithetical parallelism 对仗)
3. **颈联 (Neck Couplet):** Lines 5-6 — Deepen or turn the theme (MUST use antithetical parallelism 对仗)
4. **尾联 (Closing Couplet):** Lines 7-8 — Conclude, express emotion or resolution

## Rhyme Scheme (Based on Modern Mandarin Pronunciation)

- Rhyming lines: Lines 2, 4, 6, 8 MUST rhyme with each other.
- Line 1 MAY rhyme (if using 首句入韵 form) or MAY NOT (if using 首句不入韵 form).
- All rhyming characters must share the same **modern Mandarin final (韵母)** — e.g., all end in -ang, or all end in -an.
- All rhyming characters MUST be **平声** (1st or 2nd tone in modern Mandarin).
- Use ONLY ONE rhyme group throughout the entire poem — no switching.

### Choosing a Good Rhyme Group
Pick a rhyme group with many available characters to give yourself flexibility:
- -ang (光, 乡, 长, 伤, 荒, 霜, 疆, 方, 堂, 装, 芳...)
- -an (安, 难, 山, 还, 关, 欢, 残, 寒, 宽, 年...)
- -ing (平, 情, 声, 明, 兵, 生, 城, 宁, 营, 征...)
- -en (人, 尘, 春, 魂, 村, 存, 门, 真, 闻, 恩...)

## Antithetical Parallelism (对仗) Requirements

Lines 3-4 (颔联) and Lines 5-6 (颈联) MUST exhibit 对仗:
- Corresponding characters in the two lines should be from the same grammatical/semantic category
- Examples of matching categories: number↔number, color↔color, noun↔noun, verb↔verb, direction↔direction, nature word↔nature word
- The tonal pattern of the two lines in a couplet should be opposite (this is already ensured if following the canonical tonal template)

## Thematic Progression for "Peace" Theme

For a poem about war suffering and longing for peace:
1. **首联 (Lines 1-2):** Set the scene — describe the devastation of war (burning villages, displaced people, broken lands)
2. **颔联 (Lines 3-4):** Concrete imagery of suffering — parallel images of destruction (e.g., bones in fields / smoke over cities; widows weeping / orphans wandering)
3. **颈联 (Lines 5-6):** Personal emotion / deeper reflection — parallel expressions of longing (e.g., dreaming of harvest / hoping for reunion; plowshares vs. swords)
4. **尾联 (Lines 7-8):** Express the wish for peace — when will war end, longing for a peaceful world

## Output Format

The file `\root\poem.txt` must contain:
```
[Title in Chinese]
[Line 1 — 7 characters]
[Line 2 — 7 characters]
[Line 3 — 7 characters]
[Line 4 — 7 characters]
[Line 5 — 7 characters]
[Line 6 — 7 characters]
[Line 7 — 7 characters]
[Line 8 — 7 characters]
```

- Title on the first line (no punctuation needed, or with 《》 brackets)
- Exactly 8 subsequent lines, each with exactly 7 Chinese characters
- No punctuation within the poem lines (or traditional Chinese punctuation only — comma after character 4 and period at end are acceptable but not required)
- No blank lines between poem lines