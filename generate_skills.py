#!/usr/bin/env python3
"""
Parallel Docker skill-generation runner.

Phase 1 – Pre-build: one Docker image per (task, agent) pair.
          Skips build if stable tag already exists locally.
Phase 2 – Run: all (task × method × model) combos in parallel.
          Method prompt injected at runtime; agent pre-baked in image.
Phase 3 – Cleanup: remove stable images only if --remove-images is passed.
          Default: keep images for reuse across runs.

Usage examples:
    python generate_skills.py
    python generate_skills.py --tasks citation-check organize-messy-files
    python generate_skills.py --methods b1-one-shot b2-self-feedback
    python generate_skills.py --models claude-sonnet-4-6 --max-workers 4
    python generate_skills.py --dry-run
    python generate_skills.py --remove-images
"""
from __future__ import annotations

import argparse
import concurrent.futures
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from itertools import product
from pathlib import Path


def _require_docker() -> None:
    """Abort with a helpful message if the docker CLI is not available."""
    if shutil.which("docker") is None:
        print(
            "Error: `docker` CLI not found on PATH.\n"
            "SkillLearnBench runs every trial inside a Docker container, so Docker is required.\n"
            "Install it from: https://docs.docker.com/get-docker/",
            file=sys.stderr,
        )
        raise SystemExit(2)


_PLACEHOLDER_KEY_RE = re.compile(r"^your-.*-here$", re.IGNORECASE)

_PROVIDER_PING = {
    "ANTHROPIC_API_KEY": (
        "https://api.anthropic.com/v1/models?limit=1",
        {"x-api-key": "{key}", "anthropic-version": "2023-06-01"},
    ),
    "OPENAI_API_KEY": (
        "https://api.openai.com/v1/models",
        {"Authorization": "Bearer {key}"},
    ),
    "GEMINI_API_KEY": (
        "https://generativelanguage.googleapis.com/v1beta/models?key={key}&pageSize=1",
        {},
    ),
}


def _check_provider_key(var: str, *, timeout: float = 10.0) -> str | None:
    """Return None if the key is set and pings successfully; otherwise a short warning message."""
    import urllib.error
    import urllib.request

    key = os.environ.get(var, "").strip()
    if not key or _PLACEHOLDER_KEY_RE.match(key):
        return f"{var}: not set (or placeholder value)"

    url_tpl, header_tpl = _PROVIDER_PING[var]
    url = url_tpl.replace("{key}", key)
    headers = {h: v.replace("{key}", key) for h, v in header_tpl.items()}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                return f"{var}: ping returned HTTP {resp.status}"
    except urllib.error.HTTPError as exc:
        return f"{var}: rejected by provider (HTTP {exc.code} {exc.reason})"
    except urllib.error.URLError as exc:
        return f"{var}: cannot reach provider ({exc.reason})"
    except Exception as exc:
        return f"{var}: ping failed ({exc!r})"
    return None


def _warn_provider_keys() -> None:
    """Warn (non-fatal) about any missing / invalid provider API key."""
    issues = [msg for var in _PROVIDER_PING if (msg := _check_provider_key(var)) is not None]
    if not issues:
        return
    print("WARNING: provider API key issues detected — affected models will fail at runtime:", file=sys.stderr)
    for msg in issues:
        print(f"  - {msg}", file=sys.stderr)
    print(
        "Fix: set the missing key(s) in your environment or .env, or limit --models to "
        "providers whose keys are valid.",
        file=sys.stderr,
    )

sys.path.insert(0, str(Path(__file__).parent))

from agents import get_agent
from core.skill_runner import (
    METHODS_DIR,
    TASKS_DIR,
    TRIALS_DIR,        # output/skill_generation_log/
    SKILL_CONFIGS_DIR,  # output/skill_generation_results/
    _load_dotenv,
    _load_method_config,
    run_task,
)

try:
    from rich.console import Console as RichConsole
    from rich.console import Group
    from rich.live import Live
    from rich.progress import (
        BarColumn,
        MofNCompleteColumn,
        Progress,
        SpinnerColumn,
        TextColumn,
        TimeElapsedColumn,
        TimeRemainingColumn,
    )

    _RICH = True
except ImportError:
    _RICH = False

_PRINT_LOCK = threading.Lock()


def _log(msg: str) -> None:
    with _PRINT_LOCK:
        print(msg, flush=True)


# ── Thread-local stdout capture ────────────────────────────────────────────────

class _ThreadLocalStdout(io.TextIOBase):
    """
    Wraps sys.stdout so that each worker thread can silently capture its own
    print() output. Threads that haven't called .capture() pass through to
    the real stdout unchanged.
    """

    def __init__(self, real: io.TextIOBase) -> None:
        self._real = real
        self._local = threading.local()
        # When True, uncaptured threads have their writes silently discarded.
        # Set to True inside the Live context so that background threads spawned
        # by run_task() (e.g. _poll_skills_done) cannot write to the terminal
        # and disrupt the Rich display.
        self._suppress_all: bool = False

    def _buf(self) -> io.StringIO | None:
        return getattr(self._local, "buf", None)

    def capture(self) -> None:
        self._local.buf = io.StringIO()

    def release(self) -> io.StringIO:
        buf = self._local.buf
        self._local.buf = None
        return buf or io.StringIO()

    def write(self, s: str) -> int:
        buf = self._buf()
        if buf is not None:
            return buf.write(s)
        if self._suppress_all:
            return len(s)  # discard: background thread output during Live context
        return self._real.write(s)

    def flush(self) -> None:
        buf = self._buf()
        if buf is None:
            self._real.flush()

    @property
    def encoding(self) -> str:
        return getattr(self._real, "encoding", "utf-8")

    @property
    def errors(self) -> str:
        return getattr(self._real, "errors", "strict")


# ── API QPS monitor ───────────────────────────────────────────────────────────

class ApiQpsMonitor:
    """
    Background thread that tails active trial log files and counts API calls.
    Each 'type':'assistant' JSON line in the agent trajectory log
    represents one completed LLM API call.
    """
    WINDOW_SECS = 30
    POLL_SECS = 1.0

    def __init__(self, trials_dir: Path, run_start: float) -> None:
        self._trials_dir = trials_dir
        self._run_start = run_start
        self._lock = threading.Lock()
        self._file_offset: dict[Path, int] = {}
        self._call_times: list[float] = []
        self._total_cumulative: int = 0
        self._stop = threading.Event()
        self._thread = threading.Thread(
            target=self._loop, daemon=True, name="qps-monitor"
        )

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()

    def qps(self) -> float:
        now = time.monotonic()
        cutoff = now - self.WINDOW_SECS
        with self._lock:
            self._call_times = [t for t in self._call_times if t > cutoff]
            return len(self._call_times) / self.WINDOW_SECS

    def total_calls(self) -> int:
        with self._lock:
            return self._total_cumulative

    def _loop(self) -> None:
        while not self._stop.wait(self.POLL_SECS):
            self._scan()

    def _scan(self) -> None:
        now = time.monotonic()
        # Scan all known trajectory log patterns
        log_patterns = ["agent/claude-code.txt", "agent/gemini-code.txt", "agent/codex.txt"]
        try:
            log_files: list[Path] = []
            for pattern in log_patterns:
                log_files.extend(self._trials_dir.rglob(pattern))
        except Exception:
            return
        for log_path in log_files:
            try:
                if log_path.stat().st_mtime < self._run_start:
                    continue
                with self._lock:
                    offset = self._file_offset.get(log_path, 0)
                lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
                new_lines = lines[offset:]
                new_calls = sum(
                    1 for ln in new_lines
                    if '"type":"assistant"' in ln or '"type": "assistant"' in ln
                )
                with self._lock:
                    self._file_offset[log_path] = len(lines)
                    for _ in range(new_calls):
                        self._call_times.append(now)
                    self._total_cumulative += new_calls
            except Exception:
                pass


# ── Model → agent mapping ─────────────────────────────────────────────────────

MODEL_AGENT: dict[str, str] = {
    "claude-sonnet-4-6": "claude-code",
    "claude-opus-4-6": "claude-code",
    "claude-haiku-4-5": "claude-code",
    "gemini-3.1-flash-lite": "gemini-code",
    "gemini-3-flash-preview": "gemini-code",
    "gemini-3.1-pro-preview": "gemini-code",
}


def _infer_agent(model: str) -> str | None:
    """Infer agent ID from model name prefix for models not in MODEL_AGENT."""
    if model.startswith("claude-"):
        return "claude-code"
    if model.startswith("gemini-"):
        return "gemini-code"
    return None


def _check_api_key(provider: str) -> tuple[bool, str]:
    """Make a lightweight real API call to verify the key for a provider works."""
    if provider == "anthropic":
        key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not key:
            return False, "ANTHROPIC_API_KEY not set"
        try:
            import anthropic as _anthropic
            _anthropic.Anthropic(api_key=key).models.list()
            return True, ""
        except Exception as e:
            return False, f"ANTHROPIC_API_KEY invalid: {e}"
    if provider == "gemini":
        key = os.environ.get("GEMINI_API_KEY", "")
        if not key:
            return False, "GEMINI_API_KEY not set"
        try:
            from google import genai as _genai
            from google.genai import types as _gtypes
            _client = _genai.Client(api_key=key)
            _client.models.generate_content(
                model="gemini-2.0-flash",
                contents="hi",
                config=_gtypes.GenerateContentConfig(max_output_tokens=1),
            )
            return True, ""
        except Exception as e:
            return False, f"GEMINI_API_KEY invalid: {e}"
    return False, f"Unknown provider: {provider}"

DEFAULT_METHODS = [
    "b1-one-shot",
    "b2-self-feedback",
    "b3-teacher-feedback",
    "b4-skill-creator",
]

DEFAULT_MODELS = list(MODEL_AGENT.keys())

DEFAULT_TASKS = [
    "anthropic-poster-design",
    "chinese-poem-generator",
    "court-form-filling",
    "dbscan-parameter-tuning",
    "dependency-vulnerability-check",
    "earthquake-plate-calculation",
    "enterprise-information-search",
    "financial-analysis",
    "fix-security-bug",
    "github-repo-analytics",
    "nlp-paper-reproduction",
    "offer-letter-generator",
    "organize-messy-files",
    "python-scala-translation",
    "schedule-planning",
    "stock-data-visualization",
    "temperature-simulation",
    "travel-planning",
    "video-object-counting",
    "weighted-gdp-calculation",
]

DEFAULT_ARTIFACT = "/root/environment/skills"


# ── Stable tag: one per (task, agent) ─────────────────────────────────────────

def _stable_tag(task_id: str, agent_id: str) -> str:
    safe_task = re.sub(r"[^a-z0-9._-]", "-", task_id.lower())
    safe_task = re.sub(r"-{2,}", "-", safe_task).strip("-")
    safe_agent = re.sub(r"[^a-z0-9._-]", "-", agent_id.lower())
    return f"test_agent_skill-{safe_task}-{safe_agent}:stable"


def _image_exists(tag: str) -> bool:
    r = subprocess.run(["docker", "image", "inspect", tag], capture_output=True)
    return r.returncode == 0


# ── Task path resolution ───────────────────────────────────────────────────────

def _resolve_env_dir(task_id: str) -> Path | None:
    """Resolve the environment/ dir for a task (always tasks/<task>/<task>-1/environment/)."""
    env_dir = TASKS_DIR / task_id / (task_id + "-1") / "environment"
    return env_dir if (env_dir / "Dockerfile").exists() else None


# ── Base image build ───────────────────────────────────────────────────────────

def _build_one(task_id: str, agent_id: str) -> tuple[str, str | None]:
    """
    Ensure the per-(task, agent) stable image exists.
    Two-layer build:
      Layer 1: task base environment (from task Dockerfile)
      Layer 2: Node 20 + agent CLI baked on top
    Skips both layers if the stable tag already exists locally.
    Returns (tag, error_message_or_None).
    """
    tag = _stable_tag(task_id, agent_id)
    if _image_exists(tag):
        return tag, None  # reuse cached image

    agent = get_agent(agent_id)
    if not agent:
        return tag, f"unknown agent: {agent_id}"

    env_dir = _resolve_env_dir(task_id)
    if env_dir is None:
        return tag, f"cannot resolve environment/ dir for task: {task_id}"

    base_tag = f"{tag}-base"
    build_root = None
    try:
        # Layer 1: task environment — exclude oracle skills so the agent must
        # generate skills from scratch rather than reading the ground-truth answers.
        build_root = Path(tempfile.mkdtemp(prefix="skill_hyper_base_"))
        build_env = build_root / "environment"
        shutil.copytree(env_dir, build_env, ignore=shutil.ignore_patterns("skills"))
        (build_env / "skills").mkdir(parents=True, exist_ok=True)

        r = subprocess.run(
            ["docker", "build", "-t", base_tag, str(build_env)],
            capture_output=True, text=True,
        )
        if r.returncode != 0:
            snippet = (r.stderr or r.stdout or "")[:400].strip()
            return tag, f"base build failed: {snippet}"

        # Layer 2: bake agent CLI on top
        runtime_deps = agent.get("runtime_deps", "")
        install_cmd = agent.get("install", "")
        layer2_lines = [f"FROM {base_tag}"]
        if runtime_deps:
            layer2_lines.append(f"RUN {runtime_deps}")
        if install_cmd:
            layer2_lines.append(f"RUN {install_cmd}")
        layer2_dockerfile = "\n".join(layer2_lines) + "\n"

        r2 = subprocess.run(
            ["docker", "build", "-t", tag, "-"],
            input=layer2_dockerfile,
            capture_output=True, text=True,
        )
        if r2.returncode != 0:
            snippet = (r2.stderr or r2.stdout or "")[:400].strip()
            return tag, f"agent layer build failed: {snippet}"

        subprocess.run(["docker", "rmi", "-f", base_tag], capture_output=True)
        return tag, None
    except Exception as exc:
        return tag, str(exc)
    finally:
        if build_root and build_root.exists():
            shutil.rmtree(build_root, ignore_errors=True)


# ── Spec collection ────────────────────────────────────────────────────────────

def _collect_extra_instructions(task_id: str, n: int) -> list[str]:
    """Return up to n extra subtask instruction texts (subtask-2, -3, …)."""
    if n <= 0:
        return []
    task_path = TASKS_DIR / task_id
    extras: list[str] = []
    for i in range(2, n + 2):
        instr_file = task_path / f"{task_id}-{i}" / "instruction.md"
        if instr_file.exists():
            extras.append(instr_file.read_text(encoding="utf-8").strip())
        if len(extras) >= n:
            break
    return extras


def _collect_specs(
        task_ids: list[str],
        methods: list[str],
        models: list[str],
        extra_subtasks: int = 0,
) -> list[dict]:
    """Collect all (task, method, model) trial specs."""
    specs = []
    for task_id, method, model in product(task_ids, methods, models):
        agent_id = MODEL_AGENT.get(model) or _infer_agent(model)
        if not agent_id:
            _log(f"  [SKIP] Unknown model (no agent mapping): {model}")
            continue
        # Validate method exists: plugin methods use method.py instead of method.md.
        plugin_file = METHODS_DIR / method / "method.py"
        if not plugin_file.exists():
            method_file = METHODS_DIR / method / "method.md"
            if not method_file.exists():
                _log(f"  [SKIP] Method not found: {method}")
                continue
        extra_instructions = _collect_extra_instructions(task_id, extra_subtasks)
        # max_rounds comes from the method's own method.toml; fall back to 3.
        effective_rounds = _load_method_config(method).get("max_rounds", 3)
        specs.append({
            "task_id": task_id,
            "method": method,
            "model": model,
            "agent_id": agent_id,
            "extra_instructions": extra_instructions,
            "max_rounds": effective_rounds,
        })
    return specs


# ── Phase 2 runners ────────────────────────────────────────────────────────────

def _phase2_plain(
        specs: list[dict],
        max_workers: int,
        tag_map: dict[tuple[str, str], str],
        artifact: str,
        max_steps: int,
        skills_only: bool,
        record: bool,
        all_results: list[dict],
        results_lock: threading.Lock,
) -> None:
    """Fallback: plain output, no rich dependency."""

    def _run_one(spec: dict) -> None:
        rc, res = run_task(
            spec["task_id"],
            agent_id=spec["agent_id"],
            model=spec["model"],
            method=spec["method"],
            artifacts=[artifact],
            max_steps=max_steps,
            max_rounds=spec["max_rounds"],
            skills_only=skills_only,
            record=record,
            prebuilt_image_tag=tag_map[(spec["task_id"], spec["agent_id"])],
            prebuilt_has_agent=True,
            extra_instructions=spec.get("extra_instructions") or None,
        )
        res.setdefault("method", spec["method"])
        res.setdefault("model", spec["model"])
        res["_rc"] = rc
        with results_lock:
            all_results.append(res)

    if max_workers == 1:
        for spec in specs:
            _run_one(spec)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
            concurrent.futures.wait({ex.submit(_run_one, spec): spec for spec in specs})


def _phase2_rich(
        specs: list[dict],
        max_workers: int,
        tag_map: dict[tuple[str, str], str],
        artifact: str,
        max_steps: int,
        skills_only: bool,
        record: bool,
        all_results: list[dict],
        results_lock: threading.Lock,
) -> None:
    """
    Phase 2 with two-level rich progress display.

    Layout:
      Overall  [████████░░░░] 45/84  ETA 9:23
        Worker  0  ⠸ citation-check / b1-one-shot / claude-sonnet-4-6          1:23
        Worker  1  ⠴ organize-messy-files / b2-self-feedback / gemini-…        0:45
        Worker  2  · [idle]
        ...
    """
    real_stdout = sys.stdout
    tl_stdout = _ThreadLocalStdout(real_stdout)
    sys.stdout = tl_stdout  # type: ignore[assignment]

    _console = RichConsole(file=real_stdout)

    overall_p = Progress(
        TextColumn("{task.description}"),
        BarColumn(bar_width=None),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeRemainingColumn(),
        console=_console,
        expand=True,
    )
    worker_p = Progress(
        TextColumn("  {task.description}"),
        SpinnerColumn("dots"),
        TextColumn(" "),
        TimeElapsedColumn(),
        console=_console,
        expand=True,
    )

    overall_task_id = overall_p.add_task("[bold green]Overall[/bold green]", total=len(specs))

    worker_task_ids = [
        worker_p.add_task(f"[dim]Worker {i:2d}  · idle[/dim]", start=False)
        for i in range(max_workers)
    ]

    from collections import deque
    free_slots: deque[int] = deque(range(max_workers))
    slot_lock = threading.Lock()

    # ── API QPS monitor ────────────────────────────────────────────────────────
    monitor = ApiQpsMonitor(TRIALS_DIR, run_start=time.time())
    monitor.start()

    _qps_stop = threading.Event()

    def _qps_updater() -> None:
        while not _qps_stop.wait(2.0):
            qps = monitor.qps()
            total = monitor.total_calls()
            with slot_lock:
                busy = max_workers - len(free_slots)
            throttled = busy >= max(2, max_workers // 2) and qps < 0.3
            qps_color = "yellow" if throttled else "green"
            warn = " [yellow]⚠ throttled?[/yellow]" if throttled else ""
            overall_p.update(
                overall_task_id,
                description=(
                    f"[bold green]Overall[/bold green]  "
                    f"[{qps_color}]API {qps:.1f} req/s[/{qps_color}]"
                    f" [dim]({total} total)[/dim]{warn}"
                ),
            )

    qps_thread = threading.Thread(target=_qps_updater, daemon=True, name="qps-updater")
    qps_thread.start()

    def _shorten(s: str, maxlen: int = 38) -> str:
        return s if len(s) <= maxlen else "…" + s[-(maxlen - 1):]

    def _run_one(spec: dict) -> None:
        tl_stdout.capture()
        with slot_lock:
            slot = free_slots.popleft()

        task_short = _shorten(spec["task_id"].split("/")[-1], 22)
        method_short = _shorten(spec["method"], 20)
        model_short = _shorten(spec["model"], 22)
        desc = (
            f"[dim]Worker {slot:2d}[/dim]  "
            f"[cyan]{task_short}[/cyan] / {method_short} / {model_short}"
        )
        worker_p.reset(worker_task_ids[slot], start=False)  # clears start_time so timer resets
        worker_p._tasks[worker_task_ids[slot]].stop_time = None  # workaround: reset() doesn't clear stop_time in this Rich version
        worker_p.update(worker_task_ids[slot], description=desc)
        worker_p.start_task(worker_task_ids[slot])

        try:
            rc, res = run_task(
                spec["task_id"],
                agent_id=spec["agent_id"],
                model=spec["model"],
                method=spec["method"],
                artifacts=[artifact],
                max_steps=max_steps,
                max_rounds=spec["max_rounds"],
                skills_only=skills_only,
                record=record,
                prebuilt_image_tag=tag_map[(spec["task_id"], spec["agent_id"])],
                prebuilt_has_agent=True,
                extra_instructions=spec.get("extra_instructions") or None,
            )
            res.setdefault("method", spec["method"])
            res.setdefault("model", spec["model"])
            res["_rc"] = rc
            with results_lock:
                all_results.append(res)
        finally:
            tl_stdout.release()
            worker_p.stop_task(worker_task_ids[slot])
            worker_p.update(
                worker_task_ids[slot],
                description=f"[dim]Worker {slot:2d}  · idle[/dim]",
            )
            overall_p.advance(overall_task_id, 1)
            with slot_lock:
                free_slots.append(slot)

    group = Group(overall_p, worker_p)
    tl_stdout._suppress_all = True  # suppress background-thread prints during Live context
    try:
        with Live(group, console=_console, refresh_per_second=4, transient=False,
                  redirect_stdout=False):
            if max_workers == 1:
                for spec in specs:
                    _run_one(spec)
            else:
                with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
                    concurrent.futures.wait(
                        {ex.submit(_run_one, spec): spec for spec in specs}
                    )
    finally:
        tl_stdout._suppress_all = False
        _qps_stop.set()
        monitor.stop()
        sys.stdout = tl_stdout._real


# ── Skill config organization (auto-runs after skill generation) ─────────────
#
# Reads output/skill_generation_log/ and writes organized artifacts to
# output/skill_generation_results/ so that evaluate_skills.py can find them.
# Phase 1 layout: skill_generation_log/<config>/<task>/<task>-<ts_hash>/
#             skill_generation_results/<config>/<task>/
# "oracle" is now called "human_authored".
# Functions are prefixed _sv_ to avoid name collisions.

_SV_TS_RE  = re.compile(r"(\d{14})")   # matches timestamp anywhere in name
_SV_RUN_RE = re.compile(r"^run(\d+)_")


def _sv_filter_skill_dirs(skills_src: Path, *, full: bool = False) -> list[Path]:
    """Return skill subdirs, keeping only the latest runN_ group (unless full=True)."""
    if full:
        return [d for d in skills_src.iterdir() if d.is_dir()]
    run_groups: dict[int, list[Path]] = {}
    other: list[Path] = []
    for d in skills_src.iterdir():
        if not d.is_dir():
            continue
        m = _SV_RUN_RE.match(d.name)
        if m:
            run_groups.setdefault(int(m.group(1)), []).append(d)
        else:
            other.append(d)
    if run_groups:
        return other + sorted(run_groups[max(run_groups)])
    return other


def _sv_latest_timestamp(name: str) -> str:
    m = _SV_TS_RE.search(name)
    return m.group(1) if m else ""


def _sv_find_latest_skills(task_trial_dir: Path) -> Path | None:
    """Return artifacts/skills/ from the trial with the latest timestamp in its name."""
    best_ts = ""
    best_path: Path | None = None
    if not task_trial_dir.exists():
        return None
    for trial_dir in task_trial_dir.iterdir():
        if not trial_dir.is_dir():
            continue
        skills_path = trial_dir / "artifacts" / "skills"
        if not skills_path.exists() or not skills_path.is_dir():
            continue
        if not any(skills_path.iterdir()):
            continue
        ts = _sv_latest_timestamp(trial_dir.name)
        if ts >= best_ts:
            best_ts = ts
            best_path = skills_path
    return best_path


def _sv_find_oracle_dir(task_name: str) -> Path | None:
    """Return human_authored skills dir: tasks/<task>/<task>-1/environment/skills/"""
    first_sub = TASKS_DIR / task_name / f"{task_name}-1" / "environment" / "skills"
    return first_sub if (first_sub.exists() and first_sub.is_dir()) else None


def _sv_process_task(task_name: str, *, overwrite: bool, dry_run: bool) -> None:
    """Organize generated + human_authored skill configs for one task into SKILL_CONFIGS_DIR.

    New layout: TRIALS_DIR/<config>/<task>/<trial>/
    Scans all config dirs under TRIALS_DIR for this task_name.
    Writes to: SKILL_CONFIGS_DIR/<config>/<task>/
    """
    found_any = False

    if TRIALS_DIR.exists():
        for config_dir in sorted(TRIALS_DIR.iterdir()):
            if not config_dir.is_dir():
                continue
            task_trial_dir = config_dir / task_name
            if not task_trial_dir.is_dir():
                continue

            best_skills = _sv_find_latest_skills(task_trial_dir)
            if best_skills is None:
                continue

            config_name = config_dir.name
            dest = SKILL_CONFIGS_DIR / config_name / task_name
            if dest.exists():
                if not overwrite:
                    print(f"  [EXISTS] {config_name}/{task_name}  (use --overwrite-configs to replace)")
                    continue
                if not dry_run:
                    shutil.rmtree(dest)

            skill_dirs  = _sv_filter_skill_dirs(best_skills)
            skill_names = sorted(d.name for d in skill_dirs)
            all_names   = sorted(p.name for p in best_skills.iterdir() if p.is_dir())
            note = (f", kept {len(skill_dirs)}/{len(all_names)} after round filter"
                    if len(skill_dirs) != len(all_names) else "")
            print(f"  [{'DRY' if dry_run else 'COPY'}] {config_name}/{task_name}"
                  f"  ({len(skill_names)} skill(s){note})")
            if not dry_run:
                dest.mkdir(parents=True, exist_ok=True)
                for skill_dir in skill_dirs:
                    shutil.copytree(skill_dir, dest / skill_dir.name)
            found_any = True

    # human_authored (from tasks/<task>/environment/skills/)
    oracle_dir = _sv_find_oracle_dir(task_name)
    if oracle_dir is not None:
        dest = SKILL_CONFIGS_DIR / "human_authored" / task_name
        if dest.exists() and not overwrite:
            print(f"  [EXISTS] human_authored/{task_name}  (use --overwrite-configs to replace)")
        else:
            skill_names = sorted(p.name for p in oracle_dir.iterdir() if p.is_dir())
            print(f"  [{'DRY' if dry_run else 'COPY'}] human_authored/{task_name}"
                  f"  ({len(skill_names)} skill(s))")
            if not dry_run:
                if dest.exists():
                    shutil.rmtree(dest)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(oracle_dir, dest)
        found_any = True
    else:
        print(f"  [WARN] No human_authored skills found for {task_name}")

    if not found_any:
        print(f"  [SKIP] Nothing to export for {task_name}")


def _organize_skill_configs(
        task_ids: list[str],
        *,
        overwrite: bool = False,
        dry_run: bool = False,
) -> None:
    """Organize skill artifacts for all completed tasks into output/skill_generation_results/."""
    print(f"\n[Post-step] Organizing skill configs → {SKILL_CONFIGS_DIR}")
    if dry_run:
        print("  (dry-run — nothing will be written)")
    for task_id in task_ids:
        task_name = Path(task_id).name  # handles both "task" and "task/task-N"
        print(f"  [{task_name}]")
        _sv_process_task(task_name, overwrite=overwrite, dry_run=dry_run)
    if not dry_run:
        print(f"  Done. Variants at: {SKILL_CONFIGS_DIR}")


# ── Main orchestrator ──────────────────────────────────────────────────────────

def hyper_run(
        task_ids: list[str],
        *,
        methods: list[str],
        models: list[str],
        artifact: str,
        max_steps: int,
        skills_only: bool,
        max_workers: int,
        build_workers: int,
        remove_images: bool,
        record: bool,
        dry_run: bool,
        extra_subtasks: int = 0,
        overwrite_configs: bool = False,
) -> int:
    specs = _collect_specs(task_ids, methods, models, extra_subtasks=extra_subtasks)

    if not specs:
        print("No trial specs collected.")
        return 0

    print(
        f"Planned: {len(specs)} run(s)  "
        f"({len(task_ids)} tasks × {len(methods)} methods × {len(models)} models)"
    )

    if dry_run:
        print("(dry-run — no commands will execute)\n")
        for spec in specs:
            print(
                f"  {spec['task_id']} | {spec['method']} | {spec['model']} "
                f"[{spec['agent_id']}]"
            )
        return 0

    # ── Phase 1: Pre-build one image per (task, agent) ────────────────────────
    unique_pairs = sorted({(s["task_id"], s["agent_id"]) for s in specs})
    print(
        f"\n[Phase 1] Ensuring {len(unique_pairs)} image(s) "
        f"(build_workers={build_workers})..."
    )

    tag_map: dict[tuple[str, str], str] = {}
    build_errors: dict[tuple[str, str], str] = {}

    def _build_and_record(pair: tuple[str, str]) -> None:
        task_id, agent_id = pair
        cached = _image_exists(_stable_tag(task_id, agent_id))
        tag, err = _build_one(task_id, agent_id)
        if err:
            _log(f"  [BUILD FAIL] {task_id} / {agent_id}: {err}")
            build_errors[pair] = err
        else:
            label = "[CACHED    ]" if cached else "[BUILD OK  ]"
            _log(f"  {label} {task_id} / {agent_id}  →  {tag}")
            tag_map[pair] = tag

    if build_workers == 1:
        for pair in unique_pairs:
            _build_and_record(pair)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=build_workers) as ex:
            concurrent.futures.wait(
                {ex.submit(_build_and_record, pair): pair for pair in unique_pairs}
            )

    if build_errors:
        print(f"\n[Phase 1] WARNING: {len(build_errors)} build(s) failed.")

    runnable = [s for s in specs if (s["task_id"], s["agent_id"]) in tag_map]
    skipped_build = len(specs) - len(runnable)
    if not runnable:
        print("No runnable trials after build phase.")
        return 1

    # Ensure per-config/per-task output directories exist before trials run.
    dirs_to_create = {(f"{s['method']}-{s['model']}", Path(s['task_id']).name) for s in runnable}
    for config_name, task_name in dirs_to_create:
        (TRIALS_DIR / config_name / task_name).mkdir(parents=True, exist_ok=True)

    # ── Phase 2: Run all trials ────────────────────────────────────────────────
    print(f"\n[Phase 2] Running {len(runnable)} trial(s) (max_workers={max_workers})...")

    all_results: list[dict] = []
    results_lock = threading.Lock()

    phase2_kwargs = dict(
        max_workers=max_workers,
        tag_map=tag_map,
        artifact=artifact,
        max_steps=max_steps,
        skills_only=skills_only,
        record=record,
        all_results=all_results,
        results_lock=results_lock,
    )
    if _RICH:
        _phase2_rich(runnable, **phase2_kwargs)
    else:
        _phase2_plain(runnable, **phase2_kwargs)

    # ── Phase 3: Cleanup ──────────────────────────────────────────────────────
    if remove_images and tag_map:
        print(f"\n[Phase 3] Removing {len(tag_map)} prebuilt image(s)...")
        for tag in tag_map.values():
            subprocess.run(["docker", "rmi", "-f", tag], capture_output=True)

    if skipped_build:
        print(f"\nBuild failures: {skipped_build} trial(s) not run")

    # ── Post-step: organize skill configs ────────────────────────────────────
    _organize_skill_configs(task_ids, overwrite=overwrite_configs, dry_run=dry_run)

    return 0


# ── CLI ────────────────────────────────────────────────────────────────────────

def main() -> int:
    _load_dotenv()
    _warn_provider_keys()
    _require_docker()

    parser = argparse.ArgumentParser(
        description=(
            "Parallel Docker skill-generation runner.\n"
            "Phase 1: pre-build images; Phase 2: run all combos in parallel; "
            "Phase 3: optional cleanup."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--tasks", nargs="+", default=None, metavar="TASK_ID",
        help=f"Task IDs to run (default: all {len(DEFAULT_TASKS)} tasks in DEFAULT_TASKS)",
    )
    parser.add_argument(
        "--methods", nargs="+", default=None, metavar="METHOD",
        help=f"Methods to run (default: all {len(DEFAULT_METHODS)}). "
             f"Choices: {', '.join(DEFAULT_METHODS)}",
    )
    parser.add_argument(
        "--models", nargs="+", default=None, metavar="MODEL",
        help=f"Models to run (default: all {len(DEFAULT_MODELS)}). "
             f"Choices: {', '.join(DEFAULT_MODELS)}",
    )
    parser.add_argument(
        "--artifact", default=DEFAULT_ARTIFACT, metavar="PATH",
        help=f"Container path to copy out after each run (default: {DEFAULT_ARTIFACT})",
    )
    parser.add_argument(
        "--max-steps", type=int, default=100, metavar="N",
        help="Max tool-use steps per agent run (default: 100)",
    )
    parser.add_argument(
        "--num-subtasks", type=int, default=1, metavar="N",
        help=(
            "Number of subtask instructions to feed for skill generation "
            "(default: 1 = target subtask only). E.g. --num-subtasks 2 also "
            "feeds subtask-2 alongside the target (subtask-1)."
        ),
    )
    parser.add_argument(
        "--full-run", action="store_true",
        help="[NOT RECOMMENDED] Disable skills-only mode and run the full agent + verifier loop. "
             "Skills-only is the correct mode for Phase 1; full-run is provided only for debugging. "
             "b1/b4 normally interrupt early and skip the verifier; b2 skips the verifier after a "
             "full agent run; b3 is unaffected (verifier feeds the teacher regardless).",
    )
    parser.add_argument(
        "--max-workers", type=int, default=10,
        help="Parallel trial workers (default: 10)",
    )
    parser.add_argument(
        "--build-workers", type=int, default=3,
        help="Parallel image build workers (default: 3)",
    )
    parser.add_argument(
        "--remove-images", action="store_true",
        help="Remove prebuilt images after run (default: keep for reuse)",
    )
    parser.add_argument(
        "--no-record", action="store_true",
        help="Skip writing per-trial result.json",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print planned runs without executing",
    )
    parser.add_argument(
        "--overwrite-configs", action="store_true",
        help="Overwrite existing entries in output/skill_generation_results/ when organizing",
    )

    args = parser.parse_args()

    task_ids = args.tasks or DEFAULT_TASKS
    methods = args.methods or DEFAULT_METHODS
    models = args.models or DEFAULT_MODELS

    # Validate models: infer provider from prefix, then verify the API key works
    unroutable = [m for m in models if not _infer_agent(m)]
    if unroutable:
        print(f"Cannot determine provider for model(s): {', '.join(unroutable)}", file=sys.stderr)
        print("Model names must start with 'claude-' or 'gemini-'", file=sys.stderr)
        return 2

    providers_needed: set[str] = set()
    for m in models:
        if m.startswith("claude-"):
            providers_needed.add("anthropic")
        elif m.startswith("gemini-"):
            providers_needed.add("gemini")
    for provider in sorted(providers_needed):
        ok, msg = _check_api_key(provider)
        if not ok:
            print(f"API key check failed [{provider}]: {msg}", file=sys.stderr)
            return 2

    return hyper_run(
        task_ids,
        methods=methods,
        models=models,
        artifact=args.artifact,
        max_steps=args.max_steps,
        skills_only=not args.full_run,
        max_workers=max(1, args.max_workers),
        build_workers=max(1, args.build_workers),
        remove_images=args.remove_images,
        record=not args.no_record,
        dry_run=args.dry_run,
        extra_subtasks=args.num_subtasks - 1,
        overwrite_configs=args.overwrite_configs,
    )


if __name__ == "__main__":
    sys.exit(main())
