import sys
import logging
import time
import os
from absl import app
import cv2
import configparser
from src.pipeline.detection.detection_obj import DetectionObj
from src.pipeline.detection.yolov5_runner import Detector
from src.input.video_capture import VideoCapture


def main(arg):
    # Logging doesn't work in main function without this,
    # but it must be in main as it gets removed by documentation.py otherwise.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(filename='main.log', filemode='w',
                        format='%(asctime)s %(levelname)s %(name)s - %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    # Load the config file, take the relevant Yolov5 section
    configs = configparser.ConfigParser(allow_no_value=True)
    configs.read(('../configs.ini'))
    yolo_config = configs['Yolov5']

    t = time.localtime()

    # Instantiate the Detection Object
    det_obj = DetectionObj(t, None, 0)

    # Capture the video stream
    vid_stream = VideoCapture(os.path.join('..', yolo_config['source']))

    # Instantiate the detector
    logging.info("Instantiating detector...")
    detector = Detector(yolo_config)

    # Frame counter starts at 0. Will probably work differently for streams
    logging.info("Starting video stream...")
    frame_nr = 0
    while vid_stream.opened():
        # Set the detected bounding box list to empty
        det_obj.bounding_box = []
        ret, frame = vid_stream.get_next_frame()

        if not ret:
            if frame_nr == vid_stream.get_vid_length():
                logging.info("End of file")
                break
            else:
                raise ValueError("Feed has been interrupted")

        # update frame, frame number, and time
        det_obj.frame = frame
        det_obj.frame_nr = frame_nr
        det_obj.timestamp = time.localtime()

        detector.detect(det_obj)

        # Draw the frame with bounding boxes
        det_obj.draw_rectangles()
        frame_nr += 1

        # Play the video in a window called "Output Video"
        try:
            cv2.imshow("Output Video", det_obj.frame)
        except OSError:
            # Figure out how to get Docker to use GUI
            raise OSError("Error displaying video. Are you running this in Docker perhaps?")

        # This next line is **ESSENTIAL** for the video to actually play
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return
    
    logging.info(f'capture object stopped after {frame_nr} frames')


if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
