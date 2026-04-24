#!/usr/bin/env python3
"""Trajectory evaluation runner.

Orchestrates all trajectory metrics for a given task and skill config:
  1. auto-prepare oracle reference assets if not already present (cached in eval_keypoints/)
  2. for each subtask under the given task: run all metrics concurrently
  3. aggregate per-config statistics and write summary JSON per subtask
  4. write a single CSV (one row per run, no aggregation) to evaluation_reports/<config>/<task>/

Run from evaluation/metrics-computation/:
  python metrics/trajectory/run_trajectory_eval.py --task-id gh-repo-analytics --config human_authored --model gpt-5-mini

Trial structure (evaluation_log/):
  evaluation_log/<config>/<task-name>/<subtask-name>/<trial-id>/agent/<traj-file>

Oracle reference (eval_keypoints/<task>/<subtask>/):
  - claude-code.txt                raw oracle trajectory (REQUIRED — error if missing)
  - claude-code.dataclaw.jsonl     converted JSONL (auto-generated if missing)
  - traj-extracted-oracle.json     compact trajectory (auto-generated if missing)
  - traj-key-points.generated.json key points (auto-generated if missing)

Re-run with --force-refresh-reference to regenerate cached oracle assets.

Run selection (aligns with check_runs.py KEEP_LATEST rules):
  - subtask-1 or flat task → 3 latest runs per config
  - subtask-2, -3, …      → 1 latest run per config
"""
from __future__ import annotations

import argparse
import asyncio
import csv
import json
import math
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from utils import llm as _llm
from utils.trajectory_io import read_trajectory, sanitize_for_json, compute_efficiency_metrics
from utils import extract_oracle_compact, generate_oracle_keypoints
from metrics import (
    metric_llm_execution_order,
    metric_llm_key_points,
    metric_llm_completeness,
    metric_skill_invocation,
)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_METRICS_DIR = Path(__file__).resolve().parents[1]  # SkillLearnBench/evaluation/
_GEN_DIR = Path(__file__).resolve().parents[2]   # SkillLearnBench/

TASKS_ROOT = _GEN_DIR / "tasks"  # SkillLearnBench/tasks/
_ORACLE_REF_DIR = _GEN_DIR / "eval_keypoints"  # eval_keypoints/<task>/<subtask>/
_CONVERT = _GEN_DIR / "evaluation" / "skill" / "utils" / "convert_claude_log_to_dataclaw.py"

# ---------------------------------------------------------------------------
# Variant parsing helpers
# ---------------------------------------------------------------------------

_KNOWN_LLMS = [
    "claude-sonnet-4-6",
    "claude-opus-4-6",
    "claude-haiku-4-5",
    "gemini-3.1-pro-preview",
    "gemini-3.1-flash-lite-preview",
    "gemini-3-flash-preview",
]
_KNOWN_METHODS = [
    "b1-one-shot",
    "b2-self-feedback",
    "b3-teacher-feedback",
    "b4-skill-creator",
]


def _subtask_keep(task_name: str, subtask_name: str) -> int:
    """Return number of latest runs to keep per config (aligns with check_runs.py).

    - subtask-1 or flat task → 3
    - subtask-2, -3, …      → 1
    """
    prefix = task_name + "-"
    if subtask_name.startswith(prefix):
        suffix = subtask_name[len(prefix):]
        if suffix.isdigit() and int(suffix) >= 2:
            return 1
    return 3


def _parse_config(config: str) -> tuple[str, str]:
    """Return (llm, method) from a config directory name.

    Examples:
      b1-one-shot-claude-sonnet-4-6  → ('claude-sonnet-4-6', 'b1-one-shot')
      human_authored                        → ('human_authored', '')
      no_skill                              → ('no_skill', '')
    """
    if config in ("human_authored", "no_skill"):
        return config, ""
    for llm in _KNOWN_LLMS:
        if config.endswith(llm):
            method_part = config[: len(config) - len(llm)].rstrip("-")
            return llm, method_part
    return config, ""


# ---------------------------------------------------------------------------
# CSV output helpers
# ---------------------------------------------------------------------------

_CSV_METRIC_KEYS = (
    "pass",
    "num_steps", "num_tool_calls", "num_skill_calls", "input_tokens", "output_tokens",
    "num_skills_invoked", "num_skills_total", "skill_invocation_ratio",
    "execution_order", "trajectory_key_point_recall", "completeness",
)


def _extract_csv_metric(row: dict, key: str):
    """Extract a scalar metric value from a trial result row for CSV output."""
    if key == "pass":
        v = row.get("reward")
        return "" if v is None else int(v)
    if key == "execution_order":
        return row.get("execution_order", {}).get("score", "")
    if key == "skill_invocation_ratio":
        return row.get("skill_invocation", {}).get("skill_invocation_ratio", "")
    if key == "trajectory_key_point_recall":
        return row.get("key_points", {}).get("trajectory_key_point_recall", "")
    if key == "completeness":
        return row.get("completeness", {}).get("score", "")
    if key == "num_steps":
        return row.get("efficiency", {}).get("num_steps", "")
    if key == "num_tool_calls":
        return row.get("efficiency", {}).get("num_tools", "")
    if key == "num_skill_calls":
        return row.get("skill_invocation", {}).get("counts", {}).get("skill_calls_among_available", "")
    if key == "input_tokens":
        return row.get("efficiency", {}).get("input_tokens", "")
    if key == "output_tokens":
        return row.get("efficiency", {}).get("output_tokens", "")
    if key == "num_skills_invoked":
        return row.get("skill_invocation", {}).get("counts", {}).get("invoked_among_available", "")
    if key == "num_skills_total":
        return row.get("skill_invocation", {}).get("counts", {}).get("available", "")
    return ""


def _write_task_csv(
        task_name: str,
        config: str,
        all_summaries: dict[str, dict],
        results_root: Path,
) -> Path:
    """Write one CSV for the task (all subtasks, one row per run, no aggregation).

    Writes to evaluation_reports/<config>/<task>/<task>-trajectory-results.csv.
    """
    out_dir = results_root / config / task_name
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{task_name}-trajectory-results.csv"

    columns = ["LLM", "method", "Task", "Query", "run_id"] + list(_CSV_METRIC_KEYS)
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(columns)
        for subtask_name in sorted(all_summaries.keys()):
            for row in all_summaries[subtask_name].get("by_run", []):
                llm, method = _parse_config(row["skill_config"])
                csv_row = [
                    llm,
                    method,
                    task_name,
                    subtask_name,
                    row.get("trial_id", ""),
                ]
                csv_row += [_extract_csv_metric(row, k) for k in _CSV_METRIC_KEYS]
                writer.writerow(csv_row)

    return out_path


# ---------------------------------------------------------------------------
# Oracle reference helpers
# ---------------------------------------------------------------------------

def _find_oracle_source_path(task_name: str, subtask_name: str) -> Path:
    """Return oracle trajectory source file for a subtask.

    Prefers the pre-converted dataclaw JSONL in eval_keypoints/ (better quality
    for LLM processing). Falls back to raw claude-code.txt.
    Raises FileNotFoundError if neither exists — claude-code.txt is required.
    """
    kp_dir = _ORACLE_REF_DIR / task_name / subtask_name
    dc_path = kp_dir / "claude-code.dataclaw.jsonl"
    if dc_path.exists():
        return dc_path
    txt_path = kp_dir / "claude-code.txt"
    if txt_path.exists():
        return txt_path
    raise FileNotFoundError(
        f"oracle source not found for {task_name}/{subtask_name}: "
        f"expected claude-code.dataclaw.jsonl or claude-code.txt in {kp_dir}"
    )


def _ensure_dataclaw_oracle(task_name: str, subtask_name: str, force: bool = False) -> None:
    """Convert oracle trajectory to dataclaw JSONL and cache in eval_keypoints/.

    No-op if the dataclaw file already exists (unless force=True).
    Raises FileNotFoundError if claude-code.txt is not present in eval_keypoints/.
    """
    kp_dir = _ORACLE_REF_DIR / task_name / subtask_name
    dc_path = kp_dir / "claude-code.dataclaw.jsonl"
    if dc_path.exists() and not force:
        return
    txt_path = kp_dir / "claude-code.txt"
    if not txt_path.exists():
        raise FileNotFoundError(
            f"oracle source claude-code.txt not found: {txt_path}"
        )
    result = subprocess.run(
        [sys.executable, str(_CONVERT), str(txt_path), "-o", str(dc_path)],
        capture_output=True,
    )
    if result.returncode != 0:
        print(
            f"[warn] dataclaw conversion failed for {task_name}/{subtask_name}: "
            f"{result.stderr.decode(errors='replace').strip()}",
            file=sys.stderr,
        )


def _ensure_oracle_reference(
        task_name: str,
        subtask_name: str,
        model: str,
        force: bool = False,
) -> None:
    """Extract compact oracle trajectory and cache to eval_keypoints/.

    No-op if cache already exists (unless force=True).
    Raises FileNotFoundError if oracle source is missing from eval_keypoints/.
    """
    cache_dir = _ORACLE_REF_DIR / task_name / subtask_name
    compact_out = cache_dir / "traj-extracted-oracle.json"

    if compact_out.exists() and not force:
        return

    oracle_path = _find_oracle_source_path(task_name, subtask_name)  # raises if not found

    task_dir = TASKS_ROOT / task_name / subtask_name
    extract_oracle_compact.run(
        task_dir,
        oracle_path,
        compact_out,
        model=model,
        fallback_text_output=compact_out.with_suffix(".txt"),
        max_tries=3,
    )


def _ensure_oracle_keypoints(
        task_name: str,
        subtask_name: str,
        model: str,
        force: bool = False,
) -> None:
    """Generate trajectory key points from oracle source and cache to eval_keypoints/.

    No-op if cache already exists (unless force=True).
    Raises FileNotFoundError if oracle source is missing from eval_keypoints/.
    """
    cache_dir = _ORACLE_REF_DIR / task_name / subtask_name
    kp_path = cache_dir / "traj-key-points.generated.json"

    if kp_path.exists() and not force:
        return

    oracle_src = _find_oracle_source_path(task_name, subtask_name)  # raises if not found

    task_dir = TASKS_ROOT / task_name / subtask_name
    generate_oracle_keypoints.run(task_dir, oracle_src, kp_path, model=model)


# ---------------------------------------------------------------------------
# Trial discovery
# ---------------------------------------------------------------------------

def _find_subtasks(trials_root: Path, task_name: str, config: str) -> list[str]:
    """Return sorted list of subtask directory names under trials_root/<config>/<task_name>/."""
    task_dir = trials_root / config / task_name
    if not task_dir.exists():
        return []
    return sorted(d.name for d in task_dir.iterdir() if d.is_dir())


def _find_generated_trajectories(
        trials_root: Path,
        task_name: str,
        subtask_name: str,
        config: str,
) -> list[tuple[str, str, Path]]:
    """Return list of (skill_config, trial_id, traj_path) for a subtask.

    Limits runs to align with check_runs.py KEEP_LATEST rules:
      subtask-1 / flat → 3 latest runs  (by mtime)
      subtask-2+       → 1 latest run
    """
    subtask_dir = trials_root / config / task_name / subtask_name
    if not subtask_dir.exists():
        return []

    keep = _subtask_keep(task_name, subtask_name)

    # Sort trial dirs by mtime descending; take only `keep` latest runs
    trial_dirs = sorted(
        (p for p in subtask_dir.iterdir() if p.is_dir()),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )[:keep]

    out: list[tuple[str, str, Path]] = []
    for trial_dir in trial_dirs:
        agent_dir = trial_dir / "agent"
        if not agent_dir.exists():
            continue
        cands: list[Path] = []
        for name in ["trajectory.jsonl", "claude-code.dataclaw.jsonl",
                     "dataclaw.jsonl", "claude-code.txt"]:
            p = agent_dir / name
            if p.exists():
                cands.append(p)
        for p in agent_dir.glob("*.dataclaw.jsonl"):
            if p not in cands:
                cands.append(p)
        if not cands:
            continue
        cands.sort(key=lambda p: p.stat().st_mtime)
        out.append((config, trial_dir.name, cands[-1]))
    return out


# ---------------------------------------------------------------------------
# Per-trial metric runner
# ---------------------------------------------------------------------------

async def _run_metrics_for_trial(
        task_name: str,
        subtask_name: str,
        skill_config: str,
        traj_path: Path,
        *,
        model: str,
        client: Any | None,
        semaphore: asyncio.Semaphore | None,
        key_points: list[dict] | None,
) -> dict[str, Any]:
    """Run all applicable metrics concurrently for one trial."""
    task_dir = TASKS_ROOT / task_name / subtask_name

    instruction = ""
    for name in ["instruction.md", "instructions.md"]:
        p = task_dir / name
        if p.exists():
            instruction = sanitize_for_json(
                p.read_text(encoding="utf-8", errors="replace").strip()
            )
            break

    gen_traj = read_trajectory(traj_path)
    _MAX_HEAD, _MAX_TAIL = 400_000, 200_000
    if len(gen_traj) > _MAX_HEAD + _MAX_TAIL:
        gen_traj = (
                gen_traj[:_MAX_HEAD]
                + f"\n\n[... trajectory truncated: {len(gen_traj)} chars total ...]\n\n"
                + gen_traj[-_MAX_TAIL:]
        )

    cache_dir = _ORACLE_REF_DIR / task_name / subtask_name
    compact_path = cache_dir / "traj-extracted-oracle.json"
    if compact_path.exists():
        oracle_compact = sanitize_for_json(
            compact_path.read_text(encoding="utf-8", errors="replace").strip()
        )
    else:
        fallback = compact_path.with_suffix(".txt")
        oracle_compact = sanitize_for_json(
            fallback.read_text(encoding="utf-8", errors="replace").strip()
            if fallback.exists() else "N/A"
        )

    coros: dict[str, Any] = {
        "execution_order": metric_llm_execution_order.compute(
            instruction, oracle_compact, gen_traj,
            model=model, client=client, semaphore=semaphore,
        ),
        "completeness": metric_llm_completeness.compute(
            instruction, oracle_compact, gen_traj,
            model=model, client=client, semaphore=semaphore,
        ),
    }

    if key_points:
        coros["key_points"] = metric_llm_key_points.compute(
            key_points, gen_traj,
            model=model, client=client, semaphore=semaphore,
        )

    keys = list(coros.keys())
    results_list = await asyncio.gather(*coros.values())
    llm_results = dict(zip(keys, results_list))

    inv_result = metric_skill_invocation.compute(task_dir, traj_path, config=skill_config)
    efficiency = compute_efficiency_metrics(traj_path)

    # traj_path = .../evaluation_log/<config>/<task>/<subtask>/<trial-id>/agent/<file>
    # traj_path.parents[1] = .../evaluation_log/<config>/<task>/<subtask>/<trial-id>/
    reward_path = traj_path.parents[1] / "verifier" / "reward.txt"
    reward: int | None = None
    if reward_path.exists():
        try:
            val = reward_path.read_text(encoding="utf-8", errors="replace").strip()
            reward = int(val) if val else 0
        except (ValueError, OSError):
            reward = None

    return {
        "skill_config": skill_config,
        "trajectory_path": str(traj_path),
        "reward": reward,
        **{k: v for k, v in llm_results.items()},
        "skill_invocation": inv_result,
        "efficiency": efficiency,
    }


# ---------------------------------------------------------------------------
# Aggregation helpers
# ---------------------------------------------------------------------------

def _mean(vals: list[float]) -> float:
    return sum(vals) / len(vals) if vals else 0.0


def _std(vals: list[float]) -> float:
    if len(vals) <= 1:
        return 0.0
    m = _mean(vals)
    return math.sqrt(sum((v - m) ** 2 for v in vals) / len(vals))


def _aggregate_by_config(rows: list[dict]) -> dict[str, dict]:
    grouped: dict[str, list[dict]] = {}
    for r in rows:
        grouped.setdefault(r["skill_config"], []).append(r)

    out: dict[str, dict] = {}
    for config, items in sorted(grouped.items()):
        exec_vals = [float(i["execution_order"]["score"]) for i in items if "execution_order" in i]
        inv_vals = [float(i["skill_invocation"]["skill_invocation_ratio"]) for i in items if "skill_invocation" in i]
        tkpr_vals = [float(i["key_points"]["trajectory_key_point_recall"]) for i in items if "key_points" in i]
        comp_vals = [float(i["completeness"]["score"]) for i in items if "completeness" in i]
        reward_vals = [float(i["reward"]) for i in items if i.get("reward") is not None]

        entry: dict[str, Any] = {"runs": len(items)}
        if exec_vals:
            entry["execution_order"] = _mean(exec_vals);
            entry["execution_order_std"] = _std(exec_vals)
        if inv_vals:
            entry["skill_invocation_ratio"] = _mean(inv_vals);
            entry["skill_invocation_ratio_std"] = _std(inv_vals)
        if tkpr_vals:
            entry["trajectory_key_point_recall"] = _mean(tkpr_vals);
            entry["trajectory_key_point_recall_std"] = _std(tkpr_vals)
        if comp_vals:
            entry["completeness"] = _mean(comp_vals);
            entry["completeness_std"] = _std(comp_vals)
        if reward_vals:
            entry["success_rate"] = _mean(reward_vals)
        out[config] = entry
    return out


# ---------------------------------------------------------------------------
# Per-subtask evaluation loop
# ---------------------------------------------------------------------------

async def _run_all(
        task_name: str,
        subtask_name: str,
        trials_root: Path,
        config: str,
        *,
        model: str,
        results_dir: Path,
) -> dict[str, Any]:
    generated_rows = _find_generated_trajectories(
        trials_root, task_name, subtask_name, config,
    )
    if not generated_rows:
        raise RuntimeError(
            f"no trajectories found under {trials_root / config / task_name / subtask_name}"
        )

    by_run_dir = results_dir / "trajectory_by_run"
    by_run_dir.mkdir(parents=True, exist_ok=True)

    kp_path: Path = _ORACLE_REF_DIR / task_name / subtask_name / "traj-key-points.generated.json"
    key_points: list[dict] | None = None
    if kp_path.exists():
        import json_repair
        data = json_repair.loads(kp_path.read_text(encoding="utf-8", errors="replace"))
        if isinstance(data, list) and data:
            key_points = [
                {"index": i, "key_point": str(item.get("key_point", "")).strip()}
                for i, item in enumerate(data, start=1)
                if isinstance(item, dict) and item.get("key_point")
            ]

    provider = _llm.get_provider()
    client: Any = None
    semaphore: asyncio.Semaphore | None = None
    if provider == "openai":
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
        semaphore = asyncio.Semaphore(100)
    elif provider != "anthropic":
        raise RuntimeError("No API key found (set OPENAI_API_KEY or ANTHROPIC_API_KEY)")

    _MAX_RETRIES = 4  # up to 5 total attempts
    _RETRY_BASE_DELAY = 10  # seconds; wait = base * attempt

    def _make_partial_row(skill_config: str, trial_id: str, traj_path: Path) -> dict:
        """Fallback row with only non-LLM fields filled; LLM metrics will be empty in CSV."""
        reward_path = traj_path.parents[1] / "verifier" / "reward.txt"
        reward: int | None = None
        if reward_path.exists():
            try:
                val = reward_path.read_text(encoding="utf-8", errors="replace").strip()
                reward = int(val) if val else 0
            except (ValueError, OSError):
                pass
        task_dir = TASKS_ROOT / task_name / subtask_name
        return {
            "skill_config": skill_config,
            "trial_id": trial_id,
            "trajectory_path": str(traj_path),
            "reward": reward,
            "efficiency": compute_efficiency_metrics(traj_path),
            "skill_invocation": metric_skill_invocation.compute(
                task_dir, traj_path, config=skill_config
            ),
            "_partial": True,
        }

    async def _run_one(skill_config: str, trial_id: str, traj_path: Path) -> dict:
        safe_tag = "".join(c if c.isalnum() or c in {"-", "_"} else "_"
                           for c in f"{skill_config}__{trial_id}")
        last_exc: BaseException | None = None
        for attempt in range(_MAX_RETRIES + 1):
            if attempt > 0:
                wait = _RETRY_BASE_DELAY * attempt
                print(f"  [retry {attempt}/{_MAX_RETRIES}] {skill_config}/{trial_id} "
                      f"in {wait}s …", flush=True)
                await asyncio.sleep(wait)
            try:
                print(f"  [trial] {skill_config}/{trial_id} ← {traj_path.name}", flush=True)
                row = await _run_metrics_for_trial(
                    task_name, subtask_name, skill_config, traj_path,
                    model=model, client=client, semaphore=semaphore,
                    key_points=key_points,
                )
                row["trial_id"] = trial_id
                (by_run_dir / f"trial__{safe_tag}.json").write_text(
                    json.dumps(row, indent=2, ensure_ascii=False), encoding="utf-8"
                )
                return row
            except Exception as exc:
                last_exc = exc
                print(f"  [WARN attempt {attempt + 1}/{_MAX_RETRIES + 1}] "
                      f"{skill_config}/{trial_id}: {exc}", file=sys.stderr)

        # All retries exhausted — write partial row to preserve row count in CSV
        print(f"  [PARTIAL] {skill_config}/{trial_id}: LLM metrics empty after "
              f"{_MAX_RETRIES + 1} attempts", file=sys.stderr)
        partial = _make_partial_row(skill_config, trial_id, traj_path)
        (by_run_dir / f"trial__{safe_tag}.json").write_text(
            json.dumps(partial, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return partial

    try:
        results = await asyncio.gather(
            *[_run_one(sv, tid, tp) for sv, tid, tp in generated_rows],
            return_exceptions=True,
        )
    finally:
        if client is not None:
            await client.close()

    all_rows: list[dict] = []
    for (sv, tid, tp), res in zip(generated_rows, results):
        if isinstance(res, BaseException):
            # _run_one should never raise (retries + partial fallback), but guard anyway
            print(f"  [WARN] {sv}/{tid} failed: {res}", file=sys.stderr)
        else:
            all_rows.append(res)

    by_config = _aggregate_by_config(all_rows)
    summary = {
        "task_id": f"{task_name}/{subtask_name}",
        "model": model,
        "trials_root": str(trials_root),
        "aggregated_over_runs": len(all_rows),
        "by_config": by_config,
        "by_run": all_rows,
    }
    out_path = results_dir / "trajectory_evaluation.json"
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

_METRIC_KEYS = (
    "success_rate", "execution_order", "skill_invocation_ratio",
    "trajectory_key_point_recall", "completeness",
)


def _print_subtask_summary(task_name: str, subtask_name: str, config: str, summary: dict, results_root: Path) -> None:
    results_path = results_root / config / task_name / subtask_name / "trajectory_evaluation.json"
    print(f"\n{'=' * 64}")
    print(f"  {task_name} / {subtask_name}")
    print(f"{'=' * 64}")
    print(f"  Wrote: {results_path}")

    print("\n  By config:")
    for config, stats in summary["by_config"].items():
        parts = [f"runs={stats['runs']}"]
        for k in _METRIC_KEYS:
            if k in stats:
                parts.append(f"{k}={stats[k]:.3f}")
        print(f"    {config}: {', '.join(parts)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run trajectory evaluation for a task.")
    parser.add_argument("--task-id", required=True,
                        help="Parent task name (e.g. gh-repo-analytics). "
                             "All subtasks are discovered automatically.")
    parser.add_argument("--config", required=True,
                        help="Skill config to evaluate (e.g. human_authored, no_skill, "
                             "b1-one-shot-claude-sonnet-4-6).")
    parser.add_argument("--force-refresh-reference", action="store_true",
                        help="Force re-generation of cached oracle reference assets.")
    parser.add_argument("--trials-root", type=Path,
                        help="Override trials root (default: output/evaluation_log)")
    parser.add_argument("--results-root", type=Path,
                        help="Override results output root (default: output/evaluation_reports).")
    parser.add_argument("--model", default="gpt-5-mini")
    args = parser.parse_args()

    _llm.load_env()

    task_name = args.task_id
    config = args.config
    trials_root = args.trials_root.resolve() if args.trials_root else (_GEN_DIR / "output" / "evaluation_log")
    results_root = args.results_root.resolve() if args.results_root else (_GEN_DIR / "output" / "evaluation_reports")

    subtasks = _find_subtasks(trials_root, task_name, config)
    if not subtasks:
        print(f"No subtasks found under {trials_root / config / task_name}", file=sys.stderr)
        return 1

    n = len(subtasks)
    print(f"Found {n} subtask(s) for '{task_name}' (config={config}): {', '.join(subtasks)}")

    all_summaries: dict[str, dict] = {}

    for idx, subtask_name in enumerate(subtasks, 1):
        prefix = f"[{idx}/{n}] {subtask_name}"

        keep = _subtask_keep(task_name, subtask_name)
        print(f"{prefix}: keep={keep} run(s)", flush=True)

        # Oracle reference (cached or generate)
        compact_out = _ORACLE_REF_DIR / task_name / subtask_name / "traj-extracted-oracle.json"
        kp_out = _ORACLE_REF_DIR / task_name / subtask_name / "traj-key-points.generated.json"
        need_ref = not compact_out.exists() or args.force_refresh_reference
        need_kp = not kp_out.exists() or args.force_refresh_reference

        if need_ref:
            print(f"{prefix}: generating oracle reference ...", flush=True)
        if need_kp:
            print(f"{prefix}: generating key points ...", flush=True)
        if not need_ref and not need_kp:
            print(f"{prefix}: oracle reference cached", flush=True)

        try:
            _ensure_dataclaw_oracle(task_name, subtask_name, force=args.force_refresh_reference)
            _ensure_oracle_reference(task_name, subtask_name, args.model,
                                     force=args.force_refresh_reference)
            _ensure_oracle_keypoints(task_name, subtask_name, args.model,
                                     force=args.force_refresh_reference)
        except FileNotFoundError as exc:
            print(f"{prefix}: WARN {exc} — skipping", file=sys.stderr)
            continue

        results_dir = results_root / config / task_name / subtask_name
        results_dir.mkdir(parents=True, exist_ok=True)

        n_trials = len(_find_generated_trajectories(
            trials_root, task_name, subtask_name, config,
        ))
        print(f"{prefix}: running metrics ({n_trials} trial(s)) ...", flush=True)

        try:
            summary = asyncio.run(_run_all(
                task_name, subtask_name, trials_root, config,
                model=args.model,
                results_dir=results_dir,
            ))
        except RuntimeError as exc:
            print(f"{prefix}: WARN {exc} — skipping", file=sys.stderr)
            continue

        n_done = summary.get("aggregated_over_runs", 0)
        print(f"{prefix}: done ({n_done} trial(s) evaluated)", flush=True)
        all_summaries[subtask_name] = summary

    if not all_summaries:
        print("No subtasks evaluated successfully.", file=sys.stderr)
        return 1

    for subtask_name, summary in all_summaries.items():
        _print_subtask_summary(task_name, subtask_name, config, summary, results_root)

    # Write per-task CSV (one row per run, never aggregated)
    csv_path = _write_task_csv(task_name, config, all_summaries, results_root)
    print(f"\nCSV written → {csv_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
