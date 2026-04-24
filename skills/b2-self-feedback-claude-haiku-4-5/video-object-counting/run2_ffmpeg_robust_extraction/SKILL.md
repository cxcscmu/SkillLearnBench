---
name: run2_ffmpeg_robust_extraction
description: Robust FFmpeg video frame extraction with error handling, alternative methods, and comprehensive frame selection strategies.
---

# Robust FFmpeg Frame Extraction

## Overview
Extract frames from video files using FFmpeg with multiple extraction strategies, comprehensive error handling, and verification.

## Installation & Verification
```bash
ffmpeg -version
```

## Frame Extraction Strategies

### Strategy 1: Key Frame Only (I-Frames) - Best for Edits
Extracts only I-frames (key frames that contain complete frame data):
```bash
ffmpeg -i input.mp4 -vf "select='eq(pict_type,I)'" -vsync 0 output_%03d.png
```
- **Best for**: Videos with clear scene changes
- **Pros**: Minimal output files, lowest disk usage
- **Cons**: May miss fast-moving objects between keyframes

### Strategy 2: Fixed Frame Rate - Best for Smooth Motion
Extract frames at a fixed rate (e.g., 1 FPS, 5 FPS):
```bash
ffmpeg -i input.mp4 -vf fps=1 output_%03d.png
```
- **Best for**: Consistent time-based sampling
- **Pros**: Regular time intervals, predictable output count
- **Cons**: May be too many frames for long videos

### Strategy 3: Every Nth Frame
Extract every Nth frame from the video:
```bash
ffmpeg -i input.mp4 -vf "select='isnan(prev_selected_t)+gte(t\-prev_selected_t,2)'" -vsync 0 output_%03d.png
```
- **Best for**: Uniform frame sampling
- **Pros**: Captures motion details
- **Cons**: Requires calculation for desired interval

## Python Wrapper with Error Handling

```python
import subprocess
import os
import glob

def extract_frames(input_video, output_pattern, method='keyframe'):
    """
    Extract frames from video with error handling

    Args:
        input_video: Path to input video file
        output_pattern: Output path pattern (e.g., '/root/frames_%03d.png')
        method: 'keyframe' (I-frames only) or 'fps1' (1 frame per second)

    Returns:
        List of extracted frame paths, or None on error
    """

    # Validate input
    if not os.path.exists(input_video):
        print(f"Error: Video file not found: {input_video}")
        return None

    # Choose FFmpeg filter based on method
    if method == 'keyframe':
        vf = "select='eq(pict_type,I)'"
        vsync = "-vsync 0"
    elif method == 'fps1':
        vf = "fps=1"
        vsync = ""
    else:
        print(f"Error: Unknown method: {method}")
        return None

    # Build FFmpeg command
    cmd = f'ffmpeg -i "{input_video}" -vf "{vf}" {vsync} "{output_pattern}" 2>&1'

    # Run extraction
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"FFmpeg error: {result.stderr}")
        return None

    # Verify output files exist
    output_dir = os.path.dirname(output_pattern)
    output_prefix = os.path.basename(output_pattern).replace('%03d', '')

    frames = sorted(glob.glob(os.path.join(output_dir, output_prefix.replace('.png', '')+'*.png')))

    if not frames:
        print("Error: No frames were extracted")
        return None

    print(f"Successfully extracted {len(frames)} frames")
    return frames

# Usage
frames = extract_frames('/root/super-mario.mp4', '/root/keyframes_%03d.png', method='keyframe')
```

## Video Information Query
Get video details before extraction:
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate,duration -of default=noprint_wrappers=1 input.mp4
```

## Best Practices
1. **Always validate input file** before running FFmpeg
2. **Check available disk space** - frames require significant storage
3. **Verify output files** after extraction completes
4. **Use absolute paths** to avoid working directory issues
5. **Quote file paths** with spaces properly
