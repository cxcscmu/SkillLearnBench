"""All LLM prompt templates for trajectory evaluation.

Metrics (LLM-as-judge):
  - execution_order               (1-5)
  - key_point                     (trajectory_key_point_recall)
  - planning_quality              (1-5)
  - completeness                  (1-5)

Preparation:
  - extract_oracle_compact_trajectory
  - generate_oracle_trajectory_key_points
"""

# ---------------------------------------------------------------------------
# Preparation prompts
# ---------------------------------------------------------------------------

GENERATE_ORACLE_TRAJECTORY_KEY_POINTS = """You are an expert at extracting critical execution key points from an agent trajectory.

**Important**: Extract key points only from the oracle trajectory. Do not use or refer to any oracle skill document. The only input is the task instruction and the trajectory itself—the step-by-step execution trace of an agent that successfully completed the task.

<Input>
- **Task instruction**: The task the agent was solving.
- **Oracle trajectory**: The step-by-step execution trace (tool calls, thinking, content). Use only this to identify key points.
</Input>

<Key Point Definition>
A **trajectory key point** is a critical step, decision, or action visible in the execution that is necessary for task success. Each key point should be:
- Specific to what was done in the trajectory (e.g. "Read employee_data.json to get placeholder values", "Use paragraph-level replacement for docx placeholders", "Handle conditional {{IF_RELOCATION}} section by keeping content when RELOCATION_PACKAGE is Yes").
- Stated in natural language so that another trajectory can be checked for having the same idea (recalled) or contradicting it.
- Each key point should be a single, self-contained idea or action. Every tool call should be a separate key point.
- Aim for at least 5 key points per trajectory.
</Key Point Definition>

<Instructions>
1. Read the task instruction and the oracle trajectory only.
2. Identify the essential execution steps/decisions that led to success, from the trajectory alone.
3. Output a JSON list. Each item must have exactly:
   - "reason": string (briefly why this step is critical for the task)
   - "key_point": string (clear, self-contained description of this execution point)
   - "trajectory_reference": string (a short excerpt from the oracle trajectory that supports this key point—e.g. one sentence or tool step from the trajectory text)
</Instructions>

<Output Format>
Return only a JSON array, no markdown or explanation. Field order: reason, key_point, trajectory_reference.
[
  {{ "reason": "...", "key_point": "...", "trajectory_reference": "..." }},
  ...
]

<Task instruction>
{task_instruction}
</Task instruction>

<Oracle trajectory>
{oracle_trajectory}
</Oracle trajectory>
Return JSON only, no other text.
"""


EXTRACT_ORACLE_COMPACT_TRAJECTORY = """You are an expert trajectory analyst for skill-using agents.

Your task is to convert a raw oracle trajectory trace into a **clean minimal execution trajectory**.

The output should represent the **essential sequence of actions required to successfully complete the task**.

--------------------------------------------------
Step Definition
--------------------------------------------------

A step is an **atomic task-critical action**.

Steps may include:
- a necessary tool invocation
- a required state-changing action
- a necessary navigation decision
- a required information extraction or verification step

However:

If the action is a **skill/tool invocation**, it MUST appear as its **own step**.

Never merge multiple skill/tool uses into a single step.

--------------------------------------------------
Extraction Rules
--------------------------------------------------

Granularity
- Keep steps **fine-grained**.
- Skill/tool uses must be **separate steps**.
- Non-tool reasoning should only be kept if it represents a **necessary task action**.

Noise Removal
Remove the following from the trace:
- retries of the same action
- repeated tool calls
- loops caused by agent mistakes
- debugging or diagnostic actions
- failed or invalid tool calls
- exploration that did not contribute to the final successful path

Deduplication
If the oracle trace contains repeated attempts of the same action,
keep **only the necessary and successful occurrence**.

Example:
click search
click search
click search

→ keep only the necessary and successful click.

Dependency Preservation
Maintain the **true causal order of actions** needed to finish the task.

Do NOT reorder steps unless needed to remove retries or duplicates.

Essentiality
Only keep actions that are **required for successful completion**.

Remove steps that are:
- redundant confirmations
- unnecessary scrolling
- incidental exploration
- debugging steps

--------------------------------------------------
Step Writing Style
--------------------------------------------------

Each step should be concise and represent **one atomic action**.

Required fields:

core_step
- short description of the action

why_essential
- explain why this step is required for completing the task

evidence
- a short quote or paraphrase from the oracle trace

--------------------------------------------------
Expected Trajectory Length
--------------------------------------------------

Most tasks should produce **at least 5 steps**.

Short tasks may produce fewer.

--------------------------------------------------
Output Format (STRICT JSON ONLY)
--------------------------------------------------

[
  {{
    "step_index": 1,
    "core_step": "...",
    "why_essential": "...",
    "evidence": "short quote/paraphrase from oracle trace"
  }}
]

--------------------------------------------------
Inputs
--------------------------------------------------

<Task instruction>
{task_instruction}
</Task instruction>

<Oracle trajectory trace>
{oracle_trajectory}
</Oracle trajectory trace>
"""


# ---------------------------------------------------------------------------
# LLM-as-judge metric prompts
# ---------------------------------------------------------------------------

TRAJECTORY_EXECUTION_ORDER_SCORING = """# Task
You are an expert evaluator assessing the **Execution Order Correctness** of an AI agent trajectory.

This metric evaluates whether the agent's sequence of actions respects the dependency structure of the task — that is, whether prerequisite steps are completed before the steps that depend on them, following the canonical order demonstrated by the oracle reference.

# Inputs

## Task instruction
{task_instruction}

## Oracle reference steps (canonical execution sequence)
These steps define the correct dependency order for completing this task.

{oracle_steps_summary}

## Generated trajectory
{generated_trajectory}

# Evaluation Procedure

Work through the following steps explicitly before assigning a score:

**Step 1 — Coverage check**: For each oracle reference step, determine whether the generated trajectory contains a functionally equivalent action. Apply the strict definition below:

A step is **present** only if ALL of the following hold:
- The agent actually performs the action (not merely mentions or plans it).
- The step operates on the correct inputs (right file, right data, right target).
- The step's intermediate outcome is plausibly correct — an action executed on wrong inputs or producing clearly incorrect intermediate results does not count as present, even if the action type matches.

If a step is uncertain (you cannot determine whether it was executed correctly), count it as **absent** for scoring purposes.

List each oracle step as present or absent, with brief justification.

**Step 2 — Order check**: For the steps that are present, assess whether their relative execution order respects the dependencies implied by the oracle sequence. Identify any dependency violations.

**Step 3 — Score derivation**: Apply the rubric and score caps below.

# Score Caps (strictly enforced)
- Any major oracle step absent or uncertain → maximum score **3**
- Two or more major oracle steps absent or uncertain → maximum score **2**
- Score 5 requires: **all** major oracle steps present with plausibly correct outcomes **and** executed in dependency-correct order. When in doubt about any step's correctness, cap at **4**.

# Scoring Rubric

1: Execution order is invalid, or the trajectory is missing most oracle steps.
2: Two or more major oracle steps are absent or incorrectly executed, or ordering violates multiple key dependencies.
3: One major oracle step is absent or uncertain, or ordering has notable dependency violations despite reasonable coverage.
4: All major oracle steps are present and ordered correctly, but at least one step's outcome is ambiguous or there is a minor dependency issue.
5: All major oracle steps are present with verifiably correct outcomes and executed in a dependency-correct order. No ambiguity in coverage or ordering.

# Output Format
Return strictly valid JSON only:
{{
  "score": <integer in [1,5]>,
  "reason": "<for each oracle step state present/absent/uncertain and why; note ordering violations; then justify the score>"
}}

No markdown, no extra text.
"""


TRAJECTORY_KEY_POINT_CLASSIFICATION = """You are an LLM judge for trajectory_key_point_recall. For one key point from the oracle trajectory, judge whether the generated trajectory functionally includes it (recalled), misses it (not_recalled), or contradicts it. Output only valid JSON with "label" and "reason".

<Key point (from oracle trajectory)>
{key_point}
</Key point>

<Generated trajectory>
{generated_trajectory}
</Generated trajectory>

<Definitions>
- **recalled**: The generated trajectory clearly reflects this key point: the agent performed an equivalent step, made the same decision, or applied the same procedure. Partial or vague alignment is not enough; the functional behavior must match.
- **not_recalled**: The generated trajectory does not show this key point being followed (missing step, different approach, or unclear).
- **contradiction**: The generated trajectory shows behavior that contradicts this key point (e.g. does the opposite, or follows an incompatible procedure).
</Definitions>

<Output>
Return exactly one JSON object with:
- "label": one of "recalled" | "not_recalled" | "contradiction"
- "reason": brief explanation

Example:
{{ "label": "recalled", "reason": "The agent replaced placeholders at paragraph level and cleared other runs, matching the key point." }}

Return JSON only, no other text.
"""


TRAJECTORY_PLANNING_QUALITY_SCORING = """# Task
You are an expert evaluator assessing the **Planning Quality** of an AI agent prior to task execution.

This metric evaluates the quality of any deliberate planning, goal decomposition, or strategic thinking the agent articulates *before or during its first substantive tool call* — not the execution itself.

# Inputs

## Task instruction
{task_instruction}

## Oracle reference execution path
A canonical sequence of steps required to complete this task successfully.

{oracle_compact_trajectory}

## Generated trajectory
{generated_trajectory}

# Evaluation Procedure

Work through the following steps before assigning a score:

**Step 1 — Locate the planning section**
Find any thinking, reasoning, or stated approach that appears *before the agent's first tool call*. If the agent proceeds directly to tool execution with no articulated plan or reasoning block, the maximum score is **2**.

**Step 2 — Assess Task Comprehension**
Does the agent correctly identify the specific goal, constraints, and requirements of *this* task? Identify at least one piece of task-specific understanding (e.g., naming a specific file, format, constraint, or data field mentioned in the task instruction). Generic restatements ("I will read the input and produce the output") that could apply to any task do not demonstrate task comprehension.

**Step 3 — Assess Oracle Step Coverage**
Count how many of the oracle's key steps the plan explicitly anticipates. A plan that covers fewer than half the oracle steps cannot score above **3**.

**Step 4 — Assess Specificity**
Does the plan name concrete elements from *this task* — specific filenames, tool names, data formats, or procedural details? A plan composed entirely of generic steps with no task-specific references cannot score above **3**.

**Step 5 — Assign score using the rubric below**

# Scoring Rubric

1: No discernible pre-execution thinking, or the stated plan is entirely off-task and fundamentally misidentifies the goal.
2: Agent proceeds directly to tool calls with no articulated plan, OR a plan is present but demonstrates no task-specific understanding and anticipates fewer than two oracle steps.
3: A plan is present with at least one task-specific reference, but it is predominantly generic, covers fewer than half the oracle steps, or contains a significant factual error about the task.
4: Plan is task-specific (names at least one concrete task element), covers most oracle steps, with at most one notable gap or imprecision.
5: Plan is precise and task-specific throughout, covers all major oracle steps with correct sequencing, and would require minimal revision to guide execution directly.

# Calibration Note
Most agent plans fall in the 2–4 range. Score 2 should be assigned whenever the agent dives into execution with no articulated reasoning — this is common and should not default to 3. Score 5 is reserved for plans that are demonstrably execution-ready with full oracle coverage.

# Output Format
Return strictly valid JSON only:
{{
  "score": <integer in [1,5]>,
  "reason": "<state whether a pre-execution plan was found, what task-specific elements it named, how many oracle steps it anticipated, then justify the score>"
}}

No markdown, no extra text.
"""


TRAJECTORY_COMPLETENESS_SCORING = """# Task
You are an expert evaluator assessing the **Task Completeness** of an AI agent trajectory.

This metric evaluates whether the agent reached a *correct and sufficient end state* — not merely whether it stopped executing or produced some output. Producing an output artifact does not constitute completion if that output fails to address the task requirements.

# Inputs

## Task instruction
{task_instruction}

## Oracle reference execution path
This shows what a successful completion looks like, including the type and nature of outputs produced.

{oracle_compact_trajectory}

## Generated trajectory
{generated_trajectory}

# Evaluation Procedure

Work through the following steps before assigning a score:

**Step 1 — Identify required output**
From the task instruction and oracle reference, determine precisely what the final output must be: its type (file, value, report, etc.), format, and the specific content criteria it must satisfy.

**Step 2 — Locate the agent's final output**
Find what the agent actually produced at the end of the trajectory. Quote or paraphrase it specifically. If the trajectory ends without a clear output, note this explicitly.

**Step 3 — Verify output correctness**
Compare the agent's final output against the required output from Step 1. Assess:
- Does the output have the correct type and format?
- Does the content satisfy the specific task requirements (not just "some output was written")?
- Are there signs of partial, empty, or off-target content?

If you cannot determine from the trajectory whether the output is correct, you must treat it as **unverified** — do not assume correctness.

**Step 4 — Check for failure modes**
Did the agent: (a) explicitly give up or declare inability; (b) loop without progress; (c) stop prematurely without producing output?

**Step 5 — Assign score using the rubric and caps below**

# Score Caps (strictly enforced)
- Agent gives up, declares inability, or is stuck in a loop → max score **2**
- Agent produces output but its correctness is **unverified or uncertain** from the trajectory → max score **4**
- Agent produces output that is clearly off-target, empty, or wrong → max score **3**
- Score 5 requires: output type, format, and content are all verifiably consistent with task requirements, based on explicit evidence in the trajectory

# Scoring Rubric

1: Task clearly not completed — agent gave up, is irrecoverably stuck, or the trajectory ends without meaningful progress toward the goal.
2: Severely incomplete — agent stopped prematurely, looped without resolving, or explicitly declared failure.
3: Partially complete — agent produced some output, but it is demonstrably incomplete, off-target, or structurally wrong relative to what the task requires.
4: Likely complete — agent finished and produced output of the correct type, but the output's content correctness cannot be fully verified from the trajectory alone, or minor gaps remain.
5: Fully complete — the trajectory provides explicit evidence that the final output satisfies the task's type, format, and content requirements, comparable to the oracle's completion.

# Calibration Note
Score 5 demands evidence, not assumption. If the agent wrote a file and declared completion but the trajectory does not reveal the file's contents or confirm its correctness, that is a score 4, not 5. Default to conservative scoring whenever output quality is ambiguous.

# Output Format
Return strictly valid JSON only:
{{
  "score": <integer in [1,5]>,
  "reason": "<state Step 1 required output, Step 2 actual output, Step 3 correctness verdict, Step 4 failure modes; then justify the score>"
}}

No markdown, no extra text.
"""


