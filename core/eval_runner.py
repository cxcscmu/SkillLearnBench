#!/usr/bin/env python3
"""
Minimal CLI agent sandbox - SkillsBench/Harbor style.
Tasks are folders: tasks/<task-id>/ with instruction.md, environment/, tests/
Supports multiple agents (codex, claude-code) - add in agents/__init__.py
"""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime
import json
import json_repair
import os
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
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


# Use the unified agents registry at SkillLearnBench/agents/.
sys.path.insert(0, str(Path(__file__).parent.parent))
from agents import get_agent, list_agents

TASKS_DIR          = Path(__file__).parent.parent / "tasks"
SKILL_CONFIGS_DIR = Path(__file__).parent.parent / "output" / "skill_generation_results"
TRIALS_DIR         = Path(__file__).parent.parent / "output" / "evaluation_log"


def list_tasks(tasks_dir: Path = TASKS_DIR) -> list[str]:
    """List all query IDs in the two-level task structure (tasks/<task>/<task>-N/).
    Returns paths like 'court-form-filling/court-form-filling-1'."""
    if not tasks_dir.exists():
        return []
    result: list[str] = []
    for task_dir in sorted(tasks_dir.iterdir()):
        if not task_dir.is_dir():
            continue
        for query_dir in sorted(task_dir.iterdir()):
            if (query_dir.is_dir()
                    and (query_dir / "instruction.md").exists()
                    and (query_dir / "environment" / "Dockerfile").exists()
                    and (query_dir / "tests").exists()):
                result.append(f"{task_dir.name}/{query_dir.name}")
    return result


def _expand_subtask_range(task_id: str, task_root: Path, start: int, end: int) -> list[str]:
    """Expand task_id into query IDs for the given index range.

    Example:
      task_id = "court-form-filling", start=1, end=5
      → ["court-form-filling/court-form-filling-1",
         "court-form-filling/court-form-filling-2", ...]
         (only those query dirs that actually exist)
    """
    task_path = task_root / task_id
    task_name = Path(task_id).name
    result = []
    for i in range(start, end + 1):
        sub_name = f"{task_name}-{i}"
        sub_path = task_path / sub_name
        if (sub_path / "instruction.md").exists():
            result.append(f"{task_id}/{sub_name}")
    return result


def _mk_trial_name(task_id: str, skill_config: str, trial_id: str | None = None) -> tuple[str, str]:
    if trial_id is None:
        ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        trial_id = f"{ts}_{secrets.token_hex(3)}"
    return trial_id, trial_id


def _trial_path(task_id: str, skill_config: str, trial_id: str, trials_dir: Path = TRIALS_DIR) -> Path:
    """Canonical trial layout: evaluation_log/<config>/<task>/<subtask>/<ts_hash>/
    task_id is always 'task/task-N', e.g. 'court-form-filling/court-form-filling-1'
    → evaluation_log/human_authored/court-form-filling/court-form-filling-1/20260407190655_a3f2c6
    """
    return trials_dir / skill_config / Path(task_id) / trial_id


def _copy_skills_to_dest(src: Path, dest_skills_dir: Path) -> bool:
    """
    Populate dest_skills_dir with skills from a source folder.

    Supported source layouts:
    1) Skill directories containing SKILL.md
    2) Flat markdown files (*.md) -> each file becomes <stem>/SKILL.md
    """
    if not src.exists() or not src.is_dir():
        return False

    if dest_skills_dir.exists():
        shutil.rmtree(dest_skills_dir)
    dest_skills_dir.mkdir(parents=True, exist_ok=True)

    # Case 1: directory-based skills
    dir_skills = [d for d in src.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]
    if dir_skills:
        for d in dir_skills:
            shutil.copytree(d, dest_skills_dir / d.name)
        return True

    # Case 2: root SKILL.md
    root_skill = src / "SKILL.md"
    if root_skill.exists():
        one = dest_skills_dir / src.name
        one.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root_skill, one / "SKILL.md")
        return True

    # Case 3: flat markdown collection
    md_files = sorted(p for p in src.glob("*.md") if p.is_file())
    if md_files:
        for md in md_files:
            name = md.stem.replace("_", "-")
            out = dest_skills_dir / name
            out.mkdir(parents=True, exist_ok=True)
            shutil.copy2(md, out / "SKILL.md")
        return True

    return False


def _prepare_build_env(env_dir: Path, skill_mode: str, skill_source_dir: Path | None) -> Path:
    """Create a temporary build context and materialize environment/skills for mode.

    Oracle skills from env_dir/skills/ are never copied into the build context —
    the skills directory is always initialised empty and then populated from
    skill_source_dir according to skill_mode.  This prevents oracle skill leakage
    into no_skill or generated containers even if rmtree were to fail silently.
    """
    tmp_root = Path(tempfile.mkdtemp(prefix="evaluation_env_"))
    build_env = tmp_root / "environment"
    # Copy everything except the skills directory so oracle skills never enter
    # the build context inadvertently.
    shutil.copytree(env_dir, build_env, ignore=shutil.ignore_patterns("skills"))

    target_skills = build_env / "skills"
    target_skills.mkdir(parents=True, exist_ok=True)

    if skill_mode == "no_skill":
        # Leave skills dir empty — no skills for this config.
        return build_env

    if skill_source_dir is not None:
        ok = _copy_skills_to_dest(skill_source_dir, target_skills)
        if not ok:
            raise RuntimeError(f"skill source has no usable content: {skill_source_dir}")

    return build_env


def _resolve_skill_source(task_path: Path, skill_config: str) -> Path | None:
    """Resolve skill source dir from output/skill_generation_results/<config>/<task>/.
    task_path is always a query dir (tasks/<task>/<task>-N); parent.name is the task name.
    Returns None for no_skill (no files needed) or if dir does not exist.
    """
    if skill_config == "no_skill":
        return None
    task_name = task_path.parent.name
    d = SKILL_CONFIGS_DIR / skill_config / task_name
    return d if (d.exists() and d.is_dir()) else None


def _parse_skill_copies(dockerfile: Path) -> list[tuple[str, str]]:
    """
    Parse COPY instructions that involve the 'skills' source directory.
    Returns list of (source_pattern, container_dest).
    Examples:
      "COPY skills /root/.claude/skills"        -> ("skills", "/root/.claude/skills")
      "COPY skills/gmail-skill /root/verifier-skills/gmail-skill" -> ("skills/gmail-skill", "...")
    """
    copies: list[tuple[str, str]] = []
    if not dockerfile.exists():
        return copies
    for raw in dockerfile.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line.upper().startswith("COPY"):
            continue
        parts = line.split()
        if len(parts) < 3:
            continue
        # Drop --flag tokens
        args = [p for p in parts[1:] if not p.startswith("--")]
        if len(args) < 2:
            continue
        src, dest = args[0], args[-1]
        if src == "skills" or src.startswith("skills/"):
            copies.append((src, dest))
    return copies


def _inject_skills_runtime(
    container_name: str,
    skill_source_dir: Path,
    copies: list[tuple[str, str]],
) -> None:
    """
    Inject skills into a running container to mirror Dockerfile COPY instructions.

    For "COPY skills <dest>": normalise skill_source_dir (same logic as
    _copy_skills_to_dest) and docker-cp the result into <dest>.
    For "COPY skills/<subdir> <dest>": docker-cp skill_source_dir/<subdir> into <dest>.

    This produces the exact same container state as baking skills into the image.
    """
    for src_pattern, dest in copies:
        if src_pattern == "skills":
            local_src = skill_source_dir
        elif src_pattern.startswith("skills/"):
            local_src = skill_source_dir / src_pattern[len("skills/"):]
        else:
            continue

        if not local_src.exists():
            continue

        tmp_root = Path(tempfile.mkdtemp(prefix="inject_skills_"))
        try:
            if src_pattern == "skills":
                # Use the same normalization logic as _copy_skills_to_dest
                tmp_dest = tmp_root / "skills"
                ok = _copy_skills_to_dest(local_src, tmp_dest)
                if not ok:
                    continue
                local_to_cp = tmp_dest
            else:
                # Specific subdirectory
                tmp_dest = tmp_root / Path(src_pattern).name
                if local_src.is_dir():
                    shutil.copytree(local_src, tmp_dest)
                else:
                    tmp_dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(local_src, tmp_dest)
                local_to_cp = tmp_dest

            # Clear existing dest in container, then copy fresh content
            subprocess.run(
                ["docker", "exec", container_name, "rm", "-rf", dest],
                capture_output=True,
            )
            subprocess.run(
                ["docker", "exec", container_name, "mkdir", "-p", dest],
                capture_output=True,
                check=True,
            )
            # "src/." copies the *contents* of src into dest (docker cp convention)
            subprocess.run(
                ["docker", "cp", f"{local_to_cp}/.", f"{container_name}:{dest}"],
                capture_output=True,
                check=True,
            )
        except Exception as exc:
            print(
                f"[warn] skill injection failed for {src_pattern} -> {dest}: {exc}",
                file=sys.stderr,
            )
        finally:
            shutil.rmtree(tmp_root, ignore_errors=True)


def _to_int(v: object) -> int | None:
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, float):
        return int(v)
    if isinstance(v, str) and v.strip().isdigit():
        return int(v.strip())
    return None


def _extract_token_usage(trial_path: Path, agent: dict, agent_id: str) -> tuple[dict[str, int], str | None]:
    """
    Extract token usage from the last JSON line in the agent tee log.
    Returns (usage_dict, source_type). usage_dict is empty when unavailable.
    """
    tee_path = agent.get("trajectory_tee")
    if not tee_path:
        return {}, None
    log_name = Path(tee_path).name
    log_path = trial_path / "agent" / log_name
    if not log_path.exists():
        return {}, None

    picked_usage: dict | None = None
    picked_type: str | None = None

    for line in log_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            obj = json_repair.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(obj, dict):
            continue
        usage_obj = obj.get("usage")
        if not isinstance(usage_obj, dict):
            continue

        obj_type = str(obj.get("type") or "")
        if agent_id == "codex":
            if obj_type == "turn.completed":
                picked_usage = usage_obj
                picked_type = obj_type
        elif agent_id == "claude-code":
            if obj_type == "result":
                picked_usage = usage_obj
                picked_type = obj_type
        else:
            # Generic fallback: keep latest record with usage.
            picked_usage = usage_obj
            picked_type = obj_type

    if picked_usage is None:
        return {}, None

    out: dict[str, int] = {}
    for k in [
        "input_tokens",
        "output_tokens",
        "total_tokens",
        "cached_input_tokens",
        "reasoning_output_tokens",
        "cache_read_input_tokens",
        "cache_creation_input_tokens",
    ]:
        val = _to_int(picked_usage.get(k))
        if val is not None:
            out[k] = val

    return out, picked_type


def run_task(
    task_id: str,
    *,
    task_root: Path = TASKS_DIR,
    agent_id: str = "claude-code",
    model: str | None = None,
    record: bool = True,
    skill_config: str = "human_authored",
    skill_source_dir: Path | None = None,
    trial_id: str | None = None,
    max_steps: int = 100,
    prebuilt_image_tag: str | None = None,
    prebuilt_has_agent: bool = False,
    trials_dir: Path = TRIALS_DIR,
) -> tuple[int, dict]:
    """Build Docker image, run container, exec agent then verifier."""
    task_path = task_root / task_id
    if not task_path.exists():
        msg = f"Task not found: {task_id}"
        print(msg, file=sys.stderr)
        return 2, {"task_id": task_id, "error": msg}

    agent = get_agent(agent_id)
    if not agent:
        msg = f"Unknown agent: {agent_id}. Available: {', '.join(list_agents())}"
        print(msg, file=sys.stderr)
        return 2, {"task_id": task_id, "error": msg}

    # Check required env vars
    for env_var in agent["env"]:
        if not os.environ.get(env_var):
            msg = f"Set {env_var} (or add to SkillLearnBench/.env) to run agent {agent_id}"
            print(msg, file=sys.stderr)
            return 2, {"task_id": task_id, "error": msg}

    # Check task-required env vars (declared in task.toml [environment] required_env)
    task_cfg = _load_task_config(task_path)
    for env_var in task_cfg.get("environment", {}).get("required_env", []):
        if not os.environ.get(env_var):
            msg = (f"Task {task_id} requires ${env_var}. "
                   f"Add it to SkillLearnBench/.env (see .env.example).")
            print(msg, file=sys.stderr)
            return 2, {"task_id": task_id, "error": msg}

    env_dir = task_path / "environment"
    dockerfile = env_dir / "Dockerfile"
    if not dockerfile.exists():
        msg = f"No Dockerfile: {dockerfile}"
        print(msg, file=sys.stderr)
        return 2, {"task_id": task_id, "error": msg}

    model_name = model if model else agent.get("default_model", "")

    trial_name, trial_id = _mk_trial_name(task_id, skill_config, trial_id=trial_id)
    trial_path = _trial_path(task_id, skill_config, trial_id, trials_dir=trials_dir)
    trial_path.mkdir(parents=True, exist_ok=True)
    (trial_path / "agent").mkdir(exist_ok=True)
    (trial_path / "verifier").mkdir(exist_ok=True)

    _safe_id = task_id.replace("/", "-").replace("\\", "-")
    image_tag = f"evaluation_{_safe_id}_{skill_config}:{trial_id.lower()}"
    container_name = f"evaluation_{_safe_id}_{skill_config}_{trial_id.lower()}"

    build_env = None
    build_root = None

    try:
        if prebuilt_image_tag:
            # Skip build — reuse a pre-built stable image
            image_tag = prebuilt_image_tag
            print(f"[1/5] Using prebuilt image {image_tag} ({skill_config})...")
        else:
            build_env = _prepare_build_env(env_dir, skill_config, skill_source_dir)
            build_root = build_env.parent

            # Build
            print(f"[1/5] Building {image_tag} ({skill_config})...")
            r = subprocess.run(
                ["docker", "build", "-t", image_tag, str(build_env)],
                capture_output=True,
                text=True,
            )
            if r.returncode != 0:
                print(r.stderr or r.stdout, file=sys.stderr)
                result = {
                    "task_id": task_id,
                    "trial_name": trial_name,
                    "trial_id": trial_id,
                    "agent": agent_id,
                    "model": model_name,
                    "skill_config": skill_config,
                    "passed": False,
                    "reward": 0,
                    "agent_exit": None,
                    "verifier_exit": None,
                    "error": "docker_build_failed",
                }
                return 1, result

        # Run container (detached, with /logs and /tests mounts)
        print("[2/5] Starting container...")
        subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)

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
                "docker",
                "run",
                "-d",
                "--name",
                container_name,
                "-v",
                f"{task_path / 'tests'}:/tests:ro",
                "-v",
                f"{trial_path}:/logs",
                *env_args,
                image_tag,
                "sleep",
                "3600",
            ],
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            print(r.stderr or r.stdout, file=sys.stderr)
            result = {
                "task_id": task_id,
                "trial_name": trial_name,
                "agent": agent_id,
                "model": model_name,
                "skill_config": skill_config,
                "passed": False,
                "reward": 0,
                "agent_exit": None,
                "verifier_exit": None,
                "error": "docker_run_failed",
            }
            return 1, result

        # Runtime skill injection (only when reusing a pre-built base image).
        # The base image has empty skills dirs; we populate them here to produce
        # the same container state as baking skills into the image.
        if prebuilt_image_tag and skill_config != "no_skill" and skill_source_dir is not None:
            copies = _parse_skill_copies(dockerfile)
            if copies:
                print(f"[2b/5] Injecting skills ({skill_config})...")
                _inject_skills_runtime(container_name, skill_source_dir, copies)
                # Post-inject: run npm install for any skill that has package.json.
                # This mirrors what the original Dockerfile did at build time (RUN npm install),
                # which is skipped in the base image build because skills/ is empty.
                subprocess.run(
                    ["docker", "exec", container_name, "sh", "-c",
                     'for d in /root/.claude/skills/*/; do'
                     ' [ -f "$d/package.json" ] && (cd "$d" && npm install --silent 2>/dev/null) || true;'
                     ' done'],
                    capture_output=True,
                    timeout=180,
                )

        try:
            # [3/5] Install agent (Harbor style - runtime install)
            # Skip entirely when the prebuilt image already has Node + agent baked in.
            if prebuilt_has_agent:
                print(f"[3/5] Agent pre-installed in image, skipping install.")
            else:
                print(f"[3/5] Installing agent ({agent_id})...")
                install_cmd = agent["install"]
                uses_npm = "npm " in install_cmd or install_cmd.strip().startswith("npm")
                if uses_npm:
                    node_check = subprocess.run(
                        ["docker", "exec", container_name, "sh", "-c", "node -v 2>/dev/null || true"],
                        capture_output=True,
                        text=True,
                    )
                    node_version = (node_check.stdout or "").strip()
                    m = re.search(r"v?(\d+)", node_version)
                    node_major = int(m.group(1)) if m else 0

                    # Claude Code requires a modern Node runtime.
                    # Ubuntu apt's default node/npm can be too old (e.g. Node 10 on 20.04),
                    # which crashes with syntax errors when starting the CLI.
                    if node_major < 20:
                        print(
                            f"[3/5] node runtime too old or missing "
                            f"(detected: {node_version or 'none'}); installing Node 20..."
                        )
                        node_install = subprocess.run(
                            [
                                "docker",
                                "exec",
                                container_name,
                                "sh",
                                "-c",
                                "apt-get update && "
                                "apt-get install -y ca-certificates curl gnupg && "
                                "mkdir -p /etc/apt/keyrings && "
                                "curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key "
                                "| gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && "
                                "echo 'deb [signed-by=/etc/apt/keyrings/nodesource.gpg] "
                                "https://deb.nodesource.com/node_20.x nodistro main' "
                                "> /etc/apt/sources.list.d/nodesource.list && "
                                "apt-get update && apt-get install -y nodejs",
                            ],
                            capture_output=True,
                            text=True,
                            timeout=420,
                        )
                        if node_install.returncode != 0:
                            print(node_install.stderr or node_install.stdout, file=sys.stderr)
                            result = {
                                "task_id": task_id,
                                "trial_name": trial_name,
                                "agent": agent_id,
                                "model": model_name,
                                "skill_config": skill_config,
                                "passed": False,
                                "reward": 0,
                                "agent_exit": None,
                                "verifier_exit": None,
                                "error": "node_install_failed",
                            }
                            return 1, result

                install_r = subprocess.run(
                    ["docker", "exec", container_name, "sh", "-c", install_cmd],
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
                if install_r.returncode != 0:
                    print(install_r.stderr or install_r.stdout, file=sys.stderr)
                    result = {
                        "task_id": task_id,
                        "trial_name": trial_name,
                        "agent": agent_id,
                        "model": model_name,
                        "skill_config": skill_config,
                        "passed": False,
                        "reward": 0,
                        "agent_exit": None,
                        "verifier_exit": None,
                        "error": "agent_install_failed",
                    }
                    return 1, result

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
                    timeout=30,
                )

            # Copy instruction to container and run agent
            instruction = (task_path / "instruction.md").read_text(encoding="utf-8").strip()
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

            _subtask_name = Path(task_id).name
            _subtask_idx = re.search(r"-(\d+)$", _subtask_name)
            _extra_flags = " --settings '{\"temperature\":0}'" if (_subtask_idx and int(_subtask_idx.group(1)) > 1) else ""
            run_cmd = (
                agent["run"]
                .replace("{instruction_file}", "/tmp/instruction.txt")
                .replace("{model}", model_name)
                .replace("{max_steps}", str(max_steps))
                .replace("{allowed_tools}", _allowed_tools)
                .replace("{extra_flags}", _extra_flags)
            )
            tee_path = agent.get("trajectory_tee")
            traj_env = agent.get("trajectory_env", {})
            env_prefix = " ".join(f"{k}={v}" for k, v in traj_env.items() if v)
            if env_prefix:
                run_cmd = f"{env_prefix} {run_cmd}"
            if tee_path:
                run_cmd = f"({run_cmd}) 2>&1 | tee {tee_path}"

            print(f"[4/5] Running agent ({agent_id})...")
            agent_exit_code: int | None = None
            agent_timed_out = False
            try:
                r = subprocess.run(
                    ["docker", "exec", container_name, "sh", "-c", run_cmd],
                    capture_output=True,
                    text=True,
                    timeout=1800,
                )
                agent_stdout = r.stdout or ""
                agent_stderr = r.stderr or ""
                agent_exit_code = r.returncode
            except subprocess.TimeoutExpired as exc:
                agent_timed_out = True
                agent_stdout = (exc.stdout or b"").decode(errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
                agent_stderr = (exc.stderr or b"").decode(errors="replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
                print(f"[4/5] Agent timed out after 1800s — proceeding to verifier.", file=sys.stderr)
                # Best-effort: kill lingering agent process inside container
                subprocess.run(
                    ["docker", "exec", container_name, "sh", "-c", "pkill -f claude || true"],
                    capture_output=True,
                )

            # Remove auth.json from trial dir (CODEX_HOME may be /logs/agent = trial_path/agent)
            if setup == "auth_json" and codex_home.startswith("/logs"):
                subprocess.run(
                    ["docker", "exec", container_name, "rm", "-f", f"{codex_home}/auth.json"],
                    capture_output=True,
                )

            # Exec verifier — always runs regardless of agent outcome.
            # Use bash: test.sh may use source/uvx which dash doesn't support.
            print("[5/5] Running verifier...")
            try:
                verifier = subprocess.run(
                    ["docker", "exec", container_name, "bash", "/tests/test.sh"],
                    capture_output=True,
                    text=True,
                    timeout=1800,  # 1800s for heavy verifiers (e.g. simpo installs torch at test time)
                )
            except subprocess.TimeoutExpired:
                print("[5/5] Verifier timed out.", file=sys.stderr)
                verifier = subprocess.CompletedProcess(args=[], returncode=-1, stdout="", stderr="timeout")

            # Read reward (from mounted trial_path/verifier/reward.txt)
            reward = 0
            reward_file = trial_path / "verifier" / "reward.txt"
            if reward_file.exists():
                try:
                    reward = int(reward_file.read_text(encoding="utf-8").strip())
                except ValueError:
                    pass

            passed = reward == 1

            token_usage, token_usage_source = _extract_token_usage(trial_path, agent, agent_id)

            result = {
                "task_id": task_id,
                "trial_name": trial_name,
                "trial_id": trial_id,
                "agent": agent_id,
                "model": model_name,
                "skill_config": skill_config,
                "skill_source_dir": str(skill_source_dir) if skill_source_dir else None,
                "passed": passed,
                "reward": reward,
                "agent_exit": agent_exit_code,
                "agent_timed_out": agent_timed_out,
                "verifier_exit": verifier.returncode,
                "agent_stdout": agent_stdout[:2000],
                "agent_stderr": agent_stderr[:1000],
                "token_usage": token_usage,
                "token_usage_source": token_usage_source,
            }
            # Record results (Harbor style: trials/<trial>/)
            if record:
                (trial_path / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
                print(f"Trial: {trial_path}")

            print("PASS" if passed else "FAIL")
            return (0 if passed else 1), result
        finally:
            subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)
    finally:
        # best effort cleanup for temporary build context
        if build_root and build_root.exists():
            shutil.rmtree(build_root, ignore_errors=True)


def eval_tasks(
    task_ids: list[str],
    *,
    task_root: Path,
    agent_id: str,
    model: str | None,
    record: bool,
    modes: list[str],
    max_workers: int,
    repeats: int,
    max_steps: int = 100,
) -> int:
    """Run selected skill configs for each task and report success rates."""
    all_results: list[dict] = []
    skipped: list[dict] = []

    run_specs: list[dict] = []

    repeats = max(1, int(repeats))
    for task_id in task_ids:
        task_path = task_root / task_id
        print(f"\n=== Task: {task_id} ===")

        for rep in range(repeats):
            print(f"[eval] repeat {rep + 1}/{repeats}")

            for config in modes:
                skill_source = _resolve_skill_source(task_path, config)
                if config != "no_skill" and skill_source is None:
                    skipped.append(
                        {
                            "task_id": task_id,
                            "config": config,
                            "reason": "missing_skill_source",
                            "repeat": rep + 1,
                        }
                    )
                    print(f"[skip] {config}: missing skill source in skill_generation_results/")
                    continue

                run_specs.append(
                    {
                        "task_id": task_id,
                        "skill_config": config,
                        "skill_source_dir": skill_source,
                    }
                )

    max_workers = max(1, int(max_workers))
    if max_workers == 1:
        for spec in run_specs:
            _, res = run_task(
                spec["task_id"],
                task_root=task_root,
                agent_id=agent_id,
                model=model,
                record=record,
                skill_config=spec["skill_config"],
                skill_source_dir=spec["skill_source_dir"],
                max_steps=max_steps,
            )
            all_results.append(res)
    else:
        print(f"[eval] Running {len(run_specs)} trial(s) in parallel (max_workers={max_workers})")
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_spec = {
                executor.submit(
                    run_task,
                    spec["task_id"],
                    task_root=task_root,
                    agent_id=agent_id,
                    model=model,
                    record=record,
                    skill_config=spec["skill_config"],
                    skill_source_dir=spec["skill_source_dir"],
                    max_steps=max_steps,
                ): spec
                for spec in run_specs
            }
            for future in concurrent.futures.as_completed(future_to_spec):
                _, res = future.result()
                all_results.append(res)

    def _config_stats(config: str) -> dict:
        rows = [r for r in all_results if r.get("skill_config") == config and "passed" in r]
        total = len(rows)
        passed = sum(1 for r in rows if r.get("passed") is True)
        rate = (passed / total) if total else 0.0
        token_sums: dict[str, int] = {}
        for r in rows:
            usage = r.get("token_usage") or {}
            for k, v in usage.items():
                if isinstance(v, int):
                    token_sums[k] = token_sums.get(k, 0) + v
        return {
            "config": config,
            "total": total,
            "passed": passed,
            "success_rate": rate,
            "token_usage": token_sums,
        }

    def _exact_config_stats(skill_config: str) -> dict:
        rows = [r for r in all_results if r.get("skill_config") == skill_config and "passed" in r]
        total = len(rows)
        passed = sum(1 for r in rows if r.get("passed") is True)
        rate = (passed / total) if total else 0.0
        token_sums: dict[str, int] = {}
        for r in rows:
            usage = r.get("token_usage") or {}
            for k, v in usage.items():
                if isinstance(v, int):
                    token_sums[k] = token_sums.get(k, 0) + v
        return {
            "config": skill_config,
            "total": total,
            "passed": passed,
            "success_rate": rate,
            "token_usage": token_sums,
        }

    stats = {v: _config_stats(v) for v in modes}

    print("\n=== Summary ===")
    for config in modes:
        s = stats.get(config)
        if not s:
            continue
        tu = s["token_usage"]
        token_brief = ", ".join(f"{k}={v}" for k, v in sorted(tu.items())) if tu else "none"
        print(f"{config}: {s['passed']}/{s['total']} ({s['success_rate']:.2%}), token_usage: {token_brief}")
    if skipped:
        print(f"skipped configs: {len(skipped)}")

    return 0


def main() -> int:
    _load_dotenv()
    parser = argparse.ArgumentParser(description="Minimal agent sandbox CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="List tasks")
    sub.add_parser("agents", help="List available agents")

    run_p = sub.add_parser("run", help="Run task with agent + verifier")
    run_p.add_argument("task_id", help="Task ID (folder name)")
    run_p.add_argument("-a", "--agent", default="claude-code", help="Agent ID (default: claude-code)")
    run_p.add_argument("-m", "--model", default="claude-sonnet-4-6", help="Model name (default: claude-sonnet-4-6)")
    run_p.add_argument(
        "--skill-mode",
        default="human_authored",
        help="Skill config name (e.g. human_authored, no_skill, b1-one-shot-claude-sonnet-4-6)",
    )
    run_p.add_argument("--max-steps", type=int, default=100, metavar="N",
                       help="Max agent turns (default: 100)")
    run_p.add_argument("--no-record", action="store_true", help="Skip writing results")

    eval_p = sub.add_parser("eval", help="Evaluate skill configs across tasks")
    eval_p.add_argument("tasks", nargs="*", help="Task IDs (default: all tasks)")
    eval_p.add_argument("-a", "--agent", default="claude-code", help="Agent ID (default: claude-code)")
    eval_p.add_argument("-m", "--model", default="claude-sonnet-4-6", help="Model name (default: claude-sonnet-4-6)")
    eval_p.add_argument(
        "--modes",
        default="human_authored,no_skill",
        help="Comma-separated config names to evaluate, e.g. human_authored,b1-one-shot-claude-sonnet-4-6,no_skill",
    )
    eval_p.add_argument(
        "--max-workers",
        type=int,
        default=1,
        help="Parallel workers for eval runs (default: 1, i.e. serial)",
    )
    eval_p.add_argument(
        "--repeats",
        type=int,
        default=1,
        help="Repeat each selected mode this many times per task (default: 1)",
    )
    eval_p.add_argument("--max-steps", type=int, default=100, metavar="N",
                        help="Max agent turns per trial (default: 100)")
    eval_p.add_argument("--no-record", action="store_true", help="Skip writing per-trial result.json")

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
        task_path = TASKS_DIR / args.task_id
        skill_source = _resolve_skill_source(task_path, args.skill_mode)
        if args.skill_mode != "no_skill" and skill_source is None:
            print(f"Missing skill source for mode={args.skill_mode}", file=sys.stderr)
            return 2
        return run_task(
            args.task_id,
            agent_id=args.agent,
            model=args.model,
            record=not args.no_record,
            skill_config=args.skill_mode,
            skill_source_dir=skill_source,
            max_steps=args.max_steps,
        )[0]

    if args.cmd == "eval":
        tasks = args.tasks if args.tasks else list_tasks()
        if not tasks:
            print("No tasks found.")
            return 2
        modes = [m.strip() for m in args.modes.split(",") if m.strip()]
        if not modes:
            print("Invalid --modes: no config names provided.", file=sys.stderr)
            return 2
        return eval_tasks(
            tasks,
            task_root=TASKS_DIR,
            agent_id=args.agent,
            model=args.model,
            record=not args.no_record,
            modes=modes,
            max_workers=args.max_workers,
            repeats=args.repeats,
            max_steps=args.max_steps,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
