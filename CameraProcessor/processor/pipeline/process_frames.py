"""Contains main video processing pipeline function

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import sys
import logging
import asyncio
import cv2

import processor.utils.convert as convert

from processor.input.video_capture import VideoCapture
from processor.input.hls_capture import HlsCapture
import processor.utils.text as text
import processor.utils.display as display

from processor.pipeline.framebuffer import FrameBuffer
from processor.pipeline.detection.yolov5_runner import Yolov5Detector
from processor.pipeline.tracking.sort_tracker import SortTracker

from processor.webhosting.start_command import StartCommand
from processor.webhosting.stop_command import StopCommand


def prepare_stream(configs):
    """Read the configuration information and prepare the objects for the frame stream

    Args:
        configs (ConfigParser): Configuration of the application when preparing the stream

    Returns:
        (ICapture, Yolov5Detector, SortTracker, str): Capture instance, a detector and tracker and a websocket_id
    """
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
        capture = VideoCapture(yolo_config['source_path'])

    # Get orchestrator configuration
    orchestrator_config = configs['Orchestrator']

    return capture, detector, tracker, orchestrator_config['url']


async def process_stream(capture, detector, tracker, on_processed_frame, ws_client=None):
    """Processes a stream of frames, outputs to frame or sends to client.

    Outputs to frame using OpenCV if not client is used.
    Sends detections to client if client is used (HlsCapture).

    Args:
        capture (ICapture): capture object to process a stream of frames.
        detector (Detector): Yolov5 detector performing the detection using det_obj.
        tracker (SortTracker): tracker performing SORT tracking.
        on_processed_frame (Function): when the frame got processed. Call this function to handle effects
        ws_client (WebsocketClient): The websocket client so the message queue can be emptied
    """
    framebuffer = FrameBuffer()

    frame_nr = 0

    while capture.opened():
        ret, frame_obj = capture.get_next_frame()

        if not ret:
            continue

        # Get detections from running detection stage.
        detected_boxes = detector.detect(frame_obj)

        # Get objects tracked in current frame from tracking stage.
        tracked_boxes = tracker.track(frame_obj, detected_boxes)

        # Buffer the tracked object
        framebuffer.add(convert.to_buffer_dict(frame_obj, tracked_boxes))
        framebuffer.clean_up()

        # Handle side effects of frame processing
        await on_processed_frame(frame_obj, detected_boxes, tracked_boxes)

        # Process the message queue if there is a websocket connection
        if ws_client is not None:
            process_message_queue(ws_client)

        frame_nr += 1

    logging.info(f'capture object stopped after {frame_nr} frames')


def process_message_queue(ws_client):
    """Processes the message queue processing each start and stop command

    Args:
        ws_client (WebsocketClient): Websocket client to get the message queue from
    """
    # Empty queue if there are messages left that were not sent
    while len(ws_client.message_queue) > 0:
        logging.info(ws_client.message_queue)
        track_elem = ws_client.message_queue.popleft()
        # Start command
        if isinstance(track_elem, StartCommand):
            logging.info(f'Start tracking box {track_elem.box_id} in frame_id {track_elem.frame_id} '
                         f'with new object id {track_elem.object_id}')
        # Stop command
        elif isinstance(track_elem, StopCommand):
            logging.info(f'Stop tracking object {track_elem.object_id}')


# pylint: disable=unused-argument
async def send_to_orchestrator(ws_client, frame_obj, detected_boxes, tracked_boxes):
    """Sends the bounding boxes to the orchestrator using a websocket client

    Args:
        ws_client (WebsocketClient): Websocket object that contains the connection
        frame_obj (FrameObj): Frame object on which drawing takes place
        detected_boxes (BoundingBoxes): Boxes generated by the detection
        tracked_boxes (BoundingBoxes): Boxes generated by the tracking
    """
    # Get message and send it through the websocket
    client_message = text.bounding_boxes_to_json(tracked_boxes, frame_obj.get_timestamp())
    ws_client.write_message(client_message)
    logging.info(client_message)

    # Give control to asyncio to work through queue
    await asyncio.sleep(0)


# pylint: disable=unused-argument
async def opencv_display(frame_obj, detected_boxes, tracked_boxes):
    """Displays frame in tiled mode

    Is async because the process_frames.py loop expects to get a async function it can await

    Args:
        frame_obj (FrameObj): Frame object on which drawing takes place
        detected_boxes (BoundingBoxes): Boxes generated by the detection
        tracked_boxes (BoundingBoxes): Boxes generated by the tracking
    """
    # Generate tiled image to display in opencv
    tiled_image = display.generate_tiled_image(frame_obj, detected_boxes, tracked_boxes)

    # Play the video in a window called "Output Video"
    try:
        cv2.imshow("Output Video", tiled_image)
    except OSError as err:
        # Figure out how to get Docker to use GUI
        raise OSError("Error displaying video. Are you running this in Docker perhaps?") \
            from err

    # This next line is **ESSENTIAL** for the video to actually play
    # A timeout of 0 will not display the image
    if cv2.waitKey(1) & 0xFF == ord('q'):
        sys.exit()
