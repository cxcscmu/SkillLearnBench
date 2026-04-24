#!/usr/bin/env python3
"""Metric: Skill Invocation Ratio (no LLM).

Fraction of available skills (under skill_generation_results/<config>/<task>/) that were
actually invoked (via Skill tool calls) in the trajectory.

compute() is the primary entry point for use from run_trajectory_eval.py.
main() provides a CLI for standalone use.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_TRAJ_DIR = Path(__file__).resolve().parents[1]
if str(_TRAJ_DIR) not in sys.path:
    sys.path.insert(0, str(_TRAJ_DIR))

from utils import llm as _llm
from utils.trajectory_io import extract_skill_invocations, extract_skill_call_counts, find_generated_trajectory


def _get_available_skills(task_dir: Path, config: str = "human_authored") -> list[str]:
    # task_dir = SkillLearnBench/tasks/<task_name>/<subtask_name>/
    # task_dir.parent.name = task_name, task_dir.parents[2] = SkillLearnBench/
    # Layout: output/skill_generation_results/<config>/<task_name>/
    task_name = task_dir.parent.name
    sv_root = task_dir.parents[2] / "output" / "skill_generation_results" / config / task_name
    if not sv_root.exists() or not sv_root.is_dir():
        return []
    return sorted(d.name for d in sv_root.iterdir() if d.is_dir() and not d.name.startswith("."))


# ---------------------------------------------------------------------------
# Core compute function (synchronous — no LLM)
# ---------------------------------------------------------------------------

def compute(
        task_dir: Path,
        traj_path: Path,
        config: str = "human_authored",
) -> dict[str, Any]:
    """Return skill invocation ratio and supporting counts/lists.

    Both num_skills_invoked and skill_calls_among_available are strict subsets of
    the available skills in skill_generation_results/<config>/<task>/.
    When available_set is empty all skill metrics are 0.
    """
    available = _get_available_skills(task_dir, config=config)
    available_set = set(available)

    if not available_set:
        return {
            "skill_invocation_ratio": 0.0,
            "available_skills": [],
            "invoked_skills": [],
            "invoked_among_available": [],
            "skill_calls_among_available": 0,
            "counts": {
                "available": 0,
                "invoked_total": 0,
                "invoked_among_available": 0,
                "skill_calls_among_available": 0,
            },
        }

    invoked = extract_skill_invocations(traj_path)
    call_counts = extract_skill_call_counts(traj_path)

    invoked_in_available = invoked & available_set
    ratio = len(invoked_in_available) / len(available_set)
    skill_calls_among_available = sum(call_counts[k] for k in invoked_in_available)

    return {
        "skill_invocation_ratio": round(ratio, 4),
        "available_skills": available,
        "invoked_skills": sorted(invoked),
        "invoked_among_available": sorted(invoked_in_available),
        "skill_calls_among_available": skill_calls_among_available,
        "counts": {
            "available": len(available_set),
            "invoked_total": len(invoked),
            "invoked_among_available": len(invoked_in_available),
            "skill_calls_among_available": skill_calls_among_available,
        },
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Compute skill invocation ratio (no LLM)")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--trajectory", type=Path)
    parser.add_argument("--mode", default="human_authored",
                        help="Skill config name (e.g. human_authored, no_skill, b1-one-shot-claude-sonnet-4-6)")
    parser.add_argument("--config", default=None,
                        help="Override config name (default: same as --mode)")
    parser.add_argument("--trials-root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    _llm.load_env()

    eval_base = Path(__file__).resolve().parents[4]
    mc_base = Path(__file__).resolve().parents[3]
    tasks_root = eval_base / "tasks"
    trials_root = args.trials_root or (mc_base / "trials")

    try:
        task_dir = tasks_root / args.task_id
        if not task_dir.exists():
            raise FileNotFoundError(f"task not found: {task_dir}")

        config = args.config if args.config is not None else args.mode
        traj_path = args.trajectory or find_generated_trajectory(trials_root, args.task_id)

        result = compute(task_dir, traj_path, config=config)
        result["task_id"] = args.task_id
        result["trajectory_path"] = str(traj_path)
        result["skill_config"] = config

        out = args.output or (mc_base / "eval_results" / args.task_id / "metric_skill_invocation.json")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"skill_invocation_ratio: {result['skill_invocation_ratio']}")
        print(f"Wrote: {out}")
        return 0
    except Exception as e:
        print(f"Failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
