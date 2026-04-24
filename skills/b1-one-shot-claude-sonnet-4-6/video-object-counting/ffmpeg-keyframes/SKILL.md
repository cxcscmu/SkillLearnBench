---
name: ffmpeg-keyframes
description: Extract I-frame keyframes from video files using FFmpeg command line, saving them as numbered PNG images.
---

# FFmpeg Keyframe Extraction

## Installation
```bash
sudo apt-get install ffmpeg
# or: conda install -c conda-forge ffmpeg
```

## Extract All I-Frame Keyframes
```bash
ffmpeg -i input.mp4 -vf "select=eq(pict_type\,I)" -vsync vfr /output/keyframes_%03d.png
```
- `select=eq(pict_type\,I)` — selects only I-frames (keyframes)
- `-vsync vfr` — variable frame rate to avoid duplicate frames
- `%03d` — zero-padded 3-digit frame numbering (001, 002, ...)

## Extract Frames at Fixed Interval
```bash
ffmpeg -i input.mp4 -vf "fps=1" /output/frame_%03d.png   # 1 frame per second
ffmpeg -i input.mp4 -vf "fps=0.5" /output/frame_%03d.png # 1 frame every 2 seconds
```

## Get Video Info
```bash
ffprobe -v quiet -print_format json -show_streams input.mp4
```

## Python Wrapper
```python
import subprocess, glob, os

def extract_keyframes(video_path, output_dir, pattern="keyframes_%03d.png"):
    os.makedirs(output_dir, exist_ok=True)
    output_pattern = os.path.join(output_dir, pattern)
    cmd = [
        "ffmpeg", "-i", video_path,
        "-vf", "select=eq(pict_type\\,I)",
        "-vsync", "vfr",
        output_pattern, "-y"
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    frames = sorted(glob.glob(os.path.join(output_dir, "keyframes_*.png")))
    return frames
```

## Notes
- I-frames are self-contained frames, ideal as keyframes for analysis
- Output numbering starts at 1 by default (001, 002, ...)
- Use `-y` to overwrite existing files without prompting
