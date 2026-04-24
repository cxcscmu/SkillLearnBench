---
name: super-mario-frame-analysis
description: Complete workflow for analyzing Super Mario game video frames and generating statistics. Use this skill when you need to extract video frames, process them for analysis, count game objects using template matching, and generate CSV reports of game element statistics.
---

# Super Mario Frame Analysis Workflow

This skill provides the complete workflow for analyzing Super Mario game video clips, extracting key information, and generating statistical reports.

## Complete Workflow

### Phase 1: Video Processing
1. Extract keyframes from MP4 video file
2. Convert all frames to grayscale format
3. Store frames with standardized naming: `/root/keyframes_%03d.png`

**Related skill**: `video-to-grayscale-frames`

### Phase 2: Object Detection & Counting
1. Verify template images exist (coin.png, enemy.png, turtle.png)
2. For each grayscale keyframe:
   - Count coins using coin.png template
   - Count enemies using enemy.png template
   - Count turtles using turtle.png template
3. Store counts in an organized data structure

**Related skill**: `template-object-counting`

### Phase 3: Data Analysis & Reporting
1. Compile all counting results
2. Generate CSV file with statistics
3. Ensure data integrity and completeness

## Execution Checklist

### Pre-flight Checks
- [ ] Video file exists: `/root/super-mario.mp4`
- [ ] Template images exist:
  - [ ] `/root/coin.png`
  - [ ] `/root/enemy.png`
  - [ ] `/root/turtle.png`

### Processing Steps
- [ ] Extract keyframes from video
- [ ] Convert keyframes to grayscale
- [ ] Count coins in each frame
- [ ] Count enemies in each frame
- [ ] Count turtles in each frame
- [ ] Compile results into data structure
- [ ] Generate CSV file

### Output Validation
- [ ] CSV file created at `/root/counting_results.csv`
- [ ] CSV has 4 columns: frame_id, coins, enemies, turtles
- [ ] Frame IDs follow format: `/root/keyframes_001.png`, `/root/keyframes_002.png`, etc.
- [ ] All rows have valid counts (integers)
- [ ] Rows are sorted by frame ID (chronological order)

## CSV File Format

**Location**: `/root/counting_results.csv`

**Header**:
```
frame_id,coins,enemies,turtles
```

**Data Rows** (example):
```
/root/keyframes_001.png,5,2,1
/root/keyframes_002.png,3,1,0
/root/keyframes_003.png,7,3,2
/root/keyframes_004.png,4,2,0
```

**Requirements**:
- Comma-separated values (CSV format)
- Frame IDs must include full path: `/root/keyframes_NNN.png`
- Frame IDs must use 3-digit zero-padded format: `%03d`
- Counts must be integers
- Rows must be in order from frame 001 onwards

## Expected Outputs

After completing this workflow:

1. **Keyframe files**: `/root/keyframes_001.png` through `/root/keyframes_NNN.png` (N = total keyframes)
   - All in grayscale format
   - PNG file format

2. **Results CSV**: `/root/counting_results.csv`
   - Contains statistics for all keyframes
   - Ready for analysis or visualization

## Performance Tips

- Extract only keyframes (I-frames) rather than all frames to reduce processing time
- Process frames in order to maintain timeline consistency
- Reuse template images across all frames
- Consider processing frames in batches if dealing with large videos

## Example Timeline

For a 2-minute video at 24fps with keyframes every 2 seconds:
- Expected keyframes: ~60 frames
- Processing steps: Video extraction → Grayscale conversion → Count 3 object types per frame → CSV generation
- Total object counts per frame: 3 counts × 60 frames = 180 data points in final CSV
