---
name: skill-creator
description: Create modular skill documents (SKILL.md files) for Claude Code. Use this skill whenever a task requires generating reusable knowledge documents, capturing domain expertise, or building skills that encode workflows, APIs, or specialized techniques. Invoke this whenever you need to write a SKILL.md from scratch, even if the user doesn't explicitly ask for a "skill".
---

# Skill Creator

A guide for creating well-structured, reusable Claude Code skills.

## Communicating with the user

Pay attention to context cues to gauge familiarity. Keep explanations accessible — don't assume deep technical knowledge unless the user demonstrates it.

---

## Creating a skill

### Capture Intent

Understand what the skill should enable. Extract from the current task context:

1. What should this skill enable Claude to do?
2. When should this skill trigger? (what user phrases / contexts)
3. What's the expected output format or artifact?

### Interview and Research

Proactively think about edge cases, input/output formats, success criteria, and dependencies before writing. If useful libraries or APIs are involved, check what's available in the environment first.

### Write the SKILL.md

Based on the task requirements, fill in these components:

- **name**: Skill identifier (must match the folder name)
- **description**: When to trigger, what it does. This is the primary triggering mechanism — include both what the skill does AND specific contexts for when to use it. To combat undertriggering, make the description a little "pushy": instead of "How to do X", write "How to do X. Use this skill whenever the user mentions X, Y, or Z, even if they don't explicitly ask for it."
- **the rest of the skill body**

### Skill Writing Guide

#### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

#### Progressive Disclosure

Skills use a three-level loading system:

1. **Metadata** (name + description) — Always in context (~100 words)
2. **SKILL.md body** — In context whenever skill triggers (<500 lines ideal)
3. **Bundled resources** — Loaded on demand (unlimited size)

**Key patterns:**
- Keep SKILL.md under 500 lines; if approaching the limit, split into a SKILL.md overview + references/ files with clear pointers
- Reference bundled files clearly from SKILL.md with guidance on when to read them
- For large reference files (>300 lines), include a table of contents

**Domain organization** — when a skill supports multiple variants, organize by variant:
```
cloud-deploy/
├── SKILL.md (workflow + selection logic)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

#### Writing Patterns

Use the imperative form. Explain the **why** behind instructions — models understand reasoning, not just rules. Avoid heavy-handed ALL-CAPS MUSTs; explain why something matters instead.

**Defining output formats:**
```markdown
## Report structure
Use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

**Examples pattern:**
```markdown
## Commit message format
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

#### Principle of Lack of Surprise

Skills must not contain malware, exploit code, or content that could compromise system security. A skill's contents should not surprise the user given its description.

### Writing Style

Write a draft, then review with fresh eyes. Generalize from specific examples — don't overfit to one case. Keep skills lean: remove instructions that aren't pulling their weight. Read as if you're the model using this skill for the first time.

### Validation

After writing a skill, run the quick validator to check structure:

```bash
python environment/skills/<skill-name>/scripts/quick_validate.py environment/skills/<skill-name>/
```

---

## Output path for this task

Save each skill as `SKILL.md` inside a named subdirectory under `environment/skills/` (relative path from your working directory). Do **not** write to `/root/.claude/skills/` or any other location.

```
environment/skills/<skill-name>/SKILL.md
```

Each `SKILL.md` must begin with the YAML frontmatter block (name + description).

After creating the skills, solve the task using them as reference.
