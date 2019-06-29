import sys
from PIL import Image
import numpy as np
import cv2

v = cv2.VideoCapture('anime2.mp4')
v.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)

frames = v.get(cv2.CAP_PROP_FRAME_COUNT)
fps = v.get(cv2.CAP_PROP_FPS)

total_seconds = round(frames/fps)

s = int(total_seconds%60)
m = int((total_seconds/60)%60)
h = int((total_seconds/60/60))

print(str(h).zfill(2) + ':' + str(m).zfill(2) + ':' + str(s).zfill(2))
