---
name: run2_object-counting
description: Count template objects in keyframes using count_objects.py; parse integer from output string and generate a CSV with results per frame.
---

# Object Counting with Template Matching

## Script Location
`/root/.claude/skills/object_counter/scripts/count_objects.py`

## Usage
```bash
python3 /root/.claude/skills/object_counter/scripts/count_objects.py \
    --tool count \
    --input_image <image_file> \
    --object_image <template_image> \
    --threshold 0.9 \
    --dedup_min_dist 3
```

## Output Format
The script returns a sentence like:
```
There are 3 objects (`/root/coin.png`) in file: `/root/keyframes_001.png`
```
Parse the integer with: `grep -oP 'There are \K\d+'`

## Full Workflow: Count All Objects and Generate CSV

```bash
SCRIPT="/root/.claude/skills/object_counter/scripts/count_objects.py"

echo "frame_id,coins,enemies,turtles" > /root/counting_results.csv

for frame in $(ls /root/keyframes_*.png | sort); do
    coins=$(python3 "$SCRIPT" --tool count --input_image "$frame" \
        --object_image /root/coin.png --threshold 0.9 --dedup_min_dist 3 2>/dev/null \
        | grep -oP 'There are \K\d+')
    enemies=$(python3 "$SCRIPT" --tool count --input_image "$frame" \
        --object_image /root/enemy.png --threshold 0.9 --dedup_min_dist 3 2>/dev/null \
        | grep -oP 'There are \K\d+')
    turtles=$(python3 "$SCRIPT" --tool count --input_image "$frame" \
        --object_image /root/turtle.png --threshold 0.9 --dedup_min_dist 3 2>/dev/null \
        | grep -oP 'There are \K\d+')
    echo "$frame,${coins:-0},${enemies:-0},${turtles:-0}" >> /root/counting_results.csv
done
```

## Parameters
- `--threshold 0.9`: High confidence reduces false positives
- `--dedup_min_dist 3`: NMS deduplication prevents counting same object twice
