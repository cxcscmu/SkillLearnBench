#!/usr/bin/env python3
"""
Compute coverage by classifying each generated key point against generated skill text.

coverage = fraction of oracle key points explicitly mentioned in the generated skill.
"""
from __future__ import annotations

import argparse
import json
import json_repair
import os
import re
import sys
from pathlib import Path
from typing import Any

_skill_root = Path(__file__).resolve().parents[1]
_utils_dir = _skill_root / "utils"
if str(_utils_dir) not in (sys.path or []):
    sys.path.insert(0, str(_utils_dir))
from prompts import KEY_POINT_CLASSIFICATION_PROMPT_TEMPLATE

TEXT_EXT_ALLOWLIST = {
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".csv",
    ".tsv",
    ".py",
    ".sh",
    ".js",
    ".ts",
    ".sql",
}

# Skill folders named like run1_my-skill / run2_other-skill → one key-point eval per run-id.
_RUN_SKILL_DIR_RE = re.compile(r"^run(\d+)_(.+)$", re.IGNORECASE)


def _load_env() -> None:
    candidates = [
        Path(__file__).resolve().parents[3] / ".env",
        Path(__file__).resolve().parents[2] / ".env",
    ]
    for dotenv in candidates:
        if not dotenv.exists():
            continue
        for line in dotenv.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k and k not in os.environ:
                os.environ[k] = v


def _read(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"missing file: {path}")
    return path.read_text(encoding="utf-8", errors="replace").strip()


def _is_probably_text(path: Path) -> bool:
    try:
        data = path.read_bytes()
    except OSError:
        return False
    return b"\x00" not in data[:8192]


def _allowed_supplementary_file(skill_dir: Path, f: Path) -> bool:
    try:
        rel = f.relative_to(skill_dir)
    except ValueError:
        return False
    if not rel.parts:
        return False
    top = rel.parts[0]
    ext = f.suffix.lower()
    if top in {"scripts", "references"}:
        return ext in TEXT_EXT_ALLOWLIST and _is_probably_text(f)
    if top == "assets":
        return ext in {".md", ".txt", ".json", ".yaml", ".yml", ".csv", ".tsv"} and _is_probably_text(f)
    return False


def _group_skill_subdirs_by_run(generated_root: Path) -> dict[str, list[Path]]:
    """
    Partition immediate child skill directories under a config root.

    - Names matching ``run{N}_...`` → grouped under ``run{N}`` (normalized, no zero pad).
    - If no directory uses that prefix, all skills belong to a single group ``default``.
    - If some use the prefix and some do not, unprefixed dirs go to ``default``.
    """
    skill_dirs = sorted([d for d in generated_root.iterdir() if d.is_dir()])
    if not skill_dirs:
        raise FileNotFoundError(f"no skill subdirectories in: {generated_root}")

    groups: dict[str, list[Path]] = {}
    any_prefixed = False
    for d in skill_dirs:
        m = _RUN_SKILL_DIR_RE.match(d.name)
        if m:
            any_prefixed = True
            rid = f"run{int(m.group(1))}"
            groups.setdefault(rid, []).append(d)
        else:
            groups.setdefault("default", []).append(d)

    if not any_prefixed:
        return {"default": list(skill_dirs)}

    out = {k: sorted(v, key=lambda p: p.name) for k, v in groups.items() if v}
    if not out:
        raise FileNotFoundError(f"no skill subdirectories in: {generated_root}")
    return out


def _build_generated_skill_blob_from_dirs(skill_dirs: list[Path]) -> str:
    chunks: list[str] = []
    for idx, skill_dir in enumerate(sorted(skill_dirs, key=lambda p: p.name), start=1):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        chunks.append(f"# Skill {idx}: {skill_dir.name}")
        chunks.append("## Skill Document: SKILL.md")
        chunks.append(_read(skill_md))

        extras: list[Path] = []
        for root_name in ["scripts", "references", "assets"]:
            root = skill_dir / root_name
            if not root.exists() or not root.is_dir():
                continue
            for p in root.rglob("*"):
                if p.is_file() and _allowed_supplementary_file(skill_dir, p):
                    extras.append(p)

        for f in sorted(extras, key=lambda p: str(p.relative_to(skill_dir))):
            chunks.append(f"## Supplementary Material: {f.relative_to(skill_dir)}")
            chunks.append(_read(f))

    if not chunks:
        names = ", ".join(d.name for d in skill_dirs) or "(none)"
        raise FileNotFoundError(f"no SKILL.md found in skill dirs: {names}")
    return "\n\n".join(chunks)


def _build_generated_skill_blob(generated_root: Path) -> str:
    """Backward-compatible: all skills under config root in one blob (not used for per-run eval)."""
    if not generated_root.exists():
        raise FileNotFoundError(f"generated skill dir not found: {generated_root}")
    skill_dirs = sorted([d for d in generated_root.iterdir() if d.is_dir()])
    return _build_generated_skill_blob_from_dirs(skill_dirs)


def _resolve_generated_roots(
    task_dir: Path,
    generated_root_arg: Path | None,
    skill_configs_dir: Path | None = None,
) -> dict[str, Path]:
    if generated_root_arg:
        root = generated_root_arg
        if not root.exists() or not root.is_dir():
            raise FileNotFoundError(f"skill dir not found: {root}")
        return {root.name: root}

    configs_root = skill_configs_dir or (task_dir / "environment" / "skill_configs")
    if not configs_root.exists():
        raise FileNotFoundError(f"skill configs dir not found: {configs_root}")

    roots: dict[str, Path] = {}
    for d in sorted(configs_root.iterdir(), key=lambda p: p.name):
        if d.is_dir():
            roots[d.name] = d
    if not roots:
        raise FileNotFoundError(f"no config dirs under: {configs_root}")
    return roots


def _call_llm(prompt: str, model: str) -> str:
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("No API key found (set OPENAI_API_KEY)")
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("openai client not installed") from exc

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    try:
        resp = client.responses.create(
            model=model,
            input=prompt,
            reasoning_effort="low",
        )
    except TypeError as exc:
        if "reasoning_effort" not in str(exc):
            raise
        resp = client.responses.create(
            model=model,
            input=prompt,
        )
    return (resp.output_text or "").strip()


def _extract_json_object(raw: str) -> dict[str, Any]:
    raw = raw.strip()
    try:
        obj = json_repair.loads(raw)
        if isinstance(obj, dict):
            return obj
    except json.JSONDecodeError:
        pass

    m = re.search(r"\{[\s\S]*\}", raw)
    if not m:
        raise ValueError("Fail in load in JSON format")
    obj = json_repair.loads(m.group(0))
    if not isinstance(obj, dict):
        raise ValueError("Fail in load in JSON format")
    return obj


def _call_llm_and_parse_with_retry(
    *,
    prompt: str,
    model: str,
    max_parse_retries: int = 3,
) -> tuple[dict[str, Any], str]:
    last_exc: Exception | None = None
    last_raw = ""
    for _ in range(max(1, max_parse_retries)):
        raw = _call_llm(prompt, model=model)
        last_raw = raw
        try:
            return _extract_json_object(raw), raw
        except Exception as exc:
            last_exc = exc
    raise ValueError(f"failed to parse judge JSON after {max_parse_retries} attempts: {last_exc}; raw={last_raw}")


def _normalize_label(parsed: dict[str, Any]) -> tuple[int, str]:
    raw_id = parsed.get("label_id")
    raw_label = str(parsed.get("label", "")).strip().lower()

    try:
        label_id = int(raw_id)
    except (TypeError, ValueError):
        label_id = 0

    label_by_id = {1: "mentioned", 2: "missing", 3: "contradiction"}
    if label_id in label_by_id:
        return label_id, label_by_id[label_id]

    if raw_label in {"mentioned", "missing", "contradiction"}:
        label_id = {"mentioned": 1, "missing": 2, "contradiction": 3}[raw_label]
        return label_id, raw_label

    raise ValueError(f"invalid label output: label_id={raw_id}, label={raw_label!r}")


def _load_key_points(path: Path) -> list[dict[str, Any]]:
    data = json_repair.loads(_read(path))
    if not isinstance(data, list):
        raise ValueError(f"key points file must be a JSON list: {path}")

    points: list[dict[str, Any]] = []
    for i, item in enumerate(data, start=1):
        if isinstance(item, dict):
            kp = str(item.get("key_point", "")).strip()
            if not kp:
                continue
            points.append({"index": i, "key_point": kp})
        elif isinstance(item, str):
            kp = item.strip()
            if not kp:
                continue
            points.append({"index": i, "key_point": kp})
    return points


def _evaluate_one_run(
    *,
    config: str,
    run_id: str,
    skill_dirs: list[Path],
    config_root: Path,
    points: list[dict[str, Any]],
    model: str,
    raw_dir: Path | None,
) -> dict[str, Any]:
    generated_skill = _build_generated_skill_blob_from_dirs(skill_dirs)
    details: list[dict[str, Any]] = []

    run_raw_dir: Path | None = None
    if raw_dir:
        run_raw_dir = raw_dir / config / run_id
        run_raw_dir.mkdir(parents=True, exist_ok=True)

    for i, point in enumerate(points, start=1):
        prompt = KEY_POINT_CLASSIFICATION_PROMPT_TEMPLATE.format(
            key_point=point["key_point"],
            generated_skill=generated_skill,
        )
        parsed, raw = _call_llm_and_parse_with_retry(
            prompt=prompt,
            model=model,
            max_parse_retries=3,
        )
        label_id, label = _normalize_label(parsed)
        reason = str(parsed.get("reason", "")).strip()

        details.append(
            {
                "index": i,
                "source_index": point["index"],
                "key_point": point["key_point"],
                "label_id": label_id,
                "label": label,
                "reason": reason,
            }
        )
        if run_raw_dir:
            (run_raw_dir / f"{i:03d}.raw.txt").write_text(raw, encoding="utf-8")

    total = len(details)
    mentioned = sum(1 for d in details if d["label"] == "mentioned")

    return {
        "run_id": run_id,
        "skill_root": str(config_root),
        "skill_subdirs": [d.name for d in sorted(skill_dirs, key=lambda p: p.name)],
        "total_key_points": total,
        "counts": {
            "mentioned": mentioned,
            "missing": sum(1 for d in details if d["label"] == "missing"),
        },
        "coverage": (mentioned / total) if total else 0.0,
        "details": details,
    }


def _run_id_sort_key(run_id: str) -> tuple:
    if run_id == "default":
        return (0, 0, run_id)
    if run_id.startswith("run") and run_id[3:].isdigit():
        return (1, int(run_id[3:]), run_id)
    return (2, run_id, run_id)


def _evaluate_config_per_runs(
    *,
    config: str,
    config_root: Path,
    points: list[dict[str, Any]],
    model: str,
    raw_dir: Path | None,
) -> dict[str, Any]:
    by_run: dict[str, Any] = {}
    groups = _group_skill_subdirs_by_run(config_root)
    for run_id in sorted(groups.keys(), key=_run_id_sort_key):
        by_run[run_id] = _evaluate_one_run(
            config=config,
            run_id=run_id,
            skill_dirs=groups[run_id],
            config_root=config_root,
            points=points,
            model=model,
            raw_dir=raw_dir,
        )
    return {"by_run": by_run}


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute coverage from generated key points for all skill configs")
    parser.add_argument("--task-id", required=True, help="Task folder name under evaluation/tasks")
    parser.add_argument(
        "--generated-root",
        type=Path,
        help="Explicit skill root to evaluate; default: all config dirs under --skill-configs-dir.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output path; default: results/<task-id>/key_points.metrics.json",
    )
    parser.add_argument("--model", default="gpt-5-mini", help="OpenAI model name")
    parser.add_argument("--raw-dir", type=Path, help="Optional dir to save per-key-point raw LLM outputs")
    parser.add_argument("--task-dir", type=Path, help="Override task directory (contains instruction.md)")
    parser.add_argument("--skill-configs-dir", type=Path, help="Override skill configs directory (contains human_authored/, <config>/)")
    parser.add_argument("--key-points-path", type=Path, help="Override path to skill-key-points.generated.json")
    args = parser.parse_args()

    _load_env()
    base = Path(__file__).resolve().parents[3]
    task_dir = args.task_dir.resolve() if args.task_dir else base / "tasks" / args.task_id
    if not task_dir.exists():
        print(f"Failed: task not found: {task_dir}", file=sys.stderr)
        return 1

    generated_key_points = args.key_points_path.resolve() if args.key_points_path else task_dir / "reference" / "skill-key-points.generated.json"
    output_path = args.output or (base / "results" / args.task_id / "key_points.metrics.json")

    try:
        points = _load_key_points(generated_key_points)
        if not points:
            raise ValueError(f"no valid key points loaded from: {generated_key_points}")
        generated_roots = _resolve_generated_roots(task_dir, args.generated_root, args.skill_configs_dir)
        if args.raw_dir:
            args.raw_dir.mkdir(parents=True, exist_ok=True)

        by_config: dict[str, Any] = {}
        for config, root in generated_roots.items():
            by_config[config] = _evaluate_config_per_runs(
                config=config,
                config_root=root,
                points=points,
                model=args.model,
                raw_dir=args.raw_dir,
            )

        result = {
            "task_id": args.task_id,
            "metric": "key_points",
            "schema_version": 2,
            "model": args.model,
            "generated_key_points_path": str(generated_key_points),
            "by_config": by_config,
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

        print(f"Task: {args.task_id}")
        print(f"Generated key points: {generated_key_points}")
        print(f"Variants evaluated: {len(by_config)}")
        for config, row in by_config.items():
            by_run = row.get("by_run", {}) if isinstance(row, dict) else {}
            if isinstance(by_run, dict):
                for run_id, r in sorted(by_run.items(), key=lambda x: _run_id_sort_key(x[0])):
                    if not isinstance(r, dict):
                        continue
                    print(
                        f"{config} [{run_id}]: skill_root={r.get('skill_root')}, "
                        f"coverage={r.get('coverage')}, "
                        f"total_key_points={r.get('total_key_points')}"
                    )
            else:
                print(f"{config}: (unexpected format) {row!r}")
        print(f"Wrote metrics: {output_path}")
        return 0

    except Exception as e:
        print(f"Failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
