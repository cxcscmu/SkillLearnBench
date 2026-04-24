## Important: Use skill-creator to Generate Skills First

A `skill-creator` skill has been pre-loaded into your skills directory. Before solving this task, use it to create modular skill documents.

### Steps

1. **Invoke the `skill-creator` skill** to guide you through creating skills for this task. The skill is already available — use the `Skill` tool or follow its instructions directly.

2. **Create 1-5 modular skills** that capture the domain knowledge, libraries, or techniques needed. Follow the skill-creator's format exactly:
   - Each skill **must** be saved at `environment/skills/<skill-name>/SKILL.md` (relative path) — do **not** write to `/root/.claude/skills/` or any other location
   - Each `SKILL.md` must begin with YAML frontmatter (`name` + `description`)
   - Description must be specific enough to trigger correctly — see skill-creator for guidance

3. **Solve the task** using the skills you created as reference.

> **Critical path rule:** All skills must be written to `environment/skills/<skill-name>/SKILL.md` relative to your shell's current working directory (run `pwd` if unsure). Never write skills to any other location — not to a project subdirectory, not to an agent config folder, not to any absolute path that differs from `$(pwd)/environment/skills/`.