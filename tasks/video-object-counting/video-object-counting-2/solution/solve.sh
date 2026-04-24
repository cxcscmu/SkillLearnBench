#!/bin/bash

wd=/root
PYTHON=python3

echo "Using ffmpeg to extract keyframes from video"
ffmpeg -i $wd/super-mario.mp4 -vf "select='eq(pict_type,I)'" -vsync vfr $wd/keyframes_%03d.png

echo "Converting keyframes to gray scale images"
for img in `ls $wd/keyframes_*.png`; do
    convert $img -colorspace Gray $img
done

cat > /tmp/count_obj.py << 'PYTHON_SCRIPT'
import sys
import cv2 as cv
import numpy as np

in_img_file = sys.argv[1]
obj_img_files = sys.argv[2:]
threshold = 0.9
dedup_min_dist = 3.0

img_rgb = cv.imread(in_img_file)
assert img_rgb is not None, "file could not be read, check with os.path.exists()"
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
candidate_points = []
for obj_img_file in obj_img_files:
    template = cv.imread(obj_img_file)
    assert template is not None, f"file {obj_img_file} could not be read, check with os.path.exists()"
    template = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    candidate_points.extend(zip(*loc[::-1]))

candidate_points = sorted(candidate_points, key=lambda p: (p[1], p[0]))

uniq_points = []
def L2_dist(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

for pt in candidate_points:
    if len(uniq_points) == 0:
        uniq_points.append(pt)
    else:
        closest_d = min(L2_dist(pt, p) for p in uniq_points)
        if closest_d > dedup_min_dist:
            uniq_points.append(pt)
print(len(uniq_points), end='')

PYTHON_SCRIPT

out_f=$wd/counting_results.csv
echo "frame_id,coins,turtles" > $out_f
coin_templates=($wd/coin[0-9]*.png)
turtle_templates=($wd/turtle[0-9]*.png)

for img in `ls $wd/keyframes_*.png`; do
    echo $img
    # for each frame, put counted numbers
    echo -n "$img" >> $out_f
    echo -n , >> $out_f
    $PYTHON /tmp/count_obj.py $img "${coin_templates[@]}" >> $out_f
    echo -n , >> $out_f
    $PYTHON /tmp/count_obj.py $img "${turtle_templates[@]}" >> $out_f
    echo "" >> $out_f
done
