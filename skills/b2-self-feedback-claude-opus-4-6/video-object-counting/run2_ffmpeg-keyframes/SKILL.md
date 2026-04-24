---
name: run2_ffmpeg-keyframes
description: Extract I-frame keyframes from video files using FFmpeg, with output verification and naming conventions.
---

# FFmpeg Keyframe Extraction

## Command

```bash
ffmpeg -i input.mp4 -vf "select='eq(pict_type,I)'" -vsync vfr /root/keyframes_%03d.png
```

## Key Details

- Output numbering starts at `001` (not `000`)
- `-vsync vfr` prevents duplicate frames
- `%03d` gives zero-padded 3-digit numbering
- Frame count depends on encoding; check output to know total frames

## Verification

After extraction, verify frame count:
```bash
ls /root/keyframes_*.png | wc -l
```

## Notes

- For Super Mario gameplay video (~27 seconds), expect ~8 keyframes
- PNG format is lossless, ideal for subsequent template matching
- Frames are in timeline order by default
