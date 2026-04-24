"""Shared LLM utilities: env loading, OpenAI/Anthropic calls, JSON parsing."""
from __future__ import annotations

import asyncio
import json
import os
import re
from pathlib import Path
from typing import Any

import json_repair


# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------

def load_env() -> None:
    """Load .env from metrics-computation/ and metrics-computation/metrics/."""
    _here = Path(__file__).resolve()
    candidates = [
        _here.parents[3] / ".env",  # metrics-computation/.env
        _here.parents[2] / ".env",  # metrics-computation/metrics/.env
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


# ---------------------------------------------------------------------------
# Provider detection
# ---------------------------------------------------------------------------

def get_provider() -> str:
    """Return 'openai', 'anthropic', or '' based on available API keys."""
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic"
    return ""


# ---------------------------------------------------------------------------
# OpenAI helpers
# ---------------------------------------------------------------------------

def openai_reasoning_extra_body(model: str) -> dict[str, Any] | None:
    if not model.startswith("gpt-5"):
        return None
    effort = os.environ.get("OPENAI_REASONING_EFFORT", "low").strip()
    return {"reasoning_effort": effort} if effort else None


def _is_retryable_openai_error(exc: Exception) -> bool:
    """Return False for permanent errors that should not be retried."""
    msg = str(exc)
    permanent_codes = {"string_above_max_length", "context_length_exceeded", "invalid_request_error"}
    return not any(code in msg for code in permanent_codes)


async def call_openai_async(
    client: Any,  # AsyncOpenAI
    semaphore: asyncio.Semaphore,
    *,
    prompt: str,
    model: str,
    max_tokens: int,
    _retry: int = 1,
) -> str:
    """Call OpenAI chat completions with one automatic retry on transient API errors."""
    async with semaphore:
        for attempt in range(1 + _retry):
            try:
                r = await client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_completion_tokens=max_tokens,
                    extra_body=openai_reasoning_extra_body(model),
                )
                return (r.choices[0].message.content or "").strip()
            except Exception as exc:
                if attempt < _retry and _is_retryable_openai_error(exc):
                    print(f"[llm] OpenAI transient error (attempt {attempt + 1}), retrying: {exc}")
                    continue
                raise


# ---------------------------------------------------------------------------
# Anthropic helpers
# ---------------------------------------------------------------------------

def call_anthropic(prompt: str, model: str, max_tokens: int = 2048) -> str:
    try:
        from anthropic import Anthropic
    except ImportError as exc:
        raise RuntimeError("anthropic client not installed") from exc
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("No ANTHROPIC_API_KEY found")
    client = Anthropic(api_key=api_key)
    r = client.messages.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
    )
    blocks = getattr(r, "content", [])
    texts = [getattr(b, "text", "") for b in blocks if getattr(b, "type", "") == "text"]
    return "\n".join(texts).strip()


# ---------------------------------------------------------------------------
# JSON parsing
# ---------------------------------------------------------------------------

def extract_json_object(raw: str) -> dict[str, Any]:
    raw = raw.strip()
    try:
        obj = json_repair.loads(raw)
        if isinstance(obj, dict):
            return obj
    except json.JSONDecodeError:
        pass
    m = re.search(r"\{[\s\S]*\}", raw)
    if not m:
        raise ValueError("model output does not contain a JSON object")
    obj = json_repair.loads(m.group(0))
    if not isinstance(obj, dict):
        raise ValueError("parsed JSON is not an object")
    return obj


def extract_json_list(raw: str) -> list[Any]:
    raw = raw.strip()
    try:
        parsed = json_repair.loads(raw)
        if isinstance(parsed, list):
            return parsed
    except json.JSONDecodeError:
        pass
    m = re.search(r"\[\s*\{.*\}\s*\]", raw, flags=re.DOTALL)
    if not m:
        raise ValueError("model output does not contain a JSON list")
    parsed = json_repair.loads(m.group(0))
    if not isinstance(parsed, list):
        raise ValueError("parsed JSON is not a list")
    return parsed


# ---------------------------------------------------------------------------
# Retry wrappers (return parsed dict + raw string)
# ---------------------------------------------------------------------------

async def call_openai_with_retry(
    client: Any,
    semaphore: asyncio.Semaphore,
    *,
    prompt: str,
    model: str,
    max_tokens: int,
    retries: int = 3,
) -> tuple[dict[str, Any], str]:
    last_exc: Exception | None = None
    last_raw = ""
    for _ in range(max(1, retries)):
        raw = await call_openai_async(client, semaphore, prompt=prompt, model=model, max_tokens=max_tokens)
        last_raw = raw
        try:
            return extract_json_object(raw), raw
        except Exception as exc:
            last_exc = exc
    raise ValueError(f"failed to parse JSON after {retries} attempts: {last_exc}; raw={last_raw}")


def call_anthropic_with_retry(
    *,
    prompt: str,
    model: str,
    max_tokens: int = 2048,
    retries: int = 3,
) -> tuple[dict[str, Any], str]:
    last_exc: Exception | None = None
    last_raw = ""
    for _ in range(max(1, retries)):
        raw = call_anthropic(prompt, model=model, max_tokens=max_tokens)
        last_raw = raw
        try:
            return extract_json_object(raw), raw
        except Exception as exc:
            last_exc = exc
    raise ValueError(f"failed to parse JSON after {retries} attempts: {last_exc}; raw={last_raw}")
