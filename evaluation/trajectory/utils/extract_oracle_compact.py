#!/usr/bin/env python3
"""Extract a compact oracle trajectory from a dataclaw JSONL via LLM.

Output: tasks/<task-id>/reference/extracted-claude-code.json
"""
from __future__ import annotations

import argparse
import asyncio
import json
import json_repair
import os
import sys
from pathlib import Path
from typing import Any

_TRAJ_DIR = Path(__file__).resolve().parents[1]
if str(_TRAJ_DIR) not in sys.path:
    sys.path.insert(0, str(_TRAJ_DIR))

from utils.prompts import EXTRACT_ORACLE_COMPACT_TRAJECTORY
from utils import llm as _llm


# ---------------------------------------------------------------------------
# Trajectory formatting
# ---------------------------------------------------------------------------

def _shorten(text: str, limit: int = 220) -> str:
    s = " ".join(text.split())
    return s if len(s) <= limit else s[: limit - 3] + "..."


def _safe_json_dumps(obj: Any, limit: int = 180) -> str:
    try:
        txt = json.dumps(obj, ensure_ascii=False)
    except Exception:
        txt = str(obj)
    return _shorten(txt, limit=limit)


def _format_dataclaw_messages(messages: list[dict[str, Any]], max_events: int) -> str:
    lines: list[str] = []
    for msg in messages:
        if not isinstance(msg, dict):
            continue
        role = str(msg.get("role", "unknown")).strip()
        content = msg.get("content")
        if isinstance(content, str) and content.strip():
            lines.append(f"[{role}/text] {_shorten(content)}")
        thinking = msg.get("thinking")
        if isinstance(thinking, str) and thinking.strip():
            lines.append(f"[{role}/thinking] {_shorten(thinking)}")
        tool_uses = msg.get("tool_uses")
        if isinstance(tool_uses, list):
            for tool_use in tool_uses:
                if not isinstance(tool_use, dict):
                    continue
                name = str(tool_use.get("tool", "")).strip() or "unknown_tool"
                inp = tool_use.get("input", {})
                status = str(tool_use.get("status", "")).strip()
                lines.append(f"[{role}/tool] {name} status={status or 'unknown'} input={_safe_json_dumps(inp)}")
                out = tool_use.get("output")
                if out is not None:
                    lines.append(f"[{role}/tool_result] {_safe_json_dumps(out)}")
        if len(lines) >= max_events:
            break
    return "\n".join(lines[:max_events])


def _build_compact_oracle_trace(path: Path, max_events: int = 1200) -> str:
    raw = path.read_text(encoding="utf-8", errors="replace").strip()
    if not raw:
        raise ValueError(f"empty oracle trajectory: {path}")
    try:
        parsed = json_repair.loads(raw)
    except json.JSONDecodeError:
        parsed = None

    if isinstance(parsed, dict) and isinstance(parsed.get("messages"), list):
        lines = _format_dataclaw_messages(parsed["messages"], max_events=max_events)
        if lines:
            return lines
    if isinstance(parsed, list):
        lines = _format_dataclaw_messages(parsed, max_events=max_events)
        if lines:
            return lines

    # Fallback: parse as raw JSONL events
    lines_raw: list[str] = []
    for raw_line in raw.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        etype = str(obj.get("type", "")).strip()
        if etype:
            lines_raw.append(f"[event={etype}] {_safe_json_dumps(obj)}")
        if len(lines_raw) >= max_events:
            break
    if not lines_raw:
        raise ValueError(f"no parseable events from oracle trajectory: {path}")
    return "\n".join(lines_raw[:max_events])


def _extract_trace_or_none(path: Path, max_events: int) -> str | None:
    try:
        return _build_compact_oracle_trace(path, max_events=max_events)
    except Exception:
        return None


def _coerce_rows(parsed: Any) -> list[dict[str, Any]]:
    if isinstance(parsed, list):
        return [x for x in parsed if isinstance(x, dict)]
    if isinstance(parsed, dict):
        for key in ("steps", "items", "data", "result", "results"):
            value = parsed.get(key)
            if isinstance(value, list):
                return [x for x in value if isinstance(x, dict)]
        if "core_step" in parsed:
            return [parsed]
    return []


def _extract_json_rows(text: str) -> list[dict[str, Any]]:
    import re
    text = text.strip()
    if not text:
        return []
    try:
        parsed = json_repair.loads(text)
    except Exception:
        parsed = None
    rows = _coerce_rows(parsed)
    if rows:
        return rows
    m = re.search(r"\[[\s\S]*\]", text)
    if not m:
        return []
    try:
        parsed = json_repair.loads(m.group(0))
    except Exception:
        return []
    return _coerce_rows(parsed)


def _normalize_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for i, row in enumerate(rows, start=1):
        core = str(row.get("core_step", "")).strip()
        if not core:
            continue
        step_idx = row.get("step_index", i)
        try:
            step_idx = int(step_idx)
        except (TypeError, ValueError):
            step_idx = i
        out.append({
            "step_index": step_idx,
            "core_step": core,
            "why_essential": str(row.get("why_essential", "")).strip(),
            "evidence": str(row.get("evidence", "")).strip(),
        })
    out.sort(key=lambda x: int(x.get("step_index", 0)))
    return out


def _get_instruction(task_dir: Path) -> str:
    for name in ["instruction.md", "instructions.md"]:
        p = task_dir / name
        if p.exists():
            return p.read_text(encoding="utf-8", errors="replace").strip()
    raise FileNotFoundError(f"no instruction in {task_dir}")


# ---------------------------------------------------------------------------
# Core run function (callable from run_trajectory_eval.py)
# ---------------------------------------------------------------------------

def run(
    task_dir: Path,
    oracle_path: Path,
    output: Path,
    *,
    model: str,
    fallback_text_output: Path | None = None,
    max_events: int = 1200,
    max_tries: int = 3,
) -> None:
    """Extract compact oracle trajectory and write to output JSON.

    Falls back to plain-text output if JSON normalization fails.
    """
    fallback_txt = fallback_text_output or output.with_suffix(".txt")
    instruction = _get_instruction(task_dir)

    if not oracle_path.exists():
        raise FileNotFoundError(
            f"oracle trajectory not found: {oracle_path}. "
            "Run scripts/prepare_oracle_reference.py first."
        )

    compact_trace: str | None = None
    tries = max(1, max_tries)
    for _ in range(tries):
        compact_trace = _extract_trace_or_none(oracle_path, max_events=max(100, max_events))
        if compact_trace:
            break

    if not compact_trace:
        fallback_txt.parent.mkdir(parents=True, exist_ok=True)
        fallback_txt.write_text(
            oracle_path.read_text(encoding="utf-8", errors="replace"),
            encoding="utf-8",
        )
        print(f"[extract] fallback text saved (no parseable JSON): {fallback_txt}")
        return

    prompt = EXTRACT_ORACLE_COMPACT_TRAJECTORY.format(
        task_instruction=instruction,
        oracle_trajectory=compact_trace,
    )

    raw = ""
    normalized: list[dict[str, Any]] = []
    for attempt in range(1, tries + 1):
        if os.environ.get("OPENAI_API_KEY"):
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])

            async def _call() -> str:
                try:
                    r = await client.chat.completions.create(
                        model=model,
                        messages=[{"role": "user", "content": prompt}],
                        max_completion_tokens=2400,
                        extra_body=_llm.openai_reasoning_extra_body(model),
                    )
                    return (r.choices[0].message.content or "").strip()
                finally:
                    await client.close()

            raw = asyncio.run(_call())
        elif os.environ.get("ANTHROPIC_API_KEY"):
            raw = _llm.call_anthropic(prompt, model=model, max_tokens=2400)
        else:
            raise RuntimeError("No API key found (set OPENAI_API_KEY or ANTHROPIC_API_KEY)")

        parsed_rows = _extract_json_rows(raw)
        normalized = _normalize_rows(parsed_rows)
        if normalized:
            break
        print(f"[extract] parse attempt {attempt}/{tries} failed to produce valid JSON steps")

    if not normalized:
        fallback_txt.parent.mkdir(parents=True, exist_ok=True)
        fallback_txt.write_text(raw or compact_trace, encoding="utf-8")
        print(f"[extract] fallback text saved (invalid model output after {tries} tries): {fallback_txt}")
        return

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[extract] extracted {len(normalized)} core steps → {output}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Extract compact oracle trajectory")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--oracle-trajectory", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--model", default="gpt-5-mini")
    parser.add_argument("--raw-output", type=Path)
    parser.add_argument("--max-events", type=int, default=1200)
    parser.add_argument("--max-tries", type=int, default=3)
    parser.add_argument("--fallback-text-output", type=Path)
    args = parser.parse_args()

    _llm.load_env()

    eval_base = Path(__file__).resolve().parents[4]  # evaluation/
    tasks_root = eval_base / "tasks"

    try:
        task_dir = tasks_root / args.task_id
        if not task_dir.exists():
            raise FileNotFoundError(f"task not found: {task_dir}")
        output = args.output or (task_dir / "reference" / "extracted-claude-code.json")
        oracle_default = task_dir / "reference" / "claude-code.dataclaw.jsonl"
        oracle_path = args.oracle_trajectory or oracle_default

        run(
            task_dir,
            oracle_path,
            output,
            model=args.model,
            fallback_text_output=args.fallback_text_output,
            max_events=args.max_events,
            max_tries=args.max_tries,
        )
        return 0
    except Exception as e:
        print(f"Failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
