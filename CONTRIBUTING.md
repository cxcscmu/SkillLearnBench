# Adding a Skill-Generation Method

## Option A: Prompt-only

Create a folder under `baselines/` with a `method.md`. Its content is appended to the task instruction before the agent runs. Optionally add `method.toml` for runtime config.

```
baselines/
└── b5-my-method/
    ├── method.md       # prompt injected into the agent's task instruction
    └── method.toml     # optional runtime config (see keys below)
```

**`method.toml` keys:**

```toml
# Agent termination behaviour in skills-only mode (default: "full").
#   "interrupt"     – poll container for SKILL.md files; interrupt agent early; skip verifier
#   "skip_verifier" – let agent run to completion; skip verifier
#   "full"          – run agent to completion; run verifier
skills_only_mode = "interrupt"

# If set, substitutes {max_rounds} in method.md with this value (minimum 2 enforced).
# Omit entirely for single-pass methods.
max_rounds = 3
```

Static skill files to inject at startup can be placed in `inject/<skill-name>/SKILL.md`; the runner copies them automatically.

## Option B: Custom orchestration

Add a `method.py` alongside `method.md`. The runner delegates agent execution and verification entirely to the plugin, giving full control over multi-round loops, inter-round state, and verifier interaction.

```python
# baselines/b5-my-method/method.py
from pathlib import Path

def run(
    *,
    container_name: str,   # running Docker container
    task_path: Path,        # .../tasks/<task>/
    trial_path: Path,       # output directory for this trial (/logs inside container)
    agent: dict,            # agent config from agents/__init__.py
    model_name: str,
    instruction: str,       # base task instruction (extra subtasks already appended)
    task_workdir: str,      # effective WORKDIR inside the container
    max_rounds: int,        # from method.toml max_rounds (or runner default)
    max_steps: int,         # from --max-steps CLI flag
) -> tuple[bool, int, str, str, int | None]:
    """Returns (passed, steps_used, agent_stdout, agent_stderr, rounds_used)."""
    ...
```

Container setup (image build, container start, agent install) is still handled by the runner.

---

## Running Skill Generation

> **Always dry-run first.** A full run across 20 tasks × 4 methods × 6 models schedules hundreds of Docker trials. Use `--tasks` to target a subset.

```bash
# Preview planned runs — no execution
python generate_skills.py --tasks court-form-filling offer-letter-generator --dry-run

# Targeted run (recommended)
python generate_skills.py \
  --tasks court-form-filling offer-letter-generator \
  --methods b1-one-shot b2-self-feedback \
  --models claude-sonnet-4-6

# Full run across all tasks × methods × models (very time-consuming)
python generate_skills.py
```

Generated skills are automatically organized into `output/skill_generation_results/<method>-<model>/<task>/`.

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--tasks` | all 20 tasks | Task IDs to run |
| `--methods` | b1 b2 b3 b4 | Skill-generation methods |
| `--models` | all 6 models | LLMs to use |
| `--num-subtasks` | `1` | Extra sibling-query instructions fed as context (multi-query ablation) |
| `--max-steps` | `100` | Max agent tool-use steps per run |
| `--max-workers` | `10` | Parallel trial workers |
| `--build-workers` | `3` | Parallel image build workers |
| `--overwrite-configs` | off | Overwrite existing entries in `output/skill_generation_results/` |
| `--dry-run` | off | Print planned runs, do not execute |
| `--full-run` | off | **[Not recommended]** Run agent + verifier (skills-only is the correct Phase 1 mode) |

### Supported Models

| Provider | Model IDs |
|----------|-----------|
| Anthropic | `claude-haiku-4-5`, `claude-sonnet-4-6`, `claude-opus-4-6` |
| Google | `gemini-3.1-flash-lite-preview`, `gemini-3-flash-preview`, `gemini-3.1-pro-preview` |

---

## Developer Tools

| Script | Purpose |
|--------|---------|
| `tools/check_runs.py` | Report evaluation trial completeness; export `rerun_config.json` for missing/failed runs |
| `tools/clean_runs.py` | Remove failed or stale evaluation trials |
| `tools/check_trials.py` | Inspect skill-generation trial outputs |
| `tools/clean_trials.py` | Remove failed skill-generation trials |

Typical rerun workflow:

```bash
python tools/check_runs.py --config b1-one-shot-claude-sonnet-4-6 --export-config rerun.json
python evaluate_skills.py --job-config rerun.json
```

---

## Repo Layout

```
├── generate_skills.py       # Phase 1 CLI: skill generation
├── evaluate_skills.py       # Phase 2 CLI: evaluation + metrics
├── core/
│   ├── skill_runner.py      # Phase 1 single-trial runner
│   └── eval_runner.py       # Phase 2 single-trial runner
├── baselines/               # Method definitions (<id>-<name>/)
├── tasks/                   # Task definitions (read-only inputs)
├── eval_keypoints/          # Oracle reference trajectories + pre-computed metric inputs
├── agents/__init__.py       # Unified agent registry (claude-code, gemini-code)
├── tools/                   # Developer utilities
└── output/                  # All generated artifacts (gitignored)
```
