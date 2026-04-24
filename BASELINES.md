# Baselines

SkillLearnBench provides four skill-generation baselines, each representing a different strategy for how an agent acquires reusable skill documents.

---

## b1 — One-Shot

The agent is given a single task instance and asked to write 1–5 `SKILL.md` files *before* solving the task. No feedback loop is involved. The skills are written in a single pass, and the agent then attempts the task using those skills.

This is the simplest baseline and serves as the primary reference point for more iterative methods.

---

## b2 — Self-Feedback

After an initial skill-generation pass, the agent reflects on its own output and revises the skills over multiple rounds. No external signal is used — all feedback comes from the agent's own self-critique.

The number of rounds is configured via `max_rounds` in `method.toml` (default: 2).

---

## b3 — Teacher-Feedback

A two-agent setup:
- **Teacher** (external LLM): generates an initial skill set and provides feedback when the student fails
- **Student** (evaluation agent): attempts the task using the provided skills; on failure, the teacher's feedback is incorporated into a revised skill set

This tests whether externally guided revision produces higher-quality skills than self-reflection alone.

---

## b4 — Skill Creator

Identical to b1 in structure (single-pass, no feedback), but the agent is additionally given Claude's official skill-creator format specification. This tests whether adherence to a formal skill schema improves downstream task performance.

---

## Config Naming

Generated skill configs are named `<method>-<model>`, e.g. `b1-one-shot-claude-sonnet-4-6`. This is the directory name used in `output/skill_generation_results/` and passed to `--skill-path` during evaluation.

Special configs:

| Config | Description |
|--------|-------------|
| `human_authored` | Ground-truth skills written by task authors |
| `no_skill` | No skills injected (null baseline); pass `none` to `--skill-path` |
