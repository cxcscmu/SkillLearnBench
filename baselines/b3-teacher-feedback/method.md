# b3: Teacher-Student

This method is handled entirely by the runner — no static prompt injection.

The runner orchestrates a multi-round loop:
1. Student (LLM, direct API) generates a skill document for the task.
2. Agent inside container reads `/logs/student_skill.md` and executes the task.
3. Verifier scores the result.
4. On failure, Teacher (LLM with ground-truth access) gives modification hints.
5. Repeat up to `--max-rounds` times (default: 3).

> **Critical path rule:** All skills must be written to `environment/skills/<skill-name>/SKILL.md` relative to your shell's current working directory (run `pwd` if unsure). Never write skills to any other location — not to a project subdirectory, not to an agent config folder, not to any absolute path that differs from `$(pwd)/environment/skills/`.
