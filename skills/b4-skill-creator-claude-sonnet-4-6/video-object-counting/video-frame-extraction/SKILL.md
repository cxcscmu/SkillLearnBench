---
name: video-frame-extraction
description: Extract key frames (I-frames) from video files using FFmpeg. Use this skill whenever the user needs to pull keyframes, thumbnails, or important frames from MP4, MKV, AVI, or other video formats. Outputs PNG image files named with zero-padded indices (e.g., keyframes_001.png).
---

# Video Frame Extraction with FFmpeg

Extract I-frames (keyframes) from a video file and save them as sequentially numbered PNG images.

## Command

```bash
ffmpeg -i <input_video> -vf "select=eq(pict_type\,I)" -vsync vfr <output_dir>/keyframes_%03d.png
```

- `select=eq(pict_type\,I)` — selects only I-frames (intra-coded keyframes)
- `-vsync vfr` — variable frame rate output to avoid duplicates
- `%03d` — zero-padded 3-digit index starting at 1 (e.g., 001, 002, ...)

## Example

```bash
ffmpeg -i /root/super-mario.mp4 -vf "select=eq(pict_type\,I)" -vsync vfr /root/keyframes_%03d.png
```

Output files: `/root/keyframes_001.png`, `/root/keyframes_002.png`, etc.

## Listing Extracted Frames

After extraction, list frames sorted by name to get timeline order:

```python
import glob, os
frames = sorted(glob.glob('/root/keyframes_*.png'))
```

## Notes

- I-frames are the most information-rich frames and good representatives for scene analysis.
- Frame indices start at 1, not 0.
- If the video has no explicit I-frames, use `-vf fps=1` to extract one frame per second instead.
