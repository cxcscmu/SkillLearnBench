#!/usr/bin/env python3
"""Metric: trajectory_key_point_recall (LLM-as-judge).

trajectory_key_point_recall = fraction of oracle key points recalled by the generated trajectory.

compute() is the primary entry point for use from run_trajectory_eval.py.
main() provides a CLI for standalone use.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import json_repair
import sys
from pathlib import Path
from typing import Any

_TRAJ_DIR = Path(__file__).resolve().parents[1]
if str(_TRAJ_DIR) not in sys.path:
    sys.path.insert(0, str(_TRAJ_DIR))

from utils.prompts import TRAJECTORY_KEY_POINT_CLASSIFICATION
from utils import llm as _llm
from utils.trajectory_io import find_generated_trajectory, read_trajectory


def _load_key_points(path: Path) -> list[dict[str, Any]]:
    data = json_repair.loads(path.read_text(encoding="utf-8", errors="replace").strip())
    if not isinstance(data, list):
        raise ValueError(f"key points file must be a JSON list: {path}")
    points: list[dict[str, Any]] = []
    for i, item in enumerate(data, start=1):
        if isinstance(item, dict):
            kp = str(item.get("key_point", "")).strip()
        elif isinstance(item, str):
            kp = item.strip()
        else:
            continue
        if kp:
            points.append({"index": i, "key_point": kp})
    return points


def _normalize_label(parsed: dict[str, Any]) -> tuple[int, str]:
    raw_label = str(parsed.get("label", "")).strip().lower()
    mapping = {"recalled": 1, "not_recalled": 2, "contradiction": 3}
    if raw_label in mapping:
        return mapping[raw_label], raw_label
    raise ValueError(f"invalid label output: label={raw_label!r}")


async def _eval_one_openai(
    client: Any,
    semaphore: asyncio.Semaphore,
    *,
    model: str,
    index: int,
    source_index: int,
    key_point: str,
    generated_trajectory: str,
) -> dict[str, Any]:
    prompt = TRAJECTORY_KEY_POINT_CLASSIFICATION.format(
        key_point=key_point,
        generated_trajectory=generated_trajectory,
    )
    parsed, _ = await _llm.call_openai_with_retry(
        client, semaphore, prompt=prompt, model=model, max_tokens=800
    )
    label_id, label = _normalize_label(parsed)
    return {
        "index": index,
        "source_index": source_index,
        "key_point": key_point,
        "label_id": label_id,
        "label": label,
        "reason": str(parsed.get("reason", "")).strip(),
    }


# ---------------------------------------------------------------------------
# Core compute function
# ---------------------------------------------------------------------------

async def compute(
    points: list[dict[str, Any]],
    generated_trajectory: str,
    *,
    model: str,
    client: Any | None = None,
    semaphore: asyncio.Semaphore | None = None,
    max_concurrency: int = 8,
) -> dict[str, Any]:
    """Return {"trajectory_key_point_recall": float, "total_key_points": int, "details": list}."""
    details: list[dict[str, Any]] = []

    if client is not None:
        tasks = [
            _eval_one_openai(
                client, semaphore,
                model=model,
                index=i,
                source_index=int(p["index"]),
                key_point=str(p["key_point"]),
                generated_trajectory=generated_trajectory,
            )
            for i, p in enumerate(points, start=1)
        ]
        details = list(await asyncio.gather(*tasks))
    else:
        for i, point in enumerate(points, start=1):
            prompt = TRAJECTORY_KEY_POINT_CLASSIFICATION.format(
                key_point=point["key_point"],
                generated_trajectory=generated_trajectory,
            )
            parsed, _ = await asyncio.to_thread(
                _llm.call_anthropic_with_retry,
                prompt=prompt, model=model, max_tokens=800,
            )
            label_id, label = _normalize_label(parsed)
            details.append({
                "index": i,
                "source_index": point["index"],
                "key_point": point["key_point"],
                "label_id": label_id,
                "label": label,
                "reason": str(parsed.get("reason", "")).strip(),
            })

    total = len(details)
    recalled = sum(1 for d in details if d["label"] == "recalled")
    not_recalled = sum(1 for d in details if d["label"] == "not_recalled")

    return {
        "trajectory_key_point_recall": (recalled / total) if total else 0.0,
        "total_key_points": total,
        "counts": {"recalled": recalled, "not_recalled": not_recalled},
        "details": details,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Compute trajectory_key_point_recall from oracle key points")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--oracle-key-points", type=Path)
    parser.add_argument("--generated-trajectory", type=Path)
    parser.add_argument("--generated-trial-id", type=str)
    parser.add_argument("--trials-root", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--model", default="gpt-5-mini")
    parser.add_argument("--max-concurrency", type=int, default=8)
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

        kp_path = args.oracle_key_points or (task_dir / "reference" / "traj-key-points.generated.json")
        if not kp_path.exists():
            raise FileNotFoundError(f"key points not found: {kp_path}; run generate_oracle_keypoints.py first")

        points = _load_key_points(kp_path)
        if not points:
            raise ValueError(f"no valid key points in {kp_path}")

        gen_traj_path = args.generated_trajectory or find_generated_trajectory(
            trials_root, args.task_id, trial_id=args.generated_trial_id
        )
        gen_traj = read_trajectory(gen_traj_path)

        result = asyncio.run(_run_with_openai_or_anthropic(points, gen_traj, args.model, args.max_concurrency))
        result["task_id"] = args.task_id
        result["model"] = args.model
        result["oracle_key_points_path"] = str(kp_path)
        result["generated_trajectory_path"] = str(gen_traj_path)

        out = args.output or (mc_base / "eval_results" / args.task_id / "metric_key_points.json")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"trajectory_key_point_recall: {result['trajectory_key_point_recall']:.4f}  (n={result['total_key_points']})")
        print(f"Wrote: {out}")
        return 0
    except Exception as e:
        print(f"Failed: {e}", file=sys.stderr)
        return 1


async def _run_with_openai_or_anthropic(points, gen_traj, model, max_concurrency):
    if _llm.get_provider() == "openai":
        from openai import AsyncOpenAI
        import os
        client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
        sem = asyncio.Semaphore(max_concurrency)
        try:
            return await compute(points, gen_traj, model=model, client=client, semaphore=sem)
        finally:
            await client.close()
    return await compute(points, gen_traj, model=model, client=None, semaphore=None)


if __name__ == "__main__":
    raise SystemExit(main())
