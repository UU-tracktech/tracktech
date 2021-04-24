""" Main file running the video processing pipeline.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import sys
import logging
import os
import asyncio
import configparser
from absl import app

from processor.pipeline.detection.yolov5_runner import Yolov5Detector
from processor.input.video_capture import VideoCapture
from processor.input.hls_capture import HlsCapture
import processor.websocket_client as client
from processor.pipeline.process_frames import process_stream
from processor.pipeline.tracking.sort_tracker import SortTracker


def main(_):
    """Setup for logging and starts pipeline by reading in config information.

    Args:
        _ (list): list of arguments passed to main, contains file path per default.
    """
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

    asyncio.get_event_loop().run_until_complete(initialize(vid_stream, detector, tracker, orchestrator_config['url']))


async def initialize(vid_stream, detector, tracker, url):
    """Initialize the websocket client connecting to the processor orchestrator when a HLS stream is used.

    Args:
        vid_stream (ICapture): video stream object.
        detector (Yolov5Detector): detector object performing yolov5 detections.
        tracker (SortTracker): tracker performing SORT tracking.
        url (str): url to the processor orchestrator.
    """
    if isinstance(vid_stream, HlsCapture):
        ws_id = vid_stream.hls_url
        ws_client = await client.create_client(url, ws_id)
    else:
        ws_client = None

    await process_stream(vid_stream, detector, tracker, ws_client)


if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
