#!/usr/bin/env python3
"""
Minimal CLI agent sandbox - SkillLearnBench style.
Tasks are two-level: tasks/<task-name>/<task-name>-N/ with instruction.md, environment/, tests/
Supports multiple agents (claude-code, gemini-code) - add in agents/__init__.py
"""
from __future__ import annotations

import argparse
import datetime
import importlib.util
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path


def _load_task_config(task_path: Path) -> dict:
    """Load task.toml for a query directory. Returns empty dict on missing/error."""
    toml_path = task_path / "task.toml"
    if not toml_path.exists():
        return {}
    try:
        if sys.version_info >= (3, 11):
            import tomllib
        else:
            import tomli as tomllib  # type: ignore[no-redef]
        return tomllib.loads(toml_path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _load_dotenv() -> None:
    """Load .env from SkillLearnBench root into os.environ (no extra deps)."""
    env_file = Path(__file__).parent.parent / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, _, v = line.partition("=")
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k and k not in os.environ:
                os.environ[k] = v


# Add SkillLearnBench root for agents package
sys.path.insert(0, str(Path(__file__).parent.parent))
from agents import get_agent, list_agents

TASKS_DIR          = Path(__file__).parent.parent / "tasks"
METHODS_DIR        = Path(__file__).parent.parent / "baselines"
TRIALS_DIR         = Path(__file__).parent.parent / "output" / "skill_generation_log"
SKILL_CONFIGS_DIR = Path(__file__).parent.parent / "output" / "skill_generation_results"


def list_tasks() -> list[str]:
    """List task IDs (folder names in tasks/ that contain at least one subtask dir)."""
    if not TASKS_DIR.exists():
        return []
    return sorted(
        d.name for d in TASKS_DIR.iterdir()
        if d.is_dir()
        and (d / (d.name + "-1") / "instruction.md").exists()
    )


# ── b3 Teacher-Student prompts ───────────────────────────────────────────────

_B3_SKILL_GEN_PROMPT = """\
You are given a task. Write 1-5 modular skill documents that capture the domain knowledge needed to complete this task.

For each skill, output a [SKILL]...[/SKILL] block with YAML frontmatter:
[SKILL]
---
name: <skill-name>  (lowercase, hyphenated, e.g. python-docx-template)
description: <when to use this skill and what it does — be specific>
---

... skill body in markdown ...
[/SKILL]

You may write multiple [SKILL] blocks if the task requires distinct areas of knowledge. Do not run any commands or edit files yet.

Task:
{instruction}
"""

_B3_SKILL_GEN_WITH_FEEDBACK_PROMPT = """\
The task failed. The Teacher gave you modification suggestions (no direct solution). Write a revised version of each skill document, addressing the suggestions.

Rules:
- Output one [SKILL]...[/SKILL] block per skill — keep them separate, do NOT merge into one
- Revise each skill independently based on the Teacher's feedback
- You may add new skill blocks if a new area of knowledge is needed
- Output ONLY [SKILL] blocks — no explanations, no plans, no other text

Each block must have YAML frontmatter:
[SKILL]
---
name: <skill-name>
description: <when to use this skill and what it does — be specific>
---

... revised skill body in markdown ...
[/SKILL]

Task:
{instruction}

## Teacher's modification suggestions:
{feedback}

## Previous rounds summary (for context):
{history_text}
"""

_B3_EXECUTE_PROMPT = """\
Execute the task. The following skill document(s) have been prepared for you:
{skill_paths}

Read them carefully and follow them to complete the task.
Do not output [SKILL] or [PLAN]; just perform the task.

Task:
{instruction}
"""

_B3_TEACHER_SYSTEM = """\
You are a Teacher. The Student is trying to complete a task by writing their own skill and executing it. They do NOT see the ground-truth skill. The task run just failed.

Your job: Give **modification suggestions only**. Do NOT provide the full solution, code, or the correct skill content. Only point out what is wrong or what to change (e.g. "use paragraph-level replacement, not run-level" or "handle split placeholders by searching in full paragraph text"). Keep suggestions concise and actionable.
"""

_B3_TEACHER_USER = """\
## Task instruction:
```
{task_instruction}
```

## Ground-truth skill (for your reference only; do not copy to the Student):
```
{skill_md}
```

## Student's current skill (what they wrote):
```
{student_skill}
```

## Failure context:
```
{failure_info}
```

Give modification suggestions only (no solution). Reply with a short list of suggestions.
"""


def _call_llm_anthropic(prompt: str, model: str, system: str | None) -> str:
    """LLM call via Anthropic API."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("[b3] Error: ANTHROPIC_API_KEY not set on host", file=sys.stderr)
        return ""
    try:
        from anthropic import Anthropic
    except ImportError:
        print("[b3] Error: 'anthropic' package not installed — run: pip install anthropic", file=sys.stderr)
        return ""
    client = Anthropic()
    kwargs: dict = dict(
        model=model,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    if system:
        kwargs["system"] = system
        kwargs["max_tokens"] = 2048
    r = client.messages.create(**kwargs)
    return (r.content[0].text if r.content else "").strip()


def _call_llm_gemini(prompt: str, model: str, system: str | None) -> str:
    """LLM call via Google GenAI API."""
    if not os.environ.get("GEMINI_API_KEY"):
        print("[b3] Error: GEMINI_API_KEY not set on host", file=sys.stderr)
        return ""
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("[b3] Error: 'google-genai' package not installed — run: pip install google-genai", file=sys.stderr)
        return ""
    client = genai.Client()
    config_kwargs: dict = {"max_output_tokens": 2048 if system else 4096}
    if system:
        config_kwargs["system_instruction"] = system
    r = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(**config_kwargs),
    )
    return (r.text or "").strip()


def _call_llm(prompt: str, model: str | None = None, system: str | None = None) -> str:
    """Direct LLM call on host (used by b3 teacher-student loop). Routes to Anthropic or Gemini based on model name."""
    resolved = model or "claude-sonnet-4-6"
    if resolved.startswith("gemini"):
        return _call_llm_gemini(prompt, resolved, system)
    return _call_llm_anthropic(prompt, resolved, system)


def _extract_tag(text: str, tag: str) -> str:
    """Extract content between [TAG]...[/TAG]; falls back to full text."""
    m = re.search(rf"\[{tag}\](.*?)\[/{tag}\]", text, re.DOTALL)
    return m.group(1).strip() if m else text.strip()


def _extract_skills(text: str) -> list[tuple[str, str]]:
    """Extract all [SKILL]...[/SKILL] blocks. Returns list of (name, content).
    Name is taken from YAML frontmatter 'name:' field; falls back to 'skill-{i}'."""
    blocks = re.findall(r"\[SKILL\](.*?)\[/SKILL\]", text, re.DOTALL)
    results = []
    for i, block in enumerate(blocks):
        content = block.strip()
        m = re.search(r"name:\s*(.+)", content)
        name = m.group(1).strip() if m else f"skill-{i + 1}"
        name = re.sub(r"[^a-zA-Z0-9_-]", "-", name).strip("-") or f"skill-{i + 1}"
        results.append((name, content))
    return results


def _read_ground_truth(task_path: Path) -> str:
    """Read ground-truth skill(s) from task/environment/skills/."""
    skills_dir = task_path / "environment" / "skills"
    if not skills_dir.exists():
        return ""
    parts = []
    for skill_md in sorted(skills_dir.rglob("SKILL.md")):
        parts.append(f"# {skill_md.parent.name}\n{skill_md.read_text(encoding='utf-8')}")
    return "\n\n---\n\n".join(parts)


def _get_task_workdir(task_path: Path) -> str:
    """Parse the task's Dockerfile to find the effective WORKDIR. Returns '/root' if not found."""
    dockerfile = task_path / "environment" / "Dockerfile"
    if not dockerfile.exists():
        return "/root"
    env_vars: dict[str, str] = {}
    last_workdir = "/root"
    for raw_line in dockerfile.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        # Collect ENV definitions for variable substitution
        if line.startswith("ENV "):
            parts = line[4:].strip().split("=", 1)
            if len(parts) == 2:
                env_vars[parts[0].strip()] = parts[1].strip()
        elif line.startswith("WORKDIR "):
            raw = line[8:].strip()
            # Substitute ${VAR} and $VAR references
            def _sub(m: re.Match) -> str:
                return env_vars.get(m.group(1) or m.group(2), m.group(0))
            resolved = re.sub(r"\$\{(\w+)\}|\$(\w+)", _sub, raw)
            last_workdir = resolved
    return last_workdir


def _run_agent_streaming(
        docker_cmd: list[str],
        *,
        max_steps: int,
        stop_event: threading.Event | None = None,
) -> tuple[int, str, str, int]:
    """Run docker exec command, counting tool_use steps from stream-json stdout.
    Terminates agent when max_steps reached or stop_event is set.
    Handles both Claude (tool_use nested in assistant) and Gemini (top-level tool_use) formats.
    Returns (returncode, stdout, stderr, steps_used).
    """
    proc = subprocess.Popen(
        docker_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout_lines: list[str] = []
    stderr_lines: list[str] = []
    steps_used = 0

    def _read_stderr() -> None:
        assert proc.stderr is not None
        for line in proc.stderr:
            stderr_lines.append(line)

    stderr_thread = threading.Thread(target=_read_stderr, daemon=True)
    stderr_thread.start()

    try:
        assert proc.stdout is not None
        for line in proc.stdout:
            stdout_lines.append(line)
            stripped = line.strip()
            if stripped:
                try:
                    event = json.loads(stripped)
                    t = event.get("type")
                    # Claude: tool_use nested inside assistant message content
                    if t == "assistant":
                        for content in event.get("message", {}).get("content", []):
                            if content.get("type") == "tool_use":
                                steps_used += 1
                    # Gemini: tool_use is a top-level event
                    elif t == "tool_use":
                        steps_used += 1
                except (json.JSONDecodeError, TypeError, KeyError):
                    pass
            if max_steps > 0 and steps_used >= max_steps:
                print(f"  [!] Max steps ({max_steps}) reached — terminating agent", flush=True)
                proc.terminate()
                break
            if stop_event is not None and stop_event.is_set():
                print(f"  [skills-only] Stop signal received — terminating agent", flush=True)
                proc.terminate()
                break
    except Exception:
        proc.kill()

    try:
        proc.wait(timeout=15)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()

    stderr_thread.join(timeout=5)
    return proc.returncode or 0, "".join(stdout_lines), "".join(stderr_lines), steps_used


def _poll_skills_done(
        container_name: str,
        stop_event: threading.Event,
        stabilize_secs: int = 30,
        skills_path: str = "/root/environment/skills",
) -> None:
    """Background thread: poll Docker container for SKILL.md files under skills_path.
    Sets stop_event once files appear and the count has been stable for stabilize_secs seconds.
    """
    last_count = 0
    stable_since: float | None = None
    while not stop_event.is_set():
        r = subprocess.run(
            ["docker", "exec", container_name, "find",
             skills_path, "-name", "SKILL.md"],
            capture_output=True, text=True,
        )
        paths = [p for p in r.stdout.strip().splitlines() if p.strip()]
        count = len(paths)
        if count > 0:
            if count != last_count:
                last_count = count
                stable_since = time.monotonic()
                print(f"  [skills-only] {count} SKILL.md file(s) found, waiting for stability...", flush=True)
            elif stable_since is not None and (time.monotonic() - stable_since) >= stabilize_secs:
                print(f"  [skills-only] {count} SKILL.md file(s) stable — signalling agent stop", flush=True)
                stop_event.set()
                return
        time.sleep(3)


def _run_teacher_student_loop(
        *,
        task_path: Path,
        container_name: str,
        trial_path: Path,
        agent: dict,
        model_name: str,
        task_instruction: str,
        task_workdir: str = "/root",
        max_rounds: int,
        max_steps: int = 100,
) -> tuple[bool, int, int, int, str, str, int]:
    """
    Multi-round teacher-student loop (runs outside container, directs agent inside).
    Returns (passed, rounds_used, last_agent_exit, last_verifier_exit, agent_stdout, agent_stderr, total_steps).
    """
    ground_truth = _read_ground_truth(task_path)
    history: list[dict] = []
    feedback = ""
    agent_exit = verifier_exit = 0
    agent_stdout = agent_stderr = ""
    total_steps = 0

    # Compute allowed tools once (default_tools minus task-level disallowed_tools)
    _b3_default_tools: list[str] = agent.get("default_tools", [])
    _b3_disallowed: set[str] = set()
    _b3_task_toml = task_path / "task.toml"
    if _b3_default_tools and _b3_task_toml.exists():
        try:
            import tomllib as _tomllib
        except ImportError:
            import tomli as _tomllib  # type: ignore[no-redef]
        try:
            with open(_b3_task_toml, "rb") as _tf:
                _task_cfg = _tomllib.load(_tf)
            _b3_disallowed = set(_task_cfg.get("agent", {}).get("disallowed_tools", []))
        except Exception:
            pass
    _b3_allowed_tools = " ".join(t for t in _b3_default_tools if t not in _b3_disallowed)

    for round_num in range(1, max_rounds + 1):
        print(f"  [b3] Round {round_num}/{max_rounds} — generating student skill...")

        # Student generates skill via direct LLM call (outside container)
        if round_num == 1:
            prompt = _B3_SKILL_GEN_PROMPT.format(instruction=task_instruction)
        else:
            history_text = "\n".join(
                f"Round {h['round']}: {h['outcome']}" for h in history
            )
            prompt = _B3_SKILL_GEN_WITH_FEEDBACK_PROMPT.format(
                instruction=task_instruction,
                feedback=feedback,
                history_text=history_text,
            )

        raw = _call_llm(prompt, model=model_name)
        skills = _extract_skills(raw)
        if not skills:
            print(f"  [b3] Warning: no [SKILL]...[/SKILL] blocks found in LLM output — storing raw as skill-1",
                  file=sys.stderr)
            skills = [("skill-1", raw.strip())]

        # Docker cp each skill to container as run{n}_{name}/SKILL.md
        # (b2-style naming; artifact-copyable via --artifact /root/environment/skills)
        skills_base = f"{task_workdir}/environment/skills"
        skill_paths_list = []
        with tempfile.TemporaryDirectory() as tmpdir:
            for skill_name, skill_content in skills:
                folder = f"run{round_num}_{skill_name}"
                skill_dir = Path(tmpdir) / folder
                skill_dir.mkdir()
                (skill_dir / "SKILL.md").write_text(skill_content, encoding="utf-8")
                subprocess.run(
                    ["docker", "exec", container_name, "mkdir", "-p", f"{skills_base}/{folder}"],
                    capture_output=True,
                )
                subprocess.run(
                    ["docker", "cp", str(skill_dir / "SKILL.md"),
                     f"{container_name}:{skills_base}/{folder}/SKILL.md"],
                    capture_output=True,
                )
                skill_paths_list.append(f"  - environment/skills/{folder}/SKILL.md")
                print(f"  [b3]   skill → {folder}/SKILL.md")

        # Build execute instruction and inject into container
        execute_instruction = _B3_EXECUTE_PROMPT.format(
            instruction=task_instruction,
            skill_paths="\n".join(skill_paths_list),
        )
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(execute_instruction)
            inst_path = f.name
        try:
            subprocess.run(
                ["docker", "cp", inst_path, f"{container_name}:/tmp/instruction.txt"],
                check=True, capture_output=True,
            )
        finally:
            Path(inst_path).unlink(missing_ok=True)

        # Run agent inside container
        run_cmd = (
            agent["run"]
            .replace("{instruction_file}", "/tmp/instruction.txt")
            .replace("{model}", model_name)
            .replace("{max_steps}", str(max_steps))
            .replace("{allowed_tools}", _b3_allowed_tools)
            .replace("{extra_flags}", "")
        )
        traj_env = agent.get("trajectory_env", {})
        env_prefix = " ".join(f"{k}={v}" for k, v in traj_env.items() if v)
        if env_prefix:
            run_cmd = f"{env_prefix} {run_cmd}"
        tee_path = agent.get("trajectory_tee")
        if tee_path:
            tee_round = tee_path.replace(".txt", f"_r{round_num}.txt")
            run_cmd = f"({run_cmd}) 2>&1 | tee {tee_round}"

        print(f"  [b3] Round {round_num}/{max_rounds} — running agent...")
        agent_exit, agent_stdout, agent_stderr, round_steps = _run_agent_streaming(
            ["docker", "exec", container_name, "sh", "-c", run_cmd],
            max_steps=max_steps,
        )
        total_steps += round_steps
        print(f"  [b3] Round {round_num} steps used: {round_steps} (total: {total_steps})")

        # Run verifier
        verifier = subprocess.run(
            ["docker", "exec", container_name, "bash", "/tests/test.sh"],
            capture_output=True, text=True, timeout=600,
        )
        verifier_exit = verifier.returncode

        # Read reward
        reward_file = trial_path / "verifier" / "reward.txt"
        reward = 0
        if reward_file.exists():
            try:
                reward = int(reward_file.read_text(encoding="utf-8").strip())
            except ValueError:
                pass

        passed = reward == 1
        history.append({"round": round_num, "outcome": "PASS" if passed else "FAIL", "skills": skills})
        print(f"  [b3] Round {round_num} result: {'PASS' if passed else 'FAIL'}")

        if passed:
            return True, round_num, agent_exit, verifier_exit, agent_stdout, agent_stderr, total_steps

        # Get teacher suggestions (if more rounds remain)
        if round_num < max_rounds:
            print(f"  [b3] Round {round_num} — getting teacher suggestions...")
            student_skills_combined = "\n\n---\n\n".join(
                f"### {name}\n{content}" for name, content in skills
            )
            teacher_user = _B3_TEACHER_USER.format(
                task_instruction=task_instruction,
                skill_md=ground_truth,
                student_skill=student_skills_combined,
                failure_info=(verifier.stdout + verifier.stderr)[:2000],
            )
            feedback = _call_llm(teacher_user, model=model_name, system=_B3_TEACHER_SYSTEM)

            teacher_dir = trial_path / "teacher"
            teacher_dir.mkdir(exist_ok=True)
            (teacher_dir / f"round{round_num}_prompt.txt").write_text(teacher_user, encoding="utf-8")
            (teacher_dir / f"round{round_num}_feedback.txt").write_text(feedback, encoding="utf-8")
            # Update history JSON each time so it survives an early return True on the next round
            history_records = [
                {"round": h["round"], "outcome": h["outcome"],
                 "skills": [name for name, _ in h["skills"]]}
                for h in history
            ]
            (teacher_dir / "b3_history.json").write_text(
                json.dumps(history_records, indent=2), encoding="utf-8"
            )

    return False, max_rounds, agent_exit, verifier_exit, agent_stdout, agent_stderr, total_steps


# ── Method config + plugin loading ───────────────────────────────────────────

def _load_method_config(method: str) -> dict:
    """Load the optional method.toml from a method directory.

    Returns an empty dict if the file is absent or fails to parse.
    Recognised keys (all optional):
      skills_only_mode (str) – "interrupt" | "skip_verifier" | "full"  (default "full")
          "interrupt"     : poll container for SKILL.md; interrupt agent early; skip verifier.
          "skip_verifier" : let agent run to completion; skip verifier.
          "full"          : run agent to completion; run verifier (standard behaviour).
      max_rounds (int)       – number of rounds for multi-round methods (absent for single-pass).
          Presence triggers substitution of {max_rounds} in method.md.
          Also used by generate_skills.py as the default max_rounds for this method.
    """
    cfg_file = METHODS_DIR / method / "method.toml"
    if not cfg_file.exists():
        return {}
    try:
        try:
            import tomllib
        except ImportError:
            import tomli as tomllib  # type: ignore[no-redef]
        with open(cfg_file, "rb") as fh:
            return tomllib.load(fh)
    except Exception:
        return {}


def _load_method_plugin(method: str):
    """Dynamically load method.py from a method directory.

    Returns the loaded module, or None if the file is absent or fails to load.
    A valid plugin must export a run() callable with the signature:
        run(*, container_name, task_path, trial_path, agent, model_name,
            instruction, task_workdir, max_rounds, max_steps)
        -> tuple[bool, int, str, str, int | None]
           (passed, steps_used, agent_stdout, agent_stderr, rounds_used)
    Plugin methods handle their own agent execution and verifier logic (steps 4+5).
    The runner still owns container setup (steps 1-3) and artifact copy (step 6).
    """
    plugin_file = METHODS_DIR / method / "method.py"
    if not plugin_file.exists():
        return None
    spec = importlib.util.spec_from_file_location(f"_method_plugin_{method}", plugin_file)
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def run_task(task_id: str, *, agent_id: str = "codex", model: str | None = None, record: bool = True,
             artifacts: list[str] | None = None, method: str | None = None, max_rounds: int = 5,
             max_steps: int = 100, skills_only: bool = False,
             prebuilt_image_tag: str | None = None,
             prebuilt_has_agent: bool = False,
             extra_instructions: list[str] | None = None) -> tuple[int, dict]:
    """Build Docker image, run container, exec agent then verifier. Return (returncode, result_dict)."""
    task_path = TASKS_DIR / task_id / (task_id + "-1")
    if not task_path.exists():
        print(f"Task not found: {task_id}", file=sys.stderr)
        return 2, {}
    if not (task_path / "instruction.md").exists():
        print(f"Task '{task_id}' is missing instruction.md in subtask dir: {task_path}", file=sys.stderr)
        return 2, {}

    agent = get_agent(agent_id)
    if not agent:
        print(f"Unknown agent: {agent_id}. Available: {', '.join(list_agents())}", file=sys.stderr)
        return 2, {}

    # Check required env vars
    for env_var in agent["env"]:
        if not os.environ.get(env_var):
            print(f"Set {env_var} (or add to SkillLearnBench/.env) to run agent {agent_id}", file=sys.stderr)
            return 2, {}

    # Check task-required env vars (declared in task.toml [environment] required_env)
    task_cfg = _load_task_config(task_path)
    for env_var in task_cfg.get("environment", {}).get("required_env", []):
        if not os.environ.get(env_var):
            print(f"Task {task_id} requires ${env_var}. "
                  f"Add it to SkillLearnBench/.env (see .env.example).", file=sys.stderr)
            return 2, {}

    # Validate method if provided; load config and plugin.
    # method_text : injected into the agent instruction (None for plugin methods).
    # method_cfg  : parsed method.toml (empty dict if absent).
    # method_plugin: loaded method.py module (None if absent).
    method_text = None
    method_cfg: dict = {}
    method_plugin = None
    if method:
        method_plugin = _load_method_plugin(method)
        if method_plugin is not None:
            # Plugin methods build their own instructions; no static method.md injection.
            pass
        else:
            method_file = METHODS_DIR / method / "method.md"
            if not method_file.exists():
                print(f"Method not found: {method} (expected {method_file})", file=sys.stderr)
                return 2, {}
            method_text = method_file.read_text(encoding="utf-8").strip()
            method_cfg = _load_method_config(method)
            # If max_rounds is declared, substitute {max_rounds} in method.md.
            # Presence of max_rounds is the signal that this method is round-based.
            if "max_rounds" in method_cfg:
                effective_rounds = max(max_rounds, 2)
                method_text = method_text.replace("{max_rounds}", str(effective_rounds))

    env_dir = task_path / "environment"
    dockerfile = env_dir / "Dockerfile"
    if not dockerfile.exists():
        print(f"No Dockerfile: {dockerfile}", file=sys.stderr)
        return 2, {}

    model_name = model if model else agent.get("default_model", "")

    # task_path is always a subtask dir (tasks/<task>/<task>-1), so parent.name is the task name.
    task_dir_name = task_path.parent.name

    # config = "<method>-<model>" for Phase 1; fallback to model name alone
    if method:
        config = f"{method}-{model_name}"
        safe_id = f"{method}-{task_dir_name}"
    else:
        config = model_name or "unknown"
        safe_id = task_id.replace("/", "-").replace("\\", "-")

    ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    trial_id = f"{ts}_{secrets.token_hex(3)}"
    # Phase 1 layout: evaluation_log/<config>/<task>/<task>-<ts_hash>/
    # (_sv_find_latest_skills scans one level below <task> for trial dirs)
    trial_path = TRIALS_DIR / config / task_dir_name / f"{task_dir_name}-{trial_id}"
    trial_path.mkdir(parents=True, exist_ok=True)
    (trial_path / "agent").mkdir(exist_ok=True)
    (trial_path / "verifier").mkdir(exist_ok=True)

    # Image tag: use prebuilt if provided, else build fresh
    if prebuilt_image_tag is not None:
        image_tag = prebuilt_image_tag
    else:
        image_tag = f"test_agent_{safe_id}:latest"
    container_name = f"test_agent_{safe_id}-{trial_id}".replace(".", "-").replace("_", "-")
    task_workdir = _get_task_workdir(task_path)

    # Build (skip if prebuilt image provided)
    build_root: Path | None = None
    if prebuilt_image_tag is None:
        print(f"[1/5] Building {image_tag}...")
        # Create a temp build context that excludes oracle skills so they are
        # never baked into the image — the agent must generate skills from scratch.
        build_root = Path(tempfile.mkdtemp(prefix="skill_gen_build_"))
        build_env = build_root / "environment"
        shutil.copytree(env_dir, build_env, ignore=shutil.ignore_patterns("skills"))
        skills_stub = build_env / "skills"
        skills_stub.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(
            ["docker", "build", "-t", image_tag, str(build_env)],
            capture_output=True,
            text=True,
        )
        shutil.rmtree(build_root, ignore_errors=True)
        build_root = None
        if r.returncode != 0:
            print(r.stderr or r.stdout, file=sys.stderr)
            return 1, {}
    else:
        print(f"[1/5] Using prebuilt image: {image_tag}")

    # Run container (detached, with /logs and /tests mounts)
    print(f"[2/5] Starting container...")
    subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)
    # Pass env vars explicitly so Docker gets the values
    env_args = []
    for env_var in agent["env"]:
        val = os.environ.get(env_var)
        if val:
            env_args.extend(["-e", f"{env_var}={val}"])
    # Pass task-required env vars into the container.
    for env_var in task_cfg.get("environment", {}).get("required_env", []):
        val = os.environ.get(env_var)
        if val:
            env_args.extend(["-e", f"{env_var}={val}"])
    r = subprocess.run(
        [
            "docker", "run", "-d",
            "--name", container_name,
            "-v", f"{task_path / 'tests'}:/tests:ro",
            "-v", f"{trial_path}:/logs",
            *env_args,
            image_tag,
            "sleep", "3600",
        ],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        print(r.stderr or r.stdout, file=sys.stderr)
        return 1, {}

    try:
        # Inject method skills into container if inject/ dir exists
        if method:
            inject_dir = METHODS_DIR / method / "inject"
            if inject_dir.exists():
                skill_dest = agent.get("skill_dir", "/root/.claude/skills")
                subprocess.run(
                    ["docker", "exec", container_name, "mkdir", "-p", skill_dest],
                    capture_output=True,
                )
                for skill_dir in sorted(inject_dir.iterdir()):
                    if skill_dir.is_dir():
                        subprocess.run(
                            ["docker", "cp", str(skill_dir), f"{container_name}:{skill_dest}/"],
                            capture_output=True,
                        )
                        print(f"[*] Injected skill: {skill_dir.name} → {skill_dest}/")

        # Install agent (skip if pre-baked into image)
        if not prebuilt_has_agent:
            print(f"[3/5] Installing agent ({agent_id})...")
            runtime_deps = agent.get("runtime_deps")
            if runtime_deps:
                deps_r = subprocess.run(
                    ["docker", "exec", container_name, "sh", "-c", runtime_deps],
                    capture_output=True, text=True, timeout=600,
                )
                if deps_r.returncode != 0:
                    print(deps_r.stderr or deps_r.stdout, file=sys.stderr)
                    return 1, {}
            install_r = subprocess.run(
                ["docker", "exec", container_name, "sh", "-c", agent["install"]],
                capture_output=True,
                text=True,
                timeout=600,
            )
            if install_r.returncode != 0:
                print(install_r.stderr or install_r.stdout, file=sys.stderr)
                return 1, {}
        else:
            print(f"[3/5] Agent pre-installed in image ({agent_id})")

        # Agent-specific setup (e.g. Codex needs auth.json)
        setup = agent.get("setup")
        traj_env = agent.get("trajectory_env", {})
        codex_home = traj_env.get("CODEX_HOME", "/root/.codex")
        if setup == "auth_json":
            auth_data = {env_var: os.environ[env_var] for env_var in agent["env"]}
            with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
                json.dump(auth_data, f)
                auth_path = f.name
            try:
                subprocess.run(
                    ["docker", "exec", container_name, "mkdir", "-p", codex_home],
                    check=True,
                    capture_output=True,
                )
                subprocess.run(
                    ["docker", "cp", auth_path, f"{container_name}:{codex_home}/auth.json"],
                    check=True,
                    capture_output=True,
                )
            finally:
                Path(auth_path).unlink(missing_ok=True)
        elif isinstance(setup, str) and setup:
            subprocess.run(
                ["docker", "exec", container_name, "sh", "-c", setup],
                check=True,
                capture_output=True,
                timeout=600,
            )

        # Read task instruction (used by both normal path and b3)
        instruction = (task_path / "instruction.md").read_text(encoding="utf-8").strip()

        # Multi-query: append sibling subtask configs so the agent can generate
        # skills that generalise across the task family, not just the target subtask.
        if extra_instructions:
            extras_block = "\n\n".join(
                f"### Variant {i + 2}:\n{instr}"
                for i, instr in enumerate(extra_instructions)
            )
            instruction = (
                instruction
                + "\n\n---\n\n"
                "The following are additional configs of the same task type. "
                "Use them to understand the full scope of domain knowledge needed "
                "when generating skills.\n\n"
                + extras_block
            )

        verifier_timeout = 600

        # ── Step 4+5: Run agent + optional verifier ───────────────────────────
        agent_exit = verifier_exit = 0
        agent_stdout = agent_stderr = ""
        rounds_used = None
        reward = 0

        if method_plugin is not None:
            # Plugin method: delegate steps 4+5 entirely to the plugin.
            # The plugin owns instruction injection, agent execution, and verifier.
            print(f"[4/5] Running agent ({agent_id}) — plugin ({method})...")
            passed, steps_used, agent_stdout, agent_stderr, rounds_used = method_plugin.run(
                container_name=container_name,
                task_path=task_path,
                trial_path=trial_path,
                agent=agent,
                model_name=model_name,
                instruction=instruction,
                task_workdir=task_workdir,
                max_rounds=max_rounds,
                max_steps=max_steps,
            )
            reward = 1 if passed else 0
        else:
            # Standard single-pass: append method prompt → run agent → optionally run verifier.
            if method_text:
                instruction = instruction + "\n\n---\n\n" + method_text
            with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
                f.write(instruction)
                inst_path = f.name
            try:
                subprocess.run(
                    ["docker", "cp", inst_path, f"{container_name}:/tmp/instruction.txt"],
                    check=True,
                    capture_output=True,
                )
            finally:
                Path(inst_path).unlink(missing_ok=True)

            # Compute allowed tools: default_tools minus any task-level disallowed_tools
            # declared in task.toml [agent] section. Default (no override): full list.
            _default_tools: list[str] = agent.get("default_tools", [])
            _disallowed: set[str] = set()
            _task_toml = task_path / "task.toml"
            if _default_tools and _task_toml.exists():
                try:
                    import tomllib as _tomllib
                except ImportError:
                    import tomli as _tomllib  # type: ignore[no-redef]
                try:
                    with open(_task_toml, "rb") as _tf:
                        _task_cfg = _tomllib.load(_tf)
                    _disallowed = set(_task_cfg.get("agent", {}).get("disallowed_tools", []))
                except Exception:
                    pass
            _allowed_tools = " ".join(t for t in _default_tools if t not in _disallowed)

            run_cmd = (
                agent["run"]
                .replace("{instruction_file}", "/tmp/instruction.txt")
                .replace("{model}", model_name)
                .replace("{max_steps}", str(max_steps))
                .replace("{allowed_tools}", _allowed_tools)
                .replace("{extra_flags}", "")
            )
            tee_path = agent.get("trajectory_tee")
            _traj_env = agent.get("trajectory_env", {})
            env_prefix = " ".join(f"{k}={v}" for k, v in _traj_env.items() if v)
            if env_prefix:
                run_cmd = f"{env_prefix} {run_cmd}"
            if tee_path:
                run_cmd = f"({run_cmd}) 2>&1 | tee {tee_path}"
            # skills_only_mode from method.toml drives termination behaviour:
            #   "interrupt"     → interrupt agent early once SKILL.md files appear
            #   "skip_verifier" → let agent finish, but skip the verifier
            #   "full" (default)→ run agent + verifier normally
            _solo_mode = method_cfg.get("skills_only_mode", "full")
            skills_only_active = skills_only and _solo_mode == "interrupt"
            skip_verifier_only = skills_only and _solo_mode == "skip_verifier"
            stop_event: threading.Event | None = None
            poll_thread: threading.Thread | None = None
            if skills_only_active:
                stop_event = threading.Event()
                poll_thread = threading.Thread(
                    target=_poll_skills_done,
                    args=(container_name, stop_event),
                    kwargs={"skills_path": f"{task_workdir}/environment/skills"},
                    daemon=True,
                )
                poll_thread.start()
                print(f"[4/5] Running agent ({agent_id}) [skills-only mode]...")
            elif skip_verifier_only:
                print(f"[4/5] Running agent ({agent_id}) [skills-only: full run, verifier will be skipped]...")
            else:
                print(f"[4/5] Running agent ({agent_id})...")

            agent_exit, agent_stdout, agent_stderr, steps_used = _run_agent_streaming(
                ["docker", "exec", container_name, "sh", "-c", run_cmd],
                max_steps=max_steps,
                stop_event=stop_event,
            )
            print(f"  Steps used: {steps_used}")

            # Clean up poll thread
            if poll_thread is not None:
                stop_event.set()  # type: ignore[union-attr]
                poll_thread.join(timeout=5)

            # Remove auth.json from trial dir (CODEX_HOME may be /logs/agent = trial_path/agent)
            if setup == "auth_json" and codex_home.startswith("/logs"):
                subprocess.run(
                    ["docker", "exec", container_name, "rm", "-f", f"{codex_home}/auth.json"],
                    capture_output=True,
                )

            if skills_only_active or skip_verifier_only:
                print(f"[5/5] Verifier skipped (skills-only mode)")
                passed = False
            else:
                # Run verifier
                print(f"[5/5] Running verifier...")
                verifier = subprocess.run(
                    ["docker", "exec", container_name, "bash", "/tests/test.sh"],
                    capture_output=True,
                    text=True,
                    timeout=verifier_timeout,
                )
                verifier_exit = verifier.returncode

                # Read reward
                reward_file = trial_path / "verifier" / "reward.txt"
                if reward_file.exists():
                    try:
                        reward = int(reward_file.read_text(encoding="utf-8").strip())
                    except ValueError:
                        pass
                passed = reward == 1

        # Copy artifacts from container (equivalent to harbor --artifact)
        if artifacts:
            artifacts_dir = trial_path / "artifacts"
            artifacts_dir.mkdir(exist_ok=True)
            for artifact_path in artifacts:
                # Remap /root/... paths to the task's actual WORKDIR if they differ
                effective_path = artifact_path
                if task_workdir != "/root" and artifact_path.startswith("/root/"):
                    effective_path = task_workdir + artifact_path[len("/root"):]
                print(f"[*] Copying artifact: {effective_path}")
                subprocess.run(
                    ["docker", "cp", f"{container_name}:{effective_path}", str(artifacts_dir)],
                    capture_output=True,
                )
            # Check SKILL.md files for required YAML frontmatter
            for skill_md in sorted(artifacts_dir.rglob("SKILL.md")):
                if not skill_md.read_text(encoding="utf-8", errors="ignore").startswith("---"):
                    rel = skill_md.relative_to(artifacts_dir)
                    print(f"  [!] {rel}: missing YAML frontmatter — regenerate this skill")

        # Print verifier summary from ctrf.json
        if method_plugin is not None:
            print(f"\n[5/5] Verifier summary (final round):")
        ctrf_file = trial_path / "verifier" / "ctrf.json"
        if ctrf_file.exists():
            try:
                ctrf = json.loads(ctrf_file.read_text(encoding="utf-8"))
                summary = ctrf["results"]["summary"]
                n_pass = summary["passed"]
                n_total = summary["tests"]
                print(f"\nVerifier: {n_pass}/{n_total} tests passed", end="")
                print(f"  ({'PASS' if passed else 'FAIL'})")
                for t in ctrf["results"]["tests"]:
                    icon = "✓" if t["status"] == "passed" else "✗"
                    name = t["name"].split("::")[-1]
                    print(f"  {icon} {name}", end="")
                    if t["status"] != "passed" and t.get("trace"):
                        for line in t["trace"].splitlines():
                            if line.startswith("E "):
                                print(f"\n      {line.strip()}", end="")
                                break
                    print()
            except Exception:
                print("PASS" if passed else "FAIL")
        else:
            print("PASS" if passed else "FAIL")

        # Build result dict (always, for return value and optional recording)
        result = {
            "task_id": task_id,
            "method": method,
            "trial_name": f"{task_dir_name}-{trial_id}",
            "agent": agent_id,
            "model": model_name,
            # True only for non-plugin methods that have a non-"full" skills_only_mode.
            # Plugin methods (e.g. b3) own their own verifier logic and never set this flag.
            "skills_only": (
                skills_only
                and method_plugin is None
                and method_cfg.get("skills_only_mode", "full") != "full"
            ),
            "passed": passed,
            "reward": reward,
            "rounds_used": rounds_used,
            "steps_used": steps_used,
            "agent_exit": agent_exit,
            "verifier_exit": verifier_exit,
            "agent_stdout": agent_stdout[:2000],
            "agent_stderr": agent_stderr[:1000],
        }
        # Record results (Harbor style: trials/<trial>/)
        if record:
            (trial_path / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
            print(f"Trial: {trial_path}")
        return (0 if passed else 1), result
    finally:
        subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)


def main() -> int:
    _load_dotenv()
    parser = argparse.ArgumentParser(description="Minimal agent sandbox CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    list_p = sub.add_parser("list", help="List tasks")
    list_p.set_defaults(cmd="list")

    agents_p = sub.add_parser("agents", help="List available agents")
    agents_p.set_defaults(cmd="agents")

    run_p = sub.add_parser("run", help="Run task with agent + verifier")
    run_p.add_argument("task_id", help="Task ID (folder name)")
    run_p.add_argument("-a", "--agent", default="codex", help="Agent ID (default: codex)")
    run_p.add_argument("-m", "--model", help="Model name (e.g. gpt-5.2-codex, claude-sonnet-4-5)")
    run_p.add_argument("--method", "-M", metavar="METHOD_ID",
                       help="Method from baselines/ dir to inject into instruction (e.g. b1-self-generated)")
    run_p.add_argument("--artifact", action="append", dest="artifacts", metavar="CONTAINER_PATH",
                       help="Container path to copy out after agent runs (repeatable). E.g. /root/.claude/skills")
    run_p.add_argument("--max-rounds", type=int, default=3, metavar="N",
                       help="Max rounds for b3-teacher-guided method (default: 3)")
    run_p.add_argument("--max-steps", type=int, default=100, metavar="N",
                       help="Max tool-use steps per agent run (default: 100; 0 = unlimited)")
    run_p.add_argument("--skills-only", action="store_true",
                       help="Skill-generation mode: b1/b4 interrupt agent early + skip verifier; "
                            "b2 runs agent fully + skip verifier; b3 unaffected (verifier feeds teacher).")
    run_p.add_argument("--no-record", action="store_true", help="Skip writing results")
    run_p.set_defaults(cmd="run")

    args = parser.parse_args()

    if args.cmd == "list":
        tasks = list_tasks()
        for t in tasks:
            print(t)
        return 0

    if args.cmd == "agents":
        for aid in list_agents():
            a = get_agent(aid)
            print(f"  {aid}: {a['name']}")
        return 0

    if args.cmd == "run":
        rc, _ = run_task(
            args.task_id,
            agent_id=args.agent,
            model=args.model,
            record=not args.no_record,
            artifacts=args.artifacts,
            method=args.method,
            max_rounds=args.max_rounds,
            max_steps=args.max_steps,
            skills_only=args.skills_only,
        )
        return rc

    return 0


if __name__ == "__main__":
    sys.exit(main())
