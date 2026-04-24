## Important: Solve in {max_rounds} Rounds

Complete this task in exactly **{max_rounds} rounds** as described below.

### Round 1: Initial Solve

1. **Analyze the task requirements** and identify what domain knowledge, APIs, or techniques are needed.

2. **Write 1-5 modular skill documents** that would help solve this task. Each skill should:
   - Focus on a specific tool, library, API, or technique
   - Include installation/setup instructions if applicable
   - Provide code examples and usage patterns
   - Be reusable for similar tasks

3. **Save each skill** as `SKILL.md` inside a named subdirectory under `environment/skills/`, using the prefix `run1_` for the folder name (e.g., `environment/skills/run1_python-docx/SKILL.md`). Each `SKILL.md` **must** begin with a YAML frontmatter block:
   ```
   ---
   name: <folder-name>
   description: <one sentence: what this skill covers and when to use it>
   ---
   ```
   After saving, you can read the skill back at that same path as reference.

4. **Solve the task** using the skills you created as reference.

### Round 2+: Reflect and Improve

For **each round R from 2 to {max_rounds}**, after completing the previous round:

1. **Re-read the task instruction** from the beginning.

2. **Review your previous round's skill files** (`run(R-1)_*`). For example:
   - In Round 2: review `run1_*` files, then write `run2_*` files.
   - In Round 3: review `run2_*` files, then write `run3_*` files.

   Identify gaps, inaccuracies, or anything that could be more precise or reusable.

3. **Write skill documents for this round** as `SKILL.md` inside new subdirectories with the prefix `runR_` (e.g., Round 2 → `run2_python-docx/SKILL.md`, Round 3 → `run3_python-docx/SKILL.md`). Each must include the same YAML frontmatter format as Round 1.

   **Important:** Even if a skill document is unchanged from the previous round, you must copy it under the new `runR_` prefix. Do NOT modify or delete any previous `run*_*` directories.

4. **Re-solve the task** using your updated `runR_*` skills. Overwrite your previous output with the improved answer.

The verifier checks only your final output after Round {max_rounds} is complete.

> **Completion check:** After all rounds you must have exactly **{max_rounds}** sets of skill directories — `run1_*` through `run{max_rounds}_*` — with no gaps.

> **Critical path rule:** All skills must be written to `environment/skills/<skill-name>/SKILL.md` relative to your shell's current working directory (run `pwd` if unsure). Never write skills to any other location — not to a project subdirectory, not to an agent config folder, not to any absolute path that differs from `$(pwd)/environment/skills/`.
