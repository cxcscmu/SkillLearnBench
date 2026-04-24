#!/usr/bin/env python3
"""
One-click evaluation pipeline for all tasks x queries (skill metrics only).
"""

from __future__ import annotations

import argparse
import asyncio
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

# -----------------------------------------------------------------------------
# parents:
#   [0]=skill, [1]=evaluation, [2]=SkillLearnBench
# -----------------------------------------------------------------------------
_THIS = Path(__file__).resolve()
GENSKILLBENCH = _THIS.parents[2]

# Absolute paths
TASKS_SRC = GENSKILLBENCH / "tasks"
SKILL_CONFIGS = GENSKILLBENCH / "output" / "skill_generation_results"
MC_RESULTS = GENSKILLBENCH / "output" / "evaluation_reports"
ORACLE_REFS = GENSKILLBENCH / "eval_keypoints"

CONVERT = GENSKILLBENCH / "evaluation" / "skill" / "utils" / "convert_claude_log_to_dataclaw.py"
KEYGEN = GENSKILLBENCH / "evaluation" / "skill" / "utils" / "generate_key_points.py"
SAFETY = GENSKILLBENCH / "evaluation" / "skill" / "metrics" / "compute_safety.py"
EXECUTABILITY = GENSKILLBENCH / "evaluation" / "skill" / "metrics" / "compute_executability.py"
COVERAGE = GENSKILLBENCH / "evaluation" / "skill" / "metrics" / "compute_coverage.py"

PY = sys.executable

# Prefer Claude log first if both exist; then Codex (dataclaw --source codex).
_TRAJECTORY_TXT: list[tuple[str, str]] = [
    ("claude-code.txt", "claude"),
    ("claude_code.txt", "claude"),
    ("codex.txt", "codex"),
    ("codex_code.txt", "codex"),
]


def _pick_trajectory_txt(query_src: Path) -> tuple[Path, str] | None:
    for name, src in _TRAJECTORY_TXT:
        p = query_src / name
        if p.is_file():
            return p, src
    return None


# counters
_counts = {"ok": 0, "fail": 0, "skip": 0}
_lock = asyncio.Lock()


async def _inc(kind: str):
    async with _lock:
        _counts[kind] += 1


def _link_or_copy_dir(src: Path, dst: Path) -> None:
    """Link src → dst, falling back to a copy on platforms/accounts without symlink privilege.

    On Windows, os.symlink requires Administrator or Developer Mode; it raises
    OSError(WinError 1314) otherwise. Copy is small (skill dir) and avoids the perm issue.
    """
    try:
        os.symlink(src, dst, target_is_directory=True)
    except OSError:
        shutil.copytree(src, dst)


def _build_task_sv_tmpdir(task_name: str, config: str) -> Path:
    """Build a tmpdir mirroring skill configs so metric scripts see a flat config-subdir layout.

    Layout:
      tmpdir/
        human_authored/ → SKILL_CONFIGS/human_authored/<task>/
        <config>/      → SKILL_CONFIGS/<config>/<task>/  (omitted if config == human_authored)
    """
    tmpdir = Path(tempfile.mkdtemp(prefix="sv_"))
    ha_src = SKILL_CONFIGS / "human_authored" / task_name
    if ha_src.exists():
        _link_or_copy_dir(ha_src, tmpdir / "human_authored")
    if config != "human_authored":
        var_src = SKILL_CONFIGS / config / task_name
        if var_src.exists():
            _link_or_copy_dir(var_src, tmpdir / config)
    return tmpdir


async def run(cmd: list[str], label: str, sem: asyncio.Semaphore) -> int:
    async with sem:
        t0 = time.time()
        print(f"  ▶ {label}")
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        elapsed = time.time() - t0
        if proc.returncode == 0:
            print(f"  ✓ {label}  ({elapsed:.1f}s)")
            await _inc("ok")
        else:
            err_text = stderr.decode(errors="replace").strip()
            err_lines = err_text.split("\n")
            summary = "\n".join(err_lines[-5:])[:500] if err_lines else "(no stderr)"
            print(f"  ✗ {label}  ({elapsed:.1f}s)\n{summary}")
            await _inc("fail")
        return proc.returncode


async def process_query(
    task_name: str,
    query_id: str,
    sv_dir: Path,
    sem_api: asyncio.Semaphore,
    sem_convert: asyncio.Semaphore,
    force: bool,
    result_dir: Path,
):
    query_src = TASKS_SRC / task_name / query_id   # tasks/ — for instruction.md, tests, etc.
    oracle_dir = ORACLE_REFS / task_name / query_id  # eval_keypoints/ — all oracle files
    result_dir.mkdir(parents=True, exist_ok=True)
    oracle_dir.mkdir(parents=True, exist_ok=True)

    oracle_root = sv_dir / "human_authored"

    # step 1: convert trajectory .txt -> .dataclaw.jsonl (shared with trajectory metrics)
    # claude-code.txt lives in eval_keypoints/ (moved from tasks/)
    picked = _pick_trajectory_txt(oracle_dir)
    jsonl = oracle_dir / "claude-code.dataclaw.jsonl"

    if picked is None:
        print(f"  [ERROR] {query_id}: claude-code.txt not found in {oracle_dir}")
        await _inc("fail")
        return

    txt, dc_source = picked

    if force or not jsonl.exists():
        rc = await run(
            [
                PY,
                str(CONVERT),
                str(txt),
                "-o",
                str(jsonl),
                "--source",
                dc_source,
            ],
            f"convert      {query_id} ({dc_source})",
            sem_convert,
        )
        if rc != 0:
            return

    if not jsonl.exists():
        print(f"  [SKIP] {query_id}: no .jsonl after conversion")
        await _inc("skip")
        return

    # step 2+3: parallel branches
    # skill-key-points.generated.json is oracle-derived (config-independent) → shared cache
    kp_output = ORACLE_REFS / task_name / query_id / "skill-key-points.generated.json"

    async def branch_keypoints_then_fpc():
        if force or not kp_output.exists():
            rc = await run(
                [
                    PY,
                    str(KEYGEN),
                    "--task-id",
                    query_id,
                    "--task-dir",
                    str(query_src),
                    "--oracle-root",
                    str(oracle_root),
                    "--trajectory",
                    str(jsonl),
                    "--output",
                    str(kp_output),
                ],
                f"key_points   {query_id}",
                sem_api,
            )
            if rc != 0:
                return

        if kp_output.exists() and (force or not (result_dir / "key_points.metrics.json").exists()):
            await run(
                [
                    PY,
                    str(COVERAGE),
                    "--task-id",
                    query_id,
                    "--task-dir",
                    str(query_src),
                    "--skill-configs-dir",
                    str(sv_dir),
                    "--key-points-path",
                    str(kp_output),
                    "--output",
                    str(result_dir / "key_points.metrics.json"),
                ],
                f"coverage     {query_id}",
                sem_api,
            )

    async def branch_safety():
        if force or not (result_dir / "safety.metrics.json").exists():
            await run(
                [
                    PY,
                    str(SAFETY),
                    "--task-id",
                    query_id,
                    "--task-dir",
                    str(query_src),
                    "--skill-configs-dir",
                    str(sv_dir),
                    "--output",
                    str(result_dir / "safety.metrics.json"),
                ],
                f"safety       {query_id}",
                sem_api,
            )

    async def branch_exec():
        if force or not (result_dir / "executability.metrics.json").exists():
            await run(
                [
                    PY,
                    str(EXECUTABILITY),
                    "--task-id",
                    query_id,
                    "--task-dir",
                    str(query_src),
                    "--skill-configs-dir",
                    str(sv_dir),
                    "--output",
                    str(result_dir / "executability.metrics.json"),
                ],
                f"exec         {query_id}",
                sem_api,
            )

    await asyncio.gather(
        branch_keypoints_then_fpc(),
        branch_safety(),
        branch_exec(),
        return_exceptions=True,
    )


async def amain(args):
    sem_api = asyncio.Semaphore(args.max_api)
    sem_convert = asyncio.Semaphore(args.max_convert)
    config = args.config

    queries: list[tuple[str, str, Path, Path]] = []  # (task, query_id, sv_tmpdir, result_dir)
    tmpdirs: list[Path] = []

    for task_dir in sorted(TASKS_SRC.iterdir()):
        if not task_dir.is_dir():
            continue
        task_name = task_dir.name
        if args.tasks and task_name not in args.tasks:
            continue

        sv_tmpdir = _build_task_sv_tmpdir(task_name, config)
        tmpdirs.append(sv_tmpdir)

        for query_dir in sorted(task_dir.iterdir()):
            if not query_dir.is_dir():
                continue
            result_dir = MC_RESULTS / config / task_name / query_dir.name
            queries.append((task_name, query_dir.name, sv_tmpdir, result_dir))

    n_tasks = len(set(t for t, _, _, _ in queries))
    print(
        f"=== {len(queries)} queries across {n_tasks} tasks "
        f"(config={config}, api_concurrency={args.max_api}, convert_concurrency={args.max_convert}) ===\n"
    )

    coros = [
        process_query(task, qid, sv, sem_api, sem_convert, args.force, result_dir)
        for task, qid, sv, result_dir in queries
    ]
    await asyncio.gather(*coros, return_exceptions=True)

    for tmpdir in tmpdirs:
        shutil.rmtree(tmpdir, ignore_errors=True)

    print("\n" + "=" * 60)
    print(f"Done.  ok={_counts['ok']}  fail={_counts['fail']}  skip={_counts['skip']}")
    print(f"Results at: {MC_RESULTS / config}")


def main():
    ap = argparse.ArgumentParser(
        description="One-click skill evaluation pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument(
        "--max-api",
        type=int,
        default=5,
        help="Max concurrent API-calling subprocesses (default 5)",
    )
    ap.add_argument(
        "--max-convert",
        type=int,
        default=4,
        help="Max concurrent convert subprocesses (default 4)",
    )
    ap.add_argument("--config", required=True,
                    help="Skill config to evaluate (e.g. human_authored, "
                         "b1-one-shot-claude-sonnet-4-6).")
    ap.add_argument("--force", action="store_true", help="Re-run steps even if outputs already exist")
    ap.add_argument("--tasks", nargs="*", help="Only run these tasks (default: all)")
    asyncio.run(amain(ap.parse_args()))


if __name__ == "__main__":
    main()

