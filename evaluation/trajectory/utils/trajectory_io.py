"""Read and format trajectory files (single JSON with messages or JSONL) for prompts."""
from __future__ import annotations

import json
import json_repair
from pathlib import Path


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


def _format_messages(messages: list) -> str:
    """Format dataclaw-style messages list (each item has role/thinking/content/tool_uses)."""
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
    return "\n".join(lines) if lines else ""


def _format_jsonl(raw: str) -> str:
    """Format Claude Code native JSONL trajectory (one JSON object per line).

    Skips system init lines and isSynthetic skill-injection lines (skill documentation
    bloat that is irrelevant to trajectory evaluation). Formats assistant thinking,
    tool calls, and user tool results in a readable form for LLM prompts.
    """
    lines: list[str] = []
    msg_idx = 0
    for raw_line in raw.splitlines():
        raw_line = raw_line.strip()
        if not raw_line:
            continue
        try:
            obj = json_repair.loads(raw_line)
        except Exception:
            continue
        if not isinstance(obj, dict):
            continue

        obj_type = obj.get("type", "")
        # Skip system init and isSynthetic skill-content injections
        if obj_type == "system" or obj.get("isSynthetic"):
            continue

        message = obj.get("message")
        if not isinstance(message, dict):
            continue

        role = message.get("role", obj_type)
        msg_idx += 1
        lines.append(f"[{msg_idx}] role={role}")

        content = message.get("content", [])
        if isinstance(content, str) and content.strip():
            lines.append(f"content: {content.strip()}")
        elif isinstance(content, list):
            tool_idx = 0
            for item in content:
                if not isinstance(item, dict):
                    continue
                item_type = item.get("type", "")
                if item_type == "thinking":
                    thinking = item.get("thinking", "").strip()
                    if thinking:
                        lines.append(f"thinking: {thinking}")
                elif item_type == "text":
                    text = item.get("text", "").strip()
                    if text:
                        lines.append(f"content: {text}")
                elif item_type == "tool_use":
                    tool_idx += 1
                    name = item.get("name", "unknown")
                    inp = item.get("input") or {}
                    inp_str = json.dumps(inp, ensure_ascii=False)[:300] if inp else ""
                    lines.append(f"tool_use[{tool_idx}]: tool={name}; input={inp_str}")
                elif item_type == "tool_result":
                    result_content = item.get("content", "")
                    if isinstance(result_content, list):
                        texts = [c.get("text", "") for c in result_content
                                 if isinstance(c, dict) and c.get("type") == "text"]
                        result_content = " ".join(texts)
                    if isinstance(result_content, str):
                        result_content = result_content.strip()[:800]
                    lines.append(f"tool_result: {result_content}")
    return "\n".join(lines) if lines else ""


def sanitize_for_json(text: str) -> str:
    """Remove characters that are invalid in JSON strings.

    Specifically removes:
    - Null bytes (\\x00): not allowed in JSON strings
    - Other C0/C1 control characters except \\t, \\n, \\r
    - Lone UTF-16 surrogates (\\uD800-\\uDFFF): invalid in strict JSON (RFC 8259)
    """
    # Strip null bytes and non-printable control chars (keep \t \n \r)
    text = "".join(
        c for c in text
        if c in ("\t", "\n", "\r") or (ord(c) >= 0x20 and ord(c) != 0x7F)
    )
    # Re-encode to drop lone surrogates
    text = text.encode("utf-8", errors="replace").decode("utf-8", errors="replace")
    return text


def read_trajectory(path: Path) -> str:
    """
    Read a trajectory file and return a string suitable for LLM prompts.

    Supports three formats:
    1. Dataclaw single-JSON: {"messages": [...]} → formatted via _format_messages
    2. Claude Code native JSONL: one JSON object per line → formatted via _format_jsonl
    3. Plain text fallback: returned as-is

    Output is always sanitized to remove characters invalid in JSON strings.
    """
    raw = path.read_text(encoding="utf-8", errors="replace").strip()
    if not raw:
        return raw

    # --- Format 1: dataclaw single-JSON with "messages" list ---
    try:
        parsed = json_repair.loads(raw)
        if isinstance(parsed, dict) and isinstance(parsed.get("messages"), list):
            return sanitize_for_json(_format_messages(parsed["messages"]))
    except Exception:
        pass

    # --- Format 2: Claude Code native JSONL (first non-empty line is a JSON object
    #     with a "type" field, characteristic of Claude Code session logs) ---
    first_line = next((l.strip() for l in raw.splitlines() if l.strip()), "")
    try:
        first_obj = json_repair.loads(first_line)
        if isinstance(first_obj, dict) and "type" in first_obj:
            formatted = _format_jsonl(raw)
            if formatted:
                return sanitize_for_json(formatted)
    except Exception:
        pass

    # --- Format 3: plain text ---
    return sanitize_for_json(raw)


def _find_trajectory_file(agent_dir: Path) -> Path | None:
    """Return trajectory.jsonl or latest *.dataclaw.jsonl in agent_dir."""
    candidates: list[Path] = []
    for name in ["trajectory.jsonl", "claude-code.dataclaw.jsonl", "dataclaw.jsonl"]:
        p = agent_dir / name
        if p.exists():
            candidates.append(p)
    for p in agent_dir.glob("*.dataclaw.jsonl"):
        if p not in candidates:
            candidates.append(p)
    if not candidates:
        return None
    candidates.sort(key=lambda x: x.stat().st_mtime)
    return candidates[-1]


def find_oracle_trajectory(trials_root: Path, task_id: str) -> Path:
    """Latest human_authored trial trajectory file (trajectory.jsonl or *.dataclaw.jsonl)."""
    pattern = f"human_authored/**/{task_id}/*/agent"
    cands: list[Path] = []
    for agent_dir in trials_root.glob(pattern):
        if not agent_dir.is_dir():
            continue
        traj = _find_trajectory_file(agent_dir)
        if traj is not None:
            cands.append(traj)
    cands.sort(key=lambda p: p.stat().st_mtime)
    if not cands:
        raise FileNotFoundError(
            f"no human_authored trajectory found for task_id={task_id}; "
            f"expected under {trials_root}/human_authored/**/{task_id}/*/agent/"
        )
    return cands[-1]


def extract_skill_invocations(path: Path) -> set[str]:
    """
    Parse a trajectory file and return the set of skill names invoked via the Skill tool.

    Supports two formats:
    1. Dataclaw single-JSON: {"messages": [...]} with tool_uses entries where tool=="Skill"
    2. Claude Code native JSONL: one JSON object per line; assistant messages have
       content items with {"type":"tool_use","name":"Skill","input":{"skill":"<name>"}}
    """
    raw = path.read_text(encoding="utf-8", errors="replace").strip()
    if not raw:
        return set()

    invoked: set[str] = set()

    # --- Format 1: dataclaw single-JSON with "messages" list ---
    try:
        parsed = json_repair.loads(raw)
        if isinstance(parsed, dict) and isinstance(parsed.get("messages"), list):
            for msg in parsed["messages"]:
                if not isinstance(msg, dict):
                    continue
                for tu in msg.get("tool_uses") or []:
                    if not isinstance(tu, dict):
                        continue
                    if str(tu.get("tool", "")).strip() != "Skill":
                        continue
                    inp = tu.get("input")
                    if isinstance(inp, dict) and "skill" in inp:
                        name = str(inp["skill"]).strip()
                        if name:
                            invoked.add(name)
            return invoked
    except Exception:
        pass

    # --- Format 2: Claude Code native JSONL (one JSON object per line) ---
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json_repair.loads(line)
        except Exception:
            continue
        if not isinstance(obj, dict) or obj.get("type") != "assistant":
            continue
        message = obj.get("message")
        if not isinstance(message, dict):
            continue
        content = message.get("content")
        if not isinstance(content, list):
            continue
        for item in content:
            if not isinstance(item, dict):
                continue
            if item.get("type") != "tool_use" or item.get("name") != "Skill":
                continue
            inp = item.get("input")
            if isinstance(inp, dict) and "skill" in inp:
                name = str(inp["skill"]).strip()
                if name:
                    invoked.add(name)

    return invoked


def extract_skill_call_counts(path: Path) -> "Counter[str]":
    """Parse a trajectory and return a Counter of skill_name -> number of calls (not deduplicated
    by skill name, but deduplicated by message ID to handle streaming chunks correctly).

    Mirrors extract_skill_invocations() format detection but counts rather than collects a set.
    """
    from collections import Counter

    raw = path.read_text(encoding="utf-8", errors="replace").strip()
    if not raw:
        return Counter()

    # --- Format 1: dataclaw single-JSON with "messages" list ---
    try:
        parsed = json_repair.loads(raw)
        if isinstance(parsed, dict) and isinstance(parsed.get("messages"), list):
            counts: Counter[str] = Counter()
            for msg in parsed["messages"]:
                if not isinstance(msg, dict):
                    continue
                for tu in msg.get("tool_uses") or []:
                    if not isinstance(tu, dict):
                        continue
                    if str(tu.get("tool", "")).strip() != "Skill":
                        continue
                    inp = tu.get("input")
                    if isinstance(inp, dict) and "skill" in inp:
                        name = str(inp["skill"]).strip()
                        if name:
                            counts[name] += 1
            return counts
    except Exception:
        pass

    # --- Format 2: Claude Code native JSONL (deduplicate by message ID, last chunk wins) ---
    msg_skill_counts: dict[str, "Counter[str]"] = {}
    _anon_counter = 0
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json_repair.loads(line)
        except Exception:
            continue
        if not isinstance(obj, dict) or obj.get("type") != "assistant" or obj.get("isSynthetic"):
            continue
        message = obj.get("message")
        if not isinstance(message, dict):
            continue
        content = message.get("content")
        if not isinstance(content, list):
            continue

        mid = message.get("id")
        if mid:
            key = mid
        else:
            _anon_counter += 1
            key = f"__anon_{_anon_counter}"

        skill_counter: Counter[str] = Counter()
        for item in content:
            if not isinstance(item, dict):
                continue
            if item.get("type") != "tool_use" or item.get("name") != "Skill":
                continue
            inp = item.get("input")
            if isinstance(inp, dict) and "skill" in inp:
                name = str(inp["skill"]).strip()
                if name:
                    skill_counter[name] += 1
        msg_skill_counts[key] = skill_counter  # last chunk wins

    total: Counter[str] = Counter()
    for sc in msg_skill_counts.values():
        total.update(sc)
    return total


def compute_efficiency_metrics(path: Path) -> dict:
    """Count steps, tool calls, skill calls, and token usage from a Claude Code JSONL trajectory.

    Token counts come from the `result` line's modelUsage (includes thinking tokens).
    Falls back to per-message usage sum if no result line is present.
    Step/tool/skill counts are based on unique assistant turns (deduplicated by message ID).

    Returns:
        num_steps       — unique assistant turns (unique message IDs)
        num_tools       — total tool_use items across all unique assistant turns
        num_skill_calls — Skill tool_use items (not deduplicated; num_tools superset)
        input_tokens    — inputTokens + cacheReadInputTokens + cacheCreationInputTokens
        output_tokens   — outputTokens including thinking tokens (from result.modelUsage)
    """
    _EMPTY = {
        "num_steps": 0, "num_tools": 0, "num_skill_calls": 0,
        "input_tokens": 0, "output_tokens": 0,
    }
    raw = path.read_text(encoding="utf-8", errors="replace").strip()
    if not raw:
        return _EMPTY

    # Only applicable to Claude Code native JSONL format
    first_line = next((l.strip() for l in raw.splitlines() if l.strip()), "")
    try:
        first_obj = json_repair.loads(first_line)
        if not (isinstance(first_obj, dict) and "type" in first_obj):
            return _EMPTY
    except Exception:
        return _EMPTY

    # Per-message data keyed by message ID (last streaming chunk wins — earlier chunks
    # are partial snapshots and may not yet contain the full tool_use list).
    # Layout: {key: {"tools": int, "skills": int, "usage": dict}}
    # Messages with an ID: key = message ID (overwrite → last chunk wins).
    # Messages without an ID: key = unique sentinel (each is its own turn).
    msg_data: dict[str, dict] = {}
    _anon_counter = 0
    # Accurate token counts from result.modelUsage (includes thinking)
    result_input_tokens: int | None = None
    result_output_tokens: int | None = None

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json_repair.loads(line)
        except Exception:
            continue
        if not isinstance(obj, dict):
            continue

        obj_type = obj.get("type")

        # result line: read cumulative modelUsage (includes thinking tokens)
        if obj_type == "result":
            model_usage = obj.get("modelUsage")
            if isinstance(model_usage, dict):
                inp = out = 0
                for model_stats in model_usage.values():
                    if not isinstance(model_stats, dict):
                        continue
                    inp += (model_stats.get("inputTokens") or 0)
                    inp += (model_stats.get("cacheReadInputTokens") or 0)
                    inp += (model_stats.get("cacheCreationInputTokens") or 0)
                    out += (model_stats.get("outputTokens") or 0)
                result_input_tokens = inp
                result_output_tokens = out
            continue

        if obj_type != "assistant" or obj.get("isSynthetic"):
            continue
        message = obj.get("message")
        if not isinstance(message, dict):
            continue

        mid = message.get("id")
        if mid:
            key = mid  # overwrite → last streaming chunk for this ID wins
        else:
            _anon_counter += 1
            key = f"__anon_{_anon_counter}"  # no-ID messages are always unique turns

        tools = skill_calls = 0
        content = message.get("content", [])
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "tool_use":
                    tools += 1
                    if item.get("name") == "Skill":
                        skill_calls += 1

        usage = message.get("usage") or {}
        msg_data[key] = {"tools": tools, "skills": skill_calls, "usage": usage}

    # Aggregate across all unique messages
    num_steps      = len(msg_data)
    num_tools      = sum(d["tools"]  for d in msg_data.values())
    num_skill_calls = sum(d["skills"] for d in msg_data.values())

    fb_input_tokens = fb_output_tokens = 0
    for d in msg_data.values():
        u = d["usage"]
        fb_input_tokens  += (u.get("input_tokens") or 0)
        fb_input_tokens  += (u.get("cache_creation_input_tokens") or 0)
        fb_input_tokens  += (u.get("cache_read_input_tokens") or 0)
        fb_output_tokens += (u.get("output_tokens") or 0)

    # Prefer result.modelUsage for accuracy; fall back to per-message sums
    input_tokens  = result_input_tokens  if result_input_tokens  is not None else fb_input_tokens
    output_tokens = result_output_tokens if result_output_tokens is not None else fb_output_tokens

    return {
        "num_steps": num_steps,
        "num_tools": num_tools,
        "num_skill_calls": num_skill_calls,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
    }


def find_generated_trajectory(trials_root: Path, task_id: str, trial_id: str | None = None) -> Path:
    """Latest or specified generated trial trajectory file."""
    if trial_id:
        agent_dir = trials_root / task_id / "generated" / trial_id / "agent"
        if not agent_dir.is_dir():
            raise FileNotFoundError(f"agent dir not found: {agent_dir}")
        traj = _find_trajectory_file(agent_dir)
        if traj is None:
            raise FileNotFoundError(f"no trajectory file in {agent_dir}")
        return traj
    pattern = f"{task_id}/generated/*/agent"
    cands: list[Path] = []
    for agent_dir in trials_root.glob(pattern):
        if not agent_dir.is_dir():
            continue
        traj = _find_trajectory_file(agent_dir)
        if traj is not None:
            cands.append(traj)
    cands.sort(key=lambda p: p.stat().st_mtime)
    if not cands:
        raise FileNotFoundError(
            f"no generated trajectory found for task_id={task_id}; expected under {trials_root / task_id / 'generated'}"
        )
    return cands[-1]
