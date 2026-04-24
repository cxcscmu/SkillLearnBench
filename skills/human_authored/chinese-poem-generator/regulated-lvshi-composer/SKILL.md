---
name: regulated-lvshi-composer
description: Compose Chinese five-character and seven-character regulated verse under a strict modern Mandarin rule set. Use this Skill when the user asks for five-character or seven-character regulated verse, wants a poem written in a disciplined regulated-verse form, or wants an existing regulated poem revised to fit strict line-count, character-count, 平仄, rhyme, title quality, thematic coherence, and poetic depth requirements. This Skill uses modern Mandarin tones for 平仄, Mandarin finals for rhyme, allows polyphonic characters if any non-neutral reading fits, ignores neutral tone unless no non-neutral reading exists, and emphasizes a fitting title, unified theme, meaningful progression, balanced middle couplets, and a resonant conclusion.
---

# Regulated Lvshi Composer

## Instructions

Use this Skill only for strict five-character regulated verse and seven-character regulated verse under a modern Mandarin rule set. Do not use it for old-style verse, quatrains, lyric ci, prose poetry, or historically exact phonology unless the user explicitly asks for those.

### 1. Determine the poetic task
First identify:
- whether the user wants five-character regulated verse or seven-character regulated verse
- the theme, setting, mood, and emotional register
- whether the poem should be plain, elegant, elevated, solemn, fresh, melancholic, meditative, or expansive
- whether the user wants only the poem or also wants brief notes
- whether the user wants a new poem or a revision of an existing one
- whether the user explicitly asks for parallelism in the middle couplets

If the user does not specify five-character or seven-character regulated verse, choose the form that best fits the theme.
In general:
- five-character regulated verse suits restraint, purity, compression, and quiet feeling
- seven-character regulated verse suits broader scene-building, richer texture, and more elaborate development

### 2. Use the modern Mandarin rule set
Apply the following conventions consistently:
- 1st and 2nd tones = 平
- 3rd and 4th tones = 仄
- neutral tone does not count
- if a character has at least one non-neutral reading, use only its non-neutral readings
- if a character has only neutral readings or no usable reading, avoid the character if possible
- a polyphonic character is acceptable if any non-neutral reading satisfies the required 平仄 or rhyme condition
- rhyme is judged by modern Mandarin finals, not historical rhyme books

Do not switch to historical rhyme-book practice or medieval phonology unless the user explicitly asks for that.

### 3. Enforce the structural rules
For five-character regulated verse:
- exactly 8 lines
- exactly 5 Chinese characters per line

For seven-character regulated verse:
- exactly 8 lines
- exactly 7 Chinese characters per line

Output format:
- line 1: title
- line 2: blank line
- lines 3-10: the 8 body lines of the poem

Punctuation is optional. If punctuation is used, it must not alter the character count of the body lines.

### 4. Choose one exact canonical form
The poem must follow one and only one of the basic forms below.

#### Five-character regulated verse forms

Ping-start Ze-end no-rhyme-on-line-1
- 平平平仄仄
- 仄仄仄平平
- 仄仄平平仄
- 平平仄仄平
- 平平平仄仄
- 仄仄仄平平
- 仄仄平平仄
- 平平仄仄平

Ze-start Ze-end no-rhyme-on-line-1
- 仄仄平平仄
- 平平仄仄平
- 平平平仄仄
- 仄仄仄平平
- 仄仄平平仄
- 平平仄仄平
- 平平平仄仄
- 仄仄仄平平

Ze-start Ping-end rhyme-on-line-1
- 仄仄仄平平
- 平平仄仄平
- 平平平仄仄
- 仄仄仄平平
- 仄仄平平仄
- 平平仄仄平
- 平平平仄仄
- 仄仄仄平平

Ping-start Ping-end rhyme-on-line-1
- 平平仄仄平
- 仄仄仄平平
- 仄仄平平仄
- 平平仄仄平
- 平平平仄仄
- 仄仄仄平平
- 仄仄平平仄
- 平平仄仄平

#### Seven-character regulated verse forms

Ping-start Ze-end no-rhyme-on-line-1
- 平平仄仄平平仄
- 仄仄平平仄仄平
- 仄仄平平平仄仄
- 平平仄仄仄平平
- 平平仄仄平平仄
- 仄仄平平仄仄平
- 仄仄平平平仄仄
- 平平仄仄仄平平

Ze-start Ze-end no-rhyme-on-line-1
- 仄仄平平平仄仄
- 平平仄仄仄平平
- 平平仄仄平平仄
- 仄仄平平仄仄平
- 仄仄平平平仄仄
- 平平仄仄仄平平
- 平平仄仄平平仄
- 仄仄平平仄仄平

Ze-start Ping-end rhyme-on-line-1
- 仄仄平平仄仄平
- 平平仄仄仄平平
- 平平仄仄平平仄
- 仄仄平平仄仄平
- 仄仄平平平仄仄
- 平平仄仄仄平平
- 平平仄仄平平仄
- 仄仄平平仄仄平

Ping-start Ping-end rhyme-on-line-1
- 平平仄仄仄平平
- 仄仄平平仄仄平
- 仄仄平平平仄仄
- 平平仄仄仄平平
- 平平仄仄平平仄
- 仄仄平平仄仄平
- 仄仄平平平仄仄
- 平平仄仄仄平平

### 5. Apply the rhyme rule
For forms marked no-rhyme-on-line-1, the rhyme lines are 2, 4, 6, 8.

For forms marked rhyme-on-line-1, the rhyme lines are 1, 2, 4, 6, 8.

All required rhyme lines must share a common modern Mandarin final across their line-ending characters.

When choosing rhyme characters:
- prefer common, stable, unambiguous characters
- avoid risky polyphonic line endings
- avoid line-ending characters that are weak, colloquial, or tonally unstable
- prefer rhyme characters that also contribute to atmosphere and meaning rather than serving as empty placeholders

### 6. Give the poem a fitting title
The title is part of the poem’s design, not an afterthought.

A good title should:
- name the occasion, place, season, action, or emotional focus clearly
- prepare the reader for the poem’s world without explaining the whole poem away
- match the scale and tone of the poem
- be concise, natural, and memorable

Good title strategies include:
- place or setting: Night Mooring by the Autumn River, Dawn at the Mountain Temple
- occasion or action: Written on a Spring Night in Light Rain, Sent to a Friend Before Departure
- object or image focus: On Plum Blossoms, Hearing the Evening Bell
- reflective framing: Thoughts on Returning Late, Written While Waiting

Avoid titles that are vague, generic, overblown, or unrelated to the poem. The title should not promise a grand subject that the poem does not actually develop.

### 7. Build a unified theme with real content
Do not begin by merely filling a metrical frame. First decide what the poem is truly about.

The poem should grow from one central seed: one scene, one occasion, one emotional problem, one meditation, or one relationship between outer world and inner life. All eight lines should belong to the same poetic world. Images should support one another, diction should remain tonally coherent, and the closing couplet should arise naturally from the earlier lines.

Each couplet should add something necessary: a scene, a turn in feeling, a clarification, a memory, a tension, or a preparation for the ending. Prefer density over emptiness, precise imagery over stock phrases, and felt insight over abstract slogans. Remove lines that only decorate the poem without deepening it.

### 8. Shape progression and depth
A regulated poem should move, even when quiet. A strong default progression is:
- lines 1-2 establish the scene, season, occasion, or vantage
- lines 3-4 deepen or widen the scene and begin emotional coloring
- lines 5-6 turn inward, complicate the scene, or introduce memory, contrast, distance, or reflection
- lines 7-8 gather the poem into a conclusion with resonance

Depth does not require grand statements. It may come from implication, restraint, contrast between scene and feeling, temporal awareness, parting, aging, waiting, exile, impermanence, or an image that carries more than it says. The best ending often does not explain the poem; it deepens it and gives the whole poem a longer aftertaste.

### 9. Handle the middle couplets, imagery, and diction with discipline
The middle couplets are where the poem earns its stature. Lines 3-4 and 5-6 should be balanced, meaningful, and free of filler. If the user explicitly asks for parallelism, these two couplets should aim for clear parallel structure in syntax, imagery, and rhetorical weight.

Choose images with restraint. Prefer images that are specific, sensorial, mutually supportive, and appropriate to season, place, and voice. Do not overload the poem with unrelated objects. Choose a few strong things and let them work together.

Match diction to subject and speaker. Quiet themes should not sound bombastic; solemn themes may bear more weight; farewell poems should avoid empty grandeur; landscape poems should still carry inward life. Aim for natural compression, dignified fluency, classical atmosphere without stiffness, and beauty without ornament for ornament’s sake.

### 10. Draft and revise in the right order
Use this workflow:
1. choose the form: five-character or seven-character regulated verse
2. choose one of the four canonical forms
3. choose the rhyme plan
4. decide the title, central theme, perspective, and emotional arc
5. sketch the role of each couplet
6. choose a restrained but meaningful image set
7. build the line endings first, especially the rhyme lines
8. draft each body line to fit the exact character count
9. check every position against the target 平仄 pattern
10. improve thematic unity, emotional depth, and middle-couplet quality
11. strengthen the final couplet so it gathers the poem rather than merely ends it
12. revise the title so it fits the finished poem exactly

If revising an existing poem, preserve the theme and major images if possible, then repair structure, 平仄, rhyme, unity, depth, and parallelism in that order.

### 11. Output style and final check
By default, output only the title and the 8 body lines of the poem.

If the user asks for explanation, you may also provide the chosen form name, a brief note on the theme, whether middle-couplet parallelism was intentionally used, and a concise explanation of the poem’s inner progression.

Before returning the poem, verify all of the following:
- it has a fitting title
- it has exactly 8 body lines
- every body line has exactly 5 or 7 Chinese characters as required
- it follows one of the canonical forms under the modern Mandarin rule set
- all required rhyme lines share a valid modern Mandarin final
- the poem keeps one coherent theme throughout
- every couplet contributes something necessary
- the middle couplets are balanced, and if requested, clearly parallel
- the final couplet belongs organically to the poem and leaves resonance
- diction is coherent, natural, and proportionate to the subject
- the poem has not only form, but also inward life

## Examples

### Example 1
User request:
Write a seven-character regulated verse on a spring night with light rain. Output only the poem and do not explain it.

What to do:
- use this Skill
- choose one strict seven-character regulated verse form
- provide a fitting title on the first line
- keep the whole poem within one spring-night-rain atmosphere
- let the middle couplets deepen the scene rather than merely repeat it
- make the ending gather the emotional mood of the whole poem
- return only the title, a blank line, and the poem

### Example 2
User request:
Please write a five-character regulated verse on a mountain temple at dawn. The language should be light and refined.

What to do:
- use this Skill
- compose a strict five-character regulated verse
- choose a concise title suited to a mountain-temple dawn setting
- keep diction restrained, clean, and quiet
- build a unified mountain-temple-morning world
- let the poem carry inward stillness rather than only external scenery
- return the title and poem unless the user asks for notes
