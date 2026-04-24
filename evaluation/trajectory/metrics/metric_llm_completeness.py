#!/usr/bin/env python3
"""Metric: Completeness (LLM-as-judge, score 1-5).

Evaluates whether the agent fully carried out the task — reaching a clear
end-state — without getting stuck in loops, stopping prematurely, or giving up.

Focus is on the tail of the trajectory (completion signal).

compute() is the primary entry point for use from run_trajectory_eval.py.
main() provides a CLI for standalone use.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Any

_TRAJ_DIR = Path(__file__).resolve().parents[1]
if str(_TRAJ_DIR) not in sys.path:
    sys.path.insert(0, str(_TRAJ_DIR))

from utils.prompts import TRAJECTORY_COMPLETENESS_SCORING
from utils import llm as _llm
from utils.trajectory_io import find_generated_trajectory, read_trajectory


def _normalize(value: Any) -> float:
    try:
        score = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"completeness has invalid score: {value}") from exc
    if score < 1.0 or score > 5.0:
        raise ValueError(f"completeness score must be in [1,5], got {score}")
    return round(score, 4)


# ---------------------------------------------------------------------------
# Core compute function
# ---------------------------------------------------------------------------

async def compute(
    task_instruction: str,
    oracle_compact_trajectory: str,
    generated_trajectory: str,
    *,
    model: str,
    client: Any | None = None,
    semaphore: asyncio.Semaphore | None = None,
    retries: int = 3,
) -> dict[str, Any]:
    """Return {"score": float, "reason": str}."""
    prompt = TRAJECTORY_COMPLETENESS_SCORING.format(
        task_instruction=task_instruction,
        oracle_compact_trajectory=oracle_compact_trajectory,
        generated_trajectory=generated_trajectory,
    )
    if client is not None:
        parsed, _ = await _llm.call_openai_with_retry(
            client, semaphore, prompt=prompt, model=model, max_tokens=2048, retries=retries
        )
    else:
        parsed, _ = await asyncio.to_thread(
            _llm.call_anthropic_with_retry,
            prompt=prompt, model=model, max_tokens=2048, retries=retries,
        )
    return {
        "score": _normalize(parsed.get("score")),
        "reason": str(parsed.get("reason", "")).strip(),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Compute completeness score (1-5)")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--generated-trajectory", type=Path)
    parser.add_argument("--generated-trial-id", type=str)
    parser.add_argument("--trials-root", type=Path)
    parser.add_argument("--oracle-compact-trajectory", type=Path,
                        help="Default: tasks/<task-id>/reference/extracted-claude-code.json")
    parser.add_argument("--model", default="gpt-5-mini")
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

        instruction = next(
            p.read_text(encoding="utf-8", errors="replace").strip()
            for name in ["instruction.md", "instructions.md"]
            if (p := task_dir / name).exists()
        )

        gen_traj_path = args.generated_trajectory or find_generated_trajectory(
            trials_root, args.task_id, trial_id=args.generated_trial_id
        )
        gen_traj = read_trajectory(gen_traj_path)

        compact_path = args.oracle_compact_trajectory or (task_dir / "reference" / "extracted-claude-code.json")
        if compact_path.exists():
            oracle_compact = compact_path.read_text(encoding="utf-8", errors="replace").strip()
        else:
            fallback = compact_path.with_suffix(".txt")
            oracle_compact = fallback.read_text(encoding="utf-8", errors="replace").strip() if fallback.exists() else "N/A"

        result = asyncio.run(_run_with_openai_or_anthropic(instruction, oracle_compact, gen_traj, args.model))

        out = args.output or (mc_base / "eval_results" / args.task_id / "metric_completeness.json")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"completeness: {result['score']}  ({result['reason'][:80]})")
        print(f"Wrote: {out}")
        return 0
    except Exception as e:
        print(f"Failed: {e}", file=sys.stderr)
        return 1


async def _run_with_openai_or_anthropic(instruction, oracle_compact, gen_traj, model):
    if _llm.get_provider() == "openai":
        from openai import AsyncOpenAI
        import os
        client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
        sem = asyncio.Semaphore(1)
        try:
            return await compute(instruction, oracle_compact, gen_traj, model=model, client=client, semaphore=sem)
        finally:
            await client.close()
    return await compute(instruction, oracle_compact, gen_traj, model=model, client=None, semaphore=None)


if __name__ == "__main__":
    raise SystemExit(main())
