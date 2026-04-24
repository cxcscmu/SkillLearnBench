---
name: object_counting
description: Count objects in an image using the command-line interface of the object detection script.
---
Execute the object detection tool from the command line for each frame and specific target object. The tool is invoked via `python3 scripts/count_objects.py`. 

Example usage:
```bash
python3 scripts/count_objects.py --image /root/keyframes_001.png --template /root/coin.png
```
Capture the standard output of this command to retrieve the count for the specified object in the frame.