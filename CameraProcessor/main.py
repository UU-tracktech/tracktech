import subprocess
import sys
import cv2

hls_url = "hls://example"

cap = cv2.VideoCapture(hls_url)

counter = 0
while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("frame read failed")
        break

    # Create detectionObj
    counter += 1
