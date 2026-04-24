---
name: ffmpeg-frame-extraction
description: Use ffmpeg to extract key frames (I-frames) from a video file into a directory.
---

# FFmpeg Frame Extraction

To extract key frames (I-frames) from a video file using FFmpeg, use the following command:

```bash
ffmpeg -i input_video.mp4 -vf "select='eq(pict_type,PICT_TYPE_I)'" -vsync vfr output_folder/keyframes_%03d.png
```

- `-i input_video.mp4`: Input video file.
- `-vf "select='eq(pict_type,PICT_TYPE_I)'"`: Video filter to select only key frames.
- `-vsync vfr`: Variable frame rate to match input frame rate but only save selected frames.
- `output_folder/keyframes_%03d.png`: Output pattern for filenames.
