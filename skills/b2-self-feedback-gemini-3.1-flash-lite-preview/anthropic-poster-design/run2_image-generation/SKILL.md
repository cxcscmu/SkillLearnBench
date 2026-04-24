---
name: run2_image-generation
description: Enhanced skill for programmatic design, incorporating system-level dependency management for image generation libraries.
---
# Image Generation Skill (V2)

Use this skill for:
- Creating technical exploded-view diagrams in headless environments.
- Ensuring all system-level dependencies (`python3-pil`) are verified prior to execution.
- Applying Anthropic brand tokens precisely to visual assets.

## Execution Workflow
1. Verify system dependencies via `apt`.
2. Generate assets using Python Imaging Library (PIL).
3. Validate final file sizes and existence.
