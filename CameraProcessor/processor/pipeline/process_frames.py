"""Contains main video processing pipeline function.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import logging
import asyncio

from processor.pipeline.frame_buffer import FrameBuffer

from processor.pipeline.reidentification.reid_data import ReidData

from processor.websocket.start_message import StartMessage
from processor.websocket.stop_message import StopMessage
from processor.websocket.update_message import UpdateMessage

from processor.pipeline.prepare_pipeline import prepare_scheduler
from processor.scheduling.plan.pipeline_plan import plan_globals


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
    # Frame buffer that stores 150 frames (flushes older frames if new frames are added over the limit.
    frame_buffer = FrameBuffer(150)

    frame_nr = 0

    # Contains re-identification data.
    re_id_data = ReidData()

    while capture.opened():
        ret, frame_obj = capture.get_next_frame()

        if not ret:
            continue

        # Get detections from running detection stage.
        detected_boxes = detector.detect(frame_obj)

        # Get objects tracked in the current frame from tracking stage.
        tracked_boxes = tracker.track(frame_obj, detected_boxes, re_id_data)

        # Get objects where re-id is performed on the tracked objects.
        re_id_tracked_boxes = re_identifier.re_identify(frame_obj, tracked_boxes, re_id_data)

        # Buffer the tracked object.
        frame_buffer.add_frame(frame_obj, re_id_tracked_boxes)

        # Handle side effects of frame processing.
        on_processed_frame(frame_obj, detected_boxes, tracked_boxes, re_id_tracked_boxes)

        # Process the message queue if there is a websocket connection.
        if ws_client is not None:
            process_message_queue(ws_client, frame_buffer, re_identifier, re_id_data)

        frame_nr += 1

        await asyncio.sleep(0)

    logging.info(f'capture object stopped after {frame_nr} frames')


async def process_stream_scheduler(capture, detector, tracker, re_identifier, on_processed_frame, ws_client=None):
    """Processes a stream of frames using the scheduler, outputs to frame or sends to client.

    Outputs to frame using OpenCV if not client is used.
    Sends detections to client if client is used (HlsCapture).

    The scheduler is used to run the pipeline. Initial configuration is done to initialize the nodes.
    Each iteration all global variables (parameters of schedule node components which are readonly, shouldn't change
    during the loop). The objects called upon by the client are modified by reference thus no return is needed.

    Args:
        capture (ICapture): capture object to process a stream of frames.
        detector (IDetector): detector performing the detections on a given frame.
        tracker (ITracker): tracker performing simple tracking of all objects using the detections.
        re_identifier (IReIdentifier): re-identifier extracting features and comparing them.
        on_processed_frame (Function): when the frame got processed. Call this function to handle effects.
        ws_client (WebsocketClient): The websocket client so the message queue can be emptied.
    """
    # Frame buffer that stores 150 frames (flushes older frames if new frames are added over the limit.
    frame_buffer = FrameBuffer(150)

    # Create Scheduler by passing all information to construct the schedule nodes and its components.
    scheduler = prepare_scheduler(detector, tracker, re_identifier, on_processed_frame, frame_buffer)

    frame_nr = 0

    # Contains re-identification data.
    re_id_data = ReidData()

    while capture.opened():
        ret, frame_obj = capture.get_next_frame()

        if not ret:
            continue

        # Enforce keys of used plan globals.
        globals_readonly = plan_globals
        globals_readonly['frame_obj'] = frame_obj
        globals_readonly['re_id_data'] = re_id_data

        # Execute scheduler plan on current frame.
        scheduler.schedule_graph([], globals_readonly)

        # Process the message queue if there is a websocket connection.
        if ws_client is not None:
            process_message_queue(ws_client, frame_buffer, re_identifier, re_id_data)

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
        if isinstance(track_elem, StartMessage):
            try:
                feature_map = re_identifier.extract_features_from_image(track_elem.get_cutout(framebuffer))

                # Sends the feature map to the orchestrator using a Websocket client.
                ws_client.send_message(UpdateMessage(track_elem.object_id, feature_map))

                # Extract the features from this bounding box and store them in the data.
                re_id_data.add_query_feature(track_elem.object_id, feature_map)

                # Also store the map of the first box_id to the object_id, if we have a box ID.
                if track_elem.box_id is not None:
                    re_id_data.add_query_box(track_elem.box_id, track_elem.object_id)

            # If the image could not be found, an error is raised.
            except IndexError as index_err:
                logging.error(index_err)
            except ValueError as value_err:
                logging.error(value_err)

        # Stop command.
        elif isinstance(track_elem, StopMessage):
            logging.info(f'Stop tracking object {track_elem.object_id}')
            re_id_data.remove_query(track_elem.object_id)

        # Update command.
        elif isinstance(track_elem, UpdateMessage):
            logging.info(f'Updating object {track_elem.object_id} with feature map {track_elem.feature_map}')
            re_id_data.add_query_feature(track_elem.object_id, track_elem.feature_map)
