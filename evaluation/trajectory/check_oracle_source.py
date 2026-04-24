#!/usr/bin/env python3
"""Check which subtasks are missing oracle trajectory source files.

Uses the same path logic as run_trajectory_eval.py.

Oracle source lookup: SkillLearnBench/tasks/<task>/<subtask>/
  - claude-code.txt  (preferred)
  - codex.txt        (fallback)

Subtask discovery (mirrors run_trajectory_eval.py):
  - With --task-id:  scans eval_trials/<task>/ for subtask dirs
  - Without:         scans eval_trials/ for all task dirs, then their subtask dirs

Run from evaluation/metrics-computation/:
  python metrics/trajectory/check_oracle_source.py
  python metrics/trajectory/check_oracle_source.py --task-id anthropic-poster-design
  python metrics/trajectory/check_oracle_source.py --missing-only
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_MC_DIR = Path(__file__).resolve().parents[2]   # metrics-computation/
_EVAL_DIR = Path(__file__).resolve().parents[3]  # evaluation/
_GEN_DIR = Path(__file__).resolve().parents[4]   # SkillLearnBench/

TASKS_ROOT = _GEN_DIR / "tasks"


def _find_oracle_source_path(task_name: str, subtask_name: str) -> Path | None:
    subtask_dir = TASKS_ROOT / task_name / subtask_name
    for name in ["claude-code.txt", "codex.txt"]:
        p = subtask_dir / name
        if p.exists():
            return p
    return None


def _find_subtasks(trials_root: Path, task_name: str) -> list[str]:
    task_dir = trials_root / task_name
    if not task_dir.exists():
        return []
    return sorted(d.name for d in task_dir.iterdir() if d.is_dir())


def _find_tasks(trials_root: Path) -> list[str]:
    if not trials_root.exists():
        return []
    return sorted(d.name for d in trials_root.iterdir() if d.is_dir())


def main() -> int:
    parser = argparse.ArgumentParser(description="Check oracle source coverage across subtasks.")
    parser.add_argument("--task-id",
                        help="Single task name (e.g. anthropic-poster-design). "
                             "Omit to check all tasks.")
    parser.add_argument("--trials-root", type=Path,
                        help="Override trials root (default: evaluation/eval_trials)")
    parser.add_argument("--missing-only", action="store_true",
                        help="Only print subtasks that are missing oracle source.")
    args = parser.parse_args()

    trials_root = args.trials_root.resolve() if args.trials_root else (_EVAL_DIR / "eval_trials")

    tasks = [args.task_id] if args.task_id else _find_tasks(trials_root)
    if not tasks:
        print(f"No tasks found under {trials_root}", file=sys.stderr)
        return 1

    total_ok = 0
    total_missing = 0

    for task_name in tasks:
        subtasks = _find_subtasks(trials_root, task_name)
        if not subtasks:
            print(f"[{task_name}] no subtasks found under {trials_root / task_name}")
            continue

        task_ok = 0
        task_missing = 0
        task_lines: list[str] = []

        for subtask_name in subtasks:
            src = _find_oracle_source_path(task_name, subtask_name)
            if src:
                task_ok += 1
                if not args.missing_only:
                    task_lines.append(f"  ✓  {subtask_name}  ({src.name})")
            else:
                task_missing += 1
                expected_dir = TASKS_ROOT / task_name / subtask_name
                task_lines.append(f"  ✗  {subtask_name}  (expected in {expected_dir})")

        total_ok += task_ok
        total_missing += task_missing

        n = task_ok + task_missing
        status = "✓" if task_missing == 0 else "✗"
        print(f"\n{status}  {task_name}  ({task_ok}/{n} have oracle source)")
        for line in task_lines:
            print(line)

    print(f"\n{'─' * 56}")
    print(f"Total: {total_ok} ok, {total_missing} missing "
          f"(out of {total_ok + total_missing} subtasks across {len(tasks)} task(s))")

    return 0 if total_missing == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
