---
name: travel-planning-workflow
description: Invoke this skill when performing travel planning. It defines a structured workflow for generating itineraries. Following this workflow is essential to ensure the final plan satisfies user requirements.
---

# Overview

**This skill provides a travel planning workflow. It is important to follow this workflow.**
**IMPORTANT:Do not forget to perform final validation and refinement.**

---


# Travel Planning Workflow

## Step 1: User Preference and Constraint Analysis

Extract the user's requirements and implicit preferences, including: Trip duration, Number of travelers, Budget constraints, Transportation constraints (e.g., no flights), Special requirements (e.g., pet-friendly accommodations), Food preferences (e.g., American, Mediterranean, Chinese, Italian)

**Default assumption:**
If not explicitly specified, each day should include at least one activity (i.e., no empty days).

---

## Step 2: Global Planning and Sequential Scheduling

### 2.1 Global Skeleton Construction

- Select candidate cities based on user constraints and dataset availability
- Construct a preliminary travel route (considering distance and feasibility)
- Allocate the total number of days across selected cities as a draft plan

---

### 2.2 Sequential Day-by-Day Planning

Generate the itinerary in chronological order:

Using the provided tools, and for each day:
- **Assign one attraction per day**, unless the user explicitly indicates that they do not want to go out.
- **Assign meals** based on cuisine preferences
- **Assign accommodation** (must satisfy constraints such as pet-friendly)

---

### 2.3 Iterative Adjustment and Backtracking

During planning, continuously validate feasibility. For example:

- If a city does not have enough attractions → reduce its allocated days
- If all cities combined still lack sufficient attractions → reselect cities
- If constraints are violated (budget, accomodations, etc.) → adjust previous steps

This step introduces a **feedback loop**, allowing the system to revise earlier decisions.

---

## Step 3: Important!! Final Validation and Refinement
Before returning the final itinerary, the agent must perform an explicit final validation pass. The validation should check:
- **All user constraints must be satisfied**, including transportation constraints (e.g., no flights), special requirements (e.g., pet-friendly accommodations, which should be explicitly reflected using keywords such as pet or animal), and food preferences (e.g., American, Mediterranean, Chinese, and Italian cuisines).
- **Each day includes at least one attraction, including both the first day and last day** (unless the user explicitly indicates that they do not want to go out.)
- **Travel transitions between cities are feasible**
- **The itinerary format is complete and consistent**, with no missing or contradictory information.

**Please refine the itinerary if any violations or inconsistencies are detected**




