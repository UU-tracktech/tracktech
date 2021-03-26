import time
import os
import sys
curr_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(curr_dir, 'detection/yolov5'))

from absl import app
import cv2
import configparser
import numpy as np
from detection.dectection_obj import DetectionObj
from detection.bounding_box import BoundingBox
from detection.yolov5.yolov5_runner import Detector
from input.video_stream import VideoCapture


def main(_argv):
    """Runs YOLOv5 detection on a video file specified in configs.ini
    """
    # Load the config file, take the relevant Yolov5 section
    configs = configparser.ConfigParser(allow_no_value=True)
    configs.read(('configs.ini'))
    trueconfig = configs['Yolov5']

    t = time.localtime()

    # Instantiate the Detection Object
    det_obj = DetectionObj(t, None, 0)

    # Capture the video stream
    vidstream = VideoCapture(os.path.join(curr_dir, trueconfig['source']))

    # Instantiate the detector
    print("Instantiating detector...")
    detector = Detector(trueconfig)

    # Frame counter starts at 0. Will probably work differently for streams
    print("Starting video stream...")
    counter = 0
    while not vidstream.stopped():
        # Set the detected bounding box list to empty
        det_obj.bounding_box = []
        ret, frame = vidstream.get_next_frame()

        if not ret:
            if counter == vidstream.get_vid_length():
                print("End of file")
                break
            else:
                raise ValueError("Feed has been interrupted")

        # update frame, frame number, and time
        det_obj.frame = frame
        det_obj.frame_nr = counter
        det_obj.timestamp = time.localtime()

        detector.detect(det_obj)

        # Draw the frame with bounding boxes
        det_obj.draw_rectangles()
        counter += 1

        # Play the video in a window called "Output Video"
        try:
            cv2.imshow("Output Video", det_obj.frame)
        except Exception:
            # Figure out how to get Docker to use GUI
            print("Error displaying video. Are you running this in Docker perhaps?")

        # This next line is **ESSENTIAL** for the video to actually play
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return


if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
