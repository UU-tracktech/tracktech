import cv2
import logging
from input.icapture import ICapture


class HlsCapture(ICapture):
    # Default init is public HLS stream
    def __init__(self, hls_url='http://81.83.10.9:8001/mjpg/video.mjpg'):
        logging.info('connecting to HLS stream')
        self.cap = cv2.VideoCapture(hls_url)
        logging.info('opened HLS stream')

    # Sees whether stream has stopped
    def opened(self):
        return self.cap.isOpened()

    # When everything is done release the capture
    def close(self):
        self.cap.release()

    # Gets the next frame from the stream
    def get_next_frame(self):
        return self.cap.read()
