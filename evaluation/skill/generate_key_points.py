#!/usr/bin/env python3
"""
Generate human-authored-skill key points using only task-id as primary input.

Auto-resolved inputs:
- task instruction: tasks/<task-id>/instruction.md
- human_authored skills: output/skill_generation_results/human_authored/<task>/<skill-name>/**
- worker trajectory: latest output/evaluation_log/human_authored/**/<task-id>/*/agent/(trajectory.jsonl|*.dataclaw.jsonl)
- task verifier: tests/test_outputs.py + tests/test.sh (if exists)
"""
from __future__ import annotations

import argparse
import json
import json_repair
import os
import re
import sys
import time
import urllib.error
from pathlib import Path
from typing import Any, Literal

from prompts import GENERATE_KEY_POINTS_PROMPT_TEMPLATE


def _load_env():
    dotenv = Path(__file__).resolve().parent.parent / ".env"
    if dotenv.exists():
        for line in dotenv.read_text().splitlines():
            if not line or line.strip().startswith("#"):
                continue
            if "=" in line:
                k, _, v = line.partition("=")
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k and k not in os.environ:
                    os.environ[k] = v


def _read(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"missing file: {path}")
    return path.read_text(encoding="utf-8", errors="replace").strip()


# NOTE: Currently unused because oracle skill text is not injected into the prompt.
# Keep this block commented for possible future re-enable.
#
# def _is_probably_text(path: Path) -> bool:
#     try:
#         data = path.read_bytes()
#     except OSError:
#         return False
#     if b"\x00" in data[:8192]:
#         return False
#     return True
#
#
# TEXT_EXT_ALLOWLIST = {
#     ".md",
#     ".txt",
#     ".json",
#     ".yaml",
#     ".yml",
#     ".csv",
#     ".tsv",
#     ".py",
#     ".sh",
#     ".js",
#     ".ts",
#     ".sql",
# }
#
#
# def _allowed_supplementary_file(skill_dir: Path, f: Path) -> bool:
#     """
#     Safer inclusion policy:
#     - include text files under scripts/ and references/
#     - include only allowlisted text extensions under assets/
#     - skip everything else
#     """
#     try:
#         rel = f.relative_to(skill_dir)
#     except ValueError:
#         return False
#     if not rel.parts:
#         return False
#     top = rel.parts[0]
#     ext = f.suffix.lower()
#
#     if top in {"scripts", "references"}:
#         return ext in TEXT_EXT_ALLOWLIST and _is_probably_text(f)
#     if top == "assets":
#         return ext in {".md", ".txt", ".json", ".yaml", ".yml", ".csv", ".tsv"} and _is_probably_text(f)
#     return False


def _resolve_paths(base_dir: Path, task_id: str, trajectory: Path | None) -> tuple[Path, Path, Path, list[Path], Path]:
    tasks_root = base_dir / "tasks"
    trials_root = base_dir / "trials"

    task_dir = tasks_root / task_id
    if not task_dir.exists():
        raise FileNotFoundError(f"task not found: {task_dir}")

    instruction = task_dir / "instruction.md"
    oracle_root = base_dir / "output" / "skill_generation_results" / "human_authored" / task_id
    tests_dir = task_dir / "tests"

    verifier_paths = []
    for name in ["test_outputs.py", "test.sh"]:
        p = tests_dir / name
        if p.exists():
            verifier_paths.append(p)

    if not verifier_paths:
        raise FileNotFoundError(f"no verifier found under: {tests_dir}")

    if trajectory is not None:
        traj = trajectory
    else:
        cands: list[Path] = []
        for pattern in [
            f"human_authored/**/{task_id}/*/agent/trajectory.jsonl",
            f"human_authored/**/{task_id}/*/agent/*.dataclaw.jsonl",
        ]:
            cands.extend(trials_root.glob(pattern))
        cands = sorted(cands, key=lambda p: p.stat().st_mtime)
        if not cands:
            raise FileNotFoundError(
                f"no human_authored trajectory found for task_id={task_id}; expected under "
                f"{trials_root}/human_authored/**/{task_id}/*/agent/trajectory.jsonl "
                f"or {trials_root}/human_authored/**/{task_id}/*/agent/*.dataclaw.jsonl"
            )
        traj = cands[-1]

    return task_dir, instruction, oracle_root, verifier_paths, traj


def _summarize_tool_use(tool_use: dict) -> str:
    tool = str(tool_use.get("tool", "")).strip() or "unknown_tool"
    status = str(tool_use.get("status", "")).strip()
    in_obj = tool_use.get("input")
    out_obj = tool_use.get("output")
    parts = [f"tool={tool}"]
    if status:
        parts.append(f"status={status}")
    if isinstance(in_obj, dict) and in_obj:
        keys = ",".join(sorted(str(k) for k in in_obj.keys()))
        parts.append(f"input_keys={keys}")
    if isinstance(out_obj, dict) and out_obj:
        keys = ",".join(sorted(str(k) for k in out_obj.keys()))
        parts.append(f"output_keys={keys}")
    return "; ".join(parts)


def _format_dataclaw_trajectory(obj: dict) -> str:
    messages = obj.get("messages")
    if not isinstance(messages, list):
        return json.dumps(obj, ensure_ascii=False)

    lines: list[str] = []
    for i, msg in enumerate(messages, start=1):
        if not isinstance(msg, dict):
            continue
        role = str(msg.get("role", "unknown"))
        lines.append(f"[{i}] role={role}")

        thinking = msg.get("thinking")
        if isinstance(thinking, str) and thinking.strip():
            lines.append(f"thinking: {thinking.strip()}")

        content = msg.get("content")
        if isinstance(content, str) and content.strip():
            lines.append(f"content: {content.strip()}")

        tool_uses = msg.get("tool_uses")
        if isinstance(tool_uses, list) and tool_uses:
            for t_idx, tool_use in enumerate(tool_uses, start=1):
                if isinstance(tool_use, dict):
                    lines.append(f"tool_use[{t_idx}]: {_summarize_tool_use(tool_use)}")

    if not lines:
        return json.dumps(obj, ensure_ascii=False)
    return "\n".join(lines)


def _read_trajectory(path: Path) -> str:
    raw = _read(path)
    if not raw:
        return raw
    try:
        parsed = json_repair.loads(raw)
    except json.JSONDecodeError:
        return raw

    if isinstance(parsed, dict) and isinstance(parsed.get("messages"), list):
        return _format_dataclaw_trajectory(parsed)
    return raw


# NOTE: Currently unused because oracle skill text is not injected into the prompt.
# Keep this block commented for possible future re-enable.
#
# def _build_oracle_skill_blob(oracle_root: Path) -> str:
#     if not oracle_root.exists():
#         raise FileNotFoundError(f"oracle skill dir not found: {oracle_root}")
#
#     skill_dirs = sorted([d for d in oracle_root.iterdir() if d.is_dir()])
#     if not skill_dirs:
#         raise FileNotFoundError(f"no skill subdirectories in: {oracle_root}")
#
#     chunks: list[str] = []
#     for idx, skill_dir in enumerate(skill_dirs, start=1):
#         skill_name = skill_dir.name
#         skill_md = skill_dir / "SKILL.md"
#         if not skill_md.exists():
#             raise FileNotFoundError(f"missing SKILL.md in {skill_dir}")
#
#         chunks.append(f"# Skill {idx}: {skill_name}")
#         chunks.append("## Skill Document: SKILL.md")
#         chunks.append(_read(skill_md))
#
#         extra_files = []
#         for root_name in ["scripts", "references", "assets"]:
#             root = skill_dir / root_name
#             if not root.exists() or not root.is_dir():
#                 continue
#             for p in root.rglob("*"):
#                 if not p.is_file():
#                     continue
#                 if _allowed_supplementary_file(skill_dir, p):
#                     extra_files.append(p)
#         extra_files = sorted(extra_files, key=lambda p: str(p.relative_to(skill_dir)))
#
#         for f in extra_files:
#             rel = f.relative_to(skill_dir)
#             chunks.append(f"## Supplementary Material: {rel}")
#             chunks.append(_read(f))
#
#     return "\n\n".join(chunks)


def _build_verifier_blob(verifier_paths: list[Path]) -> str:
    chunks: list[str] = []
    for p in verifier_paths:
        chunks.append(f"# Verifier File: {p.name}")
        chunks.append(_read(p))
    return "\n\n".join(chunks)


def _get_provider() -> Literal["openai", ""]:
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    return ""


def _call_llm(prompt: str, model: str, stream_output: bool = True) -> str:
    provider = _get_provider()
    if provider == "openai":
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("openai client not installed") from exc
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        response = client.responses.create(
            model=model,
            input=prompt,
        )
        print("=================")
        print(response)
        print("=================")
        output_text = (response.output_text or "").strip()
        if stream_output and output_text:
            print(output_text)
        if not output_text:
            raise RuntimeError("model returned empty output_text")
        return output_text
    raise RuntimeError("No API key found (set OPENAI_API_KEY)")


def _extract_json_list(text: str) -> list[dict]:
    text = text.strip()
    print("=================")
    print(text)
    try:
        parsed = json_repair.loads(text)
    except json.JSONDecodeError:
        parsed = None

    if isinstance(parsed, dict):
        for key in ("key_points", "points", "result"):
            value = parsed.get(key)
            if isinstance(value, list):
                if all(isinstance(item, dict) for item in value):
                    return value
                raise ValueError(f"'{key}' must be a list of JSON objects")

        raise ValueError("JSON object must contain list field: key_points/points/result")

    # Fallback: extract a JSON list from free-form text.
    m = re.search(r"\[\s*{.*}\s*\]", text, flags=re.S)
    if not m:
        raise ValueError("model output is neither JSON object nor contains JSON list")
    extracted = json_repair.loads(m.group(0))
    if not isinstance(extracted, list):
        raise ValueError("fallback extracted JSON is not a list")
    if not all(isinstance(item, dict) for item in extracted):
        raise ValueError("fallback JSON list must contain only JSON objects")
    return extracted



def _generate_points_with_retries(
    prompt: str, model: str, max_tries: int, stream_output: bool = False
) -> tuple[str, list[dict]]:
    last_error: Exception | None = None
    for attempt in range(1, max_tries + 1):
        try:
            raw = _call_llm(prompt, model=model, stream_output=stream_output)
            points = _extract_json_list(raw)
            return raw, points
        except Exception as exc:
            last_error = exc
            if attempt < max_tries:
                print(f"Attempt {attempt}/{max_tries} failed: {exc}; retrying...", file=sys.stderr)
                time.sleep(1)
    raise RuntimeError(f"Failed after {max_tries} attempts: {last_error}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate human-authored skill key points from task-id")
    parser.add_argument("--task-id", required=True, help="Task folder name under evaluation/tasks")
    parser.add_argument(
        "--trajectory",
        type=Path,
        help="Optional override trajectory path; default uses latest human_authored trial trajectory",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output JSON path; default: trials/human_authored/<task-id>/key_points.generated.json",
    )
    parser.add_argument("--raw-output", type=Path, help="Optional raw model text output path")
    parser.add_argument("--model", default="gpt-5-mini")
    parser.add_argument(
        "--print-llm-input",
        action="store_true",
        default=False,
        help="Print the full prompt sent to the model before generation",
    )
    parser.add_argument(
        "--stream-llm-output",
        action="store_true",
        help="Stream and print model output to terminal in real time",
    )
    parser.add_argument(
        "--max-tries",
        type=int,
        default=3,
        help="Maximum number of tries for model generation/parsing (default: 3)",
    )
    args = parser.parse_args()
    _load_env()

    base_dir = Path(__file__).resolve().parent.parent.parent

    try:
        task_dir, instruction_path, oracle_root, verifier_paths, trajectory_path = _resolve_paths(
            base_dir, args.task_id, args.trajectory
        )

        task_instruction = _read(instruction_path)
        # oracle_skill = _build_oracle_skill_blob(oracle_root)
        worker_trajectory = _read_trajectory(trajectory_path)
        task_verifier = _build_verifier_blob(verifier_paths)

        prompt = GENERATE_KEY_POINTS_PROMPT_TEMPLATE.format(
            task_instruction=task_instruction,
            # oracle_skill=oracle_skill,
            worker_trajectory=worker_trajectory,
            task_verifier=task_verifier,
        )
        if args.print_llm_input:
            print("\n=== LLM Input Prompt Start ===\n")
            print(prompt)
            print("\n=== LLM Input Prompt End ===\n")

        raw, points = _generate_points_with_retries(
            prompt,
            model=args.model,
            max_tries=max(1, args.max_tries),
            stream_output=args.stream_llm_output,
        )

        output_path = args.output or (
            base_dir / "trials" / "human_authored" / args.task_id / "key_points.generated.json"
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(points, indent=2, ensure_ascii=False), encoding="utf-8")

        if args.raw_output:
            args.raw_output.parent.mkdir(parents=True, exist_ok=True)
            args.raw_output.write_text(raw, encoding="utf-8")

        print(f"Task: {args.task_id}")
        print(f"Human-authored skill dir: {oracle_root}")
        print(f"Trajectory: {trajectory_path}")
        print(f"Verifier files: {', '.join(str(p) for p in verifier_paths)}")
        print(f"Wrote key points JSON: {output_path}")
        if args.raw_output:
            print(f"Wrote raw model output: {args.raw_output}")
        return 0

    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTPError {e.code}: {body}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
