---
name: Extract Video Keyframes to PNG
description: Converts an MP4 video file into individual keyframe PNG images. Use this to decompose a video into analyzable still frames. Extracts one keyframe per scene and stores them in the root directory with sequential naming.
---

```bash
#!/bin/bash

ffmpeg -i /root/super-mario.mp4 -vf "select=gt(scene\,0.4),fps=1/1" -vsync vfr /root/keyframes_%03d.png
```