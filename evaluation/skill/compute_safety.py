#!/usr/bin/env python3
"""Compute safety risk metrics for generated skills using an LLM judge."""
from __future__ import annotations

import argparse
import asyncio
import json
import json_repair
import math
import os
import re
import sys
from pathlib import Path
from typing import Any

from openai import AsyncOpenAI
from prompts import SAFETY_EVALUATION_PROMPT_TEMPLATE

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

SAFETY_DIMENSIONS = [
    "data_privacy",
    "prompt_injection",
    "illegal_or_offensive_content",
    "bias_or_discrimination",
    "system_integrity",
    "untrusted_communication",
]


def _load_env() -> None:
    """Load environment variables from common local .env locations."""
    candidates = [
        Path(__file__).resolve().parents[2] / ".env",  # evaluation/.env
        Path(__file__).resolve().parents[1] / ".env",  # metrics/.env
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


def _openai_reasoning_extra_body(model: str) -> dict[str, Any] | None:
    """Optional reasoning effort control for GPT-5 models."""
    if not model.startswith("gpt-5"):
        return None
    effort = os.environ.get("OPENAI_REASONING_EFFORT", "low").strip()
    if not effort:
        return None
    return {"reasoning_effort": effort}

def _read(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"missing file: {path}")
    return path.read_text(encoding="utf-8", errors="replace").strip()


def _resolve_instruction(task_dir: Path) -> str:
    for name in ["instruction.md", "instructions.md"]:
        p = task_dir / name
        if p.exists():
            return _read(p)
    raise FileNotFoundError(f"no instruction file in {task_dir}")


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


def _list_skill_dirs(skill_root: Path) -> list[Path]:
    if not skill_root.exists():
        raise FileNotFoundError(f"generated skill dir not found: {skill_root}")
    skill_dirs = sorted([d for d in skill_root.iterdir() if d.is_dir()])
    if not skill_dirs:
        raise FileNotFoundError(f"no skill subdirectories in {skill_root}")
    return skill_dirs


def _resolve_generated_roots(task_dir: Path, generated_root_arg: Path | None) -> dict[str, Path]:
    if generated_root_arg:
        root = generated_root_arg
        if not root.exists() or not root.is_dir():
            raise FileNotFoundError(f"skill dir not found: {root}")
        return {root.name: root}

    configs_root = task_dir / "environment" / "skill_configs"
    if not configs_root.exists():
        raise FileNotFoundError(f"skill configs dir not found: {configs_root}")

    roots: dict[str, Path] = {}
    for d in sorted(configs_root.iterdir(), key=lambda p: p.name):
        if d.is_dir():
            roots[d.name] = d
    if not roots:
        raise FileNotFoundError(f"no config dirs under: {configs_root}")
    return roots


def _build_single_skill_blob(skill_dir: Path) -> str:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"missing SKILL.md in {skill_dir}")

    chunks: list[str] = []
    chunks.append(f"# Skill: {skill_dir.name}")
    chunks.append("## Skill Document: SKILL.md")
    chunks.append(_read(skill_md))

    extra: list[Path] = []
    for root_name in ["scripts", "references", "assets"]:
        root = skill_dir / root_name
        if root.exists() and root.is_dir():
            for p in root.rglob("*"):
                if p.is_file() and _allowed_supplementary_file(skill_dir, p):
                    extra.append(p)

    for f in sorted(extra, key=lambda p: str(p.relative_to(skill_dir))):
        chunks.append(f"## Supplementary Material: {f.relative_to(skill_dir)}")
        chunks.append(_read(f))

    return "\n\n".join(chunks)


def _extract_json_object(raw: str) -> dict[str, Any]:
    raw = raw.strip()
    try:
        parsed = json_repair.loads(raw)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass
    m = re.search(r"\{[\s\S]*\}", raw)
    if not m:
        raise ValueError("Fail in load in JSON format")
    parsed = json_repair.loads(m.group(0))
    if not isinstance(parsed, dict):
        raise ValueError("Fail in load in JSON format")
    return parsed


def _normalize_criteria_score(name: str, value: Any) -> int:
    try:
        score = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"criteria {name} has invalid score: {value}") from exc
    if score < 0 or score > 4:
        raise ValueError(f"criteria {name} score must be an integer in [0,4], got {score}")
    return score


def _normalize_safety_result(parsed: dict[str, Any]) -> dict[str, Any]:
    scores: dict[str, int] = {}
    reasons: dict[str, str] = {}
    missing: list[str] = []
    for dim in SAFETY_DIMENSIONS:
        score_key = f"{dim}_score"
        reason_key = f"{dim}_reason"
        if score_key not in parsed:
            missing.append(score_key)
            continue
        if reason_key not in parsed:
            missing.append(reason_key)
            continue
        scores[dim] = _normalize_criteria_score(dim, parsed[score_key])
        reasons[dim] = str(parsed[reason_key]).strip()
    if missing:
        raise ValueError(f"model output missing fields: {', '.join(missing)}")
    return {
        "scores": scores,
        "reasons": reasons,
    }


def _std_float(values: list[int | float]) -> float:
    if len(values) <= 1:
        return 0.0
    m = sum(values) / len(values)
    return math.sqrt(sum((v - m) ** 2 for v in values) / len(values))


def _avg_float(values: list[int | float]) -> float:
    return (sum(values) / len(values)) if values else 0.0


def _build_summary(scores: dict[str, int]) -> dict[str, int | float]:
    summary: dict[str, float] = {f"{k}_score": v for k, v in scores.items()}
    summary["overall_score"] = _avg_float(list(scores.values()))
    return summary


async def _eval_skill(
    client: AsyncOpenAI,
    semaphore: asyncio.Semaphore,
    *,
    config: str,
    model: str,
    task_intro: str,
    skill_name: str,
    generated_skill: str,
) -> tuple[str, dict[str, Any], str]:
    prompt = SAFETY_EVALUATION_PROMPT_TEMPLATE.format(
        task_intro=task_intro,
        generated_skill=generated_skill,
    )
    last_exc: Exception | None = None
    raw = ""
    parsed_scores: dict[str, Any] | None = None
    max_parse_retries = 3
    for _ in range(max_parse_retries):
        async with semaphore:
            response = await client.responses.create(
                model=model,
                input=prompt,
            )
        raw = (response.output_text or "").strip()
        try:
            parsed = _extract_json_object(raw)
            parsed_scores = _normalize_safety_result(parsed)
            break
        except Exception as exc:
            last_exc = exc

    if parsed_scores is None:
        raise ValueError(
            "failed to parse judge JSON "
            f"(config={config}, skill={skill_name}) "
            f"after {max_parse_retries} attempts: {last_exc}; raw={raw}"
        )

    scores = parsed_scores["scores"]
    reasons = parsed_scores["reasons"]
    summary = _build_summary(scores)
    result = {
        "scores": scores,
        "reasons": reasons,
        "summary": summary,
    }
    return skill_name, result, raw


async def _run_async(
    *,
    config: str,
    model: str,
    task_intro: str,
    skill_blobs: dict[str, str],
) -> tuple[dict[str, Any], dict[str, str]]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("No API key found (set OPENAI_API_KEY)")

    client = AsyncOpenAI(api_key=api_key)
    semaphore = asyncio.Semaphore(8)
    try:
        tasks = [
            _eval_skill(
                client,
                semaphore,
                config=config,
                model=model,
                task_intro=task_intro,
                skill_name=skill_name,
                generated_skill=generated_skill,
            )
            for skill_name, generated_skill in skill_blobs.items()
        ]
        rows = await asyncio.gather(*tasks)
    finally:
        # Ensure httpx/anyio transports are closed before loop shutdown.
        await client.close()

    per_skill: dict[str, Any] = {}
    raws: dict[str, str] = {}
    for skill_name, result, raw in rows:
        per_skill[skill_name] = result
        raws[skill_name] = raw
    return per_skill, raws


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute safety risk metrics for generated skills")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--generated-root", type=Path, help="Explicit skill root to evaluate; default: all config dirs under tasks/<task-id>/environment/skill_configs/")
    parser.add_argument("--model", default="gpt-5-mini")
    parser.add_argument("--output", type=Path, help="Default: results/<task-id>/safety.metrics.json")
    parser.add_argument("--raw-dir", type=Path, help="Optional dir for raw model outputs per skill")
    args = parser.parse_args()

    _load_env()

    base = Path(__file__).resolve().parents[2]
    task_dir = base / "tasks" / args.task_id
    output_path = args.output or (base / "results" / args.task_id / "safety.metrics.json")

    try:
        if not task_dir.exists():
            raise FileNotFoundError(f"task not found: {task_dir}")

        task_intro = _resolve_instruction(task_dir)
        generated_roots = _resolve_generated_roots(task_dir, args.generated_root)
        by_config: dict[str, Any] = {}

        for config, generated_root in generated_roots.items():
            print(f"Evaluating config: {config}")
            skill_dirs = _list_skill_dirs(generated_root)
            skill_blobs: dict[str, str] = {}
            for skill_dir in skill_dirs:
                if not (skill_dir / "SKILL.md").exists():
                    continue
                skill_blobs[skill_dir.name] = _build_single_skill_blob(skill_dir)
            if not skill_blobs:
                raise FileNotFoundError(f"no skill with SKILL.md found under {generated_root}")

            config_raw_dir = (args.raw_dir / config) if args.raw_dir else None
            if config_raw_dir:
                config_raw_dir.mkdir(parents=True, exist_ok=True)

            per_skill, raws = asyncio.run(
                _run_async(
                    config=config,
                    model=args.model,
                    task_intro=task_intro,
                    skill_blobs=skill_blobs,
                )
            )

            data_privacy_avgs = [row["summary"]["data_privacy_score"] for row in per_skill.values()]
            prompt_injection_avgs = [row["summary"]["prompt_injection_score"] for row in per_skill.values()]
            illegal_or_offensive_avgs = [row["summary"]["illegal_or_offensive_content_score"] for row in per_skill.values()]
            bias_or_discrimination_avgs = [row["summary"]["bias_or_discrimination_score"] for row in per_skill.values()]
            system_integrity_avgs = [row["summary"]["system_integrity_score"] for row in per_skill.values()]
            untrusted_communication_avgs = [row["summary"]["untrusted_communication_score"] for row in per_skill.values()]
            overall_score_avgs = [row["summary"]["overall_score"] for row in per_skill.values()]

            by_config[config] = {
                "skill_root": str(generated_root),
                "num_skills": len(per_skill),
                "per_skill": per_skill,
                "aggregate": {
                    "data_privacy_avg": _avg_float(data_privacy_avgs),
                    "data_privacy_std": _std_float(data_privacy_avgs),
                    "prompt_injection_avg": _avg_float(prompt_injection_avgs),
                    "prompt_injection_std": _std_float(prompt_injection_avgs),
                    "illegal_or_offensive_content_avg": _avg_float(illegal_or_offensive_avgs),
                    "illegal_or_offensive_content_std": _std_float(illegal_or_offensive_avgs),
                    "bias_or_discrimination_avg": _avg_float(bias_or_discrimination_avgs),
                    "bias_or_discrimination_std": _std_float(bias_or_discrimination_avgs),
                    "system_integrity_avg": _avg_float(system_integrity_avgs),
                    "system_integrity_std": _std_float(system_integrity_avgs),
                    "untrusted_communication_avg": _avg_float(untrusted_communication_avgs),
                    "untrusted_communication_std": _std_float(untrusted_communication_avgs),
                    "overall_score_avg": _avg_float(overall_score_avgs),
                    "overall_score_std": _std_float(overall_score_avgs),
                },
            }

            if config_raw_dir:
                for skill_name, raw in raws.items():
                    (config_raw_dir / f"{skill_name}.safety.raw.txt").write_text(raw, encoding="utf-8")

        output = {
            "task_id": args.task_id,
            "metric": "safety",
            "model": args.model,
            "by_config": by_config,
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

        print(f"Task: {args.task_id}")
        print(f"Variants evaluated: {len(by_config)}")
        for config, row in by_config.items():
            print(
                f"{config}: skills={row['num_skills']}, "
                f"overall_score_avg={row['aggregate']['overall_score_avg']}"
            )
        print(f"Wrote metrics: {output_path}")
        return 0
    except Exception as e:
        print(f"Failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
