# Trajectory Evaluation - Run Guide

This guide reflects the current trajectory evaluation behavior in `evaluation/metrics-computation`.

## 1) Environment Setup

LLM judge scripts read API keys from either:

- `evaluation/.env` (recommended), or
- exported shell environment variables.

You need one of:

- `OPENAI_API_KEY`, or
- `ANTHROPIC_API_KEY`.

Example `evaluation/.env`:

```bash
OPENAI_API_KEY=sk-...
```

## 2) Working Directory

Run commands from:

```bash
cd /path/to/SkillLearnBench/evaluation/metrics-computation
```

## 3) Recommended Command (Full Pipeline)

For end-to-end metrics (skill + trajectory + CSV table), use:

```bash
python scripts/run_task_evaluation.py --task-id offer-letter-generator-1 --model gpt-5-mini
```

What this does for trajectory:

1. prepares reference oracle assets when needed (`claude-code.dataclaw.jsonl`)
2. extracts compact oracle trajectory into `tasks/<task-id>/reference/extracted-claude-code.json` (fallback `.txt`)
3. evaluates each generated trial trajectory:
   - instruction judge (`execution_order`, 1-5)
   - skill invocation ratio
4. aggregates per-run trajectory outputs into:
   - `results/<task-id>/trajectory_instruction_scores.json`
   - `results/<task-id>/skill_invocation_ratio.json`

## 4) Trajectory-Only Unified Runner

If you only want trajectory metrics:

```bash
python metrics/trajectory/run_trajectory_eval.py --task-id offer-letter-generator-1 --model gpt-5-mini
```

Notes:

- `--prepare-oracle-reference` triggers `scripts/prepare_oracle_reference.py` first.
- if reference compact trajectory is missing and you do not pass `--prepare-oracle-reference`, it fails fast.

## 5) Run Steps Individually

```bash
# 1) Prepare oracle reference (raw -> dataclaw -> compact)
python scripts/prepare_oracle_reference.py --task-id offer-letter-generator-1 --model gpt-5-mini

# 2) Instruction judge (1-5 scoring for execution order)
python metrics/trajectory/compute_trajectory_instruction_scores.py --task-id offer-letter-generator-1 --model gpt-5-mini

# 3) Skill invocation ratio
python metrics/trajectory/compute_skill_invocation_ratio.py --task-id offer-letter-generator-1
```

## 6) JSON Parse Retry Behavior (LLM Judge)

For LLM-as-a-judge trajectory scripts, JSON parsing now retries up to 3 attempts:

- `metrics/trajectory/compute_trajectory_instruction_scores.py`
- `metrics/trajectory/compute_trajectory_key_point_metrics.py` (kept for reuse, not in default main pipeline)

If all 3 attempts fail, script exits with error.

## 7) Important Scope Notes

- Compact trajectory extraction is for task reference oracle only, not per generated trial.
- Default main pipeline does not compute trajectory_key_point_recall.
- `compute_trajectory_key_point_metrics.py` remains available for optional separate usage.

## 8) Output Paths

Under `results/<task-id>/`:

- `trajectory_instruction_scores.json`
- `skill_invocation_ratio.json`
- `trajectory_by_run/trajectory_instruction_scores__*.json`
- `trajectory_by_run/skill_invocation_ratio__*.json`
- `metrics_table.csv` (when using `scripts/run_task_evaluation.py`)
