#!/usr/bin/env python3
"""
Parallel Docker eval runner with per-task image reuse and live progress display.

Phase 1 – Pre-build: one Docker image per *task* (empty skills dir).
          Skips build if stable tag already exists locally.
Phase 2 – Run: all trials in parallel with two-level rich progress display.
          run_task() injects skills at runtime → same container state as baking.
Phase 3 – Cleanup: remove stable images only if --remove-images is passed.
          Default: keep images for reuse across runs.

Usage examples:
    python evaluate_skills.py                                           # all tasks, human_authored (default)
    python evaluate_skills.py task1 task2                               # specific tasks, human_authored
    python evaluate_skills.py --skill-path output/skill_generation_results/b1-one-shot-claude-sonnet-4-6
    python evaluate_skills.py --skill-path output/skill_generation_results/b1-one-shot-claude-sonnet-4-6 none
    python evaluate_skills.py --repeats 3 --max-workers 10 --build-workers 3
    python evaluate_skills.py --remove-images              # clean up images after run
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
from collections import deque
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


def _require_anthropic_key(timeout: float = 10.0) -> None:
    """Fail fast if ANTHROPIC_API_KEY is missing or cannot authenticate with the Anthropic API."""
    import urllib.error
    import urllib.request

    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key or _PLACEHOLDER_KEY_RE.match(key):
        raise SystemExit(
            "ERROR: ANTHROPIC_API_KEY is not set (or is still a `.env.example` placeholder).\n"
            "The evaluation agent calls the Anthropic API — export ANTHROPIC_API_KEY or put it in .env."
        )

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/models?limit=1",
        headers={
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                raise SystemExit(
                    f"ERROR: Anthropic API ping returned HTTP {resp.status}. "
                    "Check your ANTHROPIC_API_KEY."
                )
    except urllib.error.HTTPError as exc:
        raise SystemExit(
            f"ERROR: Anthropic API rejected the key (HTTP {exc.code} {exc.reason}).\n"
            "Check that ANTHROPIC_API_KEY is valid and active."
        ) from exc
    except urllib.error.URLError as exc:
        raise SystemExit(
            f"ERROR: Cannot reach Anthropic API ({exc.reason}).\n"
            "Check your network connection / proxy settings."
        ) from exc

sys.path.insert(0, str(Path(__file__).parent))

from agents import get_agent
from core.eval_runner import (
    TASKS_DIR,
    TRIALS_DIR,
    SKILL_CONFIGS_DIR,
    _expand_subtask_range,
    _load_dotenv,
    _load_task_config,
    _parse_skill_copies,
    list_tasks,
    run_task,
)


_PLACEHOLDER_RE = re.compile(r"^your-.*-here$", re.IGNORECASE)


def _is_placeholder_key(value: str | None) -> bool:
    """Treat missing, empty, or `.env.example`-style `your-*-here` values as unset."""
    if not value or not value.strip():
        return True
    return bool(_PLACEHOLDER_RE.match(value.strip()))


def _validate_api_keys(
    *,
    agent_id: str,
    task_ids: list[str],
    task_root: Path,
    need_agent_keys: bool,
    need_judge_key: bool,
) -> None:
    """Fail fast if any required API key is missing or still a `.env.example` placeholder.

    Checks:
      - agent env vars (e.g. ANTHROPIC_API_KEY for claude-code, OPENAI_API_KEY for codex)
      - per-task required_env from task.toml (e.g. GH_TOKEN for github-repo-analytics)
      - OPENAI_API_KEY when the metrics pipeline (LLM-as-judge) will run
    """
    required: dict[str, list[str]] = {}

    if need_agent_keys:
        agent = get_agent(agent_id) or {}
        for var in agent.get("env", []) or []:
            required.setdefault(var, []).append(f"agent '{agent_id}'")
        for tid in task_ids:
            cfg = _load_task_config(task_root / tid)
            for var in cfg.get("environment", {}).get("required_env", []) or []:
                required.setdefault(var, []).append(f"task '{tid}'")

    if need_judge_key:
        required.setdefault("OPENAI_API_KEY", []).append(
            "metrics pipeline (LLM-as-judge) — use --skip-metrics to disable"
        )

    missing = [
        (var, reasons) for var, reasons in required.items()
        if _is_placeholder_key(os.environ.get(var))
    ]
    if not missing:
        return

    env_file = Path(__file__).parent / ".env"
    lines = ["ERROR: missing or placeholder API key(s) in environment / .env:"]
    for var, reasons in missing:
        cur = os.environ.get(var)
        status = "not set" if not cur else f"placeholder value ({cur!r})"
        lines.append(f"  - {var}: {status}")
        for reason in reasons:
            lines.append(f"      required by: {reason}")
    lines.append("")
    lines.append(f"Fix: put real key(s) in {env_file} (or export them) and re-run.")
    raise SystemExit("\n".join(lines))

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
# Allows worker threads to suppress their own print() output (e.g. run_task's
# step banners) without affecting the main thread or each other.

class _ThreadLocalStdout(io.TextIOBase):
    """
    Wraps sys.stdout so that each worker thread can silently capture its own
    print() output. Threads that haven't called .capture() pass through to
    the real stdout unchanged.
    """
    def __init__(self, real: io.TextIOBase) -> None:
        self._real = real
        self._local = threading.local()

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

    Each 'type':'assistant' JSON line in the claude-code trajectory log
    represents one completed LLM API call (one agent turn).

    Metrics exposed:
      .qps()         — rolling calls/sec over the last WINDOW_SECS seconds
      .total_calls() — total API calls seen since monitor started
    """
    WINDOW_SECS = 30   # sliding window for QPS
    POLL_SECS   = 1.0  # scan interval

    def __init__(self, trials_dir: Path, run_start: float) -> None:
        self._trials_dir = trials_dir
        self._run_start  = run_start       # wall-clock time; ignore older files
        self._lock        = threading.Lock()
        self._file_offset: dict[Path, int]  = {}   # file → lines already counted
        self._call_times:  list[float]      = []   # monotonic timestamps of API calls
        self._stop        = threading.Event()
        self._thread      = threading.Thread(
            target=self._loop, daemon=True, name="qps-monitor"
        )

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()

    def qps(self) -> float:
        """Calls per second over the last WINDOW_SECS seconds."""
        now    = time.monotonic()
        cutoff = now - self.WINDOW_SECS
        with self._lock:
            self._call_times = [t for t in self._call_times if t > cutoff]
            return len(self._call_times) / self.WINDOW_SECS

    def total_calls(self) -> int:
        with self._lock:
            return len(self._call_times)

    # ── internal ──────────────────────────────────────────────────────────────

    def _loop(self) -> None:
        while not self._stop.wait(self.POLL_SECS):
            self._scan()

    def _scan(self) -> None:
        now = time.monotonic()
        try:
            log_files = list(self._trials_dir.rglob("agent/claude-code.txt"))
        except Exception:
            return
        for log_path in log_files:
            try:
                # Skip files that predate this run (leftovers from previous runs)
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
            except Exception:
                pass


# ── Helpers ────────────────────────────────────────────────────────────────────

def _task_name(task_id: str) -> str:
    """Extract task-level name from a query task_id ('task/task-N' → 'task')."""
    return Path(task_id).parts[0]


# ── Stable tag: one per task ───────────────────────────────────────────────────

def _stable_tag(task_id: str) -> str:
    safe = re.sub(r"[^a-z0-9._-]", "-", task_id.lower())
    safe = re.sub(r"-{2,}", "-", safe).strip("-")
    return f"eval-hyper-{safe}:stable"


def _image_exists(tag: str) -> bool:
    r = subprocess.run(["docker", "image", "inspect", tag], capture_output=True)
    return r.returncode == 0


# ── Base image build ───────────────────────────────────────────────────────────

def _prepare_base_build_env(env_dir: Path) -> Path:
    """
    Build context for the per-task base image: empty skills dir with stub
    subdirectories for any 'COPY skills/<subdir>' Dockerfile instructions.

    Oracle skills from env_dir/skills/ are excluded at copy time so they can
    never accidentally end up in the base image regardless of rmtree failures.
    """
    tmp_root = Path(tempfile.mkdtemp(prefix="evaluation_base_"))
    build_env = tmp_root / "environment"
    shutil.copytree(env_dir, build_env, ignore=shutil.ignore_patterns("skills"))

    skills_dir = build_env / "skills"
    skills_dir.mkdir(parents=True)

    dockerfile = build_env / "Dockerfile"
    for src_pattern, _ in _parse_skill_copies(dockerfile):
        if src_pattern.startswith("skills/"):
            stub = skills_dir / src_pattern[len("skills/"):]
            stub.mkdir(parents=True, exist_ok=True)

    return build_env


def _build_one(task_id: str, task_root: Path, agent_id: str) -> tuple[str, str | None]:
    """
    Ensure the per-task agent-ready image exists.
    Two-layer build:
      Layer 1: task base environment (from task Dockerfile, empty skills)
      Layer 2: Node 20 + agent CLI baked on top
    Skips both layers if the stable tag already exists locally.
    Returns (tag, error_message_or_None).
    """
    tag = _stable_tag(task_id)
    if _image_exists(tag):
        return tag, None  # reuse cached image

    agent = get_agent(agent_id)
    if not agent:
        return tag, f"unknown agent: {agent_id}"

    base_tag = f"{tag}-base"
    env_dir = task_root / task_id / (task_id + "-1") / "environment"
    build_root = None
    try:
        # Layer 1: task environment (empty skills)
        build_env = _prepare_base_build_env(env_dir)
        build_root = build_env.parent
        r = subprocess.run(
            ["docker", "build", "-t", base_tag, str(build_env)],
            capture_output=True, text=True,
        )
        if r.returncode != 0:
            snippet = (r.stderr or r.stdout or "")[:400].strip()
            return tag, f"base build failed: {snippet}"

        # Layer 2: install Node 20 + agent CLI on top of task base
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

        # Clean up intermediate base image
        subprocess.run(["docker", "rmi", "-f", base_tag], capture_output=True)
        return tag, None
    except Exception as exc:
        return tag, str(exc)
    finally:
        if build_root and build_root.exists():
            shutil.rmtree(build_root, ignore_errors=True)


# ── Spec collection ────────────────────────────────────────────────────────────

def _collect_specs(
    task_ids: list[str],
    task_root: Path,
    skill_paths: list[Path | None],
    repeats: int,
) -> tuple[list[dict], list[dict]]:
    """Collect trial specs for the given task_ids / skill_paths / repeats.

    Each skill_path is an absolute path to a skill config dir, e.g.
    output/skill_generation_results/b1-one-shot-claude-sonnet-4-6.
    The config key used for output naming is skill_path.name.
    None entries in skill_paths represent the no_skill config (no skill files injected).
    """
    specs: list[dict] = []
    skipped: list[dict] = []
    for task_id in task_ids:
        task_path = task_root / task_id
        task_name = task_path.parent.name  # e.g. 'github-repo-analytics'
        for rep in range(repeats):
            for skill_path in skill_paths:
                if skill_path is None:
                    specs.append({"task_id": task_id, "skill_config": "no_skill",
                                  "skill_source_dir": None, "repeat": rep + 1})
                    continue
                config_name = skill_path.name
                d = skill_path / task_name
                skill_source = d if d.exists() and d.is_dir() else None
                if skill_source is None:
                    skipped.append({"task_id": task_id, "skill_config": config_name,
                                    "repeat": rep + 1, "reason": "missing_skill_source"})
                    continue
                specs.append({"task_id": task_id, "skill_config": config_name,
                              "skill_source_dir": skill_source, "repeat": rep + 1})
    return specs, skipped


def _collect_specs_from_config(
    config_path: Path,
    task_root: Path,
) -> tuple[list[dict], list[dict]]:
    """Collect trial specs from a job-config JSON file.

    Config format — JSON array of entries, each with:
      task     (str)        task_id, e.g. "citation-check/citation-check-1"
      configs (list[str])  config names, e.g. ["human_authored", "b1-one-shot-claude-sonnet-4-6", "no_skill"]
      repeats  (int)        how many runs to schedule per config (default: 1)

    Variant names are resolved to paths under output/skill_generation_results/.
    """
    with open(config_path, encoding="utf-8") as fh:
        config: list[dict] = json.load(fh)

    specs: list[dict] = []
    skipped: list[dict] = []

    for entry in config:
        task_id       = str(entry["task"])
        config_names = list(entry.get("configs", ["human_authored"]))
        repeats       = int(entry.get("repeats", 1))
        task_path = task_root / task_id
        task_name = task_path.parent.name

        for rep in range(repeats):
            for config_name in config_names:
                if config_name == "no_skill":
                    # no_skill has no directory — run without injecting any skills
                    specs.append({"task_id": task_id, "skill_config": "no_skill",
                                  "skill_source_dir": None, "repeat": rep + 1})
                    continue
                skill_path = SKILL_CONFIGS_DIR / config_name
                d = skill_path / task_name
                skill_source = d if d.exists() and d.is_dir() else None
                if skill_source is None:
                    skipped.append({"task_id": task_id, "skill_config": config_name,
                                    "repeat": rep + 1, "reason": "missing_skill_source"})
                    continue
                specs.append({"task_id": task_id, "skill_config": config_name,
                              "skill_source_dir": skill_source, "repeat": rep + 1})

    return specs, skipped


# ── Phase 2 runners ────────────────────────────────────────────────────────────

def _phase2_plain(
    runnable: list[dict],
    max_workers: int,
    tag_map: dict[str, str],
    agent_id: str,
    model: str | None,
    record: bool,
    task_root: Path,
    max_steps: int,
    all_results: list[dict],
    results_lock: threading.Lock,
    trials_dir: Path = TRIALS_DIR,
) -> None:
    """Fallback: plain output, no rich dependency."""
    def _run_one(spec: dict) -> None:
        _, res = run_task(
            spec["task_id"], task_root=task_root, agent_id=agent_id, model=model,
            record=record, skill_config=spec["skill_config"],
            skill_source_dir=spec["skill_source_dir"], max_steps=max_steps,
            prebuilt_image_tag=tag_map[_task_name(spec["task_id"])],
            prebuilt_has_agent=True,
            trials_dir=trials_dir,
        )
        with results_lock:
            all_results.append(res)

    if max_workers == 1:
        for spec in runnable:
            _run_one(spec)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
            concurrent.futures.wait({ex.submit(_run_one, spec): spec for spec in runnable})


def _phase2_rich(
    runnable: list[dict],
    max_workers: int,
    tag_map: dict[str, str],
    agent_id: str,
    model: str | None,
    record: bool,
    task_root: Path,
    max_steps: int,
    all_results: list[dict],
    results_lock: threading.Lock,
    trials_dir: Path = TRIALS_DIR,
) -> None:
    """
    Phase 2 with two-level rich progress display.

    Layout:
      Overall  [████████░░░░] 45/546  ETA 9:23
        Worker 0  ⠸ task-a / human_authored            1:23
        Worker 1  ⠴ task-b / b1-one-shot-...          0:45
        Worker 2  · [idle]
        ...
    """
    # Save real stdout BEFORE replacing it, so rich renders to the actual terminal.
    # Worker threads' print() calls are captured by _ThreadLocalStdout and discarded.
    real_stdout = sys.stdout
    tl_stdout = _ThreadLocalStdout(real_stdout)
    sys.stdout = tl_stdout  # type: ignore[assignment]

    # Explicit console pointing to real_stdout so rich's isatty() check succeeds.
    _console = RichConsole(file=real_stdout)

    overall_p = Progress(
        TextColumn("{task.description}"),   # dynamic: updated by QPS thread
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

    overall_task_id = overall_p.add_task("[bold green]Overall[/bold green]", total=len(runnable))
    worker_task_ids = [
        worker_p.add_task(f"[dim]Worker {i:2d}  · idle[/dim]", start=False)
        for i in range(max_workers)
    ]

    free_slots: deque[int] = deque(range(max_workers))
    slot_lock = threading.Lock()

    # ── API QPS monitor ────────────────────────────────────────────────────────
    monitor = ApiQpsMonitor(trials_dir, run_start=time.time())
    monitor.start()

    _qps_stop = threading.Event()

    def _qps_updater() -> None:
        """Refresh the overall-bar description with live QPS every 2 s."""
        while not _qps_stop.wait(2.0):
            qps   = monitor.qps()
            total = monitor.total_calls()
            # Count busy workers (slots currently checked out)
            with slot_lock:
                busy = max_workers - len(free_slots)
            # Warn if all workers are active but QPS is suspiciously low
            # (possible external rate-limit / throttling)
            throttled = busy >= max(2, max_workers // 2) and qps < 0.3
            qps_color = "yellow" if throttled else "green"
            warn      = " [yellow]⚠ throttled?[/yellow]" if throttled else ""
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

    def _shorten_config(v: str, maxlen: int = 42) -> str:
        if len(v) <= maxlen:
            return v
        return "…" + v[-(maxlen - 1):]

    def _run_one(spec: dict) -> None:
        tl_stdout.capture()  # silence this thread's prints
        with slot_lock:
            slot = free_slots.popleft()

        config_str = _shorten_config(spec["skill_config"])
        desc = (
            f"[dim]Worker {slot:2d}[/dim]  "
            f"[cyan]{spec['task_id']}[/cyan] / {config_str}"
        )
        worker_p.reset(worker_task_ids[slot], start=False)  # clears start_time so timer resets
        worker_p._tasks[worker_task_ids[slot]].stop_time = None  # workaround: reset() doesn't clear stop_time in this Rich version
        worker_p.update(worker_task_ids[slot], description=desc)
        worker_p.start_task(worker_task_ids[slot])

        try:
            _, res = run_task(
                spec["task_id"], task_root=task_root, agent_id=agent_id, model=model,
                record=record, skill_config=spec["skill_config"],
                skill_source_dir=spec["skill_source_dir"], max_steps=max_steps,
                prebuilt_image_tag=tag_map[_task_name(spec["task_id"])],
                prebuilt_has_agent=True,
                trials_dir=trials_dir,
            )
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
    try:
        with Live(group, console=_console, refresh_per_second=4, transient=False, redirect_stdout=False):
            if max_workers == 1:
                for spec in runnable:
                    _run_one(spec)
            else:
                with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
                    concurrent.futures.wait(
                        {ex.submit(_run_one, spec): spec for spec in runnable}
                    )
    finally:
        _qps_stop.set()
        monitor.stop()
        sys.stdout = tl_stdout._real  # always restore real stdout


# ── Main orchestrator ──────────────────────────────────────────────────────────

def hyper_eval(
    task_ids: list[str],
    *,
    task_root: Path,
    agent_id: str,
    model: str | None,
    skill_paths: list[Path | None],
    repeats: int,
    max_steps: int,
    max_workers: int,
    build_workers: int,
    remove_images: bool,
    record: bool,
    dry_run: bool = False,
    config_path: Path | None = None,
    trials_dir: Path = TRIALS_DIR,
) -> int:
    if config_path is not None:
        specs, skipped = _collect_specs_from_config(config_path, task_root)
    else:
        specs, skipped = _collect_specs(task_ids, task_root, skill_paths, repeats)

    if not specs:
        print("No trial specs collected.")
        if skipped:
            print(f"Skipped {len(skipped)} spec(s) due to missing skill sources.")
        return 0

    config_names = sorted({s["skill_config"] for s in specs})
    dry_note = " (dry-run)" if dry_run else ""
    if config_path is not None:
        print(f"Collected {len(specs)} trial spec(s){dry_note} from job-config: {config_path.name}.")
    else:
        print(
            f"Collected {len(specs)} trial spec(s){dry_note} "
            f"({len(task_ids)} task(s), {repeats} repeat(s), skill configs: {', '.join(config_names)})."
        )
    if skipped:
        print(f"\n[WARN] {len(skipped)} spec(s) will be skipped — skill source directory not found:")
        # Group by (task_id, skill_config) and count repeats
        _skip_counts: dict[tuple[str, str], int] = {}
        for s in skipped:
            key = (s["task_id"], s["skill_config"])
            _skip_counts[key] = _skip_counts.get(key, 0) + 1
        for (tid, cfg), cnt in sorted(_skip_counts.items()):
            rep_note = f"  (×{cnt} repeat(s))" if cnt > 1 else ""
            print(f"  SKIP  {tid}  /  {cfg}{rep_note}")

    if dry_run:
        print()
        unique_tasks_dry = sorted({_task_name(spec["task_id"]) for spec in specs})
        print(f"Would build {len(unique_tasks_dry)} image(s):")
        for tid in unique_tasks_dry:
            print(f"  {_stable_tag(tid)}")
        print(f"\nWould run {len(specs)} trial(s):")
        for spec in specs:
            print(f"  {spec['task_id']}  /  {spec['skill_config']}  (repeat {spec['repeat']})")
        return 0

    # ── Phase 1: Pre-build one image per task (keyed by task-level name) ─────────
    unique_tasks = sorted({_task_name(spec["task_id"]) for spec in specs})
    print(
        f"\n[Phase 1] Ensuring {len(unique_tasks)} task image(s) "
        f"(build_workers={build_workers})..."
    )

    tag_map: dict[str, str] = {}   # task_name → image tag
    build_errors: dict[str, str] = {}

    def _build_and_record(task_name: str) -> None:
        cached = _image_exists(_stable_tag(task_name))
        tag, err = _build_one(task_name, task_root, agent_id)
        if err:
            _log(f"  [BUILD FAIL] {task_name}: {err}")
            build_errors[task_name] = err
        else:
            label = "[CACHED    ]" if cached else "[BUILD OK  ]"
            _log(f"  {label} {task_name}  ->  {tag}")
            tag_map[task_name] = tag

    if build_workers == 1:
        for tid in unique_tasks:
            _build_and_record(tid)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=build_workers) as ex:
            concurrent.futures.wait(
                {ex.submit(_build_and_record, tid): tid for tid in unique_tasks}
            )

    if build_errors:
        print(f"\n[Phase 1] WARNING: {len(build_errors)} build(s) failed.")

    runnable = [s for s in specs if _task_name(s["task_id"]) in tag_map]
    skipped_build = len(specs) - len(runnable)
    if not runnable:
        print("No runnable trials after build phase.")
        return 1

    # Ensure per-config/per-task output directories exist before trials run.
    for spec in runnable:
        config = spec["skill_config"]
        task_name = _task_name(spec["task_id"])
        (trials_dir / config / task_name).mkdir(parents=True, exist_ok=True)

    # ── Phase 2: Run all trials ────────────────────────────────────────────────
    print(f"\n[Phase 2] Running {len(runnable)} trial(s) (max_workers={max_workers})...")

    all_results: list[dict] = []
    results_lock = threading.Lock()

    phase2_kwargs = dict(
        max_workers=max_workers,
        tag_map=tag_map,
        agent_id=agent_id,
        model=model,
        record=record,
        task_root=task_root,
        max_steps=max_steps,
        all_results=all_results,
        results_lock=results_lock,
        trials_dir=trials_dir,
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

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n=== Summary ===")
    exact_configs = sorted(
        {str(r.get("skill_config")) for r in all_results if r.get("skill_config")}
    )
    for config in exact_configs:
        rows = [r for r in all_results if r.get("skill_config") == config]
        total = len(rows)
        passed = sum(1 for r in rows if r.get("passed") is True)
        pct = f"{passed / total:.2%}" if total else "n/a"
        print(f"  {config}: {passed}/{total} ({pct})")

    total_all = len(all_results)
    passed_all = sum(1 for r in all_results if r.get("passed") is True)
    rate_all = passed_all / total_all if total_all else 0.0
    print(f"\nOverall: {passed_all}/{total_all} ({rate_all:.2%})")
    if skipped_build:
        print(f"Build failures: {skipped_build} trial(s) not run")
    if skipped:
        print(f"\nSkipped (no skill source): {len(skipped)} spec(s)")
        _skip_counts2: dict[tuple[str, str], int] = {}
        for s in skipped:
            key = (s["task_id"], s["skill_config"])
            _skip_counts2[key] = _skip_counts2.get(key, 0) + 1
        for (tid, cfg), cnt in sorted(_skip_counts2.items()):
            rep_note = f"  (×{cnt} repeat(s))" if cnt > 1 else ""
            print(f"  SKIP  {tid}  /  {cfg}{rep_note}")

    return 0


# ── Skill path helpers ────────────────────────────────────────────────────────

_SKILL_REFERENCE_DIR = Path(__file__).parent / "skills"


def _resolve_skill_paths(raw_paths: list[str] | None) -> list[Path | None]:
    """Resolve --skill-path arguments to absolute Path objects (or None for no_skill).

    Relative paths are resolved from the GenSkillBench root (directory of this file).
    The special value "none" (case-insensitive) maps to None, meaning no skills injected.
    If no paths given, defaults to output/skill_generation_results/human_authored.
    """
    base = Path(__file__).parent
    if not raw_paths:
        return [SKILL_CONFIGS_DIR / "human_authored"]
    paths: list[Path | None] = []
    for raw in raw_paths:
        if raw.lower() == "none":
            paths.append(None)
        else:
            p = Path(raw)
            if not p.is_absolute():
                p = base / p
            paths.append(p.resolve())
    return paths


def _ensure_skill_paths(skill_paths: list[Path | None], task_ids: list[str]) -> None:
    """Auto-fill from skills/ for human_authored if task dir is missing."""
    parent_tasks = _to_parent_tasks(task_ids)
    for skill_path in skill_paths:
        if skill_path is None:
            continue  # no_skill has no directory
        for task in parent_tasks:
            dest = skill_path / task
            if dest.exists():
                continue
            # Auto-fill human_authored from skills/ if available
            if skill_path.name == "human_authored":
                src = _SKILL_REFERENCE_DIR / "human_authored" / task
                if src.exists():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copytree(src, dest)
                    print(f"[auto-fill] human_authored/{task}  (copied from skills/)")


# ── Metrics pipeline ──────────────────────────────────────────────────────────

def _to_parent_tasks(task_ids: list[str]) -> list[str]:
    """Extract unique task-level names from query task_ids ('task/task-N' → 'task')."""
    return sorted({_task_name(tid) for tid in task_ids})


def _aggregate_csvs(src_paths: list[Path], out_path: Path) -> None:
    """Concatenate multiple CSV files into one, writing the header once."""
    import csv
    rows: list[list] = []
    header: list | None = None
    for p in src_paths:
        if not p.exists():
            continue
        with open(p, newline="", encoding="utf-8") as fh:
            reader = csv.reader(fh)
            lines = list(reader)
        if not lines:
            continue
        if header is None:
            header = lines[0]
        rows.extend(lines[1:])
    if header is None:
        return
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(header)
        writer.writerows(rows)


# ── Report aggregation ────────────────────────────────────────────────────────
#
# The final report.csv rolls each metric up to a single scalar:
#   step 1: average all rows within a Task (per-metric)
#   step 2: average those task means across tasks (equal weight per task)
#   step 3: per-metric normalization to a comparable 0–100 scale (where applicable)
#
# Normalization kinds:
#   "scale_1_5": LLM rubric scores in [1,5]  → (x-1)/4 * 100  → [0,100]
#   "ratio":     proportion in [0,1]          → x * 100        → [0,100]
#   "count":     counts / token totals        → no scaling (raw mean)

_REPORT_TRAJECTORY_METRICS: dict[str, str] = {
    "pass":                         "ratio",
    "skill_invocation_ratio":       "ratio",
    "num_steps":                    "count",
    "num_tool_calls":               "count",
    "num_skill_calls":              "count",
    "input_tokens":                 "count",
    "output_tokens":                "count",
    "num_skills_invoked":           "count",
    "num_skills_total":             "count",
    "execution_order":              "scale_1_5",
    "completeness":                 "scale_1_5",
    "trajectory_key_point_recall":  "ratio",
}
_REPORT_SKILL_QUALITY_METRICS: dict[str, str] = {
    "executability_completeness":           "scale_1_5",
    "executability_consistency":            "scale_1_5",
    "executability_determinism":            "scale_1_5",
    "executability_usability":              "scale_1_5",
    "safety_bias_or_discrimination":        "scale_1_5",
    "safety_data_privacy":                  "scale_1_5",
    "safety_illegal_or_offensive_content":  "scale_1_5",
    "safety_prompt_injection":              "scale_1_5",
    "safety_system_integrity":              "scale_1_5",
    "safety_untrusted_communication":       "scale_1_5",
}
_REPORT_COVERAGE_METRICS: dict[str, str] = {
    "coverage": "ratio",
}


def _normalize_metric(kind: str, mean_val: float) -> float:
    if kind == "scale_1_5":
        return (mean_val - 1.0) / 4.0 * 100.0
    if kind == "ratio":
        return mean_val * 100.0
    return mean_val  # count


def _collect_task_then_overall_means(
    csv_path: Path, metric_keys: list[str],
) -> dict[str, float]:
    """Mean within-Task, then mean across-Task. Requires a ``Task`` column in the CSV."""
    import csv
    per_task: dict[str, dict[str, list[float]]] = {}
    if not csv_path.exists():
        return {}
    with csv_path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            task = (row.get("Task") or "").strip()
            if not task:
                continue
            bucket = per_task.setdefault(task, {})
            for k in metric_keys:
                raw = row.get(k)
                if raw is None or raw == "":
                    continue
                try:
                    bucket.setdefault(k, []).append(float(raw))
                except ValueError:
                    pass
    task_means: dict[str, dict[str, float]] = {
        t: {k: sum(vs) / len(vs) for k, vs in ms.items() if vs}
        for t, ms in per_task.items()
    }
    out: dict[str, float] = {}
    for k in metric_keys:
        vals = [tm[k] for tm in task_means.values() if k in tm]
        if vals:
            out[k] = sum(vals) / len(vals)
    return out


_VENDOR_TOKENS = {"claude", "gpt", "gemini", "qwen", "llama", "deepseek", "mistral"}


def _parse_config_llm_method(config: str) -> tuple[str, str]:
    """Split a config key into (LLM, Method). Mirrors build_metrics_csv._parse_config."""
    if config in ("human_authored", "no_skill"):
        return config, ""
    tokens = config.split("-")
    for i, tok in enumerate(tokens):
        if tok in _VENDOR_TOKENS:
            llm = "-".join(tokens[i:])
            method = "-".join(tokens[:i]) if i > 0 else ""
            return llm, method
    return "", config


def _build_skill_coverage_csv(
    config: str, active_tasks: list[str], reports_dir: Path,
) -> Path:
    """Aggregate per-query key_points.metrics.json into a single skill-coverage CSV.

    Coverage is computed once per query (compute_coverage.py runs per query against
    that query's key points). Emit one row per (task, query, run_id).
    """
    import csv
    out_path = reports_dir / config / "skill-coverage-evaluation.csv"
    columns = ["LLM", "Method", "Task", "Query", "run_id", "coverage", "total_key_points"]
    rows: list[dict] = []
    for task in active_tasks:
        task_dir = reports_dir / config / task
        if not task_dir.is_dir():
            continue
        for query_dir in sorted(p for p in task_dir.iterdir() if p.is_dir()):
            kp_file = query_dir / "key_points.metrics.json"
            if not kp_file.exists():
                continue
            try:
                data = json.loads(kp_file.read_text(encoding="utf-8", errors="replace"))
            except json.JSONDecodeError:
                continue
            if not isinstance(data, dict):
                continue
            by_config = data.get("by_config") or {}
            if not isinstance(by_config, dict):
                continue
            for cfg_name, cfg_row in by_config.items():
                if not isinstance(cfg_row, dict):
                    continue
                llm, method = _parse_config_llm_method(str(cfg_name))
                by_run = cfg_row.get("by_run") or {}
                if not isinstance(by_run, dict):
                    continue
                for run_id, r in by_run.items():
                    if not isinstance(r, dict):
                        continue
                    rows.append({
                        "LLM": llm,
                        "Method": method,
                        "Task": task,
                        "Query": query_dir.name,
                        "run_id": run_id,
                        "coverage": r.get("coverage"),
                        "total_key_points": r.get("total_key_points"),
                    })
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    return out_path


def _write_report_csv(
    *, traj_csv: Path, skill_csv: Path, coverage_csv: Path, out_path: Path,
) -> None:
    """Single-row report.csv: task-inner mean → cross-task mean → per-metric normalization."""
    import csv

    traj_keys     = list(_REPORT_TRAJECTORY_METRICS.keys())
    quality_keys  = list(_REPORT_SKILL_QUALITY_METRICS.keys())
    coverage_keys = list(_REPORT_COVERAGE_METRICS.keys())

    traj_means     = _collect_task_then_overall_means(traj_csv,     traj_keys)
    quality_means  = _collect_task_then_overall_means(skill_csv,    quality_keys)
    coverage_means = _collect_task_then_overall_means(coverage_csv, coverage_keys)

    columns = traj_keys + quality_keys + coverage_keys
    row: dict[str, str] = {}
    for k in traj_keys:
        row[k] = (
            f"{_normalize_metric(_REPORT_TRAJECTORY_METRICS[k], traj_means[k]):.4f}"
            if k in traj_means else ""
        )
    for k in quality_keys:
        row[k] = (
            f"{_normalize_metric(_REPORT_SKILL_QUALITY_METRICS[k], quality_means[k]):.4f}"
            if k in quality_means else ""
        )
    for k in coverage_keys:
        row[k] = (
            f"{_normalize_metric(_REPORT_COVERAGE_METRICS[k], coverage_means[k]):.4f}"
            if k in coverage_means else ""
        )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns)
        writer.writeheader()
        writer.writerow(row)


def _run_metrics_pipeline(
    task_ids: list[str],
    skill_paths: list[Path | None],
    judge_model: str = "gpt-5-mini",
    dry_run: bool = False,
) -> None:
    """Run trajectory and skill metrics per skill_path after agent trials complete.

    For each skill_path (config key = skill_path.name, or 'no_skill' when None):
      Step 1: Trajectory metrics (per task) → evaluation_reports/<config>/<task>/<task>-trajectory-results.csv
              Then aggregate all tasks → evaluation_reports/<config>/trajectory-evaluation.csv
      Step 2: Skill metrics JSON (per subtask) → evaluation_reports/<config>/<task>/<subtask>/*.metrics.json
              (executability, safety, key_points — skipped for no_skill)
      Step 3: Skill metrics CSVs (per task) → evaluation_reports/<config>/<task>/<task>-skills-results.csv
              Then aggregate all tasks →
                evaluation_reports/<config>/skill-quality-evaluation.csv   (executability + safety, per query × skill)
                evaluation_reports/<config>/skill-coverage-evaluation.csv  (coverage,            per query × run)
      Final:  evaluation_reports/<config>/report.csv  — single-row summary
              (task-inner mean → cross-task mean → per-metric normalization)
    """
    parent_tasks = _to_parent_tasks(task_ids)
    if not parent_tasks:
        return

    gen_dir      = Path(__file__).parent
    traj_script  = gen_dir / "evaluation" / "trajectory" / "run_trajectory_eval.py"
    skill_script = gen_dir / "evaluation" / "skill" / "run_all_eval.py"
    csv_script   = gen_dir / "evaluation" / "skill" / "utils" / "build_metrics_csv.py"
    reports_dir  = gen_dir / "output" / "evaluation_reports"
    trials_dir   = gen_dir / "output" / "evaluation_log"

    for skill_path in skill_paths:
        config = "no_skill" if skill_path is None else skill_path.name

        # Only run metrics for tasks that have actual trial logs for this config.
        tasks_with_data = [
            task for task in parent_tasks
            if (trials_dir / config / task).is_dir()
            and any((trials_dir / config / task).iterdir())
        ]
        if not tasks_with_data:
            print(f"\n{'='*60}")
            print(f"Metrics pipeline — config: {config}  [SKIP — no trial logs found]")
            print(f"{'='*60}")
            continue

        print(f"\n{'='*60}")
        skipped_tasks = [t for t in parent_tasks if t not in tasks_with_data]
        suffix = (f"  ({len(skipped_tasks)} task(s) skipped — no trial logs)"
                  if skipped_tasks else "")
        print(f"Metrics pipeline — config: {config}  ({len(tasks_with_data)} task(s)){suffix}")
        print(f"{'='*60}")

        # Rebind parent_tasks to only the tasks with data for this config iteration.
        active_tasks = tasks_with_data

        # ── Step 1: Trajectory metrics ─────────────────────────────────────────
        # One subprocess per (config, task).
        # Reads from: evaluation_log/<config>/<task>/
        # Writes:     evaluation_reports/<config>/<task>/<task>-trajectory-results.csv
        print("\n[1/3] Trajectory metrics (LLM-as-judge)...")
        for task in active_tasks:
            cmd = [
                sys.executable, str(traj_script),
                "--config", config,
                "--task-id", task,
                "--model", judge_model,
                "--trials-root", str(trials_dir),
                "--results-root", str(reports_dir),
            ]
            print(f"  {task}: ", end="", flush=True)
            if dry_run:
                print(f"(dry-run) {' '.join(cmd)}")
            else:
                rc = subprocess.run(cmd).returncode
                print("ok" if rc == 0 else f"[warn] exit {rc}")

        # Aggregate trajectory CSVs across all tasks for this config
        traj_task_csvs = [
            reports_dir / config / task / f"{task}-trajectory-results.csv"
            for task in active_tasks
        ]
        agg_traj = reports_dir / config / "trajectory-evaluation.csv"
        if not dry_run:
            _aggregate_csvs(traj_task_csvs, agg_traj)
            print(f"  → aggregated: {agg_traj}")

        if config == "no_skill":
            # no skill files to evaluate
            print(f"\n[2/3] Skill metrics — skipped (no_skill has no skill files)")
            print(f"\n[3/3] Skill CSV — skipped")
            continue

        # ── Step 2: Skill metrics (JSON) ───────────────────────────────────────
        # One subprocess per config (covers all tasks).
        # Reads skill files from: skill_generation_results/<config>/<task>/
        # Reads oracle from:      skill_generation_results/human_authored/<task>/
        # Writes per-subtask JSONs: evaluation_reports/<config>/<task>/<subtask>/*.metrics.json
        print("\n[2/3] Skill metrics (coverage, executability, safety)...")
        cmd = [
            sys.executable, str(skill_script),
            "--config", config,
            "--tasks",
        ] + active_tasks
        if dry_run:
            print(f"  (dry-run) {' '.join(cmd)}")
        else:
            rc = subprocess.run(cmd).returncode
            if rc != 0:
                print(f"  [warn] skill eval exited {rc}")

        # ── Step 3: Skill metrics CSV ──────────────────────────────────────────
        # One subprocess per (config, task).
        # Reads: evaluation_reports/<config>/<task>/<subtask>/*.metrics.json
        # Writes: evaluation_reports/<config>/<task>/<task>-skills-results.csv
        print("\n[3/3] Building skill metrics CSV...")
        for task in active_tasks:
            task_reports = reports_dir / config / task
            out_csv = task_reports / f"{task}-skills-results.csv"
            cmd = [
                sys.executable, str(csv_script),
                "--results-root", str(task_reports),
                "--output", str(out_csv),
            ]
            print(f"  {task}: ", end="", flush=True)
            if dry_run:
                print(f"(dry-run) {' '.join(cmd)}")
            else:
                rc = subprocess.run(cmd).returncode
                print("ok" if rc == 0 else f"[warn] exit {rc}")

        # Aggregate skills CSVs across all tasks for this config
        skills_task_csvs = [
            reports_dir / config / task / f"{task}-skills-results.csv"
            for task in active_tasks
        ]
        agg_skills = reports_dir / config / "skill-quality-evaluation.csv"
        if not dry_run:
            _aggregate_csvs(skills_task_csvs, agg_skills)
            print(f"  → aggregated: {agg_skills}")

        # ── Skill coverage CSV (per query × run) ────────────────────────────────
        # compute_coverage.py runs per query, so coverage is at query granularity
        # (one run, "default", per config in the human_authored case). Scrape every
        # query's key_points.metrics.json directly — it's not on the per-task
        # skills-results CSV because its granularity differs.
        agg_coverage = reports_dir / config / "skill-coverage-evaluation.csv"
        if not dry_run:
            out = _build_skill_coverage_csv(config, active_tasks, reports_dir)
            print(f"  → aggregated: {out}")

        # ── Final report.csv ────────────────────────────────────────────────────
        # Task-inner mean → cross-task mean → per-metric normalization.
        report_csv = reports_dir / config / "report.csv"
        if not dry_run:
            _write_report_csv(
                traj_csv=agg_traj,
                skill_csv=agg_skills,
                coverage_csv=agg_coverage,
                out_path=report_csv,
            )
            print(f"  → report:      {report_csv}")

    print(f"\n{'='*60}")
    print(f"Metrics complete. Reports → {reports_dir}")
    print(f"{'='*60}\n")


# ── CLI ────────────────────────────────────────────────────────────────────────

def main() -> int:
    _load_dotenv()
    _require_anthropic_key()
    _require_docker()

    parser = argparse.ArgumentParser(
        description=(
            "Parallel Docker eval runner with per-task pre-built images.\n"
            "Phase 1: ensure images; Phase 2: run trials in parallel; Phase 3: optional cleanup."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("tasks", nargs="*", help="Task IDs (default: all tasks)")
    parser.add_argument(
        "--subtask-range",
        default=None,
        metavar="N-M",
        help=(
            "Expand each task ID into subtasks N through M (inclusive). "
            "Example: --subtask-range 1-5 with citation-check "
            "yields citation-check-1 … citation-check-5 (skips missing ones). "
            "If task_id already points to a leaf task, it is used as-is."
        ),
    )
    parser.add_argument("-a", "--agent", default="claude-code",
                        help="Agent ID (default: claude-code)")
    parser.add_argument("-m", "--model", default="claude-sonnet-4-6",
                        help="Model name (default: claude-sonnet-4-6)")
    parser.add_argument(
        "--skill-path", nargs="+", default=None, metavar="PATH",
        help=(
            "Path(s) to skill config dir(s) to evaluate "
            "(default: output/skill_generation_results/human_authored). "
            "Relative paths are resolved from the GenSkillBench root. "
            "Example: output/skill_generation_results/b1-one-shot-claude-sonnet-4-6. "
            "The last path component is used as the config key for output naming. "
            "Use 'none' to run without any injected skills (no_skill config)."
        ),
    )
    parser.add_argument("--repeats", type=int, default=1,
                        help="Repeat each config per task (default: 1)")
    parser.add_argument("--max-steps", type=int, default=100, metavar="N",
                        help="Max agent turns per trial (default: 100)")
    parser.add_argument("--max-workers", type=int, default=10,
                        help="Parallel trial workers (default: 10)")
    parser.add_argument("--build-workers", type=int, default=3,
                        help="Parallel image build workers (default: 3)")
    parser.add_argument("--remove-images", action="store_true",
                        help="Remove prebuilt images after run (default: keep for reuse)")
    parser.add_argument("--no-record", action="store_true",
                        help="Skip writing per-trial result.json")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would be built/run without executing anything")
    parser.add_argument(
        "--job-config",
        default=None,
        metavar="PATH",
        help=(
            "Path to a job-config JSON file (generated by check_runs.py --export-config). "
            "Each entry specifies task, mode, configs, and repeats independently. "
            "When given, --tasks / --modes / --repeats / --subtask-range are ignored and "
            "all work items share a single Docker build phase and worker pool."
        ),
    )
    parser.add_argument(
        "--trials-dir",
        default=None,
        metavar="PATH",
        help=(
            "Directory to write trial outputs (default: output/evaluation_log/). "
            "Accepts absolute or relative paths. Use to isolate ablation runs, e.g. "
            "--trials-dir output/ablation_eval_trials"
        ),
    )
    parser.add_argument(
        "--skip-metrics",
        action="store_true",
        help="Run agent trials only; skip metrics computation (trajectory + skill metrics).",
    )
    parser.add_argument(
        "--metrics-only",
        action="store_true",
        help="Run metrics computation only; skip Docker build and agent trials.",
    )
    parser.add_argument(
        "--judge-model",
        default="gpt-5-mini",
        metavar="MODEL",
        help="OpenAI model used for LLM-as-judge metrics (default: gpt-5-mini).",
    )

    args = parser.parse_args()

    if args.skip_metrics and args.metrics_only:
        print("--skip-metrics and --metrics-only are mutually exclusive.", file=sys.stderr)
        return 2

    # ── Resolve trials_dir ─────────────────────────────────────────────────────
    _trials_dir = Path(args.trials_dir) if args.trials_dir else TRIALS_DIR
    if args.trials_dir and not _trials_dir.is_absolute():
        _trials_dir = Path(__file__).parent / _trials_dir

    # ── Job-config mode ────────────────────────────────────────────────────────
    if args.job_config:
        config_path = Path(args.job_config)
        if not config_path.exists():
            print(f"Job config not found: {config_path}", file=sys.stderr)
            return 2
        if not args.dry_run:
            try:
                job_task_ids = [
                    str(e["task"]) for e in json.loads(config_path.read_text(encoding="utf-8"))
                ]
            except Exception:
                job_task_ids = []
            _validate_api_keys(
                agent_id=args.agent,
                task_ids=job_task_ids,
                task_root=TASKS_DIR,
                need_agent_keys=True,
                need_judge_key=not args.skip_metrics,
            )
        return hyper_eval(
            [],                          # task_ids unused in config mode
            task_root=TASKS_DIR,
            agent_id=args.agent,
            model=args.model,
            skill_paths=[],              # skill_paths unused in config mode (config provides them)
            repeats=1,                   # repeats unused in config mode
            max_steps=args.max_steps,
            max_workers=max(1, args.max_workers),
            build_workers=max(1, args.build_workers),
            remove_images=args.remove_images,
            record=not args.no_record,
            dry_run=args.dry_run,
            config_path=config_path,
            trials_dir=_trials_dir,
        )

    # ── Normal mode (task_ids + modes + repeats) ───────────────────────────────
    raw_task_ids = args.tasks if args.tasks else list_tasks()
    if not raw_task_ids:
        print("No tasks found.")
        return 2

    # Expand task-level IDs to query-level IDs
    if args.subtask_range:
        m = re.match(r"^(\d+)-(\d+)$", args.subtask_range.strip())
        if not m:
            print(f"Invalid --subtask-range '{args.subtask_range}': expected format N-M (e.g. 1-5)",
                  file=sys.stderr)
            return 2
        sub_start, sub_end = int(m.group(1)), int(m.group(2))
        if sub_start > sub_end:
            print(f"Invalid --subtask-range: start ({sub_start}) > end ({sub_end})", file=sys.stderr)
            return 2
        task_ids = []
        for tid in raw_task_ids:
            expanded = _expand_subtask_range(tid, TASKS_DIR, sub_start, sub_end)
            if not expanded:
                print(f"[warn] No queries {sub_start}-{sub_end} found for '{tid}' — skipping")
            task_ids.extend(expanded)
        if not task_ids:
            print("No valid queries found after applying --subtask-range.")
            return 2
    else:
        # Auto-discover all queries under each task (sniff the task dir)
        task_ids = []
        for tid in raw_task_ids:
            task_path = TASKS_DIR / tid
            if not task_path.is_dir():
                print(f"[warn] Task not found: {tid} — skipping")
                continue
            queries = sorted(
                f"{tid}/{child.name}"
                for child in sorted(task_path.iterdir())
                if child.is_dir() and (child / "instruction.md").exists()
            )
            if not queries:
                print(f"[warn] No queries found under '{tid}' — skipping")
            task_ids.extend(queries)
        if not task_ids:
            print("No valid queries found.")
            return 2

    # Resolve skill paths: default to human_authored when not specified
    skill_paths = _resolve_skill_paths(args.skill_path)

    # Pre-flight: auto-fill any missing human_authored skills from skills/
    if not args.dry_run:
        _ensure_skill_paths(skill_paths, task_ids)

    # Pre-flight: fail fast if required API keys are missing / still placeholders.
    if not args.dry_run:
        _validate_api_keys(
            agent_id=args.agent,
            task_ids=task_ids,
            task_root=TASKS_DIR,
            need_agent_keys=not args.metrics_only,
            need_judge_key=not args.skip_metrics,
        )

    if args.metrics_only:
        _run_metrics_pipeline(
            task_ids, skill_paths=skill_paths,
            judge_model=args.judge_model, dry_run=args.dry_run,
        )
        return 0

    rc = hyper_eval(
        task_ids,
        task_root=TASKS_DIR,
        agent_id=args.agent,
        model=args.model,
        skill_paths=skill_paths,
        repeats=max(1, args.repeats),
        max_steps=args.max_steps,
        max_workers=max(1, args.max_workers),
        build_workers=max(1, args.build_workers),
        remove_images=args.remove_images,
        record=not args.no_record,
        dry_run=args.dry_run,
        config_path=None,
        trials_dir=_trials_dir,
    )

    if not args.skip_metrics:
        _run_metrics_pipeline(
            task_ids, skill_paths=skill_paths,
            judge_model=args.judge_model, dry_run=args.dry_run,
        )

    return rc


if __name__ == "__main__":
    sys.exit(main())
