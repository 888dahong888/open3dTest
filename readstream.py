import sys
from cv2 import cv2
video=cv2.VideoCapture("http://....hd.m3u8")
if not video.isOpened():
    print("Could not open video")
    sys.exit()
ok,frame=video.read()
if not ok:
    print("Could not read video file")
    sys.exit()
else:
    cv2.imshow("Tracking",frame)
k=cv2.waitKey(0)