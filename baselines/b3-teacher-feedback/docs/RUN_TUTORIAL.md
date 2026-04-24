# Run Tutorial

## Overview

Each run uses a **Teacher-Student** loop:

1. **Per round**: The Student generates a `skill.md` for the task, which is saved under the trial directory. The Student then runs the task **inside the sandbox** using that skill (at `/logs/student_skill.md`). The verifier is executed afterward.
2. **If the verifier passes**: The run finishes. `result.json` contains `passed: true` and `rounds_used` (1–5).
3. **If the verifier fails**: The run is reported to the Teacher. The Teacher returns **modification suggestions only** (no full solution). The Student generates a new `skill.md` from that feedback and the loop continues.
4. **Max rounds**: 5 by default. If still failing after 5 rounds, `result.json` has `passed: false` and `rounds_used: 5`.

## Prerequisites

- **Docker** installed and running.
- **Python 3** (e.g. 3.9+).
- **API key**: Set `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` (e.g. in a `.env` file in the project root).

## Commands

```bash
# List available tasks
python run.py list

# List available agents (e.g. codex, claude-code)
python run.py agents

# Run a task (Teacher-Student; default 5 rounds)
python run.py run offer-letter-generator

# Optional: choose agent and max rounds
python run.py run offer-letter-generator -a codex --max-rounds 5
```

## Outputs

- **`trials/<task_id>__<trial_id>/result.json`**: `passed` (bool), `rounds_used` (int), `trial_path`, etc.
- **`trials/<trial>/teacher_student_history.json`**: Per-round feedback and Teacher–Student interaction.
- **`trials/<trial>/student_skill.md`**: The Student-generated skill (updated each round).
- Task artifacts (e.g. filled docx) are copied into the same trial directory when configured.

## Troubleshooting

- **Task not found**: Ensure `tasks/<task_id>/` exists with `instruction.md`, `environment/Dockerfile` or `Dockerfile.student`, and `tests/`.
- **No skills in environment/skills**: Teacher-Student mode requires at least one `SKILL.md` under `tasks/<task_id>/environment/skills/`.
- **Missing API key**: Set `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` in the environment or in `.env`.
