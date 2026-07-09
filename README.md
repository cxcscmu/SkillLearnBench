<div align="center">

# SkillLearnBench

<img src="SkillLearnBench_logo.png" alt="SkillLearnBench" width="900">

[![Homepage](https://img.shields.io/badge/homepage-leaderboard-purple)](https://cxcscmu.github.io/SkillLearnBench)
[![Paper](https://img.shields.io/badge/paper-arXiv-red)](https://arxiv.org/abs/2604.20087)
[![Tasks](https://img.shields.io/badge/tasks-20-blue)](#tasks)
[![Methods](https://img.shields.io/badge/methods-4-green)](#baselines)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)

**SkillLearnBench**: A benchmark for continual learning methods that generate agent skills for real-world tasks. <br>
20 skill-dependent tasks · 15 sub-domains · 100 verified instances

🔥Exciting news!🔥 Our paper has been accepted to COLM 2026! 🎉🎉
</div>

## Installation

```bash
pip install anthropic openai rich tomli dataclaw json-repair   # tomli is only required on Python < 3.11
dataclaw --help                                                # verify that the dataclaw CLI is on your PATH
cp .env.example .env                                           # fill in your API keys (some tasks also require extra variables such as GH_TOKEN — see .env.example)
```

Docker is a hard requirement, since every agent trial runs inside a container. Install it from [docs.docker.com/get-docker](https://docs.docker.com/get-docker/).

## Quick Start of Evaluation

```bash
# Always dry-run first — preview what will run, no execution
python evaluate_skills.py court-form-filling github-repo-analytics --dry-run

# Evaluate with human-authored skills (default, `skills/human_authored`) on two tasks (court-form-filling, github-repo-analytics)
python evaluate_skills.py court-form-filling github-repo-analytics

# The committed `skills/<method>/` tree holds pre-generated skills for all baselines,
# e.g., compare method: one-shot (claude-sonnet-4-6) vs. human-authored vs. no-skill baseline.
# Warning: This command will evaluate these 3 methods across all 20 tasks in SkillLearnBench and requires some time to complete.
python evaluate_skills.py --skill-path skills/b1-one-shot-claude-sonnet-4-6 skills/human_authored none
```

When running `evaluate_skills.py`, the code will load the correspondent skills from `skill-path`, and evaluate them in the tasks of SkillLearnBench.
Evaluation results are written to `output/evaluation_reports/<method>/<task>/`, a `report.csv` record the average results of each metrics.

⚠️ Keep `--max-workers` ≤ 50 to avoid API rate limits. 


<a id="tasks"></a>
### (1) Tasks

SkillLearnBench contains 20 tasks across 6 real-world categories, with 100 instances in total.

| Category | Task | Instances |
|---|---|:---:|
| **Software Engineering** | python-scala-translation | 2 |
| | nlp-paper-reproduction | 3 |
| | dependency-vulnerability-check | 5 |
| | github-repo-analytics | 5 |
| | fix-security-bug | 3 |
| **Information Retrieval** | enterprise-information-search | 6 |
| | travel-planning | 5 |
| **Productivity Tools** | schedule-planning | 5 |
| | offer-letter-generator | 6 |
| | court-form-filling | 6 |
| **Data & Analytics** | earthquake-plate-calculation | 6 |
| | financial-analysis | 6 |
| | weighted-gdp-calculation | 6 |
| | dbscan-parameter-tuning | 5 |
| | stock-data-visualization | 5 |
| **Content & Creative** | anthropic-poster-design | 5 |
| | chinese-poem-generator | 5 |
| | video-object-counting | 5 |
| **Utilities & Other** | organize-messy-files | 6 |
| | temperature-simulation | 5 |

### (2) Evaluation Dimensions 

| Dimension | Metrics | What it measures |
|-----------|---------|-----------------|
| **Task Success** | Pass rate | Binary verifier outcome per trial |
| **Skill Quality** | Functional coverage, executability, safety | How well a skill describes the task and avoids unsafe instructions |
| **Trajectory Quality** | Key-point recall, execution order, completeness | Whether the solving agent's action trace matches the expected solution path |

The solving agent is powered by Claude Sonnet 4.6, and the LLM-as-judge uses GPT-5-mini.

## Baselines

We implement four continual learning methods based on skill generation.

| ID | Name | Description |
|----|------|-------------|
| b1 | One-Shot | The agent generates a skill set in a single pass. |
| b2 | Self-Feedback | The agent first generates an initial skill set and uses it to attempt the task. After execution, it reviews the trajectory, identifies issues, and refines the skills. This cycle repeats K=2 times (i.e., K−1 rounds of feedback) without any external supervision. |
| b3 | Teacher-Feedback | After each failed attempt, the agent asks the teacher questions, and the teacher provides directional guidance without revealing the ground-truth skill. The agent then updates its skills and retries the task. The skill set is regenerated up to K=3 times, with up to K−1 QA rounds triggered by failed attempts. This setting simulates a domain expert helping the agent improve. |
| b4 | Skill Creator | Claude's official skill-creator. The agent follows a structured multi-stage process: analyzing the task intent, investigating edge cases and dependencies, writing a skill specification, and validating it with automated checks. |

The agent can be powered by any LLM. In our codebase we provide results for Claude and Gemini (claude-haiku-4-5, claude-sonnet-4-6, and claude-opus-4-6; gemini-3.1-flash-lite-preview, gemini-3-flash-preview, and gemini-3.1-pro-preview).

Run a baseline to generate skills:
```bash
python generate_skills.py --tasks court-form-filling --methods b1-one-shot --models claude-sonnet-4-6
```


### (1) Evaluate other LLMs with the existing four baselines

You can plug additional LLMs into the four baselines above. See [BASELINES.md](BASELINES.md) for more details.

### (2) Evaluate other continual learning methods

To evaluate your own continual learning method, use the [tasks](./tasks) folder, which provides the verifier (in each `tests` subfolder) and the instance data for every task. Feed the `instance-1` information together WITHOUT its verifier into your method to generate skills. The generated skills should follow the same layout as any subfolder in [skills](./skills/). Then evaluate your method with `python evaluate_skills.py --skill-path your_skill_path`.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full set of options and instructions on adding new methods.


## Citation

```bibtex
@article{zhong2026skilllearnbench,
  title={SkillLearnBench: Benchmarking Continual Learning Methods for Agent Skill Generation on Real-World Tasks},
  author={Zhong, Shanshan and Lu, Yi and Ning, Jingjie and Wan, Yibing and Feng, Lihan and Ao, Yuyi and Ribeiro, Leonardo F. R. and Dreyer, Markus and Ammirati, Sean and Xiong, Chenyan},
  journal={arXiv preprint arXiv:2604.20087},
  year={2026},
  url={https://arxiv.org/abs/2604.20087}
}
```
