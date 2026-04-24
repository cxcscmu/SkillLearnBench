---
name: run2_template-matching-tuning
description: Tune OpenCV template matching parameters (threshold and dedup distance) for accurate object counting in pixel-art games.
---

# Template Matching Parameter Tuning for Pixel-Art Games

## Tool

```bash
python3 /root/.claude/skills/object_counter/scripts/count_objects.py \
    --tool count \
    --input_image <frame.png> \
    --object_image <template.png> \
    --threshold <float> \
    --dedup_min_dist <float>
```

## Parameter Tuning Strategy

### Threshold
- **0.9** (default): Strict matching. Works when objects appear identical to template.
- **0.75-0.85**: Better for pixel-art games where objects have animation frames (e.g., spinning coins show different faces).
- **Below 0.7**: Too many false positives from similar-colored regions.

### dedup_min_dist
- **3** (default): Works for very small templates but can double-count larger objects.
- **5-10**: Better for game sprites (~16-32px wide). Prevents overlapping detections.

## Recommended Parameters for Super Mario

| Object  | Threshold | dedup_min_dist | Rationale |
|---------|-----------|----------------|-----------|
| Coin    | 0.75      | 5              | Coins have multiple animation frames; lower threshold catches rotated coins |
| Enemy   | 0.9       | 5              | Goombas are distinctive and consistent in appearance |
| Turtle  | 0.9       | 5              | Koopa turtles are distinctive; 0.9 avoids false positives from terrain |

## Tuning Process

1. Start with threshold=0.9, dedup=3 (recommended defaults)
2. Visually inspect each frame to count expected objects
3. Sweep thresholds (0.9, 0.85, 0.8, 0.75, 0.7) while checking for:
   - False negatives (objects missed → lower threshold)
   - False positives (non-objects counted → raise threshold or dedup_min_dist)
4. Increase dedup_min_dist if duplicate detections appear at lower thresholds
5. Different object types may need different optimal thresholds

## Key Insight

The HUD coin icon (top of screen) is very small and typically doesn't match the template at normal thresholds. Game coins in the play area are larger and match well.
