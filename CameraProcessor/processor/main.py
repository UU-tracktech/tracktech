"""Main file running the video processing pipeline.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import sys
import logging
import os
import asyncio
import configparser
import cv2
from absl import app

import tornado.ioloop
import tornado.web

import processor.utils.text as text
import processor.utils.draw as draw

from processor.pipeline.detection.yolov5_runner import Yolov5Detector
from processor.input.video_capture import VideoCapture
from processor.input.hls_capture import HlsCapture
from processor.pipeline.process_frames import process_stream
from processor.pipeline.tracking.sort_tracker import SortTracker

import processor.webhosting.websocket_client as client


def main():
    """Setup for logging and starts pipeline by reading in config information.

    Args:
        _ (list): list of arguments passed to main, contains file path per default.
    """
    # Load the config file, take the relevant Yolov5 section
    configs = configparser.ConfigParser(allow_no_value=True)
    __root_dir = os.path.join(os.path.dirname(__file__), '../')
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

    # Frame counter starts at 0. Will probably work differently for streams
    logging.info("Starting video stream...")

    hls_config = configs['HLS']

    hls_enabled = hls_config.getboolean('enabled')

    # Capture the video stream
    if hls_enabled:
        vid_stream = HlsCapture(hls_config['url'])
    else:
        vid_stream = VideoCapture(os.path.join('..', yolo_config['source']))

    # Get orchestrator configuration
    orchestrator_config = configs['Orchestrator']

    return vid_stream, detector, tracker, orchestrator_config['url']


async def __send_orchestrator(ws_client, frame_obj, tracked_boxes):
    """Sends the bounding boxes to the orchestrator

    Args:
        frame_obj (FrameObj): Frame object on which drawing takes place
        tracked_boxes (BoundingBoxes):
    """
    client_message = text.bounding_boxes_to_json(tracked_boxes, frame_obj.get_timestamp())
    ws_client.write_message(client_message)
    logging.info(client_message)
    await asyncio.sleep(0)


async def __opencv_display(frame_obj, tracked_boxes):
    """Displays frame using the imshow of opencv

    Args:
        frame_obj (FrameObj): Frame object on which drawing takes place
        tracked_boxes (BoundingBoxes):
    """
    # Copy frame to draw over.
    frame_copy = frame_obj.get_frame().copy()

    # Draw bounding boxes with ID
    draw.draw_tracking_boxes(frame_copy, tracked_boxes.get_bounding_boxes())

    # Play the video in a window called "Output Video"
    try:
        cv2.imshow("Output Video", frame_copy)
    except OSError as err:
        # Figure out how to get Docker to use GUI
        raise OSError("Error displaying video. Are you running this in Docker perhaps?") \
            from err

    # This next line is **ESSENTIAL** for the video to actually play
    if cv2.waitKey(1) & 0xFF == ord('q'):
        exit()


async def initialize(vid_stream, detector, tracker, url):
    """Initialize the websocket client connecting to the processor orchestrator when a HLS stream is used.

    Args:
        vid_stream (ICapture): video stream object.
        detector (Yolov5Detector): detector object performing yolov5 detections.
        tracker (SortTracker): tracker performing SORT tracking.
        url (str): url to the processor orchestrator.
    """
    func = None
    if isinstance(vid_stream, HlsCapture):
        ws_id = vid_stream.hls_url
        ws_client = await client.create_client(url, ws_id)
        func = lambda frame_obj, bounding_boxes: __send_orchestrator(ws_client, frame_obj, bounding_boxes)
    else:
        ws_client = None
        func = __opencv_display

    await process_stream(vid_stream, detector, tracker, func)

if __name__ == '__main__':
    # Configure the logging
    logging.basicConfig(filename='main.log', filemode='w',
                        format='%(asctime)s %(levelname)s %(name)s - %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')

    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    vid_stream, detector, tracker, url = main()

    try:
        asyncio.get_event_loop().run_until_complete(
            initialize(vid_stream, detector, tracker, url))
    except SystemExit:
        pass
