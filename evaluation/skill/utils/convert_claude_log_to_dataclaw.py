#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run_cmd(cmd: list[str], env: dict[str, str]) -> None:
    subprocess.run(cmd, check=True, env=env)


def _has_dataclaw(py_bin: str, env: dict[str, str]) -> bool:
    probe = subprocess.run(
        [py_bin, "-c", "import dataclaw.cli"], capture_output=True, text=True, env=env
    )
    return probe.returncode == 0


def _infer_source(input_path: Path) -> str:
    """Guess dataclaw --source from filename (claude vs codex JSONL logs)."""
    n = input_path.name.lower()
    if n.startswith("claude") or "claude-code" in n or "claude_code" in n:
        return "claude"
    if "codex" in n:
        return "codex"
    return "claude"


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Convert a Claude Code or Codex session log (.txt/.jsonl) into dataclaw JSONL. "
            "Uses dataclaw export --source claude|codex."
        )
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Path to claude-code.txt, codex.txt, or similar session log",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output path. Default: <input_dir>/<input_stem>.dataclaw.jsonl",
    )
    parser.add_argument(
        "--source",
        choices=("auto", "claude", "codex"),
        default="auto",
        help="Log format for dataclaw (default: infer from filename)",
    )
    parser.add_argument(
        "--home-dir",
        type=Path,
        default=Path.cwd() / ".tmp_home_single_dataclaw",
        help="Parent directory to create an isolated HOME working dir for this run.",
    )
    parser.add_argument(
        "--keep-home-dir",
        action="store_true",
        help="Keep temporary HOME directory after conversion.",
    )
    args = parser.parse_args()

    input_path = args.input.resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    output_path = (
        args.output.resolve()
        if args.output
        else input_path.with_name(f"{input_path.stem}.dataclaw.jsonl")
    )
    home_parent = args.home_dir.resolve()
    home_parent.mkdir(parents=True, exist_ok=True)
    home_dir = Path(tempfile.mkdtemp(prefix="dataclaw_home_", dir=str(home_parent)))

    source = _infer_source(input_path) if args.source == "auto" else args.source
    project_name = input_path.parent.name or "project"

    if source == "claude":
        session_name = "session.jsonl"
        dst_dir = home_dir / ".claude" / "projects" / project_name
        dst_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(input_path, dst_dir / session_name)
    else:
        # Codex: dataclaw discovers ~/.codex/sessions/**/*.jsonl
        codex_sessions = home_dir / ".codex" / "sessions"
        codex_sessions.mkdir(parents=True, exist_ok=True)
        dest_name = f"{input_path.stem}.jsonl"
        shutil.copy2(input_path, codex_sessions / dest_name)

    env = dict(**os.environ)
    env["HOME"] = str(home_dir)
    # Preserve user site-packages path: changing HOME shifts where Python looks
    # for --user-installed packages (e.g. ~/.local/lib/...), so pin PYTHONUSERBASE
    # to the real base so dataclaw remains importable inside the subprocess.
    import site as _site
    env.setdefault("PYTHONUSERBASE", _site.getuserbase())
    py_bin = sys.executable

    if not _has_dataclaw(py_bin, env):
        raise RuntimeError(
            "dataclaw.cli is not available in current Python environment. "
            "Please install dataclaw and re-run."
        )
    run_cmd([py_bin, "-m", "dataclaw.cli", "config", "--source", source], env=env)
    run_cmd([py_bin, "-m", "dataclaw.cli", "config", "--confirm-projects"], env=env)
    run_cmd(
        [
            py_bin,
            "-m",
            "dataclaw.cli",
            "export",
            "--source",
            source,
            "--all-projects",
            "--no-push",
            "-o",
            str(output_path),
        ],
        env=env,
    )

    print(f"Input: {input_path}")
    print(f"Output: {output_path}")

    if not args.keep_home_dir:
        shutil.rmtree(home_dir, ignore_errors=True)
    else:
        print(f"Kept temp HOME: {home_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
