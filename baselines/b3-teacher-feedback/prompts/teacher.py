"""Prompts for Teacher: gives modification suggestions (no direct solution) when Student's run fails."""

TEACHER_SYSTEM_SUGGESTIONS = """You are a Teacher. The Student is trying to complete a task by writing their own skill and executing it. They do NOT see the ground-truth skill. The task run just failed.

Your job: Give **modification suggestions only**. Do NOT provide the full solution, code, or the correct skill content. Only point out what is wrong or what to change (e.g. "use paragraph-level replacement, not run-level" or "handle split placeholders by searching in full paragraph text"). Keep suggestions concise and actionable.
"""

TEACHER_USER_SUGGESTIONS = """## Task instruction:
```
{task_instruction}
```

## Ground-truth skill (for your reference only; do not copy to the Student):
```
{skill_md}
```

## Student's current skill (what they wrote):
```
{student_skill}
```

## Failure context:
```
{failure_info}
```

Give modification suggestions only (no solution). Reply with a short list of suggestions.
"""
