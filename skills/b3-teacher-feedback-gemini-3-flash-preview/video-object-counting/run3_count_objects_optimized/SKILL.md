---
name: count_objects_optimized
description: Counts occurrences of specific objects (coins, enemies, turtles) in a frame using a template matching script with optimized parameters.
---

To count objects accurately, call the `count_objects_optimized.py` script using `python3`. You must specify the counting tool mode and maintain a high confidence threshold to ensure fidelity.

Command structure:
`python3 count_objects_optimized.py --tool count --input_image <frame_path> --object_image <template_path> --dedup_min_dist <distance> --threshold 0.9`

Arguments:
- `--tool count`: Required parameter to activate the counting logic.
- `--input_image`: The path to the keyframe being analyzed (e.g., `/root/keyframes_001.png`).
- `--object_image`: The path to the template image (e.g., `/root/coin.png`).
- `--dedup_min_dist`: The minimum pixel distance between detected objects to prevent double-counting the same object (e.g., 10 or 15 depending on object size).
- `--threshold 0.9`: Sets the confidence threshold for a match to 0.9 to ensure only high-confidence detections are counted.