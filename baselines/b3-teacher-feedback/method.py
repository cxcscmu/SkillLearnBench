"""
b3-teacher-guided — method plugin for core/skill_runner.py

When this file exists, skill_runner discovers it and delegates steps 4+5
(agent execution + optional verification) to run() below instead of using
the standard single-pass path.

Loop structure (per round):
  1. Student LLM generates SKILL.md via direct API call (outside container).
  2. Skills are docker-cp'd into the running container.
  3. Agent executes the task inside the container using those skills.
  4. Verifier checks the result.
  5. If failed and rounds remain: Teacher LLM gives feedback → repeat from 1.
  The Teacher sees the ground-truth skill; the Student does not.

The actual loop implementation lives in core/skill_runner._run_teacher_student_loop.
This file is intentionally thin — it just declares that b3 uses that loop.
"""
from __future__ import annotations

from pathlib import Path
import sys

# Ensure the SkillLearnBench root is importable regardless of cwd.
sys.path.insert(0, str(Path(__file__).parents[2]))
from core.skill_runner import _run_teacher_student_loop


def run(
    *,
    container_name: str,
    task_path: Path,
    trial_path: Path,
    agent: dict,
    model_name: str,
    instruction: str,
    task_workdir: str,
    max_rounds: int,
    max_steps: int,
) -> tuple[bool, int, str, str, int | None]:
    """
    Execute the teacher-student skill generation loop.

    The container is already running and the agent is already installed;
    this function owns steps 4+5 (run agent, run verifier, give teacher
    feedback, repeat).

    Args:
        container_name: name of the running Docker container.
        task_path:       path to the task directory (contains instruction.md,
                         environment/, tests/).
        trial_path:      path to the per-trial output directory (/logs inside
                         the container).
        agent:           agent config dict from agents/__init__.py.
        model_name:      model identifier for both the student and teacher LLM.
        instruction:     base task instruction text (from instruction.md, with
                         any extra-subtask configs already appended).
        task_workdir:    effective WORKDIR inside the container.
        max_rounds:      maximum teacher-student rounds; enforced minimum of 2.
        max_steps:       maximum tool-use steps per agent run.

    Returns:
        passed      (bool):       True if the final verifier run passed.
        steps_used  (int):        total tool-use steps across all rounds.
        agent_stdout (str):       combined agent stdout (last round).
        agent_stderr (str):       combined agent stderr (last round).
        rounds_used (int | None): number of rounds actually executed.
    """
    # Minimum 2 rounds: at least one skill generation + one reflection pass.
    effective_rounds = max(max_rounds, 2)

    passed, rounds_used, _, _, agent_stdout, agent_stderr, steps_used = (
        _run_teacher_student_loop(
            task_path=task_path,
            container_name=container_name,
            trial_path=trial_path,
            agent=agent,
            model_name=model_name,
            task_instruction=instruction,
            task_workdir=task_workdir,
            max_rounds=effective_rounds,
            max_steps=max_steps,
        )
    )
    return passed, steps_used, agent_stdout, agent_stderr, rounds_used
