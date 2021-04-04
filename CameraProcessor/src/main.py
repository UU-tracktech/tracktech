import sys
import logging
import os
import configparser
import asyncio
from absl import app
from src.pipeline.detection.detection_obj import DetectionObj
from src.pipeline.detection.yolov5_runner import Detector
from src.input.video_capture import VideoCapture
from src.input.hls_capture import HlsCapture
from src.pipeline.process_frames import process_stream


def main():
    """Setup for logging and starts pipeline by reading in config information.

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
    configs.read(('../configs.ini'))
    yolo_config = configs['Yolov5']

    # Instantiate the Detection Object
    det_obj = DetectionObj(None, None, 0)

    # Instantiate the detector
    logging.info("Instantiating detector...")
    detector = Detector(yolo_config)

    # Frame counter starts at 0. Will probably work differently for streams
    logging.info("Starting video stream...")

    hls_config = configs['HLS']

    hls_enabled = hls_config.getboolean('enabled')

    # Capture the video stream
    if hls_enabled:
        vid_stream = HlsCapture(hls_config['url'])
    else:
        vid_stream = VideoCapture(os.path.join('..', yolo_config['source']))

    asyncio.get_event_loop().run_until_complete(process_stream(vid_stream,
                                                               det_obj, detector, hls_enabled))


if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
