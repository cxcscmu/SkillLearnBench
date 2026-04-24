## Important: Generate Skills First

Before attempting to solve this task, please follow these steps:

1. **Analyze the task requirements** and identify what domain knowledge, APIs, or techniques are needed.

2. **Write 1-5 modular skill documents** that would help solve these task(s). Each skill should:
   - Focus on a specific tool, library, API, or technique
   - Include installation/setup instructions if applicable
   - Provide code examples and usage patterns
   - Be reusable for similar tasks

3. **Save each skill** as `SKILL.md` inside a named subdirectory under `environment/skills/`. Use a descriptive folder name (e.g., `environment/skills/python-docx/SKILL.md`). Each `SKILL.md` **must** begin with a YAML frontmatter block:
   ```
   ---
   name: <folder-name>
   description: <one sentence: what this skill covers and when to use it>
   ---
   ```
   After saving, you can read the skill back at that same path as reference.

4. **Then solve the task** using the skills you created as reference.

This approach tests your ability to identify and document relevant knowledge before applying it.

> **Critical path rule:** All skills must be written to `environment/skills/<skill-name>/SKILL.md` relative to your shell's current working directory (run `pwd` if unsure). Never write skills to any other location — not to a project subdirectory, not to an agent config folder, not to any absolute path that differs from `$(pwd)/environment/skills/`.
