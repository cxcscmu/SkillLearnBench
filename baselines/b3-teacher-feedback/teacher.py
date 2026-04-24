#!/usr/bin/env python3
"""
Teacher: when Student's task run fails, gives modification suggestions (no direct solution).
Teacher has access to ground-truth skill; Student does not.
"""
from __future__ import annotations

import os

from prompts.teacher import TEACHER_SYSTEM_SUGGESTIONS, TEACHER_USER_SUGGESTIONS


def _get_client():
    if os.environ.get("OPENAI_API_KEY"):
        try:
            from openai import OpenAI
            return ("openai", OpenAI())
        except ImportError:
            pass
    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            from anthropic import Anthropic
            return ("anthropic", Anthropic())
        except ImportError:
            pass
    return (None, None)


def get_modification_suggestions(
    skill_md: str,
    task_instruction: str,
    student_skill: str,
    failure_info: str,
    *,
    model: str | None = None,
) -> dict:
    """
    Teacher suggests how to improve the Student's skill (no solution).
    Returns {"suggestions": str, "raw": str}.
    """
    provider_type, client = _get_client()
    if not client:
        return {
            "suggestions": "No API key (OPENAI_API_KEY or ANTHROPIC_API_KEY).",
            "raw": "",
        }

    system = TEACHER_SYSTEM_SUGGESTIONS
    user = TEACHER_USER_SUGGESTIONS.format(
        task_instruction=task_instruction,
        skill_md=skill_md,
        student_skill=(student_skill or ""),
        failure_info=failure_info,
    )

    if provider_type == "openai":
        model_name = model or "gpt-4o-mini"
        r = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0,
        )
        raw = (r.choices[0].message.content or "").strip()
    elif provider_type == "anthropic":
        model_name = model or "claude-sonnet-4-6"
        r = client.messages.create(
            model=model_name,
            max_tokens=2048,
            system=system,
            messages=[{"role": "user", "content": user}],
            temperature=0,
        )
        raw = (r.content[0].text if r.content else "").strip()
    else:
        return {"suggestions": "Unknown provider", "raw": ""}

    return {"suggestions": raw, "raw": raw}
