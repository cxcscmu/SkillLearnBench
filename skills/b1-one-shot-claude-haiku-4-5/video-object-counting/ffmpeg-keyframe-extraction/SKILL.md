---
name: ffmpeg-keyframe-extraction
description: Extract key frames (I-frames) from video files using FFmpeg to identify scene changes and important moments.
---

# FFmpeg Keyframe Extraction

## Overview
FFmpeg can extract keyframes (I-frames) from video files. Keyframes are complete frames that don't depend on other frames for decoding, making them ideal for analysis and detection tasks.

## Installation
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

## Usage

### Extract All Keyframes from Video
```bash
ffmpeg -i input.mp4 -vf "select=eq(pict_type\,I)" -vsync 0 output_%03d.png
```

**Parameters:**
- `-i input.mp4`: Input video file
- `-vf "select=eq(pict_type\,I)"`: Filter to select only I-frames (keyframes)
- `-vsync 0`: Output one image per keyframe (important for proper numbering)
- `output_%03d.png`: Output pattern with zero-padded frame numbers (001, 002, etc.)

### Extract Keyframes with Frame Rate Control
```bash
ffmpeg -i input.mp4 -vf "fps=1/5,select=eq(pict_type\,I)" -vsync 0 output_%03d.png
```
This extracts at most 1 keyframe every 5 seconds.

### Check Video Information
```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1:noprint_wrappers=1 video.mp4
```

## Output Naming Convention
When using `output_%03d.png`:
- Frame 1: `output_001.png`
- Frame 2: `output_002.png`
- Frame 100: `output_100.png`

## Python Integration
```python
import subprocess
import os

def extract_keyframes(video_path, output_dir, output_prefix="keyframes"):
    """Extract keyframes from video file"""
    os.makedirs(output_dir, exist_ok=True)
    output_pattern = os.path.join(output_dir, f"{output_prefix}_%03d.png")

    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-vf', 'select=eq(pict_type\\,I)',
        '-vsync', '0',
        output_pattern
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg error: {result.stderr}")

    # Return list of extracted frames
    frames = sorted([
        os.path.join(output_dir, f)
        for f in os.listdir(output_dir)
        if f.startswith(output_prefix)
    ])
    return frames
```

## Tips
- Keyframes are typically smaller in file size than regular frames
- For consistent results, always use `-vsync 0` with keyframe extraction
- Output pattern with `%03d` ensures consistent naming for sorting
- Check that files are being created in the expected output directory
