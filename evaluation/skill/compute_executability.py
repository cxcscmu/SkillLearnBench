#!/usr/bin/env python3
"""Compute executability metrics for generated skills using an LLM judge."""
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
from prompts import EXECUTABILITY_EVALUATION_PROMPT_TEMPLATE

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

DIMENSIONS = ["completeness", "determinism", "consistency", "usability"]


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
            raise FileNotFoundError(f"generated skill dir not found: {root}")
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

    # Robust fallback: scan for the first decodable JSON object region.
    decoder = json.JSONDecoder()
    for i, ch in enumerate(raw):
        if ch != "{":
            continue
        try:
            obj, _end = decoder.raw_decode(raw[i:])
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            return obj

    # Last resort: try brace-range matches from shortest to longest.
    for m in re.finditer(r"\{[\s\S]*?\}", raw):
        frag = m.group(0)
        try:
            obj = json_repair.loads(frag)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            return obj

    raise ValueError("model output does not contain a valid JSON object")


def _normalize_dimension_score(name: str, value: Any) -> int:
    try:
        score = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"dimension {name} has invalid score: {value}") from exc
    if score < 0 or score > 4:
        raise ValueError(f"dimension {name} score must be an integer in [0,4], got {score}")
    return score


def _normalize_executability_result(parsed: dict[str, Any]) -> dict[str, Any]:
    scores: dict[str, int] = {}
    reasons: dict[str, str] = {}
    missing: list[str] = []

    for dim in DIMENSIONS:
        score_key = f"{dim}_score"
        reason_key = f"{dim}_reason"
        if score_key not in parsed:
            missing.append(score_key)
            continue
        if reason_key not in parsed:
            missing.append(reason_key)
            continue
        scores[dim] = _normalize_dimension_score(dim, parsed[score_key])
        reasons[dim] = str(parsed[reason_key]).strip()

    if missing:
        raise ValueError(f"model output missing fields: {', '.join(missing)}")

    return {
        "scores": scores,
        "reasons": reasons,
    }


def _avg(values: list[int | float]) -> float:
    return (sum(values) / len(values)) if values else 0.0


def _std(values: list[int | float]) -> float:
    if len(values) <= 1:
        return 0.0
    m = _avg(values)
    return math.sqrt(sum((v - m) ** 2 for v in values) / len(values))


def _build_summary(scores: dict[str, int]) -> dict[str, int | float]:
    completeness = int(scores["completeness"])
    determinism = int(scores["determinism"])
    consistency = int(scores["consistency"])
    usability = int(scores["usability"])
    overall_score = _avg([completeness, determinism, consistency, usability])
    return {
        "completeness": completeness,
        "determinism": determinism,
        "consistency": consistency,
        "usability": usability,
        "overall_score": overall_score,
    }


async def _eval_skill(
    client: AsyncOpenAI,
    semaphore: asyncio.Semaphore,
    *,
    model: str,
    task_intro: str,
    skill_name: str,
    generated_skill: str,
) -> tuple[str, dict[str, Any], str]:
    prompt = EXECUTABILITY_EVALUATION_PROMPT_TEMPLATE.format(
        task_intro=task_intro,
        generated_skill=generated_skill,
    )
    last_exc: Exception | None = None
    raw = ""
    parsed_scores: dict[str, Any] | None = None
    max_parse_retries = 3
    for _ in range(max_parse_retries):
        async with semaphore:
            response = await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                reasoning_effort="low",
            )
        raw = (response.choices[0].message.content or "").strip()
        try:
            parsed = _extract_json_object(raw)
            parsed_scores = _normalize_executability_result(parsed)
            break
        except Exception as exc:
            last_exc = exc

    if parsed_scores is None:
        raise ValueError(f"failed to parse judge JSON after {max_parse_retries} attempts: {last_exc}; raw={raw}")

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
                model=model,
                task_intro=task_intro,
                skill_name=skill_name,
                generated_skill=generated_skill,
            )
            for skill_name, generated_skill in skill_blobs.items()
        ]
        rows = await asyncio.gather(*tasks)
    finally:
        # Ensure httpx/anyio transports are closed before the loop ends.
        await client.close()

    per_skill: dict[str, Any] = {}
    raws: dict[str, str] = {}
    for skill_name, result, raw in rows:
        per_skill[skill_name] = result
        raws[skill_name] = raw
    return per_skill, raws


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute executability metrics for generated skills")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--generated-root", type=Path, help="Default: tasks/<task-id>/environment/skill_configs/generated")
    parser.add_argument("--model", default="gpt-5-mini")
    parser.add_argument("--output", type=Path, help="Default: results/<task-id>/executability.metrics.json")
    parser.add_argument("--raw-dir", type=Path, help="Optional dir for raw model outputs per skill")
    args = parser.parse_args()

    _load_env()

    base = Path(__file__).resolve().parents[2]
    task_dir = base / "tasks" / args.task_id
    output_path = args.output or (base / "results" / args.task_id / "executability.metrics.json")

    try:
        if not task_dir.exists():
            raise FileNotFoundError(f"task not found: {task_dir}")

        task_intro = _resolve_instruction(task_dir)
        generated_roots = _resolve_generated_roots(task_dir, args.generated_root)
        by_config: dict[str, Any] = {}

        for config, generated_root in generated_roots.items():
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
                    model=args.model,
                    task_intro=task_intro,
                    skill_blobs=skill_blobs,
                )
            )

            completeness_scores = [row["summary"]["completeness"] for row in per_skill.values()]
            determinism_scores = [row["summary"]["determinism"] for row in per_skill.values()]
            consistency_scores = [row["summary"]["consistency"] for row in per_skill.values()]
            usability_scores = [row["summary"]["usability"] for row in per_skill.values()]
            overall_scores = [row["summary"]["overall_score"] for row in per_skill.values()]

            by_config[config] = {
                "generated_skill_root": str(generated_root),
                "num_skills": len(per_skill),
                "per_skill": per_skill,
                "aggregate": {
                    "completeness_avg": _avg(completeness_scores),
                    "completeness_std": _std(completeness_scores),
                    "determinism_avg": _avg(determinism_scores),
                    "determinism_std": _std(determinism_scores),
                    "consistency_avg": _avg(consistency_scores),
                    "consistency_std": _std(consistency_scores),
                    "usability_avg": _avg(usability_scores),
                    "usability_std": _std(usability_scores),
                    "overall_score_avg": _avg(overall_scores),
                    "overall_score_std": _std(overall_scores),
                },
            }

            if config_raw_dir:
                for skill_name, raw in raws.items():
                    (config_raw_dir / f"{skill_name}.executability.raw.txt").write_text(raw, encoding="utf-8")

        output = {
            "task_id": args.task_id,
            "metric": "executability",
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
