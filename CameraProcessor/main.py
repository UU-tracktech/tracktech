import cv2
import logging
from detection.dectection_obj import DetectionObj
from input.hls_stream import HLSCapture

frame_nr = 0
capture = HLSCapture()


while not capture.stopped():
    frame = capture.get_next_frame()

    if not frame:
        logging.warning('capture object frame missed')
        continue

    frame_nr += 1

    # Create detectionObj
    detection_obj = DetectionObj(None, frame, capture)
    # Run detection on object

    # Visualise rectangles and show it
    detection_obj.draw_rectangles()
    cv2.imshow('Frame', detection_obj.frame)

    # Close loop when q is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.close()
cv2.destroyAllWindows()
logging.info(f'capture object stopped after {frame_nr} frames')
