"""Contains main video processing pipeline function

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import logging
import asyncio
import cv2

from processor.pipeline.framebuffer import FrameBuffer
from processor.input.hls_capture import HlsCapture
# pylint: enable=unused-import


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
        ret, frame, timestamp = capture.get_next_frame()

        if not ret:
            if frame_nr == capture.get_capture_length():
                logging.info("End of file reached")
                break
            continue

        # Create detection object for this frame.
        det_obj = DetectionObj(timestamp, frame, frame_nr)

        detector.detect(det_obj)

        # Get objects tracked in current frame from tracking stage.
        track_obj = tracker.track(frame_obj, det_obj)

        # Buffer the tracked object
        framebuffer.add(convert.to_buffer_dict(frame_obj, track_obj))
        framebuffer.clean_up()

        # Write to client if client is used (should only be done when vid_stream is HlsCapture)
        if ws_client:
            ws_client.write_message(track_obj.to_json())
            logging.info(track_obj.to_json())
        else:
            # Copy frame to draw over.
            frame_copy = frame_obj.get_frame().copy()

            # Draw bounding boxes with ID
            draw.draw_tracking_boxes(frame_copy, track_obj.get_bounding_boxes())

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
