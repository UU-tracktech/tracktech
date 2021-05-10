"""File that displays the video stream on a localhost for testing.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import time
import os
import configparser
import logging
import tornado.web
import tornado.gen
import cv2

import processor.utils.draw as draw
from processor.input.hls_capture import HlsCapture
from processor.pipeline.detection.yolov5_runner import Yolov5Detector
from processor.pipeline.tracking.sort_tracker import SortTracker

# Tornado example gotten from: https://github.com/wildfios/Tornado-mjpeg-streamer-python
# Combined with: https://github.com/wildfios/Tornado-mjpeg-streamer-python/issues/7


class StreamHandler(tornado.web.RequestHandler):
    """Handler for the frame stream."""
    server_image_timestamp = 0

    @tornado.gen.coroutine
    def get(self):
        """Get request handler for the webpage to show video stream."""
        # Sets headers of the handler
        logging.info('set headers')
        self.set_header('Cache-Control',
                        'no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0')
        self.set_header('Pragma', 'no-cache')
        self.set_header('Content-Type', 'multipart/x-mixed-replace;boundary=--jpgboundary')
        self.set_header('Connection', 'close')

        served_image_timestamp = time.time()
        my_boundary = '--jpgboundary'

        # Load the config file, take the relevant Yolov5 section
        configs = configparser.ConfigParser(allow_no_value=True)
        __root_dir = os.path.join(os.path.dirname(__file__), '../../')
        configs.read(os.path.realpath(os.path.join(__root_dir, 'configs.ini')))

        # Instantiate the detector
        logging.info("Instantiating detector...")
        yolo_config = configs['Yolov5']
        config_filter = configs['Filter']
        detector = Yolov5Detector(yolo_config, config_filter)

        # Instantiate the tracker
        logging.info("Instantiating tracker...")
        sort_config = configs['SORT']
        tracker = SortTracker(sort_config)

        frame_nr = 0

        capture = HlsCapture()
        while capture.opened():
            ret, frame_obj = capture.get_next_frame()

            if not ret:
                continue

            # Get detections from running detection stage.
            bounding_boxes = detector.detect(frame_obj)

            # Get objects tracked in current frame from tracking stage.
            tracked_boxes = tracker.track(frame_obj, bounding_boxes)

            draw.draw_tracking_boxes(frame_obj.get_frame(), tracked_boxes.get_bounding_boxes())

            # If it does get the image the frame gets encoded
            ret, jpeg = cv2.imencode('.jpg', frame_obj.get_frame())
            img = jpeg.tobytes()

            # Every .1 seconds the frame gets sent to the browser
            interval = .1

            try:
                self.write(my_boundary)
                self.write('Content-type: image/jpeg\r\n')
                self.write('Content-length: %s\r\n\r\n' % len(img))
                self.write(img)
            except RuntimeError as err:
                logging.error(f'Client disconnected, throwing the following error: {err}')

            if served_image_timestamp + interval < time.time():
                self.flush()
                served_image_timestamp = time.time()

            frame_nr += 1

        logging.info(f'capture object stopped after {frame_nr} frames')
