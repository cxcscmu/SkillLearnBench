"""Prompts for Teacher-Student mode: Student generates skill.md, then executes with it."""

# Round 1: Student generates initial skill for the task (output only [SKILL]...[/SKILL]).
SKILL_GEN_PROMPT = """You are given a task. First, write a SKILL.md that describes how to do this task correctly (so someone else could follow it).
Output ONLY in this format—do not run any commands or edit files yet:
[SKILL]
... your skill content in markdown ...
[/SKILL]

Task:
{instruction}
"""

# Round 2+: Student generates a new skill incorporating Teacher's modification suggestions.
SKILL_GEN_WITH_FEEDBACK_PROMPT = """The task failed. The Teacher gave you modification suggestions (no direct solution). Write a new SKILL.md that addresses these suggestions.
Output ONLY in this format—do not run any commands or edit files yet:
[SKILL]
... your revised skill content in markdown ...
[/SKILL]

Task:
{instruction}

## Teacher's modification suggestions (do not copy the solution; use them to improve your skill):
{feedback}

## Previous rounds summary (for context):
{history_text}
"""

# After saving student_skill.md to trial (mounted at /logs), run agent with this to execute using that skill.
EXECUTE_WITH_SKILL_PROMPT = """Execute the task. You have a skill document at /logs/student_skill.md. Read it carefully, refer to it, and follow it to complete the task.
Do not output [SKILL] or [PLAN]; just perform the task.

Task:
{instruction}
"""
