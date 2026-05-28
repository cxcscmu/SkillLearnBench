"""
Agent registry - Harbor style. Add/remove agents by editing AGENTS dict.
Each agent: id -> {name, env, install, run_template, models}

Optional per-agent field:
  default_tools — ordered list of tool names used to build the --allowedTools flag.
                  run.py resolves {allowed_tools} by filtering this list against any
                  task-level disallowed_tools declared in task.toml [agent] section.
                  Default behaviour (no task.toml override): all tools are allowed.
"""
from __future__ import annotations

_NODE_BOOTSTRAP = (
    "(node --version 2>/dev/null | grep -qE '^v(2[0-9]|[3-9][0-9])') || "
    "(apt-get update -qq && apt-get install -y --no-install-recommends curl "
    "&& curl -fsSL https://deb.nodesource.com/setup_20.x | bash - "
    "&& apt-get install -y nodejs)"
)

# Default Claude Code tool whitelist — used to build {allowed_tools} at runtime.
# Tasks can restrict this via task.toml [agent] disallowed_tools = [...].
_CLAUDE_DEFAULT_TOOLS: list[str] = [
    "Bash", "Edit", "Write", "Read", "Glob", "Grep", "LS",
    "WebFetch", "NotebookEdit", "NotebookRead", "TodoRead", "TodoWrite",
    "Agent", "Skill", "SlashCommand", "Task", "WebSearch",
]

AGENTS: dict[str, dict] = {
    "codex": {
        "name": "Codex (OpenAI GPT)",
        "env": ["OPENAI_API_KEY"],
        "runtime_deps": _NODE_BOOTSTRAP,
        "install": "npm install -g @openai/codex",
        "setup": "auth_json",  # run.py writes auth.json to /root/.codex/ (Harbor style)
        "run": 'codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check --json --model {model} -- "$(cat {instruction_file})"',
        "trajectory_env": {"CODEX_HOME": "/logs/agent"},  # Codex writes sessions to /logs/agent
        "trajectory_tee": "/logs/agent/codex.txt",  # tee stdout to this file (Harbor style)
        "default_model": "gpt-5.2-codex",
    },
    "claude-code": {
        "name": "Claude Code (Anthropic)",
        "env": ["ANTHROPIC_API_KEY"],
        "runtime_deps": _NODE_BOOTSTRAP,
        "install": "npm install -g @anthropic-ai/claude-code",
        "run": 'claude --verbose --output-format stream-json --model {model} --max-turns {max_steps} -p "$(cat {instruction_file})" --allowedTools {allowed_tools}{extra_flags}',
        "default_tools": _CLAUDE_DEFAULT_TOOLS,
        "trajectory_tee": "/logs/agent/claude-code.txt",
        "default_model": "claude-sonnet-4-6",
    },
    "gemini-code": {
        "name": "Gemini Code (Google)",
        "env": ["GEMINI_API_KEY"],
        "runtime_deps": _NODE_BOOTSTRAP,
        "install": "npm install -g @google/gemini-cli",
        "run": 'gemini --yolo --output-format stream-json --model {model} -p "$(cat {instruction_file})"',
        "skill_dir": "/root/.gemini/skills",  # gemini CLI reads from here, not /root/.claude/skills
        "trajectory_tee": "/logs/agent/gemini-code.txt",
        "default_model": "gemini-3.1-flash-lite",
    },
}


def get_agent(agent_id: str) -> dict | None:
    return AGENTS.get(agent_id)


def list_agents() -> list[str]:
    return sorted(AGENTS.keys())
