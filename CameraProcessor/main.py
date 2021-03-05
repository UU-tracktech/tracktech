import cv2
from detection.dectection_obj import DetectionObj

hls_url = "http://81.83.10.9:8001/mjpg/video.mjpg"

cap = cv2.VideoCapture(hls_url)

frame_nr = 0
while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("frame read failed")
        break

    # Create detectionObj
    detection_obj = DetectionObj(None, frame, frame_nr)
    # Run detection on object

    # Visualise rectangles and show it
    detection_obj.draw_rectangles()
    cv2.imshow('Frame', detection_obj.frame)

    # Close loop when q is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done release the capture
cap.release()
cv2.destroyAllWindows()
