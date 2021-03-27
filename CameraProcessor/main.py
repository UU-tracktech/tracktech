import cv2
import logging
import sys
from detection.detection_obj import DetectionObj
from input.hls_capture import HlsCapture

logging.basicConfig(filename='app.log', filemode='w',
                    format='%(asctime)s %(levelname)s %(name)s - %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

frame_nr = 0
capture = HlsCapture()


while capture.opened():
    ret, frame = capture.get_next_frame()

    if not ret:
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
