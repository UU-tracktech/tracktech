"""Contains main video processing pipeline function.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import sys
import logging
import asyncio
import cv2

import processor.utils.text as text
import processor.utils.display as display

from processor.pipeline.framebuffer import FrameBuffer

from processor.pipeline.reidentification.reid_data import ReidData

from processor.webhosting.start_command import StartCommand
from processor.webhosting.stop_command import StopCommand
from processor.webhosting.update_command import UpdateCommand

# from processor.pipeline.prepare_pipeline import prepare_scheduler.
# from processor.scheduling.plan.pipeline_plan import plan_globals.


async def process_stream(capture, detector, tracker, re_identifier, on_processed_frame, ws_client=None):
    """Processes a stream of frames, outputs to frame or sends to client.

    Outputs to frame using OpenCV if not client is used.
    Sends detections to client if client is used (HlsCapture).

    Args:
        capture (ICapture): capture object to process a stream of frames.
        detector (IDetector): detector performing the detections on a given frame.
        tracker (ITracker): tracker performing simple tracking of all objects using the detections.
        re_identifier (IReIdentifier): re-identifier extracting features and comparing them.
        on_processed_frame (Function): when the frame got processed. Call this function to handle effects.
        ws_client (WebsocketClient): The websocket client so the message queue can be emptied.
    """
    # Create Scheduler by doing the following.
    # scheduler = prepare_scheduler(detector, tracker, re_identifier, on_processed_frame).

    framebuffer = FrameBuffer(300)

    frame_nr = 0

    # Contains re-identification data.
    re_id_data = ReidData()

    while capture.opened():
        ret, frame_obj = capture.get_next_frame()

        if not ret:
            continue

        # Enforce keys of used plan globals.
        # globals_readonly = plan_globals.
        # globals_readonly['frame_obj'] = frame_obj.
        # globals_readonly['re_id_data'] = re_id_data.

        # Execute scheduler plan on current frame.
        # scheduler.schedule_graph([], globals_readonly).

        # Get detections from running detection stage.
        detected_boxes = detector.detect(frame_obj)

        # Get objects tracked in current frame from tracking stage.
        tracked_boxes = tracker.track(frame_obj, detected_boxes, re_id_data)

        # Get objects where re-id is performed on the tracked objects.
        re_id_tracked_boxes = re_identifier.re_identify(frame_obj, tracked_boxes, re_id_data)

        # Buffer the tracked object.
        framebuffer.add_frame(frame_obj, re_id_tracked_boxes)

        # Handle side effects of frame processing.
        on_processed_frame(frame_obj, detected_boxes, tracked_boxes, re_id_tracked_boxes)

        # Process the message queue if there is a websocket connection.
        if ws_client is not None:
            process_message_queue(ws_client, framebuffer, re_identifier, re_id_data)

        frame_nr += 1

        await asyncio.sleep(0)

    logging.info(f'capture object stopped after {frame_nr} frames')


def process_message_queue(ws_client, framebuffer, re_identifier, re_id_data):
    """Processes the message queue processing each start and stop command.

    Args:
        ws_client (WebsocketClient): Websocket client to get the message queue from
        framebuffer (FrameBuffer): Frame buffer containing previous frames and bounding boxes
        re_identifier (IReIdentifier): re-identifier extracting features and comparing them
        re_id_data (ReidData): Object containing data necessary for re-identification
    """
    # Empty queue if there are messages left that were not sent.
    while len(ws_client.message_queue) > 0:
        logging.info(ws_client.message_queue)
        track_elem = ws_client.message_queue.popleft()
        # Start command.
        if isinstance(track_elem, StartCommand):
            logging.info(f'Start tracking box {track_elem.box_id} in frame_id {track_elem.frame_id} '
                         f'with new object id {track_elem.object_id}')

            # Get the feature vector of the object we want to track (query).
            # First, get the bounding box and frame for the query.
            stored_frame = framebuffer.get_frame(track_elem.frame_id)
            stored_box = framebuffer.get_box(track_elem.frame_id, track_elem.box_id)
            feature_map = re_identifier.extract_features(stored_frame, stored_box)

            # Send the feature_map to the orchestrator.
            send_feature_map_to_orchestrator(ws_client, feature_map, track_elem.object_id)

            # Extract the features from this bounding box and store them in the data.
            re_id_data.add_query_feature(track_elem.object_id, feature_map)

            # Also store the map of the first box_id to the object_id.
            re_id_data.add_query_box(track_elem.box_id, track_elem.object_id)

        # Stop command.
        elif isinstance(track_elem, StopCommand):
            logging.info(f'Stop tracking object {track_elem.object_id}')
            re_id_data.remove_query(track_elem.object_id)

        # Update command.
        elif isinstance(track_elem, UpdateCommand):
            logging.info(f'Updating object {track_elem.object_id} with feature map {track_elem.feature_map}')
            re_id_data.add_query_feature(track_elem.object_id, track_elem.feature_map)


# pylint: disable=unused-argument
def send_boxes_to_orchestrator(ws_client, frame_obj, detected_boxes, tracked_boxes, re_id_tracked_boxes):
    """Sends the bounding boxes to the orchestrator using a websocket client.

    Args:
        ws_client (WebsocketClient): Websocket object that contains the connection.
        frame_obj (FrameObj): Frame object on which drawing takes place.
        detected_boxes (BoundingBoxes): Boxes generated by the detection.
        tracked_boxes (BoundingBoxes): Boxes generated by the tracking.
        re_id_tracked_boxes (BoundingBoxes): Boxes where re-id is performed after tracking.
    """
    # Get message and send it through the websocket.
    client_message = text.bounding_boxes_to_json(tracked_boxes, frame_obj.timestamp)
    ws_client.write_message(client_message)
    logging.info(client_message)


def send_feature_map_to_orchestrator(ws_client, feature_map, object_id):
    """Sends the feature map to the orchestrator using a Websocket client.

    Args:
        ws_client (WebsocketClient): Websocket object that contains the connection.
        feature_map ([Float]): Array of float representing the feature_map.
        object_id (Int): The ID of the object the feature_map refers to.
    """
    client_message = text.feature_map_to_json(feature_map, object_id)
    ws_client.write_message(client_message)
    logging.info(client_message)


# pylint: disable=unused-argument.
def opencv_display(frame_obj, detected_boxes, tracked_boxes, re_id_tracked_boxes):
    """Displays frame in tiled mode.

    Args:
        frame_obj (FrameObj): Frame object on which drawing takes place.
        detected_boxes (BoundingBoxes): Boxes generated by the detection.
        tracked_boxes (BoundingBoxes): Boxes generated by the tracking.
        re_id_tracked_boxes (BoundingBoxes): Boxes where re-id is performed after tracking.
    """
    # Generate tiled image to display in opencv.
    tiled_image = display.generate_tiled_image(frame_obj, detected_boxes, tracked_boxes, re_id_tracked_boxes)

    # Play the video in a window called "Output Video".
    try:
        cv2.imshow("Output Video", tiled_image)
    except OSError as err:
        # Figure out how to get Docker to use GUI.
        raise OSError("Error displaying video. Are you running this in Docker perhaps?") \
            from err

    # This next line is **ESSENTIAL** for the video to actually play.
    # A timeout of 0 will not display the image.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        sys.exit()
