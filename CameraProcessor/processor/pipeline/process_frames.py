"""Contains main video processing pipeline function

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import os
import logging
import configparser

import processor.utils.draw as draw
import processor.utils.convert as convert

from processor.pipeline.framebuffer import FrameBuffer

from processor.input.video_capture import VideoCapture
from processor.input.hls_capture import HlsCapture

from processor.pipeline.detection.yolov5_runner import Yolov5Detector
from processor.pipeline.tracking.sort_tracker import SortTracker


def prepare_stream():
    """Read the configuration information and prepare the objects for the frame stream
    """
    # Load the config file
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

    # Frame counter starts at 0. Will probably work differently for streams
    logging.info("Starting stream...")

    hls_config = configs['HLS']

    hls_enabled = hls_config.getboolean('enabled')

    # Capture the video stream
    if hls_enabled:
        capture = HlsCapture(hls_config['url'])
    else:
        capture = VideoCapture(os.path.join('..', yolo_config['source']))

    # Get orchestrator configuration
    orchestrator_config = configs['Orchestrator']

    return capture, detector, tracker, orchestrator_config['url']


async def process_stream(capture, detector, tracker, func):
    """Processes a stream of frames, outputs to frame or sends to client.

    Outputs to frame using OpenCV if not client is used.
    Sends detections to client if client is used (HlsCapture).

    Args:
        capture (ICapture): capture object to process a stream of frames.
        detector (Detector): Yolov5 detector performing the detection using det_obj.
        tracker (SortTracker): tracker performing SORT tracking.
        ws_client (WebsocketClient): processor orchestrator to pass through detections.
    """
    framebuffer = FrameBuffer()

    frame_nr = 0

    while capture.opened():
        ret, frame_obj = capture.get_next_frame()

        if not ret:
            continue

        # Get detections from running detection stage.
        bounding_boxes = detector.detect(frame_obj)

        # Get objects tracked in current frame from tracking stage.
        tracked_boxes = tracker.track(frame_obj, bounding_boxes)

        draw.draw_tracking_boxes(frame_obj.get_frame(), tracked_boxes.get_bounding_boxes())

        # Buffer the tracked object
        framebuffer.add(convert.to_buffer_dict(frame_obj, tracked_boxes))
        framebuffer.clean_up()

        await func(frame_obj, tracked_boxes)

        frame_nr += 1

    logging.info(f'capture object stopped after {frame_nr} frames')
