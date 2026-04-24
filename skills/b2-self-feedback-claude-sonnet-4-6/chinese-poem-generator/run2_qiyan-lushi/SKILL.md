---
name: run2_qiyan-lushi
description: Complete rules, structure, and verification checklist for seven-character regulated verse (七言律诗), with corrected rhyme groups and parallel couplet standards.
---

# 七言律诗 (Seven-Character Regulated Verse) — Complete Guide

## Basic Structure
- **8 lines** total, each with exactly **7 Chinese characters**
- 4 named couplets:
  - 首联 (Lines 1-2): Opening couplet — sets scene, no parallel required
  - 颔联 (Lines 3-4): Second couplet — **must be parallel (对仗)**
  - 颈联 (Lines 5-6): Third couplet — **must be parallel (对仗)**
  - 尾联 (Lines 7-8): Closing couplet — expresses emotion/wish, no parallel required

## Rhyme Scheme
- Lines **1, 2, 4, 6, 8** end with rhyming characters (押平韵)
- Lines **3, 5, 7** do NOT rhyme (仄声 ending preferred)
- Each rhyme character must be **different** — no repetition allowed
- All rhyme characters belong to the same modern Mandarin rhyme group

## Modern Mandarin Rhyme Groups (正确分组)
Rhyme = same **韵母** (final vowel in Pinyin, ignoring initial consonant):

| Group | Pinyin ending | Example characters |
|-------|--------------|-------------------|
| an    | -an, -ian, -uan | 山shān, 寒hán, 难nán, 残cán, 安ān, 天tiān, 年nián, 烟yān, 关guān |
| ing   | -ing, -iong  | 明míng, 清qīng, 情qíng, 平píng, 声shēng ❌ (shēng ends in -eng, NOT -ing!) |
| eng   | -eng, -ong   | 声shēng, 城chéng, 风fēng, 中zhōng |
| i     | -i, -ü       | 时shí, 期qī, 知zhī, 迟chí |
| u     | -u           | 湖hú, 孤gū, 途tú |

**CORRECTION from run1**: 声(shēng) belongs to -eng group, NOT -ing group.

## Parallel Couplet (对仗) Requirements
Lines 3-4 and 5-6 each form a parallel pair:

### Grammar Matching
- Each character/word position should match grammatically:
  - Noun ↔ Noun, Verb ↔ Verb, Adjective ↔ Adjective
  - 2-char compounds pair with 2-char compounds

### Quality Levels
- **Excellent**: Contrasting meaning + matching grammar + vivid imagery
  - 老翁挥泪送儿去 / 稚女含悲问父难
    - 老翁(n) ↔ 稚女(n), 挥泪(vp) ↔ 含悲(vp), 送儿(vo) ↔ 问父(vo), 去(v) ↔ 难(adj)
- **Good**: Matching grammar, somewhat related meaning
- **Poor**: Only matching syllable count, different grammar

### Couplet Pair Tips
- Line 3 subject ↔ Line 4 subject should contrast (old/young, male/female, person/object)
- Actions should be parallel in intensity and type
- Both lines should advance the same theme

## Tonal Pattern (平仄) — Simplified
For modern composition, focus on rhyme. Optional but traditional:
- Rhyming lines (1,2,4,6,8) typically end with **平声** (tones 1 or 2)
- Non-rhyming lines (3,5,7) typically end with **仄声** (tones 3 or 4)

## Verification Checklist
Before finalizing:
- [ ] Exactly 7 characters per line (count each character)
- [ ] Exactly 8 lines
- [ ] Lines 1, 2, 4, 6, 8 all rhyme with the same vowel group
- [ ] No rhyme character repeated
- [ ] Lines 3, 5, 7 do NOT rhyme with the rhyme group
- [ ] Lines 3-4 form a parallel couplet (对仗)
- [ ] Lines 5-6 form a parallel couplet (对仗)
- [ ] Poem flows logically (scene → suffering → destruction → wish)
- [ ] Non-rhyming line endings are preferably 仄声

## Output Format
```
[Title]
[Line 1 - 7 chars, rhymes]
[Line 2 - 7 chars, rhymes]
[Line 3 - 7 chars, no rhyme]
[Line 4 - 7 chars, rhymes]
[Line 5 - 7 chars, no rhyme]
[Line 6 - 7 chars, rhymes]
[Line 7 - 7 chars, no rhyme]
[Line 8 - 7 chars, rhymes]
```
