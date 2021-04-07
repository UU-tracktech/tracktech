import logging
import asyncio
import cv2
# pylint: disable=unused-import
import src.websocket_client as client
from src.pipeline.detection.detection_obj import DetectionObj
from src.pipeline.detection.yolov5_runner import Detector
from src.input.hls_capture import HlsCapture
# pylint: enable=unused-import

async def process_stream(capture, det_obj, detector, ws_client=None):
    """Processes a stream of frames, outputs to frame or sends to client.

    Outputs to frame using OpenCV if not client is used.
    Sends detections to client if client is used (HlsCapture).

    Args:
        capture (ICapture): capture object to process a stream of frames.
        det_obj (DetectionObj): detection object containing all information about detections
        in the current frame.
        detector (Detector): Yolov5 detector performing the detection using det_obj.
    """
    frame_nr = 0

    while capture.opened():
        # Set the detected bounding box list to empty
        det_obj.bounding_boxes = []
        ret, frame, timestamp = capture.get_next_frame()

        if not ret:
            continue

        # update frame, frame number, and time
        det_obj.frame = frame
        det_obj.frame_nr = frame_nr
        det_obj.timestamp = timestamp

        detector.detect(det_obj)

        # Write to client if client is used (should only be done when vid_stream is HlsCapture)
        if ws_client is not None:
            ws_client.write_message(det_obj.to_json())
            logging.info(det_obj.to_json())
        else:
            # Draw the frame with bounding boxes
            det_obj.draw_rectangles()

            # Play the video in a window called "Output Video"
            try:
                cv2.imshow("Output Video", det_obj.frame)
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
