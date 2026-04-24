---
name: run2_object_counting_optimized
description: Robust object counting using template matching with parameter tuning.
---

# Robust Object Counting

Template matching counting requires careful tuning of the `threshold` and `dedup_min_dist`.

## Parameters

- **Threshold (`--threshold`)**: 
  - Values closer to `1.0` require a near-perfect match.
  - `0.9` is a good balance for high-fidelity detection.
  - Decrease if objects are slightly varied or distorted.

- **Deduplication Distance (`--dedup_min_dist`)**:
  - The minimum distance (in pixels) between two detections to consider them separate objects.
  - Set this roughly to the size of the object to avoid multiple hits on the same instance.

## Usage Example

```bash
python3 /root/.agents/skills/object_counter/scripts/count_objects.py \
    --tool count \
    --input_image frame_001.png \
    --object_image template.png \
    --threshold 0.85 \
    --dedup_min_dist 10
```

## Tips
- Ensure both the input image and the template image are in the same colorspace (e.g., both Grayscale).
- The template image should be a tight crop of the object you want to count.
