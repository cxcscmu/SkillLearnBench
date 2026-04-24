---
name: template-object-counting
description: Count specific objects in images using template matching with reference object images. Use this skill when you need to detect and count game elements, sprites, or recurring visual patterns in screenshots or game frames using a template image as reference.
---

# Template-Based Object Counting

This skill provides guidance on counting objects in images using template matching techniques, commonly used for detecting game sprites, coins, enemies, and other visual elements.

## Overview

Template matching is a computer vision technique where:
1. You provide a template image (reference) of the object you want to find
2. The algorithm searches the larger image for matches
3. Matches are counted and their locations are identified

## Workflow

### Step 1: Prepare Template Images

Each object type needs a clear reference template image:
- **Coins**: `/root/coin.png` - Image showing a single coin sprite
- **Enemies**: `/root/enemy.png` - Image showing a single enemy sprite
- **Turtles**: `/root/turtle.png` - Image showing a single turtle sprite

Templates should be:
- Minimal size (just the object itself, with minimal surrounding pixels)
- Consistent with objects in the larger image
- In the same color format as the image being analyzed (grayscale for this task)

### Step 2: Use Object Counter

Use the `object_counter` skill to count objects in each frame:

```
Input:
- Frame image: /root/keyframes_001.png (grayscale)
- Template image: /root/coin.png (grayscale)

Output:
- Count of coins in the frame: integer value
```

### Step 3: Repeat for All Object Types

For each keyframe, repeat the counting process:
1. Count coins using coin.png template
2. Count enemies using enemy.png template
3. Count turtles using turtle.png template

### Step 4: Process All Frames

Iterate through all extracted keyframes:
- keyframes_001.png → count coins, enemies, turtles
- keyframes_002.png → count coins, enemies, turtles
- keyframes_003.png → count coins, enemies, turtles
- ... and so on

## Data Structure

Organize results as you process them:

| Frame ID | Coins | Enemies | Turtles |
|----------|-------|---------|---------|
| /root/keyframes_001.png | 5 | 2 | 1 |
| /root/keyframes_002.png | 3 | 1 | 0 |
| /root/keyframes_003.png | 7 | 3 | 2 |

## Output Format

After processing all frames, create a CSV file with:
- **Column 1**: frame_id (format: `/root/keyframes_%03d.png`)
- **Column 2**: coins (count)
- **Column 3**: enemies (count)
- **Column 4**: turtles (count)

Example CSV structure:
```
frame_id,coins,enemies,turtles
/root/keyframes_001.png,5,2,1
/root/keyframes_002.png,3,1,0
/root/keyframes_003.png,7,3,2
```

## Important Considerations

- **Template matching accuracy** depends on template quality and image similarity
- **Grayscale conversion** is necessary for consistent matching across frames
- **Template size matters**: Use templates that match the object size in the larger image
- **Overlapping objects** may affect accuracy; the object counter will do its best
- **Frame format**: Ensure all images are in PNG format for consistency

## Troubleshooting

- **No objects detected**: Template may not match objects in the frame; verify templates are in grayscale
- **False positives**: Template may be matching similar-looking elements; refine template if needed
- **Inconsistent counts**: Ensure all frames are in the same format (grayscale) and resolution is consistent
