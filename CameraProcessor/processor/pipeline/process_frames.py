"""Contains main video processing pipeline function

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import logging
import asyncio
import cv2

from processor.pipeline.framebuffer import FrameBuffer
from processor.webhosting.start_command import StartCommand
from processor.webhosting.stop_command import StopCommand
import processor.utils.draw as draw
import processor.utils.convert as convert
import processor.utils.text as text


async def process_stream(capture, detector, tracker, ws_client=None):
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

        # Buffer the tracked object
        framebuffer.add(convert.to_buffer_dict(frame_obj, tracked_boxes))
        framebuffer.clean_up()

        # Write to client if client is used (should only be done when vid_stream is HlsCapture)
        if ws_client:
            # Mock functionality to start/stop tracking
            while len(ws_client.message_queue) > 0:
                logging.info(ws_client.message_queue)
                track_elem = ws_client.message_queue.popleft()
                if isinstance(track_elem, StartCommand):
                    logging.info(f'Start tracking box {track_elem.box_id} in frame_id {track_elem.frame_id} '
                                 f'with new object id {track_elem.object_id}')
                elif isinstance(track_elem, StopCommand):
                    logging.info(f'Stop tracking object {track_elem.object_id}')

            client_message = text.bounding_boxes_to_json(tracked_boxes, frame_obj.get_timestamp())
            ws_client.write_message(client_message)
            logging.info(client_message)
        else:
            # Copy frame to draw over.
            frame_copy = frame_obj.get_frame().copy()

            # Draw bounding boxes with ID
            draw.draw_tracking_boxes(frame_copy, tracked_boxes.get_bounding_boxes())

            # Play the video in a window called "Output Video"
            try:
                cv2.imshow("Output Video", frame_copy)
            except OSError as err:
                # Figure out how to get Docker to use GUI
                raise OSError("Error displaying video. Are you running this in Docker perhaps?")\
                    from err

            # This next line is **ESSENTIAL** for the video to actually play
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return

        frame_nr += 1
        await asyncio.sleep(0)

    logging.info(f'capture object stopped after {frame_nr} frames')
