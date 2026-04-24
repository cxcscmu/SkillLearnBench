#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
import json_repair
from pathlib import Path
from typing import Any


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        obj = json_repair.loads(path.read_text(encoding="utf-8", errors="replace"))
        return obj if isinstance(obj, dict) else {}
    except json.JSONDecodeError:
        return {}


def _get_by_config(obj: dict[str, Any]) -> dict[str, Any]:
    byv = obj.get("by_config", {})
    return byv if isinstance(byv, dict) else {}


def _safe_get(d: dict[str, Any], *path: str) -> Any:
    cur: Any = d
    for p in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(p)
    return cur


def _iter_result_query_dirs(results_root: Path) -> list[Path]:
    # Supports both:
    # - results/<task>/<query>/...
    # - results/<query>/...  (when results_root already points to one task dir)
    dirs: list[Path] = []
    children = sorted(p for p in results_root.iterdir() if p.is_dir())
    for child in children:
        has_metrics = (child / "executability.metrics.json").exists() or (child / "safety.metrics.json").exists()
        if has_metrics:
            dirs.append(child)
            continue
        for query_dir in sorted(p for p in child.iterdir() if p.is_dir()):
            dirs.append(query_dir)
    return dirs


def _split_task_query(query_dir: Path) -> tuple[str, str]:
    # ex: citation-check-1 -> (citation-check, 1)
    m = re.match(r"^(?P<task>.+)-(?P<query>\d+)$", query_dir.name)
    if m:
        return m.group("task"), m.group("query")
    return query_dir.parent.name, query_dir.name


def _parse_config(config: str) -> tuple[str, str]:
    # Parse "b1-one-shot-claude-opus-4-6" into:
    # method="b1-one-shot", llm="claude-opus-4-6"
    if config in ("human_authored", "no_skill"):
        return "", config

    tokens = config.split("-")
    vendor_tokens = {"claude", "gpt", "gemini", "qwen", "llama", "deepseek", "mistral"}
    model_idx = None
    for i in range(len(tokens)):
        if tokens[i] in vendor_tokens:
            model_idx = i
            break

    if model_idx is None:
        return config, ""

    method = "-".join(tokens[:model_idx]) if model_idx > 0 else ""
    llm = "-".join(tokens[model_idx:])
    return method, llm



def _extract_skill_scores(metric_config_row: dict[str, Any], skill_name: str) -> dict[str, Any]:
    return (
        _safe_get(metric_config_row, "per_skill", skill_name, "scores")
        if isinstance(metric_config_row, dict)
        else {}
    ) or {}


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build a per-query per-skill CSV from evaluation/results/<task>/<query>/ "
            "using key_points/executability/safety metrics."
        )
    )
    parser.add_argument(
        "--results-root",
        type=Path,
        default=Path(__file__).resolve().parents[3] / "output" / "evaluation_reports",
        help="Results root (default: output/evaluation_reports)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[3] / "output" / "evaluation_reports" / "query_skill_metrics.csv",
        help="Output csv path",
    )
    args = parser.parse_args()

    results_root = args.results_root.resolve()
    if not results_root.exists():
        print(f"Failed: results root not found: {results_root}")
        return 1

    fieldnames = [
        "LLM",
        "Method",
        "Task",
        "Query",
        "Skill",
        "executability_completeness",
        "executability_consistency",
        "executability_determinism",
        "executability_usability",
        "safety_bias_or_discrimination",
        "safety_data_privacy",
        "safety_illegal_or_offensive_content",
        "safety_prompt_injection",
        "safety_system_integrity",
        "safety_untrusted_communication",
    ]

    rows: list[dict[str, Any]] = []
    for query_dir in _iter_result_query_dirs(results_root):
        key_points = _load_json(query_dir / "key_points.metrics.json")
        executability = _load_json(query_dir / "executability.metrics.json")
        safety = _load_json(query_dir / "safety.metrics.json")

        kp_by = _get_by_config(key_points)
        ex_by = _get_by_config(executability)
        sa_by = _get_by_config(safety)

        if not kp_by and not ex_by and not sa_by:
            continue

        task_slug, _query_id = _split_task_query(query_dir)
        query_name = query_dir.name

        configs = sorted(set(kp_by.keys()) | set(ex_by.keys()) | set(sa_by.keys()))
        for config in configs:
            method, llm = _parse_config(config)
            kp_row = kp_by.get(config, {}) if isinstance(kp_by.get(config), dict) else {}
            ex_row = ex_by.get(config, {}) if isinstance(ex_by.get(config), dict) else {}
            sa_row = sa_by.get(config, {}) if isinstance(sa_by.get(config), dict) else {}

            ex_skills = set(
                _safe_get(ex_row, "per_skill").keys() if isinstance(_safe_get(ex_row, "per_skill"), dict) else []
            )
            sa_skills = set(
                _safe_get(sa_row, "per_skill").keys() if isinstance(_safe_get(sa_row, "per_skill"), dict) else []
            )
            skills = sorted(ex_skills | sa_skills)
            if not skills:
                # Fallback to one row even if per_skill is absent.
                skills = [""]

            for skill in skills:
                ex_scores = _extract_skill_scores(ex_row, skill)
                sa_scores = _extract_skill_scores(sa_row, skill)
                rows.append(
                    {
                        "LLM": llm,
                        "Method": method,
                        "Task": task_slug,
                        "Query": query_name,
                        "Skill": skill,
                        "executability_completeness": ex_scores.get("completeness"),
                        "executability_consistency": ex_scores.get("consistency"),
                        "executability_determinism": ex_scores.get("determinism"),
                        "executability_usability": ex_scores.get("usability"),
                        "safety_bias_or_discrimination": sa_scores.get("bias_or_discrimination"),
                        "safety_data_privacy": sa_scores.get("data_privacy"),
                        "safety_illegal_or_offensive_content": sa_scores.get("illegal_or_offensive_content"),
                        "safety_prompt_injection": sa_scores.get("prompt_injection"),
                        "safety_system_integrity": sa_scores.get("system_integrity"),
                        "safety_untrusted_communication": sa_scores.get("untrusted_communication"),
                    }
                )

    out_path = args.output.resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"Wrote CSV: {out_path}")
    print(f"Rows: {len(rows)}")
    print(f"Columns: {len(fieldnames)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
