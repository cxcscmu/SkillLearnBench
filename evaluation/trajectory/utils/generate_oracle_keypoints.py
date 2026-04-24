#!/usr/bin/env python3
"""Generate trajectory key points from the oracle trajectory (no oracle skill).

Output: tasks/<task-id>/reference/traj-key-points.generated.json
"""
from __future__ import annotations

import argparse
import json
import json_repair
import re
import sys
from pathlib import Path

_TRAJ_DIR = Path(__file__).resolve().parents[1]
if str(_TRAJ_DIR) not in sys.path:
    sys.path.insert(0, str(_TRAJ_DIR))

from utils.prompts import GENERATE_ORACLE_TRAJECTORY_KEY_POINTS
from utils import llm as _llm
from utils.trajectory_io import find_oracle_trajectory, read_trajectory


def _get_instruction(task_dir: Path) -> str:
    for name in ["instruction.md", "instructions.md"]:
        p = task_dir / name
        if p.exists():
            return p.read_text(encoding="utf-8", errors="replace").strip()
    raise FileNotFoundError(f"no instruction in {task_dir}")


def _extract_json_list(text: str) -> list[dict]:
    text = text.strip()
    try:
        parsed = json_repair.loads(text)
        if isinstance(parsed, list):
            return parsed
    except json.JSONDecodeError:
        pass
    m = re.search(r"\[\s*\{.*\}\s*\]", text, flags=re.DOTALL)
    if not m:
        raise ValueError("model output does not contain a JSON list")
    parsed = json_repair.loads(m.group(0))
    if not isinstance(parsed, list):
        raise ValueError("parsed JSON is not a list")
    return parsed


# ---------------------------------------------------------------------------
# Core run function
# ---------------------------------------------------------------------------

def run(
    task_dir: Path,
    oracle_traj_path: Path,
    output: Path,
    *,
    model: str,
) -> None:
    """Generate key points from oracle trajectory and write to output JSON."""
    instruction = _get_instruction(task_dir)
    oracle_trajectory = read_trajectory(oracle_traj_path)

    prompt = GENERATE_ORACLE_TRAJECTORY_KEY_POINTS.format(
        task_instruction=instruction,
        oracle_trajectory=oracle_trajectory,
    )
    raw = _llm.call_anthropic(prompt, model=model) if not __import__("os").environ.get("OPENAI_API_KEY") else _call_openai(prompt, model)

    points = _extract_json_list(raw)
    normalized = [
        {
            "reason": str(item.get("reason", "")).strip(),
            "key_point": str(item.get("key_point", "")).strip(),
            "trajectory_reference": str(item.get("trajectory_reference", "")).strip(),
        }
        for item in points
        if isinstance(item, dict)
    ]
    normalized = [p for p in normalized if p["key_point"]]

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(normalized, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[keypoints] wrote {len(normalized)} key points → {output}")


def _call_openai(prompt: str, model: str) -> str:
    import asyncio, os
    from openai import AsyncOpenAI

    async def _call() -> str:
        client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
        try:
            r = await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_completion_tokens=3000,
                extra_body=_llm.openai_reasoning_extra_body(model),
            )
            return (r.choices[0].message.content or "").strip()
        finally:
            await client.close()

    return asyncio.run(_call())


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Generate oracle trajectory key points")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--oracle-trajectory", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--model", default="gpt-5-mini")
    parser.add_argument("--trials-root", type=Path)
    parser.add_argument("--raw-output", type=Path)
    args = parser.parse_args()

    _llm.load_env()

    eval_base = Path(__file__).resolve().parents[4]  # evaluation/
    mc_base = Path(__file__).resolve().parents[3]    # metrics-computation/
    tasks_root = eval_base / "tasks"
    trials_root = args.trials_root or (mc_base / "trials")
    task_dir = tasks_root / args.task_id

    if not task_dir.exists():
        print(f"Failed: task not found: {task_dir}", file=sys.stderr)
        return 1

    try:
        traj_path = args.oracle_trajectory or find_oracle_trajectory(trials_root, args.task_id)
        output = args.output or (task_dir / "reference" / "traj-key-points.generated.json")
        run(task_dir, traj_path, output, model=args.model)
        return 0
    except Exception as e:
        print(f"Failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
