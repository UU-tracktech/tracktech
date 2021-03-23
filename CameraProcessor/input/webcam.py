import cv2
import logging
from input.custom_capture import ICapture


class CamCapture(ICapture):
    # Default init is public HLS stream
    def __init__(self):
        logging.info('connecting to webcam')
        self.cap = cv2.VideoCapture(0)

    # Sees whether stream has stopped
    def stopped(self):
        return not self.cap.isOpened()

    # When everything is done release the capture
    def close(self):
        self.cap.release()

    # Gets the next frame from the stream
    def get_next_frame(self):
        return self.cap.read()
