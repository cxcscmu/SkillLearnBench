---
name: object-counting
description: Use this skill for counting specific objects (coins, enemies, turtles) in images using template matching.
---

# Object Counting

To count objects, use OpenCV template matching.

## Logic
1. Load the target image (frame) and the template image (coin/enemy/turtle).
2. Perform template matching (`cv2.matchTemplate`).
3. Threshold the result.
4. Count the number of matches.
